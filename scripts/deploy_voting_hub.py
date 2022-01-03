import time
from brownie import network, VotingHub
from brownie.network.contract import ProjectContract
from brownie.network.transaction import TransactionReceipt
from scripts.util import get_account, from_account


def deploy_voting_hub():
    account = get_account()

    voting_hub: ProjectContract = VotingHub.deploy(from_account(account))

    return voting_hub


def main():
    deploy_voting_hub()
