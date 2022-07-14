from brownie import FlashLoan, config, network
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS, FORKED_LOCAL_ENVIRONMENTS


def deploy_contract():
    """
    Deploys FlashLoan contract with input parameters: owner and
    address of AAVE addresses provider contract.
    """

    # If we are working in local/dev environments than deploy contract
    if (network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS):
        account = get_account()
        flashloan = FlashLoan.deploy(
            account.address,
            config["networks"][network.show_active()]["aave-addresses-provider"],
            {"from": account},
        )
        return flashloan

    # If we are working in non-local/non-dev environments AND there are no contracts
    # deployed before than deploy contract
    if len(FlashLoan) == 0:
        account = get_account()
        flashloan = FlashLoan.deploy(
            account.address,
            config["networks"][network.show_active()]["aave-addresses-provider"],
            {"from": account},
        )
        return flashloan

    # If we are working in non-local/non-dev environments AND there are contracts deployed
    # before than deploy the most recently deployed contract
    print('The FlashLoan contract is already deployed.')
    return FlashLoan[-1]