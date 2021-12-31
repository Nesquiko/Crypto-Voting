// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract VoteToken is ERC20 {
    // initialSupply in wei
    constructor() public ERC20("VoteToken", "VT") {}
}
