import numpy as np
import math
import matplotlib.pyplot as plt
from cavityclass import *

V_i = int(input('Enter Position of Nd:YVO_4 in Cavity:    '))
M_2 = float(input('Enter M-Squared: '))
LAM = 1064*10**(-7) * M_2

ds28 = Cavity('testfile.dat',LAM)

#Set "reasonable" range for thermal lensing
thermal_range = np.arange(16,22,.1)

#Create figure, axes, and colormap
cm = plt.get_cmap('Reds')
colors = [cm(1.*i/len(thermal_range)) for i in range(len(thermal_range))]
fig = plt.figure()

#If x and y cavity are equal only one set of axes is defined,
#if they are not equal a set of axes is defined for each cavity. 
if ds28.get_xcav().cavity == ds28.get_ycav().cavity:
    ax = fig.add_subplot(1,1,1)
    ax.set_prop_cycle('color',colors)
    ax.set_xlabel('Z(cm)')
    ax.set_ylabel('Waist(cm)')
else:
    ax_x = fig.add_subplot(2,1,1)
    ax_x.set_prop_cycle('color',colors)
    ax_x.set_xlabel('Z(cm)')
    ax_x.set_ylabel('Waist(cm)')
    
    ax_y = fig.add_subplot(2,1,2)
    ax_y.set_prop_cycle('color',colors)
    ax_y.set_xlabel('Z(cm)')
    ax_y.set_ylabel('Waist(cm)')

#Loop through range of thermal lensing vaules and plot every stable cavity
for f in thermal_range:
    newcav = ds28.remove_optic(V_i).insert_optic('L',f,V_i)
    xcav = newcav.get_xcav()
    ycav = newcav.get_ycav()
    if newcav.is_stable and ycav.cavity == xcav.cavity:
        Z, W = newcav.plot_waist(100)
        ax.plot(Z,W)
    elif xcav.is_stable and ycav.is_stable:
        Zx, Wx = xcav.plot_waist(100)
        Zy, Wy = ycav.plot_waist(100)
        ax_x.plot(Zx,Wx)
        ax_y.plot(Zy,Wy)

plt.show()