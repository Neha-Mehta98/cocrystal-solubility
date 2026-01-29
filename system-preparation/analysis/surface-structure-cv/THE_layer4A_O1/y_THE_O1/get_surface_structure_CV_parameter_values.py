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
plt.close()


#################
# load the data #
#################
L_y = 3.95202  # [nm] simulation box length in x diection

data_y = pd.read_csv('density', delim_whitespace=True, comment='#', header=None)

y = data_y.values[:,0]

rho_y = data_y.values[:,1]

# Concatenate along columns (axis=1)
y = np.concatenate((y, y + L_y))

rho_y = np.concatenate((rho_y, rho_y))





########################
# get all local maxima #
########################
indices_peaks, _ = find_peaks(rho_y, distance=10000)
indices_peaks = indices_peaks[1:5]


###########################
# get median of each peak #
###########################
delta_y = y[1]-y[0]
index_bound = math.ceil(0.2/delta_y)

y_peaks = np.zeros(len(indices_peaks))

# Calculate the weighted means
for i in range(len(y_peaks)):

    index_lb = indices_peaks[i] - index_bound
    index_ub = indices_peaks[i] + index_bound

    y_peaks[i] = np.average(y[index_lb:index_ub], weights=rho_y[index_lb:index_ub])


y_peaks_modal = y[indices_peaks]


#############################################
# check y component of surface structure CV #
#############################################

# cos( (nu_x * pi)/L_x * (x_i - x_k) )^eta_x
# cos( (nu_y * pi)/L_y * (y_i - y_k) )^eta_y
# exp( - (z_i - z_k)^2 / (2*sigma_z^2) )

eta_y = 80
nu_y = 1



def cosine_func_y(y, y_k):
    
    A_y = nu_y*np.pi/L_y
    cos_y = np.cos( A_y * (y - y_k) )
    cos_pow_y = np.power(cos_y, eta_y)
    
    return cos_pow_y


cos_pow_y_1 = cosine_func_y(y, y_peaks_modal[0])
cos_pow_y_2 = cosine_func_y(y, y_peaks_modal[1])
cos_pow_y_3 = cosine_func_y(y, y_peaks_modal[2])
cos_pow_y_4 = cosine_func_y(y, y_peaks_modal[3])



#################
# plot the data #
#################
val_max = np.max(rho_y)

plt.plot(0)
plt.plot(y, rho_y)
plt.plot([-L_y/2, -L_y/2], [0, val_max],'g-.')
plt.plot([L_y/2, L_y/2], [0, val_max],'g-.')
plt.plot(y[indices_peaks], rho_y[indices_peaks], 'o')

# lower bounds
plt.plot([ y[indices_peaks-index_bound] , y[indices_peaks-index_bound] ], [0, val_max], 'r--')
# upper bounds
plt.plot([ y[indices_peaks+index_bound] , y[indices_peaks+index_bound] ], [0, val_max], 'r--')

#plt.plot([y_peaks, y_peaks], [0 , val_max], 'k-.')

# check cos_pow_y
plt.plot(y, cos_pow_y_1*val_max)
plt.plot(y, cos_pow_y_2*val_max)
plt.plot(y, cos_pow_y_3*val_max)
plt.plot(y, cos_pow_y_4*val_max)
plt.show()

#plt.grid()
#plt.xlim([y[0], 2.15])
#plt.ylim([0, val_max])

y_k = y[indices_peaks]
print('y_k =', y_k)
