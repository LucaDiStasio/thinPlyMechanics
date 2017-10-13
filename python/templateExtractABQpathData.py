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
import numpy
import visualization
import xyPlot
from odbAccess import *
from abaqusConstants import *
from odbMaterial import *
from odbSection import *
import re

def extractPathsfromODBoutputSet01(wd,project,deltapsi,nl,nSegsOnPath,tol):
    print('Starting path extraction on project ' + project + '\n')
    # define database name
    odbname = project + '.odb'
    odbfullpath = join(wd,project,'abaqus',odbname)
    # define input file name
    inpname = project + '.inp'
    inpfullpath = join(wd,project,'abqinp',inpname)
    # define csv output folder
    csvfolder = join(wd,project,'csv')
    # open odb
    print('Open odb ' + odbname + ' in folder ' + join(wd,project,'abaqus') + ' ...\n')
    odb = openOdb(path=odbfullpath)
    print('...done.\n')
    #=======================================================================
    # get first and last frame
    #=======================================================================
    print('\n')
    print('Get first and last frame...\n')
    firstFrame = odb.steps[odb.steps.keys()[-1]].frames[0]
    lastFrame = odb.steps[odb.steps.keys()[-1]].frames[-1]
    print('...done.\n')
    #=======================================================================
    # get deformed nodes
    #=======================================================================
    print('\n')
    print('Get deformed nodes...\n')
    nodes = {}
    intpoints = {}
    nodesCoords = lastFrame.fieldOutputs['COORD'].getSubset(position=NODAL)
    intpointCoords = lastFrame.fieldOutputs['COORD'].getSubset(position=INTEGRATION_POINT)
    for value in nodesCoords.values:
        components = []
        for component in value.data:
            components.append(component)
        nodes[str(value.nodeLabel)] = components
    for value in intpointCoords.values:
        components = []
        for component in value.data:
            components.append(component)
        intpoints[str(value.nodeLabel)] = components
    with open(join(csvfolder,'defnodesCoords.csv'),'w') as csv:
        csv.write('DATA\n')
        csv.write('NODE TYPE, NODE LABEL, X, Y\n')
        for value in nodesCoords.values:
            csv.write('NODAL' + ', ' + str(value.nodeLabel) + ', ' + str(value.data[0]) + ', ' + str(value.data[1]) + '\n') 
    with open(join(csvfolder,'defintpointCoords.csv'),'w') as csv:
        csv.write('DATA\n')
        csv.write('NODE TYPE, NODE LABEL, X, Y\n')
        for value in intpointCoords.values:
            csv.write('INTEGRATION-POINTS' + ', ' + str(value.nodeLabel) + ', ' + str(value.data[0]) + ', ' + str(value.data[1]) + '\n')
    defSW = nodesCoords.getSubset(region=odb.rootAssembly.instances['PART-1-1'].nodeSets['SW-CORNERNODE'])
    defSE = nodesCoords.getSubset(region=odb.rootAssembly.instances['PART-1-1'].nodeSets['SE-CORNERNODE'])
    defNE = nodesCoords.getSubset(region=odb.rootAssembly.instances['PART-1-1'].nodeSets['NE-CORNERNODE'])
    defNW = nodesCoords.getSubset(region=odb.rootAssembly.instances['PART-1-1'].nodeSets['NW-CORNERNODE'])
    defLowerSideNoCorn = nodesCoords.getSubset(region=odb.rootAssembly.instances['PART-1-1'].nodeSets['LOWERSIDE-NODES-WITHOUT-CORNERS'])
    defRightSideNoCorn = nodesCoords.getSubset(region=odb.rootAssembly.instances['PART-1-1'].nodeSets['RIGHTSIDE-NODES-WITHOUT-CORNERS'])
    defUpperSideNoCorn = nodesCoords.getSubset(region=odb.rootAssembly.instances['PART-1-1'].nodeSets['UPPERSIDE-NODES-WITHOUT-CORNERS'])
    defLeftSideNoCorn  = nodesCoords.getSubset(region=odb.rootAssembly.instances['PART-1-1'].nodeSets['LEFTSIDE-NODES-WITHOUT-CORNERS'])
    with open(join(csvfolder,'defboundaryNodesCoords.csv'),'w') as csv:
        csv.write('DATA\n')
        csv.write('NODE SET' + ', ' + 'NODE TYPE, NODE LABEL, X, Y\n')
        for value in defSW.values:
            csv.write('SW-CORNER' + ', ' + 'NODAL' + ', ' + str(value.nodeLabel) + ', ' + str(value.data[0]) + ', ' + str(value.data[1]) + '\n')
        for value in defLowerSideNoCorn.values:
            csv.write('LOWERSIDE-NODES-WITHOUT-CORNERS' + ', ' + 'NODAL' + ', ' + str(value.nodeLabel) + ', ' + str(value.data[0]) + ', ' + str(value.data[1]) + '\n')
        for value in defSE.values:
            csv.write('SE-CORNER' + ', ' + 'NODAL' + ', ' + str(value.nodeLabel) + ', ' + str(value.data[0]) + ', ' + str(value.data[1]) + '\n')
        for value in defRightSideNoCorn.values:
            csv.write('RIGHTSIDE-NODES-WITHOUT-CORNERS' + ', ' + 'NODAL' + ', ' + str(value.nodeLabel) + ', ' + str(value.data[0]) + ', ' + str(value.data[1]) + '\n')
        for value in defNE.values:
            csv.write('NE-CORNER' + ', ' + 'NODAL' + ', ' + str(value.nodeLabel) + ', ' + str(value.data[0]) + ', ' + str(value.data[1]) + '\n')
        for value in defUpperSideNoCorn.values:
            csv.write('UPPERSIDE-NODES-WITHOUT-CORNERS' + ', ' + 'NODAL' + ', ' + str(value.nodeLabel) + ', ' + str(value.data[0]) + ', ' + str(value.data[1]) + '\n')
        for value in defNW.values:
            csv.write('NW-CORNER' + ', ' + 'NODAL' + ', ' + str(value.nodeLabel) + ', ' + str(value.data[0]) + ', ' + str(value.data[1]) + '\n')
        for value in defLeftSideNoCorn.values:
            csv.write('LEFTSIDE-NODES-WITHOUT-CORNERS' + ', ' + 'NODAL' + ', ' + str(value.nodeLabel) + ', ' + str(value.data[0]) + ', ' + str(value.data[1]) + '\n')
    defFiberSurf = nodesCoords.getSubset(region=odb.rootAssembly.instances['PART-1-1'].nodeSets['FIBERSURFACE-NODES'])
    defMatrixSurfAtFiberInter = nodesCoords.getSubset(region=odb.rootAssembly.instances['PART-1-1'].nodeSets['MATRIXSURFACEATFIBERINTERFACE-NODES'])
    with open(join(csvfolder,'deffiberInterfaceNodesCoords.csv'),'w') as csv:
        csv.write('DATA\n')
        csv.write('NODE SET, NODE TYPE, NODE LABEL, X, Y\n')
        for value in defFiberSurf.values:
            csv.write('FIBERSURFACE-NODES' + ', ' + 'NODAL' + ', ' + str(value.nodeLabel) + ', ' + str(value.data[0]) + ', ' + str(value.data[1]) + '\n')
        for value in defMatrixSurfAtFiberInter.values:
            csv.write('MATRIXSURFACEATFIBERINTERFACE-NODES' + ', ' + 'NODAL' + ', ' + str(value.nodeLabel) + ', ' + str(value.data[0]) + ', ' + str(value.data[1]) + '\n')
    print('...done.\n')
    #=======================================================================
    # get Rf and l in the deformed configuration
    #=======================================================================
    print('\n')
    print('Get Rf and l in the deformed configuration...\n')
    meanDefRf = 0
    countRf = 0
    for value in defFiberSurf.values:
        countRf += 1
        meanDefRf += numpy.sqrt(numpy.power(value.data[0],2)+numpy.power(value.data[1],2))
    meanDefRf /= countRf
    minL = numpy.minimum(numpy.abs(defSW.values[0].data[0]),numpy.abs(defSW.values[0].data[1]))
    for value in defSW.values:
        if numpy.minimum(numpy.abs(value.data[0]),numpy.abs(value.data[1]))<minL:
            minL = numpy.minimum(numpy.abs(value.data[0]),numpy.abs(value.data[1]))
    for value in defLowerSideNoCorn.values:
        if numpy.abs(value.data[1])<minL:
            minL = numpy.abs(value.data[1])
    for value in defSE.values:
        if numpy.minimum(numpy.abs(value.data[0]),numpy.abs(value.data[1]))<minL:
            minL = numpy.minimum(numpy.abs(value.data[0]),numpy.abs(value.data[1]))
    for value in defRightSideNoCorn.values:
        if numpy.abs(value.data[0])<minL:
            minL = numpy.abs(value.data[0])
    for value in defNE.values:
        if numpy.minimum(numpy.abs(value.data[0]),numpy.abs(value.data[1]))<minL:
            minL = numpy.minimum(numpy.abs(value.data[0]),numpy.abs(value.data[1]))
    for value in defUpperSideNoCorn.values:
        if numpy.abs(value.data[1])<minL:
            minL = numpy.abs(value.data[1])
    for value in defNW.values:
        if numpy.minimum(numpy.abs(value.data[0]),numpy.abs(value.data[1]))<minL:
            minL = numpy.minimum(numpy.abs(value.data[0]),numpy.abs(value.data[1]))
    for value in defLeftSideNoCorn.values:
        if numpy.abs(value.data[0])<minL:
            minL = numpy.abs(value.data[0])
    print('...done.\n')
    #=======================================================================
    # get stresses and strains along radial paths
    #=======================================================================
    print('\n')
    print('Get stresses and strains along radial paths...\n')
    sessionOdb = session.openOdb(name=odbfullpath)
    session.viewports['Viewport: 1'].setValues(displayedObject=sessionOdb)
    psis = numpy.arange(0,360,deltapsi)
    with open(join(csvfolder,'radialpaths.csv'),'w') as csv:
        csv.write('VARIABLE, angle [°], Ri, Rf, FOLDER, FILENAME\n')
    for j,psi in enumerate(psis):
        session.Path(name='Radius-' + str(j+1), type=RADIAL, expression=((0, 0, 0), (0, 0, 1), (minL,0, 0)), circleDefinition=ORIGIN_AXIS, numSegments=nSegsOnPath, radialAngle=psi, startRadius=0, endRadius=CIRCLE_RADIUS)
        radpath = session.paths['Radius-' + str(j+1)]
        # sigmaxx
        sigmaxx = xyPlot.XYDataFromPath(path=radpath,includeIntersections=True,pathStyle=PATH_POINTS,numIntervals=nSegsOnPath,shape=DEFORMED,labelType=TRUE_DISTANCE,variable= ('S',INTEGRATION_POINT, ( (COMPONENT, 'S11' ), ), ))
        session.writeXYReport(fileName=join(wd,project,'dat','sigmaxx-Radius-' + str(j+1) + '.dat'),xyData=sigmaxx,appendMode=OFF)
        with open(join(csvfolder,'radialpaths.csv'),'a') as csv:
            csv.write('S11' + ', ' + str(psi) + ', ' + '0' + ', ' + str(minL) + ', ' + str(join(wd,project,'dat')) + ', ' + 'sigmaxx-Radius-' + str(j+1) + '.dat' + '\n')
        # sigmayy
        sigmayy = xyPlot.XYDataFromPath(path=radpath,includeIntersections=True,pathStyle=PATH_POINTS,numIntervals=nSegsOnPath,shape=DEFORMED,labelType=TRUE_DISTANCE,variable= ('S',INTEGRATION_POINT, ( (COMPONENT, 'S22' ), ), ))
        session.writeXYReport(fileName=join(wd,project,'dat','sigmayy-Radius-' + str(j+1) + '.dat'),xyData=sigmayy,appendMode=OFF)
        with open(join(csvfolder,'radialpaths.csv'),'a') as csv:
            csv.write('S22' + ', ' + str(psi) + ', ' + '0' + ', ' + str(minL) + ', ' + str(join(wd,project,'dat')) + ', ' + 'sigmayy-Radius-' + str(j+1) + '.dat' + '\n')
        # sigmaxy
        sigmaxy = xyPlot.XYDataFromPath(path=radpath,includeIntersections=True,pathStyle=PATH_POINTS,numIntervals=nSegsOnPath,shape=DEFORMED,labelType=TRUE_DISTANCE,variable= ('S',INTEGRATION_POINT, ( (COMPONENT, 'S12' ), ), ))
        session.writeXYReport(fileName=join(wd,project,'dat','sigmaxy-Radius-' + str(j+1) + '.dat'),xyData=sigmaxy,appendMode=OFF)
        with open(join(csvfolder,'radialpaths.csv'),'a') as csv:
            csv.write('S12' + ', ' + str(psi) + ', ' + '0' + ', ' + str(minL) + ', ' + str(join(wd,project,'dat')) + ', ' + 'sigmaxy-Radius-' + str(j+1) + '.dat' + '\n')
        # epsxx
        epsxx = xyPlot.XYDataFromPath(path=radpath,includeIntersections=True,pathStyle=PATH_POINTS,numIntervals=nSegsOnPath,shape=DEFORMED,labelType=TRUE_DISTANCE,variable= ('EE',INTEGRATION_POINT, ( (COMPONENT, 'EE11' ), ), ))
        session.writeXYReport(fileName=join(wd,project,'dat','epsxx-Radius-' + str(j+1) + '.dat'),xyData=epsxx,appendMode=OFF)
        with open(join(csvfolder,'radialpaths.csv'),'a') as csv:
            csv.write('EE11' + ', ' + str(psi) + ', ' + '0' + ', ' + str(minL) + ', ' + str(join(wd,project,'dat')) + ', ' + 'epsxx-Radius-' + str(j+1) + '.dat' + '\n')
        # epsyy
        epsyy = xyPlot.XYDataFromPath(path=radpath,includeIntersections=True,pathStyle=PATH_POINTS,numIntervals=nSegsOnPath,shape=DEFORMED,labelType=TRUE_DISTANCE,variable= ('EE',INTEGRATION_POINT, ( (COMPONENT, 'EE22' ), ), ))
        session.writeXYReport(fileName=join(wd,project,'dat','epsyy-Radius-' + str(j+1) + '.dat'),xyData=epsyy,appendMode=OFF)
        with open(join(csvfolder,'radialpaths.csv'),'a') as csv:
            csv.write('EE22' + ', ' + str(psi) + ', ' + '0' + ', ' + str(minL) + ', ' + str(join(wd,project,'dat')) + ', ' + 'epsyy-Radius-' + str(j+1) + '.dat' + '\n')
        # epsxy
        epsxy = xyPlot.XYDataFromPath(path=radpath,includeIntersections=True,pathStyle=PATH_POINTS,numIntervals=nSegsOnPath,shape=DEFORMED,labelType=TRUE_DISTANCE,variable= ('EE',INTEGRATION_POINT, ( (COMPONENT, 'EE12' ), ), ))
        session.writeXYReport(fileName=join(wd,project,'dat','epsxy-Radius-' + str(j+1) + '.dat'),xyData=epsxy,appendMode=OFF)
        with open(join(csvfolder,'radialpaths.csv'),'a') as csv:
            csv.write('EE12' + ', ' + str(psi) + ', ' + '0' + ', ' + str(minL) + ', ' + str(join(wd,project,'dat')) + ', ' + 'epsxy-Radius-' + str(j+1) + '.dat' + '\n')
    print('...done.\n')
    #=======================================================================
    # get stresses and strains along circumferential paths
    #=======================================================================
    print('\n')
    print('Get stresses and strains along circumferential paths...\n')
    rs = numpy.concatenate((numpy.linspace(0,meanDefRf,nl+1,endpoint=False)[1:],numpy.linspace(meanDefRf,minL,nl+1)[1:]),axis=0)
    with open(join(csvfolder,'circumpaths.csv'),'w') as csv:
        csv.write('VARIABLE, R, phi_i [°], phi_f [°], FOLDER, FILENAME\n')
    for j,r in enumerate(rs):
        session.Path(name='Circle-' + str(j+1), type=CIRCUMFERENTIAL, expression=((0, 0, 0), (0, 0, 1), (r, 0, 0)), circleDefinition=ORIGIN_AXIS, numSegments=nSegsOnPath, startAngle=0, endAngle=360, radius=CIRCLE_RADIUS)
        circpath = session.paths['Circle-' + str(j+1)]
        # sigmaxx
        sigmaxx = xyPlot.XYDataFromPath(path=circpath,includeIntersections=True,pathStyle=PATH_POINTS,numIntervals=nSegsOnPath,shape=DEFORMED,labelType=TRUE_DISTANCE,variable= ('S',INTEGRATION_POINT, ( (COMPONENT, 'S11' ), ), ))
        session.writeXYReport(fileName=join(wd,project,'dat','sigmaxx-Circle-' + str(j+1) + '.dat'),xyData=sigmaxx,appendMode=OFF)
        with open(join(csvfolder,'circumpaths.csv'),'a') as csv:
            csv.write('S11' + ', ' + str(r) + ', ' + '0' + ', ' + '360' + ', ' + str(join(wd,project,'dat')) + ', ' + 'sigmaxx-Circle-' + str(j+1) + '.dat' + '\n')
        # sigmayy
        sigmayy = xyPlot.XYDataFromPath(path=circpath,includeIntersections=True,pathStyle=PATH_POINTS,numIntervals=nSegsOnPath,shape=DEFORMED,labelType=TRUE_DISTANCE,variable= ('S',INTEGRATION_POINT, ( (COMPONENT, 'S22' ), ), ))
        session.writeXYReport(fileName=join(wd,project,'dat','sigmayy-Circle-' + str(j+1) + '.dat'),xyData=sigmayy,appendMode=OFF)
        with open(join(csvfolder,'circumpaths.csv'),'a') as csv:
            csv.write('S22'  + ', ' + str(r) + ', ' + '0' + ', ' + '360' + ', ' + str(join(wd,project,'dat')) + ', ' + 'sigmayy-Circle-' + str(j+1) + '.dat' + '\n')
        # sigmaxy
        sigmaxy = xyPlot.XYDataFromPath(path=circpath,includeIntersections=True,pathStyle=PATH_POINTS,numIntervals=nSegsOnPath,shape=DEFORMED,labelType=TRUE_DISTANCE,variable= ('S',INTEGRATION_POINT, ( (COMPONENT, 'S12' ), ), ))
        session.writeXYReport(fileName=join(wd,project,'dat','sigmaxy-Circle-' + str(j+1) + '.dat'),xyData=sigmaxy,appendMode=OFF)
        with open(join(csvfolder,'circumpaths.csv'),'a') as csv:
            csv.write('S12'  + ', ' + str(r) + ', ' + '0' + ', ' + '360' + ', ' + str(join(wd,project,'dat')) + ', ' + 'sigmaxy-Circle-' + str(j+1) + '.dat' + '\n')
        # epsxx
        epsxx = xyPlot.XYDataFromPath(path=circpath,includeIntersections=True,pathStyle=PATH_POINTS,numIntervals=nSegsOnPath,shape=DEFORMED,labelType=TRUE_DISTANCE,variable= ('EE',INTEGRATION_POINT, ( (COMPONENT, 'EE11' ), ), ))
        session.writeXYReport(fileName=join(wd,project,'dat','epsxx-Circle-' + str(j+1) + '.dat'),xyData=epsxx,appendMode=OFF)
        with open(join(csvfolder,'circumpaths.csv'),'a') as csv:
            csv.write('EE11'  + ', ' + str(r) + ', ' + '0' + ', ' + '360' + ', ' + str(join(wd,project,'dat')) + ', ' + 'epsxx-Circle-' + str(j+1) + '.dat' + '\n')
        # epsyy
        epsyy = xyPlot.XYDataFromPath(path=circpath,includeIntersections=True,pathStyle=PATH_POINTS,numIntervals=nSegsOnPath,shape=DEFORMED,labelType=TRUE_DISTANCE,variable= ('EE',INTEGRATION_POINT, ( (COMPONENT, 'EE22' ), ), ))
        session.writeXYReport(fileName=join(wd,project,'dat','epsyy-Circle-' + str(j+1) + '.dat'),xyData=epsyy,appendMode=OFF)
        with open(join(csvfolder,'circumpaths.csv'),'a') as csv:
            csv.write('EE22'  + ', ' + str(r) + ', ' + '0' + ', ' + '360' + ', ' + str(join(wd,project,'dat')) + ', ' + 'epsyy-Circle-' + str(j+1) + '.dat' + '\n')
        # epsxy
        epsxy = xyPlot.XYDataFromPath(path=circpath,includeIntersections=True,pathStyle=PATH_POINTS,numIntervals=nSegsOnPath,shape=DEFORMED,labelType=TRUE_DISTANCE,variable= ('EE',INTEGRATION_POINT, ( (COMPONENT, 'EE12' ), ), ))
        session.writeXYReport(fileName=join(wd,project,'dat','epsxy-Circle-' + str(j+1) + '.dat'),xyData=epsxy,appendMode=OFF)
        with open(join(csvfolder,'circumpaths.csv'),'a') as csv:
            csv.write('EE12'  + ', ' + str(r) + ', ' + '0' + ', ' + '360' + ', ' + str(join(wd,project,'dat')) + ', ' + 'epsxy-Circle-' + str(j+1) + '.dat' + '\n')
    print('...done.\n')
    #=======================================================================
    # close database
    #=======================================================================
    print('\n')
    print('Close database...\n')
    odb.close()
    print('...done.\n')