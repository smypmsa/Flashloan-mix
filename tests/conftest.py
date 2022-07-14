import pytest
from scripts.helpful_scripts import get_account, get_bad_actor_account, get_contracts
from scripts.deploy import deploy_contract
from scripts.get_weth import get_weth
from web3 import Web3


@pytest.fixture(autouse=True)
def setup(fn_isolation):
    """
    Isolation setup fixture.
    This ensures that each test runs against the same base environment.
    """
    pass


@pytest.fixture(scope="module")
def flashloan_contract():
    """
    Deploys FlashLoan contract.
    """
    return deploy_contract()


@pytest.fixture(scope="module")
def min_contract_balance():
    """
    Sets minimal Flashloan contract balance (in WETH).
    """
    min_balance = 0.01
    return Web3.toWei(min_balance, 'ether')


@pytest.fixture(scope="module")
def owner_account():
    """
    Gets owner account.
    """
    return get_account()


@pytest.fixture(scope="module")
def transfer_weth_to_flashloan_contract(owner_account, flashloan_contract, min_contract_balance, WETH):
    """
    Transfer WETH to FlashLoan contract from the owner.
    """
    tx1 = get_weth(owner_account.address)
    # tx1.wait(1)
    tx2 = WETH.transfer(flashloan_contract.address, min_contract_balance, {"from": owner_account})
    # tx2.wait(2)
    return tx2


@pytest.fixture(scope="module")
def bad_actor():
    """
    Gets bad actor account.
    """
    return get_bad_actor_account()


@pytest.fixture(scope="module")
def WETH():
    """
    Gets WETH contract.
    """
    return get_contracts()[1]


