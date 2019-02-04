! 2D Model of Fiber/Matrix Interface in Cross-ply Laminates
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

/TITLE, 2D Model of Fiber/Matrix Interface in Cross-ply Laminates

/PREP7               ! Enter the pre-processor

! Parameters

! ===> START INPUT DATA

Vf = 0.6! [-] Fiber volume fraction

Rf = 1.0           ! [mum] radius of the fiber
L = 1.144          ! [mum] length of the RVE
nAb = 5            ! [-] number of fibers above
tRatio = 1         ! [-]  ratio of bounding ply thickness to main ply
epsx = 0.01        ! [-]  applied strain

EG = 70000.0! [MPa] Glass fiber Young's modulus
nuG = 0.2! [-] Glass fiber Poisson ratio

EEp = 3500.0! [MPa] Epoxy Young's modulus
nuEp = 0.4! [-] Epoxy Poisson ratio

E1 = 43442.0! [MPa] UD longitudinal Young's modulus
E2 = 13714.0! [MPa] UD transverse Young's modulus
nu12 = 0.273! [-] UD in-plane Poisson ratio
nu23 = 0.465! [-] UD out-of-plane Poisson ratio
G12 = 4315.0! [MPa] UD in-plane shear modulus

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

*DO, i, 1, nAb, 1
 K, 8+4*(i-1)+1, 0.0, 2*L*i-Rf         ! Lower node fiber i
 K, 8+4*(i-1)+2, 0.0, 2*L*i            ! Center fiber i
 K, 8+4*(i-1)+3, 0.0, 2*L*i+Rf         ! Upper node fiber i
 K, 8+4*(i-1)+4,  Rf, 2*L*i            ! Right node fiber i
*ENDDO

! Lines

L, 1, 5                                              !1  -- S side, fiber
L, 5, 2                                              !2  -- S side, matrix
L, 2, 8                                              !3  -- E side, 90 ply
L, 8, 3                                              !4  -- E side, 0 ply
L, 3, 4                                              !5  -- N side
L, 7, 8                                              !6  -- Ply interface

L, 4, 7                                              !7  -- W side, 0 ply
L, 1, 6                                              !8  -- W side, 90 ply, fiber
L, 6, 9                                              !9  -- W side, 90 ply, first interfiber matrix region
L, 7, 8+4*(nAb-1)+3                                  !10 -- W side, 90 ply, last interfiber matrix region

*DO, i, 1, nAb-1, 1
 L, 8+4*(i-1)+3, 8+4*(i-1)+5                         ! W side, 90 ply, interfiber matrix regions
*ENDDO

*DO, i, 1, nAb, 1
 L, 8+4*(i-1)+1, 8+4*(i-1)+3                         ! W side, 90 ply, fibers
*ENDDO

! Arcs

LARC, 5, 6, 1, Rf                                    ! Fiber/matrix interface, quarter fiber

*DO, i, 1, nAb, 1
 LARC, 8+4*(i-1)+1, 8+4*(i-1)+4, 8+4*(i-1)+2, Rf     ! Fiber/matrix interface, half fiber
 LARC, 8+4*(i-1)+4, 8+4*(i-1)+3, 8+4*(i-1)+2, Rf     ! Fiber/matrix interface, half fiber
*ENDDO

! Areas

AL, 6, 4, 5, 7                                         ! UD

AL, 1, 8, 2*nAb+10                                     ! Quarter fiber

*DO, i, 1, nAb, 1
 AL, nAb+9+i, 2*nAb+10+2*(i-1)+1, 2*nAb+10+2*(i-1)+2   ! Half fibers
*ENDDO

LSEL, S, LINE, , 2, 3, 1
LSEL, A, LINE, , 6
LSEL, A, LINE, , 9, 10, 1

*DO, i, 1, nAb-1, 1
 LSEL, A, LINE, , 10+i
*ENDDO

LSEL, A, LINE, , 2*nAb+10

*DO, i, 1, nAb, 1
 LSEL, A, LINE, , 2*nAb+10+2*(i-1)+1
 LSEL, A, LINE, , 2*nAb+10+2*(i-1)+2
*ENDDO

AL, ALL

ALLSEL

! Define Material Properties
! 1 is fiber, 2 is matrix, 3 is UD

MP,EX,  1,EG      ! mp,Young's modulus,material number,value
MP,PRXY,1,nuG     ! mp,Poisson's ratio,material number,value

MP,EX,  2,EEp      ! mp,Young's modulus,material number,value
MP,PRXY,2,nuEp     ! mp,Poisson's ratio,material number,value

MP,EX,  3,E1       ! mp,Young's modulus,material number,value
MP,EY,  3,E2       ! mp,Young's modulus,material number,value
MP,EZ,  3,E2       ! mp,Young's modulus,material number,value
MP,PRXY,3,nu12     ! mp,Poisson's ratio,material number,value
MP,PRYZ,3,nu23     ! mp,Poisson's ratio,material number,value
MP,PRXZ,3,nu12     ! mp,Poisson's ratio,material number,value
MP,GXY, 3,G12      ! mp,shear modulus,material number,value

! Assign properties to areas
! ASEL, Type, Item, Comp, VMIN, VMAX, VINC, KSWP
! AATT, MAT, REAL, TYPE, ESYS, SECN
ASEL, S, AREA, , 1
AATT, 3
ASEL, S, AREA, , 2
AATT, 1

*DO, i, 1, nAb, 1
 ASEL, S, AREA, , 2+i
 AATT, 1
*ENDDO

ASEL, S, AREA, , nAb+3
AATT, 2

ALLSEL

! Seed the edges
! LESIZE, NL1, SIZE, ANGSIZ, NDIV, SPACE, KFORC, LAYER1, LAYER2, KYNDIV
LESIZE, 1, , , 20                                    !1  -- S side, fiber
LESIZE, 2, , , 50                                    !2  -- S side, matrix
LESIZE, 3, , , 100+20*nAb                            !3  -- E side, 90 ply
LESIZE, 4, , , 25                                    !4  -- E side, 0 ply
LESIZE, 6, , , 70                                    !6  -- Ply interface
LESIZE, 7, , , 25                                    !7  -- W side, 0 ply
LESIZE, 8, , , 20                                    !8  -- W side, 90 ply, fiber
LESIZE, 9, , , 100                                   !9  -- W side, 90 ply, first interfiber matrix region

LESIZE, 2*nAb+10, , angSize

*DO, i, 1, nAb-1, 1
 LESIZE, 10+i, , , 10                                !10+i -- W side, 90 ply, interfiber matrix regions
*ENDDO

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
AMESH, nAb+3
MSHKEY, 0
AMESH, 1, nAb+2, 1

ALLSEL

FINISH              ! Finish pre-processing

/SOLU               ! Enter the solution processor

ANTYPE,0            ! Analysis type,static

! Define Displacement Constraints on Lines   (dl command)
! DL, LINE, AREA, Lab, Value1, Value2
DL, 1, ,SYMM
DL, 2, ,SYMM

DL, 3, ,UX,appliedDisp
DL, 4, ,UX,appliedDisp

DL, 7, ,SYMM
DL, 8, ,SYMM
DL, 9, ,SYMM

*DO, i, 1, nAb-1, 1
 DL, 10+i, ,SYMM
*ENDDO

*DO, i, 1, nAb, 1
 DL, nAb+9+i, ,SYMM
*ENDDO

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
