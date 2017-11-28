function[projectName]=writeFEMrve(femSolver,spaceDim,workDir,index,elType,elOrder,SOLVERel,debug)
%%
%==============================================================================
% Copyright (c) 2016-2017 Universite de Lorraine & Lulea tekniska universitet
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
% Neither the name of the Universit� de Lorraine or Lule� tekniska universitet
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
%  A function to generate FEM models of RVEs with different solver, here
%  solver's selection takes place
%
%  Output:
%
%%

logfullfile = fullfile(workDir,[datestr(now,'yyyy-mm-dd_HH-MM-SS'),'_RVEgeneration.log']);

if exist(logfullfile,'file')~=2
  fileId = fopen(logfullfile,'w');
  fprintf(fileId,'%s',['Automatically created by Matlab on ',datestr(now,'dd/mm/yyyy'),' at ',datestr(now,'HH:MM:SS')]);
  fclose(fileId);
end

writeToLogFile(logfullfile,'\n')
writeToLogFile(logfullfile,'In function: writeFEMrve\n')
writeToLogFile(logfullfile,'\nStarting timer\n')
start = tic;

writeToLogFile(logfullfile,'FEM solver?\n')
switch femSolver
    case 1 % ABAQUS
        writeToLogFile(logfullfile,'==> ABAQUS\n')
        writeToLogFile(logfullfile,['    Calling function ', 'writeABQrve',' ...\n']);
        projectName = writeABQrve(logfullfile,spaceDim,workDir,index,elType,elOrder,SOLVERel,debug);
    case 2 % CALCULIX
        writeToLogFile(logfullfile,'==> CALCULIX\n')
        writeToLogFile(logfullfile,['    Calling function ', 'writeCCXrve',' ...\n']);
        projectName = writeCCXrve(logfullfile,spaceDim,workDir,index,elType,elOrder,SOLVERel,debug);
    case 3 % ANSYS
        writeToLogFile(logfullfile,'==> ANSYS\n')
        writeToLogFile(logfullfile,['    Calling function ', 'writeANSrve',' ...\n']);
        projectName = writeANSrve(logfullfile,spaceDim,workDir,index,elType,elOrder,SOLVERel,debug);
    case 4 % CODE ASTER
        writeToLogFile(logfullfile,'==> CODE ASTER\n')
        writeToLogFile(logfullfile,['    Calling function ', 'writeASTrve',' ...\n']);
        projectName = writeASTrve(logfullfile,spaceDim,workDir,index,elType,elOrder,SOLVERel,debug);
    case 5 % MSC NASTRAN
        writeToLogFile(logfullfile,'==> MSC NASTRAN\n')
        writeToLogFile(logfullfile,['    Calling function ', 'writeMSCrve',' ...\n']);
        projectName = writeMSCrve(logfullfile,spaceDim,workDir,index,elType,elOrder,SOLVERel,debug);
    otherwise
        writeToLogFile(logfullfile,'==> ABAQUS (default)\n')
        writeToLogFile(logfullfile,['    Calling function ', 'writeABQrve',' ...\n']);
        projectName = writeABQrve(logfullfile,spaceDim,workDir,index,elType,elOrder,SOLVERel,debug);
end

elapsed = toc(start);
writeToLogFile(logfullfile,'Timer stopped.\n')
writeToLogFile(logfullfile,['\nELAPSED WALLCLOCK TIME: ', num2str(elapsed),' [s]\n\n'])
writeToLogFile(logfullfile,'Exiting function: writeFEMrve\n')

return
