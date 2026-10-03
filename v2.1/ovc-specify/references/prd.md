# PRD.md template (Standard and Full tracks)

Load this when writing `docs/PRD.md`. On Lite, use `spec-lite.md` instead.

## Rules

- Every requirement has an **ID**: `FR-001`, `FR-002`, ... for functional
  requirements and `NFR-001`, ... for non-functional ones. IDs are permanent:
  never renumber; retire a requirement by marking it `Dropped`, not by
  deleting the row. The build plan, tests, and threat model point at these IDs.
- Every requirement has an **acceptance check**: something a person can do or a
  test can assert. Plain language is fine on Standard. "Works well" is not a check.
- Standard: offer EARS wording (`ears.md`) once, show how one or two
  requirements would look, and let the person choose. Full: EARS is required;
  load `ears.md` and write every requirement in it.
- Pull everything from the brief. Anything the brief does not answer becomes
  an open-question marker, not an invention.
- Performance goals from the brief become NFRs **with numbers** and a typed
  check; load `performance.md` for starting targets. A non-functional
  requirement with no number cannot be tested.

## Template

```markdown
# Product Requirements: <Project Name>

*Source of truth: `docs/project-brief.md`.*

## Overview
One paragraph restating the problem and the solution, from the brief.

## Users and use cases
Concrete scenarios: "As a <user>, I want <action>, so that <outcome>."

## Functional requirements
| ID | Requirement | Priority | Acceptance check |
|---|---|---|---|
| FR-001 | <what the system does; EARS wording on Full> | Must | <observable check> |
| FR-002 | <...> | Should | <...> |

Priority: Must (v1 fails without it), Should (important), Could (nice to have).

## Non-functional requirements
Only categories that apply: performance, availability, accessibility,
localisation, browser or OS support, privacy, maintainability. Each needs a
measurable target. Skip categories that do not apply; do not pad with "N/A".

| ID | Requirement | Target / how measured |
|---|---|---|
| NFR-001 | <e.g. "Pages load quickly on a mid-range phone"> | <e.g. under 2 s on a throttled 4G profile> |

## Out of scope
From the brief, expanded if more came up.

## Success criteria
From the brief's "Success looks like": specific, checkable outcomes that mean
v1 is done.

## Open questions
Open-question markers collected here and inline above, or "None."
```

## Full track additions

- Add a `Source` column to the functional table that cites the brief section
  or user story each requirement came from.
- Add a short "Stakeholders and approval" section: who signs off, and on what
  evidence.
- Keep requirement text to **one sentence each** so it can be traced to one
  test.
