// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

import "./VotingHub.sol";

contract VotingSession is Ownable {
    string public symbol;
    uint256 public start;
    uint256 public end;

    uint8 public numOfVotesPerUser;
    mapping(address => uint8) public votesPerUser;

    string[] public choices;
    // more efficient than array, when looking if it contains certain keys
    mapping(string => bool) public choicesMap;
    mapping(string => uint24) public votesPerChoice;

    constructor(
        string memory _symbol,
        uint256 _start,
        uint256 _end,
        uint8 _numOfVotesPerUser
    ) {
        require(
            _numOfVotesPerUser > 0,
            "Number of votes per user must be greater than 0."
        );

        symbol = _symbol;
        start = _start;
        end = _end;
        numOfVotesPerUser = _numOfVotesPerUser;
    }

    function vote(string memory choice, uint8 numberOfVotes) public {
        require(choicesMap[choice], "Invalid choice.");
        require(
            votesPerUser[msg.sender] + numberOfVotes <= numOfVotesPerUser,
            "Exceeded number of votes per user."
        );

        votesPerUser[msg.sender] += numberOfVotes;
        votesPerChoice[choice] += numberOfVotes;
    }

    function addChoice(string memory choice) public onlyOwner {
        require(block.timestamp < end, "This voting session already ended.");

        choices.push(choice);
        choicesMap[choice] = true;
    }

    function getResults() public {}
}
