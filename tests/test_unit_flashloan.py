import pytest, brownie


# Arrange, act, arrange


@pytest.mark.require_network("mainnet-fork-dev")
def test_weth_flashloan(owner_account, flashloan_contract, WETH,
                        transfer_weth_to_flashloan_contract, min_contract_balance):
    """
    Test a flashloan that borrows Wrapped Ethereum.
    """
    flashloan_contract.flashLoan(WETH, min_contract_balance, {'from': owner_account})
    

def test_bad_actor_cant_run_flashloan(bad_actor, flashloan_contract, WETH,
                        transfer_weth_to_flashloan_contract, min_contract_balance):
    """
    Test that bad actor can't run a flashloan.
    """
    with brownie.reverts():
        flashloan_contract.flashLoan(WETH, min_contract_balance, {'from': bad_actor})

    