# /scripts/deploy_token.py
#
# Deploying our Smart Contract to the chain.
# @ author: Anton Sirgue
# @ version: 22/01/2022

from brownie import OurToken
from scripts.helpful_scripts import get_account
from web3 import Web3

# Initial supply is 1000 ETH
initial_supply = Web3.toWei(1000, "ether")

def main():
    account = get_account()
    our_token = OurToken.deploy(initial_supply, {"from": account})
    print(our_token.name())