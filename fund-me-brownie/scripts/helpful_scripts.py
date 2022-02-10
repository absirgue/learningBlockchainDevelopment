from brownie import network, config, accounts, MockV3Aggregator

# from web3 import Web3 this was to convert proprely 2000 ether to Wei but we don't do it anymore bcs of the way opur contract is set up, we need to mimick it with out mock

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = [
    "development",
    "ganache-local",
    "ganache-local-2",
    "ganache-local-3",
]

DECIMALS = 8
STARTING_PRICE = 200000000000


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    # there is no price feed on development chains as they are 'new' so we will fake it by deploying our own price feed contract
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks ...")

    # We deploy only if no Mock is already deployed (MockV3Aggregator is a list of all the MockV3Aggregator contractsd we deployed)
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(
            DECIMALS, STARTING_PRICE, {"from": get_account()}
        )  # the arguments requested by the mock aggregator contract constructor and our account since we are deploying a contract

    print("Mock deployed !")
