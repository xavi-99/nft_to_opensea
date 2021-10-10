from brownie import AdvancedCollectible, accounts, config, interface, network

def get_breed(breed_number):
    switch = {0: 'RANGER_BLACK', 1: 'RANGER_RED', 2:'RANGER_WHITE'}
    return switch[breed_number]

      

def fund_advance_collectible(nft_contract):
    dev = accounts.add(config["wallets"]["from_key"])
    link_token = interface.LinkTokenInterface(
        config["networks"][network.show_active()]["link_token"]
    )
    link_token.transfer(nft_contract, 1000000000000000000, {"from": dev})
    