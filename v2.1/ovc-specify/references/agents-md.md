# AGENTS.md template (all tracks)

Load this when writing the root `AGENTS.md`. It is the primary, tool-neutral
context file: an open convention that many AI coding tools read from the
project root. Which tools read it natively, and which need a pointer file, is
in `tool-compat.md`.

## What belongs in it (keep it short)

Target 30 to 60 lines; stay under 120. Include **only what the agent cannot
infer** from the code and the docs it can read itself:

- build, test, and lint commands (exact ones)
- conventions that differ from the language or framework default
- non-negotiables (security, "never touch X")
- where the docs are and what each is for
- the definition of done

Leave out: directory listings, dependency lists, restated architecture,
generic advice ("write clean code"), and anything duplicated from the docs.
Long files cost context on every session and make instructions get ignored.

If commands are not decided yet, write
`TBD - fill in once the stack from the architecture doc is scaffolded`
rather than guessing.

## Template

```markdown
# AGENTS.md

## What this is
Two or three sentences from the brief.

## Read first
- `docs/<SPEC.md | PRD.md>`: what to build and how each part is checked
- `docs/SECURITY.md`: security requirements and the dependency check
- `docs/BUILD_PLAN.md`: phases and verification (Standard and Full only)
- `docs/ARCHITECTURE.md`, `docs/DATA_MODEL.md`, `docs/API_SPEC.md`: only those that exist
- `docs/DECISIONS.md`: the decision log; read the latest entries before changing direction

## Commands
- Install: `<cmd>`
- Run: `<cmd>`
- Test: `<cmd>`
- Lint: `<cmd>`
- Type check: `<cmd>`
- Versions: `<language and framework versions>` (docs: `<link to that version's docs>`)

## Feedback loop
After every change, run the type check, then lint, then the tests for what you
changed. Fix failures before moving on. If you fail to fix the same problem
three times, stop and say so; do not keep stacking patches.

## Rules
- Never commit secrets; configuration comes from environment variables.
- Do not add a dependency without the dependency check in `docs/SECURITY.md`
  and a line in `docs/DECISIONS.md`.
- Requirement IDs (FR-/NFR-) are permanent. Reference them in tests and commits.
- Anything the docs mark as an open question is undecided: ask, do not guess.
- Write the simplest correct version first, with a test. Optimise only against
  a measured miss of a target in `docs/<PRD.md | SPEC.md>`.
- <level rule from the table below, if any>
- <project-specific non-negotiables from SECURITY.md or the brief>

## Definition of done
A task is done only when all of these are true:
1. The tests or checks listed for it in `docs/<BUILD_PLAN.md | SPEC.md>` have been run and pass.
2. Any security row or checklist item you addressed is updated in `docs/SECURITY.md` with typed evidence (`test:`, `scan:`, or `manual:`).
3. Any decision you made or changed is appended to `docs/DECISIONS.md`.
4. The requirement table still matches what the code does; if it does not, update the doc, do not leave it stale.
5. **Final task of the project only:** `docs/GUIDE.md` exists, produced with the `ovc-explain` skill (or its template) and passing its checker. The project is not finished until the builder can understand what was built.

## Keeping docs current
These files describe the project as it really is. When reality changes,
change the file in the same piece of work.
```

### Level rule to copy into "Rules" (from the brief's `level`)

| Level | Line to add |
|---|---|
| beginner | `Explain as you go: after each change give a 2 to 3 sentence plain explanation of what the code does and why, and name any new concept in one line. Prefer the simplest approach the builder can follow.` |
| intermediate | `Note non-obvious choices and trade-offs briefly in the commit message or docs/DECISIONS.md.` |
| expert | none |

Why: see `ai-reliability.md`.

## Tool pointer files

Do **not** put tool-specific content in AGENTS.md. If the person named a tool
that needs a pointer file, create only that file, as `tool-compat.md`
describes. Never create pointer files for tools the person did not name.
