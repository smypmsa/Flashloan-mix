# Flash loan + Uniswap V2/V3
This repo inspired by [brownie mix](https://github.com/brownie-mix/aave-flashloan-mix). Tests run in Ethereum mainnet-fork (Alchemy).

The purpose is to build arbitrage smart contract utilizing flash loans.

### Run flash loan
To run flash loan in kovan testnet, follow the next steps (your test wallet must have at least 0.011 ETH, however you can update min balance in scripts):
1. Update .env file with your credentials.
```
export PRIVATE_KEY=56b44efdb532...
export BAD_ACTOR=46b44efdb532...
export WEB3_INFURA_PROJECT_ID=g5bc2a9d4a..
export WEB3_ALCHEMY_PROJECT_ID=GHJT355...
export ETHERSCAN_TOKEN=6FGRH...
```
2. Run `brownie compile` to check if the contract compiles.
3. Run `brownie run scripts/run_flashloan.py`.

### To do list
Basic tasks:
- [x] Add swaps to the contract (Uniswap V3)
- [x] Add swap to the contract (Uniswap V2)
- [x] Add tests covering swaps
- [x] Test a complete smart contract in live testnet
- [ ] Add withdrawal of all tokens to the owner
- [ ] Add fetching pool prices (off-chain?)

Advanced tasks:
- [ ] Consider potential profits/losses
- [ ] Optimize gas costs
- [ ] Refactor the code according to best practice
