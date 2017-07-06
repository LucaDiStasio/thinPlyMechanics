#!/usr/bin/env Python
# -*- coding: utf-8 -*-

'''
=====================================================================================

Copyright (c) 2016 Université de Lorraine & Luleå tekniska universitet
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
       Matlab R2007b, R2012a
       Windows 7 Integral Edition, Windows 10.

'''

from os.path import isfile, join, exists
from os import makedirs,listdir
from datetime import datetime
from time import strftime
from platform import platform
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.mlab import griddata
from matplotlib2tikz import save as tikz
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
# for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)

def grid(minx, miny, maxx, maxy, x, y, z, resX=1000, resY=1000):
    "Convert 3 column data to matplotlib grid"
    xi = np.linspace(minx, maxx, resX)
    yi = np.linspace(miny, maxy, resY)
    Z = griddata(x, y, z, xi, yi)
    #print('z=griddata() done')
    X, Y = np.meshgrid(xi, yi)
    return X, Y, Z
    
statusfile = '2017-02-02_AbaqusParametricRun_2017-02-02_18-05-02'

wd = 'D:\\01_Luca\\07_Data\\03_FEM'

statusfile += '.sta'

print('===============================================================================================\n')
print('===============================================================================================\n')
print('\n')
print('                                           LATEX GRAPHICS CREATION\n')
print('\n')
print('                                               CONTOUR PLOTS\n')
print('\n')
print('                                 Starting on ' + datetime.now().strftime('%Y-%m-%d') + ' at ' + datetime.now().strftime('%H:%M:%S') + '\n')
print('\n')
print('                                      Platform: ' + platform() + '\n')
print('\n')
print('===============================================================================================\n')
print('===============================================================================================\n')
print('\n')

print('\n')
print('Reading from status file: ' + statusfile + ' in folder ' + wd + '\n')
print('\n')
with open(join(wd,statusfile),'r') as sta:
    lines = sta.readlines()
print('\n')
print('Done.\n')
print('\n')
for i,line in enumerate(lines[3:4]):
    words = line.split(',')
    project = words[0]
    print('Starting creation of Latex contour plots on project ' + project + '\n')
    # define input file name
    inpname = project + '.inp'
    inpfullpath = join(wd,project,'abqinp',inpname)
    # define csv output folder
    csvfolder = join(wd,project,'csv')
    # define dat output folder
    datfolder = join(wd,project,'dat')
    # define latex output folder
    latexfolder = join(wd,project,'latex')
    # define pdf output folder
    pdffolder = join(wd,project,'pdf')
    boundaryNodes = []
    fiberInterfaceNodes = []
    with open(join(csvfolder,'defboundaryNodesCoords' + '.csv'),'r') as csv:
        nodes = csv.readlines()
    for node in nodes[2:]:
        boundaryNodes.append([float(node.split(',')[3]),float(node.split(',')[4])])
    with open(join(csvfolder,'deffiberInterfaceNodesCoords' + '.csv'),'r') as csv:
        nodes = csv.readlines()
    for node in nodes[2:]:
        fiberInterfaceNodes.append([float(node.split(',')[3]),float(node.split(',')[4])])
    boundaryNodes = np.array(boundaryNodes)
    fiberInterfaceNodes = np.array(fiberInterfaceNodes)
    fiberstresses = []
    with open(join(csvfolder,'fibersubset-elasticstresses' + '.csv'),'r') as csv:
        nodes = csv.readlines()
    for node in nodes[2:]:
        fiberstresses.append([float(node.split(',')[2]),float(node.split(',')[3]),float(node.split(',')[4]),float(node.split(',')[5]),float(node.split(',')[6]),float(node.split(',')[7])])
    fiberstresses = np.array(fiberstresses)
    matrixstresses = []
    with open(join(csvfolder,'matrixsubset-elasticstresses' + '.csv'),'r') as csv:
        nodes = csv.readlines()
    for node in nodes[2:]:
        matrixstresses.append([float(node.split(',')[2]),float(node.split(',')[3]),float(node.split(',')[4]),float(node.split(',')[5]),float(node.split(',')[6]),float(node.split(',')[7])])
    matrixstresses = np.array(matrixstresses)
    #plt.plot(boundaryNodes[:,0], boundaryNodes[:,1],'k.')
    #plt.plot(fiberInterfaceNodes[:,0], fiberInterfaceNodes[:,1],'k.')
    for j, node in enumerate(boundaryNodes):
        if j<len(boundaryNodes)-1:
            plt.plot(np.array([node[0],boundaryNodes[j+1,0]]),np.array([node[1],boundaryNodes[j+1,1]]),'k-')
        else:
            plt.plot(np.array([node[0],boundaryNodes[0,0]]),np.array([node[1],boundaryNodes[0,1]]),'k-')
    for j, node in enumerate(fiberInterfaceNodes):
        if j<len(fiberInterfaceNodes)-1:
            plt.plot(np.array([node[0],fiberInterfaceNodes[j+1,0]]),np.array([node[1],fiberInterfaceNodes[j+1,1]]),'k-')
        else:
            plt.plot(np.array([node[0],fiberInterfaceNodes[0,0]]),np.array([node[1],fiberInterfaceNodes[0,1]]),'k-')
    Xf, Yf, Zf = grid(np.min(boundaryNodes[:,0]),np.min(boundaryNodes[:,1]),np.max(boundaryNodes[:,0]),np.max(boundaryNodes[:,1]),fiberstresses[:,0],fiberstresses[:,1],fiberstresses[:,2],100,100)
    Xm, Ym, Zm = grid(np.min(boundaryNodes[:,0]),np.min(boundaryNodes[:,1]),np.max(boundaryNodes[:,0]),np.max(boundaryNodes[:,1]),matrixstresses[:,0],matrixstresses[:,1],matrixstresses[:,2],100,100)
    plt.contourf(Xf,Yf,Zf)
    plt.contourf(Xm,Ym,Zm)
    plt.xlabel(r"x "r"$\left[\mu m\right]$")
    plt.ylabel(r"z "r"$\left[\mu m\right]$")
    plt.title(r"Spatial distribution of stress component "r"$\sigma_{xx}$")
    plt.grid(True)
    bar = plt.colorbar()
    bar.set_label(r"$\sigma_{xx}\left[MPa\right]$",rotation=270)
    plt.axes().set_aspect('equal', 'datalim')
    plt.show()
