from brownie import VotingHub
from brownie.network.contract import ProjectContract

from scripts.util import from_account, get_account


def deploy_voting_hub():
    account = get_account()

    voting_hub: ProjectContract = VotingHub.deploy(from_account(account))

    return voting_hub


def main():
    deploy_voting_hub()
