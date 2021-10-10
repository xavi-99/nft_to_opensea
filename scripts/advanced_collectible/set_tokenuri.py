from brownie import AdvancedCollectible, network, config, accounts
from scripts.helpful_scripts import get_breed
import json


def main():

    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) - 1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print("Number of token you deployed is {}".format(number_of_advanced_collectibles))

    for token_id in range(number_of_advanced_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        tokenURI = get_metadata_json_url("{}".format(token_id))
        if not advanced_collectible.tokenURI(token_id).startswith("https://"):
            print("Setting tokenURI of {}".format(token_id))
            set_tokenURI(token_id, advanced_collectible, tokenURI)
        else:
            print("Skipping {}, we've already set that TokenURI".format(token_id))
            print("Token URI --> {}".format(advanced_collectible.tokenURI(token_id)))


# set Metadata file URL ( including attributes and img url from IPS) associated to this token ID
def set_tokenURI(token_id, nft_contract, tokenURI):
    dev = accounts.add(config["wallets"]["from_key"])
    nft_contract.setTokenURI(token_id, tokenURI, {"from": dev})
    print(
        "AWESOMe! You can view your NFT here https://testnets.opensea.io/assets/{}/{}".format(
            nft_contract.address, token_id
        )
    )
    print("Wait 20 min and hit refresh metada")


def get_metadata_json_url(token_id):
    with open(
        "./metadata/{}/urls/urls.json".format(network.show_active()), "r"
    ) as jsonFile:
        jsonObject = json.load(jsonFile)
        uri = jsonObject[token_id]
        jsonFile.close()
        return uri
