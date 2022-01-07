# Crypto-Voting

Crypto Voting is a decentralized application for a setting up a vote on a topic.
Implemented on the Ethereum Rinkeby Test Network.

## Disclaimer

<strong>Use at your own risk!</strong>

Crypto Voting is only a project created for learning more about smart contracts
and Ethereum blockchain. It is not audited nor any professional blockchain
developer approved it.

## How to

The website for interacting with this dapp is on hosted by Github pages, and you
can visit by clicking [here](https://nesquiko.github.io/crypto-voting-website/).
Also you can find the source for the website [here](https://github.com/Nesquiko/crypto-voting-website/tree/main).

## How it works

1. User enters info for the creation of a new VotingSession:
    - Symbol - a characteristic name for the new VotingSession
    - Start date - a unix timestamp when users can start voting in the new VotingSession
    - End date - a unix timestamp when users can no longer vote in this VotingSession
    - Number of votes per user - how many votes can user cast on choices in the VotingSession
2. VotingHub smart contract creates a new VotingSession and sets an owner of it to the user, who requested it.
3. Only user can now add new choices to this VotingSession. However, all choices must be added before the start date.
4. Other users can vote on any choice in the VotinSession. All votes can be casted after the start date and before the end date. Also individual users cannot exceed the Number of votes per user.

## Problems

-   Ideally voting should be free in my opinion
-   Max number of votes per choice is 2^24 - 1 = 16777215
-   Max number of votes per user is 2^8 - 1 = 255
