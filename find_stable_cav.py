import numpy as np
import math
import matplotlib.pyplot as plt
from cavityclass import *

LAM = 1064*10**(-7)

ds28 = Cavity('datatest',LAM)

#loops through a range of thermal lensing values, creates a cavity for each value.
thermal_range = np.arange(16,22,.1):
for f in thermal_range:
    newcav = ds28.remove_optic(5).insert_optic('L',f,5)
    if newcav.is_stable:
        num_stab += 1
        