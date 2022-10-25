import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt
from operators import X, Y, Z , RX, RY, H, I
from compiler import eval, eval_v, parse_circuit, parse_lane, reduce_lane, reduce_circuit, print_circuit

file_name = input('Provide a .q file \n')

df = pd.read_csv(file_name, delim_whitespace=True, header=None)
circ_raw = df.to_numpy()


circ = parse_circuit(circ_raw)

print('circuit as specified')
print_circuit(circ)

circ_opt = reduce_circuit(circ)

print('reduced circuit')
print_circuit(circ_opt)