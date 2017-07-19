function[projectName]=writeABQrve2DquadsLin(workDir,index,fibers)
%%
%==============================================================================
% Copyright (c) 2016 Université de Lorraine & Luleå tekniska universitet
% Author: Luca Di Stasio <luca.distasio@gmail.com>
%                        <luca.distasio@ingpec.eu>
%
% Redistribution and use in source and binary forms, with or without
% modification, are permitted provided that the following conditions are met:
% 
% 
% Redistributions of source code must retain the above copyright
% notice, this list of conditions and the following disclaimer.
% Redistributions in binary form must reproduce the above copyright
% notice, this list of conditions and the following disclaimer in
% the documentation and/or other materials provided with the distribution
% Neither the name of the Université de Lorraine or Luleå tekniska universitet
% nor the names of its contributors may be used to endorse or promote products
% derived from this software without specific prior written permission.
% 
% THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
% AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
% IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
% ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
% LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
% CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
% SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
% INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
% CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
% ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
% POSSIBILITY OF SUCH DAMAGE.
%==============================================================================
%
%  DESCRIPTION
%  
%  A function to generate FEM models of 2D RVEs with ABAQUS using linear
%  quadrilateral elements
%
%  Input parameters
%      fibers : cell array of struct(s)
%
%
%  unitConvFactor(1)  => length
%  unitConvFactor(2)  => mass
%  unitConvFactor(3)  => time
%  unitConvFactor(4)  => electric current
%  unitConvFactor(5)  => thermodynamic temperature
%  unitConvFactor(6)  => amount of substance
%  unitConvFactor(7)  => luminous intensity
%  unitConvFactor(8)  => density
%  unitConvFactor(9)  => pressure/stress
%  unitConvFactor(10) => thermal expansion
%  unitConvFactor(11) => thermal conductivity
%  unitConvFactor(12) => specific heat capacity
%  unitConvFactor(13) => fracture toughness
%  unitConvFactor(14) => interface stiffness
%  unitConvFactor(15) => force
%
%%

%% CREATE FILES AND FOLDERS
%-------------------------------------------------------------------------%
%-------------------------------------------------------------------------%
%-                      Generate model code                              -%
%-------------------------------------------------------------------------%
%-------------------------------------------------------------------------%

modelCodeParams = [];

modelCode = generateModelCode('VL4MoM-FRPC-RVE-2DquadsLin','ABQ',modelCodeParams);

%-------------------------------------------------------------------------%
%-------------------------------------------------------------------------%
%-                          I/O settings                                 -%
%-------------------------------------------------------------------------%
%-------------------------------------------------------------------------%

projectName = '';

if ~checkIndex(workDir,strcat(index,'.csv'),modelCode)
    projectName = incrementName(workDir,strcat(index,'.csv'));
    createWD(workDir,projectName,true,false,false,false);
    solverinputFolderPath = fullfile(workDir,projectName,'input');
    solverinputMainFilePath = fullfile(workDir,projectName,'input',strcat(projectName,'.inp'));
    csvFolderPath = fullfile(workDir,projectName,'csv');
    logFolderPath = fullfile(workDir,projectName,'log');
    logPath = createLogFile(logFolderPath,'2D RVE FEM MODEL GENERATION');
    timeNow = clock;
    writeToLogFile(logPath,['Starting on ', date, ' at ',num2str(timeNow(4)),':',num2str(timeNow(5)),':',num2str(timeNow(6)),'\n\n']);
    writeToLogFile(logPath,['2D RVE with linear quadrilateral elements to be simulated in ABAQUS','\n\n']);
    writeToLogFile(logPath,['No previous project has been found with the same parameters','\n']);
    writeToLogFile(logPath,['Project folder created','\n']);
    writeToLogFile(logPath,['Subfolders solver,input,log,csv created','\n']);
else
    projectName = strcat('A model with this set of parameters already exists. See: ',getModelFolder(workDir,strcat(index,'.csv'),modelCode));
    return
end

%-------------------------------------------------------------------------%
%-------------------------------------------------------------------------%
%-                      Create main input file                           -%
%-------------------------------------------------------------------------%
%-------------------------------------------------------------------------%

try
    writeToLogFile(logPath,['\n','Creating main input file...','\n']);
    abqinpID = fopen(solverinputMainFilePath,'w');
    fclose(abqinpID);
    writeToLogFile(logPath,['... done.','\n']);
catch ME
    writeToLogFile(logPath,['... failed. An error occurred: ',ME.identifier,'\n\n']);
    writeToLogFile(logPath,['Failed to create input file','\n']);
    writeToLogFile(logPath,['FAILURE','\n']);
    projectName = 'An error occurred. See log file.';
    return
end

%% HEADER SECTION

%-------------------------------------------------------------------------%
%-------------------------------------------------------------------------%
%-                          Write header                                 -%
%-------------------------------------------------------------------------%
%-------------------------------------------------------------------------%

try
    writeToLogFile(logPath,['\n','Writing header...','\n']);
    
    writeToLogFile(logPath,['... done.','\n']);
catch ME
    writeToLogFile(logPath,['... failed. An error occurred: ',ME.identifier,'\n\n']);
    writeToLogFile(logPath,['Failed to create input file','\n']);
    writeToLogFile(logPath,['FAILURE','\n']);
    projectName = 'An error occurred. See log file.';
    return
end

%-------------------------------------------------------------------------%
%-------------------------------------------------------------------------%
%-                          Write license                                -%
%-------------------------------------------------------------------------%
%-------------------------------------------------------------------------%

try
    writeToLogFile(logPath,['\n','Writing license...','\n']);
    holder = 'Université de Lorraine or Luleå tekniska universitet';
    author = 'Luca Di Stasio';
    writeABQlicense(solverinputMainFilePath,holder,author);
    writeToLogFile(logPath,['... done.','\n']);
catch ME
    writeToLogFile(logPath,['... failed. An error occurred: ',ME.identifier,'\n\n']);
    writeToLogFile(logPath,['Failed to create input file','\n']);
    writeToLogFile(logPath,['FAILURE','\n']);
    projectName = 'An error occurred. See log file.';
    return
end

%-------------------------------------------------------------------------%
%-------------------------------------------------------------------------%
%-                         Write heading                                 -%
%-------------------------------------------------------------------------%
%-------------------------------------------------------------------------%

try
    writeToLogFile(logPath,['\n','Writing heading...','\n']);
    writeABQheading(solverinputMainFilePath,{['2D Micromechanical Simulation of RVEs: fiber volume fraction ',num2str(Vff)]},'none');
    writeToLogFile(logPath,['... done.','\n']);
catch ME
    writeToLogFile(logPath,['... failed. An error occurred: ',ME.identifier,'\n\n']);
    writeToLogFile(logPath,['Failed to create input file','\n']);
    writeToLogFile(logPath,['FAILURE','\n']);
    projectName = 'An error occurred. See log file.';
    return
end

%-------------------------------------------------------------------------%
%-------------------------------------------------------------------------%
%-                         Write preprint                                -%
%-------------------------------------------------------------------------%
%-------------------------------------------------------------------------%

try
    writeToLogFile(logPath,['\n','Writing preprint...','\n']);
    contact = 'YES';
    echo = 'NO';
    history = 'YES';
    printModel = 'YES';
    parsubstitution =  'YES';
    parvalues = 'YES';
    massprop = 'NO';
    writeABQpreprint(solverinputMainFilePath,contact,echo,history,printModel,parsubstitution,parvalues,massprop,{},'none');
    writeToLogFile(logPath,['... done.','\n']);
catch ME
    writeToLogFile(logPath,['... failed. An error occurred: ',ME.identifier,'\n\n']);
    writeToLogFile(logPath,['Failed to create input file','\n']);
    writeToLogFile(logPath,['FAILURE','\n']);
    projectName = 'An error occurred. See log file.';
    return
end


%%                           MODEL DEFINITION
%==========================================================================

try
    writeToLogFile(logPath,['\n','Writing model section title...','\n']);
    writeABQinpfilesection(solverinputMainFilePath,'MODEL');
    writeToLogFile(logPath,['... done.','\n']);
catch ME
    writeToLogFile(logPath,['... failed. An error occurred: ',ME.identifier,'\n\n']);
    writeToLogFile(logPath,['Failed to create input file','\n']);
    writeToLogFile(logPath,['FAILURE','\n']);
    projectName = 'An error occurred. See log file.';
    return
end

%% FIBERS
% compute bounding circle and bounding rect for each fiber
try
    writeToLogFile(logPath,['\n','Computing bounding circle and bounding rect for each fiber ...','\n']);
    for i=1:length(fibers)
        fibers(i) = computeBoundingCircle(fibers(i));
        fibers(i) = computeBoundingRect(fibers(i));
    end
    writeToLogFile(logPath,['... done.','\n']);
catch ME
    writeToLogFile(logPath,['... failed. An error occurred: ',ME.identifier,'\n\n']);
    writeToLogFile(logPath,['Failed to create input file','\n']);
    writeToLogFile(logPath,['FAILURE','\n']);
    projectName = 'An error occurred. See log file.';
    return
end
% check that fibers are not overlapping
try
    writeToLogFile(logPath,['\n','Checking that files are not overlapping ...','\n']);
    for i=1:length(fibers)
        for j=i+1:length(fibers)
            if checkCircleIntersections(fibers(i).boundingCircle,fibers(j).boundingCircle)>0
                writeToLogFile(logPath,['... done.','\n']);
                writeToLogFile(logPath,['Fiber ',num2str(i),' overlaps fiber ',num2str(j),'. The case is not admissible. Computation interrupted.','\n']);
                writeToLogFile(logPath,['Failed to create input file','\n']);
                writeToLogFile(logPath,['FAILURE','\n']);
                projectName = 'At least two fibers overlap. See log file.';
                return
            end
        end
    end
    writeToLogFile(logPath,['... done.','\n']);
catch ME
    writeToLogFile(logPath,['... failed. An error occurred: ',ME.identifier,'\n\n']);
    writeToLogFile(logPath,['Failed to create input file','\n']);
    writeToLogFile(logPath,['FAILURE','\n']);
    projectName = 'An error occurred. See log file.';
    return
end
for i=1:length(fibers)
    % create input sub-file to be included in the main input file
    try
        writeToLogFile(logPath,['\n','Creating input file for fiber n. ',num2str(i),' ...','\n']);
        inputSubFilePath = fullfile(solverinputFolderPath,strcat('fiber',num2str(i),'.inp'));
        abqinpID = fopen(inputSubFilePath,'w');
        fclose(abqinpID);
        writeToLogFile(logPath,['... done.','\n']);
    catch ME
        writeToLogFile(logPath,['... failed. An error occurred: ',ME.identifier,'\n\n']);
        writeToLogFile(logPath,['Failed to create input file','\n']);
        writeToLogFile(logPath,['FAILURE','\n']);
        projectName = 'An error occurred. See log file.';
        return
    end
    % write data to input sub-file
    try
        writeToLogFile(logPath,['\n','Generating mesh and writing to input file for fiber n. ',num2str(i),' ...','\n']);
        
        writeToLogFile(logPath,['... done.','\n']);
    catch ME
        writeToLogFile(logPath,['... failed. An error occurred: ',ME.identifier,'\n\n']);
        writeToLogFile(logPath,['Failed to create input file','\n']);
        writeToLogFile(logPath,['FAILURE','\n']);
        projectName = 'An error occurred. See log file.';
        return
    end
    % include input sub-file in main file
    try
        writeToLogFile(logPath,['\n','Including input sub-file in main file ...\n']);
        writeABQinclude(solverinputMainFilePath,inputSubFilePath,'none',{},['fiber n. ',num2str(i),' model data']);
        writeToLogFile(logPath,['... done.','\n']);
    catch ME
        writeToLogFile(logPath,['... failed. An error occurred: ',ME.identifier,'\n\n']);
        writeToLogFile(logPath,['Failed to create input file','\n']);
        writeToLogFile(logPath,['FAILURE','\n']);
        projectName = 'An error occurred. See log file.';
        return
    end
end

%% MATRIX

%% MATERIALS

%% SURFACE INTERACTIONS

%% BOUNDARY CONDITIONS

%% INITIAL CONDITIONS

%% HISTORY DEFINITION
%% PROGRAM COMPLETION
%-------------------------------------------------------------------------%
%-------------------------------------------------------------------------%
%-           On successful completion, add project to index              -%
%-------------------------------------------------------------------------%
%-------------------------------------------------------------------------%

updateProjectsIndex(workDir,index,projectName,modelCode);
writeToLogFile(logPath,['Projects'' index updated','\n\n'])
writeToLogFile(logPath,['Input file successfully created','\n'])
writeToLogFile(logPath,['SUCCESS','\n'])

return