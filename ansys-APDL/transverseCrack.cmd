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


FINISH              ! Finish pre-processing

/SOLU               ! Enter the solution processor

ANTYPE,0			! Analysis type,static
