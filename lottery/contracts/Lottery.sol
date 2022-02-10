/**
    Smart Contract to implement a lottery's behaviour. The lottery can
    only be opened and closed by an administrator, anyone can enter it
    when it is open at the condition that they fund it with enough ETH
    (50$ worth). When it is closed, the lottery picks a winner at random
    and transfer its balance to the winner's account.
    In-function comments were written for learning purposes.

    @ author: Anton Sirgue
    @version: 22/01/2022
 */

// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract Lottery is VRFConsumerBase, Ownable {
    uint256 public minimumUsd;
    AggregatorV3Interface public priceFeed;
    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }

    // these diff states are represnted by nbs 0-1

    LOTTERY_STATE public lottery_state;
    uint256 public fee;
    bytes32 public keyhash;
    address payable[] public players;
    address payable public recentWinner;
    event requestedRandomness(bytes32 requestId);

    // we 'fit' the constructor for the VRFConsumerBase contract in the constructor of this contract, each parameeter of the constructor of VRFConsumerBase is first passed to our 'normal' constructor
    constructor(
        address _priceFeed,
        address _vrfCoordinator,
        address _link,
        uint256 _fee,
        bytes32 _keyhash
    ) public VRFConsumerBase(_vrfCoordinator, _link) {
        priceFeed = AggregatorV3Interface(_priceFeed);
        minimumUsd = 50 * (10**18);
        lottery_state = LOTTERY_STATE.CLOSED;
        fee = _fee;
        keyhash = _keyhash;
    }

    function enter() public payable {
        require(lottery_state == LOTTERY_STATE.OPEN);
        require(
            getConversionRate(msg.value) >= minimumUsd,
            "You need to spend more ETH!"
        );
        players.push(msg.sender);
    }

    function startLottery() public {
        require(
            lottery_state == LOTTERY_STATE.CLOSED,
            "Can't start a new lottery yet"
        );
        lottery_state = LOTTERY_STATE.OPEN;
    }

    function endLottery() public onlyOwner {
        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;

        // Request random number
        bytes32 requestId = requestRandomness(keyhash, fee); // request and receive mentality: here we call and then the chainlink will 'send' a random number to another function called 'fulfillRandomness'
        emit requestedRandomness(requestId);
    }

    // We make it internal so the Chainlink node is the only one to be able to call it, it calls the VRFConsumerBase than then calls our function. This is essential to protecting from manipulations.
    function fulfillRandomness(bytes32 _requestId, uint256 _randomness)
        internal
        override
    {
        require(
            lottery_state == LOTTERY_STATE.CALCULATING_WINNER,
            "You aren't there yet !"
        );
        require(_randomness > 0, "No random number found.");

        uint256 indexOfWinner = _randomness % players.length;
        recentWinner = players[indexOfWinner];

        // Now we want to pay the winner all the money that accumulated in the lottery
        recentWinner.transfer(address(this).balance);

        // Reset the lottery
        players = new address payable[](0);
        lottery_state = LOTTERY_STATE.CLOSED;
    }

    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer * 10000000000);
    }

    // 1000000000
    function getConversionRate(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 1000000000000000000;
        return ethAmountInUsd;
    }

    function getEntranceFee() public view returns (uint256) {
        // minimumUSD
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        return (minimumUsd * precision) / price;
    }
}
