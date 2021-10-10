from brownie import AdvancedCollectible, network
from metadata import sample_metadata
from scripts.helpful_scripts import get_breed
from pathlib import Path
import os
import requests
import json



def main():
    print("Working on " + network.show_active())
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) - 1]
    number_of_tokens = advanced_collectible.tokenCounter()
    print("The number of tokens you've deployed is {}".format(number_of_tokens))
    write_metadata(number_of_tokens, advanced_collectible)


def write_metadata(number_of_tokens, nft_contract):
    for token_id in range(number_of_tokens):
        collectible_metadata = sample_metadata.metadata_template
        breed = get_breed(nft_contract.tokenIdToBreed(token_id))
        metadata_file_name = "./metadata/{}/{}".format(
            network.show_active(), str(token_id) + "-" + breed + ".json"
        )
        # ./metadata/rinkeby/1-RANGER_BLACK.json
        if Path(metadata_file_name).exists():
            print("{} already found!".format(metadata_file_name))
        else:
            token_breed = get_breed(
                nft_contract.tokenIdToBreed(token_id)
            )
            print("Token breed --> {}".format(token_breed))
            collectible_metadata["name"] = token_breed
            collectible_metadata["description"] = "An awesome {} Ranger!".format(
                collectible_metadata["name"]
            )
            image_to_upload = None
            if os.getenv("UPLOAD_IPFS") == "true":
                print("Image to look on breed --> {}".format(breed))
                image_path = "./img/{}.png".format(breed)
                print("Image Path --> {}".format(image_path))
                image_to_upload = upload_to_ipfs(image_path)
            
            collectible_metadata["image"] = image_to_upload
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            if os.getenv("UPLOAD_IPFS") == "true":
                uri = upload_to_ipfs(metadata_file_name)
                append_metadata_uri_to_json(uri, token_id)



# IPFS API http://127.0.0.1:5001
def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        print("Uploading file to IPFS, filenmae = {}".format(filepath))
        image_binary = fp.read()
        ipfs_url = "http://localhost:5001"
        response = requests.post(ipfs_url + "/api/v0/add", files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        uri = "https://ipfs.io/ipfs/{}?filename={}".format(ipfs_hash, filename)
        print(uri)
    return uri


def append_metadata_uri_to_json(uri, token_id):

    with open("./metadata/{}/urls/urls.json".format(network.show_active()), "r+") as file:
        data = json.load(file)
        new_metadata_json_url = {token_id : uri}
        data.update(new_metadata_json_url)
        file.seek(0)
        json.dump(data, file)

