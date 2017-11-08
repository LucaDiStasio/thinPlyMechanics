function[Ntot,Etot]=writeABQmatrix2D(logfullfile,inpfullfile,numFiber,padlength,elType,elOrder,ABQel,startNode,startEl,x0,y0,lx,ly,Nx,Ny)
%%
%%==============================================================================
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
%  Input: x0 - scalar - x-coordinate of center
%         y0 - scalar - y-coordinate of center
%         lx - [M x 1] vector - Side length in each one of the M mesh regions in x-direction
%         ly - [N x 1] vector - Side length in each one of the N mesh regions in y-direction
%         Nx - [M x 1] vector - Number of ELEMENTS in each one of the M mesh regions in x-direction
%         Ny - [N x 1] vector - Number of ELEMENTS in each one of the N mesh regions in y-direction
%         fibers - [H x 3] matrix - H is the number of fibers; for each fiber the following data must be provided:
%                                   xC - scalar - x-coordinate of hole's center
%                                   yC - scalar - y-coordinate of hole's center
%                                   R - scalar - external radius of the matrix's circular annulus around the fiber
%
%%
writeToLogFile(logfullfile,'In function: writeABQmatrix2D\n')
writeToLogFile(logfullfile,'\nStarting timer\n')
start = tic;

writeToLogFile(logfullfile,['    Creating MATRIX ','\n'])

N0 = startNode + 1;
E0 = startEl + 1;

writeToLogFile(logfullfile,['    Calling function ', 'meshGenGradedCircSec',' ...\n']);

[nodes,elements,edges,...
         nodesSWcorner,nodesSEcorner,nodesNEcorner,nodesNWcorner,...
         nodesSOUTHside,nodesEASTside,nodesNORTHside,nodesWESTside,...
         edgesSOUTHside,edgesEASTside,edgesNORTHside,edgesWESTside,...
         elementsSWcorner,elementsSEcorner,elementsNEcorner,elementsNWcorner,...
         elementsSOUTHside,elementsEASTside,elementsNORTHside,elementsWESTside,...
         nodesInternalBoundaries,elementsInternalBoundaries]=meshGenCircHolesGradedRect(logfullfile,elType,elOrder,x0,y0,lx,ly,Nx,Ny,fibers)

writeABQnodegen(inpfullfile,N0,1,nodes,'NODES-MATRIX');

writeABQnodeset(inpfullfile,1,startNode + nodesSWcorner,'NODES-SW-CORNER-MATRIX');
writeABQnodeset(inpfullfile,1,startNode + nodesSEcorner,'NODES-SE-CORNER-MATRIX');
writeABQnodeset(inpfullfile,1,startNode + nodesNEcorner,'NODES-NE-CORNER-MATRIX');
writeABQnodeset(inpfullfile,1,startNode + nodesNWcorner,'NODES-NW-CORNER-MATRIX');

writeABQnodeset(inpfullfile,1,startNode + nodesSOUTHside,'NODES-SOUTH-SIDE-WITHOUT-CORNERS-MATRIX');
writeABQnodeset(inpfullfile,1,startNode + nodesEASTside,'NODES-EAST-SIDE-WITHOUT-CORNERS-MATRIX');
writeABQnodeset(inpfullfile,1,startNode + nodesNORTHside,'NODES-NORTH-SIDE-WITHOUT-CORNERS-MATRIX');
writeABQnodeset(inpfullfile,1,startNode + nodesWESTside,'NODES-WEST-SIDE-WITHOUT-CORNERS-MATRIX');

writeABQnodeset(inpfullfile,2,{'NODES-SOUTH-SIDE-WITHOUT-CORNERS-MATRIX','NODES-SW-CORNER-MATRIX','NODES-SE-CORNER-MATRIX'},'NODES-SOUTH-SIDE-MATRIX');
writeABQnodeset(inpfullfile,2,{'NODES-EAST-SIDE-WITHOUT-CORNERS-MATRIX','NODES-SE-CORNER-MATRIX','NODES-NE-CORNER-MATRIX'},'NODES-EAST-SIDE-MATRIX');
writeABQnodeset(inpfullfile,2,{'NODES-NORTH-SIDE-WITHOUT-CORNERS-MATRIX','NODES-NW-CORNER-MATRIX','NODES-NE-CORNER-MATRIX'},'NODES-NORTH-SIDE-MATRIX');
writeABQnodeset(inpfullfile,2,{'NODES-WEST-SIDE-WITHOUT-CORNERS-MATRIX','NODES-NW-CORNER-MATRIX','NODES-SW-CORNER-MATRIX'},'NODES-WEST-SIDE-MATRIX');

for i=1:length(nodesInternalBoundaries)
  writeABQnodeset(inpfullfile,1,startNode + nodesInternalBoundaries{i},['NODES-MATRIX-INTERFACE-WITH-FIBER',pad(num2str(numFiber),padlength,'left','0')]);
end

writeABQelgen(inpfullfile,E0,1,startNode.+elements,ABQel,'ELEMENTS-MATRIX');

writeABQelementset(inpfullfile,1,startEl + elementsSWcorner,'ELEMENTS-SW-CORNER-MATRIX');
writeABQelementset(inpfullfile,1,startEl + elementsSEcorner,'ELEMENTS-SE-CORNER-MATRIX');
writeABQelementset(inpfullfile,1,startEl + elementsNEcorner,'ELEMENTS-NE-CORNER-MATRIX');
writeABQelementset(inpfullfile,1,startEl + elementsNWcorner,'ELEMENTS-NW-CORNER-MATRIX');

writeABQelementset(inpfullfile,1,startEl + elementsSOUTHside,'ELEMENTS-SOUTH-SIDE-WITHOUT-CORNERS-MATRIX');
writeABQelementset(inpfullfile,1,startEl + elementsEASTside,'ELEMENTS-EAST-SIDE-WITHOUT-CORNERS-MATRIX');
writeABQelementset(inpfullfile,1,startEl + elementsNORTHside,'ELEMENTS-NORTH-SIDE-WITHOUT-CORNERS-MATRIX');
writeABQelementset(inpfullfile,1,startEl + elementsWESTside,'ELEMENTS-WEST-SIDE-WITHOUT-CORNERS-MATRIX');

writeABQelementset(inpfullfile,2,{'ELEMENTS-SOUTH-SIDE-WITHOUT-CORNERS-MATRIX','ELEMENTS-SW-CORNER-MATRIX','ELEMENTS-SE-CORNER-MATRIX'},'ELEMENTS-SOUTH-SIDE-MATRIX');
writeABQelementset(inpfullfile,2,{'ELEMENTS-EAST-SIDE-WITHOUT-CORNERS-MATRIX','ELEMENTS-SE-CORNER-MATRIX','ELEMENTS-NE-CORNER-MATRIX'},'ELEMENTS-EAST-SIDE-MATRIX');
writeABQelementset(inpfullfile,2,{'ELEMENTS-NORTH-SIDE-WITHOUT-CORNERS-MATRIX','ELEMENTS-NW-CORNER-MATRIX','ELEMENTS-NE-CORNER-MATRIX'},'ELEMENTS-NORTH-SIDE-MATRIX');
writeABQelementset(inpfullfile,2,{'ELEMENTS-WEST-SIDE-WITHOUT-CORNERS-MATRIX','ELEMENTS-NW-CORNER-MATRIX','ELEMENTS-SW-CORNER-MATRIX'},'ELEMENTS-WEST-SIDE-MATRIX');

for i=1:length(elementsInternalBoundaries)
  writeABQnodeset(inpfullfile,1,startEl + elementsInternalBoundaries{i},['ELEMENTS-MATRIX-INTERFACE-WITH-FIBER',pad(num2str(numFiber),padlength,'left','0')]);
end

Ntot = startNode + length(nodes);
Etot = startEl + length(elements);

elapsed = toc(start);
writeToLogFile(logfullfile,'Timer stopped.\n')
writeToLogFile(logfullfile,['\nELAPSED WALLCLOCK TIME: ', num2str(elapsed),' [s]\n\n'])
writeToLogFile(logfullfile,'Exiting function: writeABQfiber2D\n')

return
