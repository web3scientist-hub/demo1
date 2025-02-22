// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

interface IERC20 {
    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);
    function allowance(address owner, address spender) external view returns (uint256);
}

contract BatchTokenSender {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this");
        _;
    }

    function transferOwnership(address newOwner) public onlyOwner {
        require(newOwner != address(0), "Invalid owner address");
        owner = newOwner;
    }

    function batchTransfer(
        address tokenAddress,
        address[] memory recipients,
        uint256 amount
    ) public onlyOwner {
        IERC20 token = IERC20(tokenAddress);
        // 检查合约授权额度
        uint256 requiredAllowance = amount * recipients.length;
        require(
            token.allowance(msg.sender, address(this)) >= requiredAllowance,
            "Insufficient allowance"
        );
        for (uint256 i = 0; i < recipients.length; i++) {
            require(token.transferFrom(msg.sender, recipients[i], amount), "Transfer failed");
        }
    }
}