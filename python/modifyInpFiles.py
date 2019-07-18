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
                #with open(join(inpDir,itbaseName+'L'+L+'S'+'FHOMO'+s+ext),'r') as inp:
                with open(join(inpDir,itbaseName+'L'+L+'S'+str(n)+'FCOARED'+ext),'r') as inp:
                    lines = inp.readlines()
                #with open(join(outDir,itbaseName+'L'+L+'S'+'FHOMO'+s+ext),'w') as out:
                with open(join(outDir,itbaseName+'L'+L+'S'+str(n)+'FCOARED'+ext),'w') as out:
                    for line in lines:
                        #if 'basename' in line:
                            #newline = line.replace('sf'+str(nFib),'sf'+str(nFib+1))
                        if '1_618' in line:
                            newline = line.replace('1_618',L)
                            out.write(newline)
                        else:
                            out.write(line)

    for L in Ls:
        #for s in homogSize:
        for n in nFibs:
            #with open(join(inpDir,baseName+'L'+L+'A'+'FHOMO'+s+ext),'r') as inp:
            with open(join(inpDir,baseName+'L'+L+'A'+str(n)+'FCOARED'+ext),'r') as inp:
                lines = inp.readlines()
            #with open(join(outDir,baseName+'L'+L+'A'+'FHOMO'+s+ext),'w') as out:
            with open(join(outDir,baseName+'L'+L+'A'+str(n)+'FCOARED'+ext),'w') as out:
                for line in lines:
                    #if 'BC' in line and 'northSide' in line and 'nFibers' in line:
                    #    nFib = int(line.split('$')[0].split('@')[1])
                    #    newline = 'BC, northSide, nFibers @' + str(nFib+1) + '     $int' + '\n'
                    #    out.write(newline)
                    if '1_618' in line:
                        newline = line.replace('1_618',L)
                        out.write(newline)
                    elif '1.618' in line:
                        newline = line.replace('1.618',L.replace('_','.'))
                        out.write(newline)
                    else:
                        out.write(line)
            #with open(join(inpDir,itbaseName+'L'+L+'A'+'FHOMO'+s+ext),'r') as inp:
            with open(join(inpDir,itbaseName+'L'+L+'A'+str(n)+'FCOARED'+ext),'r') as inp:
                lines = inp.readlines()
            #with open(join(outDir,itbaseName+'L'+L+'A'+'FHOMO'+s+ext),'w') as out:
            with open(join(outDir,itbaseName+'L'+L+'A'+str(n)+'FCOARED'+ext),'w') as out:
                for line in lines:
                    #if 'basename' in line:
                    #    newline = line.replace('af'+str(nFib),'af'+str(nFib+1))
                    if '1_618' in line:
                        newline = line.replace('1_618',L)
                        out.write(newline)
                    else:
                        out.write(line)

    for L in Ls:
        #for s in homogSize:
        for n in nFibs:
            for m in nFibsA:
                if not m>n:
                    #with open(join(inpDir,baseName+'L'+L+'A'+'S'+'FHOMO'+s+ext),'r') as inp:
                    with open(join(inpDir,baseName+'L'+L+'A'+str(m)+'S'+str(n)+'FCOARED'+ext),'r') as inp:
                        lines = inp.readlines()
                    #for line in lines:
                    #    if 'BC' in line and 'rightSide' in line and 'nFibers' in line:
                    #        nFibS = int(line.split('$')[0].split('@')[1])
                    #    elif 'BC' in line and 'northSide' in line and 'nFibers' in line:
                    #        nFibA = int(line.split('$')[0].split('@')[1])
                    #if nFibS == nFibA:
                    #    newnFibS = nFibS + 1
                    #    newnFibA = 1
                    #else:
                    #    newnFibS = nFibS
                    #    newnFibA = nFibA + 1
                    #with open(join(outDir,baseName+'L'+L+'A'+'S'+'FHOMO'+s+ext),'w') as out:
                    with open(join(outDir,baseName+'L'+L+'A'+str(m)+'S'+str(n)+'FCOARED'+ext),'w') as out:
                        for line in lines:
                            #if 'BC' in line and 'rightSide' in line and 'nFibers' in line:
                            #    newline = 'BC, rightSide, nFibers @' + str(newnFibS) + '     $int' + '\n'
                            #    out.write(newline)
                            #elif 'BC' in line and 'leftSide' in line and 'nFibers' in line:
                            #    newline = 'BC, leftSide, nFibers @' + str(newnFibS) + '     $int' + '\n'
                            #    out.write(newline)
                            #elif 'BC' in line and 'northSide' in line and 'nFibers' in line:
                            #    newline = 'BC, northSide, nFibers @' + str(newnFibA) + '     $int' + '\n'
                            #    out.write(newline)
                            if '1_618' in line:
                                newline = line.replace('1_618',L)
                                out.write(newline)
                            elif '1.618' in line:
                                newline = line.replace('1.618',L.replace('_','.'))
                                out.write(newline)
                            else:
                                out.write(line)
                    #with open(join(inpDir,itbaseName+'L'+L+'A'+'S'+'FHOMO'+s+ext),'r') as inp:
                    with open(join(inpDir,itbaseName+'L'+L+'A'+str(m)+'S'+str(n)+'FCOARED'+ext),'r') as inp:
                        lines = inp.readlines()
                    #with open(join(outDir,itbaseName+'L'+L+'A'+'S'+'FHOMO'+s+ext),'w') as out:
                    with open(join(outDir,itbaseName+'L'+L+'A'+str(m)+'S'+str(n)+'FCOARED'+ext),'w') as out:
                        for line in lines:
                            #if 'basename' in line:
                            #    newline = line.replace('sf'+str(nFibS),'sf'+str(newnFibS)).replace('af'+str(nFibA),'af'+str(newnFibA))
                            #    out.write(newline)
                            if '1_618' in line:
                                newline = line.replace('1_618',L)
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
