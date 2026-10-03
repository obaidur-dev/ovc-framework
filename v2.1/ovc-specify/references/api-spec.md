# API_SPEC.md template (only if the project exposes an API)

Load this only if there is a service boundary (frontend to backend, third
parties, or between the project's own services). A project with none does not
need it. Write it after DATA_MODEL.md.

```markdown
# API Spec: <Project Name>

## Conventions
Base URL and versioning, auth method, request/response format, error format:
everything that applies to every endpoint so it is not repeated.

## Endpoints
| Method | Path | Purpose | Auth / role | Satisfies |
|---|---|---|---|---|
| POST | /api/v1/bookings | Create a booking | student | FR-003 |

For each endpoint worth detail: request shape, response shape, and the error
cases worth calling out (validation failure, not found, forbidden, conflict).

## Rate limiting and abuse handling
What limits exist and what happens when they are hit. Required if the API is
reachable from the internet; it is also the mitigation for several
denial-of-service rows in SECURITY.md.
```

Notes:
- The "Satisfies" column links endpoints to requirement IDs so the build plan
  can trace them.
- Every endpoint needs an explicit auth rule, even if it is "public". A
  missing rule is a gap in the threat model.
