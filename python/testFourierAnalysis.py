#!/usr/bin/env Python
# -*- coding: utf-8 -*-

'''
=====================================================================================

Copyright (c) 2017 - 2018 Université de Lorraine & Luleå tekniska universitet
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

Tested with Python 2.7 Anaconda 2.4.1 (64-bit) distribution
       in Windows 10.

'''

import sys, os
from os.path import isfile, join, exists
import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack, optimize 

def model(x,A,B,C):
    return (A*np.sin(B*x+C))

plt.close("all")

#wd = 'C:/02_Local-folder/01_Luca/01_WD/data/thinplymechanics'
wd = 'C:/Users/lucdis/Documents/WD/data/thinplymechanics'
filename = 'BEM-data.csv'

with open(join(wd,filename),'r') as csv:
    lines = csv.readlines()

theta = []
GI = []
GII = []
GTOT = []

for line in lines[2:]:
    theta.append(float(line.replace('\n','').split(',')[0]))
    GI.append(float(line.replace('\n','').split(',')[1]))
    GII.append(float(line.replace('\n','').split(',')[2]))
    GTOT.append(float(line.replace('\n','').split(',')[3]))

data = np.transpose(np.array([theta,GI,GII,GTOT]))

plt.figure()
plt.plot(data[:,0], data[:,1:])
plt.xlabel('deltatheta')
plt.ylabel('G/GO [-]')
plt.legend(['GI', 'GII', 'GTOT'], loc=1)
plt.show()

ft_populations = fftpack.fft(data[:,1:], axis=0)
frequencies = fftpack.fftfreq(data[:,1:].shape[0], data[1,0] - data[0,0])
periods = 1 / frequencies

plt.figure()
plt.plot(periods, abs(ft_populations), 'o')
plt.xlim(0, 180)
plt.xlabel('Period')
plt.ylabel('Power')
plt.show()

res_GI, cov_GI = optimize.curve_fit(model,data[:,0],data[:,1])
res_GII, cov_GII = optimize.curve_fit(model,data[:,0],data[:,2])
res_GTOT, cov_GTOT = optimize.curve_fit(model,data[:,0],data[:,3])

angles = np.linspace(0., 180., num=360)

plt.figure()
plt.plot(data[:,0], data[:,1], 'ro')
plt.plot(angles, model(angles, *res_GI), 'r-')
plt.plot(data[:,0], data[:,2], 'bo')
plt.plot(angles, model(angles, *res_GII), 'b-')
plt.plot(data[:,0], data[:,3], 'go')
plt.plot(angles, model(angles, *res_GTOT), 'g-')
plt.xlabel('deltatheta')
plt.ylabel('G/GO [-]')
plt.legend(['GI,data', 'GI,interp','GII,data', 'GII,interp','GTOT,data','GTOT,interp'], loc=1)

plt.show()
