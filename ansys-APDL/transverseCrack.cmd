! Command File mode of 2D Model of Transverse Cracking in Thin-ply FRPC

/title, 2D Model of Transverse Cracking in Thin-ply FRPC

/prep7               ! Enter the pre-processor

! Parameters

Vf = ! [-] Fiber volume fraction

t = 1             ! [mm] 2t = thickness of the element
tRatio = 1        ! [-]  ratio of bounding ply thickness to main ply
atRatio = 0.1     ! [-]  ratio of crack length to main ply thickness
rhon = 0.01       ! [-]  normalized crack density

EL = ! [MPa] UD longitudinal Young's modulus
ET = ! [MPa] UD transverse Young's modulus
nuLT = ! [-] UD in-plane Poisson ratio
nuTT = ! [-] UD transverse Poisson ratio
GL = ! [MPa] UD in-plane shear modulus
GT = ! [MPa] UD transverse shear modulus

L = t/rhon        ! [mm] length of the RVE
a = atRatio*t     ! [mm] 2a = crack length

tBPly = tRatio*(2*t) ! [mm] thickness of the bounding ply
tTotal = t + tBPly   ! [mm] thickness of the bounding ply

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
K, 10, 0.0, a       ! W corner in refined area interface
K, 11, a, a         ! E corner in refined area interface

! Lines

L, 1, 2            !1
L, 2, 6            !2
L, 6, 3            !3
L, 3, 4            !4
L, 4, 5            !5
L, 5, 1            !6

L, 5, 6            !7, ply interface
L, 8, 9            !8, refined area interface

! Areas

al, 1, 8, 9, 6     ! lower ply, refined area
al, 8, 2, 7, 9     ! lower ply, coarse area
al, 7, 3, 4, 5     ! upper ply

! Define Element Type

ET,1,PLANE83,0,,2      ! Quadratic plane strain quadrilaterals 
ET,1,PLANE83,1,,2      ! Quadratic plane strain triangles

! Define Material Properties

MP,EX,1,ET        ! 1 is cross-ply, 2 is ud-ply 
MP,EY,1,ET        ! 1 is cross-ply, 2 is ud-ply
MP,EZ,1,EL        ! 1 is cross-ply, 2 is ud-ply
MP,NUXY,1,nuTT    ! mp,Poisson's ratio,material number,value
MP,NUYZ,1,nuLT    ! mp,Poisson's ratio,material number,value
MP,NUXZ,1,nuLT    ! mp,Poisson's ratio,material number,value
MP,GXY,1,GTT      ! mp,Poisson's ratio,material number,value
MP,GYZ,1,GLT      ! mp,Poisson's ratio,material number,value
MP,GXZ,1,GLT      ! mp,Poisson's ratio,material number,value
MP,EX,2,EL        ! 1 is cross-ply, 2 is ud-ply 
MP,EY,2,ET        ! 1 is cross-ply, 2 is ud-ply
MP,EZ,2,ET        ! 1 is cross-ply, 2 is ud-ply
MP,NUXY,2,nuLT    ! mp,Poisson's ratio,material number,value
MP,NUYZ,2,nuTT    ! mp,Poisson's ratio,material number,value
MP,NUXZ,2,nuLT    ! mp,Poisson's ratio,material number,value
MP,GXY,2,GLT      ! mp,Poisson's ratio,material number,value
MP,GYZ,2,GTT      ! mp,Poisson's ratio,material number,value
MP,GXZ,2,GLT      ! mp,Poisson's ratio,material number,value

! Define the number of elements each line is to be divided into
AESIZE,ALL,5    	  ! lesize,all areas,size of element

! Area Meshing
AMESH,ALL	  		! amesh, all areas

FINISH              ! Finish pre-processing

/SOLU               ! Enter the solution processor

ANTYPE,0			! Analysis type,static
