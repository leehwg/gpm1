// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "./Manager.sol";


contract LetterOfCredit {
    enum LCStatus { Issued, DocumentsSubmitted, DocumentsApproved, DocumentsRejected, Settled, Cancelled }

    struct LC {
        address buyer;
        address seller;
        uint256 amount;
        string commodity;
        uint256 expiryDate;
        bytes32 docHash;
        LCStatus status;
    }

    address public issuingBank;
    IERC20 public stableToken;
    uint256 public lcCounter;

    mapping(uint256 => LC) public lcs;

    event LCIssued(uint256 indexed lcId, address indexed buyer, address indexed seller, uint256 amount);
    event DocumentsSubmitted(uint256 indexed lcId, bytes32 docHash);
    event DocumentsApproved(uint256 indexed lcId);
    event DocumentsRejected(uint256 indexed lcId);
    event PaymentReleased(uint256 indexed lcId);
    event LCCancelled(uint256 indexed lcId);

    modifier onlyBank() {
        require(msg.sender == issuingBank, "Only issuing bank can perform this action");
        _;
    }

    modifier onlyBuyer(uint256 lcId) {
        require(msg.sender == lcs[lcId].buyer, "Only buyer can perform this action");
        _;
    }

    modifier onlySeller(uint256 lcId) {
        require(msg.sender == lcs[lcId].seller, "Only seller can perform this action");
        _;
    }

    constructor(
    address _stableToken,
    address buyer,
    address seller,
    uint256 amount,
    string memory commodity,
    uint256 expiryDate
) {
    issuingBank = msg.sender;
    stableToken = IERC20(_stableToken);

    require(expiryDate > block.timestamp, "Expiry date must be in the future");
    require(stableToken.transferFrom(issuingBank, address(this), amount), "Funding failed");

    lcCounter = 1;
    lcs[lcCounter] = LC(buyer, seller, amount, commodity, expiryDate, 0x0, LCStatus.Issued);

    emit LCIssued(lcCounter, buyer, seller, amount);
}

    function issueLC(
        address buyer,
        address seller,
        uint256 amount,
        string calldata commodity,
        uint256 expiryDate
    ) external onlyBank returns (uint256) {
        require(expiryDate > block.timestamp, "Expiry date must be in the future");
        require(stableToken.transferFrom(msg.sender, address(this), amount), "Funding failed");

        lcCounter++;
        lcs[lcCounter] = LC(buyer, seller, amount, commodity, expiryDate, 0x0, LCStatus.Issued);

        emit LCIssued(lcCounter, buyer, seller, amount);
        return lcCounter;
    }

    function submitDocuments(uint256 lcId, bytes32 docHash) external onlySeller(lcId) {
        LC storage lc = lcs[lcId];
        require(lc.status == LCStatus.Issued, "LC not in correct state to submit documents");
        require(block.timestamp <= lc.expiryDate, "LC expired");

        lc.docHash = docHash;
        lc.status = LCStatus.DocumentsSubmitted;

        emit DocumentsSubmitted(lcId, docHash);
    }

    function approveDocuments(uint256 lcId) external onlyBank {
        LC storage lc = lcs[lcId];
        require(lc.status == LCStatus.DocumentsSubmitted, "No documents to approve");

        lc.status = LCStatus.DocumentsApproved;

        emit DocumentsApproved(lcId);
    }

    function rejectDocuments(uint256 lcId) external onlyBank {
        LC storage lc = lcs[lcId];
        require(lc.status == LCStatus.DocumentsSubmitted, "No documents to reject");

        lc.status = LCStatus.DocumentsRejected;

        emit DocumentsRejected(lcId);
    }

    function releasePayment(uint256 lcId) external onlyBank {
        LC storage lc = lcs[lcId];
        require(lc.status == LCStatus.DocumentsApproved, "Documents not approved");

        require(stableToken.transfer(lc.seller, lc.amount), "Payment transfer failed");
        lc.status = LCStatus.Settled;

        emit PaymentReleased(lcId);
    }

    function cancelLC(uint256 lcId) external onlyBank {
        LC storage lc = lcs[lcId];
        require(lc.status == LCStatus.Issued || lc.status == LCStatus.DocumentsRejected, "Cannot cancel");

        lc.status = LCStatus.Cancelled;
        require(stableToken.transfer(issuingBank, lc.amount), "Refund failed");

        emit LCCancelled(lcId);
    }

    function getLC(uint256 lcId) external view returns (
        address buyer,
        address seller,
        uint256 amount,
        string memory commodity,
        uint256 expiryDate,
        bytes32 docHash,
        LCStatus status
    ) {
        LC memory lc = lcs[lcId];
        return (
            lc.buyer,
            lc.seller,
            lc.amount,
            lc.commodity,
            lc.expiryDate,
            lc.docHash,
            lc.status
        );
    }
}
