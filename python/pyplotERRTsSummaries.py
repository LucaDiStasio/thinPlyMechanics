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

def plotEnergyReleaseDataOverSims(wd,statusfile,outdir,prefix,refdatadir,refdatafile,nContour):
    # read status file
    with open(join(wd,statusfile),'r') as sta:
        stalines = sta.readlines()
    for i,line in enumerate(stalines[1:]):
        words = line.split(',')
        project = words[0]
        if not exists(join(wd,project,'dat')):
            makedirs(join(wd,project,'dat'))
        #plotEnergyReleaseDataPerSim(wd,project,nContour)
    if not exists(join(outdir,prefix)):
        makedirs(join(outdir,prefix))
    if not exists(join(outdir,prefix,'latex')):
        makedirs(join(outdir,prefix,'latex'))
    if not exists(join(outdir,prefix,'pdf')):
        makedirs(join(outdir,prefix,'pdf'))
    xmin = -180.
    xmax = 180.
    xlabels = '{'
    for j,element in enumerate(np.linspace(xmin,xmax,37,endpoint=True)):
        if j>0:
            xlabels += ','
        xlabels += str(element)
    xlabels += '}'
    bemB0 = 0
    bemTheta = []
    bemGIoverG0 = []
    bemGIIoverG0 = []
    bemGTOToverG0 = []
    with open(join(refdatadir,refdatafile + '.csv'),'r') as csv:
        lines = csv.readlines()
    bemG0 = float(lines[0].replace('\n','').split(',')[-1])
    for line in lines[2:]:
        bemTheta.append(float(line.replace('\n','').split(',')[0]))
        bemGIoverG0.append(float(line.replace('\n','').split(',')[1]))
        bemGIIoverG0.append(float(line.replace('\n','').split(',')[2]))
        bemGTOToverG0.append(float(line.replace('\n','').split(',')[3]))
    bemTheta = np.array(bemTheta)
    bemGIoverG0 = np.array(bemGIoverG0)
    bemGIIoverG0 = np.array(bemGIIoverG0)
    bemGTOToverG0 = np.array(bemGTOToverG0)
    xmin = 0.
    xmax = 180.
    xlabels = '{'
    for j,element in enumerate(np.linspace(xmin,xmax,19,endpoint=True)):
        if j>0:
            xlabels += ','
        xlabels += str(element)
    xlabels += '}'
    ymin = np.around(np.amin(bemGTOToverG0)-np.abs(0.1*np.amin(bemGTOToverG0)),decimals=2)
    ymax = np.around(np.amax(bemGTOToverG0)+np.abs(0.1*np.amax(bemGTOToverG0)),decimals=2)
    axisoptions = '\n ' \
                  'width=30cm,\n' \
                  'title={Single fiber in infinite matrix with BEM: $\\frac{G_{\\left(\\cdot\\cdot\\right)}}{G_{0}}$ vs $\\theta$},\n' \
                  'xlabel={$\\theta\\left[^{\\circ}\\right]$},ylabel={$\\frac{G_{\\left(\\cdot\\cdot\\right)}}{G_{0}}\\left[-\\right]$},\n' \
                  'xmin=' + str(xmin) + ',\n' \
                  'xmax=' + str(xmax) + ',\n' \
                  'ymin=' + str(ymin) + ',\n' \
                  'ymax=' + str(ymax) + ',\n' \
                  'title style={font=\\fontsize{16}{8}\\selectfont},\n' \
                  'xlabel style={at={(axis description cs:0.5,-0.02)},anchor=north,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'ylabel style={at={(axis description cs:-0.01,.5)},anchor=south,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'tick align=outside,\n' \
                  'tick label style={font=\\normalsize},\n' \
                  'xtick=' + xlabels + ',\n' \
                  'xmajorgrids,\n' \
                  'x grid style={lightgray!92.026143790849673!black},\n' \
                  'ymajorgrids,\n' \
                  'y grid style={lightgray!92.026143790849673!black},\n' \
                  'line width=0.75mm,\n' \
                  'legend style={draw=white!80.0!black,font=\\fontsize{16}{12}\\selectfont},\n' \
                  'legend entries={{$\\frac{G_{I}}{G_{0}}$},{$\\frac{G_{II}}{G_{0}}$},{$\\frac{G_{TOT}}{G_{0}}$}},\n' \
                  'legend cell align={left}\n'
    dataoptions = ['blue,smooth,mark=*','green!50.196078431372548!black,smooth,mark=*','red,smooth,mark=*']
    data = [np.transpose(np.array([bemTheta,bemGIoverG0])),np.transpose(np.array([bemTheta,bemGIIoverG0])),np.transpose(np.array([bemTheta,bemGTOToverG0]))]
    writeLatexMultiplePlots(outdir,prefix,join(outdir,prefix,'latex'),prefix + '_refGsfromBEM',data,axisoptions,dataoptions)
    theta = []
    GI = []
    GII = []
    GTOT = []
    GIoverGTOT = []
    GIIoverGTOT = []
    J = []
    JKs = []
    JoverGTOT = []
    JKsoverGTOT = []
    JKsoverJ = []
    with open(join(outdir,prefix + '_GandJ' + '.csv'),'r') as csv:
        lines = csv.readlines()
    for line in lines[2:]:
        theta.append(float(line.replace('\n','').split(',')[0]))
        GI.append(float(line.replace('\n','').split(',')[1]))
        GII.append(float(line.replace('\n','').split(',')[2]))
        GTOT.append(float(line.replace('\n','').split(',')[3]))
        GIoverGTOT.append(float(line.replace('\n','').split(',')[4]))
        GIIoverGTOT.append(float(line.replace('\n','').split(',')[5]))
        offset = 5
        temp = []
        for c in range(1,nContour+1):
            index = offset + c
            temp.append(float(line.replace('\n','').split(',')[index]))
        J.append(temp)
        offset = index
        temp = []
        for c in range(1,nContour+1):
            index = offset + c
            temp.append(float(line.replace('\n','').split(',')[index]))
        JKs.append(temp)
        offset = index
        temp = []
        for c in range(1,nContour+1):
            index = offset + c
            temp.append(float(line.replace('\n','').split(',')[index]))
        JoverGTOT.append(temp)
        offset = index
        temp = []
        for c in range(1,nContour+1):
            index = offset + c
            temp.append(float(line.replace('\n','').split(',')[index]))
        JKsoverGTOT.append(temp)
        offset = index
        temp = []
        for c in range(1,nContour+1):
            index = offset + c
            temp.append(float(line.replace('\n','').split(',')[index]))
        JKsoverJ.append(temp)
    theta = np.array(theta)
    GI = np.array(GI)
    GII = np.array(GII)
    GTOT = np.array(GTOT)
    GIoverGTOT = np.array(GIoverGTOT)
    GIIoverGTOT = np.array(GIIoverGTOT)
    J = np.array(J)
    JKs = np.array(JKs)
    JoverGTOT = np.array(JoverGTOT)
    JKsoverGTOT = np.array(JKsoverGTOT)
    JKsoverJ = np.array(JKsoverJ)
    xmin = -180.
    xmax = 180.
    xlabels = '{'
    for j,element in enumerate(np.linspace(xmin,xmax,37,endpoint=True)):
        if j>0:
            xlabels += ','
        xlabels += str(element)
    xlabels += '}'
    ymin = np.amin(GTOT)-np.abs(0.1*np.amin(GTOT))
    ymax = np.amax(GTOT)+np.abs(0.1*np.amax(GTOT))
    axisoptions = '\n ' \
                  'width=30cm,\n' \
                  'title={Energy release rate  $G_{\\left(\\cdot\\cdot\\right)}$ vs debond angle  $\\theta$},\n' \
                  'xlabel={$\\theta\\left[^{\\circ}\\right]$},ylabel={$G_{\\left(\\cdot\\cdot\\right)}\\left[\\frac{J}{m^{2}}\\right]$},\n' \
                  'xmin=' + str(xmin) + ',\n' \
                  'xmax=' + str(xmax) + ',\n' \
                  'ymin=' + str(ymin) + ',\n' \
                  'ymax=' + str(ymax) + ',\n' \
                  'title style={font=\\fontsize{16}{8}\\selectfont},\n' \
                  'xlabel style={at={(axis description cs:0.5,-0.02)},anchor=north,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'ylabel style={at={(axis description cs:-0.01,.5)},anchor=south,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'tick align=outside,\n' \
                  'tick label style={font=\\normalsize},\n' \
                  'xtick=' + xlabels + ',\n' \
                  'xmajorgrids,\n' \
                  'x grid style={lightgray!92.026143790849673!black},\n' \
                  'ymajorgrids,\n' \
                  'y grid style={lightgray!92.026143790849673!black},\n' \
                  'line width=0.75mm,\n' \
                  'legend style={draw=white!80.0!black,font=\\fontsize{16}{12}\\selectfont},\n' \
                  'legend entries={{$G_{I}$},{$G_{II}$},{$G_{TOT}$}},\n' \
                  'legend cell align={left}\n'
    dataoptions = ['blue,smooth,mark=*','green!50.196078431372548!black,smooth,mark=*','red,smooth,mark=*']
    data = [np.transpose(np.array([theta,GI])),np.transpose(np.array([theta,GII])),np.transpose(np.array([theta,GTOT]))]
    writeLatexMultiplePlots(outdir,prefix,join(outdir,prefix,'latex'),prefix + '_Gs',data,axisoptions,dataoptions)
    ymin = 0.0
    ymax = 1.05
    axisoptions = '\n ' \
                  'width=30cm,\n' \
                  'title={Mode ratio vs debond angle  $\\theta$},\n' \
                  'xlabel={$\\theta\\left[^{\\circ}\\right]$},ylabel={$\\frac{G_{\\left(\\cdot\\cdot\\right)}}{G_{TOT}}\\left[-\\right]$},\n' \
                  'xmin=' + str(xmin) + ',\n' \
                  'xmax=' + str(xmax) + ',\n' \
                  'ymin=' + str(ymin) + ',\n' \
                  'ymax=' + str(ymax) + ',\n' \
                  'title style={font=\\fontsize{16}{8}\\selectfont},\n' \
                  'xlabel style={at={(axis description cs:0.5,-0.02)},anchor=north,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'ylabel style={at={(axis description cs:-0.01,.5)},anchor=south,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'tick align=outside,\n' \
                  'tick label style={font=\\normalsize},\n' \
                  'xtick=' + xlabels + ',\n' \
                  'xmajorgrids,\n' \
                  'x grid style={lightgray!92.026143790849673!black},\n' \
                  'ymajorgrids,\n' \
                  'y grid style={lightgray!92.026143790849673!black},\n' \
                  'line width=0.75mm,\n' \
                  'legend style={draw=white!80.0!black,font=\\fontsize{16}{12}\\selectfont},\n' \
                  'legend entries={{$\\frac{G_{I}}{G_{I}+G_{II}}$},{$\\frac{G_{II}}{G_{I}+G_{II}}$}},\n' \
                  'legend cell align={left}\n'
    dataoptions = ['blue,mark=*','green!50.196078431372548!black,mark=*']
    data = [np.transpose(np.array([theta,GIoverGTOT])),np.transpose(np.array([theta,GIIoverGTOT]))]
    writeLatexMultiplePlots(outdir,prefix,join(outdir,prefix,'latex'),prefix + '_modeRatios',data,axisoptions,dataoptions)
    ymin = np.amin(J[:,1:])-np.abs(0.1*np.amin(J[:,1:]))
    ymax = np.amax(J[:,1:])+np.abs(0.1*np.amax(J[:,1:]))
    legendEntries = '{'
    dataoptions = []
    data = []
    for c in range(0,nContour):
        if c>0:
            legendEntries += ','
        legendEntries += '{Contour ' + str(c+1) + '}'
        dataoptions.append('green!' + str(float(100.*c/nContour)) + '!black,smooth,mark=*')
        data.append(np.transpose(np.array([theta,J[:,c]])))
    legendEntries += '}'   
    axisoptions = '\n ' \
                  'width=30cm,\n' \
                  'title={Contour integral $J$ vs debond angle  $\\theta$},\n' \
                  'xlabel={$\\theta\\left[^{\\circ}\\right]$},ylabel={$J\\left[\\frac{J}{m^{2}}\\right]$},\n' \
                  'xmin=' + str(xmin) + ',\n' \
                  'xmax=' + str(xmax) + ',\n' \
                  'ymin=' + str(ymin) + ',\n' \
                  'ymax=' + str(ymax) + ',\n' \
                  'title style={font=\\fontsize{16}{8}\\selectfont},\n' \
                  'xlabel style={at={(axis description cs:0.5,-0.02)},anchor=north,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'ylabel style={at={(axis description cs:-0.01,.5)},anchor=south,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'tick align=outside,\n' \
                  'tick label style={font=\\normalsize},\n' \
                  'xtick=' + xlabels + ',\n' \
                  'xmajorgrids,\n' \
                  'x grid style={lightgray!92.026143790849673!black},\n' \
                  'ymajorgrids,\n' \
                  'y grid style={lightgray!92.026143790849673!black},\n' \
                  'line width=0.75mm,\n' \
                  'legend style={draw=white!80.0!black,font=\\fontsize{16}{12}\\selectfont},\n' \
                  'legend entries=' + legendEntries + ',\n' \
                  'legend cell align={left}\n'
    writeLatexMultiplePlots(outdir,prefix,join(outdir,prefix,'latex'),prefix + '_Js',data,axisoptions,dataoptions)
    ymin = np.amin(JKs[:,1:])-np.abs(0.1*np.amin(JKs[:,1:]))
    ymax = np.amax(JKs[:,1:])+np.abs(0.1*np.amax(JKs[:,1:]))
    legendEntries = '{'
    dataoptions = []
    data = []
    for c in range(0,nContour):
        if c>0:
            legendEntries += ','
        legendEntries += '{Contour ' + str(c+1) + '}'
        dataoptions.append('green!' + str(float(100.*c/nContour)) + '!black,smooth,mark=*')
        data.append(np.transpose(np.array([theta,JKs[:,c]])))
    legendEntries += '}'   
    axisoptions = '\n ' \
                  'width=30cm,\n' \
                  'title={Contour integral $J_{Ks}$ vs debond angle  $\\theta$},\n' \
                  'xlabel={$\\theta\\left[^{\\circ}\\right]$},ylabel={$J_{Ks}\\left[\\frac{J}{m^{2}}\\right]$},\n' \
                  'xmin=' + str(xmin) + ',\n' \
                  'xmax=' + str(xmax) + ',\n' \
                  'ymin=' + str(ymin) + ',\n' \
                  'ymax=' + str(ymax) + ',\n' \
                  'title style={font=\\fontsize{16}{8}\\selectfont},\n' \
                  'xlabel style={at={(axis description cs:0.5,-0.02)},anchor=north,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'ylabel style={at={(axis description cs:-0.01,.5)},anchor=south,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'tick align=outside,\n' \
                  'tick label style={font=\\normalsize},\n' \
                  'xtick=' + xlabels + ',\n' \
                  'xmajorgrids,\n' \
                  'x grid style={lightgray!92.026143790849673!black},\n' \
                  'ymajorgrids,\n' \
                  'y grid style={lightgray!92.026143790849673!black},\n' \
                  'line width=0.75mm,\n' \
                  'legend style={draw=white!80.0!black,font=\\fontsize{16}{12}\\selectfont},\n' \
                  'legend entries=' + legendEntries + ',\n' \
                  'legend cell align={left}\n'
    writeLatexMultiplePlots(outdir,prefix,join(outdir,prefix,'latex'),prefix + '_JKs',data,axisoptions,dataoptions)
    ymin = np.amin([np.amin(J[:,1:]),np.amin(JKs[:,1:])])-np.abs(0.1*np.amin([np.amin(J[:,1:]),np.amin(JKs[:,1:])]))
    ymax = np.amax([np.amax(J[:,1:]),np.amax(JKs[:,1:])])+np.abs(0.1*np.amax([np.amax(J[:,1:]),np.amax(JKs[:,1:])]))
    legendEntries = '{'
    dataoptions = []
    data = []
    for c in range(0,nContour):
        if c>0:
            legendEntries += ','
        legendEntries += '{$J$, Contour ' + str(c+1) + '}'
        dataoptions.append('green!' + str(float(100.*c/nContour)) + '!black,smooth,mark=*')
        data.append(np.transpose(np.array([theta,J[:,c]])))
    for c in range(0,nContour):
        if c>0:
            legendEntries += ','
        legendEntries += '{$J_{Ks}$, Contour ' + str(c+1) + '}'
        dataoptions.append('red!' + str(float(100.*c/nContour)) + '!black,smooth,mark=*')
        data.append(np.transpose(np.array([theta,JKs[:,c]])))
    legendEntries += '}'   
    axisoptions = '\n ' \
                  'width=30cm,\n' \
                  'title={Contour integral $J$ and $J_{Ks}$ vs debond angle  $\\theta$},\n' \
                  'xlabel={$\\theta\\left[^{\\circ}\\right]$},ylabel={$Energy release rate \\left[\\frac{J}{m^{2}}\\right]$},\n' \
                  'xmin=' + str(xmin) + ',\n' \
                  'xmax=' + str(xmax) + ',\n' \
                  'ymin=' + str(ymin) + ',\n' \
                  'ymax=' + str(ymax) + ',\n' \
                  'title style={font=\\fontsize{16}{8}\\selectfont},\n' \
                  'xlabel style={at={(axis description cs:0.5,-0.02)},anchor=north,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'ylabel style={at={(axis description cs:-0.01,.5)},anchor=south,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'tick align=outside,\n' \
                  'tick label style={font=\\normalsize},\n' \
                  'xtick=' + xlabels + ',\n' \
                  'xmajorgrids,\n' \
                  'x grid style={lightgray!92.026143790849673!black},\n' \
                  'ymajorgrids,\n' \
                  'y grid style={lightgray!92.026143790849673!black},\n' \
                  'line width=0.75mm,\n' \
                  'legend style={draw=white!80.0!black,font=\\fontsize{16}{12}\\selectfont},\n' \
                  'legend entries=' + legendEntries + ',\n' \
                  'legend cell align={left}\n'
    writeLatexMultiplePlots(outdir,prefix,join(outdir,prefix,'latex'),prefix + '_JsandJKs',data,axisoptions,dataoptions)
    ymin = np.amin(JoverGTOT[:,1:])-np.abs(0.1*np.amin(JoverGTOT[:,1:]))
    ymax = np.amax(JoverGTOT[:,1:])+np.abs(0.1*np.amax(JoverGTOT[:,1:]))
    legendEntries = '{'
    dataoptions = []
    data = []
    for c in range(0,nContour):
        if c>0:
            legendEntries += ','
        legendEntries += '{Contour ' + str(c+1) + '}'
        dataoptions.append('green!' + str(float(100.*c/nContour)) + '!black,smooth,mark=*')
        data.append(np.transpose(np.array([theta,JoverGTOT[:,c]])))
    legendEntries += '}'   
    axisoptions = '\n ' \
                  'width=30cm,\n' \
                  'title={$\\frac{J}{G_{TOT}}$ vs debond angle  $\\theta$},\n' \
                  'xlabel={$\\theta\\left[^{\\circ}\\right]$},ylabel={$\\frac{J}{G_{TOT}}\\left[-\\right]$},\n' \
                  'xmin=' + str(xmin) + ',\n' \
                  'xmax=' + str(xmax) + ',\n' \
                  'ymin=' + str(ymin) + ',\n' \
                  'ymax=' + str(ymax) + ',\n' \
                  'title style={font=\\fontsize{16}{8}\\selectfont},\n' \
                  'xlabel style={at={(axis description cs:0.5,-0.02)},anchor=north,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'ylabel style={at={(axis description cs:-0.01,.5)},anchor=south,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'tick align=outside,\n' \
                  'tick label style={font=\\normalsize},\n' \
                  'xtick=' + xlabels + ',\n' \
                  'xmajorgrids,\n' \
                  'x grid style={lightgray!92.026143790849673!black},\n' \
                  'ymajorgrids,\n' \
                  'y grid style={lightgray!92.026143790849673!black},\n' \
                  'line width=0.75mm,\n' \
                  'legend style={draw=white!80.0!black,font=\\fontsize{16}{12}\\selectfont},\n' \
                  'legend entries=' + legendEntries + ',\n' \
                  'legend cell align={left}\n'
    writeLatexMultiplePlots(outdir,prefix,join(outdir,prefix,'latex'),prefix + '_JsoverGTOT',data,axisoptions,dataoptions)
    ymin = np.amin(JKsoverGTOT[:,1:])-np.abs(0.1*np.amin(JKsoverGTOT[:,1:]))
    ymax = np.amax(JKsoverGTOT[:,1:])+np.abs(0.1*np.amax(JKsoverGTOT[:,1:]))
    legendEntries = '{'
    dataoptions = []
    data = []
    for c in range(0,nContour):
        if c>0:
            legendEntries += ','
        legendEntries += '{Contour ' + str(c+1) + '}'
        dataoptions.append('green!' + str(float(100.*c/nContour)) + '!black,smooth,mark=*')
        data.append(np.transpose(np.array([theta,JKsoverGTOT[:,c]])))
    legendEntries += '}'   
    axisoptions = '\n ' \
                  'width=30cm,\n' \
                  'title={$\\frac{J_{Ks}}{G_{TOT}}$ vs debond angle  $\\theta$},\n' \
                  'xlabel={$\\theta\\left[^{\\circ}\\right]$},ylabel={$\\frac{J_{Ks}}{G_{TOT}}\\left[-\\right]$},\n' \
                  'xmin=' + str(xmin) + ',\n' \
                  'xmax=' + str(xmax) + ',\n' \
                  'ymin=' + str(ymin) + ',\n' \
                  'ymax=' + str(ymax) + ',\n' \
                  'title style={font=\\fontsize{16}{8}\\selectfont},\n' \
                  'xlabel style={at={(axis description cs:0.5,-0.02)},anchor=north,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'ylabel style={at={(axis description cs:-0.01,.5)},anchor=south,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'tick align=outside,\n' \
                  'tick label style={font=\\normalsize},\n' \
                  'xtick=' + xlabels + ',\n' \
                  'xmajorgrids,\n' \
                  'x grid style={lightgray!92.026143790849673!black},\n' \
                  'ymajorgrids,\n' \
                  'y grid style={lightgray!92.026143790849673!black},\n' \
                  'line width=0.75mm,\n' \
                  'legend style={draw=white!80.0!black,font=\\fontsize{16}{12}\\selectfont},\n' \
                  'legend entries=' + legendEntries + ',\n' \
                  'legend cell align={left}\n'
    writeLatexMultiplePlots(outdir,prefix,join(outdir,prefix,'latex'),prefix + '_JKsoverGTOT',data,axisoptions,dataoptions)
    ymin = np.amin(JKsoverJ[:,1:])-np.abs(0.1*np.amin(JKsoverJ[:,1:]))
    ymax = np.amax(JKsoverJ[:,1:])+np.abs(0.1*np.amax(JKsoverJ[:,1:]))
    legendEntries = '{'
    dataoptions = []
    data = []
    for c in range(0,nContour):
        if c>0:
            legendEntries += ','
        legendEntries += '{Contour ' + str(c+1) + '}'
        dataoptions.append('green!' + str(float(100.*c/nContour)) + '!black,smooth,mark=*')
        data.append(np.transpose(np.array([theta,JKsoverJ[:,c]])))
    legendEntries += '}'   
    axisoptions = '\n ' \
                  'width=30cm,\n' \
                  'title={$\\frac{J_{Ks}}{J}$ vs debond angle  $\\theta$},\n' \
                  'xlabel={$\\theta\\left[^{\\circ}\\right]$},ylabel={$\\frac{J_{Ks}}{J}\\left[-\\right]$},\n' \
                  'xmin=' + str(xmin) + ',\n' \
                  'xmax=' + str(xmax) + ',\n' \
                  'ymin=' + str(ymin) + ',\n' \
                  'ymax=' + str(ymax) + ',\n' \
                  'title style={font=\\fontsize{16}{8}\\selectfont},\n' \
                  'xlabel style={at={(axis description cs:0.5,-0.02)},anchor=north,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'ylabel style={at={(axis description cs:-0.01,.5)},anchor=south,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'tick align=outside,\n' \
                  'tick label style={font=\\normalsize},\n' \
                  'xtick=' + xlabels + ',\n' \
                  'xmajorgrids,\n' \
                  'x grid style={lightgray!92.026143790849673!black},\n' \
                  'ymajorgrids,\n' \
                  'y grid style={lightgray!92.026143790849673!black},\n' \
                  'line width=0.75mm,\n' \
                  'legend style={draw=white!80.0!black,font=\\fontsize{16}{12}\\selectfont},\n' \
                  'legend entries=' + legendEntries + ',\n' \
                  'legend cell align={left}\n'
    writeLatexMultiplePlots(outdir,prefix,join(outdir,prefix,'latex'),prefix + '_JKsoverJ',data,axisoptions,dataoptions)
    theta = []
    GIoverG0 = []
    GIIoverG0 = []
    GTOToverG0 = []
    JoverG0 = []
    JKsoverG0 = []
    with open(join(outdir,prefix + '_GandJoverG0' + '.csv'),'r') as csv:
        lines = csv.readlines()
    for line in lines[2:]:
        if float(line.replace('\n','').split(',')[0])>=0.0:
            theta.append(float(line.replace('\n','').split(',')[0]))
            GIoverG0.append(float(line.replace('\n','').split(',')[1]))
            GIIoverG0.append(float(line.replace('\n','').split(',')[2]))
            GTOToverG0.append(float(line.replace('\n','').split(',')[3]))
            offset = 3
            temp = []
            for c in range(1,nContour+1):
                index = offset + c
                temp.append(float(line.replace('\n','').split(',')[index]))
            JoverG0.append(temp)
            offset = index
            temp = []
            for c in range(1,nContour+1):
                index = offset + c
                temp.append(float(line.replace('\n','').split(',')[index]))
            JKsoverG0.append(temp)
    theta = np.array(theta)
    GIoverG0 = np.array(GIoverG0)
    GIIoverG0 = np.array(GIIoverG0)
    GTOToverG0 = np.array(GTOToverG0)
    JoverG0 = np.array(JoverG0)
    JKsoverG0 = np.array(JKsoverG0)
    xmin = 0.
    xmax = 180.
    xlabels = '{'
    for j,element in enumerate(np.linspace(xmin,xmax,19,endpoint=True)):
        if j>0:
            xlabels += ','
        xlabels += str(element)
    xlabels += '}'
    ymin = np.amin(GTOToverG0)-np.abs(0.1*np.amin(GTOToverG0))
    ymax = np.amax(GTOToverG0)+np.abs(0.1*np.amax(GTOToverG0))
    axisoptions = '\n ' \
                  'width=30cm,\n' \
                  'title={$\\frac{G_{\\left(\\cdot\\cdot\\right)}}{G_{0}}$ vs debond angle  $\\theta$},\n' \
                  'xlabel={$\\theta\\left[^{\\circ}\\right]$},ylabel={$\\frac{G_{\\left(\\cdot\\cdot\\right)}}{g_{0}}\\left[-\\right]$},\n' \
                  'xmin=' + str(xmin) + ',\n' \
                  'xmax=' + str(xmax) + ',\n' \
                  'ymin=' + str(ymin) + ',\n' \
                  'ymax=' + str(ymax) + ',\n' \
                  'title style={font=\\fontsize{16}{8}\\selectfont},\n' \
                  'xlabel style={at={(axis description cs:0.5,-0.02)},anchor=north,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'ylabel style={at={(axis description cs:-0.01,.5)},anchor=south,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'tick align=outside,\n' \
                  'tick label style={font=\\normalsize},\n' \
                  'xtick=' + xlabels + ',\n' \
                  'xmajorgrids,\n' \
                  'x grid style={lightgray!92.026143790849673!black},\n' \
                  'ymajorgrids,\n' \
                  'y grid style={lightgray!92.026143790849673!black},\n' \
                  'line width=0.75mm,\n' \
                  'legend style={draw=white!80.0!black,font=\\fontsize{16}{12}\\selectfont},\n' \
                  'legend entries={{$\\frac{G_{I}}{G_{0}}$},{$\\frac{G_{II}}{G_{0}}$},{$\\frac{G_{I}+G_{II}}{G_{0}}$}},\n' \
                  'legend cell align={left}\n'
    dataoptions = ['blue,smooth,mark=*','green!50.196078431372548!black,smooth,mark=*','red,smooth,mark=*']
    data = [np.transpose(np.array([theta,GIoverG0])),np.transpose(np.array([theta,GIIoverG0])),np.transpose(np.array([theta,GTOToverG0]))]
    writeLatexMultiplePlots(outdir,prefix,join(outdir,prefix,'latex'),prefix + '_GsoverG0',data,axisoptions,dataoptions)
    ymin = np.amin([np.amin(bemGTOToverG0),np.amin(GTOToverG0)])-np.abs(0.1*np.amin([np.amin(bemGTOToverG0),np.amin(GTOToverG0)]))
    ymax = np.amax([np.amax(bemGTOToverG0),np.amax(GTOToverG0)])+np.abs(0.1*np.amax([np.amax(bemGTOToverG0),np.amax(GTOToverG0)]))
    axisoptions = '\n ' \
                  'width=30cm,\n' \
                  'title={$\\frac{G_{\\left(\\cdot\\cdot\\right)}}{G_{0}}$ vs debond angle  $\\theta$},\n' \
                  'xlabel={$\\theta\\left[^{\\circ}\\right]$},ylabel={$\\frac{G_{\\left(\\cdot\\cdot\\right)}}{g_{0}}\\left[-\\right]$},\n' \
                  'xmin=' + str(xmin) + ',\n' \
                  'xmax=' + str(xmax) + ',\n' \
                  'ymin=' + str(ymin) + ',\n' \
                  'ymax=' + str(ymax) + ',\n' \
                  'title style={font=\\fontsize{16}{8}\\selectfont},\n' \
                  'xlabel style={at={(axis description cs:0.5,-0.02)},anchor=north,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'ylabel style={at={(axis description cs:-0.01,.5)},anchor=south,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'tick align=outside,\n' \
                  'tick label style={font=\\normalsize},\n' \
                  'xtick=' + xlabels + ',\n' \
                  'xmajorgrids,\n' \
                  'x grid style={lightgray!92.026143790849673!black},\n' \
                  'ymajorgrids,\n' \
                  'y grid style={lightgray!92.026143790849673!black},\n' \
                  'line width=0.75mm,\n' \
                  'legend style={draw=white!80.0!black,font=\\fontsize{16}{12}\\selectfont},\n' \
                  'legend entries={{$\\frac{G_{I}}{G_{0}}-FEM$},{$\\frac{G_{II}}{G_{0}}-FEM$},{$\\frac{G_{I}+G_{II}}{G_{0}}-FEM$},{$\\frac{G_{I}}{G_{0}}-BEM$},{$\\frac{G_{II}}{G_{0}}-BEM$},{$\\frac{G_{I}+G_{II}}{G_{0}}-BEM$}},\n' \
                  'legend cell align={left}\n'
    dataoptions = ['red,smooth,mark=*','red,smooth,mark=triangle*','red,smooth,mark=square*','blue,smooth,mark=*','blue,smooth,mark=triangle*','blue,smooth,mark=square*']
    data = [np.transpose(np.array([theta,GIoverG0])),np.transpose(np.array([theta,GIIoverG0])),np.transpose(np.array([theta,GTOToverG0])),np.transpose(np.array([bemTheta,bemGIoverG0])),np.transpose(np.array([bemTheta,bemGIIoverG0])),np.transpose(np.array([bemTheta,bemGTOToverG0]))]
    writeLatexMultiplePlots(outdir,prefix,join(outdir,prefix,'latex'),prefix + '_GsoverG0_FEM-BEM-comparison',data,axisoptions,dataoptions)
    ymin = np.around(np.amin(JoverG0[:,1:])-np.abs(0.1*np.amin(JoverG0[:,1:])),decimals=2)
    ymax = np.around(np.amax(JoverG0[:,1:])+np.abs(0.1*np.amax(JoverG0[:,1:])),decimals=2)
    legendEntries = '{'
    dataoptions = []
    data = []
    for c in range(0,nContour):
        if c>0:
            legendEntries += ','
        legendEntries += '{Contour ' + str(c+1) + '}'
        dataoptions.append('green!' + str(float(100.*c/nContour)) + '!black,smooth,mark=*')
        data.append(np.transpose(np.array([theta,JoverG0[:,c]])))
    legendEntries += '}'   
    axisoptions = '\n ' \
                  'width=30cm,\n' \
                  'title={$\\frac{J}{G_{0}}$ vs debond angle  $\\theta$},\n' \
                  'xlabel={$\\theta\\left[^{\\circ}\\right]$},ylabel={$\\frac{J}{G_{0}}\\left[-\\right]$},\n' \
                  'xmin=' + str(xmin) + ',\n' \
                  'xmax=' + str(xmax) + ',\n' \
                  'ymin=' + str(ymin) + ',\n' \
                  'ymax=' + str(ymax) + ',\n' \
                  'title style={font=\\fontsize{16}{8}\\selectfont},\n' \
                  'xlabel style={at={(axis description cs:0.5,-0.02)},anchor=north,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'ylabel style={at={(axis description cs:-0.01,.5)},anchor=south,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'tick align=outside,\n' \
                  'tick label style={font=\\normalsize},\n' \
                  'xtick=' + xlabels + ',\n' \
                  'xmajorgrids,\n' \
                  'x grid style={lightgray!92.026143790849673!black},\n' \
                  'ymajorgrids,\n' \
                  'y grid style={lightgray!92.026143790849673!black},\n' \
                  'line width=0.75mm,\n' \
                  'legend style={draw=white!80.0!black,font=\\fontsize{16}{12}\\selectfont},\n' \
                  'legend entries=' + legendEntries + ',\n' \
                  'legend cell align={left}\n'
    writeLatexMultiplePlots(outdir,prefix,join(outdir,prefix,'latex'),prefix + '_JsoverG0',data,axisoptions,dataoptions)
    ymin = np.amin([np.amin(bemGTOToverG0),np.amin(JoverG0[:,1:])])-np.abs(0.1*np.amin([np.amin(bemGTOToverG0),np.amin(JoverG0[:,1:])]))
    ymax = np.amax([np.amax(bemGTOToverG0),np.amax(JoverG0[:,1:])])+np.abs(0.1*np.amax([np.amax(bemGTOToverG0),np.amax(JoverG0[:,1:])]))
    legendEntries = '{'
    dataoptions = []
    data = []
    for c in range(0,nContour):
        if c>0:
            legendEntries += ','
        legendEntries += '{Contour ' + str(c+1) + '}'
        dataoptions.append('green!' + str(25+float(75.*c/nContour)) + '!blue,smooth,mark=*')
        data.append(np.transpose(np.array([theta,JoverG0[:,c]])))
    dataoptions.append('red,smooth,mark=square*')
    legendEntries += ',{$\\frac{G_{I}+G_{II}}{G_{0}}-BEM$}'
    legendEntries += '}'
    data.append(np.transpose(np.array([bemTheta,bemGTOToverG0])))
    axisoptions = '\n ' \
                  'width=30cm,\n' \
                  'title={Normalized energy release rate vs debond angle  $\\theta$},\n' \
                  'xlabel={$\\theta\\left[^{\\circ}\\right]$},ylabel={$\\frac{J}{G_{0}}\\left[-\\right]$},\n' \
                  'xmin=' + str(xmin) + ',\n' \
                  'xmax=' + str(xmax) + ',\n' \
                  'ymin=' + str(ymin) + ',\n' \
                  'ymax=' + str(ymax) + ',\n' \
                  'title style={font=\\fontsize{16}{8}\\selectfont},\n' \
                  'xlabel style={at={(axis description cs:0.5,-0.02)},anchor=north,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'ylabel style={at={(axis description cs:-0.01,.5)},anchor=south,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'tick align=outside,\n' \
                  'tick label style={font=\\normalsize},\n' \
                  'xtick=' + xlabels + ',\n' \
                  'xmajorgrids,\n' \
                  'x grid style={lightgray!92.026143790849673!black},\n' \
                  'ymajorgrids,\n' \
                  'y grid style={lightgray!92.026143790849673!black},\n' \
                  'line width=0.75mm,\n' \
                  'legend style={draw=white!80.0!black,font=\\fontsize{16}{12}\\selectfont},\n' \
                  'legend entries=' + legendEntries + ',\n' \
                  'legend cell align={left}\n'
    writeLatexMultiplePlots(outdir,prefix,join(outdir,prefix,'latex'),prefix + '_JsoverG0_FEM-BEM-comparison',data,axisoptions,dataoptions)
    ymin = np.amin(JKsoverG0[:,1:])-np.abs(0.1*np.amin(JKsoverG0[:,1:]))
    ymax = np.amax(JKsoverG0[:,1:])+np.abs(0.1*np.amax(JKsoverG0[:,1:]))
    legendEntries = '{'
    dataoptions = []
    data = []
    for c in range(0,nContour):
        if c>0:
            legendEntries += ','
        legendEntries += '{Contour ' + str(c+1) + '}'
        dataoptions.append('green!' + str(float(100.*c/nContour)) + '!black,smooth,mark=*')
        data.append(np.transpose(np.array([theta,JKsoverG0[:,c]])))
    legendEntries += '}'   
    axisoptions = '\n ' \
                  'width=30cm,\n' \
                  'title={$\\frac{J_{Ks}}{G_{0}}$ vs debond angle  $\\theta$},\n' \
                  'xlabel={$\\theta\\left[^{\\circ}\\right]$},ylabel={$\\frac{J_{Ks}}{G_{0}}\\left[-\\right]$},\n' \
                  'xmin=' + str(xmin) + ',\n' \
                  'xmax=' + str(xmax) + ',\n' \
                  'ymin=' + str(ymin) + ',\n' \
                  'ymax=' + str(ymax) + ',\n' \
                  'title style={font=\\fontsize{16}{8}\\selectfont},\n' \
                  'xlabel style={at={(axis description cs:0.5,-0.02)},anchor=north,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'ylabel style={at={(axis description cs:-0.01,.5)},anchor=south,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'tick align=outside,\n' \
                  'tick label style={font=\\normalsize},\n' \
                  'xtick=' + xlabels + ',\n' \
                  'xmajorgrids,\n' \
                  'x grid style={lightgray!92.026143790849673!black},\n' \
                  'ymajorgrids,\n' \
                  'y grid style={lightgray!92.026143790849673!black},\n' \
                  'line width=0.75mm,\n' \
                  'legend style={draw=white!80.0!black,font=\\fontsize{16}{12}\\selectfont},\n' \
                  'legend entries=' + legendEntries + ',\n' \
                  'legend cell align={left}\n'
    writeLatexMultiplePlots(outdir,prefix,join(outdir,prefix,'latex'),prefix + '_JKsoverG0',data,axisoptions,dataoptions)
    ymin = np.amin([np.amin(bemGTOToverG0),np.amin(JKsoverG0[:,1:])])-np.abs(0.1*np.amin([np.amin(bemGTOToverG0),np.amin(JKsoverG0[:,1:])]))
    ymax = np.amax([np.amax(bemGTOToverG0),np.amax(JKsoverG0[:,1:])])+np.abs(0.1*np.amax([np.amax(bemGTOToverG0),np.amax(JKsoverG0[:,1:])]))
    legendEntries = '{'
    dataoptions = []
    data = []
    for c in range(0,nContour):
        if c>0:
            legendEntries += ','
        legendEntries += '{Contour ' + str(c+1) + '}'
        dataoptions.append('green!' + str(25+float(75.*c/nContour)) + '!blue,smooth,mark=*')
        data.append(np.transpose(np.array([theta,JKsoverG0[:,c]])))
    dataoptions.append('red,smooth,mark=square*')
    legendEntries += ',{$\\frac{G_{I}+G_{II}}{G_{0}}-BEM$}'
    legendEntries += '}'
    data.append(np.transpose(np.array([bemTheta,bemGTOToverG0])))
    axisoptions = '\n ' \
                  'width=30cm,\n' \
                  'title={Normalized energy release rate vs debond angle  $\\theta$},\n' \
                  'xlabel={$\\theta\\left[^{\\circ}\\right]$},ylabel={$\\frac{J_{Ks}}{G_{0}}\\left[-\\right]$},\n' \
                  'xmin=' + str(xmin) + ',\n' \
                  'xmax=' + str(xmax) + ',\n' \
                  'ymin=' + str(ymin) + ',\n' \
                  'ymax=' + str(ymax) + ',\n' \
                  'title style={font=\\fontsize{16}{8}\\selectfont},\n' \
                  'xlabel style={at={(axis description cs:0.5,-0.02)},anchor=north,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'ylabel style={at={(axis description cs:-0.01,.5)},anchor=south,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'tick align=outside,\n' \
                  'tick label style={font=\\normalsize},\n' \
                  'xtick=' + xlabels + ',\n' \
                  'xmajorgrids,\n' \
                  'x grid style={lightgray!92.026143790849673!black},\n' \
                  'ymajorgrids,\n' \
                  'y grid style={lightgray!92.026143790849673!black},\n' \
                  'line width=0.75mm,\n' \
                  'legend style={draw=white!80.0!black,font=\\fontsize{16}{12}\\selectfont},\n' \
                  'legend entries=' + legendEntries + ',\n' \
                  'legend cell align={left}\n'
    writeLatexMultiplePlots(outdir,prefix,join(outdir,prefix,'latex'),prefix + '_JKsoverG0_FEM-BEM-comparison',data,axisoptions,dataoptions)
    theta = []
    Jconv = []
    JKsconv = []
    K1conv = []
    K2conv = []
    Tconv = []
    with open(join(outdir,prefix + '_JcalcConvergence' + '.csv'),'r') as csv:
        lines = csv.readlines()
    for line in lines[2:]:
        theta.append(float(line.replace('\n','').split(',')[0]))
        offset = 0
        temp = []
        for c in range(1,nContour):
            index = offset + c
            temp.append(float(line.replace('\n','').split(',')[index]))
        Jconv.append(temp)
        offset = index
        temp = []
        for c in range(1,nContour):
            index = offset + c
            temp.append(float(line.replace('\n','').split(',')[index]))
        JKsconv.append(temp)
        offset = index
        temp = []
        for c in range(1,nContour):
            index = offset + c
            temp.append(float(line.replace('\n','').split(',')[index]))
        K1conv.append(temp)
        offset = index
        temp = []
        for c in range(1,nContour):
            index = offset + c
            temp.append(float(line.replace('\n','').split(',')[index]))
        K2conv.append(temp)
        offset = index
        temp = []
        for c in range(1,nContour):
            index = offset + c
            temp.append(float(line.replace('\n','').split(',')[index]))
        Tconv.append(temp)
    theta = np.array(theta)
    Jconv = np.array(Jconv)
    JKsconv = np.array(JKsconv)
    K1conv = np.array(K1conv)
    K2conv = np.array(K2conv)
    Tconv = np.array(Tconv)
    xmin = -180.
    xmax = 180.
    xlabels = '{'
    for j,element in enumerate(np.linspace(xmin,xmax,37,endpoint=True)):
        if j>0:
            xlabels += ','
        xlabels += str(element)
    xlabels += '}'
    ymin = np.amin(Jconv[:,1:])-np.abs(0.1*np.amin(Jconv[:,1:]))
    ymax = np.amax(Jconv[:,1:])+np.abs(0.1*np.amax(Jconv[:,1:]))
    legendEntries = '{'
    dataoptions = []
    data = []
    for c in range(0,nContour-1):
        if c>0:
            legendEntries += ','
        legendEntries += '{Contour ' + str(c+1) + '}'
        dataoptions.append('green!' + str(float(100.*c/nContour)) + '!black,smooth,mark=*')
        data.append(np.transpose(np.array([theta,Jconv[:,c]])))
    legendEntries += '}'   
    axisoptions = '\n ' \
                  'width=30cm,\n' \
                  'title={$J\\left(c\\right)-J\\left(c-1\\right)$ vs debond angle  $\\theta$},\n' \
                  'xlabel={$\\theta\\left[^{\\circ}\\right]$},ylabel={$J\\left[\\frac{J}{m^{2}}\\right]$},\n' \
                  'xmin=' + str(xmin) + ',\n' \
                  'xmax=' + str(xmax) + ',\n' \
                  'ymin=' + str(ymin) + ',\n' \
                  'ymax=' + str(ymax) + ',\n' \
                  'title style={font=\\fontsize{16}{8}\\selectfont},\n' \
                  'xlabel style={at={(axis description cs:0.5,-0.02)},anchor=north,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'ylabel style={at={(axis description cs:-0.01,.5)},anchor=south,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'tick align=outside,\n' \
                  'tick label style={font=\\normalsize},\n' \
                  'xtick=' + xlabels + ',\n' \
                  'xmajorgrids,\n' \
                  'x grid style={lightgray!92.026143790849673!black},\n' \
                  'ymajorgrids,\n' \
                  'y grid style={lightgray!92.026143790849673!black},\n' \
                  'line width=0.75mm,\n' \
                  'legend style={draw=white!80.0!black,font=\\fontsize{16}{12}\\selectfont},\n' \
                  'legend entries=' + legendEntries + ',\n' \
                  'legend cell align={left}\n'
    writeLatexMultiplePlots(outdir,prefix,join(outdir,prefix,'latex'),prefix + '_Jconv',data,axisoptions,dataoptions)
    ymin = np.amin(JKsconv[:,1:])-np.abs(0.1*np.amin(JKsconv[:,1:]))
    ymax = np.amax(JKsconv[:,1:])+np.abs(0.1*np.amax(JKsconv[:,1:]))
    legendEntries = '{'
    dataoptions = []
    data = []
    for c in range(0,nContour-1):
        if c>0:
            legendEntries += ','
        legendEntries += '{Contour ' + str(c+1) + '}'
        dataoptions.append('green!' + str(float(100.*c/nContour)) + '!black,smooth,mark=*')
        data.append(np.transpose(np.array([theta,JKsconv[:,c]])))
    legendEntries += '}'   
    axisoptions = '\n ' \
                  'width=30cm,\n' \
                  'title={$J_{Ks}\\left(c\\right)-J_{Ks}\\left(c-1\\right)$ vs debond angle  $\\theta$},\n' \
                  'xlabel={$\\theta\\left[^{\\circ}\\right]$},ylabel={$J_{Ks}\\left[\\frac{J}{m^{2}}\\right]$},\n' \
                  'xmin=' + str(xmin) + ',\n' \
                  'xmax=' + str(xmax) + ',\n' \
                  'ymin=' + str(ymin) + ',\n' \
                  'ymax=' + str(ymax) + ',\n' \
                  'title style={font=\\fontsize{16}{8}\\selectfont},\n' \
                  'xlabel style={at={(axis description cs:0.5,-0.02)},anchor=north,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'ylabel style={at={(axis description cs:-0.01,.5)},anchor=south,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'tick align=outside,\n' \
                  'tick label style={font=\\normalsize},\n' \
                  'xtick=' + xlabels + ',\n' \
                  'xmajorgrids,\n' \
                  'x grid style={lightgray!92.026143790849673!black},\n' \
                  'ymajorgrids,\n' \
                  'y grid style={lightgray!92.026143790849673!black},\n' \
                  'line width=0.75mm,\n' \
                  'legend style={draw=white!80.0!black,font=\\fontsize{16}{12}\\selectfont},\n' \
                  'legend entries=' + legendEntries + ',\n' \
                  'legend cell align={left}\n'
    writeLatexMultiplePlots(outdir,prefix,join(outdir,prefix,'latex'),prefix + '_JKsconv',data,axisoptions,dataoptions)
    ymin = np.amin(K1conv[:,1:])-np.abs(0.1*np.amin(K1conv[:,1:]))
    ymax = np.amax(K1conv[:,1:])+np.abs(0.1*np.amax(K1conv[:,1:]))
    legendEntries = '{'
    dataoptions = []
    data = []
    for c in range(0,nContour-1):
        if c>0:
            legendEntries += ','
        legendEntries += '{Contour ' + str(c+1) + '}'
        dataoptions.append('green!' + str(float(100.*c/nContour)) + '!black,smooth,mark=*')
        data.append(np.transpose(np.array([theta,K1conv[:,c]])))
    legendEntries += '}'   
    axisoptions = '\n ' \
                  'width=30cm,\n' \
                  'title={$K_{1}\\left(c\\right)-K_{1}\\left(c-1\\right)$ vs debond angle  $\\theta$},\n' \
                  'xlabel={$\\theta\\left[^{\\circ}\\right]$},ylabel={$K_{1}\\left[MPa\\sqrt{\\mu m}\\right]$},\n' \
                  'xmin=' + str(xmin) + ',\n' \
                  'xmax=' + str(xmax) + ',\n' \
                  'ymin=' + str(ymin) + ',\n' \
                  'ymax=' + str(ymax) + ',\n' \
                  'title style={font=\\fontsize{16}{8}\\selectfont},\n' \
                  'xlabel style={at={(axis description cs:0.5,-0.02)},anchor=north,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'ylabel style={at={(axis description cs:-0.01,.5)},anchor=south,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'tick align=outside,\n' \
                  'tick label style={font=\\normalsize},\n' \
                  'xtick=' + xlabels + ',\n' \
                  'xmajorgrids,\n' \
                  'x grid style={lightgray!92.026143790849673!black},\n' \
                  'ymajorgrids,\n' \
                  'y grid style={lightgray!92.026143790849673!black},\n' \
                  'line width=0.75mm,\n' \
                  'legend style={draw=white!80.0!black,font=\\fontsize{16}{12}\\selectfont},\n' \
                  'legend entries=' + legendEntries + ',\n' \
                  'legend cell align={left}\n'
    writeLatexMultiplePlots(outdir,prefix,join(outdir,prefix,'latex'),prefix + '_K1conv',data,axisoptions,dataoptions)
    ymin = np.amin(K2conv[:,1:])-np.abs(0.1*np.amin(K2conv[:,1:]))
    ymax = np.amax(K2conv[:,1:])+np.abs(0.1*np.amax(K2conv[:,1:]))
    legendEntries = '{'
    dataoptions = []
    data = []
    for c in range(0,nContour-1):
        if c>0:
            legendEntries += ','
        legendEntries += '{Contour ' + str(c+1) + '}'
        dataoptions.append('green!' + str(float(100.*c/nContour)) + '!black,smooth,mark=*')
        data.append(np.transpose(np.array([theta,K2conv[:,c]])))
    legendEntries += '}'   
    axisoptions = '\n ' \
                  'width=30cm,\n' \
                  'title={$K_{2}\\left(c\\right)-K_{1}\\left(c-1\\right)$ vs debond angle  $\\theta$},\n' \
                  'xlabel={$\\theta\\left[^{\\circ}\\right]$},ylabel={$K_{2}\\left[MPa\\sqrt{\\mu m}\\right]$},\n' \
                  'xmin=' + str(xmin) + ',\n' \
                  'xmax=' + str(xmax) + ',\n' \
                  'ymin=' + str(ymin) + ',\n' \
                  'ymax=' + str(ymax) + ',\n' \
                  'title style={font=\\fontsize{16}{8}\\selectfont},\n' \
                  'xlabel style={at={(axis description cs:0.5,-0.02)},anchor=north,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'ylabel style={at={(axis description cs:-0.01,.5)},anchor=south,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'tick align=outside,\n' \
                  'tick label style={font=\\normalsize},\n' \
                  'xtick=' + xlabels + ',\n' \
                  'xmajorgrids,\n' \
                  'x grid style={lightgray!92.026143790849673!black},\n' \
                  'ymajorgrids,\n' \
                  'y grid style={lightgray!92.026143790849673!black},\n' \
                  'line width=0.75mm,\n' \
                  'legend style={draw=white!80.0!black,font=\\fontsize{16}{12}\\selectfont},\n' \
                  'legend entries=' + legendEntries + ',\n' \
                  'legend cell align={left}\n'
    writeLatexMultiplePlots(outdir,prefix,join(outdir,prefix,'latex'),prefix + '_K2conv',data,axisoptions,dataoptions)
    ymin = np.amin(Tconv[:,1:])-np.abs(0.1*np.amin(Tconv[:,1:]))
    ymax = np.amax(Tconv[:,1:])+np.abs(0.1*np.amax(Tconv[:,1:]))
    legendEntries = '{'
    dataoptions = []
    data = []
    for c in range(0,nContour-1):
        if c>0:
            legendEntries += ','
        legendEntries += '{Contour ' + str(c+1) + '}'
        dataoptions.append('green!' + str(float(100.*c/nContour)) + '!black,smooth,mark=*')
        data.append(np.transpose(np.array([theta,Tconv[:,c]])))
    legendEntries += '}'   
    axisoptions = '\n ' \
                  'width=30cm,\n' \
                  'title={$T\\left(c\\right)-T\\left(c-1\\right)$ vs debond angle  $\\theta$},\n' \
                  'xlabel={$\\theta\\left[^{\\circ}\\right]$},ylabel={$T\\left[-\\right]$},\n' \
                  'xmin=' + str(xmin) + ',\n' \
                  'xmax=' + str(xmax) + ',\n' \
                  'ymin=' + str(ymin) + ',\n' \
                  'ymax=' + str(ymax) + ',\n' \
                  'title style={font=\\fontsize{16}{8}\\selectfont},\n' \
                  'xlabel style={at={(axis description cs:0.5,-0.02)},anchor=north,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'ylabel style={at={(axis description cs:-0.01,.5)},anchor=south,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'tick align=outside,\n' \
                  'tick label style={font=\\normalsize},\n' \
                  'xtick=' + xlabels + ',\n' \
                  'xmajorgrids,\n' \
                  'x grid style={lightgray!92.026143790849673!black},\n' \
                  'ymajorgrids,\n' \
                  'y grid style={lightgray!92.026143790849673!black},\n' \
                  'line width=0.75mm,\n' \
                  'legend style={draw=white!80.0!black,font=\\fontsize{16}{12}\\selectfont},\n' \
                  'legend entries=' + legendEntries + ',\n' \
                  'legend cell align={left}\n'
    writeLatexMultiplePlots(outdir,prefix,join(outdir,prefix,'latex'),prefix + '_Tconv',data,axisoptions,dataoptions)
    theta = []
    K1 = []
    K2 = []
    T = []
    with open(join(outdir,prefix + '_KandT' + '.csv'),'r') as csv:
        lines = csv.readlines()
    for line in lines[2:]:
        theta.append(float(line.replace('\n','').split(',')[0]))
        offset = 0
        temp = []
        for c in range(1,nContour+1):
            index = offset + c
            temp.append(float(line.replace('\n','').split(',')[index]))
        K1.append(temp)
        offset = index
        temp = []
        for c in range(1,nContour+1):
            index = offset + c
            temp.append(float(line.replace('\n','').split(',')[index]))
        K2.append(temp)
        offset = index
        temp = []
        for c in range(1,nContour+1):
            index = offset + c
            temp.append(float(line.replace('\n','').split(',')[index]))
        T.append(temp)
    K1 = np.array(K1)
    K2 = np.array(K2)
    T = np.array(T)
    ymin = np.amin(K1[:,1:])-np.abs(0.1*np.amin(K1[:,1:]))
    ymax = np.amax(K1[:,1:])+np.abs(0.1*np.amax(K1[:,1:]))
    legendEntries = '{'
    dataoptions = []
    data = []
    for c in range(0,nContour):
        if c>0:
            legendEntries += ','
        legendEntries += '{Contour ' + str(c+1) + '}'
        dataoptions.append('green!' + str(float(100.*c/nContour)) + '!black,smooth,mark=*')
        data.append(np.transpose(np.array([theta,K1[:,c]])))
    legendEntries += '}'   
    axisoptions = '\n ' \
                  'width=30cm,\n' \
                  'title={$K_{1}$ vs debond angle  $\\theta$},\n' \
                  'xlabel={$\\theta\\left[^{\\circ}\\right]$},ylabel={$K_{1}\\left[MPa\\sqrt{\\mu m}\\right]$},\n' \
                  'xmin=' + str(xmin) + ',\n' \
                  'xmax=' + str(xmax) + ',\n' \
                  'ymin=' + str(ymin) + ',\n' \
                  'ymax=' + str(ymax) + ',\n' \
                  'title style={font=\\fontsize{16}{8}\\selectfont},\n' \
                  'xlabel style={at={(axis description cs:0.5,-0.02)},anchor=north,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'ylabel style={at={(axis description cs:-0.01,.5)},anchor=south,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'tick align=outside,\n' \
                  'tick label style={font=\\normalsize},\n' \
                  'xtick=' + xlabels + ',\n' \
                  'xmajorgrids,\n' \
                  'x grid style={lightgray!92.026143790849673!black},\n' \
                  'ymajorgrids,\n' \
                  'y grid style={lightgray!92.026143790849673!black},\n' \
                  'line width=0.75mm,\n' \
                  'legend style={draw=white!80.0!black,font=\\fontsize{16}{12}\\selectfont},\n' \
                  'legend entries=' + legendEntries + ',\n' \
                  'legend cell align={left}\n'
    writeLatexMultiplePlots(outdir,prefix,join(outdir,prefix,'latex'),prefix + '_K1',data,axisoptions,dataoptions)
    ymin = np.amin(K2[:,1:])-np.abs(0.1*np.amin(K2[:,1:]))
    ymax = np.amax(K2[:,1:])+np.abs(0.1*np.amax(K2[:,1:]))
    legendEntries = '{'
    dataoptions = []
    data = []
    for c in range(0,nContour):
        if c>0:
            legendEntries += ','
        legendEntries += '{Contour ' + str(c+1) + '}'
        dataoptions.append('green!' + str(float(100.*c/nContour)) + '!black,smooth,mark=*')
        data.append(np.transpose(np.array([theta,K2[:,c]])))
    legendEntries += '}'   
    axisoptions = '\n ' \
                  'width=30cm,\n' \
                  'title={$K_{2}$ vs debond angle  $\\theta$},\n' \
                  'xlabel={$\\theta\\left[^{\\circ}\\right]$},ylabel={$K_{2}\\left[MPa\\sqrt{\\mu m}\\right]$},\n' \
                  'xmin=' + str(xmin) + ',\n' \
                  'xmax=' + str(xmax) + ',\n' \
                  'ymin=' + str(ymin) + ',\n' \
                  'ymax=' + str(ymax) + ',\n' \
                  'title style={font=\\fontsize{16}{8}\\selectfont},\n' \
                  'xlabel style={at={(axis description cs:0.5,-0.02)},anchor=north,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'ylabel style={at={(axis description cs:-0.01,.5)},anchor=south,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'tick align=outside,\n' \
                  'tick label style={font=\\normalsize},\n' \
                  'xtick=' + xlabels + ',\n' \
                  'xmajorgrids,\n' \
                  'x grid style={lightgray!92.026143790849673!black},\n' \
                  'ymajorgrids,\n' \
                  'y grid style={lightgray!92.026143790849673!black},\n' \
                  'line width=0.75mm,\n' \
                  'legend style={draw=white!80.0!black,font=\\fontsize{16}{12}\\selectfont},\n' \
                  'legend entries=' + legendEntries + ',\n' \
                  'legend cell align={left}\n'
    writeLatexMultiplePlots(outdir,prefix,join(outdir,prefix,'latex'),prefix + '_K2',data,axisoptions,dataoptions)
    ymin = np.amin(T[:,1:])-np.abs(0.1*np.amin(T[:,1:]))
    ymax = np.amax(T[:,1:])+np.abs(0.1*np.amax(T[:,1:]))
    legendEntries = '{'
    dataoptions = []
    data = []
    for c in range(0,nContour):
        if c>0:
            legendEntries += ','
        legendEntries += '{Contour ' + str(c+1) + '}'
        dataoptions.append('green!' + str(float(100.*c/nContour)) + '!black,smooth,mark=*')
        data.append(np.transpose(np.array([theta,T[:,c]])))
    legendEntries += '}'   
    axisoptions = '\n ' \
                  'width=30cm,\n' \
                  'title={$T$ vs debond angle  $\\theta$},\n' \
                  'xlabel={$\\theta\\left[^{\\circ}\\right]$},ylabel={$T\\left[-\\right]$},\n' \
                  'xmin=' + str(xmin) + ',\n' \
                  'xmax=' + str(xmax) + ',\n' \
                  'ymin=' + str(ymin) + ',\n' \
                  'ymax=' + str(ymax) + ',\n' \
                  'title style={font=\\fontsize{16}{8}\\selectfont},\n' \
                  'xlabel style={at={(axis description cs:0.5,-0.02)},anchor=north,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'ylabel style={at={(axis description cs:-0.01,.5)},anchor=south,font=\\fontsize{16}{8}\\selectfont},\n' \
                  'tick align=outside,\n' \
                  'tick label style={font=\\normalsize},\n' \
                  'xtick=' + xlabels + ',\n' \
                  'xmajorgrids,\n' \
                  'x grid style={lightgray!92.026143790849673!black},\n' \
                  'ymajorgrids,\n' \
                  'y grid style={lightgray!92.026143790849673!black},\n' \
                  'line width=0.75mm,\n' \
                  'legend style={draw=white!80.0!black,font=\\fontsize{16}{12}\\selectfont},\n' \
                  'legend entries=' + legendEntries + ',\n' \
                  'legend cell align={left}\n'
    writeLatexMultiplePlots(outdir,prefix,join(outdir,prefix,'latex'),prefix + '_T',data,axisoptions,dataoptions)
    

        
    
def plotEnergyReleaseDataPerSim(wd,project,nContour):
    print('')
    print('Plotting data of project ' + project)
    print('')
    # define pdf output folder
    pdffolder = join(wd,project,'pdf')
    if not exists(pdffolder):
        makedirs(pdffolder)
    # define csv output folder
    csvfolder = join(wd,project,'csv')
    # define csv output folder
    datfolder = join(wd,project,'dat')
    '''
    filelist = [ f for f in listdir(pdffolder) if f.endswith(".pdf") ]
    for f in filelist:
        remove(join(pdffolder,f))
    '''
    crackTips = []
    lines = []
    try:
        with open(join(csvfolder,'ENRRTs-Summary.csv'),'r') as csv:
            lines = csv.readlines()
    except Exception,e:
        sys.exc_clear()
    for line in lines[1:]:
        crackTips.append(int(line.replace('\n','').split(',')[0]))
    for t,tip in enumerate(crackTips):
        theta = 0
        time = []
        GI = []
        GII = []
        GTOT = []
        GIoverGTOT = []
        GIIoverGTOT = []
        if nContour>-1:
            J = []
            JKs = []
            JoverGTOT = []
            JKsoverGTOT = []
            JKsoverJ = []
        with open(join(csvfolder,'CrackTip' + str(t+1) + '_GandJhistSummary' + '.csv'),'r') as csv:
            lines = csv.readlines()
        theta = float(lines[0].replace('\n','').split(',')[-1])
        for line in lines[3:]:
            values = line.replace('\n','').split(',')
            time.append(float(values[0]))
            GI.append(float(values[1]))
            GII.append(float(values[2]))
            GTOT.append(float(values[3]))
            GIoverGTOT.append(float(values[4]))
            GIIoverGTOT.append(float(values[5]))
            offset = 5
            temp = []
            for c in range(1,nContour+1):
                index = offset+c
                temp.append(float(values[index]))
            J.append(temp)
            offset = index
            temp = []
            for c in range(1,nContour+1):
                index = offset+c
                temp.append(float(values[index]))
            JKs.append(temp)
            offset = index
            temp = []
            for c in range(1,nContour+1):
                index = offset+c
                temp.append(float(values[index]))
            JoverGTOT.append(temp)
            offset = index
            temp = []
            for c in range(1,nContour+1):
                index = offset+c
                temp.append(float(values[index]))
            JKsoverGTOT.append(temp)
            offset = index
            temp = []
            for c in range(1,nContour+1):
                index = offset+c
                temp.append(float(values[index]))
            JKsoverJ.append(temp)
        time = np.array(time)
        GI = np.array(GI)
        GII = np.array(GII)
        GTOT = np.array(GTOT)
        GIoverGTOT = np.array(GIoverGTOT)
        GIIoverGTOT = np.array(GIIoverGTOT)
        J = np.array(J)
        JKs = np.array(JKs)
        JoverGTOT = np.array(JoverGTOT)
        JKsoverGTOT = np.array(JKsoverGTOT)
        JKsoverJ = np.array(JKsoverJ)
        # plot GI, GII, GTOT vs time
        plt.figure(1)
        gi, = plt.plot(time,GI,color='r',linestyle='-',marker='.',linewidth=1.)
        gii, = plt.plot(time,GII,color='b',linestyle='-',marker='.',linewidth=1.)
        gtot, = plt.plot(time,GTOT,color='k',linestyle='-',marker='.',linewidth=1.)
        plt.xlabel(r'step time $\left[-\right]$')
        plt.ylabel(r'Energy release rate $\left[\frac{J}{m^{2}}\right]$')
        plt.title(r'$G_{I}$, $G_{II}$ and $G_{TOT}$ vs step time for $\theta=' + str(np.round(theta,decimals=0)) + '^{\circ}$')
        plt.legend([gi, gii, gtot], [r'$G_{I}$',r'$G_{II}$',r'$G_{TOT}$'])
        plt.grid(True)
        plt.savefig(join(pdffolder,'CrackTip' + str(t+1) + '_ENRRTsvsSteptime' + '.pdf'), bbox_inches='tight')
        plt.close()
        # plot GI/GTOT, GII/GTOT vs time
        plt.figure(2)
        mode1, = plt.plot(time,GIoverGTOT,color='r',linestyle='-',marker='.',linewidth=1.)
        mode2, = plt.plot(time,GIIoverGTOT,color='b',linestyle='-',marker='.',linewidth=1.)
        plt.xlabel(r'step time $\left[-\right]$')
        plt.ylabel(r'Mode ratio $\left[-\right]$')
        plt.title(r'$\frac{G_{I}}{G_{I}+G_{II}}$ and $\frac{G_{II}}{G_{I}+G_{II}}$ vs step time for $\theta=' + str(np.round(theta,decimals=0)) + '^{\circ}$')
        plt.legend([mode1, mode2], ['Mode I', 'Mode II'])
        plt.grid(True)
        plt.savefig(join(pdffolder,'CrackTip' + str(t+1) + '_ModeratiovsSteptime' + '.pdf'), bbox_inches='tight')
        plt.close()
        # plot J vs time
        plt.figure(3)
        refs = []
        labels = []
        rgbrange = np.linspace(0,1,nContour,endpoint=True)
        for c in range(0,nContour):
            pi, = plt.plot(time,J[:,c],color=(0,1,rgbrange[c]),linestyle='-',marker='.',linewidth=1.)
            refs.append(pi)
            labels.append('Contour ' + str(c+1))
        plt.xlabel(r'step time $\left[-\right]$')
        plt.ylabel(r'$J \left[\frac{J}{m^{2}}\right]$')
        plt.title(r'$J$ vs step time for $\theta=' + str(np.round(theta,decimals=0)) + '^{\circ}$')
        plt.legend(refs, labels)
        plt.grid(True)
        plt.savefig(join(pdffolder,'CrackTip' + str(t+1) + '_JvsSteptime' + '.pdf'), bbox_inches='tight')
        plt.close()
        # plot JKs vs time
        plt.figure(4)
        refs = []
        labels = []
        rgbrange = np.linspace(0,1,nContour,endpoint=True)
        for c in range(0,nContour):
            pi, = plt.plot(time,JKs[:,c],color=(0,1,rgbrange[c]),linestyle='-',marker='.',linewidth=1.)
            refs.append(pi)
            labels.append('Contour ' + str(c+1))
        plt.xlabel(r'step time $\left[-\right]$')
        plt.ylabel(r'$J_{Ks} \left[\frac{J}{m^{2}}\right]$')
        plt.title(r'$J_{Ks}$ vs step time for $\theta=' + str(np.round(theta,decimals=0)) + '^{\circ}$')
        plt.legend(refs, labels)
        plt.grid(True)
        plt.savefig(join(pdffolder,'CrackTip' + str(t+1) + '_JKsvsSteptime' + '.pdf'), bbox_inches='tight')
        plt.close()
        # plot J, JKs vs time
        plt.figure(5)
        refs = []
        labels = []
        rgbrange = np.linspace(0,1,nContour,endpoint=True)
        for c in range(0,nContour):
            pi, = plt.plot(time,J[:,c],color=(rgbrange[c],1,0),linestyle='-',marker='.',linewidth=1.)
            refs.append(pi)
            labels.append('J, Contour ' + str(c+1))
        for c in range(0,nContour):
            pi, = plt.plot(time,JKs[:,c],color=(1,0,rgbrange[c]),linestyle='-',marker='.',linewidth=1.)
            refs.append(pi)
            labels.append(r'$J_{Ks}$'+', Contour ' + str(c+1))
        plt.xlabel(r'step time $\left[-\right]$')
        plt.ylabel(r'Energy release rate $\left[\frac{J}{m^{2}}\right]$')
        plt.title(r'$J$ and $J_{Ks}$ vs step time for $\theta=' + str(np.round(theta,decimals=0)) + '^{\circ}$')
        plt.legend(refs, labels)
        plt.grid(True)
        plt.savefig(join(pdffolder,'CrackTip' + str(t+1) + '_JJKsvsSteptime' + '.pdf'), bbox_inches='tight')
        plt.close()
        # plot J, JKs over GTOT vs time
        plt.figure(6)
        refs = []
        labels = []
        rgbrange = np.linspace(0,1,nContour,endpoint=True)
        for c in range(0,nContour):
            pi, = plt.plot(time,JoverGTOT[:,c],color=(rgbrange[c],1,0),linestyle='-',marker='.',linewidth=1.)
            refs.append(pi)
            labels.append(r'$\frac{J}{G_{TOT}}$' + ', Contour ' + str(c+1))
        for c in range(0,nContour):
            pi, = plt.plot(time,JKsoverGTOT[:,c],color=(1,0,rgbrange[c]),linestyle='-',marker='.',linewidth=1.)
            refs.append(pi)
            labels.append(r'$\frac{J_{Ks}}{G_{TOT}}$' + ', Contour ' + str(c+1))
        plt.xlabel(r'step time $\left[-\right]$')
        plt.ylabel('Energy release rates'''+r' ratio $\left[-\right]$')
        plt.title(r'$\frac{J}{G_{TOT}}$ and $\frac{J_{Ks}}{G_{TOT}}$ vs step time for $\theta=' + str(np.round(theta,decimals=0)) + '^{\circ}$')
        plt.legend(refs, labels)
        plt.grid(True)
        plt.savefig(join(pdffolder,'CrackTip' + str(t+1) + '_JsoverGTOTvsSteptime' + '.pdf'))
        plt.close()
        # plot JKs over J vs time
        plt.figure(7)
        refs = []
        labels = []
        rgbrange = np.linspace(0,1,nContour,endpoint=True)
        for c in range(0,nContour):
            pi, = plt.plot(time,JKsoverJ[:,c],color=(0,1,rgbrange[c]),linestyle='-',marker='.',linewidth=1.)
            refs.append(pi)
            labels.append('Contour ' + str(c+1))
        plt.xlabel(r'step time $\left[-\right]$')
        plt.ylabel('Energy release rates'''+r' ratio $\left[-\right]$')
        plt.title(r'$\frac{J_{Ks}}{J}$ vs step time for $\theta=' + str(np.round(theta,decimals=0)) + '^{\circ}$')
        plt.legend(refs, labels)
        plt.grid(True)
        plt.savefig(join(pdffolder,'CrackTip' + str(t+1) + '_JKsoverJvsSteptime' + '.pdf'), bbox_inches='tight')
        plt.close()
        with open(join(csvfolder,'CrackTip' + str(t+1) + '_GandJoverG0histSummary' + '.csv'),'r') as csv:
            lines = csv.readlines()
        theta = 0
        time = []
        GIoverG0 = []
        GIIoverG0 = []
        GTOToverG0 = []
        JoverG0 = []
        JKsoverG0 = []
        theta = float(lines[0].replace('\n','').split(',')[-1])
        for line in lines[3:]:
            values = line.replace('\n','').split(',')
            time.append(float(values[0]))
            GIoverG0.append(float(values[1]))
            GIIoverG0.append(float(values[2]))
            GTOToverG0.append(float(values[3]))
            offset = 3
            temp = []
            for c in range(1,nContour+1):
                index = offset+c
                temp.append(float(values[index]))
            JoverG0.append(temp)
            offset = index
            temp = []
            for c in range(1,nContour+1):
                index = offset+c
                temp.append(float(values[index]))
            JKsoverG0.append(temp)
        time = np.array(time)
        GIoverG0 = np.array(GIoverG0)
        GIIoverG0 = np.array(GIIoverG0)
        GTOToverG0 = np.array(GTOToverG0)
        JoverG0 = np.array(JoverG0)
        JKsoverG0 = np.array(JKsoverG0)
        # plot GI/G0, GII/G0 and GTOT/G0 vs time
        plt.figure(8)
        gi, = plt.plot(time,GIoverG0,color='r',linestyle='-',marker='.',linewidth=1.)
        gii, = plt.plot(time,GIIoverG0,color='b',linestyle='-',marker='.',linewidth=1.)
        gtot, = plt.plot(time,GTOToverG0,color='k',linestyle='-',marker='.',linewidth=1.)
        plt.xlabel(r'step time $\left[-\right]$')
        plt.ylabel('Energy release rate'''+r' ratio $\left[-\right]$')
        plt.title(r'$\frac{G_{I}}{G_{0}}$, $\frac{G_{II}}{G_{0}}$ and $\frac{G_{TOT}}{G_{0}}$ vs step time for $\theta=' + str(np.round(theta,decimals=0)) + '^{\circ}$')
        plt.legend([gi, gii, gtot], [r'$\frac{G_{I}}{G_{0}}$',r'$\frac{G_{II}}{G_{0}}$',r'$\frac{G_{TOT}}{G_{0}}$'])
        plt.grid(True)
        plt.savefig(join(pdffolder,'CrackTip' + str(t+1) + '_ENRRTsoverG0vsSteptime' + '.pdf'), bbox_inches='tight')
        plt.close()
        # plot J/G0 vs time
        plt.figure(9)
        refs = []
        labels = []
        rgbrange = np.linspace(0,1,nContour,endpoint=True)
        for c in range(0,nContour):
            pi, = plt.plot(time,JoverG0[:,c],color=(0,1,rgbrange[c]),linestyle='-',marker='.',linewidth=1.)
            refs.append(pi)
            labels.append('Contour ' + str(c+1))
        plt.xlabel(r'step time $\left[-\right]$')
        plt.ylabel('Energy release rate'''+r' ratio $\left[-\right]$')
        plt.title(r'$\frac{J}{G_{0}}$ vs step time for $\theta=' + str(np.round(theta,decimals=0)) + '^{\circ}$')
        plt.legend(refs, labels)
        plt.grid(True)
        plt.savefig(join(pdffolder,'CrackTip' + str(t+1) + '_JoverG0vsSteptime' + '.pdf'), bbox_inches='tight')
        plt.close()
        # plot JKs/G0 vs time
        plt.figure(10)
        refs = []
        labels = []
        rgbrange = np.linspace(0,1,nContour,endpoint=True)
        for c in range(0,nContour):
            pi, = plt.plot(time,JKsoverG0[:,c],color=(0,1,rgbrange[c]),linestyle='-',marker='.',linewidth=1.)
            refs.append(pi)
            labels.append('Contour ' + str(c+1))
        plt.xlabel(r'step time $\left[-\right]$')
        plt.ylabel('Energy release rate'''+r' ratio $\left[-\right]$')
        plt.title(r'$\frac{J_{Ks}}{G_{0}}$ vs step time for $\theta=' + str(np.round(theta,decimals=0)) + '^{\circ}$')
        plt.legend(refs, labels)
        plt.grid(True)
        plt.savefig(join(pdffolder,'CrackTip' + str(t+1) + '_JKsoverG0vsSteptime' + '.pdf'), bbox_inches='tight')
        plt.close()
        with open(join(csvfolder,'CrackTip' + str(t+1) + '_JcalcConvergenceHist' + '.csv'),'r') as csv:
            lines = csv.readlines()
        theta = 0
        time = []
        J = []
        JKs = []
        K1 = []
        K2 = []
        T = []
        theta = float(lines[0].replace('\n','').split(',')[-1])
        for line in lines[3:]:
            values = line.replace('\n','').split(',')
            time.append(float(values[0]))
            offset = 0
            temp = []
            for c in range(1,nContour):
                index = offset+c
                temp.append(float(values[index]))
            J.append(temp)
            offset = index
            temp = []
            for c in range(1,nContour):
                index = offset+c
                temp.append(float(values[index]))
            JKs.append(temp)
            offset = index
            temp = []
            for c in range(1,nContour):
                index = offset+c
                temp.append(float(values[index]))
            K1.append(temp)
            offset = index
            temp = []
            for c in range(1,nContour):
                index = offset+c
                temp.append(float(values[index]))
            K2.append(temp)
            offset = index
            temp = []
            for c in range(1,nContour):
                index = offset+c
                temp.append(float(values[index]))
            T.append(temp)
        time = np.array(time)
        J = np.array(J)
        JKs = np.array(JKs)
        K1 = np.array(K1)
        K2 = np.array(K2)
        T = np.array(T)
        # plot J diff vs time
        plt.figure(11)
        refs = []
        labels = []
        rgbrange = np.linspace(0,1,nContour,endpoint=True)
        for c in range(0,nContour-1):
            pi, = plt.plot(time,J[:,c],color=(0,1,rgbrange[c]),linestyle='-',marker='.',linewidth=1.)
            refs.append(pi)
            labels.append('Contour ' + str(c+2))
        plt.xlabel(r'step time $\left[-\right]$')
        plt.ylabel(r'Energy release rate $\left[\frac{J}{m^{2}}\right]$')
        plt.title(r'$J\left(contour\ k\right)-J\left(contour\ k-1\right)$ vs step time for $\theta=' + str(np.round(theta,decimals=0)) + '^{\circ}$')
        plt.legend(refs, labels)
        plt.grid(True)
        plt.savefig(join(pdffolder,'CrackTip' + str(t+1) + '_JdiffvsSteptime' + '.pdf'), bbox_inches='tight')
        plt.close()
        # plot JKs diff vs time
        plt.figure(12)
        refs = []
        labels = []
        rgbrange = np.linspace(0,1,nContour,endpoint=True)
        for c in range(0,nContour-1):
            pi, = plt.plot(time,JKs[:,c],color=(0,1,rgbrange[c]),linestyle='-',marker='.',linewidth=1.)
            refs.append(pi)
            labels.append('Contour ' + str(c+2))
        plt.xlabel(r'step time $\left[-\right]$')
        plt.ylabel(r'Energy release rate $\left[\frac{J}{m^{2}}\right]$')
        plt.title(r'$J_{Ks}\left(contour\ k\right)-J_{Ks}\left(contour\ k-1\right)$ vs step time for $\theta=' + str(np.round(theta,decimals=0)) + '^{\circ}$')
        plt.legend(refs, labels)
        plt.grid(True)
        plt.savefig(join(pdffolder,'CrackTip' + str(t+1) + '_JKsdiffvsSteptime' + '.pdf'), bbox_inches='tight')
        plt.close()
        # plot K1 diff vs time
        plt.figure(13)
        refs = []
        labels = []
        rgbrange = np.linspace(0,1,nContour,endpoint=True)
        for c in range(0,nContour-1):
            pi, = plt.plot(time,K1[:,c],color=(0,1,rgbrange[c]),linestyle='-',marker='.',linewidth=1.)
            refs.append(pi)
            labels.append('Contour ' + str(c+2))
        plt.xlabel(r'step time $\left[-\right]$')
        plt.ylabel(r'Stress intensity factor $\left[MPa\sqrt{\mu m}\right]$')
        plt.title(r'$K_{I}\left(contour\ k\right)-K_{I}\left(contour\ k-1\right)$ vs step time for $\theta=' + str(np.round(theta,decimals=0)) + '^{\circ}$')
        plt.legend(refs, labels)
        plt.grid(True)
        plt.savefig(join(pdffolder,'CrackTip' + str(t+1) + '_K1diffvsSteptime' + '.pdf'), bbox_inches='tight')
        plt.close()
        # plot K2 diff vs time
        plt.figure(14)
        refs = []
        labels = []
        rgbrange = np.linspace(0,1,nContour,endpoint=True)
        for c in range(0,nContour-1):
            pi, = plt.plot(time,K2[:,c],color=(0,1,rgbrange[c]),linestyle='-',marker='.',linewidth=1.)
            refs.append(pi)
            labels.append('Contour ' + str(c+2))
        plt.xlabel(r'step time $\left[-\right]$')
        plt.ylabel(r'Stress intensity factor $\left[MPa\sqrt{\mu m}\right]$')
        plt.title(r'$K_{II}\left(contour\ k\right)-K_{II}\left(contour\ k-1\right)$ vs step time for $\theta=' + str(np.round(theta,decimals=0)) + '^{\circ}$')
        plt.legend(refs, labels)
        plt.grid(True)
        plt.savefig(join(pdffolder,'CrackTip' + str(t+1) + '_K2diffvsSteptime' + '.pdf'), bbox_inches='tight')
        plt.close()
        # plot T diff vs time
        plt.figure(15)
        refs = []
        labels = []
        rgbrange = np.linspace(0,1,nContour,endpoint=True)
        for c in range(0,nContour-1):
            pi, = plt.plot(time,T[:,c],color=(0,1,rgbrange[c]),linestyle='-',marker='.',linewidth=1.)
            refs.append(pi)
            labels.append('Contour ' + str(c+2))
        plt.xlabel(r'step time $\left[-\right]$')
        plt.ylabel(r'T stress $\left[\frac{J}{m^{2}}\right]$')
        plt.title(r'$T\left(contour\ k\right)-T\left(contour\ k-1\right)$ vs step time for $\theta=' + str(np.round(theta,decimals=0)) + '^{\circ}$')
        plt.legend(refs, labels)
        plt.grid(True)
        plt.savefig(join(pdffolder,'CrackTip' + str(t+1) + '_TdiffvsSteptime' + '.pdf'), bbox_inches='tight')
        plt.close()
        with open(join(csvfolder,'CrackTip' + str(t+1) + '_KandThistSummary' + '.csv'),'r') as csv:
            lines = csv.readlines()
        theta = 0
        time = []
        K1 = []
        K2 = []
        T = []
        theta = float(lines[0].replace('\n','').split(',')[-1])
        for line in lines[3:]:
            values = line.replace('\n','').split(',')
            time.append(float(values[0]))
            offset = 0
            temp = []
            for c in range(1,nContour):
                index = offset+c
                temp.append(float(values[index]))
            K1.append(temp)
            offset = index
            temp = []
            for c in range(1,nContour):
                index = offset+c
                temp.append(float(values[index]))
            K2.append(temp)
            offset = index
            temp = []
            for c in range(1,nContour):
                index = offset+c
                temp.append(float(values[index]))
            T.append(temp)
        time = np.array(time)
        K1 = np.array(K1)
        K2 = np.array(K2)
        T = np.array(T)
        # plot K1 diff vs time
        plt.figure(13)
        refs = []
        labels = []
        rgbrange = np.linspace(0,1,nContour,endpoint=True)
        for c in range(0,nContour-1):
            pi, = plt.plot(time,K1[:,c],color=(0,1,rgbrange[c]),linestyle='-',marker='.',linewidth=1.)
            refs.append(pi)
            labels.append('Contour ' + str(c+1))
        plt.xlabel(r'step time $\left[-\right]$')
        plt.ylabel(r'Stress intensity factor $\left[MPa\sqrt{\mu m}\right]$')
        plt.title(r'$K_{I}$ vs step time for $\theta=' + str(np.round(theta,decimals=0)) + '^{\circ}$')
        plt.legend(refs, labels)
        plt.grid(True)
        plt.savefig(join(pdffolder,'CrackTip' + str(t+1) + '_K1vsSteptime' + '.pdf'), bbox_inches='tight')
        plt.close()
        # plot K2 diff vs time
        plt.figure(14)
        refs = []
        labels = []
        rgbrange = np.linspace(0,1,nContour,endpoint=True)
        for c in range(0,nContour-1):
            pi, = plt.plot(time,K2[:,c],color=(0,1,rgbrange[c]),linestyle='-',marker='.',linewidth=1.)
            refs.append(pi)
            labels.append('Contour ' + str(c+1))
        plt.xlabel(r'step time $\left[-\right]$')
        plt.ylabel(r'Stress intensity factor $\left[MPa\sqrt{\mu m}\right]$')
        plt.title(r'$K_{II}$ vs step time for $\theta=' + str(np.round(theta,decimals=0)) + '^{\circ}$')
        plt.legend(refs, labels)
        plt.grid(True)
        plt.savefig(join(pdffolder,'CrackTip' + str(t+1) + '_K2vsSteptime' + '.pdf'), bbox_inches='tight')
        plt.close()
        # plot T diff vs time
        plt.figure(15)
        refs = []
        labels = []
        rgbrange = np.linspace(0,1,nContour,endpoint=True)
        for c in range(0,nContour-1):
            pi, = plt.plot(time,T[:,c],color=(0,1,rgbrange[c]),linestyle='-',marker='.',linewidth=1.)
            refs.append(pi)
            labels.append('Contour ' + str(c+1))
        plt.xlabel(r'step time $\left[-\right]$')
        plt.ylabel(r'T stress $\left[\frac{J}{m^{2}}\right]$')
        plt.title(r'$T$ vs step time for $\theta=' + str(np.round(theta,decimals=0)) + '^{\circ}$')
        plt.legend(refs, labels)
        plt.grid(True)
        plt.savefig(join(pdffolder,'CrackTip' + str(t+1) + '_TvsSteptime' + '.pdf'), bbox_inches='tight')
        plt.close()

def main(argv):

    wd = 'D:/01_Luca/07_Data/03_FEM'
    matdatafolder = 'D:/OneDrive/01_Luca/07_DocMASE/07_Data/02_Material-Properties'
    
    statusfile = '2017-03-01_AbaqusParametricRun_2017-03-03_12-56-32.sta'
    
    outdir = 'D:/OneDrive/01_Luca/07_DocMASE/07_Data/03_FEM'
    prefix = '2017-03-03_AbqRunSummary'
    
    refdatadir = 'D:/OneDrive/01_Luca/07_DocMASE/07_Data/01_References/Verification-Data'
    refdatafile = 'BEM-data'
    
    plotEnergyReleaseDataOverSims(wd,statusfile,outdir,prefix,refdatadir,refdatafile,10)
    
            

if __name__ == "__main__":
    main(sys.argv[1:])