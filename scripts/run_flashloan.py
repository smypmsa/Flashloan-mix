from brownie import config, network, interface
from scripts.get_weth import get_weth
from scripts.helpful_scripts import get_account
from scripts.deploy import deploy_contract_flashloan
from web3 import Web3


MINIMUM_BALANCE = 0.01
LOAN_AMOUNT = Web3.toWei(MINIMUM_BALANCE * 0.9, 'ether')
MINIMUM_BALANCE_WEI = Web3.toWei(MINIMUM_BALANCE, 'ether')


def main():
    # Set up Account
    account = get_account()
    get_weth_status = get_weth(account, MINIMUM_BALANCE_WEI)

    weth = interface.IWETH(config['networks'][network.show_active()]['weth-token'])
    dai = interface.IERC20(config['networks'][network.show_active()]['dai-token'])

    # Deploy Flashloan contract
    print('Getting Flashloan contract ...')
    flashloan = deploy_contract_flashloan()
    
    # Fund the contract with WETH
    if weth.balanceOf(flashloan) < MINIMUM_BALANCE_WEI:
        print('Funding FlashLoan contract with WETH ...')
        weth_tx = weth.transfer(flashloan.address, MINIMUM_BALANCE_WEI, {"from": account})
        weth_tx.wait(1)
    else:
        print('The FlashLoan contract is already funded with WETH')

    # Execute flash loan
    print('Executing flash loan ...')
    approve_tx = weth.approve(flashloan, LOAN_AMOUNT, {'from': account})
    approve_tx.wait(1)
    tx = flashloan.flashLoan(weth, dai, LOAN_AMOUNT, {'from': account})
    tx.wait(1)

    print('Success, my little flash boy!')
    return flashloan