import time
import brownie
import pytest

from brownie.network.contract import Contract, ProjectContract
from brownie.network.transaction import TransactionReceipt
from brownie import VotingSession, exceptions

from scripts.deploy_voting_hub import deploy_voting_hub
from scripts.util import from_account, get_account


def test_voting_session_creation():
    account = get_account()
    voting_hub: ProjectContract = deploy_voting_hub()

    expected_symbol = "TEST"
    start = int(time.time())
    end = start + 10
    num_votes = 2

    tx: TransactionReceipt = voting_hub.createVotingSession(
        expected_symbol, start, end, num_votes, from_account(account)
    )
    tx.wait(1)

    voting_session = Contract.from_abi(
        "VotingSession", tx.return_value, VotingSession.abi
    )

    assert voting_session.symbol() == expected_symbol
    assert voting_session.start() == start
    assert voting_session.end() == end
    assert voting_session.numOfVotesPerUser() == num_votes


def test_add_choice_from_owner():
    account = get_account()
    voting_hub: ProjectContract = deploy_voting_hub()

    symbol = "Presidential Vote"
    start = int(time.time())
    end = start + 10000000
    num_votes = 2

    tx: TransactionReceipt = voting_hub.createVotingSession(
        symbol, start, end, num_votes, from_account(account)
    )
    tx.wait(1)

    voting_session = Contract.from_abi(
        "VotingSession", tx.return_value, VotingSession.abi
    )

    choice = "Joe Biden"
    tx = voting_session.addChoice(choice, from_account(account))
    tx.wait(1)

    assert voting_session.choices(0, from_account(account)) == choice
    assert voting_session.choicesMap(choice, from_account(account)) == True
    assert voting_session.numOfVotesPerChoice(choice, from_account(account)) == 0


def test_add_choice_from_non_owner():
    account = get_account()
    voting_hub: ProjectContract = deploy_voting_hub()

    symbol = "Presidential Vote"
    start = int(time.time())
    end = start + 10000000
    num_votes = 2

    tx: TransactionReceipt = voting_hub.createVotingSession(
        symbol, start, end, num_votes, from_account(account)
    )
    tx.wait(1)

    voting_session = Contract.from_abi(
        "VotingSession", tx.return_value, VotingSession.abi
    )

    non_owner = get_account(index=1)
    choice = "Joe Biden"

    with pytest.raises(exceptions.VirtualMachineError):
        tx = voting_session.addChoice(choice, from_account(non_owner))


def test_add_choice_after_end():
    account = get_account()
    voting_hub: ProjectContract = deploy_voting_hub()

    symbol = "Presidential Vote"
    start = int(time.time()) - 100
    end = start - 50
    num_votes = 2

    tx: TransactionReceipt = voting_hub.createVotingSession(
        symbol, start, end, num_votes, from_account(account)
    )
    tx.wait(1)

    voting_session = Contract.from_abi(
        "VotingSession", tx.return_value, VotingSession.abi
    )

    choice = "Joe Biden"

    with brownie.reverts("This voting session already ended."):
        tx = voting_session.addChoice(choice, from_account(account))
