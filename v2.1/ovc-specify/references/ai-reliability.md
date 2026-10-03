# Making AI mistakes less likely (guardrails for the build)

Load this when writing `AGENTS.md` and `BUILD_PLAN.md` (or SPEC build steps).
It turns research into rules the AI coding agent follows and that the builder
can check.

## Why these rules

Each claim is stated with its scope; see `EVIDENCE.md` at the repository root.

- In one study, on average 94% of the compilation errors made by six open-weight
  models (2B to 34B parameters) writing small TypeScript functions were type
  errors (Mündler et al., PLDI 2025). A type checker or compiler run after every
  change catches errors of that kind in seconds. It does not show that typed
  languages have fewer bugs overall.
- AI tools suggest packages that do not exist. Across 16 models and 576,000
  generated Python and JavaScript samples, the average share of hallucinated
  packages was at least 5.2% for commercial models and 21.7% for open-source
  models (Spracklen et al., USENIX Security 2025). Attackers can register those
  names.
- Veracode's benchmark of 80 coding tasks across 100+ models found the model
  chose the insecure way to complete the code in 45% of cases (2025 report).
  The 2026 report puts the average security pass rate at 56% across 100+ models
  over four years (see `security.md`).
- AI models reflect a past snapshot of libraries and can use an older API.
- Models do worse on less common languages than on mainstream ones.

## The feedback loop (put the real commands in AGENTS.md)

After **every** change the agent runs, in this order, and fixes failures before
moving on:
1. Type check or compile (strict mode on).
2. Linter / formatter.
3. The tests for what it just changed.

If the stack has no type checker, add one (TypeScript strict mode, Python type
hints with a checker). Put the exact commands in `AGENTS.md` under "Commands"
and "Feedback loop". If the commands are not known yet, write
`TBD - fill in once the project is scaffolded` and make fixing that the first
build task.

## Build rules for the plan

1. **Small phases and small tasks.** One change, then check, then commit. Big
   AI changes hide mistakes.
2. **Tests first for the risky parts.** Write the test that proves the
   requirement, then the code.
3. **State the versions.** Put language and framework versions in
   `AGENTS.md` and link the matching documentation, so the agent does not use
   an older API from memory.
4. **No dependency without the dependency check** (`security.md`).
5. **The three-strikes rule.** If the agent fails to fix the same problem three
   times, stop. Simplify the task, restate it, or start a fresh session with
   `AGENTS.md` and the failing test. Do not keep stacking patches.
6. **Review the diff, not just the result.** The builder reads what changed.
7. **Ask for the assumptions.** Before a non-trivial change, the agent lists
   what it is assuming; the builder corrects anything wrong.
8. **Commit often** so any step can be undone.

## Level-specific rules for AGENTS.md

| Level | Add to AGENTS.md |
|---|---|
| Beginner | "Explain as you go": after each change, give a 2 to 3 sentence plain explanation of what the code does and why, and name any new concept in one line. Offer to explain any part when asked. Prefer the simplest approach the builder can follow over a clever one |
| Intermediate | "Explain decisions": note non-obvious choices and trade-offs briefly in the commit message or `docs/DECISIONS.md` |
| Expert | Nothing extra; keep the file minimal |

Why the beginner rule: in a randomized trial of 52 mostly junior developers
learning an unfamiliar Python library (Shen and Tamkin, arXiv 2601.20245, 2026;
the authors work at an AI developer, so read the paper's limitations), the AI
group averaged 50% on a comprehension quiz against 67% for the hand-coding group.
That is **17 percentage points lower** (about a quarter lower in relative
terms), with the largest gap on debugging questions. Within the AI group, the
patterns that scored 65% or higher involved asking for explanations alongside
generated code, asking follow-up questions after generating, or asking only
conceptual questions; patterns that handed everything to the AI scored under
40%. The subgroups were small (2 to 7 people each) and the analysis does not
establish cause. The quiz came minutes after the task, the assistant was a chat
sidebar rather than an agent, and the authors expect agentic tools may have
larger effects. Treat it as a strong hint, not a law.

## A review checklist for builders who cannot yet read the code fluently

Before accepting a change, ask the agent (or yourself):
1. What does this change do, in one sentence, and which requirement ID is it for?
2. What could go wrong? Which test would catch it?
3. Did it add a dependency? Was it checked?
4. Did it touch anything outside what I asked for?
5. Can I explain what it does to someone else? If not, ask for the explanation
   before moving on.
