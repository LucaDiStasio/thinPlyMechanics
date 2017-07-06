function[rhoc,E1,E2,nu12,nu21,G12,nu23,G23,alpha1,alpha2]=HalpinTsai(Vf,rhof,ELf,ETf,nuf,alphaf,rhom,ELm,ETm,num,alpham)
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
%  A function implementing the Halpin-Tsai method for fiber reinforced
%  composite plies
%
%%

Vm=1-Vf;

Gf = 0.5*ELf/(1+nuf);

Gm = 0.5*ELm/(1+num);

xi = 1;

rhoc = rhof*Vf + rhom*Vm;

E1 = ELf*Vf + ELm*Vm;

eta1 = (ETf/ETm-1)/(ETf/ETm+2*xi);

E2 = ETm*(1+2*xi*eta1*Vf)/(1-eta1*Vf);

nu12 = nuf*Vf + num*Vm;

eta2 = (Gf/Gm-1)/(Gf/Gm+xi);

G12 = Gm*(1+xi*eta2*Vf)/(1-eta2*Vf);

nu21=nu12*(E2/E1);

nu23=nu12*(1-nu21)/(1-nu12);

G23 = 0.5*E2/(1+nu23);

alpha1 = (ELf*alphaf*Vf+ELm*alpham*Vm)/(ELf*Vf+ELm*Vm);

alpha2 = (1+nuf)*alphaf*Vf + (1+num)*alpham*Vm - alpha1*nu12;

return