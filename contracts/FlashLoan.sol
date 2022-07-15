// SPDX-License-Identifier: MIT
pragma solidity ^0.6.12;


import {FlashLoanReceiverBase} from "@aave/contracts/flashloan/base/FlashLoanReceiverBase.sol";
import {ILendingPoolAddressesProvider} from "@aave/contracts/interfaces/ILendingPoolAddressesProvider.sol";
import {ILendingPool} from "@aave/contracts/interfaces/ILendingPool.sol";


import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";


contract FlashLoan is FlashLoanReceiverBase, Ownable {
    address payable OWNER;

    constructor(address payable _owner, address _addressesProvider) FlashLoanReceiverBase(ILendingPoolAddressesProvider(_addressesProvider)) public {
        OWNER = _owner;
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

        // Custom logic

        // Approve the LendingPool contract allowance to *pull* the owed amount
        for (uint i = 0; i < assets.length; i++) {
            uint amountOwing = amounts[i].add(premiums[i]);
            IERC20(assets[i]).approve(address(LENDING_POOL), amountOwing);
        }

        return true;
    }

    function _flashloan(address[] memory assets, uint256[] memory amounts) internal {
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

    function flashLoan(address _asset, uint256 _amount) external onlyOwner {
        bytes memory data = "";

        address[] memory assets = new address[](1);
        assets[0] = _asset;

        uint256[] memory amounts = new uint256[](1);
        amounts[0] = _amount;

        _flashloan(assets, amounts);
    }

    
    
}