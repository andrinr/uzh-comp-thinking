import numpy as np
import matplotlib.pyplot as plt

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

def to_bloch_vector(q_in):
    u = q_in[0] / q_in[1]
    
    x = 2 * u.real / (1 + u.real ** 2 + u.imag ** 2)
    y = 2 * u.imag / (1 + u.real ** 2 + u.imag ** 2)
    z = (1- u.real ** 2 - u.imag ** 2) / (1 + u.real ** 2 + u.imag ** 2)

    return np.array([x, y, z])

def eval_v(q_in, operators):
    if not check_qbit(q_in): raise Exception("invalid qubit state")

    fig, axs = plt.subplots(nrows=1, ncols=len(operators), figsize=(10, 4),  subplot_kw=dict(projection='3d'))
    fig.suptitle("Consecutive operators", fontsize=14)
    fig.tight_layout() 

    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    x = np.cos(u)*np.sin(v)
    y = np.sin(u)*np.sin(v)
    z = np.cos(v)

    op = np.identity(2)
    q = q_in.copy()
    for i in range(len(operators)):
        q = operators[i].dot(q)
        axs[i].plot_wireframe(x, y, z, color="black", alpha=0.1)
        q_b = to_bloch_vector(q)
        axs[i].quiver(0, 0, 0, q_b[0], q_b[1], q_b[2])

    plt.show()

    if not check_qbit(q): raise Exception("invalid qubit state")

    return q