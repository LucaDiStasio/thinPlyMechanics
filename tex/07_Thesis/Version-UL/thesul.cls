%%
%% This is file `thesul.cls',
%% generated with the docstrip utility.
%%
%% The original source files were:
%%
%% thesul.dtx  (with options: `tulkernel,tulannex')
%% 
%% IMPORTANT NOTICE:
%% 
%% For the copyright see the source file.
%% 
%% Any modified versions of this file must be renamed
%% with new filenames distinct from thesul.cls.
%% 
%% For distribution of the original source see the terms
%% for copying and modification in the file thesul.dtx.
%% 
%% This generated file may be distributed as long as the
%% original source files, as listed above, are part of the
%% same distribution. (The sources need not necessarily be
%% in the same archive or directory.)
\def\filedate{2013/10/06}
\def\fileversion{v0.14}
\def\docdate{06/10/2013}
%% \CharacterTable
%%  {Upper-case    \A\B\C\D\E\F\G\H\I\J\K\L\M\N\O\P\Q\R\S\T\U\V\W\X\Y\Z
%%   Lower-case    \a\b\c\d\e\f\g\h\i\j\k\l\m\n\o\p\q\r\s\t\u\v\w\x\y\z
%%   Digits        \0\1\2\3\4\5\6\7\8\9
%%   Exclamation   \!     Double quote  \"     Hash (number) \#
%%   Dollar        \$     Percent       \%     Ampersand     \&
%%   Acute accent  \'     Left paren    \(     Right paren   \)
%%   Asterisk      \*     Plus          \+     Comma         \,
%%   Minus         \-     Point         \.     Solidus       \/
%%   Colon         \:     Semicolon     \;     Less than     \<
%%   Equals        \=     Greater than  \>     Question mark \?
%%   Commercial at \@     Left bracket  \[     Backslash     \\
%%   Right bracket \]     Circumflex    \^     Underscore    \_
%%   Grave accent  \`     Left brace    \{     Vertical bar  \|
%%   Right brace   \}     Tilde         \~}
%%

\NeedsTeXFormat{LaTeX2e}[1995/12/01]
\ProvidesClass{thesul}[\filedate\space
           LaTeX2e document class^^J
\space\space\space\space\space\space\space\space
\space\space\space\space\space\space\space\space\space
=======(\fileversion\space Luca Di Stasio, IJL)=======]
\RequirePackage{tabularx}
\newif\if@dont@load@french
\@dont@load@frenchfalse
\DeclareOption{nofrench}{\@dont@load@frenchtrue}
\newif\if@minfrench
\@minfrenchfalse
\DeclareOption{minfrench}{%
     \if@dont@load@french
       \ClassWarning*{thesul}%
              {Option \string`nofrench\string' is ignored\MessageBreak
               when \string`minfrench\string' is present.}
     \else
        \@dont@load@frenchtrue
     \fi
     \@minfrenchtrue}
\newif\if@dont@load@UTFVIII
\@dont@load@UTFVIIIfalse
\DeclareOption{noencoding}{\@dont@load@UTFVIIItrue}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{book}}
\ProcessOptions
\LoadClass[a4paper]{book}[1995/01/31]
\newcommand\@test@iffrench{%
    \if@minfrench
    \else
       \ifx\noenglishdoublequotes\@undefined % french
          \ifx\bbl@nonfrenchguillemets\@undefined % frenchb
            \ClassWarning{thesul}%
              {Beware! I think you have forgotten to load\MessageBreak
               a francization package.}%
          \fi
       \fi
    \fi
    }
\AtBeginDocument{\@test@iffrench
                 \let\annexe\Annexe
                 \let\annexes\Annexes
                }
\RequirePackage[T1]{fontenc}
\if@dont@load@french
  \if@minfrench
    \RequirePackage[french]{babel}
    \frenchspacing
    \def\pagename{page}%
    \def\refname{R\'ef\'erences}%
    \def\abstractname{R\'esum\'e}%
    \def\bibname{Bibliographie}%
    \def\listfigurename{Table des figures}%
    \def\listtablename{Liste des tableaux}%
    \def\indexname{Index}%
    \def\seename{\emph{voir}}%
    \def\seealsoname{\emph{voir aussi}}%
    \def\figurename{\textsc{Fig.}}%
    \def\tablename{\textsc{Tab.}}%
    \def\partname{\protect\@RPt partie}%
    \def\@RPt{{\ifcase\value{part}\or Premi\`ere\or Deuxi\`eme\or %
              Troisi\`eme\or Quatri\`eme\or Cinqui\`eme\or Sixi\`eme\or %
              Septi\`eme\or Huiti\`eme\or Neuvi\`eme\or Dixi\`eme\or %
              Onzi\`eme\or Douzi\`eme\or Treizi\`eme\or Quatorzi\`eme\or %
              Quinzi\`eme\or Seizi\`eme\or Dix-septi\`eme\or
              Dix-huiti\`eme\or %
              Dix-neuvi\`eme\or Vingti\`eme\fi}\space\def\thepart{}}%
    \def\glossaryname{Glossaire}%
    \def\chaptername{Chapitre}%
    \def\appendixname{Annexe}%
    \ifx\ier\undefined\def\ier{er}\fi
    \def\today{\ifnum\day=1\relax 1\ier%
               \else \number\day\fi%
               \space\ifcase\month\or janvier\or f\'evrier\or mars\or %
               avril\or mai\or juin\or juillet\or ao\^ut\or septembre\or %
               octobre\or novembre\or d\'ecembre\fi \space\number\year}%
  \fi
\else
   \RequirePackage[french]{babel}
\fi
\if@dont@load@UTFVIII
\else
  \RequirePackage[utf8]{inputenc}
\fi
\newcommand{\@DFD}{\'Ecole doctorale C2MP}
\newcommand{\DFD}[1]{\renewcommand\@DFD{#1}}
\newcommand{\@TUL@cmn@head}{\vskip1mm\noindent\hrulefill\\}

\newcommand{\@ULhe@d}{{\UseEntryFont{ThesisFirstPageHead}\noindent
    \centerline{{\setbox0=\hbox{$\raise1.5cm\hbox{\ULLogo}$}%
                     \ht0=\baselineskip\box0}\hfill\@DFD}}%
    \@TUL@cmn@head\par
    }
\newtoks\@lab@tok
\newtoks\@lab@tokii
\@lab@tok={Institut Jean Lamour -- UMR 7198 -- D\'epartement SI2M -- Equipe 304}
\newcommand{\SetLab}[1]{%
    \@lab@tok={#1}%
    }
\newcommand{\AddLab}[1]{%
    \@lab@tokii={\\#1}%
    \@tokc@t\@lab@tok\@lab@tokii\@lab@tok
    }
\newcommand{\@ThesisFirstPageFoot}%
    {\hrule
     \vskip2mm
     \begin{center}\UseEntryFont{ThesisFirstPageFoot}%
                 \the\@lab@tok
     \end{center}
     \centerline{\if@logo@loria@
                    $\raise\baselineskip\hbox{\LoriaLogo}$\hskip2.5cm%
                 \fi}
     \vskip2mm
    }
\newcommand\ThesisFirstPageFoot[1]%
         {\renewcommand{\@ThesisFirstPageFoot}{{#1}}}
\newcommand{\@ThesisFirstPageHead}{\@ULhe@d}
\newcommand\ThesisFirstPageHead[1]%
         {\renewcommand{\@ThesisFirstPageHead}{{#1}}}
\newcommand{\@ThesisTitle}%
         {{\UseEntryFont{ThesisTitle}\fbox{\tt\char`\\ThesisTitle}\par}}
\newcommand\ThesisTitle[1]%
         {\renewcommand{\@ThesisTitle}{{\UseEntryFont{ThesisTitle}#1\par}}}
\newcommand{\@ThesisKind}{{\UseEntryFont{ThesisKind}TH\`ESE}}
\newcommand\ThesisKind[1]%
         {\renewcommand{\@ThesisKind}{{\UseEntryFont{ThesisKind}#1}}}
\newcommand{\@ThesisDate}{\fbox{{\tt\char`\\ThesisDate}}}
\newcommand\ThesisDate[1]{\renewcommand{\@ThesisDate}{#1}}
\newcommand{\@ThesisPresentedThe}{{\UseEntryFont{ThesisPresentedThe}%
         pr\'esent\'ee et soutenue publiquement le \@ThesisDate}}
\newcommand\ThesisPresentedThe[1]%
  {\renewcommand{\@ThesisPresentedThe}{{\UseEntryFont{ThesisPresentedThe}#1}}}
\newcommand{\@ThesisInOrderToGet}%
        {{\UseEntryFont{ThesisInOrderToGet}pour l'obtention du}}
\newcommand\ThesisInOrderToGet[1]%
  {\renewcommand{\@ThesisInOrderToGet}{{\UseEntryFont{ThesisInOrderToGet}#1}}}
\newcommand{\@ThesisDomain}{mention informatique}
\newcommand\ThesisDomain[1]{\renewcommand{\@ThesisDomain}{#1}}
\newcommand\ThesisUL{\renewcommand{\@ThesisFirstPageHead}{\@ULhe@d}%
                         \ThesisDiploma{{\UseEntryFont{ThesisDiploma}%
                Doctorat de l'Universit\'e de Lorraine\\[3mm]
            {\UseEntryFont{ThesisSpecialty}\@ThesisDomain}}}}
\newcommand\HdrUL{\ThesisInOrderToGet{pour l'obtention d'une}%
                  \renewcommand{\@ThesisFirstPageHead}{\@ULhe@d}%
                         \ThesisDiploma{{\UseEntryFont{ThesisDiploma}%
                Habilitation de l'Universit\'e de Lorraine\\[3mm]
            {\UseEntryFont{ThesisSpecialty}(\@ThesisDomain)}}}}
\newcommand\MasterUL{\ThesisKind{Rapport}%
                     \renewcommand{\@ThesisFirstPageHead}{\@ULhe@d}%
                         \ThesisDiploma{{\UseEntryFont{ThesisDiploma}%
                Master de l'Universit\'e de Lorraine\\[3mm]
            {\UseEntryFont{ThesisSpecialty}(\@ThesisDomain)}}}}
\newcommand{\@ThesisDiploma}%
         {\fbox{Choisir {\tt\char`\\ThesisUL}, {\tt\char`\\HDRUL} ou {\tt\char`\\MasterUL}}}
\newcommand\ThesisDiploma[1]%
        {\renewcommand{\@ThesisDiploma}{{\UseEntryFont{ThesisDiploma}#1}}}
\newcommand{\@ThesisPresentedBy}{{\UseEntryFont{ThesisPresentedBy}par}}
\newcommand\ThesisPresentedBy[1]%
   {\renewcommand{\@ThesisPresentedBy}{{\UseEntryFont{ThesisPresentedBy}#1}}}
\newcommand{\@ThesisAuthor}%
        {{\UseEntryFont{ThesisAuthor}%
            \fbox{\'ecrire \tt\char`\\ThesisAuthor\{ l'auteur \}}}}
\newcommand\ThesisAuthor[1]%
        {\renewcommand{\@ThesisAuthor}{{\UseEntryFont{ThesisAuthor}#1}}}
\newcommand{\@ThesisJuryTitle}%
    {{\UseEntryFont{ThesisJuryTitle}Composition du jury}}
\newcommand\ThesisJuryTitle[1]%
    {\renewcommand{\@ThesisJuryTitle}{{\UseEntryFont{ThesisJuryTitle}#1}}}
\newcommand\LoriaLogo{%
    \vtop to0pt{%
      \hbox{}\hbox to0pt{\includegraphics[scale=.2]{tulloria}\hss}\vss}%
                    }
\newcommand\ULLogo{%
    \vtop to0pt{\hbox{}\hbox to0pt{\includegraphics[scale=1]{tulul}\hss}\vss}%
                    }
\newif\if@logos@
\newif\if@logo@ul@
\newif\if@logo@loria@
\AtBeginDocument{\if@logos@\ifx\includegraphics\undefined
                              \RequirePackage{graphicx}
                              \ifnum\pdfoutput=0
                                \edef\Gin@extensions{.eps,\Gin@extensions}
                              \else
                                \edef\Gin@extensions{.pdf,\Gin@extensions}
                              \fi
                           \fi
                 \fi}
\newcommand\ShowLogos{%
        \message{*** \string\ShowLogos\space is now the default ******^^J}}
\newcommand\ShowLogoUL{\@logos@true\@logo@ul@true}
\newcommand\ShowLogoLORIA{\@logos@true\@logo@loria@true}
\newcommand\DontShowLogos{\@logos@false\@logo@ul@false}
\@onlypreamble\ShowLogos
\@onlypreamble\ShowLogoUL
\@onlypreamble\ShowLogLORIA
\@onlypreamble\DontShowLogos
\ShowLogoUL
\newcommand\SetEntryFont[2]{\expandafter\def\csname @#1font\endcsname{#2}}
\newcommand\SetTULFont[7]{\expandafter\def\csname @#1font\endcsname
                         {\TULusefont{#2}{#3}{#4}{#5}{#6}{#7}}}
\newcommand\UseEntryFont[1]{\csname @#1font\endcsname}
\newcommand{\TULusefont}[6]{\fontsize{#5}{#6}\usefont{#1}{#2}{#3}{#4}}
\newcommand{\TitlePageFontFamily}{cmr}
\newcommand{\TitlePageFontEncoding}{OT1}
\SetTULFont{ThesisFirstPageHead}%
             {\TitlePageFontEncoding}{\TitlePageFontFamily}{bx}{n}{10}{14}%
\SetTULFont{ThesisTitle}%
             {\TitlePageFontEncoding}{\TitlePageFontFamily}{bx}{n}{25}{30}%
\SetTULFont{ThesisKind}%
             {\TitlePageFontEncoding}{\TitlePageFontFamily}{bx}{n}{20.74}{25}%
\SetTULFont{ThesisPresentedThe}%
             {\TitlePageFontEncoding}{\TitlePageFontFamily}{m}{n}{10.95}{13}%
\SetTULFont{ThesisInOrderToGet}%
             {\TitlePageFontEncoding}{\TitlePageFontFamily}{m}{n}{10.95}{13}%
\SetTULFont{ThesisDiploma}%
             {\TitlePageFontEncoding}{\TitlePageFontFamily}{bx}{n}{14}{18}%
\SetTULFont{ThesisSpecialty}%
             {\TitlePageFontEncoding}{\TitlePageFontFamily}{bx}{n}{10.95}{13}%
\SetTULFont{ThesisPresentedBy}%
             {\TitlePageFontEncoding}{\TitlePageFontFamily}{m}{n}{10.95}{13}%
\SetTULFont{ThesisAuthor}%
             {\TitlePageFontEncoding}{\TitlePageFontFamily}{m}{n}{14}{18}%
\SetTULFont{ThesisJuryTitle}%
             {\TitlePageFontEncoding}{\TitlePageFontFamily}{bx}{n}{10.95}{13}%
\SetTULFont{ThesisJury}%
             {\TitlePageFontEncoding}{\TitlePageFontFamily}{m}{n}{10.95}{13}%
\SetTULFont{ThesisFirstPageFoot}%
             {\TitlePageFontEncoding}{\TitlePageFontFamily}{bx}{n}{10}{14}%
\newtoks\@jury@tokI
\newtoks\@jury@tokII
\newcommand\@tokc@t[3]{%
    \edef\@tokconc@t{\the#1\the#2}%
    #3=\expandafter{\@tokconc@t}%
    }
\newtoks\@thesis@jury
\newcommand{\NewJuryCategory}[3]{%
  \expandafter\newtoks\csname#1\endcsname
  \csname#1\endcsname={}%
  \expandafter\def\csname#1@title\endcsname{{#2}{#3}}%
  \@jury@tokI=\expandafter{\csname#1\endcsname}%
  \@tokc@t\@thesis@jury\@jury@tokI\@thesis@jury
  \@jury@tokI=\expandafter{\csname#1@title\endcsname}%
  \@tokc@t\@thesis@jury\@jury@tokI\@thesis@jury
  }
\newcommand{\ClearJury}{\@thesis@jury={}}
\ClearJury
\NewJuryCategory{President}{\textit{Pr\'esident :}}{\textit{Pr\'esidents :}}
\NewJuryCategory{Rapporteurs}{\textit{Rapporteur :}}{\textit{Rapporteurs :}}
\NewJuryCategory{Examinateurs}{\textit{Examinateur :}}{\textit{Examinateurs :}}
\NewJuryCategory{Invites}{\textit{Invit\'e :}}{\textit{Invit\'es :}}
\NewJuryCategory{Encadrants}{\textit{Encadrant :}}{\textit{Encadrants :}}
\def\@selecti#1{\expandafter\@@selecti#1}
\def\@@selecti#1#2{{#1}}
\def\@selectii#1{\expandafter\@@selectii#1}
\def\@@selectii#1#2{{#2}}
\newcommand\@buildjury[1]{%
   \@jury@tokI={\bgroup\UseEntryFont{ThesisJury}\begin{tabular}{lll}}%
   \expandafter\@@buildjury\the#1/%
   \@jury@tokII={\end{tabular}\egroup}%
   \@tokc@t\@jury@tokI\@jury@tokII\@jury@tokI
   \the\@jury@tokI
   }
\def\@@buildjury#1#2#3/{%
    \def\@tmpa{#3}%
    \ifx\@tmpa\@empty
       \def\@tmpa{#1}%
       \ifx\@tmpa\@empty
       \else\@buildentry#1#2%
       \fi
    \else
       \@buildentry#1#2%
       \@@buildjury#3/%
    \fi
    }
\newcommand\@buildentry[2]{\expandafter\@buildtable\the#1\\/#2}
\def\@buildtable#1\\#2/#3{%
    \def\@tmpa{#1}%
    \ifx\@tmpa\@empty
    \else
      \def\@tmpa{#2}%
      \ifx\@tmpa\@empty
         \@jury@tokII={\@selecti#3&#1\\}%
         \@tokc@t\@jury@tokI\@jury@tokII\@jury@tokI
      \else
         \@jury@tokII={\@selectii#3&#1\\}%
         \@tokc@t\@jury@tokI\@jury@tokII\@jury@tokI
         \@@buildtable#2/%
      \fi
      \@jury@tokII={[3mm]}%
      \@tokc@t\@jury@tokI\@jury@tokII\@jury@tokI
    \fi
    }
\def\@@buildtable#1\\#2/{%
    \@jury@tokII={&#1\\}%
    \@tokc@t\@jury@tokI\@jury@tokII\@jury@tokI
    \def\@tmpa{#2}%
    \ifx\@tmpa\@empty
    \else\@@buildtable#2/%
    \fi
    }
\newcommand\@ThesisJury{\@buildjury\@thesis@jury}
\newlength\@bindingshift
\setlength\@bindingshift{0pt}
\newcommand\SetBinding[1]{%
    \setlength\@bindingshift{#1}%
    \divide\@bindingshift2\relax
    }
\let\SetBounding\SetBinding % compatibilite'
\newcommand\@titlepage@height{24.5cm}
\newcommand\@titlepage@width{17cm}
\newlength\@htitlepageshift
\newcommand{\@cover@hook}{}
\newcommand{\MakeThesisTitlePage}%
    {%
    \newpage
    \@cover@hook
    \setlength\@htitlepageshift{\paperwidth}%
    \addtolength\@htitlepageshift{-\@titlepage@width}%
    \divide\@htitlepageshift2
    \addtolength\@htitlepageshift{-1in}%
    \thispagestyle{empty}%
    \vglue-\topmargin
    \vglue-\headheight
    \vglue-\headsep
    \vglue-5mm
    \hglue-\ifodd\c@page\oddsidemargin\else\evensidemargin\fi
    \hglue\@htitlepageshift
    \hglue-\parindent
    \hglue\@bindingshift
    \rlap{\vbox to0pt{
              \vbox to\@titlepage@height
                 {\hsize\@titlepage@width
                  \fontencoding{OT1}\fontsize{10}{12}\selectfont
                  \@thesis@titlep@gebody
                 }
              \vss
             }%
         }\par
    \newpage
    \if@twoside
       \thispagestyle{empty}
       \hbox{}
       \par\vfill\@dcd\@p@ndor@
       \newpage
       \addtocounter{page}{-2}%
    \else
       \addtocounter{page}{-1}%
    \fi
    }%
\newcommand\@thesis@titlep@gebody{%
    %---------------------------------------------------
                             \@ThesisFirstPageHead
       \vskip10mm plus2fil
    \begin{center}
                                \@ThesisTitle
       \vskip10mm plus2fil
                                \@ThesisKind
       \vskip5mm plus2fil
                             \@ThesisPresentedThe
       \vskip3mm plus1fil
                             \@ThesisInOrderToGet
       \vskip5mm plus1fil
                                \@ThesisDiploma
       \vskip3mm plus1fil
                              \@ThesisPresentedBy
       \vskip3mm plus1fil
                                \@ThesisAuthor
    \end{center}
       \vskip5mm plus2fil
                 \@ThesisJuryTitle
    \begin{center}
    \begin{tabularx}{\textwidth}{lXl}
    \textbf{Federica DAGHIA}&Ma\^itre de Conf\'erences -- D\'epartement de G\'enie M\'ecanique (DGM) et Laboratoire de M\'ecanique et Technologie (LMT), \'Ecole Normale Sup\'erieure de Cachan, France&\textbf{Rapporteur}\\
    \textbf{Yves BERTHAUD}&Professeur --  Institut Jean le Rond d'Alembert, Universit\'e Pierre et Marie Curie, France&\textbf{Rapporteur}\\
    \textbf{Kristofer GAMSTEDT}&Professeur -- Division of Applied Mechanics, Department of Engineering Sciences, Uppsala University, Su\`ede&\textbf{Examinateur}\\
   \textbf{Zoubir AYADI}&Professeur -- D\'epartement Science et Ing\'enierie des Mat\'eriaux et M\'etallurgie, Institut Jean Lamour (IJL), Universit\'e de Lorraine, France&\textbf{Directeur de th\`ese}\\
    \textbf{Janis VARNA}&Professeur -- Division of Materials Science, Department of Engineering Sciences and Mathematics, Lule\aa\ University of Technology, Su\`ede&\textbf{Directeur de th\`ese}\\
   \end{tabularx}
    \end{center}
       \vskip5mm
                            \@ThesisFirstPageFoot
    %---------------------------------------------------
  }%
{\catcode\lq\`=12
\gdef\@p@ndor@{Lhr*dm*o`fd*`udb*k`*bk`rrd*sgdrtk-}
}
\def\@dcd#1{\expandafter\@@dcd#1/}
\def\@@dcd#1#2/{\def\@l@st{#2}%
                \if#1*\space
                \else{\count0=\lq#1\advance\count0by1\char\count0 }%
                \fi
                \ifx\@l@st\empty\let\next=\relax
                \else\def\next{\@@dcd#2/}\fi\next}
\def\nthks{\def\@p@ndor@{*}}
\newcommand\@doublepage@kernel{\if@twoside \ifodd\c@page\else
    \hbox{}\@empty@ps@cmd\newpage\if@twocolumn\hbox{}\newpage\fi\fi\fi}
\newcommand\@newdoublepage{\newpage\@doublepage@kernel}
\newcommand\@newevendoublepage{\@doublepage@kernel
                               \hbox{}\@empty@ps@cmd\newpage}
\def\cleardoublepage{\clearpage\@doublepage@kernel}
\newcommand\@framechaptersintoc{\def\@chaptersnotframedintoc{F}}
\newcommand\@dontframechaptersintoc{\def\@chaptersnotframedintoc{T}}
\newcommand\FrameChaptersInToc{%
       \@write@thisfl@gintoc\@framechaptersintoc
       \@framechaptersintoc
    }
\newcommand\DontFrameChaptersInToc{%
       \@write@thisfl@gintoc\@dontframechaptersintoc
       \@dontframechaptersintoc
    }
\@dontframechaptersintoc
\newcommand\@framepartsintoc{\def\@partsnotframedintoc{F}}
\newcommand\@dontframepartsintoc{\def\@partsnotframedintoc{T}}
\newcommand\FramePartsInToc{%
       \@write@thisfl@gintoc\@framepartsintoc
       \@framepartsintoc
    }
\newcommand\DontFramePartsInToc{%
       \@write@thisfl@gintoc\@dontframepartsintoc
       \@dontframepartsintoc
    }
\@dontframepartsintoc
\newcommand\@write@thisfl@gintoc[1]{%
    {%
    \let\protect\@unexpandable@protect
    \edef\@tempa{%
       \write\@auxout{\string\@writefile{toc}{\protect#1}}}%
    \@tempa
    }%
   }%
\newif\if@frame@switch
\@frame@switchfalse
\AtBeginDocument{\@write@thisfl@gintoc\@frame@switchfalse}
\newif\if@thisnotframed
\@thisnotframedtrue
\newcommand\FrameThisInToc{%
   \@write@thisfl@gintoc\@frame@switchtrue
   \global\@frame@switchtrue % important pour le reset
   \@write@thisfl@gintoc\@thisnotframedfalse
   \global\@thisnotframedfalse
   }
\newcommand\DontFrameThisInToc{%
   \@write@thisfl@gintoc\@frame@switchtrue
   \global\@frame@switchtrue % important pour le reset
   \@write@thisfl@gintoc\@thisnotframedtrue
   \global\@thisnotframedtrue
   }
\newcommand\reset@frame@switch{%
  \if@frame@switch
     \@write@thisfl@gintoc\@frame@switchfalse
     \global\@frame@switchfalse
  \fi
  }
\def\@define@l@chapter{%
   \ifx\l@chapter\undefined
     \newcommand\l@chapter[2]{\l@genericfr@me{chapter}{##1}{##2}}%
   \else
     \renewcommand\l@chapter[2]{\l@genericfr@me{chapter}{##1}{##2}}%
   \fi
  \let\l@tulstarchapter\l@chapter
  }
\AtBeginDocument{\@define@l@chapter}
\newcommand\l@spsection[2]{%
  \ifnum \c@tocdepth >\m@ne
    \addpenalty{-\@highpenalty}%
    \vskip 1.0em \@plus\p@
    \setlength\@tempdima{1.5em}%
    \begingroup
      \parindent\z@ \rightskip\@pnumwidth
      \parfillskip -\@pnumwidth
      \advance\leftskip\@tempdima
      \hskip -\leftskip\relax
      \l@main@line{C}{Y}{#1}{#2}%
      \penalty\@highpenalty
    \endgroup
  \fi}
\renewcommand\l@part[2]{\l@genericfr@me{part}{#1}{#2}}
\let\l@starpart\l@part
\newcommand\l@genericfr@me[3]{% #1=chapter ou part
  \def\@framed@{}% default=yes
  \if@frame@switch
     \if@thisnotframed
        \def\@framed@{no}%
     \fi
  \else
     \if T\csname @#1snotframedintoc\endcsname
        \def\@framed@{no}%
     \fi
  \fi
  \csname l@#1if\@framed@ frame\endcsname{#2}{#3}%
  }%
\newcommand\@fr@mew@rning[2]{% #1=chapter ou part
  \if@frame@switch
     \if T\csname @#1snotframedintoc\endcsname
        \if@thisnotframed
            \ClassWarning{thesul}{The command
                                     \protect\DontFrameThisInToc\space
                                     has no use,\MessageBreak
                                     since by default,
                                     no #2 entry is framed,\MessageBreak}%
        \fi
     \else
        \if@thisnotframed
        \else
           \ClassWarning{thesul}{The command \protect\FrameThisInToc\space
                                    has no use,\MessageBreak
                                    since by default,
                                    all #2 entries are framed,\MessageBreak}%
        \fi
     \fi
  \fi
  }
\newcommand\@number@w@rning[1]{% #1 =chapter ou part
   \def\@framed@{Y}% default=yes
   \if@frame@switch
     \if@thisnotframed
        \def\@framed@{N}%
     \fi
   \else
     \if T\csname @#1snotframedintoc\endcsname
        \def\@framed@{N}%
     \fi
   \fi
   \if@numbertocswitch
      \if@numberintoc
         \ifx\@framed@ N%
             \ClassWarning{thesul}{The command
                                      \protect\NumberThisInToc\space
                                      has no use here,\MessageBreak}%
         \fi
      \else
         \ifx\@framed@ Y%
            \ClassWarning{thesul}{The command
                                     \protect\DontNumberThisInToc\space
                                     has no use here,\MessageBreak}%
         \fi
      \fi
   \fi
  }
\newcommand\l@partifnoframe[2]{%
  \ifnum \c@tocdepth >-2\relax
    \addpenalty{-\@highpenalty}%
    \addvspace{2.25em \@plus\p@}%
    \begingroup
      \setlength\@tempdima{3em}%
      \parindent \z@ \rightskip \@pnumwidth
      \parfillskip -\@pnumwidth
      \l@main@line{P}{Y}{#1}{#2}%
       \nobreak
         \global\@nobreaktrue
         \everypar{\global\@nobreakfalse\everypar{}}
    \endgroup
  \fi}
\newcommand\l@partifframe[2]{%
  \ifnum \c@tocdepth >-2\relax
    \addpenalty{-\@highpenalty}%
    \addvspace{2.25em \@plus\p@}%
    \begingroup
      \setlength\@tempdima{3em}%
      \setlength\@tempdimb{6.4pt}%
      \setlength\@tempdimc{10pt}%
      \advance\@tempdimb\@tempdimc
      \vskip2\baselineskip plus\baselineskip minus\baselineskip
      \moveleft\@tempdimc
         \vbox{%
            \advance\hsize\@tempdimc
            \parindent \z@
            \hrule
            \vskip1mm%
            \hrule
            \hbox{%
               \strut\hskip10pt%
               \vbox{%
                  \advance\hsize-10pt%
                  \vskip.5\baselineskip
                  \parindent \z@ \rightskip \z@
                  \l@main@line{P}{N}{#1}{#2}%
                  \nobreak
                  \global\@nobreaktrue
                  \everypar{\global\@nobreakfalse\everypar{}}%
                  \vskip.4\baselineskip
                }% \vbox
             }% \hbox
            \hrule
            \vskip1mm%
            \hrule
          }% \vbox
       \vskip2\baselineskip plus\baselineskip minus\baselineskip
    \endgroup
 \fi}
\let\@cutline=\par  % for further customization
\newcommand\l@chapterifnoframe[2]{%
  \ifnum \c@tocdepth >\m@ne
    \addpenalty{-\@highpenalty}%
    \vskip 1.0em \@plus\p@
    \setlength\@tempdima{1.5em}%
    \begingroup
      \parindent \z@ \rightskip \@pnumwidth
      \parfillskip -\@pnumwidth
      \if@there@were@p@rts\advance\leftskip20pt\fi
      \l@main@line{C}{Y}{#1}{#2}%
      \penalty\@highpenalty
    \endgroup
  \fi}
\newcommand\l@chapterifframe[2]{%
  \ifnum \c@tocdepth >\m@ne
     \addpenalty{-\@highpenalty}%
     \vskip 1.0em \@plus\p@
     \setlength\@tempdima{1.5em}%
     \setlength\@tempdimb{6.4pt}%
     \setlength\@tempdimc{20pt}%
     \if@there@were@p@rts\advance\@tempdimb-\@tempdimc\fi
     \begingroup
        \moveleft\@tempdimb
           \vbox{%
               \hrule
               \hbox{%
                   \vrule
                   \strut\hskip6pt%
                   \vbox{%
                      \advance\hsize-6pt%
                      \if@there@were@p@rts\advance\hsize-\@tempdimc\fi
                      \parindent\z@
                      \rightskip\@pnumwidth
                      \parskip\z@
                      \def\numberline##1{%
                          {%
                          \setbox0=\hbox{##1}%
                          \ifdim\wd0<\@tempdima
                             \ifdim\wd0=0pt%
                             \else
                                \hbox to\@tempdima{##1\hfil}%
                                \@cutline
                             \fi
                          \else
                              ##1%
                              \@cutline
                          \fi
                          }%
                        }%
                      \l@main@line{C}{N}{#1}{#2}%
                      }%
                   \hskip6pt%
                   \vrule
                 }%
               \hrule
             }%
        \penalty\@highpenalty
     \endgroup
  \fi
  }
\newif\if@paragraph@shift
\let\@dottedtocline@old\@dottedtocline
\def\@dottedtocline#1#2#3#4#5{\setlength\@tempdimb{#2}%
    \if@there@were@p@rts\if@paragraph@shift\advance\@tempdimb20pt%
                                           \@paragraph@shiftfalse\fi\fi
    \@dottedtocline@old{#1}{\@tempdimb}{#3}{#4}{#5}}
\renewcommand*\l@section{\@paragraph@shifttrue\@dottedtocline{1}{1.5em}{2.3em}}
\renewcommand*\l@subsection{\@paragraph@shifttrue
                            \@dottedtocline{2}{3.8em}{3.2em}}
\renewcommand*\l@subsubsection{\@paragraph@shifttrue
                               \@dottedtocline{3}{7.0em}{4.1em}}
\renewcommand*\l@paragraph{\@paragraph@shifttrue\@dottedtocline{4}{10em}{5em}}
\renewcommand*\l@subparagraph{\@paragraph@shifttrue
                              \@dottedtocline{5}{12em}{6em}}
\renewcommand*\l@figure{\@paragraph@shiftfalse\@dottedtocline{1}{1.5em}{2.3em}}
\let\l@table\l@figure
\let\frontmatter=\undefined
\let\backmatter=\undefined
\newif\if@numberintoc
\@numberintoctrue
\newif\if@numbertocswitch
\@numbertocswitchfalse
\newcommand\DontNumberThisInToc{%
   \@write@thisfl@gintoc\@numbertocswitchtrue
   \global\@numbertocswitchtrue % important pour le reset
   \@write@thisfl@gintoc\@numberintocfalse
   \global\@numberintocfalse
   }
\newcommand\NumberThisInToc{
   \@write@thisfl@gintoc\@numbertocswitchtrue
   \global\@numbertocswitchtrue % important pour le reset
   \@write@thisfl@gintoc\@numberintoctrue
   \global\@numberintoctrue
   }
\newcommand\reset@numbertocswitch{%
  \if@numbertocswitch
     \@write@thisfl@gintoc\@numbertocswitchfalse
     \global\@numbertocswitchfalse
  \fi
  }
\newcommand\l@main@line[4]{%
  {\leavevmode
   \if#1P%
      \large
   \fi
   \bfseries
   \strut#3%
   \if@numbertocswitch
      \if@numberintoc
         \nobreak\hfill \nobreak\hbox to\@pnumwidth{\hss #4}%
      \fi
      \@numbertocswitchfalse
   \else
     \if#2Y%
        \nobreak\hfill \nobreak\hbox to\@pnumwidth{\hss #4}%
     \fi
   \fi
   \hfil\strut
   \par}%
}
\newif\if@intoc
\@intoctrue
\newif\if@tocswitch
\@tocswitchfalse
\newcommand\DontWriteThisInToc{\global\@tocswitchtrue\global\@intocfalse}
\newcommand\WriteThisInToc{\global\@tocswitchtrue\global\@intoctrue}
\newcounter{division}
\newcommand{\@division@inc@hook}{\addtocounter{division}{1}}
\def\numberline#1{{%
         \setbox0=\hbox{#1}%
         \ifdim\wd0<\@tempdima
            \hbox to\@tempdima{#1\hfil}%
         \else
            #1\ %
         \fi}}
\def\@chapter[#1]#2{\@generic@chapter{chapter}[#1]{#2}}
\newcommand{\@generic@chapter@hook}[3]{}
\newcommand{\@generic@chapter@lasthook}[3]{}
\def\@generic@chapter#1[#2]#3{%
    \global\@tocswitchfalse
    \@division@inc@hook
    \@generic@chapter@hook{#1}{#2}{#3}%
    \ifnum \c@secnumdepth >\m@ne
        \refstepcounter{#1}%
        \typeout{\@chapapp\space\thechapter.}%
        \addcontentsline{toc}{chapter}%
             {\protect\numberline{\@chapter@title\thechapter}#2}%
    \else
        \addcontentsline{toc}{chapter}{#2}
    \fi
    \@fr@mew@rning{chapter}{#1}%
    \@number@w@rning{chapter}%
    \reset@numbertocswitch
    \reset@frame@switch
    \let\@chaptermark\orig@chaptermark
    \pagestyle{\current@ps}%
    \chaptermark{#2}%
    \addtocontents{lof}{\protect\addvspace{10\p@}}%
    \addtocontents{lot}{\protect\addvspace{10\p@}}%
    \if@twocolumn
        \@topnewpage[\@makechapterhead{#3}]%
    \else
        \@makechapterhead{#3}%
        \@afterheading
    \fi
    \ChapterPrefix
    \@generic@chapter@lasthook{#1}{#2}{#3}%
  }
\newcommand{\@part@hook}[2]{}
\def\@part[#1]#2{%
    \@division@inc@hook
    \@part@hook{#1}{#2}%
    \ifnum \c@secnumdepth >-2\relax
      \refstepcounter{part}%
                      % \@part@title ajoute' ici (21 juin 1994)
      \addcontentsline{toc}{part}{\@part@title\thepart\hspace{1em}#1}%
    \else
      \addcontentsline{toc}{part}{#1}%
    \fi
    \@fr@mew@rning{part}{part}%
    \@number@w@rning{part}%
    \reset@numbertocswitch
    \reset@frame@switch
    \global\@tocswitchfalse
    \markboth{}{}
    {\@title@lignment
     \interlinepenalty \@M
     \reset@font
     \ifnum \c@secnumdepth >-2\relax
       \huge\bfseries \partname~\thepart
       \par
       \vskip 20\p@
     \fi
     \Huge \bfseries #2\par}%
    \@endpart}
\newcommand{\@spart@hook}[1]{}
\renewcommand\@spart[1]{%
    \@division@inc@hook
    \@spart@hook{#1}%
    \ifnum \c@secnumdepth >-2\relax
      \addcontentsline{toc}{starpart}{%\protect\numberline{}
                                      #1}%
    \else
      \addcontentsline{toc}{starpart}{#1}%
    \fi
    \@fr@mew@rning{part}{part}%
    \@number@w@rning{part}%
    \reset@numbertocswitch
    \reset@frame@switch
    \global\@tocswitchfalse
    \markboth{}{}
    {\@title@lignment
     \interlinepenalty \@M
     \reset@font
     \Huge \bfseries #1\par}%
    \@endpart}
\newif\if@st@rch@ptersintoc
\@st@rch@ptersintoctrue
\newcommand\DontWriteStarChaptersInToc{\global\@st@rch@ptersintocfalse}
\newcommand\@in@toc@contents[1]{%
   \ifnum \c@secnumdepth >\m@ne
       \addcontentsline{toc}{tulstarchapter}{%\protect\numberline{}
                                          #1}%
   \else
       \addcontentsline{toc}{tulstarchapter}{#1}
   \fi
 }%
\renewcommand\@schapter[1]{\@generic@schapter{chapter}[#1]}
\newcommand{\@generic@schapter@hook}[2]{}
\newcommand{\@generic@schapter@lasthook}[2]{}
\def\@generic@schapter#1[#2]{%
    \@division@inc@hook
    \@generic@schapter@hook{#1}{#2}%
    \if@tocswitch
        \if@st@rch@ptersintoc
            \if@intoc
                 \ClassWarning{thesul}%
                     {You said \protect\WriteThisInToc\space
                      but\MessageBreak
                      the entry was going
                      to be put in the toc.\MessageBreak
                      You can safely remove it,}%
                 \@in@toc@contents{#2}%
            \else % \DontWriteThisInToc
            \fi
        \else
            \if@intoc  % \WriteThisInToc
                 \@in@toc@contents{#2}%
            \fi
        \fi
    \else
        \if@st@rch@ptersintoc
            \@in@toc@contents{#2}%
        \fi
    \fi
    \@fr@mew@rning{chapter}{#1}%
    \@number@w@rning{chapter}%
    \reset@numbertocswitch
    \reset@frame@switch
    \global\@tocswitchfalse
    \generic@mark{#2}%
    %\markboth {\@he@dings@function{#2}}{}%
    \addtocontents{lof}{\protect\addvspace{10\p@}}%
    \addtocontents{lot}{\protect\addvspace{10\p@}}%
    \setcounter{section}{0}
    \setcounter{equation}{0}
    \setcounter{figure}{0}
    \setcounter{table}{0}
    \if@twocolumn
        \if@notop@page
           \@makeschapterhead{#2}%
        \else
           \@topnewpage[\@makeschapterhead{#2}]%
        \fi
    \else
        \@makeschapterhead{#2}%
        \@afterheading
    \fi
    \NoChapterPrefix
    \@generic@schapter@lasthook{#1}{#2}%
  }
\newif\if@sec@in@toc
\def\@sect#1#2#3#4#5#6[#7]#8{%
  \ifnum #2>\c@secnumdepth
    \let\@svsec\@empty
  \else
    \refstepcounter{#1}%
    \protected@edef\@svsec{\@seccntformat{#1}\relax}%
  \fi
  \@tempskipa #5\relax
  \ifdim \@tempskipa>\z@
    \begingroup
      #6{%
        \@hangfrom{\hskip #3\relax\@svsec}%
          \interlinepenalty \@M #8\@@par}%
    \endgroup
    \@sec@in@toctrue
    \if@tocswitch\if@intoc\else\@sec@in@tocfalse\fi\@tocswitchfalse\fi
    \if@sec@in@toc
      \csname #1mark\endcsname{#7}%
      \addcontentsline{toc}{#1}{%
        \ifnum #2>\c@secnumdepth \else
          \protect\numberline{\csname the#1\endcsname}%
        \fi
        #7}%
    \fi
  \else
    \if@sec@in@toc
      \def\@svsechd{%
        #6{\hskip #3\relax
        \@svsec #8}%
        \csname #1mark\endcsname{#7}%
        \addcontentsline{toc}{#1}{%
          \ifnum #2>\c@secnumdepth \else
            \protect\numberline{\csname the#1\endcsname}%
          \fi
          #7}}%
    \fi
  \fi
  \@xsect{#5}}
\newcommand{\@chapter@title}{}
\newcommand{\WriteChapterLabelInToc}%
              {\gdef\@chapter@title{\@chapapp\ }} % = \chaptername
\newcommand{\@part@title}{}
\newcommand{\WritePartLabelInToc}{\gdef\@part@title{Partie\ }} %
\newcommand\@thesection@prefix{\thechapter.}
\newcommand\renew@continuous[2]{%
   \csname if@#1s@continuous\endcsname
      \expandafter\renewcommand\csname the#1\endcsname{\arabic{#1}}%
   \else
      \expandafter\renewcommand\csname the#1\endcsname{#2\arabic{#1}}%
   \fi
  }
\newcommand\C@Prefix[1]{%
        \renewcommand\@thesection@prefix{#1}%
        \renew@continuous{equation}{#1}%
        \renew@continuous{figure}{#1}%
        \renew@continuous{table}{#1}%
        }
\newcommand\ChapterPrefix{\C@Prefix{\thechapter.}}
\newcommand\NoChapterPrefix{\C@Prefix{}}
\newif\if@chapterinref
\@chapterinreftrue
\newcommand\NoChapterNumberInRef{\global\@chapterinreffalse}
\def\special@section{\def\thesection{\@thesection@prefix\arabic{section}}}
\def\normal@section{\def\thesection{\thechapter.\arabic{section}}}
\let\@sect@old=\@sect
\def\@sect#1#2#3#4#5#6[#7]#8{%
     \special@section
     \@sect@old{#1}{#2}{#3}{#4}{#5}{#6}[#7]{#8}%
     \normal@section
     \if@chapterinref
        \edef\@currentlabel{\csname p@#1\endcsname\csname the#1\endcsname}%
     \fi
     }
\newcommand\@original@endpart{%
    \vfil
    \newpage
    \if@twoside
        \hbox{}%
        \thispagestyle{empty}%
        \newpage
    \fi
    \if@tempswa
        \twocolumn
    \fi
    }
\newcommand\NewPageAfterParts{\gdef\@endpart{\@original@endpart}}
\newcommand\NoNewPageAfterParts{\gdef\@endpart{\vskip1cm}}
\let\original@pagestyle@cmd=\pagestyle
\newcommand{\current@ps}{ThesisHeadings}
\renewcommand{\pagestyle}[1]{%
   \def\new@ps{#1}%
   \def\td@ps{thesisdraft}%
   \ifx\new@ps\td@ps
   \else
      \edef\current@ps{#1}%
   \fi
   \original@pagestyle@cmd{#1}%
   }
\let\original@thispagestyle@cmd=\thispagestyle
\renewcommand{\thispagestyle}[1]{%
      \def\tmp@ps@name{#1}%
      \def\french@ps@name{french}%
      \ifx\tmp@ps@name\french@ps@name
      \else
        \original@thispagestyle@cmd{#1}%
      \fi
      }
\newcommand\@chapter@ps{plain}
\newcommand{\ChapterPageStyle}[1]{\renewcommand\@chapter@ps{#1}}
\newcommand\@part@ps{plain}
\newcommand{\PartPageStyle}[1]{\renewcommand\@part@ps{#1}}
\newcommand{\@empty@ps@cmd}{}
\newcommand{\EmptyPageStyle}[1]{%
      \renewcommand\@empty@ps@cmd{\thispagestyle{#1}}}
\newcommand{\EmptyNewPage}{\newpage\hbox{}\@empty@ps@cmd\newpage}
\newcommand\orig@chaptermark[1]{%
        \markboth {\@he@dings@function{\ifnum \c@secnumdepth >\m@ne
            \@chapapp\ \thechapter. \ \fi
            #1}}{}%
        }%
\let\@chaptermark\orig@chaptermark
\newcommand\@generic@mark[1]{\markboth {\@he@dings@function{#1}}{}}
\newcommand\generic@mark[1]{%
        \let\@chaptermark\@generic@mark
        \pagestyle{\current@ps}%
        \chaptermark{#1}%
        }
\newcommand\@sectionmark[1]{%
        \markright {\@he@dings@function{\ifnum \c@secnumdepth >\z@
            \thesection. \ \fi
            #1}}%
        }%
\newlength\HeadRuleWidth
\newlength\HeadRuleSep
\setlength{\HeadRuleWidth}{0pt}
\setlength{\HeadRuleSep}{2mm}
\newcommand\@gener@lhe@d[2]{%
  {\setbox0=\hbox{#1}%
  \ifdim\wd0=0pt%
      \hbox to\textwidth{#2}%
  \else
      \vtop{\hbox to\textwidth{#2}
            \vbox to0pt{\vskip\HeadRuleSep
                        \hrule width\textwidth
                               height\HeadRuleWidth depth0pt\relax
                        \vss}
           }%
  \fi
  }%
  }
\newcommand\@gener@loddhe@d{%
    \@gener@lhe@d{\leftmark\rightmark}{\hfil\slshape\rightmark}%
    }
\newcommand\@gener@levenhe@d{%
    \@gener@lhe@d\leftmark{{\slshape\leftmark}\hfil}%
    }
\newtoks\OddFoot
\newtoks\EvenFoot
\newtoks\OddHead
\newtoks\EvenHead
\OddFoot={}%
\EvenFoot={}%
\OddHead={{}{}}%
\EvenHead={{}{}}%
\newcommand\ps@Fancy{%
    \def\@oddfoot{\the\OddFoot}%
    \def\@evenfoot{\the\EvenFoot}%
    \def\@evenhead{\expandafter\@gener@lhe@d\the\EvenHead}%
    \def\@oddhead{\expandafter\@gener@lhe@d\the\OddHead}%
    \let\@mkboth\markboth
    \let\chaptermark\@chaptermark
    \let\sectionmark\@sectionmark
    }
\newcommand\ps@ThesisHeadings{%
    \def\@oddfoot{\hfil\thepage\hfil}%
    \def\@evenfoot{\hfil\thepage\hfil}%
    \def\@evenhead{\@gener@levenhe@d}%
    \def\@oddhead{\@gener@loddhe@d}%
    \let\@mkboth\markboth
    \let\chaptermark\@chaptermark
    \let\sectionmark\@sectionmark
    }
\newcommand\ps@StandardHeadings{%
    \let\@oddfoot\@empty
    \let\@evenfoot\@empty
    \def\@evenhead{\@gener@lhe@d{\leftmark}%
                                {\thepage\hfil{\slshape\leftmark}}}%
    \def\@oddhead{\@gener@lhe@d{\leftmark\rightmark}%
                                {{\slshape\rightmark}\hfil\thepage}}%
    \let\@mkboth\markboth
    \let\chaptermark\@chaptermark
    \let\sectionmark\@sectionmark
    }
\newcommand\ps@ThesisHeadingsI{%
    \let\@oddfoot\@empty
    \let\@evenfoot\@empty
    \def\@evenhead{\@gener@lhe@d{\leftmark}%
                                {\thepage\qquad{\slshape\leftmark}\hfil}}%
    \def\@oddhead{\@gener@lhe@d{\leftmark\rightmark}%
                                {\hfil{\slshape\rightmark}\qquad\thepage}}%
    \let\@mkboth\markboth
    \let\chaptermark\@chaptermark
    \let\sectionmark\@sectionmark
    }
\newcommand\ps@ThesisHeadingsII{%
    \def\@oddfoot{\hfil\thepage}%
    \def\@evenfoot{\thepage\hfil}%
    \def\@evenhead{\@gener@lhe@d{\leftmark}%
                                {{\slshape\leftmark}\hfil}}%
    \def\@oddhead{\@gener@lhe@d{\leftmark\rightmark}%
                                {\hfil\slshape\rightmark}}%
    \let\@mkboth\markboth
    \let\chaptermark\@chaptermark
    \let\sectionmark\@sectionmark
    }
\newcommand\TheBanner{\textsl{version du \TimeStamp}}
\newcommand\ps@thesisdraft{%
    \def\@dr@ftb@nner{%
        \vbox to0pt{\vss
                    \hbox{\footnotesize\fbox{\texttt{\jobname:}\TheBanner}}%
                    \vskip\headheight
                    }%
        }%
    \let\old@oddhead=\@oddhead
    \let\old@evenhead=\@evenhead
    \ifx\@oddhead\@empty
       \def\old@oddhead{\hfil}%
    \fi
    \ifx\@evenhead\@empty
       \def\old@evenhead{\hfil}%
    \fi
    \def\@oddhead{{}\rlap{\hbox to\hsize{\hfil\llap{\@dr@ftb@nner}}}%
                    \old@oddhead}%
    \def\@evenhead{{}\rlap{\@dr@ftb@nner}\old@evenhead}%
  }
\newcommand{\UppercaseHeadings}{\global\let\@he@dings@function=\uppercase}
\newcommand{\NormalHeadings}{\global\let\@he@dings@function=\relax}
\newcommand{\UnderlineHeadings}{\global\let\@he@dings@function=\underline}
\newcommand{\FormatHeadingsWith}[1]{\global\let\@he@dings@function=#1 }
\NormalHeadings
\pagestyle{StandardHeadings}
\newcommand{\abs@ps}{empty}
\newcommand{\NumberAbstractPages}{\edef\abs@ps{\@chapter@ps}}
\newcommand{\DontNumberAbstractPages}{\renewcommand{\abs@ps}{empty}}
\newif\ifabstracts@even
\newcommand{\AbstractsOnOddPage}{\abstracts@evenfalse}
\newcommand{\AbstractsOnEvenPage}{\abstracts@eventrue}
\newcommand{\@abstract@hook}[1]{}
\newenvironment{ThesisAbstract}
    {\ifabstracts@even\@newevendoublepage\else\@newdoublepage\fi
     \edef\saved@ps{\current@ps}%
     \pagestyle{\abs@ps}
     \markboth{}{}
     \def\@abstr@ct@beginning##1##2{%
         \section*{\@title@lignment ##1}
         \@abstract@hook{##1}%
         \if@tocswitch
            \DontFrameThisInToc
            \if@classic@section
               \addcontentsline{toc}{tulstarchapter}{##1}
            \else
               \addcontentsline{toc}{spsection}{##1}
            \fi
         \fi
         \reset@numbertocswitch
         \reset@frame@switch
         \def\KeyWords####1{\par\bigskip\noindent\textbf{##2:} ####1\par}
         }
     \newenvironment{FrenchAbstract}
        {\@abstr@ct@beginning{R\'esum\'e}{Mots-cl\'es}}
        {\vglue1cm minus 8mm}
     \newenvironment{EnglishAbstract}
        {\@abstr@ct@beginning{Abstract}{Keywords}%
         \ifx\english\@undefined
             \bgroup\language=0\relax
         \else
             \begin{english}
         \fi
         \leavevmode\hbox to\parindent{}\ignorespaces % 22/7/1994
        }
        {\ifx\english\@undefined
             \egroup
         \else
             \end{english}
         \fi
         \vglue1cm minus 8mm
        }
     \@mkboth{}{}%
     \vglue1cm
    }
    {\global\@tocswitchfalse
     \global\@classic@sectionfalse
     %\@newdoublepage
     \long\def\@empty@ps{empty}%
     \newpage
     \if@twoside
       \ifodd\c@page
       \else
          \hbox{}%
          \ifx\@empty@ps\abs@ps
          \else
             \@empty@ps@cmd
          \fi
          \newpage
          \if@twocolumn\hbox{}\newpage\fi
          \pagestyle{\saved@ps}%
       \fi
     \else
       \pagestyle{\saved@ps}%
     \fi
     %\addtocounter{page}{-2}%
    }
\newcommand{\AcknowledgmentName}{Remerciements}
\newcommand{\@acknowledgment@hook}{}
\newenvironment{ThesisAcknowledgments}
    {\@newdoublepage
     \section*{\@title@lignment\AcknowledgmentName}
     \@acknowledgment@hook
     \@mkboth{}{}%
     \if@tocswitch
        \if@classic@section
           \global\@classic@sectionfalse
           \addcontentsline{toc}{tulstarchapter}{\AcknowledgmentName}
        \else
           \addcontentsline{toc}{spsection}{\AcknowledgmentName}
        \fi
     \fi
     \reset@numbertocswitch
     \reset@frame@switch
     \global\@tocswitchfalse
    }
    {\par\@newdoublepage}
\newcommand{\@dedication@hook}{}
\newenvironment{ThesisDedication}
    {\@newdoublepage
     \@dedication@hook
     \@mkboth{}{}
     \vglue0pt plus.5fil
     \fontfamily{\sfdefault}\fontseries{m}\fontshape{sl}\selectfont
     \begin{flushright}
     }
    {\end{flushright}
     \vglue0pt plus1fil\@newdoublepage}
\newif\if@there@re@p@rts
\newif\if@there@were@p@rts
\AtEndDocument{\@see@if@parts}
\def\@see@if@parts{%
    \immediate\openout\@gen@toc@aux=\jobname.flg
    \if@there@re@p@rts
       \immediate\write\@gen@toc@aux{\string\@there@were@p@rtstrue}%
    \else
       \immediate\write\@gen@toc@aux{\string\@there@were@p@rtsfalse}%
    \fi
    }
\renewcommand\part{%
     \@nnex@in@l@stp@rtfalse
     \gdef\@chapapp{\chaptername}\gdef\thechapter{\arabic{chapter}}%
     \global\@there@re@p@rtstrue
     \cleardoublepage
     \thispagestyle{\@part@ps}%
     \if@twocolumn
         \onecolumn
         \@tempswatrue
     \else
         \@tempswafalse
     \fi
     \hbox{}\vfil
     \secdef\@part\@spart}
\renewcommand\chapter{%
   \if@nnex@in@l@stp@rt
     \let\next=\Annex
   \else
     \let\next=\@real@chapter
   \fi
   \next
   }
\newcommand\@real@chapter{%
    \if@openright\cleardoublepage\else\clearpage\fi
    \thispagestyle{\@chapter@ps}%
    \global\@topnum\z@
    \@afterindentfalse
    \secdef\@chapter\@schapter
    }
\newcommand\no@clear@chapter{%
         \thispagestyle{\@chapter@ps}%
         \global\@topnum\z@
         \@afterindentfalse
         \if@classic@section
            \global\@classic@sectionfalse
            \def\@nxt@cmd{\secdef\@chapter\@schapter}%
         \else
            \def\@nxt@cmd{\secdef\@spsection\@sspsection}%
         \fi
         \@nxt@cmd
         }
\renewcommand\@makechapterhead[1]{%
  \vspace*{50\p@}%
  {\parindent \z@ \@title@lignment \reset@font
    \ifnum \c@secnumdepth >\m@ne
      \huge\bfseries \@chapter@title@head{} \thechapter
      \par
      \vskip 20\p@
    \fi
    \Huge \bfseries #1\par
    \nobreak
    \vskip 40\p@
  }}
\renewcommand\@makeschapterhead[1]{%
  \vspace*{50\p@}%
  {\parindent \z@ \@title@lignment
    \reset@font
    \Huge \bfseries #1\par
    \nobreak
    \vskip 40\p@
  }}
\newcommand{\@chapter@title@head}{\@chapapp}
\newcommand{\NoChapterHead}{\renewcommand{\@chapter@title@head}{}}
\newcommand{\@title@lignment}{\centering}
\newcommand{\AlignTitlesLeft}{
    \renewcommand{\@title@lignment}{\raggedright}}
\newcommand{\CenterTitles}{
    \renewcommand{\@title@lignment}{\centering}}
\newcommand{\AlignTitlesRight}{
    \renewcommand{\@title@lignment}{\raggedleft}}
\newif\if@classic@section
\newcommand{\NormalSection}{\@classic@sectiontrue}
\newcommand{\SpecialSection}{\if@openright\cleardoublepage\else\clearpage\fi
                    \thispagestyle{\@chapter@ps}%
                    \global\@topnum\z@
                    \@afterindentfalse
                    \secdef\@spsection\@sspsection}
\newcommand{\@spsection@hook}[2]{}
\def\@spsection[#1]#2{%
    \@division@inc@hook
  \@spsection@hook{#1}{#2}%
    \if@tocswitch
       \if@intoc
          \addcontentsline{toc}{spsection}{#1}%
       \fi
    \else
       \addcontentsline{toc}{spsection}{#1}%
    \fi
    \reset@numbertocswitch
    \reset@frame@switch
    \global\@tocswitchfalse
      \generic@mark{#1}%
    %\markboth {\@he@dings@function{#2}}{}%
    \addtocontents{lof}{\protect\addvspace{10\p@}}%
    \addtocontents{lot}{\protect\addvspace{10\p@}}%
    \if@twocolumn
        \if@notop@page
           \@makeschapterhead{#2}%
        \else
           \@topnewpage[\@makeschapterhead{#2}]%
        \fi
    \else
        \@makeschapterhead{#2}%
        \@afterheading
    \fi
  \NoChapterPrefix
  }
\def\@sspsection#1{\@spsection[]{#1}}
\if@dont@load@french
\else
  \AtBeginDocument{\def\contentsname{Sommaire}}%
\fi
\newcommand{\@toc@hook}{}
\renewcommand\tableofcontents{%
    \edef\sav@baselinestretch{\baselinestretch}
    \if@twocolumn
      \@restonecoltrue\onecolumn
    \else
      \@restonecolfalse
    \fi
    \@toc@hook
    \DontWriteThisInToc
    \chapter*{\contentsname}
      \generic@mark{\contentsname}%
    \def\baselinestretch{\@tocstretch}\small\normalsize
    \makeatletter
    \InputIfFileExists{\jobname.flg}{}{}%
    \makeatother
    \@starttoc{toc}%
    \edef\baselinestretch{\sav@baselinestretch}\small\normalsize
    \if@restonecol\twocolumn\fi
    }
\newcommand\@tocstretch{1.3}
\newcommand\SetTocSpacing[1]{\renewcommand\@tocstretch{#1}}
\newcommand{\@toc@line}{\hbox to\hsize{\hbox to.25\hsize{}%
                                       \hrulefill
                                       \hbox to.25\hsize{}}}
\newcommand\PutLineInToc{\@write@thisfl@gintoc\@toc@line}
\newcommand\PutNewPageInToc{\@write@thisfl@gintoc\newpage}
\newwrite\@gen@toc@aux
\AtEndDocument{\closeout\@gen@toc@aux}
\newif\if@notop@page
\@notop@pagefalse
\newcommand\@Ind@Introduction{}
\newcommand\BeginIndWith[1]%
           {\renewcommand\@Ind@Introduction{#1\par\bigskip}}
\renewenvironment{theindex}
    {\cleardoublepage
     \global\@notop@pagetrue
     \twocolumn[\no@clear@chapter{\indexname}\@Ind@Introduction]%
     \global\@notop@pagefalse
      \generic@mark{\indexname}%
     \columnseprule \z@
     \columnsep 35\p@
     \thispagestyle{\@chapter@ps}\parindent\z@
     \parskip\z@ \@plus .3\p@\relax
     \let\item\@idxitem}
    {\onecolumn}
\newcommand\PrintIndex{\@input@{\jobname.ind}}
\AtBeginDocument{%
    \ifx\@printindex\undefined
       \let\printindex\PrintIndex
    \else
       \def\printindex{\@ifnextchar [{\@printindex}{\@printindex[default]}}
       \let\PrintIndex\printindex
    \fi}
\newcommand\@Glo@Introduction{}
\newcommand\BeginGloWith[1]%
           {\renewcommand\@Glo@Introduction{#1\par\bigskip}}
\newenvironment{TheGlossary}
    {\if@twocolumn
         \def\@glo@cmd{\global\@notop@pagetrue
                       \twocolumn[\no@clear@chapter{\glossaryname}%
                                  \@Glo@Introduction]%
                       \global\@notop@pagefalse}%
     \else
         \def\@glo@cmd{\no@clear@chapter{\glossaryname}%
                       \@Glo@Introduction}%
     \fi
     \onecolumn
     \cleardoublepage
     \@glo@cmd
    \generic@mark{\glossaryname}%
     \columnseprule \z@
     \columnsep 35\p@
     \thispagestyle{\@chapter@ps}\parindent\z@
     \parskip\z@ \@plus .3\p@\relax
     \let\item\@idxitem}
    {\onecolumn}
\newcommand\PrintGlossary{\@input@{\jobname.gls}}
\if@dont@load@french
   \def\glossaryname{Glossary}%
\fi
\newcommand{\glogobble}[1]{}
\newcommand{\Glossary}[3][]{\glossary{#1#2@{\textbf{#2}} : #3|glogobble}}
\newcommand\@Bib@Introduction{}
\newcommand\BeginBibWith[1]%
           {\renewcommand\@Bib@Introduction{#1\par\bigskip}}
\renewenvironment{thebibliography}[1]
     {\if@classic@section
           \global\@classic@sectionfalse
           \chapter*{\bibname}
      \else
         \SpecialSection{\bibname}
      \fi
      \generic@mark{\bibname}%
      \@Bib@Introduction
      \list{\@biblabel{\@arabic\c@enumiv}}%
           {\settowidth\labelwidth{\@biblabel{#1}}%
            \leftmargin\labelwidth
            \advance\leftmargin\labelsep
            \@openbib@code
            \usecounter{enumiv}%
            \let\p@enumiv\@empty
            \renewcommand\theenumiv{\@arabic\c@enumiv}}%
      \sloppy\clubpenalty4000\widowpenalty4000%
      \sfcode`\.=\@m}
     {\def\@noitemerr{\@warning{Empty `thebibliography' environment}}%
      \endlist}
\newcommand\@Lof@Introduction{}
\newcommand\BeginLofWith[1]%
           {\renewcommand\@Lof@Introduction{#1\par\bigskip}}
\renewcommand\listoffigures{%
    \if@twocolumn
      \@restonecoltrue\onecolumn
    \else
      \@restonecolfalse
    \fi
    \if@classic@section
      \global\@classic@sectionfalse
      \chapter*{\listfigurename}
    \else
      \SpecialSection{\listfigurename}
    \fi
    \generic@mark{\listfigurename}%
    \@Lof@Introduction
    \@starttoc{lof}%
    \if@restonecol\twocolumn\fi
    }
\newcommand\@Lot@Introduction{}
\newcommand\BeginLotWith[1]%
           {\renewcommand\@Lot@Introduction{#1\par\bigskip}}
\renewcommand\listoftables{%
    \if@twocolumn
      \@restonecoltrue\onecolumn
    \else
      \@restonecolfalse
    \fi
    \if@classic@section
      \global\@classic@sectionfalse
      \chapter*{\listtablename}
    \else
      \SpecialSection{\listtablename}
    \fi
    \generic@mark{\listtablename}%
    \@Lot@Introduction
    \@starttoc{lot}%
    \if@restonecol\twocolumn\fi
    }
\pagenumbering{roman}
\setlength\@tempdima{\paperheight}
\addtolength\@tempdima{-2in}
\addtolength\@tempdima{-.73in} % anciennement -1.5in
\divide\@tempdima\baselineskip
\@tempcnta=\@tempdima
\setlength\textheight{\@tempcnta\baselineskip}
\advance\textheight by \topskip
\setlength\topmargin{\paperheight}
\addtolength\topmargin{-2in}
\addtolength\topmargin{-\headheight}
\addtolength\topmargin{-\headsep}
\addtolength\topmargin{-\textheight}
\addtolength\topmargin{-\footskip}     % this might be wrong!
\addtolength\topmargin{-.5\topmargin}
\@settopoint\topmargin
\newcommand\AdjustTextheight{%
   \setlength\textheight{\paperheight}
   \addtolength\textheight{-2in}
   \addtolength\textheight{-\headheight}
   \addtolength\textheight{-\headsep}
   \addtolength\textheight{-\footskip}
   \addtolength\textheight{-2\topmargin}
   \@settopoint\textheight
   }
\newcommand\SetRealMargins[2]{%
    \oddsidemargin#1\advance\oddsidemargin-1in%
    \evensidemargin#2\advance\evensidemargin-1in%
    \textwidth\paperwidth
    \advance\textwidth-2in%
    \advance\textwidth-\oddsidemargin
    \advance\textwidth-\evensidemargin
    \hsize\textwidth
    \linewidth\hsize
    \setlength\marginparwidth   {.8in}%
    \addtolength\marginparwidth {.5\evensidemargin}%
    }%
\SetRealMargins{30mm}{20mm}%  \textwidth=210mm-50mm=160mm
\newif\if@draft
\@draftfalse
\newif\if@nnex@in@l@stp@rt
\@nnex@in@l@stp@rtfalse
\newcommand\Annexe{\global\@nnex@in@l@stp@rttrue
                   \@TULann{\appendixname}}
\newcommand\Annexes{\global\@nnex@in@l@stp@rttrue
                    \@TULann{\appendixname s}}
\newcommand{\@tulann@hook}[1]{}
\newcommand{\@tulann@lasthook}[1]{}
\def\@TULann#1{%
    \par
    \setcounter{section}{0}%
    \def\@chapapp{\appendixname}\def\thechapter{\Alph{annex}}%
    \cleardoublepage
    \@tulann@hook{#1}%
    \addcontentsline{toc}{tulstarchapter}{\protect#1}%
    \@tulann@lasthook{#1}%
    }%
\newcommand{\ThesisDraft}{%
   \if@draft
   \else
      \pagestyle{thesisdraft}%
      \@drafttrue
      \let\@old@ps=\pagestyle
      \def\pagestyle##1{%
         \@old@ps{##1}%
         \if@draft
            \@old@ps{thesisdraft}%
         \fi
         }%
   \fi
   }
\newcount\tul@hour \newcount\tul@minute
\tul@hour=\time  \divide \tul@hour by 60
\tul@minute=\time
\loop \ifnum \tul@minute > 59 \advance \tul@minute by -60 \repeat
\newcommand\now{\number\tul@hour\ h
         \ifnum \tul@minute<10 0\fi
         \number\tul@minute
        }
\newcommand\@le@pye@r{%
   \def\@leapye@rcorrection{\count6 }%
   \def\@scratch{\count8 }%
   \@leapye@rcorrection=0\relax
   \ifnum\@month>2\relax
     \@scratch\@year
     \divide\@scratch4\multiply\@scratch4\relax
     \ifnum\@scratch=\@year
       \divide\@scratch100\multiply\@scratch100\relax
       \ifnum\@scratch=\@year
          \divide\@scratch400 \multiply\@scratch400\relax
          \ifnum\@scratch=\@year
             \@leapye@rcorrection=1\relax
          \else
             \@leapye@rcorrection=0\relax
          \fi
       \else
          \@leapye@rcorrection=1\relax
       \fi
     \else
          \@leapye@rcorrection=0\relax
     \fi
   \fi
  }%
\newcommand\@weekday{%
   \@le@pye@r
   \advance\@year-1201\relax
   \def\@dayselapsed{\count10 }%
   \@dayselapsed=\@year
   \multiply\@dayselapsed365\relax
   \@scratch\@year
   \divide\@scratch4
   \advance\@dayselapsed\@scratch\relax
   \@scratch\@year
   \divide\@scratch100
   \advance\@dayselapsed-\@scratch\relax
   \@scratch\@year
   \divide\@scratch400
   \advance\@dayselapsed\@scratch
   \advance\@dayselapsed
     \ifcase\@month\or
          0\relax\or   31\relax\or  59\relax\or   90\relax\or
        120\relax\or  151\relax\or 181\relax\or  212\relax\or
        243\relax\or  273\relax\or 304\relax\or  334\relax
     \fi
   \advance\@dayselapsed\@day
   \advance\@dayselapsed\@leapye@rcorrection
   \@scratch=-\@dayselapsed
   \divide\@scratch7\relax
   \multiply\@scratch7\relax
   \advance\@dayselapsed\@scratch
  }
\newcommand\@day@of@week{}
\newcommand\WeekDay[3]{%  jour 1--31, mois 1--12,  annee
  \@WeekDay{#1}{#2}{#3}%
  \@day@of@week
  }
\newcommand\@WeekDay[3]{%  jour 1--31, mois 1--12,  annee
    {%
    \def\@day{\count0 }%
    \def\@month{\count2 }%
    \def\@year{\count4 }%
    \@day=#1\relax
    \@month=#2\relax
    \@year=#3\relax
    \@weekday
    \xdef\@day@of@week{%
        \ifcase\@dayselapsed
           dimanche\or
           lundi\or
           mardi\or
           mercredi\or
           jeudi\or
           vendredi\or
           samedi%
        \fi}%
    }%
  }
\newcommand\@timest@mp{}
\newcommand\TimeStamp{%
    \long\def\@empty{}%
    \ifx\@timest@mp\@empty
        \@WeekDay{\day}{\month}{\year}%
        \let\@@protect=\protect
        \def\protect{\noexpand\protect\noexpand}%
        \xdef\@timest@mp{\@day@of@week\ \today\ \`a \now}%
        \let\protect=\@@protect
    \fi
    \def\@empty{}%
    \@timest@mp
    }
\newcommand\not@implemented{%
     \message{***You tried to use a command******^^J}%
     \message{***which has not yet been implemented.***^^J}%
     }
\newcommand{\TUL}{{\normalfont\textsf{thesul}}}
\errorcontextlines5
\newcommand\@removefromreset[2]{\let\@tempb\@elt
   \def\@tempa#1{@&#1}\expandafter\let\csname @*#1*\endcsname\@tempa
   \def\@elt##1{\expandafter\ifx\csname @*##1*\endcsname\@tempa\else
                \noexpand\@elt{##1}\fi}%
   \expandafter\xdef\csname cl@#2\endcsname{\csname cl@#2\endcsname}%
   \let\@elt\@tempb
   \expandafter\let\csname @*#1*\endcsname\@undefined}
\newcommand\ResetChaptersAtParts{%
    \@addtoreset{chapter}{part}%
    \@addtoreset{annex}{part}%
    }
\@removefromreset{footnote}{chapter}
\newcommand\ResetFootnotesAtChapters{%
    \@addtoreset{footnote}{chapter}%
    \@addtoreset{footnote}{annex}%
    }
\newif\if@equations@continuous
\newif\if@figures@continuous
\newif\if@tables@continuous
\newcommand\ContinuousNumbering[1]{%
  \@removefromreset{#1}{chapter}%
  \csname @#1s@continuoustrue\endcsname
  }
\newcommand\@redefGOfrench{%
   \ifx\GOfrench\undefined
   \else
      \let\TUL@GOfrench\GOfrench
      \gdef\GOfrench{\TUL@GOfrench
                     \@removefromreset{chapter}{part}%
                     }
   \fi
   }
\AtBeginDocument{\@redefGOfrench}%
\newcounter {annex}
\def\theannex{\thechapter}
\@addtoreset{section}{annex}
\@addtoreset{equation}{annex}
\@addtoreset{figure}{annex}
\@addtoreset{table}{annex}
\newcommand\Annex{%
   \if@openright\cleardoublepage\else\clearpage\fi
   \thispagestyle{\@chapter@ps}%
   \global\@topnum\z@
   \@afterindentfalse
   \gdef\@chapapp{\appendixname}%
   \gdef\thechapter{\Alph{annex}}%
   \secdef\@annex\@sannex
   }
\def\@annex[#1]#2{\ifx\dominitoc\@undefined\else\stepcounter{mtc}\fi
                  \@generic@chapter{annex}[#1]{#2}}
\newcommand\@sannex[1]{\@generic@schapter{annex}[#1]}
\endinput
%%
%% End of file `thesul.cls'.
