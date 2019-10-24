#!/usr/bin/env Python
# -*- coding: utf-8 -*-

'''
=====================================================================================

Copyright (c) 2016-2019 Université de Lorraine & Luleå tekniska universitet
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

def getMaxSectionNumber(S,A):
    if S>0:
        if A>0:
            N = 5
        else:
            N = 4
    else:
        if A>0:
            N = 3
        else:
            N = 2
    return N

def main():
    #inpDir = 'C:/Users/luca/OneDrive/01_Luca/07_DocMASE/07_Data/03_FEM/InputData'
    #outDir = 'C:/Users/luca/OneDrive/01_Luca/07_DocMASE/07_Data/03_FEM/InputData/modified'
    #inpDir = 'C:/02_Local-folder/01_Luca/01_WD/thinPlyMechanics/windows-cmd'
    #outDir = 'C:/02_Local-folder/01_Luca/01_WD/thinPlyMechanics/windows-cmd'
    inpDir = 'C:/Users/lucdis/Documents/WD/thinPlyMechanics/windows-cmd'
    outDir = 'C:/Users/lucdis/Documents/WD/thinPlyMechanics/windows-cmd'
    #inpDir = 'D:/OneDrive/01_Luca/07_DocMASE/07_Data/03_FEM/InputData'
    #outDir = 'D:/OneDrive/01_Luca/07_DocMASE/07_Data/03_FEM/InputData/modified'
    baseName = 'inputRVEdata'
    itbaseName = 'inputRVEiterables'
    ext = '.cmd'
    Ls = [1.144]
    #nFibsA = [0,1,5,10]
    nTotFibsA = 20
    nDebsA = [1,2,5,10]
    nFibsS = [10]

    #fileListSide = []
    #fileListAbove = []
    #fileListSideAbove = []
    #for L in Ls:
    #    for s in homogSize:
    #        fileListSide.append(baseName+'L'+L+'S'+'FHOMO'+s+ext)
    #        fileListAbove.append(baseName+'L'+L+'A'+'FHOMO'+s+ext)
    #        fileListSideAbove.append(baseName+'L'+L+'A'+'S'+'FHOMO'+s+ext)

    if not exists(outDir):
        os.mkdir(outDir)

    cmdLine = ''
    count = 0
    for L in Ls:
        for s in nFibsS:
            for da in nDebsA:
                a = nTotFibsA - da
                for dtheta in range(10,160,10):
                    if not count:
                        cmdLine += 'cd C:/02*/01*/01*/thinPlyMechanics/windows-cmd && startRVESimPipeMVDLPC ' + str(L).replace('.','_')+'S'+str(s)+'A'+str(a)+'D'+str(da)+'d'+str(dtheta)
                    else:
                        cmdLine += ' && cd C:/02*/01*/01*/thinPlyMechanics/windows-cmd && startRVESimPipeMVDLPC ' + str(L).replace('.','_')+'S'+str(s)+'A'+str(a)+'D'+str(da)+'d'+str(dtheta)
                    count += 1

    with open(join(outDir,'runMVDPipeLPCtotA20'+ext),'w') as cmd:
        cmd.write(cmdLine)





if __name__ == '__main__':
    main()
