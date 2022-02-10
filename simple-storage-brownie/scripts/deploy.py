from brownie import accounts, config, SimpleStorage, network


def deploySimpleStorage():
    # spinning up a ganache account
    # account = accounts[0]   <-- this works perfectly for spinning it into ganache
    # print account

    # accessing account registered with brownie
    # account = accounts.load("testing-smartDev")
    # print(account)

    # for test nets where private key is an .env variable, it uses the brownioe-config.yaml
    # account = accounts.add(config["wallets"]["from_key"])
    # print(account)

    # our first deployment:
    account = get_account()
    simple_storage = SimpleStorage.deploy({"from": account})
    # Transact
    # Call
    stored_value = simple_storage.retrieve()
    print(stored_value)

    # Transaction
    transaction = simple_storage.store(15, {"from": account})
    transaction.wait(1)
    # check if it worked
    updated_stored_value = simple_storage.retrieve()
    print(updated_stored_value)


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    deploySimpleStorage()
