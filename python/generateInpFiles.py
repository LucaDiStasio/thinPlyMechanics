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
    secRegion2['name'] = 'matrixSection'
    secRegion2['set'] = 'MATRIX'
    secRegion2['offSetType'] = 'MIDDLE_SURFACE'
    secRegion2['offsetField'] = ' '
    secRegion2['thicknessAssignment'] = 'FROM_SECTION'
    secRegion2['offsetValue'] = '0.0'
    sectionRegionsSideAbove.append(secRegion2)
    secRegion3['name'] = 'fiberSection'
    secRegion3['set'] = 'UPPER-FIBERS'
    secRegion3['offSetType'] = 'MIDDLE_SURFACE'
    secRegion3['offsetField'] = ' '
    secRegion3['thicknessAssignment'] = 'FROM_SECTION'
    secRegion3['offsetValue'] = '0.0'
    sectionRegionsSideAbove.append(secRegion3)
    secRegion4['name'] = 'fiberSection'
    secRegion4['set'] = 'LEFT-FIBERS'
    secRegion4['offSetType'] = 'MIDDLE_SURFACE'
    secRegion4['offsetField'] = ' '
    secRegion4['thicknessAssignment'] = 'FROM_SECTION'
    secRegion4['offsetValue'] = '0.0'
    sectionRegionsSideAbove.append(secRegion4)
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
    secRegion2['name'] = 'matrixSection'
    secRegion2['set'] = 'MATRIX'
    secRegion2['offSetType'] = 'MIDDLE_SURFACE'
    secRegion2['offsetField'] = ' '
    secRegion2['thicknessAssignment'] = 'FROM_SECTION'
    secRegion2['offsetValue'] = '0.0'
    sectionRegionsSideAbove.append(secRegion2)
    secRegion4['name'] = 'fiberSection'
    secRegion4['set'] = 'LEFT-FIBERS'
    secRegion4['offSetType'] = 'MIDDLE_SURFACE'
    secRegion4['offsetField'] = ' '
    secRegion4['thicknessAssignment'] = 'FROM_SECTION'
    secRegion4['offsetValue'] = '0.0'
    sectionRegionsSideAbove.append(secRegion4)
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
    secRegion2['name'] = 'matrixSection'
    secRegion2['set'] = 'MATRIX'
    secRegion2['offSetType'] = 'MIDDLE_SURFACE'
    secRegion2['offsetField'] = ' '
    secRegion2['thicknessAssignment'] = 'FROM_SECTION'
    secRegion2['offsetValue'] = '0.0'
    sectionRegionsSideAbove.append(secRegion2)
    secRegion3['name'] = 'fiberSection'
    secRegion3['set'] = 'UPPER-FIBERS'
    secRegion3['offSetType'] = 'MIDDLE_SURFACE'
    secRegion3['offsetField'] = ' '
    secRegion3['thicknessAssignment'] = 'FROM_SECTION'
    secRegion3['offsetValue'] = '0.0'
    sectionRegionsSideAbove.append(secRegion3)

    for L in Ls:
        #for s in homogSize:
        for n in nFibsSi:
            writeIntro(join(inpDir,datbaseName+nickName+'L'+L+'S'+str(n)+ending+ext))
            writeIntro(join(inpDir,itbaseName+nickName+'L'+L+'S'+str(n)+ending+ext))

            writePipelineControls(join(inpDir,datbaseName+nickName+'L'+L+'S'+str(n)+ending+ext),pipeline)

            writeAnalysisControls(join(inpDir,datbaseName+nickName+'L'+L+'S'+str(n)+ending+ext),analysis)

            input['caefilename'] = 'sweepOverDeltatheta' + nickName+'L'+L+'S'+str(n)+ending
            writeInputControls(join(inpDir,datbaseName+nickName+'L'+L+'S'+str(n)+ending+ext),input)

            geometry['L'] = L.replace('_','.')
            writeGeometryControls(join(inpDir,datbaseName+nickName+'L'+L+'S'+str(n)+ending+ext),geometry)

            writeMaterialsControls(join(inpDir,datbaseName+nickName+'L'+L+'S'+str(n)+ending+ext),materials)

            writePostprocControls(join(inpDir,datbaseName+nickName+'L'+L+'S'+str(n)+ending+ext),postproc)

            writeSectionsControls(join(inpDir,datbaseName+nickName+'L'+L+'S'+str(n)+ending+ext),sections)

            writeSectionregionsControls(join(inpDir,datbaseName+nickName+'L'+L+'S'+str(n)+ending+ext),sectionRegionsSide)




if __name__ == '__main__':
    main()
