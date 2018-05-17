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
#import os
from os.path import isfile, join, exists
#from os import listdir, stat, makedirs
from datetime import datetime
from time import strftime
#from platform import platform
from openpyxl import Workbook
from openpyxl import load_workbook
import numpy as np
from scipy import fftpack
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)


def model(x,A,B,C,D):
    return (A*np.sin(B*x+C)+D)

def linear(x,A,B):
    return (A*x+B)

def readData(wd,workbook,boundaryCase):
    wb = load_workbook(filename=join(wd,workbook), read_only=True)
    gIvcctWorksheet = wb['GI-VCCT']
    gIjintWorksheet = wb['GI-Jint']
    gIIvcctWorksheet = wb['GII-VCCT']
    gTOTvcctWorksheet = wb['GTOT-VCCT']
    gTOTjintWorksheet = wb['GTOT-Jint']
    czWorksheet = wb['ContactZone']
    data = {}
    Vf = [0.000079,0.0001,0.2,0.3,0.4,0.5,0.55,0.6,0.65]
    Vfcolumns = {0.000079:'F',0.0001:'G',0.2:'H',0.3:'I',0.4:'J',0.5:'K',0.55:'L',0.6:'M',0.65:'N'}
    theta = [10.0,20.0,30.0,40.0,50.0,60.0,70.0,80.0,90.0,100.0,110.0,120.0,130.0,140.0,150.0]
    nTheta = len(theta)
    initTheta = 4
    for c,case in enumerate(boundaryCase):
        for v,value in enumerate(Vf):
            values = []
            for n in range(0,nTheta):
                values.append(gIvcctWorksheet[Vfcolumns[value]+str(4+c*nTheta+n)].value)
            data['GI']['VCCT'][case][v+1] = {'Vf':value,'theta':theta,'values':values}
            values = []
            for n in range(0,nTheta):
                values.append(gIjintWorksheet[Vfcolumns[value]+str(4+c*nTheta+n)].value)
            data['GI']['Jint'][case][v+1] = {'Vf':value,'theta':theta,'values':values}
            values = []
            for n in range(0,nTheta):
                values.append(gIIvcctWorksheet[Vfcolumns[value]+str(4+c*nTheta+n)].value)
            data['GII'][case][v+1] = {'Vf':value,'theta':theta,'values':values}
            values = []
            for n in range(0,nTheta):
                values.append(gTOTvcctWorksheet[Vfcolumns[value]+str(4+c*nTheta+n)].value)
            data['GTOT']['VCCT'][case][v+1] = {'Vf':value,'theta':theta,'values':values}
            values = []
            for n in range(0,nTheta):
                values.append(gTOTjintWorksheet[Vfcolumns[value]+str(4+c*nTheta+n)].value)
            data['GTOT']['Jint'][case][v+1] = {'Vf':value,'theta':theta,'values':values}
            values = []
            for n in range(0,nTheta):
                values.append(czWorksheet[Vfcolumns[value]+str(4+c*nTheta+n)].value)
            data['CZ'][case][v+1] = {'Vf':value,'theta':theta,'values':values}
    return data

def interpolateData(outdir,data,boundaryCase):
    for c,case in enumerate(boundaryCase):
        for v,vfData in enumerate(data['GI']['VCCT'][case]):
            czStart = -1
            for a,angle in data['CZ'][case][v]['values']:
                if angle>0.0:
                    czStart = a
                    break
            filename = datetime.now().strftime('%Y-%m-%d') + '_GI-VCCT-Interpolation_' + case + '_Vf' + str(vfData['Vf'])
            xs = vfData['theta'][:czStart]
            ys = vfData['values'][:czStart]
            maxIndex = 0
            maxValue = vfData['values'][maxIndex]
            for i,y in enumerate(ys):
                if y>maxValue:
                    maxIndex = i
                    maxValue = y
            res, cov = optimize.curve_fit(model,xs,ys,p0=[maxValue,1.0/xs[maxIndex],0.0,0.0],method='dogbox')
            stderr = np.sqrt(np.diag(cov))
            angles = np.linspace(0.0, xs[-1]+5, num=300)
            data['GI']['VCCT'][case][v]['coeff'] = res
            data['GI']['VCCT'][case][v]['cov'] = cov
            data['GI']['VCCT'][case][v]['std'] = stderr
            data['GI']['VCCT'][case][v]['valueAtNoDebond'] = model(0.0, *res)
            plt.figure()
            plt.plot(vfData['theta'], vfData['values'], 'ko')
            plt.plot(angles, model(angles, *res), 'b-')
            plt.xlabel(r'$\Delta\theta [^{\circ}]$')
            plt.ylabel(r'$G_{I} [\frac{J}{m^{2}}]$')
            plt.title(r'Interpolation of GI-VCCT, ' + case + ', $V_{f}=' + str(vfData['Vf']*100.0 + '%$')
            plt.legend(['data', 'interpolant'], loc=1)
            savefig(join(outdir,filename + '.png'), bbox_inches='tight')
        for v,vfData in enumerate(data['GI']['Jint'][case]):
            czStart = -1
            for a,angle in data['CZ'][case][v]['values']:
                if angle>0.0:
                    czStart = a
                    break
            filename = datetime.now().strftime('%Y-%m-%d') + '_GI-Jint-Interpolation_' + case + '_Vf' + str(vfData['Vf'])
            xs = vfData['theta'][:czStart]
            ys = vfData['values'][:czStart]
            maxIndex = 0
            maxValue = vfData['values'][maxIndex]
            for i,y in enumerate(ys):
                if y>maxValue:
                    maxIndex = i
                    maxValue = y
            res, cov = optimize.curve_fit(model,xs,ys,p0=[maxValue,1.0/xs[maxIndex],0.0,0.0],method='dogbox')
            stderr = np.sqrt(np.diag(cov))
            angles = np.linspace(0.0, xs[-1]+5, num=300)
            data['GI']['Jint'][case][v]['coeff'] = res
            data['GI']['Jint'][case][v]['cov'] = cov
            data['GI']['Jint'][case][v]['std'] = stderr
            data['GI']['Jint'][case][v]['valueAtNoDebond'] = model(0.0, *res)
            plt.figure()
            plt.plot(vfData['theta'], vfData['values'], 'ko')
            plt.plot(angles, model(angles, *res), 'b-')
            plt.xlabel(r'$\Delta\theta [^{\circ}]$')
            plt.ylabel(r'$G_{I} [\frac{J}{m^{2}}]$')
            plt.title(r'Interpolation of GI-Jint, ' + case + ', $V_{f}=' + str(vfData['Vf']*100.0 + '%$')
            plt.legend(['data', 'interpolant'], loc=1)
            savefig(join(outdir,filename + '.png'), bbox_inches='tight')
        for v,vfData in enumerate(data['GII']['VCCT'][case]):
            filename = datetime.now().strftime('%Y-%m-%d') + '_GII-VCCT-Interpolation_' + case + '_Vf' + str(vfData['Vf'])
            xs = vfData['theta']
            ys = vfData['values']
            maxIndex = 0
            maxValue = vfData['values'][maxIndex]
            for i,y in enumerate(ys):
                if y>maxValue:
                    maxIndex = i
                    maxValue = y
            res, cov = optimize.curve_fit(model,xs,ys,p0=[maxValue,1.0/xs[maxIndex],0.0,0.0],method='dogbox')
            stderr = np.sqrt(np.diag(cov))
            angles = np.linspace(0.0, xs[-1]+5, num=300)
            data['GII']['VCCT'][case][v]['coeff'] = res
            data['GII']['VCCT'][case][v]['cov'] = cov
            data['GII']['VCCT'][case][v]['std'] = stderr
            data['GII']['VCCT'][case][v]['valueAtNoDebond'] = model(0.0, *res)
            plt.figure()
            plt.plot(vfData['theta'], vfData['values'], 'ko')
            plt.plot(angles, model(angles, *res), 'b-')
            plt.xlabel(r'$\Delta\theta [^{\circ}]$')
            plt.ylabel(r'$G_{II} [\frac{J}{m^{2}}]$')
            plt.title(r'Interpolation of GII-VCCT, ' + case + ', $V_{f}=' + str(vfData['Vf']*100.0 + '%$')
            plt.legend(['data', 'interpolant'], loc=1)
            savefig(join(outdir,filename + '.png'), bbox_inches='tight')
        for v,vfData in enumerate(data['GTOT']['VCCT'][case]):
            filename = datetime.now().strftime('%Y-%m-%d') + '_GTOT-VCCT-Interpolation_' + case + '_Vf' + str(vfData['Vf'])
            xs = vfData['theta']
            ys = vfData['values']
            maxIndex = 0
            maxValue = vfData['values'][maxIndex]
            for i,y in enumerate(ys):
                if y>maxValue:
                    maxIndex = i
                    maxValue = y
            res, cov = optimize.curve_fit(model,xs,ys,p0=[maxValue,1.0/xs[maxIndex],0.0,0.0],method='dogbox')
            stderr = np.sqrt(np.diag(cov))
            angles = np.linspace(0.0, xs[-1]+5, num=300)
            data['GTOT']['VCCT'][case][v]['coeff'] = res
            data['GTOT']['VCCT'][case][v]['cov'] = cov
            data['GTOT']['VCCT'][case][v]['std'] = stderr
            data['GTOT']['VCCT'][case][v]['valueAtNoDebond'] = model(0.0, *res)
            plt.figure()
            plt.plot(vfData['theta'], vfData['values'], 'ko')
            plt.plot(angles, model(angles, *res), 'b-')
            plt.xlabel(r'$\Delta\theta [^{\circ}]$')
            plt.ylabel(r'$G_{TOT} [\frac{J}{m^{2}}]$')
            plt.title(r'Interpolation of GTOT-VCCT, ' + case + ', $V_{f}=' + str(vfData['Vf']*100.0 + '%$')
            plt.legend(['data', 'interpolant'], loc=1)
            savefig(join(outdir,filename + '.png'), bbox_inches='tight')
        for v,vfData in enumerate(data['GTOT']['Jint'][case]):
            filename = datetime.now().strftime('%Y-%m-%d') + '_GTOT-Jint-Interpolation_' + case + '_Vf' + str(vfData['Vf'])
            xs = vfData['theta']
            ys = vfData['values']
            maxIndex = 0
            maxValue = vfData['values'][maxIndex]
            for i,y in enumerate(ys):
                if y>maxValue:
                    maxIndex = i
                    maxValue = y
            res, cov = optimize.curve_fit(model,xs,ys,p0=[maxValue,1.0/xs[maxIndex],0.0,0.0],method='dogbox')
            stderr = np.sqrt(np.diag(cov))
            angles = np.linspace(0.0, xs[-1]+5, num=300)
            data['GTOT']['Jint'][case][v]['coeff'] = res
            data['GTOT']['Jint'][case][v]['cov'] = cov
            data['GTOT']['Jint'][case][v]['std'] = stderr
            data['GTOT']['Jint'][case][v]['valueAtNoDebond'] = model(0.0, *res)
            plt.figure()
            plt.plot(vfData['theta'], vfData['values'], 'ko')
            plt.plot(angles, model(angles, *res), 'b-')
            plt.xlabel(r'$\Delta\theta [^{\circ}]$')
            plt.ylabel(r'$G_{TOT} [\frac{J}{m^{2}}]$')
            plt.title(r'Interpolation of GTOT-Jint, ' + case + ', $V_{f}=' + str(vfData['Vf']*100.0 + '%$')
            plt.legend(['data', 'interpolant'], loc=1)
            savefig(join(outdir,filename + '.png'), bbox_inches='tight')
        for v,vfData in enumerate(data['CZ'][case]):
            czStart = -1
            for a,angle in vfData['values']:
                if angle>0.0:
                    czStart = a
                    break
            filename = datetime.now().strftime('%Y-%m-%d') + '_ContactZone-Interpolation_' + case + '_Vf' + str(vfData['Vf'])
            xs = vfData['theta'][czStart:]
            phis = []
            for p,phi in enumerate(vfData['values']):
                phis.append(100*phi/vfData['theta'][p])
            ys = phis[czStart:]
            for p,phi in enumerate(phis):
                ys = 100*phi/xs[p]
            res, cov = optimize.curve_fit(linear,xs,ys,method='dogbox')
            stderr = np.sqrt(np.diag(cov))
            angles = np.linspace(xs[0], xs[-1]+5, num=300)
            data['CZ'][case][v]['coeff'] = res
            data['CZ'][case][v]['cov'] = cov
            data['CZ'][case][v]['std'] = stderr
            plt.figure()
            plt.plot(vfData['theta'], phis, 'ko')
            plt.plot(angles, linear(angles, *res), 'b-')
            plt.xlabel(r'$\Delta\theta [^{\circ}]$')
            plt.ylabel(r'$\frac{\Delta\Phi}{\Delta\theta} [%]$')
            plt.title(r'Interpolation of normalized contact zone size, ' + case + ', $V_{f}=' + str(vfData['Vf']*100.0 + '%$')
            plt.legend(['data', 'interpolant'], loc=1)
            savefig(join(outdir,filename + '.png'), bbox_inches='tight')

def writeData(outdir,workbookname,data,boundaryCase):
    wb = Workbook()
    gIvcctWorksheet = wb.create_sheet(title='GI-VCCT')
    gIvcctWorksheet['A1'] = 'GI-VCCT'
    gIvcctWorksheet['A2'] = 'BOUNDARY CONDITIONS'
    gIvcctWorksheet['A3'] = 'NORTH'
    gIvcctWorksheet['B3'] = 'SOUTH'
    gIvcctWorksheet['C3'] = 'EAST'
    gIvcctWorksheet['D3'] = 'WEST'
    gIvcctWorksheet['E3'] = 'Vf [%]'
    gIvcctWorksheet['F3'] = 'Value at no debond [J/m^2]'
    gIvcctWorksheet['G2'] = 'Coefficients'
    gIvcctWorksheet['G3'] = 'A [J/m^2]'
    gIvcctWorksheet['H3'] = 'B [1/°]'
    gIvcctWorksheet['I3'] = 'C [°]'
    gIvcctWorksheet['J3'] = 'D [J/m^2]'
    gIvcctWorksheet['K2'] = 'Covariance'
    gIvcctWorksheet['K3'] = 'cov(1,1)'
    gIvcctWorksheet['L3'] = 'cov(1,2)'
    gIvcctWorksheet['M3'] = 'cov(1,3)'
    gIvcctWorksheet['N3'] = 'cov(1,4)'
    gIvcctWorksheet['O3'] = 'cov(2,1)'
    gIvcctWorksheet['P3'] = 'cov(2,2)'
    gIvcctWorksheet['Q3'] = 'cov(2,3)'
    gIvcctWorksheet['R3'] = 'cov(2,4)'
    gIvcctWorksheet['S3'] = 'cov(3,1)'
    gIvcctWorksheet['T3'] = 'cov(3,2)'
    gIvcctWorksheet['O3'] = 'cov(3,3)'
    gIvcctWorksheet['P3'] = 'cov(3,4)'
    gIvcctWorksheet['Q3'] = 'cov(4,1)'
    gIvcctWorksheet['R3'] = 'cov(4,2)'
    gIvcctWorksheet['S3'] = 'cov(4,3)'
    gIvcctWorksheet['T3'] = 'cov(4,4)'
    gIvcctWorksheet['U3'] = 'std err [J/m^2]'
    gIjintWorksheet = wb.create_sheet(title='GI-Jint')
    gIjintWorksheet['A1'] = 'GI-Jint'
    gIjintWorksheet['A2'] = 'BOUNDARY CONDITIONS'
    gIjintWorksheet['A3'] = 'NORTH'
    gIjintWorksheet['B3'] = 'SOUTH'
    gIjintWorksheet['C3'] = 'EAST'
    gIjintWorksheet['D3'] = 'WEST'
    gIjintWorksheet['E3'] = 'Vf [%]'
    gIjintWorksheet['F3'] = 'Value at no debond [J/m^2]'
    gIjintWorksheet['G2'] = 'Coefficients'
    gIjintWorksheet['G3'] = 'A [J/m^2]'
    gIjintWorksheet['H3'] = 'B [1/°]'
    gIjintWorksheet['I3'] = 'C [°]'
    gIjintWorksheet['J3'] = 'D [J/m^2]'
    gIjintWorksheet['K2'] = 'Covariance'
    gIjintWorksheet['K3'] = 'cov(1,1)'
    gIjintWorksheet['L3'] = 'cov(1,2)'
    gIjintWorksheet['M3'] = 'cov(1,3)'
    gIjintWorksheet['N3'] = 'cov(1,4)'
    gIjintWorksheet['O3'] = 'cov(2,1)'
    gIjintWorksheet['P3'] = 'cov(2,2)'
    gIjintWorksheet['Q3'] = 'cov(2,3)'
    gIjintWorksheet['R3'] = 'cov(2,4)'
    gIjintWorksheet['S3'] = 'cov(3,1)'
    gIjintWorksheet['T3'] = 'cov(3,2)'
    gIjintWorksheet['O3'] = 'cov(3,3)'
    gIjintWorksheet['P3'] = 'cov(3,4)'
    gIjintWorksheet['Q3'] = 'cov(4,1)'
    gIjintWorksheet['R3'] = 'cov(4,2)'
    gIjintWorksheet['S3'] = 'cov(4,3)'
    gIjintWorksheet['T3'] = 'cov(4,4)'
    gIjintWorksheet['U3'] = 'std err [J/m^2]'
    gIIvcctWorksheet = wb.create_sheet(title='GII-VCCT')
    gIIvcctWorksheet['A1'] = 'GII-VCCT'
    gIIvcctWorksheet['A2'] = 'BOUNDARY CONDITIONS'
    gIIvcctWorksheet['A3'] = 'NORTH'
    gIIvcctWorksheet['B3'] = 'SOUTH'
    gIIvcctWorksheet['C3'] = 'EAST'
    gIIvcctWorksheet['D3'] = 'WEST'
    gIIvcctWorksheet['E3'] = 'Vf [%]'
    gIIvcctWorksheet['F3'] = 'Value at no debond [J/m^2]'
    gIIvcctWorksheet['G2'] = 'Coefficients'
    gIIvcctWorksheet['G3'] = 'A [J/m^2]'
    gIIvcctWorksheet['H3'] = 'B [1/°]'
    gIIvcctWorksheet['I3'] = 'C [°]'
    gIIvcctWorksheet['J3'] = 'D [J/m^2]'
    gIIvcctWorksheet['K2'] = 'Covariance'
    gIIvcctWorksheet['K3'] = 'cov(1,1)'
    gIIvcctWorksheet['L3'] = 'cov(1,2)'
    gIIvcctWorksheet['M3'] = 'cov(1,3)'
    gIIvcctWorksheet['N3'] = 'cov(1,4)'
    gIIvcctWorksheet['O3'] = 'cov(2,1)'
    gIIvcctWorksheet['P3'] = 'cov(2,2)'
    gIIvcctWorksheet['Q3'] = 'cov(2,3)'
    gIIvcctWorksheet['R3'] = 'cov(2,4)'
    gIIvcctWorksheet['S3'] = 'cov(3,1)'
    gIIvcctWorksheet['T3'] = 'cov(3,2)'
    gIIvcctWorksheet['O3'] = 'cov(3,3)'
    gIIvcctWorksheet['P3'] = 'cov(3,4)'
    gIIvcctWorksheet['Q3'] = 'cov(4,1)'
    gIIvcctWorksheet['R3'] = 'cov(4,2)'
    gIIvcctWorksheet['S3'] = 'cov(4,3)'
    gIIvcctWorksheet['T3'] = 'cov(4,4)'
    gIIvcctWorksheet['U3'] = 'std err [J/m^2]'
    gTOTvcctWorksheet = wb.create_sheet(title='GTOT-VCCT')
    gTOTvcctWorksheet['A1'] = 'GTOT-VCCT'
    gTOTvcctWorksheet['A2'] = 'BOUNDARY CONDITIONS'
    gTOTvcctWorksheet['A3'] = 'NORTH'
    gTOTvcctWorksheet['B3'] = 'SOUTH'
    gTOTvcctWorksheet['C3'] = 'EAST'
    gTOTvcctWorksheet['D3'] = 'WEST'
    gTOTvcctWorksheet['E3'] = 'Vf [%]'
    gTOTvcctWorksheet['F3'] = 'Value at no debond [J/m^2]'
    gTOTvcctWorksheet['G2'] = 'Coefficients'
    gTOTvcctWorksheet['G3'] = 'A [J/m^2]'
    gTOTvcctWorksheet['H3'] = 'B [1/°]'
    gTOTvcctWorksheet['I3'] = 'C [°]'
    gTOTvcctWorksheet['J3'] = 'D [J/m^2]'
    gTOTvcctWorksheet['K2'] = 'Covariance'
    gTOTvcctWorksheet['K3'] = 'cov(1,1)'
    gTOTvcctWorksheet['L3'] = 'cov(1,2)'
    gTOTvcctWorksheet['M3'] = 'cov(1,3)'
    gTOTvcctWorksheet['N3'] = 'cov(1,4)'
    gTOTvcctWorksheet['O3'] = 'cov(2,1)'
    gTOTvcctWorksheet['P3'] = 'cov(2,2)'
    gTOTvcctWorksheet['Q3'] = 'cov(2,3)'
    gTOTvcctWorksheet['R3'] = 'cov(2,4)'
    gTOTvcctWorksheet['S3'] = 'cov(3,1)'
    gTOTvcctWorksheet['T3'] = 'cov(3,2)'
    gTOTvcctWorksheet['O3'] = 'cov(3,3)'
    gTOTvcctWorksheet['P3'] = 'cov(3,4)'
    gTOTvcctWorksheet['Q3'] = 'cov(4,1)'
    gTOTvcctWorksheet['R3'] = 'cov(4,2)'
    gTOTvcctWorksheet['S3'] = 'cov(4,3)'
    gTOTvcctWorksheet['T3'] = 'cov(4,4)'
    gTOTvcctWorksheet['U3'] = 'std err [J/m^2]'
    gTOTjintWorksheet = wb.create_sheet(title='GTOT-Jint')
    gTOTjintWorksheet['A1'] = 'GTOT-Jint'
    gTOTjintWorksheet['A2'] = 'BOUNDARY CONDITIONS'
    gTOTjintWorksheet['A3'] = 'NORTH'
    gTOTjintWorksheet['B3'] = 'SOUTH'
    gTOTjintWorksheet['C3'] = 'EAST'
    gTOTjintWorksheet['D3'] = 'WEST'
    gTOTjintWorksheet['E3'] = 'Vf [%]'
    gTOTjintWorksheet['F3'] = 'Value at no debond [J/m^2]'
    gTOTjintWorksheet['G2'] = 'Coefficients'
    gTOTjintWorksheet['G3'] = 'A [J/m^2]'
    gTOTjintWorksheet['H3'] = 'B [1/°]'
    gTOTjintWorksheet['I3'] = 'C [°]'
    gTOTjintWorksheet['J3'] = 'D [J/m^2]'
    gTOTjintWorksheet['K2'] = 'Covariance'
    gTOTjintWorksheet['K3'] = 'cov(1,1)'
    gTOTjintWorksheet['L3'] = 'cov(1,2)'
    gTOTjintWorksheet['M3'] = 'cov(1,3)'
    gTOTjintWorksheet['N3'] = 'cov(1,4)'
    gTOTjintWorksheet['O3'] = 'cov(2,1)'
    gTOTjintWorksheet['P3'] = 'cov(2,2)'
    gTOTjintWorksheet['Q3'] = 'cov(2,3)'
    gTOTjintWorksheet['R3'] = 'cov(2,4)'
    gTOTjintWorksheet['S3'] = 'cov(3,1)'
    gTOTjintWorksheet['T3'] = 'cov(3,2)'
    gTOTjintWorksheet['O3'] = 'cov(3,3)'
    gTOTjintWorksheet['P3'] = 'cov(3,4)'
    gTOTjintWorksheet['Q3'] = 'cov(4,1)'
    gTOTjintWorksheet['R3'] = 'cov(4,2)'
    gTOTjintWorksheet['S3'] = 'cov(4,3)'
    gTOTjintWorksheet['T3'] = 'cov(4,4)'
    gTOTjintWorksheet['U3'] = 'std err [J/m^2]'
    wb.save(filename = join(outdir,workbookname))
    Vf = [0.000079,0.0001,0.2,0.3,0.4,0.5,0.55,0.6,0.65]
    nVf = len(Vf)
    initVf = 4

def main(argv):

    inpDir = 'C:/Abaqus_WD'
    outdir = 'C:/Users/lucad/OneDrive/01_Luca/07_DocMASE/07_Data/03_FEM/Interpolation'

    inpWorkbook = ''
    outWorkbook = ''

    if not os.path.exists(outdir):
            os.mkdir(outdir)

    boundaryCases = ['free','geomcoupling','fixedv','fixedvlinearu']



if __name__ == "__main__":
    main(sys.argv[1:])
