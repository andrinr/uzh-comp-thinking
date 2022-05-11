import numpy as np
import random as rnd

from scipy.stats import binom
from scipy.stats import beta


thetas = [0.5, 0.65, 0.8]

# discrete integration, cause why not
def integrate(f, l, r, s):
    sum = 0
    for x in np.arange(l,r, s):
        sum += f(x)


def m_0(x):
    binom(100, x)

def m_1(x):
    binom(100, x) * beta.pdf(x, 30, 30)

for theta in thetas:
    m_0 = binom(100, theta) * 
    
