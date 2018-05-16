! Command File mode of 2D Model of Transverse Cracking in Thin-ply FRPC

/title, 2D Model of Transverse Cracking in Thin-ply FRPC

/prep7               ! Enter the pre-processor

! Parameters

Vf = ! [-] Fiber volume fraction

L = 1       ! [mm] length of the element
t = 1       ! [mm] 2t = thickness of the element
tRatio = 1  ! [-]  ratio of bounding ply thickness to main ply
a = 0.5     ! [mm] 2a = crack length
w = 0.1     ! [mm] width of refined mesh region along the crack

EL = ! [MPa] UD longitudinal Young's modulus
ET = ! [MPa] UD transverse Young's modulus
nuLT = ! [-] UD in-plane Poisson ratio
nuTT = ! [-] UD transverse Poisson ratio
GL = ! [MPa] UD in-plane shear modulus
GT = ! [MPa] UD transverse shear modulus

tBPly = tRatio*(2*t)
tTotal = t + tBPly

! Create Geometry

BLC4, 0.0, 0.0, L, tTotal

K, 1, 0.0, 0.0
K, 2, L, 0.0
K, 3, L, tTOT
K, 4, 0.0, tTOT

K, 5, w, 0.0
K, 6, w, t
K, 7, 0.0, t
K, 8, L, t

K, 9, 0.0, a

L, 1, 2
L, 2, 3
L, 3, 4
L, 4, 1

L, 7, 8
L, 5, 6

! Define Element Type

ET,1,PLANE83
KEYOPT,1,3,3		! Plane stress element with thickness

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
