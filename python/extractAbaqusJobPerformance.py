#!/usr/bin/env Python
# -*- coding: utf-8 -*-

'''
=====================================================================================

Copyright (c) 2016 Université de Lorraine & Luleå tekniska universitet
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



Tested with Python 2.7 Anaconda 2.4.1 (64-bit) distribution in Windows 10.

'''

import sys
import os
from os.path import isfile, join, exists
from os import listdir, stat, makedirs
import getopt
from datetime import datetime
from time import strftime
from platform import platform
import numpy as np


def getProjectList(wd,inpfile):
    with open(join(wd,inpfile),'r') as inp:
        lines = inp.readlines()
    projects = []
    for line in lines[1:]:
        projects.append(line.split(',')[0].replace('\n','').replace(' ',''))
    return projects

def getPerfs(wd,inpfile):
    sims = getProjectList(wd,inpfile)
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
                    while '' in words:
                        words.remove('')
                    progN = int(words[-1])
                    words = lines[l+9].split(' ')
                    while '' in words:
                        words.remove('')
                    totVar = int(words[-1])
        if exists(join(wd,sim,'abaqus',sim+'.msg')):
            with open(join(wd,sim,'abaqus',sim+'.msg'),'r') as msg:
                lines = msg.readlines()
                for line in lines:
                    if 'USING THE DIRECT SOLVER WITH' in line:
                        words = line.replace('\n','').split(' ')
                        while '' in words:
                            words.remove('')
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

def main(argv):

    # Read the command line, throw error if not option is provided
    try:
        opts, args = getopt.getopt(argv,'hw:i:o:j:',['help','Help',"workdir", "workdirectory", "wdir","inputfile", "input","out","outdir","job","jobname"])
    except getopt.GetoptError:
        print('')
        print('joinCSVs.py -w <working directory> -i <input file> -o <output directory> -j <job name>')
        print('')
        print(str(getopt.GetoptError))
        sys.exit()
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
            print('                                 EXTRACT ABAQUS PERFORMANCES\n')
            print(' ')
            print('                                              by')
            print(' ')
            print('                                    Luca Di Stasio, 2016-2017')
            print(' ')
            print(' ')
            print('*****************************************************************************************************')
            print(' ')
            print('Program syntax:')
            print('joinCSVs.py -w <working directory> -i <input file> -o <output directory> -j <job name>')
            print(' ')
            print('Mandatory arguments:')
            print('-w <working directory>')
            print('-i <input file>')
            print(' ')
            print('Optional arguments:')
            print('-o <output directory>')
            print('-j <job name>')
            print(' ')
            print('Default values:')
            print('-o <output directory>                ===> working directory')
            print('-j <job name>                        ===> inputfile')
            print(' ')
            print(' ')
            print(' ')
            sys.exit()
        elif opt in ("-w", "--workdir", "--workdirectory", "--wdir"):
            if arg[-1] != '/':
                workdir = arg
            else:
                workdir = arg[:-1]
        elif opt in ("-i", "--inputfile", "--input"):
            parts = arg.split(".")
            if len(parts) > 1:
                inputfile = arg
            else:
                inputfile = arg + '.inp'
        elif opt in ("-o", "--out","--outdir"):
            if arg[-1] != '/':
                outdir = arg
            else:
                outdir = arg[:-1]
        elif opt in ("-j", "--job", "--jobname"):
            parts = arg.split(".")
            if len(parts) > 1:
                jobname = arg
            else:
                jobname = arg + '.csv'

    # Check the existence of variables: if a required variable is missing, an error is thrown and program is terminated; if an optional variable is missing, it is set to the default value
    if 'workdir' not in locals():
        print('Error: working directory not provided.')
        sys.exit()
    if 'inputfile' not in locals():
        print('Error: status file not provided.')
        sys.exit()
    if 'outdir' not in locals():
        outdir = workdir
    if 'jobname' not in locals():
        jobname = inputfile.split('.')[0] + '.csv'
    
    print('===============================================================================================\n')
    print('===============================================================================================\n')
    print('\n')
    print('                              EXTRACTION OF PERFOMANCE DATA OF ABAQUS JOBS\n')
    print('\n')
    print('                                 Starting on ' + datetime.now().strftime('%Y-%m-%d') + ' at ' + datetime.now().strftime('%H:%M:%S') + '\n')
    print('\n')
    print('                                    Platform: ' + platform() + '\n')
    print('\n')
    print('===============================================================================================\n')
    print('===============================================================================================\n')
    print('\n')
    
    writePerfToFile(outdir,jobname,getPerfs(workdir,inputfile))


if __name__ == "__main__":
    main(sys.argv[1:])

