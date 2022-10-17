import numpy as np
import math
import matplotlib.pyplot as plt
from operators import X, Y, Z , rot_OP, H
from compiler import eval

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

def to_bloch(q_in):
    theta = np.arccos(q_in[0] * 2.)
    psi = np.log(q_in[1]) / (np.sin(theta/2.) * 1j)

    print('bloch', theta, psi)

q_a = np.array([1.+0j,0.+0j])
q_b = np.array([0.+0j,1.+0j])

r = eval(q_a, [rot_OP(0, 0.3), X, Y, Z, H])

to_bloch(r)

print(r, collapse(r))

print(collapse(q_b))

ax = plt.axes(projection='3d')
