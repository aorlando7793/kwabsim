import os.path
import numpy as np
import math
import matplotlib.pyplot as plt
from filehandling import filepath
from cavityclass import *

V_i = 5 #int(input('Enter Position of Nd:YVO_4 in Cavity:    '))
M_2x = 1 #float(input('Enter M-Squared for x axis:    '))
M_2y = 1 #float(input('Enter M-Squared for y axis:    '))
LAM = 1064*10**(-7)
LAMx = LAM * M_2x
LAMy = LAM * M_2y
zrx = 36 #float(input('Enter Rayleigh Range for x axis:    '))
zry = 42 #float(input('Enter Rayleigh Range for y axis:    '))

laser = Cavity(filepath, LAM)
laser_x = Cavity(laser.get_xcav().cavity, LAMx)
laser_y = Cavity(laser.get_ycav().cavity, LAMy)
#laser_list = [newcav = laser.remove_optic(5).insert_optic('L',i,5) for i in np.arange(15,25,.1) if newcav.is_stable]
min_diff_x = abs(zrx - laser_x.q0.imag) 
min_diff_y = abs(zry - laser_y.q0.imag)

for i in np.arange(10,40,.01):
    new_xcav = laser_x.remove_optic(V_i).insert_optic('Cx',i,V_i)
    if new_xcav.is_stable:
        diff_x = abs(zrx - new_xcav.q0.imag)
        if (diff_x < min_diff_x):
            min_diff_x = diff_x
            bestfit_x = new_xcav

    new_ycav = laser_y.remove_optic(V_i).insert_optic('Cy',i,V_i)
    if new_ycav.is_stable:
        diff_y =  abs(zry - new_ycav.q0.imag)
        if (diff_y < min_diff_y):
            min_diff_y = diff_y
            bestfit_y = new_ycav
#diff is a list of how much each cavity's initial q differs from the experimental value.

bestfit = laser.remove_optic(V_i).insert_optic('Cx', bestfit_x.cavity[V_i-1][1], V_i).insert_optic('Cy', bestfit_y.cavity[V_i-1][1], V_i+1)

print(bestfit_x.cavity)
print(bestfit_y.cavity)
print('Thermal Lensing X:', bestfit_x.cavity[V_i - 1])
print('Rayleigh Range X:', bestfit_x.q0.imag)
print('Thermal Lensing Y:', bestfit_y.cavity[V_i - 1])
print('Rayleigh Range Y:', bestfit_y.q0.imag)
#file_name = input('Enter File Name:')
#file_path = os.path.join(save_path, file_name+".dat")
#file = open(file_path,'w')
#for optic in bestfit.cavity:
    #file.write(str(optic[0]) + ' ' + str(optic[1]) + '\n')