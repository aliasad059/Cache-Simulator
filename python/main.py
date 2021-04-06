# Cache Simulator
from array import array
from collections import deque
from sys import maxsize

# these sizes are in Byte
BLOCK_SIZE = 1
CACHE_SIZE = 4
MEMORY_SIZE = 1

requests = list()
hexa = True if input("Your input is in Hex(Y/n): ").lower() == 'y' else False
inputs = input("Enter your cpu requests: ").split()
if not hexa:
    requests = list(map(int, inputs))
else: 
    requests = list(map(lambda x:int(x, base=16), inputs))


def direct_mapping(requests: list, hexa=False) -> list:
    """
    This method is implementation of Direct Mapped Cache Simulation
    
    :param requests: list of cpu requests in Hexadecimal
    :type requests: list
    :param hexa: check is requests list is in Hex base or not
    :type hexa: bool
    """
    block_num = CACHE_SIZE / BLOCK_SIZE 
    dmc = array('L', [maxsize for _ in range(CACHE_SIZE)])
    cache_index = [request % block_num for request in requests]
    result = []
    for i in range(len(requests)):
        if requests[i] == dmc[cache_index[i]]:
            result.append(1)
        else:
            result.append(0)
            dmc[cache_index[i]] = requests[i]

    hit_rate = sum(result)/len(result)
    if hexa:
        requests_hex = [hex(request) for request in requests]
        return list(zip(requests_hex, result)), hit_rate
    return list(zip(requests, result)), hit_rate


def k_way_set_associative(k: int, requests: list, policy: str, hexa=False) -> list:
    """
    This method is implementation of K Way Set Associative Cache Simulation

    :param k: length of each set in cache
    :type k: int
    :param requests: list of cpu requests in Hexadecimal
    :type requests: list
    :param policy: valid replacement policy (LRU, FIFO)
    :type policy: str
    :param hexa: check is requests list is in Hex base or not
    :type hexa: bool
    """
    
    block_num = (CACHE_SIZE // BLOCK_SIZE) // k;
    kwsa = [deque(maxlen=k) for _ in range(block_num)]
    cache_index = [request % block_num for request in requests]
    result = []
    
    if policy.upper == 'FIFO':
        for i in range(len(requests)):
            if requests[i] in kwsa[cache_index[i]]:
                result.append(1)
            else:
                result.append(0)
                kwsa[cache_index[i]].append(requests[i])

            print('cache:', kwsa, 'request:', requests[i])

    elif policy.upper == 'LRU':
        for i in range(len(requests)):
            if requests[i] in kwsa[cache_index[i]]:
                result.append(1)
            else:
                result.append(0)
            kwsa[cache_index[i]].append(requests[i])

            print('cache:', kwsa, 'request:', requests[i])

    else:
        print("[Warning]: your entered policy is not in accepted policies.\nvalid policies: ['FIFO', 'LRU']")
        return

    hit_rate = sum(result)/len(result)
    if hexa:
        requests_hex = [hex(request) for request in requests]
        return list(zip(requests_hex, result)), hit_rate
    return list(zip(requests, result)), hit_rate

# print(direct_mapping(requests, hexa))
print(k_way_set_associative(2, requests, 'LRU'))