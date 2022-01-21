from brownie import network, accounts, MockV3Aggregator, Contract, config, VRFCoordinatorMock, LinkToken
from web3 import Web3


LOCAL_BLOCHAIN_ENVIRONMENT = ["development", "ganache-local"]


def getaccounts(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)

    if network.show_active() in LOCAL_BLOCHAIN_ENVIRONMENT:
        return accounts[0]

    return accounts.load("lemmy-account")


contract_to_mock = {
    "eth_usd_price_list": MockV3Aggregator,
    "vrf_cordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}
#


def get_contract(contract_name):
    """This function will grab the contract addresses from the brownie config
    if defined, otherwise, it will deploy a mock version of that contract, and
    return that mock contract.
        Args:
            contract_name (string)
        Returns:
            brownie.network.contract.ProjectContract: The most recently deployed
            version of this contract.
    """

    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCHAIN_ENVIRONMENT:
        if len(contract_type) <= 0:
            # MockV3Aggregator.length
            deploy_mocks()
        contract = contract_type[-1]
        # MockV3Aggregator[-1]
    else:
        contract_address = config["networks"][network.show_active(
        )][contract_name]
        # address
        # ABI
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
        # MockV3Aggregator.abi
    return contract


DECIMALS = 8
INITIAL_VALUE = 200000000000


def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    account = getaccounts()
    MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print("Deployed! Mocks")
