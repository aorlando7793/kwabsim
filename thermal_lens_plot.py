import numpy as np
import math
import matplotlib.pyplot as plt
from cavityclass import *

M_2 = float(input('Enter M-Squared: '))
LAM = 1064*10**(-7)

ds28 = Cavity('datatest.dat',LAM)

thermal_range = np.arange(16,25,.1)
labels = []
Wx = []
Wy = []
for f in thermal_range:
    newcav = ds28.remove_optic(5).insert_optic('L',f,5)
    xcav = newcav.get_x_cav()
    ycav = newcav.get_y_cav()
    if xcav.is_stable and ycav.is_stable:
        Wx.append(xcav.waist(33.5))
        Wy.append(ycav.waist(33.5))
        xcav.plot_waist(250,lab=f)
        ycav.plot_waist(250,lab=f)
    else:
        Wx.append(0)
        Wy.append(0)
plt.legend()
plt.show()

plt.figure()
plt.plot(thermal_range, Wx)
plt.plot(thermal_range, Wy)
plt.show()