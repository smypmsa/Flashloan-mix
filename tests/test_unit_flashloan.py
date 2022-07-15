import pytest, brownie


# Arrange, act, arrange
@pytest.mark.require_network("mainnet-fork-dev")
def test_weth_flashloan(owner_account,
                        flashloan_contract,
                        WETH, 
                        flashloan_contract_weth_balance,
                        min_contract_balance):
    """
    Test a flashloan that borrows Wrapped Ethereum.
    """
    approve_tx = WETH.approve(flashloan_contract,
                            min_contract_balance,
                            {'from': owner_account})
    approve_tx.wait(1)

    flashloan_contract.flashLoan(WETH,
                                min_contract_balance,
                                {'from': owner_account})
    

def test_bad_actor_cant_run_flashloan(bad_actor,
                                    bad_actor_weth_balance,
                                    flashloan_contract,
                                    WETH,
                                    flashloan_contract_weth_balance,
                                    min_contract_balance):
    """
    Test that bad actor can't run a flashloan.
    """
    with brownie.reverts():
        flashloan_contract.flashLoan(WETH,
                                    min_contract_balance,
                                    {'from': bad_actor})
