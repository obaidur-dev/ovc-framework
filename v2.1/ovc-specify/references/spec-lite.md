# SPEC.md template (Lite track)

Load this only on the Lite track. It replaces PRD, ARCHITECTURE, DATA_MODEL,
API_SPEC, and BUILD_PLAN with **one page** in plain language. Target: about
60 lines. If it grows past two screens, the project probably belongs on the
Standard track; say so and offer to switch.

## Why this document exists (say this to the person)

"This page is the contract between you and the AI. It says what to build,
how you will check each part works, and in what order to build it. Without
the 'how you will check' column, 'done' just means 'the AI stopped typing'."

## Writing rules

- Plain words. A first-year student should be able to read every line.
- Every requirement gets an ID (`FR-001`, `FR-002`, ... for features;
  `NFR-001`, ... for qualities like speed or browser support) and a check a
  person can actually do: run a command, click through steps, or a named test.
- No jargon without a definition on first use (see "Words used" below).
- Unknowns become open-question markers, never guesses (see `SKILL.md`).

## Template

```markdown
# SPEC: <Project Name>

*Track: Lite. Source of truth: `docs/project-brief.md`.*

## What we are building
Two or three sentences: the problem, who it is for, the solution.

## Requirements
Each row says what the app must do and how you will check it.

| ID | The app must... | How we will check it |
|---|---|---|
| FR-001 | <one plain sentence> | manual: <steps and the result you should see> |
| FR-002 | <...> | test: <test file or function name, even if not written yet> |
| NFR-001 | <quality, e.g. "work in the latest Chrome and Firefox"> | manual: <...> |

(Checks start with `test:` for automated checks or `manual:` for steps you do
by hand, so it is always clear what "done" means.)

## Not included in v1
- <thing> - <why it waits>

## Build steps
Small steps, riskiest first. Every step ends with something you can run.
1. <step> - done when: <what you can see or run> (covers FR-001)
2. <step> - done when: <...> (covers FR-002, NFR-001)

## Security
See `docs/SECURITY.md`: a 10-line checklist. Tick items off only with
evidence.

## Understanding what you built
The final build step is to produce `docs/GUIDE.md` with the `ovc-explain`
skill: a guide to what exists, what each part does, and what is and is not
proven.

## Decisions
Big choices and changes are logged in `docs/DECISIONS.md`.

## Open questions
- <marker-style open questions, or "None.">

## Words used
- **v1**: the smallest useful version.
- **Requirement**: something the app must do, written so you can check it.
- **Test**: a check that can be repeated. Automated tests run by a command;
  manual checks are steps you follow.
```

## Notes for the agent

- Keep "Words used" to terms that actually appear. If you used **STRIDE**,
  **trust boundary**, **ADR**, **EARS**, or **traceability**, copy its
  one-sentence definition from the "Lite glossary" in `SKILL.md`; on Lite you
  usually will not need them here.
- "Build steps" replaces BUILD_PLAN. Each step must name which requirement IDs
  it covers; every ID in the table must be covered by at least one step.
- The **last build step is always the handover**: write `docs/GUIDE.md` with
  `ovc-explain` and run its checker. The spec checker fails without it.
- If the brief has a performance goal, include it as an `NFR-` row with a
  number and a typed check (see `performance.md`).
