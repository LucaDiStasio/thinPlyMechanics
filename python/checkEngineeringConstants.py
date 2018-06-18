# -*- coding: utf-8 -*-

'''
=====================================================================================

Copyright (c) 2016 Université de Lorraine & Luleå tekniska universitet
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



Tested with Python 2.7 Anaconda 2.4.1 (64-bit) distribution
       in Windows 10.

'''

from numpy import *


E1 = 3e4
E2 = 3e4
E3 = 5e5
nu12 =0.45
nu13 =(E1/E3)*0.2
nu23 =(E2/E3)*0.2

'''
E1 = 134.6287e3
E2 = 9.4757e3
E3 = 9.4757e3
nu12 =0.2883
nu13 =0.2883
nu23 =0.3969
'''
'''
E1 = 5e5
E2 = 3e4
E3 = 3e4
nu12 =0.2
nu13 =0.2
nu23 =0.45
'''

if abs(nu12)<sqrt(E1/E2):
    print 'TEST 1 ---           abs(nu12)<sqrt(E1/E2)             --- PASSED'
else:
    print 'TEST 1 ---           abs(nu12)<sqrt(E1/E2)             --- FAILED'

if abs(nu13)<sqrt(E1/E3):
    print 'TEST 2 ---           abs(nu13)<sqrt(E1/E3)             --- PASSED'
else:
    print 'TEST 2 ---           abs(nu13)<sqrt(E1/E3)             --- FAILED'

if abs(nu23)<sqrt(E2/E3):
    print 'TEST 3 ---           abs(nu23)<sqrt(E2/E3)             --- PASSED'
else:
    print 'TEST 3 ---           abs(nu23)<sqrt(E2/E3)             --- FAILED'

if 1-(E2/E1)*pow(nu12,2)-(E3/E2)*pow(nu23,2)-(E3/E1)*pow(nu13,2)-2*nu13*(E3/E2)*nu23*(E2/E1)*nu12>0:
    print 'TEST 4 --- 1-nu12nu21-nu23nu32-nu31nu13-nu21nu32nu13>0 --- PASSED'
else:
    print 'TEST 4 --- 1-nu12nu21-nu23nu32-nu31nu13-nu21nu32nu13>0 --- FAILED'
    print '           LHS = ' + str(1-(E2/E1)*pow(nu12,2)-(E3/E2)*pow(nu23,2)-(E3/E1)*pow(nu13,2)-2*nu13*(E3/E2)*nu23*(E2/E1)*nu12)
