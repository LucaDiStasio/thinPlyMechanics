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


def modeIERR(x):
    return (np.sin(x)*(((1-np.sin(0.5*x)*np.sin(0.5*x)*np.cos(0.5*x)*np.cos(0.5*x))*np.cos(0.5*x))/(1+np.sin(np.sin(0.5*x))*np.sin(0.5*x))+np.cos(1.5*x)))

def modeIIERR(Ef,nuf,Em,num):
    muf = 0.5*Ef/(1+nuf)
    mum = 0.5*Em/(1+num)

    kf = 3-4*nuf
    km = 3-4*num

    dundA = (muf*(km+1)-mum*(kf+1))/(muf*(km+1)+mum*(kf+1))
    dundB = (muf*(km-1)-mum*(kf-1))/(muf*(km+1)+mum*(kf+1))

    return dundA,dundB


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
plt.plot(angles[:2*maxIndex], Gs[maxIndex]*np.sin((90/angles[maxIndex])*angles[:2*maxIndex]*np.pi/180.0), 'r-')
plt.xlabel(r'$\Delta\theta [^{\circ}]$')
plt.ylabel(r'$G [-]$')
plt.title(r'Analytical solution from Toya')
plt.legend(('Full', r'$Asin(B\Delta\theta)$'),loc='best')
plt.grid(True)
plt.show()

angles2 = np.linspace(0.0, 115, num=300)

maxIndex = 0
ys = numCoeffF(angles2*np.pi/180.0,*coeffs)
for v,value in enumerate(ys):
    if value > ys[maxIndex]:
        maxIndex = v

res, cov = optimize.curve_fit(model,angles2,ys,p0=[ys[maxIndex],1.0/angles2[maxIndex],0.0,0.0],method='dogbox')

plt.figure()
plt.plot(angles, numCoeffF(angles*np.pi/180.0,*coeffs), 'b-')
plt.plot(angles2, model(angles2,*res), 'r-')
plt.xlabel(r'$\Delta\theta [^{\circ}]$')
plt.ylabel(r'$G [-]$')
plt.title(r'Analytical solution from Toya')
plt.legend(('num amplitude', r'$Asin(B\Delta\theta+C)+D$'),loc='best')
plt.grid(True)
plt.show()

plt.figure()
#plt.plot(angles, np.sin(angles*np.pi/180.0)*d(angles*np.pi/180.0,*coeffs)*(d(angles*np.pi/180.0,*coeffs)-2*c(angles*np.pi/180.0,*coeffs)*np.cos(angles*np.pi/180.0))/c(angles*np.pi/180.0,*coeffs), 'b-')
plt.plot(angles, np.sin(angles*np.pi/180.0)*d(angles*np.pi/180.0,*coeffs)*d(angles*np.pi/180.0,*coeffs)/c(angles*np.pi/180.0,*coeffs), 'b-')
plt.plot(angles, np.sin(angles*np.pi/180.0)*d(angles*np.pi/180.0,*coeffs)*(-2*c(angles*np.pi/180.0,*coeffs)*np.cos(angles*np.pi/180.0))/c(angles*np.pi/180.0,*coeffs), 'r-')
plt.plot(angles, c(angles*np.pi/180.0,*coeffs)*np.sin(angles*np.pi/180.0), 'g-')
plt.plot(angles, np.sin(angles*np.pi/180.0)*d(angles*np.pi/180.0,*coeffs)*d(angles*np.pi/180.0,*coeffs)/c(angles*np.pi/180.0,*coeffs)+np.sin(angles*np.pi/180.0)*d(angles*np.pi/180.0,*coeffs)*(-c(angles*np.pi/180.0,*coeffs)*np.cos(angles*np.pi/180.0))/c(angles*np.pi/180.0,*coeffs), 'k-')
plt.plot(angles, c(angles*np.pi/180.0,*coeffs)*np.sin(angles*np.pi/180.0)+np.sin(angles*np.pi/180.0)*d(angles*np.pi/180.0,*coeffs)*(-c(angles*np.pi/180.0,*coeffs)*np.cos(angles*np.pi/180.0))/c(angles*np.pi/180.0,*coeffs), 'c-')
plt.plot(angles, np.sin(angles*np.pi/180.0)*d(angles*np.pi/180.0,*coeffs)*d(angles*np.pi/180.0,*coeffs)/c(angles*np.pi/180.0,*coeffs)+np.sin(angles*np.pi/180.0)*d(angles*np.pi/180.0,*coeffs)*(-2*c(angles*np.pi/180.0,*coeffs)*np.cos(angles*np.pi/180.0))/c(angles*np.pi/180.0,*coeffs), 'm-')
plt.plot(angles, np.sin(angles*np.pi/180.0)*d(angles*np.pi/180.0,*coeffs)*d(angles*np.pi/180.0,*coeffs)/c(angles*np.pi/180.0,*coeffs)+np.sin(angles*np.pi/180.0)*d(angles*np.pi/180.0,*coeffs)*(-2*c(angles*np.pi/180.0,*coeffs)*np.cos(angles*np.pi/180.0))/c(angles*np.pi/180.0,*coeffs)+c(angles*np.pi/180.0,*coeffs)*np.sin(angles*np.pi/180.0), 'y-')
plt.xlabel(r'$\Delta\theta [^{\circ}]$')
plt.ylabel(r'$G [-]$')
plt.title(r'Analytical solution from Toya')
plt.legend(('T1','T2','T3','T1+0.5*T2','T3+0.5*T2','T1+T2','T1+T2+T3'),loc='best')
plt.grid(True)
plt.show()
