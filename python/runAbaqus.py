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

from os import listdir
from os.path import isfile, join
import sys
import getopt
from datetime import datetime
from time import strftime, sleep
from platform import platform
from numpy import arange
import math
import subprocess
import win32com.client
from sendStatusEmail import *

def buildPreprocessorCall(preprocessor,functionCall,args,wd,logfilename):
    call = functionCall + '('
    for i,arg in enumerate(args):
        if i>0:
            call += ','
        if 'String' in arg[1]:
            call += '\'' + arg[0]  + '\''
        elif 'Vector' in arg[1]:
            call += '['
            for j,element in enumerate(arg[0]):
                if j>0:
                    call += ';'
                call += element
            call += ']'
        else:
            call += str(arg[0])
    call += ')'
    if 'matlab' in preprocessor:
        preprocessorFile = 'preprocessor.m'
        with open(logfilename,'a') as log:
            log.write('Starting to write preprocessor script in Matlab.' + '\n')
            log.write('\n')
        print('Starting to write preprocessor script in Matlab.'  + '\n')
        print('\n')
    elif 'cpp' in preprocessor:
        preprocessorFile = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '_preprocessor.cpp'
        with open(logfilename,'a') as log:
            log.write('Starting to write preprocessor script in C++.' + '\n')
            log.write('\n')
        print('Starting to write preprocessor script in C++.'  + '\n')
        print('\n')
    else:
        preprocessorFile = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '_preprocessor.py'
        with open(logfilename,'a') as log:
            log.write('Starting to write preprocessor script in Python.' + '\n')
            log.write('\n')
        print('Starting to write preprocessor script in Python.'  + '\n')
        print('\n')
    try:
        with open(join(wd,preprocessorFile),'w') as pre:
            pre.write('')
            pre.write('%%\n')
            pre.write('%==============================================================================\n')
            pre.write('% Copyright (c) 2016-2017 Universite de Lorraine & Lulea tekniska universitet\n')
            pre.write('% Author: Luca Di Stasio <luca.distasio@gmail.com>\n')
            pre.write('%                        <luca.distasio@ingpec.eu>\n')
            pre.write('%\n')
            pre.write('% Redistribution and use in source and binary forms, with or without\n')
            pre.write('% modification, are permitted provided that the following conditions are met:\n')
            pre.write('% \n')
            pre.write('% Redistributions of source code must retain the above copyright\n')
            pre.write('% notice, this list of conditions and the following disclaimer.\n')
            pre.write('% Redistributions in binary form must reproduce the above copyright\n')
            pre.write('% notice, this list of conditions and the following disclaimer in\n')
            pre.write('% the documentation and/or other materials provided with the distribution\n')
            pre.write('% Neither the name of the Universite de Lorraine or Lulea tekniska universitet\n')
            pre.write('% nor the names of its contributors may be used to endorse or promote products\n')
            pre.write('% derived from this software without specific prior written permission.\n')
            pre.write('% \n')
            pre.write('% THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"\n')
            pre.write('% AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE\n')
            pre.write('% IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE\n')
            pre.write('% ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE\n')
            pre.write('% LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR\n')
            pre.write('% CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF\n')
            pre.write('% SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS\n')
            pre.write('% INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN\n')
            pre.write('% CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)\n')
            pre.write('% ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE\n')
            pre.write('% POSSIBILITY OF SUCH DAMAGE.\n')
            pre.write('%==============================================================================\n')
            pre.write('%\n')
            pre.write('%  DESCRIPTION\n')
            pre.write('%  \n')
            pre.write('%  Abaqus preprocessor script\n')
            pre.write('%  \n')
            pre.write('  \n')
            pre.write('  \n')
            pre.write('clear all;\n')
            pre.write('close all;\n')
            pre.write('  \n')
            pre.write('  \n')
            pre.write(call)
            pre.write('  \n')
        with open(logfilename,'a') as log:
            log.write('SUCCESS. File ' + preprocessorFile + ' created in folder ' + wd + '\n')
            log.write('\n')
        print('SUCCESS. File ' + preprocessorFile + ' created in folder ' + wd + '\n')
        print('\n')
    except Exception,e:
        with open(logfilename,'a') as log:
            log.write('FAILED to create file ' + preprocessorFile + ' in folder ' + wd + '\n')
            log.write('\n')
            log.write(str(Exception) + '\n')
            log.write('\n')
        print('FAILED to create file ' + preprocessorFile + ' in folder ' + wd + '\n')
        print('\n')
        print(str(Exception) + '\n')
        print('\n')
        sendStatusEmail('D:/OneDrive/01_Luca/07_DocMASE/06_WD','logData.csv','smtp.univ-lorraine.fr','luca.di-stasio@univ-lorraine.fr','luca.distasio@gmail.com','ABAQUS PARAMETRIC RUN INTERRUPTED','Abaqus parametric run interrupted on ' + datetime.now().strftime('%Y-%m-%d') + ' at ' + datetime.now().strftime('%H:%M:%S') + '\n\n An error occurred. Details:\n' + str(e)+ '\n\n View log file for further info.')
        sys.exit()
    return preprocessorFile


def runPreprocessor(preprocessor,functionCall,args,wd,logfilename):
    print('\n')
    print('=====================================================================\n')
    print('\n')
    print('                 PREPROCESSING\n')
    print('\n')
    print('          Starting on ' + datetime.now().strftime('%Y-%m-%d') + ' at ' + datetime.now().strftime('%H:%M:%S') + '\n')
    print('\n')
    print('             Preprocessor: ' + preprocessor + '\n')
    print('\n')
    print('=====================================================================\n')
    print('\n')
    with open(logfilename,'a') as log:
        log.write('\n')
        log.write('=====================================================================\n')
        log.write('\n')
        log.write('                 PREPROCESSING\n')
        log.write('\n')
        log.write('          Starting on ' + datetime.now().strftime('%Y-%m-%d') + ' at ' + datetime.now().strftime('%H:%M:%S') + '\n')
        log.write('\n')
        log.write('             Preprocessor: ' + preprocessor + '\n')
        log.write('\n')
        log.write('=====================================================================\n')
        log.write('\n')
    preprocessorFile = buildPreprocessorCall(preprocessor,functionCall,args,wd,logfilename)
    # create command
    command = 'run \'' + join(wd,preprocessorFile) + '\''
    # open preprocessor (matlab)
    with open(logfilename,'a') as log:
        log.write('Starting ' + preprocessor + '\n')
        log.write('\n')
    print('Starting ' + preprocessor + '\n')
    print('\n')
    try:
        h = win32com.client.Dispatch(preprocessor + '.application')
    except Exception,e:
        with open(logfilename,'a') as log:
            log.write('FAILED to start ' + preprocessor + '\n')
            log.write('\n')
            log.write(str(e) + '\n')
            log.write('\n')
        print('FAILED to start ' + preprocessor + '\n')
        print('\n')
        print(str(e) + '\n')
        print('\n')
        sendStatusEmail('D:/OneDrive/01_Luca/07_DocMASE/06_WD','logData.csv','smtp.univ-lorraine.fr','luca.di-stasio@univ-lorraine.fr','luca.distasio@gmail.com','ABAQUS PARAMETRIC RUN INTERRUPTED','Abaqus parametric run interrupted on ' + datetime.now().strftime('%Y-%m-%d') + ' at ' + datetime.now().strftime('%H:%M:%S') + '\n\n An error occurred. Details:\n' + str(e)+ '\n\n View log file for further info.')
        sys.exit()
    with open(logfilename,'a') as log:
        log.write('SUCCESS. ' + preprocessor + ' started.\n')
        log.write('\n')
    print('SUCCESS. ' + preprocessor + ' started.\n')
    print('\n')
    # execute command
    with open(logfilename,'a') as log:
        log.write('Executing command ' + command + '\n')
        log.write('\n')
    print('Executing command ' + command + '\n')
    print('\n')
    try:
        h.execute(command)
    except Exception,e:
        with open(logfilename,'a') as log:
            log.write('FAILED to execute ' + command + '\n')
            log.write('\n')
            log.write(str(Exception) + '\n')
            log.write('\n')
        print('FAILED to execute ' + command + '\n')
        print('\n')
        print(str(e) + '\n')
        print('\n')
        sendStatusEmail('D:/OneDrive/01_Luca/07_DocMASE/06_WD','logData.csv','smtp.univ-lorraine.fr','luca.di-stasio@univ-lorraine.fr','luca.distasio@gmail.com','ABAQUS PARAMETRIC RUN INTERRUPTED','Abaqus parametric run interrupted on ' + datetime.now().strftime('%Y-%m-%d') + ' at ' + datetime.now().strftime('%H:%M:%S') + '\n\n An error occurred. Details:\n' + str(e)+ '\n\n View log file for further info.')
        sys.exit()
    with open(logfilename,'a') as log:
        log.write('SUCCESS. ' + command + ' executed.\n')
        log.write('\n')
    print('SUCCESS. ' + command + ' executed.\n')
    print('\n')
    # get result
    variable = functionCall.split('=')[0]
    with open(logfilename,'a') as log:
        log.write('Extracting variable ' + variable + '\n')
        log.write('\n')
    print('Extracting variable ' + variable + '\n')
    print('\n')
    try:
        result = h.GetVariable(variable,"base")
    except Exception,e:
        with open(logfilename,'a') as log:
            log.write('FAILED to extract ' + variable + '\n')
            log.write('\n')
            log.write(str(e) + '\n')
            log.write('\n')
        print('FAILED to extract ' + variable + '\n')
        print('\n')
        print(str(e) + '\n')
        print('\n')
        sendStatusEmail('D:/OneDrive/01_Luca/07_DocMASE/06_WD','logData.csv','smtp.univ-lorraine.fr','luca.di-stasio@univ-lorraine.fr','luca.distasio@gmail.com','ABAQUS PARAMETRIC RUN INTERRUPTED','Abaqus parametric run interrupted on ' + datetime.now().strftime('%Y-%m-%d') + ' at ' + datetime.now().strftime('%H:%M:%S') + '\n\n An error occurred. Details:\n' + str(e)+ '\n\n View log file for further info.')
        sys.exit()
    with open(logfilename,'a') as log:
        log.write('SUCCESS. ' + variable + ' extracted.\n')
        log.write('\n')
    print('SUCCESS. ' + variable + ' extracted.\n')
    print('\n')
    # close preprocessor
    with open(logfilename,'a') as log:
        log.write('Closing ' + preprocessor + '\n')
        log.write('\n')
    print('Closing ' + preprocessor + '\n')
    print('\n')
    try:
        h.execute('exit')
    except Exception,e:
        with open(logfilename,'a') as log:
            log.write(preprocessor + ' CLOSED\n')
            log.write('\n')
        print(preprocessor + ' CLOSED\n')
        print('\n')
    print('\n')
    print('=====================================================================\n')
    print('\n')
    print('                 PREPROCESSING\n')
    print('\n')
    print('          Completed on ' + datetime.now().strftime('%Y-%m-%d') + ' at ' + datetime.now().strftime('%H:%M:%S') + '\n')
    print('\n')
    print('             Project Name: ' + result + '\n')
    print('\n')
    print('=====================================================================\n')
    print('\n')
    with open(logfilename,'a') as log:
        log.write('\n')
        log.write('=====================================================================\n')
        log.write('\n')
        log.write('                 PREPROCESSING\n')
        log.write('\n')
        log.write('          Completed on ' + datetime.now().strftime('%Y-%m-%d') + ' at ' + datetime.now().strftime('%H:%M:%S') + '\n')
        log.write('\n')
        log.write('             Project Name: ' + result + '\n')
        log.write('\n')
        log.write('=====================================================================\n')
        log.write('\n')
    return result



def buildAbaqusCall(wd,pname,cpus,mode,logfilename):
    cmdfile = join(wd,'runabaqusjob.cmd')
    with open(logfilename,'a') as log:
        log.write('Starting to write Windows command script to launch Abaqus.' + '\n')
        log.write('\n')
    print('Starting to write Windows command script to launch Abaqus.' + '\n')
    print('\n')
    try:
        with open(cmdfile,'w') as cmd:
            cmd.write('\n')
            cmd.write('CD ' + wd + '\\' + pname + '\\solver\n')
            cmd.write('\n')
            cmd.write('abaqus job=' + pname + ' analysis input=' + wd + '\\' + pname + '\\input\\' + pname + '.inp information=all ' + mode + ' cpus=' + cpus + '\n')
    except Exception,e:
        with open(logfilename,'a') as log:
            log.write('FAILED to write Windows command script.' + '\n')
            log.write('\n')
        print('FAILED to write Windows command script.' + '\n')
        print('\n')
        sendStatusEmail('D:/OneDrive/01_Luca/07_DocMASE/06_WD','logData.csv','smtp.univ-lorraine.fr','luca.di-stasio@univ-lorraine.fr','luca.distasio@gmail.com','ABAQUS PARAMETRIC RUN INTERRUPTED','Abaqus parametric run interrupted on ' + datetime.now().strftime('%Y-%m-%d') + ' at ' + datetime.now().strftime('%H:%M:%S') + '\n\n An error occurred. Details:\n' + str(e)+ '\n\n View log file for further info.')
        sys.exit()
    with open(logfilename,'a') as log:
        log.write('SUCCESS. Windows command script written.' + '\n')
        log.write('\n')
    print('SUCCESS. Windows command script written.' + '\n')
    print('\n')
    return cmdfile


def runAbaqusSolver(wd,projectName,cpus,runmode,logfilename,statusfilename):
    print('\n')
    print('=====================================================================\n')
    print('\n')
    print('                 FEM SIMULATION\n')
    print('\n')
    print('          Starting on ' + datetime.now().strftime('%Y-%m-%d') + ' at ' + datetime.now().strftime('%H:%M:%S') + '\n')
    print('\n')
    print('             FEM Solver: ' + 'Abaqus' + '\n')
    print('\n')
    print('             Project: ' + projectName + '\n')
    print('\n')
    print('=====================================================================\n')
    print('\n')
    with open(logfilename,'a') as log:
        log.write('\n')
        log.write('=====================================================================\n')
        log.write('\n')
        log.write('                 FEM SIMULATION\n')
        log.write('\n')
        log.write('          Starting on ' + datetime.now().strftime('%Y-%m-%d') + ' at ' + datetime.now().strftime('%H:%M:%S') + '\n')
        log.write('\n')
        log.write('             FEM Solver: ' + 'Abaqus' + '\n')
        log.write('\n')
        log.write('             Project: ' + projectName + '\n')
        log.write('\n')
        log.write('=====================================================================\n')
        log.write('\n')
    cmdfile = buildAbaqusCall(wd,projectName,cpus,runmode,logfilename)
    try:
        subprocess.call('cmd.exe /C ' + cmdfile,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    except Exception,e:
        print('FAILED to launch Abaqus.\n')
        print('\n')
        with open(logfilename,'a') as log:
            log.write('FAILED to launch Abaqus.\n')
            log.write('\n')
        sendStatusEmail('D:/OneDrive/01_Luca/07_DocMASE/06_WD','logData.csv','smtp.univ-lorraine.fr','luca.di-stasio@univ-lorraine.fr','luca.distasio@gmail.com','ABAQUS PARAMETRIC RUN ERROR','In Abaqus parametric run, error occurred on ' + datetime.now().strftime('%Y-%m-%d') + ' at ' + datetime.now().strftime('%H:%M:%S') + '\n\n Details:\n' + str(e)+ '\n\n View log file for further info.')
    print('SUCCESS. Abaqus simulation started.\n')
    print('\n')
    with open(logfilename,'a') as log:
        log.write('SUCCESS. Abaqus simulation started.\n')
        log.write('\n')
    sleep(600)
    while isfile(join(wd,projectName,'solver',projectName+'.lck')) or isfile(join(wd,projectName,'solver',projectName+'.023')):
        sleep(300)
    print('\n')
    print('=====================================================================\n')
    print('\n')
    print('                 FEM SIMULATION\n')
    print('\n')
    print('          Completed on ' + datetime.now().strftime('%Y-%m-%d') + ' at ' + datetime.now().strftime('%H:%M:%S') + '\n')
    print('\n')
    print('             Project: ' + projectName + '\n')
    print('\n')
    print('=====================================================================\n')
    print('\n')
    with open(logfilename,'a') as log:
        log.write('\n')
        log.write('=====================================================================\n')
        log.write('\n')
        log.write('                 FEM SIMULATION\n')
        log.write('\n')
        log.write('          Completed on ' + datetime.now().strftime('%Y-%m-%d') + ' at ' + datetime.now().strftime('%H:%M:%S') + '\n')
        log.write('\n')
        log.write('             Project: ' + projectName + '\n')
        log.write('\n')
        log.write('=====================================================================\n')
        log.write('\n')
    with open(statusfilename,'r') as sta:
        lines = sta.readlines()
    with open(statusfilename,'w') as sta:
        for line in lines:
            if projectName in line:
                parts = line.split(',')
                parts[2] = ' YES'
                line = ''
                for i,part in enumerate(parts):
                    if i>0:
                        line += ','
                    line += part
                sta.write(line)
            else:
                sta.write(line)

def iteratePreprocessor(iterables,arguments,preprocessor,functionCall,wd,logfilename,statusfilename):
    if len(iterables)>0:
        if len(iterables)>1:
            iterable = iterables[0]
            for i in arange(iterable[1],iterable[2]+iterable[3],iterable[3]):
                arguments[iterable[0]] = [i,iterable[4]]
                iteratePreprocessor(iterables[1:],arguments,preprocessor,functionCall,wd,logfilename,statusfilename)
        else:
            iterable = iterables[0]
            for i in arange(iterable[1],iterable[2]+iterable[3],iterable[3]):
                arguments[iterable[0]] = [i,iterable[4]]
                projectname = runPreprocessor(preprocessor,functionCall,arguments,wd,logfilename)
                if 'A model with this set of parameters already exists. See:' not in projectname:
                    with open(statusfilename,'a') as sta:
                        sta.write(projectname  + ', YES, NO, NO\n')
                else:
                    isOdb = False
                    filesInABQfolder = listdir(join(wd,projectname.replace(' ','').replace('\n','').split(':')[1],'solver'))
                    for file in filesInABQfolder:
                        if '.odb' in file:
                            isOdb = True
                            break
                    if isOdb:
                        with open(statusfilename,'a') as sta:
                            sta.write(projectname  + ', YES, YES, NO\n')
                    else:
                        with open(statusfilename,'a') as sta:
                            sta.write(projectname  + ', YES, NO, NO\n')
    else:
        projectname = runPreprocessor(preprocessor,functionCall,arguments,wd,logfilename)
        if 'A model with this set of parameters already exists. See:' not in projectname:
            with open(statusfilename,'a') as sta:
                sta.write(projectname  + ', YES, NO, NO\n')
        else:
            isOdb = False
            filesInABQfolder = listdir(join(wd,projectname.replace(' ','').replace('\n','').split(':')[1],'solver'))
            for file in filesInABQfolder:
                if '.odb' in file:
                    isOdb = True
                    break
            if isOdb:
                with open(statusfilename,'a') as sta:
                    sta.write(projectname  + ', YES, YES, NO\n')
            else:
                with open(statusfilename,'a') as sta:
                    sta.write(projectname  + ', YES, NO, NO\n')

def iterateFemSolver(wd,solverInputs,logfilename,statusfilename):
    cpunum = None
    mode = None
    for input in solverInputs:
        if 'cpus' in input:
            cpunum = input[1]
        elif 'mode' in input:
            mode = input[1]
    if cpunum is None:
        cpunum = '8'
    if mode is None:
        mode = 'background'
    with open(statusfilename,'r') as sta:
        lines = sta.readlines()
    count = 0
    for i,line in enumerate(lines):
        if i>0:
            parts = line.split(',')
            if 'NO' in parts[2]:
                count += 1
            if i==1 and 'NO' in parts[2]:
                projectName = parts[0]
            elif i>1:
                previousParts = lines[i-1].split(',')
                if 'NO' in parts[2] and 'YES' in previousParts[2]:
                    projectName = parts[0]
    while count>0:
        runAbaqusSolver(wd,projectName,cpunum,mode,logfilename,statusfilename)
        with open(statusfilename,'r') as sta:
            lines = sta.readlines()
        count = 0
        for i,line in enumerate(lines):
            if i>0:
                parts = line.split(',')
                if 'NO' in parts[2]:
                    count += 1
                if i==1 and 'NO' in parts[2]:
                    projectName = parts[0]
                elif i>1:
                    previousParts = lines[i-1].split(',')
                    if 'NO' in parts[2] and 'YES' in previousParts[2]:
                        projectName = parts[0]

def readInputDeck(inpFile,inpDir,logfilename):
    preprocessorPlatform = ''
    preprocessorFunction = ''
    solver = ''
    solverInputs = []
    preprocessorInputs = []
    unitConvFactors = []
    iterablePreParams = []
    iterableSolverParams = []
    lineStartUnitConv = -1
    lineStopUnitConv = -1
    positionUnitConv = -1
    lineStartPrePar = -1
    lineStopPrePar = -1
    lineStartSolPar = -1
    lineStopSolPar = -1
    with open(logfilename,'a') as log:
        log.write('Reading input deck file ' + inpFile + ' from ' + inpDir + '\n')
        log.write('')
    print('Reading input deck file ' + inpFile + ' from ' + inpDir + '\n')
    print('')
    try:
        with open(join(inpDir,inpFile),'r') as file:
            lines = file.readlines();
        with open(logfilename,'a') as log:
            log.write('SUCCESS. Input deck file read.' + '\n')
            log.write('\n')
        print('SUCCESS. Input deck file read.' + '\n')
        print('\n')
    except Exception,e:
        with open(logfilename,'a') as log:
            log.write('FAILED. Error occurred.\n')
            log.write('\n')
            log.write(str(Exception) + '\n')
            log.write('\n')
        print('FAILED. Error occurred.\n')
        print('\n')
        print(str(e) + '\n')
        print('\n')
        sendStatusEmail('D:/OneDrive/01_Luca/07_DocMASE/06_WD','logData.csv','smtp.univ-lorraine.fr','luca.di-stasio@univ-lorraine.fr','luca.distasio@gmail.com','ABAQUS PARAMETRIC RUN INTERRUPTED','Abaqus parametric run interrupted on ' + datetime.now().strftime('%Y-%m-%d') + ' at ' + datetime.now().strftime('%H:%M:%S') + '\n\n An error occurred. Details:\n' + str(e)+ '\n\n View log file for further info.')
        sys.exit()
    with open(logfilename,'a') as log:
        log.write('Start assigning input values to corresponding parameters\n')
        log.write('\n')
    print('Start assigning input values to corresponding parameters\n')
    print('\n')
    for i,line in enumerate(lines):
        if 'ITERABLE PREPROCESSOR PARAMETERS' in line:
            [name,param] = line.split(':')
            iterablePreParams = [None]*int(param)
            with open(logfilename,'a') as log:
                log.write('ITERABLE PREPROCESSOR PARAMETERS: ' + str(len(iterablePreParams)) + '\n')
                log.write('\n')
            print('ITERABLE PREPROCESSOR PARAMETERS: ' + str(len(iterablePreParams)) + '\n')
            print('\n')
        elif 'ITERABLE SOLVER PARAMETERS' in line:
            [name,param] = line.split(':')
            iterableSolverParams = [None]*int(param)
            with open(logfilename,'a') as log:
                log.write('ITERABLE SOLVER PARAMETERS: ' + str(len(iterableSolverParams)) + '\n')
                log.write('\n')
            print('ITERABLE SOLVER PARAMETERS: ' + str(len(iterableSolverParams)) + '\n')
            print('\n')
        elif 'PREPROCESSOR PLATFORM' in line:
            [name,param] = line.split(':')
            preprocessorPlatform = param.replace(' ','').replace('\n','').replace('\t','')
            with open(logfilename,'a') as log:
                log.write('PREPROCESSOR: ' + preprocessorPlatform + '\n')
                log.write('\n')
            print('PREPROCESSOR: ' + preprocessorPlatform + '\n')
            print('\n')
        elif 'PREPROCESSOR FUNCTION CALL' in line:
            [name,param] = line.split(':')
            preprocessorFunction = param.replace(' ','').replace('\n','').replace('\t','')
            with open(logfilename,'a') as log:
                log.write('PREPROCESSOR FUNCTION CALL: ' + preprocessorFunction + '\n')
                log.write('\n')
            print('PREPROCESSOR FUNCTION CALL: ' + preprocessorFunction + '\n')
            print('\n')
        elif 'TOTAL NUMBER OF PARAMETERS' in line:
            [name,param] = line.split(':')
            preprocessorInputs = [None]*int(param)
            with open(logfilename,'a') as log:
                log.write('TOTAL NUMBER OF PARAMETERS: ' + str(len(preprocessorInputs)) + '\n')
                log.write('\n')
            print('TOTAL NUMBER OF PARAMETERS: ' + str(len(preprocessorInputs)) + '\n')
            print('\n')
        elif 'TOTAL NUMBER OF UNIT CONVERSION FACTORS' in line:
            [name,param] = line.split(':')
            unitConvFactors = [None]*int(param)
            lineStartUnitConv = i + 1
            with open(logfilename,'a') as log:
                log.write('TOTAL NUMBER OF UNIT CONVERSION FACTORS: ' + str(len(unitConvFactors)) + '\n')
                log.write('\n')
            print('TOTAL NUMBER OF UNIT CONVERSION FACTORS: ' + str(len(unitConvFactors)) + '\n')
            print('\n')
        elif 'CALLING ORDER NUMBER OF UNIT CONVERSION FACTORS' in line:
            [name,param] = line.split(':')
            positionUnitConv = int(param)
            lineStopUnitConv = i - 1
            with open(logfilename,'a') as log:
                log.write('CALLING ORDER NUMBER OF UNIT CONVERSION FACTORS: ' + str(positionUnitConv) + '\n')
                log.write('\n')
            print('CALLING ORDER NUMBER OF UNIT CONVERSION FACTORS: ' + str(positionUnitConv) + '\n')
            print('\n')
        elif 'FEM SOLVER PLATFORM' in line:
            [name,param] = line.split(':')
            solver = param.replace(' ','').replace('\n','').replace('\t','')
            with open(logfilename,'a') as log:
                log.write('FEM SOLVER: ' + solver + '\n')
                log.write('\n')
            print('FEM SOLVER: ' + solver + '\n')
            print('\n')
        elif 'START PREPROCESSOR PARAMETERS' in line:
            lineStartPrePar = i + 1
        elif 'END PREPROCESSOR PARAMETERS' in line:
            lineStopPrePar = i
        elif 'START FEM SOLVER PARAMETERS' in line:
            lineStartSolPar = i + 1
        elif 'END FEM SOLVER PARAMETERS' in line:
            lineStopSolPar = i
    for i in range(lineStartUnitConv+1,lineStopUnitConv):
        line = lines[i]
        parts = line.split(',')
        index = int(parts[1])
        value = parts[2].replace(' ','')
        unitConvFactors[index] = str(10**(-int(value)))
    preprocessorInputs[positionUnitConv] = [unitConvFactors,'Vector']
    for i in range(lineStartPrePar+1,lineStopPrePar):
        line = lines[i]
        parts = line.split(',')
        if 'Integer' in parts[8] or 'Boolean' in parts[8]:
            preprocessorInputs[int(parts[1])] = [str(int(parts[4])),parts[8].replace(' ','').replace('\n','').replace('\t','')]
            if 'Yes' in parts[2]:
                iterablePreParams[int(parts[3])] = [int(parts[1]),int(parts[4]),int(parts[5]),int(parts[6]),'Integer']
        elif 'Real' in parts[8]:
            if 'theta'==parts[0].replace(' ','').replace('\n','').replace('\t','') or 'deltatheta'==parts[0].replace(' ','').replace('\n','').replace('\t','') or 'phi'==parts[0].replace(' ','').replace('\n','').replace('\t',''):
                factor = math.pi/180.
            else:
                factor = 1
            preprocessorInputs[int(parts[1])] = [str(factor*float(parts[4])),parts[8].replace(' ','').replace('\n','').replace('\t','')]
            if 'Yes' in parts[2]:
                iterablePreParams[int(parts[3])] = [int(parts[1]),factor*float(parts[4]),factor*float(parts[5]),factor*float(parts[6]),'Real']
        else:
            preprocessorInputs[int(parts[1])] = [parts[4].replace(' ','').replace('\n','').replace('\t',''),parts[8].replace(' ','').replace('\n','').replace('\t','')]
    for i in range(lineStartSolPar+1,lineStopSolPar):
        line = lines[i]
        parts = line.split(',')
        if 'No' in parts[1]:
            solverInputs.append([parts[0].replace(' ','').replace('\n','').replace('\t',''),parts[3].replace(' ','').replace('\n','').replace('\t','')])
        else:
            solverInputs.append([parts[0].replace(' ','').replace('\n','').replace('\t',''),parts[3].replace(' ','').replace('\n','').replace('\t','')])
            if 'Integer' in parts[7] or 'Boolean' in parts[7]:
                iterableSolverParams[int(parts[2])] = [parts[0].replace(' ','').replace('\n','').replace('\t',''),int(parts[3]),int(parts[4]),int(parts[5])]
            elif 'Real' in parts[7]:
                iterableSolverParams[int(parts[2])] = [parts[0].replace(' ','').replace('\n','').replace('\t',''),float(parts[3]),float(parts[4]),float(parts[5])]
    totalSIMS = 0
    for iterable in iterablePreParams:
        totalSIMS += (iterable[2]+iterable[3]-iterable[1])/iterable[3]
    with open(logfilename,'a') as log:
        log.write('TOTAL NUMBER OF SIMULATIONS: ' + str(totalSIMS) + '\n')
        log.write('\n')
        log.write('Assignment step COMPLETED\n')
        log.write('\n')
    print('Assignment step COMPLETED\n')
    print('\n')
    return preprocessorPlatform,preprocessorFunction,solver,solverInputs,preprocessorInputs,unitConvFactors,iterablePreParams,iterableSolverParams



def main(argv):

    # Read the command line, throw error if not option is provided
    try:
        opts, args = getopt.getopt(argv,'hi:d:w:s:p:',['help','Help',"inputfile", "input","inpdir", "inputdirectory", "idir","workdir", "workdirectory", "wdir","abqonly","preonly"])
    except getopt.GetoptError:
        print('runAbaqus.py -i <input deck> -d <input directory> -w <working directory> -s <status file>')
        sys.exit(2)
    # Parse the options and create corresponding variables
    for opt, arg in opts:
        if opt in ('-h', '--help','--Help'):
            print(' ')
            print(' ')
            print('*****************************************************************************************************')
            print(' ')
            print('                                   ABAQUS PARAMETRIC SIMULATION')
            print(' ')
            print(' ')
            print('                                              by')
            print(' ')
            print('                                    Luca Di Stasio, 2016-2017')
            print(' ')
            print(' ')
            print('*****************************************************************************************************')
            print(' ')
            print('Program syntax:')
            print('runAbaqus.py -i <input deck> -d <input directory> -w <working directory> -s <status file for abaqus only> -p <preprocessor>')
            print(' ')
            print('Mandatory arguments:')
            print('-i <input deck>')
            print('-d <input directory>')
            print(' ')
            print('Optional arguments:')
            print('-w <working directory>')
            print('-s <status file>')
            print('-p <preprocessor only>')
            print(' ')
            print('Default values:')
            print('-w <working directory>                ===> same as input directory')
            print(' ')
            print(' ')
            sys.exit()
        elif opt in ("-i", "--inputfile", "--input"):
            parts = arg.split(".")
            if len(parts) > 1:
                inputfile = arg
                subparts = parts[0].split('_')
                logfile = subparts[0] + '_AbaqusParametricRun_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log'
                statusfile = subparts[0] + '_AbaqusParametricRun_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.sta'
            else:
                inputfile = arg + '.csv'
                subparts = arg.split('_')
                logfile = subparts[0] + '_AbaqusParametricRun_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log'
                statusfile = subparts[0] + '_AbaqusParametricRun_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.sta'
        elif opt in ("-d", "--inpdir", "--inputdirectory", "--idir"):
            if arg[-1] != '/':
                inputdir = arg
            else:
                inputdir = arg[:-1]
        elif opt in ("-w", "--workdir", "--workdirectory", "--wdir"):
            if arg[-1] != '/':
                workdir = arg
            else:
                workdir = arg[:-1]
        elif opt in ("-s", "--abqonly"):
            statusfile = arg
            abqonly = True
        elif opt in ("-p", "--preonly"):
            preonly = True

    # Check the existence of variables: if a required variable is missing, an error is thrown and program is terminated; if an optional variable is missing, it is set to the default value
    if 'inputdir' not in locals():
        print('Error: input directory not provided.')
        sys.exit()
    if 'inputfile' not in locals():
        print('Error: input directory not provided.')
        sys.exit()
    if 'workdir' not in locals():
        workdir = inputdir
    if 'abqonly' not in locals():
        abqonly = False
    if 'preonly' not in locals():
        preonly = False

    logfilePath = join(workdir,logfile)
    with open(logfilePath,'w') as log:
        log.write('===============================================================================================\n')
        log.write('===============================================================================================\n')
        log.write('\n')
        log.write('                                     ABAQUS PARAMETRIC RUN\n')
        log.write('\n')
        log.write('                             Starting on ' + datetime.now().strftime('%Y-%m-%d') + ' at ' + datetime.now().strftime('%H:%M:%S') + '\n')
        log.write('\n')
        log.write('                               Platform: ' + platform() + '\n')
        log.write('\n')
        log.write('===============================================================================================\n')
        log.write('===============================================================================================\n')
        log.write('\n')
    print('===============================================================================================\n')
    print('===============================================================================================\n')
    print('\n')
    print('                                           ABAQUS PARAMETRIC RUN\n')
    print('\n')
    print('                                 Starting on ' + datetime.now().strftime('%Y-%m-%d') + ' at ' + datetime.now().strftime('%H:%M:%S') + '\n')
    print('\n')
    print('                                      Platform: ' + platform() + '\n')
    print('\n')
    print('===============================================================================================\n')
    print('===============================================================================================\n')
    print('\n')

    statusfilePath = join(workdir,statusfile)

    if abqonly:
        sendStatusEmail('D:/OneDrive/01_Luca/07_DocMASE/06_WD','logData.csv','smtp.univ-lorraine.fr','luca.di-stasio@univ-lorraine.fr','luca.distasio@gmail.com','ABAQUS PARAMETRIC RUN','Abaqus parametric run starting on ' + datetime.now().strftime('%Y-%m-%d') + ' at ' + datetime.now().strftime('%H:%M:%S') + '\n\nPreprocessor: none (Abaqus only)')

        iterateFemSolver(workdir,[],logfilePath,statusfilePath)
    elif preonly:
        with open(statusfilePath,'w') as sta:
            sta.write('PROJECT NAME, PREPROCESSING, FEM SOLVER, POST PROCESSING\n')

        preprocessorPlatform,preprocessorFunction,solver,solvInputs,preprocessorInputs,unitConvFactors,iterablePreParams,iterableSolverParams = readInputDeck(inputfile,inputdir,logfilePath)

        sendStatusEmail('D:/OneDrive/01_Luca/07_DocMASE/06_WD','logData.csv','smtp.univ-lorraine.fr','luca.di-stasio@univ-lorraine.fr','luca.distasio@gmail.com','ABAQUS PARAMETRIC RUN','Abaqus parametric run starting on ' + datetime.now().strftime('%Y-%m-%d') + ' at ' + datetime.now().strftime('%H:%M:%S') + '\n\nPreprocessor: '+ preprocessorPlatform)

        iteratePreprocessor(iterablePreParams,preprocessorInputs,preprocessorPlatform,preprocessorFunction,workdir,logfilePath,statusfilePath)

        sendStatusEmail('D:/OneDrive/01_Luca/07_DocMASE/06_WD','logData.csv','smtp.univ-lorraine.fr','luca.di-stasio@univ-lorraine.fr','luca.distasio@gmail.com','ABAQUS PARAMETRIC RUN','Pre-processing successfully completed on ' + datetime.now().strftime('%Y-%m-%d') + ' at ' + datetime.now().strftime('%H:%M:%S') + '.')
    else:
        with open(statusfilePath,'w') as sta:
            sta.write('PROJECT NAME, PREPROCESSING, FEM SOLVER, POST PROCESSING\n')

        preprocessorPlatform,preprocessorFunction,solver,solvInputs,preprocessorInputs,unitConvFactors,iterablePreParams,iterableSolverParams = readInputDeck(inputfile,inputdir,logfilePath)

        sendStatusEmail('D:/OneDrive/01_Luca/07_DocMASE/06_WD','logData.csv','smtp.univ-lorraine.fr','luca.di-stasio@univ-lorraine.fr','luca.distasio@gmail.com','ABAQUS PARAMETRIC RUN','Abaqus parametric run starting on ' + datetime.now().strftime('%Y-%m-%d') + ' at ' + datetime.now().strftime('%H:%M:%S') + '\n\nPreprocessor: '+ preprocessorPlatform)

        iteratePreprocessor(iterablePreParams,preprocessorInputs,preprocessorPlatform,preprocessorFunction,workdir,logfilePath,statusfilePath)

        sendStatusEmail('D:/OneDrive/01_Luca/07_DocMASE/06_WD','logData.csv','smtp.univ-lorraine.fr','luca.di-stasio@univ-lorraine.fr','luca.distasio@gmail.com','ABAQUS PARAMETRIC RUN','Pre-processing successfully completed on ' + datetime.now().strftime('%Y-%m-%d') + ' at ' + datetime.now().strftime('%H:%M:%S') + '. Starting Abaqus simulations.')

        iterateFemSolver(workdir,solvInputs,logfilePath,statusfilePath)

        sendStatusEmail('D:/OneDrive/01_Luca/07_DocMASE/06_WD','logData.csv','smtp.univ-lorraine.fr','luca.di-stasio@univ-lorraine.fr','luca.distasio@gmail.com','ABAQUS PARAMETRIC RUN','Abaqus simulations completed on ' + datetime.now().strftime('%Y-%m-%d') + ' at ' + datetime.now().strftime('%H:%M:%S'))



if __name__ == "__main__":
    main(sys.argv[1:])
