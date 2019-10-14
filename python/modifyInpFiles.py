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
    inpDir = 'C:/Users/lucad/OneDrive/01_Luca/07_DocMASE/07_Data/03_FEM/InputData/MultipleVerticalDebonds'
    outDir = 'C:/Users/lucad/OneDrive/01_Luca/07_DocMASE/07_Data/03_FEM/InputData/MultipleVerticalDebonds/modified'
    #inpDir = 'D:/OneDrive/01_Luca/07_DocMASE/07_Data/03_FEM/InputData'
    #outDir = 'D:/OneDrive/01_Luca/07_DocMASE/07_Data/03_FEM/InputData/modified'
    baseName = 'inputRVEdata'
    itbaseName = 'inputRVEiterables'
    ext = '.deck'
    Ls = [1.144]
    #nFibsA = [0,1,5,10]
    nTotFibsA = 100
    nDebsA = [1,2,5,10]
    nFibsS = [50]

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
            for s in nFibsS:
                for da in nDebsA:
                    a = nTotFibsA - da
                    for dtheta in range(10,160,10):
                        with open(join(inpDir,'inputRVEdataMVDfreeasymmL1_144S1d10COARED'+ext),'r') as inp:
                            lines = inp.readlines()
                        newlines = []
                        insertSectionAssignment = False
                        for line in lines:
                            if 'L1_144S1d10' in line:
                                newlines.append(line.replace('L1_144S1d10','L'+str(L).replace('.','_')+'S'+str(s)+'A'+str(a)+'D'+str(da)+'d'+str(dtheta)))
                            elif 'geometry, nDebonds' in line:
                                newlines.append('geometry, nDebonds            @' + str(da) +'                $int' + '\n')
                            elif 'geometry, debonds, deltatheta' in line:
                                newline = 'geometry, debonds, deltatheta @['
                                for deb in range(1,da+1):
                                    if deb>1:
                                        newline += ','
                                    newline += str(dtheta)
                                newline += ']  $list of float'
                                newlines.append(newline + '\n')
                            elif 'geometry, debonds, theta' in line:
                                newline = 'geometry, debonds, theta @['
                                for deb in range(1,da+1):
                                    if deb>1:
                                        newline += ','
                                    if deb%2>0:
                                        newline += str(180.0)
                                    else:
                                        newline += str(0.0)
                                newline += ']  $list of float'
                                newlines.append(newline + '\n')
                            elif 'sectionRegions'  in line and '@DEBFIBER-ROWS-FIBERS' in line:
                                insertSectionAssignment = True
                            elif insertSectionAssignment and 'sectionRegions'  in line and 'offsetValue'  in line:
                                newlines.append(line)
                                newlines.append('sectionRegions, 6, name                 @fiberSection $string' + '\n')
                                newlines.append('sectionRegions, 6, set                  @UPPER-FIBERS $string' + '\n')
                                newlines.append('sectionRegions, 6, offsetType           @MIDDLE_SURFACE $ABAQUS keyword' + '\n')
                                newlines.append('sectionRegions, 6, offsetField          @  $string' + '\n')
                                newlines.append('sectionRegions, 6, thicknessAssignment  @FROM_SECTION $ABAQUS keyword' + '\n')
                                newlines.append('sectionRegions, 6, offsetValue          @0.0 $float' + '\n')
                                insertSectionAssignment = False
                            elif 'BC, northSide, type' in line:
                                newlines.append('BC, northSide, type     @adjacentFibers $string' + '\n')
                            elif 'BC, northSide, nFibers' in line:
                                newlines.append('BC, northSide, nFibers  @' + str(a) + ' $int' + '\n')
                            else:
                                newlines.append(line)
                        with open(join(inpDir,baseName+'MVDfreeasymm'+'L'+str(L).replace('.','_')+'S'+str(s)+'A'+str(a)+'D'+str(da)+'d'+str(dtheta)+'COARED'+ext),'w') as inp:
                            for line in newlines:
                                inp.write(line)
                        with open(join(inpDir,itbaseName+'MVDfreeasymm'+'L'+str(L).replace('.','_')+'S'+str(s)+'A'+str(a)+'D'+str(da)+'d'+str(dtheta)+'COARED'+ext),'w') as inp:
                            inp.write('# everything after is a comment' + '\n')
                            inp.write('# keywords are divided by commas: keyword1, keyword2, ...' + '\n')
                            inp.write('# the corresponding value is introduced by @' + '\n')
                            inp.write('# variable type is introduced by $' + '\n')
                            inp.write('#' + '\n')
                            inp.write('# Output directory and filenames' + '\n')
                            inp.write('basename             @RVE1_144-HSD-MVDfreeasymm'+'L'+str(L).replace('.','_')+'S'+str(s)+'A'+str(a)+'D'+str(da)+'d'+str(dtheta)+' $string' + '\n')
                            inp.write('free parameters      @1             $int' + '\n')
                            inp.write('geometry, deltatheta @[' + str(dtheta) + ',' + str(dtheta) + ',10]   $min,max,step #other possibility: [v1,v2,...,vn] $ list of values' + '\n')
                        with open(join(inpDir,'inputRVEdataMVDfreeasymmL1_144S1d10COARED'+ext),'r') as inp:
                            lines = inp.readlines()
                        newlines = []
                        insertSectionAssignment = False
                        for line in lines:
                            if 'L1_144S1d10' in line:
                                newlines.append(line.replace('asymmL1_144S1d10','symmL'+str(L).replace('.','_')+'S'+str(s)+'A'+str(a)+'D'+str(da)+'d'+str(dtheta)))
                            elif 'geometry, nDebonds' in line:
                                newlines.append('geometry, nDebonds            @' + str(da) +'                $int' + '\n')
                            elif 'geometry, debonds, deltatheta' in line:
                                newline = 'geometry, debonds, deltatheta @['
                                for deb in range(1,da+1):
                                    if deb>1:
                                        newline += ','
                                    newline += str(dtheta)
                                newline += ']  $list of float'
                                newlines.append(newline + '\n')
                            elif 'geometry, debonds, theta' in line:
                                newline = 'geometry, debonds, theta @['
                                for deb in range(1,da+1):
                                    if deb>1:
                                        newline += ','
                                    newline += str(0.0)
                                newline += ']  $list of float'
                                newlines.append(newline + '\n')
                            elif 'sectionRegions'  in line and '@DEBFIBER-ROWS-FIBERS' in line:
                                insertSectionAssignment = True
                            elif insertSectionAssignment and 'sectionRegions'  in line and 'offsetValue'  in line:
                                newlines.append(line)
                                newlines.append('sectionRegions, 6, name                 @fiberSection $string' + '\n')
                                newlines.append('sectionRegions, 6, set                  @UPPER-FIBERS $string' + '\n')
                                newlines.append('sectionRegions, 6, offsetType           @MIDDLE_SURFACE $ABAQUS keyword' + '\n')
                                newlines.append('sectionRegions, 6, offsetField          @  $string' + '\n')
                                newlines.append('sectionRegions, 6, thicknessAssignment  @FROM_SECTION $ABAQUS keyword' + '\n')
                                newlines.append('sectionRegions, 6, offsetValue          @0.0 $float' + '\n')
                                insertSectionAssignment = False
                            elif 'BC, northSide, type' in line:
                                newlines.append('BC, northSide, type     @adjacentFibers $string' + '\n')
                            elif 'BC, northSide, nFibers' in line:
                                newlines.append('BC, northSide, nFibers  @' + str(a) + ' $int' + '\n')
                            else:
                                newlines.append(line)
                        with open(join(inpDir,baseName+'MVDfreesymm'+'L'+str(L).replace('.','_')+'S'+str(s)+'A'+str(a)+'D'+str(da)+'d'+str(dtheta)+'COARED'+ext),'w') as inp:
                            for line in newlines:
                                inp.write(line)
                        with open(join(inpDir,itbaseName+'MVDfreeasymm'+'L'+str(L).replace('.','_')+'S'+str(s)+'A'+str(a)+'D'+str(da)+'d'+str(dtheta)+'COARED'+ext),'w') as inp:
                            inp.write('# everything after is a comment' + '\n')
                            inp.write('# keywords are divided by commas: keyword1, keyword2, ...' + '\n')
                            inp.write('# the corresponding value is introduced by @' + '\n')
                            inp.write('# variable type is introduced by $' + '\n')
                            inp.write('#' + '\n')
                            inp.write('# Output directory and filenames' + '\n')
                            inp.write('basename             @RVE1_144-HSD-MVDfreesymm'+'L'+str(L).replace('.','_')+'S'+str(s)+'A'+str(a)+'D'+str(da)+'d'+str(dtheta)+' $string' + '\n')
                            inp.write('free parameters      @1             $int' + '\n')
                            inp.write('geometry, deltatheta @[' + str(dtheta) + ',' + str(dtheta) + ',10]   $min,max,step #other possibility: [v1,v2,...,vn] $ list of values' + '\n')



if __name__ == '__main__':
    main()
