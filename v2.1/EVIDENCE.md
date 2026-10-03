# Evidence register

Every number that appears in the skills, with its exact scope and how it was
checked. If a number in any file disagrees with this register, the register
wins and the file is wrong; please open an issue.

Verified on: **2026-10-02**. "Primary" means the paper or publisher page was read
directly in this check. "Derived" means arithmetic on a primary figure.

| # | Figure as used | Exact source wording / location | Scope you must keep | Status |
|---|---|---|---|---|
| E1 | 94% of compilation errors were type-check failures | Mündler et al., *Type-Constrained Code Generation with Language Models*, PLDI 2025, arXiv 2504.09246, Section 1 ("on average 94% of compilation errors result from failing type checks"). The abstract says only that type constraints cut compile errors "by more than half" | Six open-weight models (Gemma 2 at 2B, 9B, 27B; DeepSeek Coder 33B; CodeLlama 34B; Qwen2.5 32B); TypeScript versions of HumanEval and MBPP; no commercial models | Primary |
| E2 | About 6% of compile errors were syntax errors | Same paper, Sections 1 and 2.2 | Same as E1 | Primary |
| E3 | Rust 18-39%, OCaml/Haskell 40-60% compile-error rates | Same paper, Section 6, citing a GitHub "compilation benchmark" by a third party, and other work | Secondhand; not peer reviewed; hard tasks | Primary for what the paper says; the underlying benchmark was not read |
| E4 | Execution time vs C: Rust 1.04, C++ 1.56, Java 1.89, Go 2.83, Python 71.90. Energy: 1.03, 1.34, 1.98, 3.23, 75.88 | Pereira et al., *Ranking programming languages by energy efficiency*, Science of Computer Programming 205 (2021) 102609, Table 4 (C = 57.86 J and 2,019.26 ms) | 10 hand-optimised Computer Language Benchmarks Game programs, 27 languages, one Intel desktop (Ubuntu 16.10) | Primary |
| E5 | Language has no significant impact on energy beyond execution time | van Kempen, Kwon, Nguyen, Berger, *It's Not Easy Being Green*, arXiv 2410.05460 (revised Oct 2025), abstract | Critique and re-measurement of E4's methodology | Primary (abstract) |
| E6 | GPT-4: 3.12x average execution time, 13.89x worst case, 43.92x worst-case memory, 6.36x average memory | Huang et al., *EffiBench*, NeurIPS 2024, arXiv 2402.02037 | 1,000 LeetCode-style problems; the earlier version reported GPT-4-turbo at 1.69x average and 45.49x worst case; 2024-era models | Primary (abstract and tables via publisher pages) |
| E7 | AI group 50% vs 67% on the quiz; 17 percentage points; n = 52; Cohen's d = 0.738, p = 0.01 | Shen and Tamkin, arXiv 2601.20245; summary at anthropic.com/research/AI-assistance-coding-skills (29 Jan 2026) | Mostly junior developers; Python library Trio; chat sidebar assistant; quiz minutes after the task. The post's "17% lower" refers to this 17-point gap; relative to 67% it is about 25% | Primary |
| E8 | High-scoring patterns averaged 65% or higher (n = 2, 3, 7); low-scoring under 40% (n = 4, 4, 4) | Same post | Qualitative, not causal | Primary |
| E9 | 45% of cases chose the insecure option; 80 tasks; 100+ LLMs; Java over 70% failure; XSS failed 86% | Veracode press release, 30 July 2025 | Tasks designed with a secure and an insecure completion; static analysis scoring | Primary |
| E10 | Average security pass rate 56% across 100+ models over four years; 11 new models tested across 80 tasks; best 68%; Java mean 30% | Veracode 2026 GenAI Code Security Report landing page | "About 44% failing" is derived (100 - 56) and is not stated by Veracode | Primary; E10b "44%" is Derived |
| E11 | At least 5.2% (commercial) and 21.7% (open-source) hallucinated packages; 16 models; 576,000 samples; 205,474 unique names | Spracklen et al., arXiv 2406.10279 v3, abstract (USENIX Security 2025) | Python and JavaScript samples; "average percentage ... is at least" | Primary |
| E12 | TypeScript 2,636,006 monthly contributors, +66.6%, #1 in August 2025 | GitHub Blog, *Octoverse 2025* | Distinct monthly contributors; GitHub notes other indices rank JavaScript/Python higher | Primary |
| E13 | LCP 2.5 s, INP 200 ms, CLS 0.1 at the 75th percentile; INP replaced FID March 2024 | Consistent across more than ten 2026 pages that cite web.dev | Field data | Verified via secondary sources; the web.dev page was not fetched |
| E14 | OWASP LLM Top 10 2026 edition renamed and renumbered categories | Search results (August 2026) | Only part of the 2026 list was confirmed, which is why risks are cited by name | Partly verified |
| E15 | India DPDP Rules 2025 notified Nov 2025, phased; core obligations roughly May 2027 | Secondary legal sources; some conflicted | Not legal advice; confirm with MeitY / the Gazette | Secondary, conflicting |

## What was *not* verified

- That newer models have closed the efficiency gap in E6 (a 2026 follow-up was
  seen in search results but not read in this check, so no claim relies on it).
- Any language-specific accuracy ranking (Python best, and so on). No such
  ranking is asserted; E3 is the only language-gap evidence used.
- The web.dev pages themselves (E13).

## Changes in 2.1.1

The 2.1.0 files overstated or blurred four things; all are corrected here:
the 94% figure lacked its scope (E1); the quiz gap was written "17% lower"
instead of 17 percentage points (E7); the efficiency figure was attributed to
"AI code" instead of GPT-4 (E6); and energy ratios were presented as a language
property despite the critique (E5). A claim about newer models closing the gap
and a language ranking citing three benchmarks were removed because they could
not be re-verified.
