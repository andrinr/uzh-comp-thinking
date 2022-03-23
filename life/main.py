from glob import glob
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve
from matplotlib.animation import FuncAnimation

x = 20
y = 20

grid = np.random.rand(x, y) > 0.7

# Define Kernels
kernel = np.ones((3,3))
kernel[1,1] = 0

print(kernel)
fig, ax = plt.subplots()
imshow = plt.imshow(grid)

def update(i):
    global grid

    surround = convolve(grid.astype(int), kernel, mode='constant', cval=0)
    print(grid)
    print(surround)
    grid = \
        np.logical_or(\
            np.logical_and(surround == 3, np.logical_not(grid)),\
            np.logical_and(np.logical_and(surround >= 2, surround <= 3), grid))

    imshow.set_data(grid)

    print(i)


ani = FuncAnimation(fig, update, frames=np.linspace(0, 1000, 1), interval=1000, repeat=True)

plt.show()