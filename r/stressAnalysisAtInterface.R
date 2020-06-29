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
S5A0FreeTheta000 <- read.table( "S5A0-free-theta000.txt",header=TRUE,sep ="")
S5A0FreeTheta010 <- read.table( "S5A0-free-theta010.txt",header=TRUE,sep ="")
S5A0FreeTheta020 <- read.table( "S5A0-free-theta020.txt",header=TRUE,sep ="")

S5A0T1Theta000 <- read.table( "S5A0T1-theta000.txt",header=TRUE,sep ="")

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

ggplot(data = S5A0FreeTheta000, mapping = aes(x = angle, y = Srr)) + geom_point()
ggplot(data = S5A0FreeTheta010, mapping = aes(x = angle, y = Srr)) + geom_point()

ggplot(data = S5A0T1Theta000, mapping = aes(x = angle, y = Srr)) + geom_point()

ggplot()+
  geom_point(data = S5A0FreeTheta000, mapping = aes(x = angle, y = Srr),color="blue") +
  geom_point(data = S5A0T1Theta000, mapping = aes(x = angle, y = Srr),color="red")

S5A0FreeTheta000$normSrr = S5A0FreeTheta000$Srr/sigmaInf
S5A0FreeTheta000$normToAvgSrr = S5A0FreeTheta000$Srr/sigmaAvg

S5A0FreeTheta010$normSrr = S5A0FreeTheta010$Srr/sigmaInf
S5A0FreeTheta010$normToAvgSrr = S5A0FreeTheta010$Srr/sigmaAvg

S5A0FreeTheta020$normSrr = S5A0FreeTheta020$Srr/sigmaInf
S5A0FreeTheta020$normToAvgSrr = S5A0FreeTheta020$Srr/sigmaAvg

S5A0T1Theta000$normSrr = S5A0T1Theta000$Srr/sigmaInf
S5A0T1Theta000$normToAvgSrr = S5A0T1Theta000$Srr/sigmaAvg

ggplot(data = S5A0FreeTheta000, mapping = aes(x = angle, y = normSrr)) + geom_point()
ggplot(data = S5A0FreeTheta000, mapping = aes(x = angle, y = normToAvgSrr)) + geom_point()

ggplot(data = S5A0T1Theta000, mapping = aes(x = angle, y = normSrr)) + geom_point()
ggplot(data = S5A0T1Theta000, mapping = aes(x = angle, y = normToAvgSrr)) + geom_point()

S5A0FreeTheta000$SrrFFT = fft(S5A0FreeTheta000$normSrr)

S5A0FreeTheta000$k = 1:length(S5A0FreeTheta000$normSrr)
S5A0FreeTheta000$kshift = S5A0FreeTheta000$k-ceiling(0.5*length(S5A0FreeTheta000$normSrr))

S5A0FreeTheta000$SrrRe <- Re(S5A0FreeTheta000$SrrFFT)
S5A0FreeTheta000$SrrIm <- Im(S5A0FreeTheta000$SrrFFT)
S5A0FreeTheta000$SrrAmplitude <- sqrt(S5A0FreeTheta000$SrrRe*S5A0FreeTheta000$SrrRe+S5A0FreeTheta000$SrrIm*S5A0FreeTheta000$SrrIm)
S5A0FreeTheta000$SrrPhaseRad <- atan2(S5A0FreeTheta000$SrrIm,S5A0FreeTheta000$SrrRe)
S5A0FreeTheta000$SrrPhaseDeg <- S5A0FreeTheta000$SrrPhaseRad*180.0/pi
#SrrAmplitude <- matrix(0,nrow=length(data$Srr),ncol=length(data$SrrFFT))
#SrrFrequencyRad <- matrix(0,nrow=length(data$Srr),ncol=length(data$SrrFFT))
#SrrFrequencyDeg <- matrix(0,nrow=length(data$Srr),ncol=length(data$SrrFFT))

ggplot(data = S5A0FreeTheta000, mapping = aes(x = k, y = SrrAmplitude)) + geom_point()
ggplot(data = S5A0FreeTheta000, mapping = aes(x = kshift, y = fftshift(S5A0FreeTheta000$SrrAmplitude))) + geom_point()
ggplot(data = S5A0FreeTheta000, mapping = aes(x = kshift, y = fftshift(S5A0FreeTheta000$SrrPhaseDeg))) + geom_point()

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

y1 = S5A0FreeTheta000$normSrr

x1 = cos(2*1*S5A0FreeTheta000$angle*pi/180)
x2 = cos(2*2*S5A0FreeTheta000$angle*pi/180)
x3 = cos(2*3*S5A0FreeTheta000$angle*pi/180)
x4 = cos(2*4*S5A0FreeTheta000$angle*pi/180)
x5 = cos(2*5*S5A0FreeTheta000$angle*pi/180)
x6 = cos(2*6*S5A0FreeTheta000$angle*pi/180)
x7 = cos(2*7*S5A0FreeTheta000$angle*pi/180)
x8 = cos(2*8*S5A0FreeTheta000$angle*pi/180)
x9 = cos(2*9*S5A0FreeTheta000$angle*pi/180)
x10 = cos(2*10*S5A0FreeTheta000$angle*pi/180)

model1 = y1 ~ x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8

ols1 = lm(formula = model1)
ols1$coefficients

reconstructedSrrOLS <- vector(length=length(S5A0FreeTheta000$Srr),mode="double")
orderMax = 6
for (j in 0:orderMax){
  reconstructedSrrOLS = reconstructedSrrOLS + ols1$coefficients[j+1]*cos(2*j*S5A0FreeTheta000$angle*pi/180)
}
ggplot(mapping = aes(x = S5A0FreeTheta000$angle, y = S5A0FreeTheta000$normSrr-reconstructedSrrOLS)) + geom_point()

reconstructedSrrOLS010 <- vector(length=length(S5A0FreeTheta010$Srr),mode="double")
orderMax = 6
for (j in 0:orderMax){
  reconstructedSrrOLS010 = reconstructedSrrOLS010 + ols1$coefficients[j+1]*cos(2*j*S5A0FreeTheta010$angle*pi/180)
}
ggplot(mapping = aes(x = S5A0FreeTheta010$angle, y = S5A0FreeTheta010$normSrr-reconstructedSrrOLS010)) + geom_point() #+ scale_y_log10()#+ ylim(0.0,10)

reconstructedSrrOLS020 <- vector(length=length(S5A0FreeTheta020$Srr),mode="double")
orderMax = 6
for (j in 0:orderMax){
  reconstructedSrrOLS020 = reconstructedSrrOLS020 + ols1$coefficients[j+1]*cos(2*j*S5A0FreeTheta020$angle*pi/180)
}
ggplot(mapping = aes(x = S5A0FreeTheta020$angle, y = S5A0FreeTheta020$normSrr-reconstructedSrrOLS020)) + geom_point() #+ scale_y_log10()#+ ylim(0.0,10)
ggplot(mapping = aes(x = S5A0FreeTheta020$angle[S5A0FreeTheta020$angle>20.0 & S5A0FreeTheta020$angle<=50.0], y = S5A0FreeTheta020$normSrr[S5A0FreeTheta020$angle>20.0 & S5A0FreeTheta020$angle<=50.0]-reconstructedSrrOLS020[S5A0FreeTheta020$angle>20.0 & S5A0FreeTheta020$angle<=50.0])) + geom_point() + scale_x_log10()#+ ylim(0.0,10)

yRegion1 = (S5A0FreeTheta020$normSrr-reconstructedSrrOLS020)[S5A0FreeTheta020$angle>20.0 & S5A0FreeTheta020$angle<=50.0][1:3]
yRegion2 = (S5A0FreeTheta020$normSrr-reconstructedSrrOLS020)[S5A0FreeTheta020$angle>20.0 & S5A0FreeTheta020$angle<=50.0][4:length(S5A0FreeTheta020$angle)]

xRegion1 = (S5A0FreeTheta020$angle[S5A0FreeTheta020$angle>20.0 & S5A0FreeTheta020$angle<=50.0][1:3]*pi/180.0)^(-1)
olsRegion1 = lm(formula = yRegion1~xRegion1)
summary(olsRegion1)

xRegion2 = (S5A0FreeTheta020$angle[S5A0FreeTheta020$angle>20.0 & S5A0FreeTheta020$angle<=50.0][4:length(S5A0FreeTheta020$angle)]*pi/180.0)^(-0.5)
olsRegion2 = lm(formula = yRegion2~xRegion2)
summary(olsRegion2)

yLogRegion1 = log((S5A0FreeTheta020$normSrr-reconstructedSrrOLS020)[S5A0FreeTheta020$angle>20.0 & S5A0FreeTheta020$angle<=50.0][1:3])
yLogRegion2 = log((S5A0FreeTheta020$normSrr-reconstructedSrrOLS020)[S5A0FreeTheta020$angle>20.0 & S5A0FreeTheta020$angle<=50.0][4:length(S5A0FreeTheta020$angle)])

xLogRegion1 = log(S5A0FreeTheta020$angle[S5A0FreeTheta020$angle>20.0 & S5A0FreeTheta020$angle<=50.0][1:3]*pi/180.0)
olsLogRegion1 = lm(formula = yLogRegion1~xLogRegion1)
summary(olsLogRegion1)

xLogRegion2 = log(S5A0FreeTheta020$angle[S5A0FreeTheta020$angle>20.0 & S5A0FreeTheta020$angle<=50.0][4:length(S5A0FreeTheta020$angle)]*pi/180.0)
olsLogRegion2 = lm(formula = yLogRegion2~xLogRegion2)
summary(olsLogRegion2)

ggplot()+
  geom_line(mapping = aes(x = angle, y = reconstructedSrrOLS),color="red") +
  geom_point(data = data, mapping = aes(x = angle, y = normSrr),color="blue")

ggplot(mapping = aes(x = angle, y = reconstructedSrrOLS)) + geom_point()

S5A0T1Theta000$SrrFFT = fft(S5A0T1Theta000$normSrr)

S5A0T1Theta000$k = 1:length(S5A0T1Theta000$normSrr)
S5A0T1Theta000$kshift = S5A0T1Theta000$k-ceiling(0.5*length(S5A0T1Theta000$normSrr))

S5A0T1Theta000$SrrRe <- Re(S5A0T1Theta000$SrrFFT)
S5A0T1Theta000$SrrIm <- Im(S5A0T1Theta000$SrrFFT)
S5A0T1Theta000$SrrAmplitude <- sqrt(S5A0T1Theta000$SrrRe*S5A0T1Theta000$SrrRe+S5A0T1Theta000$SrrIm*S5A0T1Theta000$SrrIm)
S5A0T1Theta000$SrrPhaseRad <- atan2(S5A0T1Theta000$SrrIm,S5A0T1Theta000$SrrRe)
S5A0T1Theta000$SrrPhaseDeg <- S5A0T1Theta000$SrrPhaseRad*180.0/pi

ggplot(data = S5A0T1Theta000, mapping = aes(x = kshift, y = fftshift(S5A0T1Theta000$SrrAmplitude))) + geom_point()

ggplot() +
  geom_point(data = S5A0FreeTheta000, mapping = aes(x = kshift, y = fftshift(S5A0FreeTheta000$SrrAmplitude)),color="blue") +
  geom_point(data = S5A0T1Theta000, mapping = aes(x = kshift, y = fftshift(S5A0T1Theta000$SrrAmplitude)),color="red")

y2 = S5A0T1Theta000$normSrr

model2 = y2 ~ x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8

ols2 = lm(formula = model2)
ols2$coefficients

summary(ols1)
summary(ols2)
