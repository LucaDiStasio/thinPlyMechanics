function[projectName]=writeABQrve2D(logfullfile,inpfullfile,elType,elOrder,ABQel)
%%
%==============================================================================
% Copyright (c) 2016 - 2017 Université de Lorraine & Luleå tekniska universitet
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
% Neither the name of the Université de Lorraine & Luleå tekniska universitet
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
%  A function to generate FEM models of 2D RVEs with ABAQUS
%
%  Output:
%
%%

writeToLogFile(logfullfile,'In function: writeABQrve2D\n')
writeToLogFile(logfullfile,'\nStarting timer\n')
start = tic;

%% PREAMBLE
writeToLogFile(logfullfile,['    Calling function ', 'writeABQpreamble',' ...\n']);
writeABQpreamble(logfullfile,inpfullfile,title,subtitle,headerDict,holder,author,heading)
writeToLogFile(logfullfile,['    ... done.','\n'])

%% NODES AND ELEMENTS SECTION

writeToLogFile(logfullfile,['    Calling function ', 'writeABQmeshsec',' ...\n']);
writeABQmeshsec(abqpath);
writeToLogFile(logfullfile,['    ... done.','\n'])

padlength = length(fibers);
startNode = 1;
startEl = 1;
for i=1:length(fibers)
  writeToLogFile(logfullfile,['    Calling function ', 'writeABQfiber2D',' ...\n']);
  [Ntot,Etot] = writeABQfiber2D(logfullfile,inpfullfile,...
                                        i,padlength,elType,elOrder,ABQel,...
                                        fibers(i).xC,yC,fibers(i).Rcore,fibers(i).R,...
                                        startNode,startEl,...
                                        fibers(i).fiberMaterial,fibers(i).matrixMaterial,fibers(i).debonds,...
                                        fibers(i).thetasCore,fibers(i).deltasCore,...
                                        fibers(i).lthetaIntAnnulus,fibers(i).lRIntAnnulus,fibers(i).deltasIntAnnulus,fibers(i).NRIntAnnulus,...
                                        fibers(i).lthetaExtAnnulus,fibers(i).lRExtAnnulus,fibers(i).deltasExtAnnulus,fibers(i).NRExtAnnulus);
  writeToLogFile(logfullfile,['    ... done.','\n'])
  startNode = startNode + Ntot;
  startEl = startEl + Etot;
end

writeToLogFile(logfullfile,['    Calling function ', 'writeABQmatrix2D',' ...\n']);
[Ntot,Etot]=writeABQmatrix2D(logfullfile,inpfullfile,numFiber,padlength,elType,elOrder,ABQel,startNode,startEl,x0,y0,lx,ly,Nx,Ny);
writeToLogFile(logfullfile,['    ... done.','\n'])

%% SURFACES AND SURFACE INTERACTIONS SECTION

writeToLogFile(logfullfile,['    Calling function ', 'writeABQmeshinterfaces',' ...\n']);
writeABQmeshinterfaces(logfullfile,inpfullfile,length(fibers))

for i=1:length(fibers)

end

%% MATERIALS DEFINITION AND ASSIGNMENT SECTION
writeToLogFile(logfullfile,['    Calling function ', 'writeABQmaterialsdefinition',' ...\n']);
writeABQmaterialsdefinition(logfullfile,inpfullfile,matDBfolder,materialslist,unitConvFactor);
writeToLogFile(logfullfile,['    ... done.','\n'])

%% BOUNDARY CONDITIONS DEFINITION SECTION

%% STEPS SECTION: LOADS, IMPOSED DISPLACEMENTS AND OUTPUT REQUESTS

elapsed = toc(start);
writeToLogFile(logfullfile,'Timer stopped.\n')
writeToLogFile(logfullfile,['\nELAPSED WALLCLOCK TIME: ', num2str(elapsed),' [s]\n\n'])
writeToLogFile(logfullfile,'Exiting function: writeABQrve2D\n')

return
