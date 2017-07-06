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
from datetime import datetime
from time import strftime
from platform import platform


def getProjectList(wd,inpfile):
    with open(join(wd,inpfile),'r') as inp:
        lines = inp.readlines()
    projects = []
    for line in lines[1:]:
        files.append(line.split(',')[0].replace('\n','').replace(' ',''))
    return projects

def joinCSVs(wd,od,inpfile,csvname,globalcsv,dosort,col=0):
    sims = getProjectList(wd,inpfile)
    with open(join(wd,sims[0],'csv',csvname),'r') as csv:
        lines = csv.readlines()
    firstline = lines[0]
    with open(join(od,globalcsv),'w') as csv:
        csv.write(firstline)
    data = []
    for sim in sims:
        try:
            with open(join(wd,sim,'csv',csvname),'r') as csv:
                lines = csv.readlines()
            for line in lines[1:]:
                if dosort:
                    parts = line.replace('\n','').split(',')
                    parts[col] = float(parts[col])
                    data.append(parts)
                else:
                    data.append(line)
        except Exception:
            sys.exc_clear()
    if dosort:
        data = sorted(data, key=lambda m: m[col])
        for j,element in data:
            line = ''
            for n,value in element:
                if n>0:
                    line += ','
                line += str(value)
            data[j] = line
    with open(join(od,globalcsv),'a') as csv:
        for line in data:
            csv.write(line + '\n')


def main(argv):

    # Read the command line, throw error if not option is provided
    try:
        opts, args = getopt.getopt(argv,'hw:i:c:s:',['help','Help',"workdir", "workdirectory", "wdir","inputfile", "input","csvfile", "csv","sort","out","outdir"])
    except getopt.GetoptError:
        print('joinCSVs.py -w <working directory> -i <input file> -c <csv filename> -s <sort by column s> -o <output directory>')
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
            print('                                    JOIN DATA IN CSV FORMAT\n')
            print(' ')
            print('                                              by')
            print(' ')
            print('                                    Luca Di Stasio, 2016-2017')
            print(' ')
            print(' ')
            print('*****************************************************************************************************')
            print(' ')
            print('Program syntax:')
            print('joinCSVs.py -w <working directory> -i <input file> -c <csv filename> -s <sort by column s> -o <output directory>')
            print(' ')
            print('Mandatory arguments:')
            print('-w <working directory>')
            print('-i <input file>')
            print('-c <csv filename>')
            print(' ')
            print('Optional arguments:')
            print('-s <sort by column s>')
            print('-o <output directory>')
            print(' ')
            print('Default values:')
            print('-s <sort by column s>                ===> left unsorted')
            print('-o <output directory>                ===> working directory')
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
        elif opt in ("-c", "--csv", "--csvfile"):
            parts = arg.split(".")
            if len(parts) > 1:
                csvfile = arg
            else:
                csvfile = arg + '.csv'
        elif opt in ("-s", "--sort"):
            column = int(arg)
            sort = True
        elif opt in ("-o", "--out","--outdir"):
            if arg[-1] != '/':
                outdir = arg
            else:
                outdir = arg[:-1]

    # Check the existence of variables: if a required variable is missing, an error is thrown and program is terminated; if an optional variable is missing, it is set to the default value
    if 'workdir' not in locals():
        print('Error: working directory not provided.')
        sys.exit()
    if 'inputfile' not in locals():
        print('Error: status file not provided.')
        sys.exit()
    if 'csvfile' not in locals():
        print('Error: status file not provided.')
        sys.exit()
    if 'column' not in locals():
        sort = False
    if 'outdir' not in locals():
        outdir = workdir
        
    globalCSVname = datetime.now().strftime('%Y-%m-%d') + '_JOINED_' + csvfile
    
    if sort:
        joinCSVs(workdir,outdir,inputfile,csvfile,globalCSVname,sort,column)
    else:
        joinCSVs(workdir,outdir,inputfile,csvfile,globalCSVname,sort)


if __name__ == "__main__":
    main(sys.argv[1:])

