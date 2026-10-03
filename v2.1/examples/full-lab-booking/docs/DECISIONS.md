# Decision log

Append-only. Newest at the bottom. Never edit past entries.

## D-001 - Full track; Python, FastAPI, PostgreSQL (project start)
- Decision: Full track because the capstone is assessed on traceability and threat-model evidence; stack as in the brief.
- Why: assessment criteria; department standard stack.
- Alternatives: Standard track (rejected: assessment needs ADRs and evidence).
- Affects: all docs, ADR-001, ADR-002
- Docs updated: yes
- Supersedes: none

## D-002 - Confirm DPDP Act applicability with the department (follow-up)
- Decision: the team will ask the department whether the DPDP Act applies and record the answer in `docs/SECURITY.md` before Phase 4 closes.
- Why: the team is not sure; the spec must not assume.
- Alternatives: assume it applies (rejected: would add requirements without basis).
- Affects: SECURITY.md "Rules and policies", DATA_MODEL.md lifecycle
- Docs updated: yes (recorded as unconfirmed)
- Supersedes: none
