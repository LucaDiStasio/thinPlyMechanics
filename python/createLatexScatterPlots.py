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
import sys
import subprocess
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

def createLatexFile(folder,filename,documentclass,options=''):
    if not exists(folder):
        makedirs(folder)
    with open(join(folder,filename + '.tex'),'w') as tex:
        if options!='':
            tex.write('\\documentclass[' + options + ']{' + documentclass + '}\n')
        else:
            tex.write('\\documentclass{' + documentclass + '}\n')
        tex.write('\n')
        
def writeLatexPackages(folder,filename,packages,options):
    with open(join(folder,filename + '.tex'),'a') as tex:
        tex.write('%----------------------------------------------------------------------------------------------%\n')
        tex.write('%                                 Packages and basic declarations\n')
        tex.write('%----------------------------------------------------------------------------------------------%\n')
        tex.write('\n')
        for i,package in enumerate(packages):
            if options[i]!='':
                tex.write('\\usepackage[' + options[i] + ']{' + package + '}\n')
            else:
                tex.write('\\usepackage{' + package + '}\n')
        tex.write('\n')

def writeLatexDocumentStarts(folder,filename):
    with open(join(folder,filename + '.tex'),'a') as tex:
        tex.write('\n')
        tex.write('%----------------------------------------------------------------------------------------------%\n')
        tex.write('%----------------------------------------------------------------------------------------------%\n')
        tex.write('%                                            DOCUMENT STARTS\n')
        tex.write('%----------------------------------------------------------------------------------------------%\n')
        tex.write('%----------------------------------------------------------------------------------------------%\n')
        tex.write('\n')
        tex.write('\\begin{document}\n')
        tex.write('\n')


def writeLatexDocumentEnds(folder,filename):
    with open(join(folder,filename + '.tex'),'a') as tex:
        tex.write('\n')
        tex.write('\\end{document}\n')
        tex.write('\n')
        tex.write('%----------------------------------------------------------------------------------------------%\n')
        tex.write('%----------------------------------------------------------------------------------------------%\n')
        tex.write('%                                            DOCUMENT ENDS\n')
        tex.write('%----------------------------------------------------------------------------------------------%\n')
        tex.write('%----------------------------------------------------------------------------------------------%\n')
        tex.write('\n')

def writeLatexTikzPicStarts(folder,filename,options=''):
    with open(join(folder,filename + '.tex'),'a') as tex:
        tex.write('\n')
        tex.write('%Tikz picture starts%\n')
        tex.write('\n')
        if options!='':
            tex.write('\\begin{tikzpicture}[' + options + ']\n')
        else:
            tex.write('\\begin{tikzpicture}\n')

def writeLatexTikzPicEnds(folder,filename):
    with open(join(folder,filename + '.tex'),'a') as tex:
        tex.write('\n')
        tex.write('\\end{tikzpicture}\n')
        tex.write('%Tikz picture ends%\n')
        tex.write('\n')

def writeLatexTikzAxisStarts(folder,filename,options):
    with open(join(folder,filename + '.tex'),'a') as tex:
        tex.write('\n')
        tex.write('%Tikz axis starts%\n')
        tex.write('\n')
        if options!='':
            tex.write('\\begin{axis}[' + options + ']\n')
        else:
            tex.write('\\begin{axis}\n')

def writeLatexTikzAxisEnds(folder,filename):
    with open(join(folder,filename + '.tex'),'a') as tex:
        tex.write('\n')
        tex.write('\\end{axis}\n')
        tex.write('%Tikz axis ends%\n')
        tex.write('\n')

def writeLatexAddPlotTable(folder,filename,data,options):
    with open(join(folder,filename + '.tex'),'a') as tex:
        tex.write('\n')
        tex.write('\\addplot')
        if options!='':
            tex.write('[' + options + ']\n')
        tex.write('table{\n')
        for element in data:
            tex.write(str(element[0]) + ' ' + str(element[1]) + '\n')
        tex.write('};\n')

def writeLatexSinglePlot(wdir,proj,folder,filename,data,axoptions,dataoptions):
    createLatexFile(folder,filename,'standalone')
    writeLatexPackages(folder,filename,['inputenc','pgfplots','tikz'],['utf8','',''])
    writeLatexDocumentStarts(folder,filename)
    writeLatexTikzPicStarts(folder,filename,'')
    writeLatexTikzAxisStarts(folder,filename,axoptions)
    writeLatexAddPlotTable(folder,filename,data,dataoptions)
    writeLatexTikzAxisEnds(folder,filename)
    writeLatexTikzPicEnds(folder,filename)
    writeLatexDocumentEnds(folder,filename)
    if not exists(join(wdir,proj,'pdf')):
        makedirs(join(wdir,proj,'pdf'))
    cmdfile = join(wdir,proj,'pdf','runlatex.cmd')
    with open(cmdfile,'w') as cmd:
        cmd.write('\n')
        cmd.write('CD ' + wdir + '\\' + proj + '\\pdf\n')
        cmd.write('\n')
        cmd.write('pdflatex ' + join(folder,filename + '.tex') + ' -job-name=' + filename + '\n')
    try:
        subprocess.call('cmd.exe /C ' + cmdfile)
    except Exception:
        sys.exc_clear()
    
def writeLatexMultiplePlots(wdir,proj,folder,filename,data,axoptions,dataoptions):
    createLatexFile(folder,filename,'standalone')
    writeLatexPackages(folder,filename,['inputenc','pgfplots','tikz'],['utf8','',''])
    writeLatexDocumentStarts(folder,filename)
    writeLatexTikzPicStarts(folder,filename,'')
    writeLatexTikzAxisStarts(folder,filename,axoptions)
    for k,datum in enumerate(data):
        writeLatexAddPlotTable(folder,filename,datum,dataoptions[k])
    writeLatexTikzAxisEnds(folder,filename)
    writeLatexTikzPicEnds(folder,filename)
    writeLatexDocumentEnds(folder,filename)
    if not exists(join(wdir,proj,'pdf')):
        makedirs(join(wdir,proj,'pdf'))
    cmdfile = join(wdir,proj,'pdf','runlatex.cmd')
    with open(cmdfile,'w') as cmd:
        cmd.write('\n')
        cmd.write('CD ' + wdir + '\\' + proj + '\\pdf\n')
        cmd.write('\n')
        cmd.write('pdflatex ' + join(folder,filename + '.tex') + ' -job-name=' + filename + '\n')
    try:
        subprocess.call('cmd.exe /C ' + cmdfile)
    except Exception:
        sys.exc_clear()

def main(argv):
    #statusfile = '2017-02-02_AbaqusParametricRun_2017-02-02_18-05-02'
    statusfile = '2017-03-01_AbaqusParametricRun_2017-03-03_12-56-32'
    
    wd = 'D:\\01_Luca\\07_Data\\03_FEM'
    
    statusfile += '.sta'
    
    print('===============================================================================================\n')
    print('===============================================================================================\n')
    print('\n')
    print('                                           LATEX GRAPHICS CREATION\n')
    print('\n')
    print('                                               SCATTER PLOTS\n')
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
    for i,line in enumerate(lines[1:]):
        words = line.split(',')
        project = words[0]
        print('Starting creation of Latex scatter plots on project ' + project + '\n')
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
        '''
        # define png output folder
        pngfolder = join(wd,project,'png')
        if not exists(pngfolder):
            makedirs(pngfolder)
        '''
        #===========================================================================
        #                            Radial sections
        #===========================================================================
        theta = []
        S11 = []
        S22 = []
        S12 = []
        E11 = []
        E22 = []
        E12 = []
        with open(join(csvfolder,'radialpaths' + '.csv'),'r') as csv:
            values = csv.readlines()
        for value in values[1:]:
            if float(value.split(',')[1]) not in theta:
                theta.append(float(value.split(',')[1]))
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
            if 'S11' in str(value.split(',')[0]):
                S11.append(xy)
            elif 'S22' in str(value.split(',')[0]):
                S22.append(xy)
            elif 'S12' in str(value.split(',')[0]):
                S12.append(xy)
            elif 'EE11' in str(value.split(',')[0]):
                E11.append(xy)
            elif 'EE22' in str(value.split(',')[0]):
                E22.append(xy)
            elif 'EE12' in str(value.split(',')[0]):
                E12.append(xy)
            xy =[]
        
        # plot S11 for all sections
        plt.figure(1)
        pis = []
        labels = []
        for j,S in enumerate(S11):
            pi, = plt.plot(S[:,0],S[:,1],color=(0,1,float(j)/len(S11)),linestyle='-',linewidth=1.)
            pis.append(pi)
            labels.append(r'$\psi \left[^{\circ}\right]=' + str(np.around(theta[j],decimals=2)) +'$')
        plt.xlabel(r'$\rho \left[\mu m\right]$')
        plt.ylabel(r'$\sigma_{xx}\left[MPa\right]$')
        plt.title('Stress distribution $\sigma_{xx} $ along radial sections')
        plt.legend(pis, labels)
        plt.grid(True)
        plt.savefig(join(pdffolder,'AllRadialSections-S11' + '.pdf'), bbox_inches='tight')
        plt.close()
        
        # plot S22 for all sections
        plt.figure(2)
        pis = []
        labels = []
        for j,S in enumerate(S22):
            pi, = plt.plot(S[:,0],S[:,1],color=(0,1,float(j)/len(S22)),linestyle='-',linewidth=1.)
            pis.append(pi)
            labels.append(r'$\psi \left[^{\circ}\right]=' + str(np.around(theta[j],decimals=2)) +'$')
        plt.xlabel(r'$\rho \left[\mu m\right]$')
        plt.ylabel(r'$\sigma_{zz}\left[MPa\right]$')
        plt.title('Stress distribution $\sigma_{zz} $ along radial sections')
        plt.legend(pis, labels)
        plt.grid(True)
        plt.savefig(join(pdffolder,'AllRadialSections-S22' + '.pdf'), bbox_inches='tight')
        plt.close()
        
        # plot S12 for all sections
        plt.figure(3)
        pis = []
        labels = []
        for j,S in enumerate(S12):
            pi, = plt.plot(S[:,0],S[:,1],color=(0,1,float(j)/len(S12)),linestyle='-',linewidth=1.)
            pis.append(pi)
            labels.append(r'$\psi \left[^{\circ}\right]=' + str(np.around(theta[j],decimals=2)) +'$')
        plt.xlabel(r'$\rho \left[\mu m\right]$')
        plt.ylabel(r'$\sigma_{xz}\left[MPa\right]$')
        plt.title('Stress distribution $\sigma_{xz} $ along radial sections')
        plt.legend(pis, labels)
        plt.grid(True)
        plt.savefig(join(pdffolder,'AllRadialSections-S12' + '.pdf'), bbox_inches='tight')
        plt.close()
        
        # plot E11 for all sections
        plt.figure(4)
        pis = []
        labels = []
        for j,E in enumerate(E11):
            pi, = plt.plot(E[:,0],E[:,1],color=(0,1,float(j)/len(E11)),linestyle='-',linewidth=1.)
            pis.append(pi)
            labels.append(r'$\psi \left[^{\circ}\right]=' + str(np.around(theta[j],decimals=2)) +'$')
        plt.xlabel(r'$\rho \left[\mu m\right]$')
        plt.ylabel(r'$\varepsilon_{xx}\left[\frac{\mu m}{\mu m}\right]$')
        plt.title('Strain distribution $\varepsilon_{xx} $ along radial sections')
        plt.legend(pis, labels)
        plt.grid(True)
        plt.savefig(join(pdffolder,'AllRadialSections-E11' + '.pdf'), bbox_inches='tight')
        plt.close()
        
        # plot E22 for all sections
        plt.figure(5)
        pis = []
        labels = []
        for j,E in enumerate(E22):
            pi, = plt.plot(E[:,0],E[:,1],color=(0,1,float(j)/len(E22)),linestyle='-',linewidth=1.)
            pis.append(pi)
            labels.append(r'$\psi \left[^{\circ}\right]=' + str(np.around(theta[j],decimals=2)) +'$')
        plt.xlabel(r'$\rho \left[\mu m\right]$')
        plt.ylabel(r'$\varepsilon_{zz}\left[\frac{\mu m}{\mu m}\right]$')
        plt.title('Strain distribution $\varepsilon_{zz} $ along radial sections')
        plt.legend(pis, labels)
        plt.grid(True)
        plt.savefig(join(pdffolder,'AllRadialSections-E22' + '.pdf'), bbox_inches='tight')
        plt.close()
        
        # plot E12 for all sections
        plt.figure(6)
        pis = []
        labels = []
        for j,E in enumerate(E12):
            pi, = plt.plot(E[:,0],E[:,1],color=(0,1,float(j)/len(E12)),linestyle='-',linewidth=1.)
            pis.append(pi)
            labels.append(r'$\psi \left[^{\circ}\right]=' + str(np.around(theta[j],decimals=2)) +'$')
        plt.xlabel(r'$\rho \left[\mu m\right]$')
        plt.ylabel(r'$\varepsilon_{xz}\left[\frac{\mu m}{\mu m}\right]$')
        plt.title('Strain distribution $\varepsilon_{xz} $ along radial sections')
        plt.legend(pis, labels)
        plt.grid(True)
        plt.savefig(join(pdffolder,'AllRadialSections-E12' + '.pdf'), bbox_inches='tight')
        plt.close()
        
        for j,S in enumerate(S11):
            xmin = np.amin(S[:,0])-np.abs(0.05*np.amin(S[:,0]))
            xmax = np.amax(S[:,0])+np.abs(0.05*np.amax(S[:,0]))
            ymin = np.amin(S[:,1])-np.abs(0.05*np.amin(S[:,1]))
            ymax = np.amax(S[:,1])+np.abs(0.05*np.amax(S[:,1]))  
            axisoptions = '\n ' \
                        'width=30cm,\n' \
                        'title={$\\sigma_{xx}$ along $\\psi=' + str(np.around(theta[j],decimals=2)) + '\\left[^{\\circ}\\right]$},\n' \
                        'xlabel={$r\\left[\\mu m\\right]$},ylabel={$\\sigma_{xx}\\left[MPa\\right]$},\n' \
                        'xmin=' + str(xmin) + ',\n' \
                        'xmax=' + str(xmax) + ',\n' \
                        'ymin=' + str(ymin) + ',\n' \
                        'ymax=' + str(ymax) + ',\n' \
                        'tick align=outside,\n' \
                        'tick label style={font=\\tiny},\n' \
                        'xmajorgrids,\n' \
                        'x grid style={lightgray!92.026143790849673!black},\n' \
                        'ymajorgrids,\n' \
                        'y grid style={lightgray!92.026143790849673!black},\n' \
                        'line width=0.35mm,\n'
            writeLatexSinglePlot(wd,project,latexfolder,'S11alongPSI' + str(np.around(theta[j],decimals=2)).replace('.','_'),S,axisoptions,'blue')
        
        for j,S in enumerate(S22):
            xmin = np.amin(S[:,0])-np.abs(0.05*np.amin(S[:,0]))
            xmax = np.amax(S[:,0])+np.abs(0.05*np.amax(S[:,0]))
            ymin = np.amin(S[:,1])-np.abs(0.05*np.amin(S[:,1]))
            ymax = np.amax(S[:,1])+np.abs(0.05*np.amax(S[:,1]))  
            axisoptions = '\n ' \
                        'width=30cm,\n' \
                        'title={$\\sigma_{zz}$ along $\\psi=' + str(np.around(theta[j],decimals=2)) + '\\left[^{\\circ}\\right]$},\n' \
                        'xlabel={$r\\left[\\mu m\\right]$},ylabel={$\\sigma_{zz}\\left[MPa\\right]$},\n' \
                        'xmin=' + str(xmin) + ',\n' \
                        'xmax=' + str(xmax) + ',\n' \
                        'ymin=' + str(ymin) + ',\n' \
                        'ymax=' + str(ymax) + ',\n' \
                        'tick align=outside,\n' \
                        'tick label style={font=\\tiny},\n' \
                        'xmajorgrids,\n' \
                        'x grid style={lightgray!92.026143790849673!black},\n' \
                        'ymajorgrids,\n' \
                        'y grid style={lightgray!92.026143790849673!black},\n' \
                        'line width=0.35mm,\n'
            writeLatexSinglePlot(wd,project,latexfolder,'S22alongPSI' + str(np.around(theta[j],decimals=2)).replace('.','_'),S,axisoptions,'blue')
        
        for j,S in enumerate(S12):
            xmin = np.amin(S[:,0])-np.abs(0.05*np.amin(S[:,0]))
            xmax = np.amax(S[:,0])+np.abs(0.05*np.amax(S[:,0]))
            ymin = np.amin(S[:,1])-np.abs(0.05*np.amin(S[:,1]))
            ymax = np.amax(S[:,1])+np.abs(0.05*np.amax(S[:,1]))  
            axisoptions = '\n ' \
                        'width=30cm,\n' \
                        'title={$\\sigma_{xz}$ along $\\psi=' + str(np.around(theta[j],decimals=2)) + '\\left[^{\\circ}\\right]$},\n' \
                        'xlabel={$r\\left[\\mu m\\right]$},ylabel={$\\sigma_{xz}\\left[MPa\\right]$},\n' \
                        'xmin=' + str(xmin) + ',\n' \
                        'xmax=' + str(xmax) + ',\n' \
                        'ymin=' + str(ymin) + ',\n' \
                        'ymax=' + str(ymax) + ',\n' \
                        'tick align=outside,\n' \
                        'tick label style={font=\\tiny},\n' \
                        'xmajorgrids,\n' \
                        'x grid style={lightgray!92.026143790849673!black},\n' \
                        'ymajorgrids,\n' \
                        'y grid style={lightgray!92.026143790849673!black},\n' \
                        'line width=0.35mm,\n'
            writeLatexSinglePlot(wd,project,latexfolder,'S12alongPSI' + str(np.around(theta[j],decimals=2)).replace('.','_'),S,axisoptions,'blue')
        
        for j,E in enumerate(E11):
            xmin = np.amin(E[:,0])-np.abs(0.05*np.amin(E[:,0]))
            xmax = np.amax(E[:,0])+np.abs(0.05*np.amax(E[:,0]))
            ymin = np.amin(E[:,1])-np.abs(0.05*np.amin(E[:,1]))
            ymax = np.amax(E[:,1])+np.abs(0.05*np.amax(E[:,1]))  
            axisoptions = '\n ' \
                        'width=30cm,\n' \
                        'title={$\\varepsilon_{xx}$ along $\\psi=' + str(np.around(theta[j],decimals=2)) + '\\left[^{\\circ}\\right]$},\n' \
                        'xlabel={$r\\left[\\mu m\\right]$},ylabel={$\\varepsilon_{xx}\\left[\\frac{\\mu m}{\\mu m}\\right]$},\n' \
                        'xmin=' + str(xmin) + ',\n' \
                        'xmax=' + str(xmax) + ',\n' \
                        'ymin=' + str(ymin) + ',\n' \
                        'ymax=' + str(ymax) + ',\n' \
                        'tick align=outside,\n' \
                        'tick label style={font=\\tiny},\n' \
                        'xmajorgrids,\n' \
                        'x grid style={lightgray!92.026143790849673!black},\n' \
                        'ymajorgrids,\n' \
                        'y grid style={lightgray!92.026143790849673!black},\n' \
                        'line width=0.35mm,\n'
            writeLatexSinglePlot(wd,project,latexfolder,'E11alongPSI' + str(np.around(theta[j],decimals=2)).replace('.','_'),E,axisoptions,'blue')
        
        for j,E in enumerate(E22):
            xmin = np.amin(E[:,0])-np.abs(0.05*np.amin(E[:,0]))
            xmax = np.amax(E[:,0])+np.abs(0.05*np.amax(E[:,0]))
            ymin = np.amin(E[:,1])-np.abs(0.05*np.amin(E[:,1]))
            ymax = np.amax(E[:,1])+np.abs(0.05*np.amax(E[:,1]))  
            axisoptions = '\n ' \
                        'width=30cm,\n' \
                        'title={$\\varepsilon_{zz}$ along $\\psi=' + str(np.around(theta[j],decimals=2)) + '\\left[^{\\circ}\\right]$},\n' \
                        'xlabel={$r\\left[\\mu m\\right]$},ylabel={$\\varepsilon_{zz}\\left[\\frac{\\mu m}{\\mu m}\\right]$},\n' \
                        'xmin=' + str(xmin) + ',\n' \
                        'xmax=' + str(xmax) + ',\n' \
                        'ymin=' + str(ymin) + ',\n' \
                        'ymax=' + str(ymax) + ',\n' \
                        'tick align=outside,\n' \
                        'tick label style={font=\\tiny},\n' \
                        'xmajorgrids,\n' \
                        'x grid style={lightgray!92.026143790849673!black},\n' \
                        'ymajorgrids,\n' \
                        'y grid style={lightgray!92.026143790849673!black},\n' \
                        'line width=0.35mm,\n'
            writeLatexSinglePlot(wd,project,latexfolder,'E22alongPSI' + str(np.around(theta[j],decimals=2)).replace('.','_'),E,axisoptions,'blue')
        
        for j,E in enumerate(E12):
            xmin = np.amin(E[:,0])-np.abs(0.05*np.amin(E[:,0]))
            xmax = np.amax(E[:,0])+np.abs(0.05*np.amax(E[:,0]))
            ymin = np.amin(E[:,1])-np.abs(0.05*np.amin(E[:,1]))
            ymax = np.amax(E[:,1])+np.abs(0.05*np.amax(E[:,1]))   
            axisoptions = '\n ' \
                        'width=30cm,\n' \
                        'title={$\\varepsilon_{xz}$ along $\\psi=' + str(np.around(theta[j],decimals=2)) + '\\left[^{\\circ}\\right]$},\n' \
                        'xlabel={$r\\left[\\mu m\\right]$},ylabel={$\\varepsilon_{xz}\\left[\\frac{\\mu m}{\\mu m}\\right]$},\n' \
                        'xmin=' + str(xmin) + ',\n' \
                        'xmax=' + str(xmax) + ',\n' \
                        'ymin=' + str(ymin) + ',\n' \
                        'ymax=' + str(ymax) + ',\n' \
                        'tick align=outside,\n' \
                        'tick label style={font=\\tiny},\n' \
                        'xmajorgrids,\n' \
                        'x grid style={lightgray!92.026143790849673!black},\n' \
                        'ymajorgrids,\n' \
                        'y grid style={lightgray!92.026143790849673!black},\n' \
                        'line width=0.35mm,\n'
            writeLatexSinglePlot(wd,project,latexfolder,'E12alongPSI' + str(np.around(theta[j],decimals=2)).replace('.','_'),E,axisoptions,'blue')
        
        #===========================================================================
        #                       Circumferential sections
        #===========================================================================
        R = []
        S11 = []
        S22 = []
        S12 = []
        E11 = []
        E22 = []
        E12 = []
        with open(join(csvfolder,'circumpaths' + '.csv'),'r') as csv:
            values = csv.readlines()
        for value in values[1:]:
            if float(value.split(',')[1]) not in R:
                R.append(float(value.split(',')[1]))
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
            xmin = np.amin(xy[:,0])
            xmax = np.amax(xy[:,0])
            dx = xmax - xmin
            dhx = dx/2
            xmid = xmin + dhx
            dxt = 180.
            xmint = -180.
            xmidt = 0.
            for j,x in enumerate(xy):
                if x[0]<xmid:
                    x[0] = xmidt + dxt*(x[0]-xmin)/dhx
                else:
                    x[0] = xmint + dxt*(x[0]-xmid)/dhx
            xy = xy[xy[:,0].argsort()]
            if 'S11' in str(value.split(',')[0]):
                S11.append(xy)
            elif 'S22' in str(value.split(',')[0]):
                S22.append(xy)
            elif 'S12' in str(value.split(',')[0]):
                S12.append(xy)
            elif 'EE11' in str(value.split(',')[0]):
                E11.append(xy)
            elif 'EE22' in str(value.split(',')[0]):
                E22.append(xy)
            elif 'EE12' in str(value.split(',')[0]):
                E12.append(xy)
            xy =[]
        
        xmin = -180.
        xmax = 180.
        xlabels = '{'
        for j,element in enumerate(np.linspace(xmin,xmax,37,endpoint=True)):
            if j>0:
                xlabels += ','
            xlabels += str(element)
        xlabels += '}'
        
        # plot S11 for all sections
        plt.figure(1)
        pis = []
        labels = []
        for j,S in enumerate(S11):
            pi, = plt.plot(S[:,0],S[:,1],color=(0,1,float(j)/len(S11)),linestyle='-',linewidth=1.)
            pis.append(pi)
            labels.append(r'$r \left[\mu m\right]=' + str(np.around(R[j],decimals=2)) +'$')
        plt.xlabel(r'$\psi \left[\mu m\right]$')
        plt.ylabel(r'$\sigma_{xx}\left[^{\circ}\right]$')
        plt.title('Stress distribution $\sigma_{xx} $ along circumferential sections')
        plt.legend(pis, labels)
        plt.grid(True)
        plt.savefig(join(pdffolder,'AllCircumferentialSections-S11' + '.pdf'), bbox_inches='tight')
        plt.close()
        
        # plot S22 for all sections
        plt.figure(2)
        pis = []
        labels = []
        for j,S in enumerate(S22):
            pi, = plt.plot(S[:,0],S[:,1],color=(0,1,float(j)/len(S22)),linestyle='-',linewidth=1.)
            pis.append(pi)
            labels.append(r'$r \left[\mu m\right]=' + str(np.around(R[j],decimals=2)) +'$')
        plt.xlabel(r'$\psi \left[^{\circ}\right]$')
        plt.ylabel(r'$\sigma_{zz}\left[MPa\right]$')
        plt.title('Stress distribution $\sigma_{zz} $ along circumferential sections')
        plt.legend(pis, labels)
        plt.grid(True)
        plt.savefig(join(pdffolder,'AllCircumferentialSections-S22' + '.pdf'), bbox_inches='tight')
        plt.close()
        
        # plot S12 for all sections
        plt.figure(3)
        pis = []
        labels = []
        for j,S in enumerate(S12):
            pi, = plt.plot(S[:,0],S[:,1],color=(0,1,float(j)/len(S12)),linestyle='-',linewidth=1.)
            pis.append(pi)
            labels.append(r'$r \left[\mu m\right]=' + str(np.around(R[j],decimals=2)) +'$')
        plt.xlabel(r'$\psi \left[^{\circ}\right]$')
        plt.ylabel(r'$\sigma_{xz}\left[MPa\right]$')
        plt.title('Stress distribution $\sigma_{xz} $ along circumferential sections')
        plt.legend(pis, labels)
        plt.grid(True)
        plt.savefig(join(pdffolder,'AllCircumferentialSections-S12' + '.pdf'), bbox_inches='tight')
        plt.close()
        
        # plot E11 for all sections
        plt.figure(4)
        pis = []
        labels = []
        for j,E in enumerate(E11):
            pi, = plt.plot(E[:,0],E[:,1],color=(0,1,float(j)/len(E11)),linestyle='-',linewidth=1.)
            pis.append(pi)
            labels.append(r'$r \left[\mu m\right]=' + str(np.around(R[j],decimals=2)) +'$')
        plt.xlabel(r'$\psi \left[^{\circ}\right]$')
        plt.ylabel(r'$\varepsilon_{xx}\left[\frac{\mu m}{\mu m}\right]$')
        plt.title('Strain distribution $\varepsilon_{xx} $ along circumferential sections')
        plt.legend(pis, labels)
        plt.grid(True)
        plt.savefig(join(pdffolder,'AllCircumferentialSections-E11' + '.pdf'), bbox_inches='tight')
        plt.close()
        
        # plot E22 for all sections
        plt.figure(5)
        pis = []
        labels = []
        for j,E in enumerate(E22):
            pi, = plt.plot(E[:,0],E[:,1],color=(0,1,float(j)/len(E22)),linestyle='-',linewidth=1.)
            pis.append(pi)
            labels.append(r'$r \left[\mu m\right]=' + str(np.around(R[j],decimals=2)) +'$')
        plt.xlabel(r'$\psi \left[^{\circ}\right]$')
        plt.ylabel(r'$\varepsilon_{zz}\left[\frac{\mu m}{\mu m}\right]$')
        plt.title('Strain distribution $\varepsilon_{zz} $ along circumferential sections')
        plt.legend(pis, labels)
        plt.grid(True)
        plt.savefig(join(pdffolder,'AllCircumferentialSections-E22' + '.pdf'), bbox_inches='tight')
        plt.close()
        
        # plot E12 for all sections
        plt.figure(6)
        pis = []
        labels = []
        for j,E in enumerate(E12):
            pi, = plt.plot(E[:,0],E[:,1],color=(0,1,float(j)/len(E12)),linestyle='-',linewidth=1.)
            pis.append(pi)
            labels.append(r'$r \left[\mu m\right]=' + str(np.around(R[j],decimals=2)) +'$')
        plt.xlabel(r'$\psi \left[^{\circ}\right]$')
        plt.ylabel(r'$\varepsilon_{xz}\left[\frac{\mu m}{\mu m}\right]$')
        plt.title('Strain distribution $\varepsilon_{xz} $ along circumferential sections')
        plt.legend(pis, labels)
        plt.grid(True)
        plt.savefig(join(pdffolder,'AllCircumferentialSections-E12' + '.pdf'), bbox_inches='tight')
        plt.close()
        
        for j,S in enumerate(S11):
            ymin = np.amin(S[:,1])-np.abs(0.1*np.amin(S[:,1]))
            ymax = np.amax(S[:,1])+np.abs(0.1*np.amax(S[:,1]))
            axisoptions = '\n ' \
                        'width=30cm,\n' \
                        'title={$\\sigma_{xx}$ along $R=' + str(np.around(R[j],decimals=2)) + '\\left[\\mu m\\right]$},\n' \
                        'xlabel={$\\psi\\left[^{\\circ}\\right]$},ylabel={$\\sigma_{xx}\\left[MPa\\right]$},\n' \
                        'xmin=' + str(xmin) + ',\n' \
                        'xmax=' + str(xmax) + ',\n' \
                        'ymin=' + str(ymin) + ',\n' \
                        'ymax=' + str(ymax) + ',\n' \
                        'tick align=outside,\n' \
                        'tick label style={font=\\tiny},\n' \
                        'xtick=' + xlabels + ',\n' \
                        'xmajorgrids,\n' \
                        'x grid style={lightgray!92.026143790849673!black},\n' \
                        'ymajorgrids,\n' \
                        'y grid style={lightgray!92.026143790849673!black},\n' \
                        'line width=0.35mm,\n'
            writeLatexSinglePlot(wd,project,latexfolder,'S11alongR' + str(np.around(R[j],decimals=2)).replace('.','_'),S,axisoptions,'blue')
        
        for j,S in enumerate(S22):
            ymin = np.amin(S[:,1])-np.abs(0.1*np.amin(S[:,1]))
            ymax = np.amax(S[:,1])+np.abs(0.1*np.amax(S[:,1]))      
            axisoptions = '\n ' \
                        'width=30cm,\n' \
                        'title={$\\sigma_{zz}$ along $R=' + str(np.around(R[j],decimals=2)) + '\\left[\\mu m\\right]$},\n' \
                        'xlabel={$\\psi\\left[^{\\circ}\\right]$},ylabel={$\\sigma_{zz}\\left[MPa\\right]$},\n' \
                        'xmin=' + str(xmin) + ',\n' \
                        'xmax=' + str(xmax) + ',\n' \
                        'ymin=' + str(ymin) + ',\n' \
                        'ymax=' + str(ymax) + ',\n' \
                        'tick align=outside,\n' \
                        'tick label style={font=\\tiny},\n' \
                        'xtick=' + xlabels + ',\n' \
                        'xmajorgrids,\n' \
                        'x grid style={lightgray!92.026143790849673!black},\n' \
                        'ymajorgrids,\n' \
                        'y grid style={lightgray!92.026143790849673!black},\n' \
                        'line width=0.35mm,\n'
            writeLatexSinglePlot(wd,project,latexfolder,'S22alongR' + str(np.around(R[j],decimals=2)).replace('.','_'),S,axisoptions,'blue')
        
        for j,S in enumerate(S12):
            ymin = np.amin(S[:,1])-np.abs(0.1*np.amin(S[:,1]))
            ymax = np.amax(S[:,1])+np.abs(0.1*np.amax(S[:,1]))     
            axisoptions = '\n ' \
                        'width=30cm,\n' \
                        'title={$\\sigma_{xz}$ along $R=' + str(np.around(R[j],decimals=2)) + '\\left[\\mu m\\right]$},\n' \
                        'xlabel={$\\psi\\left[^{\\circ}\\right]$},ylabel={$\\sigma_{xz}\\left[MPa\\right]$},\n' \
                        'xmin=' + str(xmin) + ',\n' \
                        'xmax=' + str(xmax) + ',\n' \
                        'ymin=' + str(ymin) + ',\n' \
                        'ymax=' + str(ymax) + ',\n' \
                        'tick align=outside,\n' \
                        'tick label style={font=\\tiny},\n' \
                        'xtick=' + xlabels + ',\n' \
                        'xmajorgrids,\n' \
                        'x grid style={lightgray!92.026143790849673!black},\n' \
                        'ymajorgrids,\n' \
                        'y grid style={lightgray!92.026143790849673!black},\n' \
                        'line width=0.35mm,\n'
            writeLatexSinglePlot(wd,project,latexfolder,'S12alongR' + str(np.around(R[j],decimals=2)).replace('.','_'),S,axisoptions,'blue')
        
        for j,E in enumerate(E11):
            ymin = np.amin(S[:,1])-np.abs(0.1*np.amin(S[:,1]))
            ymax = np.amax(S[:,1])+np.abs(0.1*np.amax(S[:,1]))     
            axisoptions = '\n ' \
                        'width=30cm,\n' \
                        'title={$\\varepsilon_{xx}$ along $R=' + str(np.around(R[j],decimals=2)) + '\\left[\\mu m\\right]$},\n' \
                        'xlabel={$\\psi\\left[^{\\circ}\\right]$},ylabel={$\\varepsilon_{xx}\\left[\\frac{\\mu m}{\\mu m}\\right]$},\n' \
                        'xmin=' + str(xmin) + ',\n' \
                        'xmax=' + str(xmax) + ',\n' \
                        'ymin=' + str(ymin) + ',\n' \
                        'ymax=' + str(ymax) + ',\n' \
                        'tick align=outside,\n' \
                        'tick label style={font=\\tiny},\n' \
                        'xtick=' + xlabels + ',\n' \
                        'xmajorgrids,\n' \
                        'x grid style={lightgray!92.026143790849673!black},\n' \
                        'ymajorgrids,\n' \
                        'y grid style={lightgray!92.026143790849673!black},\n' \
                        'line width=0.35mm,\n'
            writeLatexSinglePlot(wd,project,latexfolder,'E11alongR' + str(np.around(R[j],decimals=2)).replace('.','_'),E,axisoptions,'blue')
        
        for j,E in enumerate(E22):
            ymin = np.amin(S[:,1])-np.abs(0.1*np.amin(S[:,1]))
            ymax = np.amax(S[:,1])+np.abs(0.1*np.amax(S[:,1]))     
            axisoptions = '\n ' \
                        'width=30cm,\n' \
                        'title={$\\varepsilon_{zz}$ along $R=' + str(np.around(R[j],decimals=2)) + '\\left[\\mu m\\right]$},\n' \
                        'xlabel={$\\psi\\left[^{\\circ}\\right]$},ylabel={$\\varepsilon_{zz}\\left[\\frac{\\mu m}{\\mu m}\\right]$},\n' \
                        'xmin=' + str(xmin) + ',\n' \
                        'xmax=' + str(xmax) + ',\n' \
                        'ymin=' + str(ymin) + ',\n' \
                        'ymax=' + str(ymax) + ',\n' \
                        'tick align=outside,\n' \
                        'tick label style={font=\\tiny},\n' \
                        'xtick=' + xlabels + ',\n' \
                        'xmajorgrids,\n' \
                        'x grid style={lightgray!92.026143790849673!black},\n' \
                        'ymajorgrids,\n' \
                        'y grid style={lightgray!92.026143790849673!black},\n' \
                        'line width=0.35mm,\n'
            writeLatexSinglePlot(wd,project,latexfolder,'E22alongR' + str(np.around(R[j],decimals=2)).replace('.','_'),E,axisoptions,'blue')
        
        for j,E in enumerate(E12):
            ymin = np.amin(S[:,1])-np.abs(0.1*np.amin(S[:,1]))
            ymax = np.amax(S[:,1])+np.abs(0.1*np.amax(S[:,1]))     
            axisoptions = '\n ' \
                        'width=30cm,\n' \
                        'title={$\\varepsilon_{xz}$ along $R=' + str(np.around(R[j],decimals=2)) + '\\left[\\mu m\\right]$},\n' \
                        'xlabel={$\\psi\\left[^{\\circ}\\right]$},ylabel={$\\varepsilon_{xz}\\left[\\frac{\\mu m}{\\mu m}\\right]$},\n' \
                        'xmin=' + str(xmin) + ',\n' \
                        'xmax=' + str(xmax) + ',\n' \
                        'ymin=' + str(ymin) + ',\n' \
                        'ymax=' + str(ymax) + ',\n' \
                        'tick align=outside,\n' \
                        'tick label style={font=\\tiny},\n' \
                        'xtick=' + xlabels + ',\n' \
                        'xmajorgrids,\n' \
                        'x grid style={lightgray!92.026143790849673!black},\n' \
                        'ymajorgrids,\n' \
                        'y grid style={lightgray!92.026143790849673!black},\n' \
                        'line width=0.35mm,\n'
            writeLatexSinglePlot(wd,project,latexfolder,'E12alongR' + str(np.around(R[j],decimals=2)).replace('.','_'),E,axisoptions,'blue')
            
        '''
        ymin = np.floor(np.amin(S11[0][:,1])-np.abs(0.1*np.amin(S11[0][:,1])))
        ymax = np.ceil(np.amax(S11[0][:,1])+np.abs(0.1*np.amax(S11[0][:,1])))
        for j,y in enumerate(S11):
            if np.floor(np.amin(y[:,1])-np.abs(0.1*np.amin(y[:,1])))<ymin:
                ymin = np.floor(np.amin(y[:,1])-np.abs(0.1*np.amin(y[:,1])))
            if np.ceil(np.amax(y[:,1])+np.abs(0.1*np.amax(y[:,1])))>ymax:
                ymin = np.ceil(np.amax(y[:,1])+np.abs(0.1*np.amax(y[:,1])))
        dataoptions = []
        for j,r in enumerate(R):
            dataoptions.append('green!' + str(gradations[j]) + '!black')   
        axisoptions = '\n ' \
                    'width=30cm,\n' \
                    'title={$\\sigma_{\\left(xx\\right)}$ along circumferential sections},\n' \
                    'xlabel={$\\psi\\left[^{\\circ}\\right]$},ylabel={$\\sigma_{\\left(xx\\right)}\\left[MPa\\right]$},\n' \
                    'xmin=' + str(xmin) + ',\n' \
                    'xmax=' + str(xmax) + ',\n' \
                    'ymin=' + str(ymin) + ',\n' \
                    'ymax=' + str(ymax) + ',\n' \
                    'tick align=outside,\n' \
                    'tick label style={font=\\tiny},\n' \
                    'xtick=' + xlabels + ',\n' \
                    'xmajorgrids,\n' \
                    'x grid style={lightgray!92.026143790849673!black},\n' \
                    'ymajorgrids,\n' \
                    'y grid style={lightgray!92.026143790849673!black},\n' \
                    'line width=0.35mm,\n' \
                    'legend style={draw=white!80.0!black,font=\\fontsize{12}{6}\\selectfont},\n' \
                    'legend entries=' + legendEntries + ',\n' \
                    'legend cell align={left}\n'
        writeLatexMultiplePlots(wd,project,latexfolder,'allS11OnCircumferentialPaths',S11,axisoptions,dataoptions)
        
        ymin = np.floor(np.amin(S22[0][:,1])-np.abs(0.1*np.amin(S22[0][:,1])))
        ymax = np.ceil(np.amax(S22[0][:,1])+np.abs(0.1*np.amax(S22[0][:,1])))
        for j,y in enumerate(S22):
            if np.floor(np.amin(y[:,1])-np.abs(0.1*np.amin(y[:,1])))<ymin:
                ymin = np.floor(np.amin(y[:,1])-np.abs(0.1*np.amin(y[:,1])))
            if np.ceil(np.amax(y[:,1])+np.abs(0.1*np.amax(y[:,1])))>ymax:
                ymin = np.ceil(np.amax(y[:,1])+np.abs(0.1*np.amax(y[:,1])))
        dataoptions = []
        for j,r in enumerate(R):
            dataoptions.append('red!' + str(gradations[j]) + '!black')  
        axisoptions = '\n ' \
                    'width=30cm,\n' \
                    'title={$\\sigma_{\\left(zz\\right)}$ along circumferential sections},\n' \
                    'xlabel={$\\psi\\left[^{\\circ}\\right]$},ylabel={$\\sigma_{\\left(zz\\right)}\\left[MPa\\right]$},\n' \
                    'xmin=' + str(xmin) + ',\n' \
                    'xmax=' + str(xmax) + ',\n' \
                    'ymin=' + str(ymin) + ',\n' \
                    'ymax=' + str(ymax) + ',\n' \
                    'tick align=outside,\n' \
                    'tick label style={font=\\tiny},\n' \
                    'xtick=' + xlabels + ',\n' \
                    'xmajorgrids,\n' \
                    'x grid style={lightgray!92.026143790849673!black},\n' \
                    'ymajorgrids,\n' \
                    'y grid style={lightgray!92.026143790849673!black},\n' \
                    'line width=0.35mm,\n' \
                    'legend style={draw=white!80.0!black,font=\\fontsize{12}{6}\\selectfont},\n' \
                    'legend entries=' + legendEntries + ',\n' \
                    'legend cell align={left}\n'
        writeLatexMultiplePlots(wd,project,latexfolder,'allS22OnCircumferentialPaths',S22,axisoptions,dataoptions)
        
        ymin = np.floor(np.amin(S12[0][:,1])-np.abs(0.1*np.amin(S12[0][:,1])))
        ymax = np.ceil(np.amax(S12[0][:,1])+np.abs(0.1*np.amax(S12[0][:,1])))
        for j,y in enumerate(S12):
            if np.floor(np.amin(y[:,1])-np.abs(0.1*np.amin(y[:,1])))<ymin:
                ymin = np.floor(np.amin(y[:,1])-np.abs(0.1*np.amin(y[:,1])))
            if np.ceil(np.amax(y[:,1])+np.abs(0.1*np.amax(y[:,1])))>ymax:
                ymin = np.ceil(np.amax(y[:,1])+np.abs(0.1*np.amax(y[:,1])))
        dataoptions = []
        for j,r in enumerate(R):
            dataoptions.append('blue!' + str(gradations[j]) + '!black')  
        axisoptions = '\n ' \
                    'width=30cm,\n' \
                    'title={$\\sigma_{\\left(xz\\right)}$ along circumferential sections},\n' \
                    'xlabel={$\\psi\\left[^{\\circ}\\right]$},ylabel={$\\sigma_{\\left(xz\\right)}\\left[MPa\\right]$},\n' \
                    'xmin=' + str(xmin) + ',\n' \
                    'xmax=' + str(xmax) + ',\n' \
                    'ymin=' + str(ymin) + ',\n' \
                    'ymax=' + str(ymax) + ',\n' \
                    'tick align=outside,\n' \
                    'tick label style={font=\\tiny},\n' \
                    'xtick=' + xlabels + ',\n' \
                    'xmajorgrids,\n' \
                    'x grid style={lightgray!92.026143790849673!black},\n' \
                    'ymajorgrids,\n' \
                    'y grid style={lightgray!92.026143790849673!black},\n' \
                    'line width=0.35mm,\n' \
                    'legend style={draw=white!80.0!black,font=\\fontsize{12}{6}\\selectfont},\n' \
                    'legend entries=' + legendEntries + ',\n' \
                    'legend cell align={left}\n'
        writeLatexMultiplePlots(wd,project,latexfolder,'allS12OnCircumferentialPaths',S12,axisoptions,dataoptions)
        
        ymin = np.floor(np.amin(E11[0][:,1])-np.abs(0.1*np.amin(E11[0][:,1])))
        ymax = np.ceil(np.amax(E11[0][:,1])+np.abs(0.1*np.amax(E11[0][:,1])))
        for j,y in enumerate(E11):
            if np.floor(np.amin(y[:,1])-np.abs(0.1*np.amin(y[:,1])))<ymin:
                ymin = np.floor(np.amin(y[:,1])-np.abs(0.1*np.amin(y[:,1])))
            if np.ceil(np.amax(y[:,1])+np.abs(0.1*np.amax(y[:,1])))>ymax:
                ymin = np.ceil(np.amax(y[:,1])+np.abs(0.1*np.amax(y[:,1])))
        dataoptions = []
        for j,r in enumerate(R):
            dataoptions.append('green!' + str(gradations[j]) + '!black')   
        axisoptions = '\n ' \
                    'width=30cm,\n' \
                    'title={$\\varepsilon_{\\left(xx\\right)}$ along circumferential sections},\n' \
                    'xlabel={$\\psi\\left[^{\\circ}\\right]$},ylabel={$\\varepsilon_{\\left(xx\\right)}\\left[\\frac{\\mu m}{\\mu m}\\right]$},\n' \
                    'xmin=' + str(xmin) + ',\n' \
                    'xmax=' + str(xmax) + ',\n' \
                    'ymin=' + str(ymin) + ',\n' \
                    'ymax=' + str(ymax) + ',\n' \
                    'tick align=outside,\n' \
                    'tick label style={font=\\tiny},\n' \
                    'xtick=' + xlabels + ',\n' \
                    'xmajorgrids,\n' \
                    'x grid style={lightgray!92.026143790849673!black},\n' \
                    'ymajorgrids,\n' \
                    'y grid style={lightgray!92.026143790849673!black},\n' \
                    'line width=0.35mm,\n' \
                    'legend style={draw=white!80.0!black,font=\\fontsize{12}{6}\\selectfont},\n' \
                    'legend entries=' + legendEntries + ',\n' \
                    'legend cell align={left}\n'
        writeLatexMultiplePlots(wd,project,latexfolder,'allE11OnCircumferentialPaths',E11,axisoptions,dataoptions)
        
        ymin = np.floor(np.amin(E22[0][:,1])-np.abs(0.1*np.amin(E22[0][:,1])))
        ymax = np.ceil(np.amax(E22[0][:,1])+np.abs(0.1*np.amax(E22[0][:,1])))
        for j,y in enumerate(E22):
            if np.floor(np.amin(y[:,1])-np.abs(0.1*np.amin(y[:,1])))<ymin:
                ymin = np.floor(np.amin(y[:,1])-np.abs(0.1*np.amin(y[:,1])))
            if np.ceil(np.amax(y[:,1])+np.abs(0.1*np.amax(y[:,1])))>ymax:
                ymin = np.ceil(np.amax(y[:,1])+np.abs(0.1*np.amax(y[:,1])))
        dataoptions = []
        for j,r in enumerate(R):
            dataoptions.append('red!' + str(gradations[j]) + '!black')   
        axisoptions = '\n ' \
                    'width=30cm,\n' \
                    'title={$\\varepsilon_{\\left(zz\\right)}$ along circumferential sections},\n' \
                    'xlabel={$\\psi\\left[^{\\circ}\\right]$},ylabel={$\\varepsilon_{\\left(zz\\right)}\\left[\\frac{\\mu m}{\\mu m}\\right]$},\n' \
                    'xmin=' + str(xmin) + ',\n' \
                    'xmax=' + str(xmax) + ',\n' \
                    'ymin=' + str(ymin) + ',\n' \
                    'ymax=' + str(ymax) + ',\n' \
                    'tick align=outside,\n' \
                    'tick label style={font=\\tiny},\n' \
                    'xtick=' + xlabels + ',\n' \
                    'xmajorgrids,\n' \
                    'x grid style={lightgray!92.026143790849673!black},\n' \
                    'ymajorgrids,\n' \
                    'y grid style={lightgray!92.026143790849673!black},\n' \
                    'line width=0.35mm,\n' \
                    'legend style={draw=white!80.0!black,font=\\fontsize{12}{6}\\selectfont},\n' \
                    'legend entries=' + legendEntries + ',\n' \
                    'legend cell align={left}\n'
        writeLatexMultiplePlots(wd,project,latexfolder,'allE22OnCircumferentialPaths',E22,axisoptions,dataoptions)
        
        ymin = np.floor(np.amin(E12[0][:,1])-np.abs(0.1*np.amin(E12[0][:,1])))
        ymax = np.ceil(np.amax(E12[0][:,1])+np.abs(0.1*np.amax(E12[0][:,1])))
        for j,y in enumerate(E12):
            if np.floor(np.amin(y[:,1])-np.abs(0.1*np.amin(y[:,1])))<ymin:
                ymin = np.floor(np.amin(y[:,1])-np.abs(0.1*np.amin(y[:,1])))
            if np.ceil(np.amax(y[:,1])+np.abs(0.1*np.amax(y[:,1])))>ymax:
                ymin = np.ceil(np.amax(y[:,1])+np.abs(0.1*np.amax(y[:,1])))
        dataoptions = []
        for j,r in enumerate(R):
            dataoptions.append('blue!' + str(gradations[j]) + '!black')   
        axisoptions = '\n ' \
                    'width=30cm,\n' \
                    'title={$\\varepsilon_{\\left(xz\\right)}$ along circumferential sections},\n' \
                    'xlabel={$\\psi\\left[^{\\circ}\\right]$},ylabel={$\\varepsilon_{\\left(xz\\right)}\\left[\\frac{\\mu m}{\\mu m}\\right]$},\n' \
                    'xmin=' + str(xmin) + ',\n' \
                    'xmax=' + str(xmax) + ',\n' \
                    'ymin=' + str(ymin) + ',\n' \
                    'ymax=' + str(ymax) + ',\n' \
                    'tick align=outside,\n' \
                    'tick label style={font=\\tiny},\n' \
                    'xtick=' + xlabels + ',\n' \
                    'xmajorgrids,\n' \
                    'x grid style={lightgray!92.026143790849673!black},\n' \
                    'ymajorgrids,\n' \
                    'y grid style={lightgray!92.026143790849673!black},\n' \
                    'line width=0.35mm,\n' \
                    'legend style={draw=white!80.0!black,font=\\fontsize{12}{6}\\selectfont},\n' \
                    'legend entries=' + legendEntries + ',\n' \
                    'legend cell align={left}\n'
        writeLatexMultiplePlots(wd,project,latexfolder,'allE12OnCircumferentialPaths',E12,axisoptions,dataoptions)
        '''
        #===========================================================================
        #                         Master surface (fiber)
        #===========================================================================
        # plot stresses
        stresses = []
        with open(join(csvfolder,'stressesOnMaster' + '.csv'),'r') as csv:
            values = csv.readlines()
        for value in values[2:]:
            stresses.append([float(value.split(',')[5]),float(value.split(',')[7]),float(value.split(',')[8]),float(value.split(',')[9]),float(value.split(',')[10])])
        stresses = np.array(stresses)
        stresses = stresses[stresses[:,0].argsort()]
        stresses[:,1] = -stresses[:,1]
    
        xmin = -180.
        xmax = 180.
        xlabels = '{'
        for j,element in enumerate(np.linspace(xmin,xmax,37,endpoint=True)):
            if j>0:
                xlabels += ','
            xlabels += str(element)
        xlabels += '}'
        ymin = np.amin(stresses[:,1:])-np.abs(0.1*np.amin(stresses[:,1:]))
        ymax = np.amax(stresses[:,1:])+np.abs(0.1*np.amax(stresses[:,1:]))
        axisoptions = '\n ' \
                    'width=30cm,\n' \
                    'title={Stress components at fiber/matrix interface on fiber surface},\n' \
                    'xlabel={$\\psi\\left[^{\\circ}\\right]$},ylabel={$\\sigma_{\\left(\\cdot\\cdot\\right)},\n' \
                    '\\tau_{\\left(\\cdot\\cdot\\right)}\\left[MPa\\right]$},\n' \
                    'xmin=' + str(xmin) + ',\n' \
                    'xmax=' + str(xmax) + ',\n' \
                    'ymin=' + str(ymin) + ',\n' \
                    'ymax=' + str(ymax) + ',\n' \
                    'tick align=outside,\n' \
                    'tick label style={font=\\tiny},\n' \
                    'xtick=' + xlabels + ',\n' \
                    'xmajorgrids,\n' \
                    'x grid style={lightgray!92.026143790849673!black},\n' \
                    'ymajorgrids,\n' \
                    'y grid style={lightgray!92.026143790849673!black},\n' \
                    'line width=0.35mm,\n' \
                    'legend style={draw=white!80.0!black,font=\\fontsize{12}{6}\\selectfont},\n' \
                    'legend entries={{$\\sigma_{nn}$},{$\\tau_{n\\psi}$},{$\\tau_{nz}$},{$\\tau^{f}_{n\\psi}$}},\n' \
                    'legend cell align={left}\n'
        dataoptions = ['blue','green!50.196078431372548!black','red','black']
        data = [np.transpose(np.array([stresses[:,0],stresses[:,1]])),np.transpose(np.array([stresses[:,0],stresses[:,2]])),np.transpose(np.array([stresses[:,0],stresses[:,3]])),np.transpose(np.array([stresses[:,0],stresses[:,4]]))]
        writeLatexMultiplePlots(wd,project,latexfolder,'allStressesOnMaster',data,axisoptions,dataoptions)
        
        ymin = np.amin(stresses[:,1])-np.abs(0.1*np.amin(stresses[:,1]))
        ymax = np.amax(stresses[:,1])+np.abs(0.1*np.amax(stresses[:,1]))
        axisoptions = '\n ' \
                    'width=30cm,\n' \
                    'title={Normal stress at fiber/matrix interface on fiber surface},\n' \
                    'xlabel={$\\psi\\left[^{\\circ}\\right]$},ylabel={$\\sigma_{\\left(nn\\right)}\\left[MPa\\right]$},\n' \
                    'xmin=' + str(xmin) + ',\n' \
                    'xmax=' + str(xmax) + ',\n' \
                    'ymin=' + str(ymin) + ',\n' \
                    'ymax=' + str(ymax) + ',\n' \
                    'tick align=outside,\n' \
                    'tick label style={font=\\tiny},\n' \
                    'xtick=' + xlabels + ',\n' \
                    'xmajorgrids,\n' \
                    'x grid style={lightgray!92.026143790849673!black},\n' \
                    'ymajorgrids,\n' \
                    'y grid style={lightgray!92.026143790849673!black},\n' \
                    'line width=0.35mm,\n'
        dataoptions = 'blue'
        data = np.transpose(np.array([stresses[:,0],stresses[:,1]]))
        writeLatexSinglePlot(wd,project,latexfolder,'normalStressOnMaster',data,axisoptions,dataoptions)
        
        ymin = np.amin(stresses[:,2])-np.abs(0.1*np.amin(stresses[:,2]))
        ymax = np.amax(stresses[:,2])+np.abs(0.1*np.amax(stresses[:,2]))
        axisoptions = '\n ' \
                    'width=30cm,\n' \
                    'title={In-plane tangential stress at fiber/matrix interface on fiber surface},\n' \
                    'xlabel={$\\psi\\left[^{\\circ}\\right]$},ylabel={$\\tau_{\\left(n\\psi\\right)}\\left[MPa\\right]$},\n' \
                    'xmin=' + str(xmin) + ',\n' \
                    'xmax=' + str(xmax) + ',\n' \
                    'ymin=' + str(ymin) + ',\n' \
                    'ymax=' + str(ymax) + ',\n' \
                    'tick align=outside,\n' \
                    'tick label style={font=\\tiny},\n' \
                    'xtick=' + xlabels + ',\n' \
                    'xmajorgrids,\n' \
                    'x grid style={lightgray!92.026143790849673!black},\n' \
                    'ymajorgrids,\n' \
                    'y grid style={lightgray!92.026143790849673!black},\n' \
                    'line width=0.35mm,\n'
        dataoptions = 'green!50.196078431372548!black'
        data = np.transpose(np.array([stresses[:,0],stresses[:,2]]))
        writeLatexSinglePlot(wd,project,latexfolder,'inplaneTangentialStressOnMaster',data,axisoptions,dataoptions)
        
        ymin = np.amin(stresses[:,3])-np.abs(0.1*np.amin(stresses[:,3]))
        ymax = np.amax(stresses[:,3])+np.abs(0.1*np.amax(stresses[:,3]))
        axisoptions = '\n ' \
                    'width=30cm,\n' \
                    'title={Out-of-plane tangential stress at fiber/matrix interface on fiber surface},\n' \
                    'xlabel={$\\psi\\left[^{\\circ}\\right]$},ylabel={$\\tau_{\\left(nz\\right)}\\left[MPa\\right]$},\n' \
                    'xmin=' + str(xmin) + ',\n' \
                    'xmax=' + str(xmax) + ',\n' \
                    'ymin=' + str(ymin) + ',\n' \
                    'ymax=' + str(ymax) + ',\n' \
                    'tick align=outside,\n' \
                    'tick label style={font=\\tiny},\n' \
                    'xtick=' + xlabels + ',\n' \
                    'xmajorgrids,\n' \
                    'x grid style={lightgray!92.026143790849673!black},\n' \
                    'ymajorgrids,\n' \
                    'y grid style={lightgray!92.026143790849673!black},\n' \
                    'line width=0.35mm,\n'
        dataoptions = 'red'
        data = np.transpose(np.array([stresses[:,0],stresses[:,3]]))
        writeLatexSinglePlot(wd,project,latexfolder,'outofplaneTangentialStressOnMaster',data,axisoptions,dataoptions)
        
        ymin = np.amin(stresses[:,4])-np.abs(0.1*np.amin(stresses[:,4]))
        ymax = np.amax(stresses[:,4])+np.abs(0.1*np.amax(stresses[:,4]))
        axisoptions = '\n ' \
                    'width=30cm,\n' \
                    'title={Frictional in-plane tangential stress at fiber/matrix interface on fiber surface},\n' \
                    'xlabel={$\\psi\\left[^{\\circ}\\right]$},ylabel={$\\tau^{f}_{\\left(n\\psi\\right)}\\left[MPa\\right]$},\n' \
                    'xmin=' + str(xmin) + ',\n' \
                    'xmax=' + str(xmax) + ',\n' \
                    'ymin=' + str(ymin) + ',\n' \
                    'ymax=' + str(ymax) + ',\n' \
                    'tick align=outside,\n' \
                    'tick label style={font=\\tiny},\n' \
                    'xtick=' + xlabels + ',\n' \
                    'xmajorgrids,\n' \
                    'x grid style={lightgray!92.026143790849673!black},\n' \
                    'ymajorgrids,\n' \
                    'y grid style={lightgray!92.026143790849673!black},\n' \
                    'line width=0.35mm,\n'
        dataoptions = 'black'
        data = np.transpose(np.array([stresses[:,0],stresses[:,4]]))
        writeLatexSinglePlot(wd,project,latexfolder,'frictionalStressOnMaster',data,axisoptions,dataoptions)
    
        print('...done')
        
        #===========================================================================
        #                         Slave surface (matrix)
        #===========================================================================
        # plot stresses
        print('Plotting stresses on slave surface...')
        stresses = []
        with open(join(csvfolder,'stressesOnSlave' + '.csv'),'r') as csv:
            values = csv.readlines()
        for value in values[2:]:
            stresses.append([float(value.split(',')[5]),float(value.split(',')[7]),float(value.split(',')[8]),float(value.split(',')[9]),float(value.split(',')[10])])
        stresses = np.array(stresses)
        stresses = stresses[stresses[:,0].argsort()]
        stresses[:,1] = -stresses[:,1]
        '''
        fig = plt.figure()
        normal, = plt.plot(stresses[:,0],stresses[:,1],color='blue', linewidth=1.0, linestyle="-",label=r"$\sigma_{nn}$")
        tang1, = plt.plot(stresses[:,0],stresses[:,2],color='green', linewidth=1.0, linestyle="-",label=r"$\tau_{n\psi}$")
        tang2, = plt.plot(stresses[:,0],stresses[:,3],color='red', linewidth=1.0, linestyle="-",label=r"$\tau_{nz}$")
        fric, = plt.plot(stresses[:,0],stresses[:,4],color='black', linewidth=1.0, linestyle="-",label=r"$\tau^{f}_{n\psi}$")
        plt.legend(handles=[normal, tang1, tang2, fric])
        plt.xlim(-180.0,180.0)
        plt.xticks(np.linspace(-180.0,180.0,37,endpoint=True))
        plt.xlabel(r"$\psi\left[^{\circ}\right]$")
        plt.ylabel(r"$\sigma_{\left(\cdot\cdot\right)},\tau_{\left(\cdot\cdot\right)}\left[MPa\right]$",rotation=90)
        plt.title("Stress components at fiber/matrix interface on matrix surface")
        plt.grid(True)
        fig.savefig(join(pngfolder,'allStressesOnSlave' + '.png'),dpi=fig.dpi)
        '''
        xmin = -180.
        xmax = 180.
        xlabels = '{'
        for j,element in enumerate(np.linspace(xmin,xmax,37,endpoint=True)):
            if j>0:
                xlabels += ','
            xlabels += str(element)
        xlabels += '}'
        ymin = np.amin(stresses[:,1:])-np.abs(0.1*np.amin(stresses[:,1:]))
        ymax = np.amax(stresses[:,1:])+np.abs(0.1*np.amax(stresses[:,1:]))
        axisoptions = '\n ' \
                    'width=30cm,\n' \
                    'title={Stress components at fiber/matrix interface on matrix surface},\n' \
                    'xlabel={$\\psi\\left[^{\\circ}\\right]$},ylabel={$\\sigma_{\\left(\\cdot\\cdot\\right)},\n' \
                    '\\tau_{\\left(\\cdot\\cdot\\right)}\\left[MPa\\right]$},\n' \
                    'xmin=' + str(xmin) + ',\n' \
                    'xmax=' + str(xmax) + ',\n' \
                    'ymin=' + str(ymin) + ',\n' \
                    'ymax=' + str(ymax) + ',\n' \
                    'tick align=outside,\n' \
                    'tick label style={font=\\tiny},\n' \
                    'xtick=' + xlabels + ',\n' \
                    'xmajorgrids,\n' \
                    'x grid style={lightgray!92.026143790849673!black},\n' \
                    'ymajorgrids,\n' \
                    'y grid style={lightgray!92.026143790849673!black},\n' \
                    'line width=0.35mm,\n' \
                    'legend style={draw=white!80.0!black,font=\\fontsize{12}{6}\\selectfont},\n' \
                    'legend entries={{$\\sigma_{nn}$},{$\\tau_{n\\psi}$},{$\\tau_{nz}$},{$\\tau^{f}_{n\\psi}$}},\n' \
                    'legend cell align={left}\n'
        dataoptions = ['blue','green!50.196078431372548!black','red','black']
        data = [np.transpose(np.array([stresses[:,0],stresses[:,1]])),np.transpose(np.array([stresses[:,0],stresses[:,2]])),np.transpose(np.array([stresses[:,0],stresses[:,3]])),np.transpose(np.array([stresses[:,0],stresses[:,4]]))]
        writeLatexMultiplePlots(wd,project,latexfolder,'allStressesOnSlave',data,axisoptions,dataoptions)
        
        ymin = np.amin(stresses[:,1])-np.abs(0.1*np.amin(stresses[:,1]))
        ymax = np.amax(stresses[:,1])+np.abs(0.1*np.amax(stresses[:,1]))
        axisoptions = '\n ' \
                    'width=30cm,\n' \
                    'title={Normal stress at fiber/matrix interface on matrix surface},\n' \
                    'xlabel={$\\psi\\left[^{\\circ}\\right]$},ylabel={$\\sigma_{\\left(nn\\right)}\\left[MPa\\right]$},\n' \
                    'xmin=' + str(xmin) + ',\n' \
                    'xmax=' + str(xmax) + ',\n' \
                    'ymin=' + str(ymin) + ',\n' \
                    'ymax=' + str(ymax) + ',\n' \
                    'tick align=outside,\n' \
                    'tick label style={font=\\tiny},\n' \
                    'xtick=' + xlabels + ',\n' \
                    'xmajorgrids,\n' \
                    'x grid style={lightgray!92.026143790849673!black},\n' \
                    'ymajorgrids,\n' \
                    'y grid style={lightgray!92.026143790849673!black},\n' \
                    'line width=0.35mm,\n'
        dataoptions = 'blue'
        data = np.transpose(np.array([stresses[:,0],stresses[:,1]]))
        writeLatexSinglePlot(wd,project,latexfolder,'normalStressOnSlave',data,axisoptions,dataoptions)
        
        ymin = np.amin(stresses[:,2])-np.abs(0.1*np.amin(stresses[:,2]))
        ymax = np.amax(stresses[:,2])+np.abs(0.1*np.amax(stresses[:,2]))
        axisoptions = '\n ' \
                    'width=30cm,\n' \
                    'title={In-plane tangential stress at fiber/matrix interface on matrix surface},\n' \
                    'xlabel={$\\psi\\left[^{\\circ}\\right]$},ylabel={$\\tau_{\\left(n\\psi\\right)}\\left[MPa\\right]$},\n' \
                    'xmin=' + str(xmin) + ',\n' \
                    'xmax=' + str(xmax) + ',\n' \
                    'ymin=' + str(ymin) + ',\n' \
                    'ymax=' + str(ymax) + ',\n' \
                    'tick align=outside,\n' \
                    'tick label style={font=\\tiny},\n' \
                    'xtick=' + xlabels + ',\n' \
                    'xmajorgrids,\n' \
                    'x grid style={lightgray!92.026143790849673!black},\n' \
                    'ymajorgrids,\n' \
                    'y grid style={lightgray!92.026143790849673!black},\n' \
                    'line width=0.35mm,\n'
        dataoptions = 'green!50.196078431372548!black'
        data = np.transpose(np.array([stresses[:,0],stresses[:,2]]))
        writeLatexSinglePlot(wd,project,latexfolder,'inplaneTangentialStressOnSlave',data,axisoptions,dataoptions)
        
        ymin = np.amin(stresses[:,3])-np.abs(0.1*np.amin(stresses[:,3]))
        ymax = np.amax(stresses[:,3])+np.abs(0.1*np.amax(stresses[:,3]))
        axisoptions = '\n ' \
                    'width=30cm,\n' \
                    'title={Out-of-plane tangential stress at fiber/matrix interface on matrix surface},\n' \
                    'xlabel={$\\psi\\left[^{\\circ}\\right]$},ylabel={$\\tau_{\\left(nz\\right)}\\left[MPa\\right]$},\n' \
                    'xmin=' + str(xmin) + ',\n' \
                    'xmax=' + str(xmax) + ',\n' \
                    'ymin=' + str(ymin) + ',\n' \
                    'ymax=' + str(ymax) + ',\n' \
                    'tick align=outside,\n' \
                    'tick label style={font=\\tiny},\n' \
                    'xtick=' + xlabels + ',\n' \
                    'xmajorgrids,\n' \
                    'x grid style={lightgray!92.026143790849673!black},\n' \
                    'ymajorgrids,\n' \
                    'y grid style={lightgray!92.026143790849673!black},\n' \
                    'line width=0.35mm,\n'
        dataoptions = 'red'
        data = np.transpose(np.array([stresses[:,0],stresses[:,3]]))
        writeLatexSinglePlot(wd,project,latexfolder,'outofplaneTangentialStressOnSlave',data,axisoptions,dataoptions)
        
        ymin = np.amin(stresses[:,4])-np.abs(0.1*np.amin(stresses[:,4]))
        ymax = np.amax(stresses[:,4])+np.abs(0.1*np.amax(stresses[:,4]))
        axisoptions = '\n ' \
                    'width=30cm,\n' \
                    'title={Frictional in-plane tangential stress at fiber/matrix interface on matrix surface},\n' \
                    'xlabel={$\\psi\\left[^{\\circ}\\right]$},ylabel={$\\tau^{f}_{\\left(n\\psi\\right)}\\left[MPa\\right]$},\n' \
                    'xmin=' + str(xmin) + ',\n' \
                    'xmax=' + str(xmax) + ',\n' \
                    'ymin=' + str(ymin) + ',\n' \
                    'ymax=' + str(ymax) + ',\n' \
                    'tick align=outside,\n' \
                    'tick label style={font=\\tiny},\n' \
                    'xtick=' + xlabels + ',\n' \
                    'xmajorgrids,\n' \
                    'x grid style={lightgray!92.026143790849673!black},\n' \
                    'ymajorgrids,\n' \
                    'y grid style={lightgray!92.026143790849673!black},\n' \
                    'line width=0.35mm,\n'
        dataoptions = 'black'
        data = np.transpose(np.array([stresses[:,0],stresses[:,4]]))
        writeLatexSinglePlot(wd,project,latexfolder,'frictionalStressOnSlave',data,axisoptions,dataoptions)
    
        print('...done')
        
        # plot displacements
        print('Plotting displacements on slave surface...')
        stresses = []
        disps = []
        with open(join(csvfolder,'displacementsOnSlave' + '.csv'),'r') as csv:
            values = csv.readlines()
        for value in values[2:]:
            disps.append([float(value.split(',')[5]),float(value.split(',')[6]),float(value.split(',')[7])])
        disps = np.array(disps)
        disps = disps[disps[:,0].argsort()]
        xmin = -180.
        xmax = 180.
        xlabels = '{'
        for j,element in enumerate(np.linspace(xmin,xmax,37,endpoint=True)):
            if j>0:
                xlabels += ','
            xlabels += str(element)
        xlabels += '}'
        ymin = np.amin(disps[:,1:])-np.abs(0.1*np.amin(disps[:,1:]))
        ymax = np.amax(disps[:,1:])+np.abs(0.1*np.amax(disps[:,1:]))
        axisoptions = '\n ' \
                    'width=30cm,\n' \
                    'title={Displacement components at fiber/matrix interface on matrix surface},\n' \
                    'xlabel={$\\psi\\left[^{\\circ}\\right]$},ylabel={$u_{\\left(\\cdot\\cdot\\right)}\\left[\mu m\\right]$},\n' \
                    'xmin=' + str(xmin) + ',\n' \
                    'xmax=' + str(xmax) + ',\n' \
                    'ymin=' + str(ymin) + ',\n' \
                    'ymax=' + str(ymax) + ',\n' \
                    'tick align=outside,\n' \
                    'tick label style={font=\\tiny},\n' \
                    'xtick=' + xlabels + ',\n' \
                    'xmajorgrids,\n' \
                    'x grid style={lightgray!92.026143790849673!black},\n' \
                    'ymajorgrids,\n' \
                    'y grid style={lightgray!92.026143790849673!black},\n' \
                    'line width=0.35mm,\n' \
                    'legend style={draw=white!80.0!black,font=\\fontsize{12}{6}\\selectfont},\n' \
                    'legend entries={{$u_{nn}$},{$u_{n\\psi}$}},\n' \
                    'legend cell align={left}\n'
        dataoptions = ['blue','green!50.196078431372548!black']
        data = [np.transpose(np.array([disps[:,0],disps[:,1]])),np.transpose(np.array([disps[:,0],disps[:,2]]))]
        writeLatexMultiplePlots(wd,project,latexfolder,'allDispsOnSlave',data,axisoptions,dataoptions)
        
        ymin = np.amin(disps[:,1])-np.abs(0.1*np.amin(disps[:,1]))
        ymax = np.amax(disps[:,1])+np.abs(0.1*np.amax(disps[:,1]))
        axisoptions = '\n ' \
                    'width=30cm,\n' \
                    'title={Normal (opening) displacement at fiber/matrix interface on matrix surface},\n' \
                    'xlabel={$\\psi\\left[^{\\circ}\\right]$},ylabel={$u_{\\left(nn\\right)}\\left[\mu m\\right]$},\n' \
                    'xmin=' + str(xmin) + ',\n' \
                    'xmax=' + str(xmax) + ',\n' \
                    'ymin=' + str(ymin) + ',\n' \
                    'ymax=' + str(ymax) + ',\n' \
                    'tick align=outside,\n' \
                    'tick label style={font=\\tiny},\n' \
                    'xtick=' + xlabels + ',\n' \
                    'xmajorgrids,\n' \
                    'x grid style={lightgray!92.026143790849673!black},\n' \
                    'ymajorgrids,\n' \
                    'y grid style={lightgray!92.026143790849673!black},\n' \
                    'line width=0.35mm,\n'
        dataoptions = 'blue'
        data = np.transpose(np.array([disps[:,0],disps[:,1]]))
        writeLatexSinglePlot(wd,project,latexfolder,'normalDispsOnSlave',data,axisoptions,dataoptions)
        
        ymin = np.amin(disps[:,2])-np.abs(0.1*np.amin(disps[:,2]))
        ymax = np.amax(disps[:,2])+np.abs(0.1*np.amax(disps[:,2]))
        axisoptions = '\n ' \
                    'width=30cm,\n' \
                    'title={In-plane tangential displacement (slip) at fiber/matrix interface on matrix surface},\n' \
                    'xlabel={$\\psi\\left[^{\\circ}\\right]$},ylabel={$u_{\\left(n\\psi\\right)}\\left[\mu m\\right]$},\n' \
                    'xmin=' + str(xmin) + ',\n' \
                    'xmax=' + str(xmax) + ',\n' \
                    'ymin=' + str(ymin) + ',\n' \
                    'ymax=' + str(ymax) + ',\n' \
                    'tick align=outside,\n' \
                    'tick label style={font=\\tiny},\n' \
                    'xtick=' + xlabels + ',\n' \
                    'xmajorgrids,\n' \
                    'x grid style={lightgray!92.026143790849673!black},\n' \
                    'ymajorgrids,\n' \
                    'y grid style={lightgray!92.026143790849673!black},\n' \
                    'line width=0.35mm,\n'
        dataoptions = 'green!50.196078431372548!black'
        data = np.transpose(np.array([disps[:,0],disps[:,2]]))
        writeLatexSinglePlot(wd,project,latexfolder,'inplaneTangentialDispsOnSlave',data,axisoptions,dataoptions)

if __name__ == "__main__":
    main(sys.argv[1:])
