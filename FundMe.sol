// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
contract FundMe{
    address ethTousd = 0x8A753747A1Fa494EC906cE90E9f37563A8AF630e;
    uint256 minimumUSD = 50;
    address public owner;

    constructor() public {
        owner = msg.sender;
    }
    mapping(address => uint256) public AddressToMoney;
    address[] public funders;

    function fund() public payable{
        require(convert(msg.value) >= minimumUSD, "You need to spend minimum ETH!");
        funders.push(msg.sender);
        AddressToMoney[msg.sender] += convert(msg.value); 
    }
    AggregatorV3Interface priceFeed = AggregatorV3Interface(ethTousd);

    function getVersion() public view returns(uint256){

        return priceFeed.version();
    }
    function getPrice() public view returns(int256){
    (,
     int256 answer,
     ,
     ,
     )
     = priceFeed.latestRoundData();
      return answer;
    }
    function convert(uint256 ethtoUSDAmount) public view returns(uint256){
        uint256 convRate = uint256(getPrice());
        uint256 finalAmount = ((ethtoUSDAmount)*convRate)/1000000000000000000;
        return finalAmount;
    }

    modifier onlyOwner{
        require(msg.sender == owner);
        _;
    }
    function withdraw() onlyOwner public payable{
        msg.sender.transfer(address(this).balance);
        for(uint256 i=0; i<funders.length;i++){
            address funder = funders[i];
            AddressToMoney[funder] = 0;
        }
    }

}