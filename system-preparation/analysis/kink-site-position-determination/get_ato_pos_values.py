#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 17:47:03 2024

@author: zoltan
"""


import numpy as np
import math
import pandas as pd
from matplotlib import pyplot as plt

from scipy.signal import find_peaks

# clear the plots
plt.close('all')


#################
# load the data #
#################
data_x = pd.read_csv('density_x', delim_whitespace=True, comment='#', header=None)
data_y = pd.read_csv('density_y', delim_whitespace=True, comment='#', header=None)
data_z = pd.read_csv('density_z', delim_whitespace=True, comment='#', header=None)

x = data_x.values[:,0]
rho_x = data_x.values[:,1]

y = data_y.values[:,0]
rho_y = data_y.values[:,1]

z = data_z.values[:,0]
rho_z = data_z.values[:,1]


L_x = 3.74711
L_y = 3.95202




########################
# get all local maxima #
########################
index_peak_x, _ = find_peaks(rho_x, distance=10000)
index_peak_y, _ = find_peaks(rho_y, distance=10000)
index_peak_z, _ = find_peaks(rho_z, distance=10000)

x_peak = x[index_peak_x][0] + L_x/2
y_peak = y[index_peak_y][0] + L_y/2
z_peak = z[index_peak_z][0]

x_pos = x[index_peak_x][0]
y_pos = y[index_peak_y][0]
z_pos = z[index_peak_z][0]

########################
# Zsphere.cpp function #
########################
def smoothstep(d):

    d_min = 1.0
    d_max = 1.5
    delta = d_max - d_min

    d_r = (d - d_min) / delta

    # Clamp the d_r values
    d_r[d_r < 0.0] = 0.0
    d_r[d_r > 1.0] = 1.0

    return d_r


d = np.arange(0, 2.01, 0.01)
d_r = smoothstep(d)




#################
# plot the data #
#################
d_min = 0.15
d_max = 0.25
delta = 0.5

plt.figure(0)
plt.plot(x, rho_x)
plt.plot(x[index_peak_x], rho_x[index_peak_x], 'ro')
plt.plot([x_pos-d_min, x_pos-d_min], [0, np.max(rho_x)], 'r-.')
plt.plot([x_pos+d_min, x_pos+d_min], [0, np.max(rho_x)], 'r-.')
plt.plot([x_pos-d_max, x_pos-d_max], [0, np.max(rho_x)], 'r-.')
plt.plot([x_pos+d_max, x_pos+d_max], [0, np.max(rho_x)], 'r-.')
plt.xlabel('x [nm]')
plt.ylabel(r'$\rho$ [nm]')
plt.xlim([x[index_peak_x]-delta, x[index_peak_x]+delta])
plt.grid()
#plt.show()

plt.figure(1)
plt.plot(y, rho_y)
plt.plot(y[index_peak_y], rho_y[index_peak_y], 'ro')
plt.plot([y_pos-d_min, y_pos-d_min], [0, np.max(rho_x)], 'r-.')
plt.plot([y_pos+d_min, y_pos+d_min], [0, np.max(rho_x)], 'r-.')
plt.plot([y_pos-d_max, y_pos-d_max], [0, np.max(rho_x)], 'r-.')
plt.plot([y_pos+d_max, y_pos+d_max], [0, np.max(rho_x)], 'r-.')
plt.xlabel('y [nm]')
plt.ylabel(r'$\rho$ [nm]')
plt.xlim([y[index_peak_y]-delta, y[index_peak_y]+delta])
plt.grid()
#plt.show()

plt.figure(2)
plt.plot(z, rho_z)
plt.plot(z[index_peak_z], rho_z[index_peak_z], 'ro')
plt.plot([z_pos-d_min, z_pos-d_min], [0, np.max(rho_x)], 'r-.')
plt.plot([z_pos+d_min, z_pos+d_min], [0, np.max(rho_x)], 'r-.')
plt.plot([z_pos-d_max, z_pos-d_max], [0, np.max(rho_x)], 'r-.')
plt.plot([z_pos+d_max, z_pos+d_max], [0, np.max(rho_x)], 'r-.')
plt.xlabel('z [nm]')
plt.ylabel(r'$\rho$ [nm]')
plt.xlim([z[index_peak_z]-delta, z[index_peak_z]+delta])
plt.grid()
plt.show()


print('x_peak =', round(x_peak, 6))
print('y_peak =', round(y_peak, 6))
print('z_peak =', round(z_peak, 6))




