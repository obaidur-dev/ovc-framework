# Build Plan: Lab Booking

## Phases
### Phase 1: Skeleton, database, and overlap guarantee
- Goal: prove the riskiest unknown, database-level overlap prevention.
- Builds: project scaffold, schema, exclusion constraint, booking create/list.
- Depends on: none
- Risk this phase retires: whether the exclusion constraint works as ADR-001 assumes.
- Verification:
  - `test: tests/test_booking.py::test_overlap_rejected_by_database` expected: second overlapping insert fails
  - `test: tests/test_booking.py::test_create_pending_booking` expected: booking is pending
- Done when: FR-003 and FR-004 checks pass.

### Phase 2: Authentication and authorization
- Goal: login, lockout, roles, owner-only reads.
- Builds: auth module, sessions, route role checks.
- Depends on: Phase 1
- Risk this phase retires: that auth stays isolated behind one module (ADR-002).
- Verification:
  - `test: tests/test_auth.py::test_login_shows_bookings` expected: list is shown
  - `test: tests/test_authz.py::test_booking_read_is_owner_only` expected: 403 or 404 for others
- Done when: FR-001, FR-002, FR-006 checks pass.

### Phase 3: Admin decisions, audit, and email
- Goal: approve or reject with a permanent record and notification.
- Builds: decision endpoint, audit entries, email sender.
- Depends on: Phase 2
- Risk this phase retires: mail relay access from the VM (a stated assumption).
- Verification:
  - `test: tests/test_audit.py::test_decision_creates_audit_entry` expected: audit row with admin and time
  - `manual: approve a booking and receive the email on the VM` expected: email arrives
- Done when: FR-005 checks pass.

### Phase 4: Hardening and evidence
- Goal: finish security rows and non-functional targets.
- Builds: rate limiting, accessibility fixes, CI scans, load test.
- Depends on: Phase 3
- Risk this phase retires: performance and accessibility targets.
- Verification:
  - `test: tests/test_ratelimit.py::test_429_after_limit` expected: 429
  - `scan: pip-audit and bandit in CI` expected: no unresolved findings
- Done when: all NFR checks and all Planned threat rows are Mitigated with evidence.

### Phase 5: Handover
- Goal: both team members can explain and defend what was built.
- Builds: `docs/GUIDE.md` via the `ovc-explain` skill, written from the code and the evidence, not from this plan.
- Depends on: Phase 4
- Risk this phase retires: building something nobody on the team can explain at the assessment.
- Verification:
  - `scan: ovc-explain check_guide.py --root .` expected: PASS
  - `manual: each team member answers the guide's Check yourself questions without notes` expected: both can explain every part
- Done when: the guide passes its checker and both members have worked through it.

## Traceability
| Requirement | Phase | Test / check |
|---|---|---|
| FR-001 | Phase 2 | test: tests/test_auth.py::test_login_shows_bookings |
| FR-002 | Phase 2 | test: tests/test_auth.py::test_lockout_after_five_failures |
| FR-003 | Phase 1 | test: tests/test_booking.py::test_create_pending_booking |
| FR-004 | Phase 1 | test: tests/test_booking.py::test_overlap_rejected_by_database |
| FR-005 | Phase 3 | test: tests/test_audit.py::test_decision_creates_audit_entry |
| FR-006 | Phase 2 | test: tests/test_authz.py::test_booking_read_is_owner_only |
| NFR-001 | Phase 4 | scan: load test report, p95 under 500 ms at 100 users |
| NFR-002 | Phase 2 | test: tests/test_auth.py::test_password_stored_as_argon2id |
| NFR-003 | Phase 4 | scan: automated accessibility scan, plus manual: keyboard walkthrough |

## Threat verification
| Threat | Phase | Check that will become its "Verified by" |
|---|---|---|
| T-001 | Phase 2 | test: tests/test_auth.py::test_lockout_after_five_failures |
| T-002 | Phase 2 | manual: cookie flags in dev tools |
| T-003 | Phase 1 | test: tests/test_booking.py::test_owner_from_session_only |
| T-004 | Phase 2 | test: tests/test_authz.py::test_student_cannot_decide |
| T-005 | Phase 2 | test: tests/test_authz.py::test_booking_read_is_owner_only |
| T-006 | Phase 3 | test: tests/test_audit.py::test_decision_creates_audit_entry |
| T-007 | Phase 4 | scan: bandit plus manual: injection payloads |
| T-008 | Phase 4 | test: tests/test_ratelimit.py::test_429_after_limit |
| T-009 | Phase 3 | decide email contents, then manual: review sent email |
| T-010 | Phase 4 | scan: pip-audit in CI |

## Rollback and reversibility
Schema changes use migrations with a down step. Take a database backup before
any migration that drops or rewrites data.

## Living document
When a decision changes mid-build, update this file and the affected PRD,
ARCHITECTURE, and SECURITY rows, and log it in `docs/DECISIONS.md`.
