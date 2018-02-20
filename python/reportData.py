#!/usr/bin/env Python
# -*- coding: utf-8 -*-

'''
=====================================================================================

Copyright (c) 2016 - 2018 Université de Lorraine & Luleå tekniska universitet
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

def writeLatexSinglePlot(folder,filename,data,axoptions,dataoptions,logfilepath,baselogindent,logindent):
    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + 'In function: writeLatexSinglePlot(folder,filename,data,axoptions,dataoptions,logfilepath,baselogindent,logindent)',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Create latex file',True)
    createLatexFile(folder,filename,'standalone')
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Write latex packages',True)
    writeLatexPackages(folder,filename,['inputenc','pgfplots','tikz'],['utf8','',''])
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Document starts',True)
    writeLatexDocumentStarts(folder,filename)
    writeLatexTikzPicStarts(folder,filename,'')
    writeLatexTikzAxisStarts(folder,filename,axoptions)
    writeLatexAddPlotTable(folder,filename,data,dataoptions)
    writeLatexTikzAxisEnds(folder,filename)
    writeLatexTikzPicEnds(folder,filename)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Document ends',True)
    writeLatexDocumentEnds(folder,filename)
    if 'Windows' in system():
        writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Create Windows command file',True)
        cmdfile = join(folder,filename,'runlatex.cmd')
        with open(cmdfile,'w') as cmd:
            cmd.write('\n')
            cmd.write('CD ' + folder + '\n')
            cmd.write('\n')
            cmd.write('pdflatex ' + join(folder,filename + '.tex') + ' -job-name=' + filename + '\n')
        writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Executing Windows command file...',True)
        try:
            subprocess.call('cmd.exe /C ' + cmdfile)
            writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
        except Exception:
            writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'ERROR',True)
            writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + str(Exception),True)
            writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + str(error),True)
            sys.exc_clear()
    elif 'Linux' in system():
        writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Create Linux bash file',True)
        bashfile = join(folder,filename,'runlatex.sh')
        with open(bashfile,'w') as bsh:
            bsh.write('#!/bin/bash\n')
            bsh.write('\n')
            bsh.write('cd ' + folder + '\n')
            bsh.write('\n')
            bsh.write('pdflatex ' + join(folder,filename + '.tex') + ' -job-name=' + filename + '\n')
            writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Executing Linux bash file...',True)
            try:
                writeLineToLogFile(logfilename,'a',baselogindent + 3*logindent + 'Change permissions to ' + bashfile ,True)
                os.chmod(bashfile, 0o755)
                writeLineToLogFile(logfilename,'a','Run bash file',True)
                rc = call('.' + bashfile)
                writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
            except Exception:
                writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'ERROR',True)
                writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + str(Exception),True)
                writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + str(error),True)
                sys.exc_clear()

def writeLatexMultiplePlots(folder,filename,data,axoptions,dataoptions,logfilepath,baselogindent,logindent):
    writeLineToLogFile(logfilepath,'a',baselogindent + logindent + 'In function: writeLatexMultiplePlots(folder,filename,data,axoptions,dataoptions,logfilepath,baselogindent,logindent)',True)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Create latex file',True)
    createLatexFile(folder,filename,'standalone')
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Write latex packages',True)
    writeLatexPackages(folder,filename,['inputenc','pgfplots','tikz'],['utf8','',''])
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Document starts',True)
    writeLatexDocumentStarts(folder,filename)
    writeLatexTikzPicStarts(folder,filename,'')
    writeLatexTikzAxisStarts(folder,filename,axoptions)
    for k,datum in enumerate(data):
        writeLatexAddPlotTable(folder,filename,datum,dataoptions[k])
    writeLatexTikzAxisEnds(folder,filename)
    writeLatexTikzPicEnds(folder,filename)
    writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Document ends',True)
    writeLatexDocumentEnds(folder,filename)
    if 'Windows' in system():
        writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Create Windows command file',True)
        cmdfile = join(folder,'runlatex.cmd')
        with open(cmdfile,'w') as cmd:
            cmd.write('\n')
            cmd.write('CD ' + folder + '\n')
            cmd.write('\n')
            cmd.write('pdflatex ' + join(folder,filename + '.tex') + ' -job-name=' + filename + '\n')
        writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Executing Windows command file...',True)
        try:
            subprocess.call('cmd.exe /C ' + cmdfile)
            writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
        except Exception,error:
            writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'ERROR',True)
            writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + str(Exception),True)
            writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + str(error),True)
            sys.exc_clear()
    elif 'Linux' in system():
        writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Create Linux bash file',True)
        bashfile = join(folder,filename,'runlatex.sh')
        with open(bashfile,'w') as bsh:
            bsh.write('#!/bin/bash\n')
            bsh.write('\n')
            bsh.write('cd ' + folder + '\n')
            bsh.write('\n')
            bsh.write('pdflatex ' + join(folder,filename + '.tex') + ' -job-name=' + filename + '\n')
            writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'Executing Linux bash file...',True)
            try:
                writeLineToLogFile(logfilename,'a',baselogindent + 3*logindent + 'Change permissions to ' + bashfile ,True)
                os.chmod(bashfile, 0o755)
                writeLineToLogFile(logfilename,'a','Run bash file',True)
                rc = call('.' + bashfile)
                writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + '... done.',True)
            except Exception:
                writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + 'ERROR',True)
                writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + str(Exception),True)
                writeLineToLogFile(logfilepath,'a',baselogindent + 2*logindent + str(error),True)
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
        elif opt in ("-e", "-excel"):
            toExcel = True
        elif opt in ("-l", "-latex"):
            toLatex = True
        elif opt in ("-d", "-sql"):
            toSql = True

    # Check the existence of variables: if a required variable is missing, an error is thrown and program is terminated; if an optional variable is missing, it is set to the default value
    if 'workdir' not in locals():
        print('Error: working directory not provided.')
        sys.exit()
    if 'inputfile' not in locals():
        print('Error: file list not provided.')
        sys.exit()
    if 'outputfile' not in locals():
        outputfileBasename = datetime.now().strftime('%Y-%m-%d') + '_' + datetime.now().strftime('%H-%M-%S') + '_' + inputfile.split(".")[0]
    if 'outdir' not in locals():
        outdir = workdir
    if 'toExcel' not in locals() and 'toLatex' not in locals() and 'toSql' not in locals():
        print('Error: no output format specified.')
        sys.exit()

    bemData = provideBEMdata()

    with open(join(workdir,inputfile),'r') as csv:
        lines = csv.readlines()

    if toExcel:
        workbook = xlsxwriter.Workbook(join(outdir,outputfileBasename + '.xlsx'))

        stringFormat = workbook.add_format({'bold': 1})
        numberFormat = workbook.add_format({'num_format': '0.000000'})

        bemdataSheetname = 'BEM-Data'
        worksheet = workbook.add_worksheet(bemdataSheetname)
        worksheet.write(0,0,'deltatheta [deg]',stringFormat)
        worksheet.write(0,1,'GI/G0 [-]',stringFormat)
        vworksheet.write(0,2,'GII/G0 [-]',stringFormat)
        worksheet.write(0,3,'GTOT/G0 [-]',stringFormat)
        for r,row in enumerate(bemData['normGs']):
            for c,value in enumerate(row):
                worksheet.write(r+1,c,value,numberFormat)

        for line in lines[1:]:
            csvPath = line.replace('\n','').split(',')[0]
            try:
                with open(csvPath,'r') as csv:
                    csvlines = csv.readlines()
            except Exception,error:
                continue
                sys.exc_clear()
            sheetName = line.replace('\n','').split(',')[1]
            toPlot = bool(line.replace('\n','').split(',')[2])
            plotSettings = []
            if toPlot:
                settingsString = ','.join(line.replace('\n','').split(',')[3:])
                plotSettings = ast.literal_eval(settingsString[1:])
            worksheet = workbook.add_worksheet(sheetName)
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
                        worksheet.write(c+1,e,str(element),numberFormat)
                        sys.exc_clear()
            for p,plot in enumerate(plotSettings):
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
                                        'name':       curve[2],
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
                chart.set_title ({'name': plot[-1]})
                chart.set_x_axis({'name': plot[-3]})
                chart.set_y_axis({'name': plot[-2]})
                worksheet.insert_chart(len(csvlines)+10,10*p, chart)

        workbook.close()

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
        G0strain = []
        GIvcctonly = []
        GIIvcctonly = []
        GTOTvcctonly = []
        GIvcctjint = []
        GIIvcctjint = []
        GTOTvcctjint = []
        LoverRf = []
        Vff = []
        phiCZ = []

        currentG0meanstress = []
        currentG0planestrainstress = []
        currentG0strain = []
        currentGIvcctonly = []
        currentGIIvcctonly = []
        currentGTOTvcctonly = []
        currentGIvcctjint = []
        currentGIIvcctjint = []
        currentGTOTvcctjint = []
        currentLoverRf = []
        currentVff = []
        currentphiCZ = []
        for line in lines[1:]:
            csvPath = line.replace('\n','').split(',')[0]
            inputdataPath = '_'.join(line.replace('\n','').split(',')[0].split('_')[:-1]) + '_InputData' + '.csv'
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
            epsxx = float(inputdatalines[1].replace('\n','').split(',')[5])
            Rf = float(inputdatalines[1].replace('\n','').split(',')[0])
            for c,csvline in enumerate(csvlines[1:]):
                values = csvline.replace('\n','').split(',')
                if len(currentLoverRf)>0:
                    if float(values[3])!=currentLoverRf[-1]:
                        G0meanstress.append(currentG0meanstress)
                        G0planestrainstress.append(currentG0planestrainstress)
                        G0strain.append(currentG0strain)
                        GIvcctonly.append(currentGIvcctonly)
                        GIIvcctonly.append(currentGIIvcctonly)
                        GTOTvcctonly.append(currentGTOTvcctonly)
                        GIvcctjint.append(currentGIvcctjint)
                        GIIvcctjint.append(currentGIIvcctjint)
                        GTOTvcctjint.append(currentGTOTvcctjint)
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
                        currentLoverRf = []
                        currentVff = []
                        currentphiCZ = []
                currentG0meanstress.append(float(values[5]))
                currentG0planestrainstress.append(np.pi*Rf*(matrixProps['E']*epsxx/(1-matrixProps['nu']*matrixProps['nu']))*(matrixProps['E']*epsxx/(1-matrixProps['nu']*matrixProps['nu']))*(1+matrixProps['k-planestrain'])/(8.0*matrixProps['G'])))
                currentG0strain.append(np.pi*Rf*(matrixProps['E']/(1-matrixProps['nu']*matrixProps['nu']))*epsxx*epsxx)
                currentGIvcctonly.append(float(values[13]))
                currentGIIvcctonly.append(float(values[14]))
                currentGTOTvcctonly.append(float(values[15]))
                currentGIvcctjint.append(float(values[16]))
                currentGIIvcctjint.append(float(values[17]))
                currentGTOTvcctjint.append(float(values[18]))
                currentLoverRf.append(float(values[3]))
                currentVff.append(0.25*np.pi/float(values[3]))
                currentphiCZ.append(float(values[4]))
        for s,valueSet in enumerate(GIvcctonly):
            currentVff = Vff[s][0]
            currentLoverRf = LoverRf[s][0]
            GI = [np.array(GIvcctonly[s]),np.array(GIvcctjint[s])]
            GII = [np.array(GIIvcctonly[s]),np.array(GIIvcctjint[s])]
            GTOT = [np.array(GTOTvcctonly[s]),np.array(GTOTvcctjint[s])]
            gMethod = ['VCCT only','VCCT/J-integral']
            G0s = [G0meanstress[s],G0planestrainstress[s],G0strain[s]]
            legendEntries = '{$GI/G0-FEM$,$GII/G0-FEM$,$GTOT/G0-FEM$,$GI/G0-BEM$,$GII/G0-BEM$,$GTOT/G0-BEM$}'
            dataoptions.append('red!' + str(100.0*float(c)/float(len(plot[:-3]))) + '!blue')
            for m,method in enumerate(gMethod):
                titles = ['\\bf{Normalized Energy Release Rate, '+method+', $Vf_{f}='+str(currentVff)+'$, $\\frac{L}{R_{f}}='+str(currentLoverRf)+'$, $G_{0}=\\frac{1+k_{m}}{8G_{m}}\\pi R_{f}\\left(\\frac{1}{2L}\\int_{-L}^{+L}\\sigma_{xx}\\left(L,z\\right)dz\\right)^{2}$}',
                          '\\bf{Normalized Energy Release Rate, '+method+', $Vf_{f}='+str(currentVff)+'$, $\\frac{L}{R_{f}}='+str(currentLoverRf)+'$, $G_{0}=\\frac{1+k_{m}}{8G_{m}}\\pi R_{f}\\left(\\frac{E_{m}}{1-\\nu^{2}}\\varepsilon_{xx}\\right)^{2}$}',
                          '\\bf{Normalized Energy Release Rate, '+method+', $Vf_{f}='+str(currentVff)+'$, $\\frac{L}{R_{f}}='+str(currentLoverRf)+'$, $G_{0}=\\frac{E_{m}}{1-\\nu^{2}}\\pi R_{f}\\varepsilon_{xx}^{2}$}']
                for g,G0 in enumerate(G0s):
                    axisoptions = 'width=30cm,\n ' \
                                  'title={'+titles[g]+'},\n ' \
                                  'title style={font=\\fontsize{40}{8}\\selectfont},\n ' \
                                  'xlabel style={at={(axis description cs:0.5,-0.02)},anchor=north,font=\\fontsize{44}{40}\\selectfont},\n ' \
                                  'ylabel style={at={(axis description cs:-0.025,.5)},anchor=south,font=\\fontsize{44}{40}\\selectfont},\n ' \
                                  'xlabel={$' + plot[-3] + '$},ylabel={$' + plot[-2] + '$},\n ' \
                                  'xmin=' + str(xmin) + ',\n ' \
                                  'xmax=' + str(xmax) + ',\n ' \
                                  'ymin=' + str(ymin) + ',\n ' \
                                  'ymax=' + str(ymax) + ',\n ' \
                                  'tick align=outside,\n ' \
                                  'tick label style={font=\\huge},\n ' \
                                  'xmajorgrids,\n ' \
                                  'x grid style={lightgray!92.026143790849673!black},\n ' \
                                  'ymajorgrids,\n ' \
                                  'y grid style={lightgray!92.026143790849673!black},\n ' \
                                  'line width=0.5mm,\n ' \
                                  'legend style={draw=white!80.0!black,font=\\fontsize{28}{24}\\selectfont,row sep=15pt},\n ' \
                                  'legend entries={' + legendEntries + '},\n ' \
                                  'legend image post style={xscale=2},\n ' \
                                  'legend cell align={left}'
            writeLatexMultiplePlots(outDir,plot[-1].replace(' ','-').replace('/','-').replace(',','') + '.tex',xyData,axisoptions,dataoptions,logfilefullpath,3*logindent,logindent)



if __name__ == "__main__":
    main(sys.argv[1:])
