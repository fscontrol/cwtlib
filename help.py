from water import Water
from params import TempP, TDSP, ConcP, Ion
import numpy as np
import functools
pka = [4.5E-7, 4.8E-11]
ka = [10**(-x) for x in pka]
conc = 0.007
c_co2 = 3E-5
c_hco3 = 7E-3
c_c02_total = c_co2 + c_hco3

def pkw(temp):
    return 14.92 - 0.03992*temp + 0.00013122*temp**2

def alpha(pH, n):
    h = 10**(-pH)
    if n == 0:
        return h**2/(h**2 + ka[0]*h + ka[0]*ka[1])
    elif n == 1:
        return h*ka[0]/(h**2 + ka[0]*h + ka[0]*ka[1])
    else:
        return ka[0]*ka[1]/(h**2 + ka[0]*h + ka[0]*ka[1])

phs = np.linspace(5, 9, 100)
for ph in phs:
    alpha_co2 = alpha(ph, 0)
    alpha_hco3 = alpha(ph, 1)
    print(ph, alpha_hco3/alpha_co2, c_hco3/c_co2)


