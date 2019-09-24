%% 2014 Modified by 
%  Luca Di Stasio,
%  Computational Physics for Engineering Materials, Institute for Building Materials, ETH Zürich
%  Stefano-Franscini-Platz 3
%  CH-8093 Zürich
%
%
% This class can be redistributed and/or modified under the terms
% of the GNU Public License, version 2.
% For the context of the licence, program shall refer to all source
% files distributed with this stylefile. Note that this does not refer
% to your documents.

% This is a style file for creating LaTeX beamer presentations
% in the ETH wide corporate design. 
%
% The following options can be used when including the package:
%
%   totalframes  prints the total number of frames
%   first        uses special first frame
%   firstalt     uses special first frame (alternative version)
%   last         uses special last frame
%   firstsupp    suppresses footer on first frame
%   lastsupp     suppresses footer on last frame
%   navigation   displays navigation symbols
%
% New background (blue)
%%
%%

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{ETHclass}[2014/09/26 v0.5]

%% --- Declaration of options ---
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{beamer}}

%% --- Execution of options ---
\ProcessOptions
\LoadClass{beamer}

\RequirePackage{ifthen}
\RequirePackage{layouts}

%%% Total page settings 
% \voffset = 0pt
% \topmargin=0pt
% \headheight=0pt
% \setbeamersize{text margin left=40pt,text margin right=4pt}

\definecolor{ETHZblue}{RGB}{0,43,94}
\definecolor{forestgreen}{RGB}{34, 139, 34} 

\setbeamercolor{title}{fg=ETHZblue}
\setbeamercolor{subtitle}{fg=ETHZblue}
\setbeamercolor{section}{fg=ETHZblue}
\setbeamercolor{subsection}{fg=ETHZblue}
\setbeamercolor{enumerate item}{fg=ETHZblue}

%%% Modified Itemizing
\usepackage{amsfonts} % Package used for Item symbols
\setlength{\leftmargini}{1.75pt} % indention of item order 1
\setlength{\leftmarginii}{16pt} % indention of item order 2
\setlength{\leftmarginiii}{16pt} % indention of item order 3
\setlength{\labelsep}{10pt} %% Separation page to item

%% Size of items
\def\Tiny{\fontsize{4.25pt}{4.25pt}\selectfont}

%% Itemizing Symbol: Square
\setbeamertemplate{itemize items}[square]

%% Position and Size of items in all three orders
\useitemizeitemtemplate{%
    \Tiny\raise3.75pt\hbox{\color{forestgreen}$\blacksquare$}%
}
\usesubitemizeitemtemplate{%
    \Tiny\raise2.5pt\hbox{\color{forestgreen}$\blacksquare$}%
}
\usesubsubitemizeitemtemplate{%
    \Tiny\raise2.5pt\hbox{\color{forestgreen}$\blacksquare$}%
}

%% Titlepage
\newcommand{\totalframes}{}
\newcommand{\normalbg}{\includegraphics[width=\paperwidth,page=3]{DocMASE_template}}
\newcommand{\firstbg}{\normalbg}
\newcommand{\lastbg}{\includegraphics[width=\paperwidth,page=4]{DocMASE_template}}

%% Position of date / institute / framenumber  
\newcommand{\normalfooter}{%
\leavevmode%
  \hbox{
    \begin{beamercolorbox}[wd=.3\paperwidth,ht=2.5ex,dp=1.5ex,left]{author in head/foot}%
      \qquad\color{white}{\tiny\underline{Luca Di Stasio}}%
    \end{beamercolorbox}%

    \begin{beamercolorbox}[wd=.45\paperwidth,ht=2.5ex,dp=1.5ex,center]{title in head/foot}%
      \color{white}{Sevilla (ES) - September 26, 2019}%
    \end{beamercolorbox}%

    \begin{beamercolorbox}[wd=.2\paperwidth,ht=2.5ex,dp=1.5ex,right]{title in head/foot}%
      \color{white}{\insertframenumber\totalframes}%
    \end{beamercolorbox}%
  }}
\newcommand{\firstfooter}{%
\leavevmode%
  \hbox{
    \begin{beamercolorbox}[wd=.3\paperwidth,ht=2.5ex,dp=0.75ex,left]{author in head/foot}%
      \qquad\color{white}{\tiny\underline{Luca Di Stasio}}%
    \end{beamercolorbox}%

    \begin{beamercolorbox}[wd=.45\paperwidth,ht=2.5ex,dp=0.75ex,center]{title in head/foot}%
      \color{white}{Sevilla (ES) - September 26, 2019}%
    \end{beamercolorbox}%

    \begin{beamercolorbox}[wd=.2\paperwidth,ht=2.5ex,dp=0.75ex,right]{title in head/foot}%
      \color{white}{\insertframenumber\totalframes}%
    \end{beamercolorbox}%
  }}
\newcommand{\lastfooter}{\normalfooter}
\newcommand{\navsymb}{\setbeamertemplate{navigation symbols}{}}
\newcommand{\usespecialtitlepagetemplate}{
\makeatletter
\setbeamertemplate{title page}%{default}[1][]
{
  \vspace{8pt}
  \begin{beamercolorbox}[wd=0.99\paperwidth,ht=5.5ex,dp=1ex,sep=1.7ex,center,shadow=true]{title}
  %\vskip0.2em
    \usebeamerfont{title}
 {\fontsize{16pt}{8pt}\textbf{\inserttitle}\par}
  \ifx\insertsubtitle\@empty%
    \else%
      \vskip0.5em%
      {\fontsize{14pt}\usebeamerfont{subtitle}\usebeamercolor[fg]{subtitle}\insertsubtitle\par}%
    \fi%     
   \end{beamercolorbox}%
  %\vskip0.5em\par
  \vspace{12pt}
   {\usebeamercolor[fg]{titlegraphic}\inserttitlegraphic\par}
  \vskip0.5em \par
   \begin{beamercolorbox}[wd=0.99\paperwidth,ht=1ex,dp=1ex,sep=2.7ex,center,shadow=true]{author}
    {\fontsize{12pt}{4pt}\usebeamerfont{author}{\insertauthor}}  
   \end{beamercolorbox}
\vskip0.35em
   \begin{beamercolorbox}[wd=0.99\paperwidth,ht=1ex,dp=1ex,sep=2.7ex,center,shadow=true]{institute}
     {\fontsize{9.5pt}{4pt}\it\usebeamerfont{author}{\insertinstitute}}  
   \end{beamercolorbox}
\vskip0.75em
  %\vskip0.5em\par
   \begin{beamercolorbox}[wd=0.99\paperwidth,ht=1ex,dp=1ex,sep=2.7ex,center,shadow=true]{date}
     {\fontsize{10.5pt}{4pt}\usebeamerfont{author}{\insertdate}}  
   \end{beamercolorbox}
\vskip1.5em
\vfill
}
\makeatother
}

% Table of contents

% \setbeamertemplate{section in toc}{
%     \protect\usebeamercolor[fg]{enumerate item}%
%     \protect\includegraphics[width=2ex]{freccia_trasparente_verde_foresta.png}\hspace{.5ex}~ {\fontsize{14pt}{4pt}{\inserttocsection}}%
% }
% 
% \setbeamertemplate{subsection in toc}{
%     \protect\usebeamercolor[fg]{enumerate item}%
%     \protect\hspace{3ex}~ {\fontsize{12pt}{2pt}{\inserttocsubsection}}%
% }

\setbeamertemplate{section in toc}{%
  {\includegraphics[width=2ex]{freccia_trasparente_verde_foresta.png}\hspace{.5ex}}~\inserttocsection}
\setbeamercolor{subsection in toc}{bg=white,fg=structure}
\setbeamertemplate{subsection in toc}{%
  \hspace{1.5em}{\color{forestgreen}\rule[0.3ex]{3pt}{3pt}}~\inserttocsubsection\par}
  
%\def\inserttocsection{{\includegraphics[width=2ex]{freccia_trasparente.png}\hspace{.5ex} }}

%\def\sectionintoc{}
%\def\beamer@sectionintoc#1#2#3#4#5{%
%  \ifnum\c@tocdepth>0%
%  \ifnum#4=\beamer@showpartnumber%
%  {
%  \beamer@saveanother%
%  \gdef\beamer@todo{}%
%  \beamer@slideinframe=#1\relax%
%  \expandafter\only\beamer@tocsections{\gdef\beamer@todo{%
%      \beamer@tempcount=#5\relax%
%      \advance\beamer@tempcount by\beamer@sectionadjust%
%      \edef\inserttocsectionnumber{\the\beamer@tempcount}%
%      \def\inserttocsection{\hyperlink{Navigation#3}{\includegraphics[width=2ex]{freccia_trasparente.png}\hspace{.5ex} #2}}%
%      \beamer@tocifnothide{\ifnum\c@section=#1\beamer@toc@cs\else\beamer@toc@os\fi}%
%      {
%        \ifbeamer@pausesections\pause\fi%
%        \ifx\beamer@toc@ooss\beamer@hidetext
%          \vskip1.5em
%        \else
%          \vfill
%        \fi
%        {%
%          \hbox{\vbox{%
%              \def\beamer@breakhere{\\}%
%              \beamer@tocact{\ifnum\c@section=#1\beamer@toc@cs\else\beamer@toc@os\fi}{section in toc}}}%
%         \par%
%        }%
%      }%
%    }
%  }%

%% Handout option
\DeclareOption{handout}{\gdef\beamer@currentmode{handout}}

%% Information floor
\DeclareOption{totalframes}{\renewcommand{\totalframes}{/\inserttotalframenumber}}
\DeclareOption{last}{\renewcommand{\lastbg}{\includegraphics[width=\paperwidth,page=4]{DocMASE_template}}}
\DeclareOption{first}{
  \renewcommand{\firstbg}{\includegraphics[width=\paperwidth,page=1]{DocMASE_template}}
  \usespecialtitlepagetemplate
}
\DeclareOption{firstalt}{
  \renewcommand{\firstbg}{\includegraphics[width=\paperwidth,page=2]{DocMASE_template}}
  \usespecialtitlepagetemplate
}

\DeclareOption{firstsupp}{\renewcommand{\firstfooter}{}}
\DeclareOption{lastsupp}{\renewcommand{\lastfooter}{}}

% execute options
\ProcessOptions

\definecolor{ETHZbluehead}{RGB}{3,67,149}
\definecolor{white}{RGB}{255,255,255}

\setbeamercolor{section in head/foot}{fg=white,bg=ETHZblue}
\setbeamercolor{subsection in head/foot}{fg=white,bg=ETHZblue}

\setbeamertemplate{section in head/foot shaded}[default][60]
\setbeamertemplate{subsection in head/foot shaded}[default][60]

\setbeamertemplate{headline}{%
\vspace{27pt}
\begin{beamercolorbox}[wd=\paperwidth]{section in head/foot}
   \insertsectionnavigationhorizontal{\paperwidth}{}{\hskip10pt plus1filll}
   \insertsubsectionnavigationhorizontal{\paperwidth}{}{\hskip10pt plus1filll}
\end{beamercolorbox}%
}

%[ht=10pt] wd=\paperwidth,ht=2.65ex,dp=1.5ex,center  \vskip2pt

\setbeamertemplate{footline}
{%
\ifthenelse{\equal{\insertframenumber}{1}}{%
    \firstfooter%
  }{%
    \ifthenelse{\equal{\insertframenumber}{\inserttotalframenumber}}{%
      \lastfooter%
    }{%
      \normalfooter%
    }
  }
}

%%% Frametitle position each slide
\setbeamertemplate{frametitle}
{
\vspace{15pt}
    \begin{beamercolorbox}[wd=.99\paperwidth,ht=3.8ex,dp=1ex,sep=1.8ex,left,shadow=true]{frametitle}%
    {\fontsize{13.9pt}{8pt}\textbf{\insertframetitle}\par}
    \end{beamercolorbox}%
\vspace{-14pt}
}

\usebackgroundtemplate{
  \ifthenelse{\equal{\insertframenumber}{1}}{%
    \firstbg%
  }{%
    \ifthenelse{\equal{\insertframenumber}{\inserttotalframenumber}}{%
      \lastbg%
    }{%
      \normalbg%
    }
  }
}

%%% Notes
%\mode<notes>

\mode<presentation>
{
  \useoutertheme{default}    % empty
%  \useoutertheme{infolines} % simple but bland
%  \useoutertheme{split}     % ok if compress option used
%  \useoutertheme{shadow}    % way too much space used -- ok with option 'compress'
  %\useoutertheme{shadow}   
  %\setbeamercovered{transparent} % or whatever (possibly just delete it)
  %\useoutertheme[subsection=false]{miniframes}
}

%%%%%%%%%%%%%%%%
% With ETH fonts
%%%%%%%%%%%%%%%%


% Use the following lines if the fonts ETH-Light are installed
% for LaTeX (Frank Schweitzer, Robert mach 2004-12-13)
% \renewcommand{\familydefault}{let}
% \renewcommand{\sfdefault}{let}
% 
% \DeclareFixedFont{\x}{T1}{let}{m}{n}{10}
% \DeclareFixedFont{\xb}{T1}{let}{b}{n}{10}
% \newfont{\xiiiv}{letr8t at 8.5pt}
% \newfont{\xiiivb}{letb8t at 8.5pt}


%%%%%%%%%%%%%%%%%
% With Helvetica fonts
%%%%%%%%%%%%%%%%

% Use the following lines if helvetica fonts should be used
% Frank Schweitzer, Robert Mach 2004-12-13
\renewcommand{\familydefault}{phv}
\renewcommand{\sfdefault}{phv}
%\renewcommand{\normalsize}{\fontsize{10.5pt}{12.5pt}\xiiiv}

\DeclareFixedFont{\x}{T1}{phv}{m}{n}{10}
\DeclareFixedFont{\xb}{T1}{phv}{b}{n}{10}
\newfont{\xiiiv}{phvr8t at 30pt}
\newfont{\xiiivb}{phvb8t at 8.5pt}

% Color definitions
\usecolortheme[RGB={0,43,94}]{structure}
\definecolor{blue}{RGB}{0,43,94}
\definecolor{black}{RGB}{0,0,0}
\definecolor{white}{RGB}{255,255,255}
\definecolor{red}{RGB}{161,80,0}
\definecolor{itemblue}{RGB}{0,80,145} %% Color of item squares (different
                                %% blue)

\setbeamercolor{block title}{use=blue,fg=blue.fg,bg=blue.fg!20!bg}
\setbeamercolor{block title alerted}{use=alerted text,fg=alerted text.fg,bg=alerted text.fg!20!bg}
\setbeamercolor{block title example}{use=example text,fg=example text.fg,bg=example text.fg!20!bg}

\setbeamercolor{block body}{parent=normal text,use=block title,bg=block title.bg!50!bg}
\setbeamercolor{block body alerted}{parent=normal text,use=block title alerted}
\setbeamercolor{block body example}{parent=normal text,use=block title example}

\setbeamercolor{normal text}{fg=black,bg=white}
\setbeamercolor{alerted text}{fg=red}

%%
%% End of file