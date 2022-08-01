from brownie import accounts, network, config
from brownie import Lottery
import scripts.helpful_scripts as hp
import time


def deploy_lottery():
    accounts = hp.getaccounts()
    Lottery.deploy(hp.get_contract("eth_usd_price_list").address,
                   hp.get_contract("vrf_cordinator").address,
                   hp.get_contract("link_token").address,
                   config["networks"][network.show_active()]["fee"],
                   config["networks"][network.show_active()
                                      ]["keyhash"],
                   # dont do this on mainnet putting gas limit
                   {"from": accounts, "gasLimit": 100000},
                   publish_source=config["networks"][network.show_active()].get("verify")) 
    print("Deployed Lottery!!")


def start_lottery():
    accounts = hp.getaccounts()
    # this means it will get the most recent deployed lottery
    lottery = Lottery[-1]
    starting_lottery_transaction = lottery.startLottery({"from": accounts})
    starting_lottery_transaction.wait(1)
    print("The lottery has started yeeeeei!!!")


def enter_lotter():
    accounts = hp.getaccounts()
    # this means it will get the most recent deployed lottery
    lottery = Lottery[-1]
    value = lottery.getEntranceFee()+100000000  # 8decimal places
    enter_lottery_transaction = lottery.enter(
        {"from": accounts, "value": value})
    enter_lottery_transaction.wait(1)
    print("Entered the Lottery!")


def end_lottery():
    accounts = hp.getaccounts()
    lottery = Lottery[-1]
    # fund the Contract
    # then end the lottery
    transaction = hp.fund_with_link(lottery.address)
    transaction.wait(1)
    ending_transaction = lottery.endLottery({"from": accounts})
    ending_transaction.wait(1)
    time.sleep(180)
    print(f"Here is our lottery winner !!!! {lottery.recentWinner}")


def main():
    deploy_lottery()
    start_lottery()
    enter_lotter()
    end_lottery()
