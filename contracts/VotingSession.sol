// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

import "./VotingHub.sol";

contract VotingSession is Ownable {
    string public symbol;
    uint256 public start;
    uint256 public end;
    uint8 public numOfVotes;

    string[] public choices;
    mapping(string => uint24) public numOfVotesPerChoice;

    VotingHub private votingHub;
    IERC20 private voteToken;

    constructor(
        string memory _symbol,
        uint256 _start,
        uint256 _end,
        uint8 _numOfVotes,
        address _voteToken,
        address _votingHub
    ) {
        symbol = _symbol;
        start = _start;
        end = _end;
        numOfVotes = _numOfVotes;
        voteToken = IERC20(_voteToken);
        votingHub = VotingHub(_votingHub);
    }

    function vote(string memory choice, uint8 numberOfVotes) public {}

    function becomeVoter() public {}

    function getResults() public {}
}
