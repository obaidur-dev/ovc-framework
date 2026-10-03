# Stack guide: choosing a language and framework

Load this when the brief's technology is not already fixed (by a course, an
employer, or an existing codebase) and the person is a beginner or
intermediate, or an expert who asks for advice. Experts who name their own
stack: skip this file, and flag a concern only once, with evidence, if their
choice clashes with a stated goal.

Sources last verified: 2026-10-02 (primary sources read directly, except where noted).
If you can search the web, re-check the figures before quoting them; otherwise
quote them exactly as written here, with their scope. A full claim register is in
`EVIDENCE.md` at the repository root.

## The honest answer first (say this in plain words)

There is no single "best language". Three different questions get mixed up:

1. **Which language runs fastest on the CPU?** On benchmark programs that are
   mostly computing, compiled languages (C, Rust, C++, then Go and Java) ran
   far faster than scripting languages such as Python (see the evidence table
   for the figures and their limits). Most apps spend their time waiting for a
   database, the network, or the user, so design (queries, caching, how much
   data you send) usually matters more than language.
2. **Which language makes AI write fewer mistakes?** Mainstream languages with
   a compiler or type checker that complains immediately. The AI's mistakes
   get caught in seconds instead of in front of your users.
3. **Which can *you* read, debug, and change?** The one you can follow. Code
   you cannot read is code you cannot fix when the AI gets stuck.

A good stack is the best compromise across all three for *this* project.

## Evidence (what is actually known, with its limits)

Every figure below was read in its primary source. Quote the scope along with the
number; a figure without its scope is how a true statistic becomes a false one.

| Claim | Evidence (exact scope) | Limits to state honestly |
|---|---|---|
| Most compile errors in AI code are type errors | Mündler et al., *Type-Constrained Code Generation with Language Models*, PLDI 2025 (arXiv 2504.09246), Section 1: in their evaluation, on average 94% of compilation errors came from failing type checks. The evaluation used **six open-weight models (2B to 34B parameters)** on **TypeScript** versions of HumanEval and MBPP (small function-level tasks). Only about 6% of compile errors were syntax errors | It counts compile errors on small tasks and tested no commercial models. It does not say typed languages have fewer bugs overall. It says a type checker flags most compile mistakes of that kind immediately. The paper itself notes stronger models make fewer typing errors on these datasets |
| TypeScript grew fastest as AI tools spread | GitHub Octoverse 2025: by distinct monthly contributors, TypeScript became the most used language on GitHub in August 2025 (2,636,006 contributors, up 66.6% year on year) | GitHub notes other indices may still rank JavaScript or Python higher. Popularity is not quality. GitHub's link to AI tools and typed languages is its own interpretation |
| AI does worse on less common languages | Mündler et al. state that models derive incomplete rules for less common languages, and cite a third-party compilation benchmark (a GitHub project, not peer reviewed) reporting compile-error rates of 18% to 39% on difficult Rust tasks across three models, and 40% to 60% for OCaml and Haskell | Secondhand and task-dependent. Read it as a direction, not a measurement of your project. It will shift with each model release |
| Compiled languages run CPU-bound code much faster | Pereira et al., *Ranking programming languages by energy efficiency*, Science of Computer Programming 205 (2021), Table 4: on 10 hand-optimised benchmark programs (Computer Language Benchmarks Game) in 27 languages on one Intel desktop, **execution time** relative to C = 1.00 was Rust 1.04, C++ 1.56, Java 1.89, Go 2.83, Python 71.90. Energy ratios in that paper were similar (1.03, 1.34, 1.98, 3.23, 75.88) | A follow-up (van Kempen et al., arXiv 2410.05460, revised October 2025) re-measured with corrected methodology, found that earlier discrepancies disappear when factors are controlled, and concluded language implementation has **no significant impact on energy beyond execution time**. So rely on the *time* ratios, as an order of magnitude, for CPU-bound code only. Most apps are I/O-bound |
| AI-written code can be slower than expert code | EffiBench (NeurIPS 2024, arXiv 2402.02037): on 1,000 LeetCode-style problems, **GPT-4** code averaged 3.12 times the execution time of the best human solutions (worst case 13.89 times; 6.36 times the memory on average). An earlier version of the paper reported GPT-4-turbo at 1.69 times on average | Small puzzles and 2024-era models. Newer models were not re-measured here. The safe conclusion is **measure, do not assume** |
| What "fast" means for a website | Core Web Vitals "good" thresholds at the 75th percentile of real visits: LCP 2.5 s or less, INP 200 ms or less, CLS 0.1 or less (INP replaced FID in March 2024) | Consistent across many 2026 sources that cite web.dev; the web.dev page itself was not fetched in this check. Field data, not lab runs, decides |

## How to choose (the decision procedure)

Ask only what you cannot infer, one short batch:

1. **What are you building?** (use the table below)
2. **What do you already know, or what must you use?** A course or employer
   requirement beats everything here. If they know nothing yet, choose for them.
3. **Is it heavy computation** (video, simulation, big data crunching,
   games), or mostly forms, lists, and database reads and writes? Almost every
   beginner project is the second kind.
4. **Where must it run?** Browser, phone, server, command line, embedded device.

Then recommend **one** default and **one** alternative with reasons, in the
style of the person's level (see below).

## Default stacks by project type

These are judgment calls informed by the evidence above, not benchmark
rankings. Say so. Framework names and versions change; tell the person to
check the current stable version and give the AI coding agent a link to that
version's documentation.

| Project | Default | Why | Watch out | Choose differently when |
|---|---|---|---|---|
| Static page, landing page, small browser tool | HTML, CSS, plain JavaScript (add TypeScript if it grows) | No build step, nothing to install, smallest download = fastest load | JavaScript has no type checker unless you add one | Many screens and shared state: use a typed framework |
| Web app with accounts and a database | TypeScript (strict mode) with one mainstream full-stack framework, plus PostgreSQL (SQLite for a single-user tool) | One language everywhere, type checker catches AI slips, huge amount of public examples | Frameworks change fast: pin versions | The person already knows Python well: Python with type hints and a mainstream framework is fine |
| Backend or API needing high throughput or low CPU use | Go (small language, compiles fast, simple concurrency) | Fast, easy for AI and humans to read, strong standard library | Fewer batteries than Python or TypeScript ecosystems | Maximum performance and memory safety, and willing to learn a steep language: Rust. Company already uses Java or C#: stay there |
| Data, automation, AI/ML scripts | Python | Biggest ecosystem; AI writes it best | Pure Python loops over big data are slow: use vectorized libraries (NumPy, pandas, Polars) so the heavy work runs in compiled code | A hot path stays slow after profiling: move only that part to a compiled language |
| Command-line tool | Go or Rust for a fast single binary; Python or Node for personal quick tools | Go/Rust start instantly and need no runtime | Rust has a learning curve | One-off for yourself: use what you know |
| Mobile app | Kotlin (Android), Swift (iOS); React Native (TypeScript) or Flutter (Dart) for both | Platform-native is most reliable; cross-platform saves time | AI error rates for these were **not verified** in this research | Choose by what the team already knows |
| Game | The engine decides (Unity uses C#, Godot uses GDScript or C#) | Engines handle the hard performance parts | Engine APIs change between versions | n/a |
| Embedded, drivers, performance-critical systems | C, C++, or Rust | Direct hardware control, no runtime | Easy to write unsafe code; AI mistakes are costlier | Strongly recommend experienced review |

Database default: SQLite for one user or small tools (a single file, nothing
to run); PostgreSQL when several people write at the same time.

## "Boring technology" rules (apply to every level)

- Prefer mainstream and well-documented over new and exciting. The AI has seen
  far more examples of it, so it errs less.
- Fewer languages, fewer frameworks, fewer dependencies. Each extra piece is
  something the AI can get wrong and you must understand.
- Turn on the strictest checking the language offers (TypeScript strict mode,
  Python type hints with a checker, a linter), so mistakes surface in seconds.
- The AI may know an older version of a framework. State the version you use
  and point it to that version's docs.
- Do not pick a language only because a benchmark says it is fast. Pick the
  simplest stack that meets the performance goal, then measure.
- A first project in Rust or C++ "for speed" usually costs more in debugging
  time than the CPU time it saves. Choose it when profiling shows you need it.

## How to talk to each level

- **Beginner.** Explain the three questions in two or three sentences, using
  `concept-cards.md` for any term they do not know. Give **one**
  recommendation and **one** alternative, in plain words: "I recommend X
  because ... Say 'ok' to accept, or tell me what you already know and I'll
  adjust." Never present more than three options.
- **Intermediate.** Two or three options in a short trade-off list (speed,
  AI-reliability, learning curve), your pick marked, and one line on what would
  change your mind.
- **Expert.** Ask for their stack. Offer advice only on request. If their
  choice conflicts with a stated goal, say so **once** with the specific
  concern, then follow their decision.

## Recording the decision in the brief

Put this under "Key decisions (with reasoning)":

```
- Technology: <language + framework + database>.
  Why: <one or two reasons, from the three questions>.
  Main alternative: <what was considered and why it lost>.
  Revisit if: <condition, for example "profiling shows the report job exceeds
  its time budget">.
```

If the person accepted defaults without a view, say "chosen as the default on
the person's behalf" so the next reader knows it was never a strong preference.
