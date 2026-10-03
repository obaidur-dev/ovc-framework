# ADR-002: Local password login in v1, SSO later

- Status: Accepted
- Date: project start
- Requirements affected: FR-001, FR-002, NFR-002

## Context
University single sign-on would remove password storage, but needs IT approval
that will not arrive within the twelve-week timeline.

## Decision
Implement email and password login behind a single auth module, with lockout
and argon2id hashing. Keep the module interface small so SSO can replace it.

## Alternatives considered
- Wait for SSO: blocks the pilot.
- Third-party login provider: adds an external dependency and data flow.

## Consequences
The team owns password-storage risk (threats T-001, T-002) until SSO exists.
A later migration touches one module.
