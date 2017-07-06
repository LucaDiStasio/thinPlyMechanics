#!/usr/local/bin/MathematicaScript -script

(* :Title: VirtualLab4CompositeTesting *)

(* :Author: Luca Di Stasio *)

(* :Summary:
	This script creates the front-end of the Virtual Laboratory for Fiber Composite Materials Testing.
*)

(* :Version: 1.0 *)

(* :Mathematica Version: 10.4 *)

(* :Copyright:
	2016 Université de Lorraine & Luleå tekniska universitet
	Author: Luca Di Stasio <luca.distasio@gmail.com>
	                        <luca.distasio@ingpec.eu>

	Redistribution and use in source and binary forms, with or without
	modification, are permitted provided that the following conditions are met:


	Redistributions of source code must retain the above copyright
	notice, this list of conditions and the following disclaimer.
	Redistributions in binary form must reproduce the above copyright
	notice, this list of conditions and the following disclaimer in
	the documentation and/or other materials provided with the distribution
	Neither the name of the Université de Lorraine or Luleå tekniska universitet
	nor the names of its contributors may be used to endorse or promote products
	derived from this software without specific prior written permission.

	THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
	AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
	IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
	ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
	LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
	CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
	SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
	INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
	CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
	ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
	POSSIBILITY OF SUCH DAMAGE.
	*)

(* :History:
	V. 1.0 July 2016, by Luca Di Stasio.
*)

(* :Keywords:
	fiber composites, composites mechanics, composite testing, virtual environment
*)

(* :Limitations:  *)

(* :Discussion:  *)

(* :=======================================================================:  *)
(* :=======================================================================:  *)
(* :=======================================================================:  *)

(* :Working Directory:  *)

wd = "C:\\01_backup-folder\\OneDrive\\01_Luca\\07_DocMASE\\05_Data";

(* :=======================================================================:  *)
(* :=======================================================================:  *)

(* :Packages:  *)

Needs["MATLink`"];

(* :=======================================================================:  *)
(* :=======================================================================:  *)

(* :Functions:  *)

(* :=======================================================================:  *)

(* :Element Quality Fields Control:  *)

quad4controls[] :=
 Column[{Control[{{minL, 0, "Minimum Edge Length"}, {0 -> "Hide",
      1 -> "Show"}}],
   Control[{{maxL, 0, "Maximum Edge Length"}, {0 -> "Hide",
      1 -> "Show"}}],
   Control[{{meanL, 0, "Mean Edge Length"}, {0 -> "Hide",
      1 -> "Show"}}],
   Control[{{minalpha, 0, "Minimum Internal Angle"}, {0 -> "Hide",
      1 -> "Show"}}],
   Control[{{maxalpha, 0, "Maximum Internal Angle"}, {0 -> "Hide",
      1 -> "Show"}}],
   Control[{{meanalpha, 0, "Mean Internal Angle"}, {0 -> "Hide",
      1 -> "Show"}}],
   Control[{{minD, 0, "Minimum Diagonal Length"}, {0 -> "Hide",
      1 -> "Show"}}],
   Control[{{maxD, 0, "Maximum Diagonal Length"}, {0 -> "Hide",
      1 -> "Show"}}],
   Control[{{meanD, 0, "Mean Diagonal Length"}, {0 -> "Hide",
      1 -> "Show"}}],
   Control[{{deltabeta, 0,
      "Diagonals' deviation from normality"}, {0 -> "Hide",
      1 -> "Show"}}],
   Control[{{A, 0, "Element Area"}, {0 -> "Hide", 1 -> "Show"}}],
   Control[{{ar, 0, "Aspect Ratio"}, {0 -> "Hide", 1 -> "Show"}}],
   Control[{{skew, 0, "Skew"}, {0 -> "Hide", 1 -> "Show"}}],
   Control[{{Tx, 0, "Taper along x"}, {0 -> "Hide", 1 -> "Show"}}],
   Control[{{Ty, 0, "Taper along y"}, {0 -> "Hide", 1 -> "Show"}}],
   Control[{{stretch, 0, "Stretch"}, {0 -> "Hide", 1 -> "Show"}}],
   Control[{{fshape, 0, "Shape Factor"}, {0 -> "Hide",
      1 -> "Show"}}]}, Spacings -> 1.5]

quad8controls[] :=
 Column[{Control[{{minL, 0, "Minimum Edge Length"}, {0 -> "Hide",
      1 -> "Show"}}],
   Control[{{maxL, 0, "Maximum Edge Length"}, {0 -> "Hide",
      1 -> "Show"}}],
   Control[{{meanL, 0, "Mean Edge Length"}, {0 -> "Hide",
      1 -> "Show"}}],
   Control[{{minalpha, 0, "Minimum Internal Angle"}, {0 -> "Hide",
      1 -> "Show"}}],
   Control[{{maxalpha, 0, "Maximum Internal Angle"}, {0 -> "Hide",
      1 -> "Show"}}],
   Control[{{meanalpha, 0, "Mean Internal Angle"}, {0 -> "Hide",
      1 -> "Show"}}],
   Control[{{minD, 0, "Minimum Diagonal Length"}, {0 -> "Hide",
      1 -> "Show"}}],
   Control[{{maxD, 0, "Maximum Diagonal Length"}, {0 -> "Hide",
      1 -> "Show"}}],
   Control[{{meanD, 0, "Mean Diagonal Length"}, {0 -> "Hide",
      1 -> "Show"}}],
   Control[{{deltabeta, 0,
      "Diagonals' deviation from normality"}, {0 -> "Hide",
      1 -> "Show"}}],
   Control[{{A, 0, "Area"}, {0 -> "Hide", 1 -> "Show"}}],
   Control[{{ar, 0, "Aspect Ratio"}, {0 -> "Hide", 1 -> "Show"}}],
   Control[{{skew, 0, "Skew"}, {0 -> "Hide", 1 -> "Show"}}],
   Control[{{Tx, 0, "Taper along x"}, {0 -> "Hide", 1 -> "Show"}}],
   Control[{{Ty, 0, "Taper along y"}, {0 -> "Hide", 1 -> "Show"}}],
   Control[{{TD, 0, "Tangential Deviation"}, {0 -> "Hide",
      1 -> "Show"}}],
   Control[{{TN, 0, "Normal Deviation"}, {0 -> "Hide",
      1 -> "Show"}}]}, Spacings -> 1.5]

tri3controls[] :=
 Column[{Control[{{minL, 0, "Minimum Edge Length"}, {0 -> "Hide",
      1 -> "Show"}}],
   Control[{{maxL, 0, "Maximum Edge Length"}, {0 -> "Hide",
      1 -> "Show"}}],
   Control[{{meanL, 0, "Mean Edge Length"}, {0 -> "Hide",
      1 -> "Show"}}],
   Control[{{minalpha, 0, "Minimum Internal Angle"}, {0 -> "Hide",
      1 -> "Show"}}],
   Control[{{maxalpha, 0, "Maximum Internal Angle"}, {0 -> "Hide",
      1 -> "Show"}}],
   Control[{{meanalpha, 0, "Mean Internal Angle"}, {0 -> "Hide",
      1 -> "Show"}}],
   Control[{{A, 0, "Area"}, {0 -> "Hide", 1 -> "Show"}}],
   Control[{{J, 0, "Jacobian"}, {0 -> "Hide", 1 -> "Show"}}],
   Control[{{JA, 0, "Jacobian/Area"}, {0 -> "Hide", 1 -> "Show"}}],
   Control[{{fshape, 0, "Shape Factor"}, {0 -> "Hide",
      1 -> "Show"}}]}, Spacings -> 1.5]

tri6controls[] :=
 Column[{Control[{{minL, 0, "Minimum Edge Length"}, {0 -> "Hide",
      1 -> "Show"}}],
   Control[{{maxL, 0, "Maximum Edge Length"}, {0 -> "Hide",
      1 -> "Show"}}],
   Control[{{meanL, 0, "Mean Edge Length"}, {0 -> "Hide",
      1 -> "Show"}}],
   Control[{{minalpha, 0, "Minimum Internal Angle"}, {0 -> "Hide",
      1 -> "Show"}}],
   Control[{{maxalpha, 0, "Maximum Internal Angle"}, {0 -> "Hide",
      1 -> "Show"}}],
   Control[{{meanalpha, 0, "Mean Internal Angle"}, {0 -> "Hide",
      1 -> "Show"}}],
   Control[{{A, 0, "Area"}, {0 -> "Hide", 1 -> "Show"}}],
   Control[{{J, 0, "Jacobian"}, {0 -> "Hide", 1 -> "Show"}}],
   Control[{{JA, 0, "Jacobian/Area"}, {0 -> "Hide", 1 -> "Show"}}],
   Control[{{fshape, 0, "Shape Factor"}, {0 -> "Hide", 1 -> "Show"}}],
    Control[{{TD, 0, "Tangential Deviation"}, {0 -> "Hide",
      1 -> "Show"}}],
   Control[{{TN, 0, "Normal Deviation"}, {0 -> "Hide",
      1 -> "Show"}}]}, Spacings -> 1.5]

assignQualityVar[minL_, maxL_, meanL_, minalpha_, maxalpha_,
  meanalpha_, minD_, maxD_, meanD_, deltabeta_, A_, ar_, skew_, Tx_,
  Ty_, stretch_, fshape_, TD_, TN_, J_, JA_] :=
 If[minL == 1, "minL", If[maxL == 1, "maxL", If[meanL == 1,
    "meanL",
    If[minalpha == 1, "minalpha",
     If[maxalpha == 1, "maxalpha",
      If[meanalpha == 1, "meanalpha",
       If[minD == 1, "minD",
        If[maxD == 1, "maxD",
         If[meanD == 1, "meanD",
          If[deltabeta == 1, "deltabeta",
           If[A == 1, "A",
            If[ar == 1, "ar",
             If[skew == 1, "skew",
              If[Tx == 1, "Tx",
               If[Ty == 1, "Ty",
                If[stretch == 1, "stretch",
                 If[fshape == 1, "fshape",
                  If[TD == 1, "TD",
                   If[TN == 1, "ND",
                    If[J == 1, "J",
                    If[JA == 1, "JA"]]]]]]]]]]]]]]]]]]]]]

assignQualityName[minL_, maxL_, meanL_, minalpha_, maxalpha_,
  meanalpha_, minD_, maxD_, meanD_, deltabeta_, A_, ar_, skew_, Tx_,
  Ty_, stretch_, fshape_, TD_, TN_, J_, JA_] :=
 If[minL == 1, "Minimum Edge Length",
  If[maxL == 1, "Maximum Edge Length", If[meanL == 1,
    "Mean Edge Length",
    If[minalpha == 1, "Minimum Internal Angle",
     If[maxalpha == 1, "Maximum Internal Angle",
      If[meanalpha == 1, "Mean Internal Angle",
       If[minD == 1, "Minimum Diagonal Length",
        If[maxD == 1, "Maximum Diagonal Length",
         If[meanD == 1, "Mean Diagonal Length",
          If[deltabeta == 1, "Diagonal Deviation from Normality",
           If[A == 1, "Element Area",
            If[ar == 1, "Aspect Ratio",

             If[skew == 1, "Skewness",
              If[Tx == 1, "Taper in x direction",
               If[Ty == 1, "Taper in y direction",
                If[stretch == 1, "Stretch",
                 If[fshape == 1, "Shape Factor",
                  If[TD == 1, "Tangential Deviation",
                   If[TN == 1, "Normal Deviation",
                    If[J == 1, "Jacobian",
                    If[JA == 1, "Jacobian/Area"]]]]]]]]]]]]]]]]]]]]]

(* :2D TPM Tests: Overall Interface:  *)

twoDthinplysection[] :=
 MenuView[{"Fiber/Matrix Interface Crack" ->
    MenuView[{"Inner Ply" ->
       MenuView[{"Select Number of Fibers" ->
          Text["Select Number of Fibers"],
         "1" -> thinplydebondinnermeshgenonefib[], "2" -> 2, "3" -> 3,
          "4 SP" -> 4, "4 CP" -> 4, "5" -> 5, "6 SP" -> 6,
         "6 CP" -> 6, "7" -> 7, "8" -> 8, "9 SP" -> 9, "9 CP" -> 9}],
      "Surface Ply" ->
       MenuView[{"Select Number of Fibers" ->
          Text["Select Number of Fibers"],
         "1" -> thinplydebondoutermeshgenonefib[], "2" -> 2, "3" -> 3,
          "4 SP" -> 4, "4 CP" -> 4, "5" -> 5, "6 SP" -> 6,
         "6 CP" -> 6, "7" -> 7, "8" -> 8, "9 SP" -> 9,
         "9 CP" -> 9}]}],
   "Matrix Bulk Crack" ->
    MenuView[{"Inner Ply" ->
       MenuView[{"Select Number of Fibers" ->
          Text["Select Number of Fibers"], "1" -> 1, "2" -> 2,
         "3" -> 3, "4 SP" -> 4, "4 CP" -> 4, "5" -> 5, "6 SP" -> 6,
         "6 CP" -> 6, "7" -> 7, "8" -> 8, "9 SP" -> 9, "9 CP" -> 9}],
      "Surface Ply" ->
       MenuView[{"Select Number of Fibers" ->
          Text["Select Number of Fibers"], "1" -> 1, "2" -> 2,
         "3" -> 3, "4 SP" -> 4, "4 CP" -> 4, "5" -> 5, "6 SP" -> 6,
         "6 CP" -> 6, "7" -> 7, "8" -> 8, "9 SP" -> 9,
         "9 CP" -> 9}]}]}]

(* :2D TPM Tests Geometry Plotting:  inner ply,  interface crack, one fiber (arrangement 1):  *)

plotSingleGeometry[Rf_, Vff_, theta_, dtheta_, a_, arrwidth1_,
  arrlength1_, arr1_, arr2_, ImgSize_] :=
 With[{l = 0.5*Rf*Sqrt[Pi/Vff]},
  Graphics[{Blue, Opacity[0.35],
    Annulus[{0, 0}, {Rf/3, 2*Rf/3}, {theta - dtheta, theta + dtheta}],
     Green, Opacity[0.35], Disk[{0, 0}, Rf/3, {0, theta}], Opacity[1],
     Black, Circle[{0, 0}, Rf], Line[{{-l, l}, {-l, -l}}],
    Line[{{l, -l}, {l, l}}],
    Line[{{0, 0}, {Rf*Cos[theta], Rf*Sin[theta]}}],
    Line[{{0, 0}, {Rf*Cos[theta - dtheta], Rf*Sin[theta - dtheta]}}],
    Line[{{0, 0}, {Rf*Cos[theta + dtheta], Rf*Sin[theta + dtheta]}}],
    Thickness[0.006], Line[{{-l, -l}, {l, -l}}],
    Line[{{l, l}, {-l, l}}], Red,
    Circle[{0, 0}, Rf, {theta - dtheta, theta + dtheta}],
    With[{r =
       0.5*Rf*Sqrt[(Cos[theta + dtheta] -
             Cos[theta - dtheta])^2 + (Sin[theta + dtheta] -
             Sin[theta - dtheta])^2]},
     With[{R = Sqrt[Rf^2 - r^2]},
      If[a == 0, Circle[{0, 0}, Rf, {theta - dtheta, theta + dtheta}],
        If[dtheta <= Pi/2,
        Rotate[
         Circle[{R*Cos[theta], R*Sin[theta]}, {r, (Rf - R + a)}, {0,
           Pi}], -(Pi/2 - theta), {R*Cos[theta], R*Sin[theta]}],
        Rotate[Circle[{0,
           0}, {0.5*Rf*
            Sqrt[(Cos[theta + 0.5*Pi] -
                 Cos[theta - 0.5*Pi])^2 + (Sin[theta + 0.5*Pi] -
                 Sin[theta - 0.5*Pi])^2], Rf + a}, {0,
           Pi}], -(Pi/2 - theta), {0, 0}]]]]],
    Text[Style["\[Theta]", 12, Black, Bold], {Rf*Cos[theta/2]/(3*1.5),
       Rf*Sin[theta/2]/(3*1.5)}],
    Text[Style["\[CapitalDelta]\[Theta]", 12, Black,
      Bold], {2*Rf*Cos[theta - dtheta/2]/(3*1.25),
      2*Rf*Sin[theta - dtheta/2]/(3*1.25)}],
    Text[Style["\[CapitalDelta]\[Theta]", 12, Black,
      Bold], {2*Rf*Cos[theta + dtheta/2]/(3*1.25),
      2*Rf*Sin[theta + dtheta/2]/(3*1.25)}],
    Text[Style[Subscript[R, f], 12, Black,
      Bold], {3*Rf*Cos[1.1*theta]/(3*1.25),
      3*Rf*Sin[1.1*theta]/(3*1.25)}],
    Text[Style[Subscript[\[CapitalOmega], m], 12, Black,
      Bold], {1.075*Rf*Cos[220 Degree], 1.075*Rf*Sin[220 Degree]}],
    Text[Style[Subscript[\[CapitalOmega], f], 12, Black,
      Bold], {0.75*Rf*Cos[205 Degree], 0.75*Rf*Sin[205 Degree]}],
    Text[Style[Subscript[\[CapitalGamma], 1], 12, Black,
      Bold], {1.075*Rf*Cos[255 Degree], 1.075*Rf*Sin[255 Degree]}],
    Text[Style[Subscript[\[CapitalGamma], 2], 12, Black,
      Bold], {0.95*Rf*Cos[theta - dtheta/2],
      0.95*Rf*Sin[theta - dtheta/2]}],
    Text[Style[Subscript[\[CapitalGamma], 3], 12, Black,
      Bold], {(1.075*Rf + a)*Cos[theta + dtheta/2], (1.075*Rf + a)*
       Sin[theta + dtheta/2]}],
    Text[Style["O", 12, Black, Bold], {-0.05, -0.05}],
    Text[Style["l", 12, Black, Bold], {-0.5*l, 0.95*l}],
    Text[Style["l", 12, Black, Bold], {0.5*l, 0.95*l}],
    Text[Style["l", 12, Black, Bold], {-0.95*l, 0.5*l}],
    Text[Style["l", 12, Black, Bold], {-0.95*l, -0.5*l}], Black, Thin,
     Table[{Arrow[{{-l, -l + i}, {-l - arrlength1*l, -l + i}}],
      Arrow[{{l, -l + i}, {l + arrlength1*l, -l + i}}]}, {i, 0, 2*l,
      2*l/(arr1 - 1)}],
    Table[{Arrow[{{0 + i/arrwidth1 - arrwidth1*l/arr2, l + i}, {l,
         l + i}}],
      Arrow[{{0 - i/arrwidth1 + arrwidth1*l/arr2, l + i}, {-l,
         l + i}}],
      Arrow[{{0 + i/arrwidth1 - arrwidth1*l/arr2, -l - i}, {l, -l -
          i}}], Arrow[{{0 - i/arrwidth1 + arrwidth1*l/arr2, -l -
          i}, {-l, -l - i}}]}, {i, arrwidth1*l/arr2, arrwidth1*l,
      arrwidth1*l/arr2}], Thickness[0.00001],
    Line[{{-l - arrlength1*l, -l}, {-l - arrlength1*l, l}}],
    Line[{{+l + arrlength1*l, -l}, {+l + arrlength1*l, l}}],
    Line[{{l, l}, {l, (1 + arrwidth1)*l}}],
    Line[{{-l, l}, {-l, (1 + arrwidth1)*l}}],
    Line[{{l, -l}, {l, -(1 + arrwidth1)*l}}],
    Line[{{-l, -l}, {-l, -(1 + arrwidth1)*l}}]}, Axes -> True,
   AxesLabel -> {x, z}, AspectRatio -> 1, ImageSize -> ImgSize]]

plotSingleSymmGeometry[Rf_, Vff_, theta_, dtheta_, a_, arrwidth1_,
  arrlength1_, arr1_, arr2_, ImgSize_] :=
 With[{l = 0.5*Rf*Sqrt[Pi/Vff]},
  Graphics[{Blue, Opacity[0.35],
    Annulus[{0, 0}, {Rf/3, 2*Rf/3}, {theta - dtheta, theta + dtheta}],
     Green, Opacity[0.35], Disk[{0, 0}, Rf/3, {0, theta}], Opacity[1],
     Black, Circle[{0, 0}, Rf], Line[{{-l, l}, {-l, -l}}],
    Line[{{l, -l}, {l, l}}],
    Line[{{0, 0}, {Rf*Cos[theta], Rf*Sin[theta]}}],
    Line[{{0, 0}, {Rf*Cos[theta - dtheta], Rf*Sin[theta - dtheta]}}],
    Line[{{0, 0}, {Rf*Cos[theta + dtheta], Rf*Sin[theta + dtheta]}}],
    Thickness[0.006], Line[{{l, l}, {-l, l}}], Red,
    Circle[{0, 0}, Rf, {theta - dtheta, theta + dtheta}],
    With[{r =
       0.5*Rf*Sqrt[(Cos[theta + dtheta] -
             Cos[theta - dtheta])^2 + (Sin[theta + dtheta] -
             Sin[theta - dtheta])^2]},
     With[{R = Sqrt[Rf^2 - r^2]},
      If[a == 0, Circle[{0, 0}, Rf, {theta - dtheta, theta + dtheta}],
        If[dtheta <= Pi/2,
        Rotate[Circle[{R*Cos[theta],
           R*Sin[theta]}, {r, (Rf - R + a)}, {0,
           Pi}], -(Pi/2 - theta), {R*Cos[theta], R*Sin[theta]}],
        Rotate[Circle[{0,
           0}, {0.5*Rf*
            Sqrt[(Cos[theta + 0.5*Pi] -
                 Cos[theta - 0.5*Pi])^2 + (Sin[theta + 0.5*Pi] -
                 Sin[theta - 0.5*Pi])^2], Rf + a}, {0,
           Pi}], -(Pi/2 - theta), {0, 0}]]]]],
    Text[Style["\[Theta]", 12, Black, Bold], {Rf*Cos[theta/2]/(3*1.5),
       Rf*Sin[theta/2]/(3*1.5)}],
    Text[Style["\[CapitalDelta]\[Theta]", 12, Black,
      Bold], {2*Rf*Cos[theta - dtheta/2]/(3*1.25),
      2*Rf*Sin[theta - dtheta/2]/(3*1.25)}],
    Text[Style["\[CapitalDelta]\[Theta]", 12, Black,
      Bold], {2*Rf*Cos[theta + dtheta/2]/(3*1.25),
      2*Rf*Sin[theta + dtheta/2]/(3*1.25)}],
    Text[Style[Subscript[R, f], 12, Black,
      Bold], {3*Rf*Cos[1.1*theta]/(3*1.25),
      3*Rf*Sin[1.1*theta]/(3*1.25)}],
    Text[Style[Subscript[\[CapitalOmega], m], 12, Black,
      Bold], {1.075*Rf*Cos[220 Degree], 1.075*Rf*Sin[220 Degree]}],
    Text[Style[Subscript[\[CapitalOmega], f], 12, Black,
      Bold], {0.75*Rf*Cos[205 Degree], 0.75*Rf*Sin[205 Degree]}],
    Text[Style[Subscript[\[CapitalGamma], 1], 12, Black,
      Bold], {1.075*Rf*Cos[255 Degree], 1.075*Rf*Sin[255 Degree]}],
    Text[Style[Subscript[\[CapitalGamma], 2], 12, Black,
      Bold], {0.95*Rf*Cos[theta - dtheta/2],
      0.95*Rf*Sin[theta - dtheta/2]}],
    Text[Style[Subscript[\[CapitalGamma], 3], 12, Black,
      Bold], {(1.075*Rf + a)*Cos[theta + dtheta/2], (1.075*Rf + a)*
       Sin[theta + dtheta/2]}],
    Text[Style["O", 12, Black, Bold], {-0.05, -0.05}],
    Text[Style["l", 12, Black, Bold], {-0.5*l, 0.95*l}],
    Text[Style["l", 12, Black, Bold], {0.5*l, 0.95*l}],
    Text[Style["l", 12, Black, Bold], {-0.95*l, 0.5*l}],
    Text[Style["l", 12, Black, Bold], {-0.95*l, -0.5*l}], Black, Thin,
     Table[{Arrow[{{-l, -l + i}, {-l - arrlength1*l, -l + i}}],
      Arrow[{{l, -l + i}, {l + arrlength1*l, -l + i}}]}, {i, 0, 2*l,
      2*l/(arr1 - 1)}],
    Table[{Arrow[{{0 + i/arrwidth1 - arrwidth1*l/arr2, l + i}, {l,
         l + i}}],
      Arrow[{{0 - i/arrwidth1 + arrwidth1*l/arr2, l + i}, {-l,
         l + i}}]}, {i, arrwidth1*l/arr2, arrwidth1*l,
      arrwidth1*l/arr2}], Thickness[0.00001],
    Line[{{-l - arrlength1*l, -l}, {-l - arrlength1*l, l}}],
    Line[{{+l + arrlength1*l, -l}, {+l + arrlength1*l, l}}],
    Line[{{l, l}, {l, (1 + arrwidth1)*l}}],
    Line[{{-l, l}, {-l, (1 + arrwidth1)*l}}], DotDashed, Blue,
    Thickness[0.006],
    Line[{{-(1 + 1.5*arrwidth1)*l, -l}, {(1 + 1.5*arrwidth1)*
        l, -l}}]}, Axes -> True, AxesLabel -> {x, z},
   AspectRatio -> 1, ImageSize -> ImgSize]]

plotSingleCohesiveGeometry[Rf_, Vff_, theta_, dtheta_, a_, arrwidth1_,
   arrlength1_, arr1_, arr2_, ImgSize_] :=
 With[{l = 0.5*Rf*Sqrt[Pi/Vff]},
  Graphics[{Opacity[1], Black, Circle[{0, 0}, Rf],
    Line[{{-l, l}, {-l, -l}}], Line[{{l, -l}, {l, l}}],
    Line[{{0, 0}, {Rf*Cos[theta], Rf*Sin[theta]}}],  Thickness[0.006],
     Line[{{-l, -l}, {l, -l}}], Line[{{l, l}, {-l, l}}],
    Thickness[0.005], Green, Circle[{0, 0}, Rf, {0, 2*Pi}],
    With[{r =
       0.5*Rf*Sqrt[(Cos[theta + dtheta] -
             Cos[theta - dtheta])^2 + (Sin[theta + dtheta] -
             Sin[theta - dtheta])^2]},
     With[{R = Sqrt[Rf^2 - r^2]},
      If[a == 0, Circle[{0, 0}, Rf, {theta - dtheta, theta + dtheta}],
        If[dtheta <= Pi/2,
        Rotate[Circle[{R*Cos[theta],
           R*Sin[theta]}, {r, (Rf - R + a)}, {0,
           Pi}], -(Pi/2 - theta), {R*Cos[theta], R*Sin[theta]}],
        Rotate[Circle[{0,
           0}, {0.5*Rf*
            Sqrt[(Cos[theta + 0.5*Pi] -
                 Cos[theta - 0.5*Pi])^2 + (Sin[theta + 0.5*Pi] -
                 Sin[theta - 0.5*Pi])^2], Rf + a}, {0,
           Pi}], -(Pi/2 - theta), {0, 0}]]]]],
    Text[Style[Subscript[R, f], 12, Black,
      Bold], {3*Rf*Cos[1.1*theta]/(3*1.25),
      3*Rf*Sin[1.1*theta]/(3*1.25)}],
    Text[Style[Subscript[\[CapitalOmega], m], 12, Black,
      Bold], {1.075*Rf*Cos[220 Degree], 1.075*Rf*Sin[220 Degree]}],
    Text[Style[Subscript[\[CapitalOmega], f], 12, Black,
      Bold], {0.75*Rf*Cos[205 Degree], 0.75*Rf*Sin[205 Degree]}],
    Text[Style["O", 12, Black, Bold], {-0.05, -0.05}],
    Text[Style["l", 12, Black, Bold], {-0.5*l, 0.95*l}],
    Text[Style["l", 12, Black, Bold], {0.5*l, 0.95*l}],
    Text[Style["l", 12, Black, Bold], {-0.95*l, 0.5*l}],
    Text[Style["l", 12, Black, Bold], {-0.95*l, -0.5*l}], Black, Thin,
     Table[{Arrow[{{-l, -l + i}, {-l - arrlength1*l, -l + i}}],
      Arrow[{{l, -l + i}, {l + arrlength1*l, -l + i}}]}, {i, 0, 2*l,
      2*l/(arr1 - 1)}],
    Table[{Arrow[{{0 + i/arrwidth1 - arrwidth1*l/arr2, l + i}, {l,
         l + i}}],
      Arrow[{{0 - i/arrwidth1 + arrwidth1*l/arr2, l + i}, {-l,
         l + i}}],
      Arrow[{{0 + i/arrwidth1 - arrwidth1*l/arr2, -l - i}, {l, -l -
          i}}], Arrow[{{0 - i/arrwidth1 + arrwidth1*l/arr2, -l -
          i}, {-l, -l - i}}]}, {i, arrwidth1*l/arr2, arrwidth1*l,
      arrwidth1*l/arr2}], Thickness[0.00001],
    Line[{{-l - arrlength1*l, -l}, {-l - arrlength1*l, l}}],
    Line[{{+l + arrlength1*l, -l}, {+l + arrlength1*l, l}}],
    Line[{{l, l}, {l, (1 + arrwidth1)*l}}],
    Line[{{-l, l}, {-l, (1 + arrwidth1)*l}}],
    Line[{{l, -l}, {l, -(1 + arrwidth1)*l}}],
    Line[{{-l, -l}, {-l, -(1 + arrwidth1)*l}}]}, Axes -> True,
   AxesLabel -> {x, z}, AspectRatio -> 1, ImageSize -> ImgSize]]

plotSingleCohesiveSymmGeometry[Rf_, Vff_, theta_, dtheta_, a_,
  arrwidth1_, arrlength1_, arr1_, arr2_, ImgSize_] :=
 With[{l = 0.5*Rf*Sqrt[Pi/Vff]},
  Graphics[{Opacity[1], Black, Circle[{0, 0}, Rf],
    Line[{{-l, l}, {-l, -l}}], Line[{{l, -l}, {l, l}}],
    Line[{{0, 0}, {Rf*Cos[theta], Rf*Sin[theta]}}],  Thickness[0.006],
     Line[{{l, l}, {-l, l}}], Thickness[0.005], Green,
    Circle[{0, 0}, Rf, {0, 2*Pi}],
    With[{r =
       0.5*Rf*Sqrt[(Cos[theta + dtheta] -
             Cos[theta - dtheta])^2 + (Sin[theta + dtheta] -
             Sin[theta - dtheta])^2]},
     With[{R = Sqrt[Rf^2 - r^2]},
      If[a == 0, Circle[{0, 0}, Rf, {theta - dtheta, theta + dtheta}],
        If[dtheta <= Pi/2,
        Rotate[Circle[{R*Cos[theta],
           R*Sin[theta]}, {r, (Rf - R + a)}, {0,
           Pi}], -(Pi/2 - theta), {R*Cos[theta], R*Sin[theta]}],
        Rotate[Circle[{0,
           0}, {0.5*Rf*
            Sqrt[(Cos[theta + 0.5*Pi] -
                 Cos[theta - 0.5*Pi])^2 + (Sin[theta + 0.5*Pi] -
                 Sin[theta - 0.5*Pi])^2], Rf + a}, {0,
           Pi}], -(Pi/2 - theta), {0, 0}]]]]],
    Text[Style[Subscript[R, f], 12, Black,
      Bold], {3*Rf*Cos[1.1*theta]/(3*1.25),
      3*Rf*Sin[1.1*theta]/(3*1.25)}],
    Text[Style[Subscript[\[CapitalOmega], m], 12, Black,
      Bold], {1.075*Rf*Cos[220 Degree], 1.075*Rf*Sin[220 Degree]}],
    Text[Style[Subscript[\[CapitalOmega], f], 12, Black,
      Bold], {0.75*Rf*Cos[205 Degree], 0.75*Rf*Sin[205 Degree]}],
    Text[Style["O", 12, Black, Bold], {-0.05, -0.05}],
    Text[Style["l", 12, Black, Bold], {-0.5*l, 0.95*l}],
    Text[Style["l", 12, Black, Bold], {0.5*l, 0.95*l}],
    Text[Style["l", 12, Black, Bold], {-0.95*l, 0.5*l}],
    Text[Style["l", 12, Black, Bold], {-0.95*l, -0.5*l}], Black, Thin,
     Table[{Arrow[{{-l, -l + i}, {-l - arrlength1*l, -l + i}}],
      Arrow[{{l, -l + i}, {l + arrlength1*l, -l + i}}]}, {i, 0, 2*l,
      2*l/(arr1 - 1)}],
    Table[{Arrow[{{0 + i/arrwidth1 - arrwidth1*l/arr2, l + i}, {l,
         l + i}}],
      Arrow[{{0 - i/arrwidth1 + arrwidth1*l/arr2, l + i}, {-l,
         l + i}}]}, {i, arrwidth1*l/arr2, arrwidth1*l,
      arrwidth1*l/arr2}], Thickness[0.00001],
    Line[{{-l - arrlength1*l, -l}, {-l - arrlength1*l, l}}],
    Line[{{+l + arrlength1*l, -l}, {+l + arrlength1*l, l}}],
    Line[{{l, l}, {l, (1 + arrwidth1)*l}}],
    Line[{{-l, l}, {-l, (1 + arrwidth1)*l}}], DotDashed, Blue,
    Thickness[0.006],
    Line[{{-(1 + 1.5*arrwidth1)*l, -l}, {(1 + 1.5*arrwidth1)*
        l, -l}}]}, Axes -> True, AxesLabel -> {x, z},
   AspectRatio -> 1, ImageSize -> ImgSize]]

plotBoundedGeometry[Rf_, Vff_, tratio_, theta_, dtheta_, a_,
  arrwidth1_, arrlength1_, arr1_, arr2_, ImgSize_] :=
 With[{l = 0.5*Rf*Sqrt[Pi/Vff]},
  Graphics[{Blue, Opacity[0.35],
    Annulus[{0, 0}, {Rf/3, 2*Rf/3}, {theta - dtheta, theta + dtheta}],
     Green, Opacity[0.35], Disk[{0, 0}, Rf/3, {0, theta}], Opacity[1],
     Black, Circle[{0, 0}, Rf], Line[{{-l, l}, {-l, -l}}],
    Line[{{l, -l}, {l, l}}],
    Line[{{0, 0}, {Rf*Cos[theta], Rf*Sin[theta]}}],
    Line[{{0, 0}, {Rf*Cos[theta - dtheta], Rf*Sin[theta - dtheta]}}],
    Line[{{0, 0}, {Rf*Cos[theta + dtheta], Rf*Sin[theta + dtheta]}}],
    Line[{{-l, -l}, {l, -l}}], Line[{{l, l}, {-l, l}}], Red,
    Circle[{0, 0}, Rf, {theta - dtheta, theta + dtheta}],
    With[{r =
       0.5*Rf*Sqrt[(Cos[theta + dtheta] -
             Cos[theta - dtheta])^2 + (Sin[theta + dtheta] -
             Sin[theta - dtheta])^2]},
     With[{R = Sqrt[Rf^2 - r^2]},
      If[a == 0, Circle[{0, 0}, Rf, {theta - dtheta, theta + dtheta}],
        If[dtheta <= Pi/2,
        Rotate[Circle[{R*Cos[theta],
           R*Sin[theta]}, {r, (Rf - R + a)}, {0,
           Pi}], -(Pi/2 - theta), {R*Cos[theta], R*Sin[theta]}],
        Rotate[Circle[{0,
           0}, {0.5*Rf*
            Sqrt[(Cos[theta + 0.5*Pi] -
                 Cos[theta - 0.5*Pi])^2 + (Sin[theta + 0.5*Pi] -
                 Sin[theta - 0.5*Pi])^2], Rf + a}, {0,
           Pi}], -(Pi/2 - theta), {0, 0}]]]]],
    Text[Style["\[Theta]", 12, Black, Bold], {Rf*Cos[theta/2]/(3*1.5),
       Rf*Sin[theta/2]/(3*1.5)}],
    Text[Style["\[CapitalDelta]\[Theta]", 12, Black,
      Bold], {2*Rf*Cos[theta - dtheta/2]/(3*1.25),
      2*Rf*Sin[theta - dtheta/2]/(3*1.25)}],
    Text[Style["\[CapitalDelta]\[Theta]", 12, Black,
      Bold], {2*Rf*Cos[theta + dtheta/2]/(3*1.25),
      2*Rf*Sin[theta + dtheta/2]/(3*1.25)}],
    Text[Style[Subscript[R, f], 12, Black,
      Bold], {3*Rf*Cos[1.1*theta]/(3*1.25),
      3*Rf*Sin[1.1*theta]/(3*1.25)}],
    Text[Style[Subscript[\[CapitalOmega], m], 12, Black,
      Bold], {1.075*Rf*Cos[220 Degree], 1.075*Rf*Sin[220 Degree]}],
    Text[Style[Subscript[\[CapitalOmega], f], 12, Black,
      Bold], {0.75*Rf*Cos[205 Degree], 0.75*Rf*Sin[205 Degree]}],
    Text[Style[Subscript[\[CapitalGamma], 1], 12, Black,
      Bold], {1.075*Rf*Cos[255 Degree], 1.075*Rf*Sin[255 Degree]}],
    Text[Style[Subscript[\[CapitalGamma], 2], 12, Black,
      Bold], {0.95*Rf*Cos[theta - dtheta/2],
      0.95*Rf*Sin[theta - dtheta/2]}],
    Text[Style[Subscript[\[CapitalGamma], 3], 12, Black,
      Bold], {(1.075*Rf + a)*Cos[theta + dtheta/2], (1.075*Rf + a)*
       Sin[theta + dtheta/2]}],
    Text[Style["O", 12, Black, Bold], {-0.05, -0.05}],
    Text[Style["l", 12, Black, Bold], {-0.5*l, 0.95*l}],
    Text[Style["l", 12, Black, Bold], {0.5*l, 0.95*l}],
    Text[Style["l", 12, Black, Bold], {-0.95*l, 0.5*l}],
    Text[Style["l", 12, Black, Bold], {-0.95*l, -0.5*l}],
    Text[Style[Subscript[\[CapitalOmega], "u,[0\[Degree]]"], 12,
      Black, Bold], {0.5*l, l + 0.5*tratio*l}],
    Text[Style[Subscript[\[CapitalOmega], "b,[0\[Degree]]"], 12,
      Black, Bold], {-0.5*l, -l - 0.5*tratio*l}], Black, Thin,
    Table[{Arrow[{{-l, -l - tratio*l + i}, {-l - arrlength1*l, -l -
          tratio*l + i}}],
      Arrow[{{l, -l - tratio*l + i}, {l + arrlength1*l, -l -
          tratio*l + i}}]}, {i, 0, 2*(l + tratio*l),
      2*(l + tratio*l)/(arr1 - 1)}], Thickness[0.00001],
    Line[{{-l - arrlength1*l, -(l + tratio*l)}, {-l -
        arrlength1*l, (l + tratio*l)}}],
    Line[{{+l + arrlength1*l, -(l + tratio*l)}, {+l +
        arrlength1*l, (l + tratio*l)}}],
    Line[{{-l, l}, {-l, l + tratio*l}, {l, l + tratio*l}, {l, l}}],
    Line[{{-l, -l}, {-l, -l - tratio*l}, {l, -l -
        tratio*l}, {l, -l}}]}, Axes -> True, AxesLabel -> {x, z},
   AspectRatio -> 1, ImageSize -> ImgSize]]

plotBoundedSymmGeometry[Rf_, Vff_, tratio_, theta_, dtheta_, a_,
  arrwidth1_, arrlength1_, arr1_, arr2_, ImgSize_] :=
 With[{l = 0.5*Rf*Sqrt[Pi/Vff]},
  Graphics[{Blue, Opacity[0.35],
    Annulus[{0, 0}, {Rf/3, 2*Rf/3}, {theta - dtheta, theta + dtheta}],
     Green, Opacity[0.35], Disk[{0, 0}, Rf/3, {0, theta}], Opacity[1],
     Black, Circle[{0, 0}, Rf], Line[{{-l, l}, {-l, -l}}],
    Line[{{l, -l}, {l, l}}],
    Line[{{0, 0}, {Rf*Cos[theta], Rf*Sin[theta]}}],
    Line[{{0, 0}, {Rf*Cos[theta - dtheta], Rf*Sin[theta - dtheta]}}],
    Line[{{0, 0}, {Rf*Cos[theta + dtheta], Rf*Sin[theta + dtheta]}}],
    Line[{{-l, -l}, {l, -l}}], Line[{{l, l}, {-l, l}}], Red,
    Circle[{0, 0}, Rf, {theta - dtheta, theta + dtheta}],
    With[{r =
       0.5*Rf*Sqrt[(Cos[theta + dtheta] -
             Cos[theta - dtheta])^2 + (Sin[theta + dtheta] -
             Sin[theta - dtheta])^2]},
     With[{R = Sqrt[Rf^2 - r^2]},
      If[a == 0, Circle[{0, 0}, Rf, {theta - dtheta, theta + dtheta}],
        If[dtheta <= Pi/2,
        Rotate[Circle[{R*Cos[theta],
           R*Sin[theta]}, {r, (Rf - R + a)}, {0,
           Pi}], -(Pi/2 - theta), {R*Cos[theta], R*Sin[theta]}],
        Rotate[Circle[{0,
           0}, {0.5*Rf*
            Sqrt[(Cos[theta + 0.5*Pi] -
                 Cos[theta - 0.5*Pi])^2 + (Sin[theta + 0.5*Pi] -
                 Sin[theta - 0.5*Pi])^2], Rf + a}, {0,
           Pi}], -(Pi/2 - theta), {0, 0}]]]]],
    Text[Style["\[Theta]", 12, Black, Bold], {Rf*Cos[theta/2]/(3*1.5),
       Rf*Sin[theta/2]/(3*1.5)}],
    Text[Style["\[CapitalDelta]\[Theta]", 12, Black,
      Bold], {2*Rf*Cos[theta - dtheta/2]/(3*1.25),
      2*Rf*Sin[theta - dtheta/2]/(3*1.25)}],
    Text[Style["\[CapitalDelta]\[Theta]", 12, Black,
      Bold], {2*Rf*Cos[theta + dtheta/2]/(3*1.25),
      2*Rf*Sin[theta + dtheta/2]/(3*1.25)}],
    Text[Style[Subscript[R, f], 12, Black,
      Bold], {3*Rf*Cos[1.1*theta]/(3*1.25),
      3*Rf*Sin[1.1*theta]/(3*1.25)}],
    Text[Style[Subscript[\[CapitalOmega], m], 12, Black,
      Bold], {1.075*Rf*Cos[220 Degree], 1.075*Rf*Sin[220 Degree]}],
    Text[Style[Subscript[\[CapitalOmega], f], 12, Black,
      Bold], {0.75*Rf*Cos[205 Degree], 0.75*Rf*Sin[205 Degree]}],
    Text[Style[Subscript[\[CapitalGamma], 1], 12, Black,
      Bold], {1.075*Rf*Cos[255 Degree], 1.075*Rf*Sin[255 Degree]}],
    Text[Style[Subscript[\[CapitalGamma], 2], 12, Black,
      Bold], {0.95*Rf*Cos[theta - dtheta/2],
      0.95*Rf*Sin[theta - dtheta/2]}],
    Text[Style[Subscript[\[CapitalGamma], 3], 12, Black,
      Bold], {(1.075*Rf + a)*Cos[theta + dtheta/2], (1.075*Rf + a)*
       Sin[theta + dtheta/2]}],
    Text[Style["O", 12, Black, Bold], {-0.05, -0.05}],
    Text[Style["l", 12, Black, Bold], {-0.5*l, 0.95*l}],
    Text[Style["l", 12, Black, Bold], {0.5*l, 0.95*l}],
    Text[Style["l", 12, Black, Bold], {-0.95*l, 0.5*l}],
    Text[Style["l", 12, Black, Bold], {-0.95*l, -0.5*l}],
    Text[Style[Subscript[\[CapitalOmega], "u,[0\[Degree]]"], 12,
      Black, Bold], {0.5*l, l + 0.5*tratio*l}], Black, Thin,
    Table[{Arrow[{{-l, -l + i}, {-l - arrlength1*l, -l + i}}],
      Arrow[{{l, -l + i}, {l + arrlength1*l, -l + i}}]}, {i,
      0, (2*l + tratio*l), (2*l + tratio*l)/(arr1 - 1)}],
    Thickness[0.00001],
    Line[{{-l - arrlength1*l, -l}, {-l -
        arrlength1*l, (l + tratio*l)}}],
    Line[{{+l + arrlength1*l, -l}, {+l +
        arrlength1*l, (l + tratio*l)}}],
    Line[{{-l, l}, {-l, l + tratio*l}, {l, l + tratio*l}, {l, l}}],
    DotDashed, Blue, Thickness[0.006],
    Line[{{-(1 + 1.5*arrwidth1)*l, -l}, {(1 + 1.5*arrwidth1)*
        l, -l}}]}, Axes -> True, AxesLabel -> {x, z},
   AspectRatio -> 1, ImageSize -> ImgSize]]

plotOneSideBoundedGeometry[Rf_, Vff_, tratio_, theta_, dtheta_, a_,
  arrwidth1_, arrlength1_, arr1_, arr2_, ImgSize_] :=
 With[{l = 0.5*Rf*Sqrt[Pi/Vff]},
  Graphics[{Blue, Opacity[0.35],
    Annulus[{0, 0}, {Rf/3, 2*Rf/3}, {theta - dtheta, theta + dtheta}],
     Green, Opacity[0.35], Disk[{0, 0}, Rf/3, {0, theta}], Opacity[1],
     Black, Circle[{0, 0}, Rf], Line[{{-l, l}, {-l, -l}}],
    Line[{{l, -l}, {l, l}}],
    Line[{{0, 0}, {Rf*Cos[theta], Rf*Sin[theta]}}],
    Line[{{0, 0}, {Rf*Cos[theta - dtheta], Rf*Sin[theta - dtheta]}}],
    Line[{{0, 0}, {Rf*Cos[theta + dtheta], Rf*Sin[theta + dtheta]}}],
    Line[{{-l, -l}, {l, -l}}], Line[{{l, l}, {-l, l}}], Red,
    Circle[{0, 0}, Rf, {theta - dtheta, theta + dtheta}],
    With[{r =
       0.5*Rf*Sqrt[(Cos[theta + dtheta] -
             Cos[theta - dtheta])^2 + (Sin[theta + dtheta] -
             Sin[theta - dtheta])^2]},
     With[{R = Sqrt[Rf^2 - r^2]},
      If[a == 0, Circle[{0, 0}, Rf, {theta - dtheta, theta + dtheta}],
        If[dtheta <= Pi/2,
        Rotate[Circle[{R*Cos[theta],
           R*Sin[theta]}, {r, (Rf - R + a)}, {0,
           Pi}], -(Pi/2 - theta), {R*Cos[theta], R*Sin[theta]}],
        Rotate[Circle[{0,
           0}, {0.5*Rf*
            Sqrt[(Cos[theta + 0.5*Pi] -
                 Cos[theta - 0.5*Pi])^2 + (Sin[theta + 0.5*Pi] -
                 Sin[theta - 0.5*Pi])^2], Rf + a}, {0,
           Pi}], -(Pi/2 - theta), {0, 0}]]]]],
    Text[Style["\[Theta]", 12, Black, Bold], {Rf*Cos[theta/2]/(3*1.5),
       Rf*Sin[theta/2]/(3*1.5)}],
    Text[Style["\[CapitalDelta]\[Theta]", 12, Black,
      Bold], {2*Rf*Cos[theta - dtheta/2]/(3*1.25),
      2*Rf*Sin[theta - dtheta/2]/(3*1.25)}],
    Text[Style["\[CapitalDelta]\[Theta]", 12, Black,
      Bold], {2*Rf*Cos[theta + dtheta/2]/(3*1.25),
      2*Rf*Sin[theta + dtheta/2]/(3*1.25)}],
    Text[Style[Subscript[R, f], 12, Black,
      Bold], {3*Rf*Cos[1.1*theta]/(3*1.25),
      3*Rf*Sin[1.1*theta]/(3*1.25)}],
    Text[Style[Subscript[\[CapitalOmega], m], 12, Black,
      Bold], {1.075*Rf*Cos[220 Degree], 1.075*Rf*Sin[220 Degree]}],
    Text[Style[Subscript[\[CapitalOmega], f], 12, Black,
      Bold], {0.75*Rf*Cos[205 Degree], 0.75*Rf*Sin[205 Degree]}],
    Text[Style[Subscript[\[CapitalGamma], 1], 12, Black,
      Bold], {1.075*Rf*Cos[255 Degree], 1.075*Rf*Sin[255 Degree]}],
    Text[Style[Subscript[\[CapitalGamma], 2], 12, Black,
      Bold], {0.95*Rf*Cos[theta - dtheta/2],
      0.95*Rf*Sin[theta - dtheta/2]}],
    Text[Style[Subscript[\[CapitalGamma], 3], 12, Black,
      Bold], {(1.075*Rf + a)*Cos[theta + dtheta/2], (1.075*Rf + a)*
       Sin[theta + dtheta/2]}],
    Text[Style["O", 12, Black, Bold], {-0.05, -0.05}],
    Text[Style["l", 12, Black, Bold], {-0.5*l, 0.95*l}],
    Text[Style["l", 12, Black, Bold], {0.5*l, 0.95*l}],
    Text[Style["l", 12, Black, Bold], {-0.95*l, 0.5*l}],
    Text[Style["l", 12, Black, Bold], {-0.95*l, -0.5*l}],
    Text[Style[Subscript[\[CapitalOmega], "u,[0\[Degree]]"], 12,
      Black, Bold], {0.5*l, l + 0.5*tratio*l}],
    Text[Style[Subscript[\[CapitalOmega], "b,[0\[Degree]]"], 12,
      Black, Bold], {-0.5*l, -l - 0.5*tratio*l}], Black, Thin,
    Table[{Arrow[{{-l, -l - tratio*l + i}, {-l - arrlength1*l, -l -
          tratio*l + i}}],
      Arrow[{{l, -l - tratio*l + i}, {l + arrlength1*l, -l -
          tratio*l + i}}]}, {i, 0, 2*(l + tratio*l),
      2*(l + tratio*l)/(arr1 - 1)}], Thickness[0.00001],
    Line[{{-l - arrlength1*l, -(l + tratio*l)}, {-l -
        arrlength1*l, (l + tratio*l)}}],
    Line[{{+l + arrlength1*l, -(l + tratio*l)}, {+l +
        arrlength1*l, (l + tratio*l)}}],
    Line[{{-l, l}, {-l, l + tratio*l}, {l, l + tratio*l}, {l, l}}],
    Line[{{-l, -l}, {-l, -l - tratio*l}, {l, -l -
        tratio*l}, {l, -l}}]}, Axes -> True, AxesLabel -> {x, z},
   AspectRatio -> 1, ImageSize -> ImgSize]]

plotBoundedCohesiveGeometry[Rf_, Vff_, tratio_, theta_, dtheta_, a_,
  arrwidth1_, arrlength1_, arr1_, arr2_, ImgSize_] :=
 With[{l = 0.5*Rf*Sqrt[Pi/Vff]},
  Graphics[{Opacity[1], Black, Circle[{0, 0}, Rf],
    Line[{{-l, l}, {-l, -l}}], Line[{{l, -l}, {l, l}}],
    Line[{{0, 0}, {Rf*Cos[theta], Rf*Sin[theta]}}],
    Line[{{-l, -l}, {l, -l}}], Line[{{l, l}, {-l, l}}], Green,
    Circle[{0, 0}, Rf, {0, 2*Pi}],
    With[{r =
       0.5*Rf*Sqrt[(Cos[theta + dtheta] -
             Cos[theta - dtheta])^2 + (Sin[theta + dtheta] -
             Sin[theta - dtheta])^2]},
     With[{R = Sqrt[Rf^2 - r^2]},
      If[a == 0, Circle[{0, 0}, Rf, {theta - dtheta, theta + dtheta}],
        If[dtheta <= Pi/2,
        Rotate[Circle[{R*Cos[theta],
           R*Sin[theta]}, {r, (Rf - R + a)}, {0,
           Pi}], -(Pi/2 - theta), {R*Cos[theta], R*Sin[theta]}],
        Rotate[Circle[{0,
           0}, {0.5*Rf*
            Sqrt[(Cos[theta + 0.5*Pi] -
                 Cos[theta - 0.5*Pi])^2 + (Sin[theta + 0.5*Pi] -
                 Sin[theta - 0.5*Pi])^2], Rf + a}, {0,
           Pi}], -(Pi/2 - theta), {0, 0}]]]]],
    Text[Style[Subscript[R, f], 12, Black,
      Bold], {3*Rf*Cos[1.1*theta]/(3*1.25),
      3*Rf*Sin[1.1*theta]/(3*1.25)}],
    Text[Style[Subscript[\[CapitalOmega], m], 12, Black,
      Bold], {1.075*Rf*Cos[220 Degree], 1.075*Rf*Sin[220 Degree]}],
    Text[Style[Subscript[\[CapitalOmega], f], 12, Black,
      Bold], {0.75*Rf*Cos[205 Degree], 0.75*Rf*Sin[205 Degree]}],
    Text[Style["O", 12, Black, Bold], {-0.05, -0.05}],
    Text[Style["l", 12, Black, Bold], {-0.5*l, 0.95*l}],
    Text[Style["l", 12, Black, Bold], {0.5*l, 0.95*l}],
    Text[Style["l", 12, Black, Bold], {-0.95*l, 0.5*l}],
    Text[Style["l", 12, Black, Bold], {-0.95*l, -0.5*l}],
    Text[Style[Subscript[\[CapitalOmega], "u,[0\[Degree]]"], 12,
      Black, Bold], {0.5*l, l + 0.5*tratio*l}],
    Text[Style[Subscript[\[CapitalOmega], "b,[0\[Degree]]"], 12,
      Black, Bold], {-0.5*l, -l - 0.5*tratio*l}], Black, Thin,
    Table[{Arrow[{{-l, -l - tratio*l + i}, {-l - arrlength1*l, -l -
          tratio*l + i}}],
      Arrow[{{l, -l - tratio*l + i}, {l + arrlength1*l, -l -
          tratio*l + i}}]}, {i, 0, 2*(l + tratio*l),
      2*(l + tratio*l)/(arr1 - 1)}], Thickness[0.00001],
    Line[{{-l - arrlength1*l, -(l + tratio*l)}, {-l -
        arrlength1*l, (l + tratio*l)}}],
    Line[{{+l + arrlength1*l, -(l + tratio*l)}, {+l +
        arrlength1*l, (l + tratio*l)}}],
    Line[{{-l, l}, {-l, l + tratio*l}, {l, l + tratio*l}, {l, l}}],
    Line[{{-l, -l}, {-l, -l - tratio*l}, {l, -l -
        tratio*l}, {l, -l}}]}, Axes -> True, AxesLabel -> {x, z},
   AspectRatio -> 1, ImageSize -> ImgSize]]

plotBoundedCohesiveSymmGeometry[Rf_, Vff_, tratio_, theta_, dtheta_,
  a_, arrwidth1_, arrlength1_, arr1_, arr2_, ImgSize_] :=
 With[{l = 0.5*Rf*Sqrt[Pi/Vff]},
  Graphics[{Opacity[1], Black, Circle[{0, 0}, Rf],
    Line[{{-l, l}, {-l, -l}}], Line[{{l, -l}, {l, l}}],
    Line[{{0, 0}, {Rf*Cos[theta], Rf*Sin[theta]}}],
    Line[{{-l, -l}, {l, -l}}], Line[{{l, l}, {-l, l}}], Green,
    Circle[{0, 0}, Rf, {0, 2*Pi}],
    With[{r =
       0.5*Rf*Sqrt[(Cos[theta + dtheta] -
             Cos[theta - dtheta])^2 + (Sin[theta + dtheta] -
             Sin[theta - dtheta])^2]},
     With[{R = Sqrt[Rf^2 - r^2]},
      If[a == 0, Circle[{0, 0}, Rf, {theta - dtheta, theta + dtheta}],
        If[dtheta <= Pi/2,
        Rotate[Circle[{R*Cos[theta],
           R*Sin[theta]}, {r, (Rf - R + a)}, {0,
           Pi}], -(Pi/2 - theta), {R*Cos[theta], R*Sin[theta]}],
        Rotate[Circle[{0,
           0}, {0.5*Rf*
            Sqrt[(Cos[theta + 0.5*Pi] -
                 Cos[theta - 0.5*Pi])^2 + (Sin[theta + 0.5*Pi] -
                 Sin[theta - 0.5*Pi])^2], Rf + a}, {0,
           Pi}], -(Pi/2 - theta), {0, 0}]]]]],
    Text[Style[Subscript[R, f], 12, Black,
      Bold], {3*Rf*Cos[1.1*theta]/(3*1.25),
      3*Rf*Sin[1.1*theta]/(3*1.25)}],
    Text[Style[Subscript[\[CapitalOmega], m], 12, Black,
      Bold], {1.075*Rf*Cos[220 Degree], 1.075*Rf*Sin[220 Degree]}],
    Text[Style[Subscript[\[CapitalOmega], f], 12, Black,
      Bold], {0.75*Rf*Cos[205 Degree], 0.75*Rf*Sin[205 Degree]}],
    Text[Style["O", 12, Black, Bold], {-0.05, -0.05}],
    Text[Style["l", 12, Black, Bold], {-0.5*l, 0.95*l}],
    Text[Style["l", 12, Black, Bold], {0.5*l, 0.95*l}],
    Text[Style["l", 12, Black, Bold], {-0.95*l, 0.5*l}],
    Text[Style["l", 12, Black, Bold], {-0.95*l, -0.5*l}],
    Text[Style[Subscript[\[CapitalOmega], "u,[0\[Degree]]"], 12,
      Black, Bold], {0.5*l, l + 0.5*tratio*l}], Black, Thin,
    Table[{Arrow[{{-l, -l + i}, {-l - arrlength1*l, -l + i}}],
      Arrow[{{l, -l + i}, {l + arrlength1*l, -l + i}}]}, {i,
      0, (2*l + tratio*l), (2*l + tratio*l)/(arr1 - 1)}],
    Thickness[0.00001],
    Line[{{-l - arrlength1*l, -l}, {-l -
        arrlength1*l, (l + tratio*l)}}],
    Line[{{+l + arrlength1*l, -l}, {+l +
        arrlength1*l, (l + tratio*l)}}],
    Line[{{-l, l}, {-l, l + tratio*l}, {l, l + tratio*l}, {l, l}}],
    DotDashed, Blue, Thickness[0.006],
    Line[{{-(1 + 1.5*arrwidth1)*l, -l}, {(1 + 1.5*arrwidth1)*
        l, -l}}]}, Axes -> True, AxesLabel -> {x, z},
   AspectRatio -> 1, ImageSize -> ImgSize]]

plotPeriodicGeometry[Rf_, Vff_, theta_, dtheta_, a_, arrwidth1_,
  arrlength1_, arr1_, arr2_, ImgSize_] :=
 With[{l = 0.5 Rf Sqrt[\[Pi]/Vff]},
  Graphics[{Blue, Opacity[0.35],
    Annulus[{0, 0}, {Rf/3, (2 Rf)/3}, {theta - dtheta,
      theta + dtheta}], Green, Opacity[0.35],
    Disk[{0, 0}, Rf/3, {0, theta}], Opacity[1], Black,
    Circle[{0, 0}, Rf], Line[{{-l, l}, {-l, -l}}],
    Line[{{l, -l}, {l, l}}],
    Line[{{0, 0}, {Rf Cos[theta], Rf Sin[theta]}}],
    Line[{{0, 0}, {Rf Cos[theta - dtheta], Rf Sin[theta - dtheta]}}],
    Line[{{0, 0}, {Rf Cos[theta + dtheta], Rf Sin[theta + dtheta]}}],
    Line[{{-l, -l}, {l, -l}}], Line[{{l, l}, {-l, l}}], Red,
    Circle[{0, 0}, Rf, {theta - dtheta, theta + dtheta}],
    With[{r =
       0.5 Rf Sqrt[(Cos[theta + dtheta] -
           Cos[theta - dtheta])^2 + (Sin[theta + dtheta] -
           Sin[theta - dtheta])^2]},
     With[{R = Sqrt[Rf^2 - r^2]},
      If[a == 0, Circle[{0, 0}, Rf, {theta - dtheta, theta + dtheta}],
        If[dtheta <= \[Pi]/2,
        Rotate[Circle[{R Cos[theta], R Sin[theta]}, {r,
           Rf - R + a}, {0, \[Pi]}], -(\[Pi]/2 - theta), {R Cos[
            theta], R Sin[theta]}],
        Rotate[Circle[{0,
           0}, {0.5 Rf Sqrt[(Cos[theta + 0.5 \[Pi]] -
               Cos[theta - 0.5 \[Pi]])^2 + (Sin[theta + 0.5 \[Pi]] -
               Sin[theta - 0.5 \[Pi]])^2],
           Rf + a}, {0, \[Pi]}], -(\[Pi]/2 - theta), {0, 0}]]]]],
    Text[Style["\[Theta]", 12, Black, Bold], {(Rf Cos[theta/2])/(
      3 1.5), (Rf Sin[theta/2])/(3 1.5)}],
    Text[Style["\[CapitalDelta]\[Theta]", 12, Black, Bold], {(
      2 Rf Cos[theta - dtheta/2])/(3 1.25), (
      2 Rf Sin[theta - dtheta/2])/(3 1.25)}],
    Text[Style["\[CapitalDelta]\[Theta]", 12, Black, Bold], {(
      2 Rf Cos[theta + dtheta/2])/(3 1.25), (
      2 Rf Sin[theta + dtheta/2])/(3 1.25)}],
    Text[Style[Subscript[R, f], 12, Black, Bold], {(
      3 Rf Cos[1.1 theta])/(3 1.25), (3 Rf Sin[1.1 theta])/(3 1.25)}],
     Text[Style[Subscript[\[CapitalOmega], m], 12, Black,
      Bold], {1.075 Rf Cos[220 \[Degree]],
      1.075 Rf Sin[220 \[Degree]]}],
    Text[Style[Subscript[\[CapitalOmega], f], 12, Black,
      Bold], {0.75 Rf Cos[205 \[Degree]],
      0.75 Rf Sin[205 \[Degree]]}],
    Text[Style[Subscript[\[CapitalGamma], 1], 12, Black,
      Bold], {1.075 Rf Cos[255 \[Degree]],
      1.075 Rf Sin[255 \[Degree]]}],
    Text[Style[Subscript[\[CapitalGamma], 2], 12, Black,
      Bold], {0.95 Rf Cos[theta - dtheta/2],
      0.95 Rf Sin[theta - dtheta/2]}],
    Text[Style[Subscript[\[CapitalGamma], 3], 12, Black,
      Bold], {(1.075 Rf + a) Cos[
        theta + dtheta/2], (1.075 Rf + a) Sin[theta + dtheta/2]}],
    Text[Style["O", 12, Black, Bold], {-0.05, -0.05}],
    Text[Style["l", 12, Black, Bold], {-0.5 l, 0.95 l}],
    Text[Style["l", 12, Black, Bold], {0.5 l, 0.95 l}],
    Text[Style["l", 12, Black, Bold], {-0.95 l, 0.5 l}],
    Text[Style["l", 12, Black, Bold], {-0.95 l, -0.5 l}], Black, Thin,
     Table[{Arrow[{{-l, -l + i}, {-l - arrlength1 l, -l + i}}],
      Arrow[{{l, -l + i}, {l + arrlength1 l, -l + i}}]}, {i, 0, 2 l, (
      2 l)/(arr1 - 1)}], Thickness[0.00001],
    Line[{{-l - arrlength1 l, -l}, {-l - arrlength1 l, l}}],
    Line[{{+l + arrlength1 l, -l}, {+l + arrlength1 l, l}}], Black,
    Thin, Dashed, Line[{{-l, -3 l}, {-l, -l}}],
    Line[{{l, -3 l}, {l, -l}}], Line[{{-l, 3 l}, {-l, l}}],
    Line[{{l, 3 l}, {l, l}}], Line[{{-3 l, -l}, {-l, -l}}],
    Line[{{-3 l, l}, {-l, l}}], Line[{{3 l, -l}, {l, -l}}],
    Line[{{3 l, l}, {l, l}}],
    Line[{{-3 l, -3 l}, {-3 l, 3 l}, {3 l,
       3 l}, {3 l, -3 l}, {-3 l, -3 l}}], Circle[{0, -2 l}, Rf],
    Circle[{0, 2 l}, Rf], Circle[{-2 l, -2 l}, Rf],
    Circle[{-2 l, 2 l}, Rf], Circle[{-2 l, 0}, Rf],
    Circle[{2 l, -2 l}, Rf], Circle[{2 l, 2 l}, Rf],
    Circle[{2 l, 0}, Rf]}, Axes -> True, AxesLabel -> {x, z},
   AspectRatio -> 1, ImageSize -> ImgSize]]

plotPeriodicCohesiveGeometry[Rf_, Vff_, theta_, dtheta_, a_,
  arrwidth1_, arrlength1_, arr1_, arr2_, ImgSize_] :=
 With[{l = 0.5 Rf Sqrt[\[Pi]/Vff]},
  Graphics[{Opacity[1], Black, Circle[{0, 0}, Rf],
    Line[{{-l, l}, {-l, -l}}], Line[{{l, -l}, {l, l}}],
    Line[{{0, 0}, {Rf Cos[theta], Rf Sin[theta]}}],
    Line[{{-l, -l}, {l, -l}}], Line[{{l, l}, {-l, l}}], Green,
    Circle[{0, 0}, Rf, {0, 2*Pi}],
    With[{r =
       0.5 Rf Sqrt[(Cos[theta + dtheta] -
           Cos[theta - dtheta])^2 + (Sin[theta + dtheta] -
           Sin[theta - dtheta])^2]},
     With[{R = Sqrt[Rf^2 - r^2]},
      If[a == 0, Circle[{0, 0}, Rf, {theta - dtheta, theta + dtheta}],
        If[dtheta <= \[Pi]/2,
        Rotate[Circle[{R Cos[theta], R Sin[theta]}, {r,
           Rf - R + a}, {0, \[Pi]}], -(\[Pi]/2 - theta), {R Cos[
            theta], R Sin[theta]}],
        Rotate[Circle[{0,
           0}, {0.5 Rf Sqrt[(Cos[theta + 0.5 \[Pi]] -
               Cos[theta - 0.5 \[Pi]])^2 + (Sin[theta + 0.5 \[Pi]] -
               Sin[theta - 0.5 \[Pi]])^2],
           Rf + a}, {0, \[Pi]}], -(\[Pi]/2 - theta), {0, 0}]]]]],
    Text[Style[Subscript[R, f], 12, Black, Bold], {(
      3 Rf Cos[1.1 theta])/(3 1.25), (3 Rf Sin[1.1 theta])/(3 1.25)}],
     Text[Style[Subscript[\[CapitalOmega], m], 12, Black,
      Bold], {1.075 Rf Cos[220 \[Degree]],
      1.075 Rf Sin[220 \[Degree]]}],
    Text[Style[Subscript[\[CapitalOmega], f], 12, Black,
      Bold], {0.75 Rf Cos[205 \[Degree]],
      0.75 Rf Sin[205 \[Degree]]}],
    Text[Style["O", 12, Black, Bold], {-0.05, -0.05}],
    Text[Style["l", 12, Black, Bold], {-0.5 l, 0.95 l}],
    Text[Style["l", 12, Black, Bold], {0.5 l, 0.95 l}],
    Text[Style["l", 12, Black, Bold], {-0.95 l, 0.5 l}],
    Text[Style["l", 12, Black, Bold], {-0.95 l, -0.5 l}], Black, Thin,
     Table[{Arrow[{{-l, -l + i}, {-l - arrlength1 l, -l + i}}],
      Arrow[{{l, -l + i}, {l + arrlength1 l, -l + i}}]}, {i, 0, 2 l, (
      2 l)/(arr1 - 1)}], Thickness[0.00001],
    Line[{{-l - arrlength1 l, -l}, {-l - arrlength1 l, l}}],
    Line[{{+l + arrlength1 l, -l}, {+l + arrlength1 l, l}}], Black,
    Thin, Dashed, Line[{{-l, -3 l}, {-l, -l}}],
    Line[{{l, -3 l}, {l, -l}}], Line[{{-l, 3 l}, {-l, l}}],
    Line[{{l, 3 l}, {l, l}}], Line[{{-3 l, -l}, {-l, -l}}],
    Line[{{-3 l, l}, {-l, l}}], Line[{{3 l, -l}, {l, -l}}],
    Line[{{3 l, l}, {l, l}}],
    Line[{{-3 l, -3 l}, {-3 l, 3 l}, {3 l,
       3 l}, {3 l, -3 l}, {-3 l, -3 l}}], Circle[{0, -2 l}, Rf],
    Circle[{0, 2 l}, Rf], Circle[{-2 l, -2 l}, Rf],
    Circle[{-2 l, 2 l}, Rf], Circle[{-2 l, 0}, Rf],
    Circle[{2 l, -2 l}, Rf], Circle[{2 l, 2 l}, Rf],
    Circle[{2 l, 0}, Rf]}, Axes -> True, AxesLabel -> {x, z},
   AspectRatio -> 1, ImageSize -> ImgSize]]

(* :2D TPM Tests Geometry Plotting:  surface ply,  interface crack, one fiber (arrangement 1):  *)

plotOuterSingleGeometry[Rf_, Vff_, theta_, dtheta_, a_, arrwidth1_,
  arrlength1_, arr1_, arr2_, ImgSize_] :=
 With[{l = 0.5*Rf*Sqrt[Pi/Vff]},
  Graphics[{Blue, Opacity[0.35],
    Annulus[{0, 0}, {Rf/3, 2*Rf/3}, {theta - dtheta, theta + dtheta}],
     Green, Opacity[0.35], Disk[{0, 0}, Rf/3, {0, theta}], Opacity[1],
     Black, Circle[{0, 0}, Rf], Line[{{-l, l}, {-l, -l}}],
    Line[{{l, -l}, {l, l}}], Line[{{-l, l}, {l, l}}],
    Line[{{0, 0}, {Rf*Cos[theta], Rf*Sin[theta]}}],
    Line[{{0, 0}, {Rf*Cos[theta - dtheta], Rf*Sin[theta - dtheta]}}],
    Line[{{0, 0}, {Rf*Cos[theta + dtheta], Rf*Sin[theta + dtheta]}}],
    Thickness[0.006], Line[{{-l, -l}, {l, -l}}], Red,
    Circle[{0, 0}, Rf, {theta - dtheta, theta + dtheta}],
    With[{r =
       0.5*Rf*Sqrt[(Cos[theta + dtheta] -
             Cos[theta - dtheta])^2 + (Sin[theta + dtheta] -
             Sin[theta - dtheta])^2]},
     With[{R = Sqrt[Rf^2 - r^2]},
      If[a == 0, Circle[{0, 0}, Rf, {theta - dtheta, theta + dtheta}],
        If[dtheta <= Pi/2,
        Rotate[Circle[{R*Cos[theta],
           R*Sin[theta]}, {r, (Rf - R + a)}, {0,
           Pi}], -(Pi/2 - theta), {R*Cos[theta], R*Sin[theta]}],
        Rotate[Circle[{0,
           0}, {0.5*Rf*
            Sqrt[(Cos[theta + 0.5*Pi] -
                 Cos[theta - 0.5*Pi])^2 + (Sin[theta + 0.5*Pi] -
                 Sin[theta - 0.5*Pi])^2], Rf + a}, {0,
           Pi}], -(Pi/2 - theta), {0, 0}]]]]],
    Text[Style["\[Theta]", 12, Black, Bold], {Rf*Cos[theta/2]/(3*1.5),
       Rf*Sin[theta/2]/(3*1.5)}],
    Text[Style["\[CapitalDelta]\[Theta]", 12, Black,
      Bold], {2*Rf*Cos[theta - dtheta/2]/(3*1.25),
      2*Rf*Sin[theta - dtheta/2]/(3*1.25)}],
    Text[Style["\[CapitalDelta]\[Theta]", 12, Black,
      Bold], {2*Rf*Cos[theta + dtheta/2]/(3*1.25),
      2*Rf*Sin[theta + dtheta/2]/(3*1.25)}],
    Text[Style[Subscript[R, f], 12, Black,
      Bold], {3*Rf*Cos[1.1*theta]/(3*1.25),
      3*Rf*Sin[1.1*theta]/(3*1.25)}],
    Text[Style[Subscript[\[CapitalOmega], m], 12, Black,
      Bold], {1.075*Rf*Cos[220 Degree], 1.075*Rf*Sin[220 Degree]}],
    Text[Style[Subscript[\[CapitalOmega], f], 12, Black,
      Bold], {0.75*Rf*Cos[205 Degree], 0.75*Rf*Sin[205 Degree]}],
    Text[Style[Subscript[\[CapitalGamma], 1], 12, Black,
      Bold], {1.075*Rf*Cos[255 Degree], 1.075*Rf*Sin[255 Degree]}],
    Text[Style[Subscript[\[CapitalGamma], 2], 12, Black,
      Bold], {0.95*Rf*Cos[theta - dtheta/2],
      0.95*Rf*Sin[theta - dtheta/2]}],
    Text[Style[Subscript[\[CapitalGamma], 3], 12, Black,
      Bold], {(1.075*Rf + a)*Cos[theta + dtheta/2], (1.075*Rf + a)*
       Sin[theta + dtheta/2]}],
    Text[Style["O", 12, Black, Bold], {-0.05, -0.05}],
    Text[Style["l", 12, Black, Bold], {-0.5*l, 0.95*l}],
    Text[Style["l", 12, Black, Bold], {0.5*l, 0.95*l}],
    Text[Style["l", 12, Black, Bold], {-0.95*l, 0.5*l}],
    Text[Style["l", 12, Black, Bold], {-0.95*l, -0.5*l}], Black, Thin,
     Table[{Arrow[{{-l, -l + i}, {-l - arrlength1*l, -l + i}}],
      Arrow[{{l, -l + i}, {l + arrlength1*l, -l + i}}]}, {i, 0, 2*l,
      2*l/(arr1 - 1)}],
    Table[{Arrow[{{0 + i/arrwidth1 - arrwidth1*l/arr2, -l -
          i}, {l, -l - i}}],
      Arrow[{{0 - i/arrwidth1 + arrwidth1*l/arr2, -l - i}, {-l, -l -
          i}}]}, {i, arrwidth1*l/arr2, arrwidth1*l,
      arrwidth1*l/arr2}], Thickness[0.00001],
    Line[{{-l - arrlength1*l, -l}, {-l - arrlength1*l, l}}],
    Line[{{+l + arrlength1*l, -l}, {+l + arrlength1*l, l}}],
    Line[{{l, -l}, {l, -(1 + arrwidth1)*l}}],
    Line[{{-l, -l}, {-l, -(1 + arrwidth1)*l}}]}, Axes -> True,
   AxesLabel -> {x, z}, AspectRatio -> 1, ImageSize -> ImgSize]]

plotOuterSingleSymmGeometry[Rf_, Vff_, theta_, dtheta_, a_,
  arrwidth1_, arrlength1_, arr1_, arr2_, ImgSize_] :=
 With[{l = 0.5*Rf*Sqrt[Pi/Vff]},
  Graphics[{Blue, Opacity[0.35],
    Annulus[{0, 0}, {Rf/3, 2*Rf/3}, {theta - dtheta, theta + dtheta}],
     Green, Opacity[0.35], Disk[{0, 0}, Rf/3, {0, theta}], Opacity[1],
     Black, Circle[{0, 0}, Rf], Line[{{-l, l}, {-l, -l}}],
    Line[{{l, -l}, {l, l}}], Line[{{-l, l}, {l, l}}],
    Line[{{0, 0}, {Rf*Cos[theta], Rf*Sin[theta]}}],
    Line[{{0, 0}, {Rf*Cos[theta - dtheta], Rf*Sin[theta - dtheta]}}],
    Line[{{0, 0}, {Rf*Cos[theta + dtheta], Rf*Sin[theta + dtheta]}}],
    Thickness[0.006], Line[{{-l, -l}, {l, -l}}], Red,
    Circle[{0, 0}, Rf, {theta - dtheta, theta + dtheta}],
    With[{r =
       0.5*Rf*Sqrt[(Cos[theta + dtheta] -
             Cos[theta - dtheta])^2 + (Sin[theta + dtheta] -
             Sin[theta - dtheta])^2]},
     With[{R = Sqrt[Rf^2 - r^2]},
      If[a == 0, Circle[{0, 0}, Rf, {theta - dtheta, theta + dtheta}],
        If[dtheta <= Pi/2,
        Rotate[Circle[{R*Cos[theta],
           R*Sin[theta]}, {r, (Rf - R + a)}, {0,
           Pi}], -(Pi/2 - theta), {R*Cos[theta], R*Sin[theta]}],
        Rotate[Circle[{0,
           0}, {0.5*Rf*
            Sqrt[(Cos[theta + 0.5*Pi] -
                 Cos[theta - 0.5*Pi])^2 + (Sin[theta + 0.5*Pi] -
                 Sin[theta - 0.5*Pi])^2], Rf + a}, {0,
           Pi}], -(Pi/2 - theta), {0, 0}]]]]],
    Text[Style["\[Theta]", 12, Black, Bold], {Rf*Cos[theta/2]/(3*1.5),
       Rf*Sin[theta/2]/(3*1.5)}],
    Text[Style["\[CapitalDelta]\[Theta]", 12, Black,
      Bold], {2*Rf*Cos[theta - dtheta/2]/(3*1.25),
      2*Rf*Sin[theta - dtheta/2]/(3*1.25)}],
    Text[Style["\[CapitalDelta]\[Theta]", 12, Black,
      Bold], {2*Rf*Cos[theta + dtheta/2]/(3*1.25),
      2*Rf*Sin[theta + dtheta/2]/(3*1.25)}],
    Text[Style[Subscript[R, f], 12, Black,
      Bold], {3*Rf*Cos[1.1*theta]/(3*1.25),
      3*Rf*Sin[1.1*theta]/(3*1.25)}],
    Text[Style[Subscript[\[CapitalOmega], m], 12, Black,
      Bold], {1.075*Rf*Cos[220 Degree], 1.075*Rf*Sin[220 Degree]}],
    Text[Style[Subscript[\[CapitalOmega], f], 12, Black,
      Bold], {0.75*Rf*Cos[205 Degree], 0.75*Rf*Sin[205 Degree]}],
    Text[Style[Subscript[\[CapitalGamma], 1], 12, Black,
      Bold], {1.075*Rf*Cos[255 Degree], 1.075*Rf*Sin[255 Degree]}],
    Text[Style[Subscript[\[CapitalGamma], 2], 12, Black,
      Bold], {0.95*Rf*Cos[theta - dtheta/2],
      0.95*Rf*Sin[theta - dtheta/2]}],
    Text[Style[Subscript[\[CapitalGamma], 3], 12, Black,
      Bold], {(1.075*Rf + a)*Cos[theta + dtheta/2], (1.075*Rf + a)*
       Sin[theta + dtheta/2]}],
    Text[Style["O", 12, Black, Bold], {-0.05, -0.05}],
    Text[Style["l", 12, Black, Bold], {-0.5*l, 0.95*l}],
    Text[Style["l", 12, Black, Bold], {0.5*l, 0.95*l}],
    Text[Style["l", 12, Black, Bold], {-0.95*l, 0.5*l}],
    Text[Style["l", 12, Black, Bold], {-0.95*l, -0.5*l}], Black, Thin,
     Table[{Arrow[{{-l, -l + i}, {-l - arrlength1*l, -l + i}}],
      Arrow[{{l, -l + i}, {l + arrlength1*l, -l + i}}]}, {i, 0, 2*l,
      2*l/(arr1 - 1)}],
    Table[{Arrow[{{0 + i/arrwidth1 - arrwidth1*l/arr2, -l -
          i}, {l, -l - i}}],
      Arrow[{{0 - i/arrwidth1 + arrwidth1*l/arr2, -l - i}, {-l, -l -
          i}}]}, {i, arrwidth1*l/arr2, arrwidth1*l,
      arrwidth1*l/arr2}], Thickness[0.00001],
    Line[{{-l - arrlength1*l, -l}, {-l - arrlength1*l, l}}],
    Line[{{+l + arrlength1*l, -l}, {+l + arrlength1*l, l}}]},
   Axes -> True, AxesLabel -> {x, z}, AspectRatio -> 1,
   ImageSize -> ImgSize]]

plotOuterSingleCohesiveGeometry[Rf_, Vff_, theta_, dtheta_, a_,
  arrwidth1_, arrlength1_, arr1_, arr2_, ImgSize_] :=
 With[{l = 0.5*Rf*Sqrt[Pi/Vff]},
  Graphics[{Opacity[1], Black, Circle[{0, 0}, Rf],
    Line[{{-l, l}, {-l, -l}}], Line[{{l, -l}, {l, l}}],
    Line[{{l, l}, {-l, l}}],
    Line[{{0, 0}, {Rf*Cos[theta], Rf*Sin[theta]}}],  Thickness[0.006],
     Line[{{-l, -l}, {l, -l}}], Thickness[0.005], Green,
    Circle[{0, 0}, Rf, {0, 2*Pi}],
    With[{r =
       0.5*Rf*Sqrt[(Cos[theta + dtheta] -
             Cos[theta - dtheta])^2 + (Sin[theta + dtheta] -
             Sin[theta - dtheta])^2]},
     With[{R = Sqrt[Rf^2 - r^2]},
      If[a == 0, Circle[{0, 0}, Rf, {theta - dtheta, theta + dtheta}],
        If[dtheta <= Pi/2,
        Rotate[Circle[{R*Cos[theta],
           R*Sin[theta]}, {r, (Rf - R + a)}, {0,
           Pi}], -(Pi/2 - theta), {R*Cos[theta], R*Sin[theta]}],
        Rotate[Circle[{0,
           0}, {0.5*Rf*
            Sqrt[(Cos[theta + 0.5*Pi] -
                 Cos[theta - 0.5*Pi])^2 + (Sin[theta + 0.5*Pi] -
                 Sin[theta - 0.5*Pi])^2], Rf + a}, {0,
           Pi}], -(Pi/2 - theta), {0, 0}]]]]],
    Text[Style[Subscript[R, f], 12, Black,
      Bold], {3*Rf*Cos[1.1*theta]/(3*1.25),
      3*Rf*Sin[1.1*theta]/(3*1.25)}],
    Text[Style[Subscript[\[CapitalOmega], m], 12, Black,
      Bold], {1.075*Rf*Cos[220 Degree], 1.075*Rf*Sin[220 Degree]}],
    Text[Style[Subscript[\[CapitalOmega], f], 12, Black,
      Bold], {0.75*Rf*Cos[205 Degree], 0.75*Rf*Sin[205 Degree]}],
    Text[Style["O", 12, Black, Bold], {-0.05, -0.05}],
    Text[Style["l", 12, Black, Bold], {-0.5*l, 0.95*l}],
    Text[Style["l", 12, Black, Bold], {0.5*l, 0.95*l}],
    Text[Style["l", 12, Black, Bold], {-0.95*l, 0.5*l}],
    Text[Style["l", 12, Black, Bold], {-0.95*l, -0.5*l}], Black, Thin,
     Table[{Arrow[{{-l, -l + i}, {-l - arrlength1*l, -l + i}}],
      Arrow[{{l, -l + i}, {l + arrlength1*l, -l + i}}]}, {i, 0, 2*l,
      2*l/(arr1 - 1)}],
    Table[{Arrow[{{0 + i/arrwidth1 - arrwidth1*l/arr2, -l -
          i}, {l, -l - i}}],
      Arrow[{{0 - i/arrwidth1 + arrwidth1*l/arr2, -l - i}, {-l, -l -
          i}}]}, {i, arrwidth1*l/arr2, arrwidth1*l,
      arrwidth1*l/arr2}], Thickness[0.00001],
    Line[{{-l - arrlength1*l, -l}, {-l - arrlength1*l, l}}],
    Line[{{+l + arrlength1*l, -l}, {+l + arrlength1*l, l}}],
    Line[{{l, -l}, {l, -(1 + arrwidth1)*l}}],
    Line[{{-l, -l}, {-l, -(1 + arrwidth1)*l}}]}, Axes -> True,
   AxesLabel -> {x, z}, AspectRatio -> 1, ImageSize -> ImgSize]]

plotOuterSingleCohesiveSymmGeometry[Rf_, Vff_, theta_, dtheta_, a_,
  arrwidth1_, arrlength1_, arr1_, arr2_, ImgSize_] :=
 With[{l = 0.5*Rf*Sqrt[Pi/Vff]},
  Graphics[{Opacity[1], Black, Circle[{0, 0}, Rf],
    Line[{{-l, l}, {-l, -l}}], Line[{{l, -l}, {l, l}}],
    Line[{{l, l}, {-l, l}}],
    Line[{{0, 0}, {Rf*Cos[theta], Rf*Sin[theta]}}],  Thickness[0.006],
     Line[{{l, -l}, {-l, -l}}], Thickness[0.005], Green,
    Circle[{0, 0}, Rf, {0, 2*Pi}],
    With[{r =
       0.5*Rf*Sqrt[(Cos[theta + dtheta] -
             Cos[theta - dtheta])^2 + (Sin[theta + dtheta] -
             Sin[theta - dtheta])^2]},
     With[{R = Sqrt[Rf^2 - r^2]},
      If[a == 0, Circle[{0, 0}, Rf, {theta - dtheta, theta + dtheta}],
        If[dtheta <= Pi/2,
        Rotate[Circle[{R*Cos[theta],
           R*Sin[theta]}, {r, (Rf - R + a)}, {0,
           Pi}], -(Pi/2 - theta), {R*Cos[theta], R*Sin[theta]}],
        Rotate[Circle[{0,
           0}, {0.5*Rf*
            Sqrt[(Cos[theta + 0.5*Pi] -
                 Cos[theta - 0.5*Pi])^2 + (Sin[theta + 0.5*Pi] -
                 Sin[theta - 0.5*Pi])^2], Rf + a}, {0,
           Pi}], -(Pi/2 - theta), {0, 0}]]]]],
    Text[Style[Subscript[R, f], 12, Black,
      Bold], {3*Rf*Cos[1.1*theta]/(3*1.25),
      3*Rf*Sin[1.1*theta]/(3*1.25)}],
    Text[Style[Subscript[\[CapitalOmega], m], 12, Black,
      Bold], {1.075*Rf*Cos[220 Degree], 1.075*Rf*Sin[220 Degree]}],
    Text[Style[Subscript[\[CapitalOmega], f], 12, Black,
      Bold], {0.75*Rf*Cos[205 Degree], 0.75*Rf*Sin[205 Degree]}],
    Text[Style["O", 12, Black, Bold], {-0.05, -0.05}],
    Text[Style["l", 12, Black, Bold], {-0.5*l, 0.95*l}],
    Text[Style["l", 12, Black, Bold], {0.5*l, 0.95*l}],
    Text[Style["l", 12, Black, Bold], {-0.95*l, 0.5*l}],
    Text[Style["l", 12, Black, Bold], {-0.95*l, -0.5*l}], Black, Thin,
     Table[{Arrow[{{-l, -l + i}, {-l - arrlength1*l, -l + i}}],
      Arrow[{{l, -l + i}, {l + arrlength1*l, -l + i}}]}, {i, 0, 2*l,
      2*l/(arr1 - 1)}],
    Table[{Arrow[{{0 + i/arrwidth1 - arrwidth1*l/arr2, -l -
          i}, {l, -l - i}}],
      Arrow[{{0 - i/arrwidth1 + arrwidth1*l/arr2, -l - i}, {-l, -l -
          i}}]}, {i, arrwidth1*l/arr2, arrwidth1*l,
      arrwidth1*l/arr2}], Thickness[0.00001],
    Line[{{-l - arrlength1*l, -l}, {-l - arrlength1*l, l}}],
    Line[{{+l + arrlength1*l, -l}, {+l + arrlength1*l, l}}],
    Line[{{l, -l}, {l, -(1 + arrwidth1)*l}}],
    Line[{{-l, -l}, {-l, -(1 + arrwidth1)*l}}]}, Axes -> True,
   AxesLabel -> {x, z}, AspectRatio -> 1, ImageSize -> ImgSize]]

plotOuterBoundedGeometry[Rf_, Vff_, tratio_, theta_, dtheta_, a_,
  arrwidth1_, arrlength1_, arr1_, arr2_, ImgSize_] :=
 With[{l = 0.5*Rf*Sqrt[Pi/Vff]},
  Graphics[{Blue, Opacity[0.35],
    Annulus[{0, 0}, {Rf/3, 2*Rf/3}, {theta - dtheta, theta + dtheta}],
     Green, Opacity[0.35], Disk[{0, 0}, Rf/3, {0, theta}], Opacity[1],
     Black, Circle[{0, 0}, Rf], Line[{{-l, l}, {-l, -l}}],
    Line[{{l, -l}, {l, l}}],
    Line[{{0, 0}, {Rf*Cos[theta], Rf*Sin[theta]}}],
    Line[{{0, 0}, {Rf*Cos[theta - dtheta], Rf*Sin[theta - dtheta]}}],
    Line[{{0, 0}, {Rf*Cos[theta + dtheta], Rf*Sin[theta + dtheta]}}],
    Line[{{-l, -l}, {l, -l}}], Line[{{l, l}, {-l, l}}], Red,
    Circle[{0, 0}, Rf, {theta - dtheta, theta + dtheta}],
    With[{r =
       0.5*Rf*Sqrt[(Cos[theta + dtheta] -
             Cos[theta - dtheta])^2 + (Sin[theta + dtheta] -
             Sin[theta - dtheta])^2]},
     With[{R = Sqrt[Rf^2 - r^2]},
      If[a == 0, Circle[{0, 0}, Rf, {theta - dtheta, theta + dtheta}],
        If[dtheta <= Pi/2,
        Rotate[Circle[{R*Cos[theta],
           R*Sin[theta]}, {r, (Rf - R + a)}, {0,
           Pi}], -(Pi/2 - theta), {R*Cos[theta], R*Sin[theta]}],
        Rotate[Circle[{0,

           0}, {0.5*Rf*
            Sqrt[(Cos[theta + 0.5*Pi] -
                 Cos[theta - 0.5*Pi])^2 + (Sin[theta + 0.5*Pi] -
                 Sin[theta - 0.5*Pi])^2], Rf + a}, {0,
           Pi}], -(Pi/2 - theta), {0, 0}]]]]],
    Text[Style["\[Theta]", 12, Black, Bold], {Rf*Cos[theta/2]/(3*1.5),
       Rf*Sin[theta/2]/(3*1.5)}],
    Text[Style["\[CapitalDelta]\[Theta]", 12, Black,
      Bold], {2*Rf*Cos[theta - dtheta/2]/(3*1.25),
      2*Rf*Sin[theta - dtheta/2]/(3*1.25)}],
    Text[Style["\[CapitalDelta]\[Theta]", 12, Black,
      Bold], {2*Rf*Cos[theta + dtheta/2]/(3*1.25),
      2*Rf*Sin[theta + dtheta/2]/(3*1.25)}],
    Text[Style[Subscript[R, f], 12, Black,
      Bold], {3*Rf*Cos[1.1*theta]/(3*1.25),
      3*Rf*Sin[1.1*theta]/(3*1.25)}],
    Text[Style[Subscript[\[CapitalOmega], m], 12, Black,
      Bold], {1.075*Rf*Cos[220 Degree], 1.075*Rf*Sin[220 Degree]}],
    Text[Style[Subscript[\[CapitalOmega], f], 12, Black,
      Bold], {0.75*Rf*Cos[205 Degree], 0.75*Rf*Sin[205 Degree]}],
    Text[Style[Subscript[\[CapitalGamma], 1], 12, Black,
      Bold], {1.075*Rf*Cos[255 Degree], 1.075*Rf*Sin[255 Degree]}],
    Text[Style[Subscript[\[CapitalGamma], 2], 12, Black,
      Bold], {0.95*Rf*Cos[theta - dtheta/2],
      0.95*Rf*Sin[theta - dtheta/2]}],
    Text[Style[Subscript[\[CapitalGamma], 3], 12, Black,
      Bold], {(1.075*Rf + a)*Cos[theta + dtheta/2], (1.075*Rf + a)*
       Sin[theta + dtheta/2]}],
    Text[Style["O", 12, Black, Bold], {-0.05, -0.05}],
    Text[Style["l", 12, Black, Bold], {-0.5*l, 0.95*l}],
    Text[Style["l", 12, Black, Bold], {0.5*l, 0.95*l}],
    Text[Style["l", 12, Black, Bold], {-0.95*l, 0.5*l}],
    Text[Style["l", 12, Black, Bold], {-0.95*l, -0.5*l}],
    Text[Style[Subscript[\[CapitalOmega], "b,[0\[Degree]]"], 12,
      Black, Bold], {-0.5*l, -l - 0.5*tratio*l}], Black, Thin,
    Table[{Arrow[{{-l, -l - tratio*l + i}, {-l - arrlength1*l, -l -
          tratio*l + i}}],
      Arrow[{{l, -l - tratio*l + i}, {l + arrlength1*l, -l -
          tratio*l + i}}]}, {i,
      0, (2*l + tratio*l), (2*l + tratio*l)/(arr1 - 1)}],
    Thickness[0.00001],
    Line[{{-l - arrlength1*l, -(l + tratio*l)}, {-l - arrlength1*l,
       l}}], Line[{{+l + arrlength1*l, -(l + tratio*l)}, {+l +
        arrlength1*l, l}}],
    Line[{{-l, -l}, {-l, -l - tratio*l}, {l, -l -
        tratio*l}, {l, -l}}]}, Axes -> True, AxesLabel -> {x, z},
   AspectRatio -> 1, ImageSize -> ImgSize]]

plotOuterBoundedSymmGeometry[Rf_, Vff_, tratio_, theta_, dtheta_, a_,
  arrwidth1_, arrlength1_, arr1_, arr2_, ImgSize_] :=
 With[{l = 0.5*Rf*Sqrt[Pi/Vff]},
  Graphics[{Blue, Opacity[0.35],
    Annulus[{0, 0}, {Rf/3, 2*Rf/3}, {theta - dtheta, theta + dtheta}],
     Green, Opacity[0.35], Disk[{0, 0}, Rf/3, {0, theta}], Opacity[1],
     Black, Circle[{0, 0}, Rf], Line[{{-l, l}, {-l, -l}}],
    Line[{{l, -l}, {l, l}}],
    Line[{{0, 0}, {Rf*Cos[theta], Rf*Sin[theta]}}],
    Line[{{0, 0}, {Rf*Cos[theta - dtheta], Rf*Sin[theta - dtheta]}}],
    Line[{{0, 0}, {Rf*Cos[theta + dtheta], Rf*Sin[theta + dtheta]}}],
    Line[{{-l, -l}, {l, -l}}], Line[{{l, l}, {-l, l}}], Red,
    Circle[{0, 0}, Rf, {theta - dtheta, theta + dtheta}],
    With[{r =
       0.5*Rf*Sqrt[(Cos[theta + dtheta] -
             Cos[theta - dtheta])^2 + (Sin[theta + dtheta] -
             Sin[theta - dtheta])^2]},
     With[{R = Sqrt[Rf^2 - r^2]},
      If[a == 0, Circle[{0, 0}, Rf, {theta - dtheta, theta + dtheta}],
        If[dtheta <= Pi/2,
        Rotate[Circle[{R*Cos[theta],
           R*Sin[theta]}, {r, (Rf - R + a)}, {0,
           Pi}], -(Pi/2 - theta), {R*Cos[theta], R*Sin[theta]}],
        Rotate[Circle[{0,
           0}, {0.5*Rf*
            Sqrt[(Cos[theta + 0.5*Pi] -
                 Cos[theta - 0.5*Pi])^2 + (Sin[theta + 0.5*Pi] -
                 Sin[theta - 0.5*Pi])^2], Rf + a}, {0,
           Pi}], -(Pi/2 - theta), {0, 0}]]]]],
    Text[Style["\[Theta]", 12, Black, Bold], {Rf*Cos[theta/2]/(3*1.5),
       Rf*Sin[theta/2]/(3*1.5)}],
    Text[Style["\[CapitalDelta]\[Theta]", 12, Black,
      Bold], {2*Rf*Cos[theta - dtheta/2]/(3*1.25),
      2*Rf*Sin[theta - dtheta/2]/(3*1.25)}],
    Text[Style["\[CapitalDelta]\[Theta]", 12, Black,
      Bold], {2*Rf*Cos[theta + dtheta/2]/(3*1.25),
      2*Rf*Sin[theta + dtheta/2]/(3*1.25)}],
    Text[Style[Subscript[R, f], 12, Black,
      Bold], {3*Rf*Cos[1.1*theta]/(3*1.25),
      3*Rf*Sin[1.1*theta]/(3*1.25)}],
    Text[Style[Subscript[\[CapitalOmega], m], 12, Black,
      Bold], {1.075*Rf*Cos[220 Degree], 1.075*Rf*Sin[220 Degree]}],
    Text[Style[Subscript[\[CapitalOmega], f], 12, Black,
      Bold], {0.75*Rf*Cos[205 Degree], 0.75*Rf*Sin[205 Degree]}],
    Text[Style[Subscript[\[CapitalGamma], 1], 12, Black,
      Bold], {1.075*Rf*Cos[255 Degree], 1.075*Rf*Sin[255 Degree]}],
    Text[Style[Subscript[\[CapitalGamma], 2], 12, Black,
      Bold], {0.95*Rf*Cos[theta - dtheta/2],
      0.95*Rf*Sin[theta - dtheta/2]}],
    Text[Style[Subscript[\[CapitalGamma], 3], 12, Black,
      Bold], {(1.075*Rf + a)*Cos[theta + dtheta/2], (1.075*Rf + a)*
       Sin[theta + dtheta/2]}],
    Text[Style["O", 12, Black, Bold], {-0.05, -0.05}],
    Text[Style["l", 12, Black, Bold], {-0.5*l, 0.95*l}],
    Text[Style["l", 12, Black, Bold], {0.5*l, 0.95*l}],
    Text[Style["l", 12, Black, Bold], {-0.95*l, 0.5*l}],
    Text[Style["l", 12, Black, Bold], {-0.95*l, -0.5*l}],
    Text[Style[Subscript[\[CapitalOmega], "b,[0\[Degree]]"], 12,
      Black, Bold], {-0.5*l, -l - 0.5*tratio*l}], Black, Thin,
    Table[{Arrow[{{-l, -l - tratio*l + i}, {-l - arrlength1*l, -l -
          tratio*l + i}}],
      Arrow[{{l, -l - tratio*l + i}, {l + arrlength1*l, -l -
          tratio*l + i}}]}, {i,
      0, (2*l + tratio*l), (2*l + tratio*l)/(arr1 - 1)}],
    Thickness[0.00001],
    Line[{{-l - arrlength1*l, -(l + tratio*l)}, {-l - arrlength1*l,
       l}}], Line[{{+l + arrlength1*l, -(l + tratio*l)}, {+l +
        arrlength1*l, l}}],
    Line[{{-l, -l}, {-l, -l - tratio*l}, {l, -l -
        tratio*l}, {l, -l}}], DotDashed, Blue, Thickness[0.006],
    Line[{{-(1 + 1.5*arrwidth1)*l, -(1 + tratio)*
        l}, {(1 + 1.5*arrwidth1)*l, -(1 + tratio)*l}}]}, Axes -> True,
    AxesLabel -> {x, z}, AspectRatio -> 1, ImageSize -> ImgSize]]

plotOuterBoundedCohesiveGeometry[Rf_, Vff_, tratio_, theta_, dtheta_,
  a_, arrwidth1_, arrlength1_, arr1_, arr2_, ImgSize_] :=
 With[{l = 0.5*Rf*Sqrt[Pi/Vff]},
  Graphics[{Opacity[1], Black, Circle[{0, 0}, Rf],
    Line[{{-l, l}, {-l, -l}}], Line[{{l, -l}, {l, l}}],
    Line[{{0, 0}, {Rf*Cos[theta], Rf*Sin[theta]}}],
    Line[{{-l, -l}, {l, -l}}], Line[{{l, l}, {-l, l}}], Green,
    Circle[{0, 0}, Rf, {0, 2*Pi}],
    With[{r =
       0.5*Rf*Sqrt[(Cos[theta + dtheta] -
             Cos[theta - dtheta])^2 + (Sin[theta + dtheta] -
             Sin[theta - dtheta])^2]},
     With[{R = Sqrt[Rf^2 - r^2]},
      If[a == 0, Circle[{0, 0}, Rf, {theta - dtheta, theta + dtheta}],
        If[dtheta <= Pi/2,
        Rotate[Circle[{R*Cos[theta],
           R*Sin[theta]}, {r, (Rf - R + a)}, {0,
           Pi}], -(Pi/2 - theta), {R*Cos[theta], R*Sin[theta]}],
        Rotate[Circle[{0,
           0}, {0.5*Rf*
            Sqrt[(Cos[theta + 0.5*Pi] -
                 Cos[theta - 0.5*Pi])^2 + (Sin[theta + 0.5*Pi] -
                 Sin[theta - 0.5*Pi])^2], Rf + a}, {0,
           Pi}], -(Pi/2 - theta), {0, 0}]]]]],
    Text[Style[Subscript[R, f], 12, Black,
      Bold], {3*Rf*Cos[1.1*theta]/(3*1.25),
      3*Rf*Sin[1.1*theta]/(3*1.25)}],
    Text[Style[Subscript[\[CapitalOmega], m], 12, Black,
      Bold], {1.075*Rf*Cos[220 Degree], 1.075*Rf*Sin[220 Degree]}],
    Text[Style[Subscript[\[CapitalOmega], f], 12, Black,
      Bold], {0.75*Rf*Cos[205 Degree], 0.75*Rf*Sin[205 Degree]}],
    Text[Style["O", 12, Black, Bold], {-0.05, -0.05}],
    Text[Style["l", 12, Black, Bold], {-0.5*l, 0.95*l}],
    Text[Style["l", 12, Black, Bold], {0.5*l, 0.95*l}],
    Text[Style["l", 12, Black, Bold], {-0.95*l, 0.5*l}],
    Text[Style["l", 12, Black, Bold], {-0.95*l, -0.5*l}],
    Text[Style[Subscript[\[CapitalOmega], "b,[0\[Degree]]"], 12,
      Black, Bold], {-0.5*l, -l - 0.5*tratio*l}], Black, Thin,
    Table[{Arrow[{{-l, -l - tratio*l + i}, {-l - arrlength1*l, -l -
          tratio*l + i}}],
      Arrow[{{l, -l - tratio*l + i}, {l + arrlength1*l, -l -
          tratio*l + i}}]}, {i,
      0, (2*l + tratio*l), (2*l + tratio*l)/(arr1 - 1)}],
    Thickness[0.00001],
    Line[{{-l - arrlength1*l, -(l + tratio*l)}, {-l - arrlength1*l,
       l}}], Line[{{+l + arrlength1*l, -(l + tratio*l)}, {+l +
        arrlength1*l, l}}],
    Line[{{-l, -l}, {-l, -l - tratio*l}, {l, -l -
        tratio*l}, {l, -l}}]}, Axes -> True, AxesLabel -> {x, z},
   AspectRatio -> 1, ImageSize -> ImgSize]]

plotOuterBoundedCohesiveSymmGeometry[Rf_, Vff_, tratio_, theta_,
  dtheta_, a_, arrwidth1_, arrlength1_, arr1_, arr2_, ImgSize_] :=
 With[{l = 0.5*Rf*Sqrt[Pi/Vff]},
  Graphics[{Opacity[1], Black, Circle[{0, 0}, Rf],
    Line[{{-l, l}, {-l, -l}}], Line[{{l, -l}, {l, l}}],
    Line[{{0, 0}, {Rf*Cos[theta], Rf*Sin[theta]}}],
    Line[{{-l, -l}, {l, -l}}], Line[{{l, l}, {-l, l}}], Green,
    Circle[{0, 0}, Rf, {0, 2*Pi}],
    With[{r =
       0.5*Rf*Sqrt[(Cos[theta + dtheta] -
             Cos[theta - dtheta])^2 + (Sin[theta + dtheta] -
             Sin[theta - dtheta])^2]},
     With[{R = Sqrt[Rf^2 - r^2]},
      If[a == 0, Circle[{0, 0}, Rf, {theta - dtheta, theta + dtheta}],
        If[dtheta <= Pi/2,
        Rotate[Circle[{R*Cos[theta],
           R*Sin[theta]}, {r, (Rf - R + a)}, {0,
           Pi}], -(Pi/2 - theta), {R*Cos[theta], R*Sin[theta]}],
        Rotate[Circle[{0,
           0}, {0.5*Rf*
            Sqrt[(Cos[theta + 0.5*Pi] -
                 Cos[theta - 0.5*Pi])^2 + (Sin[theta + 0.5*Pi] -
                 Sin[theta - 0.5*Pi])^2], Rf + a}, {0,
           Pi}], -(Pi/2 - theta), {0, 0}]]]]],
    Text[Style[Subscript[R, f], 12, Black,
      Bold], {3*Rf*Cos[1.1*theta]/(3*1.25),
      3*Rf*Sin[1.1*theta]/(3*1.25)}],
    Text[Style[Subscript[\[CapitalOmega], m], 12, Black,
      Bold], {1.075*Rf*Cos[220 Degree], 1.075*Rf*Sin[220 Degree]}],
    Text[Style[Subscript[\[CapitalOmega], f], 12, Black,
      Bold], {0.75*Rf*Cos[205 Degree], 0.75*Rf*Sin[205 Degree]}],
    Text[Style["O", 12, Black, Bold], {-0.05, -0.05}],
    Text[Style["l", 12, Black, Bold], {-0.5*l, 0.95*l}],
    Text[Style["l", 12, Black, Bold], {0.5*l, 0.95*l}],
    Text[Style["l", 12, Black, Bold], {-0.95*l, 0.5*l}],
    Text[Style["l", 12, Black, Bold], {-0.95*l, -0.5*l}],
    Text[Style[Subscript[\[CapitalOmega], "b,[0\[Degree]]"], 12,
      Black, Bold], {-0.5*l, -l - 0.5*tratio*l}], Black, Thin,
    Table[{Arrow[{{-l, -l - tratio*l + i}, {-l - arrlength1*l, -l -
          tratio*l + i}}],
      Arrow[{{l, -l - tratio*l + i}, {l + arrlength1*l, -l -
          tratio*l + i}}]}, {i,
      0, (2*l + tratio*l), (2*l + tratio*l)/(arr1 - 1)}],
    Thickness[0.00001],
    Line[{{-l - arrlength1*l, -(l + tratio*l)}, {-l - arrlength1*l,
       l}}], Line[{{+l + arrlength1*l, -(l + tratio*l)}, {+l +
        arrlength1*l, l}}],
    Line[{{-l, -l}, {-l, -l - tratio*l}, {l, -l -
        tratio*l}, {l, -l}}], DotDashed, Blue, Thickness[0.006],
    Line[{{-(1 + 1.5*arrwidth1)*l, -(1 + tratio)*
        l}, {(1 + 1.5*arrwidth1)*l, -(1 + tratio)*l}}]}, Axes -> True,
    AxesLabel -> {x, z}, AspectRatio -> 1, ImageSize -> ImgSize]]

(* :2D TPM Tests: Mesh Plotting:  *)

plotSingleMesh[Rf_, Vff_, theta_, dtheta_, f1_, f2_, f3_, ImgSize_] :=
  With[{l = 0.5*Rf*Sqrt[Pi/Vff]},
  Graphics[{Black, Circle[{0, 0}, Rf],
    Line[{{-l, -l}, {l, -l}, {l, l}, {-l, l}, {-l, -l}}], DotDashed,
    Line[{{-f1*Rf, -f1*Rf}, {f1*Rf, -f1*Rf}, {f1*Rf, f1*Rf}, {-f1*Rf,
       f1*Rf}, {-f1*Rf, -f1*Rf}}], Circle[{0, 0}, f2*Rf],
    Circle[{0, 0}, f3*Rf], Line[{{-f1*Rf, -f1*Rf}, {-l, -l}}],
    Line[{{-f1*Rf, f1*Rf}, {-l, l}}], Line[{{f1*Rf, f1*Rf}, {l, l}}],
    Line[{{f1*Rf, -f1*Rf}, {l, -l}}], Thick, AbsoluteDashing[{}], Red,
     Circle[{0, 0}, Rf, {theta - dtheta, theta + dtheta}],
    Text[Style[Subscript[N, \[Alpha]], 12, Black,
      Bold], {0.5*f1*Rf, -1.1*f1*Rf}],
    Text[Style[Subscript[N, \[Beta]], 12, Black,
      Bold], {f1*Rf + 0.95*0.5*(f2*Cos[45 Degree] - f1)*Rf, -f1*Rf -
       1.35*0.5*(f2*Cos[45 Degree] - f1)*Rf}],
    Text[Style[Subscript[N, \[Gamma]], 12, Black,
      Bold], {f2*Cos[45 Degree]*Rf +
       0.95*0.5*(1 - f2)*Cos[45 Degree]*Rf, -f2*Cos[45 Degree]*Rf -
       1.35*0.5*(1 - f2)*Cos[45 Degree]*Rf}],
    Text[Style[Subscript[N, \[Delta]], 12, Black,
      Bold], {Cos[45 Degree]*Rf +
       0.95*0.5*(f3 - 1)*Cos[45 Degree]*Rf, -Cos[45 Degree]*Rf -
       1.45*0.5*(f3 - 1)*Cos[45 Degree]*Rf}],
    Text[Style[Subscript[N, \[Epsilon]], 12, Black,
      Bold], {f3*Rf*Cos[45 Degree] +
       0.95*0.5*(l - f3*Rf*Cos[45 Degree]), -(f3*Rf*Cos[45 Degree] +
         1.1*0.5*(l - f3*Rf*Cos[45 Degree]))}]}, Axes -> True,
   AxesLabel -> {x, z}, AspectRatio -> 1, ImageSize -> ImgSize]]

plotSingleCohesiveMesh[Rf_, Vff_, theta_, dtheta_, f1_, f2_, f3_,
  ImgSize_] :=
 With[{l = 0.5*Rf*Sqrt[Pi/Vff]},
  Graphics[{Black, Circle[{0, 0}, Rf],
    Line[{{-l, -l}, {l, -l}, {l, l}, {-l, l}, {-l, -l}}], DotDashed,
    Line[{{-f1*Rf, -f1*Rf}, {f1*Rf, -f1*Rf}, {f1*Rf, f1*Rf}, {-f1*Rf,
       f1*Rf}, {-f1*Rf, -f1*Rf}}], Circle[{0, 0}, f2*Rf],
    Circle[{0, 0}, f3*Rf], Line[{{-f1*Rf, -f1*Rf}, {-l, -l}}],
    Line[{{-f1*Rf, f1*Rf}, {-l, l}}], Line[{{f1*Rf, f1*Rf}, {l, l}}],
    Line[{{f1*Rf, -f1*Rf}, {l, -l}}], Thick, AbsoluteDashing[{}],
    Green, Circle[{0, 0}, Rf, {0, 2*Pi}],
    Text[Style[Subscript[N, \[Alpha]], 12, Black,
      Bold], {0.5*f1*Rf, -1.1*f1*Rf}],
    Text[Style[Subscript[N, \[Beta]], 12, Black,
      Bold], {f1*Rf + 0.95*0.5*(f2*Cos[45 Degree] - f1)*Rf, -f1*Rf -
       1.35*0.5*(f2*Cos[45 Degree] - f1)*Rf}],
    Text[Style[Subscript[N, \[Gamma]], 12, Black,
      Bold], {f2*Cos[45 Degree]*Rf +
       0.95*0.5*(1 - f2)*Cos[45 Degree]*Rf, -f2*Cos[45 Degree]*Rf -
       1.35*0.5*(1 - f2)*Cos[45 Degree]*Rf}],
    Text[Style[Subscript[N, \[Delta]], 12, Black,
      Bold], {Cos[45 Degree]*Rf +
       0.95*0.5*(f3 - 1)*Cos[45 Degree]*Rf, -Cos[45 Degree]*Rf -
       1.45*0.5*(f3 - 1)*Cos[45 Degree]*Rf}],
    Text[Style[Subscript[N, \[Epsilon]], 12, Black,
      Bold], {f3*Rf*Cos[45 Degree] +
       0.95*0.5*(l - f3*Rf*Cos[45 Degree]), -(f3*Rf*Cos[45 Degree] +
         1.1*0.5*(l - f3*Rf*Cos[45 Degree]))}]}, Axes -> True,
   AxesLabel -> {x, z}, AspectRatio -> 1, ImageSize -> ImgSize]]

plotBoundedMesh[Rf_, Vff_, tratio_, theta_, dtheta_, f1_, f2_, f3_,
  ImgSize_] :=
 With[{l = 0.5*Rf*Sqrt[Pi/Vff]},
  Graphics[{Black, Circle[{0, 0}, Rf],
    Line[{{-l, -l}, {l, -l}, {l, l}, {-l, l}, {-l, -l}}],
    Line[{{-l, l}, {-l, l + tratio*l}, {l, l + tratio*l}, {l, l}}],
    Line[{{-l, -l}, {-l, -l - tratio*l}, {l, -l -
        tratio*l}, {l, -l}}], DotDashed,
    Line[{{-f1*Rf, -f1*Rf}, {f1*Rf, -f1*Rf}, {f1*Rf, f1*Rf}, {-f1*Rf,
       f1*Rf}, {-f1*Rf, -f1*Rf}}], Circle[{0, 0}, f2*Rf],
    Circle[{0, 0}, f3*Rf], Line[{{-f1*Rf, -f1*Rf}, {-l, -l}}],
    Line[{{-f1*Rf, f1*Rf}, {-l, l}}], Line[{{f1*Rf, f1*Rf}, {l, l}}],
    Line[{{f1*Rf, -f1*Rf}, {l, -l}}], Thick, AbsoluteDashing[{}], Red,
     Circle[{0, 0}, Rf, {theta - dtheta, theta + dtheta}],
    Text[Style[Subscript[N, \[Alpha]], 12, Black,
      Bold], {0.5*f1*Rf, -1.1*f1*Rf}],
    Text[Style[Subscript[N, \[Beta]], 12, Black,
      Bold], {f1*Rf + 0.95*0.5*(f2*Cos[45 Degree] - f1)*Rf, -f1*Rf -
       1.35*0.5*(f2*Cos[45 Degree] - f1)*Rf}],
    Text[Style[Subscript[N, \[Gamma]], 12, Black,
      Bold], {f2*Cos[45 Degree]*Rf +
       0.95*0.5*(1 - f2)*Cos[45 Degree]*Rf, -f2*Cos[45 Degree]*Rf -
       1.35*0.5*(1 - f2)*Cos[45 Degree]*Rf}],
    Text[Style[Subscript[N, \[Delta]], 12, Black,
      Bold], {Cos[45 Degree]*Rf +
       0.95*0.5*(f3 - 1)*Cos[45 Degree]*Rf, -Cos[45 Degree]*Rf -
       1.45*0.5*(f3 - 1)*Cos[45 Degree]*Rf}],
    Text[Style[Subscript[N, \[Epsilon]], 12, Black,
      Bold], {f3*Rf*Cos[45 Degree] +
       0.95*0.5*(l - f3*Rf*Cos[45 Degree]), -(f3*Rf*Cos[45 Degree] +
         1.1*0.5*(l - f3*Rf*Cos[45 Degree]))}],
    Text[Style[Subscript[N, \[Zeta]], 12, Black,
      Bold], {0.95*l, -l - 0.45*tratio*l}],
    Text[Style[Subscript[N, \[Zeta]], 12, Black,
      Bold], {0.95*l, +l + 0.45*tratio*l}]}, Axes -> True,
   AxesLabel -> {x, z}, AspectRatio -> 1, ImageSize -> ImgSize]]

plotBoundedSymmMesh[Rf_, Vff_, tratio_, theta_, dtheta_, f1_, f2_,
  f3_, ImgSize_] :=
 With[{l = 0.5*Rf*Sqrt[Pi/Vff]},
  Graphics[{Black, Circle[{0, 0}, Rf],
    Line[{{-l, -l}, {l, -l}, {l, l}, {-l, l}, {-l, -l}}],
    Line[{{-l, l}, {-l, l + tratio*l}, {l, l + tratio*l}, {l, l}}],
    DotDashed,
    Line[{{-f1*Rf, -f1*Rf}, {f1*Rf, -f1*Rf}, {f1*Rf, f1*Rf}, {-f1*Rf,
       f1*Rf}, {-f1*Rf, -f1*Rf}}], Circle[{0, 0}, f2*Rf],
    Circle[{0, 0}, f3*Rf], Line[{{-f1*Rf, -f1*Rf}, {-l, -l}}],
    Line[{{-f1*Rf, f1*Rf}, {-l, l}}], Line[{{f1*Rf, f1*Rf}, {l, l}}],
    Line[{{f1*Rf, -f1*Rf}, {l, -l}}], Thick, AbsoluteDashing[{}], Red,
     Circle[{0, 0}, Rf, {theta - dtheta, theta + dtheta}],
    Text[Style[Subscript[N, \[Alpha]], 12, Black,
      Bold], {0.5*f1*Rf, -1.1*f1*Rf}],
    Text[Style[Subscript[N, \[Beta]], 12, Black,
      Bold], {f1*Rf + 0.95*0.5*(f2*Cos[45 Degree] - f1)*Rf, -f1*Rf -
       1.35*0.5*(f2*Cos[45 Degree] - f1)*Rf}],
    Text[Style[Subscript[N, \[Gamma]], 12, Black,
      Bold], {f2*Cos[45 Degree]*Rf +
       0.95*0.5*(1 - f2)*Cos[45 Degree]*Rf, -f2*Cos[45 Degree]*Rf -
       1.35*0.5*(1 - f2)*Cos[45 Degree]*Rf}],
    Text[Style[Subscript[N, \[Delta]], 12, Black,
      Bold], {Cos[45 Degree]*Rf +
       0.95*0.5*(f3 - 1)*Cos[45 Degree]*Rf, -Cos[45 Degree]*Rf -
       1.45*0.5*(f3 - 1)*Cos[45 Degree]*Rf}],
    Text[Style[Subscript[N, \[Epsilon]], 12, Black,
      Bold], {f3*Rf*Cos[45 Degree] +
       0.95*0.5*(l - f3*Rf*Cos[45 Degree]), -(f3*Rf*Cos[45 Degree] +
         1.1*0.5*(l - f3*Rf*Cos[45 Degree]))}],
    Text[Style[Subscript[N, \[Zeta]], 12, Black,
      Bold], {0.95*l, +l + 0.45*tratio*l}]}, Axes -> True,
   AxesLabel -> {x, z}, AspectRatio -> 1, ImageSize -> ImgSize]]

plotBoundedCohesiveMesh[Rf_, Vff_, tratio_, theta_, dtheta_, f1_, f2_,
   f3_, ImgSize_] :=
 With[{l = 0.5*Rf*Sqrt[Pi/Vff]},
  Graphics[{Black, Circle[{0, 0}, Rf],
    Line[{{-l, -l}, {l, -l}, {l, l}, {-l, l}, {-l, -l}}],
    Line[{{-l, l}, {-l, l + tratio*l}, {l, l + tratio*l}, {l, l}}],
    Line[{{-l, -l}, {-l, -l - tratio*l}, {l, -l -
        tratio*l}, {l, -l}}], DotDashed,
    Line[{{-f1*Rf, -f1*Rf}, {f1*Rf, -f1*Rf}, {f1*Rf, f1*Rf}, {-f1*Rf,
       f1*Rf}, {-f1*Rf, -f1*Rf}}], Circle[{0, 0}, f2*Rf],
    Circle[{0, 0}, f3*Rf], Line[{{-f1*Rf, -f1*Rf}, {-l, -l}}],
    Line[{{-f1*Rf, f1*Rf}, {-l, l}}], Line[{{f1*Rf, f1*Rf}, {l, l}}],
    Line[{{f1*Rf, -f1*Rf}, {l, -l}}], Thick, AbsoluteDashing[{}],
    Green, Circle[{0, 0}, Rf, {0, 2*Pi}],
    Text[Style[Subscript[N, \[Alpha]], 12, Black,
      Bold], {0.5*f1*Rf, -1.1*f1*Rf}],
    Text[Style[Subscript[N, \[Beta]], 12, Black,
      Bold], {f1*Rf + 0.95*0.5*(f2*Cos[45 Degree] - f1)*Rf, -f1*Rf -
       1.35*0.5*(f2*Cos[45 Degree] - f1)*Rf}],
    Text[Style[Subscript[N, \[Gamma]], 12, Black,
      Bold], {f2*Cos[45 Degree]*Rf +
       0.95*0.5*(1 - f2)*Cos[45 Degree]*Rf, -f2*Cos[45 Degree]*Rf -
       1.35*0.5*(1 - f2)*Cos[45 Degree]*Rf}],
    Text[Style[Subscript[N, \[Delta]], 12, Black,
      Bold], {Cos[45 Degree]*Rf +
       0.95*0.5*(f3 - 1)*Cos[45 Degree]*Rf, -Cos[45 Degree]*Rf -
       1.45*0.5*(f3 - 1)*Cos[45 Degree]*Rf}],
    Text[Style[Subscript[N, \[Epsilon]], 12, Black,
      Bold], {f3*Rf*Cos[45 Degree] +
       0.95*0.5*(l - f3*Rf*Cos[45 Degree]), -(f3*Rf*Cos[45 Degree] +
         1.1*0.5*(l - f3*Rf*Cos[45 Degree]))}],
    Text[Style[Subscript[N, \[Zeta]], 12, Black,
      Bold], {0.95*l, -l - 0.45*tratio*l}],
    Text[Style[Subscript[N, \[Zeta]], 12, Black,
      Bold], {0.95*l, +l + 0.45*tratio*l}]}, Axes -> True,
   AxesLabel -> {x, z}, AspectRatio -> 1, ImageSize -> ImgSize]]

plotBoundedCohesiveSymmMesh[Rf_, Vff_, tratio_, theta_, dtheta_, f1_,
  f2_, f3_, ImgSize_] :=
 With[{l = 0.5*Rf*Sqrt[Pi/Vff]},
  Graphics[{Black, Circle[{0, 0}, Rf],
    Line[{{-l, -l}, {l, -l}, {l, l}, {-l, l}, {-l, -l}}],
    Line[{{-l, l}, {-l, l + tratio*l}, {l, l + tratio*l}, {l, l}}],
    DotDashed,
    Line[{{-f1*Rf, -f1*Rf}, {f1*Rf, -f1*Rf}, {f1*Rf, f1*Rf}, {-f1*Rf,
       f1*Rf}, {-f1*Rf, -f1*Rf}}], Circle[{0, 0}, f2*Rf],
    Circle[{0, 0}, f3*Rf], Line[{{-f1*Rf, -f1*Rf}, {-l, -l}}],
    Line[{{-f1*Rf, f1*Rf}, {-l, l}}], Line[{{f1*Rf, f1*Rf}, {l, l}}],
    Line[{{f1*Rf, -f1*Rf}, {l, -l}}], Thick, AbsoluteDashing[{}],
    Green, Circle[{0, 0}, Rf, {0, 2*Pi}],
    Text[Style[Subscript[N, \[Alpha]], 12, Black,
      Bold], {0.5*f1*Rf, -1.1*f1*Rf}],
    Text[Style[Subscript[N, \[Beta]], 12, Black,
      Bold], {f1*Rf + 0.95*0.5*(f2*Cos[45 Degree] - f1)*Rf, -f1*Rf -
       1.35*0.5*(f2*Cos[45 Degree] - f1)*Rf}],
    Text[Style[Subscript[N, \[Gamma]], 12, Black,
      Bold], {f2*Cos[45 Degree]*Rf +
       0.95*0.5*(1 - f2)*Cos[45 Degree]*Rf, -f2*Cos[45 Degree]*Rf -
       1.35*0.5*(1 - f2)*Cos[45 Degree]*Rf}],
    Text[Style[Subscript[N, \[Delta]], 12, Black,
      Bold], {Cos[45 Degree]*Rf +
       0.95*0.5*(f3 - 1)*Cos[45 Degree]*Rf, -Cos[45 Degree]*Rf -
       1.45*0.5*(f3 - 1)*Cos[45 Degree]*Rf}],
    Text[Style[Subscript[N, \[Epsilon]], 12, Black,
      Bold], {f3*Rf*Cos[45 Degree] +
       0.95*0.5*(l - f3*Rf*Cos[45 Degree]), -(f3*Rf*Cos[45 Degree] +
         1.1*0.5*(l - f3*Rf*Cos[45 Degree]))}],
    Text[Style[Subscript[N, \[Zeta]], 12, Black,
      Bold], {0.95*l, +l + 0.45*tratio*l}]}, Axes -> True,
   AxesLabel -> {x, z}, AspectRatio -> 1, ImageSize -> ImgSize]]

plotOuterBoundedMesh[Rf_, Vff_, tratio_, theta_, dtheta_, f1_, f2_,
  f3_, ImgSize_] :=
 With[{l = 0.5*Rf*Sqrt[Pi/Vff]},
  Graphics[{Black, Circle[{0, 0}, Rf],
    Line[{{-l, -l}, {l, -l}, {l, l}, {-l, l}, {-l, -l}}],
    Line[{{-l, -l}, {-l, -l - tratio*l}, {l, -l -
        tratio*l}, {l, -l}}], DotDashed,
    Line[{{-f1*Rf, -f1*Rf}, {f1*Rf, -f1*Rf}, {f1*Rf, f1*Rf}, {-f1*Rf,
       f1*Rf}, {-f1*Rf, -f1*Rf}}], Circle[{0, 0}, f2*Rf],
    Circle[{0, 0}, f3*Rf], Line[{{-f1*Rf, -f1*Rf}, {-l, -l}}],
    Line[{{-f1*Rf, f1*Rf}, {-l, l}}], Line[{{f1*Rf, f1*Rf}, {l, l}}],
    Line[{{f1*Rf, -f1*Rf}, {l, -l}}], Thick, AbsoluteDashing[{}], Red,
     Circle[{0, 0}, Rf, {theta - dtheta, theta + dtheta}],
    Text[Style[Subscript[N, \[Alpha]], 12, Black,
      Bold], {0.5*f1*Rf, -1.1*f1*Rf}],
    Text[Style[Subscript[N, \[Beta]], 12, Black,
      Bold], {f1*Rf + 0.95*0.5*(f2*Cos[45 Degree] - f1)*Rf, -f1*Rf -
       1.35*0.5*(f2*Cos[45 Degree] - f1)*Rf}],
    Text[Style[Subscript[N, \[Gamma]], 12, Black,
      Bold], {f2*Cos[45 Degree]*Rf +
       0.95*0.5*(1 - f2)*Cos[45 Degree]*Rf, -f2*Cos[45 Degree]*Rf -
       1.35*0.5*(1 - f2)*Cos[45 Degree]*Rf}],
    Text[Style[Subscript[N, \[Delta]], 12, Black,
      Bold], {Cos[45 Degree]*Rf +
       0.95*0.5*(f3 - 1)*Cos[45 Degree]*Rf, -Cos[45 Degree]*Rf -
       1.45*0.5*(f3 - 1)*Cos[45 Degree]*Rf}],
    Text[Style[Subscript[N, \[Epsilon]], 12, Black,
      Bold], {f3*Rf*Cos[45 Degree] +
       0.95*0.5*(l - f3*Rf*Cos[45 Degree]), -(f3*Rf*Cos[45 Degree] +
         1.1*0.5*(l - f3*Rf*Cos[45 Degree]))}],
    Text[Style[Subscript[N, \[Zeta]], 12, Black,
      Bold], {0.95*l, -l - 0.45*tratio*l}]}, Axes -> True,
   AxesLabel -> {x, z}, AspectRatio -> 1, ImageSize -> ImgSize]]

plotOuterBoundedCohesiveMesh[Rf_, Vff_, tratio_, theta_, dtheta_, f1_,
   f2_, f3_, ImgSize_] :=
 With[{l = 0.5*Rf*Sqrt[Pi/Vff]},
  Graphics[{Black, Circle[{0, 0}, Rf],
    Line[{{-l, -l}, {l, -l}, {l, l}, {-l, l}, {-l, -l}}],
    Line[{{-l, -l}, {-l, -l - tratio*l}, {l, -l -
        tratio*l}, {l, -l}}], DotDashed,
    Line[{{-f1*Rf, -f1*Rf}, {f1*Rf, -f1*Rf}, {f1*Rf, f1*Rf}, {-f1*Rf,
       f1*Rf}, {-f1*Rf, -f1*Rf}}], Circle[{0, 0}, f2*Rf],
    Circle[{0, 0}, f3*Rf], Line[{{-f1*Rf, -f1*Rf}, {-l, -l}}],
    Line[{{-f1*Rf, f1*Rf}, {-l, l}}], Line[{{f1*Rf, f1*Rf}, {l, l}}],
    Line[{{f1*Rf, -f1*Rf}, {l, -l}}], Thick, AbsoluteDashing[{}],
    Green, Circle[{0, 0}, Rf, {0, 2*Pi}],
    Text[Style[Subscript[N, \[Alpha]], 12, Black,
      Bold], {0.5*f1*Rf, -1.1*f1*Rf}],
    Text[Style[Subscript[N, \[Beta]], 12, Black,
      Bold], {f1*Rf + 0.95*0.5*(f2*Cos[45 Degree] - f1)*Rf, -f1*Rf -
       1.35*0.5*(f2*Cos[45 Degree] - f1)*Rf}],
    Text[Style[Subscript[N, \[Gamma]], 12, Black,
      Bold], {f2*Cos[45 Degree]*Rf +
       0.95*0.5*(1 - f2)*Cos[45 Degree]*Rf, -f2*Cos[45 Degree]*Rf -
       1.35*0.5*(1 - f2)*Cos[45 Degree]*Rf}],
    Text[Style[Subscript[N, \[Delta]], 12, Black,
      Bold], {Cos[45 Degree]*Rf +
       0.95*0.5*(f3 - 1)*Cos[45 Degree]*Rf, -Cos[45 Degree]*Rf -
       1.45*0.5*(f3 - 1)*Cos[45 Degree]*Rf}],
    Text[Style[Subscript[N, \[Epsilon]], 12, Black,
      Bold], {f3*Rf*Cos[45 Degree] +
       0.95*0.5*(l - f3*Rf*Cos[45 Degree]), -(f3*Rf*Cos[45 Degree] +
         1.1*0.5*(l - f3*Rf*Cos[45 Degree]))}],
    Text[Style[Subscript[N, \[Zeta]], 12, Black,
      Bold], {0.95*l, -l - 0.45*tratio*l}]}, Axes -> True,
   AxesLabel -> {x, z}, AspectRatio -> 1, ImageSize -> ImgSize]]

(* :2D TPM Tests: Matlab Interface and Mesh Details Plotting:  *)

plotMeshDetails[fiberArrangement_, isUpperBounded_, isLowerBounded_,
  isCohesive_, crackType_, element_, order_, optimize_, Rf_, Vff_,
  tratio_, theta_, dtheta_, f1_, f2_, f3_, N1_, N2_, N3_, N4_, N5_,
  N6_, ImgSize_] := (MEvaluate[
   StringJoin[{"clear \
all;[nodes,edges,elements,fiberN,matrixN,part6bot,part6up,fiberEl,\
matrixEl,cohesiveEl,boundedBot,boundedUp,gammaNo1,gammaNo2,gammaNo3,\
gammaNo4,gammaEl1,gammaEl2,gammaEl3,gammaEl4,NintUpNine,NintUpZero,\
NintBotNine,NintBotZero,NintUpNineCorners,NintUpZeroCorners,\
NintBotNineCorners,NintBotZeroCorners,NbotRight,NbotLeft,NupRight,\
NupLeft,EintUpNine,EintUpZero,EintBotNine,EintBotZero,EbotRight,\
EbotLeft,EupRight,EupLeft,Ncorners,Ndown,Nright,Nup,Nleft,Edown,\
Eright,Eup,Eleft]=rve_mesh(", ToString[fiberArrangement], ",",
     ToString[isUpperBounded], ",", ToString[isLowerBounded], ",",
     ToString[isCohesive], ",", ToString[crackType], ",",
     ToString[element], ",", ToString[order], ",", ToString[optimize],
      ",", ToString[Rf], ",", ToString[Vff], ",", ToString[tratio],
     ",", ToString[theta], ",", ToString[dtheta], ",", ToString[f1],
     ",", ToString[f2], ",", ToString[f3], ",", ToString[N1], ",",
     ToString[N2], ",", ToString[N3], ",", ToString[N4], ",",
     ToString[N5], ",", ToString[N6], ");"}]]; nodes = MGet["nodes"];
  edges = MGet["edges"];
  With[{l = 0.5*Rf*Sqrt[Pi/Vff]},
   Graphics[{Point[nodes],
     Table[Line[{nodes[[edges[[i, 1]]]], nodes[[edges[[i, 2]]]]}], {i,
        1, Length[edges], 1}], Thick, Black, Circle[{0, 0}, Rf],
     Line[{{-l, -l}, {l, -l}, {l, l}, {-l, l}, {-l, -l}}],
     AbsoluteDashing[{}], If[isCohesive == 0, Red, Green],
     If[isCohesive == 0,
      Circle[{0, 0}, Rf, {theta - dtheta, theta + dtheta}],
      Circle[{0, 0}, Rf]]}, Axes -> True, AxesLabel -> {x, z},
    AspectRatio -> 1, ImageSize -> ImgSize]])

plotMeshQuality[qualityVar_, qualityName_, fiberArrangement_,
  isUpperBounded_, isLowerBounded_, isCohesive_, crackType_, element_,
   order_, optimize_, Rf_, Vff_, tratio_, theta_, dtheta_, f1_, f2_,
  f3_, N1_, N2_, N3_, N4_, N5_, N6_,
  ImgSize_] := (MEvaluate[
   With[{func =
      If[element == 1,
       If[order == 1,
        "[fshape,minL,maxL,meanL,minAlpha,maxAlpha,meanAlpha,minD,\
maxD,meanD,betas,A,minA,maxA,meanA,e1,e2,e3,e4,f1,f2,f3,f4,ar,skew,Tx,\
Ty,stretch,J,JA] = quad4quality(nodes,elements);deltabeta = \
betas(:,2)-betas(:,1)",
        "[minL,maxL,meanL,minAlpha,maxAlpha,meanAlpha,minD,maxD,meanD,\
betas,A,minA,maxA,meanA,...
                 e1,e2,e3,e4,e5,e6,e7,e8,f1,f2,f3,f4,f5,f6,f7,f8,...
                 ar,skew,Tx,Ty,TD,ND,J,JA] = \
quad8quality(nodes,elements);deltabeta = betas(:,2)-betas(:,1)"],
       If[order == 1,
        "[fshape,minL,maxL,meanL,minAlpha,maxAlpha,meanAlpha,A,minA,\
maxA,meanA,J,JA] = tri3quality(nodes,elements)",
        "[fshape,TD,ND,minL,maxL,meanL,minAlpha,maxAlpha,meanAlpha,A,\
minA,maxA,meanA,J,JA] = tri6quality(nodes,elements)"]]},
    StringJoin[{"clear all; \
[nodes,edges,elements,fiberN,matrixN,part6bot,part6up,fiberEl,\
matrixEl,cohesiveEl,boundedBot,boundedUp,gammaNo1,gammaNo2,gammaNo3,\
gammaNo4,gammaEl1,gammaEl2,gammaEl3,gammaEl4,NintUpNine,NintUpZero,\
NintBotNine,NintBotZero,NintUpNineCorners,NintUpZeroCorners,\
NintBotNineCorners,NintBotZeroCorners,NbotRight,NbotLeft,NupRight,\
NupLeft,EintUpNine,EintUpZero,EintBotNine,EintBotZero,EbotRight,\
EbotLeft,EupRight,EupLeft,Ncorners,Ndown,Nright,Nup,Nleft,Edown,\
Eright,Eup,Eleft]=rve_mesh(", ToString[fiberArrangement], ",",
      ToString[isUpperBounded], ",", ToString[isLowerBounded], ",",
      ToString[isCohesive], ",", ToString[crackType], ",",
      ToString[element], ",", ToString[order], ",",
      ToString[optimize], ",", ToString[Rf], ",", ToString[Vff], ",",
      ToString[tratio], ",", ToString[theta], ",", ToString[dtheta],
      ",", ToString[f1], ",", ToString[f2], ",", ToString[f3], ",",
      ToString[N1], ",", ToString[N2], ",", ToString[N3], ",",
      ToString[N4], ",", ToString[N5], ",", ToString[N6], ");", func,
      ";"}]]]; nodes = MGet["nodes"]; edges = MGet["edges"];
  elements = MGet["elements"];
  qualityField = MGet[qualityVar];
  With[{l = 0.5*Rf*Sqrt[Pi/Vff],
    plotValues =
     Table[{Sum[nodes[[i, 1]], {i, elements[[k, ;;]]}]/
        Length[elements[[k, ;;]]],
       Sum[nodes[[i, 2]], {i, elements[[k, ;;]]}]/
        Length[elements[[k, ;;]]], qualityField[[k ;; 1]]}, {k, 1,
       Length[elements], 1}]},
   Row[{Show[{Graphics[{Thin,
         Table[Line[{nodes[[edges[[i, 1]]]],
            nodes[[edges[[i, 2]]]]}], {i, 1, Length[edges], 1}],
         Black, Circle[{0, 0}, Rf],
         Line[{{-l, -l}, {l, -l}, {l, l}, {-l, l}, {-l, -l}}]}],
       ListDensityPlot[plotValues,
        PlotLegends ->
         Placed[BarLegend[Automatic,
           LegendMargins -> {{0, 0}, {10, 5}},
           LegendLabel -> qualityVar,
           LabelStyle -> {Italic, FontFamily -> "Helvetica"}],
          Above]]}, Axes -> True, AxesLabel -> {x, z},
      AspectRatio -> 1, ImageSize -> ImgSize],
     Histogram[qualityVar, ChartStyle -> Blue,
      ChartLabels -> Placed[{qualityName}, Above]]},
    Alignment -> {Center, Center}]])

(* :2D TPM Tests Interface: inner ply,  interface crack, one fiber (arrangement 1):  *)

TPM2DiPiC01Fgeom[model_, layup_, solver_, Rf_, Vff_, tratio_, theta_,
  dtheta_, a_, arrwidth1_, arrlength1_, arr1_, arr2_, ImgSize_] :=
 If[model == 1,
  If[solver == 1,
   If[layup == 1,
    plotSingleGeometry[Rf, Vff, theta Degree, dtheta Degree, a,
     arrwidth1, arrlength1, arr1, arr2, ImgSize],
    plotSingleSymmGeometry[Rf, Vff, theta Degree, dtheta Degree, a,
     arrwidth1, arrlength1, arr1, arr2, ImgSize]],
   If[layup == 1,
    plotSingleCohesiveGeometry[Rf, Vff, theta Degree, dtheta Degree,
     a, arrwidth1, arrlength1, arr1, arr2, ImgSize],
    plotSingleCohesiveSymmGeometry[Rf, Vff, theta Degree,
     dtheta Degree, a, arrwidth1, arrlength1, arr1, arr2, ImgSize]]],
  If[model == 2,
   If[solver == 1,
    If[layup == 1,
     plotBoundedGeometry[Rf, Vff, tratio, theta Degree, dtheta Degree,
       a, arrwidth1, arrlength1, arr1, arr2, ImgSize],
     plotBoundedSymmGeometry[Rf, Vff, tratio, theta Degree,
      dtheta Degree, a, arrwidth1, arrlength1, arr1, arr2, ImgSize]],
    If[layup == 1,
     plotBoundedCohesiveGeometry[Rf, Vff, tratio, theta Degree,
      dtheta Degree, a, arrwidth1, arrlength1, arr1, arr2, ImgSize],
     plotBoundedCohesiveSymmGeometry[Rf, Vff, tratio, theta Degree,
      dtheta Degree, a, arrwidth1, arrlength1, arr1, arr2, ImgSize]]],
    If[solver == 1,
    plotPeriodicGeometry[Rf, Vff, theta Degree, dtheta Degree, a,
     arrwidth1, arrlength1, arr1, arr2, ImgSize],
    plotPeriodicCohesiveGeometry[Rf, Vff, theta Degree, dtheta Degree,
      a, arrwidth1, arrlength1, arr1, arr2, ImgSize]]]]

TPM2DiPiC01Fmesh[model_, layup_, solver_, showmesh_, eltype_,
  elorder_, optimised_, Rf_, Vff_, tratio_, theta_, dtheta_, a_,
  arrwidth1_, arrlength1_, arr1_, arr2_, f1_, f2_, f3_, N1_, N2_, N3_,
   N4_, N5_, N6_, ImgSize_] :=
 If[model == 2,
  If[solver == 1,
   If[showmesh == 0,
    If[layup == 1,
     plotBoundedMesh[Rf, Vff, tratio, theta Degree, dtheta Degree, f1,
       f2, f3, ImgSize],
     plotBoundedSymmMesh[Rf, Vff, tratio, theta Degree, dtheta Degree,
       f1, f2, f3, ImgSize]],
    With[{fiberArrangement = 1, isUpperBounded = 1,
      isLowerBounded = If[layup == 1, 1, 0], isCohesive = 0,
      crackType = 1},
     plotMeshDetails[fiberArrangement, isUpperBounded, isLowerBounded,
       isCohesive, crackType, eltype, elorder, optimised, Rf, Vff,
      tratio, N[theta Degree], N[dtheta Degree], f1, f2, f3, N1, N2,
      N3, N4, N5, N6, ImgSize]]],
   If[showmesh == 0,
    If[layup == 1,
     plotBoundedCohesiveMesh[Rf, Vff, tratio, theta Degree,
      dtheta Degree, f1, f2, f3, ImgSize],
     plotBoundedCohesiveSymmMesh[Rf, Vff, tratio, theta Degree,
      dtheta Degree, f1, f2, f3, ImgSize]],
    With[{fiberArrangement = 1, isUpperBounded = 1,
      isLowerBounded = If[layup == 1, 1, 0], isCohesive = 1,
      crackType = 1},
     plotMeshDetails[fiberArrangement, isUpperBounded, isLowerBounded,
       isCohesive, crackType, eltype, elorder, optimised, Rf, Vff,
      tratio, N[theta Degree], N[dtheta Degree], f1, f2, f3, N1, N2,
      N3, N4, N5, N6, ImgSize]]]],
  If[solver == 1,
   If[showmesh == 0,
    plotSingleMesh[Rf, Vff, theta Degree, dtheta Degree, f1, f2, f3,
     ImgSize],
    With[{fiberArrangement = 1, isUpperBounded = 0,
      isLowerBounded = 0, isCohesive = 0, crackType = 1},
     plotMeshDetails[fiberArrangement, isUpperBounded, isLowerBounded,
       isCohesive, crackType, eltype, elorder, optimised, Rf, Vff,
      tratio, N[theta Degree], N[dtheta Degree], f1, f2, f3, N1, N2,
      N3, N4, N5, N6, ImgSize]]],
   If[showmesh == 0,
    plotSingleCohesiveMesh[Rf, Vff, theta Degree, dtheta Degree, f1,
     f2, f3, ImgSize],
    With[{fiberArrangement = 1, isUpperBounded = 0,
      isLowerBounded = 0, isCohesive = 1, crackType = 1},
     plotMeshDetails[fiberArrangement, isUpperBounded, isLowerBounded,
       isCohesive, crackType, eltype, elorder, optimised, Rf, Vff,
      tratio, N[theta Degree], N[dtheta Degree], f1, f2, f3, N1, N2,
      N3, N4, N5, N6, ImgSize]]]]]

TPM2DiPiC01Fmeshquality[model_, layup_, solver_, showmesh_, eltype_,
  elorder_, optimised_, Rf_, Vff_, tratio_, theta_, dtheta_, a_,
  arrwidth1_, arrlength1_, arr1_, arr2_, f1_, f2_, f3_, N1_, N2_, N3_,
   N4_, N5_, N6_, ImgSize_, minL_, maxL_, meanL_, minalpha_,
  maxalpha_, meanalpha_, minD_, maxD_, meanD_, deltabeta_, A_, ar_,
  skew_, Tx_, Ty_, stretch_, fshape_, TD_, TN_, J_, JA_] :=
 If[AnyTrue[{minL, maxL, meanL, minalpha, maxalpha, meanalpha, minD,
    maxD, meanD, deltabeta, A, ar, skew, Tx, Ty, stretch, fshape, TD,
    TN, J, JA}, # == 1 &],
  With[{qualityVar =
     assignQualityVar[minL, maxL, meanL, minalpha, maxalpha,
      meanalpha, minD, maxD, meanD, deltabeta, A, ar, skew, Tx, Ty,
      stretch, fshape, TD, TN, J, JA],
    qualityName =
     assignQualityName[minL, maxL, meanL, minalpha, maxalpha,
      meanalpha, minD, maxD, meanD, deltabeta, A, ar, skew, Tx, Ty,
      stretch, fshape, TD, TN, J, JA]},
   If[model == 2,
    If[solver == 1,
     With[{fiberArrangement = 1, isUpperBounded = 1,
       isLowerBounded = If[layup == 1, 1, 0], isCohesive = 0,
       crackType = 1},
      plotMeshQuality[qualityVar, qualityName, fiberArrangement,
       isUpperBounded, isLowerBounded, isCohesive, crackType, eltype,
       elorder, optimised, Rf, Vff, tratio, theta, dtheta, f1, f2, f3,
        N1, N2, N3, N4, N5, N6, ImgSize]],
     With[{fiberArrangement = 1, isUpperBounded = 1,
       isLowerBounded = If[layup == 1, 1, 0], isCohesive = 1,
       crackType = 1},
      plotMeshQuality[qualityVar, qualityName, fiberArrangement,
       isUpperBounded, isLowerBounded, isCohesive, crackType, eltype,
       elorder, optimised, Rf, Vff, tratio, theta, dtheta, f1, f2, f3,
        N1, N2, N3, N4, N5, N6, ImgSize]]],
    If[solver == 1,
     With[{fiberArrangement = 1, isUpperBounded = 0,
       isLowerBounded = 0, isCohesive = 0, crackType = 1},
      plotMeshQuality[qualityVar, qualityName, fiberArrangement,
       isUpperBounded, isLowerBounded, isCohesive, crackType, eltype,
       elorder, optimised, Rf, Vff, tratio, theta, dtheta, f1, f2, f3,
        N1, N2, N3, N4, N5, N6, ImgSize]],
     With[{fiberArrangement = 1, isUpperBounded = 0,
       isLowerBounded = 0, isCohesive = 1, crackType = 1},
      plotMeshQuality[qualityVar, qualityName, fiberArrangement,
       isUpperBounded, isLowerBounded, isCohesive, crackType, eltype,
       elorder, optimised, Rf, Vff, tratio, theta, dtheta, f1, f2, f3,
        N1, N2, N3, N4, N5, N6, ImgSize]]]]],
  Row[{Graphics[{White, Rectangle[{0, 0}]}, Axes -> True,
     AxesLabel -> {x, z}, AspectRatio -> 1, ImageSize -> ImgSize],
    Graphics[{White, Rectangle[{0, 0}]}, Axes -> True,
     AxesLabel -> {value, frequency}, AspectRatio -> 1,
     ImageSize -> ImgSize]}, Alignment -> {Center, Center}]]

TPM2DiPiC01Fmodelcontrol[] :=
 Control[{{model, 1, ""}, {1 -> "Isolated RVE", 2 -> "Bounded RVE",
    3 -> "Periodic RVE"}}]

TPM2DiPiC01Flayupcontrol[] :=
 Control[{{layup, 1,
    ""}, {1 ->
     "[[0\[Degree]\!\(\*SubscriptBox[\(]\), \(n\)]\),90\[Degree],[0\
\[Degree]\!\(\*SubscriptBox[\(]\), \(n\)]\)]",
    2 -> "[[0\[Degree]\!\(\*SubscriptBox[\(]\), \
\(n\)]\),90\[Degree]\!\(\*SubscriptBox[\(]\), \(S\)]\)"}}]

TPM2DiPiC01Fgeomcontrol[] :=
 Column[{Control[{{Rf, 1,
      "\!\(\*SubscriptBox[\(R\), \(f\)]\) [\[Mu]m]"}, 0.01, 10,
     0.01}], Control[{{Vff, 0.6,
      "\!\(\*SubscriptBox[\(Vf\), \(f\)]\) [-]"}, 0.01, 1, 0.01}],
   Control[{{tratio, 0.6, "t [0\[Degree]]/[90\[Degree]] [-]"}, 0.01,
     100, 0.01}],
   Control[{{theta, 30, "\[Theta] [\[Degree]]"}, -360, 360, 0.36}],
   Control[{{dtheta, 10, "\[CapitalDelta]\[Theta] [\[Degree]]"}, 0,
     180, 0.18}],
   Control[{{a, 0, "a [\[Mu]m]"}, 0,
     Rf Sqrt[2] 0.5 Sqrt[\[Pi]/Vff] - 1, 0.01}]}, Spacings -> 1.5,
  Dividers -> {None, {False, False, True, True, False, False}}]

TPM2DiPiC01Fmeshcontrol[] :=
 Column[{Control[{{showmesh, 0, ""}, {0 -> "Hide", 1 -> "Show"}}],
   Control[{{optimised, 0, ""}, {0 -> "Basic", 1 -> "Optimised"}}],
   Control[{{f1, 0.5, "\!\(\*SubscriptBox[\(f\), \(1\)]\) [-]"}, 0.01,
      1, 0.01}],
   Control[{{f2, Sqrt[2]*f1 + 0.075,
      "\!\(\*SubscriptBox[\(f\), \(2\)]\) [-]"}, Sqrt[2]*f1, 1,
     0.01}], Control[{{f3, 1.05,
      "\!\(\*SubscriptBox[\(f\), \(3\)]\) [-]"}, 1.01,
     0.5*Sqrt[Pi/Vff], 0.01}],
   Control[{{N1, 20, "\!\(\*SubscriptBox[\(N\), \(\[Alpha]\)]\) [-]"},
      5, 1000, 1}],
   Control[{{N2, 20, "\!\(\*SubscriptBox[\(N\), \(\[Beta]\)]\) [-]"},
     5, 1000, 1}],
   Control[{{N3, 20, "\!\(\*SubscriptBox[\(N\), \(\[Gamma]\)]\) [-]"},
      5, 1000, 1}],
   Control[{{N4, 20, "\!\(\*SubscriptBox[\(N\), \(\[Delta]\)]\) [-]"},
      5, 1000, 1}],
   Control[{{N5, 20,
      "\!\(\*SubscriptBox[\(N\), \(\[Epsilon]\)]\) [-]"}, 5, 1000,
     1}], Control[{{N6, 20,
      "\!\(\*SubscriptBox[\(N\), \(\[Zeta]\)]\) [-]"}, 5, 1000, 1}],
   Row[{Style["\[Delta] [\[Degree]]", Black], Spacer[20],
     Dynamic[N[90/N1]]}],
   Row[{Style["\!\(\*SubscriptBox[\(N\), \(NODES\)]\)", Black],
     Spacer[20],
     Dynamic[If[model == 2,
       N[(N1 + 1)*(N1 + 1) + 4*N1*(N2 + N3 + 1) + 4*N1*(N4 + N5) +
         2*(N1 + 1)*(N6 + 1)],
       N[(N1 + 1)*(N1 + 1) + 4*N1*(N2 + N3 + 1) + 4*N1*(N4 + N5)]]]}],
    Row[{Style["\!\(\*SubscriptBox[\(N\), \(ELEMENTS\)]\)", Black],
     Spacer[20],
     Dynamic[If[model == 2,
       N[N1*N1 + 4*N1*(N2 + N3 + N4 + N5) + 2*N1*N6],
       N[N1*N1 + 4*N1*(N2 + N3 + N4 + N5)]]]}]}, Spacings -> 1.5,
  Dividers -> {None, {False, True, True, False, False, True, False,
     False, False, False, False, True}}]

TPM2DiPiC01Fqualitycontrol[] :=
 Column[{OpenerView[{Style[
      "\!\(\*TemplateBox[{\"1\",\"st\"},\n\"Superscript\"]\) order \
Quadrilaterals", Black, Italic, 12], quad4controls[]}, True],
   OpenerView[{Style[
      "\!\(\*TemplateBox[{\"2\",\"nd\"},\n\"Superscript\"]\) order \
Quadrilaterals", Black, Italic, 12], quad8controls[]}, True],
   OpenerView[{Style[
      "\!\(\*TemplateBox[{\"1\",\"st\"},\n\"Superscript\"]\) order \
Triangles", Black, Italic, 12], tri3controls[]}, False],
   OpenerView[{Style[
      "\!\(\*TemplateBox[{\"2\",\"nd\"},\n\"Superscript\"]\) order \
Triangles", Black, Italic, 12], tri6controls[]}, True]}]

TPM2DiPiC01Fmaterialcontrol[] :=
 Column[{Control[{{fiber, 1, "Fiber"}, {1 -> "CF", 2 -> "GF"}}],
   Control[{{matrix, 1, "Matrix"}, {1 -> "Epoxy", 2 -> "HDPE"}}]}]

TPM2DiPiC01Fboundarycontrol[] :=
 Control[{{epsilon, 0.01, Subscript["\[Epsilon]", x]}, 0, 1, 0.0001}]

TPM2DiPiC01Felementcontrol[] :=
 Column[{Control[{{eltype, 1, "Type"}, {1 -> "Quad", 2 -> "Tri"}}],
   Control[{{elorder, 1,
      "Order"}, {1 ->
       "\!\(\*TemplateBox[{\"1\",\"st\"},\n\"Superscript\"]\)",
      2 -> "\!\(\*TemplateBox[{\"2\",\"nd\"},\n\"Superscript\"]\)"}}]}]

TPM2DiPiC01Fsolvercontrol[] :=
 Control[{{solver, 1, ""}, {1 -> "Virtual Crack Closure Method",
    2 -> "Cohesive Elements Method"}}]

TPM2DiPiC01Fgraphicscontrol[] :=
 Column[{Control[{{ImgSizeS, 400, "Image Size"}, 1, 1000, 1}],
   Control[{{arr1, 10, "Number of load arrows"}, 2, 100, 1}],
   Control[{{arrlength1, 0.2, "Length of load arrows"}, 0.1, 1,
     0.01}],
   Control[{{arr2, 5, "Number of boundary arrows"}, 2, 100, 1}],
   Control[{{arrwidth1, 0.2, "Width of boundary arrows"}, 0.1, 1,
     0.01}]}]

thinplydebondinnermeshgenonefib[] :=
 Manipulate[
  With[{ImgSize = {ImgSizeS, ImgSizeS}},
   Column[{Row[{TPM2DiPiC01Fgeom[model, layup, solver, Rf, Vff,
        tratio, theta, dtheta, a, arrwidth1, arrlength1, arr1, arr2,
        ImgSize],
       TPM2DiPiC01Fmesh[model, layup, solver, showmesh, eltype,
        elorder, optimised, Rf, Vff, tratio, theta, dtheta, a,
        arrwidth1, arrlength1, arr1, arr2, f1, f2, f3, N1, N2, N3, N4,
         N5, N6, ImgSize]}, Alignment -> {Center, Center}],
     TPM2DiPiC01Fmeshquality[model, layup, solver, showmesh, eltype,
      elorder, optimised, Rf, Vff, tratio, theta, dtheta, a,
      arrwidth1, arrlength1, arr1, arr2, f1, f2, f3, N1, N2, N3, N4,
      N5, N6, ImgSize, minL, maxL, meanL, minalpha, maxalpha,
      meanalpha, minD, maxD, meanD, deltabeta, A, ar, skew, Tx, Ty,
      stretch, fshape, TD, TN, J, JA]}]],
  Row[{Column[{OpenerView[{Style["Model", Black, Bold, 12],
        TPM2DiPiC01Fmodelcontrol[]}, True],
      OpenerView[{Style["Laminate Lay-Up", Black, Bold, 12],
        TPM2DiPiC01Flayupcontrol[]}, True],
      Row[{OpenerView[{Style["Geometry", Black, Bold, 12],
          TPM2DiPiC01Fgeomcontrol[]}, True], Spacer[250],
        OpenerView[{Style["Mesh", Black, Bold, 12],
          TPM2DiPiC01Fmeshcontrol[]}, True],
        OpenerView[{Style["Mesh Quality Parameters", Black, Bold, 12],
           TPM2DiPiC01Fqualitycontrol[]}, True]}],
      Row[{OpenerView[{Style["Materials", Black, Bold, 12],
          TPM2DiPiC01Fmaterialcontrol[]}, True],
        OpenerView[{Style["Boundary Conditions", Black, Bold, 12],
          TPM2DiPiC01Fboundarycontrol[]}, True],
        OpenerView[{Style["Elements", Black, Bold, 12],
          TPM2DiPiC01Felementcontrol[]}, True],
        OpenerView[{Style["Solver", Black, Bold, 12],
          TPM2DiPiC01Fsolvercontrol[]}, True]}],
      OpenerView[{Style["Graphics", Black, Bold, 12],
        TPM2DiPiC01Fgraphicscontrol[]}, True]}], Spacer[100],
    Column[{Style["Current Project Directory", Black, Bold, 12],
      Style[Dynamic[dir], Black, Italic, 12],
      Button["Update", dir = Directory[], Method -> "Queued"],
      Button["Change Directory",
       SetDirectory[SystemDialogInput["Directory"]],
       Method -> "Queued"],
      Button["Create Project", With[{dir = Directory[]}, None]]},
     Spacings -> 2]}], ControlPlacement -> Bottom]

(* :2D TPM Tests Interface: surface ply,  interface crack, one fiber (arrangement 1):  *)

TPM2DoPiC01Fgeom[model_, layup_, solver_, Rf_, Vff_, tratio_, theta_,
  dtheta_, a_, arrwidth1_, arrlength1_, arr1_, arr2_, ImgSize_] :=
 If[model == 1,
  If[solver == 1,
   If[layup == 1,
    plotOuterSingleGeometry[Rf, Vff, theta Degree, dtheta Degree, a,
     arrwidth1, arrlength1, arr1, arr2, ImgSize],
    plotOuterSingleSymmGeometry[Rf, Vff, theta Degree, dtheta Degree,
     a, arrwidth1, arrlength1, arr1, arr2, ImgSize]],
   If[layup == 1,
    plotOuterSingleCohesiveGeometry[Rf, Vff, theta Degree,
     dtheta Degree, a, arrwidth1, arrlength1, arr1, arr2, ImgSize],
    plotOuterSingleCohesiveSymmGeometry[Rf, Vff, theta Degree,
     dtheta Degree, a, arrwidth1, arrlength1, arr1, arr2, ImgSize]]],
  If[model == 2,
   If[solver == 1,
    If[layup == 1,
     plotOuterBoundedGeometry[Rf, Vff, tratio, theta Degree,
      dtheta Degree, a, arrwidth1, arrlength1, arr1, arr2, ImgSize],
     plotOuterBoundedSymmGeometry[Rf, Vff, tratio, theta Degree,
      dtheta Degree, a, arrwidth1, arrlength1, arr1, arr2, ImgSize]],
    If[layup == 1,
     plotOuterBoundedCohesiveGeometry[Rf, Vff, tratio, theta Degree,
      dtheta Degree, a, arrwidth1, arrlength1, arr1, arr2, ImgSize],
     plotOuterBoundedCohesiveSymmGeometry[Rf, Vff, tratio,
      theta Degree, dtheta Degree, a, arrwidth1, arrlength1, arr1,
      arr2, ImgSize]]],
   If[solver == 1,
    plotPeriodicGeometry[Rf, Vff, theta Degree, dtheta Degree, a,
     arrwidth1, arrlength1, arr1, arr2, ImgSize],
    plotPeriodicCohesiveGeometry[Rf, Vff, theta Degree, dtheta Degree,
      a, arrwidth1, arrlength1, arr1, arr2, ImgSize]]]]

TPM2DoPiC01Fmesh[model_, layup_, solver_, showmesh_, eltype_,
  elorder_, optimised_, Rf_, Vff_, tratio_, theta_, dtheta_, a_,
  arrwidth1_, arrlength1_, arr1_, arr2_, f1_, f2_, f3_, N1_, N2_, N3_,
   N4_, N5_, N6_, ImgSize_] :=
 If[model == 2,
  If[solver == 1,
   If[showmesh == 0,
    plotOuterBoundedMesh[Rf, Vff, tratio, theta Degree, dtheta Degree,
      f1, f2, f3, ImgSize],
    With[{fiberArrangement = 1, isUpperBounded = 0,
      isLowerBounded = 1, isCohesive = 0, crackType = 1},
     plotMeshDetails[fiberArrangement, isUpperBounded, isLowerBounded,
       isCohesive, crackType, eltype, elorder, optimised, Rf, Vff,
      tratio, N[theta Degree], N[dtheta Degree], f1, f2, f3, N1, N2,
      N3, N4, N5, N6, ImgSize]]],
   If[showmesh == 0,
    plotOuterBoundedCohesiveMesh[Rf, Vff, tratio, theta Degree,
     dtheta Degree, f1, f2, f3, ImgSize],
    With[{fiberArrangement = 1, isUpperBounded = 0,
      isLowerBounded = 1, isCohesive = 1, crackType = 1},
     plotMeshDetails[fiberArrangement, isUpperBounded, isLowerBounded,
       isCohesive, crackType, eltype, elorder, optimised, Rf, Vff,
      tratio, N[theta Degree], N[dtheta Degree], f1, f2, f3, N1, N2,
      N3, N4, N5, N6, ImgSize]]]],
  If[solver == 1,
   If[showmesh == 0,
    plotSingleMesh[Rf, Vff, theta Degree, dtheta Degree, f1, f2, f3,
     ImgSize],
    With[{fiberArrangement = 1, isUpperBounded = 0,
      isLowerBounded = 0, isCohesive = 0, crackType = 1},
     plotMeshDetails[fiberArrangement, isUpperBounded, isLowerBounded,
       isCohesive, crackType, eltype, elorder, optimised, Rf, Vff,
      tratio, N[theta Degree], N[dtheta Degree], f1, f2, f3, N1, N2,
      N3, N4, N5, N6, ImgSize]]],
   If[showmesh == 0,
    plotSingleCohesiveMesh[Rf, Vff, theta Degree, dtheta Degree, f1,
     f2, f3, ImgSize],
    With[{fiberArrangement = 1, isUpperBounded = 0,
      isLowerBounded = 0, isCohesive = 1, crackType = 1},
     plotMeshDetails[fiberArrangement, isUpperBounded, isLowerBounded,
       isCohesive, crackType, eltype, elorder, optimised, Rf, Vff,
      tratio, N[theta Degree], N[dtheta Degree], f1, f2, f3, N1, N2,
      N3, N4, N5, N6, ImgSize]]]]]

TPM2DoPiC01Fmodelcontrol[] :=
 Control[{{model, 1, ""}, {1 -> "Isolated RVE", 2 -> "Bounded RVE",
    3 -> "Periodic RVE"}}]

TPM2DoPiC01Flayupcontrol[] :=
 Control[{{layup, 1,
    ""}, {1 ->
     "[90\[Degree],[0\[Degree]\!\(\*SubscriptBox[\(]\), \(n\)]\)]",
    2 -> "[90\[Degree],[0\[Degree]\!\(\*SubscriptBox[\(]\), \
\(n\)]\)\!\(\*SubscriptBox[\(]\), \(S\)]\)"}}]

TPM2DoPiC01Fgeomcontrol[] :=
 Column[{Control[{{Rf, 1,
      "\!\(\*SubscriptBox[\(R\), \(f\)]\) [\[Mu]m]"}, 0.01, 10,
     0.01}], Control[{{Vff, 0.6,
      "\!\(\*SubscriptBox[\(Vf\), \(f\)]\) [-]"}, 0.01, 1, 0.01}],
   Control[{{tratio, 0.6, "t [0\[Degree]]/[90\[Degree]] [-]"}, 0.01,
     100, 0.01}],
   Control[{{theta, 30, "\[Theta] [\[Degree]]"}, -360, 360, 0.36}],
   Control[{{dtheta, 10, "\[CapitalDelta]\[Theta] [\[Degree]]"}, 0,
     180, 0.18}],
   Control[{{a, 0, "a [\[Mu]m]"}, 0,
     Rf Sqrt[2] 0.5 Sqrt[\[Pi]/Vff] - 1, 0.01}]}, Spacings -> 1.5,
  Dividers -> {None, {False, False, True, True, False, False}}]

TPM2DoPiC01Fmeshcontrol[] :=
 Column[{Control[{{showmesh, 0, ""}, {0 -> "Hide", 1 -> "Show"}}],
   Control[{{optimised, 0, ""}, {0 -> "Basic", 1 -> "Optimised"}}],
   Control[{{f1, 0.5, "\!\(\*SubscriptBox[\(f\), \(1\)]\) [-]"}, 0.01,
      1, 0.01}],
   Control[{{f2, Sqrt[2]*f1 + 0.075,
      "\!\(\*SubscriptBox[\(f\), \(2\)]\) [-]"}, Sqrt[2]*f1, 1,
     0.01}], Control[{{f3, 1.05,
      "\!\(\*SubscriptBox[\(f\), \(3\)]\) [-]"}, 1.01,
     0.5*Sqrt[Pi/Vff], 0.01}],
   Control[{{N1, 20, "\!\(\*SubscriptBox[\(N\), \(\[Alpha]\)]\) [-]"},
      5, 1000, 1}],
   Control[{{N2, 20, "\!\(\*SubscriptBox[\(N\), \(\[Beta]\)]\) [-]"},
     5, 1000, 1}],
   Control[{{N3, 20, "\!\(\*SubscriptBox[\(N\), \(\[Gamma]\)]\) [-]"},
      5, 1000, 1}],
   Control[{{N4, 20, "\!\(\*SubscriptBox[\(N\), \(\[Delta]\)]\) [-]"},
      5, 1000, 1}],
   Control[{{N5, 20,
      "\!\(\*SubscriptBox[\(N\), \(\[Epsilon]\)]\) [-]"}, 5, 1000,
     1}], Control[{{N6, 20,
      "\!\(\*SubscriptBox[\(N\), \(\[Zeta]\)]\) [-]"}, 5, 1000, 1}],
   Row[{Style["\[Delta] [\[Degree]]", Black], Spacer[20],
     Dynamic[N[90/N1]]}],
   Row[{Style["\!\(\*SubscriptBox[\(N\), \(NODES\)]\)", Black],
     Spacer[20],
     Dynamic[If[model == 2,
       N[(N1 + 1)*(N1 + 1) + 4*N1*(N2 + N3 + 1) + 4*N1*(N4 + N5) +
         2*(N1 + 1)*(N6 + 1)],
       N[(N1 + 1)*(N1 + 1) + 4*N1*(N2 + N3 + 1) + 4*N1*(N4 + N5)]]]}],
    Row[{Style["\!\(\*SubscriptBox[\(N\), \(ELEMENTS\)]\)", Black],
     Spacer[20],
     Dynamic[If[model == 2,
       N[N1*N1 + 4*N1*(N2 + N3 + N4 + N5) + 2*N1*N6],
       N[N1*N1 + 4*N1*(N2 + N3 + N4 + N5)]]]}]}, Spacings -> 1.5,
  Dividers -> {None, {False, True, True, False, False, True, False,
     False, False, False, False, True}}]

TPM2DoPiC01Fqualitycontrol[] :=
 Column[{OpenerView[{Style[
      "\!\(\*TemplateBox[{\"1\",\"st\"},\n\"Superscript\"]\) order \
Quadrilaterals", Black, Italic, 12], quad4controls[]}, False],
   OpenerView[{Style[
      "\!\(\*TemplateBox[{\"2\",\"nd\"},\n\"Superscript\"]\) order \
Quadrilaterals", Black, Italic, 12], quad8controls[]}, False],
   OpenerView[{Style[
      "\!\(\*TemplateBox[{\"1\",\"st\"},\n\"Superscript\"]\) order \
Triangles", Black, Italic, 12], tri3controls[]}, False],
   OpenerView[{Style[
      "\!\(\*TemplateBox[{\"2\",\"nd\"},\n\"Superscript\"]\) order \
Triangles", Black, Italic, 12], tri6controls[]}, False]}]

TPM2DoPiC01Fmaterialcontrol[] :=
 Column[{Control[{{fiber, 1, "Fiber"}, {1 -> "CF", 2 -> "GF"}}],
   Control[{{matrix, 1, "Matrix"}, {1 -> "Epoxy", 2 -> "HDPE"}}]}]

TPM2DoPiC01Fboundarycontrol[] :=
 Control[{{epsilon, 0.01, Subscript["\[Epsilon]", x]}, 0, 1, 0.0001}]

TPM2DoPiC01Felementcontrol[] :=
 Column[{Control[{{eltype, 1, "Type"}, {1 -> "Quad", 2 -> "Tri"}}],
   Control[{{elorder, 1,
      "Order"}, {1 ->
       "\!\(\*TemplateBox[{\"1\",\"st\"},\n\"Superscript\"]\)",
      2 -> "\!\(\*TemplateBox[{\"2\",\"nd\"},\n\"Superscript\"]\)"}}]}]

TPM2DoPiC01Fsolvercontrol[] :=
 Control[{{solver, 1, ""}, {1 -> "Virtual Crack Closure Method",
    2 -> "Cohesive Elements Method"}}]

TPM2DoPiC01Fgraphicscontrol[] :=
 Column[{Control[{{ImgSizeS, 400, "Image Size"}, 1, 1000, 1}],
   Control[{{arr1, 10, "Number of load arrows"}, 2, 100, 1}],
   Control[{{arrlength1, 0.2, "Length of load arrows"}, 0.1, 1,
     0.01}],
   Control[{{arr2, 5, "Number of boundary arrows"}, 2, 100, 1}],
   Control[{{arrwidth1, 0.2, "Width of boundary arrows"}, 0.1, 1,
     0.01}]}]

thinplydebondoutermeshgenonefib[] :=
 Manipulate[
  With[{ImgSize = {ImgSizeS, ImgSizeS}},
   Row[{TPM2DoPiC01Fgeom[model, layup, solver, Rf, Vff, tratio, theta,
       dtheta, a, arrwidth1, arrlength1, arr1, arr2, ImgSize],
     TPM2DoPiC01Fmesh[model, layup, solver, showmesh, eltype, elorder,
       optimised, Rf, Vff, tratio, theta, dtheta, a, arrwidth1,
      arrlength1, arr1, arr2, f1, f2, f3, N1, N2, N3, N4, N5, N6,
      ImgSize]}, Alignment -> {Center, Center}]],
  Row[{Column[{OpenerView[{Style["Model", Black, Bold, 12],
        TPM2DoPiC01Fmodelcontrol[]}, True],
      OpenerView[{Style["Laminate Lay-Up", Black, Bold, 12],
        TPM2DoPiC01Flayupcontrol[]}, True],
      Row[{OpenerView[{Style["Geometry", Black, Bold, 12],
          TPM2DoPiC01Fgeomcontrol[]}, True], Spacer[250],
        OpenerView[{Style["Mesh", Black, Bold, 12],
          TPM2DoPiC01Fmeshcontrol[]}, True],
        OpenerView[{Style["Mesh Quality Parameters", Black, Bold, 12],
           TPM2DoPiC01Fqualitycontrol[]}, True]}],
      Row[{OpenerView[{Style["Materials", Black, Bold, 12],
          TPM2DoPiC01Fmaterialcontrol[]}, True],
        OpenerView[{Style["Boundary Conditions", Black, Bold, 12],
          TPM2DoPiC01Fboundarycontrol[]}, True],
        OpenerView[{Style["Elements", Black, Bold, 12],
          TPM2DoPiC01Felementcontrol[]}, True],
        OpenerView[{Style["Solver", Black, Bold, 12],
          TPM2DoPiC01Fsolvercontrol[]}, True]}],
      OpenerView[{Style["Graphics", Black, Bold, 12],
        TPM2DoPiC01Fgraphicscontrol[]}, True]}], Spacer[100],
    Column[{Style["Current Project Directory", Black, Bold, 12],
      Style[Dynamic[dir], Black, Italic, 12],
      Button["Update", dir = Directory[], Method -> "Queued"],
      Button["Change Directory",
       SetDirectory[SystemDialogInput["Directory"]],
       Method -> "Queued"],
      Button["Create Project", With[{dir = Directory[]}, None]]},
     Spacings -> 2]}], ControlPlacement -> Bottom]

(* :3D TPM Tests Interface:  *)

threeDthinplysection[] := Text["Under Construction"]

(* :2D Standard Mechanical Tests Interface:  *)

twoDstdmechtests[] := Text["Under Construction"]

(* :3D Standard Mechanical Tests Interface:  *)

threeDstdmechtests[] := Text["Under Construction"]

(* :3D Fiber/Matrix Interface Debonding Tests Interface:  *)

threeDfibermatrixinterface[] := Text["Under Construction"]

(* :Virtual Laboratory Interface:  *)

program[] := (SetDirectory[wd]; OpenMATLAB[];
  CreateDialog[{Deploy[
     MenuView[{"Select Test Family" -> Text["Select Test Family"],
       "2D Standard Mechanical Tests" -> twoDstdmechtests[],
       "2D Micromechanical Tests on Thin Ply FRPC Laminates" ->
        twoDthinplysection[],
       "3D Micromechanical Tests on Thin Ply FRPC Laminates" ->
        threeDthinplysection[],
       "3D Standard Mechanical Tests" -> threeDstdmechtests[],
       "3D Fiber/Matrix Crack Propagation" ->
        threeDfibermatrixinterface[]}]]},
   WindowTitle -> "Virtual Laboratory for Fiber Composite Testing",
   WindowElements -> {"VerticalScrollBar", "HorizontalScrollBar",
     "StatusArea"}])

(* :GUI:  *)

 UsingFrontEnd[NotebookEvaluate["C:\\01_backup-folder\\OneDrive\\01_Luca\\07_DocMASE\\04_WD\\thin_ply_mechanics\\mathematica"]]

(* UsingFrontEnd[program[]] *)
