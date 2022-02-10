# /scripts/deploy.py
#
# Python script to deploy Simple Storage.
# @ author: Anton Sirgue
# @ version: 22/01/2022

from brownie import accounts, config, SimpleStorage, network


def deploySimpleStorage():
    #Deployment:
    account = get_account()
    simple_storage = SimpleStorage.deploy({"from": account})
    # Transact
    # Call
    stored_value = simple_storage.retrieve()
    print(stored_value)

    # Transaction
    transaction = simple_storage.store(15, {"from": account})
    transaction.wait(1)
    # Check if it worked
    updated_stored_value = simple_storage.retrieve()
    print(updated_stored_value)


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    deploySimpleStorage()
