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

def c(theta,eps):
    return 2*np.exp(-2*eps(theta-np.pi))
    
def d(theta,eps,alpha):
    return -(4-(1-alpha)*(1+4*eps*eps)*np.sin(theta)*np.sin(theta))/(3+alpha-(1-alpha)*(np.cos(theta)-2*eps*np.sin(theta))*np.exp(2*eps*(theta-np.pi)))

def coeffF(theta,eps,alpha):
    return (d(theta,eps,alpha)*(d(theta,eps,alpha)-2*c(theta,eps)*np.cos(theta))+c(theta,eps)*c(theta,eps))/(8*c(theta,eps))

def G(theta,eps,alpha):
    def np.sin(theta)*coeffF(theta,eps,alpha)
    
Ef = 70.0 # [GPa]
nuf = 0.2 # [-]
Em = 3.5 # [GPa]
num = 0.4 # [-]

alpha,beta = dundursParams(Ef,nuf,Em,num)

epsilon = 0.5*np.log((1-beta)/(1+beta))/np.pi