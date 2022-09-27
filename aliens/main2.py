import random
import numpy as np
from matplotlib import pyplot as plt


alien = (np.random.rand(2)-[0,0.5])*100
print(alien)

n = 1000

def sample(n, thetas):
    signals_y = []
    # Generate signal data
    for i in range(n):

        dx = alien[0]
        d = dx / np.cos(theta)
        dy = d * np.sin(theta)

        signals_y.append(dy)

    return signals_y
truth = sample(1000, random.uniform(-np.pi/2, np.pi/2))

counts, edges, bars = plt.hist(signals_y, range = (-300, 300), bins=50)
plt.bar_label(bars)


maxP = 0
for i in range(100):
    for j in range(-50, 50):
        dx = i
        dy 
        p = 0

        if maxP:
            continue

plt.show()