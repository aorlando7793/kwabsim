import numpy as np
import math
import matplotlib.pyplot as plt
from cavityclass import *

LAM = 1064*10**(-7)

def stability_rate(cav_inst, tr_array, tl_pos):
    """Loops through a range of thermal lensing values and creates an instance 
    of Cavity for each one.  Then counts the number of those cavities that are stable 
    and increment num_stable.  Returns the percentage of cavities that are stable.
    """
    num_stab = 0.0
    for f in tr_array:
        newcav = cav_inst.remove_optic(tl_pos).insert_optic('L',f,tl_pos)
        if newcav.is_stable:
            num_stab += 1.0
    return num_stab/len(tr_array)

#create an initial instance of Cavity with arbitrary thermal lensing to be used as input.
#ds28 = Cavity('datatest.dat',LAM)
#s = stability_rate(ds28, thermal_range, 5)
#print('Stability Rate is:', s)        

def vary_param(cav_inst, params, pos, optic):
    rates = []
    for param in params:
        newcav = cav_inst.remove_optic(pos).insert_optic(optic, param, pos)
        rates.append(stability_rate(newcav, thermal_range, 5))
    return rates

thermal_range = np.arange(16,22,.1)
start_cav = Cavity('datatest.dat',LAM)
dist = np.arange(10,35,1)
rates = vary_param(start_cav, dist , 2, 'D')
plt.plot(dist, rates)
plt.show()
    