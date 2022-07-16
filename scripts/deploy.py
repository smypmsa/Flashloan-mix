from brownie import FlashLoan, UniswapSingleSwapV2, UniswapSingleSwapV3, config, network
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS, FORKED_LOCAL_ENVIRONMENTS


def deploy_contract_flashloan():
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
            config["networks"][network.show_active()]["uniswap-router-v2"],
            config["networks"][network.show_active()]["uniswap-router-v3"],
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


def deploy_contract_uniswap_v3():
    """
    Deploys UniswapSingleSwap (Uniswap v3) contract with input parameter Swap Router.
    """

    # If we are working in local/dev environments than deploy contract
    if (network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS):
        account = get_account()
        uniswap_v3 = UniswapSingleSwapV3.deploy(
            config["networks"][network.show_active()]["uniswap-router-v3"],
            {"from": account},
        )
        return uniswap_v3

    # If we are working in non-local/non-dev environments AND there are no contracts
    # deployed before than deploy contract
    if len(FlashLoan) == 0:
        account = get_account()
        uniswap_v3 = UniswapSingleSwapV3.deploy(
            config["networks"][network.show_active()]["uniswap-router-v3"],
            {"from": account},
        )
        return uniswap_v3

    # If we are working in non-local/non-dev environments AND there are contracts deployed
    # before than deploy the most recently deployed contract
    print('The UniswapSingleSwapV3 contract is already deployed.')
    return UniswapSingleSwapV3[-1]


def deploy_contract_uniswap_v2():
    """
    Deploys UniswapSingleSwap (Uniswap v2) contract with input parameter Swap Router.
    """

    # If we are working in local/dev environments than deploy contract
    if (network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS):
        account = get_account()
        uniswap_v2 = UniswapSingleSwapV2.deploy(
            config["networks"][network.show_active()]["uniswap-router-v2"],
            {"from": account},
        )
        return uniswap_v2

    # If we are working in non-local/non-dev environments AND there are no contracts
    # deployed before than deploy contract
    if len(FlashLoan) == 0:
        account = get_account()
        uniswap_v2 = UniswapSingleSwapV2.deploy(
            config["networks"][network.show_active()]["uniswap-router-v2"],
            {"from": account},
        )
        return uniswap_v2

    # If we are working in non-local/non-dev environments AND there are contracts deployed
    # before than deploy the most recently deployed contract
    print('The UniswapSingleSwapV2 contract is already deployed.')
    return UniswapSingleSwapV2[-1]