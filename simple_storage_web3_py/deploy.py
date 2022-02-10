from solcx import compile_standard, install_solc
from web3 import Web3
import json

with open(
    "./SimpleStorage.sol", "r"
) as file:  # all the code will run after the : and then we'll close the compiler
    simple_storage_file = file.read()  # we read our file

    # Compile Our Soldiity
    install_solc("0.6.0")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

# save compiled Solidity code to compiled_code.json file
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# gert bytecode, the succession of [] is just walking down the json of the compilation
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# for connecting to ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 1337
# we take one of our fake accounts in the ganache chain and the private key associatede to it to be able to sign our transactions
my_address = "0x3FbAc6bD5F26003327EB51D6aA1D8DdC84d4b8E8"
private_key = "0x28f86b833c424c21d963e2c37ade57eb99e26044a63701aceb7afc3f5bb0a795"

# Create the contract in Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)

# Building a transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce}
)

# Signing the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# Sending our transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)


# Working with the contract
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Call -> Simulate making the call and getting return value
# Transact -> Actually make a state change

# initial value is 0 !
print(simple_storage.functions.retrieve().call())

# We need to make a transaction to store a new value

store_transaction = simple_storage.functions.store(15).buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce + 1}
)

signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
