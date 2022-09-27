import numpy as np
from scipy.ndimage import convolve
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


#size_y = math.ceil(len(shapes) ** 0.5)
#size_x = math.ceil(len(shapes) / size_y)
#rows = []
#for j in range(size_x):
#    conc = np.concatenate(shapes[size_y * j : size_y * (j + 1)], axis= 0)
#    conc.resize((dim*size_y, dim))
#    rows.append(conc)


#fig, ax = plt.subplots()
#imshow = plt.imshow(np.concatenate(rows, axis = 1))

#plt.show()