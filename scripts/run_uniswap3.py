from brownie import config, network, interface
from scripts.get_weth import get_weth
from scripts.helpful_scripts import get_account
from scripts.deploy import deploy_contract_uniswap_v3
from web3 import Web3


MINIMUM_BALANCE = 0.01
SWAP_AMOUNT = Web3.toWei(MINIMUM_BALANCE * 0.9, 'ether')
MINIMUM_BALANCE_WEI = Web3.toWei(MINIMUM_BALANCE, 'ether')

TOKEN_IN = config['networks'][network.show_active()]['weth-token']
TOKEN_OUT = config['networks'][network.show_active()]['dai-token']


def main():
    # Set up Account
    account = get_account()
    get_weth_status = get_weth(account, MINIMUM_BALANCE_WEI)

    weth = interface.IWETH(config['networks'][network.show_active()]['weth-token'])

    # Deploy Uniswap v3 contract
    print('Getting Uniswap v3 contract ...')
    uniswap_v3 = deploy_contract_uniswap_v3()
    
    # Execute single swap
    print('Executing swap ...')
    approve_tx = weth.approve(uniswap_v3, SWAP_AMOUNT, {'from': account})
    approve_tx.wait(1)
    tx = uniswap_v3.swapExactInputSingle(SWAP_AMOUNT, TOKEN_IN, TOKEN_OUT, {'from': account})
    tx.wait(1)

    print('Success, my little uniswap boy!')
    return uniswap_v3