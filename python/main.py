# Cache Simulator
from array import array
from collections import deque
from sys import maxsize
import termtables

# these sizes are in Byte
BLOCK_SIZE = 2
CACHE_SIZE = 8
MEMORY_SIZE = 1

requests = list()
hexa = True if input("Your input is in Hex(Y/n): ").lower() == 'y' else False
inputs = input("Enter your cpu requests: ").split()
if not hexa:
    requests = list(map(int, inputs))
else: 
    requests = list(map(lambda x:int(x, base=16), inputs))
BLOCK_SIZE = int(input("Size of Block (words no.): "))
CACHE_SIZE = int(input("Size of Cache (words no.): "))
MEMORY_SIZE = int(input("Size of Memory (words no.): "))


def draw_table(cache: list(deque()), block_num: int, k:int) -> None:
    """
    Draw cache as a table in console

    :param cache: data that is in cache
    :type cache: list (deque())
    :param block_num: block numbers in cache
    :type block_num: int
    :param k: number of sets in cache
    :type k: int 
    """
    header = ['#'] + [f"way {i}" for i in range(k)]
    data = [[f'set {i}'] + ["    " for _ in range(k)] for i in range(block_num)]
    
    for i in range(len(cache)):
        for j in range(len(cache[i])):
            block_num = cache[i][j]
            word_list = [BLOCK_SIZE * block_num + k for k in range(BLOCK_SIZE)]
            data[i][j+1] = f"<{block_num}> {word_list}"

    print(85*'-')
    termtables.print(data, header=header)


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

        print('request:', requests[i])
        print('Hit' if result[i] == 1 else 'Miss')
        draw_table(dmc, block_num, 1)

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
    if block_num == 0:
        print("[Error] your entered properties isn't correct.\nCause:  block_num == 0 ")
        return []
    kwsa = [deque(maxlen=k) for _ in range(block_num)]
    requests_block = [request // BLOCK_SIZE for request in requests]
    cache_index = [request % block_num for request in requests_block]
    result = []
    draw_table(kwsa, block_num, k)
    
    if policy.upper() == 'FIFO':
        for i in range(len(requests)):
            if requests_block[i] in kwsa[cache_index[i]]:
                result.append(1)
            else:
                result.append(0)
                kwsa[cache_index[i]].append(requests_block[i])

            print('request:', requests[i])
            print('Hit' if result[i] == 1 else 'Miss')
            draw_table(kwsa, block_num, k)

    elif policy.upper() == 'LRU':
        for i in range(len(requests)):
            if requests_block[i] in kwsa[cache_index[i]]:
                result.append(1)
            else:
                result.append(0)
            kwsa[cache_index[i]].append(requests_block[i])

            print('request:', requests[i])
            print('Hit' if result[i] == 1 else 'Miss')
            draw_table(kwsa, block_num, k)

    else:
        print("[Warning]: your entered policy is not in accepted policies.\nvalid policies: ['FIFO', 'LRU']")
        return

    hit_rate = sum(result)/len(result)
    if hexa:
        requests_hex = [hex(request) for request in requests]
        return list(zip(requests_hex, result)), hit_rate
    return list(zip(requests, result)), hit_rate

if __name__ == "__main__":
    # print(direct_mapping(requests, hexa))
    k = int(input("Enter k: "))
    print('\nvalid policies:\n(1) LRU\n(2) FIFO\n')
    policy_n = int(input("Enter Policy number: "))
    policy = 'LRU' if policy_n == 1 else 'FIFO'
    result = k_way_set_associative(k, requests, policy)
    if result:
        print(result)