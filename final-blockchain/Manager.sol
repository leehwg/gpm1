// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./LC.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract LCManager {
    struct LCData {
        uint256 LCNo;
        address BuyerAcc;
        address SellerAcc;
        uint256 Amount;
        LetterOfCredit.LCStatus Status;
        uint256 DOIssue;
        uint256 DOExpiry;
        address LCAddress;
    }

    address public owner;
    IERC20 public stableToken;
    uint256 public lcCounter;

    mapping(uint256 => LCData) public lcdocs;

    event CreateLCSuccessful(uint256 lcId, address lcAddress);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    constructor(address _stableToken) {
        owner = msg.sender;
        stableToken = IERC20(_stableToken);
    }

    function createLC(address buyer, address seller, uint256 amount, string calldata commodity, uint256 expiryDate)
        external
        onlyOwner
        returns (uint256)
    {
        require(stableToken.transferFrom(msg.sender, address(this), amount), "Funding failed");

        LetterOfCredit newLC = new LetterOfCredit(
            address(stableToken),
            buyer,
            seller,
            amount,
            commodity,
            expiryDate
        );

        stableToken.approve(address(newLC), amount); // Approve for funding inside issueLC

        uint256 lcId = ++lcCounter;


        lcdocs[lcId] = LCData({
            LCNo: lcId,
            BuyerAcc: buyer,
            SellerAcc: seller,
            Amount: amount,
            Status: LetterOfCredit.LCStatus.Issued,
            DOIssue: block.timestamp,
            DOExpiry: expiryDate,
            LCAddress: address(newLC)
        });

        emit CreateLCSuccessful(lcId, address(newLC));
        return lcId;
    }

    function viewLC(uint256 lcId)
        public
        view
        returns (
            address seller,
            address buyer,
            uint256 amount,
            LetterOfCredit.LCStatus status,
            uint256 issue,
            uint256 expiry,
            address lcAddr
        )
    {
        LCData memory data = lcdocs[lcId];
        return (data.SellerAcc, data.BuyerAcc, data.Amount, data.Status, data.DOIssue, data.DOExpiry, data.LCAddress);
    }
}
