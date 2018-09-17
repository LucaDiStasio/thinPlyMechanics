function[x1,y1] = rotate(x,y,beta,xc,yc)
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
%  A function to rotate vectors, defined by the coordinates of their end-points
%  
%  Input
%  x - [Nx1] (column vector) of x-coordinates of vectors' end-points
%  y - [Nx1] (column vector) of y-coordinates of vectors' end-points
%  beta - [Nx1] (column vector) of angles in rad
%  xc - scalar or [Nx1] (column vector) of x-coordinates of vectors' start-points; if scalar the point is common to all vectors
%  yc - scalar or [Nx1] (column vector) of y-coordinates of vectors' start-points; if scalar the point is common to all vectors
%
%  Output
%  x1 - [Nx1] (column vector) of x'-coordinates (rotated frame) of vectors' end-points
%  y1 - [Nx1] (column vector) of y'-coordinates (rotated frame) of vectors' end-points
%
%%

[mx,nx] = size(x);
[my,ny] = size(y);
[mb,nb] = size(beta);

if ~exist('xc','var')
    xc = 0.0;
if ~exist('yc','var')
    yc = 0.0;

[mxc,nxc] = size(xc);
[myc,nyc] = size(yc);


if mx==my && nx==ny && mb==mx && nb==nx && nx=1 && (mxc==mx || mxc==1) && (myc==mx || myc==1) && nxc==1 && nyc==1
    cosbeta = cos(beta);
    sinbeta = sin(beta);
    r = cosbeta.*(x.-xc)+sinbeta.*(y.-yc);
    theta = -sinbeta.*(x.-xc)+cosbeta.*(y.-yc);
else
    beta = 0;
    betadeg = 0;
    disp('!------------------------------!');
    disp('!             ERROR            !');
    disp('!       Wrong dimensions       !');
    disp('!------------------------------!');

return
