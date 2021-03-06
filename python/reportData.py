#!/usr/bin/env Python
# -*- coding: utf-8 -*-

'''
=====================================================================================

Copyright (c) 2016 - 2019 Université de Lorraine & Luleå tekniska universitet
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
from shutil import copyfile
from os import listdir, stat, makedirs
from datetime import datetime
from time import strftime
from platform import platform
import matplotlib as plt
import numpy as np
import xlsxwriter
import ast
import getopt

#===============================================================================#
#                                 Latex files
#===============================================================================#

def createLatexFile(folder,filename,documentclass,options=''):
    if not exists(folder):
        makedirs(folder)
    with open(join(folder,filename + '.tex'),'w') as tex:
        if options!='':
            tex.write('\\documentclass[' + options + ']{' + documentclass + '}\n')
        else:
            tex.write('\\documentclass{' + documentclass + '}\n')
        tex.write('\n')

def writeLatexPackages(folder,filename,packages,options):
    with open(join(folder,filename + '.tex'),'a') as tex:
        tex.write('%----------------------------------------------------------------------------------------------%\n')
        tex.write('%                                 Packages and basic declarations\n')
        tex.write('%----------------------------------------------------------------------------------------------%\n')
        tex.write('\n')
        for i,package in enumerate(packages):
            if options[i]!='':
                tex.write('\\usepackage[' + options[i] + ']{' + package + '}\n')
            else:
                tex.write('\\usepackage{' + package + '}\n')
        tex.write('\n')

def writeLatexDocumentStarts(folder,filename):
    with open(join(folder,filename + '.tex'),'a') as tex:
        tex.write('\n')
        tex.write('%----------------------------------------------------------------------------------------------%\n')
        tex.write('%----------------------------------------------------------------------------------------------%\n')
        tex.write('%                                            DOCUMENT STARTS\n')
        tex.write('%----------------------------------------------------------------------------------------------%\n')
        tex.write('%----------------------------------------------------------------------------------------------%\n')
        tex.write('\n')
        tex.write('\\begin{document}\n')
        tex.write('\n')

def writeLatexDocumentEnds(folder,filename):
    with open(join(folder,filename + '.tex'),'a') as tex:
        tex.write('\n')
        tex.write('\\end{document}\n')
        tex.write('\n')
        tex.write('%----------------------------------------------------------------------------------------------%\n')
        tex.write('%----------------------------------------------------------------------------------------------%\n')
        tex.write('%                                            DOCUMENT ENDS\n')
        tex.write('%----------------------------------------------------------------------------------------------%\n')
        tex.write('%----------------------------------------------------------------------------------------------%\n')
        tex.write('\n')

def writeLatexTikzPicStarts(folder,filename,options=''):
    with open(join(folder,filename + '.tex'),'a') as tex:
        tex.write('\n')
        tex.write('%Tikz picture starts%\n')
        tex.write('\n')
        if options!='':
            tex.write('\\begin{tikzpicture}[' + options + ']\n')
        else:
            tex.write('\\begin{tikzpicture}\n')

def writeLatexTikzPicEnds(folder,filename):
    with open(join(folder,filename + '.tex'),'a') as tex:
        tex.write('\n')
        tex.write('\\end{tikzpicture}\n')
        tex.write('%Tikz picture ends%\n')
        tex.write('\n')

def writeLatexTikzAxisStarts(folder,filename,options):
    with open(join(folder,filename + '.tex'),'a') as tex:
        tex.write('\n')
        tex.write('%Tikz axis starts%\n')
        tex.write('\n')
        if options!='':
            tex.write('\\begin{axis}[' + options + ']\n')
        else:
            tex.write('\\begin{axis}\n')

def writeLatexTikzAxisEnds(folder,filename):
    with open(join(folder,filename + '.tex'),'a') as tex:
        tex.write('\n')
        tex.write('\\end{axis}\n')
        tex.write('%Tikz axis ends%\n')
        tex.write('\n')

def writeLatexAddPlotTable(folder,filename,data,options):
    with open(join(folder,filename + '.tex'),'a') as tex:
        tex.write('\n')
        tex.write('\\addplot')
        if options!='':
            tex.write('[' + options + ']\n')
        tex.write('table{\n')
        for element in data:
            tex.write(str(element[0]) + ' ' + str(element[1]) + '\n')
        tex.write('};\n')

def writeLatexSinglePlot(folder,filename,data,axoptions,dataoptions):
    print('In function: writeLatexSinglePlot(folder,filename,data,axoptions,dataoptions,logfilepath,baselogindent,logindent)')
    print('Create latex file')
    createLatexFile(folder,filename,'standalone')
    print('Write latex packages')
    writeLatexPackages(folder,filename,['inputenc','pgfplots','tikz'],['utf8','',''])
    print('Document starts')
    writeLatexDocumentStarts(folder,filename)
    writeLatexTikzPicStarts(folder,filename,'')
    writeLatexTikzAxisStarts(folder,filename,axoptions)
    writeLatexAddPlotTable(folder,filename,data,dataoptions)
    writeLatexTikzAxisEnds(folder,filename)
    writeLatexTikzPicEnds(folder,filename)
    print('Document ends')
    writeLatexDocumentEnds(folder,filename)
    if 'Windows' in system():
        print('Create Windows command file')
        cmdfile = join(folder,filename,'runlatex.cmd')
        with open(cmdfile,'w') as cmd:
            cmd.write('\n')
            cmd.write('CD ' + folder + '\n')
            cmd.write('\n')
            cmd.write('pdflatex ' + join(folder,filename + '.tex') + ' -job-name=' + filename + '\n')
        print('Executing Windows command file...')
        try:
            subprocess.call('cmd.exe /C ' + cmdfile)
            print('... done.')
        except Exception:
            print('ERROR')
            print(str(Exception))
            print(str(error))
            sys.exc_clear()
    elif 'Linux' in system():
        print('Create Linux bash file')
        bashfile = join(folder,filename,'runlatex.sh')
        with open(bashfile,'w') as bsh:
            bsh.write('#!/bin/bash\n')
            bsh.write('\n')
            bsh.write('cd ' + folder + '\n')
            bsh.write('\n')
            bsh.write('pdflatex ' + join(folder,filename + '.tex') + ' -job-name=' + filename + '\n')
            print('Executing Linux bash file...')
            try:
                print('Change permissions to ' + bashfile)
                os.chmod(bashfile, 0o755)
                print('Run bash file')
                rc = call('.' + bashfile)
                print('... done.')
            except Exception:
                print('ERROR')
                print(str(Exception))
                print(str(error))
                sys.exc_clear()

def writeLatexMultiplePlots(folder,filename,data,axoptions,dataoptions):
    print('In function: writeLatexMultiplePlots(folder,filename,data,axoptions,dataoptions,logfilepath,baselogindent,logindent)',True)
    print('Create latex file')
    createLatexFile(folder,filename,'standalone')
    print('Write latex packages')
    writeLatexPackages(folder,filename,['inputenc','pgfplots','tikz'],['utf8','',''])
    print('Document starts')
    writeLatexDocumentStarts(folder,filename)
    writeLatexTikzPicStarts(folder,filename,'')
    writeLatexTikzAxisStarts(folder,filename,axoptions)
    for k,datum in enumerate(data):
        writeLatexAddPlotTable(folder,filename,datum,dataoptions[k])
    writeLatexTikzAxisEnds(folder,filename)
    writeLatexTikzPicEnds(folder,filename)
    print('Document ends')
    writeLatexDocumentEnds(folder,filename)
    if 'Windows' in system():
        print('Create Windows command file')
        cmdfile = join(folder,'runlatex.cmd')
        with open(cmdfile,'w') as cmd:
            cmd.write('\n')
            cmd.write('CD ' + folder + '\n')
            cmd.write('\n')
            cmd.write('pdflatex ' + join(folder,filename + '.tex') + ' -job-name=' + filename + '\n')
        print('Executing Windows command file...')
        try:
            subprocess.call('cmd.exe /C ' + cmdfile)
            print('... done.')
        except Exception,error:
            print('ERROR')
            print(str(Exception))
            print(str(error))
            sys.exc_clear()
    elif 'Linux' in system():
        print('Create Linux bash file')
        bashfile = join(folder,filename,'runlatex.sh')
        with open(bashfile,'w') as bsh:
            bsh.write('#!/bin/bash\n')
            bsh.write('\n')
            bsh.write('cd ' + folder + '\n')
            bsh.write('\n')
            bsh.write('pdflatex ' + join(folder,filename + '.tex') + ' -job-name=' + filename + '\n')
            print('Executing Linux bash file...')
            try:
                print('Change permissions to ' + bashfile)
                os.chmod(bashfile, 0o755)
                print('Run bash file')
                rc = call('.' + bashfile)
                print('... done.')
            except Exception:
                print('ERROR')
                print(str(Exception))
                print(str(error))
                sys.exc_clear()

def writeLatexGenericCommand(folder,filename,command,options,arguments):
    with open(join(folder,filename + '.tex'),'a') as tex:
        if options!='' and arguments!='':
            tex.write('\\'+ command +'[' + options + ']{' + arguments + '}\n')
        elif options!='':
            tex.write('\\'+ command +'{' + arguments + '}\n')
        else:
            tex.write('\\'+ command + '\n')
        tex.write('\n')

def writeLatexCustomLine(folder,filename,line):
    with open(join(folder,filename + '.tex'),'a') as tex:
        tex.write(line + '\n')

def writeLatexSetLength(folder,filename,length,value):
    with open(join(folder,filename + '.tex'),'a') as tex:
        tex.write('\\setlength' +'{' + '\\' + length + '}' +'{' + value + '}\n')

#===============================================================================#
#                              Reference data
#===============================================================================#

def provideBEMdata():
    G0 = 7.52548E-06
    normGs = np.array([[10.,1.39E-01,3.76E-02,1.76E-01],
               [20.,1.93E-01,1.47E-01,3.40E-01],
               [30.,1.64E-01,3.02E-01,4.66E-01],
               [40.,9.80E-02,4.86E-01,5.84E-01],
               [50.,3.05E-02,6.16E-01,6.47E-01],
               [60.,1.27E-03,6.66E-01,6.67E-01],
               [70.,-4.79E-05,6.44E-01,6.44E-01],
               [80.,6.85E-05,5.79E-01,5.79E-01],
               [90.,1.12E-04,4.70E-01,4.70E-01],
               [100.,1.12E-04,3.37E-01,3.37E-01],
               [110.,8.95E-04,2.08E-01,2.09E-01],
               [120.,6.07E-03,1.05E-01,1.11E-01],
               [130.,2.29E-03,3.89E-02,4.12E-02],
               [140.,5.52E-04,7.92E-03,8.47E-03],
               [150.,3.06E-04,1.65E-04,4.71E-04]])
    BEMdata = {}
    BEMdata['G0'] = G0
    BEMdata['normGs'] = normGs
    return BEMdata

def provideMatrixProperties():
    props = {}
    props['E'] = 3500.0
    props['nu'] = 0.4
    props['G'] = 0.5*props['E']/(1+props['nu'])
    props['k-planestrain'] = 3-4*props['nu']
    return props

def provideGFiberProperties():
    props = {}
    props['E'] = 70000.0
    props['nu'] = 0.2
    props['G'] = 0.5*props['E']/(1+props['nu'])
    props['k-planestrain'] = 3-4*props['nu']
    return props

def computePlyTransverseModulus(Vff,Ef,Em):
    return (Vff/Ef + (1.0-Vff)/Em)

def main(argv):
    # Read the command line, throw error if not option is provided
    try:
        opts, args = getopt.getopt(argv,'hw:i:o:f:e:l:d:',['help','Help',"workdir", "workdirectory", "wdir","inputfile", "input","out","outdir","outputfile","xlsx","outfile","excel","latex","sql"])
    except getopt.GetoptError:
        print('reportDataToXlsx.py -w <working directory> -i <input file> -o <output directory> -f <output filename> --excel --latex --sql')
        sys.exit(2)
    # Parse the options and create corresponding variables
    for opt, arg in opts:
        if opt in ('-h', '--help','--Help'):
            print(' ')
            print(' ')
            print('*****************************************************************************************************')
            print(' ')
            print('                                GATHER DATA AND CREATE REPORTS\n')
            print(' ')
            print('                                              by')
            print(' ')
            print('                                    Luca Di Stasio, 2016-2018')
            print(' ')
            print(' ')
            print('*****************************************************************************************************')
            print(' ')
            print('Program syntax:')
            print('reportDataToXlsx.py -w <working directory> -i <input file> -o <output directory> -f <output filename> --excel --latex --sql')
            print(' ')
            print('Mandatory arguments:')
            print('-w <working directory>')
            print('-i <input file>')
            print('at least one out of: -e --excel/-l --latex/-d --sql')
            print(' ')
            print('Optional arguments:')
            print('-o <output directory>')
            print('-f <output filename>')
            print(' ')
            print('Default values:')
            print('-o <output directory>                ===> working directory')
            print('-f <output filename>                 ===> Y-m-d_H-M-S_<input file name>.xlsx')
            print(' ')
            print(' ')
            print(' ')
            sys.exit()
        elif opt in ("-w", "--workdir", "--workdirectory", "--wdir"):
            if arg[-1] != '/':
                workdir = arg
            else:
                workdir = arg[:-1]
        elif opt in ("-i", "--inputfile", "--input"):
            inputfile = arg.split(".")[0] + '.csv'
        elif opt in ("-o", "--out","--outdir"):
            if arg[-1] != '/':
                outdir = arg
            else:
                outdir = arg[:-1]
        elif opt in ("-f", "--outputfile","--xlsx","--outfile"):
            outputfileBasename = arg.split(".")[0]
        elif opt in ("-e", "--excel"):
            toExcel = True
        elif opt in ("-l", "--latex"):
            toLatex = True
        elif opt in ("-d", "--sql"):
            toSql = True

    # Check the existence of variables: if a required variable is missing, an error is thrown and program is terminated; if an optional variable is missing, it is set to the default value
    if 'workdir' not in locals():
        print('Error: working directory not provided.')
        sys.exit()
    if 'inputfile' not in locals():
        print('Error: file list not provided.')
        sys.exit()
    if 'outputfileBasename' not in locals():
        outputfileBasename = datetime.now().strftime('%Y-%m-%d') + '_' + datetime.now().strftime('%H-%M-%S') + '_' + inputfile.split(".")[0]
    if 'outdir' not in locals():
        outdir = workdir
    if 'toExcel' not in locals() and 'toLatex' not in locals() and 'toSql' not in locals():
        print('Error: no output format specified.')
        sys.exit()
    if 'toExcel' not in locals():
        toExcel = False
    if 'toLatex' not in locals():
        toLatex = False
    if 'toSql' not in locals():
        toSql = False

    bemData = provideBEMdata()

    print('Reading file ' + join(workdir,inputfile) + ' ...')
    try:
        with open(join(workdir,inputfile),'r') as csv:
            lines = csv.readlines()
        print('    Number of lines: ' + str(len(lines)))
        print('...done.')
    except Exception,error:
        print('EXCEPTION ENCOUNTERED')
        print(str(Exception))
        print(str(error))
        sys.exit(2)

    print('Extracting names of subfolders ...')
    try:
        subfoldersList = []
        for l,line in enumerate(lines[1:]):
            currentSubfolder = '/'.join(line.replace('\n','').split(',')[0].replace('\\','/').split('/')[:-1])
            if currentSubfolder != workdir:
                if (len(subfoldersList)>0 and currentSubfolder != subfoldersList[-1]) or len(subfoldersList)==0:
                    print('  ' + '-- ' + str(currentSubfolder))
                    subfoldersList.append(currentSubfolder)
        print('...done.')
    except Exception,error:
        print('EXCEPTION ENCOUNTERED')
        print(str(Exception))
        print(str(error))
        sys.exit(2)

    print('Check if .dat files are present ...')
    try:
        isDatPresent = False
        for fileName in listdir(subfoldersList[0]):
            if '.dat'in fileName:
                isDatPresent = True
                print('    .dat files are present,')
                print('    analysis of path data needs to be performed')
                break
        if not isDatPresent:
            print('    .dat files are not present.')
        print('...done.')
    except Exception,error:
        print('EXCEPTION ENCOUNTERED')
        print(str(Exception))
        print(str(error))
        sys.exit(2)

    if toExcel:

        print('Open workbook ' + join(outdir,outputfileBasename + '.xlsx'))
        workbook = xlsxwriter.Workbook(join(outdir,outputfileBasename + '.xlsx'),{'nan_inf_to_errors': True})

        print('Set string and number format')
        stringFormat = workbook.add_format({'bold': 1})
        numberFormat = workbook.add_format({'num_format': '0.000000'})

        bemdataSheetname = 'BEM-Data'
        print('Create sheet for BEM data: ' + bemdataSheetname )
        worksheet = workbook.add_worksheet(bemdataSheetname)
        print('Fill in values of BEM data...')
        worksheet.write(0,0,'deltatheta [deg]',stringFormat)
        worksheet.write(0,1,'GI/G0 [-]',stringFormat)
        worksheet.write(0,2,'GII/G0 [-]',stringFormat)
        worksheet.write(0,3,'GTOT/G0 [-]',stringFormat)
        for r,row in enumerate(bemData['normGs']):
            for c,value in enumerate(row):
                worksheet.write(r+1,c,value,numberFormat)
        print('...done.')

        print('Creating sheets for results ...')
        for line in lines[1:]:
            csvPath = line.replace('\n','').split(',')[0]
            try:
                with open(csvPath,'r') as csv:
                    csvlines = csv.readlines()
            except Exception,error:
                continue
                sys.exc_clear()
            sheetName = line.replace('\n','').split(',')[1].replace('deltatheta','')
            print('    Create sheet ' + sheetName)
            toPlot = bool(line.replace('\n','').split(',')[2])
            plotSettings = []
            if toPlot:
                settingsString = ','.join(line.replace('\n','').split(',')[3:])
                plotSettings = ast.literal_eval(settingsString[1:])
            worksheet = workbook.add_worksheet(sheetName.decode('utf-8'))
            for e,element in enumerate(csvlines[0].replace('\n','').split(',')):
                worksheet.write(0,e,element,stringFormat)
            for c,csvline in enumerate(csvlines[1:]):
                for e,element in enumerate(csvline.replace('\n','').split(',')):
                    try:
                        if 'phiCZ' in csvlines[0][e]:
                            worksheet.write(c+1,e,float(element)*180.0/np.pi,numberFormat)
                        else:
                            worksheet.write(c+1,e,float(element),numberFormat)
                    except Exception,error:
                        worksheet.write(c+1,e,str(element).decode('utf-8'),numberFormat)
                        sys.exc_clear()
            for p,plot in enumerate(plotSettings):
                print('        Create plot ' + plot[-1] + ' in sheet ' + sheetName)
                chart = workbook.add_chart({'type': 'scatter',
                                            'subtype': 'smooth_with_markers'})
                isGIinplot = False
                isGIIinplot = False
                isGTOTinplot = False
                for curve in plot[:-3]:
                    if 'GI' in csvlines[0][curve[1]]:
                        isGIinplot = True
                    elif 'GII' in csvlines[0][curve[1]]:
                        isGIIinplot = True
                    elif 'GTOT' in csvlines[0][curve[1]]:
                        isGTOTinplot = True
                    chart.add_series({
                                        'name':       curve[2].decode('utf-8'),
                                        'categories': [sheetName,1,curve[0],len(csvlines),curve[0]],
                                        'values':     [sheetName,1,curve[1],len(csvlines),curve[1]],
                                    })
                if isGIinplot:
                    chart.add_series({
                                        'name':       'GI-BEM',
                                        'categories': [bemdataSheetname,1,0,15,0],
                                        'values':     [bemdataSheetname,1,1,15,1],
                                    })
                if isGIIinplot:
                    chart.add_series({
                                        'name':       'GII-BEM',
                                        'categories': [bemdataSheetname,1,0,15,0],
                                        'values':     [bemdataSheetname,1,2,15,2],
                                    })
                if isGTOTinplot:
                    chart.add_series({
                                        'name':       'GTOT-BEM',
                                        'categories': [bemdataSheetname,1,0,15,0],
                                        'values':     [bemdataSheetname,1,3,15,3],
                                    })
                chart.set_title ({'name': plot[-1].decode('utf-8')})
                chart.set_x_axis({'name': plot[-3].decode('utf-8')})
                chart.set_y_axis({'name': plot[-2].decode('utf-8')})
                worksheet.insert_chart(len(csvlines)+10,10*p, chart)
        print('...done.')
        workbook.close()
        print('Workbook closed.')

        if isDatPresent:
            print('Analysis of path data ...')
            print(' ')
            print('----------------->')
            print('    Open workbook ' + join(outdir,outputfileBasename + '-radialpathsData' + '.xlsx'))
            radialpathsWorkbook = xlsxwriter.Workbook(join(outdir,outputfileBasename + '-radialpathsData' + '.xlsx'),{'nan_inf_to_errors': True})
            print('    Set string and number format')
            radialpathsstringFormat = radialpathsWorkbook.add_format({'bold': 1})
            radialpathsnumberFormat = radialpathsWorkbook.add_format({'num_format': '0.000000'})
            radialpathsnumberFormatReduced = radialpathsWorkbook.add_format({'num_format': '0.00'})
            print(' ')
            print('    Open workbook ' + join(outdir,outputfileBasename + '-circumferentialpathsData' + '.xlsx'))
            circumferentialpathsWorkbook = xlsxwriter.Workbook(join(outdir,outputfileBasename + '-circumferentialpathsData' + '.xlsx'),{'nan_inf_to_errors': True})
            print('    Set string and number format')
            circumferentialpathsstringFormat = circumferentialpathsWorkbook.add_format({'bold': 1})
            circumferentialpathsnumberFormat = circumferentialpathsWorkbook.add_format({'num_format': '0.000000'})
            circumferentialpathsnumberFormatReduced = radialpathsWorkbook.add_format({'num_format': '0.00'})
            print(' ')
            print('    Open workbook ' + join(outdir,outputfileBasename + '-horizontalpathsData' + '.xlsx'))
            horizontalpathsWorkbook = xlsxwriter.Workbook(join(outdir,outputfileBasename + '-horizontalpathsData' + '.xlsx'),{'nan_inf_to_errors': True})
            print('    Set string and number format')
            horizontalpathsstringFormat = horizontalpathsWorkbook.add_format({'bold': 1})
            horizontalpathsnumberFormat = horizontalpathsWorkbook.add_format({'num_format': '0.000000'})
            horizontalpathsnumberFormatReduced = radialpathsWorkbook.add_format({'num_format': '0.00'})
            print(' ')
            print('    Open workbook ' + join(outdir,outputfileBasename + '-verticalpathsData' + '.xlsx'))
            verticalpathsWorkbook = xlsxwriter.Workbook(join(outdir,outputfileBasename + '-verticalpathsData' + '.xlsx'),{'nan_inf_to_errors': True})
            print('    Set string and number format')
            verticalpathsstringFormat = verticalpathsWorkbook.add_format({'bold': 1})
            verticalpathsnumberFormat = verticalpathsWorkbook.add_format({'num_format': '0.000000'})
            verticalpathsnumberFormatReduced = radialpathsWorkbook.add_format({'num_format': '0.00'})
            print('    Open workbook ' + join(outdir,outputfileBasename + '-radialpathsStrainData' + '.xlsx'))
            radialpathsStrainWorkbook = xlsxwriter.Workbook(join(outdir,outputfileBasename + '-radialpathsStrainData' + '.xlsx'),{'nan_inf_to_errors': True})
            print('    Set string and number format')
            radialpathsStrainstringFormat = radialpathsStrainWorkbook.add_format({'bold': 1})
            radialpathsStrainnumberFormat = radialpathsStrainWorkbook.add_format({'num_format': '0.000000'})
            radialpathsStrainnumberFormatReduced = radialpathsStrainWorkbook.add_format({'num_format': '0.00'})
            print(' ')
            print('    Open workbook ' + join(outdir,outputfileBasename + '-circumferentialpathsStrainData' + '.xlsx'))
            circumferentialpathsStrainWorkbook = xlsxwriter.Workbook(join(outdir,outputfileBasename + '-circumferentialpathsStrainData' + '.xlsx'),{'nan_inf_to_errors': True})
            print('    Set string and number format')
            circumferentialpathsStrainstringFormat = circumferentialpathsStrainWorkbook.add_format({'bold': 1})
            circumferentialpathsStrainnumberFormat = circumferentialpathsStrainWorkbook.add_format({'num_format': '0.000000'})
            circumferentialpathsStrainnumberFormatReduced = radialpathsStrainWorkbook.add_format({'num_format': '0.00'})
            print(' ')
            print('    Open workbook ' + join(outdir,outputfileBasename + '-horizontalpathsStrainData' + '.xlsx'))
            horizontalpathsStrainWorkbook = xlsxwriter.Workbook(join(outdir,outputfileBasename + '-horizontalpathsStrainData' + '.xlsx'),{'nan_inf_to_errors': True})
            print('    Set string and number format')
            horizontalpathsStrainstringFormat = horizontalpathsStrainWorkbook.add_format({'bold': 1})
            horizontalpathsStrainnumberFormat = horizontalpathsStrainWorkbook.add_format({'num_format': '0.000000'})
            horizontalpathsStrainnumberFormatReduced = radialpathsStrainWorkbook.add_format({'num_format': '0.00'})
            print(' ')
            print('    Open workbook ' + join(outdir,outputfileBasename + '-verticalpathsStrainData' + '.xlsx'))
            verticalpathsStrainWorkbook = xlsxwriter.Workbook(join(outdir,outputfileBasename + '-verticalpathsStrainData' + '.xlsx'),{'nan_inf_to_errors': True})
            print('    Set string and number format')
            verticalpathsStrainstringFormat = verticalpathsStrainWorkbook.add_format({'bold': 1})
            verticalpathsStrainnumberFormat = verticalpathsStrainWorkbook.add_format({'num_format': '0.000000'})
            verticalpathsStrainnumberFormatReduced = radialpathsStrainWorkbook.add_format({'num_format': '0.00'})
            print('<-----------------')
            print(' ')
            radialpathsSheetnames = []
            radialpathsStrainSheetnames = []
            numberOfRadialpaths = []
            numberOfRadialpathsStrain = []
            radialpathsDatalengths = []
            radialpathsStrainDatalengths = []
            circumferentialpathsSheetnames = []
            circumferentialpathsStrainSheetnames = []
            numberOfCircumferentialpaths = []
            circumferentialpathsDatalengths = []
            circumferentialpathsStrainDatalengths = []
            horizontalpathsSheetnames = []
            horizontalpathsStrainSheetnames = []
            numberOfHorizontalpaths = []
            horizontalpathsDatalengths = []
            horizontalpathsStrainDatalengths = []
            verticalpathsSheetnames = []
            verticalpathsStrainSheetnames = []
            numberOfVerticalpaths = []
            verticalpathsDatalengths = []
            verticalpathsStrainDatalengths = []

            for subFolder in subfoldersList:
                radialpathsSummary = join(subFolder,subFolder.split('/')[-1] + '-stressesradialpaths' + '.csv')
                circumferentialpathsSummary = join(subFolder,subFolder.split('/')[-1] + '-stressescircumferentialpaths' + '.csv')
                horizontalpathsSummary = join(subFolder,subFolder.split('/')[-1] + '-stresseshorizontalpaths' + '.csv')
                verticalpathsSummary = join(subFolder,subFolder.split('/')[-1] + '-stressesverticalpaths' + '.csv')
                radialpathsStrainSummary = join(subFolder,subFolder.split('/')[-1] + '-strainsradialpaths' + '.csv')
                circumferentialpathsStrainSummary = join(subFolder,subFolder.split('/')[-1] + '-strainscircumferentialpaths' + '.csv')
                horizontalpathsStrainSummary = join(subFolder,subFolder.split('/')[-1] + '-strainshorizontalpaths' + '.csv')
                verticalpathsStrainSummary = join(subFolder,subFolder.split('/')[-1] + '-strainsverticalpaths' + '.csv')

                if subFolder.split('/')[-1] + '-stressesradialpaths' + '.csv' in listdir(subFolder):
                    print('----------------->')
                    print('----------------->')
                    print('    Analysis of radial paths for folder ' + subFolder)
                    print(' ')
                    with open(radialpathsSummary,'r') as csv:
                        lines = csv.readlines()
                    Sxx = []
                    Syy = []
                    Szz = []
                    Sxy = []
                    Szx = []
                    Syz = []
                    Srr = []
                    Stt = []
                    Srt = []
                    S1D3 = []
                    S2D3 = []
                    S3D3 = []
                    I1D3 = []
                    I2D3 = []
                    I3D3 = []
                    SMisesD3 = []
                    SaverD3 = []
                    S1D2 = []
                    S2D2 = []
                    I1D2 = []
                    I2D2 = []
                    SMisesD2 = []
                    SaverD2 = []
                    pathVariables = []
                    pathStartVariables = []
                    pathEndVariables = []
                    pathCoords = []
                    pathNormCoords = []

                    for line in lines[1:]:
                        stressComp = line.replace('\n','').replace(' ','').split(',')[0]
                        pathVariable = float(line.replace('\n','').replace(' ','').split(',')[1])
                        pathStartVariable = float(line.replace('\n','').replace(' ','').split(',')[2])
                        pathEndVariable = float(line.replace('\n','').replace(' ','').split(',')[3])
                        datfilePath = join(subFolder,line.replace('\n','').replace(' ','').split(',')[-1])
                        print('    Reading component ' + stressComp)
                        print('            ' + 'for radial path at ' + str(pathVariable) + ' deg')
                        print('            ' + 'starting at ' + str(pathStartVariable) + ' mum')
                        print('            ' + 'ending at ' + str(pathEndVariable))
                        print(' ')
                        with open(datfilePath,'r') as dat:
                            datLines = dat.readlines()
                        print('    --> File read')
                        print(' ')
                        currentxyData = []
                        for datLine in datLines:
                            if len(datLine.replace('\n','').replace(' ',''))>0 and 'X' not in datLine:
                                lineParts = datLine.replace('\n','').split(' ')
                                rowVec = []
                                for linePart in lineParts:
                                    if linePart!='':
                                        rowVec.append(float(linePart))
                                currentxyData.append(rowVec)
                        print('    --> Lines parsed')
                        print(' ')
                        normxData = []
                        xData = []
                        yData = []
                        for xyPair in currentxyData:
                            normxData.append(xyPair[0])
                            xData.append(pathStartVariable+(pathEndVariable-pathStartVariable)*xyPair[0])
                            yData.append(xyPair[1])
                        print('    --> Data categorized in independent and dependent variables.')
                        print(' ')
                        if 'S11' in stressComp:
                            Sxx.append(yData)
                            pathCoords.append(xData)
                            pathNormCoords.append(normxData)
                            pathVariables.append(pathVariable)
                            pathStartVariables.append(pathStartVariable)
                            pathEndVariables.append(pathEndVariable)
                            print('    --> Stress component is S11.')
                            print(' ')
                        elif 'S22' in stressComp:
                            Syy.append(yData)
                            print('    --> Stress component is S22.')
                            print(' ')
                        elif 'S23' in stressComp:
                            Syz.append(yData)
                            print('    --> Stress component is S23.')
                            print(' ')
                        elif 'S12' in stressComp:
                            Sxy.append(yData)
                            print('    --> Stress component is S12.')
                            print(' ')
                        elif 'S13' in stressComp:
                            Szx.append(yData)
                            print('    --> Stress component is S13.')
                            print(' ')
                        elif 'S33' in stressComp:
                            Szz.append(yData)
                            Szx.append(0.0)
                            Syz.append(0.0)
                            print('    --> Stress component is S33.')
                            print(' ')
                            currentSxx = Sxx[-1]
                            currentSyy = Syy[-1]
                            currentSzz = yData
                            currentSxy = Sxy[-1]
                            currentSzx = 0.0
                            currentSyz = 0.0
                            currentSrr = []
                            currentStt = []
                            currentSrt = []
                            current3DS1 = []
                            current3DS2 = []
                            current3DS3 = []
                            current3DI1 = []
                            current3DI2 = []
                            current3DI3 = []
                            current3DSMises = []
                            current3DSaver = []
                            current2DS1 = []
                            current2DS2 = []
                            current2DI1 = []
                            current2DI2 = []
                            current2DSMises = []
                            current2DSaver = []
                            rotateBy = pathVariable*np.pi/180.0
                            cosRot = np.cos(rotateBy)
                            sinRot = np.sin(rotateBy)
                            nstressPoints = np.min([len(currentSxx),len(currentSyy),len(currentSzz),len(currentSxy)])
                            for s in range(0,nstressPoints):
                                sxx = currentSxx[s]
                                syy = currentSyy[s]
                                szz = currentSzz[s]
                                sxy = currentSxy[s]
                                szx = 0.0
                                syz = 0.0
                                srr = sxx*cosRot*cosRot+syy*sinRot*sinRot+2*sxy*cosRot*sinRot
                                stt = sxx*sinRot*sinRot+syy*cosRot*cosRot-2*sxy*cosRot*sinRot
                                srt = -sxx*cosRot*sinRot+syy*cosRot*sinRot+sxy*(cosRot*cosRot-sinRot*sinRot)
                                currentSrr.append(srr)
                                currentStt.append(stt)
                                currentSrt.append(srt)
                                i1d2 = sxx + syy
                                i1d3 = sxx + syy + szz
                                i2d2 = sxx*syy - sxy*sxy
                                i2d3 = sxx*syy + syy*szz + sxx*szz - sxy*sxy - syz*syz - szx*szx
                                i3d3 = sxx*syy*szz - sxx*syz*syz - syy*szx*szx - szz*sxy*sxy + 2*sxy*syz*szx
                                saverd2 = i1d2/2.0
                                saverd3 = i1d3/3.0
                                smises2d =  np.sqrt(sxx*sxx + syy*syy - sxx*syy + 3*sxy*sxy)
                                smises3d =  np.sqrt(sxx*sxx + syy*syy + szz*szz - sxx*syy - syy*szz - sxx*szz + 3*(sxy*sxy + syz*syz + szx*szx))
                                s1d2 = 0.5*(sxx+syy)+np.sqrt((0.5*(sxx-syy))*(0.5*(sxx-syy))+sxy*sxy)
                                s2d2 = 0.5*(sxx+syy)-np.sqrt((0.5*(sxx-syy))*(0.5*(sxx-syy))+sxy*sxy)
                                try:
                                    princOrient = np.arccos((2*i1d3*i1d3*i1d3-9*i1d3*i2d3+27*i3d3)/(2*np.sqrt((i1d3*i1d3-3*i2d3)*(i1d3*i1d3-3*i2d3)*(i1d3*i1d3-3*i2d3))))/3.0
                                    s1d3 = i1d3/3.0 + 2*np.sqrt(i1d3*i1d3-3*i2d3)*np.cos(princOrient)/3.0
                                    s2d3 = i1d3/3.0 + 2*np.sqrt(i1d3*i1d3-3*i2d3)*np.cos(princOrient-2*np.pi/3.0)/3.0
                                    s3d3 = i1d3/3.0 + 2*np.sqrt(i1d3*i1d3-3*i2d3)*np.cos(princOrient-4*np.pi/3.0)/3.0
                                except Exception:
                                    s1d3 = s1d2
                                    s2d3 = s2d2
                                    s3d3 = 0.0
                                current3DS1.append(s1d3)
                                current3DS2.append(s2d3)
                                current3DS3.append(s2d3)
                                current3DI1.append(i1d3)
                                current3DI2.append(i2d3)
                                current3DI3.append(i3d3)
                                current3DSMises.append(smises3d)
                                current3DSaver.append(saverd3)
                                current2DS1.append(s1d2)
                                current2DS2.append(s2d2)
                                current2DI1.append(i1d2)
                                current2DI2.append(i2d2)
                                current2DSMises.append(smises2d)
                                current2DSaver.append(saverd2)
                            Srr.append(currentSrr)
                            Stt.append(currentStt)
                            Srt.append(currentSrt)
                            S1D3.append(current3DS1)
                            S2D3.append(current3DS2)
                            S3D3.append(current3DS3)
                            S1D2.append(current2DS1)
                            S2D2.append(current2DS2)
                            I1D3.append(current3DI1)
                            I2D3.append(current3DI2)
                            I3D3.append(current3DI3)
                            I1D2.append(current2DI1)
                            I2D2.append(current2DI2)
                            SMisesD3.append(current3DSMises)
                            SaverD3.append(current3DSaver)
                            SMisesD2.append(current2DSMises)
                            SaverD2.append(current2DSaver)
                            currentSrr = []
                            currentStt = []
                            currentSrt = []
                            current3DS1 = []
                            current3DS2 = []
                            current3DS3 = []
                            current3DI1 = []
                            current3DI2 = []
                            current3DI3 = []
                            current3DSMises = []
                            current3DSaver = []
                            current2DS1 = []
                            current2DS2 = []
                            current2DI1 = []
                            current2DI2 = []
                            current2DSMises = []
                            current2DSaver = []

                    pathVariableName = 'pathAngle [deg]'
                    pathStartVariableName = 'Ri [mum]'
                    pathEndVariableName = 'Rf [mum]'
                    pathCoordinateName = 'R [mum]'
                    datasheetName = 'Values, deltatheta=' + subFolder.split('deltatheta')[-1].replace('_','.')
                    radialpathsSheetnames.append(datasheetName)
                    numberOfRadialpaths.append(len(pathVariables))
                    worksheet = radialpathsWorkbook.add_worksheet(datasheetName.decode('utf-8'))
                    print('    --> Writing worksheet')
                    print('        ' + datasheetName)
                    print(' ')
                    for p, pathVariable in enumerate(pathVariables):
                        print('          pathAngle = ' + str(pathVariable) + ' deg')
                        worksheet.write(0,p*25,pathVariableName,radialpathsstringFormat)
                        worksheet.write(1,p*25,pathVariable,radialpathsnumberFormatReduced)
                        worksheet.write(0,p*25+1,pathStartVariableName,radialpathsstringFormat)
                        worksheet.write(1,p*25+1,pathStartVariables[p],radialpathsnumberFormat)
                        worksheet.write(0,p*25+2,pathEndVariableName,radialpathsstringFormat)
                        worksheet.write(1,p*25+2,pathEndVariables[p],radialpathsnumberFormat)
                        worksheet.write(2,p*25,pathCoordinateName,radialpathsstringFormat)
                        worksheet.write(2,p*25+1,'Norm ' + pathCoordinateName,radialpathsstringFormat)
                        worksheet.write(2,p*25+2,'Sxx [MPa]',radialpathsstringFormat)
                        worksheet.write(2,p*25+3,'Syy [MPa]',radialpathsstringFormat)
                        worksheet.write(2,p*25+4,'Szz [MPa]',radialpathsstringFormat)
                        worksheet.write(2,p*25+5,'Sxy [MPa]',radialpathsstringFormat)
                        worksheet.write(2,p*25+6,'Szx [MPa]',radialpathsstringFormat)
                        worksheet.write(2,p*25+7,'Syz [MPa]',radialpathsstringFormat)
                        worksheet.write(2,p*25+8,'Srr [MPa]',radialpathsstringFormat)
                        worksheet.write(2,p*25+9,'Stt [MPa]',radialpathsstringFormat)
                        worksheet.write(2,p*25+10,'Srt [MPa]',radialpathsstringFormat)
                        worksheet.write(2,p*25+11,'S1_3D [MPa]',radialpathsstringFormat)
                        worksheet.write(2,p*25+12,'S2_3D [MPa]',radialpathsstringFormat)
                        worksheet.write(2,p*25+13,'S3_3D [MPa]',radialpathsstringFormat)
                        worksheet.write(2,p*25+14,'S1_2D [MPa]',radialpathsstringFormat)
                        worksheet.write(2,p*25+15,'S2_2D [MPa]',radialpathsstringFormat)
                        worksheet.write(2,p*25+16,'Smises_3D [MPa]',radialpathsstringFormat)
                        worksheet.write(2,p*25+17,'Smises_2D [MPa]',radialpathsstringFormat)
                        worksheet.write(2,p*25+18,'Saverage_3D [MPa]',radialpathsstringFormat)
                        worksheet.write(2,p*25+19,'Saverage_2D [MPa]',radialpathsstringFormat)
                        worksheet.write(2,p*25+20,'I1_3D [MPa]',radialpathsstringFormat)
                        worksheet.write(2,p*25+21,'I2_3D [MPa^2]',radialpathsstringFormat)
                        worksheet.write(2,p*25+22,'I3_3D [MPa^3]',radialpathsstringFormat)
                        worksheet.write(2,p*25+23,'I1_2D [MPa]',radialpathsstringFormat)
                        worksheet.write(2,p*25+24,'I2_2D [MPa^2]',radialpathsstringFormat)
                        measureNum = np.min([len(Sxx[p]),len(Syy[p]),len(Szz[p]),len(Sxy[p])])
                        print('          number of path points = ' + str(measureNum))
                        for c in range(0,measureNum):
                            coord = pathCoords[p][c]
                            worksheet.write(3+c,p*25,coord,radialpathsnumberFormat)
                            worksheet.write(3+c,p*25+1,pathNormCoords[p][c],radialpathsnumberFormat)
                            worksheet.write(3+c,p*25+2,Sxx[p][c],radialpathsnumberFormat)
                            worksheet.write(3+c,p*25+3,Syy[p][c],radialpathsnumberFormat)
                            worksheet.write(3+c,p*25+4,Szz[p][c],radialpathsnumberFormat)
                            worksheet.write(3+c,p*25+5,Sxy[p][c],radialpathsnumberFormat)
                            worksheet.write(3+c,p*25+6,0.0,radialpathsnumberFormat)
                            worksheet.write(3+c,p*25+7,0.0,radialpathsnumberFormat)
                            worksheet.write(3+c,p*25+8,Srr[p][c],radialpathsnumberFormat)
                            worksheet.write(3+c,p*25+9,Stt[p][c],radialpathsnumberFormat)
                            worksheet.write(3+c,p*25+10,Srt[p][c],radialpathsnumberFormat)
                            worksheet.write(3+c,p*25+11,S1D3[p][c],radialpathsnumberFormat)
                            worksheet.write(3+c,p*25+12,S2D3[p][c],radialpathsnumberFormat)
                            worksheet.write(3+c,p*25+13,S3D3[p][c],radialpathsnumberFormat)
                            worksheet.write(3+c,p*25+14,S1D2[p][c],radialpathsnumberFormat)
                            worksheet.write(3+c,p*25+15,S2D2[p][c],radialpathsnumberFormat)
                            worksheet.write(3+c,p*25+16,SMisesD3[p][c],radialpathsnumberFormat)
                            worksheet.write(3+c,p*25+17,SMisesD2[p][c],radialpathsnumberFormat)
                            worksheet.write(3+c,p*25+18,SaverD3[p][c],radialpathsnumberFormat)
                            worksheet.write(3+c,p*25+19,SaverD2[p][c],radialpathsnumberFormat)
                            worksheet.write(3+c,p*25+20,I1D3[p][c],radialpathsnumberFormat)
                            worksheet.write(3+c,p*25+21,I2D3[p][c],radialpathsnumberFormat)
                            worksheet.write(3+c,p*25+22,I3D3[p][c],radialpathsnumberFormat)
                            worksheet.write(3+c,p*25+23,I1D2[p][c],radialpathsnumberFormat)
                            worksheet.write(3+c,p*25+24,I2D2[p][c],radialpathsnumberFormat)

                    graphsheetName = 'Graphs, deltatheta=' + subFolder.split('deltatheta')[-1].replace('_','.')
                    graphworksheet = radialpathsWorkbook.add_worksheet(graphsheetName.decode('utf-8'))
                    print('    --> Writing worksheet')
                    print('        ' + graphsheetName)
                    print(' ')
                    variableNames = ['Sxx [MPa]','Syy [MPa]','Szz [MPa]','Sxy [MPa]','Szx [MPa]','Syz [MPa]','Srr [MPa]','Stt [MPa]','Srt [MPa]','S1_3D [MPa]','S2_3D [MPa]','S3_3D [MPa]','S1_2D [MPa]','S2_2D [MPa]','Smises_3D [MPa]','Smises_2D [MPa]','Saver_3D [MPa]','Saver_2D [MPa]','I1_3D [MPa]','I2_3D [MPa^2]','I3_3D [MPa^3]','I1_2D [MPa]','I2_2D [MPa^2]']
                    for v,variableName in enumerate(variableNames):
                        chartA = radialpathsWorkbook.add_chart({'type': 'scatter','subtype': 'straight_with_markers'})
                        print('        Chart ' + str(v+1) + '.A')
                        print(' ')
                        for p, pathVariable in enumerate(pathVariables):
                            dataLength = len(pathCoords[p])
                            if v==0:
                                radialpathsDatalengths.append(dataLength)
                            chartA.add_series({
                                            'name':       pathVariableName + '=' + str(pathVariable),
                                            'categories': [datasheetName,3,25*p,dataLength,25*p],
                                            'values':     [datasheetName,3,25*p+2+v,dataLength,25*p+2+v],
                                             })
                            print('                  Series ' + str(p+1) + ': ' + pathVariableName + '=' + str(pathVariable))
                            print(' ')
                        chartA.set_title ({'name': variableName + ' vs path coordinates'})
                        chartA.set_x_axis({'name': pathCoordinateName})
                        chartA.set_y_axis({'name': variableName})
                        print('             Title: ' + variableName + ' vs path coordinates')
                        print('             x axis: ' + pathCoordinateName)
                        print('             y axis: ' + variableName)
                        print(' ')
                        print(' ')
                        graphworksheet.insert_chart(v*20,0,chartA)
                        chartB = radialpathsWorkbook.add_chart({'type': 'scatter','subtype': 'straight_with_markers'})
                        print('        Chart ' + str(v+1) + '.B')
                        print(' ')
                        for p, pathVariable in enumerate(pathVariables):
                            dataLength = len(pathCoords[p])
                            chartB.add_series({
                                            'name':       pathVariableName + '=' + str(pathVariable),
                                            'categories': [datasheetName,3,25*p+1,dataLength,25*p+1],
                                            'values':     [datasheetName,3,25*p+2+v,dataLength,25*p+2+v],
                                             })
                            print('                  Series ' + str(p+1) + ': ' + pathVariableName + '=' + str(pathVariable))
                            print(' ')
                        chartB.set_title ({'name': variableName + ' vs normalized path coordinates'})
                        chartB.set_x_axis({'name': 'Norm ' + pathCoordinateName.split(' ')[0] + ' [-]'})
                        chartB.set_y_axis({'name': variableName})
                        print('             Title: ' + variableName + ' vs path coordinates')
                        print('             x axis: ' + 'Norm ' + pathCoordinateName.split(' ')[0] + ' [-]')
                        print('             y axis: ' + variableName)
                        print(' ')
                        print(' ')
                        graphworksheet.insert_chart(v*20,30,chartB)

                    Sxx = []
                    Syy = []
                    Szz = []
                    Sxy = []
                    Szx = []
                    Syz = []
                    Srr = []
                    Stt = []
                    Srt = []
                    S1D3 = []
                    S2D3 = []
                    S3D3 = []
                    I1D3 = []
                    I2D3 = []
                    I3D3 = []
                    SMisesD3 = []
                    SaverD3 = []
                    S1D2 = []
                    S2D2 = []
                    I1D2 = []
                    I2D2 = []
                    SMisesD2 = []
                    SaverD2 = []
                    pathVariables = []
                    pathStartVariables = []
                    pathEndVariables = []
                    pathCoords = []
                    pathNormCoords = []
                    print('<-----------------')
                    print('<-----------------')

                if subFolder.split('/')[-1] + '-stressescircumferentialpaths' + '.csv' in listdir(subFolder):
                    print('    Analysis of circumferential paths for folder ' + subFolder)
                    print('    ')
                    with open(circumferentialpathsSummary,'r') as csv:
                        lines = csv.readlines()
                    Sxx = []
                    Syy = []
                    Szz = []
                    Sxy = []
                    Szx = []
                    Syz = []
                    Srr = []
                    Stt = []
                    Srt = []
                    S1D3 = []
                    S2D3 = []
                    S3D3 = []
                    I1D3 = []
                    I2D3 = []
                    I3D3 = []
                    SMisesD3 = []
                    SaverD3 = []
                    S1D2 = []
                    S2D2 = []
                    I1D2 = []
                    I2D2 = []
                    SMisesD2 = []
                    SaverD2 = []
                    pathVariables = []
                    pathStartVariables = []
                    pathEndVariables = []
                    pathCoords = []
                    pathNormCoords = []

                    for line in lines[1:]:
                        stressComp = line.replace('\n','').replace(' ','').split(',')[0]
                        pathVariable = float(line.replace('\n','').replace(' ','').split(',')[1])
                        pathStartVariable = float(line.replace('\n','').replace(' ','').split(',')[2])
                        pathEndVariable = float(line.replace('\n','').replace(' ','').split(',')[3])
                        datfilePath = join(subFolder,line.replace('\n','').replace(' ','').split(',')[-1])
                        print('    Reading component ' + stressComp)
                        print('            ' + 'for circumferential path at ' + str(pathVariable) + ' mum')
                        print('            ' + 'starting at ' + str(pathStartVariable) + ' deg')
                        print('            ' + 'ending at ' + str(pathEndVariable) + ' deg')
                        print(' ')
                        with open(datfilePath,'r') as dat:
                            datLines = dat.readlines()
                        currentxyData = []
                        for datLine in datLines:
                            if len(datLine.replace('\n','').replace(' ',''))>0 and 'X' not in datLine:
                                lineParts = datLine.replace('\n','').split(' ')
                                rowVec = []
                                for linePart in lineParts:
                                    if linePart!='':
                                        rowVec.append(float(linePart))
                                currentxyData.append(rowVec)
                        normxData = []
                        xData = []
                        yData = []
                        for xyPair in currentxyData:
                            normxData.append(xyPair[0])
                            xData.append(pathStartVariable+(pathEndVariable-pathStartVariable)*xyPair[0])
                            yData.append(xyPair[1])
                        if 'S11' in stressComp:
                            Sxx.append(yData)
                            pathCoords.append(xData)
                            pathNormCoords.append(normxData)
                            pathVariables.append(pathVariable)
                            pathStartVariables.append(pathStartVariable)
                            pathEndVariables.append(pathEndVariable)
                        elif 'S22' in stressComp:
                            Syy.append(yData)
                        elif 'S23' in stressComp:
                            Syz.append(yData)
                        elif 'S12' in stressComp:
                            Sxy.append(yData)
                        elif 'S13' in stressComp:
                            Szx.append(yData)
                        elif 'S33' in stressComp:
                            Szz.append(yData)
                            Szx.append(0.0)
                            Syz.append(0.0)
                            currentSxx = Sxx[-1]
                            currentSyy = Syy[-1]
                            currentSzz = yData
                            currentSxy = Sxy[-1]
                            currentSzx = 0.0
                            currentSyz = 0.0
                            currentSrr = []
                            currentStt = []
                            currentSrt = []
                            current3DS1 = []
                            current3DS2 = []
                            current3DS3 = []
                            current3DI1 = []
                            current3DI2 = []
                            current3DI3 = []
                            current3DSMises = []
                            current3DSaver = []
                            current2DS1 = []
                            current2DS2 = []
                            current2DI1 = []
                            current2DI2 = []
                            current2DSMises = []
                            current2DSaver = []
                            nstressPoints = np.min([len(currentSxx),len(currentSyy),len(currentSzz),len(currentSxy)])
                            for s in range(0,nstressPoints):
                                rotateBy = pathCoords[-1][s]*np.pi/180.0
                                cosRot = np.cos(rotateBy)
                                sinRot = np.sin(rotateBy)
                                sxx = currentSxx[s]
                                syy = currentSyy[s]
                                szz = currentSzz[s]
                                sxy = currentSxy[s]
                                szx = 0.0
                                syz = 0.0

                                srr = sxx*cosRot*cosRot+syy*sinRot*sinRot+2*sxy*cosRot*sinRot
                                stt = sxx*sinRot*sinRot+syy*cosRot*cosRot-2*sxy*cosRot*sinRot
                                srt = -sxx*cosRot*sinRot+syy*cosRot*sinRot+sxy*(cosRot*cosRot-sinRot*sinRot)
                                currentSrr.append(srr)
                                currentStt.append(stt)
                                currentSrt.append(srt)

                                i1d2 = sxx + syy
                                i1d3 = sxx + syy + szz

                                i2d2 = sxx*syy - sxy*sxy
                                i2d3 = sxx*syy + syy*szz + sxx*szz - sxy*sxy - syz*syz - szx*szx

                                i3d3 = sxx*syy*szz - sxx*syz*syz - syy*szx*szx - szz*sxy*sxy + 2*sxy*syz*szx

                                saverd2 = i1d2/2.0
                                saverd3 = i1d3/3.0

                                smises2d =  np.sqrt(sxx*sxx + syy*syy - sxx*syy + 3*sxy*sxy)
                                smises3d =  np.sqrt(sxx*sxx + syy*syy + szz*szz - sxx*syy - syy*szz - sxx*szz + 3*(sxy*sxy + syz*syz + szx*szx))

                                s1d2 = 0.5*(sxx+syy)+np.sqrt((0.5*(sxx-syy))*(0.5*(sxx-syy))+sxy*sxy)
                                s2d2 = 0.5*(sxx+syy)-np.sqrt((0.5*(sxx-syy))*(0.5*(sxx-syy))+sxy*sxy)

                                try:
                                    princOrient = np.arccos((2*i1d3*i1d3*i1d3-9*i1d3*i2d3+27*i3d3)/(2*np.sqrt((i1d3*i1d3-3*i2d3)*(i1d3*i1d3-3*i2d3)*(i1d3*i1d3-3*i2d3))))/3.0
                                    s1d3 = i1d3/3.0 + 2*np.sqrt(i1d3*i1d3-3*i2d3)*np.cos(princOrient)/3.0
                                    s2d3 = i1d3/3.0 + 2*np.sqrt(i1d3*i1d3-3*i2d3)*np.cos(princOrient-2*np.pi/3.0)/3.0
                                    s3d3 = i1d3/3.0 + 2*np.sqrt(i1d3*i1d3-3*i2d3)*np.cos(princOrient-4*np.pi/3.0)/3.0
                                except Exception:
                                    s1d3 = s1d2
                                    s2d3 = s2d2
                                    s3d3 = 0.0

                                current3DS1.append(s1d3)
                                current3DS2.append(s2d3)
                                current3DS3.append(s2d3)
                                current3DI1.append(i1d3)
                                current3DI2.append(i2d3)
                                current3DI3.append(i3d3)
                                current3DSMises.append(smises3d)
                                current3DSaver.append(saverd3)
                                current2DS1.append(s1d2)
                                current2DS2.append(s2d2)
                                current2DI1.append(i1d2)
                                current2DI2.append(i2d2)
                                current2DSMises.append(smises2d)
                                current2DSaver.append(saverd2)

                            Srr.append(currentSrr)
                            Stt.append(currentStt)
                            Srt.append(currentSrt)
                            S1D3.append(current3DS1)
                            S2D3.append(current3DS2)
                            S3D3.append(current3DS3)
                            S1D2.append(current2DS1)
                            S2D2.append(current2DS2)
                            I1D3.append(current3DI1)
                            I2D3.append(current3DI2)
                            I3D3.append(current3DI3)
                            I1D2.append(current2DI1)
                            I2D2.append(current2DI2)
                            SMisesD3.append(current3DSMises)
                            SaverD3.append(current3DSaver)
                            SMisesD2.append(current2DSMises)
                            SaverD2.append(current2DSaver)

                            currentSrr = []
                            currentStt = []
                            currentSrt = []
                            current3DS1 = []
                            current3DS2 = []
                            current3DS3 = []
                            current3DI1 = []
                            current3DI2 = []
                            current3DI3 = []
                            current3DSMises = []
                            current3DSaver = []
                            current2DS1 = []
                            current2DS2 = []
                            current2DI1 = []
                            current2DI2 = []
                            current2DSMises = []
                            current2DSaver = []

                    pathVariableName = 'pathRadius [mum]'
                    pathStartVariableName = 'startAngle [deg]'
                    pathEndVariableName = 'endAngle [deg]'
                    pathCoordinateName = 'angle [deg]'
                    datasheetName = 'Values, deltatheta=' + subFolder.split('deltatheta')[-1].replace('_','.')
                    circumferentialpathsSheetnames.append(datasheetName)
                    numberOfCircumferentialpaths.append(len(pathVariables))
                    worksheet = circumferentialpathsWorkbook.add_worksheet(datasheetName.decode('utf-8'))
                    for p, pathVariable in enumerate(pathVariables):
                        worksheet.write(0,p*25,pathVariableName,circumferentialpathsstringFormat)
                        worksheet.write(1,p*25,pathVariable,circumferentialpathsnumberFormatReduced)
                        worksheet.write(0,p*25+1,pathStartVariableName,circumferentialpathsstringFormat)
                        worksheet.write(1,p*25+1,pathStartVariables[p],circumferentialpathsnumberFormat)
                        worksheet.write(0,p*25+2,pathEndVariableName,circumferentialpathsstringFormat)
                        worksheet.write(1,p*25+2,pathEndVariables[p],circumferentialpathsnumberFormat)
                        worksheet.write(2,p*25,pathCoordinateName,circumferentialpathsstringFormat)
                        worksheet.write(2,p*25+1,'Norm ' + pathCoordinateName,circumferentialpathsstringFormat)
                        worksheet.write(2,p*25+2,'Sxx [MPa]',circumferentialpathsstringFormat)
                        worksheet.write(2,p*25+3,'Syy [MPa]',circumferentialpathsstringFormat)
                        worksheet.write(2,p*25+4,'Szz [MPa]',circumferentialpathsstringFormat)
                        worksheet.write(2,p*25+5,'Sxy [MPa]',circumferentialpathsstringFormat)
                        worksheet.write(2,p*25+6,'Szx [MPa]',circumferentialpathsstringFormat)
                        worksheet.write(2,p*25+7,'Syz [MPa]',circumferentialpathsstringFormat)
                        worksheet.write(2,p*25+8,'Srr [MPa]',circumferentialpathsstringFormat)
                        worksheet.write(2,p*25+9,'Stt [MPa]',circumferentialpathsstringFormat)
                        worksheet.write(2,p*25+10,'Srt [MPa]',circumferentialpathsstringFormat)
                        worksheet.write(2,p*25+11,'S1_3D [MPa]',circumferentialpathsstringFormat)
                        worksheet.write(2,p*25+12,'S2_3D [MPa]',circumferentialpathsstringFormat)
                        worksheet.write(2,p*25+13,'S3_3D [MPa]',circumferentialpathsstringFormat)
                        worksheet.write(2,p*25+14,'S1_2D [MPa]',circumferentialpathsstringFormat)
                        worksheet.write(2,p*25+15,'S2_2D [MPa]',circumferentialpathsstringFormat)
                        worksheet.write(2,p*25+16,'Smises_3D [MPa]',circumferentialpathsstringFormat)
                        worksheet.write(2,p*25+17,'Smises_2D [MPa]',circumferentialpathsstringFormat)
                        worksheet.write(2,p*25+18,'Saverage_3D [MPa]',circumferentialpathsstringFormat)
                        worksheet.write(2,p*25+19,'Saverage_2D [MPa]',circumferentialpathsstringFormat)
                        worksheet.write(2,p*25+20,'I1_3D [MPa]',circumferentialpathsstringFormat)
                        worksheet.write(2,p*25+21,'I2_3D [MPa^2]',circumferentialpathsstringFormat)
                        worksheet.write(2,p*25+22,'I3_3D [MPa^3]',circumferentialpathsstringFormat)
                        worksheet.write(2,p*25+23,'I1_2D [MPa]',circumferentialpathsstringFormat)
                        worksheet.write(2,p*25+24,'I2_2D [MPa^2]',circumferentialpathsstringFormat)
                        measureNum = np.min([len(Sxx[p]),len(Syy[p]),len(Szz[p]),len(Sxy[p])])
                        print('          number of path points = ' + str(measureNum))
                        for c in range(0,measureNum):
                            coord = pathCoords[p][c]
                            worksheet.write(3+c,p*25,coord,circumferentialpathsnumberFormat)
                            worksheet.write(3+c,p*25+1,pathNormCoords[p][c],circumferentialpathsnumberFormat)
                            worksheet.write(3+c,p*25+2,Sxx[p][c],circumferentialpathsnumberFormat)
                            worksheet.write(3+c,p*25+3,Syy[p][c],circumferentialpathsnumberFormat)
                            worksheet.write(3+c,p*25+4,Szz[p][c],circumferentialpathsnumberFormat)
                            worksheet.write(3+c,p*25+5,Sxy[p][c],circumferentialpathsnumberFormat)
                            worksheet.write(3+c,p*25+6,0.0,circumferentialpathsnumberFormat)
                            worksheet.write(3+c,p*25+7,0.0,circumferentialpathsnumberFormat)
                            worksheet.write(3+c,p*25+8,Srr[p][c],circumferentialpathsnumberFormat)
                            worksheet.write(3+c,p*25+9,Stt[p][c],circumferentialpathsnumberFormat)
                            worksheet.write(3+c,p*25+10,Srt[p][c],circumferentialpathsnumberFormat)
                            worksheet.write(3+c,p*25+11,S1D3[p][c],circumferentialpathsnumberFormat)
                            worksheet.write(3+c,p*25+12,S2D3[p][c],circumferentialpathsnumberFormat)
                            worksheet.write(3+c,p*25+13,S3D3[p][c],circumferentialpathsnumberFormat)
                            worksheet.write(3+c,p*25+14,S1D2[p][c],circumferentialpathsnumberFormat)
                            worksheet.write(3+c,p*25+15,S2D2[p][c],circumferentialpathsnumberFormat)
                            worksheet.write(3+c,p*25+16,SMisesD3[p][c],circumferentialpathsnumberFormat)
                            worksheet.write(3+c,p*25+17,SMisesD2[p][c],circumferentialpathsnumberFormat)
                            worksheet.write(3+c,p*25+18,SaverD3[p][c],circumferentialpathsnumberFormat)
                            worksheet.write(3+c,p*25+19,SaverD2[p][c],circumferentialpathsnumberFormat)
                            worksheet.write(3+c,p*25+20,I1D3[p][c],circumferentialpathsnumberFormat)
                            worksheet.write(3+c,p*25+21,I2D3[p][c],circumferentialpathsnumberFormat)
                            worksheet.write(3+c,p*25+22,I3D3[p][c],circumferentialpathsnumberFormat)
                            worksheet.write(3+c,p*25+23,I1D2[p][c],circumferentialpathsnumberFormat)
                            worksheet.write(3+c,p*25+24,I2D2[p][c],circumferentialpathsnumberFormat)

                    graphsheetName = 'Graphs, deltatheta=' + subFolder.split('deltatheta')[-1].replace('_','.')
                    graphworksheet = circumferentialpathsWorkbook.add_worksheet(graphsheetName.decode('utf-8'))
                    print('    --> Writing worksheet')
                    print('        ' + graphsheetName)
                    print(' ')
                    variableNames = ['Sxx [MPa]','Syy [MPa]','Szz [MPa]','Sxy [MPa]','Szx [MPa]','Syz [MPa]','Srr [MPa]','Stt [MPa]','Srt [MPa]','S1_3D [MPa]','S2_3D [MPa]','S3_3D [MPa]','S1_2D [MPa]','S2_2D [MPa]','Smises_3D [MPa]','Smises_2D [MPa]','Saverage_3D [MPa]','Saverage_2D [MPa]','I1_3D [MPa]','I2_3D [MPa^2]','I3_3D [MPa^3]','I1_2D [MPa]','I2_2D [MPa^2]']
                    circumferentialpathsDatalengths.append(len(pathCoords[p]))
                    for v,variableName in enumerate(variableNames):
                        chartA = circumferentialpathsWorkbook.add_chart({'type': 'scatter','subtype': 'straight_with_markers'})
                        print('        Chart ' + str(v+1) + '.A')
                        print(' ')
                        for p, pathVariable in enumerate(pathVariables):
                            dataLength = len(pathCoords[p])
                            if v==0:
                                circumferentialpathsDatalengths.append(dataLength)
                            chartA.add_series({
                                            'name':       pathVariableName + '=' + str(pathVariable),
                                            'categories': [datasheetName,3,25*p,dataLength,25*p],
                                            'values':     [datasheetName,3,25*p+2+v,dataLength,25*p+2+v],
                                             })
                            print('                  Series ' + str(p+1) + ': ' + pathVariableName + '=' + str(pathVariable))
                            print(' ')
                        chartA.set_title ({'name': variableName + ' vs path coordinates'})
                        chartA.set_x_axis({'name': pathCoordinateName})
                        chartA.set_y_axis({'name': variableName})
                        print('             Title: ' + variableName + ' vs path coordinates')
                        print('             x axis: ' + pathCoordinateName)
                        print('             y axis: ' + variableName)
                        print(' ')
                        print(' ')
                        graphworksheet.insert_chart(v*20,0,chartA)
                        chartB = circumferentialpathsWorkbook.add_chart({'type': 'scatter','subtype': 'straight_with_markers'})
                        print('        Chart ' + str(v+1) + '.B')
                        print(' ')
                        for p, pathVariable in enumerate(pathVariables):
                            dataLength = len(pathCoords[p])
                            chartB.add_series({
                                            'name':       pathVariableName + '=' + str(pathVariable),
                                            'categories': [datasheetName,3,25*p+1,dataLength,25*p+1],
                                            'values':     [datasheetName,3,25*p+2+v,dataLength,25*p+2+v],
                                             })
                            print('                  Series ' + str(p+1) + ': ' + pathVariableName + '=' + str(pathVariable))
                            print(' ')
                        chartB.set_title ({'name': variableName + ' vs normalized path coordinates'})
                        chartB.set_x_axis({'name': 'Norm ' + pathCoordinateName.split(' ')[0] + ' [-]'})
                        chartB.set_y_axis({'name': variableName})
                        print('             Title: ' + variableName + ' vs path coordinates')
                        print('             x axis: ' + 'Norm ' + pathCoordinateName.split(' ')[0] + ' [-]')
                        print('             y axis: ' + variableName)
                        print(' ')
                        print(' ')
                        graphworksheet.insert_chart(v*20,30,chartB)

                    Sxx = []
                    Syy = []
                    Szz = []
                    Sxy = []
                    Szx = []
                    Syz = []
                    Srr = []
                    Stt = []
                    Srt = []
                    S1D3 = []
                    S2D3 = []
                    S3D3 = []
                    I1D3 = []
                    I2D3 = []
                    I3D3 = []
                    SMisesD3 = []
                    SaverD3 = []
                    S1D2 = []
                    S2D2 = []
                    I1D2 = []
                    I2D2 = []
                    SMisesD2 = []
                    SaverD2 = []
                    pathVariables = []
                    pathStartVariables = []
                    pathEndVariables = []
                    pathCoords = []
                    pathNormCoords = []

                if subFolder.split('/')[-1] + '-stresseshorizontalpaths' + '.csv' in listdir(subFolder):
                    print('    Analysis of horizontal paths for folder ' + subFolder)
                    with open(horizontalpathsSummary,'r') as csv:
                        lines = csv.readlines()
                    Sxx = []
                    Syy = []
                    Szz = []
                    Sxy = []
                    Szx = []
                    Syz = []
                    Srr = []
                    Stt = []
                    Srt = []
                    S1D3 = []
                    S2D3 = []
                    S3D3 = []
                    I1D3 = []
                    I2D3 = []
                    I3D3 = []
                    SMisesD3 = []
                    SaverD3 = []
                    S1D2 = []
                    S2D2 = []
                    I1D2 = []
                    I2D2 = []
                    SMisesD2 = []
                    SaverD2 = []
                    pathVariables = []
                    pathStartVariables = []
                    pathEndVariables = []
                    pathCoords = []
                    pathNormCoords = []

                    for line in lines[1:]:
                        stressComp = line.replace('\n','').replace(' ','').split(',')[0]
                        pathVariable = float(line.replace('\n','').replace(' ','').split(',')[1])
                        pathStartVariable = float(line.replace('\n','').replace(' ','').split(',')[2])
                        pathEndVariable = float(line.replace('\n','').replace(' ','').split(',')[3])
                        datfilePath = join(subFolder,line.replace('\n','').replace(' ','').split(',')[-1])
                        print('    Reading component ' + stressComp)
                        print('            ' + 'for horizontal path at ' + str(pathVariable) + ' [mum]')
                        print('            ' + 'starting at ' + str(pathStartVariable) + ' mum')
                        print('            ' + 'ending at ' + str(pathEndVariable) + ' mum')
                        print(' ')
                        with open(datfilePath,'r') as dat:
                            datLines = dat.readlines()
                        currentxyData = []
                        for datLine in datLines:
                            if len(datLine.replace('\n','').replace(' ',''))>0 and 'X' not in datLine:
                                lineParts = datLine.replace('\n','').split(' ')
                                rowVec = []
                                for linePart in lineParts:
                                    if linePart!='':
                                        rowVec.append(float(linePart))
                                currentxyData.append(rowVec)
                        normxData = []
                        xData = []
                        yData = []
                        for xyPair in currentxyData:
                            normxData.append(xyPair[0])
                            xData.append(pathStartVariable+(pathEndVariable-pathStartVariable)*xyPair[0])
                            yData.append(xyPair[1])
                        if 'S11' in stressComp:
                            Sxx.append(yData)
                            pathCoords.append(xData)
                            pathNormCoords.append(normxData)
                            pathVariables.append(pathVariable)
                            pathStartVariables.append(pathStartVariable)
                            pathEndVariables.append(pathEndVariable)
                        elif 'S22' in stressComp:
                            Syy.append(yData)
                        elif 'S23' in stressComp:
                            Syz.append(yData)
                        elif 'S12' in stressComp:
                            Sxy.append(yData)
                        elif 'S13' in stressComp:
                            Szx.append(yData)
                        elif 'S33' in stressComp:
                            Szz.append(yData)
                            Szx.append(0.0)
                            Syz.append(0.0)
                            currentSxx = Sxx[-1]
                            currentSyy = Syy[-1]
                            currentSzz = yData
                            currentSxy = Sxy[-1]
                            currentSzx = 0.0
                            currentSyz = 0.0
                            currentSrr = []
                            currentStt = []
                            currentSrt = []
                            current3DS1 = []
                            current3DS2 = []
                            current3DS3 = []
                            current3DI1 = []
                            current3DI2 = []
                            current3DI3 = []
                            current3DSMises = []
                            current3DSaver = []
                            current2DS1 = []
                            current2DS2 = []
                            current2DI1 = []
                            current2DI2 = []
                            current2DSMises = []
                            current2DSaver = []
                            nstressPoints = np.min([len(currentSxx),len(currentSyy),len(currentSzz),len(currentSxy)])
                            for s in range(0,nstressPoints):
                                rotateBy = np.arctan2(pathVariable,pathCoords[-1][s])
                                cosRot = np.cos(rotateBy)
                                sinRot = np.sin(rotateBy)
                                sxx = currentSxx[s]
                                syy = currentSyy[s]
                                szz = currentSzz[s]
                                sxy = currentSxy[s]
                                szx = 0.0
                                syz = 0.0

                                srr = sxx*cosRot*cosRot+syy*sinRot*sinRot+2*sxy*cosRot*sinRot
                                stt = sxx*sinRot*sinRot+syy*cosRot*cosRot-2*sxy*cosRot*sinRot
                                srt = -sxx*cosRot*sinRot+syy*cosRot*sinRot+sxy*(cosRot*cosRot-sinRot*sinRot)
                                currentSrr.append(srr)
                                currentStt.append(stt)
                                currentSrt.append(srt)

                                i1d2 = sxx + syy
                                i1d3 = sxx + syy + szz

                                i2d2 = sxx*syy - sxy*sxy
                                i2d3 = sxx*syy + syy*szz + sxx*szz - sxy*sxy - syz*syz - szx*szx

                                i3d3 = sxx*syy*szz - sxx*syz*syz - syy*szx*szx - szz*sxy*sxy + 2*sxy*syz*szx

                                saverd2 = i1d2/2.0
                                saverd3 = i1d3/3.0

                                smises2d =  np.sqrt(sxx*sxx + syy*syy - sxx*syy + 3*sxy*sxy)
                                smises3d =  np.sqrt(sxx*sxx + syy*syy + szz*szz - sxx*syy - syy*szz - sxx*szz + 3*(sxy*sxy + syz*syz + szx*szx))

                                s1d2 = 0.5*(sxx+syy)+np.sqrt((0.5*(sxx-syy))*(0.5*(sxx-syy))+sxy*sxy)
                                s2d2 = 0.5*(sxx+syy)-np.sqrt((0.5*(sxx-syy))*(0.5*(sxx-syy))+sxy*sxy)

                                try:
                                    princOrient = np.arccos((2*i1d3*i1d3*i1d3-9*i1d3*i2d3+27*i3d3)/(2*np.sqrt((i1d3*i1d3-3*i2d3)*(i1d3*i1d3-3*i2d3)*(i1d3*i1d3-3*i2d3))))/3.0
                                    s1d3 = i1d3/3.0 + 2*np.sqrt(i1d3*i1d3-3*i2d3)*np.cos(princOrient)/3.0
                                    s2d3 = i1d3/3.0 + 2*np.sqrt(i1d3*i1d3-3*i2d3)*np.cos(princOrient-2*np.pi/3.0)/3.0
                                    s3d3 = i1d3/3.0 + 2*np.sqrt(i1d3*i1d3-3*i2d3)*np.cos(princOrient-4*np.pi/3.0)/3.0
                                except Exception:
                                    s1d3 = s1d2
                                    s2d3 = s2d2
                                    s3d3 = 0.0

                                current3DS1.append(s1d3)
                                current3DS2.append(s2d3)
                                current3DS3.append(s2d3)
                                current3DI1.append(i1d3)
                                current3DI2.append(i2d3)
                                current3DI3.append(i3d3)
                                current3DSMises.append(smises3d)
                                current3DSaver.append(saverd3)
                                current2DS1.append(s1d2)
                                current2DS2.append(s2d2)
                                current2DI1.append(i1d2)
                                current2DI2.append(i2d2)
                                current2DSMises.append(smises2d)
                                current2DSaver.append(saverd2)

                            Srr.append(currentSrr)
                            Stt.append(currentStt)
                            Srt.append(currentSrt)
                            S1D3.append(current3DS1)
                            S2D3.append(current3DS2)
                            S3D3.append(current3DS3)
                            S1D2.append(current2DS1)
                            S2D2.append(current2DS2)
                            I1D3.append(current3DI1)
                            I2D3.append(current3DI2)
                            I3D3.append(current3DI3)
                            I1D2.append(current2DI1)
                            I2D2.append(current2DI2)
                            SMisesD3.append(current3DSMises)
                            SaverD3.append(current3DSaver)
                            SMisesD2.append(current2DSMises)
                            SaverD2.append(current2DSaver)

                            currentSrr = []
                            currentStt = []
                            currentSrt = []
                            current3DS1 = []
                            current3DS2 = []
                            current3DS3 = []
                            current3DI1 = []
                            current3DI2 = []
                            current3DI3 = []
                            current3DSMises = []
                            current3DSaver = []
                            current2DS1 = []
                            current2DS2 = []
                            current2DI1 = []
                            current2DI2 = []
                            current2DSMises = []
                            current2DSaver = []

                    pathVariableName = 'y [mum]'
                    pathStartVariableName = 'xi [mum]'
                    pathEndVariableName = 'xf [mum]'
                    pathCoordinateName = 'x [mum]'
                    datasheetName = 'Values, deltatheta=' + subFolder.split('deltatheta')[-1].replace('_','.')
                    horizontalpathsSheetnames.append(datasheetName)
                    numberOfHorizontalpaths.append(len(pathVariables))
                    worksheet = horizontalpathsWorkbook.add_worksheet(datasheetName.decode('utf-8'))
                    for p, pathVariable in enumerate(pathVariables):
                        worksheet.write(0,p*25,pathVariableName,horizontalpathsstringFormat)
                        worksheet.write(1,p*25,pathVariable,horizontalpathsnumberFormatReduced)
                        worksheet.write(0,p*25+1,pathStartVariableName,horizontalpathsstringFormat)
                        worksheet.write(1,p*25+1,pathStartVariables[p],horizontalpathsnumberFormat)
                        worksheet.write(0,p*25+2,pathEndVariableName,horizontalpathsstringFormat)
                        worksheet.write(1,p*25+2,pathEndVariables[p],horizontalpathsnumberFormat)
                        worksheet.write(2,p*25,pathCoordinateName,horizontalpathsstringFormat)
                        worksheet.write(2,p*25+1,'Norm ' + pathCoordinateName,horizontalpathsstringFormat)
                        worksheet.write(2,p*25+2,'Sxx [MPa]',horizontalpathsstringFormat)
                        worksheet.write(2,p*25+3,'Syy [MPa]',horizontalpathsstringFormat)
                        worksheet.write(2,p*25+4,'Szz [MPa]',horizontalpathsstringFormat)
                        worksheet.write(2,p*25+5,'Sxy [MPa]',horizontalpathsstringFormat)
                        worksheet.write(2,p*25+6,'Szx [MPa]',horizontalpathsstringFormat)
                        worksheet.write(2,p*25+7,'Syz [MPa]',horizontalpathsstringFormat)
                        worksheet.write(2,p*25+8,'Srr [MPa]',horizontalpathsstringFormat)
                        worksheet.write(2,p*25+9,'Stt [MPa]',horizontalpathsstringFormat)
                        worksheet.write(2,p*25+10,'Srt [MPa]',horizontalpathsstringFormat)
                        worksheet.write(2,p*25+11,'S1_3D [MPa]',horizontalpathsstringFormat)
                        worksheet.write(2,p*25+12,'S2_3D [MPa]',horizontalpathsstringFormat)
                        worksheet.write(2,p*25+13,'S3_3D [MPa]',horizontalpathsstringFormat)
                        worksheet.write(2,p*25+14,'S1_2D [MPa]',horizontalpathsstringFormat)
                        worksheet.write(2,p*25+15,'S2_2D [MPa]',horizontalpathsstringFormat)
                        worksheet.write(2,p*25+16,'Smises_3D [MPa]',horizontalpathsstringFormat)
                        worksheet.write(2,p*25+17,'Smises_2D [MPa]',horizontalpathsstringFormat)
                        worksheet.write(2,p*25+18,'Saverage_3D [MPa]',horizontalpathsstringFormat)
                        worksheet.write(2,p*25+19,'Saverage_2D [MPa]',horizontalpathsstringFormat)
                        worksheet.write(2,p*25+20,'I1_3D [MPa]',horizontalpathsstringFormat)
                        worksheet.write(2,p*25+21,'I2_3D [MPa^2]',horizontalpathsstringFormat)
                        worksheet.write(2,p*25+22,'I3_3D [MPa^3]',horizontalpathsstringFormat)
                        worksheet.write(2,p*25+23,'I1_2D [MPa]',horizontalpathsstringFormat)
                        worksheet.write(2,p*25+24,'I2_2D [MPa^2]',horizontalpathsstringFormat)
                        measureNum = np.min([len(Sxx[p]),len(Syy[p]),len(Szz[p]),len(Sxy[p])])
                        print('          number of path points = ' + str(measureNum))
                        for c in range(0,measureNum):
                            coord = pathCoords[p][c]
                            worksheet.write(3+c,p*25,coord,horizontalpathsnumberFormat)
                            worksheet.write(3+c,p*25+1,pathNormCoords[p][c],horizontalpathsnumberFormat)
                            worksheet.write(3+c,p*25+2,Sxx[p][c],horizontalpathsnumberFormat)
                            worksheet.write(3+c,p*25+3,Syy[p][c],horizontalpathsnumberFormat)
                            worksheet.write(3+c,p*25+4,Szz[p][c],horizontalpathsnumberFormat)
                            worksheet.write(3+c,p*25+5,Sxy[p][c],horizontalpathsnumberFormat)
                            worksheet.write(3+c,p*25+6,0.0,horizontalpathsnumberFormat)
                            worksheet.write(3+c,p*25+7,0.0,horizontalpathsnumberFormat)
                            worksheet.write(3+c,p*25+8,Srr[p][c],horizontalpathsnumberFormat)
                            worksheet.write(3+c,p*25+9,Stt[p][c],horizontalpathsnumberFormat)
                            worksheet.write(3+c,p*25+10,Srt[p][c],horizontalpathsnumberFormat)
                            worksheet.write(3+c,p*25+11,S1D3[p][c],horizontalpathsnumberFormat)
                            worksheet.write(3+c,p*25+12,S2D3[p][c],horizontalpathsnumberFormat)
                            worksheet.write(3+c,p*25+13,S3D3[p][c],horizontalpathsnumberFormat)
                            worksheet.write(3+c,p*25+14,S1D2[p][c],horizontalpathsnumberFormat)
                            worksheet.write(3+c,p*25+15,S2D2[p][c],horizontalpathsnumberFormat)
                            worksheet.write(3+c,p*25+16,SMisesD3[p][c],horizontalpathsnumberFormat)
                            worksheet.write(3+c,p*25+17,SMisesD2[p][c],horizontalpathsnumberFormat)
                            worksheet.write(3+c,p*25+18,SaverD3[p][c],horizontalpathsnumberFormat)
                            worksheet.write(3+c,p*25+19,SaverD2[p][c],horizontalpathsnumberFormat)
                            worksheet.write(3+c,p*25+20,I1D3[p][c],horizontalpathsnumberFormat)
                            worksheet.write(3+c,p*25+21,I2D3[p][c],horizontalpathsnumberFormat)
                            worksheet.write(3+c,p*25+22,I3D3[p][c],horizontalpathsnumberFormat)
                            worksheet.write(3+c,p*25+23,I1D2[p][c],horizontalpathsnumberFormat)
                            worksheet.write(3+c,p*25+24,I2D2[p][c],horizontalpathsnumberFormat)

                    graphsheetName = 'Graphs, deltatheta=' + subFolder.split('deltatheta')[-1].replace('_','.')
                    graphworksheet = horizontalpathsWorkbook.add_worksheet(graphsheetName.decode('utf-8'))
                    print('    --> Writing worksheet')
                    print('        ' + graphsheetName)
                    print(' ')
                    variableNames = ['Sxx [MPa]','Syy [MPa]','Szz [MPa]','Sxy [MPa]','Szx [MPa]','Syz [MPa]','Srr [MPa]','Stt [MPa]','Srt [MPa]','S1_3D [MPa]','S2_3D [MPa]','S3_3D [MPa]','S1_2D [MPa]','S2_2D [MPa]','Smises_3D [MPa]','Smises_2D [MPa]','Saverage_3D [MPa]','Saverage_2D [MPa]','I1_3D [MPa]','I2_3D [MPa^2]','I3_3D [MPa^3]','I1_2D [MPa]','I2_2D [MPa^2]']
                    horizontalpathsDatalengths.append(len(pathCoords[p]))
                    for v,variableName in enumerate(variableNames):
                        chartA = horizontalpathsWorkbook.add_chart({'type': 'scatter','subtype': 'straight_with_markers'})
                        print('        Chart ' + str(v+1) + '.A')
                        print(' ')
                        for p, pathVariable in enumerate(pathVariables):
                            dataLength = len(pathCoords[p])
                            if v==0:
                                horizontalpathsDatalengths.append(dataLength)
                            chartA.add_series({
                                            'name':       pathVariableName + '=' + str(pathVariable),
                                            'categories': [datasheetName,3,25*p,dataLength,25*p],
                                            'values':     [datasheetName,3,25*p+2+v,dataLength,25*p+2+v],
                                             })
                            print('                  Series ' + str(p+1) + ': ' + pathVariableName + '=' + str(pathVariable))
                            print(' ')
                        chartA.set_title ({'name': variableName + ' vs path coordinates'})
                        chartA.set_x_axis({'name': pathCoordinateName})
                        chartA.set_y_axis({'name': variableName})
                        print('             Title: ' + variableName + ' vs path coordinates')
                        print('             x axis: ' + pathCoordinateName)
                        print('             y axis: ' + variableName)
                        print(' ')
                        print(' ')
                        graphworksheet.insert_chart(v*20,0,chartA)
                        chartB = horizontalpathsWorkbook.add_chart({'type': 'scatter','subtype': 'straight_with_markers'})
                        print('        Chart ' + str(v+1) + '.A')
                        print(' ')
                        for p, pathVariable in enumerate(pathVariables):
                            dataLength = len(pathCoords[p])
                            chartB.add_series({
                                            'name':       pathVariableName + '=' + str(pathVariable),
                                            'categories': [datasheetName,3,25*p+1,dataLength,25*p+1],
                                            'values':     [datasheetName,3,25*p+2+v,dataLength,25*p+2+v],
                                             })
                            print('                  Series ' + str(p+1) + ': ' + pathVariableName + '=' + str(pathVariable))
                            print(' ')
                        chartB.set_title ({'name': variableName + ' vs normalized path coordinates'})
                        chartB.set_x_axis({'name': 'Norm ' + pathCoordinateName.split(' ')[0] + ' [-]'})
                        chartB.set_y_axis({'name': variableName})
                        print('             Title: ' + variableName + ' vs path coordinates')
                        print('             x axis: ' + 'Norm ' + pathCoordinateName.split(' ')[0] + ' [-]')
                        print('             y axis: ' + variableName)
                        print(' ')
                        print(' ')
                        graphworksheet.insert_chart(v*20,30,chartB)

                    Sxx = []
                    Syy = []
                    Szz = []
                    Sxy = []
                    Szx = []
                    Syz = []
                    Srr = []
                    Stt = []
                    Srt = []
                    S1D3 = []
                    S2D3 = []
                    S3D3 = []
                    I1D3 = []
                    I2D3 = []
                    I3D3 = []
                    SMisesD3 = []
                    SaverD3 = []
                    S1D2 = []
                    S2D2 = []
                    I1D2 = []
                    I2D2 = []
                    SMisesD2 = []
                    SaverD2 = []
                    pathVariables = []
                    pathStartVariables = []
                    pathEndVariables = []
                    pathCoords = []
                    pathNormCoords = []

                if subFolder.split('/')[-1] + '-stressesverticalpaths' + '.csv' in listdir(subFolder):
                    print('    Analysis of vertical paths for folder ' + subFolder)
                    with open(verticalpathsSummary,'r') as csv:
                        lines = csv.readlines()
                    Sxx = []
                    Syy = []
                    Szz = []
                    Sxy = []
                    Szx = []
                    Syz = []
                    Srr = []
                    Stt = []
                    Srt = []
                    S1D3 = []
                    S2D3 = []
                    S3D3 = []
                    I1D3 = []
                    I2D3 = []
                    I3D3 = []
                    SMisesD3 = []
                    SaverD3 = []
                    S1D2 = []
                    S2D2 = []
                    I1D2 = []
                    I2D2 = []
                    SMisesD2 = []
                    SaverD2 = []
                    pathVariables = []
                    pathStartVariables = []
                    pathEndVariables = []
                    pathCoords = []
                    pathNormCoords = []

                    for line in lines[1:]:
                        stressComp = line.replace('\n','').replace(' ','').split(',')[0]
                        pathVariable = float(line.replace('\n','').replace(' ','').split(',')[1])
                        pathStartVariable = float(line.replace('\n','').replace(' ','').split(',')[2])
                        pathEndVariable = float(line.replace('\n','').replace(' ','').split(',')[3])
                        datfilePath = join(subFolder,line.replace('\n','').replace(' ','').split(',')[-1])
                        print('    Reading component ' + stressComp)
                        print('            ' + 'for vertical path at ' + str(pathVariable) + ' mum')
                        print('            ' + 'starting at ' + str(pathStartVariable) + ' mum')
                        print('            ' + 'ending at ' + str(pathEndVariable) + ' mum')
                        print(' ')
                        with open(datfilePath,'r') as dat:
                            datLines = dat.readlines()
                        currentxyData = []
                        for datLine in datLines:
                            if len(datLine.replace('\n','').replace(' ',''))>0 and 'X' not in datLine:
                                lineParts = datLine.replace('\n','').split(' ')
                                rowVec = []
                                for linePart in lineParts:
                                    if linePart!='':
                                        rowVec.append(float(linePart))
                                currentxyData.append(rowVec)
                        normxData = []
                        xData = []
                        yData = []
                        for xyPair in currentxyData:
                            normxData.append(xyPair[0])
                            xData.append(pathStartVariable+(pathEndVariable-pathStartVariable)*xyPair[0])
                            yData.append(xyPair[1])
                        if 'S11' in stressComp:
                            Sxx.append(yData)
                            pathCoords.append(xData)
                            pathNormCoords.append(normxData)
                            pathVariables.append(pathVariable)
                            pathStartVariables.append(pathStartVariable)
                            pathEndVariables.append(pathEndVariable)
                        elif 'S22' in stressComp:
                            Syy.append(yData)
                        elif 'S23' in stressComp:
                            Syz.append(yData)
                        elif 'S12' in stressComp:
                            Sxy.append(yData)
                        elif 'S13' in stressComp:
                            Szx.append(yData)
                        elif 'S33' in stressComp:
                            Szz.append(yData)
                            Szx.append(0.0)
                            Syz.append(0.0)
                            currentSxx = Sxx[-1]
                            currentSyy = Syy[-1]
                            currentSzz = yData
                            currentSxy = Sxy[-1]
                            currentSzx = 0.0
                            currentSyz = 0.0
                            currentSrr = []
                            currentStt = []
                            currentSrt = []
                            current3DS1 = []
                            current3DS2 = []
                            current3DS3 = []
                            current3DI1 = []
                            current3DI2 = []
                            current3DI3 = []
                            current3DSMises = []
                            current3DSaver = []
                            current2DS1 = []
                            current2DS2 = []
                            current2DI1 = []
                            current2DI2 = []
                            current2DSMises = []
                            current2DSaver = []
                            nstressPoints = np.min([len(currentSxx),len(currentSyy),len(currentSzz),len(currentSxy)])
                            for s in range(0,nstressPoints):
                                rotateBy = np.arctan2(xData[s],pathVariable)
                                cosRot = np.cos(rotateBy)
                                sinRot = np.sin(rotateBy)
                                sxx = currentSxx[s]
                                syy = currentSyy[s]
                                szz = currentSzz[s]
                                sxy = currentSxy[s]
                                szx = 0.0
                                syz = 0.0

                                srr = sxx*cosRot*cosRot+syy*sinRot*sinRot+2*sxy*cosRot*sinRot
                                stt = sxx*sinRot*sinRot+syy*cosRot*cosRot-2*sxy*cosRot*sinRot
                                srt = -sxx*cosRot*sinRot+syy*cosRot*sinRot+sxy*(cosRot*cosRot-sinRot*sinRot)
                                currentSrr.append(srr)
                                currentStt.append(stt)
                                currentSrt.append(srt)

                                i1d2 = sxx + syy
                                i1d3 = sxx + syy + szz

                                i2d2 = sxx*syy - sxy*sxy
                                i2d3 = sxx*syy + syy*szz + sxx*szz - sxy*sxy - syz*syz - szx*szx

                                i3d3 = sxx*syy*szz - sxx*syz*syz - syy*szx*szx - szz*sxy*sxy + 2*sxy*syz*szx

                                saverd2 = i1d2/2.0
                                saverd3 = i1d3/3.0

                                smises2d =  np.sqrt(sxx*sxx + syy*syy - sxx*syy + 3*sxy*sxy)
                                smises3d =  np.sqrt(sxx*sxx + syy*syy + szz*szz - sxx*syy - syy*szz - sxx*szz + 3*(sxy*sxy + syz*syz + szx*szx))

                                s1d2 = 0.5*(sxx+syy)+np.sqrt((0.5*(sxx-syy))*(0.5*(sxx-syy))+sxy*sxy)
                                s2d2 = 0.5*(sxx+syy)-np.sqrt((0.5*(sxx-syy))*(0.5*(sxx-syy))+sxy*sxy)

                                try:
                                    princOrient = np.arccos((2*i1d3*i1d3*i1d3-9*i1d3*i2d3+27*i3d3)/(2*np.sqrt((i1d3*i1d3-3*i2d3)*(i1d3*i1d3-3*i2d3)*(i1d3*i1d3-3*i2d3))))/3.0
                                    s1d3 = i1d3/3.0 + 2*np.sqrt(i1d3*i1d3-3*i2d3)*np.cos(princOrient)/3.0
                                    s2d3 = i1d3/3.0 + 2*np.sqrt(i1d3*i1d3-3*i2d3)*np.cos(princOrient-2*np.pi/3.0)/3.0
                                    s3d3 = i1d3/3.0 + 2*np.sqrt(i1d3*i1d3-3*i2d3)*np.cos(princOrient-4*np.pi/3.0)/3.0
                                except Exception:
                                    s1d3 = s1d2
                                    s2d3 = s2d2
                                    s3d3 = 0.0

                                current3DS1.append(s1d3)
                                current3DS2.append(s2d3)
                                current3DS3.append(s2d3)
                                current3DI1.append(i1d3)
                                current3DI2.append(i2d3)
                                current3DI3.append(i3d3)
                                current3DSMises.append(smises3d)
                                current3DSaver.append(saverd3)
                                current2DS1.append(s1d2)
                                current2DS2.append(s2d2)
                                current2DI1.append(i1d2)
                                current2DI2.append(i2d2)
                                current2DSMises.append(smises2d)
                                current2DSaver.append(saverd2)

                            Srr.append(currentSrr)
                            Stt.append(currentStt)
                            Srt.append(currentSrt)
                            S1D3.append(current3DS1)
                            S2D3.append(current3DS2)
                            S3D3.append(current3DS3)
                            S1D2.append(current2DS1)
                            S2D2.append(current2DS2)
                            I1D3.append(current3DI1)
                            I2D3.append(current3DI2)
                            I3D3.append(current3DI3)
                            I1D2.append(current2DI1)
                            I2D2.append(current2DI2)
                            SMisesD3.append(current3DSMises)
                            SaverD3.append(current3DSaver)
                            SMisesD2.append(current2DSMises)
                            SaverD2.append(current2DSaver)

                            currentSrr = []
                            currentStt = []
                            currentSrt = []
                            current3DS1 = []
                            current3DS2 = []
                            current3DS3 = []
                            current3DI1 = []
                            current3DI2 = []
                            current3DI3 = []
                            current3DSMises = []
                            current3DSaver = []
                            current2DS1 = []
                            current2DS2 = []
                            current2DI1 = []
                            current2DI2 = []
                            current2DSMises = []
                            current2DSaver = []

                    pathVariableName = 'x [mum]'
                    pathStartVariableName = 'yi [mum]'
                    pathEndVariableName = 'yf [mum]'
                    pathCoordinateName = 'y [mum]'
                    datasheetName = 'Values, deltatheta=' + subFolder.split('deltatheta')[-1].replace('_','.')
                    verticalpathsSheetnames.append(datasheetName)
                    numberOfVerticalpaths.append(len(pathVariables))
                    worksheet = verticalpathsWorkbook.add_worksheet(datasheetName.decode('utf-8'))
                    for p, pathVariable in enumerate(pathVariables):
                        worksheet.write(0,p*25,pathVariableName,verticalpathsstringFormat)
                        worksheet.write(1,p*25,pathVariable,verticalpathsnumberFormatReduced)
                        worksheet.write(0,p*25+1,pathStartVariableName,verticalpathsstringFormat)
                        worksheet.write(1,p*25+1,pathStartVariables[p],verticalpathsnumberFormat)
                        worksheet.write(0,p*25+2,pathEndVariableName,verticalpathsstringFormat)
                        worksheet.write(1,p*25+2,pathEndVariables[p],verticalpathsnumberFormat)
                        worksheet.write(2,p*25,pathCoordinateName,verticalpathsstringFormat)
                        worksheet.write(2,p*25+1,'Norm ' + pathCoordinateName,verticalpathsstringFormat)
                        worksheet.write(2,p*25+2,'Sxx [MPa]',verticalpathsstringFormat)
                        worksheet.write(2,p*25+3,'Syy [MPa]',verticalpathsstringFormat)
                        worksheet.write(2,p*25+4,'Szz [MPa]',verticalpathsstringFormat)
                        worksheet.write(2,p*25+5,'Sxy [MPa]',verticalpathsstringFormat)
                        worksheet.write(2,p*25+6,'Szx [MPa]',verticalpathsstringFormat)
                        worksheet.write(2,p*25+7,'Syz [MPa]',verticalpathsstringFormat)
                        worksheet.write(2,p*25+8,'Srr [MPa]',verticalpathsstringFormat)
                        worksheet.write(2,p*25+9,'Stt [MPa]',verticalpathsstringFormat)
                        worksheet.write(2,p*25+10,'Srt [MPa]',verticalpathsstringFormat)
                        worksheet.write(2,p*25+11,'S1_3D [MPa]',verticalpathsstringFormat)
                        worksheet.write(2,p*25+12,'S2_3D [MPa]',verticalpathsstringFormat)
                        worksheet.write(2,p*25+13,'S3_3D [MPa]',verticalpathsstringFormat)
                        worksheet.write(2,p*25+14,'S1_2D [MPa]',verticalpathsstringFormat)
                        worksheet.write(2,p*25+15,'S2_2D [MPa]',verticalpathsstringFormat)
                        worksheet.write(2,p*25+16,'Smises_3D [MPa]',verticalpathsstringFormat)
                        worksheet.write(2,p*25+17,'Smises_2D [MPa]',verticalpathsstringFormat)
                        worksheet.write(2,p*25+18,'Saverage_3D [MPa]',verticalpathsstringFormat)
                        worksheet.write(2,p*25+19,'Saverage_2D [MPa]',verticalpathsstringFormat)
                        worksheet.write(2,p*25+20,'I1_3D [MPa]',verticalpathsstringFormat)
                        worksheet.write(2,p*25+21,'I2_3D [MPa^2]',verticalpathsstringFormat)
                        worksheet.write(2,p*25+22,'I3_3D [MPa^3]',verticalpathsstringFormat)
                        worksheet.write(2,p*25+23,'I1_2D [MPa]',verticalpathsstringFormat)
                        worksheet.write(2,p*25+24,'I2_2D [MPa^2]',verticalpathsstringFormat)
                        measureNum = np.min([len(Sxx[p]),len(Syy[p]),len(Szz[p]),len(Sxy[p])])
                        print('          number of path points = ' + str(measureNum))
                        for c in range(0,measureNum):
                            coord = pathCoords[p][c]
                            worksheet.write(3+c,p*25,coord,verticalpathsnumberFormat)
                            worksheet.write(3+c,p*25+1,pathNormCoords[p][c],verticalpathsnumberFormat)
                            worksheet.write(3+c,p*25+2,Sxx[p][c],verticalpathsnumberFormat)
                            worksheet.write(3+c,p*25+3,Syy[p][c],verticalpathsnumberFormat)
                            worksheet.write(3+c,p*25+4,Szz[p][c],verticalpathsnumberFormat)
                            worksheet.write(3+c,p*25+5,Sxy[p][c],verticalpathsnumberFormat)
                            worksheet.write(3+c,p*25+6,0.0,verticalpathsnumberFormat)
                            worksheet.write(3+c,p*25+7,0.0,verticalpathsnumberFormat)
                            worksheet.write(3+c,p*25+8,Srr[p][c],verticalpathsnumberFormat)
                            worksheet.write(3+c,p*25+9,Stt[p][c],verticalpathsnumberFormat)
                            worksheet.write(3+c,p*25+10,Srt[p][c],verticalpathsnumberFormat)
                            worksheet.write(3+c,p*25+11,S1D3[p][c],verticalpathsnumberFormat)
                            worksheet.write(3+c,p*25+12,S2D3[p][c],verticalpathsnumberFormat)
                            worksheet.write(3+c,p*25+13,S3D3[p][c],verticalpathsnumberFormat)
                            worksheet.write(3+c,p*25+14,S1D2[p][c],verticalpathsnumberFormat)
                            worksheet.write(3+c,p*25+15,S2D2[p][c],verticalpathsnumberFormat)
                            worksheet.write(3+c,p*25+16,SMisesD3[p][c],verticalpathsnumberFormat)
                            worksheet.write(3+c,p*25+17,SMisesD2[p][c],verticalpathsnumberFormat)
                            worksheet.write(3+c,p*25+18,SaverD3[p][c],verticalpathsnumberFormat)
                            worksheet.write(3+c,p*25+19,SaverD2[p][c],verticalpathsnumberFormat)
                            worksheet.write(3+c,p*25+20,I1D3[p][c],verticalpathsnumberFormat)
                            worksheet.write(3+c,p*25+21,I2D3[p][c],verticalpathsnumberFormat)
                            worksheet.write(3+c,p*25+22,I3D3[p][c],verticalpathsnumberFormat)
                            worksheet.write(3+c,p*25+23,I1D2[p][c],verticalpathsnumberFormat)
                            worksheet.write(3+c,p*25+24,I2D2[p][c],verticalpathsnumberFormat)

                    graphsheetName = 'Graphs, deltatheta=' + subFolder.split('deltatheta')[-1].replace('_','.')
                    graphworksheet = verticalpathsWorkbook.add_worksheet(graphsheetName.decode('utf-8'))
                    print('    --> Writing worksheet')
                    print('        ' + graphsheetName)
                    print(' ')
                    variableNames = ['Sxx [MPa]','Syy [MPa]','Szz [MPa]','Sxy [MPa]','Szx [MPa]','Syz [MPa]','Srr [MPa]','Stt [MPa]','Srt [MPa]','S1_3D [MPa]','S2_3D [MPa]','S3_3D [MPa]','S1_2D [MPa]','S2_2D [MPa]','Smises_3D [MPa]','Smises_2D [MPa]','Saverage_3D [MPa]','Saverage_2D [MPa]','I1_3D [MPa]','I2_3D [MPa^2]','I3_3D [MPa^3]','I1_2D [MPa]','I2_2D [MPa^2]']
                    for v,variableName in enumerate(variableNames):
                        chartA = verticalpathsWorkbook.add_chart({'type': 'scatter','subtype': 'straight_with_markers'})
                        print('        Chart ' + str(v+1) + '.A')
                        print(' ')
                        for p, pathVariable in enumerate(pathVariables):
                            dataLength = len(pathCoords[p])
                            if v==0:
                                verticalpathsDatalengths.append(dataLength)
                            chartA.add_series({
                                            'name':       pathVariableName + '=' + str(pathVariable),
                                            'categories': [datasheetName,3,25*p,dataLength,25*p],
                                            'values':     [datasheetName,3,25*p+2+v,dataLength,25*p+2+v],
                                             })
                            print('                  Series ' + str(p+1) + ': ' + pathVariableName + '=' + str(pathVariable))
                            print(' ')
                        chartA.set_title ({'name': variableName + ' vs path coordinates'})
                        chartA.set_x_axis({'name': pathCoordinateName})
                        chartA.set_y_axis({'name': variableName})
                        print('             Title: ' + variableName + ' vs path coordinates')
                        print('             x axis: ' + pathCoordinateName)
                        print('             y axis: ' + variableName)
                        print(' ')
                        print(' ')
                        graphworksheet.insert_chart(v*20,0,chartA)
                        chartB = verticalpathsWorkbook.add_chart({'type': 'scatter','subtype': 'straight_with_markers'})
                        print('        Chart ' + str(v+1) + '.A')
                        print(' ')
                        for p, pathVariable in enumerate(pathVariables):
                            dataLength = len(pathCoords[p])
                            chartB.add_series({
                                            'name':       pathVariableName + '=' + str(pathVariable),
                                            'categories': [datasheetName,3,25*p+1,dataLength,25*p+1],
                                            'values':     [datasheetName,3,2+v,dataLength,2+v],
                                             })
                            print('                  Series ' + str(p+1) + ': ' + pathVariableName + '=' + str(pathVariable))
                            print(' ')
                        chartB.set_title ({'name': variableName + ' vs normalized path coordinates'})
                        chartB.set_x_axis({'name': 'Norm ' + pathCoordinateName.split(' ')[0] + ' [-]'})
                        chartB.set_y_axis({'name': variableName})
                        print('             Title: ' + variableName + ' vs path coordinates')
                        print('             x axis: ' + 'Norm ' + pathCoordinateName.split(' ')[0] + ' [-]')
                        print('             y axis: ' + variableName)
                        print(' ')
                        print(' ')
                        graphworksheet.insert_chart(v*20,30,chartB)

                    Sxx = []
                    Syy = []
                    Szz = []
                    Sxy = []
                    Szx = []
                    Syz = []
                    Srr = []
                    Stt = []
                    Srt = []
                    S1D3 = []
                    S2D3 = []
                    S3D3 = []
                    I1D3 = []
                    I2D3 = []
                    I3D3 = []
                    SMisesD3 = []
                    SaverD3 = []
                    S1D2 = []
                    S2D2 = []
                    I1D2 = []
                    I2D2 = []
                    SMisesD2 = []
                    SaverD2 = []
                    pathVariables = []
                    pathStartVariables = []
                    pathEndVariables = []
                    pathCoords = []
                    pathNormCoords = []

                if subFolder.split('/')[-1] + '-strainsradialpaths' + '.csv' in listdir(subFolder):
                    print('----------------->')
                    print('----------------->')
                    print('    Analysis of radial paths for folder ' + subFolder)
                    print(' ')
                    with open(radialpathsStrainSummary,'r') as csv:
                        lines = csv.readlines()
                    EExx = []
                    EEyy = []
                    EEzz = []
                    EExy = []
                    EEzx = []
                    EEyz = []
                    EErr = []
                    EEtt = []
                    EErt = []
                    EE1D3 = []
                    EE2D3 = []
                    EE3D3 = []
                    EEI1D3 = []
                    EEI2D3 = []
                    EEI3D3 = []
                    EEMisesD3 = []
                    EEaverD3 = []
                    EE1D2 = []
                    EE2D2 = []
                    EEI1D2 = []
                    EEI2D2 = []
                    EEMisesD2 = []
                    EEaverD2 = []
                    pathVariables = []
                    pathStartVariables = []
                    pathEndVariables = []
                    pathCoords = []
                    pathNormCoords = []

                    for line in lines[1:]:
                        strainComp = line.replace('\n','').replace(' ','').split(',')[0]
                        pathVariable = float(line.replace('\n','').replace(' ','').split(',')[1])
                        pathStartVariable = float(line.replace('\n','').replace(' ','').split(',')[2])
                        pathEndVariable = float(line.replace('\n','').replace(' ','').split(',')[3])
                        datfilePath = join(subFolder,line.replace('\n','').replace(' ','').split(',')[-1])
                        print('    Reading component ' + strainComp)
                        print('            ' + 'for radial path at ' + str(pathVariable) + ' deg')
                        print('            ' + 'starting at ' + str(pathStartVariable) + ' mum')
                        print('            ' + 'ending at ' + str(pathEndVariable))
                        print(' ')
                        with open(datfilePath,'r') as dat:
                            datLines = dat.readlines()
                        print('    --> File read')
                        print(' ')
                        currentxyData = []
                        for datLine in datLines:
                            if len(datLine.replace('\n','').replace(' ',''))>0 and 'X' not in datLine:
                                lineParts = datLine.replace('\n','').split(' ')
                                rowVec = []
                                for linePart in lineParts:
                                    if linePart!='':
                                        rowVec.append(float(linePart))
                                currentxyData.append(rowVec)
                        print('    --> Lines parsed')
                        print(' ')
                        normxData = []
                        xData = []
                        yData = []
                        for xyPair in currentxyData:
                            normxData.append(xyPair[0])
                            xData.append(pathStartVariable+(pathEndVariable-pathStartVariable)*xyPair[0])
                            yData.append(xyPair[1])
                        print('    --> Data categorized in independent and dependent variables.')
                        print(' ')
                        if 'EE11' in strainComp:
                            EExx.append(yData)
                            pathCoords.append(xData)
                            pathNormCoords.append(normxData)
                            pathVariables.append(pathVariable)
                            pathStartVariables.append(pathStartVariable)
                            pathEndVariables.append(pathEndVariable)
                            print('    --> Strain component is EE11.')
                            print(' ')
                        elif 'EE22' in strainComp:
                            EEyy.append(yData)
                            print('    --> Strain component is EE22.')
                            print(' ')
                        elif 'EE23' in strainComp:
                            EEyz.append(yData)
                            print('    --> Strain component is EE23.')
                            print(' ')
                        elif 'EE12' in strainComp:
                            EExy.append(yData)
                            print('    --> Strain component is EE12.')
                            print(' ')
                        elif 'EE13' in strainComp:
                            EEzx.append(yData)
                            print('    --> Strain component is EE13.')
                            print(' ')
                        elif 'EE33' in strainComp:
                            EEzz.append(yData)
                            EEzx.append(0.0)
                            EEyz.append(0.0)
                            print('    --> Strain component is EE33.')
                            print(' ')
                            currentEExx = EExx[-1]
                            currentEEyy = EEyy[-1]
                            currentEEzz = yData
                            currentEExy = EExy[-1]
                            currentEEzx = 0.0
                            currentEEyz = 0.0
                            currentEErr = []
                            currentEEtt = []
                            currentEErt = []
                            current3DEE1 = []
                            current3DEE2 = []
                            current3DEE3 = []
                            current3DEEI1 = []
                            current3DEEI2 = []
                            current3DEEI3 = []
                            current3DEEMises = []
                            current3DEEaver = []
                            current2DEE1 = []
                            current2DEE2 = []
                            current2DEEI1 = []
                            current2DEEI2 = []
                            current2DEEMises = []
                            current2DEEaver = []
                            rotateBy = pathVariable*np.pi/180.0
                            cosRot = np.cos(rotateBy)
                            sinRot = np.sin(rotateBy)
                            nstrainPoints = np.min([len(currentEExx),len(currentEEyy),len(currentEEzz),len(currentEExy)])
                            for s in range(0,nstrainPoints):
                                eexx = currentEExx[s]
                                eeyy = currentEEyy[s]
                                eezz = currentEEzz[s]
                                eexy = currentEExy[s]
                                eezx = 0.0
                                eeyz = 0.0
                                eerr = eexx*cosRot*cosRot+eeyy*sinRot*sinRot+2*eexy*cosRot*sinRot
                                eett = eexx*sinRot*sinRot+eeyy*cosRot*cosRot-2*eexy*cosRot*sinRot
                                eert = -eexx*cosRot*sinRot+eeyy*cosRot*sinRot+eexy*(cosRot*cosRot-sinRot*sinRot)
                                currentEErr.append(eerr)
                                currentEEtt.append(eett)
                                currentEErt.append(eert)
                                eei1d2 = eexx + eeyy
                                eei1d3 = eexx + eeyy + eezz
                                eei2d2 = eexx*eeyy - eexy*eexy
                                eei2d3 = eexx*eeyy + eeyy*eezz + eexx*eezz - eexy*eexy - eeyz*eeyz - eezx*eezx
                                eei3d3 = eexx*eeyy*eezz - eexx*eeyz*eeyz - eeyy*eezx*eezx - eezz*eexy*eexy + 2*eexy*eeyz*eezx
                                eeaverd2 = eei1d2/2.0
                                eeaverd3 = eei1d3/3.0
                                eemises2d =  np.sqrt(eexx*eexx + eeyy*eeyy - eexx*eeyy + 3*eexy*eexy)
                                eemises3d =  np.sqrt(eexx*eexx + eeyy*eeyy + eezz*eezz - eexx*eeyy - eeyy*eezz - eexx*eezz + 3*(eexy*eexy + eeyz*eeyz + eezx*eezx))
                                ee1d2 = 0.5*(eexx+eeyy)+np.sqrt((0.5*(eexx-eeyy))*(0.5*(eexx-eeyy))+eexy*eexy)
                                ee2d2 = 0.5*(eexx+eeyy)-np.sqrt((0.5*(eexx-eeyy))*(0.5*(eexx-eeyy))+eexy*eexy)
                                try:
                                    princOrient = np.arccos((2*eei1d3*eei1d3*eei1d3-9*eei1d3*eei2d3+27*eei3d3)/(2*np.sqrt((eei1d3*eei1d3-3*eei2d3)*(eei1d3*eei1d3-3*eei2d3)*(eei1d3*eei1d3-3*eei2d3))))/3.0
                                    ee1d3 = eei1d3/3.0 + 2*np.sqrt(eei1d3*eei1d3-3*eei2d3)*np.cos(princOrient)/3.0
                                    ee2d3 = eei1d3/3.0 + 2*np.sqrt(eei1d3*eei1d3-3*eei2d3)*np.cos(princOrient-2*np.pi/3.0)/3.0
                                    ee3d3 = eei1d3/3.0 + 2*np.sqrt(eei1d3*eei1d3-3*eei2d3)*np.cos(princOrient-4*np.pi/3.0)/3.0
                                except Exception:
                                    ee1d3 = ee1d2
                                    ee2d3 = ee2d2
                                    ee3d3 = 0.0
                                current3DEE1.append(ee1d3)
                                current3DEE2.append(ee2d3)
                                current3DEE3.append(ee2d3)
                                current3DEEI1.append(eei1d3)
                                current3DEEI2.append(eei2d3)
                                current3DEEI3.append(eei3d3)
                                current3DEEMises.append(eemises3d)
                                current3DEEaver.append(eeaverd3)
                                current2DEE1.append(ee1d2)
                                current2DEE2.append(ee2d2)
                                current2DEEI1.append(eei1d2)
                                current2DEEI2.append(eei2d2)
                                current2DEEMises.append(eemises2d)
                                current2DEEaver.append(eeaverd2)
                            EErr.append(currentEErr)
                            EEtt.append(currentEEtt)
                            EErt.append(currentEErt)
                            EE1D3.append(current3DEE1)
                            EE2D3.append(current3DEE2)
                            EE3D3.append(current3DEE3)
                            EE1D2.append(current2DEE1)
                            EE2D2.append(current2DEE2)
                            EEI1D3.append(current3DEEI1)
                            EEI2D3.append(current3DEEI2)
                            EEI3D3.append(current3DEEI3)
                            EEI1D2.append(current2DEEI1)
                            EEI2D2.append(current2DEEI2)
                            EEMisesD3.append(current3DEEMises)
                            EEaverD3.append(current3DEEaver)
                            EEMisesD2.append(current2DEEMises)
                            EEaverD2.append(current2DEEaver)
                            currentEErr = []
                            currentEEtt = []
                            currentEErt = []
                            current3DEE1 = []
                            current3DEE2 = []
                            current3DEE3 = []
                            current3DEEI1 = []
                            current3DEEI2 = []
                            current3DEEI3 = []
                            current3DEEMises = []
                            current3DEEaver = []
                            current2DEE1 = []
                            current2DEE2 = []
                            current2DEEI1 = []
                            current2DEEI2 = []
                            current2DEEMises = []
                            current2DEEaver = []

                    pathVariableName = 'pathAngle [deg]'
                    pathStartVariableName = 'Ri [mum]'
                    pathEndVariableName = 'Rf [mum]'
                    pathCoordinateName = 'R [mum]'
                    datasheetName = 'Values, deltatheta=' + subFolder.split('deltatheta')[-1].replace('_','.')
                    radialpathsStrainSheetnames.append(datasheetName)
                    numberOfRadialpathsStrain.append(len(pathVariables))
                    worksheet = radialpathsStrainWorkbook.add_worksheet(datasheetName.decode('utf-8'))
                    print('    --> Writing worksheet')
                    print('        ' + datasheetName)
                    print(' ')
                    for p, pathVariable in enumerate(pathVariables):
                        print('          pathAngle = ' + str(pathVariable) + ' deg')
                        worksheet.write(0,p*25,pathVariableName,radialpathsStrainstringFormat)
                        worksheet.write(1,p*25,pathVariable,radialpathsStrainnumberFormatReduced)
                        worksheet.write(0,p*25+1,pathStartVariableName,radialpathsStrainstringFormat)
                        worksheet.write(1,p*25+1,pathStartVariables[p],radialpathsStrainnumberFormat)
                        worksheet.write(0,p*25+2,pathEndVariableName,radialpathsStrainstringFormat)
                        worksheet.write(1,p*25+2,pathEndVariables[p],radialpathsStrainnumberFormat)
                        worksheet.write(2,p*25,pathCoordinateName,radialpathsStrainstringFormat)
                        worksheet.write(2,p*25+1,'Norm ' + pathCoordinateName,radialpathsStrainstringFormat)
                        worksheet.write(2,p*25+2,'EExx [mum/mum]',radialpathsStrainstringFormat)
                        worksheet.write(2,p*25+3,'EEyy [mum/mum]',radialpathsStrainstringFormat)
                        worksheet.write(2,p*25+4,'EEzz [mum/mum]',radialpathsStrainstringFormat)
                        worksheet.write(2,p*25+5,'EExy [mum/mum]',radialpathsStrainstringFormat)
                        worksheet.write(2,p*25+6,'EEzx [mum/mum]',radialpathsStrainstringFormat)
                        worksheet.write(2,p*25+7,'EEyz [mum/mum]',radialpathsStrainstringFormat)
                        worksheet.write(2,p*25+8,'EErr [mum/mum]',radialpathsStrainstringFormat)
                        worksheet.write(2,p*25+9,'EEtt [mum/mum]',radialpathsStrainstringFormat)
                        worksheet.write(2,p*25+10,'EErt [mum/mum]',radialpathsStrainstringFormat)
                        worksheet.write(2,p*25+11,'EE1_3D [mum/mum]',radialpathsStrainstringFormat)
                        worksheet.write(2,p*25+12,'EE2_3D [mum/mum]',radialpathsStrainstringFormat)
                        worksheet.write(2,p*25+13,'EE3_3D [mum/mum]',radialpathsStrainstringFormat)
                        worksheet.write(2,p*25+14,'EE1_2D [mum/mum]',radialpathsStrainstringFormat)
                        worksheet.write(2,p*25+15,'EE2_2D [mum/mum]',radialpathsStrainstringFormat)
                        worksheet.write(2,p*25+16,'EEmises_3D [mum/mum]',radialpathsStrainstringFormat)
                        worksheet.write(2,p*25+17,'EEmises_2D [mum/mum]',radialpathsStrainstringFormat)
                        worksheet.write(2,p*25+18,'EEaverage_3D [mum/mum]',radialpathsStrainstringFormat)
                        worksheet.write(2,p*25+19,'EEaverage_2D [mum/mum]',radialpathsStrainstringFormat)
                        worksheet.write(2,p*25+20,'EEI1_3D [mum/mum]',radialpathsStrainstringFormat)
                        worksheet.write(2,p*25+21,'EEI2_3D [(mum/mum)^2]',radialpathsStrainstringFormat)
                        worksheet.write(2,p*25+22,'EEI3_3D [(mum/mum)^3]',radialpathsStrainstringFormat)
                        worksheet.write(2,p*25+23,'EEI1_2D [mum/mum]',radialpathsStrainstringFormat)
                        worksheet.write(2,p*25+24,'EEI2_2D [(mum/mum)^2]',radialpathsStrainstringFormat)
                        measureNum = np.min([len(EExx[p]),len(EEyy[p]),len(EEzz[p]),len(EExy[p])])
                        print('          number of path points = ' + str(measureNum))
                        for c in range(0,measureNum):
                            coord = pathCoords[p][c]
                            worksheet.write(3+c,p*25,coord,radialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+1,pathNormCoords[p][c],radialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+2,EExx[p][c],radialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+3,EEyy[p][c],radialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+4,EEzz[p][c],radialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+5,EExy[p][c],radialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+6,0.0,radialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+7,0.0,radialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+8,EErr[p][c],radialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+9,EEtt[p][c],radialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+10,EErt[p][c],radialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+11,EE1D3[p][c],radialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+12,EE2D3[p][c],radialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+13,EE3D3[p][c],radialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+14,EE1D2[p][c],radialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+15,EE2D2[p][c],radialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+16,EEMisesD3[p][c],radialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+17,EEMisesD2[p][c],radialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+18,EEaverD3[p][c],radialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+19,EEaverD2[p][c],radialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+20,EEI1D3[p][c],radialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+21,EEI2D3[p][c],radialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+22,EEI3D3[p][c],radialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+23,EEI1D2[p][c],radialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+24,EEI2D2[p][c],radialpathsStrainnumberFormat)

                    graphsheetName = 'Graphs, deltatheta=' + subFolder.split('deltatheta')[-1].replace('_','.')
                    graphworksheet = radialpathsStrainWorkbook.add_worksheet(graphsheetName.decode('utf-8'))
                    print('    --> Writing worksheet')
                    print('        ' + graphsheetName)
                    print(' ')
                    variableNames = ['EExx [mum/mum]','EEyy [mum/mum]','EEzz [mum/mum]','EExy [mum/mum]','EEzx [mum/mum]','EEyz [mum/mum]','EErr [mum/mum]','EEtt [mum/mum]','EErt [mum/mum]','EE1_3D [mum/mum]','EE2_3D [mum/mum]','EE3_3D [mum/mum]','EE1_2D [mum/mum]','EE2_2D [mum/mum]','EEmises_3D [mum/mum]','EEmises_2D [mum/mum]','EEaver_3D [mum/mum]','EEaver_2D [mum/mum]','EEI1_3D [mum/mum]','EEI2_3D [(mum/mum)^2]','EEI3_3D [(mum/mum)^3]','EEI1_2D [mum/mum]','EEI2_2D [(mum/mum)^2]']
                    for v,variableName in enumerate(variableNames):
                        chartA = radialpathsStrainWorkbook.add_chart({'type': 'scatter','subtype': 'straight_with_markers'})
                        print('        Chart ' + str(v+1) + '.A')
                        print(' ')
                        for p, pathVariable in enumerate(pathVariables):
                            dataLength = len(pathCoords[p])
                            if v==0:
                                radialpathsStrainDatalengths.append(dataLength)
                            chartA.add_series({
                                            'name':       pathVariableName + '=' + str(pathVariable),
                                            'categories': [datasheetName,3,25*p,dataLength,25*p],
                                            'values':     [datasheetName,3,25*p+2+v,dataLength,25*p+2+v],
                                             })
                            print('                  Series ' + str(p+1) + ': ' + pathVariableName + '=' + str(pathVariable))
                            print(' ')
                        chartA.set_title ({'name': variableName + ' vs path coordinates'})
                        chartA.set_x_axis({'name': pathCoordinateName})
                        chartA.set_y_axis({'name': variableName})
                        print('             Title: ' + variableName + ' vs path coordinates')
                        print('             x axis: ' + pathCoordinateName)
                        print('             y axis: ' + variableName)
                        print(' ')
                        print(' ')
                        graphworksheet.insert_chart(v*20,0,chartA)
                        chartB = radialpathsStrainWorkbook.add_chart({'type': 'scatter','subtype': 'straight_with_markers'})
                        print('        Chart ' + str(v+1) + '.B')
                        print(' ')
                        for p, pathVariable in enumerate(pathVariables):
                            dataLength = len(pathCoords[p])
                            chartB.add_series({
                                            'name':       pathVariableName + '=' + str(pathVariable),
                                            'categories': [datasheetName,3,25*p+1,dataLength,25*p+1],
                                            'values':     [datasheetName,3,25*p+2+v,dataLength,25*p+2+v],
                                             })
                            print('                  Series ' + str(p+1) + ': ' + pathVariableName + '=' + str(pathVariable))
                            print(' ')
                        chartB.set_title ({'name': variableName + ' vs normalized path coordinates'})
                        chartB.set_x_axis({'name': 'Norm ' + pathCoordinateName.split(' ')[0] + ' [-]'})
                        chartB.set_y_axis({'name': variableName})
                        print('             Title: ' + variableName + ' vs path coordinates')
                        print('             x axis: ' + 'Norm ' + pathCoordinateName.split(' ')[0] + ' [-]')
                        print('             y axis: ' + variableName)
                        print(' ')
                        print(' ')
                        graphworksheet.insert_chart(v*20,30,chartB)

                    EExx = []
                    EEyy = []
                    EEzz = []
                    EExy = []
                    EEzx = []
                    EEyz = []
                    EErr = []
                    EEtt = []
                    EErt = []
                    EE1D3 = []
                    EE2D3 = []
                    EE3D3 = []
                    EEI1D3 = []
                    EEI2D3 = []
                    EEI3D3 = []
                    EEMisesD3 = []
                    EEaverD3 = []
                    EE1D2 = []
                    EE2D2 = []
                    EEI1D2 = []
                    EEI2D2 = []
                    EEMisesD2 = []
                    EEaverD2 = []
                    pathVariables = []
                    pathStartVariables = []
                    pathEndVariables = []
                    pathCoords = []
                    pathNormCoords = []
                    print('<-----------------')
                    print('<-----------------')

                if subFolder.split('/')[-1] + '-strainscircumferentialpaths' + '.csv' in listdir(subFolder):
                    print('    Analysis of circumferential paths for folder ' + subFolder)
                    print('    ')
                    with open(circumferentialpathsStrainSummary,'r') as csv:
                        lines = csv.readlines()
                    EExx = []
                    EEyy = []
                    EEzz = []
                    EExy = []
                    EEzx = []
                    EEyz = []
                    EErr = []
                    EEtt = []
                    EErt = []
                    EE1D3 = []
                    EE2D3 = []
                    EE3D3 = []
                    EEI1D3 = []
                    EEI2D3 = []
                    EEI3D3 = []
                    EEMisesD3 = []
                    EEaverD3 = []
                    EE1D2 = []
                    EE2D2 = []
                    EEI1D2 = []
                    EEI2D2 = []
                    EEMisesD2 = []
                    EEaverD2 = []
                    pathVariables = []
                    pathStartVariables = []
                    pathEndVariables = []
                    pathCoords = []
                    pathNormCoords = []

                    for line in lines[1:]:
                        strainComp = line.replace('\n','').replace(' ','').split(',')[0]
                        pathVariable = float(line.replace('\n','').replace(' ','').split(',')[1])
                        pathStartVariable = float(line.replace('\n','').replace(' ','').split(',')[2])
                        pathEndVariable = float(line.replace('\n','').replace(' ','').split(',')[3])
                        datfilePath = join(subFolder,line.replace('\n','').replace(' ','').split(',')[-1])
                        print('    Reading component ' + strainComp)
                        print('            ' + 'for circumferential path at ' + str(pathVariable) + ' mum')
                        print('            ' + 'starting at ' + str(pathStartVariable) + ' deg')
                        print('            ' + 'ending at ' + str(pathEndVariable) + ' deg')
                        print(' ')
                        with open(datfilePath,'r') as dat:
                            datLines = dat.readlines()
                        currentxyData = []
                        for datLine in datLines:
                            if len(datLine.replace('\n','').replace(' ',''))>0 and 'X' not in datLine:
                                lineParts = datLine.replace('\n','').split(' ')
                                rowVec = []
                                for linePart in lineParts:
                                    if linePart!='':
                                        rowVec.append(float(linePart))
                                currentxyData.append(rowVec)
                        normxData = []
                        xData = []
                        yData = []
                        for xyPair in currentxyData:
                            normxData.append(xyPair[0])
                            xData.append(pathStartVariable+(pathEndVariable-pathStartVariable)*xyPair[0])
                            yData.append(xyPair[1])
                        if 'EE11' in strainComp:
                            EExx.append(yData)
                            pathCoords.append(xData)
                            pathNormCoords.append(normxData)
                            pathVariables.append(pathVariable)
                            pathStartVariables.append(pathStartVariable)
                            pathEndVariables.append(pathEndVariable)
                            print('    --> Strain component is EE11.')
                            print(' ')
                        elif 'EE22' in strainComp:
                            EEyy.append(yData)
                            print('    --> Strain component is EE22.')
                            print(' ')
                        elif 'EE23' in strainComp:
                            EEyz.append(yData)
                            print('    --> Strain component is EE23.')
                            print(' ')
                        elif 'EE12' in strainComp:
                            EExy.append(yData)
                            print('    --> Strain component is EE12.')
                            print(' ')
                        elif 'EE13' in strainComp:
                            EEzx.append(yData)
                            print('    --> Strain component is EE13.')
                            print(' ')
                        elif 'EE33' in strainComp:
                            EEzz.append(yData)
                            EEzx.append(0.0)
                            EEyz.append(0.0)
                            print('    --> Strain component is EE33.')
                            print(' ')
                            currentEExx = EExx[-1]
                            currentEEyy = EEyy[-1]
                            currentEEzz = yData
                            currentEExy = EExy[-1]
                            currentEEzx = 0.0
                            currentEEyz = 0.0
                            currentEErr = []
                            currentEEtt = []
                            currentEErt = []
                            current3DEE1 = []
                            current3DEE2 = []
                            current3DEE3 = []
                            current3DEEI1 = []
                            current3DEEI2 = []
                            current3DEEI3 = []
                            current3DEEMises = []
                            current3DEEaver = []
                            current2DEE1 = []
                            current2DEE2 = []
                            current2DEEI1 = []
                            current2DEEI2 = []
                            current2DEEMises = []
                            current2DEEaver = []
                            nstrainPoints = np.min([len(currentEExx),len(currentEEyy),len(currentEEzz),len(currentEExy)])
                            for s in range(0,nstrainPoints):
                                rotateBy = pathCoords[-1][s]*np.pi/180.0
                                cosRot = np.cos(rotateBy)
                                sinRot = np.sin(rotateBy)
                                eexx = currentEExx[s]
                                eeyy = currentEEyy[s]
                                eezz = currentEEzz[s]
                                eexy = currentEExy[s]
                                eezx = 0.0
                                eeyz = 0.0
                                eerr = eexx*cosRot*cosRot+eeyy*sinRot*sinRot+2*eexy*cosRot*sinRot
                                eett = eexx*sinRot*sinRot+eeyy*cosRot*cosRot-2*eexy*cosRot*sinRot
                                eert = -eexx*cosRot*sinRot+eeyy*cosRot*sinRot+eexy*(cosRot*cosRot-sinRot*sinRot)
                                currentEErr.append(eerr)
                                currentEEtt.append(eett)
                                currentEErt.append(eert)
                                eei1d2 = eexx + eeyy
                                eei1d3 = eexx + eeyy + eezz
                                eei2d2 = eexx*eeyy - eexy*eexy
                                eei2d3 = eexx*eeyy + eeyy*eezz + eexx*eezz - eexy*eexy - eeyz*eeyz - eezx*eezx
                                eei3d3 = eexx*eeyy*eezz - eexx*eeyz*eeyz - eeyy*eezx*eezx - eezz*eexy*eexy + 2*eexy*eeyz*eezx
                                eeaverd2 = eei1d2/2.0
                                eeaverd3 = eei1d3/3.0
                                eemises2d =  np.sqrt(eexx*eexx + eeyy*eeyy - eexx*eeyy + 3*eexy*eexy)
                                eemises3d =  np.sqrt(eexx*eexx + eeyy*eeyy + eezz*eezz - eexx*eeyy - eeyy*eezz - eexx*eezz + 3*(eexy*eexy + eeyz*eeyz + eezx*eezx))
                                ee1d2 = 0.5*(eexx+eeyy)+np.sqrt((0.5*(eexx-eeyy))*(0.5*(eexx-eeyy))+eexy*eexy)
                                ee2d2 = 0.5*(eexx+eeyy)-np.sqrt((0.5*(eexx-eeyy))*(0.5*(eexx-eeyy))+eexy*eexy)
                                try:
                                    princOrient = np.arccos((2*eei1d3*eei1d3*eei1d3-9*eei1d3*eei2d3+27*eei3d3)/(2*np.sqrt((eei1d3*eei1d3-3*eei2d3)*(eei1d3*eei1d3-3*eei2d3)*(eei1d3*eei1d3-3*eei2d3))))/3.0
                                    ee1d3 = eei1d3/3.0 + 2*np.sqrt(eei1d3*eei1d3-3*eei2d3)*np.cos(princOrient)/3.0
                                    ee2d3 = eei1d3/3.0 + 2*np.sqrt(eei1d3*eei1d3-3*eei2d3)*np.cos(princOrient-2*np.pi/3.0)/3.0
                                    ee3d3 = eei1d3/3.0 + 2*np.sqrt(eei1d3*eei1d3-3*eei2d3)*np.cos(princOrient-4*np.pi/3.0)/3.0
                                except Exception:
                                    ee1d3 = ee1d2
                                    ee2d3 = ee2d2
                                    ee3d3 = 0.0
                                current3DEE1.append(ee1d3)
                                current3DEE2.append(ee2d3)
                                current3DEE3.append(ee2d3)
                                current3DEEI1.append(eei1d3)
                                current3DEEI2.append(eei2d3)
                                current3DEEI3.append(eei3d3)
                                current3DEEMises.append(eemises3d)
                                current3DEEaver.append(eeaverd3)
                                current2DEE1.append(ee1d2)
                                current2DEE2.append(ee2d2)
                                current2DEEI1.append(eei1d2)
                                current2DEEI2.append(eei2d2)
                                current2DEEMises.append(eemises2d)
                                current2DEEaver.append(eeaverd2)
                            EErr.append(currentEErr)
                            EEtt.append(currentEEtt)
                            EErt.append(currentEErt)
                            EE1D3.append(current3DEE1)
                            EE2D3.append(current3DEE2)
                            EE3D3.append(current3DEE3)
                            EE1D2.append(current2DEE1)
                            EE2D2.append(current2DEE2)
                            EEI1D3.append(current3DEEI1)
                            EEI2D3.append(current3DEEI2)
                            EEI3D3.append(current3DEEI3)
                            EEI1D2.append(current2DEEI1)
                            EEI2D2.append(current2DEEI2)
                            EEMisesD3.append(current3DEEMises)
                            EEaverD3.append(current3DEEaver)
                            EEMisesD2.append(current2DEEMises)
                            EEaverD2.append(current2DEEaver)
                            currentEErr = []
                            currentEEtt = []
                            currentEErt = []
                            current3DEE1 = []
                            current3DEE2 = []
                            current3DEE3 = []
                            current3DEEI1 = []
                            current3DEEI2 = []
                            current3DEEI3 = []
                            current3DEEMises = []
                            current3DEEaver = []
                            current2DEE1 = []
                            current2DEE2 = []
                            current2DEEI1 = []
                            current2DEEI2 = []
                            current2DEEMises = []
                            current2DEEaver = []

                    pathVariableName = 'pathRadius [mum]'
                    pathStartVariableName = 'startAngle [deg]'
                    pathEndVariableName = 'endAngle [deg]'
                    pathCoordinateName = 'angle [deg]'
                    datasheetName = 'Values, deltatheta=' + subFolder.split('deltatheta')[-1].replace('_','.')
                    circumferentialpathsStrainSheetnames.append(datasheetName)
                    numberOfCircumferentialpaths.append(len(pathVariables))
                    worksheet = circumferentialpathsStrainWorkbook.add_worksheet(datasheetName.decode('utf-8'))
                    for p, pathVariable in enumerate(pathVariables):
                        worksheet.write(0,p*25,pathVariableName,circumferentialpathsStrainstringFormat)
                        worksheet.write(1,p*25,pathVariable,circumferentialpathsStrainnumberFormatReduced)
                        worksheet.write(0,p*25+1,pathStartVariableName,circumferentialpathsStrainstringFormat)
                        worksheet.write(1,p*25+1,pathStartVariables[p],circumferentialpathsStrainnumberFormat)
                        worksheet.write(0,p*25+2,pathEndVariableName,circumferentialpathsStrainstringFormat)
                        worksheet.write(1,p*25+2,pathEndVariables[p],circumferentialpathsStrainnumberFormat)
                        worksheet.write(2,p*25,pathCoordinateName,circumferentialpathsStrainstringFormat)
                        worksheet.write(2,p*25+1,'Norm ' + pathCoordinateName,circumferentialpathsStrainstringFormat)
                        worksheet.write(2,p*25+2,'EExx [mum/mum]',circumferentialpathsStrainstringFormat)
                        worksheet.write(2,p*25+3,'EEyy [mum/mum]',circumferentialpathsStrainstringFormat)
                        worksheet.write(2,p*25+4,'EEzz [mum/mum]',circumferentialpathsStrainstringFormat)
                        worksheet.write(2,p*25+5,'EExy [mum/mum]',circumferentialpathsStrainstringFormat)
                        worksheet.write(2,p*25+6,'EEzx [mum/mum]',circumferentialpathsStrainstringFormat)
                        worksheet.write(2,p*25+7,'EEyz [mum/mum]',circumferentialpathsStrainstringFormat)
                        worksheet.write(2,p*25+8,'EErr [mum/mum]',circumferentialpathsStrainstringFormat)
                        worksheet.write(2,p*25+9,'EEtt [mum/mum]',circumferentialpathsStrainstringFormat)
                        worksheet.write(2,p*25+10,'EErt [mum/mum]',circumferentialpathsStrainstringFormat)
                        worksheet.write(2,p*25+11,'EE1_3D [mum/mum]',circumferentialpathsStrainstringFormat)
                        worksheet.write(2,p*25+12,'EE2_3D [mum/mum]',circumferentialpathsStrainstringFormat)
                        worksheet.write(2,p*25+13,'EE3_3D [mum/mum]',circumferentialpathsStrainstringFormat)
                        worksheet.write(2,p*25+14,'EE1_2D [mum/mum]',circumferentialpathsStrainstringFormat)
                        worksheet.write(2,p*25+15,'EE2_2D [mum/mum]',circumferentialpathsStrainstringFormat)
                        worksheet.write(2,p*25+16,'EEmises_3D [mum/mum]',circumferentialpathsStrainstringFormat)
                        worksheet.write(2,p*25+17,'EEmises_2D [mum/mum]',circumferentialpathsStrainstringFormat)
                        worksheet.write(2,p*25+18,'EEaverage_3D [mum/mum]',circumferentialpathsStrainstringFormat)
                        worksheet.write(2,p*25+19,'EEaverage_2D [mum/mum]',circumferentialpathsStrainstringFormat)
                        worksheet.write(2,p*25+20,'EEI1_3D [mum/mum]',circumferentialpathsStrainstringFormat)
                        worksheet.write(2,p*25+21,'EEI2_3D [(mum/mum)^2]',circumferentialpathsStrainstringFormat)
                        worksheet.write(2,p*25+22,'EEI3_3D [(mum/mum)^3]',circumferentialpathsStrainstringFormat)
                        worksheet.write(2,p*25+23,'EEI1_2D [mum/mum]',circumferentialpathsStrainstringFormat)
                        worksheet.write(2,p*25+24,'EEI2_2D [(mum/mum)^2]',circumferentialpathsStrainstringFormat)
                        measureNum = np.min([len(EExx[p]),len(EEyy[p]),len(EEzz[p]),len(EExy[p])])
                        print('          number of path points = ' + str(measureNum))
                        for c in range(0,measureNum):
                            coord = pathCoords[p][c]
                            worksheet.write(3+c,p*25,coord,circumferentialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+1,pathNormCoords[p][c],circumferentialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+2,EExx[p][c],circumferentialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+3,EEyy[p][c],circumferentialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+4,EEzz[p][c],circumferentialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+5,EExy[p][c],circumferentialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+6,0.0,circumferentialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+7,0.0,circumferentialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+8,EErr[p][c],circumferentialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+9,EEtt[p][c],circumferentialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+10,EErt[p][c],circumferentialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+11,EE1D3[p][c],circumferentialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+12,EE2D3[p][c],circumferentialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+13,EE3D3[p][c],circumferentialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+14,EE1D2[p][c],circumferentialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+15,EE2D2[p][c],circumferentialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+16,EEMisesD3[p][c],circumferentialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+17,EEMisesD2[p][c],circumferentialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+18,EEaverD3[p][c],circumferentialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+19,EEaverD2[p][c],circumferentialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+20,EEI1D3[p][c],circumferentialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+21,EEI2D3[p][c],circumferentialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+22,EEI3D3[p][c],circumferentialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+23,EEI1D2[p][c],circumferentialpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+24,EEI2D2[p][c],circumferentialpathsStrainnumberFormat)

                    graphsheetName = 'Graphs, deltatheta=' + subFolder.split('deltatheta')[-1].replace('_','.')
                    graphworksheet = circumferentialpathsStrainWorkbook.add_worksheet(graphsheetName.decode('utf-8'))
                    print('    --> Writing worksheet')
                    print('        ' + graphsheetName)
                    print(' ')
                    variableNames = ['EExx [mum/mum]','EEyy [mum/mum]','EEzz [mum/mum]','EExy [mum/mum]','EEzx [mum/mum]','EEyz [mum/mum]','EErr [mum/mum]','EEtt [mum/mum]','EErt [mum/mum]','EE1_3D [mum/mum]','EE2_3D [mum/mum]','EE3_3D [mum/mum]','EE1_2D [mum/mum]','EE2_2D [mum/mum]','EEmises_3D [mum/mum]','EEmises_2D [mum/mum]','EEaver_3D [mum/mum]','EEaver_2D [mum/mum]','EEI1_3D [mum/mum]','EEI2_3D [(mum/mum)^2]','EEI3_3D [(mum/mum)^3]','EEI1_2D [mum/mum]','EEI2_2D [(mum/mum)^2]']
                    #circumferentialpathsStrainDatalengths.append(len(pathCoords[p]))
                    for v,variableName in enumerate(variableNames):
                        chartA = circumferentialpathsStrainWorkbook.add_chart({'type': 'scatter','subtype': 'straight_with_markers'})
                        print('        Chart ' + str(v+1) + '.A')
                        print(' ')
                        for p, pathVariable in enumerate(pathVariables):
                            dataLength = len(pathCoords[p])
                            #if v==0:
                            #    circumferentialpathsStrainDatalengths.append(dataLength)
                            chartA.add_series({
                                            'name':       pathVariableName + '=' + str(pathVariable),
                                            'categories': [datasheetName,3,25*p,dataLength,25*p],
                                            'values':     [datasheetName,3,25*p+2+v,dataLength,25*p+2+v],
                                             })
                            print('                  Series ' + str(p+1) + ': ' + pathVariableName + '=' + str(pathVariable))
                            print(' ')
                        chartA.set_title ({'name': variableName + ' vs path coordinates'})
                        chartA.set_x_axis({'name': pathCoordinateName})
                        chartA.set_y_axis({'name': variableName})
                        print('             Title: ' + variableName + ' vs path coordinates')
                        print('             x axis: ' + pathCoordinateName)
                        print('             y axis: ' + variableName)
                        print(' ')
                        print(' ')
                        graphworksheet.insert_chart(v*20,0,chartA)
                        chartB = circumferentialpathsStrainWorkbook.add_chart({'type': 'scatter','subtype': 'straight_with_markers'})
                        print('        Chart ' + str(v+1) + '.B')
                        print(' ')
                        for p, pathVariable in enumerate(pathVariables):
                            dataLength = len(pathCoords[p])
                            chartB.add_series({
                                            'name':       pathVariableName + '=' + str(pathVariable),
                                            'categories': [datasheetName,3,25*p+1,dataLength,25*p+1],
                                            'values':     [datasheetName,3,25*p+2+v,dataLength,25*p+2+v],
                                             })
                            print('                  Series ' + str(p+1) + ': ' + pathVariableName + '=' + str(pathVariable))
                            print(' ')
                        chartB.set_title ({'name': variableName + ' vs normalized path coordinates'})
                        chartB.set_x_axis({'name': 'Norm ' + pathCoordinateName.split(' ')[0] + ' [-]'})
                        chartB.set_y_axis({'name': variableName})
                        print('             Title: ' + variableName + ' vs path coordinates')
                        print('             x axis: ' + 'Norm ' + pathCoordinateName.split(' ')[0] + ' [-]')
                        print('             y axis: ' + variableName)
                        print(' ')
                        print(' ')
                        graphworksheet.insert_chart(v*20,30,chartB)

                    EExx = []
                    EEyy = []
                    EEzz = []
                    EExy = []
                    EEzx = []
                    EEyz = []
                    EErr = []
                    EEtt = []
                    EErt = []
                    EE1D3 = []
                    EE2D3 = []
                    EE3D3 = []
                    EEI1D3 = []
                    EEI2D3 = []
                    EEI3D3 = []
                    EEMisesD3 = []
                    EEaverD3 = []
                    EE1D2 = []
                    EE2D2 = []
                    EEI1D2 = []
                    EEI2D2 = []
                    EEMisesD2 = []
                    EEaverD2 = []
                    pathVariables = []
                    pathStartVariables = []
                    pathEndVariables = []
                    pathCoords = []
                    pathNormCoords = []
                    print('<-----------------')
                    print('<-----------------')

                if subFolder.split('/')[-1] + '-strainshorizontalpaths' + '.csv' in listdir(subFolder):
                    print('    Analysis of horizontal paths for folder ' + subFolder)
                    with open(horizontalpathsStrainSummary,'r') as csv:
                        lines = csv.readlines()
                    EExx = []
                    EEyy = []
                    EEzz = []
                    EExy = []
                    EEzx = []
                    EEyz = []
                    EErr = []
                    EEtt = []
                    EErt = []
                    EE1D3 = []
                    EE2D3 = []
                    EE3D3 = []
                    EEI1D3 = []
                    EEI2D3 = []
                    EEI3D3 = []
                    EEMisesD3 = []
                    EEaverD3 = []
                    EE1D2 = []
                    EE2D2 = []
                    EEI1D2 = []
                    EEI2D2 = []
                    EEMisesD2 = []
                    EEaverD2 = []
                    pathVariables = []
                    pathStartVariables = []
                    pathEndVariables = []
                    pathCoords = []
                    pathNormCoords = []

                    for line in lines[1:]:
                        strainComp = line.replace('\n','').replace(' ','').split(',')[0]
                        pathVariable = float(line.replace('\n','').replace(' ','').split(',')[1])
                        pathStartVariable = float(line.replace('\n','').replace(' ','').split(',')[2])
                        pathEndVariable = float(line.replace('\n','').replace(' ','').split(',')[3])
                        datfilePath = join(subFolder,line.replace('\n','').replace(' ','').split(',')[-1])
                        print('    Reading component ' + strainComp)
                        print('            ' + 'for horizontal path at ' + str(pathVariable) + ' [mum]')
                        print('            ' + 'starting at ' + str(pathStartVariable) + ' mum')
                        print('            ' + 'ending at ' + str(pathEndVariable) + ' mum')
                        print(' ')
                        with open(datfilePath,'r') as dat:
                            datLines = dat.readlines()
                        currentxyData = []
                        for datLine in datLines:
                            if len(datLine.replace('\n','').replace(' ',''))>0 and 'X' not in datLine:
                                lineParts = datLine.replace('\n','').split(' ')
                                rowVec = []
                                for linePart in lineParts:
                                    if linePart!='':
                                        rowVec.append(float(linePart))
                                currentxyData.append(rowVec)
                        normxData = []
                        xData = []
                        yData = []
                        for xyPair in currentxyData:
                            normxData.append(xyPair[0])
                            xData.append(pathStartVariable+(pathEndVariable-pathStartVariable)*xyPair[0])
                            yData.append(xyPair[1])
                        if 'EE11' in strainComp:
                            EExx.append(yData)
                            pathCoords.append(xData)
                            pathNormCoords.append(normxData)
                            pathVariables.append(pathVariable)
                            pathStartVariables.append(pathStartVariable)
                            pathEndVariables.append(pathEndVariable)
                            print('    --> Strain component is EE11.')
                            print(' ')
                        elif 'EE22' in strainComp:
                            EEyy.append(yData)
                            print('    --> Strain component is EE22.')
                            print(' ')
                        elif 'EE23' in strainComp:
                            EEyz.append(yData)
                            print('    --> Strain component is EE23.')
                            print(' ')
                        elif 'EE12' in strainComp:
                            EExy.append(yData)
                            print('    --> Strain component is EE12.')
                            print(' ')
                        elif 'EE13' in strainComp:
                            EEzx.append(yData)
                            print('    --> Strain component is EE13.')
                            print(' ')
                        elif 'EE33' in strainComp:
                            EEzz.append(yData)
                            EEzx.append(0.0)
                            EEyz.append(0.0)
                            print('    --> Strain component is EE33.')
                            print(' ')
                            currentEExx = EExx[-1]
                            currentEEyy = EEyy[-1]
                            currentEEzz = yData
                            currentEExy = EExy[-1]
                            currentEEzx = 0.0
                            currentEEyz = 0.0
                            currentEErr = []
                            currentEEtt = []
                            currentEErt = []
                            current3DEE1 = []
                            current3DEE2 = []
                            current3DEE3 = []
                            current3DEEI1 = []
                            current3DEEI2 = []
                            current3DEEI3 = []
                            current3DEEMises = []
                            current3DEEaver = []
                            current2DEE1 = []
                            current2DEE2 = []
                            current2DEEI1 = []
                            current2DEEI2 = []
                            current2DEEMises = []
                            current2DEEaver = []
                            nstrainPoints = np.min([len(currentEExx),len(currentEEyy),len(currentEEzz),len(currentEExy)])
                            for s in range(0,nstrainPoints):
                                rotateBy = np.arctan2(pathVariable,pathCoords[-1][s])
                                cosRot = np.cos(rotateBy)
                                sinRot = np.sin(rotateBy)
                                eexx = currentEExx[s]
                                eeyy = currentEEyy[s]
                                eezz = currentEEzz[s]
                                eexy = currentEExy[s]
                                eezx = 0.0
                                eeyz = 0.0
                                eerr = eexx*cosRot*cosRot+eeyy*sinRot*sinRot+2*eexy*cosRot*sinRot
                                eett = eexx*sinRot*sinRot+eeyy*cosRot*cosRot-2*eexy*cosRot*sinRot
                                eert = -eexx*cosRot*sinRot+eeyy*cosRot*sinRot+eexy*(cosRot*cosRot-sinRot*sinRot)
                                currentEErr.append(eerr)
                                currentEEtt.append(eett)
                                currentEErt.append(eert)
                                eei1d2 = eexx + eeyy
                                eei1d3 = eexx + eeyy + eezz
                                eei2d2 = eexx*eeyy - eexy*eexy
                                eei2d3 = eexx*eeyy + eeyy*eezz + eexx*eezz - eexy*eexy - eeyz*eeyz - eezx*eezx
                                eei3d3 = eexx*eeyy*eezz - eexx*eeyz*eeyz - eeyy*eezx*eezx - eezz*eexy*eexy + 2*eexy*eeyz*eezx
                                eeaverd2 = eei1d2/2.0
                                eeaverd3 = eei1d3/3.0
                                eemises2d =  np.sqrt(eexx*eexx + eeyy*eeyy - eexx*eeyy + 3*eexy*eexy)
                                eemises3d =  np.sqrt(eexx*eexx + eeyy*eeyy + eezz*eezz - eexx*eeyy - eeyy*eezz - eexx*eezz + 3*(eexy*eexy + eeyz*eeyz + eezx*eezx))
                                ee1d2 = 0.5*(eexx+eeyy)+np.sqrt((0.5*(eexx-eeyy))*(0.5*(eexx-eeyy))+eexy*eexy)
                                ee2d2 = 0.5*(eexx+eeyy)-np.sqrt((0.5*(eexx-eeyy))*(0.5*(eexx-eeyy))+eexy*eexy)
                                try:
                                    princOrient = np.arccos((2*eei1d3*eei1d3*eei1d3-9*eei1d3*eei2d3+27*eei3d3)/(2*np.sqrt((eei1d3*eei1d3-3*eei2d3)*(eei1d3*eei1d3-3*eei2d3)*(eei1d3*eei1d3-3*eei2d3))))/3.0
                                    ee1d3 = eei1d3/3.0 + 2*np.sqrt(eei1d3*eei1d3-3*eei2d3)*np.cos(princOrient)/3.0
                                    ee2d3 = eei1d3/3.0 + 2*np.sqrt(eei1d3*eei1d3-3*eei2d3)*np.cos(princOrient-2*np.pi/3.0)/3.0
                                    ee3d3 = eei1d3/3.0 + 2*np.sqrt(eei1d3*eei1d3-3*eei2d3)*np.cos(princOrient-4*np.pi/3.0)/3.0
                                except Exception:
                                    ee1d3 = ee1d2
                                    ee2d3 = ee2d2
                                    ee3d3 = 0.0
                                current3DEE1.append(ee1d3)
                                current3DEE2.append(ee2d3)
                                current3DEE3.append(ee2d3)
                                current3DEEI1.append(eei1d3)
                                current3DEEI2.append(eei2d3)
                                current3DEEI3.append(eei3d3)
                                current3DEEMises.append(eemises3d)
                                current3DEEaver.append(eeaverd3)
                                current2DEE1.append(ee1d2)
                                current2DEE2.append(ee2d2)
                                current2DEEI1.append(eei1d2)
                                current2DEEI2.append(eei2d2)
                                current2DEEMises.append(eemises2d)
                                current2DEEaver.append(eeaverd2)
                            EErr.append(currentEErr)
                            EEtt.append(currentEEtt)
                            EErt.append(currentEErt)
                            EE1D3.append(current3DEE1)
                            EE2D3.append(current3DEE2)
                            EE3D3.append(current3DEE3)
                            EE1D2.append(current2DEE1)
                            EE2D2.append(current2DEE2)
                            EEI1D3.append(current3DEEI1)
                            EEI2D3.append(current3DEEI2)
                            EEI3D3.append(current3DEEI3)
                            EEI1D2.append(current2DEEI1)
                            EEI2D2.append(current2DEEI2)
                            EEMisesD3.append(current3DEEMises)
                            EEaverD3.append(current3DEEaver)
                            EEMisesD2.append(current2DEEMises)
                            EEaverD2.append(current2DEEaver)
                            currentEErr = []
                            currentEEtt = []
                            currentEErt = []
                            current3DEE1 = []
                            current3DEE2 = []
                            current3DEE3 = []
                            current3DEEI1 = []
                            current3DEEI2 = []
                            current3DEEI3 = []
                            current3DEEMises = []
                            current3DEEaver = []
                            current2DEE1 = []
                            current2DEE2 = []
                            current2DEEI1 = []
                            current2DEEI2 = []
                            current2DEEMises = []
                            current2DEEaver = []

                    pathVariableName = 'y [mum]'
                    pathStartVariableName = 'xi [mum]'
                    pathEndVariableName = 'xf [mum]'
                    pathCoordinateName = 'x [mum]'
                    datasheetName = 'Values, deltatheta=' + subFolder.split('deltatheta')[-1].replace('_','.')
                    horizontalpathsStrainSheetnames.append(datasheetName)
                    numberOfHorizontalpaths.append(len(pathVariables))
                    worksheet = horizontalpathsStrainWorkbook.add_worksheet(datasheetName.decode('utf-8'))
                    for p, pathVariable in enumerate(pathVariables):
                        worksheet.write(0,p*25,pathVariableName,horizontalpathsStrainstringFormat)
                        worksheet.write(1,p*25,pathVariable,horizontalpathsStrainnumberFormatReduced)
                        worksheet.write(0,p*25+1,pathStartVariableName,horizontalpathsStrainstringFormat)
                        worksheet.write(1,p*25+1,pathStartVariables[p],horizontalpathsStrainnumberFormat)
                        worksheet.write(0,p*25+2,pathEndVariableName,horizontalpathsStrainstringFormat)
                        worksheet.write(1,p*25+2,pathEndVariables[p],horizontalpathsStrainnumberFormat)
                        worksheet.write(2,p*25,pathCoordinateName,horizontalpathsStrainstringFormat)
                        worksheet.write(2,p*25+1,'Norm ' + pathCoordinateName,horizontalpathsStrainstringFormat)
                        worksheet.write(2,p*25+2,'EExx [mum/mum]',horizontalpathsStrainstringFormat)
                        worksheet.write(2,p*25+3,'EEyy [mum/mum]',horizontalpathsStrainstringFormat)
                        worksheet.write(2,p*25+4,'EEzz [mum/mum]',horizontalpathsStrainstringFormat)
                        worksheet.write(2,p*25+5,'EExy [mum/mum]',horizontalpathsStrainstringFormat)
                        worksheet.write(2,p*25+6,'EEzx [mum/mum]',horizontalpathsStrainstringFormat)
                        worksheet.write(2,p*25+7,'EEyz [mum/mum]',horizontalpathsStrainstringFormat)
                        worksheet.write(2,p*25+8,'EErr [mum/mum]',horizontalpathsStrainstringFormat)
                        worksheet.write(2,p*25+9,'EEtt [mum/mum]',horizontalpathsStrainstringFormat)
                        worksheet.write(2,p*25+10,'EErt [mum/mum]',horizontalpathsStrainstringFormat)
                        worksheet.write(2,p*25+11,'EE1_3D [mum/mum]',horizontalpathsStrainstringFormat)
                        worksheet.write(2,p*25+12,'EE2_3D [mum/mum]',horizontalpathsStrainstringFormat)
                        worksheet.write(2,p*25+13,'EE3_3D [mum/mum]',horizontalpathsStrainstringFormat)
                        worksheet.write(2,p*25+14,'EE1_2D [mum/mum]',horizontalpathsStrainstringFormat)
                        worksheet.write(2,p*25+15,'EE2_2D [mum/mum]',horizontalpathsStrainstringFormat)
                        worksheet.write(2,p*25+16,'EEmises_3D [mum/mum]',horizontalpathsStrainstringFormat)
                        worksheet.write(2,p*25+17,'EEmises_2D [mum/mum]',horizontalpathsStrainstringFormat)
                        worksheet.write(2,p*25+18,'EEaverage_3D [mum/mum]',horizontalpathsStrainstringFormat)
                        worksheet.write(2,p*25+19,'EEaverage_2D [mum/mum]',horizontalpathsStrainstringFormat)
                        worksheet.write(2,p*25+20,'EEI1_3D [mum/mum]',horizontalpathsStrainstringFormat)
                        worksheet.write(2,p*25+21,'EEI2_3D [(mum/mum)^2]',horizontalpathsStrainstringFormat)
                        worksheet.write(2,p*25+22,'EEI3_3D [(mum/mum)^3]',horizontalpathsStrainstringFormat)
                        worksheet.write(2,p*25+23,'EEI1_2D [mum/mum]',horizontalpathsStrainstringFormat)
                        worksheet.write(2,p*25+24,'EEI2_2D [(mum/mum)^2]',horizontalpathsStrainstringFormat)
                        measureNum = np.min([len(EExx[p]),len(EEyy[p]),len(EEzz[p]),len(EExy[p])])
                        print('          number of path points = ' + str(measureNum))
                        for c in range(0,measureNum):
                            coord = pathCoords[p][c]
                            worksheet.write(3+c,p*25,coord,horizontalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+1,pathNormCoords[p][c],horizontalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+2,EExx[p][c],horizontalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+3,EEyy[p][c],horizontalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+4,EEzz[p][c],horizontalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+5,EExy[p][c],horizontalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+6,0.0,horizontalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+7,0.0,horizontalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+8,EErr[p][c],horizontalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+9,EEtt[p][c],horizontalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+10,EErt[p][c],horizontalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+11,EE1D3[p][c],horizontalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+12,EE2D3[p][c],horizontalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+13,EE3D3[p][c],horizontalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+14,EE1D2[p][c],horizontalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+15,EE2D2[p][c],horizontalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+16,EEMisesD3[p][c],horizontalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+17,EEMisesD2[p][c],horizontalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+18,EEaverD3[p][c],horizontalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+19,EEaverD2[p][c],horizontalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+20,EEI1D3[p][c],horizontalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+21,EEI2D3[p][c],horizontalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+22,EEI3D3[p][c],horizontalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+23,EEI1D2[p][c],horizontalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+24,EEI2D2[p][c],horizontalpathsStrainnumberFormat)

                    graphsheetName = 'Graphs, deltatheta=' + subFolder.split('deltatheta')[-1].replace('_','.')
                    graphworksheet = horizontalpathsStrainWorkbook.add_worksheet(graphsheetName.decode('utf-8'))
                    print('    --> Writing worksheet')
                    print('        ' + graphsheetName)
                    print(' ')
                    variableNames = ['EExx [mum/mum]','EEyy [mum/mum]','EEzz [mum/mum]','EExy [mum/mum]','EEzx [mum/mum]','EEyz [mum/mum]','EErr [mum/mum]','EEtt [mum/mum]','EErt [mum/mum]','EE1_3D [mum/mum]','EE2_3D [mum/mum]','EE3_3D [mum/mum]','EE1_2D [mum/mum]','EE2_2D [mum/mum]','EEmises_3D [mum/mum]','EEmises_2D [mum/mum]','EEaver_3D [mum/mum]','EEaver_2D [mum/mum]','EEI1_3D [mum/mum]','EEI2_3D [(mum/mum)^2]','EEI3_3D [(mum/mum)^3]','EEI1_2D [mum/mum]','EEI2_2D [(mum/mum)^2]']
                    #horizontalpathsStrainDatalengths.append(len(pathCoords[p]))
                    for v,variableName in enumerate(variableNames):
                        chartA = horizontalpathsStrainWorkbook.add_chart({'type': 'scatter','subtype': 'straight_with_markers'})
                        print('        Chart ' + str(v+1) + '.A')
                        print(' ')
                        for p, pathVariable in enumerate(pathVariables):
                            dataLength = len(pathCoords[p])
                            #if v==0:
                            #    horizontalpathsStrainDatalengths.append(dataLength)
                            chartA.add_series({
                                            'name':       pathVariableName + '=' + str(pathVariable),
                                            'categories': [datasheetName,3,25*p,dataLength,25*p],
                                            'values':     [datasheetName,3,25*p+2+v,dataLength,25*p+2+v],
                                             })
                            print('                  Series ' + str(p+1) + ': ' + pathVariableName + '=' + str(pathVariable))
                            print(' ')
                        chartA.set_title ({'name': variableName + ' vs path coordinates'})
                        chartA.set_x_axis({'name': pathCoordinateName})
                        chartA.set_y_axis({'name': variableName})
                        print('             Title: ' + variableName + ' vs path coordinates')
                        print('             x axis: ' + pathCoordinateName)
                        print('             y axis: ' + variableName)
                        print(' ')
                        print(' ')
                        graphworksheet.insert_chart(v*20,0,chartA)
                        chartB = horizontalpathsStrainWorkbook.add_chart({'type': 'scatter','subtype': 'straight_with_markers'})
                        print('        Chart ' + str(v+1) + '.A')
                        print(' ')
                        for p, pathVariable in enumerate(pathVariables):
                            dataLength = len(pathCoords[p])
                            chartB.add_series({
                                            'name':       pathVariableName + '=' + str(pathVariable),
                                            'categories': [datasheetName,3,25*p+1,dataLength,25*p+1],
                                            'values':     [datasheetName,3,25*p+2+v,dataLength,25*p+2+v],
                                             })
                            print('                  Series ' + str(p+1) + ': ' + pathVariableName + '=' + str(pathVariable))
                            print(' ')
                        chartB.set_title ({'name': variableName + ' vs normalized path coordinates'})
                        chartB.set_x_axis({'name': 'Norm ' + pathCoordinateName.split(' ')[0] + ' [-]'})
                        chartB.set_y_axis({'name': variableName})
                        print('             Title: ' + variableName + ' vs path coordinates')
                        print('             x axis: ' + 'Norm ' + pathCoordinateName.split(' ')[0] + ' [-]')
                        print('             y axis: ' + variableName)
                        print(' ')
                        print(' ')
                        graphworksheet.insert_chart(v*20,30,chartB)

                    EExx = []
                    EEyy = []
                    EEzz = []
                    EExy = []
                    EEzx = []
                    EEyz = []
                    EErr = []
                    EEtt = []
                    EErt = []
                    EE1D3 = []
                    EE2D3 = []
                    EE3D3 = []
                    EEI1D3 = []
                    EEI2D3 = []
                    EEI3D3 = []
                    EEMisesD3 = []
                    EEaverD3 = []
                    EE1D2 = []
                    EE2D2 = []
                    EEI1D2 = []
                    EEI2D2 = []
                    EEMisesD2 = []
                    EEaverD2 = []
                    pathVariables = []
                    pathStartVariables = []
                    pathEndVariables = []
                    pathCoords = []
                    pathNormCoords = []
                    print('<-----------------')
                    print('<-----------------')

                if subFolder.split('/')[-1] + '-strainsverticalpaths' + '.csv' in listdir(subFolder):
                    print('    Analysis of vertical paths for folder ' + subFolder)
                    with open(verticalpathsStrainSummary,'r') as csv:
                        lines = csv.readlines()
                    EExx = []
                    EEyy = []
                    EEzz = []
                    EExy = []
                    EEzx = []
                    EEyz = []
                    EErr = []
                    EEtt = []
                    EErt = []
                    EE1D3 = []
                    EE2D3 = []
                    EE3D3 = []
                    EEI1D3 = []
                    EEI2D3 = []
                    EEI3D3 = []
                    EEMisesD3 = []
                    EEaverD3 = []
                    EE1D2 = []
                    EE2D2 = []
                    EEI1D2 = []
                    EEI2D2 = []
                    EEMisesD2 = []
                    EEaverD2 = []
                    pathVariables = []
                    pathStartVariables = []
                    pathEndVariables = []
                    pathCoords = []
                    pathNormCoords = []

                    for line in lines[1:]:
                        strainComp = line.replace('\n','').replace(' ','').split(',')[0]
                        pathVariable = float(line.replace('\n','').replace(' ','').split(',')[1])
                        pathStartVariable = float(line.replace('\n','').replace(' ','').split(',')[2])
                        pathEndVariable = float(line.replace('\n','').replace(' ','').split(',')[3])
                        datfilePath = join(subFolder,line.replace('\n','').replace(' ','').split(',')[-1])
                        print('    Reading component ' + strainComp)
                        print('            ' + 'for vertical path at ' + str(pathVariable) + ' mum')
                        print('            ' + 'starting at ' + str(pathStartVariable) + ' mum')
                        print('            ' + 'ending at ' + str(pathEndVariable) + ' mum')
                        print(' ')
                        with open(datfilePath,'r') as dat:
                            datLines = dat.readlines()
                        currentxyData = []
                        for datLine in datLines:
                            if len(datLine.replace('\n','').replace(' ',''))>0 and 'X' not in datLine:
                                lineParts = datLine.replace('\n','').split(' ')
                                rowVec = []
                                for linePart in lineParts:
                                    if linePart!='':
                                        rowVec.append(float(linePart))
                                currentxyData.append(rowVec)
                        normxData = []
                        xData = []
                        yData = []
                        for xyPair in currentxyData:
                            normxData.append(xyPair[0])
                            xData.append(pathStartVariable+(pathEndVariable-pathStartVariable)*xyPair[0])
                            yData.append(xyPair[1])
                        if 'EE11' in strainComp:
                            EExx.append(yData)
                            pathCoords.append(xData)
                            pathNormCoords.append(normxData)
                            pathVariables.append(pathVariable)
                            pathStartVariables.append(pathStartVariable)
                            pathEndVariables.append(pathEndVariable)
                            print('    --> Strain component is EE11.')
                            print(' ')
                        elif 'EE22' in strainComp:
                            EEyy.append(yData)
                            print('    --> Strain component is EE22.')
                            print(' ')
                        elif 'EE23' in strainComp:
                            EEyz.append(yData)
                            print('    --> Strain component is EE23.')
                            print(' ')
                        elif 'EE12' in strainComp:
                            EExy.append(yData)
                            print('    --> Strain component is EE12.')
                            print(' ')
                        elif 'EE13' in strainComp:
                            EEzx.append(yData)
                            print('    --> Strain component is EE13.')
                            print(' ')
                        elif 'EE33' in strainComp:
                            EEzz.append(yData)
                            EEzx.append(0.0)
                            EEyz.append(0.0)
                            print('    --> Strain component is EE33.')
                            print(' ')
                            currentEExx = EExx[-1]
                            currentEEyy = EEyy[-1]
                            currentEEzz = yData
                            currentEExy = EExy[-1]
                            currentEEzx = 0.0
                            currentEEyz = 0.0
                            currentEErr = []
                            currentEEtt = []
                            currentEErt = []
                            current3DEE1 = []
                            current3DEE2 = []
                            current3DEE3 = []
                            current3DEEI1 = []
                            current3DEEI2 = []
                            current3DEEI3 = []
                            current3DEEMises = []
                            current3DEEaver = []
                            current2DEE1 = []
                            current2DEE2 = []
                            current2DEEI1 = []
                            current2DEEI2 = []
                            current2DEEMises = []
                            current2DEEaver = []
                            nstrainPoints = np.min([len(currentEExx),len(currentEEyy),len(currentEEzz),len(currentEExy)])
                            for s in range(0,nstrainPoints):
                                rotateBy = np.arctan2(xData[s],pathVariable)
                                cosRot = np.cos(rotateBy)
                                sinRot = np.sin(rotateBy)
                                eexx = currentEExx[s]
                                eeyy = currentEEyy[s]
                                eezz = currentEEzz[s]
                                eexy = currentEExy[s]
                                eezx = 0.0
                                eeyz = 0.0
                                eerr = eexx*cosRot*cosRot+eeyy*sinRot*sinRot+2*eexy*cosRot*sinRot
                                eett = eexx*sinRot*sinRot+eeyy*cosRot*cosRot-2*eexy*cosRot*sinRot
                                eert = -eexx*cosRot*sinRot+eeyy*cosRot*sinRot+eexy*(cosRot*cosRot-sinRot*sinRot)
                                currentEErr.append(eerr)
                                currentEEtt.append(eett)
                                currentEErt.append(eert)
                                eei1d2 = eexx + eeyy
                                eei1d3 = eexx + eeyy + eezz
                                eei2d2 = eexx*eeyy - eexy*eexy
                                eei2d3 = eexx*eeyy + eeyy*eezz + eexx*eezz - eexy*eexy - eeyz*eeyz - eezx*eezx
                                eei3d3 = eexx*eeyy*eezz - eexx*eeyz*eeyz - eeyy*eezx*eezx - eezz*eexy*eexy + 2*eexy*eeyz*eezx
                                eeaverd2 = eei1d2/2.0
                                eeaverd3 = eei1d3/3.0
                                eemises2d =  np.sqrt(eexx*eexx + eeyy*eeyy - eexx*eeyy + 3*eexy*eexy)
                                eemises3d =  np.sqrt(eexx*eexx + eeyy*eeyy + eezz*eezz - eexx*eeyy - eeyy*eezz - eexx*eezz + 3*(eexy*eexy + eeyz*eeyz + eezx*eezx))
                                ee1d2 = 0.5*(eexx+eeyy)+np.sqrt((0.5*(eexx-eeyy))*(0.5*(eexx-eeyy))+eexy*eexy)
                                ee2d2 = 0.5*(eexx+eeyy)-np.sqrt((0.5*(eexx-eeyy))*(0.5*(eexx-eeyy))+eexy*eexy)
                                try:
                                    princOrient = np.arccos((2*eei1d3*eei1d3*eei1d3-9*eei1d3*eei2d3+27*eei3d3)/(2*np.sqrt((eei1d3*eei1d3-3*eei2d3)*(eei1d3*eei1d3-3*eei2d3)*(eei1d3*eei1d3-3*eei2d3))))/3.0
                                    ee1d3 = eei1d3/3.0 + 2*np.sqrt(eei1d3*eei1d3-3*eei2d3)*np.cos(princOrient)/3.0
                                    ee2d3 = eei1d3/3.0 + 2*np.sqrt(eei1d3*eei1d3-3*eei2d3)*np.cos(princOrient-2*np.pi/3.0)/3.0
                                    ee3d3 = eei1d3/3.0 + 2*np.sqrt(eei1d3*eei1d3-3*eei2d3)*np.cos(princOrient-4*np.pi/3.0)/3.0
                                except Exception:
                                    ee1d3 = ee1d2
                                    ee2d3 = ee2d2
                                    ee3d3 = 0.0
                                current3DEE1.append(ee1d3)
                                current3DEE2.append(ee2d3)
                                current3DEE3.append(ee2d3)
                                current3DEEI1.append(eei1d3)
                                current3DEEI2.append(eei2d3)
                                current3DEEI3.append(eei3d3)
                                current3DEEMises.append(eemises3d)
                                current3DEEaver.append(eeaverd3)
                                current2DEE1.append(ee1d2)
                                current2DEE2.append(ee2d2)
                                current2DEEI1.append(eei1d2)
                                current2DEEI2.append(eei2d2)
                                current2DEEMises.append(eemises2d)
                                current2DEEaver.append(eeaverd2)
                            EErr.append(currentEErr)
                            EEtt.append(currentEEtt)
                            EErt.append(currentEErt)
                            EE1D3.append(current3DEE1)
                            EE2D3.append(current3DEE2)
                            EE3D3.append(current3DEE3)
                            EE1D2.append(current2DEE1)
                            EE2D2.append(current2DEE2)
                            EEI1D3.append(current3DEEI1)
                            EEI2D3.append(current3DEEI2)
                            EEI3D3.append(current3DEEI3)
                            EEI1D2.append(current2DEEI1)
                            EEI2D2.append(current2DEEI2)
                            EEMisesD3.append(current3DEEMises)
                            EEaverD3.append(current3DEEaver)
                            EEMisesD2.append(current2DEEMises)
                            EEaverD2.append(current2DEEaver)
                            currentEErr = []
                            currentEEtt = []
                            currentEErt = []
                            current3DEE1 = []
                            current3DEE2 = []
                            current3DEE3 = []
                            current3DEEI1 = []
                            current3DEEI2 = []
                            current3DEEI3 = []
                            current3DEEMises = []
                            current3DEEaver = []
                            current2DEE1 = []
                            current2DEE2 = []
                            current2DEEI1 = []
                            current2DEEI2 = []
                            current2DEEMises = []
                            current2DEEaver = []

                    pathVariableName = 'x [mum]'
                    pathStartVariableName = 'yi [mum]'
                    pathEndVariableName = 'yf [mum]'
                    pathCoordinateName = 'y [mum]'
                    datasheetName = 'Values, deltatheta=' + subFolder.split('deltatheta')[-1].replace('_','.')
                    verticalpathsStrainSheetnames.append(datasheetName)
                    numberOfVerticalpaths.append(len(pathVariables))
                    worksheet = verticalpathsStrainWorkbook.add_worksheet(datasheetName.decode('utf-8'))
                    for p, pathVariable in enumerate(pathVariables):
                        worksheet.write(0,p*25,pathVariableName,verticalpathsStrainstringFormat)
                        worksheet.write(1,p*25,pathVariable,verticalpathsStrainnumberFormatReduced)
                        worksheet.write(0,p*25+1,pathStartVariableName,verticalpathsStrainstringFormat)
                        worksheet.write(1,p*25+1,pathStartVariables[p],verticalpathsStrainnumberFormat)
                        worksheet.write(0,p*25+2,pathEndVariableName,verticalpathsStrainstringFormat)
                        worksheet.write(1,p*25+2,pathEndVariables[p],verticalpathsStrainnumberFormat)
                        worksheet.write(2,p*25,pathCoordinateName,verticalpathsStrainstringFormat)
                        worksheet.write(2,p*25+1,'Norm ' + pathCoordinateName,verticalpathsStrainstringFormat)
                        worksheet.write(2,p*25+2,'EExx [mum/mum]',verticalpathsStrainstringFormat)
                        worksheet.write(2,p*25+3,'EEyy [mum/mum]',verticalpathsStrainstringFormat)
                        worksheet.write(2,p*25+4,'EEzz [mum/mum]',verticalpathsStrainstringFormat)
                        worksheet.write(2,p*25+5,'EExy [mum/mum]',verticalpathsStrainstringFormat)
                        worksheet.write(2,p*25+6,'EEzx [mum/mum]',verticalpathsStrainstringFormat)
                        worksheet.write(2,p*25+7,'EEyz [mum/mum]',verticalpathsStrainstringFormat)
                        worksheet.write(2,p*25+8,'EErr [mum/mum]',verticalpathsStrainstringFormat)
                        worksheet.write(2,p*25+9,'EEtt [mum/mum]',verticalpathsStrainstringFormat)
                        worksheet.write(2,p*25+10,'EErt [mum/mum]',verticalpathsStrainstringFormat)
                        worksheet.write(2,p*25+11,'EE1_3D [mum/mum]',verticalpathsStrainstringFormat)
                        worksheet.write(2,p*25+12,'EE2_3D [mum/mum]',verticalpathsStrainstringFormat)
                        worksheet.write(2,p*25+13,'EE3_3D [mum/mum]',verticalpathsStrainstringFormat)
                        worksheet.write(2,p*25+14,'EE1_2D [mum/mum]',verticalpathsStrainstringFormat)
                        worksheet.write(2,p*25+15,'EE2_2D [mum/mum]',verticalpathsStrainstringFormat)
                        worksheet.write(2,p*25+16,'EEmises_3D [mum/mum]',verticalpathsStrainstringFormat)
                        worksheet.write(2,p*25+17,'EEmises_2D [mum/mum]',verticalpathsStrainstringFormat)
                        worksheet.write(2,p*25+18,'EEaverage_3D [mum/mum]',verticalpathsStrainstringFormat)
                        worksheet.write(2,p*25+19,'EEaverage_2D [mum/mum]',verticalpathsStrainstringFormat)
                        worksheet.write(2,p*25+20,'EEI1_3D [mum/mum]',verticalpathsStrainstringFormat)
                        worksheet.write(2,p*25+21,'EEI2_3D [(mum/mum)^2]',verticalpathsStrainstringFormat)
                        worksheet.write(2,p*25+22,'EEI3_3D [mum/mum^3]',verticalpathsStrainstringFormat)
                        worksheet.write(2,p*25+23,'EEI1_2D [(mum/mum)]',verticalpathsStrainstringFormat)
                        worksheet.write(2,p*25+24,'EEI2_2D [(mum/mum)^2]',verticalpathsStrainstringFormat)
                        measureNum = np.min([len(EExx[p]),len(EEyy[p]),len(EEzz[p]),len(EExy[p])])
                        print('          number of path points = ' + str(measureNum))
                        for c in range(0,measureNum):
                            coord = pathCoords[p][c]
                            worksheet.write(3+c,p*25,coord,verticalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+1,pathNormCoords[p][c],verticalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+2,EExx[p][c],verticalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+3,EEyy[p][c],verticalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+4,EEzz[p][c],verticalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+5,EExy[p][c],verticalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+6,0.0,verticalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+7,0.0,verticalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+8,EErr[p][c],verticalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+9,EEtt[p][c],verticalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+10,EErt[p][c],verticalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+11,EE1D3[p][c],verticalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+12,EE2D3[p][c],verticalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+13,EE3D3[p][c],verticalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+14,EE1D2[p][c],verticalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+15,EE2D2[p][c],verticalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+16,EEMisesD3[p][c],verticalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+17,EEMisesD2[p][c],verticalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+18,EEaverD3[p][c],verticalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+19,EEaverD2[p][c],verticalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+20,EEI1D3[p][c],verticalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+21,EEI2D3[p][c],verticalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+22,EEI3D3[p][c],verticalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+23,EEI1D2[p][c],verticalpathsStrainnumberFormat)
                            worksheet.write(3+c,p*25+24,EEI2D2[p][c],verticalpathsStrainnumberFormat)

                    graphsheetName = 'Graphs, deltatheta=' + subFolder.split('deltatheta')[-1].replace('_','.')
                    graphworksheet = verticalpathsStrainWorkbook.add_worksheet(graphsheetName.decode('utf-8'))
                    print('    --> Writing worksheet')
                    print('        ' + graphsheetName)
                    print(' ')
                    variableNames = ['EExx [mum/mum]','EEyy [mum/mum]','EEzz [mum/mum]','EExy [mum/mum]','EEzx [mum/mum]','EEyz [mum/mum]','EErr [mum/mum]','EEtt [mum/mum]','EErt [mum/mum]','EE1_3D [mum/mum]','EE2_3D [mum/mum]','EE3_3D [mum/mum]','EE1_2D [mum/mum]','EE2_2D [mum/mum]','EEmises_3D [mum/mum]','EEmises_2D [mum/mum]','EEaver_3D [mum/mum]','EEaver_2D [mum/mum]','EEI1_3D [mum/mum]','EEI2_3D [(mum/mum)^2]','EEI3_3D [(mum/mum)^3]','EEI1_2D [mum/mum]','EEI2_2D [(mum/mum)^2]']
                    for v,variableName in enumerate(variableNames):
                        chartA = verticalpathsStrainWorkbook.add_chart({'type': 'scatter','subtype': 'straight_with_markers'})
                        print('        Chart ' + str(v+1) + '.A')
                        print(' ')
                        for p, pathVariable in enumerate(pathVariables):
                            dataLength = len(pathCoords[p])
                            if v==0:
                                verticalpathsStrainDatalengths.append(dataLength)
                            chartA.add_series({
                                            'name':       pathVariableName + '=' + str(pathVariable),
                                            'categories': [datasheetName,3,25*p,dataLength,25*p],
                                            'values':     [datasheetName,3,25*p+2+v,dataLength,25*p+2+v],
                                             })
                            print('                  Series ' + str(p+1) + ': ' + pathVariableName + '=' + str(pathVariable))
                            print(' ')
                        chartA.set_title ({'name': variableName + ' vs path coordinates'})
                        chartA.set_x_axis({'name': pathCoordinateName})
                        chartA.set_y_axis({'name': variableName})
                        print('             Title: ' + variableName + ' vs path coordinates')
                        print('             x axis: ' + pathCoordinateName)
                        print('             y axis: ' + variableName)
                        print(' ')
                        print(' ')
                        graphworksheet.insert_chart(v*20,0,chartA)
                        chartB = verticalpathsStrainWorkbook.add_chart({'type': 'scatter','subtype': 'straight_with_markers'})
                        print('        Chart ' + str(v+1) + '.A')
                        print(' ')
                        for p, pathVariable in enumerate(pathVariables):
                            dataLength = len(pathCoords[p])
                            chartB.add_series({
                                            'name':       pathVariableName + '=' + str(pathVariable),
                                            'categories': [datasheetName,3,25*p+1,dataLength,25*p+1],
                                            'values':     [datasheetName,3,2+v,dataLength,2+v],
                                             })
                            print('                  Series ' + str(p+1) + ': ' + pathVariableName + '=' + str(pathVariable))
                            print(' ')
                        chartB.set_title ({'name': variableName + ' vs normalized path coordinates'})
                        chartB.set_x_axis({'name': 'Norm ' + pathCoordinateName.split(' ')[0] + ' [-]'})
                        chartB.set_y_axis({'name': variableName})
                        print('             Title: ' + variableName + ' vs path coordinates')
                        print('             x axis: ' + 'Norm ' + pathCoordinateName.split(' ')[0] + ' [-]')
                        print('             y axis: ' + variableName)
                        print(' ')
                        print(' ')
                        graphworksheet.insert_chart(v*20,30,chartB)

                    EExx = []
                    EEyy = []
                    EEzz = []
                    EExy = []
                    EEzx = []
                    EEyz = []
                    EErr = []
                    EEtt = []
                    EErt = []
                    EE1D3 = []
                    EE2D3 = []
                    EE3D3 = []
                    EEI1D3 = []
                    EEI2D3 = []
                    EEI3D3 = []
                    EEMisesD3 = []
                    EEaverD3 = []
                    EE1D2 = []
                    EE2D2 = []
                    EEI1D2 = []
                    EEI2D2 = []
                    EEMisesD2 = []
                    EEaverD2 = []
                    pathVariables = []
                    pathStartVariables = []
                    pathEndVariables = []
                    pathCoords = []
                    pathNormCoords = []
                    print('<-----------------')
                    print('<-----------------')


            pathVariableName = 'pathAngle [deg]'
            pathCoordinateName = 'R [mum]'
            for n in range(0,min(numberOfRadialpaths)):
                graphsheetName = 'Graphs, path n. ' + str(n)
                graphworksheet = radialpathsWorkbook.add_worksheet(graphsheetName.decode('utf-8'))
                print('    --> Writing worksheet')
                print('        ' + graphsheetName)
                print(' ')
                variableNames = ['Sxx [MPa]','Syy [MPa]','Szz [MPa]','Sxy [MPa]','Szx [MPa]','Syz [MPa]','Srr [MPa]','Stt [MPa]','Srt [MPa]','S1_3D [MPa]','S2_3D [MPa]','S3_3D [MPa]','S1_2D [MPa]','S2_2D [MPa]','Smises_3D [MPa]','Smises_2D [MPa]','Saverage_3D [MPa]','Saverage_2D [MPa]','I1_3D [MPa]','I2_3D [MPa^2]','I3_3D [MPa^3]','I1_2D [MPa]','I2_2D [MPa^2]']
                for v,variableName in enumerate(variableNames):
                    chartA = radialpathsWorkbook.add_chart({'type': 'scatter','subtype': 'straight_with_markers'})
                    print('        Chart ' + str(v+1) + '.A')
                    for s,subFolder in enumerate(subfoldersList):
                        dataLength = radialpathsDatalengths[s]
                        datasheetName = 'Values, deltatheta=' + subFolder.split('deltatheta')[-1].replace('_','.')
                        chartA.add_series({
                                        'name':       'deltatheta' + '=' + subFolder.split('deltatheta')[-1].replace('_','.'),
                                        'categories': [datasheetName,3,n*25,dataLength,n*25],
                                        'values':     [datasheetName,3,n*25+2+v,dataLength,n*25+2+v],
                                         })
                        print('                  Series ' + str(s+1) + ': ' + 'deltatheta' + '=' + subFolder.split('deltatheta')[-1].replace('_','.'))
                        print(' ')
                    chartA.set_title ({'name': variableName + ' vs path coordinates'})
                    chartA.set_x_axis({'name': pathCoordinateName})
                    chartA.set_y_axis({'name': variableName})
                    print('             Title: ' + variableName + ' vs path coordinates')
                    print('             x axis: ' + pathCoordinateName)
                    print('             y axis: ' + variableName)
                    print(' ')
                    print(' ')
                    graphworksheet.insert_chart(v*20,0,chartA)
                    chartB = radialpathsWorkbook.add_chart({'type': 'scatter','subtype': 'straight_with_markers'})
                    print('        Chart ' + str(v+1) + '.B')
                    print(' ')
                    for s,subFolder in enumerate(subfoldersList):
                        dataLength = radialpathsDatalengths[s]
                        datasheetName = 'Values, deltatheta=' + subFolder.split('deltatheta')[-1].replace('_','.')
                        chartB.add_series({
                                        'name':       'deltatheta' + '=' + subFolder.split('deltatheta')[-1].replace('_','.'),
                                        'categories': [datasheetName,3,n*25+1,dataLength,n*25+1],
                                        'values':     [datasheetName,3,n*25+2+v,dataLength,n*25+2+v],
                                         })
                        print('                  Series ' + str(s+1) + ': ' + 'deltatheta' + '=' + subFolder.split('deltatheta')[-1].replace('_','.'))
                        print(' ')
                    chartB.set_title ({'name': variableName + ' vs normalized path coordinates'})
                    chartB.set_x_axis({'name': 'Norm ' + pathCoordinateName.split(' ')[0] + ' [-]'})
                    chartB.set_y_axis({'name': variableName})
                    print('             Title: ' + variableName + ' vs path coordinates')
                    print('             x axis: ' + 'Norm ' + pathCoordinateName.split(' ')[0] + ' [-]')
                    print('             y axis: ' + variableName)
                    print(' ')
                    print(' ')
                    graphworksheet.insert_chart(v*20,30,chartB)

            pathVariableName = 'pathRadius [mum]'
            pathCoordinateName = 'angle [deg]'
            for n in range(0,min(numberOfCircumferentialpaths)):
                graphsheetName = 'Graphs, path n. ' + str(n)
                graphworksheet = circumferentialpathsWorkbook.add_worksheet(graphsheetName.decode('utf-8'))
                print('    --> Writing worksheet')
                print('        ' + graphsheetName)
                print(' ')
                variableNames = ['Sxx [MPa]','Syy [MPa]','Szz [MPa]','Sxy [MPa]','Szx [MPa]','Syz [MPa]','Srr [MPa]','Stt [MPa]','Srt [MPa]','S1_3D [MPa]','S2_3D [MPa]','S3_3D [MPa]','S1_2D [MPa]','S2_2D [MPa]','Smises_3D [MPa]','Smises_2D [MPa]','Saverage_3D [MPa]','Saverage_2D [MPa]','I1_3D [MPa]','I2_3D [MPa^2]','I3_3D [MPa^3]','I1_2D [MPa]','I2_2D [MPa^2]']
                for v,variableName in enumerate(variableNames):
                    chartA = circumferentialpathsWorkbook.add_chart({'type': 'scatter','subtype': 'straight_with_markers'})
                    print('        Chart ' + str(v+1) + '.A')
                    print(' ')
                    for s,subFolder in enumerate(subfoldersList):
                        dataLength = circumferentialpathsDatalengths[s]
                        datasheetName = 'Values, deltatheta=' + subFolder.split('deltatheta')[-1].replace('_','.')
                        chartA.add_series({
                                        'name':       'deltatheta' + '=' + subFolder.split('deltatheta')[-1].replace('_','.'),
                                        'categories': [datasheetName,3,n*25,dataLength,n*25],
                                        'values':     [datasheetName,3,n*25+2+v,dataLength,n*25+2+v],
                                         })
                        print('                  Series ' + str(s+1) + ': ' + 'deltatheta' + '=' + subFolder.split('deltatheta')[-1].replace('_','.'))
                        print(' ')
                    chartA.set_title ({'name': variableName + ' vs path coordinates'})
                    chartA.set_x_axis({'name': pathCoordinateName})
                    chartA.set_y_axis({'name': variableName})
                    print('             Title: ' + variableName + ' vs path coordinates')
                    print('             x axis: ' + pathCoordinateName)
                    print('             y axis: ' + variableName)
                    print(' ')
                    print(' ')
                    graphworksheet.insert_chart(v*20,0,chartA)
                    chartB = circumferentialpathsWorkbook.add_chart({'type': 'scatter','subtype': 'straight_with_markers'})
                    print('        Chart ' + str(v+1) + '.B')
                    print(' ')
                    for s,subFolder in enumerate(subfoldersList):
                        dataLength = circumferentialpathsDatalengths[s]
                        datasheetName = 'Values, deltatheta=' + subFolder.split('deltatheta')[-1].replace('_','.')
                        chartB.add_series({
                                        'name':       'deltatheta' + '=' + subFolder.split('deltatheta')[-1].replace('_','.'),
                                        'categories': [datasheetName,3,n*25+1,dataLength,n*25+1],
                                        'values':     [datasheetName,3,n*25+2+v,dataLength,n*25+2+v],
                                         })
                        print('                  Series ' + str(s+1) + ': ' + 'deltatheta' + '=' + subFolder.split('deltatheta')[-1].replace('_','.'))
                        print(' ')
                    chartB.set_title ({'name': variableName + ' vs normalized path coordinates'})
                    chartB.set_x_axis({'name': 'Norm ' + pathCoordinateName.split(' ')[0] + ' [-]'})
                    chartB.set_y_axis({'name': variableName})
                    print('             Title: ' + variableName + ' vs path coordinates')
                    print('             x axis: ' + 'Norm ' + pathCoordinateName.split(' ')[0] + ' [-]')
                    print('             y axis: ' + variableName)
                    print(' ')
                    print(' ')
                    graphworksheet.insert_chart(v*20,30,chartB)

            pathVariableName = 'y [mum]'
            pathCoordinateName = 'x [mum]'
            for n in range(0,min(numberOfHorizontalpaths)):
                graphsheetName = 'Graphs, path n. ' + str(n)
                graphworksheet = horizontalpathsWorkbook.add_worksheet(graphsheetName.decode('utf-8'))
                print('    --> Writing worksheet')
                print('        ' + graphsheetName)
                print(' ')
                variableNames = ['Sxx [MPa]','Syy [MPa]','Szz [MPa]','Sxy [MPa]','Szx [MPa]','Syz [MPa]','Srr [MPa]','Stt [MPa]','Srt [MPa]','S1_3D [MPa]','S2_3D [MPa]','S3_3D [MPa]','S1_2D [MPa]','S2_2D [MPa]','Smises_3D [MPa]','Smises_2D [MPa]','Saverage_3D [MPa]','Saverage_2D [MPa]','I1_3D [MPa]','I2_3D [MPa^2]','I3_3D [MPa^3]','I1_2D [MPa]','I2_2D [MPa^2]']
                for v,variableName in enumerate(variableNames):
                    chartA = horizontalpathsWorkbook.add_chart({'type': 'scatter','subtype': 'straight_with_markers'})
                    print('        Chart ' + str(v+1) + '.A')
                    print(' ')
                    for s,subFolder in enumerate(subfoldersList):
                        dataLength = horizontalpathsDatalengths[s]
                        datasheetName = 'Values, deltatheta=' + subFolder.split('deltatheta')[-1].replace('_','.')
                        chartA.add_series({
                                        'name':       'deltatheta' + '=' + subFolder.split('deltatheta')[-1].replace('_','.'),
                                        'categories': [datasheetName,3,n*25,dataLength,n*25],
                                        'values':     [datasheetName,3,n*25+2+v,dataLength,n*25+2+v],
                                         })
                        print('                  Series ' + str(s+1) + ': ' + 'deltatheta' + '=' + subFolder.split('deltatheta')[-1].replace('_','.'))
                        print(' ')
                    chartA.set_title ({'name': variableName + ' vs path coordinates'})
                    chartA.set_x_axis({'name': pathCoordinateName})
                    chartA.set_y_axis({'name': variableName})
                    print('             Title: ' + variableName + ' vs path coordinates')
                    print('             x axis: ' + pathCoordinateName)
                    print('             y axis: ' + variableName)
                    print(' ')
                    print(' ')
                    graphworksheet.insert_chart(v*20,0,chartA)
                    chartB = horizontalpathsWorkbook.add_chart({'type': 'scatter','subtype': 'straight_with_markers'})
                    print('        Chart ' + str(v+1) + '.B')
                    print(' ')
                    for s,subFolder in enumerate(subfoldersList):
                        dataLength = horizontalpathsDatalengths[s]
                        datasheetName = 'Values, deltatheta=' + subFolder.split('deltatheta')[-1].replace('_','.')
                        chartB.add_series({
                                        'name':       'deltatheta' + '=' + subFolder.split('deltatheta')[-1].replace('_','.'),
                                        'categories': [datasheetName,3,n*25+1,dataLength,n*25+1],
                                        'values':     [datasheetName,3,n*25+2+v,dataLength,n*25+2+v],
                                         })
                        print('                  Series ' + str(s+1) + ': ' + 'deltatheta' + '=' + subFolder.split('deltatheta')[-1].replace('_','.'))
                        print(' ')
                    chartB.set_title ({'name': variableName + ' vs normalized path coordinates'})
                    chartB.set_x_axis({'name': 'Norm ' + pathCoordinateName.split(' ')[0] + ' [-]'})
                    chartB.set_y_axis({'name': variableName})
                    print('             Title: ' + variableName + ' vs path coordinates')
                    print('             x axis: ' + 'Norm ' + pathCoordinateName.split(' ')[0] + ' [-]')
                    print('             y axis: ' + variableName)
                    print(' ')
                    print(' ')
                    graphworksheet.insert_chart(v*20,30,chartB)

            pathVariableName = 'x [mum]'
            pathCoordinateName = 'y [mum]'
            for n in range(0,min(numberOfVerticalpaths)):
                graphsheetName = 'Graphs, path n. ' + str(n)
                graphworksheet = verticalpathsWorkbook.add_worksheet(graphsheetName.decode('utf-8'))
                print('    --> Writing worksheet')
                print('        ' + graphsheetName)
                print(' ')
                variableNames = ['Sxx [MPa]','Syy [MPa]','Szz [MPa]','Sxy [MPa]','Szx [MPa]','Syz [MPa]','Srr [MPa]','Stt [MPa]','Srt [MPa]','S1_3D [MPa]','S2_3D [MPa]','S3_3D [MPa]','S1_2D [MPa]','S2_2D [MPa]','Smises_3D [MPa]','Smises_2D [MPa]','Saverage_3D [MPa]','Saverage_2D [MPa]','I1_3D [MPa]','I2_3D [MPa^2]','I3_3D [MPa^3]','I1_2D [MPa]','I2_2D [MPa^2]']
                for v,variableName in enumerate(variableNames):
                    chartA = verticalpathsWorkbook.add_chart({'type': 'scatter','subtype': 'straight_with_markers'})
                    print('        Chart ' + str(v+1) + '.A')
                    print(' ')
                    for s,subFolder in enumerate(subfoldersList):
                        dataLength = verticalpathsDatalengths[s]
                        datasheetName = 'Values, deltatheta=' + subFolder.split('deltatheta')[-1].replace('_','.')
                        chartA.add_series({
                                        'name':       'deltatheta' + '=' + subFolder.split('deltatheta')[-1].replace('_','.'),
                                        'categories': [datasheetName,3,n*25,dataLength,n*25],
                                        'values':     [datasheetName,3,n*25+2+v,dataLength,n*25+2+v],
                                         })
                        print('                  Series ' + str(s+1) + ': ' + 'deltatheta' + '=' + subFolder.split('deltatheta')[-1].replace('_','.'))
                        print(' ')
                    chartA.set_title ({'name': variableName + ' vs path coordinates'})
                    chartA.set_x_axis({'name': pathCoordinateName})
                    chartA.set_y_axis({'name': variableName})
                    print('             Title: ' + variableName + ' vs path coordinates')
                    print('             x axis: ' + pathCoordinateName)
                    print('             y axis: ' + variableName)
                    print(' ')
                    print(' ')
                    graphworksheet.insert_chart(v*20,0,chartA)
                    chartB = verticalpathsWorkbook.add_chart({'type': 'scatter','subtype': 'straight_with_markers'})
                    print('        Chart ' + str(v+1) + '.B')
                    print(' ')
                    for s,subFolder in enumerate(subfoldersList):
                        dataLength = verticalpathsDatalengths[s]
                        datasheetName = 'Values, deltatheta=' + subFolder.split('deltatheta')[-1].replace('_','.')
                        chartB.add_series({
                                        'name':       'deltatheta' + '=' + subFolder.split('deltatheta')[-1].replace('_','.'),
                                        'categories': [datasheetName,3,n*25+1,dataLength,n*25+1],
                                        'values':     [datasheetName,3,n*25+2+v,dataLength,n*25+2+v],
                                         })
                        print('                  Series ' + str(s+1) + ': ' + 'deltatheta' + '=' + subFolder.split('deltatheta')[-1].replace('_','.'))
                        print(' ')
                    chartB.set_title ({'name': variableName + ' vs normalized path coordinates'})
                    chartB.set_x_axis({'name': 'Norm ' + pathCoordinateName.split(' ')[0] + ' [-]'})
                    chartB.set_y_axis({'name': variableName})
                    print('             Title: ' + variableName + ' vs path coordinates')
                    print('             x axis: ' + 'Norm ' + pathCoordinateName.split(' ')[0] + ' [-]')
                    print('             y axis: ' + variableName)
                    print(' ')
                    print(' ')
                    graphworksheet.insert_chart(v*20,30,chartB)


            print('    Close workbook ' + join(outdir,outputfileBasename + '-radialpathsData' + '.xlsx'))
            radialpathsWorkbook.close()
            print('Workbook closed.')

            print('    Close workbook ' + join(outdir,outputfileBasename + '-circumferentialpathsData' + '.xlsx'))
            circumferentialpathsWorkbook.close()
            print('Workbook closed.')

            print('    Close workbook ' + join(outdir,outputfileBasename + '-horizontalpathsData' + '.xlsx'))
            horizontalpathsWorkbook.close()
            print('Workbook closed.')

            print('    Close workbook ' + join(outdir,outputfileBasename + '-verticalpathsData' + '.xlsx'))
            verticalpathsWorkbook.close()
            print('Workbook closed.')

            print('    Close workbook ' + join(outdir,outputfileBasename + '-radialpathsStrainData' + '.xlsx'))
            radialpathsStrainWorkbook.close()
            print('Workbook closed.')

            print('    Close workbook ' + join(outdir,outputfileBasename + '-circumferentialpathsStrainData' + '.xlsx'))
            circumferentialpathsStrainWorkbook.close()
            print('Workbook closed.')

            print('    Close workbook ' + join(outdir,outputfileBasename + '-horizontalpathsStrainData' + '.xlsx'))
            horizontalpathsStrainWorkbook.close()
            print('Workbook closed.')

            print('    Close workbook ' + join(outdir,outputfileBasename + '-verticalpathsStrainData' + '.xlsx'))
            verticalpathsStrainWorkbook.close()
            print('Workbook closed.')

    if toLatex: # only for errts file

        if not os.path.exists(join(reportFolder,'pics')):
                os.mkdir(join(reportFolder,'pics'))

        copyfile(join('D:/01_Luca/06_WD/thinPlyMechanics/tex/Templates/Template_reports','Docmase_logo.jpg'),join(reportFolder,'pics','Docmase_logo.jpg'))
        copyfile(join('D:/01_Luca/06_WD/thinPlyMechanics/tex/Templates/Template_reports','erasmusmundus_logo.jpg'),join(reportFolder,'pics','erasmusmundus_logo.jpg'))
        copyfile(join('D:/01_Luca/06_WD/thinPlyMechanics/tex/Templates/Template_slides','logo-eeigm.jpg'),join(reportFolder,'pics','logo-eeigm.jpg'))
        copyfile(join('D:/01_Luca/06_WD/thinPlyMechanics/tex/Templates/Template_reports','lulea_logo1.jpg'),join(reportFolder,'pics','lulea_logo1.jpg'))

        matrixProps = provideMatrixProperties()

        G0meanstress = []
        G0planestrainstress = []
        G0planestrainstressharmonic = []
        G0planestrainstressrve = []
        G0meanstressharmonic = []
        G0meanstressrve = []
        G0strain = []
        G0strainharmonic = []
        G0strainrve = []
        GIvcctonly = []
        GIIvcctonly = []
        GTOTvcctonly = []
        GIvcctjint = []
        GIIvcctjint = []
        GTOTvcctjint = []
        deltatheta = []
        LoverRf = []
        Vff = []
        phiCZ = []
        Y0atbound = []
        sigmaXXatbound = []
        sigmaZZatbound = []
        sigmaXZatbound = []

        currentG0meanstress = []
        currentG0planestrainstress = []
        currentG0planestrainstressharmonic = []
        currentG0planestrainstressrve = []
        currentG0meanstressharmonic = []
        currentG0meanstressrve = []
        currentG0strain = []
        currentG0strainharmonic = []
        currentG0strainrve = []
        currentGIvcctonly = []
        currentGIIvcctonly = []
        currentGTOTvcctonly = []
        currentGIvcctjint = []
        currentGIIvcctjint = []
        currentGTOTvcctjint = []
        currentdeltatheta = []
        currentLoverRf = []
        currentVff = []
        currentphiCZ = []
        currentY0atbound = []
        currentsigmaXXatbound = []
        currentsigmaZZatbound = []
        currentsigmaXZatbound = []
        for line in lines[1:]:
            csvPath = line.replace('\n','').split(',')[1]
            inputdataPath = '_'.join(line.replace('\n','').split(',')[1].split('_')[:-1]) + '_InputData' + '.csv'
            dataType = line.replace('\n','').split(',')[0]
            try:
                with open(csvPath,'r') as csv:
                    csvlines = csv.readlines()
            except Exception,error:
                continue
                sys.exc_clear()
            try:
                with open(inputdataPath,'r') as csv:
                    inputdatalines = csv.readlines()
            except Exception,error:
                continue
                sys.exit(2)
            if 'ERRT' in dataType or 'ERRTS' in dataType or 'ERRTs' in dataType or 'errt' in dataType or 'errts' in dataType:
                epsxx = float(inputdatalines[1].replace('\n','').split(',')[5])
                Rf = float(inputdatalines[1].replace('\n','').split(',')[0])
                for c,csvline in enumerate(csvlines[1:]):
                    values = csvline.replace('\n','').split(',')
                    if len(currentLoverRf)>0:
                        if float(values[3])!=currentLoverRf[-1]:
                            G0meanstress.append(currentG0meanstress)
                            G0planestrainstress.append(currentG0planestrainstress)
                            G0planestrainstressharmonic.append(currentG0planestrainstressharmonic)
                            G0planestrainstressrve.append(currentG0planestrainstressrve)
                            G0meanstressharmonic.append(currentG0meanstressharmonic)
                            G0meanstressrve.append(currentG0meanstressrve)
                            G0strain.append(currentG0strain)
                            G0strainharmonic.append(currentG0strainharmonic)
                            G0strainrve.append(currentG0strainrve)
                            GIvcctonly.append(currentGIvcctonly)
                            GIIvcctonly.append(currentGIIvcctonly)
                            GTOTvcctonly.append(currentGTOTvcctonly)
                            GIvcctjint.append(currentGIvcctjint)
                            GIIvcctjint.append(currentGIIvcctjint)
                            GTOTvcctjint.append(currentGTOTvcctjint)
                            deltatheta.append(currentdeltatheta)
                            LoverRf.append(currentLoverRf)
                            Vff.append(currentVff)
                            phiCZ.append(currentphiCZ)
                            currentG0stress = []
                            currentG0strain = []
                            currentGIvcctonly = []
                            currentGIIvcctonly = []
                            currentGTOTvcctonly = []
                            currentGIvcctjint = []
                            currentGIIvcctjint = []
                            currentGTOTvcctjint = []
                            currentdeltatheta = []
                            currentLoverRf = []
                            currentVff = []
                            currentphiCZ = []
                    currentG0meanstress.append(float(values[5]))
                    currentG0planestrainstress.append(np.pi*Rf*(matrixProps['E']*epsxx/(1-matrixProps['nu']*matrixProps['nu']))*(matrixProps['E']*epsxx/(1-matrixProps['nu']*matrixProps['nu']))*(1+matrixProps['k-planestrain'])/(8.0*matrixProps['G']))
                    currentG0planestrainstressharmonic.append()
                    currentG0planestrainstressrve.append()
                    currentG0meanstressharmonic.append()
                    currentG0meanstressrve.append()
                    currentG0strain.append(np.pi*Rf*(matrixProps['E']/(1-matrixProps['nu']*matrixProps['nu']))*epsxx*epsxx)
                    currentG0strainharmonic.append()
                    currentG0strainrve.append()
                    currentGIvcctonly.append(float(values[13]))
                    currentGIIvcctonly.append(float(values[14]))
                    currentGTOTvcctonly.append(float(values[15]))
                    currentGIvcctjint.append(float(values[16]))
                    currentGIIvcctjint.append(float(values[17]))
                    currentGTOTvcctjint.append(float(values[18]))
                    currentdeltatheta.append(float(values[0]))
                    currentLoverRf.append(float(values[3]))
                    currentVff.append(0.25*np.pi/float(values[3]))
                    currentphiCZ.append(float(values[4]))
            elif 'stressesatboundary' in dataType or 'StressesAtBoundary' in dataType or 'stresses-at-boundary' in dataType or 'Stresses-At-Boundary' in dataType:
                for c,csvline in enumerate(csvlines[1:]):
                    values = csvline.replace('\n','').split(',')
                    currentY0atbound.append(values[1])
                    currentsigmaXXatbound.append(values[4])
                    currentsigmaZZatbound.append(values[5])
                    currentsigmaXZatbound.append(values[7])

        for s,valueSet in enumerate(GIvcctonly):
            currentVff = Vff[s][0]
            currentLoverRf = LoverRf[s][0]
            debondSize = np.array(deltatheta[s])
            CZsize = np.array(phiCZ[s])
            GI = [np.array(GIvcctonly[s]),np.array(GIvcctjint[s])]
            GII = [np.array(GIIvcctonly[s]),np.array(GIIvcctjint[s])]
            GTOT = [np.array(GTOTvcctonly[s]),np.array(GTOTvcctjint[s])]
            gMethod = ['VCCT only','VCCT/J-integral']
            G0s = [G0meanstress[s],G0planestrainstress[s],G0strain[s]]
            legendEntries = '{$GI/G0-FEM$,$GII/G0-FEM$,$GTOT/G0-FEM$,$GI/G0-BEM$,$GII/G0-BEM$,$GTOT/G0-BEM$}'
            dataoptions = ['red,smooth,mark=square*',
                           'red,smooth,mark=triangle*',
                           'red,smooth,mark=*',
                           'black,smooth,mark=square*',
                           'black,smooth,mark=triangle*',
                           'black,smooth,mark=*',]
            bemDSize = BEMdata['normGs'][:,0]
            bemGI = BEMdata['normGs'][:,1]
            bemGII = BEMdata['normGs'][:,2]
            bemGTOT = BEMdata['normGs'][:,3]
            for m,method in enumerate(gMethod):
                titles = ['\\bf{Normalized Energy Release Rate, '+method+', $Vf_{f}='+str(currentVff)+'$, $\\frac{L}{R_{f}}='+str(currentLoverRf)+'$, $G_{0}=\\frac{1+k_{m}}{8G_{m}}\\pi R_{f}\\left(\\frac{1}{2L}\\int_{-L}^{+L}\\sigma_{xx}\\left(L,z\\right)dz\\right)^{2}$}',
                          '\\bf{Normalized Energy Release Rate, '+method+', $Vf_{f}='+str(currentVff)+'$, $\\frac{L}{R_{f}}='+str(currentLoverRf)+'$, $G_{0}=\\frac{1+k_{m}}{8G_{m}}\\pi R_{f}\\left(\\frac{E_{m}}{1-\\nu^{2}}\\varepsilon_{xx}\\right)^{2}$}',
                          '\\bf{Normalized Energy Release Rate, '+method+', $Vf_{f}='+str(currentVff)+'$, $\\frac{L}{R_{f}}='+str(currentLoverRf)+'$, $G_{0}=\\frac{E_{m}}{1-\\nu^{2}}\\pi R_{f}\\varepsilon_{xx}^{2}$}']
                fileoptionName = ['G0-mean-stress',
                                  'G0-plane-strain-stress',
                                  'G0-strain']
                for g,G0 in enumerate(G0s):
                    normGI = GI[m]/GO
                    normGII = GII[m]/GO
                    normGTOT = GTOT[m]/GO
                    xyData = []
                    xyData.append(np.transpose(np.array([debondSize,normGI])))
                    xyData.append(np.transpose(np.array([debondSize,normGII])))
                    xyData.append(np.transpose(np.array([debondSize,normGTOT])))
                    xyData.append(np.transpose(np.array([bemDSize,bemGI])))
                    xyData.append(np.transpose(np.array([bemDSize,bemGII])))
                    xyData.append(np.transpose(np.array([bemDSize,bemGTOT])))
                    axisoptions = 'width=30cm,\n ' \
                                  'title={'+titles[g]+'},\n ' \
                                  'title style={font=\\fontsize{40}{8}\\selectfont},\n ' \
                                  'xlabel style={at={(axis description cs:0.5,-0.02)},anchor=north,font=\\fontsize{44}{40}\\selectfont},\n ' \
                                  'ylabel style={at={(axis description cs:-0.025,.5)},anchor=south,font=\\fontsize{44}{40}\\selectfont},\n ' \
                                  'xlabel={$\\Delta\\theta\\left[^{\\circ}\\right]$},ylabel={$\\frac{G_{\\left(\\cdot\\cdot\\right)}}{G_{0}}\\left[-\\right]$},\n ' \
                                  'xmin=' + str(0.0) + ',\n ' \
                                  'xmax=' + str(160.0) + ',\n ' \
                                  'ymin=' + str(0.0) + ',\n ' \
                                  'ymax=' + str([np.max(normGTOT),np.max(bemGTOT)]) + ',\n ' \
                                  'tick align=outside,\n ' \
                                  'tick label style={font=\\huge},\n ' \
                                  'xmajorgrids,\n ' \
                                  'xtick={0.0,10.0,20.0,30.0,40.0,50.0,60.0,70.0,80.0,90.0,100.0,110.0,120.0,130.0,140.0,150.0,160.0,170.0,180.0},\n ' \
                                  'x grid style={lightgray!92.026143790849673!black},\n ' \
                                  'ymajorgrids,\n ' \
                                  'y grid style={lightgray!92.026143790849673!black},\n ' \
                                  'line width=0.5mm,\n ' \
                                  'legend style={draw=white!80.0!black,font=\\fontsize{28}{24}\\selectfont,row sep=15pt},\n ' \
                                  'legend entries={' + legendEntries + '},\n ' \
                                  'legend image post style={xscale=2},\n ' \
                                  'legend cell align={left}'
                    writeLatexMultiplePlots(outDir,'Gs-SUMMARY_Vff'+str(currentVff)+'-'+method.replace(' ','-').replace('/','-')+'-'+fileoptionName[g]+'.tex',xyData,axisoptions,dataoptions)
            titles = ['\\bf{Normalized Mode I Energy Release Rate, $Vf_{f}='+str(currentVff)+'$, $\\frac{L}{R_{f}}='+str(currentLoverRf)+'$, $G_{0}=\\frac{1+k_{m}}{8G_{m}}\\pi R_{f}\\left(\\frac{1}{2L}\\int_{-L}^{+L}\\sigma_{xx}\\left(L,z\\right)dz\\right)^{2}$}',
                      '\\bf{Normalized Mode I Energy Release Rate, $Vf_{f}='+str(currentVff)+'$, $\\frac{L}{R_{f}}='+str(currentLoverRf)+'$, $G_{0}=\\frac{1+k_{m}}{8G_{m}}\\pi R_{f}\\left(\\frac{E_{m}}{1-\\nu^{2}}\\varepsilon_{xx}\\right)^{2}$}',
                      '\\bf{Normalized Mode I Energy Release Rate, $Vf_{f}='+str(currentVff)+'$, $\\frac{L}{R_{f}}='+str(currentLoverRf)+'$, $G_{0}=\\frac{E_{m}}{1-\\nu^{2}}\\pi R_{f}\\varepsilon_{xx}^{2}$}']
            fileoptionName = ['G0-mean-stress',
                              'G0-plane-strain-stress',
                              'G0-strain']
            legendEntries = '{$GI/G0-FEM,VCCT only$,$GI/G0-FEM,VCCT/J-integral$,$GI/G0-BEM$}'
            dataoptions = ['red,smooth,mark=square*',
                           'blue,smooth,mark=square*',
                           'black,smooth,mark=square*']
            for g,G0 in enumerate(G0s):
                xyData = []
                for m,method in enumerate(gMethod):
                    normGI = GI[m]/GO
                    xyData.append(np.transpose(np.array([debondSize,normGI])))
                xyData.append(np.transpose(np.array([bemDSize,bemGI])))
                axisoptions = 'width=30cm,\n ' \
                              'title={'+titles[g]+'},\n ' \
                              'title style={font=\\fontsize{40}{8}\\selectfont},\n ' \
                              'xlabel style={at={(axis description cs:0.5,-0.02)},anchor=north,font=\\fontsize{44}{40}\\selectfont},\n ' \
                              'ylabel style={at={(axis description cs:-0.025,.5)},anchor=south,font=\\fontsize{44}{40}\\selectfont},\n ' \
                              'xlabel={$\\Delta\\theta\\left[^{\\circ}\\right]$},ylabel={$\\frac{G_{I}}{G_{0}}\\left[-\\right]$},\n ' \
                              'xmin=' + str(0.0) + ',\n ' \
                              'xmax=' + str(160.0) + ',\n ' \
                              'ymin=' + str(0.0) + ',\n ' \
                              'ymax=' + str(np.max([np.max(xyData[0][:,1]),np.max(xyData[1][:,1]),np.max(xyData[2][:,1])])) + ',\n ' \
                              'tick align=outside,\n ' \
                              'tick label style={font=\\huge},\n ' \
                              'xmajorgrids,\n ' \
                              'xtick={0.0,10.0,20.0,30.0,40.0,50.0,60.0,70.0,80.0,90.0,100.0,110.0,120.0,130.0,140.0,150.0,160.0,170.0,180.0},\n ' \
                              'x grid style={lightgray!92.026143790849673!black},\n ' \
                              'ymajorgrids,\n ' \
                              'y grid style={lightgray!92.026143790849673!black},\n ' \
                              'line width=0.5mm,\n ' \
                              'legend style={draw=white!80.0!black,font=\\fontsize{28}{24}\\selectfont,row sep=15pt},\n ' \
                              'legend entries={' + legendEntries + '},\n ' \
                              'legend image post style={xscale=2},\n ' \
                              'legend cell align={left}'
                writeLatexMultiplePlots(outDir,'GI-Method-Comparison_Vff'+str(currentVff)+'-'+fileoptionName[g]+'.tex',xyData,axisoptions,dataoptions)
            titles = ['\\bf{Normalized Mode II Energy Release Rate, $Vf_{f}='+str(currentVff)+'$, $\\frac{L}{R_{f}}='+str(currentLoverRf)+'$, $G_{0}=\\frac{1+k_{m}}{8G_{m}}\\pi R_{f}\\left(\\frac{1}{2L}\\int_{-L}^{+L}\\sigma_{xx}\\left(L,z\\right)dz\\right)^{2}$}',
                      '\\bf{Normalized Mode II Energy Release Rate, $Vf_{f}='+str(currentVff)+'$, $\\frac{L}{R_{f}}='+str(currentLoverRf)+'$, $G_{0}=\\frac{1+k_{m}}{8G_{m}}\\pi R_{f}\\left(\\frac{E_{m}}{1-\\nu^{2}}\\varepsilon_{xx}\\right)^{2}$}',
                      '\\bf{Normalized Mode II Energy Release Rate, $Vf_{f}='+str(currentVff)+'$, $\\frac{L}{R_{f}}='+str(currentLoverRf)+'$, $G_{0}=\\frac{E_{m}}{1-\\nu^{2}}\\pi R_{f}\\varepsilon_{xx}^{2}$}']
            fileoptionName = ['G0-mean-stress',
                              'G0-plane-strain-stress',
                              'G0-strain']
            legendEntries = '{$GII/G0-FEM,VCCT only$,$GII/G0-FEM,VCCT/J-integral$,$GII/G0-BEM$}'
            dataoptions = ['red,smooth,mark=triangle*',
                           'blue,smooth,mark=triangle*',
                           'black,smooth,mark=triangle*']
            for g,G0 in enumerate(G0s):
                xyData = []
                for m,method in enumerate(gMethod):
                    normGII = GII[m]/GO
                    xyData.append(np.transpose(np.array([debondSize,normGII])))
                xyData.append(np.transpose(np.array([bemDSize,bemGII])))
                axisoptions = 'width=30cm,\n ' \
                              'title={'+titles[g]+'},\n ' \
                              'title style={font=\\fontsize{40}{8}\\selectfont},\n ' \
                              'xlabel style={at={(axis description cs:0.5,-0.02)},anchor=north,font=\\fontsize{44}{40}\\selectfont},\n ' \
                              'ylabel style={at={(axis description cs:-0.025,.5)},anchor=south,font=\\fontsize{44}{40}\\selectfont},\n ' \
                              'xlabel={$\\Delta\\theta\\left[^{\\circ}\\right]$},ylabel={$\\frac{G_{II}}{G_{0}}\\left[-\\right]$},\n ' \
                              'xmin=' + str(0.0) + ',\n ' \
                              'xmax=' + str(160.0) + ',\n ' \
                              'ymin=' + str(0.0) + ',\n ' \
                              'ymax=' + str(np.max([np.max(xyData[0][:,1]),np.max(xyData[1][:,1]),np.max(xyData[2][:,1])])) + ',\n ' \
                              'tick align=outside,\n ' \
                              'tick label style={font=\\huge},\n ' \
                              'xmajorgrids,\n ' \
                              'xtick={0.0,10.0,20.0,30.0,40.0,50.0,60.0,70.0,80.0,90.0,100.0,110.0,120.0,130.0,140.0,150.0,160.0,170.0,180.0},\n ' \
                              'x grid style={lightgray!92.026143790849673!black},\n ' \
                              'ymajorgrids,\n ' \
                              'y grid style={lightgray!92.026143790849673!black},\n ' \
                              'line width=0.5mm,\n ' \
                              'legend style={draw=white!80.0!black,font=\\fontsize{28}{24}\\selectfont,row sep=15pt},\n ' \
                              'legend entries={' + legendEntries + '},\n ' \
                              'legend image post style={xscale=2},\n ' \
                              'legend cell align={left}'
                writeLatexMultiplePlots(outDir,'GII-Method-Comparison_Vff'+str(currentVff)+'-'+fileoptionName[g]+'.tex',xyData,axisoptions,dataoptions)
            titles = ['\\bf{Normalized Total Energy Release Rate, $Vf_{f}='+str(currentVff)+'$, $\\frac{L}{R_{f}}='+str(currentLoverRf)+'$, $G_{0}=\\frac{1+k_{m}}{8G_{m}}\\pi R_{f}\\left(\\frac{1}{2L}\\int_{-L}^{+L}\\sigma_{xx}\\left(L,z\\right)dz\\right)^{2}$}',
                      '\\bf{Normalized Total Energy Release Rate, $Vf_{f}='+str(currentVff)+'$, $\\frac{L}{R_{f}}='+str(currentLoverRf)+'$, $G_{0}=\\frac{1+k_{m}}{8G_{m}}\\pi R_{f}\\left(\\frac{E_{m}}{1-\\nu^{2}}\\varepsilon_{xx}\\right)^{2}$}',
                      '\\bf{Normalized Total Energy Release Rate, $Vf_{f}='+str(currentVff)+'$, $\\frac{L}{R_{f}}='+str(currentLoverRf)+'$, $G_{0}=\\frac{E_{m}}{1-\\nu^{2}}\\pi R_{f}\\varepsilon_{xx}^{2}$}']
            fileoptionName = ['G0-mean-stress',
                              'G0-plane-strain-stress',
                              'G0-strain']
            legendEntries = '{$GTOT/G0-FEM,VCCT only$,$GTOT/G0-FEM,VCCT/J-integral$,$GTOT/G0-BEM$}'
            dataoptions = ['red,smooth,mark=*',
                           'blue,smooth,mark=*',
                           'black,smooth,mark=*']
            for g,G0 in enumerate(G0s):
                xyData = []
                for m,method in enumerate(gMethod):
                    normGTOT = GTOT[m]/GO
                    xyData.append(np.transpose(np.array([debondSize,normGTOT])))
                xyData.append(np.transpose(np.array([bemDSize,bemGTOT])))
                axisoptions = 'width=30cm,\n ' \
                              'title={'+titles[g]+'},\n ' \
                              'title style={font=\\fontsize{40}{8}\\selectfont},\n ' \
                              'xlabel style={at={(axis description cs:0.5,-0.02)},anchor=north,font=\\fontsize{44}{40}\\selectfont},\n ' \
                              'ylabel style={at={(axis description cs:-0.025,.5)},anchor=south,font=\\fontsize{44}{40}\\selectfont},\n ' \
                              'xlabel={$\\Delta\\theta\\left[^{\\circ}\\right]$},ylabel={$\\frac{G_{TOT}}{G_{0}}\\left[-\\right]$},\n ' \
                              'xmin=' + str(0.0) + ',\n ' \
                              'xmax=' + str(160.0) + ',\n ' \
                              'ymin=' + str(0.0) + ',\n ' \
                              'ymax=' + str(np.max([np.max(xyData[0][:,1]),np.max(xyData[1][:,1]),np.max(xyData[2][:,1])])) + ',\n ' \
                              'tick align=outside,\n ' \
                              'tick label style={font=\\huge},\n ' \
                              'xmajorgrids,\n ' \
                              'xtick={0.0,10.0,20.0,30.0,40.0,50.0,60.0,70.0,80.0,90.0,100.0,110.0,120.0,130.0,140.0,150.0,160.0,170.0,180.0},\n ' \
                              'x grid style={lightgray!92.026143790849673!black},\n ' \
                              'ymajorgrids,\n ' \
                              'y grid style={lightgray!92.026143790849673!black},\n ' \
                              'line width=0.5mm,\n ' \
                              'legend style={draw=white!80.0!black,font=\\fontsize{28}{24}\\selectfont,row sep=15pt},\n ' \
                              'legend entries={' + legendEntries + '},\n ' \
                              'legend image post style={xscale=2},\n ' \
                              'legend cell align={left}'
                writeLatexMultiplePlots(outDir,'GTOT-Method-Comparison_Vff'+str(currentVff)+'-'+fileoptionName[g]+'.tex',xyData,axisoptions,dataoptions)
            legendEntries = '{$Contact zone size$}'
            dataoptions = ['blue,smooth,mark=*']
            xyData = []
            xyData.append(np.transpose(np.array([debondSize,CZsize])))
            axisoptions = 'width=30cm,\n ' \
                          'title={Contact zone size as function of debond size},\n ' \
                          'title style={font=\\fontsize{40}{8}\\selectfont},\n ' \
                          'xlabel style={at={(axis description cs:0.5,-0.02)},anchor=north,font=\\fontsize{44}{40}\\selectfont},\n ' \
                          'ylabel style={at={(axis description cs:-0.025,.5)},anchor=south,font=\\fontsize{44}{40}\\selectfont},\n ' \
                          'xlabel={$\\Delta\\theta\\left[^{\\circ}\\right]$},ylabel={$\\Delta\\varphi\\left[^{\\circ}\\right]$},\n ' \
                          'xmin=' + str(0.0) + ',\n ' \
                          'xmax=' + str(160.0) + ',\n ' \
                          'ymin=' + str(0.0) + ',\n ' \
                          'ymax=' + str(np.max(CZsize)) + ',\n ' \
                          'tick align=outside,\n ' \
                          'tick label style={font=\\huge},\n ' \
                          'xmajorgrids,\n ' \
                          'xtick={0.0,10.0,20.0,30.0,40.0,50.0,60.0,70.0,80.0,90.0,100.0,110.0,120.0,130.0,140.0,150.0,160.0,170.0,180.0},\n ' \
                          'x grid style={lightgray!92.026143790849673!black},\n ' \
                          'ymajorgrids,\n ' \
                          'y grid style={lightgray!92.026143790849673!black},\n ' \
                          'line width=0.5mm,\n ' \
                          'legend style={draw=white!80.0!black,font=\\fontsize{28}{24}\\selectfont,row sep=15pt},\n ' \
                          'legend entries={' + legendEntries + '},\n ' \
                          'legend image post style={xscale=2},\n ' \
                          'legend cell align={left}'


if __name__ == "__main__":
    main(sys.argv[1:])
