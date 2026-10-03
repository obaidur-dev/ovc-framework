# EARS: requirement wording (required on Full, optional on Standard)

EARS means *Easy Approach to Requirements Syntax*. It gives each requirement
one of a few fixed shapes, so a vague sentence ("handle errors well") becomes
something a person or an AI agent cannot misread. Every EARS requirement uses
the word **SHALL**.

## The patterns

| Pattern | Template | Example |
|---|---|---|
| Ubiquitous (always true) | `THE <system> SHALL <response>` | THE system SHALL store passwords only as salted hashes. |
| Event-driven | `WHEN <trigger>, THE <system> SHALL <response>` | WHEN a student submits a booking, THE system SHALL reject it if the slot is already taken. |
| State-driven | `WHILE <state>, THE <system> SHALL <response>` | WHILE an upload is in progress, THE system SHALL disable the submit button. |
| Unwanted behaviour | `IF <condition>, THEN THE <system> SHALL <response>` | IF a file exceeds 10 MB, THEN THE system SHALL reject it with a clear error. |
| Optional feature | `WHERE <feature is included>, THE <system> SHALL <response>` | WHERE two-factor login is enabled, THE system SHALL require a second factor. |

Complex requirements combine patterns, for example
`WHILE <state>, WHEN <trigger>, THE <system> SHALL <response>`.

## Writing rules

1. One requirement, one `SHALL`, one testable outcome.
2. Name the system or component as the subject; do not use "it".
3. Replace vague words ("fast", "secure", "user-friendly") with a measurable
   target or a concrete behaviour.
4. Unwanted-behaviour (`IF ... THEN`) requirements are where most security and
   error handling lives. Write at least one per trust boundary.
5. Keep the ID first in the row: `| FR-004 | WHEN ..., THE system SHALL ... |`.
   The checker treats a Full-track requirement without `SHALL` as a failure.

## Converting plain language

Plain: "Users should not be able to book the same lab slot twice."
EARS: `WHEN a user submits a booking for a slot that already has an approved booking, THE system SHALL reject the request and show the existing booking's time range.`
Check: `test: tests/test_booking.py::test_double_booking_rejected`

## Offering EARS on Standard

Show the person two of their own requirements in plain language and in EARS
side by side. Say what the extra rigor buys (an AI agent cannot misread it;
each line maps to one test) and what it costs (more words per line). Let them
choose all, some, or none.
