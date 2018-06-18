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



Tested with Python 2.7 Anaconda 2.4.1 (64-bit) distribution in Windows 7.

'''

from os.path import isfile, join
import sys
import getopt
from datetime import datetime
from time import strftime, sleep
from platform import platform
from numpy import arange
import math

def main(argv):

    # Read the command line, throw error if not option is provided
    try:
        opts, args = getopt.getopt(argv,'hi:d:w:s:',['help','Help',"inputfile", "input","inpdir", "inputdirectory", "idir","workdir", "workdirectory", "wdir","abqonly"])
    except getopt.GetoptError:
        print('analyzeAbaqus.py -i <input deck> -d <input directory> -w <working directory> -s <status file>')
        sys.exit(2)
    # Parse the options and create corresponding variables
    for opt, arg in opts:
        if opt in ('-h', '--help','--Help'):
            print(' ')
            print(' ')
            print('*****************************************************************************************************')
            print(' ')
            print(' ')
            print('             MECHANICS OF EXTREME THIN PLIES IN FIBER REINFORCED COMPOSITE LAMINATES')
            print(' ')
            print('        2D PLANE STRAIN MICROMECHANICAL PARAMETRIC SIMULATION OF REFERENCE VOLUME ELEMENTS')
            print(' ')
            print('                                        POST-PROCESSING')
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
            print('analyzeAbaqus.py -i <input deck> -d <input directory> -w <working directory> -s <status file for abaqus only>')
            print(' ')
            print('Mandatory arguments:')
            print('-i <input deck>')
            print('-d <input directory>')
            print(' ')
            print('Optional arguments:')
            print('-w <working directory>')
            print('-s <status file>')
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

    # Check the existence of variables: if a required variable is missing, an error is thrown and program is terminated; if an optional variable is missing, it is set to the default value
    if 'inputdir' not in locals():
        print('Error: input directory not provided.')
        sys.exit()
    if 'inputfile' not in locals():
        print('Error: input directory not provided.')
        sys.exit()
    if 'workdir' not in locals():
        workdir = inputdir

    
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

   





if __name__ == "__main__":
    main(sys.argv[1:])
