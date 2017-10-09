#!/usr/bin/env Python
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

from os import listdir, remove
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
from sendStatusEmail import getUser, getPwd, sendStatusEmail

def intToPaddedString(anInteger,numOfDigits):
    rawString = str(anInteger)
    resString = ''
    stringLength = len(rawString)
    if stringLength<numOfDigits:
        for i in range(0,numOfDigits-stringLength):
            rawString = '0' + rawString
    return rawString

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

def readSettingsFile(filepath):
    settingsDict = {}
    with open(filepath,'r') as f:
        lines = f.readlines()
    for line in lines:
        if '#' not in line:
            parts = line.replace('\n','').split(',')
            settingsDict[parts[0]] = parts[1]
    return settingsDict

def buildPostprocessorCall(params,codeDir,wd,logfile):
    templateFile = join(codeDir,'python','templateAnalyzeABQoutputData.py')
    postprocessor = join(wd,'postprocessor.py')
    skipLineToLogFile(logFilePath,'a',True)
    writeLineToLogFile(logFilePath,'a','Reading template file ' + templateFile,True)
    with open(templateFile,'r') as template:
        lines = template.readlines()
    with open(postprocessor,'w') as post:
        for line in lines:
            post.write(line)
        post.write('' + '\n')
        post.write('' + '\n')
        post.write('def main(argv):' + '\n')
        post.write('' + '\n')
        post.write('    extractFromODBoutputSet04(workdir,proj,matfolder,1,20,1,settings[0])' + '\n')
        post.write('' + '\n')
        post.write('if __name__ == "__main__":' + '\n')
        post.write('    main(sys.argv[1:])' + '\n')
    return postprocessor
    
def runPostprocessor(preprocessor,functionCall,args,wd,logfilename):
    
def main(argv):

    # Read the command line, throw error if not option is provided
    try:
        opts, args = getopt.getopt(argv,'h:m:p:e:w:s:',["help","Help","parametersfile", "settingsfile","matdir", "materialdirectory", "mdir","workdir", "workdirectory", "wdir","extractionset","statusfile","clear"])
    except getopt.GetoptError:
        print(' ')
        print('analyzeABQoutputData.py -m <material folder> -p <parameter settings file> -e <extraction set> -w <working directory> -s <status file(s)>')
        print(' ')
        print('analyzeABQoutputData.py -h --help --Help for help on this program')
        print(' ')
        sys.exit(2)
    # Parse the options and create corresponding variables
    for opt, arg in opts:
        if opt in ('-h', '--help','--Help'):
            print(' ')
            print(' ')
            print('*****************************************************************************************************')
            print(' ')
            print('                                    ABAQUS RESULTS ANALYSIS')
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
            print('analyzeABQoutputData.py -b <codebase> -m <material folder> -p <parameter settings file> -e <extraction set> -w <working directory> -s <status file(s)> -c <files to clear>')
            print(' ')
            print('Mandatory arguments:')
            print('-b <codebase>                     ===> full/path/to/folder/without/closing/slash')
            print('-m <material folder>              ===> full/path/to/folder/without/closing/slash')
            print('-p <parameter settings file>      ===> full/path/to/file/with/extension')
            print('-e <extraction set>               ===> integer number representing set of extraction operations')
            print('-w <working directory>            ===> full/path/to/folder/without/closing/slash')
            print('-s <status file(s)>               ===> relative/path/to/file/with/extension with respect to working directory')
            print('                                       if multiple files are provided, they must be separated by a ;, for example:')
            print('                                          statusOne.sta;statusTwo.sta;statusThree.sta')
            print(' ')
            print('Optional arguments:')
            print('-c <files to clear>')
            print(' ')
            print('Default values:')
            print('-c <files to clear>                ===> no file is cleared')
            print('                                        file extensions must be provided without leading dots')
            print('                                        if multiple file extensions are provided, they must be separated by a ;, for example:')
            print('                                           ext1;ext2;ext3')
            print(' ')
            print('Available extraction sets:')
            print('    01 - 2D LEFM single fiber, single debond, full extraction')
            print(' ')
            print(' ')
            sys.exit()
        elif opt in ("-p", "--parametersfile", "--settingsfile"):
            parts = arg.split(".")
            if len(parts) > 1:
                settingsfile = arg
            else:
                settingsfile = arg + '.csv'
        elif opt in ("-b", "--codebase"):
            if arg[-1] != '/':
                codedir = arg
            else:
                codedir = arg[:-1]
        elif opt in ("-m", "--matdir", "--materialdirectory", "--mdir"):
            if arg[-1] != '/':
                matdir = arg
            else:
                matdir = arg[:-1]
        elif opt in ("-w", "--workdir", "--workdirectory", "--wdir"):
            if arg[-1] != '/':
                workdir = arg
            else:
                workdir = arg[:-1]
        elif opt in ("-e", "--extractionset"):
            extractionSet = arg
        elif opt in ("-s", "--statusfile"):
            parts = arg.split(";")
            if len(parts) > 1:
                statusfiles = parts
                statusfile = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '_ABQdataAnalysis_CollectiveStatusFile.sta'
                collect = True
            else:
                statusfile = arg
                collect = False
        elif opt in ("-c", "--clear"):
            clearFiles = True
            filesToClear = arg.split(";")

    # Check the existence of variables: if a required variable is missing, an error is thrown and program is terminated; if an optional variable is missing, it is set to the default value
    if 'codedir' not in locals():
        print('Error: codebase directory not provided.')
        sys.exit(2)
    if 'matdir' not in locals():
        print('Error: materials data directory not provided.')
        sys.exit(2)
    if 'settingsfile' not in locals():
        print('Error: settings file not provided.')
        sys.exit(2)
    if 'workdir' not in locals():
        print('Error: working directory not provided.')
        sys.exit(2)
    if 'extractionSet' not in locals():
        print('Error: extraction set not provided.')
        sys.exit(2)
    if 'statusfile' not in locals():
        print('Error: status file not provided.')
        sys.exit(2)
    if 'clearFiles' not in locals():
        clearFiles = False
    
    statusfilepath = join(workdir,statusfile)
    
    if collect:
        with open(join(workdir,statusfiles[0]),'r') as inpSta:
            lines = inpSta.readlines()
        with open(statusfilepath,'w') as outSta:
            outSta.write(lines[0])
        for staFile in statusfiles:
            with open(join(workdir,staFile),'r') as inpSta:
                lines = inpSta.readlines()
            with open(statusfilepath,'a') as outSta:
                for line in lines[1:]:
                    outSta.write(line)
    
    
    logfile = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '_ABQdataAnalysis' + '.log'        
    logfilePath = join(workdir,logfile)

    # create log file
    writeTitleSecToLogFile(logFilePath,'w','ABAQUS RESULTS ANALYSIS',True)
    
    skipLineToLogFile(logFilePath,'a',True)
    writeLineToLogFile(logFilePath,'a','Reading settings ...',True)
    settings = readSettingsFile(settingsfile)
    writeLineToLogFile(logFilePath,'a','... done.',True)
    
    subject = '[ABAQUS RESULTS ANALYSIS] Starting analysis'
    message = 'Abaqus results analysis starting on ' + datetime.now().strftime('%Y-%m-%d') + ' at ' + datetime.now().strftime('%H:%M:%S').'
    sendStatusEmail(settings['emailDataDir'],'logData.csv',settings['serverFrom'],settings['emailFrom'],settings['emailTo'],subject,message)
    
    skipLineToLogFile(logFilePath,'a',True)
    writeLineToLogFile(logFilePath,'a','Starting reading list of simulations from status file ...',True)
    with open(statusfilepath,'r') as sta:
        lines = sta.readlines()
    writeLineToLogFile(logFilePath,'a','... done.',True)
    
    for line in lines[1:]:
        simData = line.replace('\n','').split(',')
        simName = simData[0]
        isPreprocessed = simData[1]
        isSimCompleted = simData[2]
        isPostprocessed = simData[3]
        skipLineToLogFile(logFilePath,'a',True)
        writeLineToLogFile(logFilePath,'a','For simulation: ' + simName,True)
        writeLineToLogFile(logFilePath,'a','    --> has the preprocessing stage been completed? ' + isPreprocessed,True)
        writeLineToLogFile(logFilePath,'a','    --> has the simulation stage been completed? ' + isSimCompleted,True)
        writeLineToLogFile(logFilePath,'a','    --> has the postprocessing stage been completed? ' + isPostprocessed,True)
        if isPreprocessed=='YES' and isSimCompleted=='YES' and isPostprocessed=='NO':
            writeLineToLogFile(logFilePath,'a','    ooo PREPROCESSING AND SIMULATION STAGES ALREADY EXECUTED, POSTPROCESSING STILL TO BE DONE ooo',True)
            skipLineToLogFile(logFilePath,'a',True)
            writeLineToLogFile(logFilePath,'a','Starting postprocessing on simulation ' + simName + ' ...',True)
            writeLineToLogFile(logFilePath,'a','Calling function: buildPostProcessorCall ...',True)
            try:
                postProcessorFile = buildPostprocessorCall(settings,codedir,workdir,logFilePath)
            except Exception, error:
                writeErrorToLogFile(logFilePath,'a',Exception,error,True)
                writeLineToLogFile(logFilePath,'a','Moving on to the next.',True)
                sys.exc_clear()
                continue
            writeLineToLogFile(logFilePath,'a','... done.',True)
            writeLineToLogFile(logFilePath,'a','Calling function: runPostprocessor ...',True)
            try:
                runPostprocessor(preprocessor,functionCall,args,wd,logfilename)
            except Exception, error:
                writeErrorToLogFile(logFilePath,'a',Exception,error,True)
                writeLineToLogFile(logFilePath,'a','Moving on to the next.',True)
                sys.exc_clear()
                continue
            writeLineToLogFile(logFilePath,'a','... done.',True)
            if clearFiles:
                writeLineToLogFile(logFilePath,'a','Proceeding to clear files in ' + str(join(wd,simName,'solver')) + ' ...',True)
                fileList = listdir(join(wd,simName,'solver'))
                for filename in fileList:
                    if isfile(join(wd,simName,'solver',filename)) and filename.split('.')[1] in filesToClear:
                        writeLineToLogFile(logFilePath,'a','File ' + filename + ' needs to be removed ...',True)
                        try:
                            remove(join(wd,simName,'solver',filename))
                        except Exception, error:
                            writeErrorToLogFile(logFilePath,'a',Exception,error,True)
                            writeLineToLogFile(logFilePath,'a','Moving on to the next.',True)
                            sys.exc_clear()
                            continue
                        writeLineToLogFile(logFilePath,'a','... done.',True)
                writeLineToLogFile(logFilePath,'a','... done.',True)
            writeLineToLogFile(logFilePath,'a','... done.',True)
        elif isPreprocessed=='NO':
            writeLineToLogFile(logFilePath,'a','    ==> PREPROCESSING AND SIMULATION STAGES STILL NEED TO BE EXECUTED <==',True)
            writeLineToLogFile(logFilePath,'a','    Moving on to the next.',True)
        elif isPreprocessed=='YES' and isSimComplted=='NO':
            writeLineToLogFile(logFilePath,'a','    ==> SIMULATION STAGE STILL NEED TO BE EXECUTED <==',True)
            writeLineToLogFile(logFilePath,'a','    Moving on to the next.',True)
        elif isPreprocessed=='YES' and isSimComplted=='YES' and isPostprocessed=='YES':
            writeLineToLogFile(logFilePath,'a','    ==> POSTPROCESSING STAGE ALREADY EXECUTED <==',True)
            writeLineToLogFile(logFilePath,'a','    Moving on to the next.',True)
        else:
            writeLineToLogFile(logFilePath,'a','    !!! UNKNOWN ERROR WHILE PARSING LINE OF DATA !!!',True)
            writeLineToLogFile(logFilePath,'a','    Moving on to the next.',True)


if __name__ == "__main__":
    main(sys.argv[1:])
    