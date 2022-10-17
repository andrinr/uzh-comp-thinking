import numpy as np
import matplotlib.pyplot as plt

n_conflicts_x = []
n_conflicts_y = []

for j in range(10):
    n = 1<<(10+j)
    n_conflicts_x.append(n)
    m = 1<<20

    map = np.zeros(m)

    def hash_simple_masking(data):
        global m
        bitmap = m
        bitmap -= 1
        key = data & bitmap
        return key % m

    def hash_2(data):
        global m
        bitmap = m
        bitmap -= 1
        key = (data * 122478809) & bitmap
        return key % m

    hash_all = np.vectorize(hash_simple_masking)

    data_uniform = np.random.randint(0, high=1<<63, size=n>>4)
    np.interp(np.linspace(0,1, n>>4), data_uniform, np.linspace(0,1, n>>4))

    mu, sigma = 1, 0.1 # mean and standard deviation
    #data_normal = np.random.normal(mu, sigma, size=n) + 0.5 * 10**10
    hashed_data = hash_all(data_uniform)

    n_conflicts_y.append(0)

    for i in range(n):
        k = hashed_data[i]
        if map[k] != 0:
            n_conflicts_y[j] += 1

        map[k] = 1

    n_conflicts_y[j] /= n


plt.plot(n_conflicts_x, n_conflicts_y)

plt.show()