function[]=writeABQpartiallybondedinterface(logfullfile,inpfullfile)
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
writeToLogFile(logfullfile,'In function: writeABQpartiallybondedinterface\n')
writeToLogFile(logfullfile,'\nStarting timer\n')
start = tic;

if strcomp(propagationMethod,'cohesive') || strcomp(propagationMethod,'Cohesive') || strcomp(propagationMethod,'COHESIVE')

elseif strcomp(propagationMethod,'xfem') || strcomp(propagationMethod,'XFEM') || strcomp(propagationMethod,'Xfem')

elseif strcomp(propagationMethod,'VCCTdebond') || strcomp(propagationMethod,'VCCTDebond') || strcomp(propagationMethod,'VCCTDEBOND') || strcomp(propagationMethod,'VCCT-debond') || strcomp(propagationMethod,'VCCT-Debond') || strcomp(propagationMethod,'VCCT-DEBOND')

elseif strcomp(propagationMethod,'userVCCTconnector') || strcomp(propagationMethod,'userVCCTConnector') || strcomp(propagationMethod,'UserVCCTConnector') || strcomp(propagationMethod,'USERVCCTCONNECTOR') || strcomp(propagationMethod,'userVCCT-connector') || strcomp(propagationMethod,'user-VCCT-connector') || strcomp(propagationMethod,'user-VCCTconnector') || strcomp(propagationMethod,'userVCCT-Connector') || strcomp(propagationMethod,'user-VCCT-Connector') || ...
       strcomp(propagationMethod,'user-VCCTConnector') || strcomp(propagationMethod,'UserVCCT-Connector') || strcomp(propagationMethod,'User-VCCTConnector') || strcomp(propagationMethod,'User-VCCT-Connector') || strcomp(propagationMethod,'USERVCCT-CONNECTOR') || strcomp(propagationMethod,'USER-VCCTCONNECTOR') || strcomp(propagationMethod,'USER-VCCT-CONNECTOR')

elseif strcomp(propagationMethod,'userVCCTequation') || strcomp(propagationMethod,'userVCCTEquation') || strcomp(propagationMethod,'UserVCCTEquation') || strcomp(propagationMethod,'USERVCCTEQUATION') || strcomp(propagationMethod,'userVCCT-equation') || strcomp(propagationMethod,'user-VCCT-equation') || strcomp(propagationMethod,'user-VCCTequation') || strcomp(propagationMethod,'userVCCT-Equation') || strcomp(propagationMethod,'user-VCCT-Equation') || ...
      strcomp(propagationMethod,'user-VCCTEquation') || strcomp(propagationMethod,'UserVCCT-Equation') || strcomp(propagationMethod,'User-VCCTEquation') || strcomp(propagationMethod,'User-VCCT-Equation') || strcomp(propagationMethod,'USERVCCT-EQUATION') || strcomp(propagationMethod,'USER-VCCTEQUATION') || strcomp(propagationMethod,'USER-VCCT-EQUATION')

else

end

elapsed = toc(start);
writeToLogFile(logfullfile,'Timer stopped.\n')
writeToLogFile(logfullfile,['\nELAPSED WALLCLOCK TIME: ', num2str(elapsed),' [s]\n\n'])
writeToLogFile(logfullfile,'Exiting function: writeABQpartiallybondedinterface\n')

return
