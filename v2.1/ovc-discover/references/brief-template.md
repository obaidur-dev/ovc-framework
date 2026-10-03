<!--
SHARED CONTRACT - OVC project brief template, format version 2 (revision 2.1, additive).
This file is byte-identical in ovc-discover/references/ and ovc-specify/references/.
Change both copies together or neither. evals/test_check_specs.py fails if they differ.
-->

# Project brief template (format version 2)

The brief is the only artifact `ovc-discover` produces and the only input
`ovc-specify` and `ovc-explain` trust. It must be self-contained: whoever (or
whatever) reads it next has no memory of the conversation that produced it.

## The header is machine-readable

The file starts with a header block of `key: value` lines between two `---`
lines. The skills and `scripts/check_specs.py` read it.

| Key | Required | Allowed values |
|---|---|---|
| `ovc-brief-version` | yes | `2` (any other value is rejected) |
| `track` | yes | `lite`, `standard`, or `full`: how much paperwork the project needs |
| `level` | no | `beginner`, `intermediate`, or `expert`: how much teaching and guidance the person wants. If absent: `lite` means `beginner`; `standard` and `full` mean `intermediate` |
| `project` | yes | the project name |

`track` is about the **project** (size and rigor). `level` is about the
**person** (how much they want explained). They are independent: an expert can
run a Lite project; a beginner can be doing a Full capstone.

## Template

Copy this structure exactly. Do not add or rename sections.

```markdown
---
ovc-brief-version: 2
track: <lite | standard | full - pick exactly one>
level: <beginner | intermediate | expert - pick exactly one>
project: <Project Name>
---

# Project Brief: <Project Name>

## Problem
What is broken, missing, or annoying right now, and for whom. One or two
paragraphs. The actual pain, not a feature list.

## Users
Who this is for. If there is more than one kind of user (for example an admin
and an end user), describe each briefly and note where their needs conflict.

## Scope
**In scope (v1):** the smallest version that actually solves the problem.
**Explicitly out of scope (for now):** things that came up but were deferred,
and why. This list stops scope creeping back in later.

## Success looks like
How we will know it worked. At least one observable, checkable outcome
("a student can book a lab slot in under a minute", "I use it every study
day for two weeks"), not "it feels done".

## Constraints
Deadline, budget, team size and skills, target platform(s), what it must
integrate with, what it must NOT use, and which AI coding tool(s) will build
it. Fixed technology requirements go here (for example "the course requires
Python").

## Performance & efficiency goals
How fast and how light it needs to be, in numbers where possible ("usable in
under 2.5 s on a mid-range phone", "95% of requests answered in under 500 ms
for 100 users", "runs a full day on one battery"). If the person has no idea,
write the defaults chosen and say they are defaults. "Not applicable:
<reason>" is allowed.

## Key decisions (with reasoning)
Every real decision made during discovery and why. Include the technology
choice: language and framework, why, the main alternative, and when to
revisit it. "Use SQLite because it is a single-user app and needs no server"
beats "use SQLite".

## Builder & learning goals
Who will maintain this, and what they should understand by the end ("I want to
be able to explain every file", "I only need to run and deploy it", "I will
change the database myself"). This decides how the final project guide is
written.

## Security & privacy concerns already raised
Sensitive data, logins, payments, uploads, legal or policy rules (ask, do not
assume), abuse potential, any feature that calls an AI model. If truly
nothing applies, say so explicitly and say why.

## Assumptions & risks
**Assumptions:** things we are treating as true but have not verified.
**Risks:** what could stop this project or hurt it, and what we would do
about each.

## Open questions
Anything genuinely unresolved. Flagged, never silently guessed.
`ovc-specify` treats this list as required reading.

## Raw notes
Anything else worth keeping in the person's own words: a phrase that captures
the vision, a competitor they mentioned, a constraint said in passing.
```

## Rules that apply to every section

- **Considered and not applicable beats blank.** If a section does not apply,
  write "Not applicable: <reason>". A blank section cannot be told apart from
  "forgot to ask".
- **Depth scales with the track.** Lite: one or two lines per section is fine.
  Standard: full sentences with reasoning. Full: name stakeholders and the
  evidence a reviewer will expect, and write assumptions and risks in detail.
- **The person approves the brief before it is saved** (see `ovc-discover`).
- **Compatibility.** Briefs written before revision 2.1 have no `level` header
  and lack the "Performance & efficiency goals" and "Builder & learning goals"
  sections. They are still valid; the skills use the default level and ask for
  the missing information when it matters.
