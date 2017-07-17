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
from os.path import join

def main(argv):

    #matdatafolder = 'D:/OneDrive/01_Luca/07_DocMASE/07_Data/02_Material-Properties'
    
    #refdatafolder = 'D:/OneDrive/01_Luca/07_DocMASE/07_Data/01_References/Verification-Data'
    refdatafolder = 'C:/01_Backup-folder/OneDrive/01_Luca/07_DocMASE/07_Data/01_References/Verification-Data'
    refdatafilename = 'BEM-data.csv'
    
    #wd = 'D:/01_Luca/07_Data/03_FEM'
    #wd = 'H:/01_Luca/07_DocMASE/07_Data/03_FEM'
    #wd = 'D:/01_Luca/07_Data/03_FEM/StraightInterface/Full'
    #wd = 'H:/01_Luca/07_DocMASE/07_Data/03_FEM/CurvedInterface'
    wd = 'C:/01_Backup-folder/OneDrive/01_Luca/07_DocMASE/07_Data/03_FEM'
    
    #statusfile = '2017-06-23_AbaqusParametricRun_FiniteStrain.sta'
    #statusfile = '2017-06-23_AbaqusParametricRun_SmallStrain.sta'
    
    outdir = 'C:/01_Backup-folder/OneDrive/01_Luca/07_DocMASE/07_Data/03_FEM'

    ext = '.tex'
    
    prefix = '2017-07-10_AbqRunSummary_SmallStrain_M-F-VCCT'
    
    Gplots = ['GI','GII','GTOT']
    
    for plot in Gplots:
        with open(join(wd,prefix + '_' + plot + ext),'r') as plotFile:
            lines = plotFile.readlines()
        errorLines = []
        bemData = []
        isBemData = False
        for l,line in enumerate(lines):
            if '%' in line and 'BEM' in line:
                isBemData = True
                indexStart = l + 2
            elif isBemData and '};' in line:
                indexEnd = l
                break
        for line in lines[indexStart:indexEnd]:
            bemData.append([float(line.replace('\n','').split(' ')[0]),float(line.replace('\n','').split(' ')[1])])
        isLegendEntries = False
        isDataToAdd = False
        isDataTable = False
        isLineToComment = False
        dataLineCount = 0
        for line in lines:
            if 'title' in line and '=' in line and '{' in line and 'style' not in line:
                if 'GI' in plot:
                    errorLines.append('title={Error of of normalized energy release rate with respect to BEM results $\\Delta\\frac{G_{I}}{G_{0}}=\\frac{G_{I}}{G_{0}}|_{FEM}-\\frac{G_{I}}{G_{0}}|_{BEM}$ as function of crack angular semi-aperture  $\\Delta\\theta$, $VF_{f}=7.9\\cdot10^{-5}$, $\\frac{L}{R_{f}}\\sim 100$ calculated with in-house force-based VCCT post-processing routine},' + '\n')
                elif 'GII' in plot:
                    errorLines.append('title={Error of of normalized energy release rate with respect to BEM results $\\Delta\\frac{G_{II}}{G_{0}}=\\frac{G_{II}}{G_{0}}|_{FEM}-\\frac{G_{II}}{G_{0}}|_{BEM}$ as function of crack angular semi-aperture  $\\Delta\\theta$, $VF_{f}=7.9\\cdot10^{-5}$, $\\frac{L}{R_{f}}\\sim 100$ calculated with in-house force-based VCCT post-processing routine},' + '\n')
                elif 'GTOT' in plot:
                    errorLines.append('title={Error of of normalized energy release rate with respect to BEM results $\\Delta\\frac{G_{I}+G_{II}}{G_{0}}=\\frac{G_{I}+G_{II}}{G_{0}}|_{FEM}-\\frac{G_{I}+G_{II}}{G_{0}}|_{BEM}$ as function of crack angular semi-aperture  $\\Delta\\theta$, $VF_{f}=7.9\\cdot10^{-5}$, $\\frac{L}{R_{f}}\\sim 100$ calculated with in-house force-based VCCT post-processing routine},' + '\n')
            elif 'xlabel' in line and 'ylabel' in line:
                if 'GI' in plot:
                    errorLines.append('xlabel={$\\Delta\\theta\\left[^{\circ}\\right]$},ylabel={$\\Delta\\frac{G_{I}}{G_{0}}=\\frac{G_{I}}{G_{0}}|_{FEM}-\\frac{G_{I}}{G_{0}}|_{BEM}\\left[-\\right]$},' + '\n')
                elif 'GII' in plot:
                    errorLines.append('xlabel={$\\Delta\\theta\\left[^{\circ}\\right]$},ylabel={$\\Delta\\frac{G_{II}}{G_{0}}=\\frac{G_{II}}{G_{0}}|_{FEM}-\\frac{G_{II}}{G_{0}}|_{BEM}\\left[-\\right]$},' + '\n')
                elif 'GTOT' in plot:
                    errorLines.append('xlabel={$\\Delta\\theta\\left[^{\circ}\\right]$},ylabel={$\\Delta\\frac{G_{I}+G_{II}}{G_{0}}=\\frac{G_{I}+G_{II}}{G_{0}}|_{FEM}-\\frac{G_{I}+G_{II}}{G_{0}}|_{BEM}\\left[-\\right]$},' + '\n')
            elif 'ymin' in line or 'ymax' in line:
                errorLines.append('%' + line)
            elif 'legend' in line and 'entries' in line:
                isLegendEntries = True
                errorLines.append(line)
            elif isLegendEntries and 'BEM' in line:
                isLegendEntries = False
                errorLines.append('},' + '\n')
            elif 'addplot' in line and 'BEM' not in line:
                isDataToAdd = True
                errorLines.append(line)
            elif 'table' in line and isDataToAdd and not isLineToComment:
                isDataTable = True
                errorLines.append(line)
            elif isDataTable and not isLineToComment and '};' not in line:
                errorLines.append(line.replace('\n','').split(' ')[0] + ' ' + str(float(line.replace('\n','').split(' ')[1])-bemData[dataLineCount][1]) + '\n')
                dataLineCount += 1
            elif isDataTable and not isLineToComment and '};' in line:
                errorLines.append(line)
                dataLineCount = 0
                isDataToAdd = False
                isDataTable = False
            elif 'addplot' in line and 'BEM' in line:
                isDataToAdd = True
                isLineToComment = True
                errorLines.append('%' + line)
            elif 'table' in line and isDataToAdd and isLineToComment:
                isDataTable = True
                errorLines.append('%' + line)
            elif isDataTable and isLineToComment and '};' not in line:
                errorLines.append('%' + line)
            elif isDataTable and isLineToComment and '};' in line:
                errorLines.append('%' + line)
                dataLineCount = 0
                isDataToAdd = False
                isDataTable = False
                isLineToComment = False
            else:
                errorLines.append(line)
        with open(join(wd,prefix + '_' + plot + '_' + 'ERR' + ext),'w') as plotFile:
            for line in errorLines:
                plotFile.write(line)
            

if __name__ == "__main__":
    main(sys.argv[1:])
    