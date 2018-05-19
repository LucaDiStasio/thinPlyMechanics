#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
=====================================================================================

Copyright (c) 2016-2018 Universite de Lorraine & Lulea tekniska universitet
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

import os
from os.path import join
from datetime import datetime
from time import strftime, sleep
from platform import platform
import getopt
import numpy as np
from odbAccess import *
from abaqusConstants import *
from odbMaterial import *
from odbSection import *
import re

#===============================================================================#
#===============================================================================#
#                              I/O functions
#===============================================================================#
#===============================================================================#

#===============================================================================#
#                                 Log files
#===============================================================================#

def writeLineToLogFile(logFileFullPath,mode,line,toScreen):
    with open(logFileFullPath,mode) as log:
        log.write(line + '\n')
    if toScreen:
        print >> sys.__stdout__,(line + '\n')

def skipLineToLogFile(logFileFullPath,mode,toScreen):
    with open(logFileFullPath,mode) as log:
        log.write('\n')
    if toScreen:
        print >> sys.__stdout__,('\n')


#===============================================================================#
#===============================================================================#
#                      Data extraction functions
#===============================================================================#
#===============================================================================#

def getFrame(odbObj,step,frame):
    return odbObj.steps[odbObj.steps.keys()[step]].frames[frame]

def getFirstAndLastFrame(odbObj,step):
    return getFrame(odbObj,step,0),getFrame(odbObj,step,-1)

def getFirstAndLastFrameLastStep(odbObj):
    first, last = getFirstAndLastFrame(odbObj,-1)
    return first, last

def getSingleNodeSet(odbObj,part,nodeSet):
    if part==None:
        result = odbObj.rootAssembly.nodeSets[nodeSet]
    else:
        result = odbObj.rootAssembly.instances[part].nodeSets[nodeSet]
    return result

def getSingleElementSet(odbObj,part,set):
    return odbObj.rootAssembly.instances[part].elementSets[set]

def getSingleSetNodeCoordinates(odbObj,step,frame,part,nodeSet):
    frameObj = getFrame(odbObj,step,frame)
    allCoords = frameObj.fieldOutputs['COORD'].getSubset(position=NODAL)
    coords = nodesCoords.getSubset(region=odbObj.rootAssembly.instances[part].nodeSets[nodeSet])
    return coords

def getMultipleSetsNodeCoordinates(odbObj,nodeSets):
    coords = {}
    for set in nodeSets:
        step = set[0]
        frame = set[1]
        part = set[2]
        nodeSet = set[3]
        coords[nodeSet] = getSingleSetNodeCoordinates(odbObj,step,frame,part,nodeSet)
    return coords

def extractAndSaveNodesCoordinates(odbObj,nodeSetsData,folder,filename,ext):
    nodeSets = getMultipleSetsNodeCoordinates(odbObj,nodeSetsData)
    with open(join(folder,filename + ext),'w') as csv:
        if len(nodeSets[set[3]].values[0].data)==1:
            string = 'X'
        elif len(nodeSets[set[3]].values[0].data)==2:
            string = 'X, Y'
        elif len(nodeSets[set[3]].values[0].data)==3:
            string = 'X, Y, Z'
        csv.write('DATA\n')
        csv.write('NODE SET' + ', ' + 'NODE TYPE, NODE LABEL, ' + string + '\n')
        for set in nodeSetsData:
            for value in nodeSets[set[3]].values:
                line = ''
                line = set[3] + ', ' + 'NODAL' + ', ' + str(value.nodeLabel)
                for datum in value.data:
                    line += ', ' + str(datum)
                csv.write(line + '\n')

def getAllNodes(odbObj,step,frameN):
    allNodes = {}
    frame = getFrame(odbObj,step,frameN)
    nodesCoords = frame.fieldOutputs['COORD'].getSubset(position=NODAL)
    for value in nodesCoords.values:
        components = []
        for component in value.data:
            components.append(component)
        allNodes[str(value.nodeLabel)] = components
    return allNodes

def getAndSaveAllNodes(odbObj,step,frameN,folder,filename,ext):
    allNodes = {}
    frame = getFrame(odbObj,step,frameN)
    nodesCoords = frame.fieldOutputs['COORD'].getSubset(position=NODAL)
    for value in nodesCoords.values:
        components = []
        for component in value.data:
            components.append(component)
        allNodes[str(value.nodeLabel)] = components
    with open(join(folder,filename + ext),'w') as csv:
        if len(nodesCoords.values[0].data)==1:
            string = 'X'
        elif len(nodesCoords.values[0].data)==2:
            string = 'X, Y'
        elif len(nodesCoords.values[0].data)==3:
            string = 'X, Y, Z'
        csv.write('DATA\n')
        csv.write('NODE TYPE, NODE LABEL, ' + string + '\n')
        for value in nodesCoords.values:
            line = ''
            line = 'NODAL' + ', ' + str(value.nodeLabel)
            for datum in value.data:
                line += ', ' + str(datum)
            csv.write(line + '\n')
    return allNodes

def getAllIntPoints(odbObj,step,frameN):
    allIntPoints = {}
    frame = getFrame(odbObj,step,frameN)
    intpointCoords = frame.fieldOutputs['COORD'].getSubset(position=INTEGRATION_POINT)
    for value in intpointCoords.values:
        components = []
        for component in value.data:
            components.append(component)
        allIntPoints[str(value.elementLabel)+'-'+str(value.integrationPoint)] = components
    return allIntPoints

def getAndSaveAllIntPoints(odbObj,step,frameN,folder,filename,ext):
    allIntPoints = {}
    frame = getFrame(odbObj,step,frameN)
    intpointCoords = frame.fieldOutputs['COORD'].getSubset(position=INTEGRATION_POINT)
    for value in intpointCoords.values:
        components = []
        for component in value.data:
            components.append(component)
        allIntPoints[str(value.elementLabel)+'-'+str(value.integrationPoint)] = components
    with open(join(folder,filename + ext),'w') as csv:
        if len(intpointCoords.values[0].data)==1:
            string = 'X'
        elif len(intpointCoords.values[0].data)==2:
            string = 'X, Y'
        elif len(intpointCoords.values[0].data)==3:
            string = 'X, Y, Z'
        csv.write('DATA\n')
        csv.write('NODE TYPE, NODE LABEL, ' + string + '\n')
        for value in intpointCoords.values:
            line = ''
            line = 'INTEGRATION_POINT' + ', ' + str(value.elementLabel)+'-'+str(value.integrationPoint)
            for datum in value.data:
                line += ', ' + str(datum)
            csv.write(line + '\n')
    return allIntPoints

def getFieldOutput(odbObj,step,frame,fieldOutput,subset=None,pos=None):
    frame = getFrame(odbObj,step,frame)
    if subset!=None:
        if pos==1:
            out = frame.fieldOutputs[fieldOutput].getSubset(region=subset,position=INTEGRATION_POINT)
        elif pos==2:
            out = frame.fieldOutputs[fieldOutput].getSubset(region=subset,position=NODAL)
        elif pos==3:
            out = frame.fieldOutputs[fieldOutput].getSubset(region=subset,position=ELEMENT_NODAL)
        elif pos==4:
            out = frame.fieldOutputs[fieldOutput].getSubset(region=subset,position=CENTROID)
        else:
            out = frame.fieldOutputs[fieldOutput].getSubset(region=subset)
    else:
        out = frame.fieldOutputs[fieldOutput]
    return out

def extractAndSaveFieldOutput(odbObj,step,frameN,folder,filename,ext,fieldOutput,subset=None,pos=None):
    frame = getFrame(odbObj,step,frameN)
    nodes = getAllNodes(odbObj,step,frameN)
    intpoints = getAllIntPoints(odbObj,step,frameN)
    if subset!=None:
        if pos==1:
            out = frame.fieldOutputs[fieldOutput].getSubset(region=subset,position=INTEGRATION_POINT)
        elif pos==2:
            out = frame.fieldOutputs[fieldOutput].getSubset(region=subset,position=NODAL)
        elif pos==3:
            out = frame.fieldOutputs[fieldOutput].getSubset(region=subset,position=ELEMENT_NODAL)
        elif pos==4:
            out = frame.fieldOutputs[fieldOutput].getSubset(region=subset,position=CENTROID)
        else:
            out = frame.fieldOutputs[fieldOutput].getSubset(region=subset)
    else:
        out = frame.fieldOutputs[fieldOutput]
    with open(join(folder,filename + ext),'w') as csv:
        if fieldOutput== 'U' or fieldOutput=='RF':
            if len(out.values[0].data)==1:
                string = 'X, ' + fieldOutput + '1'
            elif len(out.values[0].data)==2:
                string = 'X, Y, '  + fieldOutput + '1' + ', ' + fieldOutput + '2'
            elif len(out.values[0].data)==3:
                string = 'X, Y, Z, '  + fieldOutput + '1' + ', ' + fieldOutput + '2' + ', ' + fieldOutput + '3'
        elif fieldOutput== 'S' or fieldOutput=='EE':
            if len(out.values[0].data)==2:
                string = 'X, ' + fieldOutput + '11' + ', '  + fieldOutput + '12'
            elif len(out.values[0].data)==4:
                string = 'X, Y, '  + fieldOutput + '11' + ', ' + fieldOutput + '22' + ', ' + fieldOutput + '33' + ', ' + fieldOutput + '12'
            elif len(out.values[0].data)==6:
                string = 'X, Y, Z, '  + fieldOutput + '11' + ', ' + fieldOutput + '22' + ', ' + fieldOutput + '33' + ', ' + fieldOutput + '12' + ', ' + fieldOutput + '13' + ', ' + fieldOutput + '23'
        csv.write('HEAT MAP\n')
        csv.write('NODE TYPE, NODE LABEL, ' + string + '\n')
        for value in out.values:
            if 'NODAL' in str(value.position):
                line = ''
                line = 'NODAL' + ', ' + str(value.nodeLabel)
                for datum in nodes[str(value.nodeLabel)]:
                    line += ', ' + str(datum)
                for datum in value.data:
                    line += ', ' + str(datum)
                csv.write(line + '\n')
            elif 'INTEGRATION_POINT' in str(value.position):
                line = ''
                line = 'INTEGRATION_POINT' + ', ' + str(value.elementLabel)+'-'+str(value.integrationPoint)
                for datum in intpoints[str(value.elementLabel)+'-'+str(value.integrationPoint)]:
                    line += ', ' + str(datum)
                for datum in value.data:
                    line += ', ' + str(datum)
                csv.write(line + '\n')

def calculateFiberAreaChange(logfilepath,baselogindent,logindent,wd,outDir,odbname):
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + 'In function: calculateFiberAreaChange(logfilepath,baselogindent,logindent,wd,odbname)',True)
    #=======================================================================
    # BEGIN - open ODB
    #=======================================================================
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Opening ODB database ' + odbname + ' in directory ' + wd + ' ...',True)
    if '.odb' not in odbname:
        odbname += '.odb'
    odbfullpath = join(wd,odbname)
    odb = openOdb(path=odbfullpath)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    #=======================================================================
    # END - open ODB
    #=======================================================================
    #=======================================================================
    # BEGIN - extract node sets
    #=======================================================================
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Extracting node sets ...',True)

    thirdcircle = getSingleNodeSet(odb,'RVE-ASSEMBLY','THIRDCIRCLE')
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '-- THIRDCIRCLE',True)

    matrixcrackface = getSingleNodeSet(odb,None,'MATRIX-CRACKFACE-NODES')
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '-- MATRIX-CRACKFACE-NODES',True)

    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '.. done.',True)

    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Extracting undeformed and deformed coordinates ...',True)

    thirdcircleundefCoords = getFieldOutput(odb,-1,0,'COORD',thirdcircle)
    thirdcircledefCoords = getFieldOutput(odb,-1,1,'COORD',thirdcircle)

    matrixcrackfaceundefCoords = getFieldOutput(odb,-1,0,'COORD',matrixcrackface)
    matrixcrackfacedefCoords = getFieldOutput(odb,-1,1,'COORD',matrixcrackface)

    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '.. done.',True)

    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Filter undeformed and deformed coordinates ...',True)

    undefPoints = []
    defPoints = []

    matrixcrackfaceNodeLabels = []
    for value in matrixcrackfaceundefCoords.values:
        matrixcrackfaceNodeLabels.append(value.nodeLabel)

    for value in thirdcircleundefCoords.values:
        if not value.nodeLabel in matrixcrackfaceNodeLabels:
            undefPoints.append([value.data[0],value.data[1]])

    for value in thirdcircledefCoords.values:
        if not value.nodeLabel in matrixcrackfaceNodeLabels:
            defPoints.append([value.data[0],value.data[1]])

    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '.. done.',True)

    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Compute area by trapezoidal integration ...',True)

    undefPoints = np.array(undefPoints)
    undefPoints = undefPoints[np.argsort(undefPoints[:,0])]
    defPoints = np.array(defPoints)
    defPoints = defPoints[np.argsort(defPoints[:,0])]

    undefA = 0.0
    defA = 0.0

    for p in range(1,len(undefPoints)):
        undefA += 0.5*(undefPoints[p,1]+undefPoints[p-1,1])*(undefPoints[p,0]-undefPoints[p-1,0])
        defA += 0.5*(defPoints[p,1]+defPoints[p-1,1])*(defPoints[p,0]-defPoints[p-1,0])

    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '.. done.',True)
    
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Save fiber profiles to files...',True)
    with open(join(outDir,datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '_FiberProfiles' + '.csv'),'w') as csv:
        csv.write('x0 [um], y0 [um], x [um], y [um]' + '\n')
        for p in range(0,len(undefPoints)):
            line = ''
            for v,value in enumerate([undefPoints[p,0],undefPoints[p,1],defPoints[p,0],defPoints[p,1]]):
                if v>0:
                    line += ', '
                line += str(value)
        csv.write(line + '\n')
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '.. done.',True)
    
    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + 'Exiting function: calculateFiberAreaChange(logfilepath,baselogindent,logindent,wd,odbname)',True)

    return [0.5*np.pi,undefA,defA,defA/undefA,100.0*defA/undefA,defA-undefA,(defA-undefA)/undefA]

def main(argv):

    workDir = 'C:/Abaqus_WD'
    inpDir = 'C:/Abaqus_WD'
    outdir = 'C:/Users/lucad/OneDrive/01_Luca/07_DocMASE/07_Data/03_FEM/FiberVolumeChange'

    odbs = ['RVE10',
            'RVE150']

    logfilename = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '_fiberVolumeChange' + '.log'
    logfilefullpath = join(workDir,logfilename)
    logindent = '    '

    if not os.path.exists(outdir):
            os.mkdir(outdir)

    with open(logfilefullpath,'w') as log:
        log.write('Calculation of fiber volume change with Abaqus Python' + '\n')

    results = []
    for odb in odbs:
        results.append(calculateFiberAreaChange(logfilefullpath,'',logindent,inpDir,outdir,odb))

    with open(join(outdir,datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '_fiberVolumeChange' + '.csv'),'w') as csv:
        csv.write('theoretical area [um^2], undeformed area [um^2], deformed area [um^2], ratio [-], ratio [%], change [um], change [%]' + '\n')
        for result in results:
            line = ''
            for v,value in enumerate(result):
                if v>0:
                    line += ', '
                line += str(value)
        csv.write(line + '\n')



if __name__ == "__main__":
    main(sys.argv[1:])
