! 2D Model of Fiber/Matrix Interface in cross-plies
! Stress Analysis

!
!==============================================================================
! Copyright (c) 2016-2019 Université de Lorraine & Luleå tekniska universitet
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

/title, 2D Model of Fiber/Matrix Interface in cross-plies

/prep7               ! Enter the pre-processor

! Parameters

! ===> START INPUT DATA

Vf = 0.6! [-] Fiber volume fraction

Rf = 1.0           ! [mum] radius of the fiber
L = 1.144          ! [mum] length of the RVE
nAb = 1            ! [-] number of fibers above
tRatio = 1         ! [-]  ratio of bounding ply thickness to main ply
epsx = 0.01        ! [-]  applied strain

EG = 70000.0! [MPa] Glass fiber Young's modulus
nuG = 0.2! [-] Glass fiber Poisson ratio

EEp = 3500.0! [MPa] Epoxy Young's modulus
nuEp = 0.4! [-] Epoxy Poisson ratio

elOrder = 2

angSize = 0.1! Angular size of elements at the interface

! ===> END INPUT DATA

heightCply = (2*nAb+1)*L
heightUDply = tRatio*2*heightCply

heightTOT = heightCply + heightUDply

appliedDisp = epsx*L ! [mum] applied displacement

dispreactfile = 'allDispsRFs'
stressstrainfile = 'allStressStrain'

! Create Geometry

! Points

K, 1, 0.0, 0.0              ! SW corner
K, 2, L, 0.0                ! SE corner
K, 3, L, heightTOT          ! NE corner
K, 4, 0.0, heightTOT        ! NW corner

K, 5, Rf, 0.0
K, 6, 0.0, Rf

K, 7, 0.0, heightCply       ! W interface corner
K, 8, L, heightCply         ! E interface corner

! Lines

L, 1, 5            !1 -- S side, fiber
L, 5, 2            !2 -- S side, matrix
L, 2, 3            !3 -- E side
L, 3, 4            !4 -- N side
L, 4, 6            !5 -- W side, matrix
L, 6, 1            !6 -- W side, fiber

! Arcs

LARC, 5, 6, 1, Rf !7 -- fiber/matrix interface

! Areas

AL, 1, 7, 6           ! 1, fiber
AL, 2, 3, 4, 5, 7     ! 2, matrix

! Define Material Properties
! 1 is fiber, 2 is matrix

MP,EX,1,EG        ! mp,Young's modulus,material number,value
MP,NUXY,1,nuG     ! mp,Poisson's ratio,material number,value

MP,EX,2,EEp        ! mp,Young's modulus,material number,value
MP,NUXY,2,nuEp     ! mp,Poisson's ratio,material number,value

! Assign properties to areas
! ASEL, Type, Item, Comp, VMIN, VMAX, VINC, KSWP
! AATT, MAT, REAL, TYPE, ESYS, SECN
ASEL, S, AREA, , 1
AATT, 1
ASEL, S, AREA, , 2
AATT, 2

ALLSEL

! Seed the edges
! LESIZE, NL1, SIZE, ANGSIZ, NDIV, SPACE, KFORC, LAYER1, LAYER2, KYNDIV
LESIZE, 1, , , 20
LESIZE, 2, , , 50
LESIZE, 3, , , 100
LESIZE, 4, , , 100
LESIZE, 5, , , 50
LESIZE, 1, , , 20
LESIZE, 7, , angSize

! Define Element Type

*IF, elOrder, EQ, 2, THEN
 ET,1,PLANE183,0,,2      ! Quadratic plane strain quadrilaterals
 ET,2,PLANE183,1,,2      ! Quadratic plane strain triangles
*ELSE
 ET,1,PLANE182,0,,2      ! Linear plane strain quadrilaterals
 ET,2,PLANE182,1,,2      ! Linear plane strain triangles
*ENDIF

ALLSEL

! Generate mesh
! MSHKEY, KEY (0 == free, 1 == mapped)
! AMESH, NA1, NA2, NINC
MSHKEY, 0
AMESH, 1, 2, 1

ALLSEL

LSEL, S, LINE, , 4
NSLL, S, 1
CP, 1, UY, ALL

ALLSEL

FINISH              ! Finish pre-processing

/SOLU               ! Enter the solution processor

ANTYPE,0            ! Analysis type,static

! Define Displacement Constraints on Lines   (dl command)
! DL, LINE, AREA, Lab, Value1, Value2
DL, 1, ,SYMM
DL, 2, ,SYMM
DL, 5, ,SYMM
DL, 6, ,SYMM
DL, 3, ,UX,appliedDisp

ALLSEL

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
*VWRITE, 'NODE','LABEL,','X[mum],','Z[mum],','UX','[mum],','UZ','[mum],','RX','[MN],','RZ','[MN]'
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

/EOF
