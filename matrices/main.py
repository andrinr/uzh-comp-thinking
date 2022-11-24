import numpy as np

# check if two matrices can be multiplied
def check_multiplication(sizeA, sizeB):
    if sizeA[1] == sizeB[0]:
        return True
    else:
        return False

def get_size(sizeA, sizeB):
    return [sizeA[0], sizeB[1]]

def complexity(sizeA, sizeB):
    if not check_multiplication(sizeA, sizeB):
        return np.inf

    return sizeA[0]*sizeA[1]*sizeB[1]

# generate list of random sized matrices
def gen_matrices(n, max_size = 100):

    matrices = np.zeros((n, 2), dtype = int)
    prev_size_m = np.random.randint(2, max_size)
    for i in range(n):
        size = [prev_size_m, prev_size_m] #np.random.randint(2, max_size)]
        prev_size_m = size[1]
        matrices[i] = np.array(size)
    return matrices

num_matrices = 8
matrices = gen_matrices(num_matrices)
print(matrices)
costs = np.full((num_matrices, num_matrices), np.inf)
sizes = np.zeros((num_matrices, num_matrices, 2))
sizes[1,:,:] = matrices
costs[0,:] = 0

naive_costs = 0
trailing_shape = matrices[0]
for i in range(num_matrices-1):
    costs[1, i] = complexity(trailing_shape, matrices[i+1])
    print(costs[1, i], naive_costs)
    naive_costs += costs[1, i]
    trailing_shape = get_size(trailing_shape, matrices[i+1])

#print(sizes)
#print(costs)

for l in range(2, num_matrices):
    for i in range(num_matrices - l):
        for a in range(1,l):
            b = l - a
            j = i + a

            ij = complexity(sizes[a, i], sizes[b, j])

            #print(l, i, j, a, b, ij)

            if costs[a,i] + costs[b,j] + ij < costs[l,i]:
                costs[l,i] = costs[a,i] + costs[b,j] + ij
                sizes[l,i] = get_size(sizes[a,i], sizes[b,j])

print(costs)
print('minimum number of multiplication:', np.min(costs[num_matrices-1,:]))
print('naive order costs', naive_costs)