// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract USD is ERC20, Ownable {
    constructor() ERC20("US Dollar", "USD") Ownable(msg.sender) {
        _mint(msg.sender, 1_000_000_000 * 10 ** decimals()); // 1 billion USD for testing
    }

    function mint(address to, uint256 amount) external onlyOwner {
        _mint(to, amount);
    }
}
