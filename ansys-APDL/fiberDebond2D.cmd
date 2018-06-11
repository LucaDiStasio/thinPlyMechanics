! 2D Model of Fiber/Matrix Debond in Thin-ply FRPC
! Calculation of reaction forces and displacements for external VCCT subroutine in Python

!
!==============================================================================
! Copyright (c) 2016-2018 Université de Lorraine & Luleå tekniska universitet
! Author: Luca Di Stasio <luca.distasio@gmail.com>
!                        <luca.distasio@ingpec.eu>
!
! Redistribution and use in source and binary forms, with or without
! modification, are permitted provided that the following conditions are met:
!
!
! Redistributions of source code must retain the above copyright
! notice, this list of conditions and the following disclaimer.
! Redistributions in binary form must reproduce the above copyright
! notice, this list of conditions and the following disclaimer in
! the documentation and/or other materials provided with the distribution
! Neither the name of the Université de Lorraine & Luleå tekniska universitet
! nor the names of its contributors may be used to endorse or promote products
! derived from this software without specific prior written permission.
!
! THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
! AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
! IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
! ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
! LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
! CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
! SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
! INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
! CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
! ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
! POSSIBILITY OF SUCH DAMAGE.
!==============================================================================
!

/title, 2D Model of Transverse Cracking in Thin-ply FRPC

/prep7               ! Enter the pre-processor

! Parameters

! ===> START INPUT DATA

Vf = 0.0! [-] Fiber volume fraction

t = 1             ! [mm] 2t = thickness of the element
tRatio = 1        ! [-]  ratio of bounding ply thickness to main ply
aLRatio = 0.1     ! [-]  ratio of crack length to main ply thickness
rhon = 0.01       ! [-]  normalized crack density
daOvera = 0.05    ! [-]  ratio of crack increment (i.e. crack tip element size) to crack length
epsx = 0.01       ! [-]  applied strain
uniP = 0.0        ! [-]  uniform pressure applied to crack face
reftRatio = 0.2   ! [-]  ratio of refined area height to cross-ply thickness

nContours = 10 ! [-]  number of contours for J-integral evaluation

EL = 3500.0! [MPa] UD longitudinal Young's modulus
ET = 3500.0! [MPa] UD transverse Young's modulus
nuLT = 0.4! [-] UD in-plane Poisson ratio
nuTT = 0.4! [-] UD transverse Poisson ratio
!GL = ! [MPa] UD in-plane shear modulus
!GT = ! [MPa] UD transverse shear modulus

! ===> END INPUT DATA

L = 2*t/rhon        ! [mm] length of the RVE
a = aLRatio*L     ! [mm] 2a = crack length

refHlow = (1-reftRatio)*t 
refHup = (1+reftRatio)*t

tBPly = tRatio*(2*t) ! [mm] thickness of the bounding ply
tTOT = t + tBPly     ! [mm] thickness of the bounding ply

elSize = daOvera*a ! [mm] size of element in refined region close to crack tip

vcctRegion = a+elSize

appliedDisp = epsx*L ! [mm] applied displacement

dispreactfile = 'allDispsRFs'
stressstrainfile = 'allStressStrain'

! Create Geometry

! Points

K, 1, 0.0, 0.0
K, 2, L, 0.0
K, 3, L, tTOT
K, 4, 0.0, tTOT

K, 5, 0.0, refHlow
K, 6, L, refHlow
K, 7, L, refHup
K, 8, 0.0, refHup

K, 9, a, refHlow
K,10, a, t
K,11, a, t
K,12, a, refHup
K,13, 0.0, t
K,14, 0.0, t
K,15, vcctRegion,t

K,16, L, t

! Lines

L, 1, 2            !1
L, 2, 6            !2
L, 6, 16           !3
L, 16, 7           !4
L, 7, 3            !5
L, 3, 4            !6
L, 4, 8            !7
L, 8, 14           !8
L, 13, 5           !9
L, 5, 1            !10
L, 5, 9            !11
L, 9, 6            !12
L, 8, 12           !13
L, 12, 7           !14
L, 10, 15          !15
L, 11, 15          !16
L, 15, 16          !17
L, 13, 10          !18
L, 14, 11          !19
L, 9, 10           !20
L, 11, 12          !21

! Areas

AL, 1, 2, 12, 11, 10     ! 1, lower ply, coarse area
AL, 13, 14, 5, 6, 7      ! 2, upper ply, coarse area

AL, 11, 20, 18, 9        ! 3, lower ply, free area
AL, 19, 21, 13, 8        ! 4, upper ply, free area

AL, 12, 3, 17, 15, 20    ! 5, lower ply, bonded area
AL, 4, 14, 21, 16, 17    ! 6, upper ply, bonded area

! Define Material Properties

*IF, crossPly, EQ, 0, THEN
   MP,EX,1,ET        ! 1 is cross-ply, 2 is ud-ply 
   MP,NUXY,1,nuTT    ! mp,Poisson's ratio,material number,value
*ELSE
   MP,EX,1,ET        ! 1 is cross-ply, 2 is ud-ply 
   MP,EY,1,ET        ! 1 is cross-ply, 2 is ud-ply
   MP,EZ,1,EL        ! 1 is cross-ply, 2 is ud-ply
   MP,NUXY,1,nuTT    ! mp,Poisson's ratio,material number,value
   MP,NUYZ,1,nuLT    ! mp,Poisson's ratio,material number,value
   MP,NUXZ,1,nuLT    ! mp,Poisson's ratio,material number,value
   MP,GXY,1,GTT      ! mp,Poisson's ratio,material number,value
   MP,GYZ,1,GLT      ! mp,Poisson's ratio,material number,value
   MP,GXZ,1,GLT      ! mp,Poisson's ratio,material number,value
*ENDIF

*IF, udPly, EQ, 0, THEN
   MP,EX,2,EL        ! 1 is cross-ply, 2 is ud-ply
   MP,NUXY,2,nuLT    ! mp,Poisson's ratio,material number,value
*ELSE
   MP,EX,2,EL        ! 1 is cross-ply, 2 is ud-ply 
   MP,EY,2,ET        ! 1 is cross-ply, 2 is ud-ply
   MP,EZ,2,ET        ! 1 is cross-ply, 2 is ud-ply
   MP,NUXY,2,nuLT    ! mp,Poisson's ratio,material number,value
   MP,NUYZ,2,nuTT    ! mp,Poisson's ratio,material number,value
   MP,NUXZ,2,nuLT    ! mp,Poisson's ratio,material number,value
   MP,GXY,2,GLT      ! mp,Poisson's ratio,material number,value
   MP,GYZ,2,GTT      ! mp,Poisson's ratio,material number,value
   MP,GXZ,2,GLT      ! mp,Poisson's ratio,material number,value
*ENDIF

MP,MU,3,0

! Assign properties to areas
! ASEL, Type, Item, Comp, VMIN, VMAX, VINC, KSWP
! AATT, MAT, REAL, TYPE, ESYS, SECN
ASEL, S, AREA, , 1
AATT, 1
ASEL, S, AREA, , 3
AATT, 1
ASEL, S, AREA, , 5
AATT, 1
ASEL, S, AREA, , 2
AATT, 2
ASEL, S, AREA, , 4
AATT, 2
ASEL, S, AREA, , 6
AATT, 2

ALLSEL

KSEL, S, KP, , 7
CM,CRACKTIP,KP

ALLSEL

! Seed the edges
! LESIZE, NL1, SIZE, ANGSIZ, NDIV, SPACE, KFORC, LAYER1, LAYER2, KYNDIV
LESIZE, 11, elSize
LESIZE, 12, elSize
LESIZE, 13, elSize
LESIZE, 14, elSize
LESIZE, 3, elSize
LESIZE, 4, elSize
LESIZE, 8, elSize
LESIZE, 9, elSize
LESIZE, 20, elSize
LESIZE, 21, elSize
LESIZE, 15, elSize
LESIZE, 16, elSize
LESIZE, 18, elSize
LESIZE, 19, elSize

! Define Element Type

*IF, elOrder, EQ, 2, THEN
 ET,1,PLANE183,0,,2      ! Quadratic plane strain quadrilaterals 
 ET,2,PLANE183,1,,2      ! Quadratic plane strain triangles
*ELSE
 ET,1,PLANE182,0,,2      ! Linear plane strain quadrilaterals 
 ET,2,PLANE182,1,,2      ! Linear plane strain triangles
*ENDIF
ET,3,CONTA172
KEYOPT, 3, 1, 0
KEYOPT, 3, 2, 0

ALLSEL

! Generate mesh
! MSHKEY, KEY (0 == free, 1 == mapped)
! AMESH, NA1, NA2, NINC
MSHKEY, 1
AMESH, 1, 2, 1
MSHKEY, 0
AMESH, 3, 4, 1

ALLSEL

LSEL,S,LINE,,18
NSLL,S,1
TYPE,3
MAT,3
ESURF

LSEL,S,LINE,,19
NSLL,S,1
TYPE,3
MAT,3
ESURF

ALLSEL

FINISH              ! Finish pre-processing

/SOLU               ! Enter the solution processor

ANTYPE,0            ! Analysis type,static

! Define Displacement Constraints on Lines   (dl command)
! DL, LINE, AREA, Lab, Value1, Value2
DL, 1, ,SYMM
DL, 7, ,SYMM
DL, 8, ,SYMM
DL, 2, ,UX,appliedDisp
DL, 3, ,UX,appliedDisp
DL, 4, ,UX,appliedDisp
DL, 5, ,UX,appliedDisp

ALLSEL

! Coincident constraints
LSEL,S,LINE,,15,16,1
NSLL,S,1
CPINTF,ALL

ALLSEL

! Apply pressure, if present
! SFL, Line, Lab, VALI, VALJ, VAL2I, VAL2J
*IF, uniP, GT, 0.0, THEN
   SFL, 9, PRES, uniP
   SFL, 10, PRES, uniP
   SFL, 18, PRES, uniP
   SFL, 19, PRES, uniP
*ENDIF

! For output setting: OUTRES, Item, Freq, Cname, -- , NSVAR, DSUBres

OUTRES, NSOL
OUTRES, NLOAD
OUTRES, STRS
OUTRES, EPEL
OUTRES, LOCI
OUTRES, RSOL

SOLVE                ! Solve the problem

FINISH               ! Finish the solution processor

SAVE                 ! Save your work to the database

/POST1               ! Post processing

PRCINT, 2, , JINT

ALLSEL

*GET,NNodes,NODE,0,COUNT                  !Get the number of nodes in the selected set
*DIM, resArray, ARRAY, NNodes, 13
*VGET, resArray(1,1), NODE, , NLIST
*VGET, resArray(1,2), NODE, 1, LOC, X
*VGET, resArray(1,3), NODE, 1, LOC, Y
*VGET, resArray(1,4), NODE, 1, U, X
*VGET, resArray(1,5), NODE, 1, U, Y
*VGET, resArray(1,6), NODE, 1, S, X
*VGET, resArray(1,7), NODE, 1, S, Y
*VGET, resArray(1,8), NODE, 1, S, XY
*VGET, resArray(1,9), NODE, 1, EPEL, X
*VGET, resArray(1,10), NODE, 1, EPEL, Y
*VGET, resArray(1,11), NODE, 1, EPEL, XY
*VGET, resArray(1,12), NODE, 1, RF, FX
*VGET, resArray(1,13), NODE, 1, RF, FY

*CFOPEN, dispreactfile, csv
*VWRITE, 'NODE','LABEL,','X[mm],','Z[mm],','UX','[mm],','UZ','[mm],','RX','[kN],','RZ','[kN]'
(A5,A6,A6,A6,A2,A5,A2,A5,A2,A5,A2,A4)
*VWRITE, resArray(1,1), ',', resArray(1,2), ',', resArray(1,3), ',', resArray(1,4), ',', resArray(1,5), ',', resArray(1,12), ',', resArray(1,13)
(F7.0,A1,F12.8,A1,F12.8,A1,F12.8,A1,F12.8,A1,F12.8,A1,F12.8)
*CFCLOS

*CFOPEN, stressstrainfile, csv
*VWRITE, 'NODE','LABEL,','SX','[MPa],','SZ','[MPa],','SXZ','[MPa],','EX','[-],','EZ','[-],','EXZ','[-]'
(A5,A6,A2,A6,A2,A6,A3,A6,A2,A4,A2,A4,A3,A3)
*VWRITE, resArray(1,1), ', ', resArray(1,6), ', ', resArray(1,7), ', ', resArray(1,8), ', ', resArray(1,9), ', ', resArray(1,10), ', ', resArray(1,11)
(F7.0,A1,F12.8,A1,F12.8,A1,F12.8,A1,F12.8,A1,F12.8,A1,F12.8)
*CFCLOS

PRCINT, 2, , JINT
PRCINT, 1, , G1
PRCINT, 1, , G2

/EOF
