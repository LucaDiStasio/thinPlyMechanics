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
    inpDir = 'C:/Abaqus_WD/ElType'
    outDir = 'C:/Abaqus_WD/ElType/modified'
    #inpDir = 'D:/OneDrive/01_Luca/07_DocMASE/07_Data/03_FEM/InputData'
    #outDir = 'D:/OneDrive/01_Luca/07_DocMASE/07_Data/03_FEM/InputData/modified'
    baseName = 'inputRVEdata'
    itbaseName = 'inputRVEiterables'
    ext = '.deck'
    Ls = [1.144]
    elTypes = ['PS','GPE']
    nFibsA = [0,1,5,10]
    nFibS = [0,5,10]

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

    for L in Ls:
        for elType in elTypes:
            for s in nFibS:
                for a in nFibA:
                    with open(join(inpDir,baseName+'Free'+'L'+str(L).replace('.','_')+'S'+str(s)+'A'+str(a)+elType+'-LPC'+ext),'r') as inp:
                        lines = inp.readlines()
                    newlines = []
                    for line in lines:
                        if 'L'+str(L).replace('.','_')+'S'+str(s)+'A'+str(a) in line:
                            newlines.append(line.replace('L'+str(L).replace('.','_')+'S'+str(s)+'A'+str(a),'L'+str(L).replace('.','_')+'S'+str(s)+'A'+str(a)+'T1'))
                        elif 'materials, 2, elastic, values' in line:
                            newlines.append(line)
                            newlines.append('materials, 3, name            @UD $string' + '\n')
                            newlines.append('materials, 3, elastic, type   @ENGINEERING_CONSTANTS $ABAQUS keyword' + '\n')
                            newlines.append('materials, 3, elastic, values @[43442,13714,13714,0.273,0.273,0.465,4315,4315,4681] $list of float' + '\n')
                        elif 'sections, 2, thickness' in line:
                            newlines.append(line)
                            newlines.append('sections, 3, name      @udSection $string' + '\n')
                            newlines.append('sections, 3, type      @HomogeneousSolidSection $string' + '\n')
                            newlines.append('sections, 3, material  @UD $string' + '\n')
                            newlines.append('sections, 3, thickness @1.0 $float' + '\n')
                        elif 'sectionRegions, ' + str(getMaxSectionNumber(s,a)) + ', offsetValue' in line:
                            newlines.append(line)
                            newlines.append('sectionRegions, ' + str(getMaxSectionNumber(s,a)+1) + ', name                 @udSection $string' + '\n')
                            newlines.append('sectionRegions, ' + str(getMaxSectionNumber(s,a)+1) + ', set                  @BOUNDING-PLY $string' + '\n')
                            newlines.append('sectionRegions, ' + str(getMaxSectionNumber(s,a)+1) + ', offsetType           @MIDDLE_SURFACE $ABAQUS keyword' + '\n')
                            newlines.append('sectionRegions, ' + str(getMaxSectionNumber(s,a)+1) + ', offsetField          @  $string' + '\n')
                            newlines.append('sectionRegions, ' + str(getMaxSectionNumber(s,a)+1) + ', thicknessAssignment  @FROM_SECTION $ABAQUS keyword' + '\n')
                            newlines.append('sectionRegions, ' + str(getMaxSectionNumber(s,a)+1) + ', offsetValue          @0.0 $float' + '\n')
                        elif 'BC, northSide, type' in line:
                            if a>0:
                                newlines.append('BC, northSide, type     @adjacentFibersboundingPly $string' + '\n')
                            else:
                                newlines.append('BC, northSide, type     @boundingPly $string' + '\n')
                        elif 'BC, northSide, tRatio' in line:
                            newlines.append('BC, northSide, tRatio   @1.0 $float' + '\n')
                        else:
                            newlines.append(line)
                    with open(join(outDir,baseName+'Free'+'L'+str(L).replace('.','_')+'S'+str(s)+'A'+str(a)+'T1'+elType+'-LPC'+ext),'w') as out:
                        for line in newlines:
                            out.write(line)
                    with open(join(inpDir,itbaseName+'Free'+'L'+str(L).replace('.','_')+'S'+str(s)+'A'+str(a)+elType+'-LPC'+ext),'r') as inp:
                        lines = inp.readlines()
                    with open(join(outDir,itbaseName+'L'+L+'S'+str(n)+'FCOARED'+ext),'w') as out:
                        for line in lines:
                            if 'L'+str(L).replace('.','_')+'S'+str(s)+'A'+str(a) in line:
                                out.write(line.replace('L'+str(L).replace('.','_')+'S'+str(s)+'A'+str(a),'L'+str(L).replace('.','_')+'S'+str(s)+'A'+str(a)+'T1'))
                            else:
                                out.write(line)


if __name__ == '__main__':
    main()
