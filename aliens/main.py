# Imports
import random
import numpy as np
from matplotlib import pyplot as plt


# Set positions
earth_x, earth_y = 0, 50
alien_x, alien_y = 5, 55

detectors = np.zeros(100)

n_signals = 50000


# Generate signal data
for signal in range(n_signals):
    theta = random.uniform(-np.pi/2, np.pi/2)
    dx = alien_x - earth_x
    d = dx / np.cos(theta)
    dy = d * np.sin(theta)
    detector_y = int(alien_y + round(dy))
    if 0 <= detector_y <= len(detectors)-1:
        detectors[detector_y] += 1

# Plot data
plt.plot(detectors)
plt.show()