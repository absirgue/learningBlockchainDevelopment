# /scripts/deploy_lottery.py
#
# Interracting with out contract thanks to brownie.
# @ author: Anton Sirgue
# @ version: 22/01/2022

from brownie import SimpleStorage, accounts, config

def read_contract():
    simple_contract = SimpleStorage[-1]

    print(simple_storage.retrieve())

def main():
    read_contract()