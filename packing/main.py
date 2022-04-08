import numpy as np
from scipy.ndimage import convolve
from scipy.ndimage import label
from scipy import ndimage
import matplotlib.pyplot as plt
import math

def hash(grid):
    sum0 = np.sum(grid, 0)
    sum1 = np.sum(grid, 1)

    sum0 = sum0[sum0 !=0]
    sum1 = sum1[sum1 !=0]

    return str(sum0), str(sum1), str(sum0[::-1]), str(sum1[::-1])

def hash2(grid):
    rot = np.rot90(grid)
    return [str(grid), str(np.flip(grid, 0)), str(np.flip(grid, 1)), str(np.flip(np.flip(grid, 1),0)),\
        str(rot), str(np.flip(rot, 0)), str(np.flip(rot, 1)), str(np.flip(np.flip(rot, 1),0))]

# Define Kernels
kernel = np.ones((3,3))
kernel[0,0] = 0
kernel[2,2] = 0
kernel[0,2] = 0
kernel[2,0] = 0

stack = []
total = 0

n = int(input("Number of tiles: "))
dim = math.ceil(n * 2)
init = np.zeros((3, 3))
init[1, 1] = 1

d = dict()

shapes = []

stack.append((init, 1))

while len(stack) > 0:
    grid, pieces = stack.pop()

    hashes = hash2(grid)

    if hashes[0] in d:
        continue

    else:
        for h in hashes:
            d[h] = True
        
    if pieces == n:
        total += 1
        shapes.append(grid)
        continue
    
    surround = convolve(grid.astype(int), kernel, mode='constant', cval=0)
    indices = zip(*np.where(np.logical_and(surround > grid, np.logical_not(grid))))

    sum = 0
    for i, j in indices:
        grid_ = np.copy(grid)
        grid_[i, j] = 1
        dim0, dim1 = np.shape(grid_)
        if i == 0:
            grid_ = np.pad(grid_, ((1, 0), (0, 0)))
        if i == dim0 - 1:
            grid_ = np.pad(grid_, ((0, 1), (0, 0)))

        if j == 0:
            grid_ = np.pad(grid_, ((0, 0), (1, 0)))
        if j == dim1 - 1:
            grid_ = np.pad(grid_, ((0, 0), (0, 1)))
        
        stack.append((grid_, pieces + 1))

print("Number recursions:", len(d.values()))
print("Number of possible shapes: ", total)


# Check if shapes with n = 6 can shape a box
# Find algorithm for it 
# Exhaustive search
# Must 35 * 6 = 7 * 5 * 3 * 2 = i.e. many different boxes

# Give number of 

# If we reach something a grid where we have a connected hole with 5 or less tiles this means its an invalid leaf


grid_sizes = [(7*3, 5*2), (7*2, 5*3), (3*2, 7*5)]

x, y = grid_sizes[0]

board = np.zeros((x,y))

def check(board, n):
    labeled_array, num_features = ndimage.label(np.logical_not(board))
    s = ndimage.sum(board, labeled_array, index=[n for n in range(1,num_features)])

    return min(s) > n


board[1,1] = 1
board[0,1] = 1
board[1,0] = 1

print(check(board, 2))