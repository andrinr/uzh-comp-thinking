import numpy as np

def hash(grid):

    sum0 = np.sum(grid, 0)
    sum1 = np.sum(grid, 1)

    return np.array2string(sum0[sum0 != 0]), np.array2string(sum1[sum1 != 0])

grid = np.random.rand(5, 5) > 0.7


def check_symmetric(hash1x, hash1y, hash2x, hash2y):
    if 

print(hash(grid))