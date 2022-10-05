import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve
from matplotlib.animation import FuncAnimation

import time


# Define Kernels
kernel = np.ones((3,3))
kernel[1,1] = 0

n_grid = 8
n_supergrid = 5

supergrid = np.zeros((n_supergrid, n_supergrid, n_grid, n_grid))
print(np.shape(supergrid))

map = dict()
flat = np.zeros((n_supergrid * n_grid, n_supergrid * n_grid))

def grid_to_hash(grid):
    return grid.tobytes()

def hash_to_grid(hash):
    return np.frombuffer(hash, dtype=int)

def evolve_grid(grid):
    surround = convolve(grid.astype(int), kernel, mode='wrap', cval=0)
    grid = \
        np.logical_or(surround == 3,
        np.logical_and(surround == 2, grid))

def flatten(flat, supergrid, n_supergrid, n_grid):
    
    for i in range(n_supergrid):
        for j in range(n_supergrid):
            flat[i*n_grid:(i+1)*n_grid, j*n_grid:(j+1)*n_grid] = supergrid[i, j, :, :]

    
fig, ax = plt.subplots()
imshow = plt.imshow(flat)

def update(t):

    # center
    for i in range(n_supergrid):
        for j in range(n_supergrid):
            hash = grid_to_hash(supergrid[i, j, :, :])
            print(hash)
            if hash in map:
                print(hash_to_grid(map[hash]))
                supergrid[i, j, :, :] = hash_to_grid(map[hash])
            else:
                tmp_hash = grid_to_hash(supergrid[i, j, :, :])
                evolve_grid(supergrid[i, j, :, :])
                map[tmp_hash] = grid_to_hash(supergrid[i, j, :, :])

    # update ghost cells
    for i in range(n_supergrid):
        for j in range(n_supergrid):
            
            # Reset ghost cells from self
            supergrid[i, j, 0:-1, 0] = 0
            supergrid[i, j, 0:-1, -1] = 0
            supergrid[i, j, 0, 0:-1] = 0
            supergrid[i, j, -1, 0:-1] = 0

            # corner lines
            supergrid[i, j, 1:-2, 0] = supergrid[i, (j+1)%n_supergrid, 1:-2, -2]
            supergrid[i, j, 1:-2, -1] = supergrid[i, (j-1)%n_supergrid, 1:-2, 1]
            supergrid[i, j, 0, 1:-2] = supergrid[(i+1)%n_supergrid, j, -2, 1:-2]
            supergrid[i, j, -1, 1:-2] = supergrid[(i+1)%n_supergrid, j, 1, 1:-2]

            # corner points
            #supergrid[i, j, 0, 0] = supergrid[i, (j+1)%n_supergrid, 1:-2, -2]
            #supergrid[i, j, 0, -1] = supergrid[i, (j-1)%n_supergrid, 1:-2, 1]
            #supergrid[i, j, -1, 0] = supergrid[(i+1)%n_supergrid, j, -2, 1:-2]
            #supergrid[i, j, -1, -1] = supergrid[(i+1)%n_supergrid, j, 1, 1:-2]


    flatten(flat, supergrid, n_supergrid, n_grid)
    imshow.set_data(flat)

ani = FuncAnimation(fig, update, frames=np.linspace(0, 1000, 1), interval=300, repeat=True)

plt.show()