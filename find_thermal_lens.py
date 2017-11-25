import os.path
import numpy as np
import math
import matplotlib.pyplot as plt
from cavityclass import *

save_path = 'C:/Users/R&D Group/Python/kwabsim-master/ThermalLensing/F -100 -100 35 F'

V_i = int(input('Enter Position of Nd:YVO_4 in Cavity:    '))
M_2 = float(input('Enter M-Squared:    '))
LAM = 1064*10**(-7) * M_2
zr = float(input('Enter Rayleigh Range:    '))
zr_inv = 1.0/zr 

ds28 = Cavity('testfile.dat',LAM)

#laser_list = [newcav = ds28.remove_optic(5).insert_optic('L',i,5) for i in np.arange(15,25,.1) if newcav.is_stable]
laser_list = []
#loops through a range of thermal lensing values, creates a cavity for each one and appends it to laser_list.
for i in np.arange(10,40,.01):
    newcav = ds28.remove_optic(V_i).insert_optic('L',i,V_i)
    if newcav.is_stable:
        laser_list.append(newcav)
#diff is a list of how much each cavity's initial q differs from the experimental value.
diff = [abs(zr_inv - (1/laser.q0.imag)) for laser in laser_list]
#finds index of minimum difference
min_i = diff.index(min(diff))
best_lens = laser_list[min_i]

print('Thermal Lensing:', best_lens.cavity[V_i - 1])
print('Rayleigh Range:', best_lens.q0.imag)

file_name = input('Enter File Name:')
file_path = os.path.join(save_path, file_name+".dat")
file = open(file_path,'w')
for optic in best_lens.cavity:
    for char in optic:
        file.write("%s " % char)