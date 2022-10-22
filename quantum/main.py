import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt
from operators import X, Y, Z , rot_OP, H
from compiler import eval, eval_v


file_name = input('Provide a .q file \n')

df = pd.read_csv(file_name, delim_whitespace=True, header=None)
print(df)

q_zero = np.array([1.+0j,0.+0j])
q_zero_b = np.array([1,0])
q_one_b = np.array([0,1])

def collapse(q_in):
    q_in_v = abs(q_in[0]) * q_zero_b + abs(q_in[1]) * q_one_b
    print(q_in, q_in_v)
    a = np.dot(q_in_v, q_zero_b) / \
        np.linalg.norm(q_in_v) * np.linalg.norm(q_zero_b)
    print(a)
    return int(a > (math.pi / 2.))

q_a = np.array([1.+0j,0.+0j])
q_b = np.array([0.+0j,1.+0j])

r = eval(q_a, [rot_OP(0, 0.3), X, Y, Z, H])
r = eval_v(q_a, [rot_OP(0, 0.3), X, Y, Z, H])

print(r, collapse(r))

print(collapse(q_b))


