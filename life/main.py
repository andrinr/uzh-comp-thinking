from glob import glob
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve
from matplotlib.animation import FuncAnimation

x = 50
y = 50

grid = np.random.rand(x, y) > 0.8

# Define Kernels
kernel = np.ones((3,3))
kernel[1,1] = 0

fig, ax = plt.subplots()
imshow = plt.imshow(grid)

def update(i):
    global grid

    surround = convolve(grid, kernel, mode='constant', cval=0)

    grid = \
        (surround == 3 and not grid) or \
        (surround >= 2 and surround <= 3 and grid)

    imshow.set_data(grid)


ani = FuncAnimation(fig, update, frames=np.linspace(0, 1000, 1), repeat=True)

plt.show()