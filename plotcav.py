import numpy as np
import math
import matplotlib.pyplot as plt
from cavityclass import *

M_2 = 1
LAM = 1064*10**(-7) * M_2

ds28 = Cavity('ds28.dat', LAM)

print(ds28.q(ds28.L))

Z, W = ds28.plot_waist(250)

fig = plt.figure(figsize=(10,7))
ax = fig.add_subplot(1,1,1)
ax.set_xlabel('Z(cm)')
ax.set_ylabel('Spot Size(cm)')
ax.set_ylim(0,.15)

xcav = ds28.get_xcav()
ycav = ds28.get_ycav()

if xcav == ycav:
	Z, W = ds28.plot_waist(250)
	ax.plot(Z,W)
else:
	Zx, Wx = xcav.plot_waist(250)
	Zy, Wy = ycav.plot_waist(250)
	ax.plot(Zx,Wx,label='xcav')
	ax.plot(Zy,Wy,label='ycav')
	ax.legend()
plt.show()