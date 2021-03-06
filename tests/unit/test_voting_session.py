import time

import brownie
import pytest
from brownie import VotingSession, exceptions, network
from brownie.network.contract import Contract, ProjectContract
from brownie.network.transaction import TransactionReceipt

from scripts.deploy_voting_hub import deploy_voting_hub
from scripts.util import LOCAL_BLOCKCHAIN_ENVIRONMENTS, from_account, get_account


def test_voting_session_creation():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local environment testing!")

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


def test_voting_session_creation_duplicate():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local environment testing!")

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

    with brownie.reverts("Voting session with this symbol already exists."):
        tx: TransactionReceipt = voting_hub.createVotingSession(
            expected_symbol, start, end, num_votes, from_account(account)
        )


def test_voting_session_creation_zero_num_votes_per_user():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local environment testing!")

    account = get_account()
    voting_hub: ProjectContract = deploy_voting_hub()

    expected_symbol = "TEST"
    start = int(time.time())
    end = start + 10
    num_votes = 0

    with brownie.reverts("Number of votes per user must be greater than 0."):
        voting_hub.createVotingSession(
            expected_symbol, start, end, num_votes, from_account(account)
        )


def test_add_choices_from_owner():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local environment testing!")

    account = get_account()
    voting_hub: ProjectContract = deploy_voting_hub()

    symbol = "Presidential Vote"
    start = int(time.time()) + 100
    end = start + 100
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

    choice2 = "Donald Trum"
    tx = voting_session.addChoice(choice2, from_account(account))
    tx.wait(1)

    assert voting_session.choices(0, from_account(account)) == choice
    assert voting_session.choicesMap(choice, from_account(account))
    assert voting_session.votesPerChoice(choice, from_account(account)) == 0

    assert voting_session.choices(1, from_account(account)) == choice2
    assert voting_session.choicesMap(choice2, from_account(account))
    assert voting_session.votesPerChoice(choice2, from_account(account)) == 0


def test_add_choice_from_non_owner():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local environment testing!")

    account = get_account()
    voting_hub: ProjectContract = deploy_voting_hub()

    symbol = "Presidential Vote"
    start = int(time.time())
    end = start + 100
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


def test_add_choice_after_start():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local environment testing!")

    account = get_account()
    voting_hub: ProjectContract = deploy_voting_hub()

    symbol = "Presidential Vote"
    start = int(time.time())
    end = start + 100
    num_votes = 2

    tx: TransactionReceipt = voting_hub.createVotingSession(
        symbol, start, end, num_votes, from_account(account)
    )
    tx.wait(1)

    voting_session = Contract.from_abi(
        "VotingSession", tx.return_value, VotingSession.abi
    )

    choice = "Joe Biden"

    with brownie.reverts("This voting session already started."):
        tx = voting_session.addChoice(choice, from_account(account))


def test_add_choice_after_end():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local environment testing!")

    account = get_account()
    voting_hub: ProjectContract = deploy_voting_hub()

    symbol = "Presidential Vote"
    start = int(time.time())
    end = start
    num_votes = 2

    tx: TransactionReceipt = voting_hub.createVotingSession(
        symbol, start, end, num_votes, from_account(account)
    )
    tx.wait(1)

    voting_session = Contract.from_abi(
        "VotingSession", tx.return_value, VotingSession.abi
    )

    choice = "Joe Biden"

    # wait until end of VotingSession
    with brownie.reverts("This voting session already ended."):
        tx = voting_session.addChoice(choice, from_account(account))


def test_add_duplicate_choice():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local environment testing!")

    account = get_account()
    voting_hub: ProjectContract = deploy_voting_hub()

    symbol = "Presidential Vote"
    start = int(time.time()) + 100
    end = start + 100
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

    with brownie.reverts("This choice already exists."):
        tx = voting_session.addChoice(choice, from_account(account))


def test_get_all_choices():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local environment testing!")

    account = get_account()
    voting_hub: ProjectContract = deploy_voting_hub()

    symbol = "Presidential Vote"
    start = int(time.time()) + 100
    end = start + 100
    choices = [
        "Joe Biden",
        "Donald Trump",
        "Kanye West",
        "Howie Hawkins",
        "Jo Jorgensen",
        "Bernie Sanders",
        "Elizabeth Warren",
        "Michael Bloomberg",
        "Kamala Harris",
        "Pete Buttigieg",
        "Amy Klobuchar",
        "Andrew Yang",
        "Juli??n Castro",
        "Cory Booker",
        "Joe Walsh",
        "John Delaney",
        "Michael Bennet",
        "Deval Patrick",
        "Tom Steyer",
        "William Weld",
    ]
    num_votes = 2

    tx: TransactionReceipt = voting_hub.createVotingSession(
        symbol, start, end, num_votes, from_account(account)
    )
    tx.wait(1)

    voting_session = Contract.from_abi(
        "VotingSession", tx.return_value, VotingSession.abi
    )

    for choice in choices:
        tx = voting_session.addChoice(choice, from_account(account))
        tx.wait(1)

    actual = voting_session.getAllChoices(from_account(account))
    for i in range(len(choices)):
        assert (
            actual[i] == choices[i]
        ), f"\nResults expected: {choices[i]}\nBut were: {actual[i]}"


def test_get_all_choices_zero_choices():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local environment testing!")

    account = get_account()
    voting_hub: ProjectContract = deploy_voting_hub()

    symbol = "Presidential Vote"
    start = int(time.time()) + 100
    end = start + 100
    num_votes = 2

    tx: TransactionReceipt = voting_hub.createVotingSession(
        symbol, start, end, num_votes, from_account(account)
    )
    tx.wait(1)

    voting_session = Contract.from_abi(
        "VotingSession", tx.return_value, VotingSession.abi
    )

    expected = ()
    actual = voting_session.getAllChoices(from_account(account))
    assert actual == expected, f"\nResults expected: {expected}\nBut were: {actual}"


def test_get_num_of_votes_for_user_no_votes():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local environment testing!")

    account = get_account()
    voting_hub: ProjectContract = deploy_voting_hub()

    symbol = "Presidential Vote"
    start = int(time.time()) + 100
    end = start + 100
    num_votes = 3

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

    expected = 0
    actual = voting_session.getNumOfVotesForUser(from_account(account))
    assert actual == expected, f"\nResults expected: {expected}\nBut were: {actual}"


def test_get_num_of_votes_for_user():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local environment testing!")

    account = get_account()
    voting_hub: ProjectContract = deploy_voting_hub()

    symbol = "Presidential Vote"
    start = int(time.time()) + 2
    end = start + 100
    num_votes = 3

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

    num_of_votes_owner = 2
    time.sleep(2)
    tx_vote: TransactionReceipt = voting_session.vote(
        choice, num_of_votes_owner, from_account(account)
    )
    tx_vote.wait(1)

    expected = num_of_votes_owner
    actual = voting_session.getNumOfVotesForUser(from_account(account))
    assert actual == expected, f"\nResults expected: {expected}\nBut were: {actual}"


def test_vote_owner_and_non_owner():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local environment testing!")

    account = get_account()
    voting_hub: ProjectContract = deploy_voting_hub()

    symbol = "Presidential Vote"
    start = int(time.time()) + 2
    end = start + 100
    num_votes = 3

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

    time.sleep(2)
    num_of_votes_owner = 2
    tx_vote: TransactionReceipt = voting_session.vote(
        choice, num_of_votes_owner, from_account(account)
    )
    tx_vote.wait(1)

    non_owner = get_account(index=1)
    num_of_votes_non_owner = 1
    tx_vote: TransactionReceipt = voting_session.vote(
        choice, num_of_votes_non_owner, from_account(non_owner)
    )
    tx_vote.wait(1)

    assert (
        voting_session.votesPerUser(account, from_account(account))
        == num_of_votes_owner
    )
    assert (
        voting_session.votesPerUser(non_owner, from_account(non_owner))
        == num_of_votes_non_owner
    )

    assert (
        voting_session.votesPerChoice(choice, from_account(account))
        == num_of_votes_owner + num_of_votes_non_owner
    )


def test_vote_before_start():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local environment testing!")

    account = get_account()
    voting_hub: ProjectContract = deploy_voting_hub()

    symbol = "Presidential Vote"
    start = int(time.time()) + 100
    end = start + 100
    num_votes = 3

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

    num_of_votes_owner = 2
    with brownie.reverts("This voting session did not start yet."):
        voting_session.vote(choice, num_of_votes_owner, from_account(account))


def test_vote_after_end():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local environment testing!")

    account = get_account()
    voting_hub: ProjectContract = deploy_voting_hub()

    symbol = "Presidential Vote"
    start = int(time.time()) + 2
    end = start
    num_votes = 3

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

    time.sleep(2)
    num_of_votes_owner = 2
    with brownie.reverts("This voting session already ended."):
        voting_session.vote(choice, num_of_votes_owner, from_account(account))


def test_vote_invalid_choice():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local environment testing!")

    account = get_account()
    voting_hub: ProjectContract = deploy_voting_hub()

    symbol = "Presidential Vote"
    start = int(time.time())
    end = start + 100
    num_votes = 3

    tx: TransactionReceipt = voting_hub.createVotingSession(
        symbol, start, end, num_votes, from_account(account)
    )
    tx.wait(1)

    voting_session = Contract.from_abi(
        "VotingSession", tx.return_value, VotingSession.abi
    )

    invalid_choice = "Hillary"
    num_of_votes_owner = num_votes - 1

    with brownie.reverts("Invalid choice."):
        voting_session.vote(invalid_choice, num_of_votes_owner, from_account(account))


def test_vote_exceeded_num_of_votes_per_user_first_vote():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local environment testing!")

    account = get_account()
    voting_hub: ProjectContract = deploy_voting_hub()

    symbol = "Presidential Vote"
    start = int(time.time()) + 2
    end = start + 100
    num_votes = 3

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

    time.sleep(2)
    num_of_votes_owner = num_votes + 1
    with brownie.reverts("Exceeded number of votes per user."):
        voting_session.vote(choice, num_of_votes_owner, from_account(account))


def test_vote_exceeded_num_of_votes_per_user_second_vote():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local environment testing!")

    account = get_account()
    voting_hub: ProjectContract = deploy_voting_hub()

    symbol = "Presidential Vote"
    start = int(time.time()) + 2
    end = start + 100
    num_votes = 3

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

    time.sleep(2)
    num_of_votes_owner = num_votes
    tx_vote: TransactionReceipt = voting_session.vote(
        choice, num_of_votes_owner, from_account(account)
    )
    tx_vote.wait(1)

    with brownie.reverts("Exceeded number of votes per user."):
        voting_session.vote(choice, num_of_votes_owner, from_account(account))


def test_get_results():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local environment testing!")

    account = get_account()
    voting_hub: ProjectContract = deploy_voting_hub()

    symbol = "Presidential Vote"
    start = int(time.time()) + 2
    end = start + 100
    num_votes = 3

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

    choice2 = "Donald Trump"
    tx = voting_session.addChoice(choice2, from_account(account))
    tx.wait(1)

    time.sleep(2)
    num_of_votes_owner = 2
    tx_vote: TransactionReceipt = voting_session.vote(
        choice, num_of_votes_owner, from_account(account)
    )
    tx_vote.wait(1)

    non_owner = get_account(index=1)
    num_of_votes_non_owner = 1
    tx_vote: TransactionReceipt = voting_session.vote(
        choice2, num_of_votes_non_owner, from_account(non_owner)
    )
    tx_vote.wait(1)

    expected = (
        f"{choice} => {num_of_votes_owner}\n{choice2} => {num_of_votes_non_owner}\n"
    )
    actual = voting_session.getResults(from_account(account))

    assert actual == expected, f"\nResults expected: {expected}\nBut were: {actual}"


def test_get_results_lot_of_choices():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local environment testing!")

    account = get_account()
    voting_hub: ProjectContract = deploy_voting_hub()

    symbol = "Presidential Vote"
    start = int(time.time()) + 4
    end = start + 100
    choices = [
        "Joe Biden",
        "Donald Trump",
        "Kanye West",
        "Howie Hawkins",
        "Jo Jorgensen",
        "Bernie Sanders",
        "Elizabeth Warren",
        "Michael Bloomberg",
        "Kamala Harris",
        "Pete Buttigieg",
        "Amy Klobuchar",
        "Andrew Yang",
        "Juli??n Castro",
        "Cory Booker",
        "Joe Walsh",
        "John Delaney",
        "Michael Bennet",
        "Deval Patrick",
        "Tom Steyer",
        "William Weld",
    ]
    num_votes = len(choices)

    tx: TransactionReceipt = voting_hub.createVotingSession(
        symbol, start, end, num_votes, from_account(account)
    )
    tx.wait(1)

    voting_session = Contract.from_abi(
        "VotingSession", tx.return_value, VotingSession.abi
    )

    for choice in choices:
        tx = voting_session.addChoice(choice, from_account(account))
        tx.wait(1)

    time.sleep(2)
    for i in range(len(choices)):
        voting_session.vote(
            choices[i],
            10,
            from_account(get_account(index=(i % 10))),
        )

    expected = ""
    for choice in choices:
        expected += f"{choice} => 10\n"

    results = voting_session.getResults(from_account(account))

    actual = results

    assert actual == expected, f"\nResults expected: {expected}\nBut were: {actual}"
