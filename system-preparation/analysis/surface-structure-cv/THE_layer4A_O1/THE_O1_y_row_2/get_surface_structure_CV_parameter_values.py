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
L_x = 3.74711  # simulation box length in x diection

data_x = pd.read_csv('x_THE_O1/density', delim_whitespace=True, comment='#', header=None)

x = data_x.values[:,0]

rho_x = data_x.values[:,1]

# Concatenate along columns (axis=1)
x = np.concatenate((x, x + L_x))

rho_x = np.concatenate((rho_x, rho_x))





########################
# get all local maxima #
########################
indices_peaks, _ = find_peaks(rho_x, distance=25000)
indices_peaks = indices_peaks[0:5]


###########################
# get median of each peak #
###########################
delta_x = x[1]-x[0]
index_bound = math.ceil(0.2/delta_x)

x_peaks = np.zeros(len(indices_peaks))

# Calculate the weighted means
for i in range(len(x_peaks)):

    index_lb = indices_peaks[i] - index_bound
    index_ub = indices_peaks[i] + index_bound

    x_peaks[i] = np.average(x[index_lb:index_ub], weights=rho_x[index_lb:index_ub])



#############################################
# check x component of surface structure CV #
#############################################

# cos( (nu_x * pi)/L_x * (x_i - x_k) )^eta_x
# cos( (nu_y * pi)/L_y * (y_i - y_k) )^eta_y
# exp( - (z_i - z_k)^2 / (2*sigma_z^2) )

x_k = x_peaks[0]
eta_x = 10
nu_x = 5


def cosine_func_x(x):
    
    A_x = nu_x*np.pi/L_x
    cos_x = np.cos( A_x * (x - x_k) )
    cos_pow_x = np.power(cos_x, eta_x)
    
    return cos_pow_x


cos_pow_x = cosine_func_x(x)


#################
# plot the data #
#################
val_max = np.max(rho_x)

plt.plot(0)
plt.plot(x, rho_x)
plt.plot([-L_x/2, -L_x/2], [0, val_max],'g-.')
plt.plot([L_x/2, L_x/2], [0, val_max],'g-.')
plt.plot(x[indices_peaks], rho_x[indices_peaks], 'o')

# lower bounds
plt.plot([ x[indices_peaks-index_bound] , x[indices_peaks-index_bound] ], [0, val_max], 'r--')
# upper bounds
plt.plot([ x[indices_peaks+index_bound] , x[indices_peaks+index_bound] ], [0, val_max], 'r--')

plt.plot([x_peaks, x_peaks], [0 , val_max], 'k-.')

# check cos_pow_x
plt.plot(x, cos_pow_x*val_max)

plt.grid()
plt.xlim([x[0], 2.5])
plt.ylim([0, val_max])
plt.show()


print('x_k =', round(x_k, 6))
