from brownie import config, network, interface
from scripts.helpful_scripts import get_account
from web3 import Web3


MINIMUM_AMOUNT = 0.01


def main():
    """
    Runs the get_weth function to get WETH
    """

    get_weth()


def get_weth(account=None, weth_amount=None):
    """
    Mints WETH by depositing ETH.
    """

    if not account:
        account = get_account()

    if not weth_amount:
        weth_amount = Web3.toWei(MINIMUM_AMOUNT, 'ether')

    weth_contract = interface.IWETH(config['networks'][network.show_active()]['weth-token'])

    # Check balance
    if weth_contract.balanceOf(account) < weth_amount:
        print('Funding Account with WETH ...')
        tx = weth_contract.deposit({'from': account,
                                    'value': weth_amount,
                                    'gas_limit':12000000,
                                    'allow_revert': False})
        print(f"Received {Web3.fromWei(weth_amount, 'ether')} WETH!")
        tx.wait(1)
        return tx

    else:
        print('The Account is already funded with WETH.')

    return True