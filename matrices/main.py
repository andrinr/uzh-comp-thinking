import numpy as np
import matplotlib.pyplot as plt

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

def solve_dp(matrices):
    num_matrices = matrices.shape[0]
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
            # iterate over subsequnce combinations
            for a in range(1,l):
                b = l - a
                j = i + a

                ij_cost = complexity(sizes[a, i], sizes[b, j])
                new_cost =  costs[a,i] + costs[b,j] + ij_cost

                if new_cost < costs[l,i]:
                    costs[l,i] = new_cost
                    sizes[l,i] = get_size(sizes[a,i], sizes[b,j])

    # fetch result from table
    return costs, costs[num_matrices -1, 0], naive_costs


n, m = 3, 3
fig, axs = plt.subplots(nrows=n, ncols=m, figsize=(9, 12))
fig.suptitle("DP tables with each" + str(100) + " random matrices.", fontsize=18)
fig.tight_layout(pad=3.0)

for k in range(n):
    for l in range(m):

        num_matrices = 100
        matrices = gen_matrices(num_matrices)
        costs, opt, naive = solve_dp(matrices)
        speedup = naive / opt

        axs[k,l].imshow(costs)

        axs[k,l].set_xlabel("sequence start matrix")
        axs[k,l].set_ylabel("sequence length")
        axs[k,l].set_title("Speedup " + str(int(speedup)) + "x")

plt.show()

