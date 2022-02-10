from brownie import MockV3Aggregator, FundMe, network, config
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_fund_me():
    account = get_account()
    # We need to pass the price feed address to our fundme contract

    # If we are on a persistent network, use the associated address
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]  # it will grab the price feed address corresponding to the correct network defined in the config file

    # Otherwise, deploy mocks
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )  # publish_source = True will verify our contract using ethercan, the code will then be visible on etherscan and the contract verified
    print(f"Contract deployed to {fund_me.address}")

    return fund_me  # so that our test can have access to the contract deployed to work with it


def main():
    deploy_fund_me()
