# ADR-001: PostgreSQL with an exclusion constraint for overlaps

- Status: Accepted
- Date: project start
- Requirements affected: FR-003, FR-004, NFR-001

## Context
Two students can submit overlapping requests within the same second. Checking
for overlaps in application code leaves a race window.

## Decision
Use PostgreSQL and a database exclusion constraint on (instrument, time range)
for pending and approved bookings, so the database refuses overlaps itself.

## Alternatives considered
- Application-level check only: simple, but has a race condition.
- SQLite with locking: no equivalent constraint; single-writer limits.

## Consequences
Overlap prevention is guaranteed even under concurrency. The team must learn
one PostgreSQL feature and run PostgreSQL on the VM.
