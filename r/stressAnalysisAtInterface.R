#=====================================================================================
#    
#  Copyright (c) 2020 Luca Di Stasio
#                     <luca.distasio@gmail.com>
#                     <luca.distasio@ingpec.eu>
#    
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#    
#  Redistributions of source code must retain the above copyright
#  notice, this list of conditions and the following disclaimer.
#  Redistributions in binary form must reproduce the above copyright
#  notice, this list of conditions and the following disclaimer in
#  the documentation and/or other materials provided with the distribution
#  Neither the name of the Université de Lorraine or Luleå tekniska universitet
#  nor the names of its contributors may be used to endorse or promote products
#  derived from this software without specific prior written permission.
#  
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
#  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
#  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
#  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
#  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#  POSSIBILITY OF SUCH DAMAGE.
#  
#  =====================================================================================

#---------------------------------------------------------------------------------------
# --> Get the workspace ready

# clear the workspace
rm(list=ls())

# load libraries
library("ggplot2")
library("stats")
library("SynchWave")

# set path of working directory
wDir <- file.path("C:","02_Local-folder","01_Luca","01_WD","thinPlyMechanics","r")
# set path of input directory
inpDir <- file.path("C:","02_Local-folder","01_Luca","01_WD","thinPlyMechanics","r")
# set path of output directory
outDir <- file.path("C:","02_Local-folder","01_Luca","01_WD","thinPlyMechanics","r")

# Set the working directory to the specified one
setwd(wDir)

# Check the current working directory is the desired one
getwd()

# Load data file and attach data to workspace
data <- read.table( "S5A0-free-theta000.txt",header=TRUE,sep ="")

#---------------------------------------------------------------------------------------
# --> Material and load parameters

eps = 0.01 # -
E1 = 43442.0 #MPa
E2 = 13714.0 #MPa
nu12 = 0.273 #-
nu21 = E2*nu12/E1 #-
Ehomo = E2/(1-nu21*nu12) #MPa
sigmaInf = Ehomo*eps #MPa
sigmaAvg = 156.362190 #MPa

#---------------------------------------------------------------------------------------

ggplot(data = data, mapping = aes(x = angle, y = Srr)) + geom_point()

data$normSrr = data$Srr/sigmaInf
data$normToAvgSrr = data$Srr/sigmaAvg

ggplot(data = data, mapping = aes(x = angle, y = normSrr)) + geom_point()
ggplot(data = data, mapping = aes(x = angle, y = normToAvgSrr)) + geom_point()

data$SrrFFT = fft(data$normSrr)

data$k = 1:length(data$normSrr)
data$kshift = data$k-ceiling(0.5*length(data$normSrr))

data$SrrRe <- Re(data$SrrFFT)
data$SrrIm <- Im(data$SrrFFT)
data$SrrAmplitude <- sqrt(data$SrrRe*data$SrrRe+data$SrrIm*data$SrrIm)
data$SrrPhaseRad <- atan2(data$SrrIm,data$SrrRe)
data$SrrPhaseDeg <- data$SrrPhaseRad*180.0/pi
#SrrAmplitude <- matrix(0,nrow=length(data$Srr),ncol=length(data$SrrFFT))
#SrrFrequencyRad <- matrix(0,nrow=length(data$Srr),ncol=length(data$SrrFFT))
#SrrFrequencyDeg <- matrix(0,nrow=length(data$Srr),ncol=length(data$SrrFFT))

ggplot(data = data, mapping = aes(x = data$k, y = data$SrrAmplitude)) + geom_point()
ggplot(data = data, mapping = aes(x = data$kshift, y = fftshift(data$SrrAmplitude))) + geom_point()
ggplot(data = data, mapping = aes(x = data$kshift, y = fftshift(data$SrrPhaseDeg))) + geom_point()

harmonicsIndex = 5
ggplot(data = data, mapping = aes(x = angle, y = cos(harmonicsIndex*data$angle*pi/180))) + geom_point()

harmonicsIndex = 8
ggplot(data = data, mapping = aes(x = angle, y = data$SrrAmplitude[harmonicsIndex+1]*cos(harmonicsIndex*data$angle*pi/180))) + geom_point()

angle=data$angle

reconstructedSrr <- vector(length=length(data$Srr),mode="double")
orderMax = 6
for (j in 0:orderMax){
  reconstructedSrr = reconstructedSrr + cos(2*j*data$angle*pi/180)
}
ggplot(mapping = aes(x = angle, y = reconstructedSrr)) + geom_point()

reconstructedSrrwithAmpl <- vector(length=length(data$Srr),mode="double")
orderMax = 50
for (j in 0:orderMax){
  reconstructedSrrwithAmpl = reconstructedSrrwithAmpl + data$SrrAmplitude[j+1]*cos(2*j*data$angle*pi/180)
}
reconstructedSrrwithAmpl = reconstructedSrrwithAmpl/max(reconstructedSrrwithAmpl)
ggplot(mapping = aes(x = angle, y = reconstructedSrrwithAmpl)) + geom_point()

ggplot()+
  geom_line(mapping = aes(x = angle, y = reconstructedSrrwithAmpl),color="red") +
  geom_point(data = data, mapping = aes(x = angle, y = normSrr/max(normSrr)),color="blue")

reconstructedSrrFull <- vector(length=length(data$Srr),mode="double")
orderMax = 8
for (j in 0:orderMax){
  reconstructedSrrFull = reconstructedSrrFull + data$SrrAmplitude[j+1]*cos(2*j*data$angle*pi/180+data$SrrPhaseRad[j+1])
}
reconstructedSrrFull = reconstructedSrrFull/max(reconstructedSrrFull)
ggplot(mapping = aes(x = angle, y = reconstructedSrrFull)) + geom_point()

ggplot()+
  geom_line(mapping = aes(x = angle, y = reconstructedSrrFull),color="magenta") +
  geom_point(data = data, mapping = aes(x = angle, y = normSrr/max(normSrr)),color="blue")

y = data$normSrr

x1 = cos(2*1*data$angle*pi/180)
x2 = cos(2*2*data$angle*pi/180)
x3 = cos(2*3*data$angle*pi/180)
x4 = cos(2*4*data$angle*pi/180)
x5 = cos(2*5*data$angle*pi/180)
x6 = cos(2*6*data$angle*pi/180)
x7 = cos(2*7*data$angle*pi/180)
x8 = cos(2*8*data$angle*pi/180)
x9 = cos(2*9*data$angle*pi/180)
x10 = cos(2*10*data$angle*pi/180)

model1 = y ~ x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8

ols1 = lm(formula = model1)
ols1$coefficients

reconstructedSrrOLS <- vector(length=length(data$Srr),mode="double")
orderMax = 6
for (j in 0:orderMax){
  reconstructedSrrOLS = reconstructedSrrOLS + ols1$coefficients[j+1]*cos(2*j*data$angle*pi/180)
}
ggplot(mapping = aes(x = angle, y = reconstructedSrrOLS)) + geom_point()

ggplot()+
  geom_line(mapping = aes(x = angle, y = reconstructedSrrOLS),color="red") +
  geom_point(data = data, mapping = aes(x = angle, y = normSrr),color="blue")
