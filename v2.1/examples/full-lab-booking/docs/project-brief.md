---
ovc-brief-version: 2
track: full
level: intermediate
project: Lab Booking
---

# Project Brief: Lab Booking

## Problem
Students book shared lab instruments (microscopes, 3D printers) through a
paper sheet and WhatsApp. Double bookings are common, nobody can prove who
approved what, and the lab manager spends hours reconciling requests.

## Users
**Students** request bookings and see their own. **Lab admins** (two staff)
approve or reject requests and manage instruments. Conflict: students want
instant confirmation; admins want control over scarce instruments.

## Scope
**In scope (v1):** login, instrument list, booking requests, double-booking
prevention, admin approve/reject with an audit trail, email notification.
**Explicitly out of scope (for now):** payments, mobile app, calendar sync,
multi-lab support. Deferred because the pilot is one lab.

## Success looks like
During a four-week pilot with one lab: zero double bookings, 90% of requests
decided within one working day, and the lab manager reports no manual
reconciliation. A reviewer can trace each requirement to a passing test.

## Constraints
Python and PostgreSQL (department standard). Hosted on a university VM. Team
of two final-year students, twelve weeks. Capstone assessment requires a
threat model with evidence and requirement-to-test traceability. Built with
Claude Code.

## Performance & efficiency goals
Booking list answers in under 500 ms at the 95th percentile with 100
concurrent users (the pilot lab has about 60 students). Login and booking pages
meet WCAG 2.2 AA. No other targets for v1.

## Key decisions (with reasoning)
- Technology: Python with FastAPI, PostgreSQL, server-rendered pages.
  Why: department standard, the team knows Python, the work is database-bound so
  language speed is not the bottleneck, and type hints plus a type checker give
  quick feedback on AI-written code.
  Main alternative: TypeScript full-stack (rejected: team has not used it).
  Revisit if: profiling shows request handling, not the database, is the limit.
- PostgreSQL over SQLite: concurrent bookings need a database-level guarantee
  against overlaps (see ADR-001).
- Local email and password login in v1: university single sign-on needs IT
  approval that will not arrive within the timeline (see ADR-002).

## Builder & learning goals
Both team members must be able to explain and defend every design decision to
the supervisor, and extend the system next term. Wants full depth: architecture,
trade-offs, and the evidence behind each security claim.

## Security & privacy concerns already raised
Holds student names, university emails, and booking history (personal data).
Passwords are stored. Admin actions must be attributable. Rules asked: the
team said the university's data policy applies and that India's DPDP Act may
apply; the team was told this is not legal advice and will confirm with the
department. Status of confirmation: not yet confirmed.

## Assumptions & risks
**Assumptions:** the university VM allows outbound email; two admins is
enough; slots are whole-hour blocks.
**Risks:** admins forget to decide requests (mitigation: reminder email,
out of v1 scope); SSO later forces an auth migration (mitigation: isolate
auth behind one module).

## Open questions
None that block the spec. Follow-up (tracked in `docs/DECISIONS.md` as D-002): the
team will confirm with the department whether the DPDP Act applies.

## Raw notes
"No more WhatsApp screenshots as proof."
