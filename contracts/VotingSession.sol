// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";

// https://jeancvllr.medium.com/solidity-tutorial-all-about-comments-bc31c729975a
// documentation comments
contract VotingSession is Ownable {
    string public symbol;
    uint256 public start;
    uint256 public end;
    uint8 public numOfVotes;
    mapping(string => uint20) public numOfVotes;

    constructor(
        string memory _symbol,
        uint256 _start,
        uint256 _end,
        uint8 _numOfVotes
    ) {
        symbol = _symbol;
        start = _start;
        end = _end;
        numOfVotes = _numOfVotes;
    }
}
