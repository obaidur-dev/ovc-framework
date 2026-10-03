# Product Requirements: Lab Booking

*Source of truth: `docs/project-brief.md`. Requirements use EARS wording.*

## Overview
A web app that replaces paper and WhatsApp booking of shared lab instruments:
students request slots, the system prevents overlaps, and admins decide with
a permanent record.

## Users and use cases
- As a student, I want to request an instrument slot, so that I know it is mine once approved.
- As a lab admin, I want to approve or reject requests, so that scarce instruments are used fairly and the decision is on record.

## Functional requirements
| ID | Requirement | Priority | Acceptance check | Source |
|---|---|---|---|---|
| FR-001 | WHEN a visitor submits a valid email and password, THE system SHALL start a session and show that user's bookings. | Must | A seeded user logs in and sees their list | Brief: Scope |
| FR-002 | IF five consecutive login attempts for one account fail within 10 minutes, THEN THE system SHALL refuse further logins for that account for 15 minutes. | Must | Sixth attempt is refused even with the right password | Brief: Security |
| FR-003 | WHEN a student submits a booking for a free slot of an available instrument, THE system SHALL create the booking with status pending. | Must | Booking appears as pending | Brief: Scope |
| FR-004 | IF a booking request overlaps an existing pending or approved booking for the same instrument, THEN THE system SHALL reject it and show the conflicting time range. | Must | Overlapping request returns a conflict | Brief: Success |
| FR-005 | WHEN a lab admin approves or rejects a pending booking, THE system SHALL record the decision, the admin, and the time, and email the student. | Must | Audit row exists; email sent | Brief: Problem |
| FR-006 | THE system SHALL show a booking only to its owner and to lab admins. | Must | Another student gets 403/404 | Brief: Security |

## Non-functional requirements
| ID | Requirement | Target / how measured |
|---|---|---|
| NFR-001 | THE system SHALL return a booking list in under 500 ms at the 95th percentile with 100 concurrent users. | Load test, p95 |
| NFR-002 | THE system SHALL store passwords only as salted argon2id hashes. | Code review plus test inspecting stored values |
| NFR-003 | THE system SHALL meet WCAG 2.2 level AA on the login and booking pages. | Automated accessibility scan plus keyboard walkthrough |

## Out of scope
Payments, mobile app, calendar sync, multi-lab support.

## Success criteria
Zero double bookings in a four-week pilot; 90% of requests decided within one
working day; every requirement traced to a passing test.

## Stakeholders and approval
Lab manager (accepts the pilot), project supervisor (assesses traceability and
the threat model).

## Open questions
None.
