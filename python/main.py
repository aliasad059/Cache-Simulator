# Cache Simulator
from array import array
from sys import maxsize

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
    :param hex: check is requests list is in Hex base or not
    :type hex: bool
    """
    dmc = array('L', [maxsize for _ in range(CACHE_SIZE)])    
    cache_index = [request%CACHE_SIZE for request in requests]
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


print(direct_mapping(requests, hexa))