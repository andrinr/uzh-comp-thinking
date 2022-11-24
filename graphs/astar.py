import numpy as np
import matplotlib.pyplot as plt
import networkx  as nx
import queue 

def astar(A, w, i, j):
    # A* algorithm
    n, m = A.shape
    visited = set()
    visited.add(i)
    q = queue.PriorityQueue()
    q.put_nowait((0, i))
    
    while not q.empty():
        l, v = q.get_nowait()
        #print(l)

        if v == j:
            print('found path of length', l)
            return visited
        for k in range(n):
            if A[v,k] == 1 and not k == v and k not in visited:
                q.put_nowait((l + w[v,k], k))
                visited.add(k)
    return visited

s = 5
maze = np.random.random((s, s)) < 0.8
maze[0,0] = 1
maze[-1,-1] = 1

# genereate adjacency matrix from maze
A = np.zeros((s*s, s*s))
for i in range(s):
    for j in range(s):
        if maze[i,j] == 1:
            # left
            if i > 0 and maze[i-1,j] == 1:
                A[i*s+j, (i-1)*s+j] = 1
                A[(i-1)*s+j, i*s+j] = 1
            # right
            if i < s-1 and maze[i+1,j] == 1:
                A[i*s+j, (i+1)*s+j] = 1
                A[(i+1)*s+j, i*s+j] = 1
            # down
            if j > 0 and maze[i,j-1] == 1:
                A[i*s+j, i*s+j-1] = 1
                A[i*s+j-1, i*s+j] = 1
            # up
            if j < s-1 and maze[i,j+1] == 1:
                A[i*s+j, i*s+j+1] = 1
                A[i*s+j+1, i*s+j] = 1
            # diagonal left down
            if i > 0 and j > 0 and maze[i-1,j-1] == 1:
                A[i*s+j, (i-1)*s+j-1] = 1
                A[(i-1)*s+j-1, i*s+j] = 1
            # diagonal right down
            if i < s-1 and j > 0 and maze[i+1,j-1] == 1:
                A[i*s+j, (i+1)*s+j-1] = 1
                A[(i+1)*s+j-1, i*s+j] = 1
            # diagonal left up
            if i > 0 and j < s-1 and maze[i-1,j+1] == 1:
                A[i*s+j, (i-1)*s+j+1] = 1
                A[(i-1)*s+j+1, i*s+j] = 1
            # diagonal right up
            if i < s-1 and j < s-1 and maze[i+1,j+1] == 1:
                A[i*s+j, (i+1)*s+j+1] = 1
                A[(i+1)*s+j+1, i*s+j] = 1

target = s*s-1
target_x = target % s
target_y = target // s

# generate weights accordint to euclidean distance to target point
w = np.zeros((s*s, s*s))
for i in range(s*s):
    for j in range(s*s):
        x = i % s
        y = i // s
        w[i,j] = np.sqrt((x - target_x)**2 + (y - target_y)**2)

print(w)
#plt.imshow(maze)
#plt.show()

maze = maze.astype(int)
maze *= 2
# color nodes in maze that were visited
visited = astar(A, w, 0, s*s-1)
print(visited)

for v in visited:
    i = v // s
    j = v % s
    maze[i,j] = 1

plt.imshow(maze)
plt.show()