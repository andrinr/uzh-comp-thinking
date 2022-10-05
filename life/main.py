import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve
from matplotlib.animation import FuncAnimation

import time


x = 1000
y = 1000

grid = np.random.rand(x, y) > 0.7

# Define Kernels
kernel = np.ones((3,3))
kernel[1,1] = 0

print(kernel)
fig, ax = plt.subplots()
imshow = plt.imshow(grid)

def update(i):
    global grid

    surround = convolve(grid.astype(int), kernel, mode='wrap', cval=0)

    grid = \
        np.logical_or(surround == 3,
        np.logical_and(surround == 2, grid))

    imshow.set_data(grid)

ani = FuncAnimation(fig, update, frames=np.linspace(0, 1000, 1), interval=300, repeat=True)

plt.show()