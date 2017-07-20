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
from os import makedirs,listdir
from datetime import datetime
from time import strftime
from platform import platform
import numpy as np
import re
from createLatexScatterPlots import *

def computeRefG0(wd,project,matdatafolder):
    # define input file folder
    inpfilefolder = join(wd,project,'abqinp')
    # define csv output folder
    csvfolder = join(wd,project,'csv')
    # define csv output folder
    datfolder = join(wd,project,'dat')
    with open(join(inpfilefolder,project + '.inp')) as inp:
        lines = inp.readlines()
    for l,line in enumerate(lines):
        if 'Fiber radius Rf' in line:
            Rf = float(line.replace('\n','').replace('-','').replace('*','').split(':')[1]);
        elif 'Applied Axial Strain' in line:
            epsxx = float(line.replace('\n','').replace('-','').replace('*','').split(':')[1])
        elif 'Matrix' in line:
            matrixType = line.replace('\n','').replace('-','').replace('*','').split(':')[1]
        elif 'length, SI' in line:
            lengthFactor = 1.0/float(line.replace('**','').replace('--','').replace('\n','').split(':')[1])
        elif 'energy release rate, SI' in line:
            enrrtFactor = 1.0/float(line.replace('**','').replace('--','').replace('\n','').split(':')[1])
        elif 'LICENSE' in line:
            break
    if 'Epoxy' in matrixType:
        matrix = 'EP'
    elif 'HDPE' in matrixType:
        matrix = 'HDPE'
    with open(join(matdatafolder,matrix + '.csv')) as mat:
        lines = mat.readlines()
    factors = lines[1].replace('\n','').split(',')
    elprops = lines[2].replace('\n','').split(',')
    Em = float(factors[1])*float(elprops[1])
    num = float(factors[4])*float(elprops[4])
    Gm = float(factors[3])*float(elprops[3])
    Rf *= lengthFactor
    with open(join(csvfolder,'calculatedG0' + '.csv'),'w') as csv:
        csv.write('G0: ' + str(np.pi*Rf*np.square(Em*epsxx/((1-num*num)))*(1+(3.0-4.0*num))/(8.0*Gm)) + '\n')
    return np.pi*Rf*np.square(Em*epsxx/((1-num*num)))*(1+(3.0-4.0*num))/(8.0*Gm)

def computeRefValuesSingleMaterialPlate(wd,project,matdatafolder):
    # define input file folder
    inpfilefolder = join(wd,project,'abqinp')
    # define csv output folder
    csvfolder = join(wd,project,'csv')
    # define csv output folder
    datfolder = join(wd,project,'dat')
    with open(join(inpfilefolder,project + '.inp')) as inp:
        lines = inp.readlines()
    for line in lines:
        if 'length, SI' in line:
            lengthFactor = 1.0/float(line.replace('**','').replace('--','').replace('\n','').split(':')[1])
        elif 'energy release rate, SI' in line:
            enrrtFactor = 1.0/float(line.replace('**','').replace('--','').replace('\n','').split(':')[1])
        elif 'Crack' and 'Length' in line:
            a = float(line.replace('**','').replace('--','').replace('\n','').split(':')[1])
        elif 'Crack' and 'Horizontal Aspect Ratio' in line:
            aOverW = float(line.replace('**','').replace('--','').replace('\n','').split(':')[1])
        elif 'Applied Axial Strain' in line:
            eps = float(line.replace('**','').replace('--','').replace('\n','').split(':')[1])
        elif 'Material' in line:
            material = str(line.replace('**','').replace('--','').replace('\n','').split(':')[1])
        elif 'LICENSE' in line:
            break
    if 'Epoxy' in material:
        mat = 'EP'
    elif 'HDPE' in material:
        mat = 'HDPE'
    elif 'Glass Fiber' in material:
        mat = 'GF'
    with open(join(matdatafolder,mat + '.csv')) as mat:
        lines = mat.readlines()
    factors = lines[1].replace('\n','').split(',')
    elprops = lines[2].replace('\n','').split(',')
    E = float(factors[1])*float(elprops[1])
    nu = float(factors[4])*float(elprops[4])
    G = float(factors[3])*float(elprops[3])
    Epeps = E/(1-nu*nu)
    sigma = Epeps*eps
    K1inf = sigma*np.sqrt(0.5*np.pi*a*lengthFactor)
    G1inf = K1inf*K1inf/Epeps
    K1overK1inf = np.power(1.0/np.cos(0.5*np.pi*aOverW),0.5)*(1-0.025*np.power(aOverW,2)+0.06*np.power(aOverW,4))
    G1overG1inf = (1.0/np.cos(0.5*np.pi*aOverW))*np.power(1-0.025*np.power(aOverW,2)+0.06*np.power(aOverW,4),2)
    K1 = K1inf*K1overK1inf
    G1 = G1inf*G1overG1inf
    dataToWrite = [E,nu,Epeps,eps,sigma,aOverW,K1inf,K1,K1overK1inf,G1inf,G1,G1overG1inf,0.0,0.0,1.0,0.0,0.0,1.0]
    with open(join(csvfolder,'theoreticalEstimates' + '.csv'),'w') as csv:
        csv.write('E, nu, E_plane-strain, eps, sigma, a/W, K1_inf, K1, K1/K1_inf, G1_inf, G1, G1/G1_inf, K2_inf, K2, K2/K2_inf, G2_inf, G2, G2/G2_inf' + '\n')
        line = ''
        for v,value in enumerate(dataToWrite):
            if v>0:
                line += ','
        line += str(value)
        csv.write(line + '\n')
    return enrrtFactor, E, nu, Epeps, eps, sigma, aOverW, K1, K1inf, G1, G1inf, 0.0, 0.0, 0.0, 0.0 # K2inf, G2inf

def joinEnergyReleaseDataPerSim(wd,project,matdatafolder,nContour):
    print('')
    print('Gathering data of project ' + project)
    print('')
    # define csv output folder
    csvfolder = join(wd,project,'csv')
    # define csv output folder
    datfolder = join(wd,project,'dat')
    crackTips = []
    lines = []
    try:
        with open(join(csvfolder,'ENRRTs-Summary.csv'),'r') as csv:
            lines = csv.readlines()
    except Exception,e:
        sys.exc_clear()
    for line in lines[1:]:
        crackTips.append(int(line.replace('\n','').split(',')[0]))
    G0 = computeRefG0(wd,project,matdatafolder)
    for t,tip in enumerate(crackTips):
        theta = 0
        time = []
        GI = []
        GII = []
        GTOT = []
        GIratio = []
        GIIratio = []
        GIoverG0 = []
        GIIoverG0 = []
        GTOToverG0 = []
        toWrite1 = []
        toWrite2 = []
        toWrite3 = []
        toWrite4 = []
        with open(join(csvfolder,'ENRRTs-AtCrackTip' + str(t+1) + '.csv'),'r') as csv:
            lines = csv.readlines()
        theta = np.round(float(lines[1].replace('\n','').split(',')[-1]),decimals=2)
        for line in lines[3:]:
            gi = 0
            gii = 0
            time.append(float(line.replace('\n','').split(',')[0]))
            gi = float(line.replace('\n','').split(',')[1])
            gii = float(line.replace('\n','').split(',')[2])
            GI.append(gi)
            GII.append(gii)
            GTOT.append(gi+gii)
            if (gi+gii)!=0:
                GIratio.append(gi/(gi+gii))
                GIIratio.append(gii/(gi+gii))
            else:
                GIratio.append(0.)
                GIIratio.append(0.)
            GIoverG0.append(gi/G0)
            GIIoverG0.append(gii/G0)
            GTOToverG0.append((gi+gii)/G0)
        toWrite1.append(time)
        toWrite1.append(GI)
        toWrite1.append(GII)
        toWrite1.append(GTOT)
        toWrite1.append(GIratio)
        toWrite1.append(GIIratio)
        toWrite2.append(time)
        toWrite2.append(GIoverG0)
        toWrite2.append(GIIoverG0)
        toWrite2.append(GTOToverG0)
        toWrite3.append(time)
        toWrite4.append(time)
        for contourValue in range(1,nContour+1):
            if contourValue<10:
                contour = '0' + str(contourValue)
            else:
                contour = str(contourValue)
            with open(join(csvfolder,'CrackTip' + str(t+1) + '_J_Contour' + contour + '.csv'),'r') as csv:
                lines = csv.readlines()
            temp = []
            temp3 = []
            if float(lines[1].replace('\n','').split(',')[0]) > 0:
                temp.append(0.)
                temp3.append(0.)
            for line in lines[1:]:
                temp.append(np.abs(float(line.replace('\n','').split(',')[-1])))
                temp3.append(np.abs(float(line.replace('\n','').split(',')[-1]))/G0)
            toWrite1.append(temp)#J
            toWrite2.append(temp3)#JoverG0
            temp2 = []
            if contourValue>1:
                for v,value in enumerate(temp):
                    temp2.append(value-toWrite1[-1][v])
                toWrite3.append(temp2)#JdiffOverContour
            with open(join(csvfolder,'CrackTip' + str(t+1) + '_K1_Contour' + contour + '.csv'),'r') as csv:
                lines = csv.readlines()
            temp = []
            if float(lines[1].replace('\n','').split(',')[0]) > 0:
                temp.append(0.)
            for line in lines[1:]:
                temp.append(float(line.replace('\n','').split(',')[-1]))
            toWrite4.append(temp) #K1
        for contourValue in range(1,nContour+1):
            if contourValue<10:
                contour = '0' + str(contourValue)
            else:
                contour = str(contourValue)
            with open(join(csvfolder,'CrackTip' + str(t+1) + '_JKs_Contour' + contour + '.csv'),'r') as csv:
                lines = csv.readlines()
            temp = []
            temp3 = []
            if float(lines[1].replace('\n','').split(',')[0]) > 0:
                temp.append(0.)
                temp3.append(0.)
            for line in lines[1:]:
                temp.append(float(line.replace('\n','').split(',')[-1]))
                temp3.append(float(line.replace('\n','').split(',')[-1])/G0)
            toWrite1.append(temp) #JKs
            toWrite2.append(temp3) #JKsoverG0
            temp2 = []
            if contourValue>1:
                for v,value in enumerate(temp):
                    temp2.append(value-toWrite1[-1][v])
                toWrite3.append(temp2) #JKsdiffOverContour
            with open(join(csvfolder,'CrackTip' + str(t+1) + '_K2_Contour' + contour + '.csv'),'r') as csv:
                lines = csv.readlines()
            temp = []
            if float(lines[1].replace('\n','').split(',')[0]) > 0:
                temp.append(0.)
            for line in lines[1:]:
                temp.append(float(line.replace('\n','').split(',')[-1]))
            toWrite4.append(temp) #K2    
        for contourValue in range(1,nContour+1):
            if contourValue<10:
                contour = '0' + str(contourValue)
            else:
                contour = str(contourValue)
            with open(join(csvfolder,'CrackTip' + str(t+1) + '_J_Contour' + contour + '.csv'),'r') as csv:
                lines = csv.readlines()
            temp = []
            if float(lines[1].replace('\n','').split(',')[0]) > 0:
                temp.append(0.)
            for line in lines[1:]:
                temp.append(float(line.replace('\n','').split(',')[-1]))
            temp2 = []
            for v,value in enumerate(temp):
                if GTOT[v]!=0:
                    temp2.append(np.abs(value)/GTOT[v])
                else:
                    temp2.append(0.)
            toWrite1.append(temp2) #JrelativeToGTOT
            with open(join(csvfolder,'CrackTip' + str(t+1) + '_T_Contour' + contour + '.csv'),'r') as csv:
                lines = csv.readlines()
            temp = []
            if float(lines[1].replace('\n','').split(',')[0]) > 0:
                temp.append(0.)
            for line in lines[1:]:
                temp.append(float(line.replace('\n','').split(',')[-1]))
            toWrite4.append(temp) #T
            if contourValue>1:
                if (contourValue-1)<10:
                    prevcontour = '0' + str(contourValue-1)
                else:
                    prevcontour = str(contourValue-1)
                with open(join(csvfolder,'CrackTip' + str(t+1) + '_K1_Contour' + contour + '.csv'),'r') as csv:
                    lines = csv.readlines()
                temp = []
                if float(lines[1].replace('\n','').split(',')[0]) > 0:
                    temp.append(0.)
                for line in lines[1:]:
                    temp.append(float(line.replace('\n','').split(',')[-1]))
                with open(join(csvfolder,'CrackTip' + str(t+1) + '_K1_Contour' + prevcontour + '.csv'),'r') as csv:
                    lines = csv.readlines()
                temp2 = []
                if float(lines[1].replace('\n','').split(',')[0]) > 0:
                    temp2.append(0.)
                for line in lines[1:]:
                    temp2.append(float(line.replace('\n','').split(',')[-1]))
                temp3 = []
                for v,value in enumerate(temp):
                    temp3.append(value-temp2[v])
                toWrite3.append(temp3) #K1diffOverContour    
        for contourValue in range(1,nContour+1):
            if contourValue<10:
                contour = '0' + str(contourValue)
            else:
                contour = str(contourValue)
            with open(join(csvfolder,'CrackTip' + str(t+1) + '_JKs_Contour' + contour + '.csv'),'r') as csv:
                lines = csv.readlines()
            temp = []
            if float(lines[1].replace('\n','').split(',')[0]) > 0:
                temp.append(0.)
            for line in lines[1:]:
                temp.append(float(line.replace('\n','').split(',')[-1]))
            temp2 = []
            for v,value in enumerate(temp):
                if GTOT[v]!=0:
                    temp2.append(value/GTOT[v])
                else:
                    temp2.append(0.)
            toWrite1.append(temp2) #JKsrelativeToGTOT
            if contourValue>1:
                if (contourValue-1)<10:
                    prevcontour = '0' + str(contourValue-1)
                else:
                    prevcontour = str(contourValue-1)
                with open(join(csvfolder,'CrackTip' + str(t+1) + '_K2_Contour' + contour + '.csv'),'r') as csv:
                    lines = csv.readlines()
                temp = []
                if float(lines[1].replace('\n','').split(',')[0]) > 0:
                    temp.append(0.)
                for line in lines[1:]:
                    temp.append(float(line.replace('\n','').split(',')[-1]))
                with open(join(csvfolder,'CrackTip' + str(t+1) + '_K2_Contour' + prevcontour + '.csv'),'r') as csv:
                    lines = csv.readlines()
                temp2 = []
                if float(lines[1].replace('\n','').split(',')[0]) > 0:
                    temp2.append(0.)
                for line in lines[1:]:
                    temp2.append(float(line.replace('\n','').split(',')[-1]))
                temp3 = []
                for v,value in enumerate(temp):
                    temp3.append(value-temp2[v])
                toWrite3.append(temp3) #K2diffOverContour
        for contourValue in range(1,nContour+1):
            if contourValue<10:
                contour = '0' + str(contourValue)
            else:
                contour = str(contourValue)
            with open(join(csvfolder,'CrackTip' + str(t+1) + '_J_Contour' + contour + '.csv'),'r') as csv:
                lines = csv.readlines()
            temp = []
            if float(lines[1].replace('\n','').split(',')[0]) > 0:
                temp.append(0.)
            for line in lines[1:]:
                temp.append(float(line.replace('\n','').split(',')[-1]))
            with open(join(csvfolder,'CrackTip' + str(t+1) + '_JKs_Contour' + contour + '.csv'),'r') as csv:
                lines = csv.readlines()
            temp2 = []
            if float(lines[1].replace('\n','').split(',')[0]) > 0:
                temp2.append(0.)
            for line in lines[1:]:
                temp2.append(float(line.replace('\n','').split(',')[-1]))
            temp3 = []
            for v,value in enumerate(temp):
                if value!=0:
                    temp3.append(temp2[v]/value)
                else:
                    temp3.append(0.)
            toWrite1.append(temp3) #JKsrelativeToJ
            if contourValue>1:
                if (contourValue-1)<10:
                    prevcontour = '0' + str(contourValue-1)
                else:
                    prevcontour = str(contourValue-1)
                with open(join(csvfolder,'CrackTip' + str(t+1) + '_T_Contour' + contour + '.csv'),'r') as csv:
                    lines = csv.readlines()
                temp = []
                if float(lines[1].replace('\n','').split(',')[0]) > 0:
                    temp.append(0.)
                for line in lines[1:]:
                    temp.append(float(line.replace('\n','').split(',')[-1]))
                with open(join(csvfolder,'CrackTip' + str(t+1) + '_T_Contour' + prevcontour + '.csv'),'r') as csv:
                    lines = csv.readlines()
                temp2 = []
                if float(lines[1].replace('\n','').split(',')[0]) > 0:
                    temp2.append(0.)
                for line in lines[1:]:
                    temp2.append(float(line.replace('\n','').split(',')[-1]))
                temp3 = []
                for v,value in enumerate(temp):
                    temp3.append(value-temp2[v])
                toWrite3.append(temp3) #TdiffOverContour
        toWrite1 = np.transpose(np.array(toWrite1))
        with open(join(csvfolder,'CrackTip' + str(t+1) + '_GandJhistSummary' + '.csv'),'w') as csv:
            csv.write('THETA [°], ' + str(theta) + '\n')
            line = 'STEP TIME, GI, GII, GTOT, GI/GTOT, GII/GTOT, J,'
            for k in range(1,nContour):
                line += ','
            line += 'JKs,'
            for k in range(1,nContour):
                line += ','
            line += 'J/GTOT,'
            for k in range(1,nContour):
                line += ','
            line += 'JKs/GTOT,'
            for k in range(1,nContour):
                line += ','
            line += 'JKs/J,'
            for k in range(1,nContour-1):
                line += ','
            csv.write(line + '\n')
            line = ''
            for k in range(1,7):
                line += ','
            for l in range(1,6):
                for k in range(1,nContour+1):
                    line += 'c' + str(k) + ','
            csv.write(line[:-1] + '\n')
            for m in range(0,int(toWrite1.shape[0])):
                line = ''
                for n in range(0,int(toWrite1.shape[1])):
                    if n>0:
                        line += ','
                    line += str(toWrite1[m,n])
                csv.write(line + '\n')    
        toWrite2 = np.transpose(np.array(toWrite2))
        with open(join(csvfolder,'CrackTip' + str(t+1) + '_GandJoverG0histSummary' + '.csv'),'w') as csv:
            csv.write('THETA [°], ' + str(theta) + '\n')
            line = 'STEP TIME, GI/G0, GII/G0, GTOT/G0, J/G0,'
            for k in range(1,nContour):
                line += ','
            line += 'JKs/G0,'
            for k in range(1,nContour-1):
                line += ','
            csv.write(line + '\n')
            line = ''
            for k in range(1,5):
                line += ','
            for l in range(1,3):
                for k in range(1,nContour+1):
                    line += 'c' + str(k) + ','
            csv.write(line[:-1] + '\n')
            for m in range(0,int(toWrite2.shape[0])):
                line = ''
                for n in range(0,int(toWrite2.shape[1])):
                    if n>0:
                        line += ','
                    line += str(toWrite2[m,n])
                csv.write(line + '\n')
        toWrite3 = np.transpose(np.array(toWrite3))
        with open(join(csvfolder,'CrackTip' + str(t+1) + '_JcalcConvergenceHist' + '.csv'),'w') as csv:
            csv.write('THETA [°], ' + str(theta) + '\n')
            line = 'STEP TIME, J(c)-J(c-1),'
            for k in range(1,nContour-1):
                line += ','
            line += 'JKs(c)-JKs(c-1),'
            for k in range(1,nContour-1):
                line += ','
            line += 'KI(c)-KI(c-1),'
            for k in range(1,nContour-1):
                line += ','
            line += 'KII(c)-KII(c-1),'
            for k in range(1,nContour-1):
                line += ','
            line += 'T(c)-T(c-1),'
            for k in range(1,nContour-2):
                line += ','
            csv.write(line + '\n')
            line = ''
            line += ','  
            for l in range(1,6):
                for k in range(2,nContour+1):
                    line += 'c' + str(k) + ','
            csv.write(line[:-1] + '\n')
            for m in range(0,int(toWrite3.shape[0])):
                line = ''
                for n in range(0,int(toWrite3.shape[1])):
                    if n>0:
                        line += ','
                    line += str(toWrite3[m,n])
                csv.write(line + '\n')
        toWrite4 = np.transpose(np.array(toWrite4))
        with open(join(csvfolder,'CrackTip' + str(t+1) + '_KandThistSummary' + '.csv'),'w') as csv:
            csv.write('THETA [°], ' + str(theta) + '\n')
            line = 'STEP TIME, KI,'
            for k in range(1,nContour):
                line += ','
            line += 'KII,'
            for k in range(1,nContour):
                line += ','
            line += 'T,'
            for k in range(1,nContour-1):
                line += ','
            csv.write(line + '\n')
            line = ''
            line += ','
            for l in range(1,4):
                for k in range(1,nContour+1):
                    line += 'c' + str(k) + ','
            csv.write(line[:-1] + '\n')
            for m in range(0,int(toWrite3.shape[0])):
                line = ''
                for n in range(0,int(toWrite3.shape[1])):
                    if n>0:
                        line += ','
                    line += str(toWrite3[m,n])
                csv.write(line + '\n')
                
def joinOnlyENRRTsDataPerSim(wd,project,matdatafolder):
    print('')
    print('Gathering data of project ' + project)
    print('')
    # define csv output folder
    csvfolder = join(wd,project,'csv')
    # define csv output folder
    datfolder = join(wd,project,'dat')
    crackTips = []
    lines = []
    try:
        with open(join(csvfolder,'ENRRTs-Summary.csv'),'r') as csv:
            lines = csv.readlines()
    except Exception,e:
        sys.exc_clear()
    for line in lines[1:]:
        crackTips.append(int(line.replace('\n','').split(',')[0]))
    G0 = computeRefG0(wd,project,matdatafolder)
    for t,tip in enumerate(crackTips):
        theta = 0
        time = []
        GI = []
        GII = []
        GTOT = []
        GIratio = []
        GIIratio = []
        GIoverG0 = []
        GIIoverG0 = []
        GTOToverG0 = []
        toWrite1 = []
        toWrite2 = []
        with open(join(csvfolder,'ENRRTs-AtCrackTip' + str(t+1) + '.csv'),'r') as csv:
            lines = csv.readlines()
        theta = np.round(float(lines[1].replace('\n','').split(',')[-1]),decimals=2)
        for line in lines[3:]:
            gi = 0
            gii = 0
            time.append(float(line.replace('\n','').split(',')[0]))
            gi = float(line.replace('\n','').split(',')[1])
            gii = float(line.replace('\n','').split(',')[2])
            GI.append(gi)
            GII.append(gii)
            GTOT.append(gi+gii)
            if (gi+gii)!=0:
                GIratio.append(gi/(gi+gii))
                GIIratio.append(gii/(gi+gii))
            else:
                GIratio.append(0.)
                GIIratio.append(0.)
            GIoverG0.append(gi/G0)
            GIIoverG0.append(gii/G0)
            GTOToverG0.append((gi+gii)/G0)
        toWrite1.append(time)
        toWrite1.append(GI)
        toWrite1.append(GII)
        toWrite1.append(GTOT)
        toWrite1.append(GIratio)
        toWrite1.append(GIIratio)
        toWrite2.append(time)
        toWrite2.append(GIoverG0)
        toWrite2.append(GIIoverG0)
        toWrite2.append(GTOToverG0)
        toWrite1 = np.transpose(np.array(toWrite1))
        with open(join(csvfolder,'CrackTip' + str(t+1) + '_GhistSummary' + '.csv'),'w') as csv:
            csv.write('THETA [°], ' + str(theta) + '\n')
            line = 'STEP TIME, GI, GII, GTOT, GI/GTOT, GII/GTOT'
            csv.write(line + '\n')
            for m in range(0,int(toWrite1.shape[0])):
                line = ''
                for n in range(0,int(toWrite1.shape[1])):
                    if n>0:
                        line += ','
                    line += str(toWrite1[m,n])
                csv.write(line + '\n')    
        toWrite2 = np.transpose(np.array(toWrite2))
        with open(join(csvfolder,'CrackTip' + str(t+1) + '_GoverG0histSummary' + '.csv'),'w') as csv:
            csv.write('THETA [°], ' + str(theta) + '\n')
            line = 'STEP TIME, GI/G0, GII/G0, GTOT/G0'
            csv.write(line + '\n')
            for m in range(0,int(toWrite2.shape[0])):
                line = ''
                for n in range(0,int(toWrite2.shape[1])):
                    if n>0:
                        line += ','
                    line += str(toWrite2[m,n])
                csv.write(line + '\n')

def joinEnergyReleaseDataOverSims(wd,statusfile,matdatafolder,outdir,prefix,nContour):
    # read status file
    with open(join(wd,statusfile),'r') as sta:
        stalines = sta.readlines()
    for i,line in enumerate(stalines[1:]):
        words = line.split(',')
        project = words[0]
        if not exists(join(wd,project,'dat')):
            makedirs(join(wd,project,'dat'))
        joinEnergyReleaseDataPerSim(wd,project,matdatafolder,nContour)
    print('Gathering data across projects...')
    # initialize output files
    with open(join(outdir,prefix + '_GandJ' + '.csv'),'w') as csv:
        line = 'THETA [°], GI, GII, GTOT, GI/GTOT, GII/GTOT, J,'
        for k in range(1,nContour):
            line += ','
        line += 'JKs,'
        for k in range(1,nContour):
            line += ','
        line += 'J/GTOT,'
        for k in range(1,nContour):
            line += ','
        line += 'JKs/GTOT,'
        for k in range(1,nContour):
            line += ','
        line += 'JKs/J,'
        for k in range(1,nContour-1):
            line += ','
        csv.write(line + '\n')
        line = ''
        for k in range(1,7):
            line += ','
        for l in range(1,6):
            for k in range(1,nContour+1):
                line += 'c' + str(k) + ','
        csv.write(line[:-1] + '\n')
    with open(join(outdir,prefix + '_GandJoverG0' + '.csv'),'w') as csv:
        line = 'THETA [°], GI/G0, GII/G0, GTOT/G0, J/G0,'
        for k in range(1,nContour):
            line += ','
        line += 'JKs/G0,'
        for k in range(1,nContour-1):
            line += ','
        csv.write(line + '\n')
        line = ''
        for k in range(1,5):
            line += ','
        for l in range(1,3):
            for k in range(1,nContour+1):
                line += 'c' + str(k) + ','
        csv.write(line[:-1] + '\n')   
    with open(join(outdir,prefix + '_JcalcConvergence' + '.csv'),'w') as csv:
        line = 'THETA [°], J(c)-J(c-1),'
        for k in range(1,nContour-1):
            line += ','
        line += 'JKs(c)-JKs(c-1),'
        for k in range(1,nContour-1):
            line += ','
        line += 'KI(c)-KI(c-1),'
        for k in range(1,nContour-1):
            line += ','
        line += 'KII(c)-KII(c-1),'
        for k in range(1,nContour-1):
            line += ','
        line += 'T(c)-T(c-1),'
        for k in range(1,nContour-2):
            line += ','
        csv.write(line + '\n')
        line = ''
        line += ','  
        for l in range(1,6):
            for k in range(2,nContour+1):
                line += 'c' + str(k) + ','
        csv.write(line[:-1] + '\n')
    with open(join(outdir,prefix + '_KandT' + '.csv'),'w') as csv:
        line = 'THETA [°], KI,'
        for k in range(1,nContour):
            line += ','
        line += 'KII,'
        for k in range(1,nContour):
            line += ','
        line += 'T,'
        for k in range(1,nContour-1):
            line += ','
        csv.write(line + '\n')
        line = ''
        line += ','
        for l in range(1,4):
            for k in range(1,nContour+1):
                line += 'c' + str(k) + ','
        csv.write(line[:-1] + '\n')
    # initialize data containers
    GandJ = []
    GandJoverG0 = []
    JcalcConvergence = []
    KandT = []
    # for line in status file
    for i,line in enumerate(stalines[1:]):
        words = line.split(',')
        project = words[0]
        csvfolder = join(wd,project,'csv')
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
            temp = []
            with open(join(csvfolder,'CrackTip' + str(t+1) + '_GandJhistSummary' + '.csv'),'r') as csv:
                values = csv.readlines()
            theta = np.round(float(values[0].replace('\n','').split(',')[1]),decimals=0)
            temp.append(theta)
            for value in values[-1].replace('\n','').split(',')[1:]:
                temp.append(float(value))
            GandJ.append(temp)
            temp = []
            with open(join(csvfolder,'CrackTip' + str(t+1) + '_GandJoverG0histSummary' + '.csv'),'r') as csv:
                values = csv.readlines()
            temp.append(theta)
            for value in values[-1].replace('\n','').split(',')[1:]:
                temp.append(float(value))
            GandJoverG0.append(temp)
            temp = []
            with open(join(csvfolder,'CrackTip' + str(t+1) + '_JcalcConvergenceHist' + '.csv'),'r') as csv:
                values = csv.readlines()
            temp.append(theta)
            for value in values[-1].replace('\n','').split(',')[1:]:
                temp.append(float(value))
            JcalcConvergence.append(temp)
            temp = []
            with open(join(csvfolder,'CrackTip' + str(t+1) + '_KandThistSummary' + '.csv'),'r') as csv:
                values = csv.readlines()
            temp.append(theta)
            for value in values[-1].replace('\n','').split(',')[1:]:
                temp.append(float(value))
            KandT.append(temp)
    GandJ = np.array(GandJ)
    if 0. not in GandJ[:,0]:
        temp = []
        for j in range(0,int(GandJ.shape[1])):
            temp.append(0.)
        GandJ = np.append(GandJ,[temp],axis=0) 
    GandJ = GandJ[GandJ[:,0].argsort()]
    GandJoverG0 = np.array(GandJoverG0)
    if 0. not in GandJoverG0[:,0]:
        temp = []
        for j in range(0,int(GandJoverG0.shape[1])):
            temp.append(0.)
        GandJoverG0 = np.append(GandJoverG0,[temp],axis=0) 
    GandJoverG0 = GandJoverG0[GandJoverG0[:,0].argsort()]
    JcalcConvergence = np.array(JcalcConvergence)
    if 0. not in JcalcConvergence[:,0]:
        temp = []
        for j in range(0,int(JcalcConvergence.shape[1])):
            temp.append(0.)
        JcalcConvergence = np.append(JcalcConvergence,[temp],axis=0) 
    JcalcConvergence = JcalcConvergence[JcalcConvergence[:,0].argsort()]
    KandT = np.array(KandT)
    if 0. not in KandT[:,0]:
        temp = []
        for j in range(0,int(KandT.shape[1])):
            temp.append(0.)
        KandT = np.append(KandT,[temp],axis=0) 
    KandT = KandT[KandT[:,0].argsort()]
    with open(join(outdir,prefix + '_GandJ' + '.csv'),'a') as csv:
        for m in range(0,int(GandJ.shape[0])):
            toWrite = ''
            for n in range(0,int(GandJ.shape[1])):
                if n>0:
                    toWrite += ','
                toWrite += str(GandJ[m,n])
            csv.write(toWrite + '\n')
    with open(join(outdir,prefix + '_GandJoverG0' + '.csv'),'a') as csv:
        for m in range(0,int(GandJoverG0.shape[0])):
            toWrite = ''
            for n in range(0,int(GandJoverG0.shape[1])):
                if n>0:
                    toWrite += ','
                toWrite += str(GandJoverG0[m,n])
            csv.write(toWrite + '\n')
    with open(join(outdir,prefix + '_JcalcConvergence' + '.csv'),'a') as csv:
        for m in range(0,int(JcalcConvergence.shape[0])):
            toWrite = ''
            for n in range(0,int(JcalcConvergence.shape[1])):
                if n>0:
                    toWrite += ','
                toWrite += str(JcalcConvergence[m,n])
            csv.write(toWrite + '\n')
    with open(join(outdir,prefix + '_KandT' + '.csv'),'a') as csv:
        for m in range(0,int(KandT.shape[0])):
            toWrite = ''
            for n in range(0,int(KandT.shape[1])):
                if n>0:
                    toWrite += ','
                toWrite += str(KandT[m,n])
            csv.write(toWrite + '\n')
    print('...done.')

def joinOnlyENRRTsDataOverSims(wd,statusfile,matdatafolder,outdir,prefix):
    # read status file
    with open(join(wd,statusfile),'r') as sta:
        stalines = sta.readlines()
    for i,line in enumerate(stalines[1:]):
        words = line.split(',')
        project = words[0]
        if not exists(join(wd,project,'dat')):
            makedirs(join(wd,project,'dat'))
        #joinOnlyENRRTsDataPerSim(wd,project,matdatafolder)
    print('Gathering data across projects...')
    # initialize output files
    with open(join(outdir,prefix + '_G' + '.csv'),'w') as csv:
        line = 'THETA [°], GI, GII, GTOT, GI/GTOT, GII/GTOT'
        csv.write(line + '\n')
    with open(join(outdir,prefix + '_GoverG0' + '.csv'),'w') as csv:
        line = 'THETA [°], GI/G0, GII/G0, GTOT/G0'
        csv.write(line + '\n')
    # initialize data containers
    G = []
    GoverG0 = []
    # for line in status file
    for i,line in enumerate(stalines[1:]):
        words = line.split(',')
        project = words[0]
        csvfolder = join(wd,project,'csv')
        #crackTips = []
        lines = []
        G0 = computeRefG0(wd,project,matdatafolder)
        try:
            with open(join(csvfolder,'ENRRTs-Summary.csv'),'r') as csv:
                lines = csv.readlines()
        except Exception,e:
            sys.exc_clear()
        for line in lines[1:]:
            #crackTips.append(int(line.replace('\n','').split(',')[0]))
            #theta = np.round(float(line.replace('\n','').split(',')[4]),decimals=0)
            G.append([np.round(float(line.replace('\n','').split(',')[4]),decimals=0),float(line.replace('\n','').split(',')[-2]),float(line.replace('\n','').split(',')[-1]),float(line.replace('\n','').split(',')[-2])+float(line.replace('\n','').split(',')[-1])])
            GoverG0.append([np.round(float(line.replace('\n','').split(',')[4]),decimals=0),float(line.replace('\n','').split(',')[-2])/G0,float(line.replace('\n','').split(',')[-1])/G0,(float(line.replace('\n','').split(',')[-2])+float(line.replace('\n','').split(',')[-1]))/G0])
        '''
        for t,tip in enumerate(crackTips):
            theta = 0
            temp = []
            with open(join(csvfolder,'CrackTip' + str(t+1) + '_GhistSummary' + '.csv'),'r') as csv:
                values = csv.readlines()
            theta = np.round(float(values[0].replace('\n','').split(',')[1]),decimals=0)
            temp.append(theta)
            for value in values[-1].replace('\n','').split(',')[1:]:
                temp.append(float(value))
            G.append(temp)
            temp = []
            with open(join(csvfolder,'CrackTip' + str(t+1) + '_GoverG0histSummary' + '.csv'),'r') as csv:
                values = csv.readlines()
            temp.append(theta)
            for value in values[-1].replace('\n','').split(',')[1:]:
                temp.append(float(value))
            GoverG0.append(temp)
        '''    
    G = np.array(G)
    if 0. not in G[:,0]:
        temp = []
        for j in range(0,int(G.shape[1])):
            temp.append(0.)
        G = np.append(G,[temp],axis=0) 
    G = G[G[:,0].argsort()]
    GoverG0 = np.array(GoverG0)
    if 0. not in GoverG0[:,0]:
        temp = []
        for j in range(0,int(GoverG0.shape[1])):
            temp.append(0.)
        GoverG0 = np.append(GoverG0,[temp],axis=0) 
    GoverG0 = GoverG0[GoverG0[:,0].argsort()]
    with open(join(outdir,prefix + '_G' + '.csv'),'a') as csv:
        for m in range(0,int(G.shape[0])):
            toWrite = ''
            for n in range(0,int(G.shape[1])):
                if n>0:
                    toWrite += ','
                toWrite += str(G[m,n])
            csv.write(toWrite + '\n')
    with open(join(outdir,prefix + '_GoverG0' + '.csv'),'a') as csv:
        for m in range(0,int(GoverG0.shape[0])):
            toWrite = ''
            for n in range(0,int(GoverG0.shape[1])):
                if n>0:
                    toWrite += ','
                toWrite += str(GoverG0[m,n])
            csv.write(toWrite + '\n')
    print('...done.')
    
def joinOnlyENRRTsDataOverSiPlateSims(wd,statusfile,matdatafolder,outdir,prefix):
    # read status file
    with open(join(wd,statusfile),'r') as sta:
        stalines = sta.readlines()
    print('Gathering data across projects...')
    # initialize output files
    with open(join(outdir,prefix + '_Summary' + '.csv'),'w') as csv:
        line = 'a/W [-], da/a [-], x0 [mm], E [GPa], nu [-], E_plane-strain [GPa], eps [-], sigma [MPa], K1_inf [Pa*m^0.5], K1 (analytical) [Pa*m^0.5], K1 (FEM) [Pa*m^0.5], K1/K1_inf (analytical) [-], K1/K1_inf (FEM) [-], G1_inf [J/m^2], G1 (analytical) [J/m^2], G1 (FEM) [J/m^2], G1/G1_inf (analytical) [-], G1/G1_inf (FEM) [-], K2_inf [Pa*m^0.5], K2 (analytical) [Pa*m^0.5], K2 (FEM) [Pa*m^0.5], G2_inf [J/m^2], G2 (analytical) [J/m^2], G2 (FEM) [J/m^2]' + '\n'
        csv.write(line + '\n')
    # initialize data containers
    csvdata = []
    Kdata = []
    Gdata = []
    normKdata = []
    normGdata = []
    Kdatath = []
    Gdatath = []
    normKdatath = []
    normGdatath = []
    # for line in status file
    for i,line in enumerate(stalines[1:]):
        words = line.split(',')
        project = words[0]
        csvfolder = join(wd,project,'csv')
        #crackTips = []
        lines = []
        enrrtFactor, E, nu, Epeps, eps, sigma, aOverW, K1th, K1inf, G1th, G1inf, K2th, K2inf, G2th, G2inf = computeRefValuesSingleMaterialPlate(wd,project,matdatafolder)
        try:
            with open(join(csvfolder,'ENRRTs-Summary.csv'),'r') as csv:
                lines = csv.readlines()
        except Exception,e:
            sys.exc_clear()
        for line in lines[1:]:
            aOverW = float(line.replace('\n','').split(',')[5])
            daOvera = float(line.replace('\n','').split(',')[6])
            x0 = float(line.replace('\n','').split(',')[7])
            enrrt11 = enrrtFactor*float(line.replace('\n','').split(',')[-2])
            enrrt12 = enrrtFactor*float(line.replace('\n','').split(',')[-1])
            K1 = np.sqrt(Epeps*enrrt11)
            K2 = np.sqrt(Epeps*enrrt12)
            csvdata.append([aOverW,daOvera,x0,E*1e-9,nu,Epeps*1e-9,eps,sigma*1e-6,K1inf,K1th,K1,K1th/K1inf,K1/K1inf,G1inf,G1th,enrrt11,G1th/G1inf,enrrt11/G1inf,K2inf,K2th,K2,G2inf,G2th,enrrt12])
            if x0>0:
                Kdata.append([aOverW,K1])
                Gdata.append([aOverW,enrrt11])
                normKdata.append([aOverW,K1/K1inf])
                normGdata.append([aOverW,enrrt11/G1inf])
                Kdatath.append([aOverW,K1th])
                Gdatath.append([aOverW,G1th])
                normKdatath.append([aOverW,K1th/K1inf])
                normGdatath.append([aOverW,G1th/G1inf])

    with open(join(outdir,prefix + '_Summary' + '.csv'),'a') as csv:
        for datum in csvdata:
            line = ''
            for v,value in enumerate(datum):
                if v>0:
                    line += ','
                line += str(value)
            csv.write(line + '\n')
            
    KSummary = prefix + '_KSummary'
    normKSummary = prefix + '_normKSummary'
    GSummary = prefix + '_GSummary'
    normGSummary = prefix + '_normGSummary'
    axoptions = 'width=30cm,\n' \
                'title={$K_{I}$ vs crack\'s apsect ratio  $\\frac{a}{W}$},\n' \
                'xlabel={$\\frac{a}{W}\\left[-\\right]$},ylabel={$K_{I}\\left[Pa\\sqrt{m}\\right]$},\n' \
                'xmin=0.0,\n' \
                'xmax=' + str(1.0) + ',\n' \
                'ymin=' + str(0.95*np.min([np.min(np.array(Kdata)[:,1]),np.min(np.array(Kdatath)[:,1])])) + ',\n' \
                'ymax=' + str(1.05*np.max([np.max(np.array(Kdata)[:,1]),np.max(np.array(Kdatath)[:,1])])) + ',\n' \
                'tick align=outside,\n' \
                'tick label style={font=\\tiny},\n' \
                'xtick={0.0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1.0},\n' \
                'xmajorgrids,\n' \
                'x grid style={lightgray!92.026143790849673!black},\n' \
                'ymajorgrids,\n' \
                'y grid style={lightgray!92.026143790849673!black},\n' \
                'line width=0.35mm,\n' \
                'legend style={draw=white!80.0!black,font=\\fontsize{6}{6}\\selectfont},\n' \
                'legend entries={{FEM},{Analytical}},\n' \
                'legend cell align={left}\n'
    dataoptions = ['red,only marks,mark=triangle*','black,smooth,mark=*']
    writeLatexMultiplePlots(outdir,prefix,join(outdir,prefix,'tex'),KSummary,[Kdata, Kdatath],axoptions,dataoptions)
    
    axoptions = 'width=30cm,\n' \
                'title={$\\frac{K_{I}}{K^{\infty}_{I}}$ vs crack\'s apsect ratio  $\\frac{a}{W}$},\n' \
                'xlabel={$\\frac{a}{W}\\left[-\\right]$},ylabel={$\\frac{K_{I}}{K^{\infty}_{I}}\\left[-\\right]$},\n' \
                'xmin=0.0,\n' \
                'xmax=' + str(1.0) + ',\n' \
                'ymin=' + str(0.95*np.min([np.min(np.array(normKdata)[:,1]),np.min(np.array(normKdatath)[:,1])])) + ',\n' \
                'ymax=' + str(1.05*np.max([np.max(np.array(normKdata)[:,1]),np.max(np.array(normKdatath)[:,1])])) + ',\n' \
                'tick align=outside,\n' \
                'tick label style={font=\\tiny},\n' \
                'xtick={0.0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1.0},\n' \
                'xmajorgrids,\n' \
                'x grid style={lightgray!92.026143790849673!black},\n' \
                'ymajorgrids,\n' \
                'y grid style={lightgray!92.026143790849673!black},\n' \
                'line width=0.35mm,\n' \
                'legend style={draw=white!80.0!black,font=\\fontsize{6}{6}\\selectfont},\n' \
                'legend entries={{FEM},{Analytical}},\n' \
                'legend cell align={left}\n'
    writeLatexMultiplePlots(outdir,prefix,join(outdir,prefix,'tex'),normKSummary,[normKdata, normKdatath],axoptions,dataoptions)
    
    axoptions = 'width=30cm,\n' \
                'title={$G_{I}$ vs crack\'s apsect ratio  $\\frac{a}{W}$},\n' \
                'xlabel={$\\frac{a}{W}\\left[-\\right]$},ylabel={$G_{I}\\left[\\frac{J}{m^{2}}\\right]$},\n' \
                'xmin=0.0,\n' \
                'xmax=' + str(1.0) + ',\n' \
                'ymin=' + str(0.95*np.min([np.min(np.array(Gdata)[:,1]),np.min(np.array(Gdatath)[:,1])])) + ',\n' \
                'ymax=' + str(1.05*np.max([np.max(np.array(Gdata)[:,1]),np.max(np.array(Gdatath)[:,1])])) + ',\n' \
                'tick align=outside,\n' \
                'tick label style={font=\\tiny},\n' \
                'xtick={0.0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1.0},\n' \
                'xmajorgrids,\n' \
                'x grid style={lightgray!92.026143790849673!black},\n' \
                'ymajorgrids,\n' \
                'y grid style={lightgray!92.026143790849673!black},\n' \
                'line width=0.35mm,\n' \
                'legend style={draw=white!80.0!black,font=\\fontsize{6}{6}\\selectfont},\n' \
                'legend entries={{FEM},{Analytical}},\n' \
                'legend cell align={left}\n'
    writeLatexMultiplePlots(outdir,prefix,join(outdir,prefix,'tex'),GSummary,[Gdata, Gdatath],axoptions,dataoptions)
    
    axoptions = 'width=30cm,\n' \
                'title={$\\frac{G_{I}}{G^{\infty}_{I}}$ vs crack\'s apsect ratio  $\\frac{a}{W}$},\n' \
                'xlabel={$\\frac{a}{W}\\left[-\\right]$},ylabel={$\\frac{G_{I}}{G^{\infty}_{I}}\\left[-\\right]$},\n' \
                'xmin=0.0,\n' \
                'xmax=' + str(1.0) + ',\n' \
                'ymin=' + str(0.95*np.min([np.min(np.array(normGdata)[:,1]),np.min(np.array(normGdatath)[:,1])])) + ',\n' \
                'ymax=' + str(1.05*np.max([np.max(np.array(normGdata)[:,1]),np.max(np.array(normGdatath)[:,1])])) + ',\n' \
                'tick align=outside,\n' \
                'tick label style={font=\\tiny},\n' \
                'xtick={0.0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1.0},\n' \
                'xmajorgrids,\n' \
                'x grid style={lightgray!92.026143790849673!black},\n' \
                'ymajorgrids,\n' \
                'y grid style={lightgray!92.026143790849673!black},\n' \
                'line width=0.35mm,\n' \
                'legend style={draw=white!80.0!black,font=\\fontsize{6}{6}\\selectfont},\n' \
                'legend entries={{FEM},{Analytical}},\n' \
                'legend cell align={left}\n'
    writeLatexMultiplePlots(outdir,prefix,join(outdir,prefix,'tex'),normGSummary,[normGdata, normGdatath],axoptions,dataoptions)
   
    print('...done.')
            

def joinERRTsDataOverSimsExtSet04(wd,statusfile,refdatafolder,refdatafilename,outdir,prefix,ncontInt,NEl0,NElMax,DeltaEl):
    print('Gathering data across projects...')
    # initialize output files
    line = 'NODE LABEL, X0 [m], Y0 [m], R0 [m], THETA0 [°], X [m], Y [m], R [m], THETA [°], nu [-], mu [Pa], deltaC [°], Disp_R, Disp_theta, RF_R, RF_theta, sigma_Inf_UNDAMAGED [Pa], sigma_Inf_DAMAGED [Pa], G0_UNDAMAGED [J/m^2], G0_DAMAGED [J/m^2], GI_M-F-VCCT [J/m^2], GII_M-F-VCCT [J/m^2], GTOT_M-F-VCCT [J/m^2], GI_M-F-VCCT/G0 [-], GII_M-F-VCCT/G0 [-], GTOT_M-F-VCCT/G0 [-]'# 0-25
    secondline = ', , , , , , , , , , , , , , , , , , , , , , , , , '
    numGs = (NElMax+DeltaEl-nEl0)/DeltaEl
    line += ', '
    secondline += ', '
    line += 'GI_M-SoM-VCCT [J/m^2]'
    secondline += 'N Int El ' + str(nEl0)
    for j in range(1,numGs):
        secondline += ', '
        secondline += 'N Int El ' + str(nEl0 + j*DeltaEl)
        line += ', '
    line += ', '
    secondline += ', '
    line += 'GII_M-SoM-VCCT [J/m^2]'
    secondline += 'N Int El ' + str(nEl0)
    for j in range(1,numGs):
        secondline += ', '
        secondline += 'N Int El ' + str(nEl0 + j*DeltaEl)
        line += ', '
    line += ', '
    secondline += ', '
    line += 'GTOT_M-SoM-VCCT [J/m^2]'
    secondline += 'N Int El ' + str(nEl0)
    for j in range(1,numGs):
        secondline += ', '
        secondline += 'N Int El ' + str(nEl0 + j*DeltaEl)
        line += ', '
    line += ', '
    secondline += ', '
    line += 'GI_M-SoM-VCCT/G0 [J/m^2]'
    secondline += 'N Int El ' + str(nEl0)
    for j in range(1,numGs):
        secondline += ', '
        secondline += 'N Int El ' + str(nEl0 + j*DeltaEl)
        line += ', '
    line += ', '
    secondline += ', '
    line += 'GII_M-SoM-VCCT/G0 [J/m^2]'
    secondline += 'N Int El ' + str(nEl0)
    for j in range(1,numGs):
        secondline += ', '
        secondline += 'N Int El ' + str(nEl0 + j*DeltaEl)
        line += ', '
    line += ', '
    secondline += ', '
    line += 'GTOT_M-SoM-VCCT/G0 [J/m^2]'
    secondline += 'N Int El ' + str(nEl0)
    for j in range(1,numGs):
        secondline += ', '
        secondline += 'N Int El ' + str(nEl0 + j*DeltaEl)
        line += ', '
    line += ', '
    secondline += ', '
    line += 'GI_M-SoF-VCCT [J/m^2]'
    secondline += 'N Int El ' + str(nEl0)
    for j in range(1,numGs):
        secondline += ', '
        secondline += 'N Int El ' + str(nEl0 + j*DeltaEl)
        line += ', '
    line += ', '
    secondline += ', '
    line += 'GII_M-SoF-VCCT [J/m^2]'
    secondline += 'N Int El ' + str(nEl0)
    for j in range(1,numGs):
        secondline += ', '
        secondline += 'N Int El ' + str(nEl0 + j*DeltaEl)
        line += ', '
    line += ', '
    secondline += ', '
    line += 'GTOT_M-SoF-VCCT [J/m^2]'
    secondline += 'N Int El ' + str(nEl0)
    for j in range(1,numGs):
        secondline += ', '
        secondline += 'N Int El ' + str(nEl0 + j*DeltaEl)
        line += ', '
    line += ', '
    secondline += ', '
    line += 'GI_M-SoF-VCCT/G0 [J/m^2]'
    secondline += 'N Int El ' + str(nEl0)
    for j in range(1,numGs):
        secondline += ', '
        secondline += 'N Int El ' + str(nEl0 + j*DeltaEl)
        line += ', '
    line += ', '
    secondline += ', '
    line += 'GII_M-SoF-VCCT/G0 [J/m^2]'
    secondline += 'N Int El ' + str(nEl0)
    for j in range(1,numGs):
        secondline += ', '
        secondline += 'N Int El ' + str(nEl0 + j*DeltaEl)
        line += ', '
    line += ', '
    secondline += ', '
    line += 'GTOT_M-SoF-VCCT/G0 [J/m^2]'
    secondline += 'N Int El ' + str(nEl0)
    for j in range(1,numGs):
        secondline += ', '
        secondline += 'N Int El ' + str(nEl0 + j*DeltaEl)
        line += ', '
    if ncontInt>-1:    
        line += ', '
        secondline += ', '
        line += 'GTOT_ABQ-JINT [J/m^2]'
        secondline += 'Contour 1'
        for j in range(1,ncontInt):
            secondline += ', '
            secondline += 'Contour ' + str(j)
            line += ', '
        line += ', '
        secondline += ', '
        line += 'GTOT_ABQ-JINT/G0 [-]'
        secondline += 'Contour 1'
        for j in range(1,ncontInt):
            secondline += ', '
            secondline += 'Contour ' + str(j)
            line += ', '
    line += ', G0_BEM [J/m^2], GI_BEM [J/m^2], GII_BEM [J/m^2], GTOT_BEM [J/m^2], GI_BEM/G0 [-], GII_BEM/G0 [-], GTOT_BEM/G0 [-]'
    with open(join(outdir,prefix + '_Summary' + '.csv'),'w') as csv:
        csv.write(line +'\n')
        csv.write(secondline +'\n')
    # extract reference data
    # read file
    with open(join(refdatafolder,refdatafilename),'r') as ref:
        reflines = ref.readlines()
    # initialize data containers
    refG0 = float(reflines[0].replace('\n','').split(',')[-1])
    refTheta = []
    refdata = []
    # parse lines
    for line in reflines[2:]:
        refdata.append([refG0,refG0*float(line.replace('\n','').split(',')[1]),refG0*float(line.replace('\n','').split(',')[2]),refG0*float(line.replace('\n','').split(',')[3]),float(line.replace('\n','').split(',')[1]),float(line.replace('\n','').split(',')[2]),float(line.replace('\n','').split(',')[3])])
        refTheta.append(float(line.replace('\n','').split(',')[0]))
    # extract FEM data
    # read status file
    with open(join(wd,statusfile),'r') as sta:
        stalines = sta.readlines()
    # initialize data containers
    csvdata = []
    globaldata = []
    # parse lines
    for i,line in enumerate(stalines[1:]):
        try:
            print('opening file ' + join(wd,line.replace('\n','').split(',')[0],'csv','ENRRTs-Summary.csv') + 'for project ' + line.replace('\n','').split(',')[0])
            with open(join(wd,line.replace('\n','').split(',')[0],'csv','ENRRTs-Summary.csv'),'r') as csv:
                csvlines = csv.readlines()
        except Exception,error:
            print(error)
        for csvline in csvlines[2:]:
            readings = csvline.replace('\n','').split(',')
            values = []
            for reading in readings:
                values.append(float(reading))
            csvdata.append(values)
            if np.round(values[4],decimals=0) in refTheta:
                index = -1
                for t,theta in enumerate(refTheta):
                    if np.round(values[4],decimals=0)==np.round(theta,decimals=0):
                        index = t
                        break
                for refvalue in refdata[index]:
                    values.append(refvalue)
                globaldata.append(values)
            else:
                for i in range(0,len(refdata[0])):
                    values.append(None)
                globaldata.append(values)
        try:
            print('opening file ' + join(wd,line.replace('\n','').split(',')[0],'csv','ENRRTs-VCCTinStresses-Summary.csv') + 'for project ' + line.replace('\n','').split(',')[0])
            with open(join(wd,line.replace('\n','').split(',')[0],'csv','ENRRTs-VCCTinStresses-Summary.csv'),'r') as csv:
                csvlines = csv.readlines()
        except Exception,error:
            print(error)
        for csvline in csvlines[2:]:
            readings = csvline.replace('\n','').split(',')
            values = []
            label = float(readings[0])
            for reading in readings[16:]:
                values.append(float(reading))
            if label==globaldata[-1][0]:
                globaldata[-1] = globaldata[-1][:25] + values + globaldata[-1][26:]
            else:
                globaldata[-2] = globaldata[-2][:25] + values + globaldata[-2][26:]
    globaldata = np.array(globaldata)
    globaldata = globaldata[globaldata[:,4].argsort()]
    with open(join(outdir,prefix + '_Summary' + '.csv'),'a') as csv:
        for values in globaldata:
            line = ''
            for v,value in enumerate(values):
                if v>0:
                    line += ','
                if value!=None:
                    line += str(value)
                else:
                    line += ' '
            csv.write(line + '\n')
    indexStartStressesVCCT = 25 + 1
    indexStartJINTs = 25 + 12*numGs + 1
    
    try:
        axoptions = 'width=30cm,\n' \
                    'title={Applied stress $\\sigma_{0}$ as function of crack angular semi-aperture  $\\Delta\\theta$},\n' \
                    'title style={font=\\fontsize{16}{8}\\selectfont},\n' \
                    'xlabel style={at={(axis description cs:0.5,-0.02)},anchor=north,font=\\fontsize{16}{8}\\selectfont},\n' \
                    'ylabel style={at={(axis description cs:-0.01,.5)},anchor=south,font=\\fontsize{16}{8}\\selectfont},\n' \
                    'xlabel={$\\Delta\\theta\\left[^{\\circ}\\right]$},ylabel={$\\sigma_{0}\\left[Pa\\right]$},\n' \
                    'xmin=0.0,\n' \
                    'xmax=180.0,\n' \
                    'ymin=' + str(0.95*np.min([np.min(globaldata[:,16]),np.min(globaldata[:,17])])) + ',\n' \
                    'ymax=' + str(1.05*np.max([np.max(globaldata[:,16]),np.max(globaldata[:,17])])) + ',\n' \
                    'tick align=outside,\n' \
                    'tick label style={font=\\normalsize},\n' \
                    'xtick={0.0,10.0,20.0,30.0,40.0,50.0,60.0,70.0,80.0,90.0,100.0,110.0,120.0,130.0,140.0,150.0,160.0,170.0,180.0},\n' \
                    'xmajorgrids,\n' \
                    'x grid style={lightgray!92.026143790849673!black},\n' \
                    'ymajorgrids,\n' \
                    'y grid style={lightgray!92.026143790849673!black},\n' \
                    'line width=0.35mm,\n' \
                    'legend style={draw=white!80.0!black,font=\\fontsize{16}{12}\\selectfont},\n' \
                    'legend entries={{$\\sigma_{0}$, FEM model with debond},{$\\sigma_{0}=\\frac{E}{1-\\nu^{2}}\\varepsilon_{0}$, plane strain undamaged theoretical value}},\n' \
                    'legend cell align={left}\n'
        mask1 = (globaldata[:,4] > 0) & (globaldata[:,4] < 151) & (globaldata[:,17] != None) & (globaldata[:,16] != None)
        data = [np.transpose(np.array([globaldata[mask1,4],globaldata[mask1,17]])),
                np.transpose(np.array([globaldata[mask1,4],globaldata[mask1,16]]))]
        dataoptions = ['red,smooth,mark=*','black,smooth,mark=*']
        writeLatexMultiplePlots(outdir,prefix,join(outdir,prefix,'tex'),prefix + '_sigma-inf' + '_Summary',data,axoptions,dataoptions)
    except Exception,error:
        print(error)
    
    try:
        axoptions = 'width=30cm,\n' \
                    'title={Total energy release rate for the infinite model $G0$ as function of crack angular semi-aperture  $\\Delta\\theta$},\n' \
                    'title style={font=\\fontsize{16}{8}\\selectfont},\n' \
                    'xlabel style={at={(axis description cs:0.5,-0.02)},anchor=north,font=\\fontsize{16}{8}\\selectfont},\n' \
                    'ylabel style={at={(axis description cs:-0.01,.5)},anchor=south,font=\\fontsize{16}{8}\\selectfont},\n' \
                    'xlabel={$\\Delta\\theta\\left[^{\\circ}\\right]$},ylabel={$G0\\left[\\frac{J}{m^{2}}\\right]$},\n' \
                    'xmin=0.0,\n' \
                    'xmax=180.0,\n' \
                    'ymin=' + str(0.95*np.min([np.min(globaldata[:,18]),np.min(globaldata[:,19])])) + ',\n' \
                    'ymax=' + str(1.05*np.max([np.max(globaldata[:,18]),np.max(globaldata[:,19])])) + ',\n' \
                    'tick align=outside,\n' \
                    'tick label style={font=\\normalsize},\n' \
                    'xtick={0.0,10.0,20.0,30.0,40.0,50.0,60.0,70.0,80.0,90.0,100.0,110.0,120.0,130.0,140.0,150.0,160.0,170.0,180.0},\n' \
                    'xmajorgrids,\n' \
                    'x grid style={lightgray!92.026143790849673!black},\n' \
                    'ymajorgrids,\n' \
                    'y grid style={lightgray!92.026143790849673!black},\n' \
                    'line width=0.35mm,\n' \
                    'legend style={draw=white!80.0!black,font=\\fontsize{16}{12}\\selectfont},\n' \
                    'legend entries={{$G0$, FEM model with debond},{$G0=\\pi R_{f}\\sigma_{0}^{2}\\frac{1-\\left(3-4\\nu_{m}\\right)}{\\mu_{m}}$, plane strain undamaged theoretical value}},\n' \
                    'legend cell align={left}\n'
        mask1 = (globaldata[:,4] > 0) & (globaldata[:,4] < 151) & (globaldata[:,19] != None) & (globaldata[:,18] != None)
        data = [np.transpose(np.array([globaldata[mask1,4],globaldata[mask1,19]])),
                np.transpose(np.array([globaldata[mask1,4],globaldata[mask1,18]]))]
        dataoptions = ['red,smooth,mark=*','black,smooth,mark=*']
        writeLatexMultiplePlots(outdir,prefix,join(outdir,prefix,'tex'),prefix + '_G0' + '_Summary',data,axoptions,dataoptions)
    except Exception,error:
        print(error)
    
    try:
        axoptions = 'width=30cm,\n' \
                    'title={Normalized energy release rate $\\frac{G_{\\left(\\cdot\\cdot\\right)}}{G_{0}}$ as function of crack angular semi-aperture  $\\Delta\\theta$, calculated with in-house force-based VCCT post-processing routine},\n' \
                    'title style={font=\\fontsize{16}{8}\\selectfont},\n' \
                    'xlabel style={at={(axis description cs:0.5,-0.02)},anchor=north,font=\\fontsize{16}{8}\\selectfont},\n' \
                    'ylabel style={at={(axis description cs:-0.01,.5)},anchor=south,font=\\fontsize{16}{8}\\selectfont},\n' \
                    'xlabel={$\\Delta\\theta\\left[^{\\circ}\\right]$},ylabel={$\\frac{G_{\\left(\\cdot\\cdot\\right)}}{G_{0}}\\left[-\\right]$},\n' \
                    'xmin=0.0,\n' \
                    'xmax=180.0,\n' \
                    'ymin=0.0,\n' \
                    'ymax=' + str(1.05*np.max([np.max(globaldata[:,25]),np.max(globaldata[:,-1])])) + ',\n' \
                    'tick align=outside,\n' \
                    'tick label style={font=\\normalsize},\n' \
                    'xtick={0.0,10.0,20.0,30.0,40.0,50.0,60.0,70.0,80.0,90.0,100.0,110.0,120.0,130.0,140.0,150.0,160.0,170.0,180.0},\n' \
                    'xmajorgrids,\n' \
                    'x grid style={lightgray!92.026143790849673!black},\n' \
                    'ymajorgrids,\n' \
                    'y grid style={lightgray!92.026143790849673!black},\n' \
                    'line width=0.35mm,\n' \
                    'legend style={draw=white!80.0!black,font=\\fontsize{16}{12}\\selectfont},\n' \
                    'legend entries={{$\\frac{G_{I}}{G_{0}}$, FEM},{$\\frac{G_{II}}{G_{0}}$, FEM},{$\\frac{G_{I}+G_{II}}{G_{0}}$, FEM},{$\\frac{G_{I}}{G_{0}}$, BEM},{$\\frac{G_{II}}{G_{0}}$, BEM},{$\\frac{G_{I}+G_{II}}{G_{0}}$, BEM}},\n' \
                    'legend cell align={left}\n'
        mask1 = (globaldata[:,4] > 0) & (globaldata[:,4] < 151) & (globaldata[:,23] != None) & (globaldata[:,24] != None) & (globaldata[:,25] != None)
        mask2 = (globaldata[:,4] > 0) & (globaldata[:,4] < 151) & (globaldata[:,-1] != None) & (globaldata[:,-2] != None) & (globaldata[:,-3] != None)
        data = [np.transpose(np.array([globaldata[mask1,4],globaldata[mask1,23]])),
                np.transpose(np.array([globaldata[mask1,4],globaldata[mask1,24]])),
                np.transpose(np.array([globaldata[mask1,4],globaldata[mask1,25]])),
                np.transpose(np.array([globaldata[mask2,4],globaldata[mask2,-3]])),
                np.transpose(np.array([globaldata[mask2,4],globaldata[mask2,-2]])),
                np.transpose(np.array([globaldata[mask2,4],globaldata[mask2,-1]]))]
        dataoptions = ['red,smooth,mark=square*','red,smooth,mark=triangle*','red,smooth,mark=*','black,smooth,mark=square*','black,smooth,mark=triangle*','black,smooth,mark=*']
        writeLatexMultiplePlots(outdir,prefix,join(outdir,prefix,'tex'),prefix + '_M-F-VCCT' + '_Summary',data,axoptions,dataoptions)
    except Exception,error:
        print(error)
    
    try:
        legendEntries = ''
        for i in range(0,ncontInt):
            if i>0:
                legendEntries += ','
            legendEntries += '{$\\frac{G_{TOT}}{G_{0}}$, FEM, Contour ' + str(i+1) + '}'
        legendEntries += ',{$\\frac{G_{TOT}}{G_{0}}$, BEM}'
        axoptions = 'width=30cm,\n' \
                    'title={Normalized total energy release rate $\\frac{G_{TOT}}{G_{0}}$ as function of crack angular semi-aperture  $\\Delta\\theta$, calculated with Abaqus built-in J-Integral post-processing routine (*CONTOUR INTEGRAL)},\n' \
                    'title style={font=\\fontsize{16}{8}\\selectfont},\n' \
                    'xlabel style={at={(axis description cs:0.5,-0.02)},anchor=north,font=\\fontsize{16}{8}\\selectfont},\n' \
                    'ylabel style={at={(axis description cs:-0.01,.5)},anchor=south,font=\\fontsize{16}{8}\\selectfont},\n' \
                    'xlabel={$\\Delta\\theta\\left[^{\\circ}\\right]$},ylabel={$\\frac{G_{TOT}}{G_{0}}\\left[-\\right]$},\n' \
                    'xmin=0.0,\n' \
                    'xmax=180.0,\n' \
                    'ymin=0.0,\n' \
                    'ymax=' + str(1.05*np.max([np.max(globaldata[:,indexStartJINTs+ncontInt:indexStartJINTs+2*ncontInt-1]),np.max(globaldata[:,-1])])) + ',\n' \
                    'tick align=outside,\n' \
                    'tick label style={font=\\normalsize},\n' \
                    'xtick={0.0,10.0,20.0,30.0,40.0,50.0,60.0,70.0,80.0,90.0,100.0,110.0,120.0,130.0,140.0,150.0,160.0,170.0,180.0},\n' \
                    'xmajorgrids,\n' \
                    'x grid style={lightgray!92.026143790849673!black},\n' \
                    'ymajorgrids,\n' \
                    'y grid style={lightgray!92.026143790849673!black},\n' \
                    'line width=0.35mm,\n' \
                    'legend style={draw=white!80.0!black,font=\\fontsize{6}{6}\\selectfont},\n' \
                    'legend entries={' + legendEntries + '},\n' \
                    'legend cell align={left}\n'
        mask1 = (globaldata[:,4] > 0) & (globaldata[:,4] < 151) & (globaldata[:,indexStartJINTs+ncontInt] != None)
        mask2 = (globaldata[:,4] > 0) & (globaldata[:,4] < 151) & (globaldata[:,-1] != None) & (globaldata[:,-2] != None) & (globaldata[:,-3] != None)
        data = []
        for i in range(0,ncontInt):
            data.append(np.transpose(np.array([globaldata[mask1,4],globaldata[mask1,indexStartJINTs+ncontInt+i]])))
        data.append(np.transpose(np.array([globaldata[mask2,4],globaldata[mask2,-1]])))
        dataoptions = []
        for i in range(0,ncontInt):
            dataoptions.append('red!' + str(i*100.0/(ncontInt-1)) + '!blue,smooth,mark=*') 
        dataoptions.append('black,smooth,mark=*')    
        writeLatexMultiplePlots(outdir,prefix,join(outdir,prefix,'tex'),prefix + '_J-INT' + '_Summary',data,axoptions,dataoptions)
    except Exception,error:
        print(error)
    
    try:
        legendEntries = '{$\\frac{G_{I}}{G_{0}}$, FEM-F-VCCT},{$\\frac{G_{II}}{G_{0}}$, FEM-F-VCCT},{$\\frac{G_{I}+G_{II}}{G_{0}}$, FEM-F-VCCT}'
        for i in range(0,ncontInt):
            legendEntries += ',{$\\frac{G_{TOT}}{G_{0}}$, FEM-JINT, Contour ' + str(i+1) + '}'
        legendEntries += ',{$\\frac{G_{I}}{G_{0}}$, BEM},{$\\frac{G_{II}}{G_{0}}$, BEM},{$\\frac{G_{I}+G_{II}}{G_{0}}$, BEM}'
        axoptions = 'width=30cm,\n' \
                    'title={Normalized energy release rate $\\frac{G_{\\left(\\cdot\\cdot\\right)}}{G_{0}}$ as function of crack angular semi-aperture  $\\Delta\\theta$, calculated with in-house force-based VCCT and Abaqus built-in J-Integral (*CONTOUR INTEGRAL) post-processing routines},\n' \
                    'title style={font=\\fontsize{16}{8}\\selectfont},\n' \
                    'xlabel style={at={(axis description cs:0.5,-0.02)},anchor=north,font=\\fontsize{16}{8}\\selectfont},\n' \
                    'ylabel style={at={(axis description cs:-0.01,.5)},anchor=south,font=\\fontsize{16}{8}\\selectfont},\n' \
                    'xlabel={$\\Delta\\theta\\left[^{\\circ}\\right]$},ylabel={$\\frac{G_{\\left(\\cdot\\cdot\\right)}}{G_{0}}\\left[-\\right]$},\n' \
                    'xmin=0.0,\n' \
                    'xmax=180.0,\n' \
                    'ymin=0.0,\n' \
                    'ymax=' + str(1.05*np.max([np.max(globaldata[:,25]),np.max(globaldata[:,indexStartJINTs+ncontInt:indexStartJINTs+2*ncontInt-1]),np.max(globaldata[:,-1])])) + ',\n' \
                    'tick align=outside,\n' \
                    'tick label style={font=\\normalsize},\n' \
                    'xtick={0.0,10.0,20.0,30.0,40.0,50.0,60.0,70.0,80.0,90.0,100.0,110.0,120.0,130.0,140.0,150.0,160.0,170.0,180.0},\n' \
                    'xmajorgrids,\n' \
                    'x grid style={lightgray!92.026143790849673!black},\n' \
                    'ymajorgrids,\n' \
                    'y grid style={lightgray!92.026143790849673!black},\n' \
                    'line width=0.35mm,\n' \
                    'legend style={draw=white!80.0!black,font=\\fontsize{6}{6}\\selectfont},\n' \
                    'legend entries={' + legendEntries + '},\n' \
                    'legend cell align={left}\n'
        mask1 = (globaldata[:,4] > 0) & (globaldata[:,4] < 151) & (globaldata[:,23] != None) & (globaldata[:,24] != None) & (globaldata[:,25] != None) & (globaldata[:,indexStartJINTs+ncontInt] != None)
        mask2 = (globaldata[:,4] > 0) & (globaldata[:,4] < 151) & (globaldata[:,-1] != None) & (globaldata[:,-2] != None) & (globaldata[:,-3] != None)
        data = [np.transpose(np.array([globaldata[mask1,4],globaldata[mask1,23]])),
                np.transpose(np.array([globaldata[mask1,4],globaldata[mask1,24]])),
                np.transpose(np.array([globaldata[mask1,4],globaldata[mask1,25]]))]
        for i in range(0,ncontInt):
            data.append(np.transpose(np.array([globaldata[mask1,4],globaldata[mask1,indexStartJINTs+ncontInt+i]])))
        data.append(np.transpose(np.array([globaldata[mask2,4],globaldata[mask2,-3]])))
        data.append(np.transpose(np.array([globaldata[mask2,4],globaldata[mask2,-2]])))
        data.append(np.transpose(np.array([globaldata[mask2,4],globaldata[mask2,-1]])))
        dataoptions = ['green,smooth,mark=square*','green,smooth,mark=triangle*','green,smooth,mark=*']
        for i in range(0,ncontInt):
            dataoptions.append('red!' + str(i*100.0/(ncontInt-1)) + '!blue,smooth,mark=*') 
        dataoptions.append('black,smooth,mark=square*') 
        dataoptions.append('black,smooth,mark=triangle*') 
        dataoptions.append('black,smooth,mark=*')    
        writeLatexMultiplePlots(outdir,prefix,join(outdir,prefix,'tex'),prefix + '_F-VCCT-JINT' + '_Summary',data,axoptions,dataoptions)
    except Exception,error:
        print(error)
    
    try:
        legendEntries = '{$\\frac{G_{I}}{G_{0}}$, FEM-F-VCCT},{$\\frac{G_{II}}{G_{0}}$, FEM-F-VCCT},{$\\frac{G_{I}+G_{II}}{G_{0}}$, FEM-F-VCCT}'
        for i in range(0,numGs):
            legendEntries += ',{$\\frac{G_{I}}{G_{0}}$, FEM-SoM-VCCT, N Int El ' + str(i+1) + '},{$\\frac{G_{II}}{G_{0}}$, FEM-SoM-VCCT, N Int El ' + str(i+1) + '},{$\\frac{G_{I}+G_{II}}{G_{0}}$, FEM-SoM-VCCT, N Int El ' + str(i+1) + '}'
        legendEntries += ',{$\\frac{G_{I}}{G_{0}}$, BEM},{$\\frac{G_{II}}{G_{0}}$, BEM},{$\\frac{G_{I}+G_{II}}{G_{0}}$, BEM}'
        axoptions = 'width=30cm,\n' \
                    'title={Normalized energy release rate $\\frac{G_{\\left(\\cdot\\cdot\\right)}}{G_{0}}$ as function of crack angular semi-aperture  $\\Delta\\theta$, calculated with in-house force-based and stress-based VCCT post-processing routines with stresses extracted on the matrix side of the interface},\n' \
                    'title style={font=\\fontsize{16}{8}\\selectfont},\n' \
                    'xlabel style={at={(axis description cs:0.5,-0.02)},anchor=north,font=\\fontsize{16}{8}\\selectfont},\n' \
                    'ylabel style={at={(axis description cs:-0.01,.5)},anchor=south,font=\\fontsize{16}{8}\\selectfont},\n' \
                    'xlabel={$\\Delta\\theta\\left[^{\\circ}\\right]$},ylabel={$\\frac{G_{\\left(\\cdot\\cdot\\right)}}{G_{0}}\\left[-\\right]$},\n' \
                    'xmin=0.0,\n' \
                    'xmax=180.0,\n' \
                    'ymin=0.0,\n' \
                    'ymax=' + str(1.05*np.max([np.max(globaldata[:,25]),np.max(globaldata[:,indexStartStressesVCCT+5*numGs:indexStartStressesVCCT+6*numGs-1]),np.max(globaldata[:,-1])])) + ',\n' \
                    'tick align=outside,\n' \
                    'tick label style={font=\\normalsize},\n' \
                    'xtick={0.0,10.0,20.0,30.0,40.0,50.0,60.0,70.0,80.0,90.0,100.0,110.0,120.0,130.0,140.0,150.0,160.0,170.0,180.0},\n' \
                    'xmajorgrids,\n' \
                    'x grid style={lightgray!92.026143790849673!black},\n' \
                    'ymajorgrids,\n' \
                    'y grid style={lightgray!92.026143790849673!black},\n' \
                    'line width=0.35mm,\n' \
                    'legend style={draw=white!80.0!black,font=\\fontsize{6}{6}\\selectfont},\n' \
                    'legend entries={' + legendEntries + '},\n' \
                    'legend cell align={left}\n'
        mask1 = (globaldata[:,4] > 0) & (globaldata[:,4] < 151)  
        data = [np.transpose(np.array([globaldata[mask1,4],globaldata[mask1,23]])),
                np.transpose(np.array([globaldata[mask1,4],globaldata[mask1,24]])),
                np.transpose(np.array([globaldata[mask1,4],globaldata[mask1,25]]))]
        for i in range(0,numGs):
            data.append(np.transpose(np.array([globaldata[mask1,4],globaldata[mask1,indexStartStressesVCCT+3*numGs+i]])))
            data.append(np.transpose(np.array([globaldata[mask1,4],globaldata[mask1,indexStartStressesVCCT+4*numGs+i]])))
            data.append(np.transpose(np.array([globaldata[mask1,4],globaldata[mask1,indexStartStressesVCCT+5*numGs+i]])))
        data.append(np.transpose(np.array([globaldata[mask1,4],globaldata[mask1,-3]])))
        data.append(np.transpose(np.array([globaldata[mask1,4],globaldata[mask1,-2]])))
        data.append(np.transpose(np.array([globaldata[mask1,4],globaldata[mask1,-1]])))          
        dataoptions = ['green,smooth,mark=square*','green,smooth,mark=triangle*','green,smooth,mark=*']
        for i in range(0,numGs):
            dataoptions.append('red!' + str(i*100.0/(numGs-1)) + '!blue,smooth,mark=square*') 
            dataoptions.append('red!' + str(i*100.0/(numGs-1)) + '!blue,smooth,mark=triangle*') 
            dataoptions.append('red!' + str(i*100.0/(numGs-1)) + '!blue,smooth,mark=*')
        dataoptions.append('black,smooth,mark=square*') 
        dataoptions.append('black,smooth,mark=triangle*') 
        dataoptions.append('black,smooth,mark=*')
        writeLatexMultiplePlots(outdir,prefix,join(outdir,prefix,'tex'),prefix + '_F-SoM-VCCT' + '_Summary',data,axoptions,dataoptions)
    except Exception,error:
        print(error)
    
    try:
        legendEntries = '{$\\frac{G_{I}}{G_{0}}$, FEM-F-VCCT},{$\\frac{G_{II}}{G_{0}}$, FEM-F-VCCT},{$\\frac{G_{I}+G_{II}}{G_{0}}$, FEM-F-VCCT}'
        for i in range(0,numGs):
            legendEntries += ',{$\\frac{G_{I}}{G_{0}}$, FEM-SoF-VCCT, N Int El ' + str(i+1) + '},{$\\frac{G_{II}}{G_{0}}$, FEM-SoF-VCCT, N Int El ' + str(i+1) + '},{$\\frac{G_{I}+G_{II}}{G_{0}}$, FEM-SoF-VCCT, N Int El ' + str(i+1) + '}'
        legendEntries += ',{$\\frac{G_{I}}{G_{0}}$, BEM},{$\\frac{G_{II}}{G_{0}}$, BEM},{$\\frac{G_{I}+G_{II}}{G_{0}}$, BEM}'
        axoptions = 'width=30cm,\n' \
                    'title={Normalized energy release rate $\\frac{G_{\\left(\\cdot\\cdot\\right)}}{G_{0}}$ as function of crack angular semi-aperture  $\\Delta\\theta$, calculated with in-house force-based and stress-based VCCT post-processing routines with stresses extracted on the fiber side of the interface},\n' \
                    'title style={font=\\fontsize{16}{8}\\selectfont},\n' \
                    'xlabel style={at={(axis description cs:0.5,-0.02)},anchor=north,font=\\fontsize{16}{8}\\selectfont},\n' \
                    'ylabel style={at={(axis description cs:-0.01,.5)},anchor=south,font=\\fontsize{16}{8}\\selectfont},\n' \
                    'xlabel={$\\Delta\\theta\\left[^{\\circ}\\right]$},ylabel={$\\frac{G_{\\left(\\cdot\\cdot\\right)}}{G_{0}}\\left[-\\right]$},\n' \
                    'xmin=0.0,\n' \
                    'xmax=180.0,\n' \
                    'ymin=0.0,\n' \
                    'ymax=' + str(1.05*np.max([np.max(globaldata[:,25]),np.max(globaldata[:,indexStartStressesVCCT+11*numGs:indexStartStressesVCCT+12*numGs-1]),np.max(globaldata[:,-1])])) + ',\n' \
                    'tick align=outside,\n' \
                    'tick label style={font=\\normalsize},\n' \
                    'xtick={0.0,10.0,20.0,30.0,40.0,50.0,60.0,70.0,80.0,90.0,100.0,110.0,120.0,130.0,140.0,150.0,160.0,170.0,180.0},\n' \
                    'xmajorgrids,\n' \
                    'x grid style={lightgray!92.026143790849673!black},\n' \
                    'ymajorgrids,\n' \
                    'y grid style={lightgray!92.026143790849673!black},\n' \
                    'line width=0.35mm,\n' \
                    'legend style={draw=white!80.0!black,font=\\fontsize{6}{6}\\selectfont},\n' \
                    'legend entries={' + legendEntries + '},\n' \
                    'legend cell align={left}\n'
        mask1 = (globaldata[:,4] > 0) & (globaldata[:,4] < 151)
        data = [np.transpose(np.array([globaldata[mask1,4],globaldata[mask1,23]])),
                np.transpose(np.array([globaldata[mask1,4],globaldata[mask1,24]])),
                np.transpose(np.array([globaldata[mask1,4],globaldata[mask1,25]]))]
        for i in range(0,numGs):
            data.append(np.transpose(np.array([globaldata[mask1,4],globaldata[mask1,indexStartStressesVCCT+9*numGs+i]])))
            data.append(np.transpose(np.array([globaldata[mask1,4],globaldata[mask1,indexStartStressesVCCT+10*numGs+i]])))
            data.append(np.transpose(np.array([globaldata[mask1,4],globaldata[mask1,indexStartStressesVCCT+11*numGs+i]])))
        data.append(np.transpose(np.array([globaldata[mask1,4],globaldata[mask1,-3]])))
        data.append(np.transpose(np.array([globaldata[mask1,4],globaldata[mask1,-2]])))
        data.append(np.transpose(np.array([globaldata[mask1,4],globaldata[mask1,-1]])))            
        dataoptions = ['green,smooth,mark=square*','green,smooth,mark=triangle*','green,smooth,mark=*']
        for i in range(0,numGs):
            dataoptions.append('red!' + str(i*100.0/(numGs-1)) + '!blue,smooth,mark=square*') 
            dataoptions.append('red!' + str(i*100.0/(numGs-1)) + '!blue,smooth,mark=triangle*') 
            dataoptions.append('red!' + str(i*100.0/(numGs-1)) + '!blue,smooth,mark=*')
        dataoptions.append('black,smooth,mark=square*') 
        dataoptions.append('black,smooth,mark=triangle*') 
        dataoptions.append('black,smooth,mark=*')
        writeLatexMultiplePlots(outdir,prefix,join(outdir,prefix,'tex'),prefix + '_F-SoF-VCCT' + '_Summary',data,axoptions,dataoptions)
    except Exception,error:
        print(error)
        
def main(argv):

    matdatafolder = 'D:/OneDrive/01_Luca/07_DocMASE/07_Data/02_Material-Properties'
    
    refdatafolder = 'D:/OneDrive/01_Luca/07_DocMASE/07_Data/01_References/Verification-Data'
    refdatafilename = 'BEM-data.csv'
    
    #wd = 'D:/01_Luca/07_Data/03_FEM'
    #wd = 'H:/01_Luca/07_DocMASE/07_Data/03_FEM'
    #wd = 'D:/01_Luca/07_Data/03_FEM/StraightInterface/Full'
    wd = 'D:/01_Luca/07_Data/03_FEM/CurvedInterface'
    #wd = 'H:/01_Luca/07_DocMASE/07_Data/03_FEM/CurvedInterface'
    
    #statusfile = '2017-06-23_AbaqusParametricRun_FiniteStrain.sta'
    #statusfile = '2017-06-23_AbaqusParametricRun_SmallStrain.sta'
    
    outdir = 'D:/OneDrive/01_Luca/07_DocMASE/07_Data/03_FEM'

    #prefix = '2017-06-23_AbqRunSummary_SingleFiberEqRfFiniteStrain'
    #prefix = '2017-06-23_AbqRunSummary_SingleFiberEqRfSmallStrain'
    
    statusfiles = ['2017-07-10_AbqRunSummary_SmallStrainD10',
                   '2017-07-10_AbqRunSummary_SmallStrainD09']
    
    prefixes = ['2017-07-20_AbqRunSummary_SmallStrain_D10',
                '2017-07-20_AbqRunSummary_SmallStrain_D09']
    
    '''
    statusfiles = ['2017-07-10_AbqRunSummary_SmallStrainD08',
                   '2017-07-10_AbqRunSummary_SmallStrainD07',
                   '2017-07-10_AbqRunSummary_SmallStrainD06',
                   '2017-07-10_AbqRunSummary_SmallStrainD05',
                   '2017-07-10_AbqRunSummary_SmallStrainD04',
                   '2017-07-10_AbqRunSummary_SmallStrainD03'
                   '2017-07-10_AbqRunSummary_SmallStrainD02',
                   '2017-07-10_AbqRunSummary_SmallStrainD01']
    
    prefixes = ['2017-07-20_AbqRunSummary_SmallStrain_D08',
                '2017-07-20_AbqRunSummary_SmallStrain_D07',
                '2017-07-20_AbqRunSummary_SmallStrain_D06',
                '2017-07-20_AbqRunSummary_SmallStrain_D05',
                '2017-07-20_AbqRunSummary_SmallStrain_D04',
                '2017-07-20_AbqRunSummary_SmallStrain_D03',
                '2017-07-20_AbqRunSummary_SmallStrain_D02',
                '2017-07-20_AbqRunSummary_SmallStrain_D01']
    '''

    
    ncontInt = 20
    NEl0 = 1 
    NElMax = 20
    DeltaEl = 1
    #joinEnergyReleaseDataOverSims(wd,statusfile,matdatafolder,outdir,prefix,10)
    #joinOnlyENRRTsDataOverSims(wd,statusfile,matdatafolder,outdir,prefix)
    #joinOnlyENRRTsDataOverSiPlateSims(wd,statusfile,matdatafolder,outdir,prefix)
    #joinERRTsDataOverSimsExtSet04(wd,statusfile,refdatafolder,refdatafilename,outdir,prefix,ncontInt)

    for s,statusfile in enumerate(statusfiles):
        joinERRTsDataOverSimsExtSet04(wd,statusfile,refdatafolder,refdatafilename,outdir,prefixes[s],ncontInt,NEl0,NElMax,DeltaEl)        

if __name__ == "__main__":
    main(sys.argv[1:])