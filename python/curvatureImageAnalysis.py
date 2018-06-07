# -*- coding: utf-8 -*-

'''
=====================================================================================

Copyright (c) 2016-2018 Université de Lorraine & Luleå tekniska universitet
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

Image analysis of Double Cantilever Beam test recordings.

Tested with Python 2.7 Anaconda 2.4.1 (64-bit) distribution
       in Windows 10.

'''

from os.path import join
import numpy as np
import cv2
from matplotlib import pyplot as plt

plt.close('all')

inpDir = 'C:/Users/lucad/OneDrive/01_Luca/07_DocMASE/02_Studies/09_Aerospace-materials/WD/ThermalCurvature'

fileName = 'P1010035'

ext = '.jpg'

img = cv2.imread(join(inpDir,fileName+ext),0)

ret,imgBin = cv2.threshold(img,127,255,cv2.THRESH_BINARY)

#plt.figure()
plt.imshow(imgBin,cmap = 'gray')
plt.title('pic')
plt.show()