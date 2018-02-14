import numpy as np
import math
import matplotlib.pyplot as plt
import filehandling
import pickle
from cavityclass import *

M_2x = float(input('Enter M-Squared for x-axis:    '))
M_2y = float(input('Enter M-Squared for y-axis:    '))
LAM = 1064*10**(-7)
LAM_x = LAM * M_2x
LAM_y = LAM * M_2y

with open('filepath.pkl', 'rb') as f:
	filepath = pickle.load(f)

laser = Cavity(filepath, LAM)

fig = plt.figure(figsize=(10,7))
ax = fig.add_subplot(1,1,1)
ax.set_xlabel('Z(cm)')
ax.set_ylabel('Spot Size(cm)')
ax.set_ylim(0,.15)

xcav = Cavity(laser.get_xcav().cavity, LAM_x)
ycav = Cavity(laser.get_ycav().cavity, LAM_y)

if xcav.cavity == ycav.cavity:
    Z, W = laser.plot_waist(250)
    ax.plot(Z,W)
else:
    Zx, Wx = xcav.plot_waist(250)
    Zy, Wy = ycav.plot_waist(250)
    ax.plot(Zx,Wx,label='xcav')
    ax.plot(Zy,Wy,label='ycav')
    ax.legend()
print('X-Axis')
print(xcav.analysis())
print('Y-Axis')
print(ycav.analysis())
plt.show()