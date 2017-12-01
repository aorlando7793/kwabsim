import os.path
import numpy as np
import math
import matplotlib.pyplot as plt
from cavityclass import *

save_path = 'C:/Users/R&D Group/Python/kwabsim-master'

V_i = int(input('Enter Position of Nd:YVO_4 in Cavity:    '))
M_2x = float(input('Enter M-Squared for x axis:    '))
M_2y = float(input('Enter M-Squared for y axis:    '))
LAM = 1064*10**(-7)
LAMx = LAM * M_2x
LAMy = LAM * M_2y
zrx = float(input('Enter Rayleigh Range for x axis:    '))
zry = float(input('Enter Rayleigh Range for y axis:    '))
zr_invx = 1.0/zrx
zr_invy = 1.0/zry

ds28 = Cavity('ds28.dat', LAM)
ds28_x = Cavity(ds28.get_xcav().cavity, LAMx)
ds28_y = Cavity(ds28.get_ycav().cavity, LAMy)
#laser_list = [newcav = ds28.remove_optic(5).insert_optic('L',i,5) for i in np.arange(15,25,.1) if newcav.is_stable]
laser_listx = []
laser_listy = []
#loops through a range of thermal lensing values, creates a cavity for each one and appends it to laser_list.
for i in np.arange(10,40,.01):
    new_xcav = ds28_x.remove_optic(V_i).insert_optic('Cx',i,V_i)
    new_ycav = ds28_y.remove_optic(V_i).insert_optic('Cy',i,V_i)
    if new_xcav.is_stable and new_ycav.is_stable:
        laser_listx.append(new_xcav)
        laser_listy.append(new_ycav)
#diff is a list of how much each cavity's initial q differs from the experimental value.
diffx = [abs(zr_invx - (1/laser.q0.imag)) for laser in laser_listx]
diffy = [abs(zr_invy - (1/laser.q0.imag)) for laser in laser_listy]
#finds index of minimum difference
min_ix = diffx.index(min(diffx))
bestfit_x = laser_listx[min_ix]
min_iy = diffy.index(min(diffy))
bestfit_y = laser_listy[min_iy]

bestfit = ds28.remove_optic(V_i).insert_optic('Cx', bestfit_x.cavity[V_i-1][1], V_i).insert_optic('Cy', bestfit_y.cavity[V_i-1][1], V_i+1)

print('Thermal Lensing X:', bestfit_x.cavity[V_i - 1])
print('Rayleigh Range X:', bestfit_x.q0.imag)
print('Thermal Lensing Y:', bestfit_y.cavity[V_i - 1])
print('Rayleigh Range Y:', bestfit_y.q0.imag)
file_name = input('Enter File Name:')
file_path = os.path.join(save_path, file_name+".dat")
file = open(file_path,'w')
for optic in bestfit.cavity:
    file.write(str(optic[0]) + ' ' + str(optic[1]) + '\n')