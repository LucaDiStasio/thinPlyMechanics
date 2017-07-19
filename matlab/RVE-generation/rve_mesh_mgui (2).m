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
%  A script to interface the mesh generation algorithms in matlab to the
%  Mathematica GUI
%
%%

clear all
close all
clc

%-------------------------------------------------------------------------%
%-------------------------------------------------------------------------%
%-                          Input Data                                   -%
%-------------------------------------------------------------------------%
%-------------------------------------------------------------------------%

                                                                           % flags for model type
fiberArrangement = 1;                                                      % Number and arrangement of fibers
                                                                           % 1 --> 1    (1 fiber)
                                                                           % 2 --> 2H   (2 fibers, aligned horizontally)
                                                                           % 3 --> 2V   (2 fibers, aligned vertically)
                                                                           % 4 --> 3H   (3 fibers, aligned horizontally)
                                                                           % 5 --> 3V   (3 fibers, aligned vertically)
                                                                           % 6 --> 4    (4 fibers)
                                                                           % 7 --> n    (n fibers in circular arrangement)
isUpperBounded = false;
isLowerBounded = false;
isCohesive = false;
isXFEM = false;

crackType = 1;                                                             % Type of (pre-)crack
                                                                           % 1 --> debond at fiber/matrix interface
                                                                           % 2 --> circular matrix crack
                                                                           % 3 --> straight matrix crack

element = 2;                                                               % Element type: 1 --> quads, 2 --> tri
order = 1;

optimize = true;                                                          % Perform optimization of mesh

Rf = 1;                                                                     % [10^-6 m] fiber diameter in micrometers. 
                                                                            %           Carbon fibers have a tipical diameter between 5 and 10 
                                                                            %           micrometers, glass fibers between 3 and 20
Vff = 0.6;                                                                  % [-] fiber volume fraction
tratio = 0.6;                                                               % [-] ratio of [0°] ply thickness to [90°] ply thickness
theta = 30;                                                                 % [°] angular position of crack
theta = theta*pi/180;
deltatheta = 20;                                                            % [°] angular aperture of crack
deltatheta = deltatheta*pi/180;

f1 = 0.25;                                                                   % [-] innermost square mesh region side defined by 2*f1*Rf
f2 = 0.77;                                                                  % [-] inner circular mesh region radius defined by f2*Rf
f3 = 1.05;                                                                  % [-] Outer circular mesh region radius defined by f2*Rf

                                                                            % number of elements:
N1 = 20;                                                                    % [-] notice that angular resolution is equal to 90°/N1
N2 = 20;                                                                    % [-] 
N3 = 8;                                                                     % [-] 
N4 = 5;                                                                     % [-] 
N5 = 20;                                                                    % [-] 
N6 = 20;                                                                    % [-] 

%-------------------------------------------------------------------------%
%-------------------------------------------------------------------------%
%-                        Mesh Generation                                -%
%-------------------------------------------------------------------------%
%-------------------------------------------------------------------------%

[nodes,edges,elements,...
    fiberN,matrixN,part6bot,part6up,...
    fiberEl,matrixEl,cohesiveEl,boundedBot,boundedUp,...
    gammaNo1,gammaNo2,gammaNo3,gammaNo4,gammaEl1,gammaEl2,gammaEl3,gammaEl4,...
    NintUpNine,NintUpZero,NintBotNine,NintBotZero,NintUpNineCorners,NintUpZeroCorners,NintBotNineCorners,NintBotZeroCorners,...
    NbotRight,NbotLeft,NupRight,NupLeft,EintUpNine,EintUpZero,EintBotNine,EintBotZero,EbotRight,EbotLeft,EupRight,EupLeft,...
    Ncorners,Ndown,Nright,Nup,Nleft,Edown,Eright,Eup,Eleft] = rve_mesh(fiberArrangement,isUpperBounded,isLowerBounded,isCohesive,crackType,...
                                                                          element,order,optimize,...
                                                                          Rf,Vff,tratio,theta,deltatheta,...
                                                                          f1,f2,f3,N1,N2,N3,N4,N5,N6);

%-------------------------------------------------------------------------%
%-------------------------------------------------------------------------%
%-                         Visualization                                 -%
%-------------------------------------------------------------------------%
%-------------------------------------------------------------------------%

fig0 = figure();
plot(nodes(:,1),nodes(:,2),'b.')
hold on
grid on
xlabel('x')
ylabel('y')
title('RVE mesh')
axis equal
l = 0.5*Rf*sqrt(pi/Vff);
axis([-1.1*(1+tratio)*l 1.1*(1+tratio)*l -1.1*(1+tratio)*l 1.1*(1+tratio)*l])
% hold on
% for i=1:size(nodes,1)
%     plot(nodes(i,1),nodes(i,2),'b.')
%     hold on
%     pause(0.01)
% end


fig1 = figure();
xlabel('x')
ylabel('y')
title('RVE mesh')
axis equal
l = 0.5*Rf*sqrt(pi/Vff);
axis([-1.1*(1+tratio)*l 1.1*(1+tratio)*l -1.1*(1+tratio)*l 1.1*(1+tratio)*l])
hold on
for i=1:size(edges,1)
    plot([nodes(edges(i,1),1),nodes(edges(i,2),1)],[nodes(edges(i,1),2),nodes(edges(i,2),2)],'k-')
    hold on
%     pause(0.05)
end


fig2 = figure();
xlabel('x')
ylabel('y')
title('RVE mesh')
axis equal
l = 0.5*Rf*sqrt(pi/Vff);
axis([-1.1*(1+tratio)*l 1.1*(1+tratio)*l -1.1*(1+tratio)*l 1.1*(1+tratio)*l])
hold on
for i=1:size(edges,1)
    plot([nodes(edges(i,1),1),nodes(edges(i,2),1)],[nodes(edges(i,1),2),nodes(edges(i,2),2)],'k-')
    hold on
end
plot(nodes(:,1),nodes(:,2),'k.')
hold on

fig4 = figure();
plot(nodes(:,1),nodes(:,2),'b.')
hold on
for i=1:size(nodes,1)
    txt = num2str(i);
    text(nodes(i,1),nodes(i,2),txt,'Color',[1 0 0]);
    hold on
end
xlabel('x')
ylabel('y')
title('RVE mesh')
axis equal
l = 0.5*Rf*sqrt(pi/Vff);
axis([-1.1*(1+tratio)*l 1.1*(1+tratio)*l -1.1*(1+tratio)*l 1.1*(1+tratio)*l])

% fig5 = figure();
% xlabel('x')
% ylabel('y')
% title('RVE mesh')
% axis equal
% l = 0.5*Rf*sqrt(pi/Vff);
% axis([-1.1*(1+tratio)*l 1.1*(1+tratio)*l -1.1*(1+tratio)*l 1.1*(1+tratio)*l])
% hold on
% for i=1:size(edges,1)
%     plot([nodes(edges(i,1),1),nodes(edges(i,2),1)],[nodes(edges(i,1),2),nodes(edges(i,2),2)],'k-')
%     hold on
% end
% plot(nodes(:,1),nodes(:,2),'k.')
% hold on
% for i=1:size(nodes,1)
%     txt = num2str(i);
%     text(nodes(i,1),nodes(i,2),txt,'Color',[1 0 0]);
%     hold on
% end
% for i=1:size(edges,1)
%     txt = num2str(i);
%     text(0.5*(nodes(edges(i,1),1)+nodes(edges(i,2),1)),0.5*(nodes(edges(i,1),2)+nodes(edges(i,2),2)),txt,'Color',[0 1 0]);
%     hold on
% end

% fig6 = figure();
% xlabel('x')
% ylabel('y')
% title('RVE mesh')
% axis equal
% l = 0.5*Rf*sqrt(pi/Vff);
% axis([-1.1*(1+tratio)*l 1.1*(1+tratio)*l -1.1*(1+tratio)*l 1.1*(1+tratio)*l])
% hold on
% for i=1:size(edges,1)
%     plot([nodes(edges(i,1),1),nodes(edges(i,2),1)],[nodes(edges(i,1),2),nodes(edges(i,2),2)],'k-')
%     hold on
% end
% plot(nodes(:,1),nodes(:,2),'k.')
% hold on
% for i=1:size(elements,1)
%     txt = num2str(i);
%     text(0.25*(nodes(elements(i,1),1)+nodes(elements(i,2),1)+nodes(elements(i,3),1)+nodes(elements(i,4),1)),0.25*(nodes(elements(i,1),2)+nodes(elements(i,2),2)+nodes(elements(i,3),2)+nodes(elements(i,4),2)),txt,'Color',[1 0 1]);
%     hold on
% end

% fig6 = figure();
% xlabel('x')
% ylabel('y')
% title('RVE mesh')
% axis equal
% l = 0.5*Rf*sqrt(pi/Vff);
% axis([-1.1*(1+tratio)*l 1.1*(1+tratio)*l -1.1*(1+tratio)*l 1.1*(1+tratio)*l])
% hold on
% for i=1:size(gammaNo1,1)
%     plot(nodes(gammaNo1(i,1),1),nodes(gammaNo1(i,1),2),'k.')
%     hold on
% end
% for i=1:size(gammaNo2,1)
%     plot(nodes(gammaNo2(i,1),1),nodes(gammaNo2(i,1),2),'r.')
%     hold on
% end
% for i=1:size(gammaNo3,1)
%     plot(nodes(gammaNo3(i,1),1),nodes(gammaNo3(i,1),2),'b.')
%     hold on
% end
% for i=1:size(gammaNo4,1)
%     plot(nodes(gammaNo4(i,1),1),nodes(gammaNo4(i,1),2),'g.')
%     hold on
% end

% fig7 = figure();
% xlabel('x')
% ylabel('y')
% title('RVE mesh')
% axis equal
% l = 0.5*Rf*sqrt(pi/Vff);
% axis([-1.1*(1+tratio)*l 1.1*(1+tratio)*l -1.1*(1+tratio)*l 1.1*(1+tratio)*l])
% hold on
% for i=1:size(gammaEl1,1)
%     index = gammaEl1(i);
%     plot([nodes(elements(index,1),1),nodes(elements(index,2),1)],[nodes(elements(index,1),2),nodes(elements(index,2),2)],'k-')
%     hold on
% end
% for i=1:size(gammaEl1,1)
%     index = gammaEl1(i);
%     txt = num2str(index);
%     text(0.25*(nodes(elements(index,1),1)+nodes(elements(index,2),1)+nodes(elements(index,3),1)+nodes(elements(index,4),1)),0.25*(nodes(elements(index,1),2)+nodes(elements(index,2),2)+nodes(elements(index,3),2)+nodes(elements(index,4),2)),txt,'Color',[1 0 1]);
%     hold on
% end
% for i=1:size(gammaEl2,1)
%     index = gammaEl2(i);
%     plot([nodes(elements(index,1),1),nodes(elements(index,2),1)],[nodes(elements(index,1),2),nodes(elements(index,2),2)],'k-')
%     hold on
% end
% for i=1:size(gammaEl2,1)
%     index = gammaEl2(i);
%     txt = num2str(index);
%     text(0.25*(nodes(elements(index,1),1)+nodes(elements(index,2),1)+nodes(elements(index,3),1)+nodes(elements(index,4),1)),0.25*(nodes(elements(index,1),2)+nodes(elements(index,2),2)+nodes(elements(index,3),2)+nodes(elements(index,4),2)),txt,'Color',[1 0 1]);
%     hold on
% end
% for i=1:size(gammaEl3,1)
%     index = gammaEl3(i);
%     plot([nodes(elements(index,4),1),nodes(elements(index,3),1)],[nodes(elements(index,4),2),nodes(elements(index,3),2)],'k-')
%     hold on
% end
% for i=1:size(gammaEl3,1)
%     index = gammaEl3(i);
%     txt = num2str(index);
%     text(0.25*(nodes(elements(index,1),1)+nodes(elements(index,2),1)+nodes(elements(index,3),1)+nodes(elements(index,4),1)),0.25*(nodes(elements(index,1),2)+nodes(elements(index,2),2)+nodes(elements(index,3),2)+nodes(elements(index,4),2)),txt,'Color',[1 0 1]);
%     hold on
% end
% for i=1:size(gammaEl4,1)
%     index = gammaEl4(i);
%     plot([nodes(elements(index,4),1),nodes(elements(index,3),1)],[nodes(elements(index,4),2),nodes(elements(index,3),2)],'k-')
%     hold on
% end
% for i=1:size(gammaEl4,1)
%     index = gammaEl4(i);
%     txt = num2str(index);
%     text(0.25*(nodes(elements(index,1),1)+nodes(elements(index,2),1)+nodes(elements(index,3),1)+nodes(elements(index,4),1)),0.25*(nodes(elements(index,1),2)+nodes(elements(index,2),2)+nodes(elements(index,3),2)+nodes(elements(index,4),2)),txt,'Color',[1 0 1]);
%     hold on
% end
