from brownie import network, config, accounts, interface


FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def get_bad_actor_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[1]
    else:
        return accounts.add(config["wallets"]["bad_actor"])

def get_contracts():
    provider_contract = interface.ILendingPoolAddressesProvider(config['networks'][network.show_active()]['aave-addresses-provider'])
    weth_contract = interface.IWETH(config['networks'][network.show_active()]['weth-token'])
    return provider_contract, weth_contract