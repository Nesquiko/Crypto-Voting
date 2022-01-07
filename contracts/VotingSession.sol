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

    function getNumOfVotesForUser() public view returns (uint8) {
        return votesPerUser[msg.sender];
    }

    function vote(string memory choice, uint8 numberOfVotes) public {
        require(block.timestamp < end, "This voting session already ended.");
        require(
            block.timestamp >= start,
            "This voting session did not start yet."
        );
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
        require(
            block.timestamp < start,
            "This voting session already started."
        );
        choices.push(choice);
        choicesMap[choice] = true;
    }

    function getAllChoices() public view returns (string[] memory) {
        return choices;
    }

    function getResults() public view returns (string memory) {
        string memory results = "";
        for (uint256 i = 0; i < choices.length; i++) {
            results = append(
                results,
                choices[i],
                " => ",
                uint2str(votesPerChoice[choices[i]]),
                "\n"
            );
        }

        return results;
    }

    function append(
        string memory a,
        string memory b,
        string memory c,
        string memory d,
        string memory e
    ) internal pure returns (string memory) {
        return string(abi.encodePacked(a, b, c, d, e));
    }

    function uint2str(uint256 _i)
        internal
        pure
        returns (string memory _uintAsString)
    {
        if (_i == 0) {
            return "0";
        }
        uint256 j = _i;
        uint256 len;
        while (j != 0) {
            len++;
            j /= 10;
        }
        bytes memory bstr = new bytes(len);
        uint256 k = len;
        while (_i != 0) {
            k = k - 1;
            uint8 temp = (48 + uint8(_i - (_i / 10) * 10));
            bytes1 b1 = bytes1(temp);
            bstr[k] = b1;
            _i /= 10;
        }
        return string(bstr);
    }
}
