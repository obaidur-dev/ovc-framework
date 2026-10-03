# OVC Framework v2.1.1 (Obaidur's Verified Coding Framework)

Three [Agent Skills](https://agentskills.io) that take you from "I have a rough
idea" to a built project **you actually understand**, with checks that the plan
was verified and not just written. They work for a first-year student and for a
senior engineer, because you choose how much help you want.

| Step | Skill | You give it | You get |
|---|---|---|---|
| 1 | `ovc-discover` | A rough idea | `project-brief.md`, including a reasoned tech-stack choice and performance goals |
| 2 | `ovc-specify` | That brief (or an existing repo) | Spec set, `AGENTS.md`, decision log, measurable targets |
| 3 | `ovc-explain` | The finished project | `docs/GUIDE.md`, a Builder's Guide to what was really built |

They work in any AI coding tool that supports the Agent Skills format. The
files they produce (`AGENTS.md` and Markdown docs) work with tools that do not.

```
idea -> [discover] -> project-brief.md -> (fresh session) -> [specify] -> docs/ + AGENTS.md
                                                                  |
                                                      check_specs.py (must pass)
                                                                  |
                                    ... AI coding agent builds it, phase by phase ...
                                                                  |
                          [explain] -> docs/GUIDE.md  <- check_guide.py (must pass)
```

## Two independent dials

Both are chosen in the first question of `ovc-discover` and saved in the brief.

**Level: how much help do you want?**

| Level | For | What changes |
|---|---|---|
| **Beginner** | New to building software | Plain words, a "why this step" note each time, jargon explained, the agent *recommends* (one pick plus one alternative), the AI is told to explain as it builds, the final guide is a full tour with a quiz |
| **Intermediate** | Built a few things | Options with trade-offs and a recommendation, brief rationale, a guide focused on architecture and decisions |
| **Expert** | You know what you want | Terse; follows your decisions; flags only real gaps (once, with evidence); the guide is a compact map, invariants, and runbook |

**Track: how big is the project?**

| Track | For | You get |
|---|---|---|
| **Lite** | Small or learning project | Brief, one-page `SPEC.md`, 10-line security checklist, `AGENTS.md` |
| **Standard** | A real app: logins, data, a team | Brief, PRD, architecture, data model / API spec if relevant, STRIDE security doc, build plan, `AGENTS.md`, decision log |
| **Full** | Capstone or high rigor | Standard plus EARS requirements, ADRs, data-flow diagram, full STRIDE with evidence, traceability |

An expert can run a Lite project. A beginner can be doing a Full capstone.

## What it fills in for people who do not know what they do not know

- **"Which language?"** `ovc-discover` explains that *fast on the CPU*, *fewest
  AI mistakes*, and *something I can read and debug* are three different
  questions, then recommends a mainstream, type-checked stack for the project
  type, with the evidence and its limits.
- **"Make it fast without breaking it."** Goals become numbers (for websites:
  LCP 2.5 s or less, INP 200 ms or less, CLS 0.1 or less). The plan measures
  first, fixes the biggest cost, and measures again. A checklist covers what
  AI-written code tends to get wrong (per-item database queries, missing
  indexes, loading everything into memory, polling loops).
- **"Fewer AI mistakes."** Every plan has a feedback loop (type check, lint,
  tests after each change), small phases, version pinning, a three-strikes
  rule, and a dependency check.
- **"I do not understand what was built."** `ovc-explain` writes a guide from
  the real code, ties every claim to a file and line, marks what is only
  `Partial`, lists what could not be verified, and ends with questions about
  *your* project.

## What "Verified" means here

- Every requirement has an ID (`FR-001`, `NFR-001`), and non-functional ones
  have numbers.
- The build plan traces **every ID -> phase -> test**.
- Every threat has one of four statuses (`Planned`, `Mitigated`,
  `Accepted risk`, `Open`); `Mitigated` needs typed evidence (`test:`, `scan:`,
  or `manual:`).
- The plan ends with a handover step, and the guide is checked against the real
  project: paths and `file:line` references exist, cited tests exist, every
  requirement is covered, measured numbers have evidence or say `Not measured`,
  and the security section cannot hide open items.
- `check_specs.py` and `check_guide.py` (plain Python 3, no dependencies)
  enforce this and exit non-zero on failure.

## The research behind the design

Every figure below was read in its primary source on 2026-10-02. **Always quote
the scope with the number.** The full register (exact wording, location in the
source, what was and was not verified) is in [`EVIDENCE.md`](EVIDENCE.md).

| Finding (with scope) | Source | Caveat |
|---|---|---|
| On average 94% of compilation errors made by **six open-weight models (2B to 34B)** writing small **TypeScript** functions were type-check failures | Mündler et al., PLDI 2025, Section 1 (not in the abstract) | Compile errors only; small tasks; no commercial models tested. It does not show typed languages have fewer bugs overall |
| Less common languages do worse: a third-party benchmark cited in that paper reports compile-error rates of 18-39% on hard Rust tasks and 40-60% for OCaml and Haskell | Same paper, Section 6 (secondhand) | A GitHub benchmark, not peer reviewed; direction only |
| On 10 hand-optimised benchmark programs, execution time relative to C: Rust 1.04, C++ 1.56, Java 1.89, Go 2.83, Python 71.90 | Pereira et al., Science of Computer Programming 2021, Table 4 | A re-measurement (van Kempen et al., arXiv 2410.05460, revised Oct 2025) found language has no significant effect on energy beyond execution time, so trust the *time* ratios, as an order of magnitude, for CPU-bound code only |
| **GPT-4** code averaged 3.12x the execution time of the best human solutions on 1,000 LeetCode problems (worst case 13.89x) | EffiBench, NeurIPS 2024 | 2024-era models, small puzzles. Newer models not re-measured here: measure your own app |
| 52 mostly junior developers using AI averaged **50% vs 67%** on a comprehension quiz (**17 percentage points lower**); best results came from asking for explanations | Shen and Tamkin, arXiv 2601.20245 (2026) | One Python library, quiz minutes later, small subgroups, not causal. Authors work at an AI developer |
| In 45% of cases across 80 tasks and 100+ models, the model chose the insecure way to complete code (2025). Average security pass rate 56% over four years (2026) | Veracode GenAI Code Security reports | Benchmark tasks, not a prediction for your project. "About 44% failing" is arithmetic, not Veracode's figure |
| Average hallucinated-package share **at least** 5.2% (commercial) and 21.7% (open-source) across 16 models and 576,000 Python and JavaScript samples | Spracklen et al., USENIX Security 2025 | Existence is not safety: attackers register those names |
| TypeScript became GitHub's most used language by monthly contributors in Aug 2025 (2.64 million, +66.6%) | GitHub Octoverse 2025 | Other indices differ; popularity is not quality |
| Website "good" thresholds: LCP 2.5 s, INP 200 ms, CLS 0.1 at the 75th percentile | web.dev (via many 2026 sources) | web.dev page not fetched directly in this check |

## Install

Copy (or symlink) the **folders** `ovc-discover/`, `ovc-specify/`, and
`ovc-explain/` into your tool's skills directory, then restart the tool if they
do not appear. Paths below were checked against each tool's documentation; the
date and sources are in
[`ovc-specify/references/tool-compat.md`](ovc-specify/references/tool-compat.md),
which is the single place tool facts are kept.

| Tool | Project-level | Personal (all repos) |
|---|---|---|
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| OpenAI Codex | `.agents/skills/` | `$HOME/.agents/skills/` |
| Cursor | `.agents/skills/` | `~/.agents/skills/` |
| GitHub Copilot | `.github/skills/`, `.claude/skills/`, or `.agents/skills/` | `~/.copilot/skills/` or `~/.agents/skills/` |
| Gemini CLI | `.gemini/skills/` or `.agents/skills/` | `~/.gemini/skills/` or `~/.agents/skills/` |
| OpenCode | `.opencode/skills/`, `.claude/skills/`, or `.agents/skills/` | `~/.config/opencode/skills/` |
| Claude.ai web/desktop upload | **UNVERIFIED** (see Anthropic's Help Center) | |
| Other tools | **UNVERIFIED** (if it supports Agent Skills, try `.agents/skills/`; otherwise paste `SKILL.md` into the session) | |

Example (Codex, project-level):
```
mkdir -p .agents/skills
cp -r ovc-discover ovc-specify ovc-explain .agents/skills/
```

`.skill` files are ordinary zip archives of one skill folder.

## Use

1. Start a session in your project folder: *"I have an idea for an app. Help me
   plan it."* -> `ovc-discover` asks level and size, interviews you, helps pick a
   stack, shows the brief, saves `project-brief.md`.
2. Fresh session (or cleared context): *"Here is project-brief.md. Make the spec
   set."* -> `ovc-specify` creates the docs and runs the checker.
3. *"Read AGENTS.md, then start Phase 1."* The AI builds phase by phase.
4. When it is built: *"Explain what we built."* -> `ovc-explain` writes
   `docs/GUIDE.md`, offers an interactive tour, and runs its checker.

For an existing repo: *"Document this repo for an AI agent and check its
security."* -> `ovc-specify` brownfield mode (no brief needed). To understand
an existing project: `ovc-explain`.

## Running the checkers yourself

```
python3 ovc-specify/scripts/check_specs.py --brief project-brief.md
python3 ovc-specify/scripts/check_specs.py --root . --brief docs/project-brief.md
python3 ovc-specify/scripts/check_specs.py --root . --mode brownfield
python3 ovc-explain/scripts/check_guide.py --root .
```
Exit codes: 0 pass, 1 checks failed, 2 rejected (unknown brief version, missing
guide). Add `--allow-open-questions` to the spec checker only for questions you
deliberately left open.

## Repository contents

```
ovc-discover/   skill 1 (brief template, stack guide, concept cards)
ovc-specify/    skill 2 (one reference per document, performance, AI-reliability, check_specs.py)
ovc-explain/    skill 3 (guide template, teaching levels, check_guide.py)
examples/       Lite example with real code and a checked guide; abbreviated Full example
evals/          5 behaviour evals + automated tests (python3 -m unittest discover -s evals)
```

## Honest limits

- The checkers verify **structure, consistency, and evidence format**. They
  cannot tell a true `manual:` claim from a false one, and they cannot tell
  whether an explanation in the guide is *correct*. A person still has to read it.
- Stack and performance guidance is judgment informed by studies with real
  limits (see the table and `EVIDENCE.md`). It is not a benchmark ranking, and models change.
- The behaviour evals have not been run against a live coding agent; the
  scripts, examples, and structure are tested automatically.
- Security statistics and tool behaviour are dated and sourced in the reference
  files; re-check them before citing.
- Nothing here is legal advice. Compliance questions are asked, never answered.

## Licence and version

MIT, see [`LICENSE`](LICENSE). Version 2.1.1, see [`CHANGELOG.md`](CHANGELOG.md).
