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

def model1(x,A,B,C,D):
    return (A*np.sin(B*x))

def model2(x,A,B,C,D):
    return (A*np.sin(B*x+C))

def model3(x,A,B,C,D):
    return (A*np.sin(B*x+C)+D)

def model4(x,A,B,C,D):
    return (A*np.sin(B*x)+D)

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

ft_GI = fftpack.fft(data[:,1])
ft_GII = fftpack.fft(data[:,2])
ft_GTOT = fftpack.fft(data[:,3])
freq_GI = fftpack.fftfreq(data[:,1].shape[0], data[1,0] - data[0,0])
freq_GII = fftpack.fftfreq(data[:,2].shape[0], data[1,0] - data[0,0])
freq_GTOT = fftpack.fftfreq(data[:,3].shape[0], data[1,0] - data[0,0])
period_GI = 1 / freq_GI
period_GII = 1 / freq_GII
period_GTOT = 1 / freq_GTOT

print(freq_GI)
print(freq_GII)
print(freq_GTOT)

plt.figure()
plt.plot(freq_GI, abs(ft_GI), 'o')
plt.xlim(0, 1.01*np.max(freq_GI))
plt.xlabel('Frequencies')
plt.ylabel('Power - GI')
plt.show()

plt.figure()
plt.plot(freq_GII, abs(ft_GII), 'o')
plt.xlim(0, 1.01*np.max(freq_GI))
plt.xlabel('Frequencies')
plt.ylabel('Power - GII')
plt.show()

plt.figure()
plt.plot(freq_GTOT, abs(ft_GTOT), 'o')
plt.xlim(0, 1.01*np.max(freq_GI))
plt.xlabel('Frequencies')
plt.ylabel('Power - GTOT')
plt.show()

models = [model1,model2,model3,model4]
titles = ['A*sin(B*x)','A*sin(B*x+C)','A*sin(B*x+C)+D','A*sin(B*x)+D']

for m,model in enumerate(models):
    res_GI, cov_GI = optimize.curve_fit(model,data[:6,0],data[:6,1],p0=[0.3,1.0/20.0,0.0,0.0])
    res_GII, cov_GII = optimize.curve_fit(model,data[:,0],data[:,2],p0=[0.7,1.0/60.0,0.0,0.0])
    res_GTOT, cov_GTOT = optimize.curve_fit(model,data[:,0],data[:,3],p0=[0.7,1.0/60.0,0.0,0.0])

    print('res_GI')
    print(res_GI)
    print('res_GII')
    print(res_GII)
    print('res_GTOT')
    print(res_GTOT)

    print('cov_GI')
    print(cov_GI)
    print('cov_GII')
    print(cov_GII)
    print('cov_GTOT')
    print(cov_GTOT)

    angles = np.linspace(0., 150., num=300)
    angles1 = np.linspace(0., 60., num=120)

    plt.figure()
    plt.plot(data[:,0], data[:,1], 'ro')
    plt.plot(angles1, model(angles1, *res_GI), 'r-')
    plt.plot(data[:,0], data[:,2], 'bo')
    plt.plot(angles, model(angles, *res_GII), 'b-')
    plt.plot(data[:,0], data[:,3], 'go')
    plt.plot(angles, model(angles, *res_GTOT), 'g-')
    plt.xlabel('deltatheta')
    plt.ylabel('G/GO [-]')
    plt.title(titles[m])
    plt.legend(['GI,data', 'GI,interp','GII,data', 'GII,interp','GTOT,data','GTOT,interp'], loc=1)

    plt.show()
