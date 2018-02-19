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
from os import listdir, stat, makedirs
from datetime import datetime
from time import strftime
from platform import platform
import matplotlib as plt
import numpy as np
import xlsxwriter
import ast
import getopt

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


def main(argv):
    # Read the command line, throw error if not option is provided
    try:
        opts, args = getopt.getopt(argv,'hw:i:o:f:e:l:',['help','Help',"workdir", "workdirectory", "wdir","inputfile", "input","out","outdir","outputfile","xlsx","outfile","excel","latex"])
    except getopt.GetoptError:
        print('reportDataToXlsx.py -w <working directory> -i <input file> -o <output directory> -f <output filename> -excel -latex')
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
            print('reportDataToXlsx.py -w <working directory> -i <input file> -o <output directory> -f <output filename> --excel --latex')
            print(' ')
            print('Mandatory arguments:')
            print('-w <working directory>')
            print('-i <input file>')
            print('at least one out of: -e --excel/-l --latex')
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
    if 'toExcel' not in locals() and 'toLatex' not in locals():
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

    if toLatex:
        G0 = []
        GIvcctonly = []
        GIIvcctonly = []
        GTOTvcctonly = []
        GIvcctjint = []
        GIIvcctjint = []
        GTOTvcctjint = []
        LoverRf = []
        Vff = []
        phiCZ = []

        currentG0 = []
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
            try:
                with open(csvPath,'r') as csv:
                    csvlines = csv.readlines()
            except Exception,error:
                continue
                sys.exc_clear()
            for c,csvline in enumerate(csvlines[1:]):
                values = csvline.replace('\n','').split(',')
                if len(currentLoverRf)>0:
                    if float(values[3])!=currentLoverRf[-1]:
                        G0.append(currentG0)
                        GIvcctonly.append(currentGIvcctonly)
                        GIIvcctonly.append(currentGIIvcctonly)
                        GTOTvcctonly.append(currentGTOTvcctonly)
                        GIvcctjint.append(currentGIvcctjint)
                        GIIvcctjint.append(currentGIIvcctjint)
                        GTOTvcctjint.append(currentGTOTvcctjint)
                        LoverRf.append(currentLoverRf)
                        Vff.append(currentVff)
                        phiCZ.append(currentphiCZ)
                        currentG0 = []
                        currentGIvcctonly = []
                        currentGIIvcctonly = []
                        currentGTOTvcctonly = []
                        currentGIvcctjint = []
                        currentGIIvcctjint = []
                        currentGTOTvcctjint = []
                        currentLoverRf = []
                        currentVff = []
                        currentphiCZ = []
                currentG0.append(float(values[5]))
                currentGIvcctonly.append(float(values[13]))
                currentGIIvcctonly.append(float(values[14]))
                currentGTOTvcctonly.append(float(values[15]))
                currentGIvcctjint.append(float(values[16]))
                currentGIIvcctjint.append(float(values[17]))
                currentGTOTvcctjint.append(float(values[18]))
                currentLoverRf.append(float(values[3]))
                currentVff.append(0.25*np.pi/float(values[3]))
                currentphiCZ.append(float(values[4]))



if __name__ == "__main__":
    main(sys.argv[1:])
