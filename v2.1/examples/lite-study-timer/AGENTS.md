# AGENTS.md

## What this is
Study Timer: a one-page web timer (25-minute focus, 5-minute break) that counts
today's completed blocks. Plain HTML, CSS, and JavaScript modules. Built by a
first-year student; keep code simple and commented.

## Read first
- `docs/SPEC.md`: what to build and how each part is checked
- `docs/SECURITY.md`: the 10-line security checklist
- `docs/DECISIONS.md`: the decision log; read the latest entries before changing direction
- `docs/GUIDE.md`: the Builder's Guide to what exists (written at the end of the build)

## Commands
- Install: nothing to install (no dependencies)
- Run: `python3 -m http.server 8000`, then open http://localhost:8000 (opening the file directly will not load the scripts)
- Test: `npm test` (uses the built-in test runner)
- Lint: none yet
- Type check: none (plain JavaScript)
- Versions: Node.js 22 for tests; any current Chrome or Firefox for the page

## Feedback loop
After every change, run the tests for what you changed. Fix failures before
moving on. If you fail to fix the same problem three times, stop and say so; do
not keep stacking patches.

## Rules
- Never commit secrets. This project should not need any.
- Do not add a dependency without checking it exists, is maintained, and is
  spelled right (see `docs/SECURITY.md` item 6), and add a line to
  `docs/DECISIONS.md`.
- Requirement IDs (FR-/NFR-) are permanent. Mention them in tests and commits.
- Anything the docs mark as an open question is undecided: ask, do not guess.
- Write the simplest correct version first, with a test. Optimise only against
  a measured miss of a target in `docs/SPEC.md`.
- Explain as you go: after each change give a 2 to 3 sentence plain
  explanation of what the code does and why, and name any new concept in one
  line. Prefer the simplest approach the builder can follow.
- Show the study label with `textContent`, never `innerHTML`.

## Definition of done
1. The checks for the step in `docs/SPEC.md` ("How we will check it") have been run and pass.
2. Security checklist items you addressed are ticked in `docs/SECURITY.md` with evidence (`test:`, `scan:`, or `manual:`).
3. Any decision you made or changed is appended to `docs/DECISIONS.md`.
4. The requirements table still matches what the app does; update the doc if not.
5. Final task only: `docs/GUIDE.md` exists, produced with `ovc-explain`, and passes its checker.
