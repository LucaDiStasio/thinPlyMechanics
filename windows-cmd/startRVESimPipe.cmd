SET pyfolder=D://OneDrive/01_Luca/07_DocMASE/06_WD/thin_ply_mechanics/python
SET pyexec=runAbaqus
SET inputdeck=2017-01-26_AbaqusInputDeck
SET inputdir=D://01_Luca/07_Data/03_FEM
SET workdir=D://01_Luca/07_Data/03_FEM

python %pyfolder%/%pyexec%.py -i %inputdeck%.csv -d %inputdir% -w %workdir%

prompt $D$S$T$S$P$G && d: && cd 01*/07*/03*/Curved* && abaqus CAE noGUI=D:/01_Luca/06_WD/thinPlyMechanics/python/createAndAnalyzeRVEs.py -- -dir D:/OneDrive/01_Luca/07_DocMASE/07_Data/03_FEM/InputData -data inputRVEdataL1_144.deck -iterables inputRVEiterablesL1_144.deck -plot inputRVEplot
