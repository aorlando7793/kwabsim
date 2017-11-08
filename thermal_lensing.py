import numpy as np
import math
import matplotlib.pyplot as plt
from cavityclass import *

LAM = 1064*10**(-7)

q_exp = -4.55 + 1j*27.8

ds28 = Cavity('datatest.dat',LAM)

#laser_list = [newcav = ds28.remove_optic(5).insert_optic('L',i,5) for i in np.arange(15,25,.1) if newcav.is_stable]
laser_list = []
#loops through a range of thermal lensing values, creates a cavity for each one and appends it to laser_list.
for i in np.arange(15,25,.01):
    newcav = ds28.remove_optic(5).insert_optic('L',i,5)
    if newcav.is_stable:
        laser_list.append(newcav)
#diff is a list of how much each cavity's initial q differs from the experimental value.
diff = [abs(q_exp - laser.q0) for laser in laser_list]
#finds index of minimum difference
min_i = diff.index(min(diff))
best_lens = laser_list[min_i]

print('Cavity with Thermal Lensing:', best_lens.cavity)

file_name = input('Enter File name:')
file = open(file_name,'w')
for optic in best_lens.cavity:
    file.write("%s\n" % optic)