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
from datetime import datetime
from time import strftime
import numpy as np
from scipy import sparse

#===============================================================================#
#===============================================================================#
#                              I/O functions
#===============================================================================#
#===============================================================================#

#===============================================================================#
#                                  SHELL
#===============================================================================#

def printHelp():
    print(' ')
    print(' ')
    print('*****************************************************************************************************')
    print(' ')
    print('                                        DISCRETE VCCT')
    print(' ')
    print(' ')
    print('                                              by')
    print(' ')
    print('                                    Luca Di Stasio, 2016-2019')
    print(' ')
    print(' ')
    print('*****************************************************************************************************')
    print(' ')
    print('Program syntax:')
    print(' ')
    print('discreteVCCT.py -- -dir/-directory <input file directory> -data <RVE base data> -iterables <parameters for iterations> -plot <parameters for plotting> -debug')
    print(' ')
    print(' ')
    print('Mandatory arguments:')
    print(' ')
    print('-dir/-directory <input file directory>                     ===> full/path/to/folder/without/closing/slash')
    print('-data <RVE base data>                                      ===> full/path/to/file/without/closing/slash')
    print('-iterables <parameters for iterations>                     ===> full/path/to/file/without/extension')
    print('-plot <parameters for plotting>                            ===> full/path/to/file/without/extension')
    print(' ')
    print(' ')
    print('Optional arguments:')
    print(' ')
    print('-debug                                                     ===> debug mode active')
    print(' ')
    print(' ')
    sys.exit()

#===============================================================================#
#                                  DECK file
#===============================================================================#

def fillDataDictionary(dataDict,inputKeywords,inputValue):
    if len(inputKeywords)>1:
        branchDict = dataDict.setdefault(inputKeywords[0],{})
        fillDataDictionary(branchDict,inputKeywords[1:],inputValue)
    else:
        dataDict[inputKeywords[0]] = inputValue


#===============================================================================#
#===============================================================================#
#                                 Analysis
#===============================================================================#
#===============================================================================#

def Tpq(elType,elOrder,p,q):
    tpq = 0.0
    order = {}
    order['first'] = 1
    order['second'] = 2
    order['third'] = 3
    order['fourth'] = 4
    if 'quad' in elType:
        if p==q and p<(order[elType]+1):
            tpq = 1.0
        else:
            tpq = 0.0
    return tpq

def discreteVCCT(parameters):

    #=======================================================================
    # BEGIN - compute crack tip reference frame transformation
    #=======================================================================
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Compute crack tip reference frame transformation ...',True)

    phi = parameters['geometry']['deltatheta']*np.pi/180.0

    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    #=======================================================================
    # END - compute crack tip reference frame transformation
    #=======================================================================

    #=======================================================================
    # BEGIN - compute mesh size reference frame transformation
    #=======================================================================
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Compute mesh size reference frame transformation ...',True)

    delta = parameters['mesh']['size']['delta']*np.pi/180.0

    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
    #=======================================================================
    # END - compute mesh size reference frame transformation
    #=======================================================================

    #=======================================================================
    # BEGIN - Read stiffness matrix from csv file
    #=======================================================================
    print('Read stiffness matrix from csv file...')
    with open(join(parameters['output']['local']['directory'],parameters['output']['local']['filenames']['globalstiffnessmatrix'].split('.')[0]+'.csv'),'r') as csv:
        lines = csv.readlines()
    globalMatrix = {}
    for line in lines[2:]:
        values = line.split(',')
        rowIndex = int(values[0])
        columnIndex = int(values[2])
        rowDOF = int(values[1])
        columnDOF = int(values[3])
        if rowIndex not in globalMatrix:
            globalMatrix[rowIndex] = {}
            globalMatrix[rowIndex][rowDOF] = {}
            globalMatrix[rowIndex][rowDOF][columnIndex] = {}
        elif rowDOF not in globalMatrix[rowIndex]:
            globalMatrix[rowIndex][rowDOF] = {}
            globalMatrix[rowIndex][rowDOF][columnIndex] = {}
        elif columnIndex not in globalMatrix[rowIndex][rowDOF]:
            globalMatrix[rowIndex][rowDOF][columnIndex] = {}
        globalMatrix[rowIndex][rowDOF][columnIndex][columnDOF] = int(values[-1])

    #=======================================================================
    # END - Read stiffness matrix from csv file
    #=======================================================================


#===============================================================================#
#===============================================================================#
#                                    MAIN
#===============================================================================#
#===============================================================================#

def main(argv):

    #=======================================================================
    # BEGIN - PARSE COMMAND LINE
    #=======================================================================

    debug = False

    for a,arg in enumerate(argv):
        if '-help' in arg:
            printHelp()
        elif '-dir' in arg or '-directory' in arg:
            inputDirectory = argv[a+1]
        elif '-data' in arg:
            dataFile = argv[a+1]
        elif '-iterables' in arg:
            iterablesFile = argv[a+1]
        elif '-plot' in arg:
            plotFile = argv[a+1]
        elif '-debug' in arg:
            debug = True
            print(' ')
            print(' ')
            print('>>>>-----------------------<<<<')
            print('>>>> Running in DEBUG MODE <<<<')
            print('>>>>-----------------------<<<<')
            print(' ')
            print(' ')

    if 'inputDirectory' not in locals():
        print(' ')
        print(' ')
        print('!!! ERROR: missing input directory !!!')
        print(' ')
        print(' ')
        printHelp()
    if 'dataFile' not in locals():
        print(' ')
        print(' ')
        print('!!! ERROR: missing data file !!!')
        print(' ')
        print(' ')
        printHelp()
    if 'iterablesFile' not in locals():
        print(' ')
        print(' ')
        print('!!! ERROR: missing iterables file !!!')
        print(' ')
        print(' ')
        printHelp()
    if 'plotFile' not in locals():
        print(' ')
        print(' ')
        print('!!! ERROR: missing plot file !!!')
        print(' ')
        print(' ')
        printHelp()

    #=======================================================================
    # END - PARSE COMMAND LINE
    #=======================================================================


    #=======================================================================
    # BEGIN - DATA
    #=======================================================================

    # units are already the ones used in simulation, not SI

    ABQbuiltinDict = {'ISOTROPIC':ISOTROPIC,
                      'ENGINEERING_CONSTANTS':ENGINEERING_CONSTANTS,
                      'MIDDLE_SURFACE':MIDDLE_SURFACE,
                      'FROM_SECTION':FROM_SECTION}

    if inputDirectory[-1]=='/' or inputDirectory[-1]=='\\':
        inputDirectory = inputDirectory[:-1]

    with open(join(inputDirectory,dataFile.split('.')[0]+'.deck'),'r') as deck:
        decklines = deck.readlines()

    keywords = []
    values = []

    for line in decklines:
        if line[0] == '#':
            continue
        removeComment = line.replace('\n','').split('#')[0]
        keywordSet = removeComment.split('@')[0]
        keywords.append(keywordSet.replace(' ','').split(','))
        dataType = removeComment.split('$')[1]
        if  'list of boolean' in dataType:
            listAsString = removeComment.split('@')[1].split('$')[0].replace(' ','').replace('[','').replace(']','').split(',')
            dataList = []
            for dataString in listAsString:
                dataList.append(ast.literal_eval(dataString))
            values.append(dataList)
        elif  'list of int' in dataType:
            listAsString = removeComment.split('@')[1].split('$')[0].replace(' ','').replace('[','').replace(']','').split(',')
            dataList = []
            for dataString in listAsString:
                dataList.append(int(dataString))
            values.append(dataList)
        elif  'list of float' in dataType:
            listAsString = removeComment.split('@')[1].split('$')[0].replace(' ','').replace('[','').replace(']','').split(',')
            dataList = []
            for dataString in listAsString:
                dataList.append(float(dataString))
            values.append(dataList)
        elif  'list of string' in dataType:
            listAsString = removeComment.split('@')[1].split('$')[0].replace(' ','').replace('[','').replace(']','').split(',')
            dataList = []
            for dataString in listAsString:
                dataList.append(str(dataString))
            values.append(dataList)
        elif  'list of ABAQUS keyword' in dataType:
            values.append(ABQbuiltinDict[removeComment.split('@')[1].split('$')[0]])
            listAsString = removeComment.split('@')[1].split('$')[0].replace(' ','').replace('[','').replace(']','').split(',')
            dataList = []
            for dataString in listAsString:
                dataList.append(ABQbuiltinDict[dataString])
            values.append(dataList)
        elif 'boolean' in dataType:
            values.append(ast.literal_eval(removeComment.split('@')[1].split('$')[0].replace(' ','')))
        elif  'int' in dataType:
            values.append(int(removeComment.split('@')[1].split('$')[0].replace(' ','')))
        elif  'float' in dataType:
            values.append(float(removeComment.split('@')[1].split('$')[0].replace(' ','')))
        elif  'string' in dataType:
            values.append(str(removeComment.split('@')[1].split('$')[0].replace(' ','')))
        elif  'ABAQUS keyword' in dataType:
            values.append(ABQbuiltinDict[removeComment.split('@')[1].split('$')[0].replace(' ','')])

    RVEparams = {}

    for k,keywordSet in enumerate(keywords):
        fillDataDictionary(RVEparams,keywordSet,values[k])

    # parameters for iterations
    # RVEparams['modelname']
    # RVEparams['deltatheta']
    # RVEparams['deltapsi']
    # RVEparams['deltaphi']

    #=======================================================================
    # END - DATA
    #=======================================================================

    #=======================================================================
    # BEGIN - ITERABLES
    #=======================================================================

    with open(join(inputDirectory,iterablesFile.split('.')[0]+'.deck'),'r') as deck:
        decklines = deck.readlines()

    for l,line in enumerate(decklines):
        if line[0] == '#':
            continue
        elif 'basename' in line:
            basename = str(line.replace('\n','').split('#')[0].split('$')[0].split('@')[1].replace(' ',''))
        elif 'free parameters' in line:
            freeParamsStart = l+1

    keywords = []
    values = []
    lenOfValues = []

    for line in decklines[freeParamsStart:]:
        if line[0] == '#':
            continue
        removeComment = line.replace('\n','').split('#')[0]
        keywordSet = removeComment.split('@')[0]
        keywords.append(keywordSet.replace(' ','').split(','))
        dataType = removeComment.split('$')[1]
        listAsString = removeComment.split('@')[1].split('$')[0].replace('[','').replace(']','').split(',')
        dataList = []
        for dataString in listAsString:
            dataList.append(float(dataString))
        if 'min' in dataType and 'max' in dataType and 'step' in dataType:
            values.append(np.arange(dataList[0],dataList[1]+dataList[2],dataList[2]))
        else:
            values.append(dataList)
        lenOfValues.append(len(values[-1]))

    lenSortedIndeces = np.argsort(lenOfValues)
    sortedValues = []
    sortedKeywords = []
    for index in lenSortedIndeces:
        sortedValues.append(values[index])
        sortedKeywords.append(keywords[index])

    iterationsSets = []
    indecesCollection = []

    totalSets = 1
    for valueSet in sortedValues:
        totalSets *= len(valueSet)

    indeces = []
    for j in range(0,len(sortedKeywords)):
        indeces.append(0)
    indecesCollection.append(indeces)
    iterationSet = []
    for i,index in enumerate(indeces):
        iterationSet.append(sortedValues[i][index])
    iterationsSets.append(iterationSet)

    for k in range(1,totalSets):
        indeces = []
        for j in range(0,len(sortedKeywords)-1):
            indeces.append(0)
        if indecesCollection[k-1][-1]==len(sortedValues[-1])-1:
            indeces.append(0)
        else:
            indeces.append(indecesCollection[k-1][-1] + 1)
        for j in range(len(sortedKeywords)-2,-1,-1):
            if indeces[j+1]==0:
                if indecesCollection[k-1][j]==len(sortedValues[j])-1:
                    indeces.append(0)
                else:
                    indeces.append(indecesCollection[k-1][j] + 1)
            else:
                indeces.append(indecesCollection[k-1][j])
        indecesCollection.append(indeces)
        iterationSet = []
        for i,index in enumerate(indeces):
            iterationSet.append(sortedValues[i][index])
        iterationsSets.append(iterationSet)

    #=======================================================================
    # END - ITERABLES
    #=======================================================================

    #=======================================================================
    # BEGIN - PLOT SETTINGS
    #=======================================================================

    with open(join(inputDirectory,plotFile.split('.')[0]+'.deck'),'r') as deck:
        decklines = deck.readlines()

    keywords = []
    values = []

    for line in decklines:
        if line[0] == '#':
            continue
        removeComment = line.replace('\n','').split('#')[0]
        keywordSet = removeComment.split('@')[0]
        keywords.append(keywordSet.replace(' ','').split(','))
        dataType = removeComment.split('$')[1]
        if  'list of boolean' in dataType:
            listAsString = removeComment.split('@')[1].split('$')[0].replace(' ','').replace('[','').replace(']','').split(',')
            dataList = []
            for dataString in listAsString:
                dataList.append(ast.literal_eval(dataString))
            values.append(dataList)
        elif  'list of int' in dataType:
            listAsString = removeComment.split('@')[1].split('$')[0].replace(' ','').replace('[','').replace(']','').split(',')
            dataList = []
            for dataString in listAsString:
                dataList.append(int(dataString))
            values.append(dataList)
        elif  'list of float' in dataType:
            listAsString = removeComment.split('@')[1].split('$')[0].replace(' ','').replace('[','').replace(']','').split(',')
            dataList = []
            for dataString in listAsString:
                dataList.append(float(dataString))
            values.append(dataList)
        elif  'list of string' in dataType:
            listAsString = removeComment.split('@')[1].split('$')[0].replace('[','').replace(']','').split(',')
            dataList = []
            for dataString in listAsString:
                dataList.append(str(dataString))
            values.append(dataList)
        elif  'list of ABAQUS keyword' in dataType:
            values.append(ABQbuiltinDict[removeComment.split('@')[1].split('$')[0]])
            listAsString = removeComment.split('@')[1].split('$')[0].replace(' ','').replace('[','').replace(']','').split(',')
            dataList = []
            for dataString in listAsString:
                dataList.append(ABQbuiltinDict[dataString])
            values.append(dataList)
        elif 'boolean' in dataType:
            values.append(ast.literal_eval(removeComment.split('@')[1].split('$')[0].replace(' ','')))
        elif  'int' in dataType:
            values.append(int(removeComment.split('@')[1].split('$')[0].replace(' ','')))
        elif  'float' in dataType:
            values.append(float(removeComment.split('@')[1].split('$')[0].replace(' ','')))
        elif  'string' in dataType:
            values.append(str(removeComment.split('@')[1].split('$')[0]))
        elif  'ABAQUS keyword' in dataType:
            values.append(ABQbuiltinDict[removeComment.split('@')[1].split('$')[0].replace(' ','')])

    for k,keywordSet in enumerate(keywords):
        fillDataDictionary(RVEparams,keywordSet,values[k])

    #=======================================================================
    # END - PLOT SETTINGS
    #=======================================================================

    #=======================================================================
    # BEGIN - ANALYSIS
    #=======================================================================

    workDir = RVEparams['input']['wd']

    RVEparams['output']['global']['filenames']['energyreleaserate'] = basename + '_ERRTS'

    for iterationSet in iterationsSets:

        timedataList = []
        totalIterationTime = 0.0
        variationString = ''
        for v,value in enumerate(iterationSet):
            if v>0:
                variationString += '-'
            variationString += str(sortedKeywords[v][-1]) + str(value).replace('.','_')
            fillDataDictionary(RVEparams,sortedKeywords[v],value)

        RVEparams['input']['modelname'] = basename + '_' + variationString
        RVEparams['output']['local']['directory'] = join(RVEparams['output']['global']['directory'],RVEparams['input']['modelname'])
        RVEparams['output']['local']['filenames']['globalstiffnessmatrix'] = RVEparams['input']['modelname'] + '-globalstiffnessmatrix'
        RVEparams['output']['local']['filenames']['globalloadvector'] = RVEparams['input']['modelname'] + '-globalloadvector'
        RVEparams['output']['local']['filenames']['globaldispvector'] = RVEparams['input']['modelname'] + '-globaldispvector'




if __name__ == "__main__":
    main(sys.argv[1:])
