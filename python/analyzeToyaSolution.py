#!/usr/bin/env Python
# -*- coding: utf-8 -*-

'''
=====================================================================================

Copyright (c) 2016-2018 Université de Lorraine & Luleå tekniska universitet
Author: Luca Di Stasio <luca.distasio@gmail.com>
                       <luca.distasio@ingpec.eu>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

=====================================================================================

DESCRIPTION



Tested with Python 2.7 Anaconda 2.4.1 (64-bit) distribution in Windows 10.

'''

import sys
import os
from os.path import isfile, join, exists
#from os import listdir, stat, makedirs
from datetime import datetime
from time import strftime
import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
# for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)

def dundursParams(Ef,nuf,Em,num):
    muf = 0.5*Ef/(1+nuf)
    mum = 0.5*Em/(1+num)
    
    kf = 3-4*nuf
    km = 3-4*num
    
    dundA = (muf*(km+1)-mum*(kf+1))/(muf*(km+1)+mum*(kf+1))
    dundB = (muf*(km-1)-mum*(kf-1))/(muf*(km+1)+mum*(kf+1))
    
    return dundA,dundB

def c(theta,epsil,alpha):
    return 2*np.exp(-2*epsil*(theta-np.pi))
    
def d(theta,epsil,alpha):
    return -(4-(1-alpha)*(1+4*epsil*epsil)*np.sin(theta)*np.sin(theta))/(3+alpha-(1-alpha)*(np.cos(theta)-2*epsil*np.sin(theta))*np.exp(2*epsil*(theta-np.pi)))

def numCoeffF(theta,epsil,alpha):
    return (d(theta,epsil,alpha)*(d(theta,epsil,alpha)-2*c(theta,epsil,alpha)*np.cos(theta))+c(theta,epsil,alpha)*c(theta,epsil,alpha))

def denCoeffF(theta,epsil,alpha):
    return 1/(8*c(theta,epsil,alpha))
    
def coeffF(theta,epsil,alpha):
    return numCoeffF(theta,epsil,alpha)*denCoeffF(theta,epsil,alpha)

def G(theta,epsil,alpha):
    return np.sin(theta)*coeffF(theta,epsil,alpha)

plt.close("all")

Ef = 70.8 # [GPa]
nuf = 0.22 # [-]
Em = 2.79 # [GPa]
num = 0.33 # [-]

alpha,beta = dundursParams(Ef,nuf,Em,num)

epsilon = 0.5*np.log((1-beta)/(1+beta))/np.pi

coeffs = [epsilon,alpha]

angles = np.linspace(0.0, 180, num=300)

# Gs = []
# for angle in angles:
#     Gs.append(G(angles,epsilon,alpha))

plt.figure()
plt.plot(angles, G(angles*np.pi/180.0,*coeffs), 'b-')
plt.plot(angles, np.sin(angles*np.pi/180.0), 'k-')
plt.plot(angles, coeffF(angles*np.pi/180.0,*coeffs), 'r-')
plt.plot(angles, denCoeffF(angles*np.pi/180.0,*coeffs), 'g-')
plt.plot(angles, numCoeffF(angles*np.pi/180.0,*coeffs), 'c-')
plt.xlabel(r'$\Delta\theta [^{\circ}]$')
plt.ylabel(r'$G [-]$')
plt.title(r'Analytical solution from Toya')
plt.legend(('Full', r'$sin(\Delta\theta)$','Amplitude function',r'$\frac{1}{8c(\Delta\theta)}$','Numerator'),loc='best')
plt.grid(True)
plt.show()
#plt.savefig(join(outdir,filename + '.png'), bbox_inches='tight')

maxIndex = 0
Gs = G(angles*np.pi/180.0,*coeffs)
for v,value in enumerate(Gs):
    if value > Gs[maxIndex]:
        maxIndex = v

plt.figure()
plt.plot(angles, G(angles*np.pi/180.0,*coeffs), 'b-')
plt.plot(angles, Gs[maxIndex]*np.sin(angles*np.pi/180.0), 'k-')
plt.xlabel(r'$\Delta\theta [^{\circ}]$')
plt.ylabel(r'$G [-]$')
plt.title(r'Analytical solution from Toya')
plt.legend(('Full', r'$Asin(\Delta\theta)$'),loc='best')
plt.grid(True)
plt.show()