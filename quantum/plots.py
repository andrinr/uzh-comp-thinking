import numpy as np
import matplotlib.pyplot as plt
from compiler import check_qbit

def to_bloch_vector(q_in):
    u = q_in[0] / q_in[1]
    
    x = 2 * u.real / (1 + u.real ** 2 + u.imag ** 2)
    y = 2 * u.imag / (1 + u.real ** 2 + u.imag ** 2)
    z = (1- u.real ** 2 - u.imag ** 2) / (1 + u.real ** 2 + u.imag ** 2)

    return np.array([x, y, z])


def eval_lane_v(q_in, operators):
    if not check_qbit(q_in): raise Exception("invalid qubit state")

    fig, axs = plt.subplots(nrows=1, ncols=len(operators)+1, figsize=(10, 4),  subplot_kw=dict(projection='3d'))
    fig.suptitle("Consecutive operators", fontsize=14)
    fig.tight_layout() 

    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    x = np.cos(u)*np.sin(v)
    y = np.sin(u)*np.sin(v)
    z = np.cos(v)

    op = np.identity(2)
    q = q_in.copy()
    axs[0].plot_wireframe(x, y, z, color="black", alpha=0.1)
    q_b = to_bloch_vector(q)
    axs[0].quiver(0, 0, 0, q_b[0], q_b[1], q_b[2])
    for i in range(len(operators)):
        q = operators[i].M.dot(q)
        axs[i+1].plot_wireframe(x, y, z, color="black", alpha=0.1)
        q_b = to_bloch_vector(q)
        axs[i+1].quiver(0, 0, 0, q_b[0], q_b[1], q_b[2])

    plt.show()

    if not check_qbit(q): raise Exception("invalid qubit state")

    return q