# AGENTS.md

## What this is
Lab Booking: students request lab-instrument bookings; admins approve them.
Python, FastAPI, PostgreSQL. Capstone project: traceability and security
evidence are graded.

## Read first
- `docs/PRD.md`: requirements (FR-/NFR- IDs) in EARS form
- `docs/ARCHITECTURE.md` and `docs/adr/`: structure and why
- `docs/DATA_MODEL.md`, `docs/API_SPEC.md`
- `docs/SECURITY.md`: threat model; statuses need typed evidence
- `docs/BUILD_PLAN.md`: phases, verification, traceability
- `docs/DECISIONS.md`: the decision log; read the latest entries before changing direction

## Commands
- Install: TBD - fill in once the project is scaffolded in Phase 1
- Run: TBD
- Test: TBD
- Lint: TBD
- Type check: TBD (run the Python type checker in strict mode once scaffolded)
- Versions: TBD - record Python, FastAPI, and PostgreSQL versions in Phase 1 and link their docs

## Feedback loop
After every change, run the type check, then lint, then the tests for what you
changed. Fix failures before moving on. If you fail to fix the same problem
three times, stop and say so; do not keep stacking patches.

## Rules
- Never commit secrets; configuration comes from environment variables.
- Do not add a dependency without the dependency check in `docs/SECURITY.md`
  and a line in `docs/DECISIONS.md`.
- Requirement IDs (FR-/NFR-) and threat IDs (T-) are permanent. Name them in
  test names and commit messages.
- Booking ownership always comes from the session, never from the request body.
- Anything the docs mark as an open question is undecided: ask, do not guess.
- Write the simplest correct version first, with a test. Optimise only against
  a measured miss of NFR-001 in `docs/PRD.md`.
- Note non-obvious choices and trade-offs briefly in the commit message or `docs/DECISIONS.md`.

## Definition of done
1. The tests or checks listed for the task in `docs/BUILD_PLAN.md` have been run and pass.
2. Any threat row you addressed is updated in `docs/SECURITY.md` with typed evidence (`test:`, `scan:`, or `manual:`).
3. Any decision you made or changed is appended to `docs/DECISIONS.md`.
4. The traceability table still matches the code; update the doc if it does not.
5. Final task only: `docs/GUIDE.md` exists, produced with `ovc-explain`, and passes its checker.
