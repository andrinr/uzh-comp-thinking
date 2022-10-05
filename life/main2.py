from copy import copy
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve
from matplotlib.animation import FuncAnimation

import time


x = 50
y = 200

grid = np.zeros((x, y))

cx = 25
cy = 20
k = 5

init = np.random.rand(2*k, 2*k) > 0.5

grid[cx - k: cx + k, cy - k: cy + k] =  init

# Define Kernels
kernel = np.ones((3,3))
kernel[1,1] = 0
print(kernel)
fig, ax = plt.subplots()
imshow = plt.imshow(grid)

tmp = np.array(grid, copy=True)  

# update function
distance = 0
counter = 0

distances_hist = np.zeros(10)
def update(i):
    global distance
    global grid
    global counter

    surround = convolve(grid.astype(int), kernel, mode='wrap', cval=0)
    
    grid = \
        np.logical_or(surround == 3,
        np.logical_and(surround == 2, grid))

    grid[:,y-1] = 0
    other, candidates = np.nonzero(grid)
    if np.all((grid == 0)):
        distance = 0
        return

    distance = max(np.max(candidates), distance)

    #np.roll(distances_hist, 1)
    #distances_hist[0] = distance

    #avg = np.average(distances_hist)
    #print(prev_avg, avg)
    #return avg > prev_avg or i < 20


# evolution
g_max_distance = 0
max_init = np.copy(init)
for g in range(200):
    
    distance = 0
    for t in range(300):
        update(t)

    if distance > g_max_distance:
        g_max_distance = distance
        max_init = np.copy(init)
    else:
        init = max_init

    print(g_max_distance, distance, t)

    rand = np.random.rand(2*k, 2*k) > 0.9
    init[rand] = np.invert( init  )[rand]

    grid = np.zeros((x,y))
    grid[cx - k: cx + k, cy - k: cy + k] = init

# plotting
def update_anim(i):
    update(i)
    imshow.set_data(grid)

grid = np.zeros((x,y))
grid[cx - k: cx + k, cy - k: cy + k] = max_init
ani = FuncAnimation(fig, update_anim, frames=np.linspace(0, 1000, 1), interval=100, repeat=True)

plt.show()