import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve
from matplotlib.animation import FuncAnimation

# Mixture between primitve hashlife and optimal compuations using accelerated convolution functions

# Define Kernels
kernel = np.ones((3,3))
kernel[1,1] = 0

# Params
n_grid = 512 + 2
n_supergrid = 12
speedup = 10

# Define data structures
supergrid = np.zeros((n_supergrid, n_supergrid, n_grid, n_grid))
supergrid[2, 2, 1:-1, 1:-1] = np.random.rand(n_grid - 2, n_grid - 2) > 0.7

map = dict()
flat = np.zeros((n_supergrid * n_grid, n_supergrid * n_grid))

# helper functions
def grid_to_hash(grid):
    a = sum(grid)
    a *= np.linspace(1, 9, num=n_grid)
    return sum(a)

def evolve_grid(grid):  
    surround = convolve(grid.astype(int), kernel, mode='wrap', cval=0)
    grid = \
        np.logical_or(surround == 3,
        np.logical_and(surround == 2, grid))

    return grid

def flatten(flat, supergrid, n_supergrid, n_grid):
    for i in range(n_supergrid):
        for j in range(n_supergrid):
            flat[i*n_grid:(i+1)*n_grid, j*n_grid:(j+1)*n_grid] = supergrid[i, j, :, :]


flatten(flat, supergrid, n_supergrid, n_grid)    
fig, ax = plt.subplots()
imshow = plt.imshow(flat)

def update(t):

    for k in range(speedup):
        print('update ', t)
        # center
        for i in range(n_supergrid):
            for j in range(n_supergrid):
                hash = grid_to_hash(supergrid[i, j, :, :])
                
                if hash in map:
                    next_hash, supergrid[i, j, :, :] = map[hash]
                else:
                    supergrid[i, j, :, :]= evolve_grid(supergrid[i, j, :, :])
                    map[hash] = ( grid_to_hash(supergrid[i, j, :, :]), supergrid[i, j, :, :])

        # update ghost cells
        for i in range(n_supergrid):
            for j in range(n_supergrid):
                
                # Reset ghost cells from self
                supergrid[i, j, :, 0] = 0
                supergrid[i, j, :, -1] = 0
                supergrid[i, j, 0, :] = 0
                supergrid[i, j, -1, :] = 0

                # Fetch ghost cells from neighbours
                n = n_supergrid
                # lower line fetches from lower upper line
                supergrid[i, j, 1:-1, 0] = supergrid[i, (j-1)%n, 1:-1, -2]
                # upper line fetches from upper lower line
                supergrid[i, j, 1:-1, -1] = supergrid[i, (j+1)%n, 1:-1, 1]
                # left line fetches from left right line
                supergrid[i, j, 0, 1:-1] = supergrid[(i-1)%n, j, -2, 1:-1]
                # right line fetches from right left line
                supergrid[i, j, -1, 1:-1] = supergrid[(i+1)%n, j, 1, 1:-1]

                # corner points, not done yet
                #supergrid[i, j, 0, 0] = supergrid[i, (j+1)%n_supergrid, 1:-2, -2]
                #supergrid[i, j, 0, -1] = supergrid[i, (j-1)%n_supergrid, 1:-2, 1]
                #supergrid[i, j, -1, 0] = supergrid[(i+1)%n_supergrid, j, -2, 1:-2]
                #supergrid[i, j, -1, -1] = supergrid[(i+1)%n_supergrid, j, 1, 1:-2]


    flatten(flat, supergrid, n_supergrid, n_grid)
    imshow.set_data(flat)

ani = FuncAnimation(fig, update, frames=np.linspace(0, 2001, num=2000), interval=300, repeat=False)

plt.show()