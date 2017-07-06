#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
=====================================================================================

Copyright (c) 2016-2017 Universite de Lorraine & Lulea tekniska universitet
Author: Luca Di Stasio <luca.distasio@gmail.com>
                       <luca.distasio@ingpec.eu>

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in
the documentation and/or other materials provided with the distribution
Neither the name of the Université de Lorraine or Luleå tekniska universitet
nor the names of its contributors may be used to endorse or promote products
derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.

=====================================================================================

DESCRIPTION



Tested with Abaqus Python 2.6 (64-bit) distribution in Windows 7.

'''

import sys
from os.path import isfile, join, exists
from os import makedirs,listdir,remove
from datetime import datetime
from time import strftime
from platform import platform
import numpy as np
import re
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
# for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)
from createLatexScatterPlots import *

def plotRadialSectionsOverSims(wd,outdir,prefix,lines,sourceprefix,variable):
    varpis = []
    varlabels = []
    for i,line in enumerate(lines[1:]):
        words = line.split(',')
        project = words[0]
        # define input file name
        inpname = project + '.inp'
        inpfullpath = join(wd,project,'abqinp',inpname)
        # define csv output folder
        csvfolder = join(wd,project,'csv')
        # define dat output folder
        datfolder = join(wd,project,'dat')
        # define latex output folder
        latexfolder = join(outdir,prefix,'latex')
        # define pdf output folder
        pdffolder = join(outdir,prefix,'pdf')
        with open(inpfullpath,'r') as inp:
            values = inp.readlines()
        theta = 0
        for value in values:
            if 'Crack Angular Aperture' in value:
                theta = float(value.replace('\n','').replace('--','').replace('**','').replace('deg','').split(':')[-1])
        psi = []
        var = []
        with open(join(csvfolder,sourceprefix + '.csv'),'r') as csv:
            values = csv.readlines()
        for value in values[1:]:
            if float(value.split(',')[1]) not in psi:
                psi.append(float(value.split(',')[1]))
            datafile = join(datfolder,value.split(',')[5].replace(' ','').replace('\n',''))
            with open(datafile,'r') as dat:
                sectionValues = dat.readlines()
            xy = []
            for sectionValue in sectionValues:
                if len(sectionValue.replace('\n','').replace(' ',''))>0 and 'X' not in sectionValue:
                    parts = sectionValue.replace('\n','').split(' ')
                    temp = []
                    for part in parts:
                        if part!='':
                            temp.append(float(part))
                    xy.append(temp)
            xy = np.array(xy)
            xy = xy[xy[:,0].argsort()]
            if variable in str(value.split(',')[0]):
                var.append(xy)
            xy =[]
        temppis = []
        templabels = []
        for j,V in enumerate(var):
            plt.figure(j+1)
            pi, = plt.plot(V[:,0],V[:,1],color=(1,0,float(i)/len(lines[1:])),linestyle='-',linewidth=1.)
            temppis.append(pi)
            templabels.append(r'$\theta \left[^{\circ}\right]=' + str(np.around(theta,decimals=0)) +'$')
        varpis.append(temppis)
        varlabels.append(templabels)
    for j,V in enumerate(var):
        plt.figure(j+1)
        pis = []
        labels = []
        for k in range(0,len(varpis)):
            pis.append(varpis[k][j])
            labels.append(varlabels[k][j])
        plt.xlabel(r'$\rho \left[\mu m\right]$')
        if 'S11' in variable:
            plt.ylabel(r'$\sigma_{xx} \left[MPa\right]$')
            plt.title(r'Stress distribution $\sigma_{xx}$ along radial section at $\psi=' + str(psi[j]) + '^{\circ}$')
        elif 'S22' in variable:
            plt.ylabel(r'$\sigma_{zz} \left[MPa\right]$')
            plt.title(r'Stress distribution $\sigma_{zz}$ along radial section at $\psi=' + str(psi[j]) + '^{\circ}$')
        elif 'S12' in variable:
            plt.ylabel(r'$\sigma_{xz} \left[MPa\right]$')
            plt.title(r'Stress distribution $\sigma_{xz}$ along radial section at $\psi=' + str(psi[j]) + '^{\circ}$')
        elif 'EE11' in variable:
            plt.ylabel(r'$\varepsilon_{xx} \left[-\right]$')
            plt.title(r'Strain distribution $\varepsilon_{xx}$ along radial section at $\psi=' + str(psi[j]) + '^{\circ}$')
        elif 'EE22' in variable:
            plt.ylabel(r'$\varepsilon_{zz} \left[-\right]$')
            plt.title(r'Strain distribution $\varepsilon_{zz}$ along radial section at $\psi=' + str(psi[j]) + '^{\circ}$')
        elif 'EE12' in variable:
            plt.ylabel(r'$\varepsilon_{xz} \left[-\right]$')
            plt.title(r'Strain distribution $\varepsilon_{xz}$ along radial section at $\psi=' + str(psi[j]) + '^{\circ}$')
        plt.legend(pis, labels)
        plt.grid(True)
        plt.savefig(join(pdffolder,prefix + '_AllRadialSections-' + variable + '_PSI' + str(psi[j]) + '.pdf'), bbox_inches='tight')
        plt.close()

def plotStressesAtInterfaceOverSims(wd,outdir,prefix,lines,surf):
    masterS11 = 1
    masterS12 = 2
    masterS13 = 3
    masterS12fric = 4
    masterS11pis = []
    masterS12pis = []
    masterS13pis = []
    masterS12fricpis = []
    labels = []
    for i,line in enumerate(lines[1:]):
        words = line.split(',')
        project = words[0]
        # define input file name
        inpname = project + '.inp'
        inpfullpath = join(wd,project,'abqinp',inpname)
        # define csv output folder
        csvfolder = join(wd,project,'csv')
        # define dat output folder
        datfolder = join(wd,project,'dat')
        # define latex output folder
        latexfolder = join(outdir,prefix,'latex')
        # define pdf output folder
        pdffolder = join(outdir,prefix,'pdf')
        with open(inpfullpath,'r') as inp:
            values = inp.readlines()
        theta = 0
        stresses = []
        for value in values:
            if 'Crack Angular Aperture' in value:
                theta = float(value.replace('\n','').replace('--','').replace('**','').replace('deg','').split(':')[-1])
        with open(join(csvfolder,'stressesOn' + surf + '.csv'),'r') as csv:
            values = csv.readlines()
        for value in values[2:]:
            stresses.append([float(value.split(',')[5]),float(value.split(',')[7]),float(value.split(',')[8]),float(value.split(',')[9]),float(value.split(',')[10])])
        stresses = np.array(stresses)
        stresses = stresses[stresses[:,0].argsort()]
        stresses[:,1] = -stresses[:,1]
        plt.figure(masterS11)
        pi, = plt.plot(stresses[:,0],stresses[:,1],color=(1,0,float(i)/len(lines[1:])),linestyle='-',linewidth=1.)
        masterS11pis.append(pi)
        plt.figure(masterS12)
        pi, = plt.plot(stresses[:,0],stresses[:,2],color=(1,0,float(i)/len(lines[1:])),linestyle='-',linewidth=1.)
        masterS12pis.append(pi)
        plt.figure(masterS13)
        pi, = plt.plot(stresses[:,0],stresses[:,3],color=(1,0,float(i)/len(lines[1:])),linestyle='-',linewidth=1.)
        masterS13pis.append(pi)
        plt.figure(masterS12fric)
        pi, = plt.plot(stresses[:,0],stresses[:,4],color=(1,0,float(i)/len(lines[1:])),linestyle='-',linewidth=1.)
        masterS12fricpis.append(pi)
        labels.append(r'$\theta \left[^{\circ}\right]=' + str(np.around(theta,decimals=0)) +'$')
    plt.figure(masterS11)
    plt.legend(masterS11pis, labels)
    plt.xlabel(r'$\psi \left[^{\circ}\right]$')
    plt.ylabel(r'$\sigma_{nn}\left[MPa\right]$')
    plt.title('Stress distribution $\sigma_{nn} $ on ' + surf + ' surface')
    plt.grid(True)
    plt.savefig(join(pdffolder,prefix + '_AllNormalStressOn' + surf + '.pdf'), bbox_inches='tight')
    plt.close()
    plt.figure(masterS12)
    plt.legend(masterS12pis, labels)
    plt.xlabel(r'$\psi \left[^{\circ}\right]$')
    plt.ylabel(r'$\tau_{n\psi}\left[MPa\right]$')
    plt.title(r'Stress distribution $\tau_{n\psi} $ on ' + surf + ' surface')
    plt.grid(True)
    plt.savefig(join(pdffolder,prefix + '_AllInPlaneShearOn' + surf + '.pdf'), bbox_inches='tight')
    plt.close()
    plt.figure(masterS13)
    plt.legend(masterS13pis, labels)
    plt.xlabel(r'$\psi \left[^{\circ}\right]$')
    plt.ylabel(r'$\tau_{ny}\left[MPa\right]$')
    plt.title(r'Stress distribution $\tau_{ny} $ on ' + surf + ' surface')
    plt.grid(True)
    plt.savefig(join(pdffolder,prefix + '_AllOutOfPlaneShearOn' + surf + '.pdf'), bbox_inches='tight')
    plt.close()
    plt.figure(masterS12fric)
    plt.legend(masterS12fricpis, labels)
    plt.xlabel(r'$\psi \left[^{\circ}\right]$')
    plt.ylabel(r'$\tau_{n\psi}^{fric}\left[MPa\right]$')
    plt.title(r'Stress distribution $\tau_{n\psi}^{fric} $ on ' + surf + ' surface')
    plt.grid(True)
    plt.savefig(join(pdffolder,prefix + '_AllFricShearOn' + surf + '.pdf'), bbox_inches='tight')
    plt.close()

def plotDispsAtInterfaceOverSims(wd,outdir,prefix,lines,surf):
    E11 = 1
    E12 = 2
    E11pis = []
    E12pis = []
    labels = []
    for i,line in enumerate(lines[1:]):
        words = line.split(',')
        project = words[0]
        # define input file name
        inpname = project + '.inp'
        inpfullpath = join(wd,project,'abqinp',inpname)
        # define csv output folder
        csvfolder = join(wd,project,'csv')
        # define dat output folder
        datfolder = join(wd,project,'dat')
        # define latex output folder
        latexfolder = join(outdir,prefix,'latex')
        # define pdf output folder
        pdffolder = join(outdir,prefix,'pdf')
        with open(inpfullpath,'r') as inp:
            values = inp.readlines()
        theta = 0
        disps = []
        for value in values:
            if 'Crack Angular Aperture' in value:
                theta = float(value.replace('\n','').replace('--','').replace('**','').replace('deg','').split(':')[-1])
        with open(join(csvfolder,'displacementsOn' + surf + '.csv'),'r') as csv:
            values = csv.readlines()
        for value in values[2:]:
            disps.append([float(value.split(',')[5]),float(value.split(',')[6]),float(value.split(',')[7])])
        disps = np.array(disps)
        disps = disps[disps[:,0].argsort()]
        plt.figure(E11)
        pi, = plt.plot(disps[:,0],disps[:,1],color=(1,0,float(i)/len(lines[1:])),linestyle='-',linewidth=1.)
        E11pis.append(pi)
        plt.figure(E12)
        pi, = plt.plot(disps[:,0],disps[:,2],color=(1,0,float(i)/len(lines[1:])),linestyle='-',linewidth=1.)
        E12pis.append(pi)
        labels.append(r'$\theta \left[^{\circ}\right]=' + str(np.around(theta,decimals=0)) +'$')
    plt.figure(E11)
    plt.legend(E11pis, labels)
    plt.xlabel(r'$\psi \left[^{\circ}\right]$')
    plt.ylabel(r'$\delta u_{nn}\left[\mu m\right]$')
    plt.title('Displacement $\delta u_{nn} $ on ' + surf + ' surface')
    plt.grid(True)
    plt.savefig(join(pdffolder,prefix + '_AllNormalDispsOn' + surf + '.pdf'), bbox_inches='tight')
    plt.close()
    plt.figure(E12)
    plt.legend(E12pis, labels)
    plt.xlabel(r'$\psi \left[^{\circ}\right]$')
    plt.ylabel(r'$\delta u_{n\psi}\left[\mu m\right]$')
    plt.title('Displacement $\delta u_{n\psi} $ on ' + surf + ' surface')
    plt.grid(True)
    plt.savefig(join(pdffolder,prefix + '_AllTangentialDispsOn' + surf + '.pdf'), bbox_inches='tight')
    plt.close()
    
def plotCircumSectionsOverSims(wd,outdir,prefix,lines,sourceprefix,variable):
    varpis = []
    varlabels = []
    for i,line in enumerate(lines[1:]):
        words = line.split(',')
        project = words[0]
        # define input file name
        inpname = project + '.inp'
        inpfullpath = join(wd,project,'abqinp',inpname)
        # define csv output folder
        csvfolder = join(wd,project,'csv')
        # define dat output folder
        datfolder = join(wd,project,'dat')
        # define latex output folder
        latexfolder = join(outdir,prefix,'latex')
        # define pdf output folder
        pdffolder = join(outdir,prefix,'pdf')
        with open(inpfullpath,'r') as inp:
            values = inp.readlines()
        theta = 0
        for value in values:
            if 'Crack Angular Aperture' in value:
                theta = float(value.replace('\n','').replace('--','').replace('**','').replace('deg','').split(':')[-1])
        psi = []
        var = []
        with open(join(csvfolder,sourceprefix + '.csv'),'r') as csv:
            values = csv.readlines()
        for value in values[1:]:
            if float(value.split(',')[1]) not in psi:
                psi.append(float(value.split(',')[1]))
            datafile = join(datfolder,value.split(',')[5].replace(' ','').replace('\n',''))
            with open(datafile,'r') as dat:
                sectionValues = dat.readlines()
            xy = []
            for sectionValue in sectionValues:
                if len(sectionValue.replace('\n','').replace(' ',''))>0 and 'X' not in sectionValue:
                    parts = sectionValue.replace('\n','').split(' ')
                    temp = []
                    for part in parts:
                        if part!='':
                            temp.append(float(part))
                    xy.append(temp)
            xy = np.array(xy)
            xy = xy[xy[:,0].argsort()]
            if variable in str(value.split(',')[0]):
                var.append(xy)
            xy =[]
        temppis = []
        templabels = []
        for j,V in enumerate(var):
            plt.figure(j+1)
            pi, = plt.plot(V[:,0],V[:,1],color=(1,0,float(i)/len(lines[1:])),linestyle='-',linewidth=1.)
            temppis.append(pi)
            templabels.append(r'$\theta \left[^{\circ}\right]=' + str(np.around(theta,decimals=0)) +'\mu m$')
        varpis.append(temppis)
        varlabels.append(templabels)
    for j,V in enumerate(var):
        plt.figure(j+1)
        pis = []
        labels = []
        for k in range(0,len(varpis)):
            pis.append(varpis[k][j])
            labels.append(varlabels[k][j])
        plt.xlabel(r'$\psi \left[^{\circ}\right]$')
        if 'S11' in variable:
            plt.ylabel(r'$\sigma_{xx} \left[MPa\right]$')
            plt.title(r'Stress distribution $\sigma_{xx}$ along circumferential section at $r=' + str(psi[j]) + '^{\circ}$')
        elif 'S22' in variable:
            plt.ylabel(r'$\sigma_{zz} \left[MPa\right]$')
            plt.title(r'Stress distribution $\sigma_{zz}$ along circumferential section at $r=' + str(psi[j]) + '^{\circ}$')
        elif 'S12' in variable:
            plt.ylabel(r'$\sigma_{xz} \left[MPa\right]$')
            plt.title(r'Stress distribution $\sigma_{xz}$ along circumferential section at $r=' + str(psi[j]) + '^{\circ}$')
        elif 'EE11' in variable:
            plt.ylabel(r'$\varepsilon_{xx} \left[-\right]$')
            plt.title(r'Strain distribution $\varepsilon_{xx}$ along circumferential section at $r=' + str(psi[j]) + '^{\circ}$')
        elif 'EE22' in variable:
            plt.ylabel(r'$\varepsilon_{zz} \left[-\right]$')
            plt.title(r'Strain distribution $\varepsilon_{zz}$ along circumferential section at $r=' + str(psi[j]) + '^{\circ}$')
        elif 'EE12' in variable:
            plt.ylabel(r'$\varepsilon_{xz} \left[-\right]$')
            plt.title(r'Strain distribution $\varepsilon_{xz}$ along circumferential section at $r=' + str(psi[j]) + '^{\circ}$')
        plt.legend(pis, labels)
        plt.grid(True)
        plt.savefig(join(pdffolder,prefix + '_AllCircumSections-' + variable + '_R' + str(psi[j]) + '.pdf'), bbox_inches='tight')
        plt.close()

def plotSurfaceVarsOverSims(wd,statusfile,outdir,prefix):
    if not exists(join(outdir,prefix)):
        makedirs(join(outdir,prefix))
    if not exists(join(outdir,prefix,'latex')):
        makedirs(join(outdir,prefix,'latex'))
    if not exists(join(outdir,prefix,'pdf')):
        makedirs(join(outdir,prefix,'pdf'))
    # read status file
    with open(join(wd,statusfile),'r') as sta:
        stalines = sta.readlines()
    #===========================================================================
    #                            Radial sections
    #===========================================================================
    # plot S11
    plotRadialSectionsOverSims(wd,outdir,prefix,stalines,'radialpaths','S11')
    # plot S22 
    plotRadialSectionsOverSims(wd,outdir,prefix,stalines,'radialpaths','S22')
    # plot S12 
    plotRadialSectionsOverSims(wd,outdir,prefix,stalines,'radialpaths','S12')
    # plot EE11
    plotRadialSectionsOverSims(wd,outdir,prefix,stalines,'radialpaths','EE11')
    # plot EE22
    plotRadialSectionsOverSims(wd,outdir,prefix,stalines,'radialpaths','EE22')
    # plot EE12
    plotRadialSectionsOverSims(wd,outdir,prefix,stalines,'radialpaths','EE12')
    #===========================================================================
    #                       Circumferential sections
    #===========================================================================
    # plot S11
    plotCircumSectionsOverSims(wd,outdir,prefix,stalines,'circumpaths','S11')
    # plot S22
    plotCircumSectionsOverSims(wd,outdir,prefix,stalines,'circumpaths','S22')
    # plot S12
    plotCircumSectionsOverSims(wd,outdir,prefix,stalines,'circumpaths','S12')
    # plot EE11
    plotCircumSectionsOverSims(wd,outdir,prefix,stalines,'circumpaths','EE11')
    # plot EE22
    plotCircumSectionsOverSims(wd,outdir,prefix,stalines,'circumpaths','EE22')
    # plot EE12
    plotCircumSectionsOverSims(wd,outdir,prefix,stalines,'circumpaths','EE12')
    #===========================================================================
    #                       Stresses on Master
    #===========================================================================
    plotStressesAtInterfaceOverSims(wd,outdir,prefix,stalines,'Master')
    #===========================================================================
    #                       Stresses on Slave
    #===========================================================================
    plotStressesAtInterfaceOverSims(wd,outdir,prefix,stalines,'Slave')
    #===========================================================================
    #                     Displacements on Slave
    #===========================================================================
    plotDispsAtInterfaceOverSims(wd,outdir,prefix,stalines,'Slave')
    
    

def main(argv):

    wd = 'D:/01_Luca/07_Data/03_FEM'
    matdatafolder = 'D:/OneDrive/01_Luca/07_DocMASE/07_Data/02_Material-Properties'
    
    statusfile = '2017-03-01_AbaqusParametricRun_2017-03-03_12-56-32.sta'
    
    outdir = 'D:/OneDrive/01_Luca/07_DocMASE/07_Data/03_FEM'
    prefix = '2017-03-03_AbqRunSummary'
    
    refdatadir = 'D:/OneDrive/01_Luca/07_DocMASE/07_Data/01_References/Verification-Data'
    refdatafile = 'BEM-data'
    
    plotSurfaceVarsOverSims(wd,statusfile,outdir,prefix)
    
            

if __name__ == "__main__":
    main(sys.argv[1:])