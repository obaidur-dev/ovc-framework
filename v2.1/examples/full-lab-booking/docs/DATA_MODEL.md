# Data Model: Lab Booking

## Entities
| Entity | Field | Type | Constraints | Sensitive? |
|---|---|---|---|---|
| User | id | uuid | primary key | No |
| User | email | text | unique, required | Yes (personal data) |
| User | password_hash | text | required, argon2id | Yes (credential) |
| User | role | text | student or admin | No |
| Instrument | id, name, available | | name unique | No |
| Booking | id, user_id, instrument_id | | foreign keys | No |
| Booking | period | time range | exclusion constraint with instrument_id (ADR-001) | No |
| Booking | status | text | pending, approved, rejected | No |
| AuditEntry | id, booking_id, admin_id, decision, decided_at | | append-only | Yes (links an admin to a student) |

## Relationships
A user has many bookings; an instrument has many bookings; a booking has zero
or more audit entries.

## Data lifecycle
Bookings are kept for one academic year, then deleted. Audit entries are kept
as long as their booking. A student can ask for deletion of their account;
their bookings are anonymised. Satisfies FR-005 and the university data policy.
Whether the DPDP Act applies is not yet confirmed (see SECURITY.md).

## Sensitive fields
email, password_hash, and audit entries; see SECURITY.md data classification.
