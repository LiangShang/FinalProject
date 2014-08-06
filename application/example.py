from multiprocessing import Pool
from time import time
import sys

K = 50
def CostlyFunction((z,)):
    r = 0
    for k in xrange(1, K+2):
        r += z ** (1 / k**1.5)
    return r

if __name__ == '__main__':
    processes = int(sys.argv[-1])
    r = int(sys.argv[1])
    pool = Pool(processes=processes)
    res = pool.map(CostlyFunction, [(i,) for i in range(r)])
    print sum(res)
