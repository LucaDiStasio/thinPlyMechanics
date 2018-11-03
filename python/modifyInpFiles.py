#!/usr/bin/env Python
# -*- coding: utf-8 -*-

'''
=====================================================================================

Copyright (c) 2016-2018 Université de Lorraine & Luleå tekniska universitet
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
#from os import listdir, stat, makedirs
from datetime import datetime
from time import strftime


def main():
    #inpDir = 'C:/Users/luca/OneDrive/01_Luca/07_DocMASE/07_Data/03_FEM/InputData'
    #outDir = 'C:/Users/luca/OneDrive/01_Luca/07_DocMASE/07_Data/03_FEM/InputData/modified'
    inpDir = 'D:/OneDrive/01_Luca/07_DocMASE/07_Data/03_FEM/InputData'
    outDir = 'D:/OneDrive/01_Luca/07_DocMASE/07_Data/03_FEM/InputData/modified'
    baseName = 'inputRVEdata'
    ext = '.deck'
    Ls = ['1_25','1_144','1_0992']
    nFibs = [1,2,3,5]

    fileList = []
    for L in Ls:
        for n in nFibs:
            fileList.append(baseName+'L'+L+'S'+str(n)+'F-LPC'+ext)
            fileList.append(baseName+'L'+L+'A'+str(n)+'F-LPC'+ext)
            for m in range(1,n+1):
                fileList.append(baseName+'L'+L+'A'+str(m)+'S'+str(n)+'F-LPC'+ext)

    if not exists(outDir):
        os.mkdir(outDir)

    for name in fileList:
        with open(join(inpDir,name),'r') as inp:
            lines = inp.readlines()
        with open(join(outDir,name),'w') as out:
            for line in lines:
                if 'BC' in line and 'northSide' in line and 'type' in line:
                    newline = line.replace('vkinCouplingmeancorners','vkinCouplingmeancornersulinearCoupling')
                    out.write(newline)
                else:
                    out.write(line)

    baseName = 'inputRVEiterables'
    fileList = []
    for L in Ls:
        for n in nFibs:
            fileList.append(baseName+'L'+L+'S'+str(n)+'F-LPC'+ext)
            fileList.append(baseName+'L'+L+'A'+str(n)+'F-LPC'+ext)
            for m in range(1,n+1):
                fileList.append(baseName+'L'+L+'A'+str(m)+'S'+str(n)+'F-LPC'+ext)

    for name in fileList:
        with open(join(inpDir,name),'r') as inp:
            lines = inp.readlines()
        with open(join(outDir,name),'w') as out:
            for line in lines:
                if 'basename' in line:
                    newline = line.replace('vk','vkul')
                    out.write(newline)
                else:
                    out.write(line)


if __name__ == '__main__':
    main()
