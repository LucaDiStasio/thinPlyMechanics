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

def writeIntro(fullPath):
    with open(fullPath,'w') as out:
        out.write('# Automatically generated on ' + datetime.now().strftime('%d/%m/%Y') + ' at ' + datetime.now().strftime('%H:%M:%S') + '\n')
        out.write('# everything after is a comment' + '\n')
        out.write('# keywords are divided by commas: keyword1, keyword2, ...' + '\n')
        out.write('# the corresponding value is introduced by @' + '\n')
        out.write('# variable type is introduced by $' + '\n')
        out.write('#' + '\n')

def writePipelineControls(fullPath,pipelineControls):
    with open(fullPath,'a') as out:
        out.write('# Select execution steps in the pipeline' + '\n')
        for key in pipelineControls:
            out.write('# simulation-pipeline, ' + str(key) + ' @' + str(pipelineControls[key]) + ' $boolean' + '\n')
        out.write('#' + '\n')

def writeAnalysisControls(fullPath,analysisControls):
    with open(fullPath,'a') as out:
        out.write('# Select outputs in the analysis phase' + '\n')
        for key in analysisControls:
            out.write('# simulation-pipeline, analysis, ' + str(key) + ' @' + str(analysisControls[key]) + ' $boolean' + '\n')
        out.write('#' + '\n')

def main():

    PC = 'LucaPC'
    onedriveSubfolder = '01_Luca/07_DocMASE/07_Data/03_FEM/InputData/new'

    if PC=='LucaPC':
        outDir = 'C:/Users/luca/OneDrive/' + onedriveSubfolder
    elif PC=='EEIGM':
        outDir = 'D:/OneDrive/' + onedriveSubfolder
    else:
        outDir = 'C:/Users/lucdis/OneDrive/' + onedriveSubfolder

    if PC=='LucaPC':
        ending = '-LPC'
    else:
        ending = '-COARED'

    datbaseName = 'inputRVEdata'
    itbaseName = 'inputRVEiterables'
    ext = '.deck'
    Ls = ['1_25','1_144','1_0992']
    #homogSize = ['1','2','3','5']
    nFibsAb = [1,2,3,5,10,50,100]
    nFibsSi = [10,50,100]

    nickName = 'Asymm'

    if not exists(outDir):
        os.mkdir(outDir)

    pipeline = {}
    pipeline['create-CAE'] = 'True'
    pipeline['modify-INP'] = 'True'
    pipeline['analyze-ODB'] = 'True'
    pipeline['archive-ODB'] = 'False'
    pipeline['archive-CAE'] = 'False'
    pipeline['remove-ODB'] = 'True'
    pipeline['remove-DAT'] = 'True'
    pipeline['remove-PRT'] = 'True'
    pipeline['remove-STA'] = 'True'
    pipeline['remove-SIM'] = 'True'
    pipeline['remove-MSG'] = 'True'
    pipeline['remove-INP'] = 'True'
    pipeline['remove-COM'] = 'True'
    pipeline['report-LATEX'] = 'False'
    pipeline['report-EXCEL'] = 'False'
    analysis = {}
    for L in Ls:
        #for s in homogSize:
        for n in nFibsSi:
            writeIntro(join(inpDir,datbaseName+nickName+'L'+L+'S'+str(n)+'-LPC'+ext))
            writeIntro(join(inpDir,itbaseName+nickName+'L'+L+'S'+str(n)+'-LPC'+ext))




if __name__ == '__main__':
    main()
