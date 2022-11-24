
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
    while P[i,j] == 0:
        l += 1
        P = np.linalg.matrix_power(A, l)
        if l == n:
            return None
        
    # test with networkx
    G = nx.from_numpy_array(A)
    if nx.shortest_path_length(G, i, j) != l:
        print('lengths do not match, should be', nx.shortest_path_length(G, i, j))

    return l

def min_spanning_tree(A, w):
    # greedy shortest path (kruskal's algorithm)
    n, m = A.shape
    edges = []
    for i in range(n):
        for j in range(i, n):
            if A[i,j] == 1:
                edges.append((i, j, w[i,j]))
   
    edges = sorted(edges, key=lambda x: x[2])
    visited_nodes = set()
    visited_nodes.add(0)
    
    length = 0
    tree = []
    for e in edges:
        if e[0] not in visited_nodes or e[1] not in visited_nodes:
            visited_nodes.add(e[0])
            visited_nodes.add(e[1])
            tree.append(e)
            length += e[2]

    return length, tree

A, w = gen_graph(50, 0.05)
nx.draw(nx.from_numpy_matrix(A), with_labels=True, node_size=20)

sp = shortest_path(A, 0, 5) 
print('Shortest path length', sp)

tree_length, tree = min_spanning_tree(A, w)
print('Tree length', tree_length)

