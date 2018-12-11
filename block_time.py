```
Based on https://github.com/jgarzik/python-bitcoinrpc
```

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from datetime import datetime
from sys import argv, exit
    
# rpc_user and rpc_password are set in the bitcoin.conf file
if len(argv) != 4:
	print("Usage: python block_time.py nodeAddress:rpcPort rpcUser rpcPassword")
	exit(1)

nodeAddr = argv[1]
nodeUser = argv[2]
nodePass = argv[3]

rpc_connection = AuthServiceProxy("http://{}:{}@{}".format(nodeUser, nodePass, nodeAddr))
best_block_hash = rpc_connection.getbestblockhash()
tip = rpc_connection.getblock(best_block_hash)
# print(tip)

# batch support : print timestamps of blocks 0 to 99 in 2 RPC round-trips:
commands = [ [ "getblockhash", height] for height in range(tip["height"] + 1) ]
block_hashes = rpc_connection.batch_(commands)
blocks = rpc_connection.batch_([ [ "getblock", h ] for h in block_hashes ])
block_times = [ block["time"] for block in blocks ]
print(block_times)

N = len(block_times)

def average_diff(times):
    num = len(times)
    sum = 0
    for i in range(1, num):
        sum += times[i] - times[i-1]
    return sum/num
    
for i in range(1, N):
    block_time = block_times[i]
    hash_time = block_time - block_times[i-1]
    timestamp = datetime.utcfromtimestamp(block_time).strftime('%Y-%m-%d %H:%M:%S')
    if i > 6:
        window = block_times[i-6:i+1]
        time_avg = average_diff(window)
    else:
        time_avg = 0
        
    print('{:>5}, {}, {:>5}, {:8.2f}'.format(i, timestamp, hash_time, time_avg))
    


