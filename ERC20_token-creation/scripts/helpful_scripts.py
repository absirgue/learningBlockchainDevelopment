# /scripts/helpful_scripts.py
#
# Scripts like get_account or get_contract that are heavily used in other
# parts of the program. These scripts are heavily reliant on the config file.
# Note: in-function comments are here for learning purposes.
# @ author: Anton Sirgue
# @ version: 22/01/2022

from os import link
from brownie import (
    network,
    config,
    accounts,
    MockV3Aggregator,
    Contract,
    VRFCoordinatorMock,
    LinkToken,
)


FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = [
    "development",
    "ganache-local",
    "ganache-local-2",
    "ganache-local-3",
]
DECIMALS = 8
STARTING_PRICE = 200000000000

# This function allows to return the correct account depending on the network
# we are working with (development, main net fork, test nest, ...).
def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


# This function deploys mock contracts when testing on a development network.
def deploy_mocks(decimals=DECIMALS, initial_value=STARTING_PRICE):
    account = get_account()
    MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print("Deployed!")


# Contract name to type mapping to be used in get_contract().
contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}

# This function will grab the contract addresses from the brownie config
# if defined, otherwise, it will deploy a mock version of that contract,
# and return that mock contract.
# @param contract_name (string)
# @return brownie.network.contract.ProjectContract <- the most recently
# deployed version of the contract we are looking for
def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()

        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


# This function allows to directly fund the contract with LINK token to
# allow it to call Chainlink VRF. Default amount funded is 0.1 LINK.
def fund_with_link(
    contract_address, account=None, link_token=None, amount=100000000000000000
):
    account = (
        account if account else get_account()
    )  # we take the account in parameters if there is one or we get_account
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("Contract funded !")
    return tx
