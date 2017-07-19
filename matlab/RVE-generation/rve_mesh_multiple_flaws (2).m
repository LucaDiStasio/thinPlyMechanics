function[nodes,edges,elements,...
    fiberN,matrixN,part6bot,part6up,...
    fiberEl,matrixEl,cohesiveEl,boundedBot,boundedUp,...
    gammaNo1,gammaNo2,gammaNo3,gammaNo4,gammaEl1,gammaEl2,gammaEl3,gammaEl4,...
    NintUpNine,NintUpZero,NintBotNine,NintBotZero,NintUpNineCorners,NintUpZeroCorners,NintBotNineCorners,NintBotZeroCorners,...
    NbotRight,NbotLeft,NupRight,NupLeft,EintUpNine,EintUpZero,EintBotNine,EintBotZero,EbotRight,EbotLeft,EupRight,EupLeft,...
    Ncorners,Ndown,Nright,Nup,Nleft,Edown,Eright,Eup,Eleft]=rve_mesh(fiberArrangement,isUpperBounded,isLowerBounded,isCohesive,crackType,...
                                                                          element,order,optimize,...
                                                                          Rf,Vff,tratio,theta,deltatheta,...
                                                                          f1,f2,f3,N1,N2,N3,N4,N5,N6)
%%
%==============================================================================
% Copyright (c) 2016 Université de Lorraine & Luleå tekniska universitet
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
% Neither the name of the Université de Lorraine or Luleå tekniska universitet
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
%  A function to perform 
%
%  Input: isBounded = true; % flag for model type
% 
% Rf = 1; %[10^-6 m] Fiber diameter in micrometers. 
%         % Carbon fibers have a tipical diameter between 5 and 10 
%         % micrometers, glass fibers between 3 and 20
% Vff = 0.6; %[-] Fiber volume fraction
% tratio = 0.6; % [-] ratio of [0°] ply thickness to [90°] ply thickness
% theta = 30; %[°] angular position of crack
% theta = theta*pi/180;
% deltatheta = 10; %[°] angular aperture of crack
% deltatheta = deltatheta*pi/180;
% 
% f1 = 0.5; %[-] Innermost square mesh region side defined by 2*f1*Rf
% f2 = 0.77; %[-] Inner circular mesh region radius defined by f2*Rf
% f3 = 1.05; %[-] Outer circular mesh region radius defined by f2*Rf
% 
% %Number of elements:
% N1 = 20; %[-] Notice that angular resolution is equal to 90°/N1
% N2 = 10; %[-] 
% N3 = 8; %[-] 
% N4 = 5; %[-] 
% N5 = 20; %[-] 
% N6 = 20; %[-] 
%  Output: 
%
%%

switch fiberArrangement
    case 1
        switch crackType
            case 1
                if element ==1
                    if order==1
                        [nodes,edges,elements,...
                            fiberN,matrixN,part6bot,part6up,...
                            fiberEl,matrixEl,cohesiveEl,boundedBot,boundedUp,...
                            gammaNo1,gammaNo2,gammaNo3,gammaNo4,gammaEl1,gammaEl2,gammaEl3,gammaEl4,...
                            NintUpNine,NintUpZero,NintBotNine,NintBotZero,NintUpNineCorners,NintUpZeroCorners,NintBotNineCorners,NintBotZeroCorners,...
                            NbotRight,NbotLeft,NupRight,NupLeft,EintUpNine,EintUpZero,EintBotNine,EintBotZero,EbotRight,EbotLeft,EupRight,EupLeft,...
                            Ncorners,Ndown,Nright,Nup,Nleft,Edown,Eright,Eup,Eleft]=rve_mesh_F1_C1_quad1(isUpperBounded,isLowerBounded,isCohesive,Rf,Vff,tratio,theta,deltatheta,f1,f2,f3,N1,N2,N3,N4,N5,N6);
                    elseif order==2
                        [nodes,edges,elements]=rve_mesh_F1_C1_quad2(isUpperBounded,isLowerBounded,isCohesive,Rf,Vff,tratio,theta,deltatheta,f1,f2,f3,N1,N2,N3,N4,N5,N6);
                    end
                else
                    if order==1
                        [nodes,edges,elements,...
                            fiberN,matrixN,part6bot,part6up,...
                            fiberEl,matrixEl,cohesiveEl,boundedBot,boundedUp,...
                            gammaNo1,gammaNo2,gammaNo3,gammaNo4,gammaEl1,gammaEl2,gammaEl3,gammaEl4,...
                            NintUpNine,NintUpZero,NintBotNine,NintBotZero,NintUpNineCorners,NintUpZeroCorners,NintBotNineCorners,NintBotZeroCorners,...
                            NbotRight,NbotLeft,NupRight,NupLeft,EintUpNine,EintUpZero,EintBotNine,EintBotZero,EbotRight,EbotLeft,EupRight,EupLeft,...
                            Ncorners,Ndown,Nright,Nup,Nleft,Edown,Eright,Eup,Eleft]=rve_mesh_F1_C1_tri1(isUpperBounded,isLowerBounded,isCohesive,Rf,Vff,tratio,theta,deltatheta,f1,f2,f3,N1,N2,N3,N4,N5,N6);
                        if optimize
                            boundary = [Ncorners;Ndown;Nright;Nup;Nleft;...
                                        NbotRight;NbotLeft;NupRight;NupLeft;...
                                        gammaNo1;gammaNo2;gammaNo3;gammaNo4,...
                                        NintUpNine;NintUpZero;NintBotNine;NintBotZero;NintUpNineCorners;NintUpZeroCorners;NintBotNineCorners;NintBotZeroCorners];
                            obj = 0.9;
                            tol = 0.01;
                            maxIt = 100;
                            [nodes,edges,elements] = tri3optimize(nodes,edges,elements,boundary,obj,tol,maxIt);
                        end
                    elseif order==2
                        [nodes,edges,elements]=rve_mesh_F1_C1_tri2(isUpperBounded,isLowerBounded,isCohesive,Rf,Vff,tratio,theta,deltatheta,f1,f2,f3,N1,N2,N3,N4,N5,N6);
                    end
                end
            case 2
                if element ==1
                    if order==1
                        [nodes,edges,elements,gammaNo1,gammaNo2,gammaEl1,gammaEl2]=rve_mesh_F1_C2_quad1(isUpperBounded,isLowerBounded,isCohesive,Rf,Vff,tratio,theta,deltatheta,f1,f2,f3,N1,N2,N3,N4,N5,N6);
                    elseif order==2
                        [nodes,edges,elements,gammaNo1,gammaNo2,gammaEl1,gammaEl2]=rve_mesh_F1_C2_quad2(isUpperBounded,isLowerBounded,isCohesive,Rf,Vff,tratio,theta,deltatheta,f1,f2,f3,N1,N2,N3,N4,N5,N6);
                    end
                else
                    if order==1
                        [nodes,edges,elements,gammaNo1,gammaNo2,gammaEl1,gammaEl2]=rve_mesh_F1_C2_tri1(isUpperBounded,isLowerBounded,isCohesive,Rf,Vff,tratio,theta,deltatheta,f1,f2,f3,N1,N2,N3,N4,N5,N6);
                    elseif order==2
                        [nodes,edges,elements,gammaNo1,gammaNo2,gammaEl1,gammaEl2]=rve_mesh_F1_C2_tri2(isUpperBounded,isLowerBounded,isCohesive,Rf,Vff,tratio,theta,deltatheta,f1,f2,f3,N1,N2,N3,N4,N5,N6);
                    end
                end
            case 3
                if element ==1
                    if order==1
                        [nodes,edges,elements,gammaNo1,gammaNo2,gammaEl1,gammaEl2]=rve_mesh_F1_C3_quad1(isUpperBounded,isLowerBounded,isCohesive,Rf,Vff,tratio,theta,deltatheta,f1,f2,f3,N1,N2,N3,N4,N5,N6);
                    elseif order==2
                        [nodes,edges,elements,gammaNo1,gammaNo2,gammaEl1,gammaEl2]=rve_mesh_F1_C3_quad2(isUpperBounded,isLowerBounded,isCohesive,Rf,Vff,tratio,theta,deltatheta,f1,f2,f3,N1,N2,N3,N4,N5,N6);
                    end
                else
                    if order==1
                        [nodes,edges,elements,gammaNo1,gammaNo2,gammaEl1,gammaEl2]=rve_mesh_F1_C3_tri1(isUpperBounded,isLowerBounded,isCohesive,Rf,Vff,tratio,theta,deltatheta,f1,f2,f3,N1,N2,N3,N4,N5,N6);
                    elseif order==2
                        [nodes,edges,elements,gammaNo1,gammaNo2,gammaEl1,gammaEl2]=rve_mesh_F1_C3_tri2(isUpperBounded,isLowerBounded,isCohesive,Rf,Vff,tratio,theta,deltatheta,f1,f2,f3,N1,N2,N3,N4,N5,N6);
                    end
                end
        end
    case 2
        
    case 3
        
    case 4
        
    case 5
        
    case 6
        
    case 7
    
end

if ~exist('nodes')
    nodes = [];
end
if ~exist('edges')
    edges = [];
end
if ~exist('elements')
    elements = [];
end
if ~exist('fiberN')
    fiberN = [];
end
if ~exist('matrixN')
    matrixN = [];
end
if ~exist('part6bot')
    part6bot = [];
end
if ~exist('part6up')
    part6up = [];
end
if ~exist('fiberEl')
    fiberEl = [];
end
if ~exist('matrixEl')
    matrixEl = [];
end
if ~exist('cohesiveEl')
    cohesiveEl = [];
end
if ~exist('boundedBot')
    boundedBot = [];
end
if ~exist('boundedUp')
    boundedUp = [];
end
if ~exist('gammaNo1')
    gammaNo1 = [];
end
if ~exist('gammaNo2')
    gammaNo2 = [];
end
if ~exist('gammaNo3')
    gammaNo3 = [];
end
if ~exist('gammaNo4')
    gammaNo4 = [];
end
if ~exist('gammaEl1')
    gammaEl1 = [];
end
if ~exist('gammaEl2')
    gammaEl2 = [];
end
if ~exist('gammaEl3')
    gammaEl3 = [];
end
if ~exist('gammaEl4')
    gammaEl4 = [];
end
if ~exist('NintUpNine')
    NintUpNine = [];
end
if ~exist('NintUpZero')
    NintUpZero = [];
end
if ~exist('NintBotNine')
    NintBotNine = [];
end
if ~exist('NintBotZero')
    NintBotZero = [];
end
if ~exist('NintUpNineCorners')
    NintUpNineCorners = [];
end
if ~exist('NintUpZeroCorners')
    NintUpZeroCorners = [];
end
if ~exist('NintBotNineCorners')
    NintBotNineCorners = [];
end
if ~exist('NintBotZeroCorners')
    NintBotZeroCorners = [];
end
if ~exist('NbotRight')
    NbotRight = [];
end
if ~exist('NbotLeft')
    NbotLeft = [];
end
if ~exist('NupRight')
    NupRight = [];
end
if ~exist('NupLeft')
    NupLeft = [];
end
if ~exist('EintUpNine')
    EintUpNine = [];
end
if ~exist('EintUpZero')
    EintUpZero = [];
end
if ~exist('EintBotNine')
    EintBotNine = [];
end
if ~exist('EintBotZero')
    EintBotZero = [];
end
if ~exist('EbotRight')
    EbotRight = [];
end
if ~exist('EbotLeft')
    EbotLeft = [];
end
if ~exist('EupRight')
    EupRight = [];
end
if ~exist('EupLeft')
    EupLeft = [];
end
if ~exist('Ncorners')
    Ncorners = [];
end
if ~exist('Ndown')
    Ndown = [];
end
if ~exist('Nright')
    Nright = [];
end
if ~exist('Nup')
    Nup = [];
end
if ~exist('Nleft')
    Nleft = [];
end
if ~exist('Edown')
    Edown = [];
end
if ~exist('Eright')
    Eright = [];
end
if ~exist('Eup')
    Eup = [];
end
if ~exist('Eleft')
    Eleft = [];
end

return