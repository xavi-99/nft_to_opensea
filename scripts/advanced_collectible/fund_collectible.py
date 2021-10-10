from brownie import AdvancedCollectible
from scripts.helpful_scripts import fund_advance_collectible

def main():
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) -1] # most recent deployment
    fund_advance_collectible(advanced_collectible)

