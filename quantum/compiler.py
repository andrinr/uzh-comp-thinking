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

def apply_equivs(circuit_obj):
    circuit = circuit_obj.circuit
    n, m = np.shape(circuit)
    total_mutations = 0
    while True:
        mutations = 0
        for i in range(m-1):
            for row in range(n):
                a = circuit[row, i].id
        
                # search for the next non-id operator
                j = i+1
                while(j < m-1 and circuit[row, j].id == 'i'):
                    j +=1 
                b = circuit[row, j].id
                if a == 'i' and b=='i': continue

                if a + b in equivs:
                    s = equivs[a + b]
                    circuit[row, i] = parse_symbol(s, row, i)
                    circuit[row, j] = I()
                    circuit[row, j].set_position(row, j)
                    mutations+=1
                    continue

                elif a == 'rx' and b == 'rx':
                    circuit[row, i] = RX(circuit[row, i].angle + circuit[row, j].angle)
                    circuit[row, i].set_position(row, i)
                    circuit[row, j] = I()
                    circuit[row, j].set_position(row, j)
                    mutations+=1
                    continue

                elif a == 'ry' and b == 'ry':
                    circuit[row, i] = RY(circuit[row, i].angle + circuit[row, j].angle)
                    circuit[row, i].set_position(row, i)
                    circuit[row, j] = I()
                    circuit[row, j].set_position(row, j)
                    n+=1
                    continue

                elif a == 'rz' and b == 'rz':
                    circuit[row, i] = RZ(circuit[row, i].angle + circuit[row, j].angle)
                    circuit[row, i].set_position(row, i)
                    circuit[row, j] = I()
                    circuit[row, j].set_position(row, j)
                    mutations+=1
                    continue
                    
                elif b != 'c' and a == 'i':
                    circuit[row, i] = circuit[row, j]
                    circuit[row, i].set_position(row, i)
                    circuit[row, j] = I()
                    circuit[row, j].set_position(row, j)
                    mutations+=1
                    continue
                
                elif b == 'c' and a == 'i':
                    row_linked = circuit[row, j].linked.i

                    only_identities = True
                    for k in range(i, j):
                        if circuit[row_linked, k].id != 'i':
                            only_identities = False
                    
                    if only_identities:
                        circuit[row, i] = circuit[row, j]
                        circuit[row, i].set_position(row, i)
                        circuit[row, j] = I()
                        circuit[row, j].set_position(row, j)

                        circuit[row_linked, i] = circuit[row_linked, j]
                        circuit[row_linked, i].set_position(row_linked, i)

                        circuit[row_linked, j] = I()
                        circuit[row_linked, j].set_position(row_linked, j)
                        mutations+=2
                        continue
        
        # break in case of no optimization
        total_mutations += mutations

        if 0 == mutations:
            break

    #print('total mutations: ', total_mutations)


def reduce_circuit(circuit_object):
    circ = circuit_object.circuit
    n, m = np.shape(circ)

    apply_equivs(circuit_object)

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


