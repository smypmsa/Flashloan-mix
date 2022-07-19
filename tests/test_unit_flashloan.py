import pytest, brownie


# Arrange, act, arrange
@pytest.mark.require_network("mainnet-fork-dev")
def test_weth_flashloan(owner_account,
                        flashloan_contract,
                        WETH,
                        DAI,
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
                                DAI,
                                min_contract_balance,
                                {'from': owner_account})


@pytest.mark.require_network("mainnet-fork-dev")
def test_buy_sell_dai(owner_account,
                        flashloan_contract,
                        WETH,
                        DAI,
                        flashloan_contract_weth_balance,
                        min_contract_balance):
    """
    Test a flashloan that borrows Wrapped Ethereum, buys and sells DAI.
    """
    start_dai_balance = DAI.balanceOf(flashloan_contract)

    approve_tx = WETH.approve(flashloan_contract,
                            min_contract_balance,
                            {'from': owner_account})
    approve_tx.wait(1)

    flashloan_contract.flashLoan(WETH,
                                DAI,
                                min_contract_balance,
                                {'from': owner_account})

    end_dai_balance = DAI.balanceOf(flashloan_contract)
    # For testing purposes, we do not sell all bought DAI
    assert end_dai_balance > start_dai_balance

    
def test_bad_actor_cant_run_flashloan(bad_actor,
                                    bad_actor_weth_balance,
                                    flashloan_contract,
                                    WETH,
                                    DAI,
                                    flashloan_contract_weth_balance,
                                    min_contract_balance):
    """
    Test that bad actor can't run a flashloan.
    """
    with brownie.reverts():
        flashloan_contract.flashLoan(WETH,
                                    DAI,
                                    min_contract_balance,
                                    {'from': bad_actor})
