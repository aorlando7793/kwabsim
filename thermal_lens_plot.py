import numpy as np
import math
import matplotlib.pyplot as plt
from filehandling import filepath
from cavityclass import *

V_i = int(input('Enter Position of Nd:YVO_4 in Cavity:    '))
M_2 = float(input('Enter M-Squared: '))
LAM = 1064*10**(-7) * M_2

laser = Cavity(filepath, LAM)

#Set "reasonable" range for thermal lensing
thermal_range = np.arange(16,24,.1)

#Create figure, axes, and colormap
cm = plt.get_cmap('Reds')
colors = [cm((1.0 - 1.*i/len(thermal_range))) for i in range(len(thermal_range))]
fig = plt.figure()

#If x and y cavity are equal only one set of axes is defined,
#if they are not equal a set of axes is defined for each cavity. 
if laser.get_xcav().cavity == laser.get_ycav().cavity:
    ax = fig.add_subplot(1,1,1)
    ax.set_prop_cycle('color',colors)
    ax.set_xlabel('Z(cm)')
    ax.set_ylabel('Waist(cm)')
    ax.set_ylim(0,.2)
else:
    ax_x = fig.add_subplot(2,1,1)
    ax_x.set_prop_cycle('color',colors)
    ax_x.set_xlabel('Z(cm)')
    ax_x.set_ylabel('Waist(cm)')
    ax_x.set_ylim(0,.2)
    
    ax_y = fig.add_subplot(2,1,2)
    ax_y.set_prop_cycle('color',colors)
    ax_y.set_xlabel('Z(cm)')
    ax_y.set_ylabel('Waist(cm)')
    ax_y.set_ylim(0,.2)

#Loop through range of thermal lensing vaules and plot every stable cavity
for f in thermal_range:
    newcav = laser.remove_optic(V_i).insert_optic('L',f,V_i)
    xcav = newcav.get_xcav()
    ycav = newcav.get_ycav()
    if newcav.is_stable and ycav.cavity == xcav.cavity:
        Z, W = newcav.plot_waist(250)
        ax.plot(Z,W)
    elif xcav.is_stable and ycav.is_stable:
        Zx, Wx = xcav.plot_waist(250)
        Zy, Wy = ycav.plot_waist(250)
        ax_x.plot(Zx,Wx)
        ax_y.plot(Zy,Wy)

plt.show()