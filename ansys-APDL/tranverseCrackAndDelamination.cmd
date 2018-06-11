! Command File mode of 2D Model of Transverse Cracking in Thin-ply FRPC

/title, 2D Model of Transverse Cracking in Thin-ply FRPC

/prep7               ! Enter the pre-processor

! Parameters

! ===> START INPUT DATA

Vf = 0.0! [-] Fiber volume fraction

t = 1             ! [mm] 2t = thickness of the element
tRatio = 49.5     ! [-]  ratio of bounding ply thickness to main ply
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
K,16, vcctRegion,t

K,17, L, t

! Lines

L, 1, 2            !1
L, 2, 6            !2
L, 1, 8            !3
L, 1, 8            !4
L, 1, 8            !5
L, 1, 8            !6
L, 1, 8            !7
L, 1, 8            !8
L, 1, 8            !9
L, 1, 8            !10
L, 1, 8            !11
L, 1, 8            !12
L, 1, 8            !13
L, 1, 8            !14
L, 1, 8            !15
