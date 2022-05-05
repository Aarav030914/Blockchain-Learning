from solcx import compile_standard

from web3 import Web3

#just to print the version of web3 library being used
import web3
print(web3.__version__)

import os
import json 
from dotenv import load_dotenv
load_dotenv()

# Get the solidity to be compiled
with open("./SimpleStorage.sol") as file:
    simple_storage_content = file.read()

compile = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_content}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        }
    },
    solc_version="0.6.0"
)

with open("compiled_code.json", "w") as file:
    json.dump(compile, file)

# get bytecode
bytecode = compile["contracts"]["SimpleStorage.sol"]["simplestorage"]["evm"]["bytecode"]["object"]

# get abi
abi = json.loads(
    compile["contracts"]["SimpleStorage.sol"]["simplestorage"]["metadata"]
)["output"]["abi"]

# connecting to ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 1337
address = os.getenv("ADDRESS")
private_key = os.getenv("PRIVATE_KEY")

# Create the contract in python
simplestorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the latest transaction
nonce = w3.eth.getTransactionCount(address)

transaction = simplestorage.constructor().buildTransaction({
    "chainId": chain_id,
    "gasPrice": w3.eth.gas_price,
    "from": address,
    "nonce": nonce
})
# Sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# Send the transaction hash
txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# Wait for the transaction to be completed
txn_reciept = w3.eth.wait_for_transaction_receipt(txn_hash)



# Working with deployed
simple_storage = w3.eth.contract(address=txn_reciept.contractAddress, abi=abi)

#To call the add function in solidity we need to make changes to the blockchain, thus need to build a transaction
add_transaction = simplestorage.functions.store(10).buildTransaction({
    "chainId": chain_id,
    "gasPrice": w3.eth.gas_price,
    "to":"0xA3Cb86E4C26FA8502F8740A47f8f27fa474f4299",
    "from": address,
    "nonce": nonce + 1,
    })

add_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

send_add_tnx = w3.eth.send_raw_transaction(add_txn.rawTransaction)
txn_reciept = w3.eth.wait_for_transaction_receipt(send_add_tnx)

print(simple_storage.functions.retrieve().call())



