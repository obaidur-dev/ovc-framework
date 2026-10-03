# BUILD_PLAN.md template (Standard and Full tracks)

Load this when writing `docs/BUILD_PLAN.md`, **after** PRD and SECURITY exist,
so the plan can trace every requirement and verify every planned mitigation.

## Rules

- Order phases to de-risk the biggest unknowns first, not to do easy work first.
- Every phase has a **Verification** section: the specific commands, tests, or
  manual steps that show it works. "Code was written" is not verification.
- The **traceability table** is mandatory: every requirement ID from the PRD
  appears with the phase that delivers it and the test or check that proves
  it. `scripts/check_specs.py` fails if an ID is missing.
- Check vocabulary: start each check with `test:` (automated), `scan:` (a tool
  run), or `manual:` (steps a person follows). Test names may be planned names
  for tests not yet written.
- Include a security phase or tasks so each Planned row in SECURITY.md has a
  home (mitigation work and the check that will become its "Verified by").
- Include a **performance pass** phase when the PRD has performance targets
  (see `performance.md`): baseline, profile, fix the biggest cost, re-measure.
- The **last phase is always "Handover"**: run the `ovc-explain` skill to
  produce `docs/GUIDE.md`, and run its checker. The spec checker fails if the
  plan has no handover step.
- Keep phases small and give each a type check, lint, and test run (see
  `ai-reliability.md`).

## Template

```markdown
# Build Plan: <Project Name>

## Phases
### Phase 1: <name>
- Goal: <...>
- Builds: <...>
- Depends on: <none | Phase N>
- Risk this phase retires: <the unknown it proves out>
- Verification:
  - `test: <command or file::name>` expected: <result>
  - `manual: <steps>` expected: <result>
- Done when: <acceptance condition>

### Phase 2: <name>
...

### Phase N (last): Handover
- Goal: the builder understands what was built and what each part does.
- Builds: `docs/GUIDE.md` via the `ovc-explain` skill, written from the actual
  code and evidence, not from this plan.
- Depends on: all earlier phases
- Verification:
  - `scan: ovc-explain check_guide.py --root .` expected: PASS
  - `manual: builder answers the guide's Check yourself questions` expected: can explain each part
- Done when: the guide passes its checker and the builder has worked through it.

## Traceability
Every requirement, the phase that delivers it, and how it is checked.

| Requirement | Phase | Test / check |
|---|---|---|
| FR-001 | Phase 1 | test: tests/test_x.py::test_y |
| FR-002 | Phase 2 | manual: open /bookings, create one, see it listed |
| NFR-001 | Phase 3 | scan: load test report under 2 s p95 |

## Threat verification (Full track)
| Threat | Phase | Check that will become its "Verified by" |
|---|---|---|
| T-001 | Phase 2 | test: tests/test_auth.py::test_lockout |

## Rollback and reversibility
For any phase touching production data or irreversible actions: how to back
out.

## Living document
When a real decision changes mid-build, update this file and the affected
PRD / ARCHITECTURE / SECURITY rows, and log it in `docs/DECISIONS.md`.
```
