import numpy as np
from scipy.ndimage import convolve
import matplotlib.pyplot as plt

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

def solve(grid, pieces, max, dict, shapes):
    h1, h2, h1r, h2r = hash(grid)

    if (h1 + h2) in dict or (h2 + h1) in dict or\
        (h1r + h2) in dict or (h2 + h1r) in dict or\
        (h1 + h2r) in dict or (h2r + h1) in dict or\
        (h1r + h2r) in dict or (h2r + h1r) in dict:
        return 0
    else:
        dict[h1+h2] = grid

    if pieces == max:
        shapes.append(grid)
        return 1
    
    surround = convolve(grid.astype(int), kernel, mode='constant', cval=0)
    indices = zip(*np.where(np.logical_and(surround > grid, np.logical_not(grid))))

    sum = 0
    for i, j in indices:
        grid_ = np.copy(grid)
        grid_[i, j] = 1
        sum += solve(grid_, pieces + 1, max, dict, shapes)

    return sum

n = int(input("Number of tiles: "))

init = np.zeros((n*2,n*2))
init[n, n] = 1

d = dict()

shapes = []
c = solve(init, 1, n, d, shapes)
size_x = round(c ** 0.5)
size_y = round(1+ (c / size_x))

print(shapes)
rows = []
for j in range(size_y):
    rows.append(np.concatenate(shapes[size_x * j : size_x * (j + 1)]))

print("Number of possible shapes: ", c)

fig, ax = plt.subplots()
imshow = plt.imshow(np.concatenate(rows))

plt.show()