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

def parseInputDeck():

def generatePreprocessorInputData():


def main(argv):

    # Read the command line, throw error if not option is provided
    try:
        opts, args = getopt.getopt(argv,'hm:i:d:w:s:p:l:',['help','Help',"mode","inputfile", "input","inpdir", "inputdirectory", "idir","workdir", "workdirectory", "wdir","statusfile","email", "emaildir", "edir"])
    except getopt.GetoptError:
        print('runFEM.py -m <mode> -i <input deck> -d <input directory> -w <working directory> -s <status file for restart>')
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
            print('runFEM.py -m <mode> -i <input deck> -d <input directory> -w <working directory> -s <status file for restart> -l <status email data directory>')
            print(' ')
            print('Mandatory arguments:')
            print('-i <input deck>')
            print('-d <input directory>')
            print(' ')
            print('Optional arguments:')
            print('-m <mode>                             ===> all, preprocessor, solver, postprocessor, preprocessor+solver, solver+postprocessor')
            print('-w <working directory>')
            print('-s <status file>')
            print('-l <status email data directory>')
            print(' ')
            print('Default values:')
            print('-m <mode>                             ===> all (preprocesssor + solver + postprocessor)')
            print('-w <working directory>                ===> same as input directory')
            print('-l <status email data directory>      ===> same as input directory')
            print(' ')
            print(' ')
            sys.exit()
        elif opt in ("-m", "--mode"):
            if 'all' in opt:
                isPreprocessorOn = True
                isSolverOn = True
                isPostprocessorOn = True
            elif 'preprocessor+solver' in opt:
                isPreprocessorOn = True
                isSolverOn = True
                isPostprocessorOn = False
            elif 'solver+postprocesor' in opt:
                isPreprocessorOn = False
                isSolverOn = True
                isPostprocessorOn = True
            elif 'preprocessor' in opt:
                isPreprocessorOn = True
                isSolverOn = False
                isPostprocessorOn = False
            elif 'solver' in opt:
                isPreprocessorOn = False
                isSolverOn = True
                isPostprocessorOn = False
            elif 'postprocessor' in opt:
                isPreprocessorOn = False
                isSolverOn = False
                isPostprocessorOn = True
        elif opt in ("-i", "--inputfile", "--input"): # input file has extension .deck, but it is a Comma-Separated Values file
            parts = arg.split(".")
            if len(parts) > 1:
                inputfile = arg
                subparts = parts[0].split('_')
                logfile = subparts[0] + '_FemParametricRun_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log'
                statusfile = subparts[0] + '_FemParametricRun_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.sta'
            else:
                inputfile = arg + '.deck'
                subparts = arg.split('_')
                logfile = subparts[0] + '_FemParametricRun_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log'
                statusfile = subparts[0] + '_FemParametricRun_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.sta'
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
        elif opt in ("-s", "--statusfile"):
            statusfile = arg
        elif opt in ("-l", "--email", "--emaildir", "--edir"):
            if arg[-1] != '/':
                emaildatadir = arg
            else:
                emaildatadir = arg[:-1]

    # Check the existence of variables: if a required variable is missing, an error is thrown and program is terminated; if an optional variable is missing, it is set to the default value
    if 'isPreprocessorOn' not in locals() or 'isSolverOn' not in locals() r 'isPostprocessorOn' not in locals():
        print('Error: mode of operation not provided.')
        sys.exit()
    if 'inputdir' not in locals():
        print('Error: input directory not provided.')
        sys.exit()
    if 'inputfile' not in locals():
        print('Error: input directory not provided.')
        sys.exit()
    if 'workdir' not in locals():
        workdir = inputdir
    if 'emaildatadir' not in locals():
        emaildatadir = inputdir

    logfilePath = join(workdir,logfile)
    with open(logfilePath,'w') as log:
        log.write('===============================================================================================\n')
        log.write('===============================================================================================\n')
        log.write('\n')
        log.write('                                     FEM PARAMETRIC RUN\n')
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
    print('                                           FEM PARAMETRIC RUN\n')
    print('\n')
    print('                                 Starting on ' + datetime.now().strftime('%Y-%m-%d') + ' at ' + datetime.now().strftime('%H:%M:%S') + '\n')
    print('\n')
    print('                                      Platform: ' + platform() + '\n')
    print('\n')
    print('===============================================================================================\n')
    print('===============================================================================================\n')
    print('\n')

    statusfilePath = join(workdir,statusfile)

    with open(join(emaildatadir,'logData.csv'),'r') as emailData:
        lines = emailData.readlines()

    serverFrom = lines[1].replace('\n','').replace(' ','').split(',')[2]
    emailFrom = lines[1].replace('\n','').replace(' ','').split(',')[3]
    emailTo = lines[1].replace('\n','').replace(' ','').split(',')[4]

    if isPreprocessorOn:
        subject = '[FEM PARAMETRIC RUN] Preprocessor starts'
        message = 'FEM parametric run update on ' + datetime.now().strftime('%Y-%m-%d') + ' at ' + datetime.now().strftime('%H:%M:%S') + '\n\nStarting preprocessor.'
        sendStatusEmail(emaildatadir,'logData.csv',serverFrom,emailFrom,emailTo,subject,message)
        try:
            with open(statusfilePath,'w') as sta:
                sta.write('PROJECT NAME, PREPROCESSING, FEM SOLVER, POST PROCESSING, DETAILS\n')

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
        subject = '[FEM PARAMETRIC RUN] Preprocessor terminated'
        message = 'FEM parametric run update on ' + datetime.now().strftime('%Y-%m-%d') + ' at ' + datetime.now().strftime('%H:%M:%S') + '\n\nPreprocessor terminated.'
        sendStatusEmail(emaildatadir,'logData.csv',serverFrom,emailFrom,emailTo,subject,message)
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
