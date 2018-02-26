#Extra-cavity propagation 
#2/20/18

import numpy as np
import math
import matplotlib.pyplot as plt
from filehandling import filepath
from cavityclass import *

Zr_x = 34.2 #cm
Zr_y = 30.12 #cm
M2_x = 1.32
M2_y = 1.348
Z0_x = 34.4 #cm
Z0_y = 39.4 #cm

#Zr_x = 33.92
#Zr_y = 31.3
#M2_x = 1.312
#M2_y = 1.332
#Z0_x = 32.1
#Z0_y = 35.9

q_x = complex(Z0_x,Zr_x)
q_y = complex(Z0_y,Zr_y)

wx = np.sqrt((4*1064*10**(-7)*M2_x/math.pi)*(q_x.imag + ((q_x.real)**2)/q_x.imag))
wy = np.sqrt((4*1064*10**(-7)*M2_y/math.pi)*(q_y.imag + ((q_y.real)**2)/q_y.imag))
print('start spot x = ',wx)
print('start spot y = ',wy)

filecavity = open(filepath, 'r+')

print('q_x start = ',q_x)
print('q_y start = ',q_y)

cavity = []
for line in filecavity:
    part = []
    for s in line.split():
        try:
            part.append(float(s))
        except ValueError:
            part.append(s)
    cavity.append(part)

print('cavity = ', cavity)
    
for optic in cavity:
    q_x = prop_q(q_x,optics[optic[0]](optic[1]))
    q_y = prop_q(q_y,optics[optic[0]](optic[1]))
   
print('q_x end = ',q_x)
print('q_y end = ',q_y)

wx = np.sqrt((4*1064*10**(-7)*M2_x/math.pi)*(q_x.imag + ((q_x.real)**2)/q_x.imag))
wy = np.sqrt((4*1064*10**(-7)*M2_y/math.pi)*(q_y.imag + ((q_y.real)**2)/q_y.imag))
print('spot x = ',wx)
print('spot y = ',wy)