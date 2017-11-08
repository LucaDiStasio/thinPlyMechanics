function[projectName]=writeABQmaterialsdefinition(logfullfile,inpfullfile,matDBfolder,materialslist,unitConvFactor)
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
%  materialslist: [N x 2] - vector - {[material name, material input type in Abaqus (isotropic, engineering constants, ...)]}
%
%%
writeToLogFile(logfullfile,'In function: writeABQmaterialregions\n')
writeToLogFile(logfullfile,'\nStarting timer\n')
start = tic;

for i=1:length(materialslist)
  writeToLogFile(logfullfile,['    Reading material ', materialslist{i},' ...\n']);
  writeToLogFile(logfullfile,['    Calling function ', 'getValuesFromCSV',' ...\n']);
  try
    props = getValuesFromCSV(matDBfolder,strcat(materialslist{i}(1),'.csv'),2,0,9);
    unitConv = getValuesFromCSV(matDBfolder,strcat(materialslist{i}(1),'.csv'),1,0,9);
    rho    = props(1)*unitConv(1);
    E1     = props(2)*unitConv(2);
    E2     = props(3)*unitConv(3);
    G12    = props(4)*unitConv(4);
    nu12   = props(5)*unitConv(5);
    nu23   = props(6)*unitConv(6);
    alpha1 = props(7)*unitConv(7);
    alpha2 = props(8)*unitConv(8);
    writeABQmaterial(inpfullfile,materialslist{i}(1),'none','none','none',{},'none');
    if strcomp(materialslist{i}(2),'ENGINEERING CONSTANTS') || strcomp(materialslist{i}(2),'engineering constants') || strcomp(materialslist{i}(2),'Engineering Constants') || strcomp(materialslist{i}(2),'Engineering constants')
      writeABQelastic(abqpath,'none','none','none','ENGINEERING CONSTANTS',...
                        {strcat(num2str(E2*unitConvFactor(9), '%10.5e'),', ',num2str(E2*unitConvFactor(9), '%10.5e'),', ',num2str(E1*unitConvFactor(9), '%10.5e'),...
                        ', ',num2str(nu23, '%10.5e'),', ',num2str((E2/E1)*nu12, '%10.5e'),', ',num2str((E2/E1)*nu12, '%10.5e'),...
                        ', ',num2str((0.5*E2/(1+nu23))*unitConvFactor(9), '%10.5e'),', ',num2str(G12*unitConvFactor(9), '%10.5e'));...
                        num2str(G12*unitConvFactor(9), '%10.5e')},...
                        'E2 E2 E1 nu23 nu21 nu31 G23 G21 G31');
      writeABQdensity(abqpath,'none','none',{num2str(rho*unitConvFactor(8), '%10.5e')},'rho');
      writeABQexpansion(abqpath,'none','none','none','ORTHO','none','none',...
                          {strcat(num2str(alpha2*unitConvFactor(10), '%10.5e'),', ',num2str(alpha2*unitConvFactor(10), '%10.5e'),', ',num2str(alpha1*unitConvFactor(10), '%10.5e'))},'alpha22, alpha22, alpha11');

    elseif strcomp(materialslist{i}(2),'ISOTROPIC') || strcomp(materialslist{i}(2),'isotropic') || strcomp(materialslist{i}(2),'Isotropic')
      writeABQelastic(inpfullfile,'none','none','none','ISOTROPIC',{strcat(num2str(E1*unitConvFactor(9), '%10.5e'),', ',num2str(nu12, '%10.5e'))},'E nu');
      writeABQdensity(inpfullfile,'none','none',{num2str(rho*unitConvFactor(8), '%10.5e')},'rho');
      writeABQexpansion(inpfullfile,'none','none','none','ISO','none','none',{strcat(num2str(alpha1*unitConvFactor(10), '%10.5e'))},'alpha');
    end
  catch ME
    writeToLogFile(logfullfile,['An error occurred: ', ME.identifier])
    writeToLogFile(logfullfile,['Terminating program.','\n'])
    exit(2)
  end
  writeToLogFile(logfullfile,['    ... done.\n']);
end

elapsed = toc(start);
writeToLogFile(logfullfile,'Timer stopped.\n')
writeToLogFile(logfullfile,['\nELAPSED WALLCLOCK TIME: ', num2str(elapsed),' [s]\n\n'])
writeToLogFile(logfullfile,'Exiting function: writeABQmaterialregions\n')

return
