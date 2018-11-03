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
    itbaseName = 'inputRVEiterables'
    ext = '.deck'
    Ls = ['1_618','1_25','1_144','1_0992']
    homogSize = ['1','2','3','5']
    #nFibs = [1,2,3,5]

    fileListSide = []
    fileListAbove = []
    fileListSideAbove = []
    for L in Ls:
        for s in homogSize:
            fileListSide.append(baseName+'L'+L+'S'+'FHOMO'+s+ext)
            fileListAbove.append(baseName+'L'+L+'A'+'FHOMO'+s+ext)
            fileListSideAbove.append(baseName+'L'+L+'A'+'S'+'FHOMO'+s+ext)

    if not exists(outDir):
        os.mkdir(outDir)

    for name in fileListSide:
        with open(join(inpDir,name),'r') as inp:
            lines = inp.readlines()
        with open(join(outDir,name),'w') as out:
            for line in lines:
                if 'BC' in line and 'rightSide' in line and 'nFibers' in line:
                    nFib = int(line.split('$')[0].split('@')[1])
                    newline = 'BC, rightSide, nFibers @' + str(nFib+1) + '$int' + '\n'
                    out.write(newline)
                elif 'BC' in line and 'leftSide' in line and 'nFibers' in line:
                    nFib = int(line.split('$')[0].split('@')[1])
                    newline = 'BC, leftSide, nFibers @' + str(nFib+1) + '$int' + '\n'
                    out.write(newline)
                else:
                    out.write(line)
        with open(join(inpDir,itbaseName+'L'+L+'S'+'FHOMO'+s+ext),'r') as inp:
            lines = inp.readlines()
        with open(join(outDir,itbaseName+'L'+L+'S'+'FHOMO'+s+ext),'w') as out:
            for line in lines:
                        if 'basename' in line:
                            newline = line.replace('sf'+str(nFib),'sf'+str(nFib+1))
                            out.write(newline)
                        else:
                            out.write(line)

    for name in fileListAbove:
        with open(join(inpDir,name),'r') as inp:
            lines = inp.readlines()
        with open(join(outDir,name),'w') as out:
            for line in lines:
                if 'BC' in line and 'northSide' in line and 'nFibers' in line:
                    nFib = int(line.split('$')[0].split('@')[1])
                    newline = 'BC, northSide, nFibers @' + str(nFib+1) + '$int' + '\n'
                    out.write(newline)
                else:
                    out.write(line)
        with open(join(inpDir,itbaseName+'L'+L+'A'+'FHOMO'+s+ext),'r') as inp:
            lines = inp.readlines()
        with open(join(outDir,itbaseName+'L'+L+'A'+'FHOMO'+s+ext),'w') as out:
            for line in lines:
                        if 'basename' in line:
                            newline = line.replace('sf'+str(nFib),'sf'+str(nFib+1))
                            out.write(newline)
                        else:
                            out.write(line)

    for name in fileListSideAbove:
        with open(join(inpDir,name),'r') as inp:
            lines = inp.readlines()
        for line in lines:
            if 'BC' in line and 'rightSide' in line and 'nFibers' in line:
                nFibS = int(line.split('$')[0].split('@')[1])
            elif 'BC' in line and 'northSide' in line and 'nFibers' in line:
                nFibA = int(line.split('$')[0].split('@')[1])
        if nFibS == nFibA:
            newnFibS = nFibS + 1
            newnFibA = 1
        else:
            newnFibS = nFibS
            newnFibA = nFibA + 1
        with open(join(outDir,name),'w') as out:
            for line in lines:
                if 'BC' in line and 'rightSide' in line and 'nFibers' in line:
                    newline = 'BC, rightSide, nFibers @' + str(newnFibS) + '$int' + '\n'
                    out.write(newline)
                elif 'BC' in line and 'leftSide' in line and 'nFibers' in line:
                    newline = 'BC, leftSide, nFibers @' + str(newnFibS) + '$int' + '\n'
                    out.write(newline)
                elif 'BC' in line and 'northSide' in line and 'nFibers' in line:
                    newline = 'BC, northSide, nFibers @' + str(newnFibA) + '$int' + '\n'
                    out.write(newline)
                else:
                    out.write(line)
        with open(join(inpDir,itbaseName+'L'+L+'A'+'S'+'FHOMO'+s+ext),'r') as inp:
            lines = inp.readlines()
        with open(join(outDir,itbaseName+'L'+L+'A'+'S'+'FHOMO'+s+ext),'w') as out:
            for line in lines:
                        if 'basename' in line:
                            newline = line.replace('sf'+str(nFibS),'sf'+str(newnFibS)).replace('af'+str(nFibA),'af'+str(newnFibA))
                            out.write(newline)
                        else:
                            out.write(line)

    #baseName = 'inputRVEiterables'
    #fileListSide = []
    #fileListAbove = []
    #fileListSideAbove = []
    #for L in Ls:
    #    for n in nFibs:
    #        fileListSide.append(baseName+'L'+L+'S'+'FHOMO'+s+ext)
    #        fileListAbove.append(baseName+'L'+L+'A'+'FHOMO'+s+ext)
    #        fileListSideAbove.append(baseName+'L'+L+'A'+'S'+'FHOMO'+s+ext)

    #for name in fileListSide:
    #    with open(join(inpDir,name),'r') as inp:
    #        lines = inp.readlines()
    #    with open(join(outDir,name),'w') as out:
    #        for line in lines:
    #            if 'basename' in line:
    #                newline = line.replace('vk','vkul')
    #                out.write(newline)
    #            else:
    #                out.write(line)


if __name__ == '__main__':
    main()
