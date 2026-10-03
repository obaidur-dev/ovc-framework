# Security: Lab Booking

*Snapshot for illustration: taken after Phase 2 of the build, so two rows show
`Mitigated` with evidence. The repository named in the evidence is
hypothetical. At spec time every row would be `Planned`.*

## Why this document exists
Benchmarks of AI-generated code (Veracode's 2025 GenAI Code Security Report: in
45% of 80 test cases across 100+ models the model chose the insecure option; its
2026 report: a 56% average security pass rate) show that unverified AI output is
risky. The "Verified by" column requires
proof, not belief.

## Data classification
| Data | Sensitivity | Where |
|---|---|---|
| Email, name | Personal data | `users` table |
| Password hashes | Credential | `users` table |
| Booking history, admin decisions | Personal data (links people to activity) | `bookings`, `audit_entries` |

## Rules and policies that apply
University data policy: applies (stated by the team). India's DPDP Act:
applicability not yet confirmed; the team will confirm with the department
(D-002 in `docs/DECISIONS.md`). This is not legal advice.

## Trust boundaries
TB-1 browser to server; TB-2 app to database; TB-3 database host; TB-4 app to
mail relay (see the data-flow diagram in `docs/ARCHITECTURE.md`).

## STRIDE threat walkthrough
STRIDE is a checklist of six ways software gets attacked: Spoofing, Tampering,
Repudiation, Information disclosure, Denial of service, Elevation of privilege.

| ID | Component / boundary | Category | Threat | Mitigation | Status | Verified by |
|---|---|---|---|---|---|---|
| T-001 | Login [TB-1] | Spoofing | Credential stuffing against student accounts | Lockout after five failures (FR-002), argon2id hashes (NFR-002), rate limit | Planned | test: tests/test_auth.py::test_lockout_after_five_failures |
| T-002 | Session cookie [TB-1] | Spoofing | Session theft or fixation | HttpOnly, Secure, SameSite cookies; new session ID at login | Planned | manual: inspect cookie flags in browser dev tools after Phase 2 |
| T-003 | Booking API [TB-1] | Tampering | Client sets another user as booking owner | Owner always taken from the session, body field ignored | Planned | test: tests/test_booking.py::test_owner_from_session_only |
| T-004 | Decision endpoint [TB-1] | Elevation of privilege | Student calls the approve endpoint | Role check on every route, deny by default | Mitigated | test: tests/test_authz.py::test_student_cannot_decide |
| T-005 | Booking read [TB-1] | Information disclosure | Student reads another's booking by guessing an ID | Owner filter on the server (FR-006) | Mitigated | test: tests/test_authz.py::test_booking_read_is_owner_only |
| T-006 | Audit log | Repudiation | Admin denies having approved a booking | Append-only audit entry with admin ID and time (FR-005) | Planned | test: tests/test_audit.py::test_decision_creates_audit_entry |
| T-007 | Database access [TB-2] | Information disclosure | SQL injection through search or booking fields | Parameterised queries via the ORM, no string-built SQL | Planned | scan: bandit in CI plus manual: injection payloads against every text field |
| T-008 | Login and booking endpoints [TB-1] | Denial of service | Request flood exhausts the VM | Per-IP and per-account rate limits returning 429 | Planned | test: tests/test_ratelimit.py::test_429_after_limit |
| T-009 | Notification email [TB-4] | Information disclosure | Email body reveals another student's details | Decide what the email may contain; send minimal text | Open | |
| T-010 | Dependencies | Tampering | Hallucinated or malicious package installed | Dependency check below; pinned lockfile | Planned | scan: pip-audit in CI plus manual: dependency table reviewed each phase |
| T-011 | Database backups [TB-3] | Information disclosure | Unencrypted backup exposes student data | Accepted by the lab manager: backups stay on the university-managed VM in v1; revisit before multi-lab rollout | Accepted risk | n/a (accepted risk, reason in Mitigation) |

## Auth and authorization approach
Email and password behind one auth module (ADR-002). Two roles: student and
admin. Every route declares its required role; the default is deny.

## Secrets and configuration
Database URL, mail credentials, and the session signing key come from
environment variables on the VM; none are committed.

## Dependency check
Procedure: take names from official documentation, look each package up on
PyPI (first-published date, releases, maintainers), confirm the linked
repository matches and is active, compare against well-known names, pin
versions and commit the lockfile, then run `pip-audit`. Existence alone is not
enough because attackers register names that AI tools tend to invent.

| Package | Purpose | Exists and spelled right | Maintained | Verified by |
|---|---|---|---|---|
| fastapi | Web framework | Name taken from official docs | Active releases | manual: PyPI page and repository reviewed (illustrative entry) |
| argon2-cffi | Password hashing | Name taken from official docs | Active releases | manual: PyPI page and repository reviewed (illustrative entry) |

## Logging and audit
Log request IDs, user IDs, and decisions. Never log passwords, session
cookies, or full emails in error messages.

## Residual risk
After mitigations, the main remaining risks are local password storage (until
SSO) and the accepted backup risk (T-011). The project supervisor and lab
manager are informed.
