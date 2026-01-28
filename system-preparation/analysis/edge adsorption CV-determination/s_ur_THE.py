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
import subprocess
import os

from scipy.signal import find_peaks

# clear the plots
plt.close('all')


##########################
# load the density plots #
##########################
pwd = os.getcwd()


# THE C2 density functions
os.chdir("../../THE_layer4B_C2/xy_THE_C2/")
with open("plotDensity.py") as file:
    exec(file.read())

os.chdir("../xz_THE_C2/")
with open("plotDensity.py") as file:
    exec(file.read())

os.chdir("../yz_THE_C2/")
with open("plotDensity.py") as file:
    exec(file.read())

os.chdir(pwd)# THE O1 density functions
os.chdir("../../THE_layer4B_O1/xy_THE_O1/")
with open("plotDensity.py") as file:
    exec(file.read())

os.chdir("../xy_THE_O1/")
with open("plotDensity.py") as file:
    exec(file.read())

os.chdir("../yz_THE_O1/")
with open("plotDensity.py") as file:
    exec(file.read())

os.chdir(pwd)



# THE O1 density functions
os.chdir("../../THE_layer4A_O1/xy_THE_O1/")
with open("plotDensity.py") as file:
    exec(file.read())

os.chdir("../xy_THE_O1/")
with open("plotDensity.py") as file:
    exec(file.read())

os.chdir("../yz_THE_O1/")
with open("plotDensity.py") as file:
    exec(file.read())

os.chdir(pwd)


# ASP C3 density functions
os.chdir("../../ASP_layer4B_C3/xy_ASP_C3/")
with open("plotDensity.py") as file:
    exec(file.read())

os.chdir("../xy_ASP_C3/")
with open("plotDensity.py") as file:
    exec(file.read())

os.chdir("../yz_ASP_C3/")
with open("plotDensity.py") as file:
    exec(file.read())

os.chdir(pwd)

# ASP O2 density functions
os.chdir("../../ASP_layer4B_O2/xy_ASP_O2/")
with open("plotDensity.py") as file:
    exec(file.read())

os.chdir("../xy_ASP_O2/")
with open("plotDensity.py") as file:
    exec(file.read())

os.chdir("../yz_ASP_O2/")
with open("plotDensity.py") as file:
    exec(file.read())

os.chdir(pwd)

######################
# get all parameters #
######################
L_x =  3.74711    # [nm] simulation box length in x diection
L_y =  3.95202    # [nm] simulation box length in y diection
L_z = 17.58461    # [nm] simulation box length in z diection


# # THE C2 setup: row 1 (s_ar_THE_C2)
# zetal_y = -1.97000    # [nm]    
# zetau_y = -1.69000   # [nm]
# sigmal_y = 300
# sigmau_y = 300

# zetal_z = 1.0000    # [nm]
# zetau_z = 2.2500    # [nm]
# sigmal_z = 1000
# sigmau_z = 75


# THE O1 setup: row 1 (s_ar_THE_O1)
# zetal_y = -1.97000    # [nm]    
# zetau_y = -1.70000    # -1.68000   # [nm]
# sigmal_y = 300
# sigmau_y = 300

# zetal_z = 1.1000    # [nm]
# zetau_z = 2.2500    # [nm]
# sigmal_z = 1000
# sigmau_z = 75


# THE C2 setup: rows above kink site (s_ur_THE_C2)
zetal_y = -1.1500  # -1.12000  # [nm]    
zetau_y = 1.96000   # [nm]
sigmal_y = 150
sigmau_y = 150

zetal_z = 1.1000    # [nm]
zetau_z = 2.0500    # [nm]
sigmal_z = 1000
sigmau_z = 150



#################
# get all terms #
#################

def s_f(q, sigma, zeta):
    return 1 / (1 + np.exp(-sigma * (q - zeta)) )


def f_lu(q, sigmal, zetal, sigmau, zetau):
    f_l = s_f(q, sigmal, zetal)
    f_u = s_f(q, sigmau, zetau)

    return f_l * (1 - f_u)

############
# xy plane #
############
def row_func_xy(x, y):

    return f_lu(y, sigmal_y, zetal_y, sigmau_y, zetau_y)





############
# xz plane #
############
def row_func_xz(x, z):   #, x_b, L_x, nu_x, eta_x, z, z_b, sigma_z):

    return f_lu(z, sigmal_z, zetal_z, sigmau_z, zetau_z)


############
# yz plane #
############
def row_func_yz(y, z):

    return f_lu(y, sigmal_y, zetal_y, sigmau_y, zetau_y) * f_lu(z, sigmal_z, zetal_z, sigmau_z, zetau_z)


# y_mesh = np.linspace(-L_y/2, L_y/2, 1000)
# s_y_1 = s_f(y_mesh, sigmal_y, zetal_y)
# s_y_2 = 1 - s_f(y_mesh, sigmau_y, zetau_y)
# f_lu_val = f_lu(y_mesh, sigmal_y, zetal_y, sigmau_y, zetau_y)

# plt.plot(y_mesh, s_y_1)
# plt.plot(y_mesh, s_y_2)
# plt.plot(y_mesh, f_lu_val)


####################
# plot the xy data #
####################
# Generate a grid of x and y values
x_mesh = np.linspace(-L_x/2, L_x/2, 1000)
y_mesh = np.linspace(-L_y/2, L_y/2, 1000)
X_xy, Y_xy = np.meshgrid(x_mesh, y_mesh)

# evaluate 
s_xy = row_func_xy(X_xy, Y_xy)

# create contour plot
plt.figure(0)
plt.contour(X_xy, Y_xy, s_xy)
plt.xlabel('x')
plt.ylabel('y')
plt.gca().set_aspect('equal', adjustable='box')
#plt.colorbar(label='Function Value')

#plt.show()
###################
# plot the xz data #
####################
# Generate a grid of x and y values
z_mesh = np.linspace(0, 5, 1000)
X_xz, Z_xz = np.meshgrid(x_mesh, z_mesh)

# evaluate 
s_xz = row_func_xz(X_xz, Z_xz)

# create contour plot
plt.figure(1)
plt.contour(X_xz, Z_xz, s_xz)
plt.xlabel('x')
plt.ylabel('z')
plt.gca().set_aspect('equal', adjustable='box')
#plt.colorbar(label='Function Value')
plt.ylim([1.25, 2.5])

#plt.show()



####################
# plot the yz data #
####################
# Generate a grid of x and y values
Y_yz, Z_yz = np.meshgrid(y_mesh, z_mesh)

# evaluate
s_yz = row_func_yz(Y_yz, Z_xz)

# create contour plot
plt.figure(2)
plt.contour(Y_yz, Z_yz, s_yz)
plt.xlabel('y')
plt.ylabel('z')
plt.gca().set_aspect('equal', adjustable='box')
#plt.colorbar(label='Function Value')
plt.ylim([1.25, 2.5])

plt.show()


