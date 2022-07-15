import pytest
from scripts.helpful_scripts import get_account, get_bad_actor_account, get_contracts
from scripts.deploy import deploy_contract_flashloan, deploy_contract_uniswap_v3
from scripts.get_weth import get_weth
from web3 import Web3


@pytest.fixture(autouse=True)
def setup(fn_isolation):
    """
    Isolation setup fixture.
    This ensures that each test runs against the same base environment.
    """
    pass


# CONTRACTS
# Contracts which are under testing.

@pytest.fixture(scope="module")
def flashloan_contract():
    """
    Deploys FlashLoan contract.
    """
    return deploy_contract_flashloan()


@pytest.fixture(scope="module")
def uniswap3_contract():
    """
    Deploys UniswapSingleSwap contract.
    """
    return deploy_contract_uniswap_v3()


# ACCOUNTS
# All accounts used in testing.

@pytest.fixture(scope="module")
def owner_account():
    """
    Gets owner account.
    """
    return get_account()


@pytest.fixture(scope="module")
def bad_actor():
    """
    Gets bad actor account.
    """
    return get_bad_actor_account()


# PARAMETERS
# Set parameters values for testing.

@pytest.fixture(scope="module")
def min_contract_balance():
    """
    Sets minimal Flashloan contract balance (in WETH).
    """
    min_balance = 0.01
    return Web3.toWei(min_balance, 'ether')


@pytest.fixture(scope="module")
def swap_amount():
    """
    Sets swap amount.
    """
    swap_am = 0.01
    return Web3.toWei(swap_am, 'ether')


# BALANCES
# Fund accounts, transfer tokens, etc.

@pytest.fixture(scope="module")
def owner_account_weth_balance(owner_account, min_contract_balance):
    """
    Gets WETH on owner account.
    """
    return get_weth(account=owner_account.address, weth_amount=min_contract_balance)


@pytest.fixture(scope="module")
def bad_actor_weth_balance(bad_actor, min_contract_balance):
    """
    Gets WETH on bad actor account.
    """
    return get_weth(account=bad_actor.address, weth_amount=min_contract_balance)


@pytest.fixture(scope="module")
def flashloan_contract_weth_balance(owner_account, flashloan_contract, min_contract_balance, WETH):
    """
    Transfer WETH to FlashLoan contract from the owner.
    """
    tx1 = get_weth(owner_account.address)
    # tx1.wait(1)
    tx2 = WETH.transfer(flashloan_contract.address, min_contract_balance, {"from": owner_account})
    # tx2.wait(2)
    return tx2


# TOKEN CONTRACTS
# Get token contracts used in testing.

@pytest.fixture(scope="module")
def WETH():
    """
    Gets WETH contract.
    """
    return get_contracts()[1]

@pytest.fixture(scope="module")
def DAI():
    """
    Gets DAI contract.
    """
    return get_contracts()[2]
