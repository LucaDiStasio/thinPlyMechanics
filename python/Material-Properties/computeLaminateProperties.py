#!/usr/bin/env Python
# -*- coding: utf-8 -*-

'''
=====================================================================================

Copyright (c) 2016-2018 Université de Lorraine or Luleå tekniska universitet
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


ested with Python 2.7 (64-bit) distribution in Windows 10.

'''

import sys, os
import numpy as np
from os.path import isfile, join, exists
from shutil import copyfile
import sqlite3
from datetime import datetime
from time import strftime, sleep
import timeit

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
        for row in data:
            line = ''
            for v,value in enumerate(row):
                if v>1:
                    line += ', '
                line += str(value)
            csv.write(line + '\n')

#===============================================================================#
#                                 LOG files
#===============================================================================#

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

#===============================================================================#
#===============================================================================#
#                                Ply properties
#===============================================================================#
#===============================================================================#
def RoM(Vf,rhof,ELf,ETf,nuf,alphaf,rhom,ELm,ETm,num,alpham):
    Vm = 1 - Vf
    Gf = 0.5*ELf/(1+nuf)
    Gm = 0.5*ELm/(1+num)
    rhoc = dot(rhof,Vf) + dot(rhom,Vm)
    E1 = dot(ELf,Vf) + dot(ELm,Vm)
    E2 = (Vf / ETf + Vm / ETm) ** (- 1)
    nu12 = dot(nuf,Vf) + dot(num,Vm)
    G12 = (Vf / Gf + Vm / Gm) ** (- 1)
    nu21 = dot(nu12,(E2 / E1))
    nu23 = dot(nu12,(1 - nu21)) / (1 - nu12)
    G23 = dot(0.5,E2) / (1 + nu23)
    alpha1 = (dot(dot(ELf,alphaf),Vf) + dot(dot(ELm,alpham),Vm)) / (dot(ELf,Vf) + dot(ELm,Vm))
    alpha2 = dot(dot((1 + nuf),alphaf),Vf) + dot(dot((1 + num),alpham),Vm) - dot(alpha1,nu12)
    return rhoc,E1,E2,nu12,nu21,G12,nu23,G23,alpha1,alpha2
#===============================================================================#
#===============================================================================#
#                              Laminate properties
#===============================================================================#
#===============================================================================#

#===============================================================================#
#===============================================================================#
#                               Transformations
#===============================================================================#
#===============================================================================#

#===============================================================================#
#===============================================================================#
#                                    MAIN
#===============================================================================#
#===============================================================================#

def main(argv):

if __name__ == "__main__":
    main(sys.argv[1:])
