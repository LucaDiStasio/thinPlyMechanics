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

from os.path import isfile, join, exists
from os import makedirs,listdir
from datetime import datetime
from time import strftime
from platform import platform
import numpy as np
import visualization
import xyPlot
from odbAccess import *
from abaqusConstants import *
from odbMaterial import *
from odbSection import *
import re

def convertDatToCsv(wd,project,datfile,titleline):
    # define csv output folder
    csvfolder = join(wd,project,'csv')
    # define csv output folder
    datfolder = join(wd,project,'dat')
    datafile = join(datfolder,datfile)
    with open(datafile,'r') as dat:
        lines = dat.readlines()
    xy = []
    for line in lines:
        if len(line.replace('\n','').replace(' ',''))>0 and 'X' not in line:
            parts = line.replace('\n','').split(' ')
            temp = []
            for part in parts:
                if part!='':
                    temp.append(float(part))
            xy.append(temp)
    xy = np.array(xy)
    xy = xy[xy[:,0].argsort()]
    with open(join(csvfolder,datfile.split('.')[0]+'.csv'),'w') as csv:
        csv.write(titleline.replace('\n','') + '\n')
        for value in xy:
            line = ''
            for s,subvalue in enumerate(value):
                if s>0:
                    line += ','
                line += str(subvalue)
            csv.write(line + '\n')

def extractJintegralsFromODBoutputSet01(wd,project,nContour):
    print('Starting path extraction on project ' + project + '\n')
    # define database name
    odbname = project + '.odb'
    odbfullpath = join(wd,project,'abaqus',odbname)
    # define input file name
    inpname = project + '.inp'
    inpfullpath = join(wd,project,'abqinp',inpname)
    # define csv output folder
    csvfolder = join(wd,project,'csv')
    # define csv output folder
    datfolder = join(wd,project,'dat')
    print('...done.\n')
    #=======================================================================
    # read crack tips from csv
    #=======================================================================
    crackTips = []
    lines = []
    try:
        with open(join(csvfolder,'ENRRTs-Summary.csv'),'r') as csv:
            lines = csv.readlines()
    except Exception,e:
        sys.exc_clear()
    for line in lines[1:]:
        crackTips.append(int(line.replace('\n','').split(',')[0]))
    #=======================================================================
    # open database
    #=======================================================================
    odb = openOdb(path=odbfullpath)
    sessionOdb = session.openOdb(name=odbfullpath)
    session.viewports['Viewport: 1'].setValues(displayedObject=sessionOdb)
    for t,tip in enumerate(crackTips):
        for contourValue in range(1,nContour+1):
            if contourValue<10:
                contour = '0' + str(contourValue)
            else:
                contour = str(contourValue)
            try:
                J = xyPlot.XYDataFromHistory(odb=sessionOdb,
            outputVariableName='J-integral: J at INTERFACEATNODE-' + str(tip) + '_NODE-' + str(tip) + '_Contour_' + contour +' in ELSET  ALL ELEMENTS',steps=(odb.steps.keys()[-1], ), )
                session.writeXYReport(fileName=join(wd,project,'dat','CrackTip' + str(t+1) + '_J_Contour' + contour + '.dat'),xyData=J,appendMode=OFF)
                convertDatToCsv(wd,project,'CrackTip' + str(t+1) + '_J_Contour' + contour + '.dat','step time T,J')
            except Exception,e:
                sys.exc_clear()
            try:
                JKs = xyPlot.XYDataFromHistory(odb=sessionOdb,outputVariableName='J-integral estimated from Ks: JKs at INTERFACEATNODE-' + str(tip) + '_NODE-' + str(tip) + '_Contour_' + contour +' in ELSET  ALL ELEMENTS',steps=(odb.steps.keys()[-1], ), )
                session.writeXYReport(fileName=join(wd,project,'dat','CrackTip' + str(t+1) + '_JKs_Contour' + contour + '.dat'),xyData=JKs,appendMode=OFF)
                convertDatToCsv(wd,project,'CrackTip' + str(t+1) + '_JKs_Contour' + contour + '.dat','step time T,JKs')
            except Exception,e:
                sys.exc_clear()
            try:
                K1 = xyPlot.XYDataFromHistory(odb=sessionOdb,outputVariableName='Stress intensity factor K1: K1 at INTERFACEATNODE-' + str(tip) + '_NODE-' + str(tip) + '_Contour_' + contour +' in ELSET  ALL ELEMENTS',steps=(odb.steps.keys()[-1], ), )
                session.writeXYReport(fileName=join(wd,project,'dat','CrackTip' + str(t+1) + '_K1_Contour' + contour + '.dat'),xyData=K1,appendMode=OFF)
                convertDatToCsv(wd,project,'CrackTip' + str(t+1) + '_K1_Contour' + contour + '.dat','step time T,K1')
            except Exception,e:
                sys.exc_clear()
            try:
                K2 = xyPlot.XYDataFromHistory(odb=sessionOdb,outputVariableName='Stress intensity factor K2: K2 at INTERFACEATNODE-' + str(tip) + '_NODE-' + str(tip) + '_Contour_' + contour +' in ELSET  ALL ELEMENTS',steps=(odb.steps.keys()[-1], ), )
                session.writeXYReport(fileName=join(wd,project,'dat','CrackTip' + str(t+1) + '_K2_Contour' + contour + '.dat'),xyData=K2,appendMode=OFF)
                convertDatToCsv(wd,project,'CrackTip' + str(t+1) + '_K2_Contour' + contour + '.dat','step time T,K2')
            except Exception,e:
                sys.exc_clear()
            try:
                T = xyPlot.XYDataFromHistory(odb=sessionOdb,outputVariableName='T-stress: T at INTERFACEATNODE-' + str(tip) + '_NODE-' + str(tip) + '_Contour_' + contour +' in ELSET  ALL ELEMENTS',steps=(odb.steps.keys()[-1], ), )
                session.writeXYReport(fileName=join(wd,project,'dat','CrackTip' + str(t+1) + '_T_Contour' + contour + '.dat'),xyData=T,appendMode=OFF)
                convertDatToCsv(wd,project,'CrackTip' + str(t+1) + '_T_Contour' + contour + '.dat','step time T,T-stress')
            except Exception,e:
                sys.exc_clear()
    #=======================================================================
    # close database
    #=======================================================================
    print('\n')
    print('Close database...\n')
    odb.close()
    print('...done.\n')


def main(argv):

    wd = 'D:/01_Luca/07_Data/03_FEM'
    matdatafolder = 'D:/OneDrive/01_Luca/07_DocMASE/07_Data/02_Material-Properties'

    statusfile = '2017-03-01_AbaqusParametricRun_2017-03-03_12-56-32.sta'

    with open(join(wd,statusfile),'r') as sta:
        lines = sta.readlines()
    for i,line in enumerate(lines[1:]):
        words = line.split(',')
        project = words[0]
        if not exists(join(wd,project,'dat')):
            makedirs(join(wd,project,'dat'))
        extractJintegralsFromODBoutputSet01(wd,project,10)


if __name__ == "__main__":
    main(sys.argv[1:])
