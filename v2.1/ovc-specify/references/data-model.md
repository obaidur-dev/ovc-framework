# DATA_MODEL.md template (only if the project persists data)

Load this only if the project stores data. A stateless tool, pure CLI
transformer, or static site does not need it: say so and skip it. Write it
after ARCHITECTURE.md and before SECURITY.md (which cross-references it).

```markdown
# Data Model: <Project Name>

## Entities
| Entity | Field | Type | Constraints | Sensitive? |
|---|---|---|---|---|
| User | email | text | unique, required | Yes (personal data) |

## Relationships
One-to-many, many-to-many, etc., with a simple diagram if not obvious.

## Data lifecycle
What is created, updated, archived, or deleted, and when. Include retention
and deletion rules (user-requested account deletion, expiring records) and
which requirement IDs they satisfy.

## Sensitive fields
Cross-reference SECURITY.md's data classification: which fields need
encryption, masking, or restricted access.
```

Notes:
- "Sensitive?" feeds the data classification in SECURITY.md. Any column marked
  Yes needs a matching row or note there.
- If a law or policy was named for this project, state which fields it covers
  and what it requires for deletion or export. If it was never answered, add
  an open-question marker; do not assume.
