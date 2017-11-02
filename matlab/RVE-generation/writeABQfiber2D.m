function[projectName]=writeABQfiber2D(logfullfile,inpfullfile,...
                                      numFiber,padlength,elType,elOrder,ABQel,...
                                      xC,yC,Rcore,R,Rannulus,...
                                      startNode,startEl,...
                                      fiberMaterial,matrixMaterial,debonds,...
                                      interfaceFormulation)
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
%  A function to generate FEM models of RVEs with ABAQUS, here a 2D fiber is constructed
%
%  Input: debond - [d x 3] vector - [theta, deltatheta, Jintegral]
%         interfaceFormulation - scalar - flag for interface formulation
%
%%

writeToLogFile(logfullfile,'In function: writeABQfiber2D\n')
writeToLogFile(logfullfile,'\nStarting timer\n')
start = tic;

writeToLogFile(logfullfile,['    Creating FIBER N. ',num2str(numFiber),'\n'])

writeABQcomment(inpfullfile,'==========================================================================================');
writeABQcomment(inpfullfile,'==========================================================================================');
writeABQcomment(inpfullfile,['                                   FIBER N. ',pad(num2str(numFiber),padlength,'left','0')]);
writeABQcomment(inpfullfile,'==========================================================================================');
writeABQcomment(inpfullfile,'==========================================================================================');

writeToLogFile(logfullfile,'    Creating core ...\n')

N0core = startNode + 1;
E0core = startEl + 1;

[nodes,elements,edges,...
    nodesSWcorner,nodesSEcorner,nodesNEcorner,nodesNWcorner,...
    nodesSOUTHside,nodesEASTside,nodesNORTHside,nodesWESTside,...
    edgesSOUTHside,edgesEASTside,edgesNORTHside,edgesWESTside,...
    elementsSWcorner,elementsSEcorner,elementsNEcorner,elementsNWcorner,...
    elementsSOUTHside,elementsEASTside,elementsNORTHside,elementsWESTside]=meshGenGradedCircSec(logfullfile,elType,elOrder,x0,y0,R,thetas,deltas);

writeABQnodegen(inpfullfile,N0core,1,nodes,['NODES-CORE-FIBER',pad(num2str(numFiber),padlength,'left','0')]);

interfaceNodes = startNode + [nodesSWcorner;nodesSOUTHside;nodesSEcorner;nodesEASTside;nodesNEcorner;nodesNORTHside;nodesNWcorner;nodesWESTside];
writeABQnodeset(inpfullfile,1,interfaceNodes,['NODES-CORE-INTERFACE-FIBER',pad(num2str(numFiber),padlength,'left','0')]);

writeABQelgen(inpfullfile,E0core,1,startNode.+elements,ABQel,['ELEMENTS-CORE-FIBER',pad(num2str(numFiber),padlength,'left','0')]);

interfaceElements = startEl + [elementsSWcorner;elementsSOUTHside;elementsSEcorner;elementsEASTside;elementsNEcorner;elementsNORTHside;elementsNWcorner;elementsWESTside];
writeABQelementset(inpfullfile,1,interfaceElements,['ELEMENTS-CORE-INTERFACE-FIBER',pad(num2str(numFiber),padlength,'left','0')])

writeToLogFile(logfullfile,'    ... done.\n')

writeToLogFile(logfullfile,'    Creating annular part of the fiber ...\n')

N0annular = N0core + length(nodes);
E0annular = E0core + length(elements);

[nodes,elements,edges,...
    nodesSWcorner,nodesSEcorner,nodesNEcorner,nodesNWcorner,...
    nodesSOUTHside,nodesEASTside,nodesNORTHside,nodesWESTside,...
    edgesSOUTHside,edgesEASTside,edgesNORTHside,edgesWESTside,...
    elementsSWcorner,elementsSEcorner,elementsNEcorner,elementsNWcorner,...
    elementsSOUTHside,elementsEASTside,elementsNORTHside,elementsWESTside]=meshGenGradedAnnularSec(logfullfile,elType,elOrder,isClosed,x0,y0,Rin,theta0,ltheta,lR,deltas,NR)

writeABQnodegen(inpfullfile,N0annular,1,nodes,['NODES-ANNULUS-FIBER',pad(num2str(numFiber),padlength,'left','0')]);

intInterfaceNodes = N0core + nodesSOUTHside;
writeABQnodeset(inpfullfile,1,intInterfaceNodes,['NODES-ANNULUS-INTINTERFACE-FIBER',pad(num2str(numFiber),padlength,'left','0')]);

extInterfaceNodes = N0core + nodesNORTHside;
writeABQnodeset(inpfullfile,1,extInterfaceNodes,['NODES-ANNULUS-EXTINTERFACE-FIBER',pad(num2str(numFiber),padlength,'left','0')]);

writeABQelgen(inpfullfile,E0annular,1,N0core.+elements,ABQel,['ELEMENTS-ANNULUS-FIBER',pad(num2str(numFiber),padlength,'left','0')]);

intInterfaceElements = E0core + elementsSOUTHside;
writeABQelementset(inpfullfile,1,intInterfaceElements,['ELEMENTS-ANNULUS-INTINTERFACE-FIBER',pad(num2str(numFiber),padlength,'left','0')])

extInterfaceElements = E0core + elementsNORTHside;
writeABQelementset(inpfullfile,1,extInterfaceElements,['ELEMENTS-ANNULUS-EXTINTERFACE-FIBER',pad(num2str(numFiber),padlength,'left','0')])

for d=1:length(debonds)
  thetalo = debonds(d,1)-debonds(d,2);
  thetaup = debonds(d,1)+debonds(d,2);
  costhetalo = cos(thetalo);
  sinthetalo = sin(thetalo);
  costhetaup = cos(thetaup);
  sinthetaup = sin(thetaup);
  deltaEl = 2*pi/length(extInterfaceElements);
  nEls = size(elements,2);
  for e=1:length(extInterfaceElements)
    inDebond = []
    for n=1:nEls
      x = nodes(elements(extInterfaceElements(e),n),1);
      y = nodes(elements(extInterfaceElements(e),n),2);
      if ~isempty(find(N0core.+elements(extInterfaceElements(e),n)==intInterfaceNodes))

      end
    end
  end
end

writeToLogFile(logfullfile,'    ... done.\n')

writeToLogFile(logfullfile,'    Creating annular sorrounding matrix ...\n')
N0extannular = N0annular + length(nodes);
[nodes,elements,edges,...
    nodesSWcorner,nodesSEcorner,nodesNEcorner,nodesNWcorner,...
    nodesSOUTHside,nodesEASTside,nodesNORTHside,nodesWESTside,...
    edgesSOUTHside,edgesEASTside,edgesNORTHside,edgesWESTside,...
    elementsSWcorner,elementsSEcorner,elementsNEcorner,elementsNWcorner,...
    elementsSOUTHside,elementsEASTside,elementsNORTHside,elementsWESTside]=meshGenGradedAnnularSec(logfullfile,elType,elOrder,isClosed,x0,y0,Rin,theta0,ltheta,lR,deltas,NR)


writeABQnodegen(inpfullfile,N0extannular,1,nodes,['NODES-EXTANNULUS-FIBER',pad(num2str(numFiber),padlength,'left','0')]);

writeToLogFile(logfullfile,'    ... done.\n')

elapsed = toc(start);
writeToLogFile(logfullfile,'Timer stopped.\n')
writeToLogFile(logfullfile,['\nELAPSED WALLCLOCK TIME: ', num2str(elapsed),' [s]\n\n'])
writeToLogFile(logfullfile,'Exiting function: writeABQfiber2D\n')


return
