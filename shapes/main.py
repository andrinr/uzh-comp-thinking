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
init = np.zeros((dim, dim))
init[round(dim/2), round(dim/2)] = 1

d = dict()

shapes = []

stack.append((init, 1))

while len(stack) > 0:
    grid, pieces = stack.pop()

    h1, h2, h1r, h2r = hash(grid)

    if (h1 + h2) in d:
        continue

    else:
        # all possible permutations
        d[h1+h2] = True
        d[h2+h1] = True

        d[h1r+h2] = True
        d[h2+h1r] = True

        d[h1+h2r] = True
        d[h2r+h1] = True

        d[h1r+h2r] = True
        d[h2r+h1r] = True
        

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
        stack.append((grid_, pieces + 1))



print("Number recursions:", len(d.values()))
print("Number of possible shapes: ", total)


size_y = math.ceil(len(shapes) ** 0.5)
size_x = math.ceil(len(shapes) / size_y)
rows = []
for j in range(size_x):
    conc = np.concatenate(shapes[size_y * j : size_y * (j + 1)], axis= 0)
    conc.resize((dim*size_y, dim))
    rows.append(conc)


fig, ax = plt.subplots()
imshow = plt.imshow(np.concatenate(rows, axis = 1))

plt.show()