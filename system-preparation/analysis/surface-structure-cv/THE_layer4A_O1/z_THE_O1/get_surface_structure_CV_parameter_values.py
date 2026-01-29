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
#plt.close()


#################
# load the data #
#################
data_z = pd.read_csv('density', delim_whitespace=True, comment='#', header=None)

z = data_z.values[:,0]

rho_z = data_z.values[:,1]



########################
# get all local maxima #
########################
indices_peaks, _ = find_peaks(rho_z, distance=10000)
#indices_peaks = indices_peaks[:4]


###########################
# get median of each peak #
###########################
delta_z = z[1]-z[0]
index_bound = math.ceil(0.3/delta_z)

z_peaks = np.zeros(len(indices_peaks))

# Calculate the weighted means
for i in range(len(z_peaks)):

    index_lb = indices_peaks[i] - index_bound
    index_ub = indices_peaks[i] + index_bound

    z_peaks[i] = np.average(z[index_lb:index_ub], weights=rho_z[index_lb:index_ub])


z_peaks_modal = z[indices_peaks]


# #############################################
# # check z component of surface structure CV #
# #############################################

# # cos( (nu_x * pi)/L_x * (x_i - x_k) )^eta_x
# # cos( (nu_y * pi)/L_y * (y_i - y_k) )^eta_y
# # exp( - (z_i - z_k)^2 / (2*sigma_z^2) )

# z_k = z_peaks_modal    # [nm]
# sigma_z = 0.1          # [nm]

# def gaussian_func_z(z):
    
#     gaussian_z = np.exp( - (z - z_k)**2 / (2*sigma_z**2) )
    
#     return gaussian_z

# gaussian_z = gaussian_func_z(z)



#################
# plot the data #
#################
val_max = np.max(rho_z)

plt.plot(0)
plt.plot(z, rho_z)
plt.plot(z[indices_peaks], rho_z[indices_peaks], 'o')


# lower bounds
plt.plot([ z[indices_peaks-index_bound] , z[indices_peaks-index_bound] ], [0, val_max], 'r--')
# upper bounds
plt.plot([ z[indices_peaks+index_bound] , z[indices_peaks+index_bound] ], [0, val_max], 'r--')

#plt.plot([y_peaks, y_peaks], [0 , val_max], 'k-.')

# # check gaussian_z
# plt.plot(z, gaussian_z*val_max)

plt.grid()
#plt.xlim([1.0, 1.7])
plt.show()

print('z_peaks =', round(z_peaks[0], 6))
