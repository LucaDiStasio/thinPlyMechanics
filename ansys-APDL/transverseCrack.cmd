! Command File mode of 2D Model of Transverse Cracking in Thin-ply FRPC

/title, 2D Model of Transverse Cracking in Thin-ply FRPC

/prep7               ! Enter the pre-processor

! Parameters

! ===> START INPUT DATA

*DIM,wd,STRING,18
wd = 'C:/Ansys_WD/Debug/'
*DIM,wd,STRING,6
basename = 'debug_'

wd = 'C:/Ansys_WD/Debug'
basename = 'debug_'

Vf = 0.0! [-] Fiber volume fraction

t = 1             ! [mm] 2t = thickness of the element
tRatio = 49.5     ! [-]  ratio of bounding ply thickness to main ply
atRatio = 0.1     ! [-]  ratio of crack length to main ply thickness
rhon = 0.01       ! [-]  normalized crack density
daOvera = 0.05    ! [-]  ratio of crack increment (i.e. crack tip element size) to crack length
epsx = 0.01       ! [-]  applied strain
uniP = 0.0        ! [-]  uniform pressure applied to crack face

nContours = 10 ! [-]  number of contours for J-integral evaluation

EL = 3500.0! [MPa] UD longitudinal Young's modulus
ET = 3500.0! [MPa] UD transverse Young's modulus
nuLT = 0.4! [-] UD in-plane Poisson ratio
nuTT = 0.4! [-] UD transverse Poisson ratio
!GL = ! [MPa] UD in-plane shear modulus
!GT = ! [MPa] UD transverse shear modulus

! ===> END INPUT DATA

L = t/rhon        ! [mm] length of the RVE
a = atRatio*t     ! [mm] 2a = crack length

tBPly = tRatio*(2*t) ! [mm] thickness of the bounding ply
tTOT = t + tBPly   ! [mm] thickness of the bounding ply

elSize = daOvera*a ! [mm] size of element in refined region close to crack tip

appliedDisp = epsx*L ! [mm] applied displacement

CFFileCoordDisp = 'C:/Ansys_WD/Debug/debug_CFCoordDisp'
CFFileStressStrain = 'C:/Ansys_WD/Debug/debug_CFStressStrain'

YsymmLow = 'C:/Ansys_WD/Debug/ysymmLowerData'
YsymmUp = 'C:/Ansys_WD/Debug/ysymmUpperData'
XsymmLeft = 'C:/Ansys_WD/Debug/xsymmLeftData'
XsymmRight = 'C:/Ansys_WD/Debug/xsymmRightData'
loadUp = 'C:/Ansys_WD/Debug/loadUpperData'
loadLow = 'C:/Ansys_WD/Debug/loadLowerData'

! Create Geometry

! Points

K, 1, 0.0, 0.0     ! SW corner
K, 2, L, 0.0       ! SE corner
K, 3, L, tTOT      ! NE corner
K, 4, 0.0, tTOT    ! NW corner

K, 5, 0.0, t       ! W corner of ply interface
K, 6, L, t         ! E corner of ply interface

K, 7, 0.0, a       ! crack tip
K, 8, a, 0.0       ! S corner of refined area interface
K, 9, a, t         ! N corner of refined area interface
K, 10, a, a         ! E corner in refined area interface

! Lines

L, 1, 8            !1
L, 8, 2            !2
L, 2, 6            !3
L, 6, 3            !4
L, 3, 4            !5
L, 4, 5            !6
L, 5, 7            !7
L, 7, 1            !8

L, 5, 9            !9, ply interface
L, 9, 6            !10, ply interface
L, 8, 10           !11, refined area interface
L, 10, 9           !12, refined area interface
L, 7, 10           !13, refined area mid-interface

! Areas

AL, 1, 11, 13, 8     ! 1, lower ply, lower refined area
AL, 13, 12, 9, 7     ! 2, lower ply, upper refined area
AL, 2, 3, 10, 11, 12 ! 3, lower ply, coarse area
AL, 9, 10, 4, 5, 6   ! 4, upper ply

! Define entities

! KSEL, Type, Item, Comp, VMIN, VMAX, VINC, KABS
! LSEL, Type, Item, Comp, VMIN, VMAX, VINC, KSWP
! CM, Cname, Entity

KSEL, S, KP, , 7
CM,CRACKTIP,KP

LSEL, S, LINE, , 8
CM,CRACK,LINE

LSEL, S, LINE, , 7
CM,YSYMMBCCROSS,LINE

LSEL, S, LINE, , 6
CM,YSYMMBCUD,LINE

LSEL, S, LINE, , 3
CM,LOADBCCROSS,LINE

LSEL, S, LINE, , 4
CM,LOADBCUD,LINE

LSEL, S, LINE, , 1
CM,XSYMMBCCRACK,LINE

LSEL, S, LINE, , 2
CM,XSYMMBCBULK,LINE

ALLSEL

! Define Material Properties

MP,EX,1,ET        ! 1 is cross-ply, 2 is ud-ply 
!MP,EY,1,ET        ! 1 is cross-ply, 2 is ud-ply
!MP,EZ,1,EL        ! 1 is cross-ply, 2 is ud-ply
MP,NUXY,1,nuTT    ! mp,Poisson's ratio,material number,value
!MP,NUYZ,1,nuLT    ! mp,Poisson's ratio,material number,value
!MP,NUXZ,1,nuLT    ! mp,Poisson's ratio,material number,value
!MP,GXY,1,GTT      ! mp,Poisson's ratio,material number,value
!MP,GYZ,1,GLT      ! mp,Poisson's ratio,material number,value
!MP,GXZ,1,GLT      ! mp,Poisson's ratio,material number,value
MP,EX,2,EL        ! 1 is cross-ply, 2 is ud-ply 
!MP,EY,2,ET        ! 1 is cross-ply, 2 is ud-ply
!MP,EZ,2,ET        ! 1 is cross-ply, 2 is ud-ply
MP,NUXY,2,nuLT    ! mp,Poisson's ratio,material number,value
!MP,NUYZ,2,nuTT    ! mp,Poisson's ratio,material number,value
!MP,NUXZ,2,nuLT    ! mp,Poisson's ratio,material number,value
!MP,GXY,2,GLT      ! mp,Poisson's ratio,material number,value
!MP,GYZ,2,GTT      ! mp,Poisson's ratio,material number,value
!MP,GXZ,2,GLT      ! mp,Poisson's ratio,material number,value

! Assign properties to areas
! ASEL, Type, Item, Comp, VMIN, VMAX, VINC, KSWP
! AATT, MAT, REAL, TYPE, ESYS, SECN
ASEL, S, AREA, , 1
AATT, 1
ASEL, S, AREA, , 2
AATT, 1
ASEL, S, AREA, , 3
AATT, 1
ASEL, S, AREA, , 4
AATT, 2

ALLSEL

! Seed the edges
! LESIZE, NL1, SIZE, ANGSIZ, NDIV, SPACE, KFORC, LAYER1, LAYER2, KYNDIV
LESIZE, 1, elSize
LESIZE, 11, elSize
LESIZE, 13, elSize
LESIZE, 8, elSize
LESIZE, 12, elSize
LESIZE, 9, elSize
LESIZE, 7, elSize

! Define Element Type

ET,1,PLANE183,0,,2      ! Quadratic plane strain quadrilaterals 
ET,2,PLANE183,1,,2      ! Quadratic plane strain triangles

! Generate mesh
! MSHKEY, KEY (0 == free, 1 == mapped)
! AMESH, NA1, NA2, NINC
MSHKEY, 1
AMESH, 1, 2, 1
MSHKEY, 0
AMESH, 3, 4, 1

FINISH              ! Finish pre-processing

/SOLU               ! Enter the solution processor

ANTYPE,0            ! Analysis type,static


! Define Displacement Constraints on Lines   (dl command)
! DL, LINE, AREA, Lab, Value1, Value2
DL, 1, ,SYMM
DL, 2, ,SYMM
DL, 6, ,SYMM
DL, 7, ,SYMM
DL, 3, ,UX,appliedDisp
DL, 4, ,UX,appliedDisp

! Apply pressure, if present
! SFL, Line, Lab, VALI, VALJ, VAL2I, VAL2J
*IF, uniP, GT, 0.0, THEN
   SFL, 8, PRES, uniP
*ENDIF

! VCCT
CINT,NEW,1
CINT,TYPE,VCCT
CINT,CTNCP,CRACKTIP
CINT,SYMM,ON
OUTRES,CINT,LAST

! J-integral
CINT,NEW,2
CINT,CTNC,CRACKTIP
CINT,SYMM,ON
CINT,NCON,nContours
OUTRES,CINT,LAST

! For output setting: OUTRES, Item, Freq, Cname, -- , NSVAR, DSUBres

OUTRES, NSOL
OUTRES, NLOAD
OUTRES, STRS
OUTRES, EPEL
OUTRES, LOCI

OUTRES, RSOL, YSYMMBCCROSS
OUTRES, RSOL, YSYMMBCUD
OUTRES, RSOL, XSYMMBCCRACK
OUTRES, RSOL, XSYMMBCBULK

SOLVE                ! Solve the problem

FINISH               ! Finish the solution processor

SAVE                 ! Save your work to the database

/POST1               ! Post processing

ALLSEL

LSEL,S,LINE,,8                            ! Crack
NSLL,S,1                                  !Select nodes associated to this line
*GET,NNodes,NODE,0,COUNT                  !Get the number of nodes in the selected set
*DIM, CrackDisps, ARRAY, NNodes, 11
*VGET, CrackDisps(1,1), NODE, , NLIST
*VGET, CrackDisps(1,2), NODE, 1, LOC, Y
*VGET, CrackDisps(1,3), NODE, 1, LOC, X
*VGET, CrackDisps(1,4), NODE, 1, U, X
*VGET, CrackDisps(1,5), NODE, 1, U, Y
*VGET, CrackDisps(1,6), NODE, 1, S, X
*VGET, CrackDisps(1,7), NODE, 1, S, Y
*VGET, CrackDisps(1,8), NODE, 1, S, XY
*VGET, CrackDisps(1,9), NODE, 1, EPEL, X
*VGET, CrackDisps(1,10), NODE, 1, EPEL, Y
*VGET, CrackDisps(1,11), NODE, 1, EPEL, XY
!*VGET, CrackDisps(1,1), NODE, 1, NODE(CrackDisps(1,2),CrackDisps(1,3),CrackDisps(1,4))

!*DIM, CrackDisps, ARRAY, NNodes, 11
!*MOPER, CrackDisps, UnCrackDisps, SORT, , 3, 1

*CFOPEN, CFFileCoordDisp, csv
*VWRITE, 'NODE','LABEL,','X[mm],','Z[mm],','UX','[mm],','UZ','[mm]'
(A5,A6,A6,A6,A2,A5,A2,A4)
*VWRITE, CrackDisps(1,1), ',', CrackDisps(1,2), ',', CrackDisps(1,3), ',', CrackDisps(1,4), ',', CrackDisps(1,5)
(F5.0,A2,F12.8,A2,F12.8,A2,F12.8,A2,F12.8)
*CFCLOS

*CFOPEN, CFFileStressStrain, csv
*VWRITE, 'NODE LABEL, SX [MPa], SZ [MPa], SXZ [MPa], EX [-], EZ [-], EXZ [-]'
(A80)
*VWRITE, CrackDisps(1,1), ', ', CrackDisps(1,6), ', ', CrackDisps(1,7), ', ', CrackDisps(1,8), ', ', CrackDisps(1,9), ', ', CrackDisps(1,10), ', ', CrackDisps(1,11)
(I5,A2,F12.8,A2,F12.8,A2,F12.8,A2,F12.8,A2,F12.8,A2,F12.8)
*CFCLOS

/EOF
