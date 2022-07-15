pragma solidity ^0.6.12;
pragma experimental ABIEncoderV2;

import '@uniswap3periphery/contracts/libraries/TransferHelper.sol';
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

import {IUniswapV2Router02} from '../interfaces/IUniswapV2Router02.sol';
import {SafeMath} from '../libraries/SafeMath.sol';


contract UniswapSingleSwapV2 is Ownable {
    using SafeMath for uint256;

    IUniswapV2Router02 public immutable router;

    constructor(IUniswapV2Router02 router_) public {
        router = router_;
    }

    function swapExactInputSingle(
        uint256 amountIn,
        address tokenIn,
        address tokenOut
    ) onlyOwner external {

        TransferHelper.safeTransferFrom(tokenIn, msg.sender, address(this), amountIn);
        TransferHelper.safeApprove(tokenIn, address(router), amountIn);

        address[] memory path = new address[](2);
        path[0] = tokenIn;
        path[1] = tokenOut;

        router.swapExactTokensForTokens(
            amountIn,
            0, // amountOutMin: we can skip computing this number because the math is tested
            path,
            msg.sender, // recipient of the output tokens
            block.timestamp // deadline: unix timestamp after which the transaction will revert
        );
    }
}