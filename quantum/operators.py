import numpy as np

### Quantum Operators
X = np.array([
    [0. +0j, 1. +0j], 
    [1. +0, 0. +0j]])
    
Y = np.array([
    [0. +0j, 0. -1j], 
    [0. -1j, 0. +0j]])

Z = np.array([
    [1. +0j, 0. +0j], 
    [0. +0j, -1. +0j]])

is2 = 1 / np.sqrt(2) + 0j
H = np.array([
    [is2, is2], 
    [is2, -is2]])

def rot_OP(axis, angle):
    c = np.cos(angle/2) + 0j
    s = np.sin(angle/2) + 0j
    if axis == 0:
        R = np.array([
            [c, (0.-1j) * s], 
            [(0.-1j) * s, c]])
    elif axis == 1:
        R = np.array([
            [c, -s], 
            [s, c]])
    else:
        R = np.array([
            [np.exp(-1j * angle / 2), 0], 
            [0, np.exp(1j * angle / 2)]])

    return R