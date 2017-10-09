#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
=====================================================================================

Copyright (c) 2016-2017 Université de Lorraine & Luleå tekniska universitet
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



Tested with Python 2.7 Anaconda 2.4.1 (64-bit) distribution in Windows 7.

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

def getPerfs(wd,sims):
    perf = []
    perf.append(['PROJECT NAME','DEBOND [°]','NUMBER OF CPUS [-]','USER TIME [s]','SYSTEM TIME [s]','USER TIME/TOTAL CPU TIME [%]','SYSTEM TIME/TOTAL CPU TIME [%]','TOTAL CPU TIME [s]','WALLCLOCK TIME [s]','WALLCLOCK TIME [m]','WALLCLOCK TIME [h]','WALLCLOCK TIME/TOTAL CPU TIME [%]','ESTIMATED FLOATING POINT OPERATIONS PER ITERATION [-]','MINIMUM REQUIRED MEMORY [MB]','MEMORY TO MINIMIZE I/O [MB]','TOTAL NUMBER OF ELEMENTS [-]','NUMBER OF ELEMENTS DEFINED BY THE USER [-]','NUMBER OF ELEMENTS DEFINED BY THE PROGRAM [-]','TOTAL NUMBER OF NODES [-]','NUMBER OF NODES DEFINED BY THE USER [-]','NUMBER OF NODES DEFINED BY THE PROGRAM [-]','TOTAL NUMBER OF VARIABLES [-]'])
    print('')
    for sim in sims:
        print('Extracting data from project: ' + sim)
        usertime = 0
        systemtime = 0
        totalcpu = 0
        wallclock = 0
        floatops = 0
        minMemory = 0
        minIOmemory = 0
        totEl = 0
        userEl = 0
        progEl = 0
        totN = 0
        userN = 0
        progN = 0
        totVar = 0
        cpus = 0
        debond = 0
        if exists(join(wd,sim,'abaqus',sim+'.dat')):
            with open(join(wd,sim,'abaqus',sim+'.dat'),'r') as dat:
                lines = dat.readlines()
            for l,line in enumerate(lines):
                if 'JOB TIME SUMMARY' in line:
                    for subline in lines[l:]:
                        if 'USER TIME' in subline:
                            usertime = float(subline.split('=')[1])
                        elif 'SYSTEM TIME' in subline:
                            systemtime = float(subline.split('=')[1])
                        elif 'TOTAL CPU TIME' in subline:
                            totalcpu = float(subline.split('=')[1])
                        elif 'WALLCLOCK TIME' in subline:
                            wallclock = float(subline.split('=')[1])
                elif 'M E M O R Y   E S T I M A T E' in line:
                    values = lines[l+6].replace('\n','').split(' ')
                    while '' in values: values.remove('')
                    floatops = float(values[1])
                    minMemory = float(values[2])
                    minIOmemory = float(values[3])
                elif 'P R O B L E M   S I Z E' in line:
                    words = lines[l+3].replace('\n','').split(' ')
                    while '' in words: words.remove('')
                    totEl = int(words[-1])
                    words = lines[l+4].split(' ')
                    while '' in words: words.remove('')
                    userEl = int(words[-1])
                    words = lines[l+5].split(' ')
                    while '' in words: words.remove('')
                    progEl = int(words[-1])
                    words = lines[l+6].split(' ')
                    while '' in words: words.remove('')
                    totN = int(words[-1])
                    words = lines[l+7].split(' ')
                    while '' in words: words.remove('')
                    userN = int(words[-1])
                    words = lines[l+8].split(' ')
                    while '' in words: words.remove('')
                    progN = int(words[-1])
                    words = lines[l+9].split(' ')
                    while '' in words: words.remove('')
                    totVar = int(words[-1])
        if exists(join(wd,sim,'abaqus',sim+'.msg')):
            with open(join(wd,sim,'abaqus',sim+'.msg'),'r') as msg:
                lines = msg.readlines()
                for line in lines:
                    if 'USING THE DIRECT SOLVER WITH' in line:
                        words = line.replace('\n','').split(' ')
                        while '' in words: words.remove('')
                        cpus = int(words[words.index('PROCESSORS')-1])
        if exists(join(wd,sim,'abqinp',sim+'.inp')):
            with open(join(wd,sim,'abqinp',sim+'.inp'),'r') as inp:
                lines = inp.readlines()
            for line in lines:
                 if 'Crack Angular Aperture' in line:
                     debond = np.round(float(line.replace('\n','').replace('*','').replace('-','').split(':')[-1].replace('deg','')))
                     break
        perf.append([sim,debond,cpus,usertime,systemtime,usertime/totalcpu,systemtime/totalcpu,totalcpu,wallclock,wallclock/60.,wallclock/3600.,wallclock/totalcpu,floatops,minMemory,minIOmemory,totEl,userEl,progEl,totN,userN,progN,totVar])
    return perf

def writePerfToFile(od,outfile,performanceslist):
    with open(join(od,outfile),'w') as csv:
        for performances in performanceslist:
            line = ''
            for i,performance in enumerate(performances):
                if i>0:
                    line += ','
                line += str(performance)
            csv.write(line + '\n')
            
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
#   Full analysis
#   Extract coordinates of nodes and integration points, displacements, strains,
#   stresses, displacements and reactions at boundaries, displacements and stresses
#   at interfaces, compute VCCT and VCCI
#
#===============================================================================#

def extractFromODBoutputSet01(wd,project,matdatafolder,nEl0,NElMax,DeltaEl,tol):
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
    # extract performances
    #=======================================================================
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
    
    print('...done.\n')
    print('\n')
    print('Get displacements in fiber subset...\n')
    
    extractAndSaveFieldOutput(odb,-1,-1,csvfolder,'fibersubset-displacements','.csv','U',fiberNodes)
       
    print('...done.\n')
    print('\n')
    print('Get displacements in matrix subset...\n')
    
    extractAndSaveFieldOutput(odb,-1,-1,csvfolder,'matrixsubset-displacements','.csv','U',matrixNodes)
      
    print('...done.\n')
    #=======================================================================
    # get strains
    #=======================================================================
    print('\n')
    print('Get strains in the entire model...\n')
    
    extractAndSaveFieldOutput(odb,-1,-1,csvfolder,'all-elasticstrains','.csv','EE')
    
    print('...done.\n')
    print('\n')
    print('Get strains in fiber subset...\n')
    
    extractAndSaveFieldOutput(odb,-1,-1,csvfolder,'fibersubset-elasticstrains','.csv','EE',fiberElements)
    
    print('...done.\n')
    print('\n')
    print('Get strains in matrix subset...\n')
    
    extractAndSaveFieldOutput(odb,-1,-1,csvfolder,'matrixsubset-elasticstrains','.csv','EE',matrixElements)
    
    print('...done.\n')
    #=======================================================================
    # get stresses 
    #=======================================================================
    print('\n')
    print('Get stresses in the entire model...\n')
    
    extractAndSaveFieldOutput(odb,-1,-1,csvfolder,'all-elasticstresses','.csv','S')
    
    print('...done.\n')
    print('\n')
    print('Get stresses in fiber subset...\n')
    
    extractAndSaveFieldOutput(odb,-1,-1,csvfolder,'fibersubset-elasticstresses','.csv','S',fiberElements)
    
    print('...done.\n')
    print('\n')
    print('Get stresses in matrix subset...\n')
    
    extractAndSaveFieldOutput(odb,-1,-1,csvfolder,'matrixsubset-elasticstresses','.csv','S',matrixElements)
    
    print('...done.\n')
    #=======================================================================
    # get displacement and reaction force at boundary
    #=======================================================================
    print('\n')
    print('Get displacement and reaction force at boundary...\n')
    
    meanleftdisp,totalleftforce = getDispVsReactionOnBoundarySubset(odb,-1,-1,'PART-1-1','LEFTSIDE-NODES-WITH-CORNERS',0)
    
    meanrightdisp,totalrightforce = getDispVsReactionOnBoundarySubset(odb,-1,-1,'PART-1-1','RIGHTSIDE-NODES-WITH-CORNERS',0)
        
    with open(join(csvfolder,'dispVSreactionforce.csv'),'w') as csv:
        csv.write('TABLE\n')
        csv.write('SIDE, U1, RF1\n')
        csv.write('RIGHT, ' + str(meanrightdisp) + ', ' + str(totalrightforce) + '\n')
        csv.write('LEFT, ' + str(meanleftdisp) + ', ' + str(totalleftforce) + '\n')
        
    print('...done.\n')
    #=======================================================================
    # get interfaces
    #=======================================================================
    print('\n')
    print('Get interfaces...\n')
    master = getSingleNodeSet(odb,'PART-1-1','FIBERSURFACE-NODES')
    slave = getSingleNodeSet(odb,'PART-1-1','MATRIXSURFACEATFIBERINTERFACE-NODES')
    print('...done.\n')
    #=======================================================================
    # get stresses at interface (on slave and master)
    #=======================================================================
    print('\n')
    print('Get stresses at interface (on slave and master)...\n')
    
    # on master
    print('\n')
    print('...on master...\n')
    
    # get values
    cstatusOnMaster = getFieldOutput(odb,-1,-1,'CSTATUS',master)
    cpressOnMaster  = getFieldOutput(odb,-1,-1,'CPRESS',master)
    cshearOnMaster  = getFieldOutput(odb,-1,-1,'CSHEARF',master)
    cshearfOnMaster  = getFieldOutput(odb,-1,-1,'CSHEAR1',master)
    
    # write to file
    toWrite = []
    for value in cstatusOnMaster.values:
        if 'NODAL' in str(value.position):
            pos = nodes
            typeOfVar = 'NODAL'
        elif 'INTEGRATION_POINT' in str(value.position):
            pos = intpoints
            typeOfVar = 'INTEGRATION_POINT'
        toWrite.append([typeOfVar,str(value.nodeLabel),str(pos[str(value.nodeLabel)][0]),str(pos[str(value.nodeLabel)][1]),str(numpy.sqrt(numpy.power(pos[str(value.nodeLabel)][0],2)+numpy.power(pos[str(value.nodeLabel)][1],2))),str(numpy.arctan2(pos[str(value.nodeLabel)][1],pos[str(value.nodeLabel)][0])* 180/numpy.pi),str(value.data),'0','0','0','0'])
    for value in cpressOnMaster.values:
        posit = -1
        for k,item in enumerate(toWrite):
            if item[1]==str(value.nodeLabel):
                posit = k
                break
        if posit>-1:
            toWrite[posit][7] = str(value.data)
        else:
            if 'NODAL' in str(value.position):
                pos = nodes
                typeOfVar = 'NODAL'
            elif 'INTEGRATION_POINT' in str(value.position):
                pos = intpoints
                typeOfVar = 'INTEGRATION_POINT'
            toWrite.append([typeOfVar,str(value.nodeLabel),str(pos[str(value.nodeLabel)][0]),str(pos[str(value.nodeLabel)][1]),str(numpy.sqrt(numpy.power(pos[str(value.nodeLabel)][0],2)+numpy.power(pos[str(value.nodeLabel)][1],2))),str(numpy.arctan2(pos[str(value.nodeLabel)][1],pos[str(value.nodeLabel)][0])* 180/numpy.pi),'0',str(value.data),'0','0','0'])
    for value in cshearOnMaster.values:
        posit = -1
        for k,item in enumerate(toWrite):
            if item[1]==str(value.nodeLabel):
                posit = k
                break
        if posit>-1:
            toWrite[posit][8] = str(value.data[0])
            toWrite[posit][9] = str(value.data[1])
        else:
            if 'NODAL' in str(value.position):
                pos = nodes
                typeOfVar = 'NODAL'
            elif 'INTEGRATION_POINT' in str(value.position):
                pos = intpoints
                typeOfVar = 'INTEGRATION_POINT'
            toWrite.append([typeOfVar,str(value.nodeLabel),str(pos[str(value.nodeLabel)][0]),str(pos[str(value.nodeLabel)][1]),str(numpy.sqrt(numpy.power(pos[str(value.nodeLabel)][0],2)+numpy.power(pos[str(value.nodeLabel)][1],2))),str(numpy.arctan2(pos[str(value.nodeLabel)][1],pos[str(value.nodeLabel)][0])* 180/numpy.pi),'0','0',str(value.data[0]),str(value.data[1]),'0'])
    for value in cshearfOnMaster.values:
        posit = -1
        for k,item in enumerate(toWrite):
            if item[1]==str(value.nodeLabel):
                posit = k
                break
        if posit>-1:
            toWrite[posit][10] = str(value.data)
        else:
            if 'NODAL' in str(value.position):
                pos = nodes
                typeOfVar = 'NODAL'
            elif 'INTEGRATION_POINT' in str(value.position):
                pos = intpoints
                typeOfVar = 'INTEGRATION_POINT'
            toWrite.append([typeOfVar,str(value.nodeLabel),str(pos[str(value.nodeLabel)][0]),str(pos[str(value.nodeLabel)][1]),str(numpy.sqrt(numpy.power(pos[str(value.nodeLabel)][0],2)+numpy.power(pos[str(value.nodeLabel)][1],2))),str(numpy.arctan2(pos[str(value.nodeLabel)][1],pos[str(value.nodeLabel)][0])* 180/numpy.pi),'0','0','0','0',str(value.data)])
    with open(join(csvfolder,'stressesOnMaster.csv'),'w') as csv:
        csv.write('SCATTER PLOT\n')
        csv.write('NODE TYPE, NODE LABEL, X, Y, R, THETA [°], CSTATUS, CPRESS, CSHEAR1, CSHEAR2, CSHEARFRIC1\n')
        for item in toWrite:
            csv.write(item[0] + ', ' + item[1] + ', ' + item[2] + ', ' + item[3] + ', ' + item[4] + ', ' + item[5] + ', ' + item[6] + ', ' + item[7] + ', ' + item[8] + ', ' + item[9] + ', ' + item[10] + '\n')
    
    print('...done...\n')
    
    # on slave
    print('\n')
    print('...on slave...\n')
    
    # get values
    cstatusOnSlave = getFieldOutput(odb,-1,-1,'CSTATUS',slave)
    cpressOnSlave  = getFieldOutput(odb,-1,-1,'CPRESS',slave)
    cshearOnSlave  = getFieldOutput(odb,-1,-1,'CSHEARF',slave)
    cshearfOnSlave  = getFieldOutput(odb,-1,-1,'CSHEAR1',slave)
    
    # write to file
    toWrite = []
    for value in cstatusOnSlave.values:
        if 'NODAL' in str(value.position):
            pos = nodes
            typeOfVar = 'NODAL'
        elif 'INTEGRATION_POINT' in str(value.position):
            pos = intpoints
            typeOfVar = 'INTEGRATION_POINT'
        toWrite.append([typeOfVar,str(value.nodeLabel),str(pos[str(value.nodeLabel)][0]),str(pos[str(value.nodeLabel)][1]),str(numpy.sqrt(numpy.power(pos[str(value.nodeLabel)][0],2)+numpy.power(pos[str(value.nodeLabel)][1],2))),str(numpy.arctan2(pos[str(value.nodeLabel)][1],pos[str(value.nodeLabel)][0])* 180/numpy.pi),str(value.data),'0','0','0','0'])
    for value in cpressOnSlave.values:
        posit = -1
        for k,item in enumerate(toWrite):
            if item[1]==str(value.nodeLabel):
                posit = k
                break
        if posit>-1:
            toWrite[posit][7] = str(value.data)
        else:
            if 'NODAL' in str(value.position):
                pos = nodes
                typeOfVar = 'NODAL'
            elif 'INTEGRATION_POINT' in str(value.position):
                pos = intpoints
                typeOfVar = 'INTEGRATION_POINT'
            toWrite.append([typeOfVar,str(value.nodeLabel),str(pos[str(value.nodeLabel)][0]),str(pos[str(value.nodeLabel)][1]),str(numpy.sqrt(numpy.power(pos[str(value.nodeLabel)][0],2)+numpy.power(pos[str(value.nodeLabel)][1],2))),str(numpy.arctan2(pos[str(value.nodeLabel)][1],pos[str(value.nodeLabel)][0])* 180/numpy.pi),'0',str(value.data),'0','0','0'])
    for value in cshearOnSlave.values:
        posit = -1
        for k,item in enumerate(toWrite):
            if item[1]==str(value.nodeLabel):
                posit = k
                break
        if posit>-1:
            toWrite[posit][8] = str(value.data[0])
            toWrite[posit][9] = str(value.data[1])
        else:
            if 'NODAL' in str(value.position):
                pos = nodes
                typeOfVar = 'NODAL'
            elif 'INTEGRATION_POINT' in str(value.position):
                pos = intpoints
                typeOfVar = 'INTEGRATION_POINT'
            toWrite.append([typeOfVar,str(value.nodeLabel),str(pos[str(value.nodeLabel)][0]),str(pos[str(value.nodeLabel)][1]),str(numpy.sqrt(numpy.power(pos[str(value.nodeLabel)][0],2)+numpy.power(pos[str(value.nodeLabel)][1],2))),str(numpy.arctan2(pos[str(value.nodeLabel)][1],pos[str(value.nodeLabel)][0])* 180/numpy.pi),'0','0',str(value.data[0]),str(value.data[1]),'0'])
    for value in cshearfOnSlave.values:
        posit = -1
        for k,item in enumerate(toWrite):
            if item[1]==str(value.nodeLabel):
                posit = k
                break
        if posit>-1:
            toWrite[posit][10] = str(value.data)
        else:
            if 'NODAL' in str(value.position):
                pos = nodes
                typeOfVar = 'NODAL'
            elif 'INTEGRATION_POINT' in str(value.position):
                pos = intpoints
                typeOfVar = 'INTEGRATION_POINT'
            toWrite.append([typeOfVar,str(value.nodeLabel),str(pos[str(value.nodeLabel)][0]),str(pos[str(value.nodeLabel)][1]),str(numpy.sqrt(numpy.power(pos[str(value.nodeLabel)][0],2)+numpy.power(pos[str(value.nodeLabel)][1],2))),str(numpy.arctan2(pos[str(value.nodeLabel)][1],pos[str(value.nodeLabel)][0])* 180/numpy.pi),'0','0','0','0',str(value.data)])
    with open(join(csvfolder,'stressesOnSlave.csv'),'w') as csv:
        csv.write('SCATTER PLOT\n')
        csv.write('NODE TYPE, NODE LABEL, X, Y, R, THETA [°], CSTATUS, CPRESS, CSHEAR1, CSHEAR2, CSHEARFRIC1\n')
        for item in toWrite:
            csv.write(item[0] + ', ' + item[1] + ', ' + item[2] + ', ' + item[3] + ', ' + item[4] + ', ' + item[5] + ', ' + item[6] + ', ' + item[7] + ', ' + item[8] + ', ' + item[9] + ', ' + item[10] + '\n')
    
    print('...done.\n')
    #=======================================================================
    # get displacements at interface (on slave only)
    #=======================================================================
    print('\n')
    print('Get displacements at interface (on slave only)...\n')
    
    # get values
    copenOnSlave = getFieldOutput(odb,-1,-1,'COPEN',slave)
    cslipOnSlave  = getFieldOutput(odb,-1,-1,'CSLIP1',slave)
    
    # write to file
    toWrite = []
    for value in copenOnSlave.values:
        if 'NODAL' in str(value.position):
            pos = nodes
            typeOfVar = 'NODAL'
        elif 'INTEGRATION_POINT' in str(value.position):
            pos = intpoints
            typeOfVar = 'INTEGRATION_POINT'
        toWrite.append([typeOfVar,str(value.nodeLabel),str(pos[str(value.nodeLabel)][0]),str(pos[str(value.nodeLabel)][1]),str(numpy.sqrt(numpy.power(pos[str(value.nodeLabel)][0],2)+numpy.power(pos[str(value.nodeLabel)][1],2))),str(numpy.arctan2(pos[str(value.nodeLabel)][1],pos[str(value.nodeLabel)][0])* 180/numpy.pi),str(value.data),'0'])
    for value in cslipOnSlave.values:
        posit = -1
        for k,item in enumerate(toWrite):
            if item[1]==str(value.nodeLabel):
                posit = k
                break
        if posit>-1:
            toWrite[posit][7] = str(value.data)
        else:
            if 'NODAL' in str(value.position):
                pos = nodes
                typeOfVar = 'NODAL'
            elif 'INTEGRATION_POINT' in str(value.position):
                pos = intpoints
                typeOfVar = 'INTEGRATION_POINT'
            toWrite.append([typeOfVar,str(value.nodeLabel),str(pos[str(value.nodeLabel)][0]),str(pos[str(value.nodeLabel)][1]),str(numpy.sqrt(numpy.power(pos[str(value.nodeLabel)][0],2)+numpy.power(pos[str(value.nodeLabel)][1],2))),str(numpy.arctan2(pos[str(value.nodeLabel)][1],pos[str(value.nodeLabel)][0])* 180/numpy.pi),'0',str(value.data)])
    with open(join(csvfolder,'displacementsOnSlave.csv'),'w') as csv:
        csv.write('SCATTER PLOT\n')
        csv.write('NODE TYPE, NODE LABEL, X, Y, R, THETA [°], COPEN, CSLIP\n')
        for item in toWrite:
            csv.write(item[0] + ', ' + item[1] + ', ' + item[2] + ', ' + item[3] + ', ' + item[4] + ', ' + item[5] + ', ' + item[6] + ', ' + item[7] + '\n')
    toWrite = []
    
    print('...done.\n')
    #=======================================================================
    # get stresses at boundaries
    #=======================================================================
    print('\n')
    print('Get stresses at boundaries...\n')
    leftSide = getSingleNodeSet(odb,'PART-1-1','LEFTSIDE-NODES-WITH-CORNERS')
    rightSide = getSingleNodeSet(odb,'PART-1-1','RIGHTSIDE-NODES-WITH-CORNERS')
    extractAndSaveFieldOutput(odb,-1,-1,csvfolder,'StressesOnRightSide','.csv','S',rightSide,3)
    extractAndSaveFieldOutput(odb,-1,-1,csvfolder,'StressesOnLeftSide','.csv','S',leftSide,3)
    rightStresses = getFieldOutput(odb,-1,-1,'S',rightSide,3)
    leftStresses = getFieldOutput(odb,-1,-1,'S',leftSide,3)
    maxRight = rightStresses.values[0].data[0]
    minRight = rightStresses.values[0].data[0]
    meanRight = 0
    countRight = 0
    for value in rightStresses.values:
        if value.data[0]>maxRight:
            maxRight = value.data[0]
        elif value.data[0]<minRight:
            minRight = value.data[0]
        meanRight += value.data[0]
        countRight += 1
    meanRight /=countRight
    maxLeft = leftStresses.values[0].data[0]
    minLeft = leftStresses.values[0].data[0]
    meanLeft = 0
    countLeft = 0
    for value in leftStresses.values:
        if value.data[0]>maxLeft:
            maxLeft = value.data[0]
        elif value.data[0]<minLeft:
            minLeft = value.data[0]
        meanLeft += value.data[0]
        countLeft += 1
    meanLeft /=countLeft
    sigmaInf = 0.5*(meanRight+meanLeft)
    print('...done.\n')
    #=======================================================================
    # get simulation's units of measurement, material and geometry
    #=======================================================================
    print('\n')
    print('Get simulation''s units of measurement, material and geometry...\n')
    with open(join(csvfolder,project + '.csv')) as csv:
        lines = csv.readlines()
    for l,line in enumerate(lines):
        if 'Fiber radius Rf' in line:
            Rf = float(line.replace('\n','').replace('-','').replace('*','').split(',')[1]);
        elif 'Applied Axial Strain' in line:
            epsxx = float(line.replace('\n','').replace('-','').replace('*','').split(',')[1])
        elif 'Matrix' in line:
            matrixType = line.replace('\n','').replace('-','').replace('*','').split(',')[1]
        elif 'length, SI' in line:
            lengthFactor = 1.0/float(line.replace('**','').replace('--','').replace('\n','').split(',')[2])
        elif 'energy release rate, SI' in line:
            enrrtFactor = 1.0/float(line.replace('**','').replace('--','').replace('\n','').split(',')[2])
        elif 'force, SI' in line:
            forceFactor = 1.0/float(line.replace('**','').replace('--','').replace('\n','').split(',')[2])
        elif 'pressure/stress, SI' in line:
            stressFactor = 1.0/float(line.replace('**','').replace('--','').replace('\n','').split(',')[2])
    print('...done.\n')
    #=======================================================================
    # compute G0
    #=======================================================================
    print('\n')
    print('Compute G0...\n')
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
    Rf *= lengthFactor #recast in SI units
    sigmaInf *= stressFactor  #recast in SI units
    G0 = numpy.pi*Rf*sigmaInf*sigmaInf*(1+(3.0-4.0*num))/(8.0*Gm)
    print('...done.\n')
    #=======================================================================
    # get J-integrals
    #=======================================================================
    print('\n')
    print('Get J-integrals...\n')
    isJINTcomputed = False
    with open(join(wd,project,'abaqus',project + '.dat'),'r') as dat:
        lines = dat.readlines()
    lineIndex = 0
    for l,line in enumerate(lines):
        if 'J - I N T E G R A L   E S T I M A T E S' in line:
            isJINTcomputed = True
            lineIndex = l
            break
    if isJINTcomputed:
        JINTs = []
        JINToverG0s = []
        startIndex = 0
        for l,line in enumerate(lines[lineIndex:]):
            if 'INCREMENT' in line and 'SUMMARY' in line:
                startIndex = lineIndex + l
        for l,line in enumerate(lines[startIndex:]):
            if 'J - I N T E G R A L   E S T I M A T E S' in line:
                temp1 = filter(lambda x: x!=' ' and x!='', lines[startIndex+l+11].replace('\n','').split(' '))[2:]
                temp2 = filter(lambda x: x!=' ' and x!='', lines[startIndex+l+12].replace('\n','').split(' '))
                temp3 = filter(lambda x: x!=' ' and x!='', lines[startIndex+l+13].replace('\n','').split(' '))
                temp4 = filter(lambda x: x!=' ' and x!='', lines[startIndex+l+14].replace('\n','').split(' '))
                try:
                    setName = filter(lambda x: x!=' ' and x!='', lines[startIndex+l+20].replace('\n','').split(' '))[-1]
                except Exception:
                    setName = filter(lambda x: x!=' ' and x!='', lines[startIndex+l+24].replace('\n','').split(' '))[-1]
                if setName=='' or setName ==' ':
                    setName = filter(lambda x: x!=' ' and x!='', lines[startIndex+l+24].replace('\n','').split(' '))[-1]
                values = []
                valuesOverG0 = []
                values.append(setName)
                valuesOverG0.append(setName)
                for value in temp1:
                    values.append(enrrtFactor*float(value))
                    valuesOverG0.append(enrrtFactor*float(value)/G0)
                for value in temp2:
                    values.append(enrrtFactor*float(value))
                    valuesOverG0.append(enrrtFactor*float(value)/G0)
                for value in temp3:
                    values.append(enrrtFactor*float(value))
                    valuesOverG0.append(enrrtFactor*float(value)/G0)
                for value in temp4:
                    values.append(enrrtFactor*float(value))
                    valuesOverG0.append(enrrtFactor*float(value)/G0)
                JINTs.append(values)
                JINToverG0s.append(valuesOverG0)
    print('...done.\n')
    #=======================================================================
    # VCCT in forces
    #=======================================================================
    print('\n')
    print('Compute energy release rates with VCCT in forces...\n')
    
    crackTips = []
    
    with open(join(csvfolder,project + '.csv')) as csv:
        lines = csv.readlines()
    for line in lines:
        if 'Nalpha' in line:
            N1 = int(line.replace('\n','').split(',')[-1])
        elif 'Nbeta' in line:
            N2 = int(line.replace('\n','').split(',')[-1])
        elif 'Ngamma' in line:
            N3 = int(line.replace('\n','').split(',')[-1])
        elif 'Ndelta' in line:
            N4 = int(line.replace('\n','').split(',')[-1])
        elif 'Neps' in line:
            N5 = int(line.replace('\n','').split(',')[-1])
        elif 'Fiber radius Rf' in line:
            Rf = float(line.replace('\n','').split(',')[-1])
        elif 'Angular discretization at interface' in line:
            deltaC = float(line.replace('\n','').replace('deg','').split(',')[-1])*numpy.pi/180.0
        elif 'Crack Angular Aperture' in line:
            deltaTheta = float(line.replace('\n','').replace('deg','').split(',')[-1])
           
    if deltaTheta>0 and deltaTheta<180:
        matrixCrackTip1 = getSingleNodeSet(odb,'PART-1-1','MATRIXCRACKTIP1-NODE')
        fiberCrackTip1 = getSingleNodeSet(odb,'PART-1-1','FIBERCRACKTIP1-NODE')
        matrixCrackTip2 = getSingleNodeSet(odb,'PART-1-1','MATRIXCRACKTIP2-NODE')
        fiberCrackTip2 = getSingleNodeSet(odb,'PART-1-1','FIBERCRACKTIP2-NODE')
        gamma2 = getSingleNodeSet(odb,'PART-1-1','GAMMA4-NODES')
        
        matrixCrackTip1Label = int(lastFrame.fieldOutputs['COORD'].getSubset(position=NODAL).getSubset(region=matrixCrackTip1).values[0].nodeLabel)
        matrixCrackTip2Label = int(lastFrame.fieldOutputs['COORD'].getSubset(position=NODAL).getSubset(region=matrixCrackTip2).values[0].nodeLabel)
        gamma2Labels = []
        for value in lastFrame.fieldOutputs['COORD'].getSubset(position=NODAL).getSubset(region=gamma2).values:
            gamma2Labels.append(int(value.nodeLabel))
        if matrixCrackTip1Label==4*N1*(N4+N5+1):
            if 4*N1*(N4+N5) in gamma2Labels:
                preMatrixCrackTip1Label = 4*N1*(N4+N5)
            else:
                preMatrixCrackTip1Label = matrixCrackTip1Label-1
        elif matrixCrackTip1Label==4*N1*(N4+N5):
            if matrixCrackTip1Label+1 in gamma2Labels:
                preMatrixCrackTip1Label = matrixCrackTip1Label+1
            else:
                preMatrixCrackTip1Label = 4*N1*(N4+N5+1)
        else:
            if matrixCrackTip1Label+1 in gamma2Labels:
                preMatrixCrackTip1Label = matrixCrackTip1Label+1
            else:
                preMatrixCrackTip1Label = matrixCrackTip1Label-1
        if matrixCrackTip2Label==4*N1*(N4+N5+1):
            if matrixCrackTip2Label-1 in gamma2Labels:
                preMatrixCrackTip1Label = matrixCrackTip2Label-1
            else:
                preMatrixCrackTip1Label = 4*N1*(N4+N5)
        elif matrixCrackTip2Label==4*N1*(N4+N5):
            if 4*N1*(N4+N5+1) in gamma2Labels:
                preMatrixCrackTip1Label = 4*N1*(N4+N5+1)
            else:
                preMatrixCrackTip1Label = matrixCrackTip2Label+1
        else:
            if matrixCrackTip2Label-1 in gamma2Labels:
                preMatrixCrackTip2Label = matrixCrackTip2Label-1
            else:
                preMatrixCrackTip2Label = matrixCrackTip2Label+1
                
        preMatrixCrackTip1 = odb.rootAssembly.instances['PART-1-1'].getNodeFromLabel(preMatrixCrackTip1Label)
        preMatrixCrackTip2 = odb.rootAssembly.instances['PART-1-1'].getNodeFromLabel(preMatrixCrackTip2Label)
        preFiberCrackTip1 = odb.rootAssembly.instances['PART-1-1'].getNodeFromLabel(preMatrixCrackTip1Label+4*N1)
        preFiberCrackTip2 = odb.rootAssembly.instances['PART-1-1'].getNodeFromLabel(preMatrixCrackTip2Label+4*N1)
        
        undeftip1 = firstFrame.fieldOutputs['COORD'].getSubset(position=NODAL).getSubset(region=matrixCrackTip1).values[0]
        deftip1 = lastFrame.fieldOutputs['COORD'].getSubset(position=NODAL).getSubset(region=matrixCrackTip1).values[0]
        undeftip2 = firstFrame.fieldOutputs['COORD'].getSubset(position=NODAL).getSubset(region=matrixCrackTip2).values[0]
        deftip2 = lastFrame.fieldOutputs['COORD'].getSubset(position=NODAL).getSubset(region=matrixCrackTip2).values[0]
        
        undefmatrixpretip1 = firstFrame.fieldOutputs['COORD'].getSubset(position=NODAL).getSubset(region=preMatrixCrackTip1).values[0]
        undefmatrixpretip2 = firstFrame.fieldOutputs['COORD'].getSubset(position=NODAL).getSubset(region=preMatrixCrackTip2).values[0]
        undeffiberpretip1 = firstFrame.fieldOutputs['COORD'].getSubset(position=NODAL).getSubset(region=preFiberCrackTip1).values[0]
        undeffiberpretip2 = firstFrame.fieldOutputs['COORD'].getSubset(position=NODAL).getSubset(region=preFiberCrackTip2).values[0]
        
        defmatrixpretip1 = lastFrame.fieldOutputs['COORD'].getSubset(position=NODAL).getSubset(region=preMatrixCrackTip1).values[0]
        defmatrixpretip2 = lastFrame.fieldOutputs['COORD'].getSubset(position=NODAL).getSubset(region=preMatrixCrackTip2).values[0]
        deffiberpretip1 = lastFrame.fieldOutputs['COORD'].getSubset(position=NODAL).getSubset(region=preFiberCrackTip1).values[0]
        deffiberpretip2 = lastFrame.fieldOutputs['COORD'].getSubset(position=NODAL).getSubset(region=preFiberCrackTip2).values[0]
        
        dispmatrixpretip1 = lastFrame.fieldOutputs['U'].getSubset(position=NODAL).getSubset(region=preMatrixCrackTip1).values[0]
        dispmatrixpretip2 = lastFrame.fieldOutputs['U'].getSubset(position=NODAL).getSubset(region=preMatrixCrackTip2).values[0]
        dispfiberpretip1 = lastFrame.fieldOutputs['U'].getSubset(position=NODAL).getSubset(region=preFiberCrackTip1).values[0]
        dispfiberpretip2 = lastFrame.fieldOutputs['U'].getSubset(position=NODAL).getSubset(region=preFiberCrackTip2).values[0]
        
        beta1 = numpy.arctan2(undeftip1.data[1],undeftip1.data[0])
        beta2 = numpy.arctan2(undeftip2.data[1],undeftip2.data[0])
        
        #print('orientation defined')
        '''
        xdispcracktip1 = (defmatrixpretip1.data[0]-undefmatrixpretip1.data[0]) - (deffiberpretip1.data[0]-undeffiberpretip1.data[0])
        zdispcracktip1 = (defmatrixpretip1.data[1]-undefmatrixpretip1.data[1]) - (deffiberpretip1.data[1]-undeffiberpretip1.data[1])
        
        xdispcracktip2 = (defmatrixpretip2.data[0]-undefmatrixpretip2.data[0]) - (deffiberpretip2.data[0]-undeffiberpretip2.data[0])
        zdispcracktip2 = (defmatrixpretip2.data[1]-undefmatrixpretip2.data[1]) - (deffiberpretip2.data[1]-undeffiberpretip2.data[1])
        '''
        
        xdispcracktip1 = dispmatrixpretip1.data[0] - dispfiberpretip1.data[0]
        zdispcracktip1 = dispmatrixpretip1.data[1] - dispfiberpretip1.data[1]
        
        xdispcracktip2 = dispmatrixpretip2.data[0] - dispfiberpretip2.data[0]
        zdispcracktip2 = dispmatrixpretip2.data[1] - dispfiberpretip2.data[1]
        
        rdispcracktip1 = numpy.cos(beta1)*xdispcracktip1 + numpy.sin(beta1)*zdispcracktip1
        thetadispcracktip1 = -numpy.sin(beta1)*xdispcracktip1 + numpy.cos(beta1)*zdispcracktip1
        
        rdispcracktip2 = numpy.cos(beta2)*xdispcracktip2 + numpy.sin(beta2)*zdispcracktip2
        thetadispcracktip2 = -numpy.sin(beta2)*xdispcracktip2 + numpy.cos(beta2)*zdispcracktip2
        #print('disps rotated:')
        
        try:
            dummy1Node = odb.rootAssembly.instances['PART-1-1'].nodeSets['DUMMY1-NODE']
            dummy2Node = odb.rootAssembly.instances['PART-1-1'].nodeSets['DUMMY2-NODE']
            isDummy = True
            #print('is dummy')
        except Exception,error:
            #print(str(Exception))
            #print(str(error))
            isDummy = False
            #print('is not dummy')
            sys.exc_clear()
            #sys.exit(2)
        if isDummy:
            xRFcracktip1 = lastFrame.fieldOutputs['RF'].getSubset(region=dummy1Node,position=NODAL).values[0].data[0]
            zRFcracktip1 = lastFrame.fieldOutputs['RF'].getSubset(region=dummy1Node,position=NODAL).values[0].data[1]
            xRFcracktip2 = lastFrame.fieldOutputs['RF'].getSubset(region=dummy2Node,position=NODAL).values[0].data[0]
            zRFcracktip2 = lastFrame.fieldOutputs['RF'].getSubset(region=dummy2Node,position=NODAL).values[0].data[1]
            #print('got reaction forces')
        else:
            connectorElcracktip1 = odb.rootAssembly.instances['PART-1-1'].elementSets['CONNECTORCRACKTIP1-ELEMENT']
            connectorElcracktip1label = connectorElcracktip1.elements[0].label
            connectorElcracktip2 = odb.rootAssembly.instances['PART-1-1'].elementSets['CONNECTORCRACKTIP2-ELEMENT']
            connectorElcracktip2label = connectorElcracktip2.elements[0].label
            for region in odb.steps[odb.steps.keys()[-1]].historyRegions.keys():
                if 'Node' not in region:
                    if str(connectorElcracktip1label) in region:
                        connectorElcracktip1histregion = region
                    elif str(connectorElcracktip2label) in region:
                        connectorElcracktip2histregion = region
            crf1key = ''
            crf2key = ''
            for key in odb.steps[odb.steps.keys()[-1]].historyRegions[connectorElcracktip1histregion].historyOutputs.keys():
                if 'CRF1' in key:
                    crf1key = key
                elif 'CRF2' in key:
                    crf2key = key
            if len(crf1key)>0 and len(crf2key)>0:
                crf1Hist = odb.steps[odb.steps.keys()[-1]].historyRegions[connectorElcracktip1histregion].historyOutputs[crf1key]
                crf2Hist = odb.steps[odb.steps.keys()[-1]].historyRegions[connectorElcracktip1histregion].historyOutputs[crf2key]
            xRFcracktip1 = crf1Hist.data[-1][1]
            zRFcracktip1 = crf2Hist.data[-1][1]
            crf1key = ''
            crf2key = ''
            for key in odb.steps[odb.steps.keys()[-1]].historyRegions[connectorElcracktip2histregion].historyOutputs.keys():
                if 'CRF1' in key:
                    crf1key = key
                elif 'CRF2' in key:
                    crf2key = key
            if len(crf1key)>0 and len(crf2key)>0:
                crf1Hist = odb.steps[odb.steps.keys()[-1]].historyRegions[connectorElcracktip2histregion].historyOutputs[crf1key]
                crf2Hist = odb.steps[odb.steps.keys()[-1]].historyRegions[connectorElcracktip2histregion].historyOutputs[crf2key]    
            xRFcracktip2 = crf1Hist.data[-1][1]
            zRFcracktip2 = crf2Hist.data[-1][1]
        
        rRFcracktip1 = numpy.cos(beta1)*xRFcracktip1 + numpy.sin(beta1)*zRFcracktip1
        thetaRFcracktip1 = -numpy.sin(beta1)*xRFcracktip1 + numpy.cos(beta1)*zRFcracktip1
        
        rRFcracktip2 = numpy.cos(beta2)*xRFcracktip2 + numpy.sin(beta2)*zRFcracktip2
        thetaRFcracktip2 = -numpy.sin(beta2)*xRFcracktip2 + numpy.cos(beta2)*zRFcracktip2
        #print('forces rotated')
        
        G1cracktip1 = enrrtFactor*numpy.abs(0.5*(rRFcracktip1*rdispcracktip1)/(Rf*deltaC))
        G2cracktip1 = enrrtFactor*numpy.abs(0.5*(thetaRFcracktip1*thetadispcracktip1)/(Rf*deltaC))
        G1cracktip2 = enrrtFactor*numpy.abs(0.5*(rRFcracktip2*rdispcracktip2)/(Rf*deltaC))
        G2cracktip2 = enrrtFactor*numpy.abs(0.5*(thetaRFcracktip2*thetadispcracktip2)/(Rf*deltaC))
        
        #print('Gs calculated')
        
        crackTip1 = [undeftip1.nodeLabel,
                        lengthFactor*undeftip1.data[0], lengthFactor*undeftip1.data[1],
                        lengthFactor*numpy.sqrt(numpy.power(undeftip1.data[0],2)+numpy.power(undeftip1.data[1],2)), numpy.arctan2(undeftip1.data[1],undeftip1.data[0])*180/numpy.pi,
                        lengthFactor*deftip1.data[0], lengthFactor*deftip1.data[1],
                        lengthFactor*numpy.sqrt(numpy.power(deftip1.data[0],2)+numpy.power(deftip1.data[1],2)), numpy.arctan2(deftip1.data[1],deftip1.data[0])*180/numpy.pi,
                        num, Gm, deltaC*180/numpy.pi, lengthFactor*rdispcracktip1, lengthFactor*thetadispcracktip1, forceFactor*rRFcracktip1, forceFactor*thetaRFcracktip1,
                        epsxx*Em/(1-num*num), sigmaInf, numpy.pi*lengthFactor*Rf*(epsxx*Em/(1-num*num))*(epsxx*Em/(1-num*num))*(1+(3.0-4.0*num))/(8.0*Gm), G0,
                        G1cracktip1, G2cracktip1, G1cracktip1+G2cracktip1, G1cracktip1/G0, G2cracktip1/G0, (G1cracktip1+G2cracktip1)/G0]
                                           
        crackTip2 = [undeftip2.nodeLabel,
                        lengthFactor*undeftip2.data[0], lengthFactor*undeftip2.data[1],
                        lengthFactor*numpy.sqrt(numpy.power(undeftip2.data[0],2)+numpy.power(undeftip2.data[1],2)), numpy.arctan2(undeftip2.data[1],undeftip2.data[0])*180/numpy.pi,
                        lengthFactor*deftip2.data[0], lengthFactor*deftip2.data[1],
                        lengthFactor*numpy.sqrt(numpy.power(deftip2.data[0],2)+numpy.power(deftip2.data[1],2)), numpy.arctan2(deftip2.data[1],deftip2.data[0])*180/numpy.pi,
                        num, Gm, deltaC*180/numpy.pi, lengthFactor*rdispcracktip2, lengthFactor*thetadispcracktip2, forceFactor*rRFcracktip2, forceFactor*thetaRFcracktip2,
                        epsxx*Em/(1-num*num), sigmaInf, numpy.pi*lengthFactor*Rf*(epsxx*Em/(1-num*num))*(epsxx*Em/(1-num*num))*(1+(3.0-4.0*num))/(8.0*Gm), G0,
                        G1cracktip2, G2cracktip2, G1cracktip2+G2cracktip2, G1cracktip2/G0, G2cracktip2/G0, (G1cracktip2+G2cracktip2)/G0]
        for tip in JINTs:
            if 'CONTOURINTEGRALCRACKTIP1-NODES' in tip[0]:
                for value in tip[1:]:
                    crackTip1.append(value)
            else:
                for value in tip[1:]:
                    crackTip2.append(value)
        for tip in JINToverG0s:
            if 'CONTOURINTEGRALCRACKTIP1-NODES' in tip[0]:
                for value in tip[1:]:
                    crackTip1.append(value)
            else:
                for value in tip[1:]:
                    crackTip2.append(value)
        
        crackTips.append(crackTip1)
        crackTips.append(crackTip2)
        
        print('data saved in list')
        
        line = 'NODE LABEL, X0 [m], Y0 [m], R0 [m], THETA0 [°], X [m], Y [m], R [m], THETA [°], nu [-], mu [Pa], deltaC [°], Disp_R, Disp_theta, RF_R, RF_theta, sigma_Inf_UNDAMAGED [Pa], sigma_Inf_DAMAGED [Pa], G0_UNDAMAGED [J/m^2], G0_DAMAGED [J/m^2], GI_M-VCCT [J/m^2], GII_M-VCCT [J/m^2], GTOT_M-VCCT [J/m^2], GI_M-VCCT/G0 [-], GII_M-VCCT/G0 [-], GTOT_M-VCCT/G0 [-]' 
        
        if len(JINTs)>0 and len(JINTs[0])>0:
            numJINTs = len(JINTs[0])-1
            secondline = ', , , , , , , , , , , , , , , , , , , , , , , , , '
            line += ', '
            secondline += ', '
            line += 'GTOT_ABQ-JINT [J/m^2]'
            secondline += 'Contour 1'
            for j in range(1,numJINTs):
                secondline += ', '
                secondline += 'Contour ' + str(j)
                line += ', '
            line += ', '
            secondline += ', '
            line += 'GTOT_ABQ-JINT/G0 [-]'
            secondline += 'Contour 1'
            for j in range(1,numJINTs):
                secondline += ', '
                secondline += 'Contour ' + str(j)
                line += ', '
        
        with open(join(csvfolder,'ENRRTs-Summary.csv'),'w') as csv:
            csv.write(line + '\n')
            csv.write(secondline + '\n')
            for tip in crackTips:
                line = ''
                for v,value in enumerate(tip):
                    if v>0:
                        line += ','
                    line += str(value)
                csv.write(line + '\n')
                    
    print('...done.\n')
    #=======================================================================
    # VCCT in stresses (trapezoidal integration for elements of equal length at the interface in the undeformed configuration)
    #=======================================================================
    print('\n')
    print('Compute energy release rates with VCCT in stresses...\n')
    
    crackTips = []
    
    if deltaTheta>0 and deltaTheta<180:
        # get crack tips' node sets
        matrixCrackTip1 = getSingleNodeSet(odb,'PART-1-1','MATRIXCRACKTIP1-NODE')
        fiberCrackTip1 = getSingleNodeSet(odb,'PART-1-1','FIBERCRACKTIP1-NODE')
        matrixCrackTip2 = getSingleNodeSet(odb,'PART-1-1','MATRIXCRACKTIP2-NODE')
        fiberCrackTip2 = getSingleNodeSet(odb,'PART-1-1','FIBERCRACKTIP2-NODE')
        #print('crack tips node sets')
        # get surface sections' node sets
        gamma2 = getSingleNodeSet(odb,'PART-1-1','GAMMA4-NODES')
        #print('gamma4 node set')
        # get crack tips' node labels
        matrixCrackTip1Label = int(lastFrame.fieldOutputs['COORD'].getSubset(position=NODAL).getSubset(region=matrixCrackTip1).values[0].nodeLabel)
        matrixCrackTip2Label = int(lastFrame.fieldOutputs['COORD'].getSubset(position=NODAL).getSubset(region=matrixCrackTip2).values[0].nodeLabel)
        #print('crack tips node labels')
        # get labels of nodes just before the crack tip on matrix side
        gamma2Labels = []
        for value in lastFrame.fieldOutputs['COORD'].getSubset(position=NODAL).getSubset(region=gamma2).values:
            gamma2Labels.append(int(value.nodeLabel))
        if matrixCrackTip1Label==4*N1*(N4+N5+1):
            if 4*N1*(N4+N5) in gamma2Labels:
                preMatrixCrackTip1Label = 4*N1*(N4+N5)
            else:
                preMatrixCrackTip1Label = matrixCrackTip1Label-1
        elif matrixCrackTip1Label==4*N1*(N4+N5):
            if matrixCrackTip1Label+1 in gamma2Labels:
                preMatrixCrackTip1Label = matrixCrackTip1Label+1
            else:
                preMatrixCrackTip1Label = 4*N1*(N4+N5+1)
        else:
            if matrixCrackTip1Label+1 in gamma2Labels:
                preMatrixCrackTip1Label = matrixCrackTip1Label+1
            else:
                preMatrixCrackTip1Label = matrixCrackTip1Label-1
        if matrixCrackTip2Label==4*N1*(N4+N5+1):
            if matrixCrackTip2Label-1 in gamma2Labels:
                preMatrixCrackTip1Label = matrixCrackTip2Label-1
            else:
                preMatrixCrackTip1Label = 4*N1*(N4+N5)
        elif matrixCrackTip2Label==4*N1*(N4+N5):
            if 4*N1*(N4+N5+1) in gamma2Labels:
                preMatrixCrackTip1Label = 4*N1*(N4+N5+1)
            else:
                preMatrixCrackTip1Label = matrixCrackTip2Label+1
        else:
            if matrixCrackTip2Label-1 in gamma2Labels:
                preMatrixCrackTip2Label = matrixCrackTip2Label-1
            else:
                preMatrixCrackTip2Label = matrixCrackTip2Label+1
        #print('node labels of crack tips on matrix side')
        # get crack tips' coordinates
        undeftip1 = firstFrame.fieldOutputs['COORD'].getSubset(position=NODAL).getSubset(region=matrixCrackTip1).values[0]
        deftip1 = lastFrame.fieldOutputs['COORD'].getSubset(position=NODAL).getSubset(region=matrixCrackTip1).values[0]
        undeftip2 = firstFrame.fieldOutputs['COORD'].getSubset(position=NODAL).getSubset(region=matrixCrackTip2).values[0]
        deftip2 = lastFrame.fieldOutputs['COORD'].getSubset(position=NODAL).getSubset(region=matrixCrackTip2).values[0]
        #print('crack tips coordinates')
        # define the orientation at crack tips
        beta1 = numpy.arctan2(undeftip1.data[1],undeftip1.data[0])
        beta2 = numpy.arctan2(undeftip2.data[1],undeftip2.data[0])
        #print('direction at crack tips')
        # compute energy release rates for crack tip 1
        dataMatrixSideCrackTip1 = []
        dataFiberSideCrackTip1 = []
        for elN in range(nEl0,NElMax+DeltaEl,DeltaEl):
            psMatrix = []
            psFiber = []
            if preMatrixCrackTip1Label<matrixCrackTip1Label:
                for n in range(0,elN+1,1):
                    # get matrix node before and after the crack tip
                    preMatrixNode = odb.rootAssembly.instances['PART-1-1'].getNodeFromLabel(matrixCrackTip1Label-(elN-n))
                    postMatrixNode = odb.rootAssembly.instances['PART-1-1'].getNodeFromLabel(matrixCrackTip1Label+n)
                    # get matrix node before and after the crack tip
                    preFiberNode = odb.rootAssembly.instances['PART-1-1'].getNodeFromLabel(matrixCrackTip1Label-(elN-n)+4*N1)
                    postFiberNode = odb.rootAssembly.instances['PART-1-1'].getNodeFromLabel(matrixCrackTip1Label+n+4*N1)
                    # get displacements on matrix and fiber
                    dispPreMatrixNode = lastFrame.fieldOutputs['U'].getSubset(position=NODAL).getSubset(region=preMatrixNode).values[0]
                    dispPreFiberNode = lastFrame.fieldOutputs['U'].getSubset(position=NODAL).getSubset(region=preFiberNode).values[0]
                    # calculate crack face displacement
                    xdisp = dispPreMatrixNode.data[0] - dispPreFiberNode.data[0]
                    zdisp = dispPreMatrixNode.data[1] - dispPreFiberNode.data[1]
                    # rotate displacements to crack tip local system
                    rdisp = numpy.cos(beta1)*xdisp + numpy.sin(beta1)*zdisp
                    thetadisp = -numpy.sin(beta1)*xdisp + numpy.cos(beta1)*zdisp
                    # get stresses on matrix and fiber
                    postMatrixStresses = getFieldOutput(odb,-1,-1,'S',postMatrixNode,3)
                    postFiberStresses = getFieldOutput(odb,-1,-1,'S',postFiberNode,3)
                    # define stress components on matrix
                    sxxMatrix = postMatrixStresses.values[0].data[0]
                    szzMatrix = postMatrixStresses.values[0].data[1]
                    sxzMatrix = postMatrixStresses.values[0].data[3]
                    # define stress components on matrix
                    sxxFiber = postFiberStresses.values[0].data[0]
                    szzFiber = postFiberStresses.values[0].data[1]
                    sxzFiber = postFiberStresses.values[0].data[3]
                    # rotate stress components on matrix
                    srrMatrix = numpy.power(numpy.cos(beta1),2)*sxxMatrix + 2*numpy.sin(beta1)*numpy.cos(beta1)*sxzMatrix + numpy.power(numpy.sin(beta1),2)*szzMatrix
                    srthetaMatrix = (sxxMatrix+szzMatrix)*numpy.cos(beta1)*numpy.sin(beta1) + sxzMatrix*(numpy.power(numpy.cos(beta1),2)-numpy.power(numpy.sin(beta1),2))
                    # rotate stress components on fiber
                    srrFiber = numpy.power(numpy.cos(beta1),2)*sxxFiber + 2*numpy.sin(beta1)*numpy.cos(beta1)*sxzFiber + numpy.power(numpy.sin(beta1),2)*szzFiber
                    srthetaFiber = (sxxFiber+szzFiber)*numpy.cos(beta1)*numpy.sin(beta1) + sxzFiber*(numpy.power(numpy.cos(beta1),2)-numpy.power(numpy.sin(beta1),2))
                    # compute products on matrix
                    prrMatrix = srrMatrix*rdisp
                    prthetaMatrix = srthetaMatrix*thetadisp
                    # compute products on fiber
                    prrFiber = srrFiber*rdisp
                    prthetaFiber = srthetaFiber*thetadisp
                    #save products to array
                    psMatrix.append([prrMatrix,prthetaMatrix])
                    psFiber.append([prrFiber,prthetaFiber])
            else:
                for n in range(0,elN+1,1):
                    # get matrix node before and after the crack tip
                    postMatrixNode = odb.rootAssembly.instances['PART-1-1'].getNodeFromLabel(matrixCrackTip1Label-(elN-n))
                    preMatrixNode = odb.rootAssembly.instances['PART-1-1'].getNodeFromLabel(matrixCrackTip1Label+n)
                    # get matrix node before and after the crack tip
                    postFiberNode = odb.rootAssembly.instances['PART-1-1'].getNodeFromLabel(matrixCrackTip1Label-(elN-n)+4*N1)
                    preFiberNode = odb.rootAssembly.instances['PART-1-1'].getNodeFromLabel(matrixCrackTip1Label+n+4*N1)
                    # get displacements on matrix and fiber
                    dispPreMatrixNode = lastFrame.fieldOutputs['U'].getSubset(position=NODAL).getSubset(region=preMatrixNode).values[0]
                    dispPreFiberNode = lastFrame.fieldOutputs['U'].getSubset(position=NODAL).getSubset(region=preFiberNode).values[0]
                    # calculate crack face displacement
                    xdisp = dispPreMatrixNode.data[0] - dispPreFiberNode.data[0]
                    zdisp = dispPreMatrixNode.data[1] - dispPreFiberNode.data[1]
                    # rotate displacements to crack tip local system
                    rdisp = numpy.cos(beta1)*xdisp + numpy.sin(beta1)*zdisp
                    thetadisp = -numpy.sin(beta1)*xdisp + numpy.cos(beta1)*zdisp
                    # get stresses on matrix and fiber
                    postMatrixStresses = getFieldOutput(odb,-1,-1,'S',postMatrixNode,3)
                    postFiberStresses = getFieldOutput(odb,-1,-1,'S',postFiberNode,3)
                    # define stress components on matrix
                    sxxMatrix = postMatrixStresses.values[0].data[0]
                    szzMatrix = postMatrixStresses.values[0].data[1]
                    sxzMatrix = postMatrixStresses.values[0].data[3]
                    # define stress components on matrix
                    sxxFiber = postFiberStresses.values[0].data[0]
                    szzFiber = postFiberStresses.values[0].data[1]
                    sxzFiber = postFiberStresses.values[0].data[3]
                    # rotate stress components on matrix
                    srrMatrix = numpy.power(numpy.cos(beta1),2)*sxxMatrix + 2*numpy.sin(beta1)*numpy.cos(beta1)*sxzMatrix + numpy.power(numpy.sin(beta1),2)*szzMatrix
                    srthetaMatrix = (sxxMatrix+szzMatrix)*numpy.cos(beta1)*numpy.sin(beta1) + sxzMatrix*(numpy.power(numpy.cos(beta1),2)-numpy.power(numpy.sin(beta1),2))
                    # rotate stress components on fiber
                    srrFiber = numpy.power(numpy.cos(beta1),2)*sxxFiber + 2*numpy.sin(beta1)*numpy.cos(beta1)*sxzFiber + numpy.power(numpy.sin(beta1),2)*szzFiber
                    srthetaFiber = (sxxFiber+szzFiber)*numpy.cos(beta1)*numpy.sin(beta1) + sxzFiber*(numpy.power(numpy.cos(beta1),2)-numpy.power(numpy.sin(beta1),2))
                    # compute products on matrix
                    prrMatrix = srrMatrix*rdisp
                    prthetaMatrix = srthetaMatrix*thetadisp
                    # compute products on fiber
                    prrFiber = srrFiber*rdisp
                    prthetaFiber = srthetaFiber*thetadisp
                    #save products to array
                    psMatrix.append([prrMatrix,prthetaMatrix])
                    psFiber.append([prrFiber,prthetaFiber])
            GI = 0
            GII = 0
            for e,element in enumerate(psMatrix):
                if e>0 and e<len(psMatrix)-1:
                    GI += 2*abs(psMatrix[e][0])
                    GII += 2*abs(psMatrix[e][1])
                else:
                    GI += abs(psMatrix[e][0])
                    GII += abs(psMatrix[e][1])
            GI *= 0.25/elN
            GII *= 0.25/elN
            dataMatrixSideCrackTip1.append([elN, enrrtFactor*GI, enrrtFactor*GII, enrrtFactor*(GI+GII), enrrtFactor*GI/G0, enrrtFactor*GII/G0, enrrtFactor*(GI+GII)/G0])
            GI = 0
            GII = 0
            for e,element in enumerate(psFiber):
                if e>0 and e<len(psFiber)-1:
                    GI += 2*abs(psFiber[e][0])
                    GII += 2*abs(psFiber[e][1])
                else:
                    GI += abs(psFiber[e][0])
                    GII += abs(psFiber[e][1])
            GI *= 0.25/elN
            GII *= 0.25/elN
            dataFiberSideCrackTip1.append([elN, enrrtFactor*GI, enrrtFactor*GII, enrrtFactor*(GI+GII), enrrtFactor*GI/G0, enrrtFactor*GII/G0, enrrtFactor*(GI+GII)/G0])
        #print('errt crack tip 1 calculated')
        # compute energy release rates for crack tip 2
        dataMatrixSideCrackTip2 = []
        dataFiberSideCrackTip2 = []
        for elN in range(nEl0,NElMax+DeltaEl,DeltaEl):
            psMatrix = []
            psFiber = []
            if preMatrixCrackTip2Label<matrixCrackTip2Label:
                for n in range(0,elN+1,1):
                    # get matrix node before and after the crack tip
                    preMatrixNode = odb.rootAssembly.instances['PART-1-1'].getNodeFromLabel(matrixCrackTip2Label-(elN-n))
                    postMatrixNode = odb.rootAssembly.instances['PART-1-1'].getNodeFromLabel(matrixCrackTip2Label+n)
                    # get matrix node before and after the crack tip
                    preFiberNode = odb.rootAssembly.instances['PART-1-1'].getNodeFromLabel(matrixCrackTip2Label-(elN-n)+4*N1)
                    postFiberNode = odb.rootAssembly.instances['PART-1-1'].getNodeFromLabel(matrixCrackTip2Label+n+4*N1)
                    # get displacements on matrix and fiber
                    dispPreMatrixNode = lastFrame.fieldOutputs['U'].getSubset(position=NODAL).getSubset(region=preMatrixNode).values[0]
                    dispPreFiberNode = lastFrame.fieldOutputs['U'].getSubset(position=NODAL).getSubset(region=preFiberNode).values[0]
                    # calculate crack face displacement
                    xdisp = dispPreMatrixNode.data[0] - dispPreFiberNode.data[0]
                    zdisp = dispPreMatrixNode.data[1] - dispPreFiberNode.data[1]
                    # rotate displacements to crack tip local system
                    rdisp = numpy.cos(beta2)*xdisp + numpy.sin(beta2)*zdisp
                    thetadisp = -numpy.sin(beta2)*xdisp + numpy.cos(beta2)*zdisp
                    # get stresses on matrix and fiber
                    postMatrixStresses = getFieldOutput(odb,-1,-1,'S',postMatrixNode,3)
                    postFiberStresses = getFieldOutput(odb,-1,-1,'S',postFiberNode,3)
                    # define stress components on matrix
                    sxxMatrix = postMatrixStresses.values[0].data[0]
                    szzMatrix = postMatrixStresses.values[0].data[1]
                    sxzMatrix = postMatrixStresses.values[0].data[3]
                    # define stress components on matrix
                    sxxFiber = postFiberStresses.values[0].data[0]
                    szzFiber = postFiberStresses.values[0].data[1]
                    sxzFiber = postFiberStresses.values[0].data[3]
                    # rotate stress components on matrix
                    srrMatrix = numpy.power(numpy.cos(beta2),2)*sxxMatrix + 2*numpy.sin(beta2)*numpy.cos(beta2)*sxzMatrix + numpy.power(numpy.sin(beta2),2)*szzMatrix
                    srthetaMatrix = (sxxMatrix+szzMatrix)*numpy.cos(beta2)*numpy.sin(beta2) + sxzMatrix*(numpy.power(numpy.cos(beta2),2)-numpy.power(numpy.sin(beta2),2))
                    # rotate stress components on fiber
                    srrFiber = numpy.power(numpy.cos(beta2),2)*sxxFiber + 2*numpy.sin(beta2)*numpy.cos(beta2)*sxzFiber + numpy.power(numpy.sin(beta2),2)*szzFiber
                    srthetaFiber = (sxxFiber+szzFiber)*numpy.cos(beta2)*numpy.sin(beta2) + sxzFiber*(numpy.power(numpy.cos(beta2),2)-numpy.power(numpy.sin(beta2),2))
                    # compute products on matrix
                    prrMatrix = srrMatrix*rdisp
                    prthetaMatrix = srthetaMatrix*thetadisp
                    # compute products on fiber
                    prrFiber = srrFiber*rdisp
                    prthetaFiber = srthetaFiber*thetadisp
                    #save products to array
                    psMatrix.append([prrMatrix,prthetaMatrix])
                    psFiber.append([prrFiber,prthetaFiber])
            else:
                for n in range(0,elN+1,1):
                    # get matrix node before and after the crack tip
                    postMatrixNode = odb.rootAssembly.instances['PART-1-1'].getNodeFromLabel(matrixCrackTip2Label-(elN-n))
                    preMatrixNode = odb.rootAssembly.instances['PART-1-1'].getNodeFromLabel(matrixCrackTip2Label+n)
                    # get matrix node before and after the crack tip
                    postFiberNode = odb.rootAssembly.instances['PART-1-1'].getNodeFromLabel(matrixCrackTip2Label-(elN-n)+4*N1)
                    preFiberNode = odb.rootAssembly.instances['PART-1-1'].getNodeFromLabel(matrixCrackTip2Label+n+4*N1)
                    # get displacements on matrix and fiber
                    dispPreMatrixNode = lastFrame.fieldOutputs['U'].getSubset(position=NODAL).getSubset(region=preMatrixNode).values[0]
                    dispPreFiberNode = lastFrame.fieldOutputs['U'].getSubset(position=NODAL).getSubset(region=preFiberNode).values[0]
                    # calculate crack face displacement
                    xdisp = dispPreMatrixNode.data[0] - dispPreFiberNode.data[0]
                    zdisp = dispPreMatrixNode.data[1] - dispPreFiberNode.data[1]
                    # rotate displacements to crack tip local system
                    rdisp = numpy.cos(beta2)*xdisp + numpy.sin(beta2)*zdisp
                    thetadisp = -numpy.sin(beta2)*xdisp + numpy.cos(beta2)*zdisp
                    # get stresses on matrix and fiber
                    postMatrixStresses = getFieldOutput(odb,-1,-1,'S',postMatrixNode,3)
                    postFiberStresses = getFieldOutput(odb,-1,-1,'S',postFiberNode,3)
                    # define stress components on matrix
                    sxxMatrix = postMatrixStresses.values[0].data[0]
                    szzMatrix = postMatrixStresses.values[0].data[1]
                    sxzMatrix = postMatrixStresses.values[0].data[3]
                    # define stress components on matrix
                    sxxFiber = postFiberStresses.values[0].data[0]
                    szzFiber = postFiberStresses.values[0].data[1]
                    sxzFiber = postFiberStresses.values[0].data[3]
                    # rotate stress components on matrix
                    srrMatrix = numpy.power(numpy.cos(beta2),2)*sxxMatrix + 2*numpy.sin(beta2)*numpy.cos(beta2)*sxzMatrix + numpy.power(numpy.sin(beta2),2)*szzMatrix
                    srthetaMatrix = (sxxMatrix+szzMatrix)*numpy.cos(beta2)*numpy.sin(beta2) + sxzMatrix*(numpy.power(numpy.cos(beta2),2)-numpy.power(numpy.sin(beta2),2))
                    # rotate stress components on fiber
                    srrFiber = numpy.power(numpy.cos(beta2),2)*sxxFiber + 2*numpy.sin(beta2)*numpy.cos(beta2)*sxzFiber + numpy.power(numpy.sin(beta2),2)*szzFiber
                    srthetaFiber = (sxxFiber+szzFiber)*numpy.cos(beta2)*numpy.sin(beta2) + sxzFiber*(numpy.power(numpy.cos(beta2),2)-numpy.power(numpy.sin(beta2),2))
                    # compute products on matrix
                    prrMatrix = srrMatrix*rdisp
                    prthetaMatrix = srthetaMatrix*thetadisp
                    # compute products on fiber
                    prrFiber = srrFiber*rdisp
                    prthetaFiber = srthetaFiber*thetadisp
                    #save products to array
                    psMatrix.append([prrMatrix,prthetaMatrix])
                    psFiber.append([prrFiber,prthetaFiber])
            GI = 0
            GII = 0
            for e,element in enumerate(psMatrix):
                if e>0 and e<len(psMatrix)-1:
                    GI += 2*abs(psMatrix[e][0])
                    GII += 2*abs(psMatrix[e][1])
                else:
                    GI += abs(psMatrix[e][0])
                    GII += abs(psMatrix[e][1])
            GI *= 0.25/elN
            GII *= 0.25/elN
            dataMatrixSideCrackTip2.append([elN, enrrtFactor*GI, enrrtFactor*GII, enrrtFactor*(GI+GII), enrrtFactor*GI/G0, enrrtFactor*GII/G0, enrrtFactor*(GI+GII)/G0])
            GI = 0
            GII = 0
            for e,element in enumerate(psFiber):
                if e>0 and e<len(psFiber)-1:
                    GI += 2*abs(psFiber[e][0])
                    GII += 2*abs(psFiber[e][1])
                else:
                    GI += abs(psFiber[e][0])
                    GII += abs(psFiber[e][1])
            GI *= 0.25/elN
            GII *= 0.25/elN
            dataFiberSideCrackTip2.append([elN, enrrtFactor*GI, enrrtFactor*GII, enrrtFactor*(GI+GII), enrrtFactor*GI/G0, enrrtFactor*GII/G0, enrrtFactor*(GI+GII)/G0])
        #print('errts crack tip  2 calculated')
        #print('Gs calculated')
        
        crackTip1 = [undeftip1.nodeLabel,
                     lengthFactor*undeftip1.data[0], lengthFactor*undeftip1.data[1],
                     lengthFactor*numpy.sqrt(numpy.power(undeftip1.data[0],2)+numpy.power(undeftip1.data[1],2)), numpy.arctan2(undeftip1.data[1],undeftip1.data[0])*180/numpy.pi,
                     lengthFactor*deftip1.data[0], lengthFactor*deftip1.data[1],
                     lengthFactor*numpy.sqrt(numpy.power(deftip1.data[0],2)+numpy.power(deftip1.data[1],2)), numpy.arctan2(deftip1.data[1],deftip1.data[0])*180/numpy.pi,
                     num, Gm, deltaC*180/numpy.pi,
                        epsxx*Em/(1-num*num), sigmaInf, numpy.pi*lengthFactor*Rf*(epsxx*Em/(1-num*num))*(epsxx*Em/(1-num*num))*(1+(3.0-4.0*num))/(8.0*Gm), G0]
                                           
        crackTip2 = [undeftip2.nodeLabel,
                     lengthFactor*undeftip2.data[0], lengthFactor*undeftip2.data[1],
                     lengthFactor*numpy.sqrt(numpy.power(undeftip2.data[0],2)+numpy.power(undeftip2.data[1],2)), numpy.arctan2(undeftip2.data[1],undeftip2.data[0])*180/numpy.pi,
                     lengthFactor*deftip2.data[0], lengthFactor*deftip2.data[1],
                     lengthFactor*numpy.sqrt(numpy.power(deftip2.data[0],2)+numpy.power(deftip2.data[1],2)), numpy.arctan2(deftip2.data[1],deftip2.data[0])*180/numpy.pi,
                     num, Gm, deltaC*180/numpy.pi,
                        epsxx*Em/(1-num*num), sigmaInf, numpy.pi*lengthFactor*Rf*(epsxx*Em/(1-num*num))*(epsxx*Em/(1-num*num))*(1+(3.0-4.0*num))/(8.0*Gm), G0]
        
        for v in range(1,len(dataMatrixSideCrackTip1[0])):
            for data in dataMatrixSideCrackTip1:
                crackTip1.append(data[v])
        for v in range(1,len(dataFiberSideCrackTip1[0])):
            for data in dataFiberSideCrackTip1:
                crackTip1.append(data[v])
        
        for v in range(1,len(dataMatrixSideCrackTip2[0])):
            for data in dataMatrixSideCrackTip2:
                crackTip2.append(data[v])
        for v in range(1,len(dataFiberSideCrackTip2[0])):
            for data in dataFiberSideCrackTip2:
                crackTip2.append(data[v])
        
        crackTips.append(crackTip1)
        crackTips.append(crackTip2)
        
        #print('data saved in list')
        
        line = 'NODE LABEL, X0 [m], Y0 [m], R0 [m], THETA0 [°], X [m], Y [m], R [m], THETA [°], nu [-], mu [Pa], deltaC [°], sigma_Inf_UNDAMAGED [Pa], sigma_Inf_DAMAGED [Pa], G0_UNDAMAGED [J/m^2], G0_DAMAGED [J/m^2], '
        secondline = ' , , , , , , , , , , , , , , , , '
        
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
        
        with open(join(csvfolder,'ENRRTs-VCCTinStresses-Summary.csv'),'w') as csv:
            csv.write(line + '\n')
            csv.write(secondline + '\n')
            for tip in crackTips:
                line = ''
                for v,value in enumerate(tip):
                    if v>0:
                        line += ','
                    line += str(value)
                csv.write(line + '\n')
    #print('data written to file')                
    print('...done.\n')
    #=======================================================================
    # close database
    #=======================================================================
    print('\n')
    print('Close database...\n')
    odb.close()
    print('...done.\n')