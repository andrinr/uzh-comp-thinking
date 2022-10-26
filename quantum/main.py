import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from operators import X, Y, Z , RX, RY, H, I
from compiler import reduce_circuit
from circuit import Circuit

file_name = input('Provide a .q file \n')

circ1 = Circuit.read_dot_q(file_name)

print('circuit as specified')
circ1.log()

circ_opt = reduce_circuit(circ1)

print('reduced circuit')
circ1.log()

q_zero = np.full(2**circ1.n(), 0+0j)
q_zero[0] = 1 + 0j
#q_res = circ1.evaluate(q_zero)

#print('resulting qubit state', q_res)