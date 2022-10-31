
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def gen_graph(N, p):
    rd = np.random.rand(N, N)
    A = np.triu(rd < (p))
    np.fill_diagonal(A, 0)
    A[np.tril_indices(N)] = A.T[np.tril_indices(N)]

    rd = np.random.rand(N, N)
    w = np.triu(rd)
    np.fill_diagonal(rd * A, 0)
    w[np.tril_indices(N)] = w.T[np.tril_indices(N)]
    return A, w

def shortest_path(A, i, j):
    l = 1
    P = A.copy()
    n, m = A.shape
    while P[i,j] == 0 and l < n:
        P = np.linalg.matrix_power(P, 2)
        l += 1

    # test with networkx
    G = nx.from_numpy_array(A)
    if nx.shortest_path_length(G, i, j) != l:
        print('error')

    return l

def min_spanning_tree(A, w):
    n, m = A.shape
    edges = []
    for i in range(n):
        for j in range(i, n):
            if A[i,j] == 1:
                edges.append((i, j, w[i,j]))
   
    edges = sorted(edges, key=lambda x: x[2])
    visited_nodes = set()
    visited_nodes.add(0)
    
    tree = []
    for e in edges:
        if e[0] not in visited_nodes or e[1] not in visited_nodes:
            visited_nodes.add(e[0])
            visited_nodes.add(e[1])
            A[e[0], e[1]] = 2
            A[e[1], e[0]] = 2
            tree.append(e)

    return tree

A, w = gen_graph(20, 0.2)
print(A, w)
nx.draw(nx.from_numpy_matrix(A), with_labels=True)

sp = shortest_path(A, 0, 5) 
tree = min_spanning_tree(A, w)
print(tree)

if sp == 20:
    print('No path found')
else:
    print('Shortest path length', sp)
plt.show()

