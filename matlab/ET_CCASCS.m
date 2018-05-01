function[ET]=ET_CCASCS(VFf, Em, num, Ef1, Ef2, nuf12, nuf23)
%%
%==============================================================================
% Copyright (c) 2016-2017 Université de Lorraine & Luleå tekniska universitet
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
%
%%

VFm = 1 - VFf;
Gf23 = 0.5 * Ef2 / (1 + nuf23);
Gm = 0.5 * Em / (1 + num);
kmT = 0.5 * Em / (1 - num - 2 * num * num);
kfT = 0.5 * Ef1 * Ef2 / (Ef1 * (1 - nuf23) - 2 * Ef2 * nuf12 * nuf12);
lambda1 = 2 / (1 / Gm + VFf / kmT + VFm / kfT);
E1 = VFf * Ef1 + VFm * Em + 2 * lambda1 * VFf * VFm * (num - nuf12) * (num - nuf12);
nu12 = VFf * nuf12 + VFm * num + 0.5 * lambda1 * VFf * VFm * (num - nuf12) * (1 / kfT - 1 / kmT);
K23 = (VFm * kmT * (kfT + Gm) + VFf * kfT * (kmT + Gm)) / (VFm * (kfT + Gm) + VFf * (kmT + Gm));

etam = 3-4*num;
etaf = 3-4*nuf23;

A = 3*VFf*VFm*VFm*(Gf23/Gm-1)*(Gf23/Gm+etaf)+(etam*Gf23/Gm+etaf*etam-(etam*Gf23/Gm-etaf)*VFf*VFf*VFf)*(etam*VFf*(Gf23/Gm-1)-(etam*Gf23/Gm+1));
B = -6*VFf*VFm*VFm*(Gf23/Gm-1)*(Gf23/Gm+etaf)+(etam*Gf23/Gm+(Gf23/Gm-1)*VFf+1)*((etam-1)*(Gf23/Gm+etaf)-2*VFf*VFf*VFf*(etam*Gf23/Gm-etaf))+(etam+1)*VFf*(Gf23/Gm-1)*(Gf23/Gm+etaf+(etam*Gf23/Gm-etaf)*VFf*VFf*VFf);
D = 3*VFf*VFm*VFm*(Gf23/Gm-1)*(Gf23/Gm+etaf)+(etam*Gf23/Gm+(Gf23/Gm-1)*VFf+1)*(Gf23/Gm+etaf+(etam*Gf23/Gm-etaf)*VFf*VFf*VFf);
G23=Gm*(-B-sqrt(B*B-4*A*D))/(2*A)


ET = 1 / (0.25 / K23 + 0.25 / G23 + nu12 * nu12 / E1);
   
 return