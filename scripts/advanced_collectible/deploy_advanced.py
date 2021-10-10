# deploy contract to Rinkeby TestNet

from brownie import AdvancedCollectible, accounts, network, config
from scripts.helpful_scripts import fund_advance_collectible


def main():
    dev = accounts.add(config["wallets"]["from_key"])# metamask address
    print(dev)
    
    publish_source = False
    advanced_collectible = AdvancedCollectible.deploy(
        config["networks"][network.show_active()]["vrf_coordinator"],
        config["networks"][network.show_active()]["link_token"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": dev},
        publish_source=publish_source,
    )

    fund_advance_collectible(advanced_collectible) # second transaction funding
    return advanced_collectible
