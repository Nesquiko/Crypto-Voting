// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

import "./VotingSession.sol";

contract VotingHub {
    string[] public votingSessionSymbols;
    mapping(string => address) public addressesOfVotingSessions;

    function createVotingSession(
        string memory symbol,
        uint256 start,
        uint256 end,
        uint8 numOfVotes
    ) public returns (address) {
        require(
            addressesOfVotingSessions[symbol] == address(0),
            "Voting session with this symbol already exists."
        );

        VotingSession newVotingSession = new VotingSession(
            symbol,
            start,
            end,
            numOfVotes
        );

        newVotingSession.transferOwnership(msg.sender);

        votingSessionSymbols.push(symbol);
        addressesOfVotingSessions[symbol] = address(newVotingSession);

        return address(newVotingSession);
    }

    function getAllVotinSessionsSymbols()
        public
        view
        returns (string[] memory)
    {
        return votingSessionSymbols;
    }
}
