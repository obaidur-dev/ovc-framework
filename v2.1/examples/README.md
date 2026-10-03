# Worked examples

Both examples pass the checkers:

```
python3 ovc-specify/scripts/check_specs.py --root examples/lite-study-timer --brief examples/lite-study-timer/docs/project-brief.md
python3 ovc-explain/scripts/check_guide.py --root examples/lite-study-timer
python3 ovc-specify/scripts/check_specs.py --root examples/full-lab-booking --brief examples/full-lab-booking/docs/project-brief.md
```

## 1. `lite-study-timer/` - the whole cycle, with real code (Lite track, beginner level)

A first-year student's pomodoro web page. This one is **complete**: idea ->
brief -> spec -> real working code and tests -> Builder's Guide. It shows the
project at the **end of the build**.

| File | What it shows |
|---|---|
| `idea.txt` | The raw, messy input a student might actually type |
| `docs/project-brief.md` | What `ovc-discover` saves: header with track and level, stack decision with reasons, performance and learning goals |
| `docs/SPEC.md` | One-page spec: IDs, plain language, a typed check per requirement, a handover step |
| `src/`, `index.html`, `tests/`, `package.json` | The actual app (about 7 KB, no dependencies) and 13 passing tests (`npm test`) |
| `docs/SECURITY.md` | The checklist after the build: items ticked **with evidence**, one honest open item (HTTPS, not deployed yet) |
| `docs/DECISIONS.md` | The decision log, grown during the build |
| `docs/GUIDE.md` | The Builder's Guide from `ovc-explain`: tour of every file, flows traced to line numbers, honest `Done`/`Partial` statuses, measured numbers, check-yourself questions |
| `AGENTS.md` | Short context file with feedback loop, beginner "explain as you go" rule, and Definition of done |

Things worth noticing in the guide:
- Only 3 of 8 requirements are `Done`. Five are `Partial` because nobody has
  clicked through the page in a real browser, and the guide says so.
- The guide discloses a real limitation the spec never mentioned (the count
  keeps running across midnight).
- Running the app requires a local server, not double-clicking `index.html`;
  this was discovered while writing the guide and logged as D-003.

The brief names Codex as the build tool, so **no pointer file** was created
(see `ovc-specify/references/tool-compat.md`).

## 2. `full-lab-booking/` - a project with logins (Full track, intermediate level, abbreviated)

A final-year capstone: students book lab equipment, admins approve. Shortened
for reading: six functional requirements, eleven threat rows, two ADRs. It stops
at the spec stage (no code), so it has no `GUIDE.md`; the plan ends with a
Handover phase for it.

What to look at:
- `docs/PRD.md`: EARS requirements with IDs and numeric targets
- `docs/ARCHITECTURE.md` plus `docs/adr/`: data-flow diagram with trust
  boundaries, two decision records
- `docs/SECURITY.md`: STRIDE table with all four statuses and a "Verified by"
  column; the dependency check; the compliance question recorded as
  "not confirmed" rather than assumed
- `docs/BUILD_PLAN.md`: phases ending in Handover, traceability table, threat
  verification table
- `CLAUDE.md`: a one-line pointer (`@AGENTS.md`), because the brief names
  Claude Code as the build tool

**Read this before copying:** the SECURITY.md in this example is a mid-build
*snapshot* so two rows can show `Mitigated` with evidence; the test names refer
to a repository that does not exist; and the dependency-table entries show the
format, not real vetting. At spec time every row would be `Planned`.
