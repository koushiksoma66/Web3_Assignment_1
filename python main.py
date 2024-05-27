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
        for i in range(0,len(valid_txid_hashes),2):
            if i==(len(valid_txid_hashes)-1): temp_list.append(hash(valid_txid_hashes[i]+valid_txid_hashes[i]))
            else: temp_list.append(hash(valid_txid_hashes[i]+valid_txid_hashes[i+1]))
        valid_txid_hashes = temp_list

    return valid_txid_hashes[0]

    

mempool_path = r'C:\Users\koush\Downloads\VS Code files\Web3 Assignment\mempool'
mempool = os.listdir(mempool_path) # Makes a list of path of all the files in the mempool

count=0
valid_txid_list = []

for file_path in mempool:
    with open(os.path.join(mempool_path,file_path),'r') as file:
        transaction = json.load(file)
        if(validate(transaction)):
            valid_txid_list.append(os.path.basename(file_path).split('.')[0])
            count += 1


merkle_root_ = cal_merkel_root(valid_txid_list)

## Header Components


version = "01000000"
previous_block_hash = "0000000000000000000000000000000000000000000000000000000000000000"
merkle_root = f"{merkle_root_}"
time_stamp = f'{hex(int(time.time())).split('x')[1]}'
difficulty_target = "0000ffff00000000000000000000000000000000000000000000000000000000"
nonce = 0

# Concating header components
header_without_nonce = version+previous_block_hash+ merkle_root+time_stamp

## Nonce calculation

while True:  # Can't write it as while header_hash>difficuly_target since, for that header_hash must be declared outside the loop
    header = header_without_nonce + str(hex(nonce))
    header_hash = hash(header)
    if int(header_hash,16)<int(difficulty_target,16): break
    nonce += 1



