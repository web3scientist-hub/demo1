import json
import time

from web3 import Web3, HTTPProvider

w3 = Web3(HTTPProvider("https://rpc-bsc.48.club"))

# 鸟币合约
tokenAddress = Web3.to_checksum_address('0xde6e12bdb2062dc48b409f0086219464a0c317a0');
# 自己部署的智能合约地址
my_deploy_contract = Web3.to_checksum_address('xx')
# 自己钱包的公私钥
my_address = Web3.to_checksum_address("xx")
my_private_key = "xx"
# 空投钱包文件
file_path = '../address.txt'
# 批量空投，每批100个钱包
batch_size = 100
# 每人空投1亿
amount = w3.to_wei(10 ** 8, 'ether')

abi = open('abi/batch_niao_con.json', "r")
contract_obj = w3.eth.contract(address=my_deploy_contract, abi=json.loads(abi.read()))


def airdropNiao():
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.readlines()
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            addressList = []
            for j in range(0, len(batch)):
                addressList.append(Web3.to_checksum_address(batch[j].strip()))

            transaction = contract_obj.functions.batchTransfer(tokenAddress, addressList, amount).build_transaction(
                {
                    "gas": 5000000,
                    "gasPrice": 10 ** 9,  # 1GWei
                    "from": my_address,
                    "nonce": w3.eth.get_transaction_count(my_address),
                }
            )
            # 签名交易
            signed_txn = w3.eth.account.sign_transaction(transaction, private_key=my_private_key)
            # 发送交易
            send_tx = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            print("tx:", send_tx.hex())
            time.sleep(30)


airdropNiao()
