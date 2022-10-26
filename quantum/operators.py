import numpy as np
from string import digits
import re

### Quantum Operators
class OP: 
    def __init__(self, id, M):
        self.id = id
        self.M = M
        self.next = None
    
    def __str__(self):
        return self.id

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
        self.angle = angle
        c = np.cos(angle/2) + 0j
        s = np.sin(angle/2) + 0j
        M = np.array([
            [c, (0.-1j) * s], 
            [(0.-1j) * s, c]])

        OP.__init__(self, 'rx', M)

class RY(OP):
    def __init__(self, angle):
        self.angle = angle
        c = np.cos(angle/2) + 0j
        s = np.sin(angle/2) + 0j
        M = np.array([
           [c, -s], 
            [s, c]])

        OP.__init__(self, 'ry', M)

class RZ(OP):
    def __init__(self, angle):
        self.angle = angle
        M = np.array([
            [np.exp(-1j * angle / 2), 0], 
            [0, np.exp(1j * angle / 2)]])

        OP.__init__(self, 'rz', M)

class CNOT(OP):
    data = dict()

    def __init__(self, type, op_ID, column, circuit_ID):
        self.type = type
        key = str(op_ID) + str(column) + str(circuit_ID)

        # interlink the CNOTs
        if key in CNOT.data:
            self.linked = CNOT.data[key]
            CNOT.data[key].linked = self
        else:
            self.linked = None
            CNOT.data[key] = self

        OP.__init__(self, 'c', None)


equivs = {
    'xx' : 'i',
    'yy' : 'i',
    'hh' : 'i',
    'zz' : 'i',
    'xz' : 'y',
}

# parses a symbol into an operator
def parse_symbol(symbol, column = -1, circuit_ID = -1):
    op = re.sub('[^a-zA-Z]+', '', symbol)
    if op == "x":
        return X()

    elif op == "y":
        return Y()

    elif op == "z":
        return Z()

    elif op == "h":
        return H()

    elif op == "i":
        return I()

    elif op == "cc":
        if column == -1 or circuit_ID == -1:
            raise Exception("CNOTs must be parsed with column and circuit_ID")
        op_ID = int(re.search(r'\d+', symbol).group())
        return CNOT("c", op_ID, column, circuit_ID)

    elif op == "ct":
        if column == -1 or circuit_ID == -1:
            raise Exception("CNOTs must be parsed with column and circuit_ID")
        op_ID = int(re.search(r'\d+', symbol).group())
        return CNOT("t", op_ID, column, circuit_ID)

    elif op == "rx":
        floats = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", symbol)
        if len(floats) == 0:
            raise Exception("RX must be parsed with an angle")
        angle = float(floats[0])
        return RX(angle)
        
    elif op == "ry":
        floats = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", symbol)
        if len(floats) == 0:
            raise Exception("RX must be parsed with an angle")
        angle = float(floats[0])
        return RY(angle)

    elif op == "rz":
        floats = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", symbol)
        if len(floats) == 0:
            raise Exception("RX must be parsed with an angle")
        angle = float(floats[0])
        return RZ(angle)

    else:
        raise Exception("Unknown symbol: " + symbol)
        return None