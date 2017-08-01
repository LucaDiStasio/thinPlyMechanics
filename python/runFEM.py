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


def extractSectionFromInputDeck(deckFullPath,sectionName):
    with open(deckFullPath,'r') as f:
        lines = f.readlines()
    section = []
    add = False
    for line in lines:
        if 'START SECTION:' in line and sectionName in line:
            add = True
        elif 'END SECTION:' in line and sectionName in line:
            add = False
            break
        else:
            if add:
                section.append(line)
    return section

def parseAndAssignToDict(lineList,keyList,labelDict):
    data = {}
    for line in lineList:
        for key in keyList:
            if labelDict[key] in line:
                data[key] = line.replace('\n','').split('#')[0].split(':')[1].replace(' ','')
                break
    return data

def readIOdataFromInputDeck(deckFullPath):
    lines = extractSectionFromInputDeck(deckFullPath,'I/O MANAGEMENT')
    keys = ['WD','MDF','PSF','NESF','SF']
    labels = {'WD':'WORKING DIRECTORY','MDF':'MATERIAL DATA FOLDER','PSF':'POSTPROCESSING SETTINGS FOLDER','NESF':'NOTIFICATION EMAILS SETTINGS FOLDER','SF':'STATUS FILE'}
    data = parseAndAssignToDict(lines,keys,labels)
    for key in keys[1:4]:
        if data[key]=='' or data[key]==' ' or data[key]==None or len(data[key])<1:
            data[key] = data['WD']
    if data['SF']=='' or data['SF']==' ' or data['SF']==None or len(data['SF'])<1:
        data['SF'] = 'FemParametricRun_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.sta'
    elif len(data['SF'].split('.'))<2:
        data['SF'] = data['SF'] + '.sta'
    return data

def readSOFTdataFromInputDeck(deckFullPath):
    lines = extractSectionFromInputDeck(deckFullPath,'SOFTWARE')
    keys = ['isPreprocessorOn','preprocessorPlatform','preprocessorCall','isSolverOn','solverPlatform','solverCall','isPostprocessorOn','postprocessorPlatform','postprocessorCall']
    labels = {'isPreprocessorOn':'RUN PREPROCESSOR','preprocessorPlatform':'PREPROCESSOR PLATFORM','preprocessorCall':'PREPROCESSOR CALL','isSolverOn':'RUN SOLVER','solverPlatform':'SOLVER PLATFORM','solverCall':'SOLVER CALL','isPostprocessorOn':'RUN POSTPROCESSOR','postprocessorPlatform':'POSTPROCESSOR PLATFORM','postprocessorCall':'POSTPROCESSOR CALL'}
    data = parseAndAssignToDict(lines,keys,labels)
    return data


def main(argv):

    # Read the command line, throw error if not option is provided
    try:
        opts, args = getopt.getopt(argv,'hi:d:',['help','Help',"inputfile", "input","inpdir", "inputdirectory", "idir"])
    except getopt.GetoptError:
        print('runFEM.py -i <input deck> -d <input directory>')
        sys.exit(2)
    # Parse the options and create corresponding variables
    for opt, arg in opts:
        if opt in ('-h', '--help','--Help'):
            print(' ')
            print(' ')
            print('*****************************************************************************************************')
            print(' ')
            print('                                    FEM PARAMETRIC SIMULATION')
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
            print('runFEM.py -i <input deck> -d <input directory>')
            print(' ')
            print('Mandatory arguments:')
            print('-i <input deck>')
            print('-d <input directory>')
            print(' ')
            print(' ')
            sys.exit()
        elif opt in ("-i", "--inputfile", "--input"): # input file has extension .deck, but it is a Comma-Separated Values file
            parts = arg.split(".")
            if len(parts) > 1:
                inputfile = arg
                subparts = parts[0].split('_')
                logfile = subparts[0] + '_FemParametricRun_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log'
            else:
                inputfile = arg + '.deck'
                subparts = arg.split('_')
                logfile = subparts[0] + '_FemParametricRun_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log'
        elif opt in ("-d", "--inpdir", "--inputdirectory", "--idir"):
            if arg[-1] != '/':
                inputdir = arg
            else:
                inputdir = arg[:-1]

    # Check the existence of variables: if a required variable is missing, an error is thrown and program is terminated; if an optional variable is missing, it is set to the default value
    if 'inputdir' not in locals():
        print('Error: input directory not provided.')
        sys.exit()
    if 'inputfile' not in locals():
        print('Error: input directory not provided.')
        sys.exit()

    # initialize full paths of deck and log file
    inputDeckFullPath = join(inputdir,inputfile)

    logFolder = join(inputdir,datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '_logFolder')

    logfilePath = join(logFolder,logfile)

    # create log file
    writeTitleSecToLogFile(logFilePath,'w','FEM PARAMETRIC RUN',True)

    # read I/O data from input deck and assign to variables
    skipLineToLogFile(logFilePath,'a',True)
    writeLineToLogFile(logFilePath,'a','Reading I/O data from input deck and assigning to variables ...',True)
    try:
        IOdata = readIOdataFromInputDeck(deckFullPath)
        statusfilePath = join(logFolder,IOdata['SF'])
        emaildatadir = IOdata['NESF']
        writeLineToLogFile(logFilePath,'a','...done.',True)
        writeLineToLogFile(logFilePath,'a','WORKING DIRECTORY: ' + IOdata['WD'],True)
        writeLineToLogFile(logFilePath,'a','MATERIAL DATA FOLDER: ' + IOdata['MDF'],True)
        writeLineToLogFile(logFilePath,'a','POSTPROCESSING SETTINGS FOLDER: ' + IOdata['PSF'],True)
        writeLineToLogFile(logFilePath,'a','NOTIFICATION EMAILS SETTINGS FOLDER: ' + IOdata['NESF'],True)
        writeLineToLogFile(logFilePath,'a','STATUS FILE: ' + IOdata['SF'],True)
    except Exception, error:
        writeErrorToLogFile(logFilePath,'a',Exception,error,True)
        sys.exit(2)

    # read software data from input deck and assign to variables
    skipLineToLogFile(logFilePath,'a',True)
    writeLineToLogFile(logFilePath,'a','Reading software data from input deck and assigning to variables ...',True)
    try:
        SOFTdata = readSOFTdataFromInputDeck(deckFullPath)
        if SOFTdata['isPreprocessorOn']=='YES' or SOFTdata['isPreprocessorOn']=='Yes' or SOFTdata['isPreprocessorOn']=='y' or SOFTdata['isPreprocessorOn']=='yes':
            isPreprocessorOn = SOFTdata['isPreprocessorOn']
        if SOFTdata['isSolverOn']=='YES' or SOFTdata['isSolverOn']=='Yes' or SOFTdata['isSolverOn']=='y' or SOFTdata['isSolverOn']=='yes':
            isSolverOn = SOFTdata['isSolverOn']
        if SOFTdata['isPostprocessorOn']=='YES' or SOFTdata['isPostprocessorOn']=='Yes' or SOFTdata['isPostprocessorOn']=='y' or SOFTdata['isPostprocessorOn']=='yes':
            isPostprocessorOn = SOFTdata['isPostprocessorOn']
        writeLineToLogFile(logFilePath,'a','...done.',True)
        writeLineToLogFile(logFilePath,'a','RUN PREPROCESSOR: ' + SOFTdata['isPreprocessorOn'],True)
        writeLineToLogFile(logFilePath,'a','PREPROCESSOR PLATFORM: ' + SOFTdata['preprocessorPlatform'],True)
        writeLineToLogFile(logFilePath,'a','PREPROCESSOR CALL: ' + SOFTdata['preprocessorCall'],True)
        writeLineToLogFile(logFilePath,'a','RUN SOLVER: ' + SOFTdata['isSolverOn'],True)
        writeLineToLogFile(logFilePath,'a','SOLVER PLATFORM: ' + SOFTdata['solverPlatform'],True)
        writeLineToLogFile(logFilePath,'a','SOLVER CALL: ' + SOFTdata['solverCall'],True)
        writeLineToLogFile(logFilePath,'a','RUN POSTPROCESSOR: ' + SOFTdata['isPostprocessorOn'],True)
        writeLineToLogFile(logFilePath,'a','POSTPROCESSOR PLATFORM: ' + SOFTdata['postprocessorPlatform'],True)
        writeLineToLogFile(logFilePath,'a','POSTPROCESSOR CALL: ' + SOFTdata['postprocessorCall'],True)
    except Exception, error:
        writeErrorToLogFile(logFilePath,'a',Exception,error,True)
        sys.exit(2)

    # read server data from notification emails settings
    skipLineToLogFile(logFilePath,'a',True)
    writeLineToLogFile(logFilePath,'a','Reading server data from notification emails settings ...',True)
    try:
        with open(join(emaildatadir,'logData.csv'),'r') as emailData:
            lines = emailData.readlines()
        serverFrom = lines[1].replace('\n','').replace(' ','').split(',')[2]
        emailFrom = lines[1].replace('\n','').replace(' ','').split(',')[3]
        emailTo = lines[1].replace('\n','').replace(' ','').split(',')[4]
        writeLineToLogFile(logFilePath,'a','...done.',True)
        writeLineToLogFile(logFilePath,'a','From ' + emailFrom,True)
        writeLineToLogFile(logFilePath,'a','on server ' + serverFrom,True)
        writeLineToLogFile(logFilePath,'a','to ' + emailTo,True)
    except Exception, error:
        writeErrorToLogFile(logFilePath,'a',Exception,error,True)
        sys.exit(2)

    # starting simulation pipe
    if isPreprocessorOn:
        skipLineToLogFile(logFilePath,'a',True)
        writeLineToLogFile(logFilePath,'a','Sending notification email ...',True)
        try:
            subject = '[FEM PARAMETRIC RUN] Preprocessor starts'
            message = 'FEM parametric run update on ' + datetime.now().strftime('%Y-%m-%d') + ' at ' + datetime.now().strftime('%H:%M:%S') + '\n\nStarting preprocessor.'
            sendStatusEmail(emaildatadir,'logData.csv',serverFrom,emailFrom,emailTo,subject,message)
            writeLineToLogFile(logFilePath,'a','...done.',True)
        except Exception, error:
            writeErrorToLogFile(logFilePath,'a',Exception,error,True)
            sys.exc_clear()
        skipLineToLogFile(logFilePath,'a',True)
        writeLineToLogFile(logFilePath,'a','Creating status file ...',True)
        try:
            with open(statusfilePath,'w') as sta:
                sta.write('PROJECT NAME, PREPROCESSING, FEM SOLVER, POST PROCESSING, DETAILS\n')
            writeLineToLogFile(logFilePath,'a','...done.',True)
            writeLineToLogFile(logFilePath,'a','Status file ' + statusfilePath + ' created.',True)
        except Exception, error:
            writeErrorToLogFile(logFilePath,'a',Exception,error,True)
            skipLineToLogFile(logFilePath,'a',True)
            writeLineToLogFile(logFilePath,'a','Sending notification email ...',True)
            try:
                subject = '[FEM PARAMETRIC RUN] Preprocessor terminated'
                message = 'FEM parametric run update on ' + datetime.now().strftime('%Y-%m-%d') + ' at ' + datetime.now().strftime('%H:%M:%S') + '\n\nPreprocessor terminated.'
                sendStatusEmail(emaildatadir,'logData.csv',serverFrom,emailFrom,emailTo,subject,message)
                writeLineToLogFile(logFilePath,'a','...done.',True)
            except Exception, error:
                writeErrorToLogFile(logFilePath,'a',Exception,error,True)
                sys.exc_clear()
            sys.exit(2)
    if isSolverOn:
        subject = '[FEM PARAMETRIC RUN] Solver starts'
        message = 'FEM parametric run update on ' + datetime.now().strftime('%Y-%m-%d') + ' at ' + datetime.now().strftime('%H:%M:%S') + '\n\nStarting solver.'
        sendStatusEmail(emaildatadir,'logData.csv',serverFrom,emailFrom,emailTo,subject,message)
        try:

        except Exception, error:
            with open(logfilePath,'a') as log:
                log.write('!!! ----------------------------------------------------------------------------------------!!!\n')
                log.write('\n')
                log.write('                                     AN ERROR OCCURED\n')
                log.write('\n')
                log.write('                                -------------------------\n')
                log.write('\n')
                log.write(str(Exception) + '\n')
                log.write(str(error) + '\n')
                log.write('\n')
                log.write('Terminating program\n')
                log.write('\n')
                log.write('!!! ----------------------------------------------------------------------------------------!!!\n')
                log.write('\n')
            print('!!! ----------------------------------------------------------------------------------------!!!\n')
            print('\n')
            print('                                     AN ERROR OCCURED\n')
            print('\n')
            print('                                -------------------------\n')
            print('\n')
            print(str(Exception) + '\n')
            print(str(error) + '\n')
            print('\n')
            print('Terminating program\n')
            print('\n')
            print('!!! ----------------------------------------------------------------------------------------!!!\n')
            print('\n')
        subject = '[FEM PARAMETRIC RUN] Solver terminated'
        message = 'FEM parametric run update on ' + datetime.now().strftime('%Y-%m-%d') + ' at ' + datetime.now().strftime('%H:%M:%S') + '\n\nSolver terminated.'
        sendStatusEmail(emaildatadir,'logData.csv',serverFrom,emailFrom,emailTo,subject,message)
    if isPostprocessorOn:
        subject = '[FEM PARAMETRIC RUN] Postprocessor starts'
        message = 'FEM parametric run update on ' + datetime.now().strftime('%Y-%m-%d') + ' at ' + datetime.now().strftime('%H:%M:%S') + '\n\nStarting postprocessor.'
        sendStatusEmail(emaildatadir,'logData.csv',serverFrom,emailFrom,emailTo,subject,message)
        try:

        except Exception, error:
            with open(logfilePath,'a') as log:
                log.write('!!! ----------------------------------------------------------------------------------------!!!\n')
                log.write('\n')
                log.write('                                     AN ERROR OCCURED\n')
                log.write('\n')
                log.write('                                -------------------------\n')
                log.write('\n')
                log.write(str(Exception) + '\n')
                log.write(str(error) + '\n')
                log.write('\n')
                log.write('Terminating program\n')
                log.write('\n')
                log.write('!!! ----------------------------------------------------------------------------------------!!!\n')
                log.write('\n')
            print('!!! ----------------------------------------------------------------------------------------!!!\n')
            print('\n')
            print('                                     AN ERROR OCCURED\n')
            print('\n')
            print('                                -------------------------\n')
            print('\n')
            print(str(Exception) + '\n')
            print(str(error) + '\n')
            print('\n')
            print('Terminating program\n')
            print('\n')
            print('!!! ----------------------------------------------------------------------------------------!!!\n')
            print('\n')
        subject = '[FEM PARAMETRIC RUN] Postprocessor terminated'
        message = 'FEM parametric run update on ' + datetime.now().strftime('%Y-%m-%d') + ' at ' + datetime.now().strftime('%H:%M:%S') + '\n\nPostprocessor terminated.'
        sendStatusEmail(emaildatadir,'logData.csv',serverFrom,emailFrom,emailTo,subject,message)



if __name__ == "__main__":
    main(sys.argv[1:])
