import numpy as np
import random as rnd

from scipy.stats import binom
from scipy.stats import beta

n = 100
Hs = [50, 75, 80]

# discrete integration, cause why not
def integrate(f, l, r, s, k):
    sum = 0.0
    for x in np.arange(l,r, s):
        sum += f(k, x) * s
    
    print(sum)
    return sum


def m_0(k, x):
    return binom.pmf(k, n, x)

def m_1(k, x):
    return binom.pmf(k, n, x) * beta.pdf(x, 30, 30)

factors = []
for H in Hs:
    factors.append(integrate(m_0, 0, 1, 0.001, H) / integrate(m_1, 0, 1, 0.001, H))


print(factors)

