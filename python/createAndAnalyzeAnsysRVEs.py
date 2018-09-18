#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
=====================================================================================

Copyright (c) 2016-2018 Université de Lorraine or Luleå tekniska universitet
Author: Luca Di Stasio <luca.distasio@gmail.com>
                       <luca.distasio@ingpec.eu>

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in
the documentation and/or other materials provided with the distribution
Neither the name of the Université de Lorraine or Luleå tekniska universitet
nor the names of its contributors may be used to endorse or promote products
derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.

=====================================================================================

DESCRIPTION

Tested with Abaqus Python 2.6 (64-bit) distribution in Windows 7.

'''
import sys, os
import numpy as np
import math
import subprocess
from os.path import isfile, join, exists
from platform import platform,system
from shutil import copyfile
import sqlite3
import locale
import ast
from datetime import datetime
from time import strftime, sleep
import timeit

#===============================================================================#
#===============================================================================#
#                              I/O functions
#===============================================================================#
#===============================================================================#

#===============================================================================#
#                                  SHELL
#===============================================================================#

def printHelp():
    print >> sys.__stdout__,(' ')
    print >> sys.__stdout__,(' ')
    print >> sys.__stdout__,('*****************************************************************************************************')
    print >> sys.__stdout__,(' ')
    print >> sys.__stdout__,('                       CREATION AND ANALYSIS OF RVEs/RUCs WITH FEM IN ANSYS')
    print >> sys.__stdout__,(' ')
    print >> sys.__stdout__,(' ')
    print >> sys.__stdout__,('                                              by')
    print >> sys.__stdout__,(' ')
    print >> sys.__stdout__,('                                    Luca Di Stasio, 2016-2018')
    print >> sys.__stdout__,(' ')
    print >> sys.__stdout__,(' ')
    print >> sys.__stdout__,('*****************************************************************************************************')
    print >> sys.__stdout__,(' ')
    print >> sys.__stdout__,('Program syntax:')
    print >> sys.__stdout__,(' ')
    print >> sys.__stdout__,('python createAndAnalyzeAnsysRVEs.py -dir/-directory <input file directory> -data <RVE base data> -iterables <parameters for iterations> -plot <parameters for plotting> -debug')
    print >> sys.__stdout__,(' ')
    print >> sys.__stdout__,(' ')
    print >> sys.__stdout__,('Mandatory arguments:')
    print >> sys.__stdout__,(' ')
    print >> sys.__stdout__,('-dir/-directory <input file directory>                     ===> full/path/to/folder/without/closing/slash')
    print >> sys.__stdout__,('-data <RVE base data>                                      ===> full/path/to/file/without/closing/slash')
    print >> sys.__stdout__,('-iterables <parameters for iterations>                     ===> full/path/to/file/without/extension')
    print >> sys.__stdout__,('-plot <parameters for plotting>                            ===> full/path/to/file/without/extension')
    print >> sys.__stdout__,(' ')
    print >> sys.__stdout__,(' ')
    print >> sys.__stdout__,('Optional arguments:')
    print >> sys.__stdout__,(' ')
    print >> sys.__stdout__,('-debug                                                     ===> debug mode active')
    print >> sys.__stdout__,(' ')
    print >> sys.__stdout__,(' ')
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
#                                    CSV files
#===============================================================================#

def createCSVfile(dir,filename,titleline=None):
    if len(filename.split('.'))<2:
        filename += '.csv'
    with open(join(dir,filename),'w') as csv:
        if titleline != None:
            csv.write(titleline.replace('\n','') + '\n')
        else:
            csv.write('# Automatically created on ' + datetime.now().strftime('%d/%m/%Y') + ' at' + datetime.now().strftime('%H:%M:%S') + '\n')

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
                if v>0:
                    line += ', '
                line += str(value)
            csv.write(line + '\n')

#===============================================================================#
#                            ANSYS command files
#===============================================================================#

def createANSfile(ansFullPath,titleline=None):
    with open(ansFullPath,'w') as ans:
        if titleline != None:
            csv.write('!' + titleline.replace('\n','') + '\n')
        csv.write('! Automatically created on ' + datetime.now().strftime('%d/%m/%Y') + ' at' + datetime.now().strftime('%H:%M:%S') + '\n')

def writeLicense(ansFullPath):
    with open(ansFullPath,'a') as ans:
        ans.write('!' + '\n')
        ans.write('!==============================================================================' + '\n')
        ans.write('! Copyright (c) 2016-' + datetime.now().strftime('%Y') + ' Universite de Lorraine & Lulea tekniska universitet' + '\n')
        ans.write('! Author: Luca Di Stasio <luca.distasio@gmail.com>' + '\n')
        ans.write('!                        <luca.distasio@ingpec.eu>' + '\n')
        ans.write('!' + '\n')
        ans.write('! Redistribution and use in source and binary forms, with or without' + '\n')
        ans.write('! modification, are permitted provided that the following conditions are met:' + '\n')
        ans.write('!
        ans.write('!' + '\n')
        ans.write('! Redistributions of source code must retain the above copyright' + '\n')
        ans.write('! notice, this list of conditions and the following disclaimer.' + '\n')
        ans.write('! Redistributions in binary form must reproduce the above copyright' + '\n')
        ans.write('! notice, this list of conditions and the following disclaimer in' + '\n')
        ans.write('! the documentation and/or other materials provided with the distribution' + '\n')
        ans.write('! Neither the name of the Universite de Lorraine & Lulea tekniska universitet' + '\n')
        ans.write('! nor the names of its contributors may be used to endorse or promote products' + '\n')
        ans.write('! derived from this software without specific prior written permission.' + '\n')
        ans.write('!' + '\n')
        ans.write('! THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"' + '\n')
        ans.write('! AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE' + '\n')
        ans.write('! IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE' + '\n')
        ans.write('! ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE' + '\n')
        ans.write('! LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR' + '\n')
        ans.write('! CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF' + '\n')
        ans.write('! SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS' + '\n')
        ans.write('! INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN' + '\n')
        ans.write('! CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)' + '\n')
        ans.write('! ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE' + '\n')
        ans.write('! POSSIBILITY OF SUCH DAMAGE.' + '\n')
        ans.write('!==============================================================================' + '\n')
        ans.write('!' + '\n')

def writeAnsTitle(ansFullPath,title):
    with open(ansFullPath,'a') as ans:
        ans.write('!' + '\n')
        ans.write('/' + 'title, ' + title + '\n')
        ans.write('!' + '\n')

def writeAnsInpData(ansFullPath,parameters):
    with open(ansFullPath,'a') as ans:
        ans.write('!' + '\n')
        ans.write('/' + 'prep7               ! Enter the pre-processor' + '\n')
        ans.write('!' + '\n')
        ans.write('! Parameters' + '\n')
        ans.write('!' + '\n')
        ans.write('! ===> START INPUT DATA' + '\n')
        ans.write('!' + '\n')
        for input in parameters['inputData'].values():
            ans.write(input['name'] + ' = ' + str(input['value']) + '\n')
        ans.write('!' + '\n')
        ans.write('! ===> END INPUT DATA' + '\n')
        ans.write('!' + '\n')

def writeAnsBody(ansFullPath,ansTemplateFullPath):
    with open(ansTemplateFullPath,'r') as tem:
        lines = tem.readlines()
    with open(ansFullPath,'a') as ans:
        for line in lines:
            ans.write(line)

def createAPDL(params,logfilepath,baselogindent,logindent):
    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + 'In function createAPDL(params,logfilepath,baselogindent,logindent)',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '- Working directory: ' + params['input']['wd'],True)
    if not params['input']['apdlfilename'].split('.')>0:
        params['input']['apdlfilename'] += '.cmd'
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '- APDL file name: ' + params['input']['apdlfilename'],True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '- Template directory: ' + params['input']['templatedir'],True)
    if not params['input']['apdltemplate'].split('.')>0:
        params['input']['apdltemplate'] += '.cmd'
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '- APDL template file name: ' + params['input']['apdltemplate'],True)
    ansFullPath = join(params['input']['wd'])
    ansTemplateFullPath
    
    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + 'Exiting function createAPDL(params,logfilepath,baselogindent,logindent)',True)
    

#===============================================================================#
#                                 Log files
#===============================================================================#

def writeLineToLogFile(logFileFullPath,mode,line,toScreen):
    with open(logFileFullPath,mode) as log:
        log.write(line + '\n')
    if toScreen:
        print >> sys.__stdout__,(line + '\n')

def skipLineToLogFile(logFileFullPath,mode,toScreen):
    with open(logFileFullPath,mode) as log:
        log.write('\n')
    if toScreen:
        print >> sys.__stdout__,('\n')

def writeTitleSepLineToLogFile(logFileFullPath,mode,toScreen):
    with open(logFileFullPath,mode) as log:
        log.write('===============================================================================================\n')
    if toScreen:
        print >> sys.__stdout__,('===============================================================================================\n')

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
        print >> sys.__stdout__,('!!! ----------------------------------------------------------------------------------------!!!\n')
        print >> sys.__stdout__,('\n')
        print >> sys.__stdout__,('                                     AN ERROR OCCURED\n')
        print >> sys.__stdout__,('\n')
        print >> sys.__stdout__,('                                -------------------------\n')
        print >> sys.__stdout__,('\n')
        print >> sys.__stdout__,(str(exc) + '\n')
        print >> sys.__stdout__,(str(err) + '\n')
        print >> sys.__stdout__,('\n')
        print >> sys.__stdout__,('Terminating program\n')
        print >> sys.__stdout__,('\n')
        print>> sys.__stdout__, ('!!! ----------------------------------------------------------------------------------------!!!\n')
        print>> sys.__stdout__, ('\n')

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
            print >> sys.__stdout__,(' ')
            print >> sys.__stdout__,(' ')
            print >> sys.__stdout__,('>>>>-----------------------<<<<')
            print >> sys.__stdout__,('>>>> Running in DEBUG MODE <<<<')
            print >> sys.__stdout__,('>>>>-----------------------<<<<')
            print >> sys.__stdout__,(' ')
            print >> sys.__stdout__,(' ')

    if 'inputDirectory' not in locals():
        print >> sys.__stdout__,(' ')
        print >> sys.__stdout__,(' ')
        print >> sys.__stdout__,('!!! ERROR: missing input directory !!!')
        print >> sys.__stdout__,(' ')
        print >> sys.__stdout__,(' ')
        printHelp()
    if 'dataFile' not in locals():
        print >> sys.__stdout__,(' ')
        print >> sys.__stdout__,(' ')
        print >> sys.__stdout__,('!!! ERROR: missing data file !!!')
        print >> sys.__stdout__,(' ')
        print >> sys.__stdout__,(' ')
        printHelp()
    if 'iterablesFile' not in locals():
        print >> sys.__stdout__,(' ')
        print >> sys.__stdout__,(' ')
        print >> sys.__stdout__,('!!! ERROR: missing iterables file !!!')
        print >> sys.__stdout__,(' ')
        print >> sys.__stdout__,(' ')
        printHelp()
    if 'plotFile' not in locals():
        print >> sys.__stdout__,(' ')
        print >> sys.__stdout__,(' ')
        print >> sys.__stdout__,('!!! ERROR: missing plot file !!!')
        print >> sys.__stdout__,(' ')
        print >> sys.__stdout__,(' ')
        printHelp()

    #=======================================================================
    # END - PARSE COMMAND LINE
    #=======================================================================

    #=======================================================================
    # BEGIN - DATA
    #=======================================================================

    # units are already the ones used in simulation, not SI

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
        elif 'boolean' in dataType:
            values.append(ast.literal_eval(removeComment.split('@')[1].split('$')[0].replace(' ','')))
        elif  'int' in dataType:
            values.append(int(removeComment.split('@')[1].split('$')[0].replace(' ','')))
        elif  'float' in dataType:
            values.append(float(removeComment.split('@')[1].split('$')[0].replace(' ','')))
        elif  'string' in dataType:
            values.append(str(removeComment.split('@')[1].split('$')[0].replace(' ','')))

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
            freeParams = int(line.replace('\n','').split('#')[0].split('$')[0].split('@')[1].replace(' ',''))
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
        elif 'boolean' in dataType:
            values.append(ast.literal_eval(removeComment.split('@')[1].split('$')[0].replace(' ','')))
        elif  'int' in dataType:
            values.append(int(removeComment.split('@')[1].split('$')[0].replace(' ','')))
        elif  'float' in dataType:
            values.append(float(removeComment.split('@')[1].split('$')[0].replace(' ','')))
        elif  'string' in dataType:
            values.append(str(removeComment.split('@')[1].split('$')[0]))

    for k,keywordSet in enumerate(keywords):
        fillDataDictionary(RVEparams,keywordSet,values[k])

    #=======================================================================
    # END - PLOT SETTINGS
    #=======================================================================

    #=======================================================================
    # BEGIN - ANALYSIS
    #=======================================================================

    workDir = RVEparams['input']['wd']
    RVEparams['output']['global']['filenames']['inputdata'] = basename + '_InputData'
    RVEparams['output']['global']['filenames']['performances'] = basename + '_ANS-Performances'
    RVEparams['output']['global']['filenames']['energyreleaserate'] = basename + '_ERRTS'
    if len(RVEparams['steps'])>1:
        RVEparams['output']['global']['filenames']['thermalenergyreleaserate'] = basename + '_thermalERRTS'

    logfilename = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '_ANS-RVE-generation-and-analysis' + '.log'
    logfilefullpath = join(workDir,logfilename)
    logindent = '    '

    if not os.path.exists(RVEparams['output']['global']['directory']):
            os.mkdir(RVEparams['output']['global']['directory'])

    with open(logfilefullpath,'w') as log:
        log.write('Automatic generation and FEM analysis of RVEs with Python and Ansys' + '\n')

    skipLineToLogFile(logfilefullpath,'a',True)
    writeLineToLogFile(logfilefullpath,'a','In function: main(argv)',True)

    skipLineToLogFile(logfilefullpath,'a',True)
    writeLineToLogFile(logfilefullpath,'a',logindent + 'Global timer starts',True)
    globalStart = timeit.default_timer()

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

        #================= create ANSYS APDL file
        skipLineToLogFile(logfilefullpath,'a',True)
        writeLineToLogFile(logfilefullpath,'a',logindent + 'Calling function: createAPDL(RVEparams,logfilefullpath,logindent,logindent)',True)
        writeLineToLogFile(logfilefullpath,'a',logindent + 'Local timer starts',True)
        localStart = timeit.default_timer()
        try:
            if RVEparams['simulation-pipeline']['create-APDL']:
                modelData = createAPDL(RVEparams,logfilefullpath,logindent,logindent)
            localElapsedTime = timeit.default_timer() - localStart
            timedataList.append(localElapsedTime)
            totalIterationTime += localElapsedTime
            writeLineToLogFile(logfilefullpath,'a',logindent + 'Successfully returned from function:  createAPDL(RVEparams,logfilefullpath,logindent,logindent)',True)
            writeLineToLogFile(logfilefullpath,'a',logindent + 'Local timer stopped',True)
            writeLineToLogFile(logfilefullpath,'a',logindent + 'Elapsed time: ' + str(localElapsedTime) + ' [s]',True)
        except Exception, error:
            writeErrorToLogFile(logfilefullpath,'a',Exception,error,True)
            sys.exit(2)

        #================= run ANSYS simulation
        skipLineToLogFile(logfilefullpath,'a',True)
        writeLineToLogFile(logfilefullpath,'a',logindent + 'Calling function: runRVEsimulation(wd,inpfile,ncpus,logfilepath,baselogindent,logindent)',True)
        writeLineToLogFile(logfilefullpath,'a',logindent + 'Local timer starts',True)
        localStart = timeit.default_timer()
        try:
            if RVEparams['simulation-pipeline']['run-APDL']:
                runRVEsimulation(RVEparams['input']['wd'],inputfilename,RVEparams['solver']['cpus'],logfilefullpath,logindent,logindent)
            localElapsedTime = timeit.default_timer() - localStart
            timedataList.append(localElapsedTime)
            totalIterationTime += localElapsedTime
            writeLineToLogFile(logfilefullpath,'a',logindent + 'Successfully returned from function: runRVEsimulation(wd,inpfile,ncpus,logfilepath,baselogindent,logindent)',True)
            writeLineToLogFile(logfilefullpath,'a',logindent + 'Local timer stopped',True)
            writeLineToLogFile(logfilefullpath,'a',logindent + 'Elapsed time: ' + str(localElapsedTime) + ' [s]',True)
        except Exception, error:
            writeErrorToLogFile(logfilefullpath,'a',Exception,error,True)
            sys.exit(2)

        #================= extract and analyze data
        skipLineToLogFile(logfilefullpath,'a',True)
        writeLineToLogFile(logfilefullpath,'a',logindent + 'Calling function: analyzeRVEresults(wd,odbname,logfilepath,parameters)',True)
        writeLineToLogFile(logfilefullpath,'a',logindent + 'Local timer starts',True)
        localStart = timeit.default_timer()
        try:
            if RVEparams['simulation-pipeline']['analyze-ANS']:
                analyzeRVEresults(inputfilename.split('.')[0]+'.odb',RVEparams,logfilefullpath,logindent,logindent)
            localElapsedTime = timeit.default_timer() - localStart
            timedataList.append(localElapsedTime)
            totalIterationTime += localElapsedTime
            writeLineToLogFile(logfilefullpath,'a',logindent + 'Successfully returned from function: analyzeRVEresults(wd,odbname,logfilepath,parameters)',True)
            writeLineToLogFile(logfilefullpath,'a',logindent + 'Local timer stopped',True)
            writeLineToLogFile(logfilefullpath,'a',logindent + 'Elapsed time: ' + str(localElapsedTime) + ' [s]',True)
        except Exception, error:
            writeErrorToLogFile(logfilefullpath,'a',Exception,error,True)
            sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])
