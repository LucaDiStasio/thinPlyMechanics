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
import subprocess
from os.path import isfile, join, exists
from shutil import copyfile
import sqlite3
import locale
import ast
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
from odbAccess import *
from odbMaterial import *
from odbSection import *
#import __main__

#===============================================================================#
#===============================================================================#
#                              I/O functions
#===============================================================================#
#===============================================================================#

#===============================================================================#
#                              CSV files
#===============================================================================#

def createCSVfile(dir,filename,titleline=None):
    if len(filename.split('.'))<2:
        filename += '.csv'
    with open(join(dir,filename),'w') as csv:
        if titleline != None:
            csv.write(titleline.replace('\n','') + '\n')
        else:
            csv.write('# Automatically created on ' + datetime.now().strftime('%d/%m/%Y') + ' at' + datetime.now().strftime('%H:%M:%S') + '\n')

def appendCSVfile(dir,filename,data):
    # data is a list of lists
    # each list is written to a row
    # no check is made on data consistency
    if len(filename.split('.'))<2:
        filename += '.csv'
    with open(join(dir,filename),'a') as csv:
        for row in data:
            line = ''
            for v,value in enumerate(row):
                if v>0:
                    line += ', '
                line += str(value)
            csv.write(line + '\n')

#===============================================================================#
#                              ABAQUS input files
#===============================================================================#

def createABQinpfile(path):
    with open(path,'w') as fi:
        fi.write('** ABAQUS INPUT FILE' + '\n')
        fi.write('** Automatically created on ' + datetime.now().strftime('%d/%m/%Y') + ' at ' + datetime.now().strftime('%H:%M:%S') + '\n')
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

def writeTitleSepLineToLogFile(logFileFullPath,mode,toScreen):
    with open(logFileFullPath,mode) as log:
        log.write('===============================================================================================\n')
    if toScreen:
        print >> sys.__stdout__,('===============================================================================================\n')

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
        print >> sys.__stdout__,('!!! ----------------------------------------------------------------------------------------!!!\n')
        print >> sys.__stdout__,('\n')
        print >> sys.__stdout__,('                                     AN ERROR OCCURED\n')
        print >> sys.__stdout__,('\n')
        print >> sys.__stdout__,('                                -------------------------\n')
        print >> sys.__stdout__,('\n')
        print >> sys.__stdout__,(str(exc) + '\n')
        print >> sys.__stdout__,(str(err) + '\n')
        print >> sys.__stdout__,('\n')
        print >> sys.__stdout__,('Terminating program\n')
        print >> sys.__stdout__,('\n')
        print>> sys.__stdout__, ('!!! ----------------------------------------------------------------------------------------!!!\n')
        print>> sys.__stdout__, ('\n')

#===============================================================================#
#                                 Latex files
#===============================================================================#

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

def writeLatexMultiplePlots(folder,filename,data,axoptions,dataoptions,logfilepath,baselogindent,logindent):
    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + 'In function: writeLatexMultiplePlots(folder,filename,data,axoptions,dataoptions,logfilepath,baselogindent,logindent)',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Create latex file',True)
    createLatexFile(folder,filename,'standalone')
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Write latex packages',True)
    writeLatexPackages(folder,filename,['inputenc','pgfplots','tikz'],['utf8','',''])
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Document starts',True)
    writeLatexDocumentStarts(folder,filename)
    writeLatexTikzPicStarts(folder,filename,'')
    writeLatexTikzAxisStarts(folder,filename,axoptions)
    for k,datum in enumerate(data):
        writeLatexAddPlotTable(folder,filename,datum,dataoptions[k])
    writeLatexTikzAxisEnds(folder,filename)
    writeLatexTikzPicEnds(folder,filename)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Document ends',True)
    writeLatexDocumentEnds(folder,filename)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Create Windows command file',True)
    cmdfile = join(folder,'runlatex.cmd')
    with open(cmdfile,'w') as cmd:
        cmd.write('\n')
        cmd.write('CD ' + folder + '\n')
        cmd.write('\n')
        cmd.write('pdflatex ' + join(folder,filename + '.tex') + ' -job-name=' + filename + '\n')
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Executing Windows command file...',True)
    try:
        subprocess.call('cmd.exe /C ' + cmdfile)
        writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    except Exception,error:
        writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'ERROR',True)
        writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + str(Exception),True)
        writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + str(error),True)
        sys.exc_clear()

def writeLatexGenericCommand(folder,filename,command,options,arguments):
    with open(join(folder,filename + '.tex'),'a') as tex:
        if options!='' and arguments!='':
            tex.write('\\'+ command +'[' + options + ']{' + arguments + '}\n')
        elif options!='':
            tex.write('\\'+ command +'{' + arguments + '}\n')
        else:
            tex.write('\\'+ command + '\n')
        tex.write('\n')

def writeLatexCustomLine(folder,filename,line):
    with open(join(folder,filename + '.tex'),'a') as tex:
        tex.write(line + '\n')

def writeLatexSetLength(folder,filename,length,value):
    with open(join(folder,filename + '.tex'),'a') as tex:
        tex.write('\\setlength' +'{' + '\\' + length + '}' +'{' + value + '}\n')


#===============================================================================#
#===============================================================================#
#                        Data extraction functions
#===============================================================================#
#===============================================================================#

def getPerfs(wd,sims,logfilepath,baselogindent,logindent):
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + 'In function: getPerfs(wd,sims,logfilepath,baselogindent,logindent)',True)
    perf = []
    perf.append(['PROJECT NAME','DEBOND [°]','NUMBER OF CPUS [-]','USER TIME [s]','SYSTEM TIME [s]','USER TIME/TOTAL CPU TIME [%]','SYSTEM TIME/TOTAL CPU TIME [%]','TOTAL CPU TIME [s]','WALLCLOCK TIME [s]','WALLCLOCK TIME [m]','WALLCLOCK TIME [h]','WALLCLOCK TIME/TOTAL CPU TIME [%]','ESTIMATED FLOATING POINT OPERATIONS PER ITERATION [-]','MINIMUM REQUIRED MEMORY [MB]','MEMORY TO MINIMIZE I/O [MB]','TOTAL NUMBER OF ELEMENTS [-]','NUMBER OF ELEMENTS DEFINED BY THE USER [-]','NUMBER OF ELEMENTS DEFINED BY THE PROGRAM [-]','TOTAL NUMBER OF NODES [-]','NUMBER OF NODES DEFINED BY THE USER [-]','NUMBER OF NODES DEFINED BY THE PROGRAM [-]','TOTAL NUMBER OF VARIABLES [-]'])
    print('')
    for sim in sims:
        writeLineToLogFile(logfilepath,'a',baselogindent + logindent + 'Extract performances for simulation ' + sim,True)
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
        writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'In DAT file',True)
        if exists(join(wd,sim+'.dat')):
            with open(join(wd,sim+'.dat'),'r') as dat:
                lines = dat.readlines()
            for l,line in enumerate(lines):
                if 'JOB TIME SUMMARY' in line:
                    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '  - JOB TIME SUMMARY',True)
                    for subline in lines[l:]:
                        if 'USER TIME' in subline:
                            writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '  - USER TIME',True)
                            usertime = float(subline.split('=')[1])
                        elif 'SYSTEM TIME' in subline:
                            writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '  - SYSTEM TIME',True)
                            systemtime = float(subline.split('=')[1])
                        elif 'TOTAL CPU TIME' in subline:
                            writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '  - TOTAL CPU TIME',True)
                            totalcpu = float(subline.split('=')[1])
                        elif 'WALLCLOCK TIME' in subline:
                            writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '  - WALLCLOCK TIME',True)
                            wallclock = float(subline.split('=')[1])
                elif 'M E M O R Y   E S T I M A T E' in line:
                    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '  - MEMORY ESTIMATE',True)
                    values = lines[l+6].replace('\n','').split(' ')
                    while '' in values: values.remove('')
                    floatops = float(values[1])
                    minMemory = float(values[2])
                    minIOmemory = float(values[3])
                elif 'P R O B L E M   S I Z E' in line:
                    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '  - PROBLEM SIZE',True)
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
            writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'In MSG file',True)
            with open(join(wd,sim+'.msg'),'r') as msg:
                lines = msg.readlines()
                for line in lines:
                    if 'USING THE DIRECT SOLVER WITH' in line:
                        words = line.replace('\n','').split(' ')
                        while '' in words:
                            words.remove('')
                        cpus = int(words[words.index('PROCESSORS')-1])
                writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '  - PROCESSORS',True)
        perf.append([sim,cpus,usertime,systemtime,usertime/totalcpu,systemtime/totalcpu,totalcpu,wallclock,wallclock/60.,wallclock/3600.,wallclock/totalcpu,floatops,minMemory,minIOmemory,totEl,userEl,progEl,totN,userN,progN,totVar])
    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + 'Exiting function: getPerfs(wd,sims,logfilepath,baselogindent,logindent)',True)
    return perf

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

def getSingleElementSet(odbObj,part,elementSet):
    if part==None:
        result = odbObj.rootAssembly.elementSets[elementSet]
    else:
        result = odbObj.rootAssembly.instances[part].elementSets[elementSet]
    return result

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
#                        Data reporting functions
#===============================================================================#
#===============================================================================#

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
#                        Model creation functions
#===============================================================================#
#===============================================================================#

def reportSketchGeomElements(sketchGeometry,sketchVertices,logfilepath,baselogindent,logindent):
    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + 'The sketch has ' + str(len(sketchGeometry)) + ' geometric elements',True)
    for key in sketchGeometry.keys():
        writeLineToLogFile(logfilepath,'a',baselogindent + logindent + 'fiberGeometry[' + str(key) + '] = ' + str(sketchGeometry[key]),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + 'The sketch has ' + str(len(sketchVertices)) + ' vertices',True)
    for key in sketchVertices.keys():
        writeLineToLogFile(logfilepath,'a',baselogindent + logindent + 'fiberVertices[' + str(key) + '] = ' + str(sketchVertices[key]),True)

def defineSetOfVerticesByBoundingSphere(modelpart,Cx,Cy,Cz,R,setName,logfile,indent,toScreen):
    setOfVertices = modelpart.vertices.getByBoundingSphere(center=(Cx,Cy,Cz),radius=R)
    modelpart.Set(vertices=setOfVertices, name=setName)
    writeLineToLogFile(logfile,'a',indent + '-- ' + setName,toScreen)

def defineSetOfEdgesByClosestPoints(modelpart,Ax,Ay,Az,Bx,By,Bz,setName,logfile,indent,toScreen):
    setOfEdges = modelpart.edges.getClosest(coordinates=((Ax,Ay,Az),(Bx,By,Bz),))[0][0]
    modelpart.Set(edges = modelpart.edges[setOfEdges.index:setOfEdges.index+1], name=setName)
    writeLineToLogFile(logfile,'a',indent + '-- ' + setName,toScreen)

def defineSetOfFacesByFindAt(modelpart,Ax,Ay,Az,setName,logfile,indent,toScreen):
    setOfFaces = modelpart.faces.findAt(coordinates=(Ax,Ay,Az))
    modelpart.Set(faces = modelpart.faces[setOfFaces.index:setOfFaces.index+1], name=setName)
    writeLineToLogFile(logfile,'a',indent + '-- ' + setName,toScreen)

def create2Drectanglesketch(currentmodel,partName,partDimensionality,partType,sizeOfSheet,Ax,Ay,Bx,By,Cx,Cy,Dx,Dy,Clabel,Dlabel,logfilepath,baselogindent,logindent):
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + 'In function: create2Drectanglesketch(currentmodel,partName,partDimensionality,partType,sizeOfSheet,Ax,Ay,Bx,By,Cx,Cy,Dx,Dy,Clabel,Dlabel,logfilepath,baselogindent,logindent)',True)
    # create sketch
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Initialize sketch to draw the external shape of the RVE ...',True)
    currentsketch = currentmodel.ConstrainedSketch(name='__profile__',sheetSize=sizeOfSheet)
    currentsketch.setPrimaryObject(option=STANDALONE)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    # create rectangle
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Draw a rectangle ...',True)
    currentsketch.rectangle(point1=(Ax, Ay), point2=(Bx,By))
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    # set dimension labels
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Set dimension labels ...',True)
    v = currentsketch.vertices
    currentsketch.ObliqueDimension(vertex1=v[0], vertex2=v[1], textPoint=(Cx,Cy), value=Clabel)
    currentsketch.ObliqueDimension(vertex1=v[1], vertex2=v[2], textPoint=(Dx,Dy), value=Dlabel)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    # assign to part
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Assign sketch geometry to the part ...',True)
    currentpart = currentmodel.Part(name='RVE',dimensionality=TWO_D_PLANAR,type=DEFORMABLE_BODY)
    currentpart = currentmodel.parts['RVE']
    currentpart.BaseShell(sketch=RVEsketch)
    currentsketch.unsetPrimaryObject()
    del currentmodel.sketches['__profile__']
    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + '... done.',True)

def create2DRVEregion(currentmodel,type,L,logfilepath,baselogindent,logindent):
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + 'In function: create2DRVEregion(currentmodel,type,L,logfilepath,baselogindent,logindent)',True)
    # initialize parameters
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Initialize parameters ...',True)
    if type=='quarter':
        writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '  Model: quarter of RVE',True)
        sizeOfSheet = 2*L
        Ax = 0.0
        Ay = 0.0
        Bx = L
        By = L
        Cx = 0.5*L
        Cy = 1.1*L
        Dx = 1.1*L
        Dy = 0.5*L
        Clabel = L
        Dlabel = L
    elif type=='half':
        writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '  Model: quarter of RVE',True)
        sizeOfSheet = 3*L
        Ax = -L
        Ay = 0.0
        Bx = L
        By = L
        Cx = 1.1*L
        Cy = 0.5*L
        Dx = 0.0
        Dy = 1.1*L
        Clabel = L
        Dlabel = 2*L
    else:
        writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '  Model: quarter of RVE',True)
        sizeOfSheet = 3*L
        Ax = -L
        Ay = -L
        Bx = L
        By = L
        Cx = -1.1*L
        Cy = 0.0
        Dx = 0.0
        Dy = 1.1*L
        Clabel = 2*L
        Dlabel = 2*L
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '  sheet size = ' + str(sizeOfSheet),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '  Ax = ' + str(Ax),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '  Ay = ' + str(Ay),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '  Bx = ' + str(Bx),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '  By = ' + str(By),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '  Cx = ' + str(Cx),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '  Cy = ' + str(Cy),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '  Dx = ' + str(Dx),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '  Dy = ' + str(Dy),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '  Clabel = ' + str(Clabel),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '  Dlabel = ' + str(Dlabel),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Calling function: create2Drectanglesketch(currentmodel,partName,partDimensionality,partType,sizeOfSheet,Ax,Ay,Bx,By,Cx,Cy,Dx,Dy,Clabel,Dlabel,logfilepath,baselogindent,logindent)',True)
    create2Drectanglesketch(currentmodel,'RVE',TWO_D_PLANAR,DEFORMABLE_BODY,sizeOfSheet,Ax,Ay,Bx,By,Cx,Cy,Dx,Dy,Clabel,Dlabel,logfilepath,baselogindent + 2*logindent,logindent)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Successfully returned from function: create2Drectanglesketch(currentmodel,partName,partDimensionality,partType,sizeOfSheet,Ax,Ay,Bx,By,Cx,Cy,Dx,Dy,Clabel,Dlabel,logfilepath,baselogindent,logindent)',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + '... done.',True)

def add2DSymmCrack(currentmodel,logfilepath,baselogindent,logindent):
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + 'In function: add2DSymmCrack()',True)

    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + '... done.',True)

def add2DFullCrack(currentmodel,logfilepath,baselogindent,logindent):
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + 'In function: add2DFullCrack()',True)

    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + '... done.',True)

def add2DFiberSection(currentpart,currentmodel,planeToSketch,fiber,L,logfilepath,baselogindent,logindent):
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + 'In function: add2DFiberSection()',True)
    # create geometrical transform to draw partition sketch
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Create geometrical transform to draw partition sketch ...',True)
    transformToSketch = currentpart.MakeSketchTransform(sketchPlane=planeToSketch, sketchPlaneSide=SIDE1, origin=(0.0,0.0,0.0))
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    # create sketch
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Create sketch ...',True)
    fiberSketch = model.ConstrainedSketch(name='fiberSketch',sheetSize=3*L, gridSpacing=L/100.0, transform=transformToSketch)
    fiberSketch = model.sketches['fiberSketch']
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    # create reference to geometrical objects (faces, edges and vertices) of the partition sketch
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Create reference to geometrical objects of the partition sketch ...',True)
    fiberGeometry = fiberSketch.geometry
    fiberVertices = fiberSketch.vertices
    fiberSketch.setPrimaryObject(option=SUPERIMPOSE)
    reportSketchGeomElements(sketchGeometry,sketchVertices,logfilepath,baselogindent + 2*logindent,logindent)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    # Project reference onto sketch
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Project reference onto sketch ...',True)
    currentpart.projectReferencesOntoSketch(sketch=fiberSketch, filter=COPLANAR_EDGES)
    reportSketchGeomElements(fiberGeometry,fiberVertices,logfilepath,baselogindent + 2*logindent,logindent)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    # draw fiber
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Draw fiber ...',True)
    fiberSketch.ArcByCenterEnds(center=(fiber['center'][0], fiber['center'][1]), point1=(fiber['center'][0]+fiber['Rf']*np.cos(fiber['arcStart']*np.pi/180.0), fiber['center'][1]+fiber['Rf']*np.sin(fiber['arcStart']*np.pi/180.0)), point2=(fiber['center'][0]+fiber['Rf']*np.cos(fiber['arcStop']*np.pi/180.0), fiber['center'][1]+fiber['Rf']*np.sin(fiber['arcStop']*np.pi/180.0)), direction=CLOCKWISE) # fiberGeometry[6]
    reportSketchGeomElements(fiberGeometry,fiberVertices,logfilepath,baselogindent + 2*logindent,logindent)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Identify indeces of fiber and its center point ...',True)
    lastGeometryKey = 0
    for key in fiberGeometry.keys():
        lastGeometryKey = key
        if 'ARC' in fiberGeometry[key]['curveType']:
            fiberIndex = key
    lastVerticesKey = 0
    for key in fiberVertices.keys():
        lastVerticesKey = key
        if fiberVertices[key]['coords'][0]==0.0 and fiberVertices[key]['coords'][1]==0.0:
            fiberOriginIndex = key
    if fiber['isCracked']:
        writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'The fiber IS CRACKED',True)
        regionRadiuses = [fiber['R1'],fiber['R2'],fiber['R3'],fiber['R4']]
        circsectionsIndeces = []
        for R in regionRadiuses:
            writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Draw circular section with R = ' + str(R) + ' ...',True)
            fiberSketch.ArcByCenterEnds(center=(fiber['center'][0], fiber['center'][1]), point1=(fiber['center'][0]+R*np.cos(fiber['arcStart']*np.pi/180.0), fiber['center'][1]+R*np.sin(fiber['arcStart']*np.pi/180.0)), point2=(fiber['center'][0]+R*np.cos(fiber['arcStop']*np.pi/180.0), fiber['center'][1]+R*np.sin(fiber['arcStop']*np.pi/180.0)), direction=CLOCKWISE) # fiberGeometry[6]
            reportSketchGeomElements(fiberGeometry,fiberVertices,logfilepath,baselogindent + 2*logindent,logindent)
            lastGeometryKey += 1
            circsectionsIndeces.append(lastGeometryKey)
            writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
        if len(fiber['cracks'])>1:
            writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'There is 1 crack',True)
        else:
            writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'There are ' + str(len(fiber['cracks'])) + ' cracks',True)
        for cNum,crack in enumerate(fiber['cracks']):
            writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Crack number ' + str(cNum),True)
            angles = [crack['theta']+crack['deltatheta']]
            if crack['isMeasured']:
                writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The crack IS SUBJECT TO MEASUREMENTS',True)
                angles.append(crack['theta']+crack['deltatheta']-crack['deltapsi'])
                angles.append(crack['theta']+crack['deltatheta']+crack['deltapsi'])
                angles.append(crack['theta']+crack['deltatheta']+crack['deltapsi']+crack['deltaphi'])
            else:
                writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The crack IS NOT SUBJECT TO MEASUREMENTS',True)
            if not crack['isSymm']:
                writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The crack IS NOT SYMMETRIC',True)
                angles = [crack['theta']-crack['deltatheta']]
                angles.append(crack['theta']-crack['deltatheta']+crack['deltapsi'])
                angles.append(crack['theta']-crack['deltatheta']-crack['deltapsi'])
                angles.append(crack['theta']-crack['deltatheta']-crack['deltapsi']-crack['deltaphi'])
            else:
                writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The crack IS SYMMETRIC',True)
            constructionLinesIndeces = []
            for angle in angles:
                writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Draw construction line at = ' + str(angle) + ' deg ...',True)

    else:
        writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'The fiber IS NOT CRACKED',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + '... done.',True)

def add2DFullFiber(currentmodel,fiber,logfilepath,baselogindent,logindent):
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + 'In function: add2DFullFiber()',True)
    # create geometrical transform to draw partition sketch
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Create geometrical transform to draw partition sketch ...',True)
    transformToSketch = currentpart.MakeSketchTransform(sketchPlane=planeToSketch, sketchPlaneSide=SIDE1, origin=(0.0,0.0,0.0))
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    # create sketch
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Create sketch ...',True)
    fiberSketch = model.ConstrainedSketch(name='fiberSketch',sheetSize=3*L, gridSpacing=L/100.0, transform=transformToSketch)
    fiberSketch = model.sketches['fiberSketch']
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    # create reference to geometrical objects (faces, edges and vertices) of the partition sketch
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Create reference to geometrical objects of the partition sketch ...',True)
    fiberGeometry = fiberSketch.geometry
    fiberVertices = fiberSketch.vertices
    fiberSketch.setPrimaryObject(option=SUPERIMPOSE)
    reportSketchGeomElements(sketchGeometry,sketchVertices,logfilepath,baselogindent + 2*logindent,logindent)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    # Project reference onto sketch
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Project reference onto sketch ...',True)
    currentpart.projectReferencesOntoSketch(sketch=fiberSketch, filter=COPLANAR_EDGES)
    reportSketchGeomElements(sketchGeometry,sketchVertices,logfilepath,baselogindent + 2*logindent,logindent)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    # draw fiber
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Draw fiber ...',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Fiber',True)
    fiberSketch.CircleByCenterPerimeter(center=(fiber['center'][0], fiber['center'][1]), point1=(fiber['center'][0]+fiber['Rf']*np.cos(45.0*np.pi/180.0), fiber['center'][1]+fiber['Rf']*np.sin(45.0*np.pi/180.0)))
    reportSketchGeomElements(sketchGeometry,sketchVertices,logfilepath,baselogindent + 2*logindent,logindent)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    if fiber['cracks']['isCracked']:
        writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'The fiber IS CRACKED',True)
    else:
        writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'The fiber IS NOT CRACKED',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + '... done.',True)

def addMaterial(currentmodel,material,logfilepath,baselogindent,logindent):
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + 'In function: addMaterial()',True)
    currentmodel.Material(name=material['name'])
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'MATERIAL: ' + material['name'],True)
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
        writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '  ELASTIC',True)
        line = '    '
        for v,value in enumerate(values):
            if v>0:
                line += ', '
            line += str(value)
        writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + line,True)
    except Exception, error:
        writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '  NO ELASTIC PROPERTY',True)
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
        writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '  DENSITY',True)
        line = '    '
        for v,value in enumerate(values):
            if v>0:
                line += ', '
            line += str(value)
        writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + line,True)
    except Exception, error:
        writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '  NO DENSITY PROPERTY',True)
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
        writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '  THERMAL EXPANSION',True)
        line = '    '
        for v,value in enumerate(values):
            if v>0:
                line += ', '
            line += str(value)
        writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + line,True)
    except Exception, error:
        writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '  NO THERMAL EXPANSION PROPERTY',True)
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
        writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '  THERMAL CONDUCTIVITY',True)
        line = '    '
        for v,value in enumerate(values):
            if v>0:
                line += ', '
            line += str(value)
        writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + line,True)
    except Exception, error:
        writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '  NO THERMAL CONDUCTIVITY PROPERTY',True)
        sys.exc_clear()
    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + '... done.',True)

def assignMeshControls(thisModel,assemblyName,setName,elementShape,controls,logfile,indent,toScreen):
    thisModel.rootAssembly.setMeshControls(regions=(thisModel.rootAssembly.instances[assemblyName].sets[setName].faces), elemShape=elementShape, technique=controls)
    writeLineToLogFile(logfile,'a',indent + '-- ' + setName,toScreen)

def seedEdgeByNumber(thisModel,assemblyName,setName,seedsNumber,seedsConstraint,logfile,indent,toScreen):
    thisModel.rootAssembly.seedEdgeByNumber(edges=(thisModel.rootAssembly.instances[assemblyName].sets[setName].edges), number=int(seedsNumber), constraint=seedsConstraint)
    writeLineToLogFile(logfile,'a',indent + '-- ' + setName,toScreen)

def assemble2DRVE(parameters,logfilepath,baselogindent,logindent):
    # this will supersede and substitute createRVE()
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + 'In function: assemble2DRVE(parameters,logfilepath,baselogindent,logindent)',True)

#===============================================================================#
#                          Model database creation
#===============================================================================#
# if CAE database exists, open it; otherwise create new one
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Creating CAE database and model ...',True)
    caefullpath = join(parameters['input']['wd'],parameters['input']['caefilename'])
    if isfile(caefullpath):
        skipLineToLogFile(logfilepath,'a',True)
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'CAE database already exists. Opening it ...',True)
        openMdb(caefullpath)
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)
    else:
        skipLineToLogFile(logfilepath,'a',True)
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'CAE database does not exist. Creating it ...',True)
        mdb.saveAs(caefullpath)
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)
    # create and assign model object to variable for lighter code
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Creating model ' + parameters['input']['modelname'] + ' ...',True)
    mdb.Model(name=parameters['input']['modelname'])
    model = mdb.models[parameters['input']['modelname']]
    writeLineToLogFile(logfilepath,'a',baselogindent + 3**logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)

#===============================================================================#
#                            Create RVE region
#===============================================================================#
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Creating RVE region ...',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Calling function: create2DRVEregion(currentmodel,type,L,logfilepath,baselogindent,logindent)',True)
    create2DRVEregion(model,parameters['geometry']['RVE-type'],parameters['geometry']['L'],logfilepath,baselogindent + logindent,logindent)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Successfully returned from function: create2DRVEregion(currentmodel,type,L,logfilepath,baselogindent,logindent)',True)

    mdb.save()

    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)

#===============================================================================#
#                         Create fibers and debonds
#===============================================================================#
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Creating fibers and debonds ...',True)
    for fiber in parameters['fibers']:
        if fiber['type'] == 'quarter':
            writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Calling function: ',True)

            writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Successfully returned from function: ',True)
        elif fiber['type'] == 'half':
            writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Calling function: ',True)

            writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Successfully returned from function: ',True)
        else:
            writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Calling function: ',True)

            writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Successfully returned from function: ',True)

    mdb.save()

    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)

#===============================================================================#
#                             Materials creation
#===============================================================================#

    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Creating materials ...',True)
    for material in parameters['materials']:
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Calling function: addMaterial(currentmodel,material,logfilepath,baselogindent,logindent)',True)
        addMaterial(model,material,logfilepath,baselogindent + 3*logindent,logindent)
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Successfully returned from function: addMaterial(currentmodel,material,logfilepath,baselogindent,logindent)',True)

    mdb.save()

    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)

def createRVE(parameters,logfilepath,baselogindent,logindent):
#===============================================================================#
#                               Parameters
#===============================================================================#
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + 'In function: createRVE(parameters,logfilepath,logindent)',True)
    # assign most used parameters to variables
    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + 'Read and assign most used parameters to variables ...',True)
    baselogindent += logindent
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
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Working directory: ' + wd,True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'CAE database name: ' + caefilename,True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Model name: ' + modelname,True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'L: ' + str(L),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Rf: ' + str(Rf),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'L/Rf: ' + str(L/Rf),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'theta: ' + str(theta),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'deltatheta: ' + str(deltatheta),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'deltapsi: ' + str(deltapsi),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'deltaphi: ' + str(deltaphi),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'delta: ' + str(delta),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'minElnum: ' + str(minElNum),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + '... done.',True)
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
        writeLineToLogFile(logfilepath,'a',baselogindent + logindent + '... done.',True)
    # create and assign model object to variable for lighter code
    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + 'Creating model ' + modelname + ' ...',True)
    mdb.Model(name=modelname)
    model = mdb.models[modelname]
    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + '... done.',True)
#===============================================================================#
#                             Parts creation
#===============================================================================#
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + 'Creating part ...',True)
    # create sketch
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Initialize sketch to draw the external shape of the RVE ...',True)
    RVEsketch = model.ConstrainedSketch(name='__profile__',
        sheetSize=3*L)
    RVEsketch.setPrimaryObject(option=STANDALONE)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    # create rectangle
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Draw a rectangle ...',True)
    RVEsketch.rectangle(point1=(-L, 0.0), point2=(L,L))
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    # set dimension labels
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Set dimension labels ...',True)
    v = RVEsketch.vertices
    RVEsketch.ObliqueDimension(vertex1=v[0], vertex2=v[1], textPoint=(-1.1*L,0.5*L), value=L)
    RVEsketch.ObliqueDimension(vertex1=v[1], vertex2=v[2], textPoint=(0.0,1.1*L), value=2*L)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    # assign to part
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Assign sketch geometry to the part ...',True)
    RVEpart = model.Part(name='RVE',dimensionality=TWO_D_PLANAR,type=DEFORMABLE_BODY)
    RVEpart = model.parts['RVE']
    RVEpart.BaseShell(sketch=RVEsketch)
    RVEsketch.unsetPrimaryObject()
    del model.sketches['__profile__']
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    # create reference to geometrical objects (faces, edges and vertices) of the part
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Create reference to geometrical objects of the part ...',True)
    RVEfaces = RVEpart.faces
    RVEedges = RVEpart.edges
    RVEvertices = RVEpart.vertices
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    # create geometrical transform to draw partition sketch
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Create geometrical transform to draw partition sketch ...',True)
    transformToSketch = RVEpart.MakeSketchTransform(sketchPlane=RVEfaces[0], sketchPlaneSide=SIDE1, origin=(0.0,0.5*L, 0.0))
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    # create sketch
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Create sketch ...',True)
    fiberSketch = model.ConstrainedSketch(name='fiberSketch',sheetSize=3*L, gridSpacing=L/100.0, transform=transformToSketch)
    fiberSketch = model.sketches['fiberSketch']
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    # create reference to geometrical objects (faces, edges and vertices) of the partition sketch
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Create reference to geometrical objects of the partition sketch ...',True)
    fiberGeometry = fiberSketch.geometry
    fiberVertices = fiberSketch.vertices
    fiberSketch.setPrimaryObject(option=SUPERIMPOSE)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The sketch has ' + str(len(fiberGeometry)) + ' geometric elements',True)
    for key in fiberGeometry.keys():
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'fiberGeometry[' + str(key) + '] = ' + str(fiberGeometry[key]),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The sketch has ' + str(len(fiberVertices)) + ' vertices',True)
    for key in fiberVertices.keys():
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'fiberVertices[' + str(key) + '] = ' + str(fiberVertices[key]),True)
    #raw_input()
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    # Project reference onto sketch
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Project reference onto sketch ...',True)
    RVEpart.projectReferencesOntoSketch(sketch=fiberSketch, filter=COPLANAR_EDGES)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The sketch has ' + str(len(fiberGeometry)) + ' geometric elements',True)
    for key in fiberGeometry.keys():
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'fiberGeometry[' + str(key) + '] = ' + str(fiberGeometry[key]),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The sketch has ' + str(len(fiberVertices)) + ' vertices',True)
    for key in fiberVertices.keys():
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'fiberVertices[' + str(key) + '] = ' + str(fiberVertices[key]),True)
    #raw_input()
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    # draw fiber and circular sections for mesh generation
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Draw fiber and circular sections for mesh generation ...',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Fiber',True)
    fiberSketch.ArcByCenterEnds(center=(0.0, -0.5*L), point1=(-Rf, -0.5*L), point2=(Rf,-0.5*L), direction=CLOCKWISE) # fiberGeometry[6]
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The sketch has ' + str(len(fiberGeometry)) + ' geometric elements',True)
    for key in fiberGeometry.keys():
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'fiberGeometry[' + str(key) + '] = ' + str(fiberGeometry[key]),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The sketch has ' + str(len(fiberVertices)) + ' vertices',True)
    for key in fiberVertices.keys():
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'fiberVertices[' + str(key) + '] = ' + str(fiberVertices[key]),True)
    #raw_input()
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Arc at 0.75*Rf',True)
    fiberSketch.ArcByCenterEnds(center=(0.0, -0.5*L), point1=(-0.75*Rf, -0.5*L), point2=(0.75*Rf,-0.5*L), direction=CLOCKWISE) # fiberGeometry[7]
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The sketch has ' + str(len(fiberGeometry)) + ' geometric elements',True)
    for key in fiberGeometry.keys():
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'fiberGeometry[' + str(key) + '] = ' + str(fiberGeometry[key]),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The sketch has ' + str(len(fiberVertices)) + ' vertices',True)
    for key in fiberVertices.keys():
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'fiberVertices[' + str(key) + '] = ' + str(fiberVertices[key]),True)
    #raw_input()
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Arc at 0.5*Rf',True)
    fiberSketch.ArcByCenterEnds(center=(0.0, -0.5*L), point1=(-0.5*Rf, -0.5*L), point2=(0.5*Rf,-0.5*L), direction=CLOCKWISE) # fiberGeometry[8]
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The sketch has ' + str(len(fiberGeometry)) + ' geometric elements',True)
    for key in fiberGeometry.keys():
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'fiberGeometry[' + str(key) + '] = ' + str(fiberGeometry[key]),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The sketch has ' + str(len(fiberVertices)) + ' vertices',True)
    for key in fiberVertices.keys():
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'fiberVertices[' + str(key) + '] = ' + str(fiberVertices[key]),True)
    #raw_input()
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Arc at 1.25*Rf',True)
    if L>2*Rf:
        fiberSketch.ArcByCenterEnds(center=(0.0, -0.5*L), point1=(-1.25*Rf, -0.5*L), point2=(1.25*Rf,-0.5*L), direction=CLOCKWISE) # fiberGeometry[9]
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The sketch has ' + str(len(fiberGeometry)) + ' geometric elements',True)
        for key in fiberGeometry.keys():
            writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'fiberGeometry[' + str(key) + '] = ' + str(fiberGeometry[key]),True)
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The sketch has ' + str(len(fiberVertices)) + ' vertices',True)
        for key in fiberVertices.keys():
            writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'fiberVertices[' + str(key) + '] = ' + str(fiberVertices[key]),True)
        #raw_input()
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Arc at 1.5*Rf',True)
        fiberSketch.ArcByCenterEnds(center=(0.0, -0.5*L), point1=(-1.5*Rf, -0.5*L), point2=(1.5*Rf,-0.5*L), direction=CLOCKWISE) # fiberGeometry[10]
    else:
        fiberSketch.ArcByCenterEnds(center=(0.0, -0.5*L), point1=(-(Rf+0.25*(L-Rf)), -0.5*L), point2=((Rf+0.25*(L-Rf)),-0.5*L), direction=CLOCKWISE) # fiberGeometry[9]
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The sketch has ' + str(len(fiberGeometry)) + ' geometric elements',True)
        for key in fiberGeometry.keys():
            writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'fiberGeometry[' + str(key) + '] = ' + str(fiberGeometry[key]),True)
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The sketch has ' + str(len(fiberVertices)) + ' vertices',True)
        for key in fiberVertices.keys():
            writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'fiberVertices[' + str(key) + '] = ' + str(fiberVertices[key]),True)
        #raw_input()
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Arc at 1.5*Rf',True)
        fiberSketch.ArcByCenterEnds(center=(0.0, -0.5*L), point1=(-(Rf+0.5*(L-Rf)), -0.5*L), point2=((Rf+0.5*(L-Rf)),-0.5*L), direction=CLOCKWISE) # fiberGeometry[10]
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The sketch has ' + str(len(fiberGeometry)) + ' geometric elements',True)
    for key in fiberGeometry.keys():
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'fiberGeometry[' + str(key) + '] = ' + str(fiberGeometry[key]),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The sketch has ' + str(len(fiberVertices)) + ' vertices',True)
    for key in fiberVertices.keys():
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'fiberVertices[' + str(key) + '] = ' + str(fiberVertices[key]),True)
    #raw_input()
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    # calculate angles for construction lines
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Calculate angles for construction lines ...',True)
    alpha = theta + deltatheta - deltapsi
    beta = theta + deltatheta + deltapsi
    gamma = theta + deltatheta + deltapsi + deltaphi
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The sketch has ' + str(len(fiberGeometry)) + ' geometric elements',True)
    for key in fiberGeometry.keys():
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'fiberGeometry[' + str(key) + '] = ' + str(fiberGeometry[key]),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The sketch has ' + str(len(fiberVertices)) + ' vertices',True)
    for key in fiberVertices.keys():
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'fiberVertices[' + str(key) + '] = ' + str(fiberVertices[key]),True)
    #raw_input()
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    # draw construction lines
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Draw construction lines ...',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Construction line at ' + str(theta+deltatheta) + ' deg',True)
    fiberSketch.ConstructionLine(point1=(0.0, -0.5*L), angle=(theta+deltatheta)) # fiberGeometry[11]
    fiberSketch.CoincidentConstraint(entity1=fiberVertices[6], entity2=fiberGeometry[11],addUndoState=False)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The sketch has ' + str(len(fiberGeometry)) + ' geometric elements',True)
    for key in fiberGeometry.keys():
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'fiberGeometry[' + str(key) + '] = ' + str(fiberGeometry[key]),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The sketch has ' + str(len(fiberVertices)) + ' vertices',True)
    for key in fiberVertices.keys():
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'fiberVertices[' + str(key) + '] = ' + str(fiberVertices[key]),True)
    #raw_input()
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Construction line at ' + str(alpha) + ' deg',True)
    fiberSketch.ConstructionLine(point1=(0.0, -0.5*L), angle=alpha) # fiberGeometry[12]
    fiberSketch.CoincidentConstraint(entity1=fiberVertices[6], entity2=fiberGeometry[12],addUndoState=False)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The sketch has ' + str(len(fiberGeometry)) + ' geometric elements',True)
    for key in fiberGeometry.keys():
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'fiberGeometry[' + str(key) + '] = ' + str(fiberGeometry[key]),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The sketch has ' + str(len(fiberVertices)) + ' vertices',True)
    for key in fiberVertices.keys():
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'fiberVertices[' + str(key) + '] = ' + str(fiberVertices[key]),True)
    #raw_input()
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Construction line at ' + str(beta) + ' deg',True)
    fiberSketch.ConstructionLine(point1=(0.0, -0.5*L), angle=beta) # fiberGeometry[13]
    fiberSketch.CoincidentConstraint(entity1=fiberVertices[6], entity2=fiberGeometry[13],addUndoState=False)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The sketch has ' + str(len(fiberGeometry)) + ' geometric elements',True)
    for key in fiberGeometry.keys():
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'fiberGeometry[' + str(key) + '] = ' + str(fiberGeometry[key]),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The sketch has ' + str(len(fiberVertices)) + ' vertices',True)
    for key in fiberVertices.keys():
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'fiberVertices[' + str(key) + '] = ' + str(fiberVertices[key]),True)
    #raw_input()
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Construction line at ' + str(gamma) + ' deg',True)
    fiberSketch.ConstructionLine(point1=(0.0, -0.5*L), angle=gamma) # fiberGeometry[14]
    fiberSketch.CoincidentConstraint(entity1=fiberVertices[6], entity2=fiberGeometry[14],addUndoState=False)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The sketch has ' + str(len(fiberGeometry)) + ' geometric elements',True)
    for key in fiberGeometry.keys():
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'fiberGeometry[' + str(key) + '] = ' + str(fiberGeometry[key]),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The sketch has ' + str(len(fiberVertices)) + ' vertices',True)
    for key in fiberVertices.keys():
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'fiberVertices[' + str(key) + '] = ' + str(fiberVertices[key]),True)
    #raw_input()
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    # draw angular sections to identify the crack and for mesh generation
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'draw angular sections to identify the crack and for mesh generation ...',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Compute internal and external radii ...',True)
    Rint = 0.75*Rf
    if L>2*Rf:
        Rext = 1.25*Rf
    else:
        Rext = Rf+0.25*(L-Rf)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The sketch has ' + str(len(fiberGeometry)) + ' geometric elements',True)
    for key in fiberGeometry.keys():
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'fiberGeometry[' + str(key) + '] = ' + str(fiberGeometry[key]),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The sketch has ' + str(len(fiberVertices)) + ' vertices',True)
    for key in fiberVertices.keys():
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'fiberVertices[' + str(key) + '] = ' + str(fiberVertices[key]),True)
    #raw_input()
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Create first circular section ...',True)
    Ax = Rint*np.cos(alpha*np.pi/180.0)
    Ay = -0.5*L+Rint*np.sin(alpha*np.pi/180.0)
    Bx = Rext*np.cos(alpha*np.pi/180.0)
    By = -0.5*L+Rext*np.sin(alpha*np.pi/180.0)
    fiberSketch.Line(point1=(Ax,Ay),point2=(Bx,By)) # fiberGeometry[15]
    fiberSketch.PerpendicularConstraint(entity1=fiberGeometry[7], entity2=fiberGeometry[15],addUndoState=False)
    fiberSketch.CoincidentConstraint(entity1=fiberVertices[15], entity2=fiberGeometry[7],addUndoState=False)
    fiberSketch.CoincidentConstraint(entity1=fiberVertices[16], entity2=fiberGeometry[9],addUndoState=False)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The sketch has ' + str(len(fiberGeometry)) + ' geometric elements',True)
    for key in fiberGeometry.keys():
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'fiberGeometry[' + str(key) + '] = ' + str(fiberGeometry[key]),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The sketch has ' + str(len(fiberVertices)) + ' vertices',True)
    for key in fiberVertices.keys():
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'fiberVertices[' + str(key) + '] = ' + str(fiberVertices[key]),True)
    #raw_input()
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Create second circular section ...',True)
    Ax = Rint*np.cos((theta+deltatheta)*np.pi/180.0)
    Ay = -0.5*L+Rint*np.sin((theta+deltatheta)*np.pi/180.0)
    Bx = Rext*np.cos((theta+deltatheta)*np.pi/180.0)
    By = -0.5*L+Rext*np.sin((theta+deltatheta)*np.pi/180.0)
    fiberSketch.Line(point1=(Ax,Ay),point2=(Bx,By)) # fiberGeometry[16]
    fiberSketch.PerpendicularConstraint(entity1=fiberGeometry[7], entity2=fiberGeometry[16],addUndoState=False)
    fiberSketch.CoincidentConstraint(entity1=fiberVertices[17], entity2=fiberGeometry[7],addUndoState=False)
    fiberSketch.CoincidentConstraint(entity1=fiberVertices[18], entity2=fiberGeometry[9],addUndoState=False)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The sketch has ' + str(len(fiberGeometry)) + ' geometric elements',True)
    for key in fiberGeometry.keys():
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'fiberGeometry[' + str(key) + '] = ' + str(fiberGeometry[key]),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The sketch has ' + str(len(fiberVertices)) + ' vertices',True)
    for key in fiberVertices.keys():
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'fiberVertices[' + str(key) + '] = ' + str(fiberVertices[key]),True)
    #raw_input()
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Create third circular section ...',True)
    Ax = Rint*np.cos(beta*np.pi/180.0)
    Ay = -0.5*L+Rint*np.sin(beta*np.pi/180.0)
    Bx = Rext*np.cos(beta*np.pi/180.0)
    By = -0.5*L+Rext*np.sin(beta*np.pi/180.0)
    fiberSketch.Line(point1=(Ax,Ay),point2=(Bx,By)) # fiberGeometry[17]
    fiberSketch.PerpendicularConstraint(entity1=fiberGeometry[7], entity2=fiberGeometry[17],addUndoState=False)
    fiberSketch.CoincidentConstraint(entity1=fiberVertices[19], entity2=fiberGeometry[7],addUndoState=False)
    fiberSketch.CoincidentConstraint(entity1=fiberVertices[20], entity2=fiberGeometry[9],addUndoState=False)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The sketch has ' + str(len(fiberGeometry)) + ' geometric elements',True)
    for key in fiberGeometry.keys():
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'fiberGeometry[' + str(key) + '] = ' + str(fiberGeometry[key]),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The sketch has ' + str(len(fiberVertices)) + ' vertices',True)
    for key in fiberVertices.keys():
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'fiberVertices[' + str(key) + '] = ' + str(fiberVertices[key]),True)
    #raw_input()
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Create fourth circular section ...',True)
    Ax = Rint*np.cos(gamma*np.pi/180.0)
    Ay = -0.5*L+Rint*np.sin(gamma*np.pi/180.0)
    Bx = Rext*np.cos(gamma*np.pi/180.0)
    By = -0.5*L+Rext*np.sin(gamma*np.pi/180.0)
    fiberSketch.Line(point1=(Ax,Ay),point2=(Bx,By)) # fiberGeometry[18]
    fiberSketch.PerpendicularConstraint(entity1=fiberGeometry[7], entity2=fiberGeometry[18],addUndoState=False)
    fiberSketch.CoincidentConstraint(entity1=fiberVertices[21], entity2=fiberGeometry[7],addUndoState=False)
    fiberSketch.CoincidentConstraint(entity1=fiberVertices[22], entity2=fiberGeometry[9],addUndoState=False)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The sketch has ' + str(len(fiberGeometry)) + ' geometric elements',True)
    for key in fiberGeometry.keys():
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'fiberGeometry[' + str(key) + '] = ' + str(fiberGeometry[key]),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The sketch has ' + str(len(fiberVertices)) + ' vertices',True)
    for key in fiberVertices.keys():
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'fiberVertices[' + str(key) + '] = ' + str(fiberVertices[key]),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Assign partition sketch to part ...',True)
    pickedFaces = RVEfaces.findAt(coordinates=(0.0, 0.5*L, 0))
    RVEpart.PartitionFaceBySketch(faces=pickedFaces, sketch=fiberSketch)
    fiberSketch.unsetPrimaryObject()
    del model.sketches['fiberSketch']
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)

    mdb.save()

    #-------------------#
    #                   #
    #    create sets    #
    #                   #
    #-------------------#

    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Create sets ...',True)

    # create reference to geometric elements for lighter code
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Create reference to geometric elements of the part ...',True)
    RVEvertices = RVEpart.vertices
    RVEedges = RVEpart.edges
    RVEfaces = RVEpart.faces
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The part has ' + str(len(RVEvertices)) + ' vertices',True)
    for e,element in enumerate(RVEvertices):
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'RVEvertices[' + str(e) + '] = ' + str(element),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The part has ' + str(len(RVEedges)) + ' edges',True)
    for e,element in enumerate(RVEedges):
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'RVEedges[' + str(e) + '] = ' + str(element),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'The part has ' + str(len(RVEfaces)) + ' faces',True)
    for e,element in enumerate(RVEfaces):
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'RVEfaces[' + str(e) + '] = ' + str(element),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)

    # sets of vertices
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Sets of vertices',True)
    defineSetOfVerticesByBoundingSphere(RVEpart,Rf*np.cos((theta+deltatheta)*np.pi/180),Rf*np.sin((theta+deltatheta)*np.pi/180),0.0,0.001*Rf,'CRACKTIP',logfilepath,baselogindent + 4*logindent,True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)

    # sets of edges
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Sets of edges',True)
    setsOfEdgesData = [[0.99*Rf*np.cos(0.5*alpha*np.pi/180),0.99*Rf*np.sin(0.5*alpha*np.pi/180),0.0,1.01*Rf*np.cos(0.5*alpha*np.pi/180),1.01*Rf*np.sin(0.5*alpha*np.pi/180),0.0,'CRACK-LOWER'],
 [0.99*Rf*np.cos((alpha+0.5*deltapsi)*np.pi/180),0.99*Rf*np.sin((alpha+0.5*deltapsi)*np.pi/180),0.0,1.01*Rf*np.cos((alpha+0.5*deltapsi)*np.pi/180),1.01*Rf*np.sin((alpha+0.5*deltapsi)*np.pi/180),0.0,'CRACK-UPPER']]
    for setOfEdgesData in setsOfEdgesData:
        defineSetOfEdgesByClosestPoints(RVEpart,setOfEdgesData[0],setOfEdgesData[1],setOfEdgesData[2],setOfEdgesData[3],setOfEdgesData[4],setOfEdgesData[5],setOfEdgesData[-1],logfilepath,baselogindent + 4*logindent,True)
    RVEpart.SetByBoolean(name='CRACK', sets=[RVEpart.sets['CRACK-LOWER'],RVEpart.sets['CRACK-UPPER']])
    writeLineToLogFile(logfilepath,'a',baselogindent + 4*logindent + '-- CRACK',True)

    setsOfEdgesData = [[0.001*Rf,0.001,0.0,0.001*Rf,-0.001,0.0,'LOWERSIDE-CENTER'],
                       [0.65*Rf,0.001,0.0,0.65*Rf,-0.001,0.0,'LOWERSIDE-FIRSTRING-RIGHT'],
                       [-0.65*Rf,0.001,0.0,-0.65*Rf,-0.001,0.0,'LOWERSIDE-FIRSTRING-LEFT']]
    for setOfEdgesData in setsOfEdgesData:
        defineSetOfEdgesByClosestPoints(RVEpart,setOfEdgesData[0],setOfEdgesData[1],setOfEdgesData[2],setOfEdgesData[3],setOfEdgesData[4],setOfEdgesData[5],setOfEdgesData[-1],logfilepath,baselogindent + 4*logindent,True)

    RVEpart.SetByBoolean(name='LOWERSIDE-FIRSTRING', sets=[RVEpart.sets['LOWERSIDE-FIRSTRING-RIGHT'],RVEpart.sets['LOWERSIDE-FIRSTRING-LEFT']])
    writeLineToLogFile(logfilepath,'a',baselogindent + 4*logindent + '-- LOWERSIDE-FIRSTRING',True)
    #RVEedges.getClosest(coordinates=(,,))[0][0]

    setsOfEdgesData = [[0.85*Rf,0.001,0.0,0.85*Rf,-0.001,0.0,'LOWERSIDE-SECONDRING-RIGHT'],
                       [-0.85*Rf,0.001,0.0,-0.85*Rf,-0.001,0.0,'LOWERSIDE-SECONDRING-LEFT']]
    for setOfEdgesData in setsOfEdgesData:
        defineSetOfEdgesByClosestPoints(RVEpart,setOfEdgesData[0],setOfEdgesData[1],setOfEdgesData[2],setOfEdgesData[3],setOfEdgesData[4],setOfEdgesData[5],setOfEdgesData[-1],logfilepath,baselogindent + 4*logindent,True)

    RVEpart.SetByBoolean(name='LOWERSIDE-SECONDRING', sets=[RVEpart.sets['LOWERSIDE-SECONDRING-RIGHT'],RVEpart.sets['LOWERSIDE-SECONDRING-LEFT']])
    writeLineToLogFile(logfilepath,'a',baselogindent + 4*logindent + '-- LOWERSIDE-SECONDRING',True)

    if L>2*Rf:
        R1 = (1+0.5*0.25)*Rf
        R2 = (1.25+0.5*0.25)*Rf
    else:
        R1 = Rf+0.5*0.25*(L-Rf)
        R2 = Rf+1.5*0.25*(L-Rf)

    setsOfEdgesData = [[R1,0.001,0.0,R1,-0.001,0.0,'LOWERSIDE-THIRDRING-RIGHT'],
                       [-R1,0.001,0.0,-R1,-0.001,0.0,'LOWERSIDE-THIRDRING-LEFT']]
    for setOfEdgesData in setsOfEdgesData:
        defineSetOfEdgesByClosestPoints(RVEpart,setOfEdgesData[0],setOfEdgesData[1],setOfEdgesData[2],setOfEdgesData[3],setOfEdgesData[4],setOfEdgesData[5],setOfEdgesData[-1],logfilepath,baselogindent + 4*logindent,True)

    RVEpart.SetByBoolean(name='LOWERSIDE-THIRDRING', sets=[RVEpart.sets['LOWERSIDE-THIRDRING-RIGHT'],RVEpart.sets['LOWERSIDE-THIRDRING-LEFT']])
    writeLineToLogFile(logfilepath,'a',baselogindent + 4*logindent + '-- LOWERSIDE-THIRDRING',True)

    setsOfEdgesData = [[R2,0.001,0.0,R2,-0.001,0.0,'LOWERSIDE-FOURTHRING-RIGHT'],
                       [-R2,0.001,0.0,-R2,-0.001,0.0,'LOWERSIDE-FOURTHRING-LEFT']]
    for setOfEdgesData in setsOfEdgesData:
        defineSetOfEdgesByClosestPoints(RVEpart,setOfEdgesData[0],setOfEdgesData[1],setOfEdgesData[2],setOfEdgesData[3],setOfEdgesData[4],setOfEdgesData[5],setOfEdgesData[-1],logfilepath,baselogindent + 4*logindent,True)

    RVEpart.SetByBoolean(name='LOWERSIDE-FOURTHRING', sets=[RVEpart.sets['LOWERSIDE-FOURTHRING-RIGHT'],RVEpart.sets['LOWERSIDE-FOURTHRING-LEFT']])
    writeLineToLogFile(logfilepath,'a',baselogindent + 4*logindent + '-- LOWERSIDE-FOURTHRING',True)

    RVEpart.SetByBoolean(name='LOWERSIDE', sets=[RVEpart.sets['LOWERSIDE-FIRSTRING'],RVEpart.sets['LOWERSIDE-SECONDRING'],RVEpart.sets['LOWERSIDE-THIRDRING'],RVEpart.sets['LOWERSIDE-FOURTHRING']])
    writeLineToLogFile(logfilepath,'a',baselogindent + 4*logindent + '-- LOWERSIDE',True)

    setsOfEdgesData = [[0.001,L,0.0,-0.001,L,0.0,'UPPERSIDE'],
                       [0.99*L,0.5*L,0.0,1.01*L,0.5*L,0.0,'RIGHTSIDE'],
                       [-0.99*L,0.5*L,0.0,-1.01*L,0.5*L,0.0,'LEFTSIDE'],
                       [0.49*Rf*np.cos((theta+deltatheta)*np.pi/180),0.49*Rf*np.sin((theta+deltatheta)*np.pi/180),0.0,0.51*Rf*np.cos((theta+deltatheta)*np.pi/180),0.51*Rf*np.sin((theta+deltatheta)*np.pi/180),0.0,'FIRSTCIRCLE'],
                       [0.74*Rf*np.cos(0.5*alpha*np.pi/180),0.74*Rf*np.sin(0.5*alpha*np.pi/180),0.0,0.76*Rf*np.cos(0.5*alpha*np.pi/180),0.76*Rf*np.sin(0.5*alpha*np.pi/180),0.0,'SECONDCIRCLE-LOWERCRACK'],
                       [0.74*Rf*np.cos((alpha+0.5*deltapsi)*np.pi/180),0.74*Rf*np.sin((alpha+0.5*deltapsi)*np.pi/180),0.0,0.76*Rf*np.cos((alpha+0.5*deltapsi)*np.pi/180),0.76*Rf*np.sin((alpha+0.5*deltapsi)*np.pi/180),0.0,'SECONDCIRCLE-UPPERCRACK'],
                       [0.74*Rf*np.cos((theta+deltatheta+0.5*deltapsi)*np.pi/180),0.74*Rf*np.sin((theta+deltatheta+0.5*deltapsi)*np.pi/180),0.0,0.76*Rf*np.cos((theta+deltatheta+0.5*deltapsi)*np.pi/180),0.76*Rf*np.sin((theta+deltatheta+0.5*deltapsi)*np.pi/180),0.0,'SECONDCIRCLE-FIRSTBOUNDED'],
                       [0.74*Rf*np.cos((beta+0.5*deltaphi)*np.pi/180),0.74*Rf*np.sin((beta+0.5*deltaphi)*np.pi/180),0.0,0.76*Rf*np.cos((beta+0.5*deltaphi)*np.pi/180),0.76*Rf*np.sin((beta+0.5*deltaphi)*np.pi/180),0.0,'SECONDCIRCLE-SECONDBOUNDED'],
                       [0.74*Rf*np.cos((gamma+0.5*(180.0-gamma))*np.pi/180),0.74*Rf*np.sin((gamma+0.5*(180.0-gamma))*np.pi/180),0.0,0.76*Rf*np.cos((gamma+0.5*(180.0-gamma))*np.pi/180),0.76*Rf*np.sin((gamma+0.5*(180.0-gamma))*np.pi/180),0.0,'SECONDCIRCLE-RESTBOUNDED']]
    for setOfEdgesData in setsOfEdgesData:
        defineSetOfEdgesByClosestPoints(RVEpart,setOfEdgesData[0],setOfEdgesData[1],setOfEdgesData[2],setOfEdgesData[3],setOfEdgesData[4],setOfEdgesData[5],setOfEdgesData[-1],logfilepath,baselogindent + 4*logindent,True)

    RVEpart.SetByBoolean(name='SECONDCIRCLE', sets=[RVEpart.sets['SECONDCIRCLE-LOWERCRACK'],RVEpart.sets['SECONDCIRCLE-UPPERCRACK'],RVEpart.sets['SECONDCIRCLE-FIRSTBOUNDED'],RVEpart.sets['SECONDCIRCLE-SECONDBOUNDED'],RVEpart.sets['SECONDCIRCLE-RESTBOUNDED']])
    writeLineToLogFile(logfilepath,'a',baselogindent + 4*logindent + '-- SECONDCIRCLE',True)

    setsOfEdgesData = [[0.99*Rf*np.cos(0.5*alpha*np.pi/180),0.99*Rf*np.sin(0.5*alpha*np.pi/180),0.0,1.01*Rf*np.cos(0.5*alpha*np.pi/180),1.01*Rf*np.sin(0.5*alpha*np.pi/180),0.0,'THIRDCIRCLE-LOWERCRACK'],
                       [0.99*Rf*np.cos((alpha+0.5*deltapsi)*np.pi/180),0.99*Rf*np.sin((alpha+0.5*deltapsi)*np.pi/180),0.0,1.01*Rf*np.cos((alpha+0.5*deltapsi)*np.pi/180),1.01*Rf*np.sin((alpha+0.5*deltapsi)*np.pi/180),0.0,'THIRDCIRCLE-UPPERCRACK'],
                       [0.99*Rf*np.cos((theta+deltatheta+0.5*deltapsi)*np.pi/180),0.99*Rf*np.sin((theta+deltatheta+0.5*deltapsi)*np.pi/180),0.0,1.01*Rf*np.cos((theta+deltatheta+0.5*deltapsi)*np.pi/180),1.01*Rf*np.sin((theta+deltatheta+0.5*deltapsi)*np.pi/180),0.0,'THIRDCIRCLE-FIRSTBOUNDED'],
                       [0.99*Rf*np.cos((beta+0.5*deltaphi)*np.pi/180),0.99*Rf*np.sin((beta+0.5*deltaphi)*np.pi/180),0.0,1.01*Rf*np.cos((beta+0.5*deltaphi)*np.pi/180),1.01*Rf*np.sin((beta+0.5*deltaphi)*np.pi/180),0.0,'THIRDCIRCLE-SECONDBOUNDED'],
                       [0.99*Rf*np.cos((gamma+0.5*(180.0-gamma))*np.pi/180),0.99*Rf*np.sin((gamma+0.5*(180.0-gamma))*np.pi/180),0.0,1.01*Rf*np.cos((gamma+0.5*(180.0-gamma))*np.pi/180),1.01*Rf*np.sin((gamma+0.5*(180.0-gamma))*np.pi/180),0.0,'THIRDCIRCLE-RESTBOUNDED']]
    for setOfEdgesData in setsOfEdgesData:
        defineSetOfEdgesByClosestPoints(RVEpart,setOfEdgesData[0],setOfEdgesData[1],setOfEdgesData[2],setOfEdgesData[3],setOfEdgesData[4],setOfEdgesData[5],setOfEdgesData[-1],logfilepath,baselogindent + 4*logindent,True)

    RVEpart.SetByBoolean(name='THIRDCIRCLE', sets=[RVEpart.sets['THIRDCIRCLE-LOWERCRACK'],RVEpart.sets['THIRDCIRCLE-UPPERCRACK'],RVEpart.sets['THIRDCIRCLE-FIRSTBOUNDED'],RVEpart.sets['THIRDCIRCLE-SECONDBOUNDED'],RVEpart.sets['THIRDCIRCLE-RESTBOUNDED']])
    writeLineToLogFile(logfilepath,'a',baselogindent + 4*logindent + '-- THIRDCIRCLE',True)

    if L>2*Rf:
        R4 = 1.25*Rf
    else:
        R4 = Rf+0.25*(L-Rf)

    setsOfEdgesData = [[0.99*R4*np.cos(0.5*alpha*np.pi/180),0.99*R4*np.sin(0.5*alpha*np.pi/180),0.0,1.01*R4*np.cos(0.5*alpha*np.pi/180),1.01*R4*np.sin(0.5*alpha*np.pi/180),0.0,'FOURTHCIRCLE-LOWERCRACK'],
                       [0.99*R4*np.cos((alpha+0.5*deltapsi)*np.pi/180),0.99*R4*np.sin((alpha+0.5*deltapsi)*np.pi/180),0.0,1.01*R4*np.cos((alpha+0.5*deltapsi)*np.pi/180),1.01*R4*np.sin((alpha+0.5*deltapsi)*np.pi/180),0.0,'FOURTHCIRCLE-UPPERCRACK'],
                       [0.99*R4*np.cos((theta+deltatheta+0.5*deltapsi)*np.pi/180),0.99*R4*np.sin((theta+deltatheta+0.5*deltapsi)*np.pi/180),0.0,1.01*R4*np.cos((theta+deltatheta+0.5*deltapsi)*np.pi/180),1.01*R4*np.sin((theta+deltatheta+0.5*deltapsi)*np.pi/180),0.0,'FOURTHCIRCLE-FIRSTBOUNDED'],
                       [0.99*R4*np.cos((beta+0.5*deltaphi)*np.pi/180),0.99*R4*np.sin((beta+0.5*deltaphi)*np.pi/180),0.0,1.01*R4*np.cos((beta+0.5*deltaphi)*np.pi/180),1.01*R4*np.sin((beta+0.5*deltaphi)*np.pi/180),0.0,'FOURTHCIRCLE-SECONDBOUNDED'],
                       [0.99*R4*np.cos((gamma+0.5*(180.0-gamma))*np.pi/180),0.99*R4*np.sin((gamma+0.5*(180.0-gamma))*np.pi/180),0.0,1.01*R4*np.cos((gamma+0.5*(180.0-gamma))*np.pi/180),1.01*R4*np.sin((gamma+0.5*(180.0-gamma))*np.pi/180),0.0,'FOURTHCIRCLE-RESTBOUNDED']]
    for setOfEdgesData in setsOfEdgesData:
        defineSetOfEdgesByClosestPoints(RVEpart,setOfEdgesData[0],setOfEdgesData[1],setOfEdgesData[2],setOfEdgesData[3],setOfEdgesData[4],setOfEdgesData[5],setOfEdgesData[-1],logfilepath,baselogindent + 4*logindent,True)

    RVEpart.SetByBoolean(name='FOURTHCIRCLE', sets=[RVEpart.sets['FOURTHCIRCLE-LOWERCRACK'],RVEpart.sets['FOURTHCIRCLE-UPPERCRACK'],RVEpart.sets['FOURTHCIRCLE-FIRSTBOUNDED'],RVEpart.sets['FOURTHCIRCLE-SECONDBOUNDED'],RVEpart.sets['FOURTHCIRCLE-RESTBOUNDED']])
    writeLineToLogFile(logfilepath,'a',baselogindent + 4*logindent + '-- FOURTHCIRCLE',True)

    if L>2*Rf:
        setsOfEdgesData = [[1.49*Rf*np.cos((theta+deltatheta)*np.pi/180),1.49*Rf*np.sin((theta+deltatheta)*np.pi/180),0.0,1.51*Rf*np.cos((theta+deltatheta)*np.pi/180),1.51*Rf*np.sin((theta+deltatheta)*np.pi/180),0.0,'FIFTHCIRCLE']]
    else:
        setsOfEdgesData = [[(Rf+0.49*(L-Rf))*np.cos((theta+deltatheta)*np.pi/180),(Rf+0.49*(L-Rf))*np.sin((theta+deltatheta)*np.pi/180),0.0,(Rf+0.51*(L-Rf))*np.cos((theta+deltatheta)*np.pi/180),(Rf+0.51*(L-Rf))*np.sin((theta+deltatheta)*np.pi/180),0.0,'FIFTHCIRCLE']]
    for setOfEdgesData in setsOfEdgesData:
        defineSetOfEdgesByClosestPoints(RVEpart,setOfEdgesData[0],setOfEdgesData[1],setOfEdgesData[2],setOfEdgesData[3],setOfEdgesData[4],setOfEdgesData[5],setOfEdgesData[-1],logfilepath,baselogindent + 4*logindent,True)

    setsOfEdgesData = [[0.85*Rf*np.cos(0.99*alpha*np.pi/180),0.85*Rf*np.sin(0.99*alpha*np.pi/180),0.0,0.85*Rf*np.cos(1.01*alpha*np.pi/180),0.85*Rf*np.sin(1.01*alpha*np.pi/180),0.0,'TRANSVERSALCUT-FIRSTFIBER'],
                       [1.05*Rf*np.cos(0.99*alpha*np.pi/180),1.05*Rf*np.sin(0.99*alpha*np.pi/180),0.0,1.05*Rf*np.cos(1.01*alpha*np.pi/180),1.05*Rf*np.sin(1.01*alpha*np.pi/180),0.0,'TRANSVERSALCUT-FIRSTMATRIX'],
                       [0.85*Rf*np.cos(0.99*(theta+deltatheta)*np.pi/180),0.85*Rf*np.sin(0.99*(theta+deltatheta)*np.pi/180),0.0,0.85*Rf*np.cos(1.01*(theta+deltatheta)*np.pi/180),0.85*Rf*np.sin(1.01*(theta+deltatheta)*np.pi/180),0.0,'TRANSVERSALCUT-SECONDFIBER'],
                       [1.05*Rf*np.cos(0.99*(theta+deltatheta)*np.pi/180),1.05*Rf*np.sin(0.99*(theta+deltatheta)*np.pi/180),0.0,1.05*Rf*np.cos(1.01*(theta+deltatheta)*np.pi/180),1.05*Rf*np.sin(1.01*(theta+deltatheta)*np.pi/180),0.0,'TRANSVERSALCUT-SECONDMATRIX'],
                       [0.85*Rf*np.cos(0.99*beta*np.pi/180),0.85*Rf*np.sin(0.99*beta*np.pi/180),0.0,0.85*Rf*np.cos(1.01*beta*np.pi/180),0.85*Rf*np.sin(1.01*beta*np.pi/180),0.0,'TRANSVERSALCUT-THIRDFIBER'],
                       [1.05*Rf*np.cos(0.99*beta*np.pi/180),1.05*Rf*np.sin(0.99*beta*np.pi/180),0.0,1.05*Rf*np.cos(1.01*beta*np.pi/180),1.05*Rf*np.sin(1.01*beta*np.pi/180),0.0,'TRANSVERSALCUT-THIRDMATRIX'],
                       [0.85*Rf*np.cos(0.99*gamma*np.pi/180),0.85*Rf*np.sin(0.99*gamma*np.pi/180),0.0,0.85*Rf*np.cos(1.01*gamma*np.pi/180),0.85*Rf*np.sin(1.01*gamma*np.pi/180),0.0,'TRANSVERSALCUT-FOURTHFIBER'],
                       [1.05*Rf*np.cos(0.99*gamma*np.pi/180),1.05*Rf*np.sin(0.99*gamma*np.pi/180),0.0,1.05*Rf*np.cos(1.01*gamma*np.pi/180),1.05*Rf*np.sin(1.01*gamma*np.pi/180),0.0,'TRANSVERSALCUT-FOURTHMATRIX']]
    for setOfEdgesData in setsOfEdgesData:
        defineSetOfEdgesByClosestPoints(RVEpart,setOfEdgesData[0],setOfEdgesData[1],setOfEdgesData[2],setOfEdgesData[3],setOfEdgesData[4],setOfEdgesData[5],setOfEdgesData[-1],logfilepath,baselogindent + 4*logindent,True)

    # sets of faces
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Sets of faces',True)

    setsOfFacesData = [[0.0, 0.25*Rf, 0,'FIBER-CENTER'],
                       [0.0, 0.65*Rf, 0,'FIBER-INTERMEDIATEANNULUS'],
                       [0.85*Rf*np.cos(0.5*alpha*np.pi/180), 0.85*Rf*np.sin(0.5*alpha*np.pi/180), 0,'FIBER-EXTANNULUS-LOWERCRACK'],
                       [0.85*Rf*np.cos((alpha+0.5*deltapsi)*np.pi/180), 0.85*Rf*np.sin((alpha+0.5*deltapsi)*np.pi/180), 0,'FIBER-EXTANNULUS-UPPERCRACK'],
                       [0.85*Rf*np.cos((theta+deltatheta+0.5*deltapsi)*np.pi/180), 0.85*Rf*np.sin((theta+deltatheta+0.5*deltapsi)*np.pi/180), 0,'FIBER-EXTANNULUS-FIRSTBOUNDED'],
                       [0.85*Rf*np.cos((beta+0.5*deltaphi)*np.pi/180), 0.85*Rf*np.sin((beta+0.5*deltaphi)*np.pi/180), 0,'FIBER-EXTANNULUS-SECONDBOUNDED'],
                       [0.85*Rf*np.cos((gamma+0.5*(180-gamma))*np.pi/180), 0.85*Rf*np.sin((gamma+0.5*(180-gamma))*np.pi/180), 0,'FIBER-EXTANNULUS-RESTBOUNDED']]

    for setOfFacesData in setsOfFacesData:
        defineSetOfFacesByFindAt(RVEpart,setOfFacesData[0],setOfFacesData[1],setOfFacesData[2],setOfFacesData[-1],logfilepath,baselogindent + 4*logindent,True)

    RVEpart.SetByBoolean(name='FIBER-EXTANNULUS', sets=[RVEpart.sets['FIBER-EXTANNULUS-LOWERCRACK'],RVEpart.sets['FIBER-EXTANNULUS-UPPERCRACK'],RVEpart.sets['FIBER-EXTANNULUS-FIRSTBOUNDED'],RVEpart.sets['FIBER-EXTANNULUS-SECONDBOUNDED'],RVEpart.sets['FIBER-EXTANNULUS-RESTBOUNDED']])
    writeLineToLogFile(logfilepath,'a',baselogindent + 4*logindent + '-- FIBER-EXTANNULUS',True)
    RVEpart.SetByBoolean(name='FIBER', sets=[RVEpart.sets['FIBER-CENTER'],RVEpart.sets['FIBER-INTERMEDIATEANNULUS'],RVEpart.sets['FIBER-EXTANNULUS']])
    writeLineToLogFile(logfilepath,'a',baselogindent + 4*logindent + '-- FIBER',True)

    if L>2*Rf:
        R1 = (1+0.5*0.25)*Rf
        R2 = (1.25+0.5*0.25)*Rf
    else:
        R1 = Rf+0.5*0.25*(L-Rf)
        R2 = Rf+1.5*0.25*(L-Rf)

    setsOfFacesData = [[R1*np.cos(0.5*alpha*np.pi/180), R1*np.sin(0.5*alpha*np.pi/180), 0,'MATRIX-INTANNULUS-LOWERCRACK'],
                       [R1*np.cos((alpha+0.5*deltapsi)*np.pi/180), R1*np.sin((alpha+0.5*deltapsi)*np.pi/180), 0,'MATRIX-INTANNULUS-UPPERCRACK'],
                       [R1*np.cos((theta+deltatheta+0.5*deltapsi)*np.pi/180), R1*np.sin((theta+deltatheta+0.5*deltapsi)*np.pi/180), 0,'MATRIX-INTANNULUS-FIRSTBOUNDED'],
                       [R1*np.cos((beta+0.5*deltaphi)*np.pi/180), R1*np.sin((beta+0.5*deltaphi)*np.pi/180), 0,'MATRIX-INTANNULUS-SECONDBOUNDED'],
                       [R1*np.cos((gamma+0.5*(180-gamma))*np.pi/180), R1*np.sin((gamma+0.5*(180-gamma))*np.pi/180), 0,'MATRIX-INTANNULUS-RESTBOUNDED']]

    for setOfFacesData in setsOfFacesData:
        defineSetOfFacesByFindAt(RVEpart,setOfFacesData[0],setOfFacesData[1],setOfFacesData[2],setOfFacesData[-1],logfilepath,baselogindent + 4*logindent,True)

    RVEpart.SetByBoolean(name='MATRIX-INTANNULUS', sets=[RVEpart.sets['MATRIX-INTANNULUS-LOWERCRACK'],RVEpart.sets['MATRIX-INTANNULUS-UPPERCRACK'],RVEpart.sets['MATRIX-INTANNULUS-FIRSTBOUNDED'],RVEpart.sets['MATRIX-INTANNULUS-SECONDBOUNDED'],RVEpart.sets['MATRIX-INTANNULUS-RESTBOUNDED']])
    writeLineToLogFile(logfilepath,'a',baselogindent + 4*logindent + '-- MATRIX-INTANNULUS',True)

    setsOfFacesData = [[0.0, R2, 0,'MATRIX-INTERMEDIATEANNULUS'],
                       [0.0, Rf+0.5*(L-Rf), 0,'MATRIX-BODY']]


    for setOfFacesData in setsOfFacesData:
        defineSetOfFacesByFindAt(RVEpart,setOfFacesData[0],setOfFacesData[1],setOfFacesData[2],setOfFacesData[-1],logfilepath,baselogindent + 4*logindent,True)

    RVEpart.SetByBoolean(name='MATRIX', sets=[RVEpart.sets['MATRIX-BODY'],RVEpart.sets['MATRIX-INTERMEDIATEANNULUS'],RVEpart.sets['MATRIX-INTANNULUS']])
    writeLineToLogFile(logfilepath,'a',baselogindent + 4*logindent + '-- MATRIX',True)

    RVEpart.SetByBoolean(name='RVE', sets=[RVEpart.sets['FIBER'],RVEpart.sets['MATRIX']])
    writeLineToLogFile(logfilepath,'a',baselogindent + 4*logindent + '-- RVE',True)

    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)

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
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'MATERIAL: ' + material['name'],True)
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
            writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '  ELASTIC',True)
            line = '    '
            for v,value in enumerate(values):
                if v>0:
                    line += ', '
                line += str(value)
            writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + line,True)
        except Exception, error:
            writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '  NO ELASTIC PROPERTY',True)
            #sys.exit(2)
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
            writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '  DENSITY',True)
            line = '    '
            for v,value in enumerate(values):
                if v>0:
                    line += ', '
                line += str(value)
            writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + line,True)
        except Exception, error:
            writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '  NO DENSITY PROPERTY',True)
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
            writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '  THERMAL EXPANSION',True)
            line = '    '
            for v,value in enumerate(values):
                if v>0:
                    line += ', '
                line += str(value)
            writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + line,True)
        except Exception, error:
            writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '  NO THERMAL EXPANSION PROPERTY',True)
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
            writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '  THERMAL CONDUCTIVITY',True)
            line = '    '
            for v,value in enumerate(values):
                if v>0:
                    line += ', '
                line += str(value)
            writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + line,True)
        except Exception, error:
            writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '  NO THERMAL CONDUCTIVITY PROPERTY',True)
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
            model.DisplacementBC(name=load['name'],createStepName='Load-Step',region=model.rootAssembly.instances['RVE-assembly'].sets[load['set']], u1=load['value'][0]*L, amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='',localCsys=None)
        elif 'applieddisplacement' in load['type'] or 'appliedDisplacement' in load['type'] or 'Applied Displacement' in load['type'] or 'applied displacement' in load['type']:
            model.DisplacementBC(name=load['name'],createStepName='Load-Step',region=model.rootAssembly.instances['RVE-assembly'].sets[load['set']], u1=load['value'][0], amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='',localCsys=None)
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
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Assigning mesh controls ...',True)

    regionSets = [['FIBER-EXTANNULUS-LOWERCRACK',QUAD,STRUCTURED],
                    ['FIBER-EXTANNULUS-UPPERCRACK',QUAD,STRUCTURED],
                    ['FIBER-EXTANNULUS-FIRSTBOUNDED',QUAD,STRUCTURED],
                    ['MATRIX-INTANNULUS-LOWERCRACK',QUAD,STRUCTURED],
                    ['MATRIX-INTANNULUS-UPPERCRACK',QUAD,STRUCTURED],
                    ['MATRIX-INTANNULUS-FIRSTBOUNDED',QUAD,STRUCTURED],
                    ['FIBER-CENTER',QUAD_DOMINATED,FREE],
                    ['FIBER-INTERMEDIATEANNULUS',QUAD_DOMINATED,FREE],
                    ['FIBER-EXTANNULUS-SECONDBOUNDED',QUAD,STRUCTURED],
                    ['FIBER-EXTANNULUS-RESTBOUNDED',QUAD,STRUCTURED],
                    ['MATRIX-INTANNULUS-SECONDBOUNDED',QUAD,STRUCTURED],
                    ['MATRIX-INTANNULUS-RESTBOUNDED',QUAD,STRUCTURED],
                    ['MATRIX-INTERMEDIATEANNULUS',QUAD_DOMINATED,FREE],
                    ['MATRIX-BODY',QUAD_DOMINATED,FREE]]

    for regionSet in regionSets:
        assignMeshControls(model,'RVE-assembly',regionSet[0],regionSet[1],regionSet[2],logfilepath,baselogindent + 3*logindent,True)

    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)

    # assign seeds
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Seeding edges ...',True)

    nTangential = np.floor(deltapsi/delta)
    nRadialFiber = np.floor(0.25/(delta*np.pi/180.0))
    nTangential1 = np.floor(deltaphi/parameters['mesh']['size']['delta2'])
    nTangential2 = np.floor((180-(theta+deltatheta+deltapsi+deltaphi))/parameters['mesh']['size']['delta3'])
    nTangential3 = np.floor(alpha/parameters['mesh']['size']['delta1'])
    #nRadialFiber1 = np.floor(0.25/parameters['mesh']['size']['delta3'])
    if L>2*Rf:
        nRadialMatrix = np.floor(0.25/(delta*np.pi/180.0))
        #nRadialMatrix1 = np.floor(0.25/parameters['mesh']['size']['delta3'])
    else:
        nRadialMatrix = np.floor(0.25*(L-Rf)/(delta*np.pi/180.0))
        #nRadialMatrix1 = np.floor(0.25*(L-Rf)/(Rf*parameters['mesh']['size']['delta3']))

    regionSets = [['SECONDCIRCLE-UPPERCRACK',nTangential],
                    ['SECONDCIRCLE-FIRSTBOUNDED',nTangential],
                    ['THIRDCIRCLE-UPPERCRACK',nTangential],
                    ['THIRDCIRCLE-FIRSTBOUNDED',nTangential],
                    ['FOURTHCIRCLE-UPPERCRACK',nTangential],
                    ['FOURTHCIRCLE-FIRSTBOUNDED',nTangential],
                    ['TRANSVERSALCUT-FIRSTFIBER',nRadialFiber],
                    ['TRANSVERSALCUT-FIRSTMATRIX',nRadialMatrix],
                    ['TRANSVERSALCUT-SECONDFIBER',nRadialFiber],
                    ['TRANSVERSALCUT-SECONDMATRIX',nRadialMatrix],
                    ['TRANSVERSALCUT-THIRDFIBER',nRadialFiber],
                    ['TRANSVERSALCUT-THIRDMATRIX',nRadialMatrix],
                    ['LOWERSIDE-SECONDRING-RIGHT',nRadialFiber],
                    ['LOWERSIDE-THIRDRING-RIGHT',nRadialMatrix],
                    ['LOWERSIDE-CENTER',6],
                    ['FIRSTCIRCLE',18],
                    ['SECONDCIRCLE-SECONDBOUNDED',nTangential1],
                    ['SECONDCIRCLE-RESTBOUNDED',nTangential2],
                    ['THIRDCIRCLE-SECONDBOUNDED',nTangential1],
                    ['THIRDCIRCLE-RESTBOUNDED',nTangential2],
                    ['FOURTHCIRCLE-SECONDBOUNDED',nTangential1],
                    ['FOURTHCIRCLE-RESTBOUNDED',nTangential2],
                    ['TRANSVERSALCUT-FOURTHFIBER',nRadialFiber],
                    ['TRANSVERSALCUT-FOURTHMATRIX',nRadialMatrix],
                    ['SECONDCIRCLE-LOWERCRACK',nTangential3],
                    ['THIRDCIRCLE-LOWERCRACK',nTangential3],
                    ['FOURTHCIRCLE-LOWERCRACK',nTangential3],
                    ['FIFTHCIRCLE',90],
                    ['RIGHTSIDE',30],
                    ['LEFTSIDE',30]]

    for regionSet in regionSets:
        seedEdgeByNumber(model,'RVE-assembly',regionSet[0],regionSet[1],FINER,logfilepath,baselogindent + 3*logindent,True)

    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)

    # select element type
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Selecting and assigning element types ...',True)

    if 'first' in parameters['mesh']['elements']['order']:
        elemType1 = mesh.ElemType(elemCode=CPE4, elemLibrary=STANDARD)
        elemType2 = mesh.ElemType(elemCode=CPE3, elemLibrary=STANDARD)
    elif 'second' in parameters['mesh']['elements']['order']:
        elemType1 = mesh.ElemType(elemCode=CPE8, elemLibrary=STANDARD)
        elemType2 = mesh.ElemType(elemCode=CPE6, elemLibrary=STANDARD)
    model.rootAssembly.setElementType(regions=(model.rootAssembly.instances['RVE-assembly'].sets['RVE']), elemTypes=(elemType1, elemType2))

    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)

    # mesh part
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Meshing part ...',True)
    localStart = timeit.default_timer()

    model.rootAssembly.generateMesh(regions=(model.rootAssembly.instances['RVE-assembly'],))

    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Mesh creation time: ' + str(timeit.default_timer() - localStart) + ' [s]',True)

    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)

    mdb.save()

    # extract mesh statistics
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Extracting mesh statistics ...',True)

    meshStats = model.rootAssembly.getMeshStats(regions=(model.rootAssembly.instances['RVE-assembly'],))

    modelData = {}
    modelData['numNodes'] =  meshStats.numNodes
    modelData['numQuads'] =  meshStats.numQuadElems
    modelData['numTris'] =  meshStats.numTriElems
    modelData['numEls'] =  meshStats.numQuadElems + meshStats.numTriElems

    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)

    mdb.save()

    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)

#===============================================================================#
#                                   Output
#===============================================================================#

    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Creating output requests ...',True)

    # field output
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Field output ...',True)

    model.FieldOutputRequest(name='F-Output-1',createStepName='Load-Step',variables=('U','RF','S','E','EE','COORD',))
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)

    # history output
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'History output ...',True)

    #model.HistoryOutputRequest(name='H-Output-1',createStepName='Load-Step')
    model.historyOutputRequests['H-Output-1'].setValues(contourIntegral='Debond',sectionPoints=DEFAULT,rebar=EXCLUDE,numberOfContours=parameters['Jintegral']['numberOfContours'])

    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)

    mdb.save()

    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)

#===============================================================================#
#                                Job creation
#===============================================================================#

    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Creating and submitting job ...',True)

    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Set job name',True)
    modelData['jobname'] = 'Job-Jintegral-' + modelname

    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Create job',True)
    mdb.Job(name='Job-Jintegral-' + modelname, model=modelname, description='', type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=99, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=ON, modelPrint=ON, contactPrint=ON, historyPrint=ON, userSubroutine='',scratch='', multiprocessingMode=DEFAULT, numCpus=parameters['solver']['cpus'], numDomains=12,numGPUs=0)

    mdb.save()

    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Submit job and wait for completion',True)
    localStart = timeit.default_timer()
    #mdb.jobs['Job-' + modelname].submit(consistencyChecking=OFF)
    mdb.jobs['Job-Jintegral-' + modelname].writeInput(consistencyChecking=OFF)
    mdb.jobs['Job-Jintegral-' + modelname].waitForCompletion()

    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Job time: ' + str(timeit.default_timer() - localStart) + ' [s]',True)

    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)

    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Closing database ...',True)
    mdb.save()
    mdb.close()

    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)

    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + 'Exiting function: createRVE(parameters,logfilepath,logindent)',True)

    return modelData

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
    modinpname = 'Job-VCCTandJintegral-' + parameters['input']['modelname'] + '.inp'
    modinpfullpath = join(parameters['input']['wd'],modinpname)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Working directory: ' + parameters['input']['wd'],True)
    #writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'ODB database name: ' + odbname,True)
    #writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'ODB database full path: ' + join(parameters['wd'],odbname),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Input file name: ' + inpname,True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Input file full path: ' + join(parameters['input']['wd'],inpname),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Modified input file name: ' + modinpname,True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Modified input file full path: ' + join(parameters['input']['wd'],modinpname),True)
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
            nodes[int(line.replace('\n','').split(',')[0])] = [float(line.replace('\n','').split(',')[1]),float(line.replace('\n','').split(',')[2])]
            #writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Stored node ' + str(int(line.replace('\n','').split(',')[0])) + ' with coordinates (' + str(float(line.replace('\n','').split(',')[1])) + ', ' + str(float(line.replace('\n','').split(',')[2])) + ')',True)
            #writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Node section ends at line ' + str(l),True)
            #writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'No more to go',True)
            store = False
            break
        elif store == True:
            nodes[int(line.replace('\n','').split(',')[0])] = [float(line.replace('\n','').split(',')[1]),float(line.replace('\n','').split(',')[2])]
            #writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Stored node ' + str(int(line.replace('\n','').split(',')[0])) + ' with coordinates (' + str(float(line.replace('\n','').split(',')[1])) + ', ' + str(float(line.replace('\n','').split(',')[2])) + ')',True)
        elif ('*Node' in line or '*NODE' in line) and len(inpfilelines[l+1].replace('\n','').split(','))==3:
            #writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Node section starts at line ' + str(l),True)
            store = True
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
            store = False
            break
        elif store == True:
            quadIndex = int(line.replace('\n','').split(',')[0])
            quads[quadIndex] = []
            for node in line.replace('\n','').split(',')[1:]:
                quads[quadIndex].append(int(node))
        elif ('*Element, type=CPE8' in line or '*ELEMENT, type=CPE8' in line or '*Element, type=CPE4' in line or '*ELEMENT, type=CPE4' in line) and (len(inpfilelines[l+1].replace('\n','').split(','))==5 or len(inpfilelines[l+1].replace('\n','').split(','))==9):
            store = True
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Reading crack tip set and saving to variable ...',True)
    for l,line in enumerate(inpfilelines):
        if ('*Nset' in line or '*NSET' in line) and line.replace('\n','').split(',')[1].split('=')[1] in ['CRACKTIP','cracktip']:
            cracktipIndex = int(inpfilelines[l+1].replace('\n','').split(',')[0])
            break
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Reading crack faces node set and saving to list ...',True)
    crackfacesNodeset = []
    store = False
    for l,line in enumerate(inpfilelines):
        if store == True and '*' in inpfilelines[l+1]:
            for index in line.replace('\n','').split(','):
                if index!='' and index!=' ':
                    crackfacesNodeset.append(int(index))
            store = False
            break
        elif store == True:
            for index in line.replace('\n','').split(','):
                if index!='' and index!=' ':
                    crackfacesNodeset.append(int(index))
        elif ('*Nset' in line or '*NSET' in line) and line.replace('\n','').split(',')[1].split('=')[1] in ['CRACK','crack']:
            store = True
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Reading crack faces element set and saving to list ...',True)
    crackfacesElementset = []
    store = False
    for l,line in enumerate(inpfilelines):
        if store == True and '*' in inpfilelines[l+1]:
            for index in line.replace('\n','').split(','):
                if index!='' and index!=' ':
                    crackfacesElementset.append(int(index))
            store = False
            break
        elif store == True:
            for index in line.replace('\n','').split(','):
                if index!='' and index!=' ':
                    crackfacesElementset.append(int(index))
        elif ('*Elset' in line or '*ELSET' in line) and line.replace('\n','').split(',')[1].split('=')[1] in ['CRACK','crack']:
            store = True
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Reading fiber node set and saving to list ...',True)
    fiberNodeset = []
    store = False
    for l,line in enumerate(inpfilelines):
        if store == True and '*' in inpfilelines[l+1]:
            for index in line.replace('\n','').split(','):
                if index!='' and index!=' ':
                    fiberNodeset.append(int(index))
            store = False
            break
        elif store == True:
            for index in line.replace('\n','').split(','):
                if index!='' and index!=' ':
                    fiberNodeset.append(int(index))
        elif ('*Nset' in line or '*NSET' in line) and line.replace('\n','').split(',')[1].split('=')[1] in ['FIBER','fiber']:
            store = True
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Reading matrix node set and saving to list ...',True)
    matrixNodeset = []
    store = False
    for l,line in enumerate(inpfilelines):
        if store == True and '*' in inpfilelines[l+1]:
            for index in line.replace('\n','').split(','):
                if index!='' and index!=' ':
                    matrixNodeset.append(int(index))
            store = False
            break
        elif store == True:
            for index in line.replace('\n','').split(','):
                if index!='' and index!=' ':
                    matrixNodeset.append(int(index))
        elif ('*Nset' in line or '*NSET' in line) and line.replace('\n','').split(',')[1].split('=')[1] in ['MATRIX','matrix']:
            store = True
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Reading fiber element set and saving to list ...',True)
    fiberElementset = []
    store = False
    for l,line in enumerate(inpfilelines):
        if store == True and '*' in inpfilelines[l+1]:
            for index in line.replace('\n','').split(','):
                if index!='' and index!=' ':
                    fiberElementset.append(int(index))
            store = False
            break
        elif store == True:
            for index in line.replace('\n','').split(','):
                if index!='' and index!=' ':
                    fiberElementset.append(int(index))
        elif ('*Elset' in line or '*ELSET' in line) and line.replace('\n','').split(',')[1].split('=')[1] in ['FIBER','fiber']:
            store = True
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Reading matrix element set and saving to list ...',True)
    matrixElementset = []
    store = False
    for l,line in enumerate(inpfilelines):
        if store == True and '*' in inpfilelines[l+1]:
            for index in line.replace('\n','').split(','):
                if index!='' and index!=' ':
                    matrixElementset.append(int(index))
            store = False
            break
        elif store == True:
            for index in line.replace('\n','').split(','):
                if index!='' and index!=' ':
                    matrixElementset.append(int(index))
        elif ('*Elset' in line or '*ELSET' in line) and line.replace('\n','').split(',')[1].split('=')[1] in ['MATRIX','matrix']:
            store = True
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Insert new coincident node(s) at the crack tip and create dummy node(s) ...',True)
    numNodes = mdbData['numNodes']
    numEls = mdbData['numEls']
    numQuads = mdbData['numQuads']
    numTris = mdbData['numTris']
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Total number of nodes = ' + str(numNodes),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Total number of elements = ' + str(numEls),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Total number of quadrilateral elements = ' + str(numQuads),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Total number of triangular elements = ' + str(numTris),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Index of current crack tip node: ' + str(cracktipIndex),True)
    matrixCracktipIndex = numNodes + 1000
    cracktipDummyIndex = numNodes + 1000 + 1
    nodes[matrixCracktipIndex] = [nodes[cracktipIndex][0],nodes[cracktipIndex][1]]
    nodes[cracktipDummyIndex] = [-5*parameters['geometry']['Rf'],-10*parameters['geometry']['Rf']]
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Creating matrix crack tip node with index ' + str(matrixCracktipIndex) + ' and coordinates (' + str(nodes[cracktipIndex][0]) + ', '+ str(nodes[cracktipIndex][1]) + ')',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Creating matrix dummy node with index ' + str(cracktipDummyIndex)+ ' and coordinates (' + str(-5*parameters['geometry']['Rf']) + ', '+ str(-10*parameters['geometry']['Rf']) + ')',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Searching for elements connected to the crack tip',True)
    fiberElswithCracktip = []
    matrixElswithCracktip = []
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Found',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '  On fiber',True)
    for element in fiberElementset:
        if element in quads.keys():
            if cracktipIndex in quads[element]:
                fiberElswithCracktip.append(element)
                if len(fiberElswithCracktip) == 2:
                    break
    for element in fiberElswithCracktip:
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '   - element ' + str(element),True)
    for element in matrixElementset:
        if element in quads.keys():
            if cracktipIndex in quads[element]:
                matrixElswithCracktip.append(element)
                if len(matrixElswithCracktip) == 2:
                    break
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '  On matrix',True)
    for element in matrixElswithCracktip:
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '   - element ' + str(element),True)
    if 'second' in parameters['mesh']['elements']['order']:
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Second order elements are used',True)
        matrixFirstBehindCracktipIndex = numNodes + 1000 + 2
        firstBehindCracktipDummyIndex = numNodes + 1000 + 3
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Creating matrix first behind crack tip node with index ' + str(matrixFirstBehindCracktipIndex),True)
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Creating matrix dummy node with index ' + str(firstBehindCracktipDummyIndex),True)
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Find common nodes of bounded crack tip elements on fiber and matrix',True)
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
                        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '   - node ' + str(node),True)
                if len(commonNodes)==3:
                    found = True
                    break
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Compute distances of bounded nodes from cracktip',True)
        distances = []
        for node in commonNodes:
            if node != cracktipIndex:
                distances.append(np.sqrt((nodes[node][0]-nodes[cracktipIndex][0])*(nodes[node][0]-nodes[cracktipIndex][0])+(nodes[node][1]-nodes[cracktipIndex][1])*(nodes[node][1]-nodes[cracktipIndex][1])))
            else:
                distances.append(0.0)
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Reordering labels based on distances',True)
        fiberFirstBehindCracktipIndex = commonNodes[np.argmax(distances)]
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Creating matrix crack tip node with index ' + str(matrixFirstBehindCracktipIndex) + ' and coordinates (' + str(nodes[fiberFirstBehindCracktipIndex][0]) + ', '+ str(nodes[fiberFirstBehindCracktipIndex][1]) + ')',True)
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Creating matrix dummy node with index ' + str(firstBehindCracktipDummyIndex)+ ' and coordinates (' + str(5*parameters['geometry']['Rf']) + ', '+ str(-10*parameters['geometry']['Rf']) + ')',True)
        nodes[matrixFirstBehindCracktipIndex] = [nodes[fiberFirstBehindCracktipIndex][0],nodes[fiberFirstBehindCracktipIndex][1]]
        nodes[firstBehindCracktipDummyIndex] = [5*parameters['geometry']['Rf'],-10*parameters['geometry']['Rf']]
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Identify nodes on crack faces for displacement measurements ...',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Find nodes belonging to the fiber elements around the crack tip',True)
    nodesAroundCracktip = []
    for element in fiberElswithCracktip:
        for node in quads[element]:
            nodesAroundCracktip.append(node)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Of these, identify the ones beloging to the crack surface',True)
    nodesFiberDisplacementMeas = []
    for node in crackfacesNodeset:
        if node in nodesAroundCracktip:
            nodesFiberDisplacementMeas.append(node)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Found ' + str(len(nodesFiberDisplacementMeas)) + ' nodes',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Compute distances of debonded nodes from cracktip',True)
    distancesFiberDisplacementMeas = []
    for node in nodesFiberDisplacementMeas:
        distancesFiberDisplacementMeas.append(np.sqrt((nodes[node][0]-nodes[cracktipIndex][0])*(nodes[node][0]-nodes[cracktipIndex][0])+(nodes[node][1]-nodes[cracktipIndex][1])*(nodes[node][1]-nodes[cracktipIndex][1])))
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Find nodes belonging to the matrix elements around the crack tip',True)
    nodesAroundCracktip = []
    for element in matrixElswithCracktip:
        for node in quads[element]:
            nodesAroundCracktip.append(node)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Of these, identify the ones beloging to the crack surface',True)
    nodesMatrixDisplacementMeas = []
    for node in crackfacesNodeset:
        if node in nodesAroundCracktip:
            nodesMatrixDisplacementMeas.append(node)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Found ' + str(len(nodesMatrixDisplacementMeas)) + ' nodes',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Compute distances of debonded nodes from cracktip',True)
    distancesMatrixDisplacementMeas = []
    for node in nodesMatrixDisplacementMeas:
        distancesMatrixDisplacementMeas.append(np.sqrt((nodes[node][0]-nodes[cracktipIndex][0])*(nodes[node][0]-nodes[cracktipIndex][0])+(nodes[node][1]-nodes[cracktipIndex][1])*(nodes[node][1]-nodes[cracktipIndex][1])))
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Sort lists with computed distances',True)
    sortedFiberDistanceIndeces = np.argsort(distancesFiberDisplacementMeas)
    sortedMatrixDistanceIndeces = np.argsort(distancesMatrixDisplacementMeas)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Indeces to sort fiber nodes ' + str(sortedFiberDistanceIndeces),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Indeces to sort matrix nodes ' + str(sortedMatrixDistanceIndeces),True)
    if 'second' in parameters['mesh']['elements']['order']:
        cracktipFiberDispMeasIndex = nodesFiberDisplacementMeas[sortedFiberDistanceIndeces[-1]]
        firstBehindCracktipFiberDispMeasIndex = nodesFiberDisplacementMeas[sortedFiberDistanceIndeces[-2]]
        cracktipMatrixDispMeasIndex = nodesMatrixDisplacementMeas[sortedMatrixDistanceIndeces[-1]]
        firstBehindCracktipMatrixDispMeasIndex = nodesMatrixDisplacementMeas[sortedMatrixDistanceIndeces[-2]]
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Displacement for the matrix crack tip is measured on node ' + str(cracktipMatrixDispMeasIndex),True)
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Displacement for the first bonded node behind the matrix crack tip is measured on node ' + str(firstBehindCracktipMatrixDispMeasIndex),True)
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Displacement for the fiber crack tip is measured on node ' + str(cracktipFiberDispMeasIndex),True)
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Displacement for the first bonded node behind the fiber crack tip is measured on node ' + str(firstBehindCracktipFiberDispMeasIndex),True)
    else:
        cracktipFiberDispMeasIndex = nodesFiberDisplacementMeas[sortedFiberDistanceIndeces[-1]]
        cracktipMatrixDispMeasIndex = nodesMatrixDisplacementMeas[sortedMatrixDistanceIndeces[-1]]
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Assign new crack tip nodes to matrix elements at crack tip ...',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Identify bonded and debonded elements around crack tip on fiber and matrix',True)
    found = False
    for fIndex,fiberEl in enumerate(fiberElswithCracktip):
        if found:
            break
        fiberElnodes = quads[fiberEl]
        for mIndex,matrixEl in enumerate(matrixElswithCracktip):
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
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Assign new crack tip index to the bonded element on the matrix',True)
    for n,node in enumerate(quads[firstboundedMatrixEl]):
        if node == cracktipIndex:
            quads[firstboundedMatrixEl][n] = matrixCracktipIndex
    if 'second' in parameters['mesh']['elements']['order']:
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Assign new first behind crack tip index to the bonded element on the matrix',True)
        for n,node in enumerate(quads[firstboundedMatrixEl]):
            if node == fiberFirstBehindCracktipIndex:
                quads[firstboundedMatrixEl][n] = matrixFirstBehindCracktipIndex
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Assign new crack tip index to the debonded element on the matrix',True)
    for n,node in enumerate(quads[firstdebondedMatrixEl]):
        if node == cracktipIndex:
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
        elif ('*Node' in line or '*NODE' in line) and len(inpfilelines[l+1].replace('\n','').split(',')) == 3:
            nodeSecStart = l
            started = True
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Node section begins at line ' + str(nodeSecStart) + ' and ends at line ' + str(nodeSecStop),True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Identify quadrilateral element section  ...',True)
    started = False
    for l,line in enumerate(inpfilelines):
        if started and '*' in line:
            elementSecStop = l-1
            break
        elif ('*Element, type=CPE8' in line or '*ELEMENT, type=CPE8' in line or '*Element, type=CPE4' in line or '*ELEMENT, type=CPE4' in line) and (len(inpfilelines[l+1].replace('\n','').split(','))==5 or len(inpfilelines[l+1].replace('\n','').split(','))==9):
            elementSecStart = l
            started = True
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Element section begins at line ' + str(elementSecStart) + ' and ends at line ' + str(elementSecStop),True)
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
                line += ', ' + str(coord)
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
                line += ', ' + str(node)
            inp.write(line + '\n')
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Write from original input file  ...',True)
    with open(modinpfullpath,'a') as inp:
        for line in inpfilelines[elementSecStop+1:endAssembly]:
            inp.write(line)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Write crack faces node and element sets ...',True)
    with open(modinpfullpath,'a') as inp:
        inp.write('*NSET, NSET=FIBER-CRACKFACE-NODES, INSTANCE=RVE-assembly' + '\n')
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
        inp.write('*NSET, NSET=MATRIX-CRACKFACE-NODES, INSTANCE=RVE-assembly' + '\n')
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
        inp.write('*ELSET, ELSET=FIBER-CRACKFACE-ELEMENTS, INSTANCE=RVE-assembly' + '\n')
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
        inp.write('*ELSET, ELSET=MATRIX-CRACKFACE-ELEMENTS, INSTANCE=RVE-assembly' + '\n')
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
        inp.write('*NSET, NSET=FIBER-CRACKTIP, INSTANCE=RVE-assembly' + '\n')
        inp.write(' ' + str(cracktipIndex) + '\n')
        inp.write('*NSET, NSET=MATRIX-CRACKTIP, INSTANCE=RVE-assembly' + '\n')
        inp.write(' ' + str(matrixCracktipIndex) + '\n')
        inp.write('*NSET, NSET=FIBER-CRACKTIP-DISPMEAS, INSTANCE=RVE-assembly' + '\n')
        inp.write(' ' + str(cracktipFiberDispMeasIndex) + '\n')
        inp.write('*NSET, NSET=MATRIX-CRACKTIP-DISPMEAS, INSTANCE=RVE-assembly' + '\n')
        inp.write(' ' + str(cracktipMatrixDispMeasIndex) + '\n')
        if 'second' in parameters['mesh']['elements']['order']:
            inp.write('*NSET, NSET=FIBER-NODE-FIRSTBOUNDED, INSTANCE=RVE-assembly' + '\n')
            inp.write(' ' + str(fiberFirstBehindCracktipIndex) + '\n')
            inp.write('*NSET, NSET=MATRIX-NODE-FIRSTBOUNDED, INSTANCE=RVE-assembly' + '\n')
            inp.write(' ' + str(matrixFirstBehindCracktipIndex) + '\n')
            inp.write('*NSET, NSET=FIBER-FIRSTBOUNDED-DISPMEAS, INSTANCE=RVE-assembly' + '\n')
            inp.write(' ' + str(firstBehindCracktipFiberDispMeasIndex) + '\n')
            inp.write('*NSET, NSET=MATRIX-FIRSTBOUNDED-DISPMEAS, INSTANCE=RVE-assembly' + '\n')
            inp.write(' ' + str(firstBehindCracktipMatrixDispMeasIndex) + '\n')
        inp.write('*NSET, NSET=CRACKTIP-DUMMY-NODE, INSTANCE=RVE-assembly' + '\n')
        inp.write(' ' + str(cracktipDummyIndex) + '\n')
        if 'second' in parameters['mesh']['elements']['order']:
            inp.write('*NSET, NSET=FIRSTBOUNDED-DUMMY-NODE, INSTANCE=RVE-assembly' + '\n')
            inp.write(' ' + str(firstBehindCracktipDummyIndex) + '\n')
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Write equation definitions ...',True)
    with open(modinpfullpath,'a') as inp:
        inp.write('*EQUATION' + '\n')
        inp.write(' 3' + '\n')
        inp.write(' FIBER-CRACKTIP,1,1,MATRIX-CRACKTIP,1,-1,CRACKTIP-DUMMY-NODE,1,-1' + '\n')
        inp.write(' 3' + '\n')
        inp.write(' FIBER-CRACKTIP,2,1,MATRIX-CRACKTIP,2,-1,CRACKTIP-DUMMY-NODE,2,-1' + '\n')
        if 'second' in parameters['mesh']['elements']['order']:
            inp.write(' 3' + '\n')
            inp.write(' FIBER-NODE-FIRSTBOUNDED,1,1,MATRIX-NODE-FIRSTBOUNDED,1,-1,FIRSTBOUNDED-DUMMY-NODE,1,-1' + '\n')
            inp.write(' 3' + '\n')
            inp.write(' FIBER-NODE-FIRSTBOUNDED,2,1,MATRIX-NODE-FIRSTBOUNDED,2,-1,FIRSTBOUNDED-DUMMY-NODE,2,-1' + '\n')
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Write surface definitions ...',True)
    with open(modinpfullpath,'a') as inp:
        inp.write('*SURFACE, NAME=FiberSurface, TYPE=ELEMENT' + '\n')
        inp.write(' FIBER-CRACKFACE-ELEMENTS' + '\n')
        inp.write('*SURFACE, NAME=MatrixSurface, TYPE=ELEMENT' + '\n')
        inp.write(' MATRIX-CRACKFACE-ELEMENTS' + '\n')
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
    return modinpname

def runRVEsimulation(wd,inpfile,logfilepath,baselogindent,logindent):
    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + 'In function: runRVEsimulation(wd,inpfile)',True)

    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Creating and submitting job ...',True)

    mdb.JobFromInputFile(name=inpfile.split('.')[0],inputFileName=inpfile,type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=99, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, userSubroutine='',scratch='', multiprocessingMode=DEFAULT, numCpus=12, numDomains=12,numGPUs=0)

    mdb.jobs[inpfile.split('.')[0]].submit(consistencyChecking=OFF)

    mdb.jobs[inpfile.split('.')[0]].waitForCompletion()

    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + 'Exiting function: runRVEsimulation(wd,inpfile,baselogindent,logindent)',True)

def analyzeRVEresults(odbname,parameters,logfilepath,baselogindent,logindent):

    skipLineToLogFile(logfilepath,'a',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + 'In function: analyzeRVEresults(wd,odbname)',True)

    wd = parameters['input']['wd']

    #=======================================================================
    # BEGIN - extract performances
    #=======================================================================
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Extract performances...',True)
    try:
        performances = getPerfs(wd,[odbname.split('.')[0]],logfilepath,baselogindent + 2*logindent,logindent)
    except Exception,e:
        writeErrorToLogFile(logfilepath,'a',Exception,e,True)
        sys.exc_clear()
    appendCSVfile(parameters['output']['global']['directory'],parameters['output']['global']['filenames']['performances'],[performances[1]])
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    #=======================================================================
    # END - extract performances
    #=======================================================================

    #=======================================================================
    # BEGIN - extract J-integral results
    #=======================================================================
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Extracting J-integral results ...',True)
    try:
        Jintegrals = getJintegrals(wd,odbname.split('.')[0],parameters['Jintegral']['numberOfContours'])
    except Exception,e:
        writeErrorToLogFile(logfilepath,'a',Exception,e,True)
        sys.exc_clear()
    JintegralsWithDistance = []
    for v,value in enumerate(Jintegrals):
        JintegralsWithDistance.append([v+1,(v+1)*parameters['geometry']['Rf']*parameters['mesh']['size']['delta']*np.pi/180.0,value])
    createCSVfile(parameters['output']['local']['directory'],parameters['output']['local']['filenames']['Jintegral'],'CONTOUR, AVERAGE DISTANCE, GTOT')
    appendCSVfile(parameters['output']['local']['directory'],parameters['output']['local']['filenames']['Jintegral'],JintegralsWithDistance)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    #=======================================================================
    # END - extract J-integral results
    #=======================================================================

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

    rightSide = getSingleNodeSet(odb,'RVE-ASSEMBLY','RIGHTSIDE')
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '-- RIGHTSIDE',True)

    fiberCrackfaceNodes = getSingleNodeSet(odb,None,'FIBER-CRACKFACE-NODES')
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '-- FIBER-CRACKFACE-NODES',True)

    matrixCrackfaceNodes = getSingleNodeSet(odb,None,'MATRIX-CRACKFACE-NODES')
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '-- MATRIX-CRACKFACE-NODES',True)

    fiberCracktip = getSingleNodeSet(odb,None,'FIBER-CRACKTIP')
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '-- FIBER-CRACKTIP',True)

    matrixCracktip = getSingleNodeSet(odb,None,'MATRIX-CRACKTIP')
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '-- MATRIX-CRACKTIP',True)

    cracktipDummyNode = getSingleNodeSet(odb,None,'CRACKTIP-DUMMY-NODE')
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '-- CRACKTIP-DUMMY-NODE',True)

    fiberCracktipDispMeas = getSingleNodeSet(odb,None,'FIBER-CRACKTIP-DISPMEAS')
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '-- FIBER-CRACKTIP-DISPMEAS',True)

    matrixCracktipDispMeas = getSingleNodeSet(odb,None,'MATRIX-CRACKTIP-DISPMEAS')
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '-- MATRIX-CRACKTIP-DISPMEAS',True)

    if 'second' in parameters['mesh']['elements']['order']:
        fiberFirstbounded = getSingleNodeSet(odb,None,'FIBER-NODE-FIRSTBOUNDED')
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '-- FIBER-NODE-FIRSTBOUNDED',True)

        matrixFirstbounded = getSingleNodeSet(odb,None,'MATRIX-NODE-FIRSTBOUNDED')
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '-- MATRIX-NODE-FIRSTBOUNDED',True)

        firstboundedDummyNode = getSingleNodeSet(odb,None,'FIRSTBOUNDED-DUMMY-NODE')
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '-- FIRSTBOUNDED-DUMMY-NODE',True)

        fiberFirstboundedDispMeas = getSingleNodeSet(odb,None,'FIBER-FIRSTBOUNDED-DISPMEAS')
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '-- FIBER-FIRSTBOUNDED-DISPMEAS',True)

        matrixFirstboundedDispMeas = getSingleNodeSet(odb,None,'MATRIX-FIRSTBOUNDED-DISPMEAS')
        writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '-- MATRIX-FIRSTBOUNDED-DISPMEAS',True)

    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    #=======================================================================
    # END - extract node sets
    #=======================================================================

    #=======================================================================
    # BEGIN - extract stresses at the boundary
    #=======================================================================
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Extracting stresses at the boundary ...',True)

    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Extract stresses along the right side ...',True)
    rightsideStress = getFieldOutput(odb,-1,-1,'S',rightSide,3)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)

    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Extract deformed coordinates along the right side ...',True)
    rightsideDefcoords = getFieldOutput(odb,-1,-1,'COORD',rightSide)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)

    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Extract undeformed coordinates along the right side ...',True)
    rightsideUndefcoords = getFieldOutput(odb,-1,0,'COORD',rightSide)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)

    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Pair data: x0, y0, x, y, sigma_xx, sigma_zz, sigma_yy, tau_xz ...',True)
    rightsideStressdata = []
    for value in rightsideUndefcoords.values:
        node = odb.rootAssembly.instances['RVE-ASSEMBLY'].getNodeFromLabel(value.nodeLabel)
        stress = getFieldOutput(odb,-1,-1,'S',node,3)
        defcoords = getFieldOutput(odb,-1,-1,'COORD',node)
        rightsideStressdata.append([value.data[0],value.data[1],defcoords.values[0].data[0],defcoords.values[0].data[1],stress.values[0].data[0],stress.values[0].data[1],stress.values[0].data[2],stress.values[0].data[3]])
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)

    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Compute minimum, maximum and mean stress ...',True)
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
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)

    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Save data to csv file ...',True)
    createCSVfile(parameters['output']['local']['directory'],parameters['output']['local']['filenames']['stressesatboundary'],'x0, y0, x, y, sigma_xx, sigma_zz, sigma_yy, tau_xz')
    appendCSVfile(parameters['output']['local']['directory'],parameters['output']['local']['filenames']['stressesatboundary'],rightsideStressdata)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)

    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    #=======================================================================
    # END - extract stresses at the boundary
    #=======================================================================

    #=======================================================================
    # BEGIN - compute G0
    #=======================================================================
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Compute G0...',True)
    G0 = np.pi*parameters['geometry']['Rf']*meanSigmaxx*meanSigmaxx*(1+(3.0-4.0*parameters['postproc']['nu-G0']))/(8.0*parameters['postproc']['G-G0'])
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    #=======================================================================
    # END - compute G0
    #=======================================================================

    #=======================================================================
    # BEGIN - compute reference frame transformation
    #=======================================================================
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Compute reference frame transformation ...',True)

    undefCracktipCoords = getFieldOutput(odb,-1,0,'COORD',fiberCracktip)
    phi = np.arctan2(undefCracktipCoords.values[0].data[1],undefCracktipCoords.values[0].data[0])

    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    #=======================================================================
    # END - compute reference frame transformation
    #=======================================================================

    #=======================================================================
    # BEGIN - compute contact zone
    #=======================================================================
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Compute contact zone ...',True)

    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Extract displacements on fiber ...',True)
    fiberCrackfaceDisps = getFieldOutput(odb,-1,-1,'U',fiberCrackfaceNodes)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)

    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Extract displacements on matrix ...',True)
    matrixCrackfaceDisps = getFieldOutput(odb,-1,-1,'U',matrixCrackfaceNodes)
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)

    fiberAngles = []
    matrixAngles = []
    fiberDisps = []
    matrixDisps = []

    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Rotate fiber displacements ...',True)
    for value in fiberCrackfaceDisps.values:
        if value.nodeLabel!=undefCracktipCoords.values[0].nodeLabel:
            node = odb.rootAssembly.instances['RVE-ASSEMBLY'].getNodeFromLabel(value.nodeLabel)
            undefCoords = getFieldOutput(odb,-1,0,'COORD',node)
            beta = np.arctan2(undefCoords.values[0].data[1],undefCoords.values[0].data[0])
            fiberAngles.append(beta)
            fiberDisps.append([np.cos(beta)*value.data[0]+np.sin(beta)*value.data[1],-np.sin(beta)*value.data[0]+np.cos(beta)*value.data[1]])
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)

    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Rotate matrix displacements ...',True)
    for value in matrixCrackfaceDisps.values:
        node = odb.rootAssembly.instances['RVE-ASSEMBLY'].getNodeFromLabel(value.nodeLabel)
        undefCoords = getFieldOutput(odb,-1,0,'COORD',node)
        beta = np.arctan2(undefCoords.values[0].data[1],undefCoords.values[0].data[0])
        matrixAngles.append(beta)
        matrixDisps.append([np.cos(beta)*value.data[0]+np.sin(beta)*value.data[1],-np.sin(beta)*value.data[0]+np.cos(beta)*value.data[1]])
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)

    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Sort fiber displacements ...',True)
    fiberDisps = np.array(fiberDisps)[np.argsort(fiberAngles)].tolist()
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)

    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Sort matrix displacements ...',True)
    matrixDisps = np.array(matrixDisps)[np.argsort(matrixAngles)].tolist()
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)

    crackDisps = []
    uR = []
    uTheta = []

    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Compute crack displacements ...',True)
    for s,dispset in enumerate(fiberDisps):
        crackDisps.append([matrixDisps[s][0]-dispset[0],matrixDisps[s][1]-dispset[1]])
        uR.append(matrixDisps[s][0]-dispset[0])
        uTheta.append(matrixDisps[s][1]-dispset[1])
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)

    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Compute contact zone size ...',True)
    phiCZ = 0.0
    for s,dispset in enumerate(crackDisps):
        if dispset[0]<1e-10:
            phiCZ = phi - fiberAngles[s]
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)

    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Save to file ...',True)
    createCSVfile(parameters['output']['local']['directory'],parameters['output']['local']['filenames']['crackdisplacements'],'beta, uR_fiber, uTheta_fiber, uR_matrix, uTheta_matrix, uR, uTheta')
    for s,dispset in enumerate(crackDisps):
        appendCSVfile(parameters['output']['local']['directory'],parameters['output']['local']['filenames']['crackdisplacements'],[[fiberAngles[s],fiberDisps[s][0],fiberDisps[s][1],matrixDisps[s][0],matrixDisps[s][1],dispset[0],dispset[1]]])
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)

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
    if 'second' in parameters['mesh']['elements']['order']:
        RFfirstbounded = getFieldOutput(odb,-1,-1,'RF',firstboundedDummyNode)
    fiberCracktipDisplacement = getFieldOutput(odb,-1,-1,'U',fiberCracktipDispMeas)
    matrixCracktipDisplacement = getFieldOutput(odb,-1,-1,'U',matrixCracktipDispMeas)
    if 'second' in parameters['mesh']['elements']['order']:
        fiberFirstboundedDisplacement = getFieldOutput(odb,-1,-1,'U',fiberFirstboundedDispMeas)
        matrixFirstboundedDisplacement = getFieldOutput(odb,-1,-1,'U',matrixFirstboundedDispMeas)

    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)

    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Rotate forces and displacements ...',True)

    xRFcracktip = RFcracktip.values[0].data[0]
    yRFcracktip = RFcracktip.values[0].data[1]
    rRFcracktip = np.cos(phi)*xRFcracktip + np.sin(phi)*yRFcracktip
    thetaRFcracktip = -np.sin(phi)*xRFcracktip + np.cos(phi)*yRFcracktip
    if 'second' in parameters['mesh']['elements']['order']:
        xRFfirstbounded = RFfirstbounded.values[0].data[0]
        yRFfirstbounded = RFfirstbounded.values[0].data[1]
        rRFfirstbounded = np.cos(phi)*xRFfirstbounded + np.sin(phi)*yRFfirstbounded
        thetaRFfirstbounded = -np.sin(phi)*xRFfirstbounded + np.cos(phi)*yRFfirstbounded

    xfiberCracktipDisplacement = fiberCracktipDisplacement.values[0].data[0]
    yfiberCracktipDisplacement = fiberCracktipDisplacement.values[0].data[1]
    rfiberCracktipDisplacement = np.cos(phi)*xfiberCracktipDisplacement + np.sin(phi)*yfiberCracktipDisplacement
    thetafiberCracktipDisplacement = -np.sin(phi)*xfiberCracktipDisplacement + np.cos(phi)*yfiberCracktipDisplacement
    xmatrixCracktipDisplacement = matrixCracktipDisplacement.values[0].data[0]
    ymatrixCracktipDisplacement = matrixCracktipDisplacement.values[0].data[1]
    rmatrixCracktipDisplacement = np.cos(phi)*xmatrixCracktipDisplacement + np.sin(phi)*ymatrixCracktipDisplacement
    thetamatrixCracktipDisplacement = -np.sin(phi)*xmatrixCracktipDisplacement + np.cos(phi)*ymatrixCracktipDisplacement
    if 'second' in parameters['mesh']['elements']['order']:
        xfiberFirstboundedDisplacement = fiberFirstboundedDisplacement.values[0].data[0]
        yfiberFirstboundedDisplacement = fiberFirstboundedDisplacement.values[0].data[1]
        rfiberFirstboundedDisplacement = np.cos(phi)*xfiberFirstboundedDisplacement + np.sin(phi)*yfiberFirstboundedDisplacement
        thetafiberFirstboundedDisplacement = -np.sin(phi)*xfiberFirstboundedDisplacement + np.cos(phi)*yfiberFirstboundedDisplacement
        xmatrixFirstboundedDisplacement = matrixFirstboundedDisplacement.values[0].data[0]
        ymatrixFirstboundedDisplacement = matrixFirstboundedDisplacement.values[0].data[1]
        rmatrixFirstboundedDisplacement = np.cos(phi)*xmatrixFirstboundedDisplacement + np.sin(phi)*ymatrixFirstboundedDisplacement
        thetamatrixFirstboundedDisplacement = -np.sin(phi)*xmatrixFirstboundedDisplacement + np.cos(phi)*ymatrixFirstboundedDisplacement

    xcracktipDisplacement = xmatrixCracktipDisplacement - xfiberCracktipDisplacement
    ycracktipDisplacement = ymatrixCracktipDisplacement - yfiberCracktipDisplacement
    rcracktipDisplacement = rmatrixCracktipDisplacement - rfiberCracktipDisplacement
    thetacracktipDisplacement = thetamatrixCracktipDisplacement - thetafiberCracktipDisplacement
    if 'second' in parameters['mesh']['elements']['order']:
        xfirstboundedDisplacement = xmatrixFirstboundedDisplacement - xfiberFirstboundedDisplacement
        yfirstboundedDisplacement = ymatrixFirstboundedDisplacement - yfiberFirstboundedDisplacement
        rfirstboundedDisplacement = rmatrixFirstboundedDisplacement - rfiberFirstboundedDisplacement
        thetafirstboundedDisplacement = thetamatrixFirstboundedDisplacement - thetafiberFirstboundedDisplacement

    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)

    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Compute VCCT with GTOT=GI+GII ...',True)

    if 'second' in parameters['mesh']['elements']['order']:
        GI = np.abs(0.5*(rRFcracktip*rcracktipDisplacement+rRFfirstbounded*rfirstboundedDisplacement)/(parameters['geometry']['Rf']*parameters['mesh']['size']['delta']*np.pi/180.0))
        GII = np.abs(0.5*(thetaRFcracktip*thetacracktipDisplacement+thetaRFfirstbounded*thetafirstboundedDisplacement)/(parameters['geometry']['Rf']*parameters['mesh']['size']['delta']*np.pi/180.0))
        GTOTequiv = np.abs(0.5*(xRFcracktip*xcracktipDisplacement+yRFcracktip*ycracktipDisplacement+xRFfirstbounded*xfirstboundedDisplacement+yRFfirstbounded*yfirstboundedDisplacement)/(parameters['geometry']['Rf']*parameters['mesh']['size']['delta']*np.pi/180.0))
    else:
        GI = np.abs(0.5*(rRFcracktip*rcracktipDisplacement)/(parameters['geometry']['Rf']*parameters['mesh']['size']['delta']*np.pi/180.0))
        GII = np.abs(0.5*(thetaRFcracktip*thetacracktipDisplacement)/(parameters['geometry']['Rf']*parameters['mesh']['size']['delta']*np.pi/180.0))
        GTOTequiv = np.abs(0.5*(xRFcracktip*xcracktipDisplacement+yRFcracktip*ycracktipDisplacement)/(parameters['geometry']['Rf']*parameters['mesh']['size']['delta']*np.pi/180.0))

    GTOT = GI + GII

    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)

    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Compute VCCT with GI=GTOT-GII ...',True)

    if 'second' in parameters['mesh']['elements']['order']:
        GIIv2 = np.abs(0.5*(thetaRFcracktip*thetacracktipDisplacement+thetaRFfirstbounded*thetafirstboundedDisplacement)/(parameters['geometry']['Rf']*parameters['mesh']['size']['delta']*np.pi/180.0))
    else:
        GIIv2 = np.abs(0.5*(thetaRFcracktip*thetacracktipDisplacement)/(parameters['geometry']['Rf']*parameters['mesh']['size']['delta']*np.pi/180.0))

    GTOTv2 = Jintegrals[-1]

    GIv2 = GTOTv2 - GIIv2

    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)

    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + 'Save to file ...',True)
    if 'second' in parameters['mesh']['elements']['order']:
        appendCSVfile(parameters['output']['global']['directory'],parameters['output']['global']['filenames']['energyreleaserate'],[[parameters['geometry']['deltatheta'],parameters['geometry']['Rf'],parameters['geometry']['L'],parameters['geometry']['L']/parameters['geometry']['Rf'],phiCZ,G0,GI/G0,GII/G0,GTOT/G0,GIv2/G0,GIIv2/G0,GTOTv2/G0,GTOTequiv/G0,GI,GII,GTOT,GIv2,GIIv2,GTOTv2,GTOTequiv,np.min(uR),np.max(uR),np.mean(uR),np.min(uTheta),np.max(uTheta),np.mean(uTheta),xRFcracktip,yRFcracktip,xRFfirstbounded,yRFfirstbounded,rRFcracktip,thetaRFcracktip,rRFfirstbounded,thetaRFfirstbounded,xcracktipDisplacement,ycracktipDisplacement,rcracktipDisplacement,thetacracktipDisplacement,xfirstboundedDisplacement,yfirstboundedDisplacement,rfirstboundedDisplacement,thetafirstboundedDisplacement,xfiberCracktipDisplacement,yfiberCracktipDisplacement,rfiberCracktipDisplacement,thetafiberCracktipDisplacement,xfiberFirstboundedDisplacement,yfiberFirstboundedDisplacement,rfiberFirstboundedDisplacement,thetafiberFirstboundedDisplacement,xmatrixCracktipDisplacement,ymatrixCracktipDisplacement,rmatrixCracktipDisplacement,thetamatrixCracktipDisplacement,xmatrixFirstboundedDisplacement,ymatrixFirstboundedDisplacement,rmatrixFirstboundedDisplacement,thetamatrixFirstboundedDisplacement]])
    else:
        appendCSVfile(parameters['output']['global']['directory'],parameters['output']['global']['filenames']['energyreleaserate'],[[parameters['geometry']['deltatheta'],parameters['geometry']['Rf'],parameters['geometry']['L'],parameters['geometry']['L']/parameters['geometry']['Rf'],phiCZ,G0,GI/G0,GII/G0,GTOT/G0,GIv2/G0,GIIv2/G0,GTOTv2/G0,GTOTequiv/G0,GI,GII,GTOT,GIv2,GIIv2,GTOTv2,GTOTequiv,np.min(uR),np.max(uR),np.mean(uR),np.min(uTheta),np.max(uTheta),np.mean(uTheta),xRFcracktip,yRFcracktip,rRFcracktip,thetaRFcracktip,xcracktipDisplacement,ycracktipDisplacement,rcracktipDisplacement,thetacracktipDisplacement,xfiberCracktipDisplacement,yfiberCracktipDisplacement,rfiberCracktipDisplacement,thetafiberCracktipDisplacement,xmatrixCracktipDisplacement,ymatrixCracktipDisplacement,rmatrixCracktipDisplacement,thetamatrixCracktipDisplacement]])
    writeLineToLogFile(logfilepath,'a',baselogindent + 3*logindent + '... done.',True)

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

    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + 'Exiting function: analyzeRVEresults(wd,odbname,parameters)',True)



def main(argv):

    debug = True

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
                               'elastic':{'type':ISOTROPIC,
                                           'values':[70e3,0.2]}},
                               {'name':'epoxy',
                               'elastic':{'type':ISOTROPIC,
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
    RVEparams['postproc'] = {'nu-G0':RVEparams['materials'][1]['elastic']['values'][1],
                              'G-G0':0.5*RVEparams['materials'][1]['elastic']['values'][0]/(1+RVEparams['materials'][1]['elastic']['values'][1])}
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
                                    'offsetType':MIDDLE_SURFACE,
                                    'offsetField':'',
                                    'thicknessAssignment':FROM_SECTION,
                                    'offsetValue':0.0},
                                    {'name':'matrixSection',
                                    'set':'MATRIX',
                                    'offsetType':MIDDLE_SURFACE,
                                    'offsetField':'',
                                    'thicknessAssignment':FROM_SECTION,
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
    RVEparams['mesh'] = {'size':{'deltapsi':'',
                                 'deltaphi':'',
                                 'delta':0.05,
                                 'delta1':0.1,
                                 'delta2':0.5,
                                 'delta3':1.0},
                         'elements':{'minElNum':10,
                                     'order':'second'}}
    RVEparams['Jintegral'] = {'numberOfContours':50}
    RVEparams['output'] = {'global':{'directory':'D:/OneDrive/01_Luca/07_DocMASE/07_Data/03_FEM/caePythonTest',
                                     'filenames':{'performances':'caePythonTest-performances',
                                                  'energyreleaserate':'caePythonTest-energyreleaserates',
                                                  'inputdata':'caePythonTest-inputdata'}},
                           'local':{'directory':'D:/OneDrive/01_Luca/07_DocMASE/07_Data/03_FEM/caePythonTest',
                                     'filenames':{'Jintegral':'',
                                                  'stressesatboundary':'',
                                                  'crackdisplacements':''}},
                           'report':{'global':{'directory':'D:/OneDrive/01_Luca/07_DocMASE/07_Data/03_FEM/caePythonTest',
                                                'filename':'caePythonTest-report'},
                                     'local':{'directory':[],
                                               'filenames':{'Jintegral':[],
                                                            'stressesatboundary':[],
                                                            'crackdisplacements':[]}}},
                           'sql':{'global':{'directory':'D:/OneDrive/01_Luca/07_DocMASE/07_Data/03_FEM/caePythonTest',
                                            'filename':'caePythonTestDB'}}
                          }
    RVEparams['solver'] = {'cpus':12}

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
        iterationsSets.append([value1,value2,value3,value4])

    #=======================================================================
    # END - ITERABLES
    #=======================================================================

    #=======================================================================
    # BEGIN - ANALYSIS
    #=======================================================================

    workDir = RVEparams['input']['wd']

    logfilename = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '_ABQ-RVE-generation-and-analysis' + '.log'
    logfilefullpath = join(workDir,logfilename)
    logindent = '    '

    if not os.path.exists(RVEparams['output']['global']['directory']):
            os.mkdir(RVEparams['output']['global']['directory'])

    with open(logfilefullpath,'w') as log:
        log.write('Automatic generation and FEM analysis of RVEs with Abaqus Python' + '\n')

    createCSVfile(RVEparams['output']['global']['directory'],logfilename.split('.')[0] + '_TIME','ITERATION PARAMETER VALUE, T(createRVE()) [s], T(modifyRVEinputfile()) [s], T(runRVEsimulation()) [s], T(analyzeRVEresults()) [s],TOTAL TIME FOR ITERATION [s]')

    createCSVfile(RVEparams['output']['global']['directory'],RVEparams['output']['global']['filenames']['inputdata'],'Rf [um],L [um],L/Rf [-],Vff [-],BC,applied strain [-],fiber,matrix')
    appendCSVfile(RVEparams['output']['global']['directory'],RVEparams['output']['global']['filenames']['inputdata'],[[RVEparams['geometry']['Rf'],RVEparams['geometry']['L'],RVEparams['geometry']['L']/RVEparams['geometry']['Rf'],(4*RVEparams['geometry']['L']*RVEparams['geometry']['L'])/(RVEparams['geometry']['Rf']*RVEparams['geometry']['Rf']*np.pi),
                                                                                                                      'FREE',RVEparams['loads'][0]['value'][0],RVEparams['sections'][0]['material'],RVEparams['sections'][1]['material']]])


    createCSVfile(RVEparams['output']['global']['directory'],logfilename.split('.')[0] + '_csvfileslist','ABSOLUTE PATH, NAME, TO PLOT, PLOT VARIABLES')
    appendCSVfile(RVEparams['output']['global']['directory'],logfilename.split('.')[0] + '_csvfileslist',[[join(RVEparams['output']['global']['directory'],RVEparams['output']['global']['filenames']['inputdata']+'.csv'),'MODEL-DATA','False','[]']])
    appendCSVfile(RVEparams['output']['global']['directory'],logfilename.split('.')[0] + '_csvfileslist',[[join(RVEparams['output']['global']['directory'],RVEparams['output']['global']['filenames']['energyreleaserate']+'.csv'),'GLOBAL-ERRTS','True','[[[0,6,"GI(VCCT)"],[0,7,"GII(VCCT)"],[0,8,"GI+GII(VCCT)"],"Debond size [deg]","Normalized energy release rate [-]","Normalized energy release rates from VCCT"],' \
                                                                                                                                                                                                                                                          '[[0,9,"Jint(50)-GII(VCCT)"],[0,10,"GII(VCCT)"],[0,11,"Jint(50)"],"Debond size [deg]","Normalized energy release rate [-]","Normalized energy release rates from mixed VCCT/J-integral approach"],' \
                                                                                                                                                                                                                                                          '[[0,8,"GI+GII(VCCT)"],[0,11,"Jint(50)"],[0,12,"GTOTequiv(XY)"],"Debond size [deg]","Total normalized energy release rate [-]","Total normalized energy release rates from VCCT, J-integral and VCCT in in non-rotated frame"],' \
                                                                                                                                                                                                                                                          '[[0,6,"GI(VCCT)"],[0,9,"Jint(50)-GII(VCCT)"],"Debond size [deg]","Mode I energy release rate [-]","Mode I normalized energy release rate"],' \
                                                                                                                                                                                                                                                          '[[0,20,"min(uR)"],[0,21,"max(uR)"],[0,22,"mean(uR)"],"Debond size [deg]","Radial displacement [um]","Minimum, maximum and mean radial displacement"],' \
                                                                                                                                                                                                                                                          '[[0,23,"min(uTheta)"],[0,24,"max(uTheta)"],[0,25,"mean(uTheta)"],"Debond size [deg]","Tangential displacement [um]","Minimum, maximum and mean tangential displacement"],' \
                                                                                                                                                                                                                                                          '[[0,20,"min(uR)"],[0,23,"min(uTheta)"],"Debond size [deg]","Minimum displacement [um]","Minimum radial and tangential displacement"],' \
                                                                                                                                                                                                                                                          '[[0,21,"max(uR)"],[0,24,"max(uTheta)"],"Debond size [deg]","Maximum displacement [um]","Maximum radial and tangential displacement"],' \
                                                                                                                                                                                                                                                          '[[0,22,"mean(uR)"],[0,25,"mean(uTheta)"],"Debond size [deg]","Mean displacement [um]","Mean radial and tangential displacement"],' \
                                                                                                                                                                                                                                                          '[[0,4,"Contact zone size"],"Debond size [deg]","Contact zone size [deg]","Contact zone size"]]']])
    appendCSVfile(RVEparams['output']['global']['directory'],logfilename.split('.')[0] + '_csvfileslist',[[join(RVEparams['output']['global']['directory'],logfilename.split('.')[0] + '_TIME'+'.csv'),'GLOBAL-TIME','True','[[[0,1,"createRVE()"],[0,2,"modifyRVEinputfile()"],[0,3,"runRVEsimulationRVE()"],[0,4,"analyzeRVEresults()"],[0,5,"TOTAL TIME"],"Debond size [deg]","Time [s]","Pipeline execution time [s]"]]']])
    appendCSVfile(RVEparams['output']['global']['directory'],logfilename.split('.')[0] + '_csvfileslist',[[join(RVEparams['output']['global']['directory'],RVEparams['output']['global']['filenames']['performances']+'.csv'),'GLOBAL-ABQperformances','True','[[[14,2,"User time [s]"],[0,3,"System time [s]"],[14,5,"Total cpu time [s]"],[14,6,"Wallclock time [s]"],"Number of elements [-]","Time [s]","ABAQUS Simulation Time"],' \
                                                                                                                                                                                                                                                               '[[14,4,"User time/total cpu time [s]"],[14,5,"System time/Total cpu time [s]"],[14,9,"Wallclock time/Total cpu time [s]"],"Number of elements [-]","Normalized time [-]","ABAQUS Normalized Simulation Time"]]']])

    skipLineToLogFile(logfilefullpath,'a',True)
    writeLineToLogFile(logfilefullpath,'a','In function: main(argv)',True)

    skipLineToLogFile(logfilefullpath,'a',True)
    writeLineToLogFile(logfilefullpath,'a',logindent + 'Global timer starts',True)
    globalStart = timeit.default_timer()

    for set in iterationsSets:

        timedataList = []
        totalIterationTime = 0.0

        RVEparams['input']['modelname'] = set[0]
        RVEparams['geometry']['deltatheta'] = set[1]
        RVEparams['mesh']['size']['deltapsi'] = set[2]
        RVEparams['mesh']['size']['deltaphi'] = set[3]

        RVEparams['output']['local']['directory'] = join(RVEparams['output']['global']['directory'],set[0])
        RVEparams['output']['local']['filenames']['Jintegral'] = set[0] + '-Jintegral'
        RVEparams['output']['local']['filenames']['stressesatboundary'] = set[0] + '-stressesatboundary'
        RVEparams['output']['local']['filenames']['crackdisplacements'] = set[0] + '-crackdisplacements'

        RVEparams['output']['report']['local']['directory'].append(join(RVEparams['output']['global']['directory'],set[0]))
        RVEparams['output']['report']['local']['filenames']['Jintegral'].append(set[0] + '-Jintegral')
        RVEparams['output']['report']['local']['filenames']['stressesatboundary'].append(set[0] + '-stressesatboundary')
        RVEparams['output']['report']['local']['filenames']['crackdisplacements'].append(set[0] + '-crackdisplacements')

        appendCSVfile(RVEparams['output']['global']['directory'],logfilename.split('.')[0] + '_csvfileslist',[[join(RVEparams['output']['local']['directory'],RVEparams['output']['local']['filenames']['Jintegral']+'.csv'),'Jintegral-Param='+str(set[1]),'True','[[[1,2,"J-integral"],"Average distance [um]","GTOT [J/m^2]","GTOT from J-integral"]]']])
        appendCSVfile(RVEparams['output']['global']['directory'],logfilename.split('.')[0] + '_csvfileslist',[[join(RVEparams['output']['local']['directory'],RVEparams['output']['local']['filenames']['stressesatboundary']+'.csv'),'StressAtBoundary-Param='+str(set[1]),'True','[[[1,4,"sigma_xx"],"z [um]","Axial stress [MPa]","Stress along the right boundary"]]']])
        appendCSVfile(RVEparams['output']['global']['directory'],logfilename.split('.')[0] + '_csvfileslist',[[join(RVEparams['output']['local']['directory'],RVEparams['output']['local']['filenames']['crackdisplacements']+'.csv'),'CrackDisps-Param='+str(set[1]),'True','[[[0,5,"Radial"],[0,6,"Tangential"],"Angle [deg]","Displacement [um]","Crack faces displacements"],' \
                                                                                                                                                                                                                                                                              '[[0,1,"Radial"],[0,2,"Tangential"],"Angle [deg]","Displacement [um]","Fiber crack faces displacements"],' \
                                                                                                                                                                                                                                                                              '[[0,3,"Radial"],[0,4,"Tangential"],"Angle [deg]","Displacement [um]","Matrix crack faces displacements"]]']])

        timedataList.append(set[1])

        if not os.path.exists(RVEparams['output']['local']['directory']):
                os.mkdir(RVEparams['output']['local']['directory'])

        #================= create ABAQUS CAE model
        skipLineToLogFile(logfilefullpath,'a',True)
        writeLineToLogFile(logfilefullpath,'a',logindent + 'Calling function: createRVE(parameters,logfilepath,baselogindent,logindent)',True)
        writeLineToLogFile(logfilefullpath,'a',logindent + 'Local timer starts',True)
        localStart = timeit.default_timer()
        try:
            modelData = createRVE(RVEparams,logfilefullpath,logindent,logindent)
            localElapsedTime = timeit.default_timer() - localStart
            timedataList.append(localElapsedTime)
            totalIterationTime += localElapsedTime
            writeLineToLogFile(logfilefullpath,'a',logindent + 'Successfully returned from function: createRVE(parameters,logfilepath,baselogindent,logindent)',True)
            writeLineToLogFile(logfilefullpath,'a',logindent + 'Local timer stopped',True)
            writeLineToLogFile(logfilefullpath,'a',logindent + 'Elapsed time: ' + str(localElapsedTime) + ' [s]',True)
        except Exception, error:
            writeErrorToLogFile(logfilefullpath,'a',Exception,error,True)
            sys.exit(2)

        #================= modify input file
        skipLineToLogFile(logfilefullpath,'a',True)
        writeLineToLogFile(logfilefullpath,'a',logindent + 'Calling function: modifyRVEinputfile(parameters,mdbData,logfilepath,baselogindent,logindent)',True)
        writeLineToLogFile(logfilefullpath,'a',logindent + 'Local timer starts',True)
        localStart = timeit.default_timer()
        try:
            inputfilename = modifyRVEinputfile(RVEparams,modelData,logfilefullpath,logindent,logindent)
            localElapsedTime = timeit.default_timer() - localStart
            timedataList.append(localElapsedTime)
            totalIterationTime += localElapsedTime
            writeLineToLogFile(logfilefullpath,'a',logindent + 'Successfully returned from function: modifyRVEinputfile(parameters,mdbData,logfilepath,baselogindent,logindent)',True)
            writeLineToLogFile(logfilefullpath,'a',logindent + 'Local timer stopped',True)
            writeLineToLogFile(logfilefullpath,'a',logindent + 'Elapsed time: ' + str(localElapsedTime) + ' [s]',True)
        except Exception, error:
            writeErrorToLogFile(logfilefullpath,'a',Exception,error,True)
            sys.exit(2)

        #================= run ABAQUS simulation
        skipLineToLogFile(logfilefullpath,'a',True)
        writeLineToLogFile(logfilefullpath,'a',logindent + 'Calling function: runRVEsimulation(wd,inpfile,logfilepath,baselogindent,logindent)',True)
        writeLineToLogFile(logfilefullpath,'a',logindent + 'Local timer starts',True)
        localStart = timeit.default_timer()
        try:
            runRVEsimulation(RVEparams['input']['wd'],inputfilename,logfilefullpath,logindent,logindent)
            localElapsedTime = timeit.default_timer() - localStart
            timedataList.append(localElapsedTime)
            totalIterationTime += localElapsedTime
            writeLineToLogFile(logfilefullpath,'a',logindent + 'Successfully returned from function: runRVEsimulation(wd,inpfile,logfilepath,baselogindent,logindent)',True)
            writeLineToLogFile(logfilefullpath,'a',logindent + 'Local timer stopped',True)
            writeLineToLogFile(logfilefullpath,'a',logindent + 'Elapsed time: ' + str(localElapsedTime) + ' [s]',True)
        except Exception, error:
            writeErrorToLogFile(logfilefullpath,'a',Exception,error,True)
            sys.exit(2)
        #inputfilename = 'Job-VCCTandJintegral-RVE100-Half-SmallDisplacement-Free-10' + '.inp'

        #================= extract and analyze data from ODB
        skipLineToLogFile(logfilefullpath,'a',True)
        writeLineToLogFile(logfilefullpath,'a',logindent + 'Calling function: analyzeRVEresults(wd,odbname,logfilepath,parameters)',True)
        writeLineToLogFile(logfilefullpath,'a',logindent + 'Local timer starts',True)
        localStart = timeit.default_timer()
        try:
            createCSVfile(RVEparams['output']['global']['directory'],RVEparams['output']['global']['filenames']['performances'],'PROJECT NAME, NUMBER OF CPUS [-], USER TIME [s], SYSTEM TIME [s], USER TIME/TOTAL CPU TIME [%], SYSTEM TIME/TOTAL CPU TIME [%], TOTAL CPU TIME [s], WALLCLOCK TIME [s], WALLCLOCK TIME [m], WALLCLOCK TIME [h], WALLCLOCK TIME/TOTAL CPU TIME [%], ESTIMATED FLOATING POINT OPERATIONS PER ITERATION [-], MINIMUM REQUIRED MEMORY [MB], MEMORY TO MINIMIZE I/O [MB], TOTAL NUMBER OF ELEMENTS [-], NUMBER OF ELEMENTS DEFINED BY THE USER [-], NUMBER OF ELEMENTS DEFINED BY THE PROGRAM [-], TOTAL NUMBER OF NODES [-], NUMBER OF NODES DEFINED BY THE USER [-], NUMBER OF NODES DEFINED BY THE PROGRAM [-], TOTAL NUMBER OF VARIABLES [-]')
            titleline = ''
            if 'second' in RVEparams['mesh']['elements']['order']:
                titleline = 'deltatheta,Rf,L,Rf/L,phiCZ,G0,GI/G0,GII/G0,GTOT/G0,GIv2/G0,GIIv2/G0,GTOTv2/G0,GTOTequiv/G0,GI,GII,GTOT,GIv2,GIIv2,GTOTv2,GTOTequiv,np.min(uR),np.max(uR),np.mean(uR),np.min(uTheta),np.max(uTheta),np.mean(uTheta),xRFcracktip,yRFcracktip,xRFfirstbounded,yRFfirstbounded,rRFcracktip,thetaRFcracktip,rRFfirstbounded,thetaRFfirstbounded,xcracktipDisplacement,ycracktipDisplacement,rcracktipDisplacement,thetacracktipDisplacement,xfirstboundedDisplacement,yfirstboundedDisplacement,rfirstboundedDisplacement,thetafirstboundedDisplacement,xfiberCracktipDisplacement,yfiberCracktipDisplacement,rfiberCracktipDisplacement,thetafiberCracktipDisplacement,xfiberFirstboundedDisplacement,yfiberFirstboundedDisplacement,rfiberFirstboundedDisplacement,thetafiberFirstboundedDisplacement,xmatrixracktipDisplacement,ymatrixCracktipDisplacement,rmatrixCracktipDisplacement,thetamatrixCracktipDisplacement,xmatrixFirstboundedDisplacement,ymatrixFirstboundedDisplacement,rmatrixFirstboundedDisplacement,thetamatrixFirstboundedDisplacement'
            else:
                titleline = 'deltatheta,Rf,L,Rf/L,phiCZ,G0,GI/G0,GII/G0,GTOT/G0,GIv2/G0,GIIv2/G0,GTOTv2/G0,GTOTequiv/G0,GI,GII,GTOT,GIv2,GIIv2,GTOTv2,GTOTequiv,np.min(uR),np.max(uR),np.mean(uR),np.min(uTheta),np.max(uTheta),np.mean(uTheta),xRFcracktip,yRFcracktip,rRFcracktip,thetaRFcracktip,xcracktipDisplacement,ycracktipDisplacement,rcracktipDisplacement,thetacracktipDisplacement,xfiberCracktipDisplacement,yfiberCracktipDisplacement,rfiberCracktipDisplacement,thetafiberCracktipDisplacement,xmatrixCracktipDisplacement,ymatrixCracktipDisplacement,rmatrixCracktipDisplacement,thetamatrixCracktipDisplacement'
            createCSVfile(RVEparams['output']['global']['directory'],RVEparams['output']['global']['filenames']['energyreleaserate'],titleline)
            analyzeRVEresults(inputfilename.split('.')[0]+'.odb',RVEparams,logfilefullpath,logindent,logindent)
            localElapsedTime = timeit.default_timer() - localStart
            timedataList.append(localElapsedTime)
            totalIterationTime += localElapsedTime
            writeLineToLogFile(logfilefullpath,'a',logindent + 'Successfully returned from function: analyzeRVEresults(wd,odbname,logfilepath,parameters)',True)
            writeLineToLogFile(logfilefullpath,'a',logindent + 'Local timer stopped',True)
            writeLineToLogFile(logfilefullpath,'a',logindent + 'Elapsed time: ' + str(localElapsedTime) + ' [s]',True)
        except Exception, error:
            writeErrorToLogFile(logfilefullpath,'a',Exception,error,True)
            sys.exit(2)

        timedataList.append(np.sum(timedataList[1:]))
        appendCSVfile(RVEparams['output']['global']['directory'],logfilename.split('.')[0] + '_TIME',[timedataList])

        if debug:
            break

    #=======================================================================
    # END - ANALYSIS
    #=======================================================================

    #=======================================================================
    # BEGIN - REPORTING
    #=======================================================================

    skipLineToLogFile(logfilefullpath,'a',True)
    writeLineToLogFile(logfilefullpath,'a',logindent + 'Begin reporting',True)
    writeLineToLogFile(logfilefullpath,'a',logindent + 'Local timer starts',True)
    localStart = timeit.default_timer()

    writeLineToLogFile(logfilefullpath,'a',logindent + 'Setting the locale to US english ... ',True)
    locale.setlocale(locale.LC_TIME,'us_US')
    writeLineToLogFile(logfilefullpath,'a',logindent + '... done.',True)

    writeLineToLogFile(logfilefullpath,'a',logindent + 'Check if latex output directories exist and create them if needed ... ',True)

    reportFolder = RVEparams['output']['report']['global']['directory']
    reportFilename = RVEparams['output']['report']['global']['filename'].split('.')[0]

    if not os.path.exists(reportFolder):
            os.mkdir(reportFolder)

    if not os.path.exists(join(reportFolder,'pics')):
            os.mkdir(join(reportFolder,'pics'))

    writeLineToLogFile(logfilefullpath,'a',logindent + '... done.',True)

    writeLineToLogFile(logfilefullpath,'a',logindent + 'Copy report template images to latex folder ... ',True)
    copyfile(join('D:/01_Luca/06_WD/thinPlyMechanics/tex/Templates/Template_reports','Docmase_logo.jpg'),join(reportFolder,'pics','Docmase_logo.jpg'))
    copyfile(join('D:/01_Luca/06_WD/thinPlyMechanics/tex/Templates/Template_reports','erasmusmundus_logo.jpg'),join(reportFolder,'pics','erasmusmundus_logo.jpg'))
    copyfile(join('D:/01_Luca/06_WD/thinPlyMechanics/tex/Templates/Template_slides','logo-eeigm.jpg'),join(reportFolder,'pics','logo-eeigm.jpg'))
    copyfile(join('D:/01_Luca/06_WD/thinPlyMechanics/tex/Templates/Template_reports','lulea_logo1.jpg'),join(reportFolder,'pics','lulea_logo1.jpg'))
    writeLineToLogFile(logfilefullpath,'a',logindent + '... done.',True)

    writeLineToLogFile(logfilefullpath,'a',logindent + 'Reading index of generated csv files ... ',True)
    with open(join(RVEparams['output']['global']['directory'],logfilename.split('.')[0] + '_csvfileslist' + '.csv'),'r') as csv:
        lines = csv.readlines()
    writeLineToLogFile(logfilefullpath,'a',logindent + '... done.',True)

    writeLineToLogFile(logfilefullpath,'a',logindent + 'Generating local plots ... ',True)
    for l,line in enumerate(lines[5:]):
        csvPath = line.replace('\n','').split(',')[0]
        outDir = csvPath.split('\\')[0] + '/' + csvPath.split('\\')[1]
        writeLineToLogFile(logfilefullpath,'a',2*logindent + 'Opening file ' + csvPath,True)
        with open(csvPath,'r') as csv:
            csvlines = csv.readlines()
        plotName = line.replace('\n','').split(',')[1]
        toPlot = bool(line.replace('\n','').split(',')[2])
        plotSettings = []
        if toPlot:
            stringToEval = ','.join(line.replace('\n','').split(',')[3:])
            plotSettings = ast.literal_eval(stringToEval[1:])
            writeLineToLogFile(logfilefullpath,'a',2*logindent + str(len(plotSettings)) + ' PLOTS REQUESTED',True)
            for p,plot in enumerate(plotSettings):
                writeLineToLogFile(logfilefullpath,'a',3*logindent + 'Plot name: ' + plot[-1],True)
                writeLineToLogFile(logfilefullpath,'a',3*logindent + 'x-axis name: ' + plot[-3],True)
                writeLineToLogFile(logfilefullpath,'a',3*logindent + 'y-axis name: ' + plot[-2],True)
                writeLineToLogFile(logfilefullpath,'a',3*logindent + 'Number of curves: ' + str(len(plot[:-3])),True)
                xyData = []
                xmin = 0.0
                xmax = 0.0
                ymin = 0.0
                ymax = 0.0
                legendEntries = ''
                dataoptions = []
                for c,curve in enumerate(plot[:-3]):
                    writeLineToLogFile(logfilefullpath,'a',4*logindent + '(' + str(c+1) + ') Curve name: ' + curve[2],True)
                    writeLineToLogFile(logfilefullpath,'a',4*logindent + '    x-values: ' + csvlines[0].replace('\n','').split(',')[int(curve[0])],True)
                    xData = []
                    for csvline in csvlines[1:]:
                        if len(csvline)>2:
                            xData.append(float(csvline.replace('\n','').split(',')[int(curve[0])]))
                    writeLineToLogFile(logfilefullpath,'a',4*logindent + '    y-values: ' + csvlines[0].replace('\n','').split(',')[int(curve[1])],True)
                    yData = []
                    for csvline in csvlines[1:]:
                        if len(csvline)>2:
                            yData.append(float(csvline.replace('\n','').split(',')[int(curve[1])]))
                    xyData.append(np.transpose([np.array(xData),np.array(yData)]))
                    if c>0:
                        if np.min(xData)<xmin:
                            xmin = np.min(xData)
                    else:
                        xmin = np.min(xData)
                    if c>0:
                        if np.max(xData)<xmax:
                            xmax = np.max(xData)
                    else:
                        xmax = np.max(xData)
                    if c>0:
                        if np.min(yData)<ymin:
                            ymin = np.min(yData)
                    else:
                        ymin = np.min(yData)
                    if c>0:
                        if np.max(yData)<ymax:
                            ymax = np.max(yData)
                    else:
                        ymax = np.max(yData)
                    if c>0:
                        legendEntries += ', '
                    legendEntries += '{$' + curve[2] + '$}'
                    dataoptions.append('red!' + str(100.0*float(c)/float(len(plot[:-3]))) + '!blue')
                axisoptions = 'width=30cm,\n ' \
                              'title={\\bf{' + plot[-1] + '}},\n ' \
                              'title style={font=\\fontsize{40}{8}\\selectfont},\n ' \
                              'xlabel style={at={(axis description cs:0.5,-0.02)},anchor=north,font=\\fontsize{44}{40}\\selectfont},\n ' \
                              'ylabel style={at={(axis description cs:-0.025,.5)},anchor=south,font=\\fontsize{44}{40}\\selectfont},\n ' \
                              'xlabel={$' + plot[-3] + '$},ylabel={$' + plot[-2] + '$},\n ' \
                              'xmin=' + str(xmin) + ',\n ' \
                              'xmax=' + str(xmax) + ',\n ' \
                              'ymin=' + str(ymin) + ',\n ' \
                              'ymax=' + str(ymax) + ',\n ' \
                              'tick align=outside,\n ' \
                              'tick label style={font=\\huge},\n ' \
                              'xmajorgrids,\n ' \
                              'x grid style={lightgray!92.026143790849673!black},\n ' \
                              'ymajorgrids,\n ' \
                              'y grid style={lightgray!92.026143790849673!black},\n ' \
                              'line width=0.5mm,\n ' \
                              'legend style={draw=white!80.0!black,font=\\fontsize{28}{24}\\selectfont,row sep=15pt},\n ' \
                              'legend entries={' + legendEntries + '},\n ' \
                              'legend image post style={xscale=2},\n ' \
                              'legend cell align={left}'
                writeLineToLogFile(logfilefullpath,'a',3*logindent + 'Create plot in file ' + plot[-1].replace(' ','-').replace('/','-').replace(',','') + '.pdf' + ' in directory ' + outDir,True)
                writeLatexMultiplePlots(outDir,plot[-1].replace(' ','-').replace('/','-').replace(',','') + '.tex',xyData,axisoptions,dataoptions,logfilefullpath,3*logindent,logindent)
        else:
            writeLineToLogFile(logfilefullpath,'a',2*logindent + 'NO PLOT REQUESTED',True)

    writeLineToLogFile(logfilefullpath,'a',logindent + 'Generating global plots ... ',True)
    for l,line in enumerate(lines[1:5]):
        csvPath = line.replace('\n','').split(',')[0]
        outDir = csvPath.split('\\')[0]
        writeLineToLogFile(logfilefullpath,'a',2*logindent + 'Opening file ' + csvPath,True)
        with open(csvPath,'r') as csv:
            csvlines = csv.readlines()
        plotName = line.replace('\n','').split(',')[1]
        toPlot = bool(line.replace('\n','').split(',')[2])
        plotSettings = []
        if toPlot:
            stringToEval = ','.join(line.replace('\n','').split(',')[3:])
            plotSettings = ast.literal_eval(stringToEval[1:])
            writeLineToLogFile(logfilefullpath,'a',2*logindent + str(len(plotSettings)) + ' PLOTS REQUESTED',True)
            for p,plot in enumerate(plotSettings):
                writeLineToLogFile(logfilefullpath,'a',3*logindent + 'Plot name: ' + plot[-1],True)
                writeLineToLogFile(logfilefullpath,'a',3*logindent + 'x-axis name: ' + plot[-3],True)
                writeLineToLogFile(logfilefullpath,'a',3*logindent + 'y-axis name: ' + plot[-2],True)
                writeLineToLogFile(logfilefullpath,'a',3*logindent + 'Number of curves: ' + str(len(plot[:-3])),True)
                xyData = []
                xmin = 0.0
                xmax = 0.0
                ymin = 0.0
                ymax = 0.0
                legendEntries = ''
                dataoptions = []
                for c,curve in enumerate(plot[:-3]):
                    writeLineToLogFile(logfilefullpath,'a',4*logindent + '(' + str(c+1) + ') Curve name: ' + curve[2],True)
                    writeLineToLogFile(logfilefullpath,'a',4*logindent + '    x-values: ' + csvlines[0].replace('\n','').split(',')[int(curve[0])],True)
                    xData = []
                    for csvline in csvlines[1:]:
                        if len(csvline)>2:
                            xData.append(float(csvline.replace('\n','').split(',')[int(curve[0])]))
                    writeLineToLogFile(logfilefullpath,'a',4*logindent + '    y-values: ' + csvlines[0].replace('\n','').split(',')[int(curve[1])],True)
                    yData = []
                    for csvline in csvlines[1:]:
                        if len(csvline)>2:
                            yData.append(float(csvline.replace('\n','').split(',')[int(curve[1])]))
                    xyData.append(np.transpose([np.array(xData),np.array(yData)]))
                    if c>0:
                        if np.min(xData)<xmin:
                            xmin = np.min(xData)
                    else:
                        xmin = np.min(xData)
                    if c>0:
                        if np.max(xData)<xmax:
                            xmax = np.max(xData)
                    else:
                        xmax = np.max(xData)
                    if c>0:
                        if np.min(yData)<ymin:
                            ymin = np.min(yData)
                    else:
                        ymin = np.min(yData)
                    if c>0:
                        if np.max(yData)<ymax:
                            ymax = np.max(yData)
                    else:
                        ymax = np.max(yData)
                    if c>0:
                        legendEntries += ', '
                    legendEntries += '{$' + curve[2] + '$}'
                    dataoptions.append('red!' + str(100.0*float(c)/float(len(plot[:-3]))) + '!blue')
                axisoptions = 'width=30cm,\n ' \
                              'title={\\bf{' + plot[-1] + '}},\n ' \
                              'title style={font=\\fontsize{40}{8}\\selectfont},\n ' \
                              'xlabel style={at={(axis description cs:0.5,-0.02)},anchor=north,font=\\fontsize{44}{40}\\selectfont},\n ' \
                              'ylabel style={at={(axis description cs:-0.025,.5)},anchor=south,font=\\fontsize{44}{40}\\selectfont},\n ' \
                              'xlabel={$' + plot[-3] + '$},ylabel={$' + plot[-2] + '$},\n ' \
                              'xmin=' + str(xmin) + ',\n ' \
                              'xmax=' + str(xmax) + ',\n ' \
                              'ymin=' + str(ymin) + ',\n ' \
                              'ymax=' + str(ymax) + ',\n ' \
                              'tick align=outside,\n ' \
                              'tick label style={font=\\huge},\n ' \
                              'xmajorgrids,\n ' \
                              'x grid style={lightgray!92.026143790849673!black},\n ' \
                              'ymajorgrids,\n ' \
                              'y grid style={lightgray!92.026143790849673!black},\n ' \
                              'line width=0.5mm,\n ' \
                              'legend style={draw=white!80.0!black,font=\\fontsize{28}{24}\\selectfont,row sep=15pt},\n ' \
                              'legend entries={' + legendEntries + '},\n ' \
                              'legend image post style={xscale=2},\n ' \
                              'legend cell align={left}'
                writeLineToLogFile(logfilefullpath,'a',3*logindent + 'Create plot in file ' + plot[-1].replace(' ','-').replace('/','-').replace(',','') + '.pdf' + ' in directory ' + outDir,True)
                writeLatexMultiplePlots(outDir,plot[-1].replace(' ','-').replace('/','-').replace(',','') + '.tex',xyData,axisoptions,dataoptions,logfilefullpath,3*logindent,logindent)
        else:
            writeLineToLogFile(logfilefullpath,'a',2*logindent + 'NO PLOT REQUESTED',True)

    writeLineToLogFile(logfilefullpath,'a',logindent + '... done.',True)

    writeLineToLogFile(logfilefullpath,'a',logindent + 'Creating main report ...',True)

    writeLineToLogFile(logfilefullpath,'a',2*logindent + 'Create latex file ...',True)
    createLatexFile(reportFolder,reportFilename,'scrartcl',options='a4paper, twoside,12pt, abstract')
    packages = ['inputenc',
                'fontenc',
                'amsfonts',
                'amsmath',
                'amssymb',
                'amstext',
                'animate',
                'babel',
                'biblatex',
                'bm',
                'booktabs',
                'caption',
                'colortbl',
                'csquotes',
                'enumerate',
                'eurosym',
                'geometry',
                'graphicx',
                'float',
                'helvet',
                'longtable',
                'makeidx',
                'multirow',
                'nameref',
                'parskip',
                'pdfpages',
                'rotating',
                'scrpage2',
                'setspace',
                'standalone',
                'subcaption',
                'tabularx',
                'tikz',
                'xcolor',
                'glossaries',
                'hyperref']
    options = ['utf8',
               'fontenc',
               '',
               '',
               '',
               '',
               '',
               'english',
               'backend=bibtex, sorting=none,style=numeric',
               '',
               '',
               '',
               '',
               '',
               '',
               'right',
               'inner=3cm,outer=2cm,top=2.7cm,bottom=3.2cm',
               '',
               '',
               'scaled=.90',
               '',
               '',
               '',
               '',
               '',
               '',
               '',
               '',
               '',
               '',
               '',
               '',
               '',
               '',
               'acronym,nonumberlist,nopostdot,toc',
               '']
    writeLatexPackages(reportFolder,reportFilename,packages,options)
    writeLineToLogFile(logfilefullpath,'a',2*logindent + '... done.',True)

    writeLineToLogFile(logfilefullpath,'a',2*logindent + 'Write packages ...',True)
    writeLatexCustomLine(reportFolder,reportFilename,'\\definecolor{Gray}{gray}{0.85}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\definecolor{LightCyan}{rgb}{0.88,1,1}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\sloppy % avoids lines that are too long on the right side')
    writeLatexCustomLine(reportFolder,reportFilename,'% avoid "orphans"')
    writeLatexCustomLine(reportFolder,reportFilename,'\\clubpenalty = 10000')
    writeLatexCustomLine(reportFolder,reportFilename,'% avoid "widows"')
    writeLatexCustomLine(reportFolder,reportFilename,'\\widowpenalty = 10000')
    writeLatexCustomLine(reportFolder,reportFilename,'% this makes the table of content etc. look better')
    writeLatexCustomLine(reportFolder,reportFilename,'\\renewcommand{\\dotfill}{\\leaders\\hbox to 5pt{\\hss.\\hss}\\hfill}')
    writeLatexCustomLine(reportFolder,reportFilename,'% avoid indentation of line after a paragraph')
    writeLatexSetLength(reportFolder,reportFilename,'parindent','0pt')
    writeLatexGenericCommand(reportFolder,reportFilename,'pagestyle','','scrheadings')
    writeLatexGenericCommand(reportFolder,reportFilename,'automark','section','section')
    writeLatexGenericCommand(reportFolder,reportFilename,'ofoot','','\\pagemark')
    writeLatexGenericCommand(reportFolder,reportFilename,'ifoot','','Research Plan')
    writeLatexSetLength(reportFolder,reportFilename,'unitlength','1cm')
    writeLatexSetLength(reportFolder,reportFilename,'oddsidemargin','0.3cm')
    writeLatexSetLength(reportFolder,reportFilename,'evensidemargin','0.3cm')
    writeLatexSetLength(reportFolder,reportFilename,'textwidth','15.5cm')
    writeLatexSetLength(reportFolder,reportFilename,'topmargin','0cm')
    writeLatexSetLength(reportFolder,reportFilename,'textheight','22cm')
    writeLatexCustomLine(reportFolder,reportFilename,'\\columnsep 0.5cm')
    writeLatexCustomLine(reportFolder,reportFilename,'\\newcommand{\\brac}[1]{\\left(#1\\right)}')
    writeLatexGenericCommand(reportFolder,reportFilename,'graphicspath','','{./pics/}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\addto\\captionsenglish{\\renewcommand{\\listfigurename}{Figures}}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\addto\\captionsenglish{\\renewcommand{\\listtablename}{Tables}}')
    writeLatexGenericCommand(reportFolder,reportFilename,'makeglossaries','','')
    writeLatexGenericCommand(reportFolder,reportFilename,'makeindex','','',)
    writeLineToLogFile(logfilefullpath,'a',2*logindent + '... done.',True)

    writeLineToLogFile(logfilefullpath,'a',2*logindent + 'Document starts ...',True)

    writeLatexDocumentStarts(reportFolder,reportFilename)

    writeLineToLogFile(logfilefullpath,'a',3*logindent + 'Title page',True)

    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'%------------------------------------------------%')
    writeLatexCustomLine(reportFolder,reportFilename,'%------------------------------------------------%')
    writeLatexCustomLine(reportFolder,reportFilename,'%                  Front Matter                  %')
    writeLatexCustomLine(reportFolder,reportFilename,'%------------------------------------------------%')
    writeLatexCustomLine(reportFolder,reportFilename,'%------------------------------------------------%')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'%------------------------------------------------%')
    writeLatexCustomLine(reportFolder,reportFilename,'%                 Title Page')
    writeLatexCustomLine(reportFolder,reportFilename,'%------------------------------------------------%')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'\\clearscrheadings')
    writeLatexCustomLine(reportFolder,reportFilename,'\\pagestyle{scrheadings}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\manualmark')
    writeLatexCustomLine(reportFolder,reportFilename,'\\ihead{\\href{http://www.ltu.se/}{\\includegraphics[height=1.5cm]{lulea_logo1.jpg}}\\hspace{6.1953125cm}\\href{http://www.eeigm.univ-lorraine.fr/}{\\includegraphics[height=1.5cm]{logo-eeigm.jpg}}}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\ifoot{\\noindent\\makebox[\\linewidth]{\\rule{\\textwidth}{0.4pt}}\\\\\\href{http://eacea.ec.europa.eu/erasmus_mundus/index_en.php}{\\includegraphics[height=1.75cm]{erasmusmundus_logo.jpg}}\\hspace{9.55cm}\\href{http://www.uni-saarland.de/einrichtung/eusmat/international-studies/phd/docmase.html}{\\includegraphics[height=1.75cm]{Docmase_logo.jpg}}}')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'\\setheadsepline{0.5pt}')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'\\begin{center}')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'\\vspace*{0.1cm}')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'\\begin{Large}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\textbf{\\textsc{EUSMAT}}\\\\[0.75ex]')
    writeLatexCustomLine(reportFolder,reportFilename,'\\end{Large}')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'\\begin{large}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\textbf{European School of Materials}\\\\[0.75ex]')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'\\vspace*{1cm}')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'\\textbf{DocMASE}\\\\[0.75ex]')
    writeLatexCustomLine(reportFolder,reportFilename,'\\textbf{\\textsc{Doctorate in Materials Science and Engineering}}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\end{large}')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'\\vspace{1.75cm}')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'\\begin{Large}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\textbf{\\textsc{Simulation Report}}\\\\[0.75ex]')
    writeLatexCustomLine(reportFolder,reportFilename,'\\end{Large}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\vspace*{0.5cm}')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'\\begin{LARGE}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\textbf{\\textsc{Report of ABAQUS simulations}}\\\\[0.75ex]')
    writeLatexCustomLine(reportFolder,reportFilename,'\\end{LARGE}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\vspace*{2.5cm}')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'\\begin{flushright}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\begin{tabular}{l l }')
    writeLatexCustomLine(reportFolder,reportFilename,'{\\large \\textbf{Doctoral Candidate:}} & {\\large \\href{http://lucadistasioengineering.com/}{Luca DI STASIO}}\\\\')
    writeLatexCustomLine(reportFolder,reportFilename,'&\\\\')
    writeLatexCustomLine(reportFolder,reportFilename,'&\\\\')
    writeLatexCustomLine(reportFolder,reportFilename,'&\\\\')
    writeLatexCustomLine(reportFolder,reportFilename,'{\\large \\textbf{Thesis Supervisors:}}& {\\large Prof. Zoubir AYADI}\\\\')
    writeLatexCustomLine(reportFolder,reportFilename,'&{\\large Universit\\\'e de Lorraine}\\\\')
    writeLatexCustomLine(reportFolder,reportFilename,'&{\\large Nancy, France}\\\\')
    writeLatexCustomLine(reportFolder,reportFilename,'&\\\\')
    writeLatexCustomLine(reportFolder,reportFilename,'& {\\large Prof. Janis VARNA}\\\\')
    writeLatexCustomLine(reportFolder,reportFilename,'&{\\large Lule\\aa\\ University of Technology}\\\\')
    writeLatexCustomLine(reportFolder,reportFilename,'&{\\large Lule\\aa, Sweden}\\\\')
    writeLatexCustomLine(reportFolder,reportFilename,'\\end{tabular}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\end{flushright}')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'\\vspace*{2cm}')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    timeNow = datetime.now()
    writeLatexCustomLine(reportFolder,reportFilename,'{\\large \\textbf{Created on ' + timeNow.strftime('%B') + timeNow.strftime('%d') + ', ' + timeNow.strftime('%Y') +'}}\\\\[10pt]')
    writeLatexCustomLine(reportFolder,reportFilename,'{\\large \\textbf{Last Updated on \\today}}\\\\')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'\\end{center}')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'\\cleardoublepage')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLineToLogFile(logfilefullpath,'a',3*logindent + 'Table of Contents',True)
    writeLatexCustomLine(reportFolder,reportFilename,'%------------------------------------------------%')
    writeLatexCustomLine(reportFolder,reportFilename,'%            Table of Contents')
    writeLatexCustomLine(reportFolder,reportFilename,'%------------------------------------------------%')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'\\pagenumbering{roman}')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'\\setcounter{page}{1}')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'\\clearscrheadings')
    writeLatexCustomLine(reportFolder,reportFilename,'\\pagestyle{scrheadings}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\manualmark')
    writeLatexCustomLine(reportFolder,reportFilename,'\\ofoot{\\\\ \\hyperref[sec:content]{\\pagemark}}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\ifoot{} % ofoo')
    writeLatexCustomLine(reportFolder,reportFilename,'\\ohead{\\contentsname}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\setheadtopline{2pt}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\setheadsepline{0.5pt}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\setfootsepline{0.5pt}')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'\\tableofcontents')
    writeLatexCustomLine(reportFolder,reportFilename,'\\label{sec:content}')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'\\cleardoublepageusingstyle{scrheadings}')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLineToLogFile(logfilefullpath,'a',3*logindent + 'List of Figures',True)
    writeLatexCustomLine(reportFolder,reportFilename,'%------------------------------------------------%')
    writeLatexCustomLine(reportFolder,reportFilename,'%            List of Figures')
    writeLatexCustomLine(reportFolder,reportFilename,'%------------------------------------------------%')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'\\clearscrheadings')
    writeLatexCustomLine(reportFolder,reportFilename,'\\pagestyle{scrheadings}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\manualmark')
    writeLatexCustomLine(reportFolder,reportFilename,'\\ofoot{\\\\ \\hyperref[sec:content]{\\pagemark}}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\ifoot{} % ofoo')
    writeLatexCustomLine(reportFolder,reportFilename,'\\ohead{\\listfigurename}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\setheadtopline{2pt}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\setheadsepline{0.5pt}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\setfootsepline{0.5pt}')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'%\\section*{List of Figures}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\addcontentsline{toc}{section}{\\listfigurename}')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'\\listoffigures')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'\\cleardoublepageusingstyle{scrheadings}')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLineToLogFile(logfilefullpath,'a',3*logindent + 'List of Tables',True)
    writeLatexCustomLine(reportFolder,reportFilename,'%------------------------------------------------%')
    writeLatexCustomLine(reportFolder,reportFilename,'%            List of Tables')
    writeLatexCustomLine(reportFolder,reportFilename,'%------------------------------------------------%')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'\\clearscrheadings')
    writeLatexCustomLine(reportFolder,reportFilename,'\\pagestyle{scrheadings}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\manualmark')
    writeLatexCustomLine(reportFolder,reportFilename,'\\ofoot{\\\\ \\hyperref[sec:content]{\\pagemark}}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\ifoot{} % ofoo')
    writeLatexCustomLine(reportFolder,reportFilename,'\\ohead{\\listtablename}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\setheadtopline{2pt}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\setheadsepline{0.5pt}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\setfootsepline{0.5pt}')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'%\\section*{List of Tables}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\addcontentsline{toc}{section}{\\listtablename}')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'\\listoftables')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'\\cleardoublepageusingstyle{scrheadings}')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLineToLogFile(logfilefullpath,'a',3*logindent + 'List of Acronyms',True)
    writeLatexCustomLine(reportFolder,reportFilename,'%------------------------------------------------%')
    writeLatexCustomLine(reportFolder,reportFilename,'%            List of Acronyms')
    writeLatexCustomLine(reportFolder,reportFilename,'%------------------------------------------------%')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'\\clearscrheadings')
    writeLatexCustomLine(reportFolder,reportFilename,'\\pagestyle{scrheadings}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\manualmark')
    writeLatexCustomLine(reportFolder,reportFilename,'\\ofoot{\\\\ \\hyperref[sec:content]{\\pagemark}}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\ifoot{} % ofoo')
    writeLatexCustomLine(reportFolder,reportFilename,'\\ohead{\\nameref{sec:acr}}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\setheadtopline{2pt}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\setheadsepline{0.5pt}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\setfootsepline{0.5pt}')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'\\section*{Acronyms}\\label{sec:acr}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\addcontentsline{toc}{section}{\\nameref{sec:acr}}')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'\\printglossary[type=\\acronymtype]')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'%\\printglossary')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'\\cleardoublepageusingstyle{scrheadings}')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLineToLogFile(logfilefullpath,'a',3*logindent + 'List of Symbols',True)
    writeLatexCustomLine(reportFolder,reportFilename,'%------------------------------------------------%')
    writeLatexCustomLine(reportFolder,reportFilename,'%            List of Symbols')
    writeLatexCustomLine(reportFolder,reportFilename,'%------------------------------------------------%')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'\\clearscrheadings')
    writeLatexCustomLine(reportFolder,reportFilename,'\\pagestyle{scrheadings}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\manualmark')
    writeLatexCustomLine(reportFolder,reportFilename,'\\ofoot{\\\\ \\hyperref[sec:content]{\\pagemark}}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\ifoot{} % ofoo')
    writeLatexCustomLine(reportFolder,reportFilename,'\\ohead{\\nameref{sec:sym}}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\setheadtopline{2pt}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\setheadsepline{0.5pt}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\setfootsepline{0.5pt}')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'\\section*{Symbols}\\label{sec:sym}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\addcontentsline{toc}{section}{\\nameref{sec:sym}}')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'%\\input{symbols}')
    writeLatexCustomLine(reportFolder,reportFilename,'%')
    writeLatexCustomLine(reportFolder,reportFilename,'\\cleardoublepageusingstyle{scrheadings}')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLineToLogFile(logfilefullpath,'a',3*logindent + 'Abstract',True)
    writeLatexCustomLine(reportFolder,reportFilename,'%------------------------------------------------%')
    writeLatexCustomLine(reportFolder,reportFilename,'%                   Abstract')
    writeLatexCustomLine(reportFolder,reportFilename,'%------------------------------------------------%')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'\\clearscrheadings')
    writeLatexCustomLine(reportFolder,reportFilename,'\\pagestyle{scrheadings}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\manualmark')
    writeLatexCustomLine(reportFolder,reportFilename,'\\ofoot{\\\\ \\hyperref[sec:content]{\\pagemark}}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\ifoot{} % ofoo')
    writeLatexCustomLine(reportFolder,reportFilename,'\\ohead{\\nameref{sec:abs}}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\setheadtopline{2pt}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\setheadsepline{0.5pt}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\setfootsepline{0.5pt}')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'\\section*{Abstract}\\label{sec:abs}')
    writeLatexCustomLine(reportFolder,reportFilename,'\\addcontentsline{toc}{section}{\\nameref{sec:abs}}')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'\\cleardoublepageusingstyle{scrheadings}')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'%------------------------------------------------%')
    writeLatexCustomLine(reportFolder,reportFilename,'%------------------------------------------------%')
    writeLatexCustomLine(reportFolder,reportFilename,'%                   Main Matter                  %')
    writeLatexCustomLine(reportFolder,reportFilename,'%------------------------------------------------%')
    writeLatexCustomLine(reportFolder,reportFilename,'%------------------------------------------------%')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'\\pagenumbering{arabic}')
    writeLatexCustomLine(reportFolder,reportFilename,'')
    writeLatexCustomLine(reportFolder,reportFilename,'\\setcounter{page}{1}')
    writeLatexCustomLine(reportFolder,reportFilename,'')

    writeLineToLogFile(logfilefullpath,'a',3*logindent + 'Global results',True)
    for l,line in enumerate(lines[1:5]):
        csvPath = line.replace('\n','').split(',')[0]
        outDir = csvPath.split('\\')[0]
        writeLineToLogFile(logfilefullpath,'a',4*logindent + 'Opening file ' + csvPath,True)
        with open(csvPath,'r') as csv:
            csvlines = csv.readlines()
        plotName = line.replace('\n','').split(',')[1]
        toPlot = bool(line.replace('\n','').split(',')[2])
        plotSettings = []
        if toPlot:
            writeLineToLogFile(logfilefullpath,'a',4*logindent + str(len(plotSettings)) + ' PLOTS TO BE INSERTED',True)
            plotSettings = ast.literal_eval(','.join(line.replace('\n','').split(',')[3:]))
            for p,plot in enumerate(plotSettings):
                writeLatexCustomLine(reportFolder,reportFilename,'%------------------------------------------------%')
                writeLatexCustomLine(reportFolder,reportFilename,'%               GLOBAL - ' + plot[-1])
                writeLatexCustomLine(reportFolder,reportFilename,'%------------------------------------------------%')
                writeLatexCustomLine(reportFolder,reportFilename,'')
                writeLatexCustomLine(reportFolder,reportFilename,'\\clearscrheadings')
                writeLatexCustomLine(reportFolder,reportFilename,'\\pagestyle{scrheadings}')
                writeLatexCustomLine(reportFolder,reportFilename,'\\manualmark')
                writeLatexCustomLine(reportFolder,reportFilename,'\\ofoot{\\\\ \\hyperref[sec:content]{\\pagemark}}')
                writeLatexCustomLine(reportFolder,reportFilename,'\\ifoot{} % ofoo')
                writeLatexCustomLine(reportFolder,reportFilename,'\\ohead{\\nameref{sec:sec1}}')
                writeLatexCustomLine(reportFolder,reportFilename,'\\setheadtopline{2pt}')
                writeLatexCustomLine(reportFolder,reportFilename,'\\setheadsepline{0.5pt}')
                writeLatexCustomLine(reportFolder,reportFilename,'\\setfootsepline{0.5pt}')
                writeLatexCustomLine(reportFolder,reportFilename,'')
                writeLatexCustomLine(reportFolder,reportFilename,'\\section{Parametric study: ' + plot[-1] + '}\label{sec:sec1}')
                writeLatexCustomLine(reportFolder,reportFilename,'\\begin{figure}[!h]')
                writeLatexCustomLine(reportFolder,reportFilename,'\\includegraphics[width=\\textwidth]{' + outDir + plot[-1].replace(' ','-').replace('/','-').replace(',','') + '.pdf}')
                writeLatexCustomLine(reportFolder,reportFilename,'\\end{figure}')
                writeLatexCustomLine(reportFolder,reportFilename,'')
                writeLatexCustomLine(reportFolder,reportFilename,'\\cleardoublepageusingstyle{scrheadings}')
                writeLatexCustomLine(reportFolder,reportFilename,'')

    writeLineToLogFile(logfilefullpath,'a',3*logindent + 'Local results',True)
    for l,line in enumerate(lines[5:]):
        csvPath = line.replace('\n','').split(',')[0]
        outDir = csvPath.split('\\')[0] + '/' + csvPath.split('\\')[1]
        writeLineToLogFile(logfilefullpath,'a',4*logindent + 'Opening file ' + csvPath,True)
        with open(csvPath,'r') as csv:
            csvlines = csv.readlines()
        plotName = line.replace('\n','').split(',')[1]
        toPlot = bool(line.replace('\n','').split(',')[2])
        plotSettings = []
        if toPlot:
            writeLineToLogFile(logfilefullpath,'a',4*logindent + str(len(plotSettings)) + ' PLOTS TO BE INSERTED',True)
            plotSettings = ast.literal_eval(','.join(line.replace('\n','').split(',')[3:]))
            writeLatexCustomLine(reportFolder,reportFilename,'%------------------------------------------------%')
            writeLatexCustomLine(reportFolder,reportFilename,'%               SIMULATION N. ' + str(p+1))
            writeLatexCustomLine(reportFolder,reportFilename,'%------------------------------------------------%')
            writeLatexCustomLine(reportFolder,reportFilename,'')
            writeLatexCustomLine(reportFolder,reportFilename,'\\clearscrheadings')
            writeLatexCustomLine(reportFolder,reportFilename,'\\pagestyle{scrheadings}')
            writeLatexCustomLine(reportFolder,reportFilename,'\\manualmark')
            writeLatexCustomLine(reportFolder,reportFilename,'\\ofoot{\\\\ \\hyperref[sec:content]{\\pagemark}}')
            writeLatexCustomLine(reportFolder,reportFilename,'\\ifoot{} % ofoo')
            writeLatexCustomLine(reportFolder,reportFilename,'\\ohead{\\nameref{sec:sec1}}')
            writeLatexCustomLine(reportFolder,reportFilename,'\\setheadtopline{2pt}')
            writeLatexCustomLine(reportFolder,reportFilename,'\\setheadsepline{0.5pt}')
            writeLatexCustomLine(reportFolder,reportFilename,'\\setfootsepline{0.5pt}')
            writeLatexCustomLine(reportFolder,reportFilename,'')
            writeLatexCustomLine(reportFolder,reportFilename,'\\section{Simulation n. ' + str(p+1) + '}\label{sec:sec1}')
            for p,plot in enumerate(plotSettings):
                writeLatexCustomLine(reportFolder,reportFilename,'\\begin{figure}[!h]')
                writeLatexCustomLine(reportFolder,reportFilename,'\\includegraphics[width=\\textwidth]{' + outDir + plot[-1].replace(' ','-').replace('/','-').replace(',','') + '.pdf}')
                writeLatexCustomLine(reportFolder,reportFilename,'\\end{figure}')
            writeLatexCustomLine(reportFolder,reportFilename,'')
            writeLatexCustomLine(reportFolder,reportFilename,'\\cleardoublepageusingstyle{scrheadings}')
            writeLatexCustomLine(reportFolder,reportFilename,'')

    writeLineToLogFile(logfilefullpath,'a',3*logindent + 'Documents ends',True)
    writeLatexDocumentEnds(reportFolder,reportFilename)

    writeLineToLogFile(logfilefullpath,'a',2*logindent + '... done. ',True)

    writeLineToLogFile(logfilefullpath,'a',2*logindent + 'Compile pdf ... ',True)
    cmdfile = join(reportFolder,'runlatex.cmd')
    with open(cmdfile,'w') as cmd:
        cmd.write('\n')
        cmd.write('CD ' + reportFolder + '\n')
        cmd.write('\n')
        cmd.write('pdflatex ' + join(reportFolder,reportFilename.split(',')[0] + '.tex') + ' -job-name=' + reportFilename.split(',')[0] + '\n')
    try:
        subprocess.call('cmd.exe /C ' + cmdfile)
    except Exception:
        sys.exc_clear()
    writeLineToLogFile(logfilefullpath,'a',2*logindent + '... done. ',True)

    writeLineToLogFile(logfilefullpath,'a',logindent + 'Local timer stopped',True)
    writeLineToLogFile(logfilefullpath,'a',logindent + 'Elapsed time: ' + str(localElapsedTime) + ' [s]',True)

    writeLineToLogFile(logfilefullpath,'a',logindent + '... done. ',True)

    #=======================================================================
    # END - REPORTING
    #=======================================================================

    globalElapsedTime = timeit.default_timer() - globalStart
    writeLineToLogFile(logfilefullpath,'a',logindent + 'Global timer stopped',True)
    writeLineToLogFile(logfilefullpath,'a',logindent + 'Elapsed time: ' + str(globalElapsedTime) + ' [s]',True)

    skipLineToLogFile(logfilefullpath,'a',True)
    writeLineToLogFile(logfilefullpath,'a','Exiting function: main(argv)',True)
    writeLineToLogFile(logfilefullpath,'a','Goodbye!',True)

if __name__ == "__main__":
    main(sys.argv[1:])
