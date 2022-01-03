from brownie.network import account
from brownie.network.transaction import TransactionReceipt
from brownie.network.contract import ContractTx, ProjectContract
from scripts.util import from_account, get_account
from scripts.deploy_voting_hub import deploy_voting_hub
import time


def test_create_voting_session():
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

    actual_symbol = voting_hub.votingSessionSymbols(0, from_account(account))

    assert expected_symbol == actual_symbol


def test_addresses_of_voting_sessions():
    account = get_account()
    voting_hub: ProjectContract = deploy_voting_hub()

    symbol1, symbol2 = "TEST", "Symbol2"
    start = int(time.time())
    end = start + 10
    num_votes = 2

    tx: TransactionReceipt = voting_hub.createVotingSession(
        symbol1, start, end, num_votes, from_account(account)
    )
    tx.wait(1)
    voting_session1_address = tx.return_value

    tx: TransactionReceipt = voting_hub.createVotingSession(
        symbol2, start, end, num_votes, from_account(account)
    )
    tx.wait(1)
    voting_session2_address = tx.return_value

    assert (
        voting_hub.addressesOfVotingSessions(symbol1, from_account(account))
        == voting_session1_address
    )
    assert (
        voting_hub.addressesOfVotingSessions(symbol2, from_account(account))
        == voting_session2_address
    )


def test_get_all_voting_session_symbols():
    account = get_account()
    voting_hub: ProjectContract = deploy_voting_hub()

    symbol1, symbol2 = "TEST", "Symbol2"
    start = int(time.time())
    end = start + 10
    num_votes = 2

    tx: TransactionReceipt = voting_hub.createVotingSession(
        symbol1, start, end, num_votes, from_account(account)
    )
    tx.wait(1)

    tx: TransactionReceipt = voting_hub.createVotingSession(
        symbol2, start, end, num_votes, from_account(account)
    )
    tx.wait(1)

    voting_symbols = voting_hub.getAllVotinSessionsSymbols()

    assert voting_symbols == [symbol1, symbol2]
