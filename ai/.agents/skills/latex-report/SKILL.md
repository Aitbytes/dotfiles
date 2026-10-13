---
name: latex-report
description: Produce a professional LaTeX research report from findings. Includes a document class preamble, section templates, and a ready-to-run nix-shell pdflatex pipeline.
---

## What I do

Convert structured research into a publication-quality PDF LaTeX document. The output is a well-structured `.tex` file and compiled `.pdf` using a standard article class with professional formatting.

## When to use me

When the user needs a formal, citable research report with precise structure, floating figures, proper citations, and a polished layout. Ideal for academic submissions, formal deliverables, or archival-quality documentation.

## Requirements

- `nix-shell -p texlive.combined.scheme-medium` for the full LaTeX toolchain
- Note: texlive derivation builds on first run (~5-10 min cached thereafter)

## Document Structure

Use this skeleton:

```latex
\documentclass[12pt,a4paper]{article}

% Layout
\usepackage[margin=1in,headheight=13.6pt]{geometry}
\usepackage{parskip}
\usepackage{fancyhdr}
\fancyhf{}
\rhead{\thepage}
\pagestyle{fancy}

% Fonts
\usepackage[T1]{fontenc}
\usepackage{lmodern}

% Graphics & Colors
\usepackage{graphicx}
\usepackage{xcolor}
\usepackage{booktabs}      % tables
\usepackage{hyperref}      % clickable links

% Citations
\usepackage{cite}
\bibliographystyle{plain}

\title{Research Title}
\author{Research Team}
\date{\today}

\begin{document}

\maketitle
\thispagestyle{empty}

\begin{abstract}
% 2-3 sentence summary of the objective and key findings
\end{abstract}

\section{Introduction}
% Context: why this research matters and what the objective was

\section{Key Findings}
% Main discoveries with source attributions and confidence levels

\section{Analysis}
% Deeper exploration of findings, implications, cross-referencing

\section{Methodology}
% Brief description of research approach and sources consulted

\section{Conclusions}
% Synthesis, actionable takeaways, open questions

\bibliography{references}

\end{document}
```

\section{Tables}

Use `booktabs` for publication-quality tables:

```latex
\begin{table}[htbp]
  \centering
  \begin{tabular}{llr}
    \toprule
    \textbf{Claim} & \textbf{Source} & \textbf{Confidence} \\
    \midrule
    Finding 1 & Source A & High \\
    Finding 2 & Source B & Medium \\
    \bottomrule
  \end{tabular}
  \caption{Key findings summary}
  \label{tab:findings}
\end{table}
```

\section{Figures}

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.8\textwidth]{figure.png}
  \caption{Description of the figure}
  \label{fig:example}
\end{figure}
```

\section{Citations}

For inline citations:

```latex
According to prior research~\cite{smith2024}.
Multiple findings support this~\cite{smith2024,jones2023}.
```

Create a `references.bib` file:

```bibtex
@article{smith2024,
  author    = {Smith, J. and Doe, A.},
  title     = {Title of the Paper},
  journal   = {Journal Name},
  year      = {2024},
  volume    = {10},
  pages     = {1--15}
}
```

## How to compile

```bash
# Step 1: write the .tex and .bib files to output/
# Step 2: compile twice (for cross-references)
nix-shell -p texlive.combined.scheme-medium --run "pdflatex -interaction=nonstopmode output/report.tex && bibtex output/report && pdflatex -interaction=nonstopmode output/report.tex && pdflatex -interaction=nonstopmode output/report.tex"
```

Or for faster iteration with scheme-basic:

```bash
nix-shell -p texlive.combined.scheme-basic --run "pdflatex -interaction=nonstopmode output/report.tex && pdflatex -interaction=nonstopmode output/report.tex"
```

## Output envelope

The skill produces `output/report.tex` and `output/report.pdf`. The agent should write both paths as tool results. The `.tex` is useful for the user to edit further; the `.pdf` is the final deliverable.

## Limitations

- texlive first-run build is slow (5-10 min); cached thereafter
- Avoid extremely complex custom macros — keep it to standard package commands
- For very long documents, consider splitting into multiple `\input{}` files
