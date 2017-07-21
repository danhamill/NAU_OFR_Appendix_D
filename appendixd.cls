


% Specify which version of latex to use
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{appendixd}[7/20/2017]

\DeclareOption{12pt}{
	\PassOptionsToClass{\CurrentOption}{book}
}

%% Fallback
\DeclareOption*{
	\ClassWarning{myclass}{Unknown option '\CurrentOption'}
}

%{{{ Font size control
\newcommand{\@@fontsize}{11pt}
\newcommand{\set@@fontsize}[1]{\renewcommand{\@@fontsize}{#1}}
\DeclareOption{10pt}{\set@@fontsize{10pt}}
\DeclareOption{11pt}{\set@@fontsize{11pt}}
\DeclareOption{12pt}{\set@@fontsize{12pt}}
%}}}


% Catch any undeclared options and pass them to book class
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{book}%
	\typeout{Passing '\CurrentOption' on to LaTex2e book.cls}}


%% Process given options
\ProcessOptions\relax


%% Load base class
\LoadClass[letterpaper]{book}

%{{{ Line-spacing control
\RequirePackage{setspace}
\newcommand{\singlespaced}{\singlespacing}
\newcommand{\doublespaced}{\doublespacing}
\newcommand{\triplespaced}{\setstretch {2.6}}
%}}}

%{{{ Set up margins, and other page parameters.
% Use the geometry package for margins to make our life easier
\RequirePackage{geometry}
\geometry{%
	paper=letterpaper,
	includeheadfoot,
	truedimen,
	left=1in,
	top=1in,
	right=1in,
	bottom=1in,
	headheight=\@@fontsize,
	headsep=\baselineskip,
	footskip=0pt}


\endinput