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
import xlsxwriter
import ast
import getopt


def main(argv):
    # Read the command line, throw error if not option is provided
    try:
        opts, args = getopt.getopt(argv,'hw:i:o:f:',['help','Help',"workdir", "workdirectory", "wdir","inputfile", "input","out","outdir","outputfile","xlsx","outfile"])
    except getopt.GetoptError:
        print('reportDataToXlsx.py -w <working directory> -i <input file> -o <output directory> -f <output filename>')
        sys.exit(2)
    # Parse the options and create corresponding variables
    for opt, arg in opts:
        if opt in ('-h', '--help','--Help'):
            print(' ')
            print(' ')
            print('*****************************************************************************************************')
            print(' ')
            print('                                GATHER DATA IN CSV FILES TO XLSX\n')
            print(' ')
            print('                                              by')
            print(' ')
            print('                                    Luca Di Stasio, 2016-2018')
            print(' ')
            print(' ')
            print('*****************************************************************************************************')
            print(' ')
            print('Program syntax:')
            print('reportDataToXlsx.py -w <working directory> -i <input file> -o <output directory> -f <output filename>')
            print(' ')
            print('Mandatory arguments:')
            print('-w <working directory>')
            print('-i <input file>')
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
            outputfile = arg.split(".")[0] + '.xlsx'

    # Check the existence of variables: if a required variable is missing, an error is thrown and program is terminated; if an optional variable is missing, it is set to the default value
    if 'workdir' not in locals():
        print('Error: working directory not provided.')
        sys.exit()
    if 'inputfile' not in locals():
        print('Error: file list not provided.')
        sys.exit()
    if 'outputfile' not in locals():
        outputfile = datetime.now().strftime('%Y-%m-%d') + '_' + datetime.now().strftime('%H-%M-%S') + '_' + inputfile.split(".")[0] + '.xlsx'
    if 'outdir' not in locals():
        outdir = workdir

    with open(join(workdir,inputfile),'r') as csv:
        lines = csv.readlines()

    workbook = xlsxwriter.Workbook(join(outdir,outputfile))

    stringFormat = workbook.add_format({'bold': 1})
    numberFormat = workbook.add_format({'num_format': '0.000000'})

    for line in lines[1:]:
        csvPath = line.replace('\n','').split(',')[0]
        sheetName = line.replace('\n','').split(',')[1]
        toPlot = bool(line.replace('\n','').split(',')[2])
        plotSettings = []
        if toPlot:
            settingsString = ','.join(line.replace('\n','').split(',')[3:])
            plotSettings = ast.literal_eval(settingsString[1:])
        worksheet = workbook.add_worksheet(sheetName)
        with open(csvPath,'r') as csv:
            csvlines = csv.readlines()
        for e,element in enumerate(csvlines[0].replace('\n','').split(',')):
            worksheet.write(0,e,element,stringFormat)
        for c,csvline in enumerate(csvlines[1:]):
            for e,element in enumerate(csvline.replace('\n','').split(',')):
                try:
                    worksheet.write(c+1,e,float(element),numberFormat)
                except Exception,error:
                    worksheet.write(c+1,e,str(element),numberFormat)
                    sys.exc_clear()
        for p,plot in enumerate(plotSettings):
            chart = workbook.add_chart({'type': 'scatter',
                                        'subtype': 'smooth_with_markers'})
            for curve in plot[:-3]:
                chart.add_series({
                                    'name':       curve[2],
                                    'categories': [sheetName,1,curve[0],len(csvlines),curve[0]],
                                    'values':     [sheetName,1,curve[1],len(csvlines),curve[1]],
                                })
            chart.set_title ({'name': plot[-1]})
            chart.set_x_axis({'name': plot[-3]})
            chart.set_y_axis({'name': plot[-2]})
            worksheet.insert_chart(len(csvlines)+10,10*p, chart)

    workbook.close()



if __name__ == "__main__":
    main(sys.argv[1:])
