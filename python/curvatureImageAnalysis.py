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
height,width = img.shape

f = 0.1
redImg = img[int(np.floor(f*height)):int(np.floor((1-f)*height)),int(np.floor(f*width)):int(np.floor((1-f)*width))]

img = redImg

ret1,imgBin1 = cv2.threshold(img,150,255,cv2.THRESH_BINARY)
ret2,imgBin2 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
            
#plt.figure()
plt.subplot(2,2,1)
plt.imshow(imgBin1,cmap = 'gray')
plt.title('Threshold')
plt.subplot(2,2,2)
plt.imshow(imgBin2,cmap = 'gray')
plt.title('Otsu')
plt.subplot(2,2,3)
plt.imshow(th2,cmap = 'gray')
plt.title('Mean')
plt.subplot(2,2,4)
plt.imshow(th3,cmap = 'gray')
plt.title('Gaussian')

plt.show()