# /scripts/fund_and_withdraw.py
#
# Interracting with our smart contract, we can fund it and thenm withdraw the funds (as we are the owner of this contract).
# @ author: Anton Sirgue
# @ version: 22/01/2022

from brownie import FundMe
from scripts.helpful_scripts import get_account


def fund():
    fund_me = FundMe[-1]
    account = get_account()

    entrance_fee = fund_me.getEntranceFee()
    print(f"Entrance fee : {entrance_fee}")

    print("Funding")
    fund_me.fund({"from": account, "value": entrance_fee})


def withdraw():
    fund_me = FundMe[-1]
    account = get_account()

    fund_me.withdraw({"from": account})


def main():
    fund()
    withdraw()
