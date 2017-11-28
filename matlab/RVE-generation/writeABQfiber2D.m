function[Ntot,Etot]=writeABQfiber2D(logfullfile,inpfullfile,...
                                      numFiber,padlength,elType,elOrder,ABQel,...
                                      xC,yC,Rcore,R,...
                                      startNode,startEl,...
                                      fiberMaterial,matrixMaterial,debonds,...
                                      thetasCore,deltasCore,lthetaIntAnnulus,lRIntAnnulus,deltasIntAnnulus,NRIntAnnulus,lthetaExtAnnulus,lRExtAnnulus,deltasExtAnnulus,NRExtAnnulus)
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

writeToLogFile(logfullfile,['    Calling function ', 'meshGenGradedCircSec',' ...\n']);

[nodes,elements,edges,...
    nodesSWcorner,nodesSEcorner,nodesNEcorner,nodesNWcorner,...
    nodesSOUTHside,nodesEASTside,nodesNORTHside,nodesWESTside,...
    edgesSOUTHside,edgesEASTside,edgesNORTHside,edgesWESTside,...
    elementsSWcorner,elementsSEcorner,elementsNEcorner,elementsNWcorner,...
    elementsSOUTHside,elementsEASTside,elementsNORTHside,elementsWESTside]=meshGenGradedCircSec(logfullfile,elType,elOrder,xC,yC,Rcore,thetasCore,deltasCore);

writeToLogFile(logfullfile,['    ... done.','\n'])

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

writeToLogFile(logfullfile,['    Calling function ', 'meshGenGradedAnnularSec',' ...\n']);

[nodes,elements,edges,...
    nodesSWcorner,nodesSEcorner,nodesNEcorner,nodesNWcorner,...
    nodesSOUTHside,nodesEASTside,nodesNORTHside,nodesWESTside,...
    edgesSOUTHside,edgesEASTside,edgesNORTHside,edgesWESTside,...
    elementsSWcorner,elementsSEcorner,elementsNEcorner,elementsNWcorner,...
    elementsSOUTHside,elementsEASTside,elementsNORTHside,elementsWESTside]=meshGenGradedAnnularSec(logfullfile,elType,elOrder,1,xC,yC,Rcore,0.0,lthetaIntAnnulus,lRIntAnnulus,deltasIntAnnulus,NRIntAnnulus)

writeToLogFile(logfullfile,['    ... done.','\n'])

writeABQnodegen(inpfullfile,N0annular,1,nodes,['NODES-ANNULUS-FIBER',pad(num2str(numFiber),padlength,'left','0')]);

writeABQnodeset(inpfullfile,2,{['NODES-CORE-FIBER',pad(num2str(numFiber),padlength,'left','0')],['NODES-ANNULUS-FIBER',pad(num2str(numFiber),padlength,'left','0')]},['NODES-FIBER',pad(num2str(numFiber),padlength,'left','0')]);

intInterfaceNodes = N0core + nodesSOUTHside;
writeABQnodeset(inpfullfile,1,intInterfaceNodes,['NODES-ANNULUS-INTINTERFACE-FIBER',pad(num2str(numFiber),padlength,'left','0')]);

extInterfaceNodes = N0core + nodesNORTHside;
writeABQnodeset(inpfullfile,1,extInterfaceNodes,['NODES-ANNULUS-EXTINTERFACE-FIBER',pad(num2str(numFiber),padlength,'left','0')]);

writeABQelgen(inpfullfile,E0annular,1,N0core.+elements,ABQel,['ELEMENTS-ANNULUS-FIBER',pad(num2str(numFiber),padlength,'left','0')]);

writeABQelementset(inpfullfile,2,{['ELEMENTS-CORE-FIBER',pad(num2str(numFiber),padlength,'left','0')],['ELEMENTS-ANNULUS-FIBER',pad(num2str(numFiber),padlength,'left','0')]},['ELEMENTS-FIBER',pad(num2str(numFiber),padlength,'left','0')]);

intInterfaceElements = E0core + elementsSOUTHside;
writeABQelementset(inpfullfile,1,intInterfaceElements,['ELEMENTS-ANNULUS-INTINTERFACE-FIBER',pad(num2str(numFiber),padlength,'left','0')]);

extInterfaceElements = E0core + elementsNORTHside;
writeABQelementset(inpfullfile,1,extInterfaceElements,['ELEMENTS-ANNULUS-EXTINTERFACE-FIBER',pad(num2str(numFiber),padlength,'left','0')]);


% ========> creating debonds on the fiber surface
if strcomp(elType,'quads') || strcomp(elType,'quad') || strcomp(elType,'quadrilaterals') || strcomp(elType,'quadrilateral')
  Nnodes = 4;
  if strcomp(elOrder,'first') || strcomp(elOrder,'First') || strcomp(elOrder,'1st') || strcomp(elOrder,'1')
    writeToLogFile(logfullfile,['    Type ad order of elements : First order quadrilaterals','\n'])
    multNodes = 1;
  elseif strcomp(elOrder,'second') || strcomp(elOrder,'Second') || strcomp(elOrder,'2nd') || strcomp(elOrder,'2')
    writeToLogFile(logfullfile,['    Type ad order of elements : Second order quadrilaterals','\n'])
    multNodes = 2;
  end
elseif strcomp(elType,'tris') || strcomp(elType,'tri') || strcomp(elType,'triangles') || strcomp(elType,'triangle')
  Nnodes = 3;
  if strcomp(elOrder,'first') || strcomp(elOrder,'First') || strcomp(elOrder,'1st') || strcomp(elOrder,'1')
    writeToLogFile(logfullfile,['    Type ad order of elements : First order triangles','\n'])
    multNodes = 1;
  elseif strcomp(elOrder,'second') || strcomp(elOrder,'Second') || strcomp(elOrder,'2nd') || strcomp(elOrder,'2')
    writeToLogFile(logfullfile,['    Type ad order of elements : Second order triangles','\n'])
    multNodes = 2;
  end
end

extLabelMax = max(extInterfaceElements);
extLabelMin = min(extInterfaceElements);

angleTol = 0.00001; % 0.001%

writeToLogFile(logfullfile,'    Creating debonded region on fiber surface ...\n')

if length(debonds)>0                                      % at least one debond
  if length(debonds)==1 && abs(pi-debonds(1,2))<=angleTol % completely detached interface
    writeToLogFile(logfullfile,'    Attention! The interface is completely detached.\n')
    writeABQnodeset(inpfullfile,1,extInterfaceNodes,['NODES-DEBOND-WITHOUT-CT-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0')]);
    writeABQelementset(inpfullfile,1,extInterfaceElements,['ELEMENTS-DEBOND-WITHOUT-CT-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0')]);
  else                                                    % at least one partial debond
    debondedNodes = [];
    debondedEls = [];
    firstBondedEls = [];
    allVcctForceNodes = [];
    for d=1:length(debonds)
      currentDebondNodes = [];
      currentDebondElementsWithoutCrackTips = [];
      currentDebondElementsFirstInside = zeros(1,2);            % [at -deltatheta, at +deltatheta]
      currentDebondElementsFirstOutside = zeros(1,2);           % [at -deltatheta, at +deltatheta]
      crackTips = zeros(1,2);                                   % [at -deltatheta, at +deltatheta]
      vcctForceNodes = [zeros(1,multNodes) zeros(1,multNodes)]; % [[at -deltatheta], [at +deltatheta]]
      vcctDispNodes = [zeros(1,multNodes) zeros(1,multNodes)];  % [[at -deltatheta], [at +deltatheta]]
      theta = debonds(d,1);
      deltatheta = debonds(d,2);
      if theta>=-pi && theta<0                              % recast theta in the domain [0,2*pi] if it's in [-pi,0]
        theta = 2*pi + theta;
      end
      if deltatheta<=0 || deltatheta>pi                     % deltatheta is outside its domain of definition, skip this debond
        writeToLogFile(logfullfile,'    Error!! Deltatheta is outside its domain of definition, skipping this debond.\n')
        continue
      end
      if length(debonds)>1                                  % if there's more than one debond, check for overlaps
        toSkip = 0;
        for c=1:d-1
          theta2 = debonds(c,1);
          deltatheta2 = debonds(c,2);
          if theta2>=-pi && theta2<0                              % recast theta2 in the domain [0,2*pi] if it's in [-pi,0]
            theta2 = 2*pi + theta2;
          end
          if deltatheta2<=0 || deltatheta2>pi                     % deltatheta2 is outside its domain of definition, skip this debond
            writeToLogFile(logfullfile,'    Error!! Deltatheta is outside its domain of definition, skipping this debond.\n')
            continue
          end
          if theta2==theta
            writeToLogFile(logfullfile,'    Error!! Debond ',num2str(d),' is centered on the same angle as debond ',num2str(c),', skipping this debond.\n')
            toSkip = 1;
            break
          elseif theta2>theta
            delta1 = theta2 - theta;
            delta2 = theta + (2*pi - theta2)
            if deltatheta+deltatheta2>=delta1 || deltatheta+deltatheta2>=delta2
              writeToLogFile(logfullfile,'    Error!! Debond ',num2str(d),' is overlapping debond ',num2str(c),', skipping this debond.\n')
              toSkip = 1;
              break
            end
          else
            delta1 = theta - theta2;
            delta2 = theta2 + (2*pi - theta)
            if deltatheta+deltatheta2>=delta1 || deltatheta+deltatheta2>=delta2
              writeToLogFile(logfullfile,'    Error!! Debond ',num2str(d),' is overlapping debond ',num2str(c),', skipping this debond.\n')
              toSkip = 1;
              break
            end
          end
        end
        for c=d+1:length(debonds)
          theta2 = debonds(c,1);
          deltatheta2 = debonds(c,2);
          if theta2>=-pi && theta2<0                              % recast theta2 in the domain [0,2*pi] if it's in [-pi,0]
            theta2 = 2*pi + theta2;
          end
          if deltatheta2<=0 || deltatheta2>pi                     % deltatheta2 is outside its domain of definition, skip this debond
            writeToLogFile(logfullfile,'    Error!! Deltatheta is outside its domain of definition, skipping this debond.\n')
            continue
          end
          if theta2==theta
            writeToLogFile(logfullfile,'    Error!! Debond ',num2str(d),' is centered on the same angle as debond ',num2str(c),', skipping this debond.\n')
            toSkip = 1;
            break
          elseif theta2>theta
            delta1 = theta2 - theta;
            delta2 = theta + (2*pi - theta2)
            if deltatheta+deltatheta2>=delta1 || deltatheta+deltatheta2>=delta2
              writeToLogFile(logfullfile,'    Error!! Debond ',num2str(d),' is overlapping debond ',num2str(c),', skipping this debond.\n')
              toSkip = 1;
              break
            end
          else
            delta1 = theta - theta2;
            delta2 = theta2 + (2*pi - theta)
            if deltatheta+deltatheta2>=delta1 || deltatheta+deltatheta2>=delta2
              writeToLogFile(logfullfile,'    Error!! Debond ',num2str(d),' is overlapping debond ',num2str(c),', skipping this debond.\n')
              toSkip = 1;
              break
            end
          end
        end
        if toSkip
          continue
        end
      end
      %thetalo = theta-deltatheta;
      %thetaup = theta+deltatheta;
      %costhetalo = cos(thetalo);
      %sinthetalo = sin(thetalo);
      %costhetaup = cos(thetaup);
      %sinthetaup = sin(thetaup);
      %deltaEl = min(thetas./deltas);
      for e=1:length(extInterfaceElements)                         % sweep through the elements at the external interface
        if isempty(find(extInterfaceElements(e)==debondedEls))     % check the interface element e if it's not inside another debond
          onSurface = []
          for n=1:Nnodes
            if ~isempty(find(N0core.+elements(extInterfaceElements(e)-E0core,n)==intInterfaceNodes))
              onSurface = [onSurface; elements(extInterfaceElements(e),n)];
            end
          end
          x1 = nodes(onSurface(1),1);
          y1 = nodes(onSurface(1),2);
          x2 = nodes(onSurface(2),1);
          y2 = nodes(onSurface(2),2);
          alpha1 = atan2(y1,x1);
          alpha2 = atan2(y2,x2);
          beta1 = alpha1 - theta;
          beta2 = alpha2 - theta;
          beta1abs = abs(beta1);
          beta2abs = abs(beta2);
          deltathetaabs = abs(deltatheta);
          %if beta1abs>deltathetaabs && beta2abs>deltathetaabs       % completely outside the debond
          if beta1abs<deltathetaabs && beta2abs<deltathetaabs   % completely inside the debond
            if isempty(find(N0core.+onSurface(1)==currentDebondNodes)
              currentDebondNodes = [currentDebondNodes;N0core.+onSurface(1)];
            end
            if isempty(find(N0core.+onSurface(2)==currentDebondNodes)
              currentDebondNodes = [currentDebondNodes;N0core.+onSurface(2)];
            end
            if multNodes>1
              for n=Nnodes+1:multNodes*Nnodes
                if ~isempty(find(N0core.+elements(extInterfaceElements(e)-E0core,n)==intInterfaceNodes))
                  onSurface = [onSurface; elements(extInterfaceElements(e),n)];
                  break
                end
              end
              if isempty(find(N0core.+onSurface(3)==currentDebondNodes)
                currentDebondNodes = [currentDebondNodes;N0core.+onSurface(3)];
              end
            end
            currentDebondElementsWithoutCrackTips = [currentDebondElementsWithoutCrackTips;extInterfaceElements(e)];
          elseif (beta1abs>deltathetaabs && beta2abs<deltathetaabs) || (beta1abs<deltathetaabs && beta2abs>deltathetaabs)  % one node outside and one node inside, the element is across the crack tip
            % the current element is the first inside the debond
            % the first element outside must be searched among a restricted pool of candidates
            if beta1abs>deltathetaabs  % node 1 is outside and 2 inside => node 1 is the crack tip
              if beta2<0               % the element is at -deltatheta
                if isempty(find(extInterfaceElements(e)-1==extInterfaceElements)
                  currentDebondElementsFirstOutside(1) = extLabelMax;
                else
                  currentDebondElementsFirstOutside(1) = extInterfaceElements(e)-1;
                end
                crackTips(1) = N0core.+onSurface(1);
                currentDebondElementsFirstInside(1) = extInterfaceElements(e);
                vcctForceNodes(1,1) = N0core.+onSurface(1);
                vcctDispNodes(1,1) = N0core.+onSurface(2);
                if multNodes>1
                  for n=Nnodes+1:multNodes*Nnodes
                    if ~isempty(find(N0core.+elements(extInterfaceElements(e)-E0core,n)==intInterfaceNodes))
                      onSurface = [onSurface; elements(extInterfaceElements(e),n)];
                      break
                    end
                  end
                  for n=Nnodes+1:multNodes*Nnodes
                    if ~isempty(find(N0core.+elements(currentDebondElementsFirstOutside(1)-E0core,n)==intInterfaceNodes))
                      vcctForceNodes(1,2) = N0core.+elements(extInterfaceElements(e),n);
                      break
                    end
                  end
                  vcctDispNodes(1,2) = N0core.+onSurface(3);
                end
              else                     % the element is at +deltatheta
                if isempty(find(extInterfaceElements(e)-1==extInterfaceElements)
                  currentDebondElementsFirstOutside(2) = extLabelMin;
                else
                  currentDebondElementsFirstOutside(2) = extInterfaceElements(e)-1;
                end
                crackTips(2) = N0core.+onSurface(1);
                currentDebondElementsFirstInside(2) = extInterfaceElements(e);
                vcctForceNodes(2,1) = N0core.+onSurface(1);
                vcctDispNodes(2,1) = N0core.+onSurface(2);
                if multNodes>1
                  for n=Nnodes+1:multNodes*Nnodes
                    if ~isempty(find(N0core.+elements(extInterfaceElements(e)-E0core,n)==intInterfaceNodes))
                      onSurface = [onSurface; elements(extInterfaceElements(e),n)];
                      break
                    end
                  end
                  for n=Nnodes+1:multNodes*Nnodes
                    if ~isempty(find(N0core.+elements(currentDebondElementsFirstOutside(2)-E0core,n)==intInterfaceNodes))
                      vcctForceNodes(2,2) = N0core.+elements(extInterfaceElements(e),n);
                      break
                    end
                  end
                  vcctDispNodes(2,2) = N0core.+onSurface(3);
                end
              end
            else                       % node 1 is inside and 2 outside => node 2 is the crack tip
              if beta1<0               % the element is at -deltatheta
                if isempty(find(extInterfaceElements(e)-1==extInterfaceElements)
                  currentDebondElementsFirstOutside(1) = extLabelMax;
                else
                  currentDebondElementsFirstOutside(1) = extInterfaceElements(e)-1;
                end
                crackTips(1) = N0core.+onSurface(2);
                currentDebondElementsFirstInside(1) = extInterfaceElements(e);
                vcctForceNodes(1,1) = N0core.+onSurface(2);
                vcctDispNodes(1,1) = N0core.+onSurface(1);
                if multNodes>1
                  for n=Nnodes+1:multNodes*Nnodes
                    if ~isempty(find(N0core.+elements(extInterfaceElements(e)-E0core,n)==intInterfaceNodes))
                      onSurface = [onSurface; elements(extInterfaceElements(e),n)];
                      break
                    end
                  end
                  for n=Nnodes+1:multNodes*Nnodes
                    if ~isempty(find(N0core.+elements(currentDebondElementsFirstOutside(1)-E0core,n)==intInterfaceNodes))
                      vcctForceNodes(1,2) = N0core.+elements(extInterfaceElements(e),n);
                      break
                    end
                  end
                  vcctDispNodes(1,2) = N0core.+onSurface(3);
                end
              else                     % the element is at +deltatheta
                if isempty(find(extInterfaceElements(e)-1==extInterfaceElements)
                  currentDebondElementsFirstOutside(2) = extLabelMin;
                else
                  currentDebondElementsFirstOutside(2) = extInterfaceElements(e)-1;
                end
                crackTips(2) = N0core.+onSurface(2);
                currentDebondElementsFirstInside(2) = extInterfaceElements(e);
                vcctForceNodes(2,1) = N0core.+onSurface(2);
                vcctDispNodes(2,1) = N0core.+onSurface(1);
                if multNodes>1
                  for n=Nnodes+1:multNodes*Nnodes
                    if ~isempty(find(N0core.+elements(extInterfaceElements(e)-E0core,n)==intInterfaceNodes))
                      onSurface = [onSurface; elements(extInterfaceElements(e),n)];
                      break
                    end
                  end
                  for n=Nnodes+1:multNodes*Nnodes
                    if ~isempty(find(N0core.+elements(currentDebondElementsFirstOutside(2)-E0core,n)==intInterfaceNodes))
                      vcctForceNodes(2,2) = N0core.+elements(extInterfaceElements(e),n);
                      break
                    end
                  end
                  vcctDispNodes(2,2) = N0core.+onSurface(3);
                end
              end
            end
          elseif (beta1abs>deltathetaabs && beta2abs==deltathetaabs) || (beta1abs==deltathetaabs && beta2abs>deltathetaabs)  % one node outside and one node at the crack tip, the element is the first outside the debond
            if beta1abs==deltathetaabs                  % Node 1 is at the crack tip
              if beta1<0                                % Crack tip at -deltatheta
                currentDebondElementsFirstOutside(1) = extInterfaceElements(e);
                if multNodes>1
                  for n=Nnodes+1:multNodes*Nnodes
                    if ~isempty(find(N0core.+elements(extInterfaceElements(e)-E0core,n)==intInterfaceNodes))
                      onSurface = [onSurface; elements(extInterfaceElements(e),n)];
                      break
                    end
                  end
                  vcctForceNodes(1,2) = N0core.+onSurface(3);
                end
              else                                      % Crack tip at +deltatheta
                currentDebondElementsFirstOutside(2) = extInterfaceElements(e);
                if multNodes>1
                  for n=Nnodes+1:multNodes*Nnodes
                    if ~isempty(find(N0core.+elements(extInterfaceElements(e)-E0core,n)==intInterfaceNodes))
                      onSurface = [onSurface; elements(extInterfaceElements(e),n)];
                      break
                    end
                  end
                  vcctForceNodes(2,2) = N0core.+onSurface(3);
                end
              end
            else                                        % Node 2 is at the crack tip
              if beta2<0                                % Crack tip at -deltatheta
                currentDebondElementsFirstOutside(1) = extInterfaceElements(e);
                if multNodes>1
                  for n=Nnodes+1:multNodes*Nnodes
                    if ~isempty(find(N0core.+elements(extInterfaceElements(e)-E0core,n)==intInterfaceNodes))
                      onSurface = [onSurface; elements(extInterfaceElements(e),n)];
                      break
                    end
                  end
                  vcctForceNodes(1,2) = N0core.+onSurface(3);
                end
              else                                      % Crack tip at +deltatheta
                currentDebondElementsFirstOutside(2) = extInterfaceElements(e);
                if multNodes>1
                  for n=Nnodes+1:multNodes*Nnodes
                    if ~isempty(find(N0core.+elements(extInterfaceElements(e)-E0core,n)==intInterfaceNodes))
                      onSurface = [onSurface; elements(extInterfaceElements(e),n)];
                      break
                    end
                  end
                  vcctForceNodes(2,2) = N0core.+onSurface(3);
                end
              end
            end
          elseif (beta1abs<deltathetaabs && beta2abs==deltathetaabs) || (beta1abs==deltathetaabs && beta2abs<deltathetaabs)  % one node inside and one node at the crack tip, the element is the first inside the debond
            if beta1abs==deltathetaabs                  % Node 1 is at the crack tip
              if beta1<0                                % Crack tip at -deltatheta
                crackTips(1) = N0core.+onSurface(1);
                currentDebondElementsFirstInside(1) = extInterfaceElements(e);
                vcctForceNodes(1,1) = N0core.+onSurface(1);
                vcctDispNodes(1,1) = N0core.+onSurface(2);
                if multNodes>1
                  for n=Nnodes+1:multNodes*Nnodes
                    if ~isempty(find(N0core.+elements(extInterfaceElements(e)-E0core,n)==intInterfaceNodes))
                      onSurface = [onSurface; elements(extInterfaceElements(e),n)];
                      break
                    end
                  end
                  vcctDispNodes(1,2) = N0core.+onSurface(3);
                end
              else                                      % Crack tip at +deltatheta
                crackTips(2) = N0core.+onSurface(1);
                currentDebondElementsFirstInside(2) = extInterfaceElements(e);
                vcctForceNodes(2,1) = N0core.+onSurface(1);
                vcctDispNodes(2,1) = N0core.+onSurface(2);
                if multNodes>1
                  for n=Nnodes+1:multNodes*Nnodes
                    if ~isempty(find(N0core.+elements(extInterfaceElements(e)-E0core,n)==intInterfaceNodes))
                      onSurface = [onSurface; elements(extInterfaceElements(e),n)];
                      break
                    end
                  end
                  vcctDispNodes(2,2) = N0core.+onSurface(3);
                end
              end
            else                                        % Node 2 is at the crack tip
              if beta2<0                                % Crack tip at -deltatheta
                crackTips(1) = N0core.+onSurface(2);
                currentDebondElementsFirstInside(1) = extInterfaceElements(e);
                vcctForceNodes(1,1) = N0core.+onSurface(2);
                vcctDispNodes(1,1) = N0core.+onSurface(1);
                if multNodes>1
                  for n=Nnodes+1:multNodes*Nnodes
                    if ~isempty(find(N0core.+elements(extInterfaceElements(e)-E0core,n)==intInterfaceNodes))
                      onSurface = [onSurface; elements(extInterfaceElements(e),n)];
                      break
                    end
                  end
                  vcctDispNodes(1,2) = N0core.+onSurface(3);
                end
              else                                      % Crack tip at +deltatheta
                crackTips(2) = N0core.+onSurface(2);
                currentDebondElementsFirstInside(1) = extInterfaceElements(e);
                vcctForceNodes(2,1) = N0core.+onSurface(2);
                vcctDispNodes(2,1) = N0core.+onSurface(1);
                if multNodes>1
                  for n=Nnodes+1:multNodes*Nnodes
                    if ~isempty(find(N0core.+elements(extInterfaceElements(e)-E0core,n)==intInterfaceNodes))
                      onSurface = [onSurface; elements(extInterfaceElements(e),n)];
                      break
                    end
                  end
                  vcctDispNodes(2,2) = N0core.+onSurface(3);
                end
              end
            end
          end
      end
      % the sweep over the interface elements for the current debond is done
      % add the nodes where vcct displacements will be extracted to the list of current debonded nodes
      if isempty(find(vcctDispNodes(1,1)==currentDebondNodes)
        currentDebondNodes = [currentDebondNodes;vcctDispNodes(1,1)];
      end
      if isempty(find(vcctDispNodes(2,1)==currentDebondNodes)
        currentDebondNodes = [currentDebondNodes;vcctDispNodes(2,1)];
      end
      if multNodes>1
        if isempty(find(vcctDispNodes(1,2)==currentDebondNodes)
          currentDebondNodes = [currentDebondNodes;vcctDispNodes(1,2)];
        end
        if isempty(find(vcctDispNodes(2,2)==currentDebondNodes)
          currentDebondNodes = [currentDebondNodes;vcctDispNodes(2,2)];
        end
      end
      % let's save debonded nodes, vcct forces nodes, debonded elements, first debonded elements and first bonded elements to the global containers
      debondedNodes = [debondedNodes;currentDebondNodes];
      debondedEls = [debondedEls;currentDebondElementsWithoutCrackTips;currentDebondElementsFirstInside(1);currentDebondElementsFirstInside(2)];
      firstBondedEls = [firstBondedEls;currentDebondElementsFirstOutside(1);currentDebondElementsFirstOutside(2)];
      allVcctForceNodes = [allVcctForceNodes;vcctForceNodes(1,1);vcctForceNodes(2,1)];
      if multNodes>1
        allVcctForceNodes = [allVcctForceNodes;vcctForceNodes(1,2);vcctForceNodes(2,2)];
      end
      % and write the debond in the Abaqus input file
      writeABQnodeset(inpfullfile,1,currentDebondNodes,['NODES-DEBOND-WITHOUT-CT-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
      writeABQnodeset(inpfullfile,1,crackTips,['NODES-CRACK-TIPS-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
      writeABQnodeset(inpfullfile,1,crackTips(1),['NODES-CRACK-TIP-NEG-DELTATHETA-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
      writeABQnodeset(inpfullfile,1,crackTips(2),['NODES-CRACK-TIP-POS-DELTATHETA-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
      if multNodes>1
        writeABQnodeset(inpfullfile,1,vcctForceNodes(1,1),['NODES-VCCT-FORCE1-NEG-DELTATHETA-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
        writeABQnodeset(inpfullfile,1,vcctForceNodes(1,2),['NODES-VCCT-FORCE2-NEG-DELTATHETA-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
        writeABQnodeset(inpfullfile,1,vcctDispNodes(1,1),['NODES-VCCT-DISP1-NEG-DELTATHETA-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
        writeABQnodeset(inpfullfile,1,vcctDispNodes(1,2),['NODES-VCCT-DISP2-NEG-DELTATHETA-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
        writeABQnodeset(inpfullfile,1,vcctForceNodes(2,1),['NODES-VCCT-FORCE1-POS-DELTATHETA-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
        writeABQnodeset(inpfullfile,1,vcctForceNodes(2,2),['NODES-VCCT-FORCE2-POS-DELTATHETA-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
        writeABQnodeset(inpfullfile,1,vcctDispNodes(2,1),['NODES-VCCT-DISP1-POS-DELTATHETA-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
        writeABQnodeset(inpfullfile,1,vcctDispNodes(2,2),['NODES-VCCT-DISP2-POS-DELTATHETA-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
      else
        writeABQnodeset(inpfullfile,1,vcctForceNodes(1,1),['NODES-VCCT-FORCE1-NEG-DELTATHETA-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
        writeABQnodeset(inpfullfile,1,vcctDispNodes(1,1),['NODES-VCCT-DISP1-NEG-DELTATHETA-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
        writeABQnodeset(inpfullfile,1,vcctForceNodes(2,1),['NODES-VCCT-FORCE1-POS-DELTATHETA-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
        writeABQnodeset(inpfullfile,1,vcctDispNodes(2,1),['NODES-VCCT-DISP1-POS-DELTATHETA-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
      end
      writeABQelementset(inpfullfile,1,currentDebondElementsWithoutCrackTips,['ELEMENTS-DEBOND-WITHOUT-CT-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
      writeABQelementset(inpfullfile,1,currentDebondElementsFirstInside(1),['ELEMENTS-FIRST-DEBONDED-NEG-DELTATHETA-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
      writeABQelementset(inpfullfile,1,currentDebondElementsFirstInside(2),['ELEMENTS-FIRST-DEBONDED-POS-DELTATHETA-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
      writeABQelementset(inpfullfile,1,currentDebondElementsFirstOutside(1),['ELEMENTS-FIRST-BONDED-NEG-DELTATHETA-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
      writeABQelementset(inpfullfile,1,currentDebondElementsFirstOutside(2),['ELEMENTS-FIRST-BONDED-POS-DELTATHETA-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
      writeABQelementset(inpfullfile,2,{['ELEMENTS-DEBOND-WITHOUT-CT-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')],...
                                        ['ELEMENTS-FIRST-DEBONDED-NEG-DELTATHETA-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')],...
                                        ['ELEMENTS-FIRST-DEBONDED-POS-DELTATHETA-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]},['ELEMENTS-DEBOND-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
    end
  end
  bondedNodes = [];
  for i=1:length(extInterfaceNodes)
    if isempty(extInterfaceNodes(i)==[debondedNodes;allVcctForceNodes])
      bondedNodes = [bondedNodes; extInterfaceNodes(i)];
    end
  end
  bondedElements = [];
  for i=1:length(extInterfaceElements)
    if isempty(extInterfaceElements(i)==[debondedEls;firstBondedEls])
      bondedElements = [bondedElements; extInterfaceElements(i)];
    end
  end
  writeABQnodeset(inpfullfile,1,bondedNodes,['NODES-BONDED-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0')]);
  writeABQelementset(inpfullfile,1,bondedElements,['ELEMENTS-BONDED-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0')]);
else     % no debond
  writeToLogFile(logfullfile,'    Attention! The interface is completely bonded, no debond present.\n')
  writeABQnodeset(inpfullfile,1,extInterfaceNodes,['NODES-BONDED-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0')]);
  writeABQelementset(inpfullfile,1,extInterfaceElements,['ELEMENTS-BONDED-FIBERSURF-FIBER',pad(num2str(numFiber),padlength,'left','0')]);

end


writeToLogFile(logfullfile,'    ... done.\n')

writeToLogFile(logfullfile,'    Creating annular sorrounding matrix ...\n')

N0core = N0annular;
E0core = E0annular;

N0annular = N0annular + length(nodes);
E0annular = E0annular + length(elements);

writeToLogFile(logfullfile,['    Calling function ', 'meshGenGradedAnnularSec',' ...\n']);

[nodes,elements,edges,...
    nodesSWcorner,nodesSEcorner,nodesNEcorner,nodesNWcorner,...
    nodesSOUTHside,nodesEASTside,nodesNORTHside,nodesWESTside,...
    edgesSOUTHside,edgesEASTside,edgesNORTHside,edgesWESTside,...
    elementsSWcorner,elementsSEcorner,elementsNEcorner,elementsNWcorner,...
    elementsSOUTHside,elementsEASTside,elementsNORTHside,elementsWESTside]=meshGenGradedAnnularSec(logfullfile,elType,elOrder,1,xC,yC,R,0.0,lthetaExtAnnulus,lRExtAnnulus,deltasExtAnnulus,NRExtAnnulus)


writeToLogFile(logfullfile,['    ... done.','\n'])

writeABQnodegen(inpfullfile,N0annular,1,nodes,['NODES-ANNULUS-MATRIX',pad(num2str(numFiber),padlength,'left','0')]);

writeABQnodeset(inpfullfile,2,{['NODES-CORE-MATRIX',pad(num2str(numFiber),padlength,'left','0')],['NODES-ANNULUS-MATRIX',pad(num2str(numFiber),padlength,'left','0')]},['NODES-MATRIX',pad(num2str(numFiber),padlength,'left','0')]);

intInterfaceNodes = N0core + nodesSOUTHside;
writeABQnodeset(inpfullfile,1,intInterfaceNodes,['NODES-ANNULUS-INTINTERFACE-MATRIX',pad(num2str(numFiber),padlength,'left','0')]);

extInterfaceNodes = N0core + nodesNORTHside;
writeABQnodeset(inpfullfile,1,extInterfaceNodes,['NODES-ANNULUS-EXTINTERFACE-MATRIX',pad(num2str(numFiber),padlength,'left','0')]);

writeABQelgen(inpfullfile,E0annular,1,N0core.+elements,ABQel,['ELEMENTS-ANNULUS-MATRIX',pad(num2str(numFiber),padlength,'left','0')]);

writeABQelementset(inpfullfile,2,{['ELEMENTS-CORE-MATRIX',pad(num2str(numFiber),padlength,'left','0')],['ELEMENTS-ANNULUS-MATRIX',pad(num2str(numFiber),padlength,'left','0')]},['ELEMENTS-MATRIX',pad(num2str(numFiber),padlength,'left','0')]);

intInterfaceElements = E0core + elementsSOUTHside;
writeABQelementset(inpfullfile,1,intInterfaceElements,['ELEMENTS-ANNULUS-INTINTERFACE-MATRIX',pad(num2str(numFiber),padlength,'left','0')]);

extInterfaceElements = E0core + elementsNORTHside;
writeABQelementset(inpfullfile,1,extInterfaceElements,['ELEMENTS-ANNULUS-EXTINTERFACE-MATRIX',pad(num2str(numFiber),padlength,'left','0')]);


% ========> creating debonds on the matrix surface
if strcomp(elType,'quads') || strcomp(elType,'quad') || strcomp(elType,'quadrilaterals') || strcomp(elType,'quadrilateral')
  Nnodes = 4;
  if strcomp(elOrder,'first') || strcomp(elOrder,'First') || strcomp(elOrder,'1st') || strcomp(elOrder,'1')
    writeToLogFile(logfullfile,['    Type ad order of elements : First order quadrilaterals','\n'])
    multNodes = 1;
  elseif strcomp(elOrder,'second') || strcomp(elOrder,'Second') || strcomp(elOrder,'2nd') || strcomp(elOrder,'2')
    writeToLogFile(logfullfile,['    Type ad order of elements : Second order quadrilaterals','\n'])
    multNodes = 2;
  end
elseif strcomp(elType,'tris') || strcomp(elType,'tri') || strcomp(elType,'triangles') || strcomp(elType,'triangle')
  Nnodes = 3;
  if strcomp(elOrder,'first') || strcomp(elOrder,'First') || strcomp(elOrder,'1st') || strcomp(elOrder,'1')
    writeToLogFile(logfullfile,['    Type ad order of elements : First order triangles','\n'])
    multNodes = 1;
  elseif strcomp(elOrder,'second') || strcomp(elOrder,'Second') || strcomp(elOrder,'2nd') || strcomp(elOrder,'2')
    writeToLogFile(logfullfile,['    Type ad order of elements : Second order triangles','\n'])
    multNodes = 2;
  end
end

extLabelMax = max(extInterfaceElements);
extLabelMin = min(extInterfaceElements);

angleTol = 0.00001; % 0.001%

writeToLogFile(logfullfile,'    Creating debonded region on matrix surface ...\n')

if length(debonds)>0                                      % at least one debond
  if length(debonds)==1 && abs(pi-debonds(1,2))<=angleTol % completely detached interface
    writeToLogFile(logfullfile,'    Attention! The interface is completely detached.\n')
    writeABQnodeset(inpfullfile,1,extInterfaceNodes,['NODES-DEBOND-WITHOUT-CT-MATRIXSURF-MATRIX',pad(num2str(numFiber),padlength,'left','0')]);
    writeABQelementset(inpfullfile,1,extInterfaceElements,['ELEMENTS-DEBOND-WITHOUT-CT-MATRIXSURF-MATRIX',pad(num2str(numFiber),padlength,'left','0')]);
  else                                                    % at least one partial debond
    debondedNodes = [];
    debondedEls = [];
    firstBondedEls = [];
    allVcctForceNodes = [];
    for d=1:length(debonds)
      currentDebondNodes = [];
      currentDebondElementsWithoutCrackTips = [];
      currentDebondElementsFirstInside = zeros(1,2);            % [at -deltatheta, at +deltatheta]
      currentDebondElementsFirstOutside = zeros(1,2);           % [at -deltatheta, at +deltatheta]
      crackTips = zeros(1,2);                                   % [at -deltatheta, at +deltatheta]
      vcctForceNodes = [zeros(1,multNodes) zeros(1,multNodes)]; % [[at -deltatheta], [at +deltatheta]]
      vcctDispNodes = [zeros(1,multNodes) zeros(1,multNodes)];  % [[at -deltatheta], [at +deltatheta]]
      theta = debonds(d,1);
      deltatheta = debonds(d,2);
      if theta>=-pi && theta<0                              % recast theta in the domain [0,2*pi] if it's in [-pi,0]
        theta = 2*pi + theta;
      end
      if deltatheta<=0 || deltatheta>pi                     % deltatheta is outside its domain of definition, skip this debond
        writeToLogFile(logfullfile,'    Error!! Deltatheta is outside its domain of definition, skipping this debond.\n')
        continue
      end
      if length(debonds)>1                                  % if there's more than one debond, check for overlaps
        toSkip = 0;
        for c=1:d-1
          theta2 = debonds(c,1);
          deltatheta2 = debonds(c,2);
          if theta2>=-pi && theta2<0                              % recast theta2 in the domain [0,2*pi] if it's in [-pi,0]
            theta2 = 2*pi + theta2;
          end
          if deltatheta2<=0 || deltatheta2>pi                     % deltatheta2 is outside its domain of definition, skip this debond
            writeToLogFile(logfullfile,'    Error!! Deltatheta is outside its domain of definition, skipping this debond.\n')
            continue
          end
          if theta2==theta
            writeToLogFile(logfullfile,'    Error!! Debond ',num2str(d),' is centered on the same angle as debond ',num2str(c),', skipping this debond.\n')
            toSkip = 1;
            break
          elseif theta2>theta
            delta1 = theta2 - theta;
            delta2 = theta + (2*pi - theta2)
            if deltatheta+deltatheta2>=delta1 || deltatheta+deltatheta2>=delta2
              writeToLogFile(logfullfile,'    Error!! Debond ',num2str(d),' is overlapping debond ',num2str(c),', skipping this debond.\n')
              toSkip = 1;
              break
            end
          else
            delta1 = theta - theta2;
            delta2 = theta2 + (2*pi - theta)
            if deltatheta+deltatheta2>=delta1 || deltatheta+deltatheta2>=delta2
              writeToLogFile(logfullfile,'    Error!! Debond ',num2str(d),' is overlapping debond ',num2str(c),', skipping this debond.\n')
              toSkip = 1;
              break
            end
          end
        end
        for c=d+1:length(debonds)
          theta2 = debonds(c,1);
          deltatheta2 = debonds(c,2);
          if theta2>=-pi && theta2<0                              % recast theta2 in the domain [0,2*pi] if it's in [-pi,0]
            theta2 = 2*pi + theta2;
          end
          if deltatheta2<=0 || deltatheta2>pi                     % deltatheta2 is outside its domain of definition, skip this debond
            writeToLogFile(logfullfile,'    Error!! Deltatheta is outside its domain of definition, skipping this debond.\n')
            continue
          end
          if theta2==theta
            writeToLogFile(logfullfile,'    Error!! Debond ',num2str(d),' is centered on the same angle as debond ',num2str(c),', skipping this debond.\n')
            toSkip = 1;
            break
          elseif theta2>theta
            delta1 = theta2 - theta;
            delta2 = theta + (2*pi - theta2)
            if deltatheta+deltatheta2>=delta1 || deltatheta+deltatheta2>=delta2
              writeToLogFile(logfullfile,'    Error!! Debond ',num2str(d),' is overlapping debond ',num2str(c),', skipping this debond.\n')
              toSkip = 1;
              break
            end
          else
            delta1 = theta - theta2;
            delta2 = theta2 + (2*pi - theta)
            if deltatheta+deltatheta2>=delta1 || deltatheta+deltatheta2>=delta2
              writeToLogFile(logfullfile,'    Error!! Debond ',num2str(d),' is overlapping debond ',num2str(c),', skipping this debond.\n')
              toSkip = 1;
              break
            end
          end
        end
        if toSkip
          continue
        end
      end
      %thetalo = theta-deltatheta;
      %thetaup = theta+deltatheta;
      %costhetalo = cos(thetalo);
      %sinthetalo = sin(thetalo);
      %costhetaup = cos(thetaup);
      %sinthetaup = sin(thetaup);
      %deltaEl = min(thetas./deltas);
      for e=1:length(extInterfaceElements)                         % sweep through the elements at the external interface
        if isempty(find(extInterfaceElements(e)==debondedEls))     % check the interface element e if it's not inside another debond
          onSurface = []
          for n=1:Nnodes
            if ~isempty(find(N0core.+elements(extInterfaceElements(e)-E0core,n)==intInterfaceNodes))
              onSurface = [onSurface; elements(extInterfaceElements(e),n)];
            end
          end
          x1 = nodes(onSurface(1),1);
          y1 = nodes(onSurface(1),2);
          x2 = nodes(onSurface(2),1);
          y2 = nodes(onSurface(2),2);
          alpha1 = atan2(y1,x1);
          alpha2 = atan2(y2,x2);
          beta1 = alpha1 - theta;
          beta2 = alpha2 - theta;
          beta1abs = abs(beta1);
          beta2abs = abs(beta2);
          deltathetaabs = abs(deltatheta);
          %if beta1abs>deltathetaabs && beta2abs>deltathetaabs       % completely outside the debond
          if beta1abs<deltathetaabs && beta2abs<deltathetaabs   % completely inside the debond
            if isempty(find(N0core.+onSurface(1)==currentDebondNodes)
              currentDebondNodes = [currentDebondNodes;N0core.+onSurface(1)];
            end
            if isempty(find(N0core.+onSurface(2)==currentDebondNodes)
              currentDebondNodes = [currentDebondNodes;N0core.+onSurface(2)];
            end
            if multNodes>1
              for n=Nnodes+1:multNodes*Nnodes
                if ~isempty(find(N0core.+elements(extInterfaceElements(e)-E0core,n)==intInterfaceNodes))
                  onSurface = [onSurface; elements(extInterfaceElements(e),n)];
                  break
                end
              end
              if isempty(find(N0core.+onSurface(3)==currentDebondNodes)
                currentDebondNodes = [currentDebondNodes;N0core.+onSurface(3)];
              end
            end
            currentDebondElementsWithoutCrackTips = [currentDebondElementsWithoutCrackTips;extInterfaceElements(e)];
          elseif (beta1abs>deltathetaabs && beta2abs<deltathetaabs) || (beta1abs<deltathetaabs && beta2abs>deltathetaabs)  % one node outside and one node inside, the element is across the crack tip
            % the current element is the first inside the debond
            % the first element outside must be searched among a restricted pool of candidates
            if beta1abs>deltathetaabs  % node 1 is outside and 2 inside => node 1 is the crack tip
              if beta2<0               % the element is at -deltatheta
                if isempty(find(extInterfaceElements(e)-1==extInterfaceElements)
                  currentDebondElementsFirstOutside(1) = extLabelMax;
                else
                  currentDebondElementsFirstOutside(1) = extInterfaceElements(e)-1;
                end
                crackTips(1) = N0core.+onSurface(1);
                currentDebondElementsFirstInside(1) = extInterfaceElements(e);
                vcctForceNodes(1,1) = N0core.+onSurface(1);
                vcctDispNodes(1,1) = N0core.+onSurface(2);
                if multNodes>1
                  for n=Nnodes+1:multNodes*Nnodes
                    if ~isempty(find(N0core.+elements(extInterfaceElements(e)-E0core,n)==intInterfaceNodes))
                      onSurface = [onSurface; elements(extInterfaceElements(e),n)];
                      break
                    end
                  end
                  for n=Nnodes+1:multNodes*Nnodes
                    if ~isempty(find(N0core.+elements(currentDebondElementsFirstOutside(1)-E0core,n)==intInterfaceNodes))
                      vcctForceNodes(1,2) = N0core.+elements(extInterfaceElements(e),n);
                      break
                    end
                  end
                  vcctDispNodes(1,2) = N0core.+onSurface(3);
                end
              else                     % the element is at +deltatheta
                if isempty(find(extInterfaceElements(e)-1==extInterfaceElements)
                  currentDebondElementsFirstOutside(2) = extLabelMin;
                else
                  currentDebondElementsFirstOutside(2) = extInterfaceElements(e)-1;
                end
                crackTips(2) = N0core.+onSurface(1);
                currentDebondElementsFirstInside(2) = extInterfaceElements(e);
                vcctForceNodes(2,1) = N0core.+onSurface(1);
                vcctDispNodes(2,1) = N0core.+onSurface(2);
                if multNodes>1
                  for n=Nnodes+1:multNodes*Nnodes
                    if ~isempty(find(N0core.+elements(extInterfaceElements(e)-E0core,n)==intInterfaceNodes))
                      onSurface = [onSurface; elements(extInterfaceElements(e),n)];
                      break
                    end
                  end
                  for n=Nnodes+1:multNodes*Nnodes
                    if ~isempty(find(N0core.+elements(currentDebondElementsFirstOutside(2)-E0core,n)==intInterfaceNodes))
                      vcctForceNodes(2,2) = N0core.+elements(extInterfaceElements(e),n);
                      break
                    end
                  end
                  vcctDispNodes(2,2) = N0core.+onSurface(3);
                end
              end
            else                       % node 1 is inside and 2 outside => node 2 is the crack tip
              if beta1<0               % the element is at -deltatheta
                if isempty(find(extInterfaceElements(e)-1==extInterfaceElements)
                  currentDebondElementsFirstOutside(1) = extLabelMax;
                else
                  currentDebondElementsFirstOutside(1) = extInterfaceElements(e)-1;
                end
                crackTips(1) = N0core.+onSurface(2);
                currentDebondElementsFirstInside(1) = extInterfaceElements(e);
                vcctForceNodes(1,1) = N0core.+onSurface(2);
                vcctDispNodes(1,1) = N0core.+onSurface(1);
                if multNodes>1
                  for n=Nnodes+1:multNodes*Nnodes
                    if ~isempty(find(N0core.+elements(extInterfaceElements(e)-E0core,n)==intInterfaceNodes))
                      onSurface = [onSurface; elements(extInterfaceElements(e),n)];
                      break
                    end
                  end
                  for n=Nnodes+1:multNodes*Nnodes
                    if ~isempty(find(N0core.+elements(currentDebondElementsFirstOutside(1)-E0core,n)==intInterfaceNodes))
                      vcctForceNodes(1,2) = N0core.+elements(extInterfaceElements(e),n);
                      break
                    end
                  end
                  vcctDispNodes(1,2) = N0core.+onSurface(3);
                end
              else                     % the element is at +deltatheta
                if isempty(find(extInterfaceElements(e)-1==extInterfaceElements)
                  currentDebondElementsFirstOutside(2) = extLabelMin;
                else
                  currentDebondElementsFirstOutside(2) = extInterfaceElements(e)-1;
                end
                crackTips(2) = N0core.+onSurface(2);
                currentDebondElementsFirstInside(2) = extInterfaceElements(e);
                vcctForceNodes(2,1) = N0core.+onSurface(2);
                vcctDispNodes(2,1) = N0core.+onSurface(1);
                if multNodes>1
                  for n=Nnodes+1:multNodes*Nnodes
                    if ~isempty(find(N0core.+elements(extInterfaceElements(e)-E0core,n)==intInterfaceNodes))
                      onSurface = [onSurface; elements(extInterfaceElements(e),n)];
                      break
                    end
                  end
                  for n=Nnodes+1:multNodes*Nnodes
                    if ~isempty(find(N0core.+elements(currentDebondElementsFirstOutside(2)-E0core,n)==intInterfaceNodes))
                      vcctForceNodes(2,2) = N0core.+elements(extInterfaceElements(e),n);
                      break
                    end
                  end
                  vcctDispNodes(2,2) = N0core.+onSurface(3);
                end
              end
            end
          elseif (beta1abs>deltathetaabs && beta2abs==deltathetaabs) || (beta1abs==deltathetaabs && beta2abs>deltathetaabs)  % one node outside and one node at the crack tip, the element is the first outside the debond
            if beta1abs==deltathetaabs                  % Node 1 is at the crack tip
              if beta1<0                                % Crack tip at -deltatheta
                currentDebondElementsFirstOutside(1) = extInterfaceElements(e);
                if multNodes>1
                  for n=Nnodes+1:multNodes*Nnodes
                    if ~isempty(find(N0core.+elements(extInterfaceElements(e)-E0core,n)==intInterfaceNodes))
                      onSurface = [onSurface; elements(extInterfaceElements(e),n)];
                      break
                    end
                  end
                  vcctForceNodes(1,2) = N0core.+onSurface(3);
                end
              else                                      % Crack tip at +deltatheta
                currentDebondElementsFirstOutside(2) = extInterfaceElements(e);
                if multNodes>1
                  for n=Nnodes+1:multNodes*Nnodes
                    if ~isempty(find(N0core.+elements(extInterfaceElements(e)-E0core,n)==intInterfaceNodes))
                      onSurface = [onSurface; elements(extInterfaceElements(e),n)];
                      break
                    end
                  end
                  vcctForceNodes(2,2) = N0core.+onSurface(3);
                end
              end
            else                                        % Node 2 is at the crack tip
              if beta2<0                                % Crack tip at -deltatheta
                currentDebondElementsFirstOutside(1) = extInterfaceElements(e);
                if multNodes>1
                  for n=Nnodes+1:multNodes*Nnodes
                    if ~isempty(find(N0core.+elements(extInterfaceElements(e)-E0core,n)==intInterfaceNodes))
                      onSurface = [onSurface; elements(extInterfaceElements(e),n)];
                      break
                    end
                  end
                  vcctForceNodes(1,2) = N0core.+onSurface(3);
                end
              else                                      % Crack tip at +deltatheta
                currentDebondElementsFirstOutside(2) = extInterfaceElements(e);
                if multNodes>1
                  for n=Nnodes+1:multNodes*Nnodes
                    if ~isempty(find(N0core.+elements(extInterfaceElements(e)-E0core,n)==intInterfaceNodes))
                      onSurface = [onSurface; elements(extInterfaceElements(e),n)];
                      break
                    end
                  end
                  vcctForceNodes(2,2) = N0core.+onSurface(3);
                end
              end
            end
          elseif (beta1abs<deltathetaabs && beta2abs==deltathetaabs) || (beta1abs==deltathetaabs && beta2abs<deltathetaabs)  % one node inside and one node at the crack tip, the element is the first inside the debond
            if beta1abs==deltathetaabs                  % Node 1 is at the crack tip
              if beta1<0                                % Crack tip at -deltatheta
                crackTips(1) = N0core.+onSurface(1);
                currentDebondElementsFirstInside(1) = extInterfaceElements(e);
                vcctForceNodes(1,1) = N0core.+onSurface(1);
                vcctDispNodes(1,1) = N0core.+onSurface(2);
                if multNodes>1
                  for n=Nnodes+1:multNodes*Nnodes
                    if ~isempty(find(N0core.+elements(extInterfaceElements(e)-E0core,n)==intInterfaceNodes))
                      onSurface = [onSurface; elements(extInterfaceElements(e),n)];
                      break
                    end
                  end
                  vcctDispNodes(1,2) = N0core.+onSurface(3);
                end
              else                                      % Crack tip at +deltatheta
                crackTips(2) = N0core.+onSurface(1);
                currentDebondElementsFirstInside(2) = extInterfaceElements(e);
                vcctForceNodes(2,1) = N0core.+onSurface(1);
                vcctDispNodes(2,1) = N0core.+onSurface(2);
                if multNodes>1
                  for n=Nnodes+1:multNodes*Nnodes
                    if ~isempty(find(N0core.+elements(extInterfaceElements(e)-E0core,n)==intInterfaceNodes))
                      onSurface = [onSurface; elements(extInterfaceElements(e),n)];
                      break
                    end
                  end
                  vcctDispNodes(2,2) = N0core.+onSurface(3);
                end
              end
            else                                        % Node 2 is at the crack tip
              if beta2<0                                % Crack tip at -deltatheta
                crackTips(1) = N0core.+onSurface(2);
                currentDebondElementsFirstInside(1) = extInterfaceElements(e);
                vcctForceNodes(1,1) = N0core.+onSurface(2);
                vcctDispNodes(1,1) = N0core.+onSurface(1);
                if multNodes>1
                  for n=Nnodes+1:multNodes*Nnodes
                    if ~isempty(find(N0core.+elements(extInterfaceElements(e)-E0core,n)==intInterfaceNodes))
                      onSurface = [onSurface; elements(extInterfaceElements(e),n)];
                      break
                    end
                  end
                  vcctDispNodes(1,2) = N0core.+onSurface(3);
                end
              else                                      % Crack tip at +deltatheta
                crackTips(2) = N0core.+onSurface(2);
                currentDebondElementsFirstInside(1) = extInterfaceElements(e);
                vcctForceNodes(2,1) = N0core.+onSurface(2);
                vcctDispNodes(2,1) = N0core.+onSurface(1);
                if multNodes>1
                  for n=Nnodes+1:multNodes*Nnodes
                    if ~isempty(find(N0core.+elements(extInterfaceElements(e)-E0core,n)==intInterfaceNodes))
                      onSurface = [onSurface; elements(extInterfaceElements(e),n)];
                      break
                    end
                  end
                  vcctDispNodes(2,2) = N0core.+onSurface(3);
                end
              end
            end
          end
      end
      % the sweep over the interface elements for the current debond is done
      % add the nodes where vcct displacements will be extracted to the list of current debonded nodes
      if isempty(find(vcctDispNodes(1,1)==currentDebondNodes)
        currentDebondNodes = [currentDebondNodes;vcctDispNodes(1,1)];
      end
      if isempty(find(vcctDispNodes(2,1)==currentDebondNodes)
        currentDebondNodes = [currentDebondNodes;vcctDispNodes(2,1)];
      end
      if multNodes>1
        if isempty(find(vcctDispNodes(1,2)==currentDebondNodes)
          currentDebondNodes = [currentDebondNodes;vcctDispNodes(1,2)];
        end
        if isempty(find(vcctDispNodes(2,2)==currentDebondNodes)
          currentDebondNodes = [currentDebondNodes;vcctDispNodes(2,2)];
        end
      end
      % let's save debonded nodes, vcct forces nodes, debonded elements, first debonded elements and first bonded elements to the global containers
      debondedNodes = [debondedNodes;currentDebondNodes];
      debondedEls = [debondedEls;currentDebondElementsWithoutCrackTips;currentDebondElementsFirstInside(1);currentDebondElementsFirstInside(2)];
      firstBondedEls = [firstBondedEls;currentDebondElementsFirstOutside(1);currentDebondElementsFirstOutside(2)];
      allVcctForceNodes = [allVcctForceNodes;vcctForceNodes(1,1);vcctForceNodes(2,1)];
      if multNodes>1
        allVcctForceNodes = [allVcctForceNodes;vcctForceNodes(1,2);vcctForceNodes(2,2)];
      end
      % and write the debond in the Abaqus input file
      writeABQnodeset(inpfullfile,1,currentDebondNodes,['NODES-DEBOND-WITHOUT-CT-MATRIXSURF-MATRIX',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
      writeABQnodeset(inpfullfile,1,crackTips,['NODES-CRACK-TIPS-MATRIXSURF-MATRIX',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
      writeABQnodeset(inpfullfile,1,crackTips(1),['NODES-CRACK-TIP-NEG-DELTATHETA-MATRIXSURF-MATRIX',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
      writeABQnodeset(inpfullfile,1,crackTips(2),['NODES-CRACK-TIP-POS-DELTATHETA-MATRIXSURF-MATRIX',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
      if multNodes>1
        writeABQnodeset(inpfullfile,1,vcctForceNodes(1,1),['NODES-VCCT-FORCE1-NEG-DELTATHETA-MATRIXSURF-MATRIX',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
        writeABQnodeset(inpfullfile,1,vcctForceNodes(1,2),['NODES-VCCT-FORCE2-NEG-DELTATHETA-MATRIXSURF-MATRIX',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
        writeABQnodeset(inpfullfile,1,vcctDispNodes(1,1),['NODES-VCCT-DISP1-NEG-DELTATHETA-MATRIXSURF-MATRIX',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
        writeABQnodeset(inpfullfile,1,vcctDispNodes(1,2),['NODES-VCCT-DISP2-NEG-DELTATHETA-MATRIXSURF-MATRIX',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
        writeABQnodeset(inpfullfile,1,vcctForceNodes(2,1),['NODES-VCCT-FORCE1-POS-DELTATHETA-MATRIXSURF-MATRIX',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
        writeABQnodeset(inpfullfile,1,vcctForceNodes(2,2),['NODES-VCCT-FORCE2-POS-DELTATHETA-MATRIXSURF-MATRIX',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
        writeABQnodeset(inpfullfile,1,vcctDispNodes(2,1),['NODES-VCCT-DISP1-POS-DELTATHETA-MATRIXSURF-MATRIX',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
        writeABQnodeset(inpfullfile,1,vcctDispNodes(2,2),['NODES-VCCT-DISP2-POS-DELTATHETA-MATRIXSURF-MATRIX',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
      else
        writeABQnodeset(inpfullfile,1,vcctForceNodes(1,1),['NODES-VCCT-FORCE1-NEG-DELTATHETA-MATRIXSURF-MATRIX',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
        writeABQnodeset(inpfullfile,1,vcctDispNodes(1,1),['NODES-VCCT-DISP1-NEG-DELTATHETA-MATRIXSURF-MATRIX',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
        writeABQnodeset(inpfullfile,1,vcctForceNodes(2,1),['NODES-VCCT-FORCE1-POS-DELTATHETA-MATRIXSURF-MATRIX',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
        writeABQnodeset(inpfullfile,1,vcctDispNodes(2,1),['NODES-VCCT-DISP1-POS-DELTATHETA-MATRIXSURF-MATRIX',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
      end
      writeABQelementset(inpfullfile,1,currentDebondElementsWithoutCrackTips,['ELEMENTS-DEBOND-WITHOUT-CT-MATRIXSURF-MATRIX',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
      writeABQelementset(inpfullfile,1,currentDebondElementsFirstInside(1),['ELEMENTS-FIRST-DEBONDED-NEG-DELTATHETA-MATRIXSURF-MATRIX',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
      writeABQelementset(inpfullfile,1,currentDebondElementsFirstInside(2),['ELEMENTS-FIRST-DEBONDED-POS-DELTATHETA-MATRIXSURF-MATRIX',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
      writeABQelementset(inpfullfile,1,currentDebondElementsFirstOutside(1),['ELEMENTS-FIRST-BONDED-NEG-DELTATHETA-MATRIXSURF-MATRIX',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
      writeABQelementset(inpfullfile,1,currentDebondElementsFirstOutside(2),['ELEMENTS-FIRST-BONDED-POS-DELTATHETA-MATRIXSURF-MATRIX',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
      writeABQelementset(inpfullfile,2,{['ELEMENTS-DEBOND-WITHOUT-CT-MATRIXSURF-MATRIX',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')],...
                                        ['ELEMENTS-FIRST-DEBONDED-NEG-DELTATHETA-MATRIXSURF-MATRIX',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')],...
                                        ['ELEMENTS-FIRST-DEBONDED-POS-DELTATHETA-MATRIXSURF-MATRIX',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]},['ELEMENTS-DEBOND-MATRIXSURF-MATRIX',pad(num2str(numFiber),padlength,'left','0'),'-DEBOND',pad(num2str(d),padlength,'left','0')]);
    end
  end
  bondedNodes = [];
  for i=1:length(extInterfaceNodes)
    if isempty(extInterfaceNodes(i)==[debondedNodes;allVcctForceNodes])
      bondedNodes = [bondedNodes; extInterfaceNodes(i)];
    end
  end
  allBondedNodes = [];
  for i=1:length(extInterfaceNodes)
    if isempty(extInterfaceNodes(i)==debondedNodes)
      allBondedNodes = [allBondedNodes; extInterfaceNodes(i)];
    end
  end
  bondedElements = [];
  for i=1:length(extInterfaceElements)
    if isempty(extInterfaceElements(i)==[debondedEls;firstBondedEls])
      bondedElements = [bondedElements; extInterfaceElements(i)];
    end
  end
  allBondedElements = [];
  for i=1:length(extInterfaceElements)
    if isempty(extInterfaceElements(i)==debondedEls)
      allBondedElements = [allBondedElements; extInterfaceElements(i)];
    end
  end
  writeABQnodeset(inpfullfile,1,bondedNodes,['NODES-BONDED-MATRIXSURF-MATRIX',pad(num2str(numFiber),padlength,'left','0')]);
  writeABQelementset(inpfullfile,1,bondedElements,['ELEMENTS-BONDED-MATRIXSURF-MATRIX',pad(num2str(numFiber),padlength,'left','0')]);
  writeABQnodeset(inpfullfile,1,allBondedNodes,['NODES-ALLBONDED-MATRIXSURF-MATRIX',pad(num2str(numFiber),padlength,'left','0')]);
  writeABQelementset(inpfullfile,1,allBondedElements,['ELEMENTS-ALLBONDED-MATRIXSURF-MATRIX',pad(num2str(numFiber),padlength,'left','0')]);
else     % no debond
  writeToLogFile(logfullfile,'    Attention! The interface is completely bonded, no debond present.\n')
  writeABQnodeset(inpfullfile,1,extInterfaceNodes,['NODES-BONDED-MATRIXSURF-MATRIX',pad(num2str(numFiber),padlength,'left','0')]);
  writeABQelementset(inpfullfile,1,extInterfaceElements,['ELEMENTS-BONDED-MATRIXSURF-MATRIX',pad(num2str(numFiber),padlength,'left','0')]);

end

Ntot = N0annular + length(nodes) -1;
Etot = E0annular + length(elements) -1;

writeToLogFile(logfullfile,'    ... done.\n')

elapsed = toc(start);
writeToLogFile(logfullfile,'Timer stopped.\n')
writeToLogFile(logfullfile,['\nELAPSED WALLCLOCK TIME: ', num2str(elapsed),' [s]\n\n'])
writeToLogFile(logfullfile,'Exiting function: writeABQfiber2D\n')


return
