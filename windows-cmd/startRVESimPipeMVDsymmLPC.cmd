cd C:/Abaqus_WD/CurvedInterface && abaqus CAE noGUI=C:/02_Local-folder/01_Luca/01_WD/thinPlyMechanics/python/createAndAnalyzeMultipleVerticalDebondRVEs.py -- -dir C:/Users/lucad/OneDrive/01_Luca/07_DocMASE/07_Data/03_FEM/InputData/MultipleVerticalDebonds -data inputRVEdataMVDvksymmL%1-LPC.deck -iterables inputRVEiterablesMVDvksymmL%1-LPC.deck -plot inputRVEplot && python C:/02_Local-folder/01_Luca/01_WD/thinPlyMechanics/python/reportData.py -w C:/Users/lucad/OneDrive/01_Luca/07_DocMASE/07_Data/03_FEM/LucaPC/sweepOverDeltathetaMVDvksymmL%1 -i ABQ-RVE-generation-and-analysis_csvfileslist.csv -f sweepL%1.xlsx --excel
