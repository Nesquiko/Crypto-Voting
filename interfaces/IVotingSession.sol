// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IVotingSession {
    function vote(string memory choice, uint8 numberOfVotes) external;

    function addChoice(string memory choice) external;

    function getResults() external;
}
