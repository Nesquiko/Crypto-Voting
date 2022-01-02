// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

import "./VotingSession.sol";
import "./VoteToken.sol";

contract VotingHub {
    string[] public votingSessionSymbols;
    mapping(string => address) public addressesOfVotingSessions;
    IERC20 public voteToken;

    constructor() {
        voteToken = new VoteToken();
    }

    function createVotingSession(
        string memory symbol,
        uint256 start,
        uint256 end,
        uint8 numOfVotes
    ) public {
        VotingSession newVotingSession = new VotingSession(
            symbol,
            start,
            end,
            numOfVotes,
            address(voteToken),
            address(this)
        );

        votingSessionSymbols.push(symbol);
        addressesOfVotingSessions[symbol] = address(newVotingSession);
    }

    function getAllVotinSessionsSymbols()
        public
        view
        returns (string[] memory)
    {
        return votingSessionSymbols;
    }
}
