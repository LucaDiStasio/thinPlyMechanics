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
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
# for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)


def modeIERR(x):
    return (np.sin(x)*(((1-np.sin(0.5*x)*np.sin(0.5*x)*np.cos(0.5*x)*np.cos(0.5*x))*np.cos(0.5*x))/(1+np.sin(np.sin(0.5*x))*np.sin(0.5*x))+np.cos(1.5*x))**2)

def modeIERRcurvature(x):
    return ((((1-np.sin(0.5*x)*np.sin(0.5*x)*np.cos(0.5*x)*np.cos(0.5*x))*np.cos(0.5*x))/(1+np.sin(np.sin(0.5*x))*np.sin(0.5*x))+np.cos(1.5*x))**2)

def chordSize(x):
    return (np.sin(x))

def modeIIERR(x):
    return (np.sin(x)*(((1-np.sin(0.5*x)*np.sin(0.5*x)*np.cos(0.5*x)*np.cos(0.5*x))*np.sin(0.5*x))/(1+np.sin(np.sin(0.5*x))*np.sin(0.5*x))+np.sin(1.5*x))**2)

def modeIIERRcurvature(x):
    return ((((1-np.sin(0.5*x)*np.sin(0.5*x)*np.cos(0.5*x)*np.cos(0.5*x))*np.sin(0.5*x))/(1+np.sin(np.sin(0.5*x))*np.sin(0.5*x))+np.sin(1.5*x))**2)


plt.close("all")

angles = np.linspace(0.0, 180, num=300)

# Gs = []
# for angle in angles:
#     Gs.append(G(angles,epsilon,alpha))

plt.figure()
plt.plot(angles, modeIERR(angles*np.pi/180.0), 'b-')
plt.xlabel(r'$\Delta\theta [^{\circ}]$')
plt.ylabel(r'$\frac{G_{I}}{E^{*}\varepsilon_{0}^{2}R} [-]$')
plt.title(r'Mode I ERR Shape Factor')
plt.legend((r'$Mode\ I$'),loc='best')
plt.grid(True)
#plt.show()
#plt.savefig(join(outdir,filename + '.png'), bbox_inches='tight')

plt.figure()
plt.plot(angles, modeIIERR(angles*np.pi/180.0), 'b-')
plt.xlabel(r'$\Delta\theta [^{\circ}]$')
plt.ylabel(r'$\frac{G_{II}}{E^{*}\varepsilon_{0}^{2}R} [-]$')
plt.title(r'Mode II ERR Shape Factor')
plt.legend((r'$Mode\ II$'),loc='best')
plt.grid(True)
#plt.show()
#plt.savefig(join(outdir,filename + '.png'), bbox_inches='tight')

plt.figure()
plt.plot(angles, modeIERR(angles*np.pi/180.0), 'b-')
plt.plot(angles, modeIIERR(angles*np.pi/180.0), 'r-')
plt.xlabel(r'$\Delta\theta [^{\circ}]$')
plt.ylabel(r'$\frac{G_{I}}{E^{*}\varepsilon_{0}^{2}R} [-]$')
plt.title(r'ERR Shape Factor')
plt.legend((r'$Mode\ I$',r'$Mode\ II$'),loc='best')
plt.grid(True)
#plt.show()
#plt.savefig(join(outdir,filename + '.png'), bbox_inches='tight')

plt.figure()
plt.plot(angles, modeIERRcurvature(angles*np.pi/180.0), 'b-')
plt.xlabel(r'$\Delta\theta [^{\circ}]$')
plt.ylabel(r'$\frac{G_{I}}{E^{*}\varepsilon_{0}^{2}R\sin{\Delta\theta}} [-]$')
plt.title(r'Mode I ERR Curvature Factor')
plt.legend((r'$Mode\ I$'),loc='best')
plt.grid(True)
#plt.show()
#plt.savefig(join(outdir,filename + '.png'), bbox_inches='tight')

plt.figure()
plt.plot(angles, modeIIERRcurvature(angles*np.pi/180.0), 'b-')
plt.xlabel(r'$\Delta\theta [^{\circ}]$')
plt.ylabel(r'$\frac{G_{II}}{E^{*}\varepsilon_{0}^{2}R\sin{\Delta\theta}} [-]$')
plt.title(r'Mode II ERR Curvature Factor')
plt.legend((r'$Mode\ II$'),loc='best')
plt.grid(True)
#plt.show()
#plt.savefig(join(outdir,filename + '.png'), bbox_inches='tight')

plt.figure()
plt.plot(angles, modeIERRcurvature(angles*np.pi/180.0), 'b-')
plt.plot(angles, modeIIERRcurvature(angles*np.pi/180.0), 'r-')
plt.xlabel(r'$\Delta\theta [^{\circ}]$')
plt.ylabel(r'$\frac{G_{I}}{E^{*}\varepsilon_{0}^{2}R\sin{\Delta\theta}} [-]$')
plt.title(r'ERR Curvature Factor')
plt.legend((r'$Mode\ I$',r'$Mode\ II$'),loc='best')
plt.grid(True)
#plt.show()
#plt.savefig(join(outdir,filename + '.png'), bbox_inches='tight')

plt.figure()
plt.plot(angles, chordSize(angles*np.pi/180.0), 'b-')
plt.plot(angles, modeIERRcurvature(angles*np.pi/180.0), 'r-')
plt.xlabel(r'$\Delta\theta [^{\circ}]$')
plt.ylabel(r'$\frac{G_{I}}{E^{*}\varepsilon_{0}^{2}Rf\left(\Delta\theta\right)} [-]$')
plt.title(r'Mode I ERR Chord-Size and Curvature Factor')
plt.legend((r'Chord Size',r'Curvature'),loc='best')
plt.grid(True)

#plt.savefig(join(outdir,filename + '.png'), bbox_inches='tight')

plt.figure()
plt.plot(angles, chordSize(angles*np.pi/180.0), 'b-')
plt.plot(angles, modeIIcurvature(angles*np.pi/180.0), 'b-')
plt.xlabel(r'$\Delta\theta [^{\circ}]$')
plt.ylabel(r'$\frac{G_{II}}{E^{*}\varepsilon_{0}^{2}Rf\left(\Delta\theta\right)} [-]$')
plt.title(r'Mode II ERR Chord-Size and Shape Factor')
plt.legend((r'Chord Size',r'Curvature'),loc='best')
plt.grid(True)

#plt.savefig(join(outdir,filename + '.png'), bbox_inches='tight')

plt.show()
