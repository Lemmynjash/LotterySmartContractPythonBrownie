// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0 <0.9.0;

contract Lottery {
    address payable[] public players; // will going to use this to track all the players

    function enter() public payable {}

    function getEntranceFee() public {}

    function startLottery() public {}

    function endLottery() public {}
}
