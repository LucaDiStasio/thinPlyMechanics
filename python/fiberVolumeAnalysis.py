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

from os.path import isfile, join, exists
from os import makedirs
from datetime import datetime
from time import strftime, sleep
from platform import platform
import getopt
import numpy
from odbAccess import *
from abaqusConstants import *
from odbMaterial import *
from odbSection import *
import re

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

def getSingleNodeSet(odbObj,part,set):
    return odbObj.rootAssembly.instances[part].nodeSets[set]

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

def getDispVsReactionOnBoundarySubset(odbObj,step,frame,part,subset,component):

    set = getSingleNodeSet(odbObj,part,subset)

    disp = getFieldOutput(odbObj,-1,-1,'U',set)

    countdisp = 0
    meandisp = 0

    for value in disp.values:
        countdisp += 1
        meandisp += value.data[component]
    meandisp /= countdisp

    force = getFieldOutput(odbObj,-1,-1,'RF',set)

    totalforce = 0

    for value in force.values:
        totalforce += value.data[component]

    return meandisp,totalforce


#===============================================================================#
#===============================================================================#
#                       Data extraction sets
#===============================================================================#
#===============================================================================#

#===============================================================================#
#   extractFromODBoutputSet01
#
#   For Single Fiber RVE model
#
#   Extract coordinates of nodes and integration points, displacements, strains,
#   stresses, displacements and reactions at boundaries, displacements and stresses
#   at interfaces, Abaqus VCCT results
#
#===============================================================================#

def extractFromODBoutputSet01(wd,project,tol):
    print('Starting post-processing on project ' + project + '\n')
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
    try:
        odb = openOdb(path=odbfullpath)
    except Exception,e:
        print('An error occurred:')
        print(str(Exception))
        print(str(e))
        sys.exc_clear()
        return
    print('...done.\n')
    #=======================================================================
    # get first and last frame
    #=======================================================================
    print('\n')
    print('Get first and last frame...\n')
    firstFrame,lastFrame = getFirstAndLastFrameLastStep(odb)
    print('...done.\n')
    #=======================================================================
    # get deformed nodes
    #=======================================================================
    print('\n')
    print('Get deformed nodes...\n')

    nodes = getAndSaveAllNodes(odb,-1,-1,csvfolder,'defnodesCoords','.csv')
    intpoints = getAndSaveAllIntPoints(odb,-1,-1,csvfolder,'defintpointCoords','.csv')

    boundaryNodeSetsData = [[-1,-1,'PART-1-1','SW-CORNERNODE'],
                            [-1,-1,'PART-1-1','SE-CORNERNODE'],
                            [-1,-1,'PART-1-1','NE-CORNERNODE'],
                            [-1,-1,'PART-1-1','NW-CORNERNODE'],
                            [-1,-1,'PART-1-1','LOWERSIDE-NODES-WITHOUT-CORNERS'],
                            [-1,-1,'PART-1-1','RIGHTSIDE-NODES-WITHOUT-CORNERS'],
                            [-1,-1,'PART-1-1','UPPERSIDE-NODES-WITHOUT-CORNERS'],
                            [-1,-1,'PART-1-1','LEFTSIDE-NODES-WITHOUT-CORNERS']]
    extractAndSaveNodesCoordinates(odb,boundaryNodeSetsData,csvfolder,'defboundaryNodesCoords','.csv')

    interfaceNodeSetsData = [[-1,-1,'PART-1-1','FIBERSURFACE-NODES'],
                            [-1,-1,'PART-1-1','MATRIXSURFACEATFIBERINTERFACE-NODES']]
    extractAndSaveNodesCoordinates(odb,interfaceNodeSetsData,csvfolder,'deffiberInterfaceNodesCoords','.csv')

    print('...done.\n')
    #=======================================================================
    # get undeformed nodes
    #=======================================================================
    print('\n')
    print('Get undeformed nodes...\n')

    undefNodes = getAndSaveAllNodes(odb,-1,0,csvfolder,'undefnodesCoords','.csv')
    undefIntpoints = getAndSaveAllIntPoints(odb,-1,0,csvfolder,'undefintpointCoords','.csv')

    undefBoundaryNodeSetsData = [[-1,0,'PART-1-1','SW-CORNERNODE'],
                            [-1,0,'PART-1-1','SE-CORNERNODE'],
                            [-1,0,'PART-1-1','NE-CORNERNODE'],
                            [-1,0,'PART-1-1','NW-CORNERNODE'],
                            [-1,0,'PART-1-1','LOWERSIDE-NODES-WITHOUT-CORNERS'],
                            [-1,0,'PART-1-1','RIGHTSIDE-NODES-WITHOUT-CORNERS'],
                            [-1,0,'PART-1-1','UPPERSIDE-NODES-WITHOUT-CORNERS'],
                            [-1,0,'PART-1-1','LEFTSIDE-NODES-WITHOUT-CORNERS']]
    extractAndSaveNodesCoordinates(odb,undefBoundaryNodeSetsData,csvfolder,'undefboundaryNodesCoords','.csv')

    undefInterfaceNodeSetsData = [[-1,0,'PART-1-1','FIBERSURFACE-NODES'],
                                  [-1,0,'PART-1-1','MATRIXSURFACEATFIBERINTERFACE-NODES']]
    extractAndSaveNodesCoordinates(odb,undefInterfaceNodeSetsData,csvfolder,'undeffiberInterfaceNodesCoords','.csv')

    print('...done.\n')
    #=======================================================================
    # get fiber and matrix elements' and nodes' subsets
    #=======================================================================
    fiberNodes = getSingleNodeSet(odb,'PART-1-1','FIBER-NODES')
    matrixNodes = getSingleNodeSet(odb,'PART-1-1','MATRIX-NODES')
    fiberElements = getSingleElementSet(odb,'PART-1-1','FIBER-ELEMENTS')
    matrixElements = getSingleElementSet(odb,'PART-1-1','MATRIX-ELEMENTS')
    #=======================================================================
    # get displacements
    #=======================================================================
    print('\n')
    print('Get displacements in the entire model...\n')

    extractAndSaveFieldOutput(odb,-1,-1,csvfolder,'all-displacements','.csv','U')



def main(argv):

    matfolder = 'D:/OneDrive/01_Luca/07_DocMASE/07_Data/02_Material-Properties'

    #workdir = 'D:/01_Luca/07_Data/03_FEM'
    #workdir = 'D:/01_Luca/07_Data/03_FEM/StraightInterface/Full'
    workdir = 'D:/01_Luca/07_Data/03_FEM/CurvedInterface'
    #workdir = 'H:/01_Luca/07_DocMASE/07_Data/03_FEM'
    #workdir = 'H:/01_Luca/07_DocMASE/07_Data/03_FEM/CurvedInterface'
    #workdir = 'H:/01_Luca/07_DocMASE/07_Data/03_FEM/StraightInterface/Full'
    #workdir = 'H:/01_Luca/07_DocMASE/07_Data/03_FEM/StraightInterface/Quarter'

    #statusfile = '2017-06-23_AbaqusParametricRun_2017-06-23_16-57-17.sta'
    #statusfile = '2017-06-23_AbaqusParametricRun_SecondPart.sta'
    statusfile = '2017-06-23_AbaqusParametricRun_All.sta'

    settingsfile = 'D:/01_Luca/07_Data/03_FEM/postProcessorSettings.csv'

    


if __name__ == "__main__":
    main(sys.argv[1:])
