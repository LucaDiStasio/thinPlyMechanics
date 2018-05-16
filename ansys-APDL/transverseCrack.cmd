! Command File mode of 2D Model of Transverse Cracking in Thin-ply FRPC

/title, 2D Model of Transverse Cracking in Thin-ply FRPC

/prep7               ! Enter the pre-processor

! Parameters

L = 1       ! [mm] length of the element
t = 1       ! [mm] 2t = thickness of the element
tRatio = 1  ! [-]  ratio of bounding ply thickness to main ply
a = 0.5     ! [mm] 2a = crack length
w = 0.1     ! [mm] width of refined mesh region along the crack

tBPly = tRatio*(2*t)
tTotal = t + tBPly

! Create Geometry

BLC4, 0.0, 0.0, L, tTotal

K, 1, 0.0, a
K, 2, w, 0.0
K, 3, w, t
K, 4, 0.0, t
K, 5, L, t

L, 4, 5
L, 2, 3

! Define Element Type

ET,1,PLANE82
KEYOPT,1,3,3		! Plane stress element with thickness

! Define Material Properties

MP,EX,1,200000        ! mp,Young's modulus,material number,value
MP,PRXY,1,0.3         ! mp,Poisson's ratio,material number,value

! Define the number of elements each line is to be divided into
AESIZE,ALL,5    	  ! lesize,all areas,size of element

! Area Meshing
AMESH,ALL	  		! amesh, all areas

FINISH              ! Finish pre-processing

/SOLU               ! Enter the solution processor

ANTYPE,0			! Analysis type,static
