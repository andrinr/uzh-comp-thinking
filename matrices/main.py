import numpy as np

# check if two matrices can be multiplied
def check_multiplication(sizeA, sizeB):
    if sizeA[1] == sizeB[0]:
        return True
    else:
        return False

# returns the size of the resulting matrix after multiplication
def get_size(sizeA, sizeB):
    return [sizeA[0], sizeB[1]]

# returns complexity of matrix multiplication
def complexity(sizeA, sizeB):
    if not check_multiplication(sizeA, sizeB):
        return np.inf

    return sizeA[0]*sizeA[1]*sizeB[1]

# generate list of random sized matrices
def gen_matrices(n, max_size = 100):
    matrices = np.zeros((n, 2), dtype = int)
    # ensure matrices are indeed computable
    prev_size_m = np.random.randint(2, max_size)
    for i in range(n):
        size = [prev_size_m, np.random.randint(2, max_size)]
        prev_size_m = size[1]
        matrices[i] = np.array(size)
    return matrices

# generate matrices
num_matrices = 200
matrices = gen_matrices(num_matrices)
print("random matrix sequence: ", matrices)

# compute costs without any optimzation
naive_costs = 0
trailing_shape = matrices[0]
for i in range(num_matrices-2):
    naive_costs += complexity(trailing_shape, matrices[i+1])
    trailing_shape = get_size(trailing_shape, matrices[i+1])

# init DP tables
costs = np.full((num_matrices, num_matrices), np.inf)
sizes = np.zeros((num_matrices, num_matrices, 2))
sizes[1,:,:] = matrices
costs[:2,:] = 0

# evaluate DP tables, cost: O(n**3)
for l in range(2, num_matrices):
    for i in range(num_matrices - l):
        for a in range(1,l):
            b = l - a
            j = i + a

            ij = complexity(sizes[a, i], sizes[b, j])

            if costs[a,i] + costs[b,j] + ij < costs[l,i]:
                costs[l,i] = costs[a,i] + costs[b,j] + ij
                sizes[l,i] = get_size(sizes[a,i], sizes[b,j])

# fetch result from table
min_cost = costs[num_matrices-1,0]
print('optimized multiplication cost is ' + format(min_cost / naive_costs  * 100, '.1f') +  ' percent of naive ordered multiplication costs.')

import matplotlib.pyplot as plt
plt.imshow(costs)
plt.xlabel("sequence start matrix")
plt.ylabel("sequence length")
plt.show()

