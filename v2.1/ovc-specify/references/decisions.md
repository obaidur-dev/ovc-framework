# docs/DECISIONS.md template (all tracks)

Load this when creating `docs/DECISIONS.md`. It is an **append-only decision
log**. Its job is to make keeping docs current cheap: instead of rewriting the
PRD every time something shifts, add a two-minute entry saying what changed
and which docs it touches.

## Rules

- **Append only.** Never edit or delete a past entry. If a decision is
  reversed, add a new entry that says "Supersedes D-003".
- Newest entry at the bottom; IDs `D-001`, `D-002`, ... in order.
- Log: a dependency added, a requirement added or changed, a security
  mitigation designed or redesigned, a stack or architecture choice, a
  decision to accept a risk, anything that makes another doc wrong.
- Do not log routine code changes.
- Each entry names the docs it affects. If those docs were not updated in the
  same piece of work, say so; that is a debt to repay.
- ADRs (Full track) record decisions made **before** building. This log
  records decisions and changes made **while** building. Do not duplicate:
  link to the ADR if one exists.

## Template

```markdown
# Decision log

Append-only. Newest at the bottom. Never edit past entries.

## D-001 - <short title> (<date>)
- Decision: <what was decided>
- Why: <the reasoning, one or two lines>
- Alternatives: <what else was considered, or "none">
- Affects: <FR-/NFR-/T- IDs and docs>
- Docs updated: yes | no (<which are still stale>)
- Supersedes: <D-00N or none>
```

Seed the file with one entry `D-001` recording the track chosen and the main
stack decision from the brief, so the log is never empty.
