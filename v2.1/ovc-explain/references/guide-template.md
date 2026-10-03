# GUIDE.md template (the Builder's Guide)

Load this when writing `docs/GUIDE.md`. Write it from the **actual code and
real command output**, not from the plan. Where the plan and the code disagree,
the code wins and the difference is reported.

## Rules (the checker enforces most of these)

- Section headings must contain the words shown below. Order may not change.
- Every path in the Project tour must exist. Every `file:line` reference must
  point to a real line.
- Every requirement ID from the PRD (or SPEC) appears in Requirements coverage.
- Status values are exactly `Done`, `Partial`, `Not built`.
  - `Done` needs typed evidence (`test:`, `scan:`, or `manual:`) that you
    actually ran or inspected. A `test: path::name` entry must point at a real
    file containing that test name.
  - `Partial` says in the Evidence cell what is proven and what is not.
  - `Not built` gives the reason.
- Performance numbers are written only if they were **measured**. Otherwise the
  cell says exactly `Not measured`.
- Never invent. If you could not check something, it goes under "What I could
  not verify".
- Never include secret values. Name the kind and place only.

## Depth by level

| Section | Beginner | Intermediate | Expert |
|---|---|---|---|
| At a glance | 1 short paragraph, everyday words | paragraph + stack | 3 lines |
| The big picture | picture + plain-language caption | components + data flow | components + invariants |
| Project tour | every file, with an everyday description | every file or folder | folders and entry points only |
| Walkthrough | 2 to 3 flows, step by step, every step linked to code | 1 to 2 flows with key decisions | 1 flow, compact |
| Concepts | every concept actually used, each tied to a place in this project | non-obvious ones | omit |
| Check yourself | 5 to 8 questions | 3 to 5 questions | optional |

## Template

```markdown
# Builder's Guide: <Project Name>

*Level: <level>. Written from the code as it exists. Last verified against the
project on <date>. Commit: <short hash or "not a git repo">.*

## At a glance
What this is and who it is for, in plain words. The stack in one line and why
(link the decision in `docs/DECISIONS.md` or the brief). What state it is in
overall: how many requirements are Done, Partial, Not built.

## How to run it
Exact commands, copied from commands you ran or `AGENTS.md`.
- Install: `<cmd>`
- Run: `<cmd>`  (then open <address>)
- Test: `<cmd>`  (what a pass looks like)
Say which of these you actually ran.

## The big picture
A diagram (mermaid) of the parts and how data moves between them, with trust
boundaries marked, plus a caption. Draw what the code does, not what the plan
intended. If they differ, add a "Differs from the plan" list.

## Project tour
Every file or folder worth knowing, and when you would edit it.

| Path | What it does | Edit it when |
|---|---|---|
| `src/timer.js` | The countdown logic, with no screen code | You change how phases or time work |

## Walkthrough
Follow one or more real user actions through the code, step by step.
**Flow 1: <action>**
1. <what happens, in words> (`src/app.js:41`)
2. <next step> (`src/timer.js:18`)

## Requirements coverage
One row per requirement ID in the PRD or SPEC.

| ID | Where it lives | Status | Evidence |
|---|---|---|---|
| FR-001 | `src/timer.js:12` | Done | test: tests/timer.test.js::counts_down_from_25_minutes |
| FR-003 | `src/app.js:60` | Partial | manual: code written; not heard in a browser yet |

## Security status
What is protected and how it was checked, what is accepted, and what is still
open or unverified. Summarise `docs/SECURITY.md`; do not copy it. List every
item that is not yet verified.

## Performance
Targets from the brief or PRD, with what was actually measured.

| Target | Goal | Measured | How measured |
|---|---|---|---|
| Page weight | 1 MB or less | 7 KB | scan: total bytes of served files |
| Load time | 2.5 s or less (LCP) | Not measured | n/a |

## Concepts
Only the ideas this project actually uses, each tied to where it appears here.
**Event loop (`src/app.js:30`)**: the browser calls your function again and
again instead of you looping yourself.

## Limits and known gaps
What it does not do, what could break it, and what you would hit first as it
grows.

## Changing it safely
For the three most likely changes ("add a feature", "change a rule", "change
the data"): which files to edit, which tests to run, which requirement IDs and
docs to update, and what to log in `docs/DECISIONS.md`. Include a "if you change
X, also check Y" list.

## Check yourself
Questions about this project (see `teaching-levels.md`). Answers go at the end.

Q1. <question>
Q2. <question>

### Answers
A1. <answer, with a `file:line` pointer>
A2. <answer>

## What I could not verify
Everything you did not run, read, or measure, and why (no browser available,
no permission to run, no data). Write "Nothing" only if that is true.
```
