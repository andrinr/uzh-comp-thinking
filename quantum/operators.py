import numpy as np

### Quantum Operators
class OP: 
    def __init__(self, id, M):
        self.id = id
        self.M = M

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

def train():
    ops = {0: 'x', 1: 'y', 2: 'z', 3: 'i', 4: 'h'}
    n = 40
    lane = np.vectorize(ops.get)(np.random.randint(0, len(ops), n))
    print(lane)
    for i in range(10):
        i = 0
        j = 1
        while( i < len(lane) and  j < len(lane)):
            while(i < len(lane) and lane[i] == '-' ):
                i+=1
                j+=1
            if (i >= len(lane) or j >= len(lane)):
                break
            while(j < len(lane) and lane[j] == '-'):
                j+=1
            
            print(i, j)
            c = lane[i] + lane[j]
            if c in equis:
                lane[i] = equis[c]
                lane[j] = '-'

            i+=1
            j+=1

            print(lane)

    

train()



def reduce(ops):
    a = np.zeros(len(ops))

    

