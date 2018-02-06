#!/usr/bin/env Python
# -*- coding: utf-8 -*-

'''
=====================================================================================

Copyright (c) 2017 - 2018 Université de Lorraine & Luleå tekniska universitet
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

Tested with Python 2.7 in Ubuntu 14.04

'''

import sys, os
import errno
from os import makedirs
from os.path import isfile, join, exists
import ast

wd = 'C:/Users/lucdis/Documents/WD/thinPlyMechanics/python'
deck = 'inputRVEdata.deck'

with open(join(wd,deck),'r') as d:
    lines = d.readlines()

stringToEval = ''

for line in lines:
    stringToEval += line.replace('\n','').replace('  ','')

dataDict = ast.literal_eval(stringToEval)
