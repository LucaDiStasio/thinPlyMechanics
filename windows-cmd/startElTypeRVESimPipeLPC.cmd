cd C:/Abaqus_WD/CurvedInterface && abaqus CAE noGUI=C:/02_Local-folder/01_Luca/01_WD/thinPlyMechanics/python/createAndAnalyzeRVEs.py -- -dir C:/Users/lucad/OneDrive/01_Luca/07_DocMASE/07_Data/03_FEM/InputData/ElType -data inputRVEdata%1GPE-LPC.deck -iterables inputRVEiterablesL%1GPE-LPC.deck -plot inputRVEplot && python C:/02_Local-folder/01_Luca/01_WD/thinPlyMechanics/python/reportData.py -w C:/Users/lucad/OneDrive/01_Luca/07_DocMASE/07_Data/03_FEM/LucaPC/sweepOverDeltatheta%1GPE -i ABQ-RVE-generation-and-analysis_csvfileslist.csv -f sweep%1.xlsx --excel && cd C:/Abaqus_WD/CurvedInterface && abaqus CAE noGUI=C:/02_Local-folder/01_Luca/01_WD/thinPlyMechanics/python/createAndAnalyzeRVEs.py -- -dir C:/Users/lucad/OneDrive/01_Luca/07_DocMASE/07_Data/03_FEM/InputData/ElType -data inputRVEdata%1PS-LPC.deck -iterables inputRVEiterablesL%1PS-LPC.deck -plot inputRVEplot && python C:/02_Local-folder/01_Luca/01_WD/thinPlyMechanics/python/reportData.py -w C:/Users/lucad/OneDrive/01_Luca/07_DocMASE/07_Data/03_FEM/LucaPC/sweepOverDeltatheta%1PS -i ABQ-RVE-generation-and-analysis_csvfileslist.csv -f sweep%1.xlsx --excel
