function[isInContact] = checkContact(xref,yref,ux1,uy1,ux2,uy2,tol,xc,yc)
%%
%==============================================================================
% Copyright (c) 2016-2018 Universite de Lorraine & Lulea tekniska universitet
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
% Neither the name of the Universite de Lorraine or Lulea tekniska universitet
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
%  A function to check the contact of two surfaces in 2D, given the displacements
%  and coordinates of their nodes in the global reference frame
%
%  Input
%  xref  - [Nx1] (column vector) of x-coordinates of one surface's nodes
%  yref  - [Nx1] (column vector) of y-coordinates of one surface's nodes
%  ux1 - [Nx1] (column vector) of x-component of displacement of the first surface's nodes
%  uy1 - [Nx1] (column vector) of y-component of displacement of the first surface's nodes
%  ux2 - [Nx1] (column vector) of x-component of displacement of the second surface's nodes
%  uy2 - [Nx1] (column vector) of y-component of displacement of the second surface's nodes
%
%  OBS: nodes belonging to the two surfaces must be ordered in the same way, i.e.
%       node 1 of surface 1 is in front of node 1 of surface, they are coincident 
%       in the undeformed configuration
%
%  xc  - scalar or [Nx1] (column vector) of x-coordinates of vectors' start-points; if scalar the point is common to all vectors
%  yc  - scalar or [Nx1] (column vector) of y-coordinates of vectors' start-points; if scalar the point is common to all vectors
%  tol - scalar, tolerance on crack radial displacement, default = 0
%
%  Output
%  isInContact - [Nx1] (column vector) of 0s and 1s: 0 = surfaces not in contact, 1 = surfaces in contact
%%

if ~exist('tol','var')
    tol = 0.0;
end

[mx1,nx1] = size(ux1);
[my1,ny1] = size(uy1);
[mx2,nx2] = size(ux2);
[my2,ny2] = size(uy2);
[mxr,nxr] = size(xref);
[myr,nyr] = size(yref);

if ~exist('xc','var')
    xc = 0.0;
end
if ~exist('yc','var')
    yc = 0.0;
end

[mxc,nxc] = size(xc);
[myc,nyc] = size(yc);

if mx1==my1 && nx1==ny1 && mx2==my2 && nx2==ny2 && mx2==mx1 && nx1==nx2 && mxr==myr && nxr==nyr && mxr==mx1 && nxr==nx2 && nx1==1 && (mxc==mx1 || mxc==1) && (myc==mx1 || myc==1) && nxc==1 && nyc==1
    [beta,betadeg] = getOrientation(xref,yref);
    [ur1,utheta1] = rotate(ux1,uy1,beta);
    [ur2,utheta2] = rotate(ux2,uy2,beta);
    deltaur = abs(ur2 - ur1);
    isInContact = zeros(mx1,1);
    isInContact(deltaur<=tol) = 1; 
else
    isInContact = 0;
    disp('!------------------------------!');
    disp('!             ERROR            !');
    disp('!       Wrong dimensions       !');
    disp('!------------------------------!');
end

return
