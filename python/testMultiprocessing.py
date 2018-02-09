#!/usr/bin/env Python
# -*- coding: utf-8 -*-

'''
=====================================================================================

Copyright (c) 2018 Luca Di Stasio
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


Tested with Python 2.7 in Windows 10

'''

import sys
from multiprocessing import Pool

def OCRimage(file_name):
    print >> sys.__stdout__, "file_name = %s" % file_name

def main():
    print >> sys.__stdout__, 'filter files'
    filterfiles = ["image%03d.tif" % n for n in range(5)]
    print >> sys.__stdout__, 'open pool of processes'
    pool = Pool(processes=2)
    print >> sys.__stdout__, 'get results from pool'
    result = pool.map(OCRimage, filterfiles)
    print >> sys.__stdout__, 'close pool'
    pool.close()
    pool.join()

if __name__ == '__main__':
    main()
