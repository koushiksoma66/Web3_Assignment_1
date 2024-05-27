import os
import json
import hashlib
import time

def validate(transaction):
    input_value = 0
    output_value = 0

    for input in transaction['vin']:
        input_value += input['prevout']['value']
    for output in transaction['vout']:
        output_value += output['value']

    if(input_value>output_value): return True
    else: return False


def hash(str):
    return hashlib.sha256(str.encode('utf-8')).hexdigest()


def cal_merkel_root(valid_txid_list):

    valid_txid_hashes = []
    for txid in valid_txid_list:
        valid_txid_hashes.append(hash(txid))

    while(len(valid_txid_hashes)>1):
        temp_list = []
        for i in range(0,len(valid_txid_hashes),2):  #Takes steps of size 2
            if i==(len(valid_txid_hashes)-1): temp_list.append(hash(valid_txid_hashes[i]+valid_txid_hashes[i]))
            else: temp_list.append(hash(valid_txid_hashes[i]+valid_txid_hashes[i+1]))
        valid_txid_hashes = temp_list

    return valid_txid_hashes[0]

    

current_directory = os.path.dirname(os.path.abspath(__file__))  # Gives the path of the current directory
mempool_path = os.path.join(current_directory, 'mempool') # Gives the path of the file/folder named mempool in the current directory
mempool = os.listdir(mempool_path) # Makes a list of name of all the files in the mempool


valid_txid_list = []

for file_name in mempool:
    with open(os.path.join(mempool_path,file_name),'r') as file:
        transaction = json.load(file)
        if(validate(transaction)):
            valid_txid_list.append(file_name.split('.')[0]) # Removes .json extension from the file name


merkle_root_ = cal_merkel_root(valid_txid_list)

## Header Components


version = "01000000"
previous_block_hash = "0000000000000000000000000000000000000000000000000000000000000000"
merkle_root = f"{merkle_root_}"
time_stamp = f'{hex(int(time.time())).split('x')[1]}' # Converted the time_stamp into hexadecimal and removed the 0x part in the beginning
difficulty_target = "0000ffff00000000000000000000000000000000000000000000000000000000"
nonce = 0

# Concating header components
header_without_nonce = version+previous_block_hash+ merkle_root+time_stamp # Nonce should be added inside the loop so that the header_hash can get updated in each iteration

## Nonce calculation

while True:  # Can't write it as "while header_hash>difficuly_target" since, for that header_hash must be declared outside the loop
    header = header_without_nonce + str(hex(nonce)) 
    header_hash = hash(header)
    if int(header_hash,16)<int(difficulty_target,16): break
    nonce += 1


text_to_be_printed = f"""Block Header:
{{
  "version": 1,
  "previous_block_hash": "0000000000000000000000000000000000000000000000000000000000000000",
  "merkle_root": "{merkle_root_}",
  "timestamp": {int(time.time())},
  "difficulty_target": "0000ffff00000000000000000000000000000000000000000000000000000000",
  "nonce": {nonce}
}}

Serialized Coinbase Transaction:
{{
  "txid": "4a7b8a1f3f6b3a9b8a1f3f6b3a9b8a1f3f6b3a7b8a1f3f6b3a9b8a1f3f6b3a9b",
  "vin": [
    {{
      "coinbase": "04ffff001d0104455468652054696d65732030332f4a616e2f32303233204368616e63656c6c6f72206f6e20626974636f696e2062756c6c",
      "sequence": 4294967295
    }}
  ],
  "vout": [
    {{
      "value": 5000000000,
      "scriptPubKey": "4104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac"
    }}
  ]
}}

Transaction IDs:
"""

with open('output.txt','w') as file:
    file.write(text_to_be_printed)
    file.write('"4a7b8a1f3f6b3a9b8a1f3f6b3a9b8a1f3f6b3a7b8a1f3f6b3a9b8a1f3f6b3a9b"\n')
    for txid in valid_txid_list:
        file.write(f'"{txid}"\n')


