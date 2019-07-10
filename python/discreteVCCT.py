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

def printHelp():
    print(' ')
    print(' ')
    print('*****************************************************************************************************')
    print(' ')
    print('                                        DISCRETE VCCT\n')
    print(' ')
    print('                                              by')
    print(' ')
    print('                                    Luca Di Stasio, 2016-2019')
    print(' ')
    print(' ')
    print('*****************************************************************************************************')
    print(' ')
    print('Program syntax:')
    print('discreteVCCT.py -w <working directory>')
    print(' ')
    print('Mandatory arguments:')
    print('-w <working directory>')
    print(' ')
    print('Optional arguments:')
    print(' ')
    print('Default values:')
    print(' ')
    print(' ')
    print(' ')
    sys.exit()

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

def main(argv):
    # Read the command line, throw error if not option is provided
    try:
        opts, args = getopt.getopt(argv,'hw:',['help','Help',"workdir", "workdirectory", "wdir"])
    except getopt.GetoptError:
        print('discreteVCCT.py -w <working directory>)
        sys.exit(2)
    # Parse the options and create corresponding variables
    for opt, arg in opts:
        if opt in ('-h', '--help','--Help'):
            printHelp()
        elif opt in ("-w", "--workdir", "--workdirectory", "--wdir"):
            if arg[-1] != '/':
                workdir = arg
            else:
                workdir = arg[:-1]

    # Check the existence of variables: if a required variable is missing, an error is thrown and program is terminated; if an optional variable is missing, it is set to the default value
    if 'workdir' not in locals():
        print('Error: working directory not provided.')
        sys.exit()




if __name__ == "__main__":
    main(sys.argv[1:])
