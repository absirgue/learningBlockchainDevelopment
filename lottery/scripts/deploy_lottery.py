# /scripts/deploy_lottery.py
#
# Python script to deploy, start, and end the lottery.
# Note: in-function comments are here for learning purposes.
# @ author: Anton Sirgue
# @ version: 22/01/2022

from scripts.helpful_scripts import get_account, get_contract, fund_with_link
from brownie import Lottery, config, network

# Deploys the Lottery contract.
def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get(
            "verify", False
        ),  # .get() allows to set a default so that is still work if we don't define it
    )

    print("Deployed lottery !")
    return lottery


# Starts the lottery,
def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({"from": account})
    starting_tx.wait(1)
    print("*********")
    print("Lottery started !")
    print("*********")


# Enters the lottery.
def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 100000000
    tx = lottery.enter({"from": account, "value": value})
    tx.wait(1)
    print("You entered the lottery !")


# Ends the lottery and picks a winner.
def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    # We need to fund the contract as endLottery calls the reandomness function that requires some LINK token
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    ending_tx = lottery.endLottery({"from": account})
    ending_tx.wait(1)
    # Waiting for chainlink node to pick a random number so that we can pick the winner
    time.sleep(60)
    print(f"{lottery.recentWinner()} is the new winner !")


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
