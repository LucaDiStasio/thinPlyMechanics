cd D:/01*/07*/03*/Curved* && abaqus CAE noGUI=D:/01_Luca/06_WD/thinPlyMechanics/python/createAndAnalyzeRVEs.py -- -dir D:/OneDrive/01_Luca/07_DocMASE/07_Data/03_FEM/InputData/asymm -data inputRVEdataAsymmL%1-LPC.deck -iterables inputRVEiterablesAsymmL%1-LPC.deck -plot inputRVEplot && python D:/01_Luca/06_WD/thinPlyMechanics/python/reportData.py -w D:/OneDrive/01_Luca/07_DocMASE/07_Data/03_FEM/LucaPC/sweepOverDeltathetaAsymmL%1 -i ABQ-RVE-generation-and-analysis_csvfileslist.csv -f sweepAsymmL%1.xlsx --excel
