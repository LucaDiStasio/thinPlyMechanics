function[]=writeABQmeshinterfaces(logfullfile,inpfullfile,numFibers)
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
%  A function to generate FEM models of RVEs with ABAQUS, here space
%  dimension selection takes place
%
%  Output:
%
%%
writeToLogFile(logfullfile,'In function: writeABQmeshinterfaces\n')
writeToLogFile(logfullfile,'\nStarting timer\n')
start = tic;

for i=1:numFibers
  % use node-based surface definition
  % fiber core to fiber annulus interface
  writeABQsurface(abqpath,['FiberCoreSurface-Fiber',pad(num2str(i),numFibers,'left','0')],'none','none','none','none','none','none','none','none','NODE','none','none','none','none',...
                            {['NODES-CORE-INTERFACE-FIBER',pad(num2str(numFiber),numFibers,'left','0')]},'Fiber core surface');
  writeABQsurface(abqpath,['FiberAnnulusIntSurface-Fiber',pad(num2str(i),numFibers,'left','0')],'none','none','none','none','none','none','none','none','NODE','none','none','none','none',...
                            {['NODES-ANNULUS-INTINTERFACE-FIBER',pad(num2str(numFiber),numFibers,'left','0')]},'Fiber annulus internal surface');
  % tie constraint
  writeABQtie(abqpath,['FiberInternalMeshContraint-Fiber',pad(num2str(i),numFibers,'left','0')],'none','none','YES','none','none','none','none','SURFACE TO SURFACE',...
          {'FiberAnnulusIntSurface-Fiber',pad(num2str(i),numFibers,'left','0'),', ','FiberCoreSurface-Fiber',pad(num2str(i),numFibers,'left','0')},'tie constraint to ensure mesh continuity');
  % matrix annulus to matrix bulk interface
  writeABQsurface(abqpath,['MatrixAnnulusExtSurface-Fiber',pad(num2str(i),numFibers,'left','0')],'none','none','none','none','none','none','none','none','NODE','none','none','none','none',...
                            {['NODES-ANNULUS-EXTINTERFACE-MATRIX',pad(num2str(numFiber),numFibers,'left','0')]},'Matrix annulus surface');
  writeABQsurface(abqpath,['MatrixBulkSurface-Fiber',pad(num2str(i),numFibers,'left','0')],'none','none','none','none','none','none','none','none','NODE','none','none','none','none',...
                            {['NODES-MATRIX-INTERFACE-WITH-FIBER',pad(num2str(numFiber),numFibers,'left','0')]},'Matrix internal surface');
  % tie constraint
  writeABQtie(abqpath,['MatrixInternalMeshContraint-Fiber',pad(num2str(i),numFibers,'left','0')],'none','none','YES','none','none','none','none','SURFACE TO SURFACE',...
          {'MatrixAnnulusExtSurface-Fiber',pad(num2str(i),numFibers,'left','0'),', ','MatrixBulkSurface-Fiber',pad(num2str(i),numFibers,'left','0')},'tie constraint to ensure mesh continuity');
end

elapsed = toc(start);
writeToLogFile(logfullfile,'Timer stopped.\n')
writeToLogFile(logfullfile,['\nELAPSED WALLCLOCK TIME: ', num2str(elapsed),' [s]\n\n'])
writeToLogFile(logfullfile,'Exiting function: writeABQmeshinterfaces\n')

return
