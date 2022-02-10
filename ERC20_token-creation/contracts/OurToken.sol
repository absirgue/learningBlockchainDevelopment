/**
    Simple ERC20 token based on Open Zeppelin's interface. This has no real use apart from showing 
    that creating a token can be done in only a few lines of code !

    @ author: Anton Sirgue
    @version: 22/01/2022
 */

// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract OurToken is ERC20 {
    constructor(uint256 initialSupply)
        public
        ERC20Detailed("OurToken", "OT", 18)
    {
        _mint(msg.sender, initialSupply);
    }
}
