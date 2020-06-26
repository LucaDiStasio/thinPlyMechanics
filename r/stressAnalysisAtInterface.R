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

ggplot(data = data, mapping = aes(x = angle, y = normSrr)) + geom_point()

data$SrrFFT = fft(data$normSrr)

SrrHarmonics <- matrix(0,nrow=length(data$Srr),ncol=length(data$SrrFFT))
for (i in seq_along(SrrHarmonics[,0])) {
  for (j in seq_along(SrrHarmonics[i,])) {
    SrrHarmonics[i,j] <- data$SrrFFT[j]*exp(-(2*pi*i*(i-1)*(j-1)/length(data$Srr)))
  }
}