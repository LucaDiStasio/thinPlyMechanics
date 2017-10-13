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
from platform import platform,system
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
    analysisDict = {}
    analysisList = []
    with open(filepath,'r') as f:
        lines = f.readlines()
    startSettingsLines = 0
    endSettingsLines = 0
    startAnalysisLines = 0
    endAnalysisLines = 0
    for l,line in enumerate(lines):
        if 'BEGIN SETTINGS' in line:
            startSettingsLines = l
        elif 'END SETTINGS' in line:
            endSettingsLines = l
        elif 'BEGIN ANALYSIS SECTIONS' in line:
            startAnalysisLines = l
        elif 'END ANALYSIS SECTIONS' in line:
            endAnalysisLines = l
    for line in lines[startSettingsLines:endSettingsLines]:
        if '#' not in line:
            parts = line.replace('\n','').split(',')
            settingsDict[parts[0]] = parts[1]
    for line in lines[startAnalysisLines:endAnalysisLines]:
        if '#' not in line:
            parts = line.replace('\n','').split(',')
            analysisList.append(parts[0])
            if 'YES' in parts[1]:
                analysisDict[parts[0]] = 1
            else:
                analysisDict[parts[0]] = 0
    return settingsDict,analysisList,analysisDict

def buildPostprocessorCall(params,analysisList,analysisDict,extSet,sim,codeDir,wd,matfolder,logfile,logfilename):
    templateFile = join(codeDir,'templateAnalyzeABQoutputData.py')
    postprocessor = join(wd,'postprocessor.py')
    skipLineToLogFile(logfile,'a',True)
    writeLineToLogFile(logfile,'a','Reading template file ' + templateFile,True)
    with open(templateFile,'r') as template:
        lines = template.readlines()
    writeToPost = True
    with open(postprocessor,'w') as post:
        for line in lines:
            if '#' in line and 'BEGIN' in line:
                sectionName = line.replace('\n','').split('-')[1].strip()
                if analysisDict[sectionName]:
                    writeToPost = True
                else:
                    writeToPost = False
            elif '#' in line and 'END' in line:
                writeToPost = True
            if writeToPost:
                post.write(line)
        post.write('' + '\n')
        post.write('' + '\n')
        post.write('def main(argv):' + '\n')
        post.write('' + '\n')
        post.write('    workdir = \'' + wd + '\'' + '\n')
        post.write('    matdir = \'' + matfolder + '\'' + '\n')
        post.write('    proj = \'' + sim + '\'' + '\n')
        post.write('    logfile = \'' + logfilename + '\'' + '\n')
        post.write('    logfilePath = join(workdir,logfile)' + '\n')
        post.write('' + '\n')
        post.write('    settingsData = {}' + '\n')
        post.write('    settingsData[\'nEl0\'] = ' + str(params['nEl0']) + '\n')
        post.write('    settingsData[\'NElMax\'] = ' + str(params['NElMax']) + '\n')
        post.write('    settingsData[\'DeltaEl\'] = ' + str(params['DeltaEl']) + '\n')
        post.write('    settingsData[\'deltapsi\'] = ' + str(params['deltapsi']) + '\n')
        post.write('    settingsData[\'nl\'] = ' + str(params['nl']) + '\n')
        post.write('    settingsData[\'nSegsOnPath\'] = ' + str(params['nSegsOnPath']) + '\n')
        post.write('    settingsData[\'tol\'] = ' + str(params['tol']) + '\n')
        post.write('' + '\n')
        post.write('    skipLineToLogFile(logfilePath,\'a\',True)' + '\n')
        post.write('    writeLineToLogFile(logfilePath,\'a\',\'Calling function extractFromODBoutputSet' + extSet.zfill(2) + ' ...\',True)' + '\n')
        post.write('    try:' + '\n')
        post.write('        extractFromODBoutputSet' + extSet.zfill(2) + '(workdir,proj,matdir,settingsData,logfilePath)' + '\n')
        post.write('    except Exception, error:' + '\n')
        post.write('        writeErrorToLogFile(logfilePath,\'a\',Exception,error,True)' + '\n')
        post.write('' + '\n')
        post.write('if __name__ == "__main__":' + '\n')
        post.write('    main(sys.argv[1:])' + '\n')
    return postprocessor
    
def runPostprocessor(wd,postprocessor,call,logfilename):
    skipLineToLogFile(logfilename,'a',True)
    if 'Windows' in system():
        cmdfile = join(wd,'runpostprocessor.cmd')
        writeLineToLogFile(logfilename,'a','Working in Windows',True)
        writeLineToLogFile(logfilename,'a','Writing Windows command file ' + cmdfile + ' ...',True)
        with open(cmdfile,'w') as cmd:
            cmd.write('\n')
            cmd.write('CD ' + wd + '\n')
            cmd.write('\n')
            cmd.write(call.strip() + ' ' + postprocessor + '\n')
        writeLineToLogFile(logfilename,'a','... done.',True)
        writeLineToLogFile(logfilename,'a','Running postprocessor ... ',True)
        try:
            #subprocess.call('cmd.exe /C ' + cmdfile,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            p = subprocess.Popen(cmdfile,shell=True,stderr=subprocess.PIPE)
            while True:
                output = p.stderr.read(1)
                if output == '' and p.poll()!= None:
                    break
                if out != '':
                    sys.stdout.write(output)
                    sys.stdout.flush()
        except Exception, error:
            writeErrorToLogFile(logfilename,'a',Exception,error,True)
            sys.exc_clear()
        writeLineToLogFile(logfilename,'a','... done.',True)
    elif 'Linux' in system():
        bashfile = join(wd,'runpostprocessor.sh')
        writeLineToLogFile(logfilename,'a','Working in Linux',True)
        writeLineToLogFile(logfilename,'a','Writing bash file ' + bashfile + ' ...',True)
        with open(bashfile,'w') as bash:
            bash.write('#!/bin/bash\n')
            bash.write('\n')
            bash.write('cd ' + wd + '\n')
            bash.write('\n')
            bash.write(call.strip() + ' ' + postprocessor + '\n')
        writeLineToLogFile(logfilename,'a','... done.',True)
        writeLineToLogFile(logfilename,'a','Changing permissions to ' + bashfile + ' ...',True)
        os.chmod(bashfile, 0o755)
        writeLineToLogFile(logfilename,'a','... done.',True)
        writeLineToLogFile(logfilename,'a','Running postprocessor ... ',True)
        rc = call('.' + bashfile)
        writeLineToLogFile(logfilename,'a','... done.',True)
    
    
def main(argv):

    # Read the command line, throw error if not option is provided
    try:
        opts, args = getopt.getopt(argv,'hb:m:p:e:w:s:c:',["help","Help","codebase","parametersfile", "settingsfile","matdir", "materialdirectory", "mdir","workdir", "workdirectory", "wdir","extractionset","statusfile","clear"])
    except getopt.GetoptError:
        print(' ')
        print('analyzeABQoutputData.py -b <codebase> -m <material folder> -p <parameter settings file> -e <extraction set>')
        print('                        -w <working directory> -s <status file(s)> -c <files to clear>')
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
            print(' ')
            print('analyzeABQoutputData.py -b <codebase> -m <material folder> -p <parameter settings file> -e <extraction set>')
            print('                        -w <working directory> -s <status file(s)> -c <files to clear>')
            print(' ')
            print(' ')
            print('Mandatory arguments:')
            print(' ')
            print('-b <codebase>                     ===> full/path/to/folder/without/closing/slash')
            print('-m <material folder>              ===> full/path/to/folder/without/closing/slash')
            print('-p <parameter settings file>      ===> full/path/to/file/with/extension')
            print('-e <extraction set>               ===> integer number representing set of extraction operations')
            print('-w <working directory>            ===> full/path/to/folder/without/closing/slash')
            print('-s <status file(s)>               ===> relative/path/to/file/with/extension with respect to working directory')
            print('                                       if multiple files are provided, they must be separated by a ;, for example:')
            print('                                          statusOne.sta;statusTwo.sta;statusThree.sta')
            print(' ')
            print(' ')
            print('Optional arguments:')
            print(' ')
            print('-c <files to clear>')
            print(' ')
            print(' ')
            print('Default values:')
            print(' ')
            print('-c <files to clear>                ===> no file is cleared')
            print('                                        file extensions must be provided without leading dots')
            print('                                        if multiple file extensions are provided, they must be separated by a ;, for example:')
            print('                                           ext1;ext2;ext3')
            print(' ')
            print(' ')
            print('Available extraction sets:')
            print(' ')
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
    logFilePath = join(workdir,logfile)

    # create log file
    writeTitleSecToLogFile(logFilePath,'w','ABAQUS RESULTS ANALYSIS',True)
    
    skipLineToLogFile(logFilePath,'a',True)
    writeLineToLogFile(logFilePath,'a','Reading settings ...',True)
    settings,sectionList,sectionsToExec = readSettingsFile(settingsfile)
    writeLineToLogFile(logFilePath,'a','... done.',True)
    
    subject = '[ABAQUS RESULTS ANALYSIS] Starting analysis'
    message = 'Abaqus results analysis starting on ' + datetime.now().strftime('%Y-%m-%d') + ' at ' + datetime.now().strftime('%H:%M:%S')
    sendStatusEmail(settings['emailDataDir'],'logData.csv',settings['serverFrom'],settings['emailFrom'],settings['emailTo'],subject,message)
    
    skipLineToLogFile(logFilePath,'a',True)
    writeLineToLogFile(logFilePath,'a','Starting reading list of simulations from status file ...',True)
    with open(statusfilepath,'r') as sta:
        lines = sta.readlines()
    writeLineToLogFile(logFilePath,'a','... done.',True)
    
    for l,line in enumerate(lines[1:]):
        simData = line.replace('\n','').split(',')
        simName = simData[0].strip()
        isPreprocessed = simData[1].strip()
        isSimCompleted = simData[2].strip()
        isPostprocessed = simData[3].strip()
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
                postProcessorFile = buildPostprocessorCall(settings,sectionList,sectionsToExec,extractionSet,simName,codedir,workdir,matdir,logFilePath,logfile)
            except Exception, error:
                writeErrorToLogFile(logFilePath,'a',Exception,error,True)
                writeLineToLogFile(logFilePath,'a','Moving on to the next.',True)
                sys.exc_clear()
                continue
            writeLineToLogFile(logFilePath,'a','... done.',True)
            writeLineToLogFile(logFilePath,'a','Calling function: runPostprocessor ...',True)
            try:
                runPostprocessor(workdir,postProcessorFile,settings['functionCall'],logFilePath)
            except Exception, error:
                writeErrorToLogFile(logFilePath,'a',Exception,error,True)
                writeLineToLogFile(logFilePath,'a','Moving on to the next.',True)
                sys.exc_clear()
                continue
            writeLineToLogFile(logFilePath,'a','... done.',True)
            simData[3] = 'YES'
            lines[l+1] = simData[0] + ', ' + simData[1] + ', ' + simData[2] + ', ' + simData[3] + '\n'
            with open(statusfilepath,'w') as sta:
                for li in lines:
                    sta.write(li)
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
        elif isPreprocessed=='YES' and isSimCompleted=='NO':
            writeLineToLogFile(logFilePath,'a','    ==> SIMULATION STAGE STILL NEED TO BE EXECUTED <==',True)
            writeLineToLogFile(logFilePath,'a','    Moving on to the next.',True)
        elif isPreprocessed=='YES' and isSimCompleted=='YES' and isPostprocessed=='YES':
            writeLineToLogFile(logFilePath,'a','    ==> POSTPROCESSING STAGE ALREADY EXECUTED <==',True)
            writeLineToLogFile(logFilePath,'a','    Moving on to the next.',True)
        else:
            writeLineToLogFile(logFilePath,'a','    !!! UNKNOWN ERROR WHILE PARSING LINE OF DATA !!!',True)
            writeLineToLogFile(logFilePath,'a','    Moving on to the next.',True)


if __name__ == "__main__":
    main(sys.argv[1:])
    