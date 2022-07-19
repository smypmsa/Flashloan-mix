// SPDX-License-Identifier: MIT
pragma solidity ^0.6.12;
pragma experimental ABIEncoderV2;

import {FlashLoanReceiverBase} from "@aave/contracts/flashloan/base/FlashLoanReceiverBase.sol";
import {ILendingPoolAddressesProvider} from "@aave/contracts/interfaces/ILendingPoolAddressesProvider.sol";
import {ILendingPool} from "@aave/contracts/interfaces/ILendingPool.sol";

import {TransferHelper} from '@uniswap3periphery/contracts/libraries/TransferHelper.sol';
import {ISwapRouter} from '@uniswap3periphery/contracts/interfaces/ISwapRouter.sol';
import {IUniswapV2Router02} from '../interfaces/IUniswapV2Router02.sol';

import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";


contract FlashLoan is FlashLoanReceiverBase, Ownable {
    address payable OWNER;
    IUniswapV2Router02 internal routerV2;
    ISwapRouter internal routerV3;

    address private tokenA;
    address private tokenB;
    uint256 private swapAmount;

    // For this example, we will set the pool fee to 0.3%.
    uint24 public constant poolFee = 3000;

    constructor(address payable _owner,
                address _addressesProvider,
                IUniswapV2Router02 _routerV2,
                ISwapRouter _routerV3
                ) FlashLoanReceiverBase(ILendingPoolAddressesProvider(_addressesProvider)) public {
        OWNER = _owner;
        routerV2 = _routerV2;
        routerV3 = _routerV3;
    }

    // Uniswap V2
    function swapExactInputSingle_V2 (
        uint256 amountIn,
        address tokenIn,
        address tokenOut
    ) internal returns (uint256 amountOut) {
        // msg.sender must approve this contract
        TransferHelper.safeApprove(
            tokenIn,
            address(routerV2),
            amountIn);

        address[] memory path = new address[](2);
        path[0] = tokenIn;
        path[1] = tokenOut;

        amountOut = routerV2.swapExactTokensForTokens(
            amountIn,
            0, // amountOutMin: we can skip computing this number because the math is tested
            path,
            address(this), // msg.sender in this case won't work as DAI would return to Aave contract
            block.timestamp // deadline: unix timestamp after which the transaction will revert
        )[1];
    }

    // Uniswap V3
    function swapExactInputSingle_V3 (
        uint256 amountIn,
        address tokenIn,
        address tokenOut
    ) internal returns (uint256 amountOut) {
        // msg.sender must approve this contract
        TransferHelper.safeApprove(
            tokenIn,
            address(routerV3),
            amountIn);

        ISwapRouter.ExactInputSingleParams memory params =
            ISwapRouter.ExactInputSingleParams({
                tokenIn: tokenIn,
                tokenOut: tokenOut,
                fee: poolFee,
                recipient: address(this), // msg.sender in this case won't work as DAI would return to Aave contract
                deadline: block.timestamp,
                amountIn: amountIn,
                amountOutMinimum: 0,
                sqrtPriceLimitX96: 0
            });

        // The call to `exactInputSingle` executes the swap.
        amountOut = routerV3.exactInputSingle(params);
    }

    function executeOperation(
        address[] calldata assets,
        uint256[] calldata amounts,
        uint256[] calldata premiums,
        address initiator,
        bytes calldata params
    )
        external
        override
        returns (bool)
    {
        uint256 outputAmount = swapExactInputSingle_V2(swapAmount, tokenA, tokenB);
        // Sell all of token_b
        swapExactInputSingle_V3(outputAmount * 1/2, tokenB, tokenA);

        // Approve the LendingPool contract allowance to *pull* the owed amount
        for (uint i = 0; i < assets.length; i++) {
            uint amountOwing = amounts[i].add(premiums[i]);
            IERC20(assets[i]).approve(address(LENDING_POOL), amountOwing);
        }

        return true;
    }

    function _flashloan(
        address[] memory assets,
        uint256[] memory amounts
    ) internal {
        address receiverAddress = address(this);
        address onBehalfOf = address(this);

        bytes memory params = "";
        uint16 referralCode = 0;

        uint256[] memory modes = new uint256[](assets.length);

        // 0 = no debt (flash), 1 = stable, 2 = variable
        for (uint256 i = 0; i < assets.length; i++) {
            modes[i] = 0;
        }

        LENDING_POOL.flashLoan(
            receiverAddress,
            assets,
            amounts,
            modes,
            onBehalfOf,
            params,
            referralCode
        );
    }

    function flashLoan(
        address _tokenA,
        address _tokenB,
        uint256 _amount
    ) external onlyOwner {
        bytes memory data = "";
        
        address[] memory assets = new address[](1);
        assets[0] = _tokenA;

        uint256[] memory amounts = new uint256[](1);
        amounts[0] = _amount;

        // Token A is a token which we get from Aave
        // and which we sell in the first swap.
        tokenA = _tokenA;
        tokenB = _tokenB;
        // Swap amount is less than loan amount
        // for testing purposes.
        swapAmount = _amount * 3/4;

        _flashloan(assets, amounts);
    }


}