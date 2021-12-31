// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VotingHub {
    mapping(string => address) public addressesOfVotingSessions;

    function createVotingSession(
        string memory symbol,
        uint256 start,
        uint256 end,
        uint8 numOfVotes
    ) public {}
}
