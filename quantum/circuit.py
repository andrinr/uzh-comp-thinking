from itertools import count
import pandas as pd
import numpy as np
from operators import parse_symbol

class Circuit:

    count = 0

    def __init__(self, circuit):
        self.circuit = circuit
        self.id = Circuit.count
        Circuit.count += 1
    
    def evaluate(self, q_in):
        n, m = np.shape(self.circuit)

        q = q_in.copy()
        for j in range(m):
            M = self.circuit[0,j].M
            for i in range(1,n):
                M = np.kron(self.circuit[i,j].M, M)

            q = M.dot(q)
            
        return q

    def log(self):
        n, m = np.shape(self.circuit)
        for j in range(m):
            print(j,  end ="\t")
        print('')
        for j in range(m):
            print('--------',  end ="")
        print('')
        for i in range(n):
            for j in range(m):
                print(self.circuit[i,j].id,  end ="\t")
            print('')

        for j in range(m):
            print('--------',  end ="")
        print('')

    def n(self):
        return np.shape(self.circuit)[0]

    def m(self):
        return np.shape(self.circuit)[1]

    def parse(raw_circuit, circuit_ID):
        n, m = np.shape(raw_circuit)
        circuit = np.empty((n,m), dtype=object)
        for i in range(n):
            for j in range(m):
                circuit[i,j] = parse_symbol(raw_circuit[i, j], i, j, circuit_ID)

        return circuit

    def read_dot_q(path):
        df = pd.read_csv(path, delim_whitespace=True, header=None)
        circ_raw = df.to_numpy()

        return Circuit(Circuit.parse(circ_raw, Circuit.count))

