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

def discreteVCCT(iteration,parameters):

    #=======================================================================
    # BEGIN - Read content of global ERR file
    #=======================================================================
    print('Read content of global ERR file...')
    with open(join(parameters['output']['global']['directory'],parameters['output']['global']['filenames']['energyreleaserate'].split('.')[0]+'.csv'),'r') as csv:
        lines = csv.readlines()
    errTitleLine = lines[0]
    errData = []
    for line in lines[1:]:
        row = []
        data = line.replace('\n','').split(',')
        for datum in data:
            row.append(float(datum))
        errData.append(row)
    errData = np.array(errData)
    print('...done.')
    #=======================================================================
    # END - Read content of global ERR file
    #=======================================================================

    #=======================================================================
    # BEGIN - compute crack tip reference frame transformation
    #=======================================================================
    print('Compute crack tip reference frame transformation ...')
    phi = parameters['geometry']['deltatheta']*np.pi/180.0
    print('...done.')
    #=======================================================================
    # END - compute crack tip reference frame transformation
    #=======================================================================

    #=======================================================================
    # BEGIN - compute mesh size reference frame transformation
    #=======================================================================
    print('Compute mesh size reference frame transformation ...')
    delta = parameters['mesh']['size']['delta']*np.pi/180.0
    print('...done.')
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
    print('...done.')
    #=======================================================================
    # END - Read stiffness matrix from csv file
    #=======================================================================

    #=======================================================================
    # BEGIN - Read load vector from csv file
    #=======================================================================
    print('Read load vector from csv file...')
    with open(join(parameters['output']['local']['directory'],parameters['output']['local']['filenames']['globalloadvector'].split('.')[0]+'.csv'),'r') as csv:
        lines = csv.readlines()
    globalVector = {}
    for line in lines[2:]:
        values = line.split(',')
        rowIndex = int(values[0])
        rowDOF = int(values[1])
        if rowIndex not in globalVector:
            globalVector[rowIndex] = {}
        globalVector[rowIndex][rowDOF] = int(values[-1])
    print('...done.')
    #=======================================================================
    # END - Read stiffness matrix from csv file
    #=======================================================================

    #=======================================================================
    # BEGIN - Read load vector from csv file
    #=======================================================================
    print('Read load vector from csv file...')
    with open(join(parameters['output']['local']['directory'],parameters['output']['local']['filenames']['globalloadvector'].split('.')[0]+'.csv'),'r') as csv:
        lines = csv.readlines()
    globalVector = {}
    for line in lines[2:]:
        values = line.split(',')
        rowIndex = int(values[0])
        rowDOF = int(values[1])
        if rowIndex not in globalVector:
            globalVector[rowIndex] = {}
        globalVector[rowIndex][rowDOF] = int(values[-1])
    print('...done.')
    #=======================================================================
    # END - Read stiffness matrix from csv file
    #=======================================================================

    #=======================================================================
    # BEGIN - Read displacements of all nodes from csv file
    #=======================================================================
    print('Read displacements of all nodes from csv file...')
    with open(join(parameters['output']['local']['directory'],parameters['output']['local']['filenames']['globaldispvector'].split('.')[0]+'.csv'),'r') as csv:
        lines = csv.readlines()
    globalDisps = {}
    for line in lines[2:]:
        values = line.split(',')
        rowIndex = int(values[0])
        globalDisps[rowIndex] = {}
        globalDisps[rowIndex][1] = float(values[1])
        globalDisps[rowIndex][2] = float(values[2])
    print('...done.')
    #=======================================================================
    # END - Read displacements of all nodes from csv file
    #=======================================================================

    #=======================================================================
    # BEGIN - build matrices
    #=======================================================================
    print('Build matrices...')

    print('    -- R')
    R = np.matrix([[np.cos(phi),np.sin(phi)],[-np.sin(phi),np.cos(phi)]])

    print('    -- inv R')
    invR = np.matrix([[np.cos(phi),-np.sin(phi)],[np.sin(phi),np.cos(phi)]])

    shapeFuncOrder = {}
    shapeFuncOrder['first'] = 1
    shapeFuncOrder['second'] = 2
    shapeFuncOrder['third'] = 3
    shapeFuncOrder['fourth'] = 4
    m = shapeFuncOrder[parameters['mesh']['element']['order']]

    print('    -- P (m=' + str(m) + ')')
    P = []
    for p in range(1,m+2):
        P.append(np.matrix([[np.cos((1+(1-p)/m)*delta),np.sin((1+(1-p)/m)*delta)],[-np.sin((1+(1-p)/m)*delta),np.cos((1+(1-p)/m)*delta)]]))

    print('-- inv P (m=' + str(m) + ')',True)
    invP = []
    for p in range(1,m+2):
        invP.append(np.matrix([[np.cos((1+(1-p)/m)*delta),-np.sin((1+(1-p)/m)*delta)],[np.sin((1+(1-p)/m)*delta),np.cos((1+(1-p)/m)*delta)]]))

    print('    -- Q (m=' + str(m) + ')')
    Q = []
    for q in range(1,m+2):
        Q.append(np.matrix([[np.cos(((q-1)/m)*delta),np.sin(((q-1)/m)*delta)],[-np.sin(((q-1)/m)*delta),np.cos(((q-1)/m)*delta)]]))

    print('    -- inv Q (m=' + str(m) + ')')
    invQ = []
    for q in range(1,m+2):
        invQ.append(np.matrix([[np.cos(((q-1)/m)*delta),-np.sin(((q-1)/m)*delta)],[np.sin(((q-1)/m)*delta),np.cos(((q-1)/m)*delta)]]))

    print('    -- U (ABAQUS solution)')
    rowIndeces = []
    columnIndeces = []
    values = []
    for key in globalDisps.keys():
        rowIndeces.append(2*(key-1))
        rowIndeces.append(2*(key-1)+1)
        columnIndeces.append(0)
        columnIndeces.append(0)
        values.append(globalDisps[key][1])
        values.append(globalDisps[key][2])
    NNodes = np.max(globalDisps.keys())
    globalDisps = {}
    Uabq = sparse.coo_matrix((np.array(values), (np.array(rowIndeces), np.array(columnIndeces))), shape=(NNodes, 1))
    rowIndeces = []
    columnIndeces = []
    values = []

    print('    -- K')
    rowIndeces = []
    columnIndeces = []
    values = []
    for rowKey in globalMatrix.keys():
        for dofKey in globalMatrix[rowKey].keys():
            for columnKey in globalMatrix[rowKey][dofKey].keys():
                for cdofKey in globalMatrix[rowKey][dofKey][columnKey].keys():
                    rowIndeces.append(2*(rowKey-1)+dofKey-1)
                    columnIndeces.append(2*(columnKey-1)+cdofKey-1)
                    values.append(globalMatrix[rowKey][dofKey][columnKey][cdofKey])
    globalMatrix = {}
    K = sparse.coo_matrix((np.array(values), (np.array(rowIndeces), np.array(columnIndeces))), shape=(NNodes, NNodes))
    rowIndeces = []
    columnIndeces = []
    values = []

    print('    -- Kct')
    with open(join(parameters['output']['local']['directory'],parameters['output']['local']['filenames']['matrixindeces'].split('.')[0]+'.csv'),'r') as csv:
        lines = csv.readlines()
    cracktipIndex = int(lines[0].split(',')[0])
    fibercracktipdispmeasIndex = int(lines[0].split(',')[1])
    matrixcracktipdispmeasIndex = int(lines[0].split(',')[2])
    if 'second' in parameters['mesh']['elements']['order']:
        fiberfirstBounded = int(lines[0].split(',')[3])
        fiberfirstboundispmeasIndex = int(lines[0].split(',')[4])
        matrixfirstboundispmeasIndex = int(lines[0].split(',')[5])
    Kct = []
    rowCTx = [K[2*(cracktipIndex-1)-1+1,2*(matrixcracktipdispmeasIndex-1)-1+1],K[2*(cracktipIndex-1)-1+1,2*(matrixcracktipdispmeasIndex-1)-1+2]]
    rowCTy = [K[2*(cracktipIndex-1)-1+2,2*(matrixcracktipdispmeasIndex-1)-1+1],K[2*(cracktipIndex-1)-1+2,2*(matrixcracktipdispmeasIndex-1)-1+2]]
    if 'second' in parameters['mesh']['elements']['order']:
        rowCTx.append(K[2*(cracktipIndex-1)-1+1,2*(matrixfirstboundispmeasIndex-1)-1+1])
        rowCTx.append(K[2*(cracktipIndex-1)-1+1,2*(matrixfirstboundispmeasIndex-1)-1+2])
        rowCTy.append(K[2*(cracktipIndex-1)-1+2,2*(matrixfirstboundispmeasIndex-1)-1+1])
        rowCTy.append(K[2*(cracktipIndex-1)-1+2,2*(matrixfirstboundispmeasIndex-1)-1+2])
        rowFBx = [K[2*(fiberfirstBounded-1)-1+1,2*(matrixcracktipdispmeasIndex-1)-1+1],K[2*(fiberfirstBounded-1)-1+1,2*(matrixcracktipdispmeasIndex-1)-1+2],K[2*(fiberfirstBounded-1)-1+1,2*(matrixfirstboundispmeasIndex-1)-1+1],K[2*(fiberfirstBounded-1)-1+1,2*(matrixfirstboundispmeasIndex-1)-1+2]]
        rowFBy = [K[2*(fiberfirstBounded-1)-1+2,2*(matrixcracktipdispmeasIndex-1)-1+1],K[2*(fiberfirstBounded-1)-1+2,2*(matrixcracktipdispmeasIndex-1)-1+2],K[2*(fiberfirstBounded-1)-1+2,2*(matrixfirstboundispmeasIndex-1)-1+1],K[2*(fiberfirstBounded-1)-1+2,2*(matrixfirstboundispmeasIndex-1)-1+2]]
        Kct.append(np.array([rowFBx,rowFBy]))
    Kct.insert(0,np.array([rowCTx,rowCTy]))

    print('    -- Kstruct2ct')
    allcolKstruct2ct = np.array([K[2*(cracktipIndex-1)-1+1,:],K[2*(cracktipIndex-1)-1+1,:]])
    allcolKstruct2ct[0,2*(fibercracktipdispmeasIndex-1)-1+1] = allcolKstruct2ct[0,2*(matrixcracktipdispmeasIndex-1)-1+1] + allcolKstruct2ct[0,2*(fibercracktipdispmeasIndex-1)-1+1]
    allcolKstruct2ct[0,2*(fibercracktipdispmeasIndex-1)-1+2] = allcolKstruct2ct[0,2*(matrixcracktipdispmeasIndex-1)-1+2] + allcolKstruct2ct[0,2*(fibercracktipdispmeasIndex-1)-1+2]
    if 'second' in parameters['mesh']['elements']['order']:
        allcolKstruct2ct2 = np.array([K[2*(fiberfirstBounded-1)-1+1,:],K[2*(fiberfirstBounded-1)-1+2,:]])
        allcolKstruct2ct2[0,2*(fiberfirstboundispmeasIndex-1)-1+1] = allcolKstruct2ct2[0,2*(matrixfirstboundispmeasIndex-1)-1+1] + allcolKstruct2ct2[0,2*(fiberfirstboundispmeasIndex-1)-1+1]
        allcolKstruct2ct2[0,2*(fiberfirstboundispmeasIndex-1)-1+2] = allcolKstruct2ct2[0,2*(matrixfirstboundispmeasIndex-1)-1+2] + allcolKstruct2ct2[0,2*(fiberfirstboundispmeasIndex-1)-1+2]
    toSkip = [2*(matrixcracktipdispmeasIndex-1)-1+1,2*(matrixcracktipdispmeasIndex-1)-1+2]
    if 'second' in parameters['mesh']['elements']['order']:
        toSkip.append(2*(matrixfirstboundispmeasIndex-1)-1+1)
        toSkip.append(2*(matrixfirstboundispmeasIndex-1)-1+2)
    Kstruct2ct1 = []
    Kstruct2ct2 = []
    for i in range(0,2*m-1):
        row1 = []
        row2 = []
        for element,e in enumerate(allcolKstruct2ct[i,:]):
            if e not in toSkip:
                row1.append(element)
                if 'second' in parameters['mesh']['elements']['order']:
                    row2.append(allcolKstruct2ct2[i,e])
        Kstruct2ct.append(row1)
        Kstruct2ct2.append(row2)
    Kstruct2ct = sparse.coo_matrix(np.array(Kstruct2ct))
    Kstruct2ct2 = sparse.coo_matrix(np.array(Kstruct2ct2))
    Kstruct2ctList = [Kstruct2ct,Kstruct2ct2]
    allcolKstruct2ct = []
    allcolKstruct2ct2 = []

    print('    -- CDabq')
    CDabq1 = np.array([Uabq[2*(matrixcracktipdispmeasIndex-1),0]-Uabq[2*(fibercracktipdispmeasIndex-1),0],Uabq[2*(matrixcracktipdispmeasIndex-1)+1,0]-Uabq[2*(fibercracktipdispmeasIndex-1)+1,0]])
    if 'second' in parameters['mesh']['elements']['order']:
        CDabq2 = np.array(Uabq[2*(matrixfirstboundispmeasIndex-1),0]-Uabq[2*(fiberfirstboundispmeasIndex-1),0],Uabq[2*(matrixfirstboundispmeasIndex-1)+1,0]-Uabq[2*(fiberfirstboundispmeasIndex-1)+1,0])
    CDabq =[CDabq1,CDabq2]

    print('   -- Ustructabq')
    toSkip = [2*(matrixcracktipdispmeasIndex-1)-1+1,2*(matrixcracktipdispmeasIndex-1)-1+2]
    if 'second' in parameters['mesh']['elements']['order']:
        toSkip.append(2*(matrixfirstboundispmeasIndex-1)-1+1)
        toSkip.append(2*(matrixfirstboundispmeasIndex-1)-1+2)
    Ustructabq1 = []
    Ustructabq2 = []
    for element,e in enumerate(Uabq[:,1]):
        if e not in toSkip:
            Ustructabq1.append(element)
            if 'second' in parameters['mesh']['elements']['order']:
                Ustructabq2.append(Uabq[e,1])
    Ustructabq1 = np.array(Ustructabq1)
    Ustructabq2 = np.array(Ustructabq2)
    Ustructabq = [Ustructabq1,Ustructabq2]

    print('    -- F')
    rowIndeces = []
    columnIndeces = []
    values = []
    for key in globalVector.keys():
        for dof in globalVector[key].keys():
            rowIndeces.append(2*(key-1)+dof)
            columnIndeces.append(0)
            values.append(globalDisps[key][dof])
    globalVector = {}
    F = sparse.coo_matrix((np.array(values), (np.array(rowIndeces), np.array(columnIndeces))), shape=(NNodes, 1))
    rowIndeces = []
    columnIndeces = []
    values = []

    print('... done.')
    #=======================================================================
    # END - build matrices
    #=======================================================================

    #=======================================================================
    # BEGIN - compute global displacement vector
    #=======================================================================
    print('Compute displacement vectors...')

    print('    -- U')
    invK = sparse.linalg.inv(K)
    U = invK.dot(F)

    print('    -- CD')
    CD1 = np.array([U[2*(matrixcracktipdispmeasIndex-1),0]-U[2*(fibercracktipdispmeasIndex-1),0],U[2*(matrixcracktipdispmeasIndex-1)+1,0]-U[2*(fibercracktipdispmeasIndex-1)+1,0]])
    if 'second' in parameters['mesh']['elements']['order']:
        CD2 = np.array(U[2*(matrixfirstboundispmeasIndex-1),0]-U[2*(fiberfirstboundispmeasIndex-1),0],U[2*(matrixfirstboundispmeasIndex-1)+1,0]-U[2*(fiberfirstboundispmeasIndex-1)+1,0])
    CD =[CD1,CD2]

    print('    -- Ustruct')
    toSkip = [2*(matrixcracktipdispmeasIndex-1)-1+1,2*(matrixcracktipdispmeasIndex-1)-1+2]
    if 'second' in parameters['mesh']['elements']['order']:
        toSkip.append(2*(matrixfirstboundispmeasIndex-1)-1+1)
        toSkip.append(2*(matrixfirstboundispmeasIndex-1)-1+2)
    Ustruct1 = []
    Ustruct2 = []
    for element,e in enumerate(U[:,1]):
        if e not in toSkip:
            Ustruct1.append(element)
            if 'second' in parameters['mesh']['elements']['order']:
                Ustruct2.append(U[e,1])
    Ustruct1 = np.array(Ustruct1)
    Ustruct2 = np.array(Ustruct2)
    Ustruct = [Ustruct1,Ustruct2]

    print('... done.')
    #=======================================================================
    # END - compute global displacement vector
    #=======================================================================

    #=======================================================================
    # BEGIN - compute ERR matrix
    #=======================================================================
    print('Compute ERR matrix...')

    print('    -- ABAQUS solution')
    matGabq = 0
    for Pmat, pi in enumerate(P):
        for Qmat, qi in enumerate(Q):
            matGabq += Q[qi].dot(R.dot(np.outer((Kct[qi].dot(CDabq[qi])+Kstruct2ct[qi].dot(Ustructabq[qi])),CDabq[pi]).dot(invR.dot(invP[pi].dot(Tpq('quad',parameters['mesh']['elements']['order'],pi,qi))))))

    print('    -- Recalculated solution')
    matG = 0
    for Pmat, pi in enumerate(P):
        for Qmat, qi in enumerate(Q):
            matG += Q[qi].dot(R.dot(np.outer((Kct[qi].dot(CD[qi])+Kstruct2ct[qi].dot(Ustruct[qi])),CD[pi]).dot(invR.dot(invP[pi].dot(Tpq('quad',parameters['mesh']['elements']['order'],pi,qi))))))


    print('... done.')
    #=======================================================================
    # END - compute ERR matrix
    #=======================================================================

    #=======================================================================
    # BEGIN - diagonalize ERR matrix
    #=======================================================================
    print('Diagonalize ERR matrix...')

    print('    -- ABAQUS solution')
    G11 = matGabq[0,0]
    G12 = matGabq[0,1]
    G21 = matGabq[1,0]
    G22 = matGabq[1,1]
    eigG1abq = 0.5*(-(G11+G22)+np.sqrt((G11+G22)*(G11+G22)-4*(G11*G22-G12*G21)))
    eigG2abq = 0.5*(-(G11+G22)-np.sqrt((G11+G22)*(G11+G22)-4*(G11*G22-G12*G21)))
    eigvecG1abq = [1/np.sqrt(1+G21*G21/((G22-eigG1abq)*(G22-eigG1abq))),-G21/((G22-eigG1abq)*np.sqrt(1+G21*G21/((G22-eigG1abq)*(G22-eigG1abq))))]
    eigvecG2abq = [1/np.sqrt(1+G21*G21/((G22-eigG2abq)*(G22-eigG2abq))),-G21/((G22-eigG2abq)*np.sqrt(1+G21*G21/((G22-eigG2abq)*(G22-eigG2abq))))]
    cospsi1 = 1/np.sqrt(1+G21*G21/((G22-eigG1abq)*(G22-eigG1abq)))
    cospsi2 = 1/np.sqrt(1+G21*G21/((G22-eigG2abq)*(G22-eigG2abq)))
    psi1abq = np.arctan2(np.sqrt(1-cospsi1*cospsi1),cospsi1)
    psi2abq = np.arctan2(np.sqrt(1-cospsi2*cospsi2),cospsi2)

    print('    -- Recalculated solution')
    G11 = matG[0,0]
    G12 = matG[0,1]
    G21 = matG[1,0]
    G22 = matG[1,1]
    eigG1 = 0.5*(-(G11+G22)+np.sqrt((G11+G22)*(G11+G22)-4*(G11*G22-G12*G21)))
    eigG2 = 0.5*(-(G11+G22)-np.sqrt((G11+G22)*(G11+G22)-4*(G11*G22-G12*G21)))
    eigvecG1 = [1/np.sqrt(1+G21*G21/((G22-eigG1)*(G22-eigG1))),-G21/((G22-eigG1)*np.sqrt(1+G21*G21/((G22-eigG1)*(G22-eigG1))))]
    eigvecG2 = [1/np.sqrt(1+G21*G21/((G22-eigG2)*(G22-eigG2))),-G21/((G22-eigG2)*np.sqrt(1+G21*G21/((G22-eigG2)*(G22-eigG2))))]
    cospsi1 = 1/np.sqrt(1+G21*G21/((G22-eigG1)*(G22-eigG1)))
    cospsi2 = 1/np.sqrt(1+G21*G21/((G22-eigG2)*(G22-eigG2)))
    psi1 = np.arctan2(np.sqrt(1-cospsi1*cospsi1),cospsi1)
    psi2 = np.arctan2(np.sqrt(1-cospsi2*cospsi2),cospsi2)

    print('... done.')
    #=======================================================================
    # END - diagonalize ERR matrix
    #=======================================================================

    #=======================================================================
    # BEGIN - Update content of global ERR file
    #=======================================================================
    print('Update content of global ERR file...')

    rowUpdate = [matGabq[0,0],matGabq[0,1],matGabq[1,0],matGabq[1,1],matG[0,0],matG[0,1],matG[1,0],matG[1,1],eigG1abq,eigG2abq,eigG1,eigG2,eigvecG1abq[0],eigvecG1abq[1],eigvecG1[0],eigvecG1[1],psi1abq*180.0/np.pi,psi2abq*180.0/np.pi,psi1*180.0/np.pi,psi2*180.0/np.pi,psi1abq*180.0/np.pi+90.0,psi2abq*180.0/np.pi+90.0,psi1*180.0/np.pi+90.0,psi2*180.0/np.pi+90.0]
    errData[iteration,27:27+24] = rowUpdate

    with open(join(parameters['output']['global']['directory'],parameters['output']['global']['filenames']['energyreleaserate'].split('.')[0]+'.csv'),'w') as csv:
        csv.write(errTitleLine)
        for row in errData:
            line = ''
            for e,el in enumerate(row):
                if e>0:
                    line += ','
                line += str(el)
            csv.write(line+'\n')
    print('...done.')
    #=======================================================================
    # END - Update content of global ERR file
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

    for i,iterationSet in enumerate(iterationsSets):

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

        discreteVCCT(i,RVEparams)



if __name__ == "__main__":
    main(sys.argv[1:])
