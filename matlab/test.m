clear all;
close all;
clc

matDbfolder = 'D:\OneDrive\01_Luca\07_DocMASE\07_Data\02_Material-Properties';

projectName=rve_mesh_create_project('VL4FC-2DmmTPL-IC-1-1-1-1-1-0-1-1-1-0-1-0-1-0.6-0.6-30-10-0-0-0.01-1-1-1-1-0.5-0.782107-1.05-20-20-20-20-20-20-6921.-6800.',...
                                    'D:\OneDrive\01_Luca\07_DocMASE\07_Data\03_FEM',matDbfolder,'projectsIndex',...
                                     1,1,1,0,0,0,1,1,1,0,1,0,1,0.6,0.6,30,10,0,0,0.01,1,1,1,1,[1e6;1e0;1e0;1e0;1e0;1e0;1e0;1e-18;1e-6;1e0;1e0;1e0;1e0;1e-12;1e6],...
                                     0.5,0.782107,1.05,20,20,20,20,20,20,6921.,6800.);
disp(projectName);