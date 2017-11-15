import numpy as np
import math
import matplotlib.pyplot as plt
from cavityclass import *

LAM = 1064*10**(-7)

ds28 = Cavity('datatest.dat',LAM)

thermal_range = np.arange(16,22,.1)
labels = []
W = []
for f in thermal_range:
    newcav = ds28.remove_optic(5).insert_optic('L',f,5)
    if newcav.is_stable:
        W.append(newcav.waist(33.5))
        newcav.plot_waist(250,lab=f)
    else:
        W.append(0)
plt.legend()
plt.show()

plt.figure()
plt.plot(thermal_range, W)
plt.show()