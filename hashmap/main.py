import numpy as np
import matplotlib.pyplot as plt


n_conflicts_x = []
n_conflicts_y = []

for j in range(10):
    n = 1<<(10+j)
    n_conflicts_x.append(n)
    m = 1<<20

    map = np.zeros(m)

    def hash(data):
        global m
        bitmap = 1 << 60
        bitmap -= 1
        key = data & bitmap
        return key % m

    hash_all = np.vectorize(hash)

    data = np.random.randint(0, high=1<<63, size=n)
    hashed_data = hash_all(data)

    n_conflicts_y.append(0)

    for i in range(n):
        k = hashed_data[i]
        if map[i] != 0:
            n_conflicts_y[j] += 1

        map[k] = k

    n_conflicts_y[j] /= n

plt.plot(n_conflicts_x, n_conflicts_y)

plt.show()