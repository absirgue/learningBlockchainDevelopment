# /tests/test_lottery_intergation.py
#
# Python script to conduct integration testing on our Lottery contract.
# Note: in-function comments are here for learning purposes. Those tests
# are conducted on a live chain, Rinkeby here. Only one test is written
# but all functionalities would have to be tested before a real use.
# @ author: Anton Sirgue
# @ version: 22/01/2022

from brownie import network
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    fund_with_link,
    get_account,
)
from scripts.deploy_lottery import deploy_lottery
import pytest

# Testing the contract's ability to pick a winner on a real chain
def can_pick_winner():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    lottery = deploy_lottery()
    account = get_account()

    lottery.startLottery({"from": account})
    lottery.enter({"value": account, "value": lottery.getEntranceFee()})
    lottery.enter({"value": account, "value": lottery.getEntranceFee()})

    fund_with_link(lottery)

    lottery.endLottery({"from": account})
    time.sleep(60)

    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
