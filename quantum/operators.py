import numpy as np
from string import digits
import re

### Quantum Operators
class OP: 
    def __init__(self, id, M):
        self.id = id
        self.M = M
        self.next = None
    
    def set_next(self, next):
        self.next = next

class I(OP):
    def __init__(self):
        M = np.array([
            [1. +0j, 0. +0j], 
            [0. +0, 1. +0j]])

        OP.__init__(self, 'i', M)

class X(OP):
    def __init__(self):
        M = np.array([
            [0. +0j, 1. +0j], 
            [1. +0, 0. +0j]])

        OP.__init__(self, 'x', M)

class Y(OP):
    def __init__(self):
        M = np.array([
            [0. +0j, 0. -1j], 
            [0. -1j, 0. +0j]])

        OP.__init__(self, 'y', M)

class Z(OP):
    def __init__(self):
        M = np.array([
            [1. +0j, 0. +0j], 
            [0. +0j, -1. +0j]])

        OP.__init__(self, 'z', M)

class H(OP):
    def __init__(self):
        is2 = 1 / np.sqrt(2) + 0j
        M = np.array([
            [is2, is2], 
            [is2, -is2]])

        OP.__init__(self, 'h', M)

class RX(OP):
    def __init__(self, angle):
        c = np.cos(angle/2) + 0j
        s = np.sin(angle/2) + 0j
        M = np.array([
            [c, (0.-1j) * s], 
            [(0.-1j) * s, c]])

        OP.__init__(self, 'rx' + angle, M)

class RY(OP):
    def __init__(self, angle):
        c = np.cos(angle/2) + 0j
        s = np.sin(angle/2) + 0j
        M = np.array([
           [c, -s], 
            [s, c]])

        OP.__init__(self, 'ry' + angle, M)

class RZ(OP):
    def __init__(self, angle):
        M = np.array([
            [np.exp(-1j * angle / 2), 0], 
            [0, np.exp(1j * angle / 2)]])

        OP.__init__(self, 'rz' + angle, M)

equis = {
    'xx' : 'i',
    'yy' : 'i',
    'hh' : 'i',
    'zz' : 'i',
    'xz' : 'y',
    'ix' : 'x',
    'xi' : 'x',
    'iy' : 'y',
    'yi' : 'y',
    'iz' : 'z',
    'zi' : 'z',
    'ih' : 'h',
    'hi' : 'h',
}

# parses a symbol into an operator
def parse_symbol(symbol):
    remove_digits = str.maketrans('', '', digits)
    symbol = symbol.translate(remove_digits)

    if symbol == 'x':
        return X()
    elif symbol == 'y':
        return Y()
    elif symbol == 'z':
        return Z()
    elif symbol == 'h':
        return H()
    elif symbol == 'i':
        return I()
    elif symbol == 'rx':
        angle = re.findall("\d+\.\d+", symbol)[0]
        return RX(angle)
    elif symbol == 'ry':
        angle = re.findall("\d+\.\d+", symbol)[0]
        return RY(angle)
    elif symbol == 'rz':
        angle = re.findall("\d+\.\d+", symbol)[0]
        return RZ(angle)


