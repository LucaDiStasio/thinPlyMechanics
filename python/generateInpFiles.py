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
            out.write('simulation-pipeline, ' + str(key) + ' @' + str(pipelineControls[key]) + ' $boolean' + '\n')
        out.write('#' + '\n')

def writeAnalysisControls(fullPath,analysisControls):
    with open(fullPath,'a') as out:
        out.write('# Select outputs in the analysis phase' + '\n')
        for key in analysisControls:
            out.write('simulation-pipeline, analysis, ' + str(key) + ' @' + str(analysisControls[key]) + ' $boolean' + '\n')
        out.write('#' + '\n')

def writeInputControls(fullPath,inputControls):
    with open(fullPath,'a') as out:
        out.write('# Directory and names for CAE model generation' + '\n')
        for key in inputControls:
            out.write('input, ' + str(key) + ' @' + str(inputControls[key]) + ' $string' + '\n')
        out.write('#' + '\n')

def writeGeometryControls(fullPath,geometryControls):
    with open(fullPath,'a') as out:
        out.write('# Geometry' + '\n')
        for key in geometryControls:
            if 'fiberType' in key:
                out.write('geometry, fiber, type @' + str(geometryControls[key]) + ' $string' + '\n')
            else:
                out.write('geometry, ' + str(key) + ' @' + str(geometryControls[key]) + ' $float' + '\n')
        out.write('#' + '\n')

def writeMaterialsControls(fullPath,materialsControls):
    with open(fullPath,'a') as out:
        out.write('# Materials (repeat keywords for every material to be defined)' + '\n')
        for m,material in enumerate(materialsControls):
            out.write('materials, ' + str(m+1) + ', name            @' + str(material['name']) + ' $string'  + '\n')
            out.write('materials, ' + str(m+1) + ', elastic, type   @' + str(material['type']) +   ' $ABAQUS keyword'  + '\n')
            out.write('materials, ' + str(m+1) + ', elastic, values @' + str(material['elProps']) + ' $list of float'  + '\n')
        out.write('#' + '\n')

def writePostprocControls(fullPath,postprocControls):
    with open(fullPath,'a') as out:
        out.write('# Values of nu and G needed for postprocessing' + '\n')
        for key in postprocControls:
            out.write('postproc, ' + str(key) + ' @' + str(postprocControls[key]) + ' $float' + '\n')
        out.write('#' + '\n')

def writeSectionsControls(fullPath,sectionsControls):
    with open(fullPath,'a') as out:
        out.write('# Section properties (repeat for every section to be defined)' + '\n')
        for s,section in enumerate(sectionsControls):
            out.write('sections, ' + str(s+1) + ', name      @' + str(section['name']) + ' $string'  + '\n')
            out.write('sections, ' + str(s+1) + ', type      @' + str(section['type']) +   ' $string'  + '\n')
            out.write('sections, ' + str(s+1) + ', material  @' + str(section['material']) + ' $string'  + '\n')
            out.write('sections, ' + str(s+1) + ', thickness @' + str(section['thickness']) + ' $float'  + '\n')
        out.write('#' + '\n')

def writeSectionregionsControls(fullPath,sectionregionsControls):
    with open(fullPath,'a') as out:
        out.write('# Section assignments (repeat as needed)' + '\n')
        for r,sectionregion in enumerate(sectionregionsControls):
            out.write('sectionRegions, ' + str(r+1) + ', name                 @' + str(sectionregion['name']) + ' $string'  + '\n')
            out.write('sectionRegions, ' + str(r+1) + ', set                  @' + str(sectionregion['set']) +   ' $string'  + '\n')
            out.write('sectionRegions, ' + str(r+1) + ', offsetType           @' + str(sectionregion['offsetType']) + ' $ABAQUS keyword'  + '\n')
            out.write('sectionRegions, ' + str(r+1) + ', offsetField          @' + str(sectionregion['offsetField']) + ' $string'  + '\n')
            out.write('sectionRegions, ' + str(r+1) + ', thicknessAssignment  @' + str(sectionregion['thicknessAssignment']) + ' $ABAQUS keyword'  + '\n')
            out.write('sectionRegions, ' + str(r+1) + ', offsetValue          @' + str(sectionregion['offsetValue']) + ' $float'  + '\n')
        out.write('#' + '\n')

def writeStepsControls(fullPath,stepsControls):
    with open(fullPath,'a') as out:
        out.write('# Step data' + '\n')
        for s,step in enumerate(stepsControls):
            out.write('steps, ' + str(s+1) + ', name             @' + str(step['name'])             + ' $string'  + '\n')
            out.write('steps, ' + str(s+1) + ', previous         @' + str(step['previous'])         + ' $string'  + '\n')
            out.write('steps, ' + str(s+1) + ', minimumIncrement @' + str(step['minimumIncrement']) + ' $float'  + '\n')
        out.write('#' + '\n')

def writeLoadsControls(fullPath,loadsControls):
    with open(fullPath,'a') as out:
        out.write('# Loads' + '\n')
        for l,load in enumerate(loadsControls):
            out.write('loads, ' + str(l+1) + ', name     @' + str(load['name'])     + ' $string'  + '\n')
            out.write('loads, ' + str(l+1) + ', type     @' + str(load['type'])     + ' $string'  + '\n')
            out.write('loads, ' + str(l+1) + ', set      @' + str(load['set'])      + ' $string'  + '\n')
            out.write('loads, ' + str(l+1) + ', value    @' + str(load['value'])    + ' $list of float'  + '\n')
            out.write('loads, ' + str(l+1) + ', stepName @' + str(load['stepName']) + ' $string'  + '\n')
        out.write('#' + '\n')

def writeBCsControls(fullPath,bcNORTHcontrols,bcRIGHTcontrols,bcLEFTcontrols):
    with open(fullPath,'a') as out:
        out.write('# Boundary conditions' + '\n')
        out.write('# vgeomcoupling           ==> nodes belong to line, free to move and rotate rigidly' + '\n')
        out.write('# vkinCouplingmeancorners ==> coupling of vertical displacement' + '\n')
        out.write('# antisymmetry            ==> antisymmetric coupling' + '\n')
        out.write('# ulinearCoupling         ==> linear distribution of horizontal displacement' + '\n')
        out.write('# boundingPly             ==> homogenized material' + '\n')
        out.write('# adjacentFibers          ==> fibers and matrix (microstructure)' + '\n')
        out.write('BC, northSide, type     @' + str(bcNORTHcontrols['type'])    + ' $string'  + '\n')
        out.write('BC, northSide, tRatio   @' + str(bcNORTHcontrols['tRatio'])  + ' $float'  + '\n')
        out.write('BC, northSide, nFibers  @' + str(bcNORTHcontrols['nFibers']) + ' $int'  + '\n')
        out.write('BC, rightSide, type     @' + str(bcRIGHTcontrols['type'])    + ' $string'  + '\n')
        out.write('BC, rightSide, tRatio   @' + str(bcRIGHTcontrols['tRatio'])  + ' $float'  + '\n')
        out.write('BC, rightSide, nFibers  @' + str(bcRIGHTcontrols['nFibers']) + ' $int'  + '\n')
        out.write('BC, leftSide, type      @' + str(bcLEFTcontrols['type'])     + ' $string'  + '\n')
        out.write('BC, leftSide, tRatio    @' + str(bcLEFTcontrols['tRatio'])   + ' $float'  + '\n')
        out.write('BC, leftSide, nFibers   @' + str(bcLEFTcontrols['nFibers'])  + ' $int'  + '\n')
        out.write('#' + '\n')

def writeSurfacefrictionControls(fullPath,surfacefrictionControls):
    with open(fullPath,'a') as out:
        out.write('# Surface friction' + '\n')
        out.write('# none         ==> frictionless surface' + '\n')
        out.write('# static       ==> static friction is present' + '\n')
        out.write('# dynamic      ==> dynamic friction is present' + '\n')
        out.write('# cpress       ==> contact pressure dependent' + '\n')
        out.write('# temperature  ==> temperature dependent' + '\n')
        out.write('# maxtau       ==> maximum value of frictional shear stress' + '\n')
        out.write('surface, friction, type          @' + str(surfacefrictionControls['type'])         + ' $string' + '\n')
        out.write('surface, friction, static        @' + str(surfacefrictionControls['static'])       + ' $float'  + '\n')
        out.write('surface, friction, dynamic       @' + str(surfacefrictionControls['dynamic'])      + ' $float'  + '\n')
        out.write('surface, friction, cpress        @' + str(surfacefrictionControls['cpress'])       + ' $float'  + '\n')
        out.write('surface, friction, temperature   @' + str(surfacefrictionControls['temperature'])  + ' $float'  + '\n')
        out.write('surface, friction, maxtau        @' + str(surfacefrictionControls['maxtau'])       + ' $float'  + '\n')
        out.write('#' + '\n')

def writeMeshControls(fullPath,meshControls):
    with open(fullPath,'a') as out:
        out.write('# Mesh' + '\n')
        out.write('mesh, size, deltapsi      @' + str(meshControls['deltapsi']) + ' $float' + '\n')
        out.write('mesh, size, deltaphi      @' + str(meshControls['deltaphi']) + ' $float'  + '\n')
        out.write('mesh, size, delta         @' + str(meshControls['delta'])    + ' $float'  + '\n')
        out.write('mesh, size, delta1        @' + str(meshControls['delta1'])   + ' $float'  + '\n')
        out.write('mesh, size, delta2        @' + str(meshControls['delta2'])   + ' $float'  + '\n')
        out.write('mesh, size, delta3        @' + str(meshControls['delta3'])   + ' $float'  + '\n')
        out.write('mesh, elements, minElNum  @' + str(meshControls['minElNum']) + ' $int' + '\n')
        out.write('mesh, elements, order     @' + str(meshControls['order'])    + ' $string'  + '\n')
        out.write('#' + '\n')

def writeJintegralControls(fullPath,jintegralControls):
    with open(fullPath,'a') as out:
        out.write('# J-Integral' + '\n')
        out.write('Jintegral, numberOfContours  @' + str(jintegralControls['numberOfContours']) + ' $int' + '\n')
        out.write('singularity, type            @' + str(jintegralControls['type'])             + ' $string'  + '\n')
        out.write('#' + '\n')

def writeSolverControls(fullPath,solverControls):
    with open(fullPath,'a') as out:
        out.write('# Solver properties' + '\n')
        out.write('solver, cpus  @' + str(solverControls['cpus']) + ' $int' + '\n')
        out.write('#' + '\n')

def writeOutputControls(fullPath,outputControls):
    with open(fullPath,'a') as out:
        out.write('# Output directory and filenames' + '\n')
        out.write('output, archive, directory                             @' + str(outputControls['archive']['directory']) + ' $string' + '\n')
        out.write('output, global, directory                              @' + str(outputControls['global']['directory']) + ' $string' + '\n')
        out.write('output, global, filenames, performances                @' + str(outputControls['global']['filenames']['performances']) + ' $string' + '\n')
        out.write('output, global, filenames, energyreleaserate           @' + str(outputControls['global']['filenames']['energyreleaserate']) + ' $string' + '\n')
        out.write('output, global, filenames, inputdata                   @' + str(outputControls['global']['filenames']['inputdata']) + ' $string' + '\n')
        out.write('output, local, directory                               @' + str(outputControls['local']['directory']) + ' $string' + '\n')
        out.write('output, local, filenames, Jintegral                    @' + str(outputControls['local']['filenames']['Jintegral']) + ' $string' + '\n')
        out.write('output, local, filenames, stressesatboundary           @' + str(outputControls['local']['filenames']['stressesatboundary']) + ' $string' + '\n')
        out.write('output, local, filenames, crackdisplacements           @' + str(outputControls['local']['filenames']['crackdisplacements']) + ' $string' + '\n')
        out.write('output, local, filenames, contactzonetolerance         @' + str(outputControls['local']['filenames']['contactzonetolerance']) + ' $string' + '\n')
        out.write('output, report, global, directory                      @' + str(outputControls['report']['global']['directory']) + ' $string' + '\n')
        out.write('output, report, global, filename                       @' + str(outputControls['report']['global']['filename']) + ' $string' + '\n')
        out.write('output, report, local, directory                       @' + str(outputControls['report']['local']['directory']) + ' $list of string' + '\n')
        out.write('output, report, local, filenames, Jintegral            @' + str(outputControls['report']['local']['filenames']['Jintegral']) + ' $list of string' + '\n')
        out.write('output, report, local, filenames, stressesatboundary   @' + str(outputControls['report']['local']['filenames']['stressesatboundary']) + ' $list of string' + '\n')
        out.write('output, report, local, filenames, crackdisplacements   @' + str(outputControls['report']['local']['filenames']['crackdisplacements']) + ' $list of string' + '\n')
        out.write('output, report, local, filenames, contactzonetolerance @' + str(outputControls['report']['local']['filenames']['contactzonetolerance']) + ' $list of string' + '\n')
        out.write('output, sql, global, directory                         @' + str(outputControls['sql']['global']['directory']) + ' $string' + '\n')
        out.write('output, sql, global, filename                          @' + str(outputControls['sql']['global']['filename']) + ' $string' + '\n')
        out.write('#' + '\n')

def main():

    runningOn = 'LTU'
    PC = 'LucaPC'
    onedriveSubfolder = '01_Luca/07_DocMASE/07_Data/03_FEM/InputData/asymm'

    if runningOn=='LucaPC':
        outDir = 'C:/Users/luca/OneDrive/' + onedriveSubfolder
    elif runningOn=='EEIGM':
        outDir = 'D:/OneDrive/' + onedriveSubfolder
    else:
        outDir = 'C:/Users/lucdis/OneDrive/' + onedriveSubfolder

    if PC=='LucaPC':
        ending = '-LPC'
        onedriveDir = 'C:/Users/luca/OneDrive/'
        onedriveOutSubfolder = '01_Luca/07_DocMASE/07_Data/03_FEM/LucaPC'
    else:
        ending = 'COARED'
        onedriveDir = 'D:/OneDrive/'
        onedriveOutSubfolder = '01_Luca/07_DocMASE/07_Data/03_FEM'

    datbaseName = 'inputRVEdata'
    itbaseName = 'inputRVEiterables'
    ext = '.deck'
    Ls = ['1_144'] # out of ['1_618','1_25','1_144','1_0992']
    #homogSize = ['1','2','3','5']
    nFibsAb = [1,2,3,5,10,50,100]
    nFibsSi = [1,2,3,5,10,50,100]

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
    pipeline['report-energyreleaserates'] = 'True'
    pipeline['report-contactzone'] = 'False'
    pipeline['report-stressesatboundary'] = 'False'
    pipeline['report-stressesatsymmetryline'] = 'False'
    pipeline['report-stressesatbondedinterface'] = 'False'
    pipeline['report-crackdisplacements'] = 'False'

    input = {}
    input['wd'] = 'C:/Abaqus_WD/CurvedInterface'
    input['caefilename'] = 'sweepOverDeltathetaL1_0992A1S2F'
    input['modelname'] = 'aname'

    geometry  = {}
    geometry['fiberType'] = 'half'
    geometry['L'] = '1.0992'
    geometry['Rf'] = '1.0'
    geometry['theta'] = '0.0'
    geometry['deltatheta'] = '10.0'

    materials = []
    mat1 = {}
    mat1['name'] = 'glassFiber'
    mat1['type'] = 'ISOTROPIC'
    mat1['elProps'] = '[70e3,0.2]'
    materials.append(mat1)
    mat2 = {}
    mat2['name'] = 'epoxy'
    mat2['type'] = 'ISOTROPIC'
    mat2['elProps'] = '[3.5e3,0.4]'
    materials.append(mat2)

    postproc = {}
    postproc['nu-G0'] = '0.4'
    postproc['G-G0'] = '1250.0'

    sections = []
    sec1 = {}
    sec1['name'] = 'fiberSection'
    sec1['type'] = 'HomogeneousSolidSection'
    sec1['material'] = 'glassFiber'
    sec1['thickness'] = '1.0'
    sections.append(sec1)
    sec2 = {}
    sec2['name'] = 'matrixSection'
    sec2['type'] = 'HomogeneousSolidSection'
    sec2['material'] = 'epoxy'
    sec2['thickness'] = '1.0'
    sections.append(sec2)

    sectionRegionsSideAbove = []
    secRegion1 = {}
    secRegion1['name'] = 'fiberSection'
    secRegion1['set'] = 'FIBER'
    secRegion1['offSetType'] = 'MIDDLE_SURFACE'
    secRegion1['offsetField'] = ' '
    secRegion1['thicknessAssignment'] = 'FROM_SECTION'
    secRegion1['offsetValue'] = '0.0'
    sectionRegionsSideAbove.append(secRegion1)
    secRegion2 = {}
    secRegion2['name'] = 'matrixSection'
    secRegion2['set'] = 'MATRIX'
    secRegion2['offSetType'] = 'MIDDLE_SURFACE'
    secRegion2['offsetField'] = ' '
    secRegion2['thicknessAssignment'] = 'FROM_SECTION'
    secRegion2['offsetValue'] = '0.0'
    sectionRegionsSideAbove.append(secRegion2)
    secRegion3 = {}
    secRegion3['name'] = 'fiberSection'
    secRegion3['set'] = 'UPPER-FIBERS'
    secRegion3['offSetType'] = 'MIDDLE_SURFACE'
    secRegion3['offsetField'] = ' '
    secRegion3['thicknessAssignment'] = 'FROM_SECTION'
    secRegion3['offsetValue'] = '0.0'
    sectionRegionsSideAbove.append(secRegion3)
    secRegion4 = {}
    secRegion4['name'] = 'fiberSection'
    secRegion4['set'] = 'LEFT-FIBERS'
    secRegion4['offSetType'] = 'MIDDLE_SURFACE'
    secRegion4['offsetField'] = ' '
    secRegion4['thicknessAssignment'] = 'FROM_SECTION'
    secRegion4['offsetValue'] = '0.0'
    sectionRegionsSideAbove.append(secRegion4)
    secRegion5 = {}
    secRegion5['name'] = 'fiberSection'
    secRegion5['set'] = 'RIGHT-FIBERS'
    secRegion5['offSetType'] = 'MIDDLE_SURFACE'
    secRegion5['offsetField'] = ' '
    secRegion5['thicknessAssignment'] = 'FROM_SECTION'
    secRegion5['offsetValue'] = '0.0'
    sectionRegionsSideAbove.append(secRegion5)

    sectionRegionsSide = []
    secRegion1 = {}
    secRegion1['name'] = 'fiberSection'
    secRegion1['set'] = 'FIBER'
    secRegion1['offSetType'] = 'MIDDLE_SURFACE'
    secRegion1['offsetField'] = ' '
    secRegion1['thicknessAssignment'] = 'FROM_SECTION'
    secRegion1['offsetValue'] = '0.0'
    sectionRegionsSideAbove.append(secRegion1)
    secRegion2 = {}
    secRegion2['name'] = 'matrixSection'
    secRegion2['set'] = 'MATRIX'
    secRegion2['offSetType'] = 'MIDDLE_SURFACE'
    secRegion2['offsetField'] = ' '
    secRegion2['thicknessAssignment'] = 'FROM_SECTION'
    secRegion2['offsetValue'] = '0.0'
    sectionRegionsSideAbove.append(secRegion2)
    secRegion4 = {}
    secRegion4['name'] = 'fiberSection'
    secRegion4['set'] = 'LEFT-FIBERS'
    secRegion4['offSetType'] = 'MIDDLE_SURFACE'
    secRegion4['offsetField'] = ' '
    secRegion4['thicknessAssignment'] = 'FROM_SECTION'
    secRegion4['offsetValue'] = '0.0'
    sectionRegionsSideAbove.append(secRegion4)
    secRegion5 = {}
    secRegion5['name'] = 'fiberSection'
    secRegion5['set'] = 'RIGHT-FIBERS'
    secRegion5['offSetType'] = 'MIDDLE_SURFACE'
    secRegion5['offsetField'] = ' '
    secRegion5['thicknessAssignment'] = 'FROM_SECTION'
    secRegion5['offsetValue'] = '0.0'
    sectionRegionsSideAbove.append(secRegion5)

    sectionRegionsAbove = []
    secRegion1 = {}
    secRegion1['name'] = 'fiberSection'
    secRegion1['set'] = 'FIBER'
    secRegion1['offSetType'] = 'MIDDLE_SURFACE'
    secRegion1['offsetField'] = ' '
    secRegion1['thicknessAssignment'] = 'FROM_SECTION'
    secRegion1['offsetValue'] = '0.0'
    sectionRegionsSideAbove.append(secRegion1)
    secRegion2 = {}
    secRegion2['name'] = 'matrixSection'
    secRegion2['set'] = 'MATRIX'
    secRegion2['offSetType'] = 'MIDDLE_SURFACE'
    secRegion2['offsetField'] = ' '
    secRegion2['thicknessAssignment'] = 'FROM_SECTION'
    secRegion2['offsetValue'] = '0.0'
    sectionRegionsSideAbove.append(secRegion2)
    secRegion3 = {}
    secRegion3['name'] = 'fiberSection'
    secRegion3['set'] = 'UPPER-FIBERS'
    secRegion3['offSetType'] = 'MIDDLE_SURFACE'
    secRegion3['offsetField'] = ' '
    secRegion3['thicknessAssignment'] = 'FROM_SECTION'
    secRegion3['offsetValue'] = '0.0'
    sectionRegionsSideAbove.append(secRegion3)

    steps = []
    step1 = {}
    step1['name'] = 'Load-Step'
    step1['previous'] = 'Initial'
    step1['minimumIncrement'] = '1e-10'
    steps.append(step1)

    loads = []
    load1 = {}
    load1['name'] = 'rightBC'
    load1['type'] = 'appliedStrain'
    load1['set'] = 'RIGHTSIDE'
    load1['value'] = '[0.01,0.0,0.0]'
    load1['stepName'] = 'Load-Step'
    loads.append(load1)
    load2 = {}
    load2['name'] = 'leftBC'
    load2['type'] = 'appliedStrain'
    load2['set'] = 'LEFTSIDE'
    load2['value'] = '[0.01,0.0,0.0]'
    load2['stepName'] = 'Load-Step'
    loads.append(load2)

    bcNORTH = {}
    bcNORTH['type'] = 'adjacentFibers'
    bcNORTH['tRatio'] = '0.0'
    bcNORTH['nFibers'] = '1'
    bcRIGHT = {}
    bcRIGHT['type'] = 'adjacentFibers'
    bcRIGHT['wRatio'] = '0.0'
    bcRIGHT['nFibers'] = '1'
    bcLEFT = {}
    bcLEFT['type'] = 'adjacentFibers'
    bcLEFT['wRatio'] = '0.0'
    bcLEFT['nFibers'] = '1'

    friction = {}
    friction['type']        = 'none'
    friction['static']      = '0.0'
    friction['dynamic']     = '0.0'
    friction['cpress']      = '0.0'
    friction['temperature'] = '0.0'
    friction['maxtau']      = '0.0'

    mesh = {}
    mesh['deltapsi'] = '10.0'
    mesh['deltaphi'] = '10.0'
    mesh['delta']    = '0.05'
    mesh['delta1']   = '1.0'
    mesh['delta2']   = '1.0'
    mesh['delta3']   = '1.0'
    mesh['minElNum'] = '5'
    mesh['order']    = 'second'

    jint = {}
    jint['numberOfContours'] = '5'
    jint['type'] = 'none'

    solver = {}
    solver['cpus'] = '4'

    output = {}
    output['archive'] = {}
    output['archive']['directory'] = 'G:/sweepDeltathetaVff-GF-BCvkinmeancornerscoupling'
    output['global'] = {}
    output['global']['directory'] = 'C:/Users/lucad/OneDrive/01_Luca/07_DocMASE/07_Data/03_FEM/LucaPC/sweepOverDeltathetaL1_0992A1S1F'
    output['global']['filenames'] = {}
    output['global']['filenames']['performances'] = 'sweepOverDeltathetaL1_0992A1S1F-performances'
    output['global']['filenames']['energyreleaserates'] = 'sweepOverDeltathetaL1_0992A1S1F-energyreleaserates'
    output['global']['filenames']['inputdata'] = 'sweepOverDeltathetaL1_0992A1S1F-inputdata'
    output['local'] = {}
    output['local']['directory'] = 'C:/Users/lucad/OneDrive/01_Luca/07_DocMASE/07_Data/03_FEM/LucaPC/sweepOverDeltathetaL1_0992A1S1F'
    output['local']['filenames'] = {}
    output['local']['filenames']['Jintegral'] = 'C:/'
    output['local']['filenames']['stressesatboundary'] = 'C:/'
    output['local']['filenames']['crackdisplacements'] = 'C:/'
    output['local']['filenames']['contactzonetolerance'] = 'C:/'
    output['report'] = {}
    output['report']['global'] = {}
    output['report']['global']['directory'] = 'C:/Users/lucad/OneDrive/01_Luca/07_DocMASE/07_Data/03_FEM/LucaPC/sweepOverDeltathetaL1_0992A1S1F'
    output['report']['global']['filename'] = 'sweepOverDeltathetaL1_0992A1S1F-report'
    output['report']['local'] = {}
    output['report']['local']['directory'] = '[]'
    output['report']['local']['filenames'] = {}
    output['report']['local']['filenames']['Jintegral'] = '[]'
    output['report']['local']['filenames']['stressesatboundary'] = '[]'
    output['report']['local']['filenames']['crackdisplacements'] = '[]'
    output['report']['local']['filenames']['contactzonetolerance'] = '[]'
    output['sql'] = {}
    output['sql']['global'] = {}
    output['sql']['global']['directory'] = 'C:/Users/lucad/OneDrive/01_Luca/07_DocMASE/07_Data/03_FEM/LucaPC/sweepOverDeltathetaL1_0992A1S1F'
    output['sql']['global']['filename'] = 'sweepOverDeltathetaL1_0992A1S1FDB'

    for L in Ls:
        #for s in homogSize:
        for n in nFibsSi:
            writeIntro(join(inpDir,datbaseName+nickName+'L'+L+'S'+str(n)+ending+ext))
            writeIntro(join(inpDir,itbaseName+nickName+'L'+L+'S'+str(n)+ending+ext))

            writePipelineControls(join(inpDir,datbaseName+nickName+'L'+L+'S'+str(n)+ending+ext),pipeline)

            writeAnalysisControls(join(inpDir,datbaseName+nickName+'L'+L+'S'+str(n)+ending+ext),analysis)

            input['caefilename'] = 'sweepOverDeltatheta' + nickName + 'L' + L + 'S' + str(n) + ending
            writeInputControls(join(inpDir,datbaseName+nickName+'L'+L+'S'+str(n)+ending+ext),input)

            geometry['L'] = L.replace('_','.')
            writeGeometryControls(join(inpDir,datbaseName+nickName+'L'+L+'S'+str(n)+ending+ext),geometry)

            writeMaterialsControls(join(inpDir,datbaseName+nickName+'L'+L+'S'+str(n)+ending+ext),materials)

            writePostprocControls(join(inpDir,datbaseName+nickName+'L'+L+'S'+str(n)+ending+ext),postproc)

            writeSectionsControls(join(inpDir,datbaseName+nickName+'L'+L+'S'+str(n)+ending+ext),sections)

            writeSectionregionsControls(join(inpDir,datbaseName+nickName+'L'+L+'S'+str(n)+ending+ext),sectionRegionsSide)

            writeStepsControls(join(inpDir,datbaseName+nickName+'L'+L+'S'+str(n)+ending+ext),steps)

            writeLoadsControls(join(inpDir,datbaseName+nickName+'L'+L+'S'+str(n)+ending+ext),loads)

            bcNORTH = {}
            bcNORTH['type'] = 'antisymmetry'
            bcNORTH['tRatio'] = '0.0'
            bcNORTH['nFibers'] = '0'

            bcRIGHT = {}
            bcRIGHT['type'] = 'adjacentFibers'
            bcRIGHT['wRatio'] = '0.0'
            bcRIGHT['nFibers'] = str(n)

            bcLEFT = {}
            bcLEFT['type'] = 'adjacentFibers'
            bcLEFT['wRatio'] = '0.0'
            bcLEFT['nFibers'] = str(n)

            writeBCsControls(join(inpDir,datbaseName+nickName+'L'+L+'S'+str(n)+ending+ext),bcNORTH,bcRIGHT,bcLEFT)

            writeSurfacefrictionControls(join(inpDir,datbaseName+nickName+'L'+L+'S'+str(n)+ending+ext),friction)

            writeMeshControls(join(inpDir,datbaseName+nickName+'L'+L+'S'+str(n)+ending+ext),mesh)

            writeJintegralControls(join(inpDir,datbaseName+nickName+'L'+L+'S'+str(n)+ending+ext),jint)

            writeSolverControls(join(inpDir,datbaseName+nickName+'L'+L+'S'+str(n)+ending+ext),solver)


            output['global']['directory'] = onedriveDir + onedriveOutSubfolder + '/' + 'sweepOverDeltatheta' + nickName + 'L' + L + 'S' + str(n) + ending

            output['global']['filenames']['performances'] = 'sweepOverDeltatheta' + nickName + 'L' + L + 'S' + str(n) + ending + '-performances'
            output['global']['filenames']['energyreleaserates'] = 'sweepOverDeltatheta' + nickName + 'L' + L + 'S' + str(n) + ending + '-energyreleaserates'
            output['global']['filenames']['inputdata'] = 'sweepOverDeltatheta' + nickName + 'L' + L + 'S' + str(n) + ending + '-inputdata'

            output['local']['directory'] = onedriveDir + onedriveOutSubfolder + '/' + 'sweepOverDeltatheta' + nickName + 'L' + L + 'S' + str(n) + ending

            output['report']['global']['directory'] = onedriveDir + onedriveOutSubfolder + '/' + 'sweepOverDeltatheta' + nickName + 'L' + L + 'S' + str(n) + ending
            output['report']['global']['filename'] = 'sweepOverDeltatheta' + nickName + 'L' + L + 'S' + str(n) + ending + '-report'

            output['sql']['global']['directory'] = onedriveDir + onedriveOutSubfolder + '/' + 'sweepOverDeltatheta' + nickName + 'L' + L + 'S' + str(n) + ending
            output['sql']['global']['filename'] = 'sweepOverDeltatheta' + nickName + 'L' + L + 'S' + str(n) + ending + 'DB'

            writeOutputControls(join(inpDir,datbaseName+nickName+'L'+L+'S'+str(n)+ending+ext),output)

if __name__ == '__main__':
    main()
