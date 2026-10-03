---
name: ovc-specify
description: Turns a finished project-brief.md (from ovc-discover) into a verified spec set for an AI coding agent, covering requirements with IDs, architecture, a STRIDE threat model with evidence, measurable performance targets, a build plan with a requirement-to-test traceability table, AGENTS.md, and a decision log. Scales by size (lite, standard, full) and by the builder's level (beginner, intermediate, expert). Use when someone provides a project brief or asks for a PRD, spec, threat model, build plan, or AGENTS.md from one, or mentions OVC or "spec set". Also has a brownfield mode that, for an EXISTING repo, scans the code and writes AGENTS.md, SECURITY.md, and a gap list. Runs scripts/check_specs.py before handover. Do NOT use to write application code, debug, or for one-off scripts. Part 2 of 3 of the OVC Framework (Obaidur's Verified Coding Framework).
license: MIT
metadata:
  version: "2.1.1"
  framework: "OVC (Obaidur's Verified Coding Framework)"
  part: "2 of 3"
---

# OVC Specify (part 2 of 3)

Takes the approved brief from `ovc-discover` and produces the documents an AI
coding agent builds from. What makes the framework "Verified": every
requirement has an ID, every ID is traced to a phase and a test, no security
threat is called `Mitigated` without evidence, and the plan ends with a guide
(`ovc-explain`) so the builder understands what was built.

**Fresh session or cleared context.** Run this in a fresh session (or after
clearing the context) so the brief is the only source of truth. Old discovery
chatter can quietly override what the person approved. If the session already
holds the discovery conversation, that is allowed, but re-read the brief from
disk and ignore anything not written in it.

## Step 0 - Choose the mode

- **Brownfield:** the person points at an existing repository and wants docs,
  a security review, or an `AGENTS.md` for it. Read `references/brownfield.md`
  and follow it; then jump to Step 7. No brief, track, or level is needed
  (ask which level only if they want explanations).
- **Greenfield (default):** a new project. Continue below.

If the request is really "write the code" or "fix this bug", this is the wrong
skill; say so and just help.

## Step 1 - Validate the brief; read track and level

Run the header check (path is relative to this skill's folder):

```
python3 scripts/check_specs.py --brief <path-to>/project-brief.md
```

It prints the track and the effective level. Exit code 2 means the brief is
rejected:

- **Unknown `ovc-brief-version`:** stop. Say this skill reads version 2 only
  and which version the file says. Do not guess a conversion.
- **No header at all:** probably a v1 brief. Do not proceed silently. Offer to
  upgrade it: ask track and level, add the header, and ask the missing
  questions for the sections it lacks. Save the upgraded file only after they
  approve it.
- **Invalid `track` or `level`:** ask which valid value they meant.

If Python or a shell is unavailable, check by eye: the file starts with a `---`
header containing `ovc-brief-version: 2` and `track:`.

If `level` is absent, use `beginner` for lite and `intermediate` otherwise. A
brief from before revision 2.1 may also lack "Performance & efficiency goals"
and "Builder & learning goals": ask for them in Step 2.

**No brief at all?** Do not hard-block. Ask once for the essentials (problem,
users, scope, success outcome, constraints, anything sensitive), write a brief
using `references/brief-template.md`, note "reconstructed without a discovery
interview" in Raw notes, get approval, then continue. If the input is only a few
words, say plainly that `ovc-discover` will give a better result.

Read the brief fully, especially "Open questions" and "Assumptions & risks".
Copy it to `docs/project-brief.md` unchanged.

### What the level changes here

| | Beginner | Intermediate | Expert |
|---|---|---|---|
| Explanations | "Why this step" line per document; jargon defined on first use (glossary below) | Brief rationale where a choice was made | None unless asked |
| Open questions | Ask in plain words, offer a recommended answer to accept | Ask with options | Ask tersely |
| `AGENTS.md` | Adds the "Explain as you go" rule | Adds "note non-obvious choices" | Minimal |
| Handover guide | Full guide with check-yourself questions | Guide with architecture and trade-offs | Compact map and runbook |

## Step 2 - Ask what the brief may not answer (once, one message)

1. **Which AI coding tool will build this?** Skip if the brief's Constraints say.
   Used only to decide whether a pointer file is needed (Step 6).
2. **Rules or policies** (only if personal data, children, health, or payments
   are involved and the brief does not answer): ask, never assume. Wording is in
   `references/security.md`.
3. **Performance and learning goals** if the brief lacks them: ask the short
   questions from `ovc-discover` Step 4, in the person's level.

## Step 3 - Pick the documents

| Document | Lite | Standard | Full | Load this reference |
|---|---|---|---|---|
| `docs/SPEC.md` (one page) | yes | no | no | `spec-lite.md` |
| `docs/PRD.md` | no | yes | yes (EARS) | `prd.md` (+ `ears.md` on Full, or if offered and accepted) |
| `docs/ARCHITECTURE.md` | no | yes | yes + data-flow diagram | `architecture.md` |
| `docs/adr/ADR-NNN-*.md` | no | no | yes (2+) | `architecture.md` |
| `docs/DATA_MODEL.md` | no | if data persists | if data persists | `data-model.md` |
| `docs/API_SPEC.md` | no | if there is an API | if there is an API | `api-spec.md` |
| `docs/SECURITY.md` | 10-line checklist | STRIDE | STRIDE + full evidence | `security-lite.md` or `security.md` |
| `docs/BUILD_PLAN.md` | no (steps in SPEC.md) | yes | yes | `build-plan.md` |
| Performance targets and checks | one NFR row if the brief has a goal | NFRs + perf pass | NFRs + perf pass | `performance.md` |
| `AGENTS.md` (root) | yes | yes | yes | `agents-md.md` + `ai-reliability.md` |
| `docs/DECISIONS.md` | yes | yes | yes | `decisions.md` |
| Tool pointer file | named tool only | named tool only | named tool only | `tool-compat.md` |

Say plainly which files you will generate and which you are skipping, with a
one-line reason for each skip. **Load a reference file only when you are about
to write that document**; never load files for documents you are skipping.

**Beginner "Why this step" lines:**

| Document | Why this step |
|---|---|
| SPEC / PRD | It is the contract: what to build and how you will check each part. |
| ARCHITECTURE | A map of the parts, so nothing is built twice or forgotten. |
| SECURITY | AI-written code often has security holes unless someone checks; this is the check. |
| Performance targets | "Fast" is a wish until it is a number you can measure. |
| BUILD_PLAN | Small steps, each ending with a check, keep the AI from going far in a wrong direction. |
| AGENTS.md | The AI forgets between sessions; this file reminds it every time. |
| DECISIONS.md | A running note of choices means the docs never have to be rewritten. |
| Final guide | At the end you get a guide to what exists, so you are not left with code you cannot explain. |

**Beginner glossary.** Define each term inline in one sentence the first time it
appears, including when you explain what Standard or Full would add:

| Term | Plain definition |
|---|---|
| STRIDE | A six-letter checklist of ways software gets attacked: Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege. |
| Threat model | Listing what could go wrong and what you will do about each, before building. |
| Trust boundary | A line where data passes from something you control to something you do not, such as a user's browser sending input to your server. |
| ADR | Architecture Decision Record: a short note saying what big choice was made, what else was considered, and why. |
| EARS | A fixed sentence shape for requirements ("WHEN this happens, the system SHALL do that") so they cannot be misread. |
| Traceability | A table showing every requirement has a plan step and a check, so nothing gets lost. |
| Profiling | Measuring where a program really spends its time, instead of guessing. |

## Step 4 - Generate, in dependency order

PRD or SPEC -> ARCHITECTURE (+ ADRs) -> DATA_MODEL -> API_SPEC -> SECURITY ->
BUILD_PLAN -> AGENTS.md -> DECISIONS -> pointer file. Security comes after
architecture because the data flow gives you the trust boundaries; the plan
comes after security so every planned mitigation gets a phase and a check.

Rules that apply everywhere:

- **Pull from the brief; do not invent.** Where it is silent, see Step 5.
- **"Considered and not applicable" beats blank.** Write
  "Not applicable: <reason>" instead of leaving a section empty.
- **Skip padding.** In a threat table or non-functional list, include only what
  genuinely applies.
- **Numbers, not wishes.** Non-functional requirements (speed, size, capacity)
  need a number and a typed check (`performance.md`).
- **IDs are permanent:** requirements `FR-001`, `NFR-001`; threats `T-001`;
  gaps `G-001`; decisions `D-001`.
- **The plan ends with the handover step** (produce `docs/GUIDE.md` with
  `ovc-explain`), and so does the "Definition of done" in `AGENTS.md`.

## Step 5 - Handle gaps: open-question markers, batched

When a document needs something the brief does not answer:

1. Write an open-question marker in that spot: the text
   `[OPEN QUESTION: <what is missing and why it matters>]`. An invented answer
   looks identical to a real decision to the next reader; an honest gap does not.
2. Collect every marker across all documents into one list.
3. Before finishing, show that list **in one batch** and ask. Do not drip them
   one at a time and do not silently skip them. Beginner level: offer a
   recommended answer for each so they can just accept.
4. Apply their answers and remove the matching markers. Anything they choose
   to leave open stays flagged.

Hold the security document to a higher bar: for how sensitive data is handled,
ask rather than flag and move on.

## Step 6 - The verification chain and the pointer file

**Requirements -> plan -> tests.** Every requirement has an ID and an acceptance
check. The BUILD_PLAN traceability table (Lite: the SPEC.md requirements table)
maps every ID to a phase and a typed check (`test:`, `scan:`, or `manual:`).
Test names may be planned names.

**Threats -> evidence.** Every STRIDE row has a status from the four-value key:
`Planned`, `Mitigated`, `Accepted risk`, `Open`. A row cannot be `Mitigated`
without typed evidence in "Verified by". Nothing is built at spec time, so new
rows are normally `Planned` with the planned check named.

**Pointer file.** Follow `references/tool-compat.md`: create a pointer file only
for the tool the person named, and only if the table says one is needed.
Otherwise create nothing extra and say why.

**Dependencies.** The AI coding agent must not add packages without the
dependency check (`references/security.md`; Lite item 6).

## Step 7 - Run the checker before handing over

```
python3 scripts/check_specs.py --root <project-root> --brief docs/project-brief.md
python3 scripts/check_specs.py --root <project-root> --mode brownfield    # brownfield only
```

It exits non-zero and lists each failure with file and line. It checks:

1. no unresolved open-question markers remain
2. every `FR-`/`NFR-` ID in the PRD (Lite: SPEC.md) is traced to a phase and a
   typed check
3. every STRIDE row has one of the four statuses
4. no row is `Mitigated` without typed evidence
5. required files exist for the track; `AGENTS.md` points to files that exist,
   references `docs/DECISIONS.md`, and includes the `docs/GUIDE.md` handover
6. the plan ends with the handover step (`docs/GUIDE.md`)
7. on Full: requirements use EARS (`SHALL`), a data-flow section exists, and at
   least one ADR exists

It also warns when no non-functional requirement contains a number, and when a
beginner's `AGENTS.md` lacks the explain-as-you-go rule.

Fix every failure and re-run. If the only failures are open questions the
person has **explicitly chosen to leave open**, re-run with
`--allow-open-questions` and list those questions in your handover message. If
the script cannot run, do the checks by hand and say you did.

## Step 8 - Hand over

Present the files. Name which you generated and which you skipped and why. Show
any questions still open. Then say explicitly:

- **These are living documents.** When a decision changes mid-build, update the
  affected file and append a line to `docs/DECISIONS.md`.
- **How to start building:** point the AI coding agent at the project root and
  say, for example, "Read AGENTS.md, then start Phase 1." If a pointer file was
  created, name it.
- **Definition of done** (in `AGENTS.md`): run the planned tests, update
  security evidence, log decisions.
- **At the end of the build, run `ovc-explain`.** It writes `docs/GUIDE.md`, a
  guide to what was actually built, what each part does, what is proven and
  what is not. The project is not finished without it.
