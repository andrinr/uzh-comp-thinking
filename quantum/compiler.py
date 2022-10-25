import numpy as np
import matplotlib.pyplot as plt
from operators import I, H, RX, RY, RZ, X, Y, Z, equis, parse_symbol
import random
import math

# Params
ERROR_MARGIN = 0.00001

def check_qbit(qbit):
    alpha = qbit[0]
    beta = qbit[1]
    d = (1 - (np.abs(alpha) ** 2 + np.abs(beta) ** 2))
    return np.abs(d) < ERROR_MARGIN

def eval(q_in, operators):
    if not check_qbit(q_in): raise Exception("invalid qubit state")

    op = I().M
    for i in range(len(operators)):
        op = np.matmul(operators[i].M, op)

    q_out = op.dot(q_in)

    if not check_qbit(q_out): raise Exception("invalid qubit state")

    return q_out

def to_bloch_vector(q_in):
    u = q_in[0] / q_in[1]
    
    x = 2 * u.real / (1 + u.real ** 2 + u.imag ** 2)
    y = 2 * u.imag / (1 + u.real ** 2 + u.imag ** 2)
    z = (1- u.real ** 2 - u.imag ** 2) / (1 + u.real ** 2 + u.imag ** 2)

    return np.array([x, y, z])

def eval_v(q_in, operators):
    if not check_qbit(q_in): raise Exception("invalid qubit state")

    fig, axs = plt.subplots(nrows=1, ncols=len(operators)+1, figsize=(10, 4),  subplot_kw=dict(projection='3d'))
    fig.suptitle("Consecutive operators", fontsize=14)
    fig.tight_layout() 

    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    x = np.cos(u)*np.sin(v)
    y = np.sin(u)*np.sin(v)
    z = np.cos(v)

    op = np.identity(2)
    q = q_in.copy()
    axs[0].plot_wireframe(x, y, z, color="black", alpha=0.1)
    q_b = to_bloch_vector(q)
    axs[0].quiver(0, 0, 0, q_b[0], q_b[1], q_b[2])
    for i in range(len(operators)):
        q = operators[i].M.dot(q)
        axs[i+1].plot_wireframe(x, y, z, color="black", alpha=0.1)
        q_b = to_bloch_vector(q)
        axs[i+1].quiver(0, 0, 0, q_b[0], q_b[1], q_b[2])

    plt.show()

    if not check_qbit(q): raise Exception("invalid qubit state")

    return q

# parses array of symbols into array of operators and generates a linked list
def parse_lane(lane):
    parsed_lane = []
    for i in range(len(lane)):
        parsed_lane.append(parse_symbol(lane[i]))

    return parsed_lane

def reduce_lane(parsed_lane):
    n_reduced = 0
    n = 0
    while True:
        for i in range(len(parsed_lane)-1):
            a = parsed_lane[i].id
            if a == 'i': continue

            # search for the next non-id operator
            j = i+1
            while(j < len(parsed_lane)-1 and parsed_lane[j].id == 'i'):
                j +=1 
            b = parsed_lane[j].id

            if a + b in equis:
                s = equis[a + b]
                parsed_lane[i] = parse_symbol(s)
                parsed_lane[j] = I()
                n+=1
                continue

            if a == 'rx' and b == 'rx':
                parsed_lane[i] = RX(parsed_lane[i].angle + parsed_lane[j].angle)
                parsed_lane[j] = I()
                n+=1
                continue

            if a == 'ry' and b == 'ry':
                parsed_lane[i] = RY(parsed_lane[i].angle + parsed_lane[j].angle)
                parsed_lane[j] = I()
                n+=1
                continue

            if a == 'rz' and b == 'rz':
                parsed_lane[i] = RZ(parsed_lane[i].angle + parsed_lane[j].angle)
                parsed_lane[j] = I()
                n+=1
                continue
            
            # set j to next non id operator
            i = j

        # break in case of no optimization
        n_reduced += n

        if n == 0:
            break

        n = 0
    
    return parsed_lane

def parse_circuit(circ):
    n, m = np.shape(circ)
    for i in range(n):
        circ[i,:] = parse_lane(circ[i,:])

    return circ

def reduce_circuit(circ):
    n, m = np.shape(circ)

    for i in range(n):
        circ[i,:] = reduce_lane(circ[i,:])

    print('with equis')
    print_circuit(circ)

    mask = []
    for j in range(m):
        mask.append(False)
        for i in range(n):
            if circ[i,j].id != 'i':
                mask[j] = True
                break
    
    print(mask)
    circ = circ[:, mask]

    return circ

def print_circuit(circ):
    n, m = np.shape(circ)
    for i in range(n):
        for j in range(m):
            print(circ[i,j].id,  end ="\t")
        print('')

def test():
    ops = ['x', 'y', 'z', 'h', 'i', 'rx', 'ry', 'rz']
    rands = np.random.randint(0, len(ops), size = 1000)

    lane = []
    for i in range(len(rands)):
        lane.append(ops[rands[i]])
        if lane[i] == 'rx' or lane[i] == 'ry' or lane[i] == 'rz':
            lane[i] += str(random.uniform(0, math.pi))

    parsed_lane = parse_lane(lane)
    reduced_lane = reduce_lane(parsed_lane)

#test()


