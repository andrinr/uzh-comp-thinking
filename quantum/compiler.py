import numpy as np
from operators import I, H, RX, RY, RZ, X, Y, Z, equivs, parse_symbol
import random
import math

# Params
ERROR_MARGIN = 0.00001
def check_qbit(qbit):
    alpha = qbit[0]
    beta = qbit[1]
    d = (1 - (np.abs(alpha) ** 2 + np.abs(beta) ** 2))
    return np.abs(d) < ERROR_MARGIN

def apply_equivs(lane):
    n_mutations = 0
    n = 0
    while True:
        for i in range(len(lane)-1):
            a = lane[i].id
    
            # search for the next non-id operator
            j = i+1
            while(j < len(lane)-1 and lane[j].id == 'i'):
                j +=1 
            b = lane[j].id
            if a == 'i' and b=='i': continue

            if a + b in equivs:
                s = equivs[a + b]
                lane[i] = parse_symbol(s)
                lane[j] = I()
                n+=1
                continue

            elif a == 'rx' and b == 'rx':
                lane[i] = RX(lane[i].angle + lane[j].angle)
                lane[j] = I()
                n+=1
                continue

            elif a == 'ry' and b == 'ry':
                lane[i] = RY(lane[i].angle + lane[j].angle)
                lane[j] = I()
                n+=1
                continue

            elif a == 'rz' and b == 'rz':
                lane[i] = RZ(lane[i].angle + lane[j].angle)
                lane[j] = I()
                n+=1
                continue

            #elif b != 'c' and a == 'i':
            #    lane[i] = lane[j]
            #    lane[j] = I()
            #    n+=1
            #    continue
            
            # set j to next non id operator
            i = j

        # break in case of no optimization
        n_mutations += n

        if n == 0:
            break

        n = 0
    
    return lane


def reduce_circuit(circuit_object):
    circ = circuit_object.circuit
    n, m = np.shape(circ)

    for i in range(n):
        circ[i,:] = apply_equivs(circ[i,:])

    print('with equis')

    mask = []
    for j in range(m):
        mask.append(False)
        for i in range(n):
            if circ[i,j].id != 'i':
                mask[j] = True
                break

    circ = circ[:, mask]

    circuit_object.circuit = circ

def test():
    ops = ['x', 'y', 'z', 'h', 'i', 'rx', 'ry', 'rz']
    rands = np.random.randint(0, len(ops), size = 1000)

    lane = []
    for i in range(len(rands)):
        lane.append(ops[rands[i]])
        if lane[i] == 'rx' or lane[i] == 'ry' or lane[i] == 'rz':
            lane[i] += str(random.uniform(0, math.pi))

    #parsed_lane = parse_lane(lane)
    #reduced_lane = apply_equivs(parsed_lane)

#test()


