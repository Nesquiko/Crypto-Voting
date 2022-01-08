from brownie import VotingHub, config, network
from brownie.network.contract import ProjectContract

from scripts.util import from_account, get_account


def deploy_voting_hub():
    account = get_account()

    voting_hub: ProjectContract = VotingHub.deploy(
        from_account(account),
        publish_source=config["networks"][network.show_active()]["verify"],
    )

    return voting_hub


def main():
    deploy_voting_hub()
