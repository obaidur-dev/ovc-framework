# API Spec: Lab Booking

## Conventions
Base path `/api/v1`. Session cookie authentication. JSON bodies. Errors are
`{"error": "<code>", "detail": "<message>"}` with no stack traces.

## Endpoints
| Method | Path | Purpose | Auth / role | Satisfies |
|---|---|---|---|---|
| POST | /api/v1/login | Start a session | public | FR-001, FR-002 |
| GET | /api/v1/bookings | List own bookings (admins: all) | student or admin | FR-001, FR-006, NFR-001 |
| POST | /api/v1/bookings | Request a booking | student | FR-003, FR-004 |
| POST | /api/v1/bookings/{id}/decision | Approve or reject | admin | FR-005 |

## Rate limiting and abuse handling
Per-IP and per-account limits on `/login` and `POST /bookings`; exceeding
returns 429 with a retry hint.
