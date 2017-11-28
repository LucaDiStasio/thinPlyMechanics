function[]=writeABQpartiallybondedinterface(logfullfile,inpfullfile,elOrder,Nnodes,RVEl,numFiber,padlength,numDebonds,frictionLess,interfaceFriction)
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
  writeABQsurface(abqpath,['FiberSurface-Fiber',pad(num2str(i),numFibers,'left','0')],'none','none','none','none','none','none','none','none','NODE','none','none','none','none',...
                            {['NODES-ANNULUS-EXTINTERFACE-FIBER',pad(num2str(numFiber),numFibers,'left','0')]},'Fiber surface');
  writeABQsurface(abqpath,['MatrixInterfaceSurface-Fiber',pad(num2str(i),numFibers,'left','0')],'none','none','none','none','none','none','none','none','NODE','none','none','none','none',...
                            {['NODES-ANNULUS-INTINTERFACE-MATRIX',pad(num2str(numFiber),numFibers,'left','0')]},'Matrix surface at fiber interface');
  % contact interaction
  writeABQcontactpair(abqpath,['FiberMatrixInterfaceInteraction-Fiber',pad(num2str(i),numFibers,'left','0')],'none','none','none','none','none','none','none','none','none','none','none','none','none','NODE TO SURFACE',...
                               {['MatrixInterfaceSurface-Fiber',pad(num2str(i),numFibers,'left','0'),', FiberSurface-Fiber',pad(num2str(i),numFibers,'left','0')]},'slave, master');
  writeABQsurfaceinteraction(abqpath,['FiberMatrixInterfaceInteraction-Fiber',pad(num2str(i),numFibers,'left','0')],'none','none','none','none','none','none',{'1.0'},'Out-of-plane thickness of the surface');
  if ~frictionLess>0
      writeABQfriction(abqpath,'none','none','none','0.005','none','none','none','none','none','none','none','none','none',{num2str(interfaceFriction, '%10.5e')},'friction coefficient');
  end
  writeABQinitialconditions(abqpath,'CONTACT','none','none','none','none','none','none','none','none','none','none','none','none','none','none','none','none','none','none','none','none',...
                          {['MatrixInterfaceSurface-Fiber',pad(num2str(i),numFibers,'left','0'),', FiberSurface-Fiber',pad(num2str(i),numFibers,'left','0'),',','NODES-ALLBONDED-MATRIXSURF-MATRIX',pad(num2str(numFiber),padlength,'left','0')]},'none');
elseif strcomp(propagationMethod,'userVCCTequation') || strcomp(propagationMethod,'userVCCTEquation') || strcomp(propagationMethod,'UserVCCTEquation') || strcomp(propagationMethod,'USERVCCTEQUATION') || strcomp(propagationMethod,'userVCCT-equation') || strcomp(propagationMethod,'user-VCCT-equation') || strcomp(propagationMethod,'user-VCCTequation') || strcomp(propagationMethod,'userVCCT-Equation') || strcomp(propagationMethod,'user-VCCT-Equation') || ...
      strcomp(propagationMethod,'user-VCCTEquation') || strcomp(propagationMethod,'UserVCCT-Equation') || strcomp(propagationMethod,'User-VCCTEquation') || strcomp(propagationMethod,'User-VCCT-Equation') || strcomp(propagationMethod,'USERVCCT-EQUATION') || strcomp(propagationMethod,'USER-VCCTEQUATION') || strcomp(propagationMethod,'USER-VCCT-EQUATION')
    % tied fiber surface
    writeABQsurface(abqpath,['FiberBondedSurface-Fiber',pad(num2str(numFiber),padlength,'left','0')],'none','none','none','none','none','none','none','none','ELEMENT','none','none','none','none',...
                    {['ELEMENTS-BONDED-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'S3']},'fiber surface');
    % tied matrix surface at fiber interface
    writeABQsurface(abqpath,['MatrixAtFiberInterfaceBondedSurface-Fiber',pad(num2str(numFiber),padlength,'left','0')],'none','none','none','none','none','none','none','none','ELEMENT','none','none','none','none',...
                    {['ELEMENTS-BONDED-MATRIXSURF-MATRIX',pad(num2str(numFiber),padlength,'left','0'),'S1']},'matrix surface at fiber interface');
    % tie constraint
    writeABQtie(abqpath,['FiberMatrixBondedInterface-Fiber',pad(num2str(i),numFibers,'left','0')],'none','none','YES','none','none','none','none','SURFACE TO SURFACE',...
            {'MatrixAtFiberInterfaceBondedSurface-Fiber',pad(num2str(i),numFibers,'left','0'),', ','FiberBondedSurface-Fiber',pad(num2str(i),numFibers,'left','0')},'tie constraint');
    for i=1:numDebonds
      % debonded fiber surface
      writeABQsurface(abqpath,['FiberDebondedSurface-Fiber',pad(num2str(numFiber),padlength,'left','0'),'-Debond',pad(num2str(i),padlength,'left','0')],'none','none','none','none','none','none','none','none','ELEMENT','none','none','none','none',...
                      {['ELEMENTS-DEBOND-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(i),padlength,'left','0'),'S3']},'fiber surface');
      % debonded matrix surface at fiber interface
      writeABQsurface(abqpath,['MatrixAtFiberInterfaceDebondedSurface-Fiber',pad(num2str(numFiber),padlength,'left','0'),'-Debond',pad(num2str(i),padlength,'left','0')],'none','none','none','none','none','none','none','none','ELEMENT','none','none','none','none',...
                      {['ELEMENTS-DEBOND-MATRIXSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(i),padlength,'left','0'),'S1']},'matrix surface at fiber interface');
      % debond contact interaction
      writeABQcontactpair(abqpath,['DebondContactInteraction-Fiber',pad(num2str(numFiber),padlength,'left','0'),'-Debond',pad(num2str(i),padlength,'left','0')],'none','none','none','none','none','none','none','SMALL SLIDING','none','none','none','none','none','SURFACE TO SURFACE',...
                           {['MatrixAtFiberInterfaceDebondedSurface-Fiber',pad(num2str(numFiber),padlength,'left','0'),'-Debond',pad(num2str(i),padlength,'left','0'),', FiberDebondedSurface-Fiber',pad(num2str(numFiber),padlength,'left','0'),'-Debond',pad(num2str(i),padlength,'left','0')]},'slave, master');
      writeABQsurfaceinteraction(abqpath,['DebondContactInteraction-Fiber',pad(num2str(numFiber),padlength,'left','0'),'-Debond',pad(num2str(i),padlength,'left','0')],'none','none','none','none','none','none',{'1.0'},'Out-of-plane thickness of the surface');
      if ~frictionLess
          writeABQfriction(abqpath,'none','none','none','0.005','none','none','none','none','none','none','none','none','none',{num2str(interfaceFriction, '%10.5e')},'friction coefficient');
      end
      if strcomp(elOrder,'first') || strcomp(elOrder,'First') || strcomp(elOrder,'1st') || strcomp(elOrder,'1')
        writeToLogFile(logfullfile,['   Order of elements : First order quadrilaterals','\n'])
        writeABQnodegen(abqpath,Nnodes+2*(i-1)+1,1,[0 -(1.5*RVEl+100*(numFiber-1)+i);0 (1.5*RVEl+100*(numFiber-1)+i)],['NODES-DUMMY-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
        writeABQnodeset(abqpath,1,[Nnodes+2*(i-1)+1],['NODE-DUMMY-FORCE1-NEG-DELTATHETA-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
        writeABQnodeset(abqpath,1,[Nnodes+2*(i-1)+2],['NODE-DUMMY-FORCE1-POS-DELTATHETA-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
        writeABQequation(abqpath,'none',{'3';['NODES-VCCT-FORCE1-NEG-DELTATHETA-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0'),',1,1,',...
                                              'NODES-VCCT-FORCE1-NEG-DELTATHETA-MATRIXSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0'),',1,-1,',...
                                              'NODE-DUMMY-FORCE1-NEG-DELTATHETA-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0'),',1,-1,']},'none');
        writeABQequation(abqpath,'none',{'3';['NODES-VCCT-FORCE1-NEG-DELTATHETA-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0'),',2,1,',...
                                              'NODES-VCCT-FORCE1-NEG-DELTATHETA-MATRIXSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0'),',2,-1,',...
                                              'NODE-DUMMY-FORCE1-NEG-DELTATHETA-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0'),',2,-1,']},'none');
        writeABQequation(abqpath,'none',{'3';['NODES-VCCT-FORCE1-POS-DELTATHETA-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0'),',1,1,',...
                                              'NODES-VCCT-FORCE1-POS-DELTATHETA-MATRIXSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0'),',1,-1,',...
                                              'NODE-DUMMY-FORCE1-POS-DELTATHETA-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0'),',1,-1,']},'none');
        writeABQequation(abqpath,'none',{'3';['NODES-VCCT-FORCE1-POS-DELTATHETA-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0'),',2,1,',...
                                              'NODES-VCCT-FORCE1-POS-DELTATHETA-MATRIXSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0'),',2,-1,',...
                                              'NODE-DUMMY-FORCE1-POS-DELTATHETA-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0'),',2,-1,']},'none');
        writeABQboundary(abqpath,'none','none','none','none','none','none','none','none','none','none','none','none',...
                                 {['NODES-DUMMY-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0'),',ENCASTRE']},'none');
      elseif strcomp(elOrder,'second') || strcomp(elOrder,'Second') || strcomp(elOrder,'2nd') || strcomp(elOrder,'2')
        writeToLogFile(logfullfile,['    Order of elements : Second order quadrilaterals','\n'])
        writeABQnodegen(abqpath,Nnodes+4*(i-1)+1,1,[0 -(1.5*RVEl+100*(numFiber-1)+i);0 (1.5*RVEl+100*(numFiber-1)+i);-(1.5*RVEl+100*(numFiber-1)+i) 0;(1.5*RVEl+100*(numFiber-1)+i) 0],['NODES-DUMMY-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
        writeABQnodeset(abqpath,1,[Nnodes+2*(i-1)+1],['NODE-DUMMY-FORCE1-NEG-DELTATHETA-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
        writeABQnodeset(abqpath,1,[Nnodes+2*(i-1)+2],['NODE-DUMMY-FORCE2-NEG-DELTATHETA-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
        writeABQnodeset(abqpath,1,[Nnodes+2*(i-1)+1],['NODE-DUMMY-FORCE1-POS-DELTATHETA-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
        writeABQnodeset(abqpath,1,[Nnodes+2*(i-1)+2],['NODE-DUMMY-FORCE2-POS-DELTATHETA-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
        writeABQequation(abqpath,'none',{'3';['NODES-VCCT-FORCE1-NEG-DELTATHETA-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0'),',1,1,',...
                                              'NODES-VCCT-FORCE1-NEG-DELTATHETA-MATRIXSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0'),',1,-1,',...
                                              'NODE-DUMMY-FORCE1-NEG-DELTATHETA-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0'),',1,-1,']},'none');
        writeABQequation(abqpath,'none',{'3';['NODES-VCCT-FORCE1-NEG-DELTATHETA-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0'),',2,1,',...
                                            'NODES-VCCT-FORCE1-NEG-DELTATHETA-MATRIXSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0'),',2,-1,',...
                                            'NODE-DUMMY-FORCE1-NEG-DELTATHETA-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0'),',2,-1,']},'none');
        writeABQequation(abqpath,'none',{'3';['NODES-VCCT-FORCE2-NEG-DELTATHETA-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0'),',1,1,',...
                                              'NODES-VCCT-FORCE2-NEG-DELTATHETA-MATRIXSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0'),',1,-1,',...
                                              'NODE-DUMMY-FORCE2-NEG-DELTATHETA-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0'),',1,-1,']},'none');
        writeABQequation(abqpath,'none',{'3';['NODES-VCCT-FORCE2-NEG-DELTATHETA-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0'),',2,1,',...
                                            'NODES-VCCT-FORCE2-NEG-DELTATHETA-MATRIXSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0'),',2,-1,',...
                                            'NODE-DUMMY-FORCE2-NEG-DELTATHETA-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0'),',2,-1,']},'none');
        writeABQequation(abqpath,'none',{'3';['NODES-VCCT-FORCE1-POS-DELTATHETA-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0'),',1,1,',...
                                              'NODES-VCCT-FORCE1-POS-DELTATHETA-MATRIXSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0'),',1,-1,',...
                                              'NODE-DUMMY-FORCE1-POS-DELTATHETA-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0'),',1,-1,']},'none');
        writeABQequation(abqpath,'none',{'3';['NODES-VCCT-FORCE1-POS-DELTATHETA-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0'),',2,1,',...
                                            'NODES-VCCT-FORCE1-POS-DELTATHETA-MATRIXSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0'),',2,-1,',...
                                            'NODE-DUMMY-FORCE1-POS-DELTATHETA-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0'),',2,-1,']},'none');
        writeABQequation(abqpath,'none',{'3';['NODES-VCCT-FORCE2-POS-DELTATHETA-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0'),',1,1,',...
                                              'NODES-VCCT-FORCE2-POS-DELTATHETA-MATRIXSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0'),',1,-1,',...
                                              'NODE-DUMMY-FORCE2-POS-DELTATHETA-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0'),',1,-1,']},'none');
        writeABQequation(abqpath,'none',{'3';['NODES-VCCT-FORCE2-POS-DELTATHETA-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0'),',2,1,',...
                                            'NODES-VCCT-FORCE2-POS-DELTATHETA-MATRIXSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0'),',2,-1,',...
                                            'NODE-DUMMY-FORCE2-POS-DELTATHETA-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0'),',2,-1,']},'none');
        writeABQboundary(abqpath,'none','none','none','none','none','none','none','none','none','none','none','none',...
                                 {['NODES-DUMMY-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0'),',ENCASTRE']},'none');
      end
    end
else

end

elapsed = toc(start);
writeToLogFile(logfullfile,'Timer stopped.\n')
writeToLogFile(logfullfile,['\nELAPSED WALLCLOCK TIME: ', num2str(elapsed),' [s]\n\n'])
writeToLogFile(logfullfile,'Exiting function: writeABQpartiallybondedinterface\n')

return
