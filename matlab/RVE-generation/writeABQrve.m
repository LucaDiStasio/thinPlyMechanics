function[projectName]=writeABQrve(logfullfile,spaceDim,workDir,index,elType,elOrder,ABQel,debug)
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
%  A function to generate FEM models of RVEs with ABAQUS, here space
%  dimension selection takes place
%
%  Output:
%
%%

writeToLogFile(logfullfile,'\n')
writeToLogFile(logfullfile,'In function: writeABQrve\n')
writeToLogFile(logfullfile,'\nStarting timer\n')
start = tic;

switch spaceDim
    case 2 % 2D
        if debug
          projectName = [datestr(now,'yyyy-mm-dd_HH-MM-SS'),'_RVE2D'];
        else
          modelCode = generateModelCode('RVE2D','ABQ',params);
          if ~checkIndex(workDir,strcat(index,'.csv'),modelCode)
            projectName = incrementName(workDir,strcat(index,'.csv'));
          else
            projectName = strcat('A model with this set of parameters already exists. See: ',getModelFolder(workDir,strcat(index,'.csv'),model));
            return
          end
        end
        % createWD(path,wd,csv,dat,json,latex)
        createWD(workDir,projectName,true,false,false,false);
        inpfullfile = fullfile(workDir,projectName,'input',[projectName,'.inp'])
        fileId = fopen(inpfullfile,'w');
        fprintf(fileId,'%s','**\n');
        fprintf(fileId,'%s','**\n');
        fprintf(fileId,'%s',['**Automatically created by Matlab on ',datestr(now,'dd/mm/yyyy'),' at ',datestr(now,'HH:MM:SS')]);
        fprintf(fileId,'%s','**\n');
        fprintf(fileId,'%s','**\n');
        fclose(fileId);
        writeToLogFile(logfullfile,['    Calling function ', 'writeABQrve2D',' ...\n']);
        writeABQrve2D(logfullfile,inpfullfile,elType,elOrder,ABQel);
    case 2.5 % 2&1/2 D
        if debug
          projectName = [datestr(now,'yyyy-mm-dd_HH-MM-SS'),'_RVE2D'];
        else
          modelCode = generateModelCode('RVE2andHalfD','ABQ',params);
          if ~checkIndex(workDir,strcat(index,'.csv'),modelCode)
            projectName = incrementName(workDir,strcat(index,'.csv'));
          else
            projectName = strcat('A model with this set of parameters already exists. See: ',getModelFolder(workDir,strcat(index,'.csv'),model));
            return
          end
        end
        % createWD(path,wd,csv,dat,json,latex)
        createWD(workDir,projectName,true,false,false,false);
        inpfullfile = fullfile(workDir,projectName,'input',[projectName,'.inp'])
        fileId = fopen(inpfullfile,'w');
        fprintf(fileId,'%s','**\n');
        fprintf(fileId,'%s','**\n');
        fprintf(fileId,'%s',['**Automatically created by Matlab on ',datestr(now,'dd/mm/yyyy'),' at ',datestr(now,'HH:MM:SS')]);
        fprintf(fileId,'%s','**\n');
        fprintf(fileId,'%s','**\n');
        fclose(fileId);
        writeToLogFile(logfullfile,['    Calling function ', 'writeABQrve2D',' ...\n']);
        writeABQrve2andHalfD(logfullfile,inpfullfile,elType,elOrder,ABQel);
    case 3 % 3D
        if debug
          projectName = [datestr(now,'yyyy-mm-dd_HH-MM-SS'),'_RVE2D'];
        else
          modelCode = generateModelCode('RVE3D','ABQ',params);
          if ~checkIndex(workDir,strcat(index,'.csv'),modelCode)
            projectName = incrementName(workDir,strcat(index,'.csv'));
          else
            projectName = strcat('A model with this set of parameters already exists. See: ',getModelFolder(workDir,strcat(index,'.csv'),model));
            return
          end
        end
        % createWD(path,wd,csv,dat,json,latex)
        createWD(workDir,projectName,true,false,false,false);
        inpfullfile = fullfile(workDir,projectName,'input',[projectName,'.inp'])
        fileId = fopen(inpfullfile,'w');
        fprintf(fileId,'%s','**\n');
        fprintf(fileId,'%s','**\n');
        fprintf(fileId,'%s',['**Automatically created by Matlab on ',datestr(now,'dd/mm/yyyy'),' at ',datestr(now,'HH:MM:SS')]);
        fprintf(fileId,'%s','**\n');
        fprintf(fileId,'%s','**\n');
        fclose(fileId);
        writeToLogFile(logfullfile,['    Calling function ', 'writeABQrve3D',' ...\n']);
        writeABQrve3D(logfullfile,inpfullfile,elType,elOrder,ABQel);
    otherwise
        if debug
          projectName = [datestr(now,'yyyy-mm-dd_HH-MM-SS'),'_RVE2D'];
        else
          modelCode = generateModelCode('RVE2D','ABQ',params);
          if ~checkIndex(workDir,strcat(index,'.csv'),modelCode)
            projectName = incrementName(workDir,strcat(index,'.csv'));
          else
            projectName = strcat('A model with this set of parameters already exists. See: ',getModelFolder(workDir,strcat(index,'.csv'),model));
            return
          end
        end
        % createWD(path,wd,csv,dat,json,latex)
        createWD(workDir,projectName,true,false,false,false);
        inpfullfile = fullfile(workDir,projectName,'input',[projectName,'.inp'])
        fileId = fopen(inpfullfile,'w');
        fprintf(fileId,'%s','**\n');
        fprintf(fileId,'%s','**\n');
        fprintf(fileId,'%s',['**Automatically created by Matlab on ',datestr(now,'dd/mm/yyyy'),' at ',datestr(now,'HH:MM:SS')]);
        fprintf(fileId,'%s','**\n');
        fprintf(fileId,'%s','**\n');
        fclose(fileId);
        writeToLogFile(logfullfile,['    Calling function ', 'writeABQrve2D',' ...\n']);
        writeABQrve2D(logfullfile,inpfullfile,elType,elOrder,ABQel);
end

fileId = fopen(fullfile(folder,strcat(index,'.csv')),'a');
fprintf(fileId,'%s',strcat(projectName,',',model));
fprintf(fileId,'\n');
fclose(fileId);

elapsed = toc(start);
writeToLogFile(logfullfile,'Timer stopped.\n')
writeToLogFile(logfullfile,['\nELAPSED WALLCLOCK TIME: ', num2str(elapsed),' [s]\n\n'])
writeToLogFile(logfullfile,'Exiting function: writeABQrve\n')

return
