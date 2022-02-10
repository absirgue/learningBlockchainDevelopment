from brownie import SimpleStorage, accounts, config

def read_contract():
    simple_contract = SimpleStorage[-1]

    print(simple_storage.retrieve())

def main():
    read_contract()