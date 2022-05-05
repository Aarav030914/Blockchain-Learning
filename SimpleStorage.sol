// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.9.0;

contract simplestorage{
    uint256 my_age = 18;
    uint256 my_number = 10;
    function add(uint256 x) public returns(uint256){
        my_number = my_number+x;
        return my_number;
    }
    function retrieve() public view returns(uint256){
        return my_number;
    }
    function store(uint256 _favoriteNumber) public {
        my_number = _favoriteNumber;
    }
}