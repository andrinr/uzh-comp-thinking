import numpy as np

# Params
ERROR_MARGIN = 0.00001

def check_qbit(qbit):
    alpha = qbit[0]
    beta = qbit[1]
    d = (1 - (np.abs(alpha) ** 2 + np.abs(beta) ** 2))
    return np.abs(d) < ERROR_MARGIN


def eval(q_in, operators):
    if not check_qbit(q_in): raise Exception("invalid qubit state")

    op = np.identity(2)
    for i in range(len(operators)):
        op = np.matmul(operators[i], op)

    q_out = op.dot(q_in)

    if not check_qbit(q_out): raise Exception("invalid qubit state")

    return q_out
