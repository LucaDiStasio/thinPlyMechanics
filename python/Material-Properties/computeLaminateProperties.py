#!/usr/bin/env Python
# -*- coding: utf-8 -*-

'''
=====================================================================================

Copyright (c) 2016-2018 Université de Lorraine or Luleå tekniska universitet
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


ested with Python 2.7 (64-bit) distribution in Windows 10.

'''

import sys, os
from numpy import cos, sin, array, transpose, matmul, add
from numpy import sum as npsum
from numpy.linalg import inv
from os.path import isfile, join, exists
from shutil import copyfile
import sqlite3
from datetime import datetime
from time import strftime, sleep
import timeit

#===============================================================================#
#===============================================================================#
#                              I/O functions
#===============================================================================#
#===============================================================================#

#===============================================================================#
#                              CSV files
#===============================================================================#

def createCSVfile(dir,filename,titleline=None):
    if len(filename.split('.'))<2:
        filename += '.csv'
    with open(join(dir,filename),'w') as csv:
        csv.write('# Automatically created on ' + datetime.now().strftime('%d/%m/%Y') + ' at' + datetime.now().strftime('%H:%M:%S') + '\n')
        if titleline != None:
            csv.write(titleline.replace('\n','') + '\n')

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
                if v>1:
                    line += ', '
                line += str(value)
            csv.write(line + '\n')

#===============================================================================#
#                                 LOG files
#===============================================================================#

def writeLineToLogFile(logFileFullPath,mode,line,toScreen):
    with open(logFileFullPath,mode) as log:
        log.write(line + '\n')
    if toScreen:
        print(line + '\n')

def skipLineToLogFile(logFileFullPath,mode,toScreen):
    with open(logFileFullPath,mode) as log:
        log.write('\n')
    if toScreen:
        print('\n')

def writeTitleSepLineToLogFile(logFileFullPath,mode,toScreen):
    with open(logFileFullPath,mode) as log:
        log.write('===============================================================================================\n')
    if toScreen:
        print('===============================================================================================\n')

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
        print('!!! ----------------------------------------------------------------------------------------!!!\n')
        print('\n')
        print('                                     AN ERROR OCCURED\n')
        print('\n')
        print('                                -------------------------\n')
        print('\n')
        print(str(exc) + '\n')
        print(str(err) + '\n')
        print('\n')
        print('Terminating program\n')
        print('\n')
        print('!!! ----------------------------------------------------------------------------------------!!!\n')
        print('\n')

#===============================================================================#
#===============================================================================#
#                                Ply properties
#===============================================================================#
#===============================================================================#
def RoM(Vf,rhof,ELf,ETf,nuf,alphaf,rhom,ELm,ETm,num,alpham):
    Vm = 1 - Vf
    Gf = 0.5*ELf/(1+nuf)
    Gm = 0.5*ELm/(1+num)
    rhoc = rhof*Vf + rhom*Vm
    E1 = ELf*Vf + ELm*Vm
    E2 = 1.0/(Vf/ETf + Vm/ETm)
    nu12 = *nuf*Vf + num*Vm
    G12 = 1/(Vf/Gf + Vm/Gm)
    nu21 = nu12*(E2/E1)
    nu23 = nu12*(1 - nu21)/(1 - nu12)
    G23 = 0.5*E2)/(1 + nu23)
    alpha1 = (ELf*alphaf*Vf + ELm*alpham*Vm)/(ELf*Vf + ELm*Vm)
    alpha2 = (1 + nuf)*alphaf*Vf + (1 + num)*alpham*Vm - alpha1*nu12
    return rhoc,E1,E2,nu12,nu21,G12,nu23,G23,alpha1,alpha2

def HalpinTsai(Vf,rhof,ELf,ETf,nuf,alphaf,rhom,ELm,ETm,num,alpham):
    Vm = 1-Vf
    Gf = 0.5*ELf/(1+nuf)
    Gm = 0.5*ELm/(1+num)
    xi = 1
    rhoc = rhof*Vf + rhom*Vm
    E1 = ELf*Vf + ELm*Vm
    eta1 = (ETf/ETm - 1)/(ETf/ETm + 2*xi)
    E2 = (ETm*(1 + 2*xi*eta1*Vf))/(1-eta1*Vf)
    nu12 = nuf*Vf + num*Vm
    eta2 = (Gf/Gm-1)/(Gf/Gm + xi)
    G12 = (Gm*(1 + xi*eta2*Vf)/(1-eta2*Vf)
    nu21 = nu12*(E2/E1)
    nu23 = nu12*(1-nu21)/(1-nu12)
    G23 = 0.5*E2/(1+nu23)
    alpha1 = (ELf*alphaf*Vf + ELm*alpham*Vm)/(ELf*Vf + ELm*Vm)
    alpha2 = (1 + nuf)*alphaf*Vf + (1 + num)*alpham*Vm - alpha1*nu12
    return rhoc,E1,E2,nu12,nu21,G12,nu23,G23,alpha1,alpha2

def Hashin(Vf,rhof,ELf,ETf,nu12f,nu23f,alphaLf,alphaTf,rhom,ELm,ETm,num,alpham):
    Vm = 1.0-Vf
    G12f = 0.5*ELf/(1.0+nu12f)
    Gm = 0.5*ELm/(1.0+num)
    rhoc = rhof*Vf + rhom*Vm
    kmT = 0.5*ELm/(1.0-num-2.0*num*num)
    kfT = ELf*ETf/(2*ELf*(1.0-nu23f)-4.0*ETf*nu12f*nu12f)
    lambda1 = 1.0/(2*(1/Gm + Vf/kmT + Vm/kfT)
    E1 = Vf*ELf + Vm*ELm + 2.0*lambda1*Vf*Vm*(num - nu12f)*(num - nu12f)
    nu12 = Vf*nu12f + Vm*num + 0.5*lambda1*(num - nu12f)*(1.0/kfT - 1.0/kmT)*Vf*Vm
    G12 = Gm + Vf/(1.0/(G12f - Gm) + (0.5*Vm)/Gm)
    K23 = (kmT*(kfT + Gm)*Vm + kfT*(kmT + Gm)*Vf)/((kfT + Gm)*Vm + (kmT + Gm)*Vf)
    lambda3 = 1.0 + (4*K23*nu12*nu12)/E1
    G23 = Gm + Vf/(1.0/(0.5*ETf/(1 + nu23f)-Gm) + Vm*(kmT + 2*Gm)/(2*Gm*(kmT + Gm)))
    E2 = 4*G23/(1 + lambda3*G23/K23)
    nu21 = nu12*(E2/E1)
    nu23 = nu12*(1-nu21)/(1 - nu12)
    km = Gm/(1-2*num)
    lambda2 = 1.0/(0.5*(1/Gm + Vf/km + Vm/kfT))
    alpha1 = (ELf*alphaf*Vf + ELm*alpham*Vm)/(ELf*Vf + ELm*Vm)
    alpha2 = -nu12*alpha1 + (alphaTf + nu12f*alphaLf)*Vf + (alpham + num*alpham)*Vm + 0.5*lambda2*(1/kfT-1/km)*Vf*Vm*((alpham + num*alpham) - (alphaTf + nu23f*alphaLf))
    return rhoc,E1,E2,nu12,nu21,G12,nu23,G23,alpha1,alpha2

#===============================================================================#
#===============================================================================#
#                              Laminate properties
#===============================================================================#
#===============================================================================#

def locallaminaQ(E1,E2,nu12,nu21,G12):
    Q11 = E1/(1-nu12*nu21)
    Q12 = nu12*E2/(1-nu12*nu21)
    Q21 = Q12
    Q22 = E2/(1- nu12*nu21)
    Q66 = G12
    Q = array([[Q11,Q12,0],[Q21,Q22,0],[0,0,Q66]])
    return Q

def locallaminaS(E1,E2,nu12,nu21,G12):
    S11 = 1/E1
    S12 = -nu12/E1
    S21 = S12
    S22 = 1/E2
    S66 = G12
    S = array([[S11,S12,0],[S21,S22,0],[0,0,S66]])
    return S

def laminaQ(theta,E1,E2,nu12,nu21,G12):
    R = inv(T(theta))
    Q = matmul(matmul(R,locallaminaQ(E1,E2,nu12,nu21,G12)),transpose(R))
    return Q

def laminaS(theta,E1,E2,nu12,nu21,G12):
    S = matmul(matmul(transpose(T(theta)),locallaminaS(E1,E2,nu12,nu21,G12)),T(theta))
    return S

def CLT(thicknesses,angles,properties,isSymmetric):
    # thicknesses and angles must be ordered from bottom to top, symmetry line is on top
    # properties = [...,[E1,E2,nu12,nu21,G12],...]  ordered from bottom to top
    totalThick = npsum(thicknesses)
    if isSymmetric:
        totalThick *= 2
    midplaneHeight = 0.5*totalThick
    if isSymmetric:
        l = len(thicknesses)
        for t in range(l-1,-1,-1):
            thicknesses.append(thicknesses[t])
    z = [] # ply through-the-stack coordinates
    for t,thickness in enumerate(thicknesses):
        zk1 = npsum(thicknesses[:t]) - midplaneHeight
        zk2 = npsum(thicknesses[:t+1]) - midplaneHeight
        z.append([zk1,zk2])
    A = array([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])
    B = array([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])
    D = array([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])
    for t,thickness in enumerate(thicknesses):
        A = add(A,thickness*laminaQ(angles[t],properties[t][0],properties[t][1],properties[t][2],properties[t][3],properties[t][4]))
        B = add(B,0.5*(z[t][1]*z[t][1]-z[t][0]*z[t][0])*laminaQ(angles[t],properties[t][0],properties[t][1],properties[t][2],properties[t][3],properties[t][4]))
        D = add(D,(1.0/3.0))*(z[t][1]*z[t][1]*z[t][1]-z[t][0]*z[t][0]*z[t][0])*laminaQ(angles[t],properties[t][0],properties[t][1],properties[t][2],properties[t][3],properties[t][4]))
        Qlam = array([[A[0,0],A[0,1],A[0,2],B[0,0],B[0,1],B[0,2]],
                      [A[1,0],A[1,1],A[1,2],B[1,0],B[1,1],B[1,2]],
                      [A[2,0],A[2,1],A[2,2],B[2,0],B[2,1],B[2,2]],
                      [B[0,0],B[0,1],B[0,2],D[0,0],D[0,1],D[0,2]],
                      [B[1,0],B[1,1],B[1,2],D[1,0],D[1,1],D[1,2]],
                      [B[2,0],B[2,1],B[2,2],D[2,0],D[2,1],D[2,2]]])
    return A,B,D,Qlam

#===============================================================================#
#===============================================================================#
#                               Transformations
#===============================================================================#
#===============================================================================#

def T(theta):
    m = cos(theta)
    n = sin(theta)
    matrixT = np.array([m*m,n*n,2*m*n],[n*n,m*m,-2*m*n],[-m*n,m*n,m*m - n*n])
    return matrixT

#===============================================================================#
#===============================================================================#
#                                    MAIN
#===============================================================================#
#===============================================================================#

def main(argv):

if __name__ == "__main__":
    main(sys.argv[1:])
