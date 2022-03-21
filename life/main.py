import numpy as np
from scipy.ndimage import convolve

x = 50
y = 50

grid = np.random.rand(x, y) > 0.8

print(grid)

# Define Kernels
kernel = np.ones((3,3))
kernel[1,1] = 0

def step():
    surround = convolve(grid, kernel, mode='constant', cval=0)

    new = surround == 3 and not grid
    new = not(surround <= 1 and grid) and grid
    dead = 
