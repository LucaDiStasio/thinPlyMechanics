#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
=====================================================================================

Copyright (c) 2016-2018 Université de Lorraine or Luleå tekniska universitet
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
import sys, os
import numpy as np
from os.path import isfile
from datetime import datetime
from time import strftime, sleep
import timeit
from abaqus import *
from abaqusConstants import *
import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior
#import __main__

#===============================================================================#
#===============================================================================#
#                              I/O functions
#===============================================================================#
#===============================================================================#

def createCSVfile(dir,filename,titleline=None):
    if len(filename.split('.'))<2:
        filename += '.csv'
    with open(join(dir,filename),'w') as csv:
        csv.write('# Automatically created on ' + datetime.now().strftime('%d/%m/%Y') + ' at' + datetime.now().strftime('%H:%M:%S') + '\n')
        if titleline != None:
            csv.write(titleline.replace('\n','') + '\n')

def appendCSVfile(dir,filename,data):
    # data is a list of lists
    # each list is written to a row
    # no check is made on data consistency
    if len(filename.split('.'))<2:
        filename += '.csv'
    with open(join(dir,filename),'a') as csv:
        if len(data)>1 and len(data[0]>1):
            for row in data:
                line = ''
                for v,value in enumerate(row):
                    if v>1:
                        line += ', '
                    line += str(value)
                csv.write(line + '\n')
        else:
            line = ''
            for v,value in enumerate(data):
                if v>1:
                    line += ', '
                line += str(value)
            csv.write(line + '\n')

def createABQinpfile(path):
    with open(path,'w') as fi:
        fi.write('** ABAQUS INPUT FILE' + '\n')
        fi.write('** Automatically created on ' + datetime.now().strftime('%d/%m/%Y') + ' at' + datetime.now().strftime('%H:%M:%S') + '\n')
        fi.write('**' + '\n')
        fi.write('**==============================================================================' + '\n')
        fi.write('** Copyright (c) 2016-2018 Universite de Lorraine & Lulea tekniska universitet' + '\n')
        fi.write('** Author: Luca Di Stasio <luca.distasio@gmail.com>' + '\n')
        fi.write('**                        <luca.distasio@ingpec.eu>' + '\n')
        fi.write('**' + '\n')
        fi.write('** Redistribution and use in source and binary forms, with or without' + '\n')
        fi.write('** modification, are permitted provided that the following conditions are met:' + '\n')
        fi.write('**'  + '\n')
        fi.write('** Redistributions of source code must retain the above copyright' + '\n')
        fi.write('** notice, this list of conditions and the following disclaimer.' + '\n')
        fi.write('** Redistributions in binary form must reproduce the above copyright' + '\n')
        fi.write('** notice, this list of conditions and the following disclaimer in' + '\n')
        fi.write('** the documentation and/or other materials provided with the distribution' + '\n')
        fi.write('** Neither the name of the Universite de Lorraine or Lulea tekniska universitet' + '\n')
        fi.write('** nor the names of its contributors may be used to endorse or promote products' + '\n')
        fi.write('** derived from this software without specific prior written permission.' + '\n')
        fi.write('**'  + '\n')
        fi.write('** THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"' + '\n')
        fi.write('** AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE' + '\n')
        fi.write('** IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE' + '\n')
        fi.write('** ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE' + '\n')
        fi.write('** LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR' + '\n')
        fi.write('** CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF' + '\n')
        fi.write('** SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS' + '\n')
        fi.write('** INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN' + '\n')
        fi.write('** CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)' + '\n')
        fi.write('** ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE' + '\n')
        fi.write('** POSSIBILITY OF SUCH DAMAGE.' + '\n')
        fi.write('**==============================================================================' + '\n')
        fi.write('**' + '\n')
        
def writeLineToLogFile(logFileFullPath,mode,line,toScreen):
    with open(logFileFullPath,mode) as log:
        log.write(line + '\n')
    if toScreen:
        print(line + '\n')

def skipLineToLogFile(logFileFullPath,mode,toScreen):
    with open(logFileFullPath,mode) as log:
        log.write('\n')
    if toScreen:
        print('\n')

def writeTitleSepLineToLogFile(logFileFullPath,mode,toScreen):
    with open(logFileFullPath,mode) as log:
        log.write('===============================================================================================\n')
    if toScreen:
        print('===============================================================================================\n')

def writeTitleSecToLogFile(logFileFullPath,mode,title,toScreen):
    writeTitleSepLineToLogFile(logFileFullPath,mode,toScreen)
    writeTitleSepLineToLogFile(logFileFullPath,'a',toScreen)
    skipLineToLogFile(logFileFullPath,'a',toScreen)
    writeLineToLogFile(logFileFullPath,'a',title,toScreen)
    skipLineToLogFile(logFileFullPath,'a',toScreen)
    writeLineToLogFile(logFileFullPath,'a','Starting on ' + datetime.now().strftime('%Y-%m-%d') + ' at ' + datetime.now().strftime('%H:%M:%S'),toScreen)
    skipLineToLogFile(logFileFullPath,'a',toScreen)
    writeLineToLogFile(logFileFullPath,'a','Platform: ' + platform(),toScreen)
    skipLineToLogFile(logFileFullPath,'a',toScreen)
    writeTitleSepLineToLogFile(logFileFullPath,'a',toScreen)
    writeTitleSepLineToLogFile(logFileFullPath,'a',toScreen)
    skipLineToLogFile(logFileFullPath,'a',toScreen)

def writeErrorToLogFile(logFileFullPath,mode,exc,err,toScreen):
    with open(logFileFullPath,mode) as log:
        log.write('!!! ----------------------------------------------------------------------------------------!!!\n')
        log.write('\n')
        log.write('                                     AN ERROR OCCURED\n')
        log.write('\n')
        log.write('                                -------------------------\n')
        log.write('\n')
        log.write(str(exc) + '\n')
        log.write(str(err) + '\n')
        log.write('\n')
        log.write('Terminating program\n')
        log.write('\n')
        log.write('!!! ----------------------------------------------------------------------------------------!!!\n')
        log.write('\n')
    if toScreen:
        print('!!! ----------------------------------------------------------------------------------------!!!\n')
        print('\n')
        print('                                     AN ERROR OCCURED\n')
        print('\n')
        print('                                -------------------------\n')
        print('\n')
        print(str(exc) + '\n')
        print(str(err) + '\n')
        print('\n')
        print('Terminating program\n')
        print('\n')
        print('!!! ----------------------------------------------------------------------------------------!!!\n')
        print('\n')

def writePerfToFile(od,outfile,performanceslist):
    with open(join(od,outfile),'w') as csv:
        for performances in performanceslist:
            line = ''
            for i,performance in enumerate(performances):
                if i>0:
                    line += ','
                line += str(performance)
            csv.write(line + '\n')
            
#===============================================================================#
#===============================================================================#
#                        Data analysis functions
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
        if exists(join(wd,sim+'.dat')):
            with open(join(wd,sim+'.dat'),'r') as dat:
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
        if exists(join(wd,sim+'.msg')):
            with open(join(wd,sim,'solver',sim+'.msg'),'r') as msg:
                lines = msg.readlines()
                for line in lines:
                    if 'USING THE DIRECT SOLVER WITH' in line:
                        words = line.replace('\n','').split(' ')
                        while '' in words: words.remove('')
                        cpus = int(words[words.index('PROCESSORS')-1])
        perf.append([sim,cpus,usertime,systemtime,usertime/totalcpu,systemtime/totalcpu,totalcpu,wallclock,wallclock/60.,wallclock/3600.,wallclock/totalcpu,floatops,minMemory,minIOmemory,totEl,userEl,progEl,totN,userN,progN,totVar])
    return perf

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
    coords = allCoords.getSubset(region=odbObj.rootAssembly.instances[part].nodeSets[nodeSet])
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
        if len(nodeSets[nodeSetsData[0][3]].values[0].data)==1:
            string = 'X'
        elif len(nodeSets[nodeSetsData[0][3]].values[0].data)==2:
            string = 'X, Y'
        elif len(nodeSets[nodeSetsData[0][3]].values[0].data)==3:
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

def getJintegrals(wd,sim,ncontours):
    with open(join(wd,sim + '.dat'),'r') as dat:
        lines = dat.readlines()
    values = []
    for l,line in enumerate(lines):
        if 'J - I N T E G R A L   E S T I M A T E S' in line:
            for n in range(1,int(np.ceil(ncontours/5))+1):
                if n>1:
                    temp = filter(lambda x: x!=' ' and x!='', lines[l+6+int(np.ceil(ncontours/5))+n].replace('\n','').split(' '))
                else:
                    temp = filter(lambda x: x!=' ' and x!='', lines[l+6+int(np.ceil(ncontours/5))+n].replace('\n','').split(' '))[2:]
                for value in temp:
                    values.append(float(value))
            break
    return values
    
#===============================================================================#
#===============================================================================#
#                        Model creation functions
#===============================================================================#
#===============================================================================#
    
def createRVE(parameters,logfilepath,baselogindent,logindent):
#===============================================================================#
#                               Parameters
#===============================================================================#
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + 'In function: createRVE(parameters,logfilepath,logindent)',True)
    # assign most used parameters to variables
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Read and assign most used parameters to variables ...',True)
    wd = parameters['input']['wd']
    caefilename = parameters['input']['caefilename']
    modelname = parameters['input']['modelname']
    L = parameters['geometry']['L']
    Rf = parameters['geometry']['Rf']
    theta = 0.0
    deltatheta = parameters['geometry']['deltatheta'] # in degrees !!!
    deltapsi = parameters['mesh']['size']['deltapsi'] # in degrees !!!
    deltaphi = parameters['mesh']['size']['deltaphi'] # in degrees !!!
    delta = parameters['mesh']['size']['delta'] # in degrees !!!
    minElNum = parameters['mesh']['elements']['minElNum']
    if ((theta+deltatheta-deltapsi)<=0.0 or (theta+deltatheta-deltapsi)/delta<minElNum) and ((theta+deltatheta+deltapsi+deltaphi)>=180.0 or (180.0-(theta+deltatheta+deltapsi+deltaphi))/delta<minElNum):
        deltapsi = 0.6*((180.0-(theta+deltatheta))-np.max([0.5*(theta+deltatheta),0.1*(180.0-(theta+deltatheta)),minElnum*delta]))
        deltaphi = 0.4*((180.0-(theta+deltatheta))-np.max([0.5*(theta+deltatheta),0.1*(180.0-(theta+deltatheta)),minElnum*delta]))
    elif (theta+deltatheta-deltapsi)<=0.0 or (theta+deltatheta-deltapsi)/delta<minElNum:
        deltapsi = (theta+deltatheta) - np.max([0.5*(theta+deltatheta),minElnum*delta])
    elif (theta+deltatheta+deltapsi+deltaphi)>=180.0 or (180.0-(theta+deltatheta+deltapsi+deltaphi))/delta<minElNum:
        deltapsi = 0.6*((180.0-(theta+deltatheta))-np.max([0.1*(180.0-(theta+deltatheta)),minElnum*delta]))
        deltaphi = 0.4*((180.0-(theta+deltatheta))-np.max([0.1*(180.0-(theta+deltatheta)),minElnum*delta]))
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Working directory: ' + wd,True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'CAE database name: ' + caefilename,True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Model name: ' + modelname,True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'L: ' + str(L),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Rf: ' + str(Rf),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'L/Rf: ' + str(L/Rf),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'theta: ' + str(theta),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'deltatheta: ' + str(deltatheta),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'deltapsi: ' + str(deltapsi),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'deltaphi: ' + str(deltaphi),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'delta: ' + str(delta),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'minElnum: ' + str(minElnum),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
#===============================================================================#
#                          Model database creation
#===============================================================================#
# if CAE database exists, open it; otherwise create new one
    caefullpath = join(wd,caefilename)
    if isfile(caefullpath):
        skipLineToLogFile(logfilepath,'a',True)
        writeLineToLogFile(logfilepath,'a',baselogindent + logindent + 'CAE database already exists. Opening it ...',True)
        openMdb(caefullpath)
        writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    else:
        skipLineToLogFile(logfilepath,'a',True)
        writeLineToLogFile(logfilepath,'a',baselogindent + logindent + 'CAE database does not exist. Creating it ...',True)
        mdb.saveAs(caefullpath)
        writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    # assign model object to variable for lighter code
    model = mdb.models[modelname]
#===============================================================================#
#                             Parts creation
#===============================================================================#
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + 'Creating part ...',True)
    # create sketch
    RVEsketch = model.ConstrainedSketch(name='__profile__', 
        sheetSize=3*L)
    RVEsketch.setPrimaryObject(option=STANDALONE)
    # create rectangle
    RVEsketch.rectangle(point1=(-L, 0.0), point2=(L,L))
    # set dimension labels
    RVEsketch.ObliqueDimension(vertex1=v[0], vertex2=v[1], textPoint=(-1.1*L,0.5*L), value=L)
    RVEsketch.ObliqueDimension(vertex1=v[1], vertex2=v[2], textPoint=(0.0,1.1*L), value=2*L)
    # assign to part
    RVEpart = model.Part(name='RVE',dimensionality=TWO_D_PLANAR,type=DEFORMABLE_BODY)
    RVEpart = model.parts['RVE']
    RVEpart.BaseShell(sketch=RVEsketch)
    RVEsketch.unsetPrimaryObject()
    del model.sketches['__profile__']
    # create reference to geometrical objects (faces, edges and vertices) of the part
    RVEfaces = RVEpart.faces
    RVEedges = RVEpart.edges
    RVEvertices = RVEpart.vertices
    # create geometrical transform to draw partition sketch
    transformToSketch = RVEpart.MakeSketchTransform(sketchPlane=RVEfaces[0], sketchPlaneSide=SIDE1, origin=(0.0,0.5*L, 0.0))
    # create sketch
    fiberSketch = model.ConstrainedSketch(name='fiberSketch',sheetSize=3*L, gridSpacing=L/100.0, transform=transformToSketch)
    fiberSketch = model.sketches['fiberSketch']
    # create reference to geometrical objects (faces, edges and vertices) of the partition sketch
    fiberGeometry = fiberSketch.geometry
    fiberVertices = fiberSketch.vertices
    fiberSketch.setPrimaryObject(option=SUPERIMPOSE)
    #p = mdb.models[modelname].parts['RVE']
    RVEpart.projectReferencesOntoSketch(sketch=fiberSketch, filter=COPLANAR_EDGES)
    # draw fiber and circular sections for mesh generation
    fiberSketch.ArcByCenterEnds(center=(0.0, -0.5*L), point1=(-Rf, -0.5*L), point2=(Rf,-0.5*L), direction=CLOCKWISE) # fiberGeometry[6]
    fiberSketch.ArcByCenterEnds(center=(0.0, -0.5*L), point1=(-0.75*Rf, -0.5*L), point2=(0.75*Rf,-0.5*L), direction=CLOCKWISE) # fiberGeometry[7]
    fiberSketch.ArcByCenterEnds(center=(0.0, -0.5*L), point1=(-0.5*Rf, -0.5*L), point2=(0.5*Rf,-0.5*L), direction=CLOCKWISE) # fiberGeometry[8]
    if L>2*Rf:
        fiberSketch.ArcByCenterEnds(center=(0.0, -0.5*L), point1=(-1.25*Rf, -0.5*L), point2=(1.25*Rf,-0.5*L), direction=CLOCKWISE) # fiberGeometry[9]
        fiberSketch.ArcByCenterEnds(center=(0.0, -0.5*L), point1=(-1.5*Rf, -0.5*L), point2=(1.5*Rf,-0.5*L), direction=CLOCKWISE) # fiberGeometry[10]
    else:
        fiberSketch.ArcByCenterEnds(center=(0.0, -0.5*L), point1=(-(Rf+0.25*(L-Rf)), -0.5*L), point2=((Rf+0.25*(L-Rf)),-0.5*L), direction=CLOCKWISE) # fiberGeometry[9]
        fiberSketch.ArcByCenterEnds(center=(0.0, -0.5*L), point1=(-(Rf+0.5*(L-Rf)), -0.5*L), point2=((Rf+0.5*(L-Rf)),-0.5*L), direction=CLOCKWISE) # fiberGeometry[10]
    
    # calculate angles for construction lines    
    alpha = theta + deltatheta - deltapsi
    beta = theta + deltatheta + deltapsi
    gamma = theta + deltatheta + deltapsi + deltaphi
    
    # draw construction lines  
    fiberSketch.ConstructionLine(point1=(0.0, -0.5*L), angle=(theta+deltatheta)) # fiberGeometry[11]
    fiberSketch.CoincidentConstraint(entity1=fiberVertices[6], entity2=fiberGeometry[11],addUndoState=False)
    
    fiberSketch.ConstructionLine(point1=(0.0, -0.5*L), angle=alpha) # fiberGeometry[12]
    fiberSketch.CoincidentConstraint(entity1=fiberVertices[6], entity2=fiberGeometry[12],addUndoState=False)
    
    fiberSketch.ConstructionLine(point1=(0.0, -0.5*L), angle=beta) # fiberGeometry[13]
    fiberSketch.CoincidentConstraint(entity1=fiberVertices[6], entity2=fiberGeometry[13],addUndoState=False)
    
    fiberSketch.ConstructionLine(point1=(0.0, -0.5*L), angle=gamma) # fiberGeometry[14]
    fiberSketch.CoincidentConstraint(entity1=fiberVertices[6], entity2=fiberGeometry[14],addUndoState=False)
    
    # draw angular sections to identify the crack and for mesh generation
    Rint = 0.75*Rf
    if L>2*Rf:
        Rext = 1.25*Rf
    else:
        Rext = Rf+0.25*(L-Rf)
    
    Ax = Rint*np.cos(alpha*np.pi/180.0)
    Ay = -0.5*L+Rint*np.sin(alpha*np.pi/180.0)
    Bx = Rext*np.cos(alpha*np.pi/180.0)
    By = -0.5*L+Rint*np.sin(alpha*np.pi/180.0)
    fiberSketch.Line(point1=(Ax,Ay),point2=(Bx,By)) # fiberGeometry[15]
    fiberSketch.PerpendicularConstraint(entity1=fiberGeometry[7], entity2=fiberGeometry[15],addUndoState=False)
    fiberSketch.CoincidentConstraint(entity1=fiberVertices[15], entity2=fiberGeometry[7],addUndoState=False)
    fiberSketch.CoincidentConstraint(entity1=fiberVertices[16], entity2=fiberGeometry[9],addUndoState=False)
    
    Ax = Rint*np.cos((theta+deltatheta)*np.pi/180.0)
    Ay = -0.5*L+Rint*np.sin((theta+deltatheta)*np.pi/180.0)
    Bx = Rext*np.cos((theta+deltatheta)*np.pi/180.0)
    By = -0.5*L+Rext*np.sin((theta+deltatheta)*np.pi/180.0)
    fiberSketch.Line(point1=(Ax,Ay),point2=(Bx,By)) # fiberGeometry[16]
    fiberSketch.PerpendicularConstraint(entity1=fiberGeometry[7], entity2=fiberGeometry[16],addUndoState=False)
    fiberSketch.CoincidentConstraint(entity1=fiberVertices[17], entity2=fiberGeometry[7],addUndoState=False)
    fiberSketch.CoincidentConstraint(entity1=fiberVertices[18], entity2=fiberGeometry[9],addUndoState=False)
    
    Ax = Rint*np.cos(beta*np.pi/180.0)
    Ay = -0.5*L+Rint*np.sin(beta*np.pi/180.0)
    Bx = Rext*np.cos(beta*np.pi/180.0)
    By = -0.5*L+Rext*np.sin(beta*np.pi/180.0)
    fiberSketch.Line(point1=(Ax,Ay),point2=(Bx,By)) # fiberGeometry[17]
    fiberSketch.PerpendicularConstraint(entity1=fiberGeometry[7], entity2=fiberGeometry[17],addUndoState=False)
    fiberSketch.CoincidentConstraint(entity1=fiberVertices[19], entity2=fiberGeometry[7],addUndoState=False)
    fiberSketch.CoincidentConstraint(entity1=fiberVertices[20], entity2=fiberGeometry[9],addUndoState=False)
    
    Ax = Rint*np.cos(gamma*np.pi/180.0)
    Ay = -0.5*L+Rint*np.sin(gamma*np.pi/180.0)
    Bx = Rext*np.cos(gamma*np.pi/180.0)
    By = -0.5*L+Rext*np.sin(gamma*np.pi/180.0)
    fiberSketch.Line(point1=(Ax,Ay),point2=(Bx,By)) # fiberGeometry[18]
    fiberSketch.PerpendicularConstraint(entity1=fiberGeometry[7], entity2=fiberGeometry[18],addUndoState=False)
    fiberSketch.CoincidentConstraint(entity1=fiberVertices[25], entity2=fiberGeometry[7],addUndoState=False)
    fiberSketch.CoincidentConstraint(entity1=fiberVertices[26], entity2=fiberGeometry[9],addUndoState=False)
    
    pickedFaces = RVEfaces.findAt(coordinates=(0.0, 0.5*L, 0))
    RVEpart.PartitionFaceBySketch(faces=pickedFaces, sketch=fiberSketch)
    fiberSketch.unsetPrimaryObject()
    del model.sketches['__profile__']
    
    #-------------------#
    #                   #
    #    create sets    #
    #                   #
    #-------------------#
    
    # create reference to geometric elements for lighter code
    RVEvertices = RVEpart.vertices
    RVEedges = RVEpart.edges
    RVEfaces = RVEpart.faces
    
    # sets of vertices
    crackTip = RVEvertices.getByBoundingSphere(center=(Rf*np.cos((theta+deltatheta)*np.pi/180),Rf*np.sin((theta+deltatheta)*np.pi/180),0.0),radius=0.001*Rf)
    RVEpart.Set(vertices=crackTip, name='CRACKTIP')
    
    # sets of edges
    crackEdge1=RVEedges.getByBoundingSphere(center=(Rf*np.cos(0.5*alpha*np.pi/180),Rf*np.sin(0.5*alpha*np.pi/180),0.0),radius=0.01*Rf)
    crackEdge2=RVEedges.getByBoundingSphere(center=(Rf*np.cos((alpha+0.5*deltapsi)*np.pi/180),Rf*np.sin((alpha+0.5*deltapsi)*np.pi/180),0.0),radius=0.01*Rf)
    RVEpart.Set(edges=crackEdge1, name='CRACK-LOWER')
    RVEpart.Set(edges=crackEdge2, name='CRACK-UPPER')
    RVEpart.SetByBoolean(name='CRACK', sets=[RVEpart.sets['CRACK-LOWER'],RVEpart.sets['CRACK-UPPER']])
    
    RVEpart.Set(edges=crackEdge1, name='LOWERSIDE-CENTER')
    
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(0.001*Rf,0.0,0.0),radius=0.001*Rf), name='LOWERSIDE-CENTER')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(0.65*Rf,0.0,0.0),radius=0.001*Rf), name='LOWERSIDE-FIRSTRING-RIGHT')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(-0.65*Rf,0.0,0.0),radius=0.001*Rf), name='LOWERSIDE-FIRSTRING-LEFT')
    RVEpart.SetByBoolean(name='LOWERSIDE-FIRSTRING', sets=[RVEpart.sets['LOWERSIDE-FIRSTRING-RIGHT'],RVEpart.sets['LOWERSIDE-FIRSTRING-LEFT']])
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(0.85*Rf,0.0,0.0),radius=0.001*Rf), name='LOWERSIDE-SECONDRING-RIGHT')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(-0.85*Rf,0.0,0.0),radius=0.001*Rf), name='LOWERSIDE-SECONDRING-LEFT')
    RVEpart.SetByBoolean(name='LOWERSIDE-SECONDRING', sets=[RVEpart.sets['LOWERSIDE-SECONDRING-RIGHT'],RVEpart.sets['LOWERSIDE-SECONDRING-LEFT']])
    if L>2*Rf:
        R1 = (1+0.5*0.25)*Rf
        R2 = (1.25+0.5*0.25)*Rf
    else:
        R1 = Rf+0.5*0.25*(L-Rf)
        R2 = Rf+1.5*0.25*(L-Rf)
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(R1,0.0,0.0),radius=0.001*Rf), name='LOWERSIDE-THIRDRING-RIGHT')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(-R1,0.0,0.0),radius=0.001*Rf), name='LOWERSIDE-THIRDRING-LEFT')
    RVEpart.SetByBoolean(name='LOWERSIDE-THIRDRING', sets=[RVEpart.sets['LOWERSIDE-THIRDRING-RIGHT'],RVEpart.sets['LOWERSIDE-THIRDRING-LEFT']])
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(R2,0.0,0.0),radius=0.001*Rf), name='LOWERSIDE-FOURTHRING-RIGHT')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(-R2,0.0,0.0),radius=0.001*Rf), name='LOWERSIDE-FOURTHRING-LEFT')
    RVEpart.SetByBoolean(name='LOWERSIDE-FOURTHRING', sets=[RVEpart.sets['LOWERSIDE-FOURTHRING-RIGHT'],RVEpart.sets['LOWERSIDE-FOURTHRING-LEFT']])
    RVEpart.SetByBoolean(name='LOWERSIDE', sets=[RVEpart.sets['LOWERSIDE-FIRSTRING'],RVEpart.sets['LOWERSIDE-SECONDRING'],RVEpart.sets['LOWERSIDE-THIRDRING'],RVEpart.sets['LOWERSIDE-FOURTHRING']])
    
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(0.0,L,0.0),radius=0.001*Rf), name='UPPERSIDE')    
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(L,0.5*L,0.0),radius=0.001*Rf), name='RIGHTSIDE')    
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(-L,0.5*L,0.0),radius=0.001*Rf), name='LEFTSIDE')
    
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(0.5*Rf*np.cos((theta+deltatheta)*np.pi/180),0.5*Rf*np.sin((theta+deltatheta)*np.pi/180),0.0),radius=0.001*Rf), name='FIRSTCIRCLE')
    
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(0.75*Rf*np.cos(0.5*alpha*np.pi/180),0.75*Rf*np.sin(0.5*alpha*np.pi/180),0.0),radius=0.001*Rf), name='SECONDCIRCLE-LOWERCRACK')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(0.75*Rf*np.cos((alpha+0.5*deltapsi)*np.pi/180),0.75*Rf*np.sin((alpha+0.5*deltapsi)*np.pi/180),0.0),radius=0.001*Rf), name='SECONDCIRCLE-UPPERCRACK')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(0.75*Rf*np.cos((theta+deltatheta+0.5*deltapsi)*np.pi/180),0.75*Rf*np.sin((theta+deltatheta+0.5*deltapsi)*np.pi/180),0.0),radius=0.001*Rf), name='SECONDCIRCLE-FIRSTBOUNDED')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(0.75*Rf*np.cos((beta+0.5*deltaphi)*np.pi/180),0.75*Rf*np.sin((beta+0.5*deltaphi)*np.pi/180),0.0),radius=0.001*Rf), name='SECONDCIRCLE-SECONDBOUNDED')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(0.75*Rf*np.cos((gamma+0.5*(180.0-gamma))*np.pi/180),0.75*Rf*np.sin((gamma+0.5*(180.0-gamma))*np.pi/180),0.0),radius=0.001*Rf), name='SECONDCIRCLE-RESTBOUNDED')
    RVEpart.SetByBoolean(name='SECONDCIRCLE', sets=[RVEpart.sets['SECONDCIRCLE-LOWERCRACK'],RVEpart.sets['SECONDCIRCLE-UPPERCRACK'],RVEpart.sets['SECONDCIRCLE-FIRSTBOUNDED'],RVEpart.sets['SECONDCIRCLE-SECONDBOUNDED'],RVEpart.sets['SECONDCIRCLE-RESTBOUNDED']])
    
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(Rf*np.cos(0.5*alpha*np.pi/180),Rf*np.sin(0.5*alpha*np.pi/180),0.0),radius=0.001*Rf), name='THIRDCIRCLE-LOWERCRACK')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(Rf*np.cos((alpha+0.5*deltapsi)*np.pi/180),Rf*np.sin((alpha+0.5*deltapsi)*np.pi/180),0.0),radius=0.001*Rf), name='THIRDCIRCLE-UPPERCRACK')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(Rf*np.cos((theta+deltatheta+0.5*deltapsi)*np.pi/180),Rf*np.sin((theta+deltatheta+0.5*deltapsi)*np.pi/180),0.0),radius=0.001*Rf), name='THIRDCIRCLE-FIRSTBOUNDED')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(Rf*np.cos((beta+0.5*deltaphi)*np.pi/180),Rf*np.sin((beta+0.5*deltaphi)*np.pi/180),0.0),radius=0.001*Rf), name='THIRDCIRCLE-SECONDBOUNDED')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(Rf*np.cos((gamma+0.5*(180.0-gamma))*np.pi/180),Rf*np.sin((gamma+0.5*(180.0-gamma))*np.pi/180),0.0),radius=0.001*Rf), name='THIRDCIRCLE-RESTBOUNDED')
    RVEpart.SetByBoolean(name='THIRDCIRCLE', sets=[RVEpart.sets['THIRDCIRCLE-LOWERCRACK'],RVEpart.sets['THIRDCIRCLE-UPPERCRACK'],RVEpart.sets['THIRDCIRCLE-FIRSTBOUNDED'],RVEpart.sets['THIRDCIRCLE-SECONDBOUNDED'],RVEpart.sets['THIRDCIRCLE-RESTBOUNDED']])
    
    if L>2*Rf:
        R4 = 1.25*Rf
    else:
        R4 = Rf+0.25*(L-Rf)
        
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(R4*np.cos(0.5*alpha*np.pi/180),R4*np.sin(0.5*alpha*np.pi/180),0.0),radius=0.001*Rf), name='FOURTHCIRCLE-LOWERCRACK')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(R4*np.cos((alpha+0.5*deltapsi)*np.pi/180),R4*np.sin((alpha+0.5*deltapsi)*np.pi/180),0.0),radius=0.001*Rf), name='FOURTHCIRCLE-UPPERCRACK')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(R4*np.cos((theta+deltatheta+0.5*deltapsi)*np.pi/180),R4*np.sin((theta+deltatheta+0.5*deltapsi)*np.pi/180),0.0),radius=0.001*Rf), name='FOURTHCIRCLE-FIRSTBOUNDED')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(R4*np.cos((beta+0.5*deltaphi)*np.pi/180),R4*np.sin((beta+0.5*deltaphi)*np.pi/180),0.0),radius=0.001*Rf), name='FOURTHCIRCLE-SECONDBOUNDED')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(R4*np.cos((gamma+0.5*(180.0-gamma))*np.pi/180),R4*np.sin((gamma+0.5*(180.0-gamma))*np.pi/180),0.0),radius=0.001*Rf), name='FOURTHCIRCLE-RESTBOUNDED')
    RVEpart.SetByBoolean(name='FOURTHCIRCLE', sets=[RVEpart.sets['FOURTHCIRCLE-LOWERCRACK'],RVEpart.sets['FOURTHCIRCLE-UPPERCRACK'],RVEpart.sets['FOURTHCIRCLE-FIRSTBOUNDED'],RVEpart.sets['FOURTHCIRCLE-SECONDBOUNDED'],RVEpart.sets['FOURTHCIRCLE-RESTBOUNDED']])
    
    if L>2*Rf:
        RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(1.5*Rf*np.cos((theta+deltatheta)*np.pi/180),1.5*Rf*np.sin((theta+deltatheta)*np.pi/180),0.0),radius=0.001*Rf), name='FIFTHCIRCLE')
    else:
        RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=((Rf+0.5*(L-Rf))*np.cos((theta+deltatheta)*np.pi/180),(Rf+0.5*(L-Rf))*np.sin((theta+deltatheta)*np.pi/180),0.0),radius=0.001*Rf), name='FIFTHCIRCLE')
    
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(0.85*Rf*np.cos(alpha*np.pi/180),0.75*Rf*np.sin(alpha*np.pi/180),0.0),radius=0.001*Rf), name='TRANSVERSALCUT-FIRSTFIBER')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(1.05*Rf*np.cos(alpha*np.pi/180),1.05*Rf*np.sin(alpha*np.pi/180),0.0),radius=0.001*Rf), name='TRANSVERSALCUT-FIRSTMATRIX')
    
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(0.85*Rf*np.cos((theta+deltatheta)*np.pi/180),0.75*Rf*np.sin((theta+deltatheta)*np.pi/180),0.0),radius=0.001*Rf), name='TRANSVERSALCUT-SECONDFIBER')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(1.05*Rf*np.cos((theta+deltatheta)*np.pi/180),1.05*Rf*np.sin((theta+deltatheta)*np.pi/180),0.0),radius=0.001*Rf), name='TRANSVERSALCUT-SECONDMATRIX')
    
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(0.85*Rf*np.cos(beta*np.pi/180),0.75*Rf*np.sin(beta*np.pi/180),0.0),radius=0.001*Rf), name='TRANSVERSALCUT-THIRDFIBER')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(1.05*Rf*np.cos(beta*np.pi/180),1.05*Rf*np.sin(beta*np.pi/180),0.0),radius=0.001*Rf), name='TRANSVERSALCUT-THIRDMATRIX')
    
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(0.85*Rf*np.cos(gamma*np.pi/180),0.75*Rf*np.sin(gamma*np.pi/180),0.0),radius=0.001*Rf), name='TRANSVERSALCUT-FOURTHFIBER')
    RVEpart.Set(edges=RVEedges.getByBoundingSphere(center=(1.05*Rf*np.cos(gamma*np.pi/180),1.05*Rf*np.sin(gamma*np.pi/180),0.0),radius=0.001*Rf), name='TRANSVERSALCUT-FOURTHMATRIX')
    
    # sets of faces
    RVEpart.Set(faces=RVEfaces.findAt(coordinates=(0.0, 0.25*L, 0)), name='FIBER-CENTER')
    RVEpart.Set(faces=RVEfaces.findAt(coordinates=(0.0, 0.65*L, 0)), name='FIBER-INTERMEDIATEANNULUS')
    RVEpart.Set(faces=RVEfaces.findAt(coordinates=(0.85*Rf*np.cos(0.5*alpha*np.pi/180), 0.85*Rf*np.sin(0.5*alpha*np.pi/180), 0)), name='FIBER-EXTANNULUS-LOWERCRACK')
    RVEpart.Set(faces=RVEfaces.findAt(coordinates=(0.85*Rf*np.cos((alpha+0.5*deltapsi)*np.pi/180), 0.85*Rf*np.sin((alpha+0.5*deltapsi)*np.pi/180), 0)), name='FIBER-EXTANNULUS-UPPERCRACK')
    RVEpart.Set(faces=RVEfaces.findAt(coordinates=(0.85*Rf*np.cos((theta+deltatheta+0.5*deltapsi)*np.pi/180), 0.85*Rf*np.sin((theta+deltatheta+0.5*deltapsi)*np.pi/180), 0)), name='FIBER-EXTANNULUS-FIRSTBOUNDED')
    RVEpart.Set(faces=RVEfaces.findAt(coordinates=(0.85*Rf*np.cos((beta+0.5*deltaphi)*np.pi/180), 0.85*Rf*np.sin((beta+0.5*deltaphi)*np.pi/180), 0)), name='FIBER-EXTANNULUS-SECONDBOUNDED')
    RVEpart.Set(faces=RVEfaces.findAt(coordinates=(0.85*Rf*np.cos((gamma+0.5*(180-gamma))*np.pi/180), 0.85*Rf*np.sin((gamma+0.5*(180-gamma))*np.pi/180), 0)), name='FIBER-EXTANNULUS-RESTBOUNDED')
    RVEpart.SetByBoolean(name='FIBER-EXTANNULUS', sets=[RVEpart.sets['FIBER-EXTANNULUS-LOWERCRACK'],RVEpart.sets['FIBER-EXTANNULUS-UPPERCRACK'],RVEpart.sets['FIBER-EXTANNULUS-FIRSTBOUNDED'],RVEpart.sets['FIBER-EXTANNULUS-SECONDBOUNDED'],RVEpart.sets['FIBER-EXTANNULUS-RESTBOUNDED']])
    RVEpart.SetByBoolean(name='FIBER', sets=[RVEpart.sets['FIBER-CENTER'],RVEpart.sets['FIBER-INTERMEDIATEANNULUS'],RVEpart.sets['FIBER-EXTANNULUS']])
    
    if L>2*Rf:
        R1 = (1+0.5*0.25)*Rf
        R2 = (1.25+0.5*0.25)*Rf
    else:
        R1 = Rf+0.5*0.25*(L-Rf)
        R2 = Rf+1.5*0.25*(L-Rf)
        
    RVEpart.Set(faces=RVEfaces.findAt(coordinates=(R1*np.cos(0.5*alpha*np.pi/180), R1*np.sin(0.5*alpha*np.pi/180), 0)), name='MATRIX-INTANNULUS-LOWERCRACK')
    RVEpart.Set(faces=RVEfaces.findAt(coordinates=(R1*np.cos((alpha+0.5*deltapsi)*np.pi/180), R1*np.sin((alpha+0.5*deltapsi)*np.pi/180), 0)), name='MATRIX-INTANNULUS-UPPERCRACK')
    RVEpart.Set(faces=RVEfaces.findAt(coordinates=(R1*np.cos((theta+deltatheta+0.5*deltapsi)*np.pi/180), R1*np.sin((theta+deltatheta+0.5*deltapsi)*np.pi/180), 0)), name='MATRIX-INTANNULUS-FIRSTBOUNDED')
    RVEpart.Set(faces=RVEfaces.findAt(coordinates=(R1*np.cos((beta+0.5*deltaphi)*np.pi/180), R1*np.sin((beta+0.5*deltaphi)*np.pi/180), 0)), name='MATRIX-INTANNULUS-SECONDBOUNDED')
    RVEpart.Set(faces=RVEfaces.findAt(coordinates=(R1*np.cos((gamma+0.5*(180-gamma))*np.pi/180), R1*np.sin((gamma+0.5*(180-gamma))*np.pi/180), 0)), name='MATRIX-INTANNULUS-RESTBOUNDED')
    RVEpart.SetByBoolean(name='MATRIX-INTANNULUS', sets=[RVEpart.sets['MATRIX-INTANNULUS-LOWERCRACK'],RVEpart.sets['MATRIX-INTANNULUS-UPPERCRACK'],RVEpart.sets['MATRIX-INTANNULUS-FIRSTBOUNDED'],RVEpart.sets['MATRIX-INTANNULUS-SECONDBOUNDED'],RVEpart.sets['MATRIX-INTANNULUS-RESTBOUNDED']])
    RVEpart.Set(faces=RVEfaces.findAt(coordinates=(0.0, R2, 0)), name='MATRIX-INTERMEDIATEANNULUS')
    RVEpart.Set(faces=RVEfaces.findAt(coordinates=(0.0, Rf+0.5*(L-Rf), 0)), name='MATRIX-BODY')
    RVEpart.SetByBoolean(name='MATRIX', sets=[RVEpart.sets['MATRIX-BODY'],RVEpart.sets['MATRIX-INTERMEDIATEANNULUS'],RVEpart.sets['MATRIX-INTANNULUS']])
    
    RVEpart.SetByBoolean(name='RVE', sets=[RVEpart.sets['FIBER'],RVEpart.sets['MATRIX']])
                                    
    # sets of cells (none, i.e. 2D geometry)
    
    mdb.save()
    
    writeLineToLogFile(logfilepath,'a',2*logindent + '... done.',True)
    
#===============================================================================#
#                             Materials creation
#===============================================================================#    
    
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Creating materials ...',True)
    
    for material in parameters['materials']:
        mdb.models[modelname].Material(name=material['name'])
        try:
            values = material['elastic']['values']
            tuplelist = []
            valuelist = []
            for v,value in enumerate(values):
                if v>0 and v%8==0:
                    tuplelist.append(tuple(valuelist))
                    valuelist = []
                valuelist.append(value)
            tuplelist.append(tuple(valuelist))    
            mdb.models[modelname].materials[material['name']].Elastic(type=material['elastic']['type'],table=tuple(tuplelist))
        except Exception, error:
            sys.exc_clear()
        try:
            values = material['density']['values']
            tuplelist = []
            valuelist = []
            for v,value in enumerate(values):
                if v>0 and v%8==0:
                    tuplelist.append(tuple(valuelist))
                    valuelist = []
                valuelist.append(value)
            tuplelist.append(tuple(valuelist))    
            mdb.models[modelname].materials[material['name']].Density(table=tuple(tuplelist))
        except Exception, error:
            sys.exc_clear()
        try:
            values = material['thermalexpansion']['values']
            tuplelist = []
            valuelist = []
            for v,value in enumerate(values):
                if v>0 and v%8==0:
                    tuplelist.append(tuple(valuelist))
                    valuelist = []
                valuelist.append(value)
            tuplelist.append(tuple(valuelist))    
            mdb.models[modelname].materials[material['name']].Expansion(type=material['thermalexpansion']['type'],table=tuple(tuplelist))
        except Exception, error:
            sys.exc_clear()
        try:
            values = material['thermalconductivity']['values']
            tuplelist = []
            valuelist = []
            for v,value in enumerate(values):
                if v>0 and v%8==0:
                    tuplelist.append(tuple(valuelist))
                    valuelist = []
                valuelist.append(value)
            tuplelist.append(tuple(valuelist))    
            mdb.models[modelname].materials[material['name']].Conductivity(type=material['thermalconductivity']['type'],table=tuple(tuplelist))
        except Exception, error:
            sys.exc_clear()

    mdb.save()

    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)

#===============================================================================#
#                             Sections creation
#===============================================================================#
    
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Creating sections ...',True)
    
    for section in parameters['sections']:
        if 'HomogeneousSolidSection' in section['type'] or 'Homogeneous Solid Section' in section['type'] or 'somogeneoussolidsection' in section['type'] or 'homogeneous solid section' in section['type'] or 'Homogeneous solid section' in section['type']:
        mdb.models[modelname].HomogeneousSolidSection(name=section['name'], 
            material=section['material'], thickness=section['thickness'])
    
    mdb.save()
    
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    
#===============================================================================#
#                             Sections assignment
#===============================================================================# 

    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Making section assignments ...',True)
     
    for sectionRegion in parameters['sectionRegions']:
        RVEpart.SectionAssignment(region=RVEpart.sets[sectionRegion['set']], sectionName=sectionRegion['name'], offset=sectionRegion['offsetValue'],offsetType=sectionRegion['offsetType'], offsetField=sectionRegion['offsetField'],thicknessAssignment=sectionRegion['thicknessAssignment'])
    
    # p.SectionAssignment(region=region, sectionName='MatrixSection', offset=0.0, 
    #     offsetType=MIDDLE_SURFACE, offsetField='', 
    #     thicknessAssignment=FROM_SECTION)
        
    mdb.save()
    
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    
#===============================================================================#
#                             Instance creation
#===============================================================================#

    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Creating instance ...',True)
    
    model.rootAssembly.DatumCsysByDefault(CARTESIAN)
    model.rootAssembly.Instance(name='RVE-assembly', part=RVEpart, dependent=OFF)
    
    mdb.save()
    
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    
#===============================================================================#
#                             Step creation
#===============================================================================#
    
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Creating step ...',True)
    
    model.StaticStep(name='Load-Step', previous='Initial', 
        minInc=parameters['step']['minimumIncrement'])

    mdb.save()
    
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)

#===============================================================================#
#                             Boundary conditions
#===============================================================================#
    
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Assigning boundary conditions ...',True)
    
    # SOUTH side: symmetry line
    
    model.YsymmBC(name='SymmetryBound', createStepName='Load-Step', 
        region=model.rootAssembly.instances['RVE-assembly'].sets['LOWERSIDE'], localCsys=None)
    
    # NORTH side
    
    # if 'periodic' in parameters['boundaryConditions']['north']['type']:
    #     
    # elif 'rigidbar' in parameters['boundaryConditions']['north']['type']:
    # 
    # elif 'homogeneousdisplacement' in parameters['boundaryConditions']['north']['type']:
    #
    # else free
    
    # EAST side
    
    # if 'periodic' in parameters['boundaryConditions']['north']['type']:
    #
    # else free
    
    # WEST side
    
    # if 'periodic' in parameters['boundaryConditions']['north']['type']:
    #
    # else free
    
    mdb.save()
    
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    
#===============================================================================#
#                                Applied load
#===============================================================================#    
    
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a',2*logindent + 'Assigning loads ...',True)
    
    for load in parameters['loads']:
        if 'appliedstrain' in load['type'] or 'appliedStrain' in load['type'] or 'Applied Strain' in load['type'] or 'applied strain' in load['type']:
            model.DisplacementBC(name=load['name'],createStepName='Load-Step',region=model.rootAssembly.instances['RVE-assembly'].sets[load['set']], u1=load['value'][0]*L, u2=load['value'][1]*L, ur3=load['value'][2]*L, amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='',localCsys=None)
        elif 'applieddisplacement' in load['type'] or 'appliedDisplacement' in load['type'] or 'Applied Displacement' in load['type'] or 'applied displacement' in load['type']:
            model.DisplacementBC(name=load['name'],createStepName='Load-Step',region=model.rootAssembly.instances['RVE-assembly'].sets[load['set']], u1=load['value'][0], u2=load['value'][1], ur3=load['value'][2], amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='',localCsys=None)
        # elif 'appliedstress' in load['type'] or 'appliedStress' in load['type'] or 'Applied Stress' in load['type'] or 'applied stress' in load['type']:
        # 
        # elif 'appliedforce' in load['type'] or 'appliedForce' in load['type'] or 'Applied Force' in load['type'] or 'applied Force' in load['type']:
    
    mdb.save()
    
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)

#===============================================================================#
#                                   Crack
#===============================================================================#
   
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Creating cracks ...',True)
    
    # assign seam
    model.rootAssembly.engineeringFeatures.assignSeam(regions=model.rootAssembly.instances['RVE-assembly'].sets['CRACK'])
        
    # contour integral
    xC = Rf*np.cos((theta+deltatheta)*np.pi/180)
    yC = Rf*np.sin((theta+deltatheta)*np.pi/180)
    xA = Rf*np.cos((theta+1.025*deltatheta)*np.pi/180)
    yA = -xC*(xA-xC)/yC + yC
    model.rootAssembly.engineeringFeatures.ContourIntegral(name='Debond',symmetric=OFF,crackFront=model.rootAssembly.instances['RVE-assembly'].sets['CRACK'],crackTip=model.rootAssembly.instances['RVE-assembly'].sets['CRACKTIP'],extensionDirectionMethod=Q_VECTORS, qVectors=(((xC,yC,0.0),(xA,yA,0.0)), ), midNodePosition=0.5, collapsedElementAtTip=NONE)
    
    mdb.save()
    
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)

#===============================================================================#
#                                   Mesh
#===============================================================================#
    
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Creating mesh ...',True)
    
    # assign mesh controls
    model.rootAssembly.setMeshControls(regions=model.rootAssembly.instances['RVE-assembly'].sets['FIBER-EXTANNULUS-LOWERCRACK'], elemShape=QUAD, technique=STRUCTURED)
    model.rootAssembly.setMeshControls(regions=model.rootAssembly.instances['RVE-assembly'].sets['FIBER-EXTANNULUS-UPPERCRACK'], elemShape=QUAD, technique=STRUCTURED)
    model.rootAssembly.setMeshControls(regions=model.rootAssembly.instances['RVE-assembly'].sets['FIBER-EXTANNULUS-FIRSTBOUNDED'], elemShape=QUAD, technique=STRUCTURED)
    model.rootAssembly.setMeshControls(regions=model.rootAssembly.instances['RVE-assembly'].sets['MATRIX-INTANNULUS-LOWERCRACK'], elemShape=QUAD, technique=STRUCTURED)
    model.rootAssembly.setMeshControls(regions=model.rootAssembly.instances['RVE-assembly'].sets['MATRIX-INTANNULUS-UPPERCRACK'], elemShape=QUAD, technique=STRUCTURED)
    model.rootAssembly.setMeshControls(regions=model.rootAssembly.instances['RVE-assembly'].sets['MATRIX-INTANNULUS-FIRSTBOUNDED'], elemShape=QUAD, technique=STRUCTURED)
    
    model.rootAssembly.setMeshControls(regions=model.rootAssembly.instances['RVE-assembly'].sets['FIBER-CENTER'], elemShape=QUAD_DOMINATED, technique=FREE)
    model.rootAssembly.setMeshControls(regions=model.rootAssembly.instances['RVE-assembly'].sets['FIBER-INTANNULUS'], elemShape=QUAD_DOMINATED, technique=FREE)
    model.rootAssembly.setMeshControls(regions=model.rootAssembly.instances['RVE-assembly'].sets['FIBER-EXTANNULUS-SECONDBOUNDED'], elemShape=QUAD, technique=STRUCTURED)
    model.rootAssembly.setMeshControls(regions=model.rootAssembly.instances['RVE-assembly'].sets['FIBER-EXTANNULUS-RESTBOUNDED'], elemShape=QUAD, technique=STRUCTURED)
    model.rootAssembly.setMeshControls(regions=model.rootAssembly.instances['RVE-assembly'].sets['MATRIX-INTANNULUS-SECONDBOUNDED'], elemShape=QUAD, technique=STRUCTURED)
    model.rootAssembly.setMeshControls(regions=model.rootAssembly.instances['RVE-assembly'].sets['MATRIX-INTANNULUS-RESTBOUNDED'], elemShape=QUAD, technique=STRUCTURED)
    model.rootAssembly.setMeshControls(regions=model.rootAssembly.instances['RVE-assembly'].sets['MATRIX-EXTANNULUS'], elemShape=QUAD_DOMINATED, technique=FREE)
    model.rootAssembly.setMeshControls(regions=model.rootAssembly.instances['RVE-assembly'].sets['MATRIX-BODY'], elemShape=QUAD_DOMINATED, technique=FREE)
    
    # assign seeds
    nTangential = np.floor(deltapsi/delta) 
    nRadialFiber = np.floor(0.25/delta)
    if L>2*Rf:
        nRadialMatrix = np.floor(0.25/delta)
    else:
        nRadialMatrix = np.floor(0.25*(L-Rf)/delta)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['SECONDCIRCLE-UPPERCRACK'], number=nTangential, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['SECONDCIRCLE-FIRSTBOUNDED'], number=nTangential, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['THIRDCIRCLE-UPPERCRACK'], number=nTangential, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['THIRDCIRCLE-FIRSTBOUNDED'], number=nTangential, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['FOURTHCIRCLE-UPPERCRACK'], number=nTangential, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['FOURTHCIRCLE-FIRSTBOUNDED'], number=nTangential, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['TRANSVERSALCUT-FIRSTFIBER'], number=nRadialFiber, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['TRANSVERSALCUT-FIRSTMATRIX'], number=nRadialMatrix, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['TRANSVERSALCUT-SECONDFIBER'], number=nRadialFiber, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['TRANSVERSALCUT-SECONDMATRIX'], number=nRadialMatrix, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['TRANSVERSALCUT-THIRDFIBER'], number=nRadialFiber, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['TRANSVERSALCUT-THIRDMATRIX'], number=nRadialMatrix, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['LOWERSIDE-SECONDRING-RIGHT'], number=nRadialFiber, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['LOWERSIDE-THIRDRING-RIGHT'], number=nRadialMatrix, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['LOWERSIDE-CENTER'], number=6, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['FIRSTCIRCLE'], number=18, constraint=FINER)
    nTangential1 = np.floor(deltaphi/parameters['mesh']['size']['delta2'])
    nTangential2 = np.floor((180-(theta+deltatheta+deltapsi+deltaphi))/parameters['mesh']['size']['delta3'])
    nTangential3 = np.floor(alpha/parameters['mesh']['size']['delta1'])
    nRadialFiber1 = np.floor(0.25/parameters['mesh']['size']['delta3'])
    if L>2*Rf:
        nRadialMatrix1 = np.floor(0.25/parameters['mesh']['size']['delta3'])
    else:
        nRadialMatrix1 = np.floor(0.25*(L-Rf)/(Rf*parameters['mesh']['size']['delta3']))
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['SECONDCIRCLE-SECONDBOUNDED'], number=nTangential1, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['SECONDCIRCLE-RESTBOUNDED'], number=nTangential2, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['THIRDCIRCLE-SECONDBOUNDED'], number=nTangential1, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['THIRDCIRCLE-RESTBOUNDED'], number=nTangential2, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['FOURTHCIRCLE-SECONDBOUNDED'], number=nTangential1, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['FOURTHCIRCLE-RESTBOUNDED'], number=nTangential2, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['TRANSVERSALCUT-FOURTHFIBER'], number=nRadialFiber1, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['TRANSVERSALCUT-FOURTHMATRIX'], number=nRadialMatrix1, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['SECONDCIRCLE-LOWERCRACK'], number=nTangential3, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['THIRDCIRCLE-LOWERCRACK'], number=nTangential3, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['FOURTHCIRCLE-LOWERCRACK'], number=nTangential3, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['FIFTHCIRCLE'], number=90, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['RIGHTSIDE'], number=30, constraint=FINER)
    model.rootAssembly.seedEdgeByNumber(edges=model.rootAssembly.instances['RVE-assembly'].sets['LEFTSIDE'], number=30, constraint=FINER)
    
    # select element type
    if 'first' in parameters['mesh']['elements']['order']:
        elemType1 = mesh.ElemType(elemCode=CPE4, elemLibrary=STANDARD)
        elemType2 = mesh.ElemType(elemCode=CPE3, elemLibrary=STANDARD)
    elif 'second' in parameters['mesh']['elements']['order']:
        elemType1 = mesh.ElemType(elemCode=CPE8, elemLibrary=STANDARD)
        elemType2 = mesh.ElemType(elemCode=CPE6, elemLibrary=STANDARD)
    model.rootAssembly.setElementType(regions=model.rootAssembly.instances['RVE-assembly'].sets['RVE'], elemTypes=(elemType1, elemType2))
    
    # mesh part
    model.rootAssembly.generateMesh(regions=model.rootAssembly.instances['RVE-assembly'])
    
    mdb.save()
    
    # extract mesh statistics
    meshStats = model.rootAssembly.getMeshStats(regions=model.rootAssembly.instances['RVE-assembly'])
    
    modelData = {}
    modelData['numNodes'] =  meshStats.numNodes
    modelData['numQuads'] =  meshStats.numQuadElems
    modelData['numTris'] =  meshStats.numTriElems
    modelData['numEls'] =  meshStats.numQuadElems + meshStats.numTriElems
    
    mdb.save()
    
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    
#===============================================================================#
#                                   Output
#===============================================================================#
    
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Creating output requests ...',True)
    
    # field output
    
    # history output
    model.historyOutputRequests['H-Output-1'].setValues(contourIntegral='Debond',sectionPoints=DEFAULT,rebar=EXCLUDE,numberOfContours=parameters['Jintegral']['numberOfContours'])
    
    mdb.save()
    
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    
#===============================================================================#
#                                Job creation
#===============================================================================#
    
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Creating and submitting job ...',True)
    
    modelData['jobname'] = 'Job-Jintegral-' + modelname
    
    mdb.Job(name='Job-Jintegral-' + modelname, model=modelname, description='', type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=99, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=ON, modelPrint=ON, contactPrint=ON, historyPrint=ON, userSubroutine='',scratch='', multiprocessingMode=DEFAULT, numCpus=12, numDomains=12,numGPUs=0)
    
    mdb.save()
    
    #mdb.jobs['Job-' + modelname].submit(consistencyChecking=OFF)
    mdb.jobs['Job-' + modelname].writeInput(consistencyChecking=OFF)
    mdb.jobs['Job-' + modelname].waitForCompletion()
    
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Closing database ...',True)
    mdb.save()
    mdb.close()
    
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    
    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + 'Exiting function: createRVE(parameters,logfilepath,logindent)',True)
    
    return modelData()
    
def modifyRVEinputfile(parameters,mdbData,logfilepath,baselogindent,logindent):
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + 'In function: modifyRVE(parameters,mdbData)',True)
    skipLineToLogFile(logfilepath,'a',True)
    # odb name and path
    #odbname = mdbData['jobname'] + '.odb'
    #odbfullpath = join(parameters['wd'],odbname)
    # input file name and path
    inpname = mdbData['jobname'] + '.inp'
    inpfullpath = join(parameters['input']['wd'],inpname)
    # modified input file name
    modinpname = 'Job-VCCTandJintegral-' + parameters['input']['modelname']
    modinpfullpath = join(parameters['input']['wd'],modinpname)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Working directory: ' + parameters['wd'],True)
    #writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'ODB database name: ' + odbname,True)
    #writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'ODB database full path: ' + join(parameters['wd'],odbname),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Input file name: ' + inpname,True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Input file full path: ' + join(parameters['wd'],inpname),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Modified input file name: ' + modinpname,True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Modified input file full path: ' + join(parameters['wd'],modinpname),True)
    createABQinpfile(modinpname)
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Reading content of original input file ...',True)
    with open(inpfullpath,'r') as inp:
        inpfilelines = inp.readlines()
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Reading nodes and saving to dictionary ...',True)
    nodes = {}
    store = False
    for l,line in enumerate(inpfilelines):
        if store == True and '*' in inpfilelines[l+1]:
            nodes[int(line.replace('\n','').split(',')[0])] = [float(line.replace('\n','').split(',')[1]),float(line.replace('\n','').split(',')[1])]
            store == False
            break
        elif store == True:
            nodes[int(line.replace('\n','').split(',')[0])] = [float(line.replace('\n','').split(',')[1]),float(line.replace('\n','').split(',')[1])]
        elif ('*Node' in line or '*NODE' in line) and len(inpfilelines[l+1].replace('\n','').split(','))==3:
            store == True
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Reading quadrilateral elements and saving to dictionary ...',True)
    quads = {}
    store = False
    for l,line in enumerate(inpfilelines):
        if store == True and '*' in inpfilelines[l+1]:
            quadIndex = int(line.replace('\n','').split(',')[0])
            quads[quadIndex] = []
            for node in line.replace('\n','').split(',')[1:]:
                quads[quadIndex].append(int(node))
            store == False
            break
        elif store == True:
            quadIndex = int(line.replace('\n','').split(',')[0])
            quads[quadIndex] = []
            for node in line.replace('\n','').split(',')[1:]:
                quads[quadIndex].append(int(node))
        elif ('*Element, type=CPE8' in line or '*ELEMENT, type=CPE8' in line or '*Element, type=CPE4' in line or '*ELEMENT, type=CPE4' in line) and (len(inpfilelines[l+1].replace('\n','').split(','))==5 or len(inpfilelines[l+1].replace('\n','').split(','))==9):
            store == True
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Reading crack tip set and saving to variable ...',True)
    for l,line in enumerate(inpfilelines):
        if ('*Nset' in line or '*NSET' in line) and ('cracktip' in line or 'CRACKTIP' in line or 'Cracktip' in line):
            cracktipIndex = int(inpfilelines[l+1].replace('\n').split(',')[0])
            break
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Reading crack faces node set and saving to list ...',True)
    crackfacesNodeset = []
    store = False
    for l,line in enumerate(inpfilelines):
        if store == True and '*' in inpfilelines[l+1]:
            for index in line.replace('\n','').split(','):
                crackfacesNodeset.append(int(index))
            store == False
            break
        elif store == True:
            for index in line.replace('\n','').split(','):
                crackfacesNodeset.append(int(index))
        elif ('*Nset' in line or '*NSET' in line) and ('crack' in line or 'CRACK' in line or 'Crack' in line) and and ('cracktip' not in line and 'CRACKTIP' not in line and 'Cracktip' not in line)):
            store = True
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Reading crack faces element set and saving to list ...',True)
    crackfacesElementset = []
    store = False
    for l,line in enumerate(inpfilelines):
        if store == True and '*' in inpfilelines[l+1]:
            for index in line.replace('\n','').split(','):
                crackfacesElementset.append(int(index))
            store == False
            break
        elif store == True:
            for index in line.replace('\n','').split(','):
                crackfacesElementset.append(int(index))
        elif ('*Elset' in line or '*ELSET' in line) and ('crack' in line or 'CRACK' in line or 'Crack' in line) and and ('cracktip' not in line and 'CRACKTIP' not in line and 'Cracktip' not in line)):
            store = True
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Reading fiber node set and saving to list ...',True)
    fiberNodeset = []
    store = False
    for l,line in enumerate(inpfilelines):
        if store == True and '*' in inpfilelines[l+1]:
            for index in line.replace('\n','').split(','):
                fiberNodeset.append(int(index))
            store == False
            break
        elif store == True:
            for index in line.replace('\n','').split(','):
                fiberNodeset.append(int(index))
        elif ('*Nset' in line or '*NSET' in line) and ('fiber' in line or 'FIBER' in line or 'Fiber' in line) and and ('fiber-' not in line and 'FIBER-' not in line and 'Fiber-' not in line)):
            store = True
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Reading matrix node set and saving to list ...',True)
    matrixNodeset = []
    store = False
    for l,line in enumerate(inpfilelines):
        if store == True and '*' in inpfilelines[l+1]:
            for index in line.replace('\n','').split(','):
                matrixNodeset.append(int(index))
            store == False
            break
        elif store == True:
            for index in line.replace('\n','').split(','):
                matrixNodeset.append(int(index))
        elif ('*Nset' in line or '*NSET' in line) and ('matrix' in line or 'MATRIX' in line or 'Matrix' in line) and and ('matrix-' not in line and 'MATRIX-' not in line and 'Matrix-' not in line)):
            store = True
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Reading fiber element set and saving to list ...',True)
    fiberElementset = []
    store = False
    for l,line in enumerate(inpfilelines):
        if store == True and '*' in inpfilelines[l+1]:
            for index in line.replace('\n','').split(','):
                fiberElementset.append(int(index))
            store == False
            break
        elif store == True:
            for index in line.replace('\n','').split(','):
                fiberElementset.append(int(index))
        elif ('*Elset' in line or '*ELSET' in line) and ('fiber' in line or 'FIBER' in line or 'Fiber' in line) and and ('fiber-' not in line and 'FIBER-' not in line and 'Fiber-' not in line)):
            store = True
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Reading matrix element set and saving to list ...',True)
    matrixElementset = []
    store = False
    for l,line in enumerate(inpfilelines):
        if store == True and '*' in inpfilelines[l+1]:
            for index in line.replace('\n','').split(','):
                matrixElementset.append(int(index))
            store == False
            break
        elif store == True:
            for index in line.replace('\n','').split(','):
                matrixElementset.append(int(index))
        elif ('*Elset' in line or '*ELSET' in line) and ('matrix' in line or 'MATRIX' in line or 'Matrix' in line) and and ('matrix-' not in line and 'MATRIX-' not in line and 'Matrix-' not in line)):
            store = True
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Insert new coincident node(s) at the crack tip and create dummy node(s) ...',True)
    numNodes = mdbData['numNodes']
    matrixCracktipIndex = numNodes + 1000
    cracktipDummyIndex = numNodes + 1000 + 1
    nodes[matrixCracktipIndex] = [nodes[cracktipIndex][0],nodes[cracktipIndex][1]]
    nodes[cracktipDummyIndex] = [-5*parameters['Rf'],-10*parameters['Rf']]
    fiberElswithCracktip = []
    matrixElswithCracktip = []
    for element in fiberElementset:
        if cracktipIndex in quads[element]:
            fiberElswithCracktip.append(element)
            if len(fiberElswithCracktip) == 2:
                break
    for element in matrixElementset:
        if cracktipIndex in quads[element]:
            matrixElswithCracktip.append(element)
            if len(matrixElswithCracktip) == 2:
                break
    if 'second' in parameters['elements']['order']:
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Second order elements are used',True)
        matrixFirstBehindCracktipIndex = numNodes + 1000 + 2
        firstBehindCracktipDummyIndex = numNodes + 1000 + 3
        found = False
        for fiberEl in fiberElswithCracktip:
            if found:
                break
            fiberElnodes = quads[fiberEl]
            for matrixEl in matrixElswithCracktip:
                commonNodes = []
                matrixElnodes = quads[matrixEl]
                for node in fiberElnodes:
                    if node in matrixElnodes:
                        commonNodes.append(node)
                if len(commonNodes)==3:
                    found = True
                    break
        distances = []
        for node in commonNodes:
            if node != cracktipIndex:
                distances.append(np.sqrt((nodes[node][0]-nodes[cracktip][0])*(nodes[node][0]-nodes[cracktip][0])+(nodes[node][1]-nodes[cracktip][1])*(nodes[node][1]-nodes[cracktip][1])))
            else:
                distances.append(0.0)
        fiberFirstBehindCracktipIndex = commonNodes[np.argmax(distances)]
        nodes[matrixFirstBehindCracktipIndex] = [nodes[fiberFirstBehindCracktipIndex][0],nodes[fiberFirstBehindCracktipIndex][1]]
        nodes[firstBehindCracktipDummyIndex] = [5*parameters['Rf'],-10*parameters['Rf']]
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Identify nodes on crack faces for displacement measurements ...',True)
    nodesAroundCracktip = []
    for element in fiberElswithCracktip:
        for node in quads[element]:
            nodesAroundCracktip.append(node)
    nodesFiberDisplacementMeas = []
    for node in crackfacesNodeset:
        if node in nodesAroundCracktip:
            nodesFiberDisplacementMeas.append(node)
    distancesFiberDisplacementMeas = []
    for node in nodesFiberDisplacementMeas:
        distancesFiberDisplacementMeas.append(np.sqrt((nodes[node][0]-nodes[cracktipIndex][0])*(nodes[node][0]-nodes[cracktipIndex][0])+(nodes[node][1]-nodes[cracktipIndex][1])*(nodes[node][1]-nodes[cracktipIndex][1])))
    nodesAroundCracktip = []
    for element in matrixElswithCracktip:
        for node in quads[element]:
            nodesAroundCracktip.append(node)
    nodesMatrixDisplacementMeas = []
    for node in crackfacesNodeset:
        if node in nodesAroundCracktip:
            nodesMatrixDisplacementMeas.append(node)
    distancesMatrixDisplacementMeas = []
    for node in nodesMatrixDisplacementMeas:
        distancesFiberDisplacementMeas.append(np.sqrt((nodes[node][0]-nodes[cracktipIndex][0])*(nodes[node][0]-nodes[cracktipIndex][0])+(nodes[node][1]-nodes[cracktipIndex][1])*(nodes[node][1]-nodes[cracktipIndex][1])))
    sortedFiberDistanceIndeces = np.argsort(distancesFiberDisplacementMeas)
    sortedMatrixDistanceIndeces = np.argsort(distancesMatrixDisplacementMeas)
    if 'second' in parameters['elements']['order']:
        cracktipFiberDispMeasIndex = nodesFiberDisplacementMeas[sortedFiberDistanceIndeces[-1]]
        firstBehindCracktipFiberDispMeasIndex = nodesFiberDisplacementMeas[sortedFiberDistanceIndeces[-2]]
        cracktipMatrixDispMeasIndex = nodesMatrixDisplacementMeas[sortedMatrixDistanceIndeces[-1]]
        firstBehindCracktipMatrixDispMeasIndex = nodesMatrixDisplacementMeas[sortedMatrixDistanceIndeces[-2]]
    else:
        cracktipFiberDispMeasIndex = nodesFiberDisplacementMeas[sortedFiberDistanceIndeces[-1]]
        cracktipMatrixDispMeasIndex = nodesMatrixDisplacementMeas[sortedMatrixDistanceIndeces[-1]]
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Assign new crack tip nodes to matrix elements at crack tip ...',True)
    found = False
    for fIndex,fiberEl in fiberElswithCracktip:
        if found:
            break
        fiberElnodes = quads[fiberEl]
        for mIndex,matrixEl in matrixElswithCracktip:
            commonNodes = []
            matrixElnodes = quads[matrixEl]
            for node in fiberElnodes:
                if node in matrixElnodes:
                    commonNodes.append(node)
            if len(commonNodes)>1:
                firstboundedFiberEl = fiberEl
                firstboundedMatrixEl = matrixEl
                firstdebondedFiberEl = fiberElswithCracktip[1-fIndex]
                firstdebondedMatrixEl = matrixElswithCracktip[1-mIndex]
                found = True
                break
    for n,node in enumerate(quads[firstboundedMatrixEl]):
        if node == crackTipIndex:
            quads[firstboundedMatrixEl][n] = matrixCracktipIndex
    if 'second' in parameters['elements']['order']:
        for n,node in enumerate(quads[firstboundedMatrixEl]):
            if node == fiberFirstBehindCracktipIndex:
                quads[firstboundedMatrixEl][n] = matrixFirstBehindCracktipIndex
    for n,node in enumerate(quads[firstdebondedMatrixEl]):
        if node == crackTipIndex:
            quads[firstdebondedMatrixEl][n] = matrixCracktipIndex
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Find set of debonded elements on fiber and on matrix  ...',True)
    crackfaceFiberElementset = []
    crackfaceMatrixElementset = []
    for element in crackfacesElementset:
        if element in fiberElementset:
            crackfaceFiberElementset.append(element)
        else:
            crackfaceMatrixElementset.append(element)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Find set of debonded nodes on fiber and on matrix  ...',True)
    crackfaceFiberNodeset = []
    crackfaceMatrixNodeset = []
    for node in crackfacesNodeset:
        if node in fiberNodeset:
            crackfaceFiberNodeset.append(node)
        else:
            crackfaceMatrixNodeset.append(node)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Writing new input file  ...',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Identify node section  ...',True)
    started = False
    for l,line in enumerate(inpfilelines):
        if started and '*' in line:
            nodeSecStop = l-1
            break
        elif started
            continue
        elif ('*Node' in line or '*NODE' in line) and len(inpfilelines[l+1].replace('\n').split(',')) == 3:
            nodeSecStart = l
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Identify quadrilateral element section  ...',True)
    started = False
    for l,line in enumerate(inpfilelines):
        if started and '*' in line:
            elementSecStop = l-1
            break
        elif started
            continue
        elif ('*Element, type=CPE8' in line or '*ELEMENT, type=CPE8' in line or '*Element, type=CPE4' in line or '*ELEMENT, type=CPE4' in line) and (len(inpfilelines[l+1].replace('\n','').split(','))==5 or len(inpfilelines[l+1].replace('\n','').split(','))==9):
            elementSecStart = l
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Identify end of assembly section  ...',True)
    for l,line in enumerate(inpfilelines):
        if '*End Assembly' in line or '*END ASSEMBLY' in line:
            endAssembly = l
            break 
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Identify start of boundary conditions section  ...',True)
    for l,line in enumerate(inpfilelines):
        if '** BOUNDARY CONDITIONS' in line or '** Boundary Conditions' in line:
            startBC = l
            break 
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Write from original input file  ...',True)
    with open(modinpfullpath,'a') as inp:
        for line in inpfilelines[:nodeSecStart]:
            inp.write(line)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Write nodes ...',True)
    with open(modinpfullpath,'a') as inp:
        inp.write('*NODE' + '\n')
        for node in nodes.keys():
            line = str(node)
            for coord in nodes[node]:
                line += ', ' + coord
            inp.write(line + '\n')
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Write from original input file  ...',True)
    with open(modinpfullpath,'a') as inp:
        for line in inpfilelines[nodeSecStop+1:elementSecStart]:
            inp.write(line)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Write quadrilateral elements ...',True)
    with open(modinpfullpath,'a') as inp:
        inp.write(inpfilelines[elementSecStart])
        for quad in quads.keys():
            line = str(quad)
            for node in quads[quad]:
                line += ', ' + node
            inp.write(line + '\n')
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Write from original input file  ...',True)
    with open(modinpfullpath,'a') as inp:
        for line in inpfilelines[elementSecStop+1:endAssembly]:
            inp.write(line)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Write crack faces node and element sets ...',True)
    with open(modinpfullpath,'a') as inp:
        inp.write('*NSET, NSET=FIBER-CRACKFACE-NODES, INSTANCE=RVEassembly' + '\n')
        line = ''
        for n,node in enumerate(crackfaceFiberNodeset):
            if n>0 and n%8==0.0:
                line += ' ' + str(node)
                inp.write(line + '\n')
                line = ''
            else:
                line += ' ' + str(node) + ','
        if len(line)>0:
            inp.write(line + '\n')
        inp.write('*NSET, NSET=MATRIX-CRACKFACE-NODES, INSTANCE=RVEassembly' + '\n')
        line = ''
        for n,node in enumerate(crackfaceMatrixNodeset):
            if n>0 and n%8==0.0:
                line += ' ' + str(node)
                inp.write(line + '\n')
                line = ''
            else:
                line += ' ' + str(node) + ','
        if len(line)>0:
            inp.write(line + '\n')
        inp.write('*ELSET, ELSET=FIBER-CRACKFACE-ELEMENTS, INSTANCE=RVEassembly' + '\n')
        line = ''
        for n,element in enumerate(crackfaceFiberElementset):
            if n>0 and n%8==0.0:
                line += ' ' + str(element)
                inp.write(line + '\n')
                line = ''
            else:
                line += ' ' + str(element) + ','
        if len(line)>0:
            inp.write(line + '\n')
        inp.write('*ELSET, ELSET=MATRIX-CRACKFACE-ELEMENTS, INSTANCE=RVEassembly' + '\n')
        line = ''
        for n,element in enumerate(crackfaceMatrixElementset):
            if n>0 and n%8==0.0:
                line += ' ' + str(element)
                inp.write(line + '\n')
                line = ''
            else:
                line += ' ' + str(element) + ','
        if len(line)>0:
            inp.write(line + '\n')
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Write VCCT node sets ...',True)
    with open(modinpfullpath,'a') as inp:
        inp.write('*NSET, NSET=FIBER-CRACKTIP, INSTANCE=RVEassembly' + '\n')
        inp.write(' ' + str(cracktipIndex) + '\n')
        inp.write('*NSET, NSET=MATRIX-CRACKTIP, INSTANCE=RVEassembly' + '\n')
        inp.write(' ' + str(matrixCracktipIndex) + '\n')
        inp.write('*NSET, NSET=FIBER-CRACKTIP-DISPMEAS, INSTANCE=RVEassembly' + '\n')
        inp.write(' ' + str(cracktipFiberDispMeasIndex) + '\n')
        inp.write('*NSET, NSET=MATRIX-CRACKTIP-DISPMEAS, INSTANCE=RVEassembly' + '\n')
        inp.write(' ' + str(cracktipMatrixDispMeasIndex) + '\n')
        if 'second' in parameters['elements']['order']:
            inp.write('*NSET, NSET=FIBER-NODE-FIRSTBOUNDED, INSTANCE=RVEassembly' + '\n')
            inp.write(' ' + str(fiberFirstBehindCracktipIndex) + '\n')
            inp.write('*NSET, NSET=MATRIX-NODE-FIRSTBOUNDED, INSTANCE=RVEassembly' + '\n')
            inp.write(' ' + str(matrixFirstBehindCracktipIndex) + '\n')
            inp.write('*NSET, NSET=FIBER-FIRSTBOUNDED-DISPMEAS, INSTANCE=RVEassembly' + '\n')
            inp.write(' ' + str(firstBehindCracktipFiberDispMeasIndex) + '\n')
            inp.write('*NSET, NSET=MATRIX-FIRSTBOUNDED-DISPMEAS, INSTANCE=RVEassembly' + '\n')
            inp.write(' ' + str(firstBehindCracktipMatrixDispMeasIndex) + '\n')
        inp.write('*NSET, NSET=CRACKTIP-DUMMY-NODE, INSTANCE=RVEassembly' + '\n')
        inp.write(' ' + str(cracktipDummyIndex) + '\n')
        if 'second' in parameters['elements']['order']:
            inp.write('*NSET, NSET=FIRSTBOUNDED-DUMMY-NODE, INSTANCE=RVEassembly' + '\n')
            inp.write(' ' + str(FirstBehindCracktipDummyIndex) + '\n')
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Write equation definitions ...',True)
    with open(modinpfullpath,'a') as inp:
        inp.write('*EQUATION' + '\n')
        inp.write(' 3' + '\n')
        inp.write(' FIBER-CRACKTIP,1,1,MATRIX-CRACKTIP,1,-1,CRACKTIP-DUMMY-NODE,1,-1' + '\n')
        inp.write(' 3' + '\n')
        inp.write(' FIBER-CRACKTIP,2,1,MATRIX-CRACKTIP,2,-1,CRACKTIP-DUMMY-NODE,2,-1' + '\n')
        if 'second' in parameters['elements']['order']:
            inp.write(' 3' + '\n')
            inp.write(' FIBER-NODE-FIRSTBOUNDED,1,1,MATRIX-NODE-FIRSTBOUNDED,1,-1,FIRSTBOUNDED-DUMMY-NODE,1,-1' + '\n')
            inp.write(' 3' + '\n')
            inp.write(' FIBER-NODE-FIRSTBOUNDED,2,1,MATRIX-NODE-FIRSTBOUNDED,2,-1,FIRSTBOUNDED-DUMMY-NODE,2,-1' + '\n')
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Write surface definitions ...',True)
    with open(modinpfullpath,'a') as inp:
        inp.write('*SURFACE, NAME=FiberSurface, TYPE=ELEMENT' + '\n')
        inp.write(' crackfaceFiberElementset' + '\n')
        inp.write('*SURFACE, NAME=MatrixSurface, TYPE=ELEMENT' + '\n')
        inp.write(' crackfaceMatrixElementset' + '\n')
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Write end assembly ...',True)
    with open(modinpfullpath,'a') as inp:
        inp.write('*End Assembly' + '\n')
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Write contact interaction ...',True)
    with open(modinpfullpath,'a') as inp:
        inp.write('*CONTACT PAIR, INTERACTION=CrackFacesContact, SMALL SLIDING' + '\n')
        inp.write(' MatrixSurface, FiberSurface' + '\n')
        inp.write('*SURFACE INTERACTION, NAME=CrackFacesContact' + '\n')
        inp.write(' 1.0' + '\n')
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Write from original input file  ...',True)
    with open(modinpfullpath,'a') as inp:
        for line in inpfilelines[endAssembly+1:startBC]:
            inp.write(line)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Write boundary conditions for VCCT  ...',True)
    with open(modinpfullpath,'a') as inp:
        inp.write('BOUNDARY CONDITIONS' + '\n')
        inp.write('**' + '\n')
        inp.write('*BOUNDARY, OP=MOD' + '\n')
        inp.write(' CRACKTIP-DUMMY-NODE, ENCASTRE' + '\n')
        inp.write(' FIRSTBOUNDED-DUMMY-NODE, ENCASTRE' + '\n')
        inp.write('**' + '\n')
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Write from original input file  ...',True)
    with open(modinpfullpath,'a') as inp:
        for line in inpfilelines[startBC+1:]:
            inp.write(line)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    writeLineToLogFile(logfilefullpath,'a','modifyRVEinputfile(parameters,mdbData,baselogindent,logindent)',True)
    return modinpname

def runRVEsimulation(wd,inpfile,logfilepath,baselogindent,logindent):
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + 'In function: runRVEsimulation(wd,inpfile)',True)
    
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Creating and submitting job ...',True)
    
    mdb.JobFromInputFile(name=inpfile.split('.')[0],inputFileName=inpfile,type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=99, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=ON, modelPrint=ON, contactPrint=ON, historyPrint=ON, userSubroutine='',scratch='', multiprocessingMode=DEFAULT, numCpus=12, numDomains=12,numGPUs=0)
    
    mdb.jobs[inpfile.split('.')[0]].submit(consistencyChecking=OFF)
    
    mdb.jobs[inpfile.split('.')[0]].waitForCompletion()
    
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    writeLineToLogFile(logfilefullpath,'a',baselogindent + logindent + 'Exiting function: runRVEsimulation(wd,inpfile,baselogindent,logindent)',True)

def analyzeRVEresults(odbname,parameters,logfilepath,baselogindent,logindent):
    
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + 'In function: analyzeRVEresults(wd,odbname)',True)
    
    wd = parameters['input']['wd']
    
    #=======================================================================
    # BEGIN - extract performances
    #=======================================================================
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Extract performances...',True)
    try:
        performances = getPerfs(wd,getPerfs(wd,[odbname.split('.')[0]]))
    except Exception,e:
        writeErrorToLogFile(logfilepath,'a',Exception,e,True)
        sys.exc_clear()
    appendCSVfile(parameters['output']['global']['directory'],parameters['output']['global']['filenames']['performances'],performances[1])
    writeLineToLogFile(logfilepath,'a','... done.',True)
    #=======================================================================
    # END - extract performances
    #=======================================================================
    
    #=======================================================================
    # BEGIN - extract J-integral results
    #=======================================================================
    writeLineToLogFile(logfilepathpath,'a',baselogindent + 2*logindent + 'Extracting J-integral results ...',True)
    try:
        Jintegrals = getJintegrals(wd,odbname.split('.')[0],parameters['Jintegral']['numberOfContours'])
    except Exception,e:
        writeErrorToLogFile(logfilepath,'a',Exception,e,True)
        sys.exc_clear()
    JintegralsWithDistance = []
    for v,value in enumerate(Jintegrals):
        JintegralsWithDistance.append([(v+1)*parameters['Rf']*parameters['delta']*np.pi/180.0,value])
    createCSVfile(parameters['output']['local']['directory'],parameters['output']['local']['filenames']['Jintegral'],'CONTOUR, AVERAGE DISTANCE, GTOT')
    appendCSVfile(parameters['output']['local']['directory'],parameters['output']['local']['filenames']['Jintegral'],JintegralsWithDistance)
    writeLineToLogFile(logfilepathpath,'a',baselogindent + 2*logindent + '... done.',True)
    #=======================================================================
    # END - extract J-integral results
    #=======================================================================
    
    #=======================================================================
    # BEGIN - open ODB
    #=======================================================================
    writeLineToLogFile(logfilepathpath,'a',baselogindent + 2*logindent + 'Opening ODB database + ' + odbname + ' in directory ' + wd + ' ...',True)
    if '.odb' not in odbname:
        odbname += '.odb'
    odbfullpath = join(wd,odbname)
    odb = openOdb(path=odbfullpath)
    writeLineToLogFile(logfilepathpath,'a',baselogindent + 2*logindent + '... done.',True)
    #=======================================================================
    # END - open ODB
    #=======================================================================
    
    #=======================================================================
    # BEGIN - extract node sets
    #=======================================================================
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Extracting node sets ...',True)
    
    rightSide = getSingleNodeSet(odb,'RVE','RIGHTSIDE')
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '-- RIGHTSIDE',True)
    
    fiberCrackfaceNodes = getSingleNodeSet(odb,'RVE','FIBER-CRACKFACE-NODES')
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '-- FIBER-CRACKFACE-NODES',True)
    
    matrixCrackfaceNodes = getSingleNodeSet(odb,'RVE','MATRIX-CRACKFACE-NODES')
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '-- MATRIX-CRACKFACE-NODES',True)
    
    fiberCracktip = getSingleNodeSet(odb,'RVE','FIBER-CRACKTIP')
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '-- FIBER-CRACKTIP',True)
    
    matrixCracktip = getSingleNodeSet(odb,'RVE','MATRIX-CRACKTIP')
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '-- MATRIX-CRACKTIP',True)
    
    cracktipDummyNode = getSingleNodeSet(odb,'RVE','CRACKTIP-DUMMY-NODE')
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '-- CRACKTIP-DUMMY-NODE',True)
    
    fiberCracktipDispMeas = getSingleNodeSet(odb,'RVE','FIBER-CRACKTIP-DISPMEAS')
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '-- FIBER-CRACKTIP-DISPMEAS',True)
    
    matrixCracktipDispMeas = getSingleNodeSet(odb,'RVE','MATRIX-CRACKTIP-DISPMEAS')
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '-- MATRIX-CRACKTIP-DISPMEAS',True)
    
    if 'second' in parameters['elements']['order']:
        fiberFirstbounded = getSingleNodeSet(odb,'RVE','FIBER-NODE-FIRSTBOUNDED')
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '-- FIBER-NODE-FIRSTBOUNDED',True)
        
        matrixFirstbounded = getSingleNodeSet(odb,'RVE','MATRIX-NODE-FIRSTBOUNDED')
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '-- MATRIX-NODE-FIRSTBOUNDED',True)
        
        firstboundedDummyNode = getSingleNodeSet(odb,'RVE','FIRSTBOUNDED-DUMMY-NODE')
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '-- FIRSTBOUNDED-DUMMY-NODE',True)
        
        fiberFirstboundedDispMeas = getSingleNodeSet(odb,'RVE','FIBER-FIRSTBOUNDED-DISPMEAS')
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '-- FIBER-FIRSTBOUNDED-DISPMEAS',True)
        
        matrixFirstboundedDispMeas = getSingleNodeSet(odb,'RVE','MATRIX-FIRSTBOUNDED-DISPMEAS')
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '-- MATRIX-FIRSTBOUNDED-DISPMEAS',True)
        
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    #=======================================================================
    # END - extract node sets
    #=======================================================================
    
    #=======================================================================
    # BEGIN - extract stresses at the boundary
    #=======================================================================
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Extracting stresses at the boundary ...',True)
    
    rightsideStress = getFieldOutput(odb,-1,-1,'S',rightSide,3)
    
    rightsideDefcoords = getFieldOutput(odb,-1,-1,'COORD',rightSide)
    
    rightsideStressdata = []
    rightsideUndefcoords = getFieldOutput(odb,-1,0,'COORD',rightSide)
    for value in rightsideUndefcoords:
        node = odb.rootAssembly.instances['RVEassembly'].getNodeFromLabel(value.label)
        stress = getFieldOutput(odb,-1,-1,'S',node,3)
        defcoords = getFieldOutput(odb,-1,-1,'COORD',node)
        rightsideStressdata.append([value.data[0],value.data[1],defcoords.value[0].data[0],defcoords.value[0].data[1],stress.value[0].data[0],stress.value[0].data[1],stress.value[0].data[2],stress.value[0].data[3]])
    
    maxSigmaxx = rightsideStressdata[0][4]
    minSigmaxx = rightsideStressdata[0][4]
    meanSigmaxx = 0.0
    for stress in rightsideStressdata:
        meanSigmaxx += stress[4]
        if stress[4]>maxSigmaxx:
            maxSigmaxx = stress[4]
        elif stress[4]<minSigmaxx:
            minSigmaxx = stress[4]
    meanSigmaxx /= len(rightsideStressdata)
    
    createCSVfile(parameters['output']['local']['directory'],parameters['output']['local']['filenames']['stressesatboundary'],'x0, y0, x, y, sigma_xx, sigma_zz, sigma_yy, tau_xz')
    appendCSVfile(parameters['output']['local']['directory'],parameters['output']['local']['filenames']['stressesatboundary'],rightsideStressdata)
    
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    #=======================================================================
    # END - extract stresses at the boundary
    #=======================================================================
    
    #=======================================================================
    # BEGIN - compute G0
    #=======================================================================
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Extract performances...',True)
    G0 = np.pi*parameters['geometry']['Rf']*meanSigmaxx*meanSigmaxx*(1+(3.0-4.0*parameters['materials']['nu-G0']))/(8.0*parameters['materials']['G-G0'])
    writeLineToLogFile(logfilepath,'a','... done.',True)
    #=======================================================================
    # END - compute G0
    #=======================================================================
    
    #=======================================================================
    # BEGIN - compute reference frame transformation
    #=======================================================================
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Compute reference frame transformation ...',True)
    
    undefCracktipCoords = getFieldOutput(odb,-1,0,'COORD',fiberCracktip)
    phi = np.arctan2(undefCracktipCoords.data[1],undefCracktipCoords.data[0])
    
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    #=======================================================================
    # END - compute reference frame transformation
    #=======================================================================
    
    #=======================================================================
    # BEGIN - compute contact zone
    #=======================================================================
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Compute contact zone ...',True)
    
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Extract displacements ...',True)
    
    fiberCrackfaceDisps = getFieldOutput(odb,-1,-1,'U',fiberCrackfaceNodes)
    matrixCrackfaceDisps = getFieldOutput(odb,-1,-1,'U',matrixCrackfaceNodes)
    
    fiberAngles = []
    matrixAngles = []
    fiberDisps = []
    matrixDisps = []
    
    for value in fiberCrackfaceDisps.values:
        node = odb.rootAssembly.instances['RVEassembly'].getNodeFromLabel(value.label)
        undefCoords = getFieldOutput(odb,-1,0,'COORD',node)
        beta = np.arctan2(undefCoords.value[0].data[1],undefCoords.value[0].data[0])
        fiberAngles.append(beta)
        fiberDisps.append([np.cos(beta)*value.data[0]+np.sin(beta)*value.data[1],-np.sin(beta)*value.data[0]+np.cos(beta)*value.data[1]])
    for value in matrixCrackfaceDisps.values:
        node = odb.rootAssembly.instances['RVEassembly'].getNodeFromLabel(value.label)
        undefCoords = getFieldOutput(odb,-1,0,'COORD',node)
        beta = np.arctan2(undefCoords.value[0].data[1],undefCoords.value[0].data[0])
        matrixAngles.append(beta)
        matrixDisps.append([np.cos(beta)*value.data[0]+np.sin(beta)*value.data[1],-np.sin(beta)*value.data[0]+np.cos(beta)*value.data[1]])
    
    fiberDisps = np.array(fiberDisps)[np.argsort(fiberAngles)].tolist()
    matrixDisps = np.array(matrixDisps)[np.argsort(matrixAngles)].tolist()
    
    crackDisps = []
    uR = []
    uTheta = []
    
    for s,dispset in enumerate(fiberDisps):
        crackDisps.append([matrixDisps[s][0]-dispset[0],matrixDisps[s][1]-dispset[1]])
        uR.append(matrixDisps[s][0]-dispset[0])
        uTheta.append(matrixDisps[s][1]-dispset[1])
        
    phiCZ = 0.0
    for s,dispset in enumerate(crackDisps):
        if dispset[0]<1e-10:
            phiCZ = phi - fiberAngles[s]
    
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)
    
    createCSVfile(parameters['output']['local']['directory'],parameters['output']['local']['filenames']['crackdisplacements'],'beta, uR_fiber, uTheta_fiber, uR_matrix, uTheta_matrix, uR, uTheta')
    for s,dispset, in enumerate(crackDisps):
        appendCSVfile(parameters['output']['local']['directory'],parameters['output']['local']['filenames']['crackdisplacements'],[fiberAngles[s],fiberDisps[s][0],fiberDisps[s][1],matrixDisps[s][0],matrixDisps[s][1],crackDisps[s][0],crackDisps[s][1]])
    
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    #=======================================================================
    # END - compute contact zone
    #=======================================================================
    
    #=======================================================================
    # BEGIN - compute VCCT
    #=======================================================================
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Compute VCCT ...',True)
    
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Extract forces and displacements ...',True)
    
    RFcracktip = getFieldOutput(odb,-1,-1,'RF',cracktipDummyNode)
    if 'second' in parameters['elements']['order']:
        RFfirstbounded = getFieldOutput(odb,-1,-1,'RF',firstboundedDummyNode)
    fiberCracktipDisplacement = getFieldOutput(odb,-1,-1,'U',fiberCracktipDispMeas)
    matrixCracktipDisplacement = getFieldOutput(odb,-1,-1,'U',matrixCracktipDispMeas)
    if 'second' in parameters['elements']['order']:
        fiberFirstboundedDisplacement = getFieldOutput(odb,-1,-1,'U',fiberFirstboundedDispMeas)
        matrixFirstboundedDisplacement = getFieldOutput(odb,-1,-1,'U',matrixFirstboundedDispMeas)
    
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)
    
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Rotate forces and displacements ...',True)
    
    xRFcracktip = RFcracktip.value[0].data[0]
    yRFcracktip = RFcracktip.value[0].data[1]
    rRFcracktip = np.cos(phi)*xRFcracktip + np.sin(phi)*yRFcracktip 
    thetaRFcracktip = -np.sin(phi)*xRFcracktip + np.cos(phi)*yRFcracktip
    if 'second' in parameters['elements']['order']:
        xRFfirstbounded = RFfirstbounded.value[0].data[0]
        yRFfirstbounded = RFfirstbounded.value[0].data[1]
        rRFfirstbounded = np.cos(phi)*xRFfirstbounded + np.sin(phi)*yRFfirstbounded 
        thetaRFfirstbounded = -np.sin(phi)*xRFfirstbounded + np.cos(phi)*yRFfirstbounded
    
    xfiberCracktipDisplacement = fiberCracktipDisplacement.value[0].data[0]
    yfiberCracktipDisplacement = fiberCracktipDisplacement.value[0].data[1]
    rfiberCracktipDisplacement = np.cos(phi)*xfiberCracktipDisplacement + np.sin(phi)*yfiberCracktipDisplacement
    thetafiberCracktipDisplacement = -np.sin(phi)*xfiberCracktipDisplacement + np.cos(phi)*yfiberCracktipDisplacement
    xmatrixCracktipDisplacement = matrixCracktipDisplacement.value[0].data[0]
    ymatrixCracktipDisplacement = matrixCracktipDisplacement.value[0].data[1]
    rmatrixCracktipDisplacement = np.cos(phi)*xmatrixCracktipDisplacement + np.sin(phi)*ymatrixCracktipDisplacement 
    thetamatrixCracktipDisplacement = -np.sin(phi)*xmatrixCracktipDisplacement + np.cos(phi)*ymatrixCracktipDisplacement
    if 'second' in parameters['elements']['order']:
        xfiberFirstboundedDisplacement = fiberFirstboundedDisplacement.value[0].data[0]
        yfiberFirstboundedDisplacement = fiberFirstboundedDisplacement.value[0].data[1]
        rfiberFirstboundedDisplacement = np.cos(phi)*xfiberFirstboundedDisplacement + np.sin(phi)*yfiberFirstboundedDisplacement
        thetafiberFirstboundedDisplacement = -np.sin(phi)*xfiberFirstboundedDisplacement + np.cos(phi)*yfiberFirstboundedDisplacement
        xmatrixFirstboundedDisplacement = matrixFirstboundedDisplacement.value[0].data[0]
        ymatrixFirstboundedDisplacement = matrixFirstboundedDisplacement.value[0].data[1]
        rmatrixFirstboundedDisplacement = np.cos(phi)*xmatrixFirstboundedDisplacement + np.sin(phi)*ymatrixFirstboundedDisplacement
        thetamatrixFirstboundedDisplacement = -np.sin(phi)*xmatrixFirstboundedDisplacement + np.cos(phi)*ymatrixFirstboundedDisplacement
    
    xcracktipDisplacement = xmatrixCracktipDisplacement - xfiberCracktipDisplacement
    ycracktipDisplacement = ymatrixCracktipDisplacement - yfiberCracktipDisplacement
    rcracktipDisplacement = rmatrixCracktipDisplacement - rfiberCracktipDisplacement
    thetacracktipDisplacement = thetamatrixCracktipDisplacement - thetafiberCracktipDisplacement
    if 'second' in parameters['elements']['order']:
        xfirstboundedDisplacement = xmatrixFirstboundedDisplacement - xfiberFirstboundedDisplacement
        yfirstboundedDisplacement = ymatrixFirstboundedDisplacement - yfiberFirstboundedDisplacement
        rfirstboundedDisplacement = rmatrixFirstboundedDisplacement - rfiberFirstboundedDisplacement
        thetafirstboundedDisplacement = thetamatrixFirstboundedDisplacement - thetafiberFirstboundedDisplacement
        
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)
    
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Compute VCCT with GTOT=GI+GII ...',True)
    
    if 'second' in parameters['elements']['order']:
        GI = np.abs(0.5*(rRFcracktip*rcracktipDisplacement+rRFfirstbounded*rfirstboundedDisplacement)/(parameters['Rf']*parameters['delta']*np.pi/180.0))
        GII = np.abs(0.5*(thetaRFcracktip*thetacracktipDisplacement+thetaRFfirstbounded*thetafirstboundedDisplacement)/(parameters['Rf']*parameters['delta']*np.pi/180.0))
        GTOTequiv = np.abs(0.5*(xRFcracktip*xcracktipDisplacement+yRFcracktip*ycracktipDisplacement+xRFfirstbounded*xfirstboundedDisplacement+yRFfirstbounded*yfirstboundedDisplacement)/(parameters['Rf']*parameters['delta']*np.pi/180.0))
    else:
        GI = np.abs(0.5*(rRFcracktip*rcracktipDisplacement)/(parameters['Rf']*parameters['delta']*np.pi/180.0))
        GII = np.abs(0.5*(thetaRFcracktip*thetacracktipDisplacement)/(parameters['Rf']*parameters['delta']*np.pi/180.0))
        GTOTequiv = np.abs(0.5*(xRFcracktip*xcracktipDisplacement+yRFcracktip*ycracktipDisplacement)/(parameters['Rf']*parameters['delta']*np.pi/180.0))
    
    GTOT = GI + GII
    
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)
    
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Compute VCCT with GI=GTOT-GII ...',True)
    
    if 'second' in parameters['elements']['order']:
        GIIv2 = np.abs(0.5*(thetaRFcracktip*thetacracktipDisplacement+thetaRFfirstbounded*thetafirstboundedDisplacement)/(parameters['Rf']*parameters['delta']*np.pi/180.0))
    else:
        GIIv2 = np.abs(0.5*(thetaRFcracktip*thetacracktipDisplacement)/(parameters['Rf']*parameters['delta']*np.pi/180.0))
    
    GTOTv2 = Jintegrals[-1]
    
    GIv2 = GTOTv2 - GIIv2
    
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)
    
    if 'second' in parameters['elements']['order']:
        appendCSVfile(parameters['output']['global']['directory'],parameters['output']['global']['filenames']['energyreleaserate'],[parameters['deltatheta'],parameters['Rf'],parameters['Rf'],parameters['Rf']/parameters['Rf'],phiCZ,G0,GI/G0,GII/G0,GTOT/G0,GIv2/G0,GIIv2/G0,GTOTv2/G0,GTOTequiv/G0,GI,GII,GTOT,GIv2,GIIv2,GTOTv2,GTOTequiv,np.min(uR),np.max(uR),np.mean(uR),np.min(uTheta),np.max(uTheta),np.mean(uTheta),xRFcracktip,yRFcracktip,xRFfirstbounded,yRFfirstbounded,rRFcracktip,thetaRFcracktip,rRFfirstbounded,thetaRFfirstbounded,xcracktipDisplacement,ycracktipDisplacement,rcracktipDisplacement,thetacracktipDisplacement,xfirstboundedDisplacement,yfirstboundedDisplacement,rfirstboundedDisplacement,thetafirstboundedDisplacement,xfiberCracktipDisplacement,yfiberCracktipDisplacement,rfiberCracktipDisplacement,thetafiberCracktipDisplacement,xfiberFirstboundedDisplacement,yfiberFirstboundedDisplacement,rfiberFirstboundedDisplacement,thetafiberFirstboundedDisplacement,xmatrixracktipDisplacement,ymatrixCracktipDisplacement,rmatrixCracktipDisplacement,thetamatrixCracktipDisplacement,xmatrixFirstboundedDisplacement,ymatrixFirstboundedDisplacement,rmatrixFirstboundedDisplacement,thetamatrixFirstboundedDisplacement])
    else:
        appendCSVfile(parameters['output']['global']['directory'],parameters['output']['global']['filenames']['energyreleaserate'],[parameters['deltatheta'],parameters['Rf'],parameters['Rf'],parameters['Rf']/parameters['Rf'],phiCZ,G0,GI/G0,GII/G0,GTOT/G0,GIv2/G0,GIIv2/G0,GTOTv2/G0,GTOTequiv/G0,GI,GII,GTOT,GIv2,GIIv2,GTOTv2,GTOTequiv,np.min(uR),np.max(uR),np.mean(uR),np.min(uTheta),np.max(uTheta),np.mean(uTheta),xRFcracktip,yRFcracktip,rRFcracktip,thetaRFcracktip,,xcracktipDisplacement,ycracktipDisplacement,rcracktipDisplacement,thetacracktipDisplacement,xfiberCracktipDisplacement,yfiberCracktipDisplacement,rfiberCracktipDisplacement,thetafiberCracktipDisplacement,xmatrixCracktipDisplacement,ymatrixCracktipDisplacement,rmatrixCracktipDisplacement,thetamatrixCracktipDisplacement])
    
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    #=======================================================================
    # END - compute VCCT
    #=======================================================================
    
    #=======================================================================
    # BEGIN - close ODB
    #=======================================================================
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Closing ODB database ...',True)
    odb.close()
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    #=======================================================================
    # END - close ODB
    #=======================================================================
    
    writeLineToLogFile(logfilefullpath,'a',baselogindent + logindent + 'Exiting function: analyzeRVEresults(wd,odbname,parameters)',True)
    
    
    
def main(argv):
    
    #=======================================================================
    # BEGIN - DATA
    #=======================================================================
    
    # units are already the ones used in simulation, not SI ==> conversion tool must be added
    
    # constant Vff, i.e. L/Rf, and variable deltatheta
    
    RVEparams = {}
    
    RVEparams['input'] = {'wd':'D:/01_Luca/07_Data/03_FEM/CurvedInterface',
                          'caefilename':'caePythonTest',
                          'modelname':''}
    RVEparams['geometry'] = {'L':100.0,
                             'Rf':1.0,
                             'deltatheta':10.0}
    RVEparams['materials'] = [{'name':'glassFiber',
                               'elastic':{'type':'ISOTROPIC',
                                           'values':[70e3,0.2]}},
                               {'name':'epoxy',
                               'elastic':{'type':'ISOTROPIC',
                                           'values':[3.5e3,0.4]}}]
    # in general:
    # params['materials'] = [{'name':'material1',
    #                            'elastic':{'type':'type1',
    #                                        'values':[]},
    #                            'density':{'values':[]},
    #                            'thermalexpansion':{'type':'type1',
    #                                                'values':[]},
    #                            'thermalconductivity':{'type':'type1',
    #                                                   'values':[]}},
    #                            {'name':'material2',
    #                            'elastic':{'type':'type2',
    #                                        'values':[]}}]
    RVEparams['sections'] = [{'name':'fiberSection',
                              'type':'HomogeneousSolidSection',
                              'material':'glassFiber',
                              'thickness':1.0},
                              {'name':'matrixSection',
                              'type':'HomogeneousSolidSection',
                              'material':'epoxy',
                              'thickness':1.0}]
    RVEparams['sectionRegions'] = [{'name':'fiberSection',
                                    'set':'FIBER',
                                    'offsetType':'MIDDLE_SURFACE',
                                    'offsetField':'',
                                    'thicknessAssignment':'FROM_SECTION',
                                    'offsetValue':0.0},
                                    {'name':'fiberSection',
                                    'set':'FIBER',
                                    'offsetType':'MIDDLE_SURFACE',
                                    'offsetField':'',
                                    'thicknessAssignment':'FROM_SECTION',
                                    'offsetValue':0.0}]
    RVEparams['step'] = {'minimumIncrement':1e-10}
    RVEparams['loads'] = [{'name':'rightBC',
                           'type':'appliedStrain',
                           'set':'RIGHTSIDE',
                           'value':[0.01,0.0,0.0]},
                            {'name':'leftBC',
                           'type':'appliedStrain',
                           'set':'LEFTSIDE',
                           'value':[-0.01,0.0,0.0]}]
    RVEparams['mesh'] = {'size':{'deltapsi':,
                                 'deltaphi':,
                                 'delta':0.05,
                                 'delta1':0.1,
                                 'delta2':0.5,
                                 'delta3':1.0},
                         'elements':{'minElNum':10,
                                     'order':'second'}}
    RVEparams['Jintegral'] = {'numberOfContours':50}
    RVEparams['output'] = {'global':{'directory':'D:/OneDrive/01_Luca/07_DocMASE/07_Data/03_FEM/caePythonTest',
                                     'filenames':{'performances':'',
                                                  'energyreleaserate':''}},
                           'local':{'directory':'D:/OneDrive/01_Luca/07_DocMASE/07_Data/03_FEM/caePythonTest',
                                     'filenames':{'Jintegral':'',
                                                  'stressesatboundary':'',
                                                  'crackdisplacements':''}},
                           'report':{'global':{},
                                     'local':{}}
                          }
    
    # parameters for iterations
    # RVEparams['modelname']
    # RVEparams['deltatheta']
    # RVEparams['deltapsi']
    # RVEparams['deltaphi']
    
    #=======================================================================
    # END - DATA
    #=======================================================================
    
    #=======================================================================
    # BEGIN - ITERABLES
    #=======================================================================
    
    basename = 'RVE100-Half-SmallDisplacement-Free'
    
    iterationsSets = []
    
    for angle in range(10,160,10):
        set = []
        value1 = basename + '-' + str(angle).replace('.','_')
        value2 = angle
        if angle<20:
            value3 = 0.5*angle
            value4 = 20.0
        elif angle<140:
            value3 = 10.0
            value4 = 20.0
        else:
            value3 = 0.4*(180.0-angle)
            value4 = 0.4*(180.0-angle)
        set.append([value1,value2,value3,value4])
    
    #=======================================================================
    # END - ITERABLES
    #=======================================================================
    
    #=======================================================================
    # BEGIN - ANALYSIS
    #=======================================================================
    
    workDir = RVEparams['input']['wd']
    
    logfilename = datetime.now().strftime('%Y-%m-%d_%H-%m-%s') + '_ABQ-RVE-generation-and-analysis' + '.log'
    logfilefullpath = join(workDir,logfilename)
    logindent = '    '
    
    if not os.path.exists(RVEparams['output']['global']['directory']):
            os.mkdirs(RVEparams['output']['global']['directory'])
            
    with open(logfilefullpath,'w') as log:
        log.write('Automatic generation and FEM analysis of RVEs with Abaqus Python' + '\n')
        
    skipLineToLogFile(logfilefullpath,'a',True)
    writeLineToLogFile(logfilefullpath,'a','In function: main(argv)',True)
    
    skipLineToLogFile(logfilefullpath,'a',True)
    writeLineToLogFile(logfilefullpath,'a',logindent + 'Global timer starts',True)
    globalStart = timeit.default_timer()
    
    for set in iterationsSets:
        
        RVEparams['input']['modelname'] = set[0]
        RVEparams['geometry']['deltatheta'] = set[1]
        RVEparams['mesh']['size']['deltapsi'] = set[2]
        RVEparams['mesh']['size']['deltaphi'] = set[3]        
        RVEparams['output']['local']['directory'] = join(RVEparams['output']['global']['directory'],set[0])
        
        if not os.path.exists(RVEparams['output']['local']['directory']):
                os.mkdirs(RVEparams['output']['local']['directory'])
                
        skipLineToLogFile(logfilefullpath,'a',True)
        writeLineToLogFile(logfilefullpath,'a',logindent + 'Calling function: createRVE(parameters,logfilepath,baselogindent,logindent)',True)
        writeLineToLogFile(logfilefullpath,'a',logindent + 'Local timer starts',True)
        localStart = timeit.default_timer()
        try:
            modelData = createRVE(RVEparams,logfilefullpath,logindent,logindent)
            localElapsedTime = timeit.default_timer() - localStart
            writeLineToLogFile(logfilefullpath,'a',logindent + 'Successfully returned from function: ',True)
            writeLineToLogFile(logfilefullpath,'a',logindent + 'Local timer stopped',True)
            writeLineToLogFile(logfilefullpath,'a',logindent + 'Elapsed time: ' + str(localElapsedTime),True)
        except Exception, error:
            writeErrorToLogFile(logfilefullpath,'a',Exception,error,True)
            sys.exit(2)
            
        skipLineToLogFile(logfilefullpath,'a',True)
        writeLineToLogFile(logfilefullpath,'a',logindent + 'Calling function: modifyRVEinputfile(parameters,mdbData,logfilepath,baselogindent,logindent)',True)
        writeLineToLogFile(logfilefullpath,'a',logindent + 'Local timer starts',True)
        localStart = timeit.default_timer()
        try:
            inputfilename = modifyRVEinputfile(RVEparams,modelData,logfilefullpath,logindent,logindent)
            localElapsedTime = timeit.default_timer() - localStart
            writeLineToLogFile(logfilefullpath,'a',logindent + 'Successfully returned from function: ',True)
            writeLineToLogFile(logfilefullpath,'a',logindent + 'Local timer stopped',True)
            writeLineToLogFile(logfilefullpath,'a',logindent + 'Elapsed time: ' + str(localElapsedTime),True)
        except Exception, error:
            writeErrorToLogFile(logfilefullpath,'a',Exception,error,True)
            sys.exit(2)
        
        skipLineToLogFile(logfilefullpath,'a',True)
        writeLineToLogFile(logfilefullpath,'a',logindent + 'Calling function: runRVEsimulation(wd,inpfile,logfilepath,baselogindent,logindent)',True)
        writeLineToLogFile(logfilefullpath,'a',logindent + 'Local timer starts',True)
        localStart = timeit.default_timer()
        try:
            runRVEsimulation(RVEparams['input']['wd'],inputfilename,logfilefullpath,logindent,logindent)
            localElapsedTime = timeit.default_timer() - localStart
            writeLineToLogFile(logfilefullpath,'a',logindent + 'Successfully returned from function: ',True)
            writeLineToLogFile(logfilefullpath,'a',logindent + 'Local timer stopped',True)
            writeLineToLogFile(logfilefullpath,'a',logindent + 'Elapsed time: ' + str(localElapsedTime),True)
        except Exception, error:
            writeErrorToLogFile(logfilefullpath,'a',Exception,error,True)
            sys.exit(2)
        
        skipLineToLogFile(logfilefullpath,'a',True)
        writeLineToLogFile(logfilefullpath,'a',logindent + 'Calling function: analyzeRVEresults(wd,odbname,logfilepath,parameters)',True)
        writeLineToLogFile(logfilefullpath,'a',logindent + 'Local timer starts',True)
        localStart = timeit.default_timer()
        try:
            createCSVfile(parameters['output']['global']['directory'],parameters['output']['global']['filenames']['performances'],'PROJECT NAME, NUMBER OF CPUS [-], USER TIME [s], SYSTEM TIME [s], USER TIME/TOTAL CPU TIME [%], SYSTEM TIME/TOTAL CPU TIME [%], TOTAL CPU TIME [s], WALLCLOCK TIME [s], WALLCLOCK TIME [m], WALLCLOCK TIME [h], WALLCLOCK TIME/TOTAL CPU TIME [%], ESTIMATED FLOATING POINT OPERATIONS PER ITERATION [-], MINIMUM REQUIRED MEMORY [MB], MEMORY TO MINIMIZE I/O [MB], TOTAL NUMBER OF ELEMENTS [-], NUMBER OF ELEMENTS DEFINED BY THE USER [-], NUMBER OF ELEMENTS DEFINED BY THE PROGRAM [-], TOTAL NUMBER OF NODES [-], NUMBER OF NODES DEFINED BY THE USER [-], NUMBER OF NODES DEFINED BY THE PROGRAM [-], TOTAL NUMBER OF VARIABLES [-]')
            createCSVfile(parameters['output']['global']['directory'],parameters['output']['global']['filenames']['energyreleaserate'],'')
            analyzeRVEresults(inputfilename.split('.')[0]+'.odb',RVEparams,logfilefullpath,logindent,logindent)
            localElapsedTime = timeit.default_timer() - localStart
            writeLineToLogFile(logfilefullpath,'a',logindent + 'Successfully returned from function: ',True)
            writeLineToLogFile(logfilefullpath,'a',logindent + 'Local timer stopped',True)
            writeLineToLogFile(logfilefullpath,'a',logindent + 'Elapsed time: ' + str(localElapsedTime),True)
        except Exception, error:
            writeErrorToLogFile(logfilefullpath,'a',Exception,error,True)
            sys.exit(2)
    
    globalElapsedTime = timeit.default_timer() - globalStart
    writeLineToLogFile(logfilefullpath,'a',logindent + 'Global timer stopped',True)
    writeLineToLogFile(logfilefullpath,'a',logindent + 'Elapsed time: ' + str(globalElapsedTime),True)
    
    skipLineToLogFile(logfilefullpath,'a',True)
    writeLineToLogFile(logfilefullpath,'a','Exiting function: main(argv)',True)
    writeLineToLogFile(logfilefullpath,'a','Goodbye!',True)

if __name__ == "__main__":
    main(sys.argv[1:])