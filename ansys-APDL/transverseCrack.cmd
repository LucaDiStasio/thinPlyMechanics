! Command File mode of 2D Model of Transverse Cracking in Thin-ply FRPC

/title, 2D Model of Transverse Cracking in Thin-ply FRPC

/prep7               ! Enter the pre-processor

! Parameters

L = 1       ! [mm] length of the element
t = 1       ! [mm] 2t = thickness of the element
tRatio = 1  ! [-]  ratio of bounding ply thickness to main ply

! Create Geometry

BLC4, XCORNER, YCORNER, WIDTH, HEIGHT, DEPTH
