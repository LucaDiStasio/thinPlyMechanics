function[rhoc,E1,E2,nu12,nu21,G12,nu23,G23,alpha1,alpha2]=Hashin(Vf,rhof,ELf,ETf,nu12f,nu23f,alphaLf,alphaTf,rhom,ELm,ETm,num,alpham)
%%
%==============================================================================
% Copyright (c) 2017 Université de Lorraine & Luleå tekniska universitet
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
%  A function implementing the Hashin (CCA) method for fiber reinforced
%  composite plies
%
%%

Vm=1-Vf;

G12f = 0.5*ELf/(1+nu12f);

Gm = 0.5*ELm/(1+num);

rhoc = rhof*Vf + rhom*Vm;

kmT = 0.5*ELm/(1-num-2*num^2);

kfT = ELf*ETf/(2*ELf*(1-nu23f)-4*ETf*nu12f^2);

lambda1 = 2*(1/Gm+Vf/kmT+Vm/kfT)^(-1);

E1 = Vf*ELf + Vm*ELm + 2*lambda1*Vf*Vm*(num-nu12f)^2;

nu12 = Vf*nu12f + Vm*num + 0.5*lambda1*(num-nu12f)*(1/kfT-1/kmT)*Vf*Vm;

G12 = Gm + Vf/(1/(G12f-Gm)+0.5*Vm/Gm);

K23 = (kmT*(kfT+Gm)*Vm+kfT*(kmT+Gm)*Vf)/((kfT+Gm)*Vm+(kmT+Gm)*Vf);

lambda3 = 1 + 4*(K23*nu12^2)/E1;

G23 = Gm + Vf/(1/(0.5*ETf/(1+nu23f)-Gm)+Vm*(kmT+2*Gm)/(2*Gm*(kmT+Gm)));

E2 = 4*G23/(1+lambda3*G23/K23);

nu21=nu12*(E2/E1);

nu23=nu12*(1-nu21)/(1-nu12);

km = Gm/(1-2*num);

lambda = (0.5*(1/Gm+Vf/km+Vm/kfT))^(-1);

alpha1 = (ELf*alphaf*Vf+ELm*alpham*Vm)/(ELf*Vf+ELm*Vm);

alpha2 = -nu12*alpha1 + (alphaTf+nu12f*alphaLf)*Vf + (alpham+num*alpham)*Vm + 0.5*lambda*(1/kfT-1/km)*Vf*Vm*((alpham+num*alpham)-(alphaTf+nu23f*alphaLf));

return