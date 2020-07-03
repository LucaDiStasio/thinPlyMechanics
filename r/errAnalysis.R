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
S100A5FreeGI <- read.table( "ERR-S100A5-free-GI.txt",header=TRUE,sep ="")
S100A5FreeGII <- read.table( "ERR-S100A5-free-GII.txt",header=TRUE,sep ="")


#---------------------------------------------------------------------------------------
# --> Material and load parameters

Rf = 10^-6 # m
eps = 0.01 # -
E1 = 43442.0 #MPa
E2 = 13714.0 #MPa
nu12 = 0.273 #-
nu21 = E2*nu12/E1 #-
Ehomo = E2/(1-nu21*nu12) #MPa
sigmaInf = Ehomo*eps #MPa

G0 = Ehomo*10^6*Rf*eps^2 #J/m^2

#---------------------------------------------------------------------------------------

ggplot(data = S100A5FreeGI, mapping = aes(x = angle, y = GI)) + geom_point()
ggplot(data = S100A5FreeGII, mapping = aes(x = angle, y = GII)) + geom_point()

S100A5FreeGI$normGI = S100A5FreeGI$GI/G0
S100A5FreeGII$normGII = S100A5FreeGII$GII/G0

ggplot(data = S100A5FreeGI, mapping = aes(x = angle, y = normGI)) + geom_point()
ggplot(data = S100A5FreeGII, mapping = aes(x = angle, y = normGII)) + geom_point()

CZonset = S100A5FreeGI$angle[S100A5FreeGI$normGI<10^-3 & S100A5FreeGI$angle!=0.0][1]

nPeriods = 5
reducedAngle = S100A5FreeGI$angle[S100A5FreeGI$angle<=CZonset]
reducedGI = S100A5FreeGI$GI[S100A5FreeGI$angle<=CZonset]
extendedAngle <- vector(length=2*nPeriods*(length(reducedAngle)-1)+1,mode="double")
extendedGI <- vector(length=2*nPeriods*(length(reducedAngle)-1)+1,mode="double")
for (i in 1:(2*nPeriods)){
  for (j in 1:(length(reducedAngle)-1)){
    extendedAngle[1+(i-1)*(length(reducedAngle)-1)+j] = (i-1)*CZonset + reducedAngle[j+1]
    extendedGI[1+(i-1)*(length(reducedAngle)-1)+j] = ((-1)^(i-1))*reducedGI[((i-1)%%2)*length(reducedAngle)+((-1)^(i-1))*j+(i%%2)]
  }
}

ggplot()+
  geom_point(mapping=aes(x=extendedAngle,y=extendedGI),color="blue")+
  geom_point(mapping=aes(x=reducedAngle,y=reducedGI),color="red")

curvatureEffectGI = (cos(0.5*reducedAngle*pi/180)*(1-sin(0.5*reducedAngle*pi/180)^2*cos(0.5*reducedAngle*pi/180)^2)/(1+sin(0.5*reducedAngle*pi/180)^2)+cos(1.5*reducedAngle*pi/180))^2

ggplot()+
  geom_point(mapping=aes(x=reducedAngle,y=reducedGI/sin(reducedAngle*pi/180)),color="red")+
  geom_point(mapping=aes(x=reducedAngle,y=reducedGI/(sin(reducedAngle*pi/180)*curvatureEffectGI)),color="green")

y2 = reducedGI/sin(reducedAngle*pi/180)
y3 = reducedGI/(sin(reducedAngle*pi/180)*curvatureEffectGI)

x = reducedAngle-CZonset
x2 = x^2
x3 = x^3

ols2 = lm(formula = y2~x+x2)
summary(ols2)
ggplot()+
  geom_point(mapping=aes(x=reducedAngle,y=reducedGI/sin(reducedAngle*pi/180)),color="red")+
  geom_line(mapping=aes(x=reducedAngle,y=ols2$coefficients[1]+ols2$coefficients[2]*x+ols2$coefficients[3]*x2),color="green")

ols3 = lm(formula = y3~x+x2+x3)
summary(ols3)
ggplot()+
  geom_point(mapping=aes(x=reducedAngle,y=reducedGI/(sin(reducedAngle*pi/180)*curvatureEffectGI)),color="red")+
  geom_line(mapping=aes(x=reducedAngle,y=ols3$coefficients[2]*x+ols3$coefficients[3]*x2+ols3$coefficients[4]*x3),color="green")

S100A5FreeGI$GIFFT = fft(S100A5FreeGI$normGI)
S100A5FreeGII$GIIFFT = fft(S100A5FreeGII$normGII)

extendedGIFFT = fft(extendedGI)

S100A5FreeGI$k = 1:length(S100A5FreeGI$normGI)
S100A5FreeGI$kshift = S100A5FreeGI$k-ceiling(0.5*length(S100A5FreeGI$normGI))

extendedk = 1:length(extendedGI)
extendedkshift = extendedk-ceiling(0.5*length(extendedGI))

S100A5FreeGII$k = 1:length(S100A5FreeGII$normGII)
S100A5FreeGII$kshift = S100A5FreeGII$k-ceiling(0.5*length(S100A5FreeGII$normGII))

S100A5FreeGI$GIRe <- Re(S100A5FreeGI$GIFFT)
S100A5FreeGI$GIIm <- Im(S100A5FreeGI$GIFFT)
S100A5FreeGI$GIAmplitude <- sqrt(S100A5FreeGI$GIRe*S100A5FreeGI$GIRe+S100A5FreeGI$GIIm*S100A5FreeGI$GIIm)
S100A5FreeGI$GIPhaseRad <- atan2(S100A5FreeGI$GIIm,S100A5FreeGI$GIRe)
S100A5FreeGI$GIPhaseDeg <- S100A5FreeGI$GIPhaseRad*180.0/pi

extendedGIRe <- Re(extendedGIFFT)
extendedGIIm <- Im(extendedGIFFT)
extendedGIAmplitude <- sqrt(extendedGIRe*extendedGIRe+extendedGIIm*extendedGIIm)
extendedGIPhaseRad <- atan2(extendedGIIm,extendedGIRe)
extendedGIPhaseDeg <- extendedGIPhaseRad*180.0/pi

S100A5FreeGII$GIIRe <- Re(S100A5FreeGII$GIIFFT)
S100A5FreeGII$GIIIm <- Im(S100A5FreeGII$GIIFFT)
S100A5FreeGII$GIIAmplitude <- sqrt(S100A5FreeGII$GIIRe*S100A5FreeGII$GIIRe+S100A5FreeGII$GIIIm*S100A5FreeGII$GIIIm)
S100A5FreeGII$GIIPhaseRad <- atan2(S100A5FreeGII$GIIIm,S100A5FreeGII$GIIRe)
S100A5FreeGII$GIIPhaseDeg <- S100A5FreeGII$GIIPhaseRad*180.0/pi

ggplot(data = S100A5FreeGI, mapping = aes(x = k, y = GIAmplitude)) + geom_point()
ggplot(data = S100A5FreeGI, mapping = aes(x = kshift, y = fftshift(GIAmplitude))) + geom_point()

ggplot(mapping = aes(x = extendedkshift, y = fftshift(extendedGIAmplitude))) + geom_point()


y1 = extendedGI

angleOLS = extendedAngle

angFreq = CZonset/180.0

x1 = sin(1*angFreq*angleOLS*pi/180)
x2 = sin(2*angFreq*angleOLS*pi/180)
x3 = sin(3*angFreq*angleOLS*pi/180)
x4 = sin(4*angFreq*angleOLS*pi/180)
x5 = sin(5*angFreq*angleOLS*pi/180)
x6 = sin(6*angFreq*angleOLS*pi/180)
x7 = sin(7*angFreq*angleOLS*pi/180)
x8 = sin(8*angFreq*angleOLS*pi/180)
x9 = sin(9*angFreq*angleOLS*pi/180)
x10 = sin(10*angFreq*angleOLS*pi/180)
x11 = sin(11*angFreq*angleOLS*pi/180)
x12 = sin(12*angFreq*angleOLS*pi/180)
x13 = sin(13*angFreq*angleOLS*pi/180)
x14 = sin(14*angFreq*angleOLS*pi/180)
x15 = sin(15*angFreq*angleOLS*pi/180)
x16 = sin(6*angFreq*angleOLS*pi/180)
x17 = sin(7*angFreq*angleOLS*pi/180)
x18 = sin(8*angFreq*angleOLS*pi/180)
x19 = sin(9*angFreq*angleOLS*pi/180)
x20 = sin(10*angFreq*angleOLS*pi/180)

modelGI = y1 ~ x1  + x2 + x3 + x4 + x5 + x6 + x7 + x8 + x9 + x10 +x11 + x12 + x13 + x14 + x15

olsGI = lm(formula = modelGI)
summary(olsGI)

angleReconstruction = seq(from=0.0,to=extendedAngle[length(extendedAngle)],by=0.1)
reconstructedGIOLS <- vector(length=length(angleReconstruction),mode="double")
orderMin = 1
orderMax = 15
for (j in c(6,7,13)){
  reconstructedGIOLS = reconstructedGIOLS + olsGI$coefficients[j+1]*sin(j*angFreq*angleReconstruction*pi/180)
}
ggplot()+
  geom_line(mapping = aes(x = angleReconstruction[angleReconstruction<=CZonset], y = reconstructedGIOLS[angleReconstruction<=CZonset]),color="green")+
  geom_point(mapping = aes(x = reducedAngle, y = reducedGI),color="blue")

angleReconstruction = seq(from=0.0,to=70.0,by=0.1)
reconstructedGIOLS <- vector(length=length(angleReconstruction),mode="double")
orderMin = 0
orderMax = 1
for (j in 0:orderMax){
  reconstructedGIOLS = reconstructedGIOLS + olsGI$coefficients[j+1]*sin(2*j*angleReconstruction*pi/180)
}
ggplot()+
  geom_line(mapping = aes(x = angleReconstruction, y = reconstructedGIOLS),color="green")+
  geom_point(data=S100A5FreeGI,mapping = aes(x = angle, y = GI),color="blue")
  
