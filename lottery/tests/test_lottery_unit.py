# /tests/test_lottery_unit.py
#
# Python script to conduct unit testing on our Lottery contract.
# Note: in-function comments are here for learning purposes.
# @ author: Anton Sirgue
# @ version: 22/01/2022

from brownie import Lottery, accounts, config, network, exceptions
from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    fund_with_link,
    get_contract,
)
from web3 import Web3
import pytest


# Testing contract's ability to set the correct entry fee to the lottery
def test_get_entrance_fee():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    lottery = deploy_lottery()
    # Act
    expected_entrance_fee = Web3.toWei(
        50 / 2000, "ether"
    )  # we set the ETH price to 2000 here bcs we are working with our mock contracts and it is the initial value we set
    entrance_fee = lottery.getEntranceFee()
    # Assert
    assert expected_entrance_fee == entrance_fee


# Testing the contract's ability to block entries to the lottery until it has been opened by administrator
def test_cant_enter_until_started():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    lottery = deploy_lottery()
    # Act / Assert
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from": get_account(), "value": lottery.getEntranceFee()})


# Testing the contract's ability to start the lottery and to let people enter it
def test_can_start_and_enter():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    lottery = deploy_lottery()
    account = get_account()
    # Act
    tx1 = lottery.startLottery({"from": account})
    tx1.wait(1)
    tx2 = lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    tx2.wait(1)
    # Assert
    assert lottery.players(0) == account


# Teting the contract's ability to close the lottery
def test_can_end_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    lottery = deploy_lottery()
    account = get_account()
    # Act
    tx1 = lottery.startLottery({"from": account})
    tx1.wait(1)
    tx2 = lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    tx2.wait(1)
    fund_with_link(lottery)
    tx3 = lottery.endLottery({"from": account})
    tx3.wait(1)
    # Asssert
    assert lottery.lottery_state() == 2


# Testing the contract's ability to correctly pick a winner, reset balance to 0, and transfer all funds to the winner's account
def test_can_pick_winner_correctly():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    lottery = deploy_lottery()
    account = get_account()
    # Act
    tx1 = lottery.startLottery({"from": account})
    tx1.wait(1)
    tx2 = lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    tx2.wait(1)
    tx3 = lottery.enter(
        {"from": get_account(index=1), "value": lottery.getEntranceFee()}
    )
    tx3.wait(1)
    tx4 = lottery.enter(
        {"from": get_account(index=2), "value": lottery.getEntranceFee()}
    )
    tx4.wait(1)
    fund_with_link(lottery)
    transaction = lottery.endLottery({"from": account})
    request_id = transaction.events["requestedRandomness"]["requestId"]
    # Now, we fake gettting a random nb from the chainlink node to check the handling of randomness by our contract
    STATIC_RNG = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        request_id, STATIC_RNG, lottery.address, {"from": account}
    )

    starting_balance_of_account = account.balance()
    balance_of_lottery = lottery.balance()
    # Now, we check if, with this 777 number, our contract gets the correct winner
    assert lottery.recentWinner() == account
    # We need to assert that the balance has been emptied ...
    assert lottery.balance() == 0
    # ... and that the money has been transferred to the winner
    assert account.balance() == starting_balance_of_account + balance_of_lottery
