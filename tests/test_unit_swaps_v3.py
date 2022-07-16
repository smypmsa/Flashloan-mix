import pytest, brownie
from web3 import Web3


# Arrange, act, arrange
@pytest.mark.require_network("mainnet-fork-dev")
def test_exact_input_swap(owner_account,
                    owner_account_weth_balance,
                    uniswap3_contract,
                    WETH,
                    DAI,
                    swap_amount):
    """
    Test a single exact input swap WETH-DAI.
    """
    start_dai_balance = DAI.balanceOf(owner_account)

    approve_tx = WETH.approve(uniswap3_contract,
                            swap_amount,
                            {'from': owner_account})
    approve_tx.wait(1)

    swap_tx = uniswap3_contract.swapExactInputSingle(swap_amount,
                                                    WETH.address,
                                                    DAI.address,
                                                    {'from': owner_account})
    swap_tx.wait(1)

    end_dai_balance = DAI.balanceOf(owner_account)
    assert end_dai_balance > start_dai_balance


def test_exact_output_swap(owner_account,
                    owner_account_weth_balance,
                    uniswap3_contract,
                    WETH,
                    DAI,
                    swap_amount):
    """
    Test a single exact output swap WETH-DAI.
    """
    start_dai_balance = DAI.balanceOf(owner_account)

    approve_tx = WETH.approve(uniswap3_contract,
                            swap_amount,
                            {'from': owner_account})
    approve_tx.wait(1)

    # How much DAI we consider to get after swap completed
    exact_dai_output = Web3.toWei(10, 'ether')

    swap_tx = uniswap3_contract.swapExactOutputSingle(exact_dai_output,
                                                    swap_amount,
                                                    WETH.address,
                                                    DAI.address,
                                                    {'from': owner_account})
    swap_tx.wait(1)

    end_dai_balance = DAI.balanceOf(owner_account)
    assert end_dai_balance > start_dai_balance


def test_bad_actor_cant_run_swap(bad_actor,
                                bad_actor_weth_balance,
                                uniswap3_contract,
                                WETH,
                                DAI,
                                swap_amount):
    """
    Test that bad actor can't run a swap.
    """

    approve_tx = WETH.approve(uniswap3_contract,
                            swap_amount,
                            {'from': bad_actor})
    approve_tx.wait(1)

    with brownie.reverts():
        swap_tx = uniswap3_contract.swapExactInputSingle(swap_amount,
                                                        WETH.address,
                                                        DAI.address,
                                                        {'from': bad_actor})
        # swap_tx.wait(1)

    