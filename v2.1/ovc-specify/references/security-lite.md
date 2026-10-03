# SECURITY.md template (Lite track: 10-line checklist)

Load this only on the Lite track. Standard and Full use `security.md`
instead. Never skip security on Lite: tiny projects are exactly where nobody
stops to look.

## Why this document exists (say this to the person)

"AI tools write working code very quickly, and independent tests keep finding
that a large share of what they write has known security weaknesses unless
someone checks. This checklist is that 'someone checks' step, shrunk to ten
lines you can do in an afternoon."

Optionally add one line of evidence: in Veracode's 2025 benchmark of 80 coding
tasks across 100+ models, the model chose the insecure way to complete the code
in 45% of cases, and its 2026 report puts the average security pass rate at
56%. Say it is a benchmark of controlled tasks, not a prediction for this
project. Details and sources: `security.md`.

## How to fill it in

- Keep **exactly the ten items** below, in this order. For an item that does
  not apply, keep the line and write `N/A: <reason>`; do not delete it.
- At spec time nothing is built yet, so every applicable item starts as
  `- [ ]` (not done). The builder ticks `- [x]` **only** with evidence:
  `verified by test: ...`, `verified by scan: ...`, or `verified by manual: ...`.
- Add a short "Data this project touches" line above the list (even if it is
  "nothing sensitive: <why>").
- If the project calls an AI model, add a **conditional line 11** (see below).
- If the person named a law or policy (asked in the brief), add a line
  stating it, or `Not sure yet` as an open question.

## Template

```markdown
# SECURITY: <Project Name> (Lite checklist)

*Track: Lite. Tick a box only when you can point to evidence.*

**Data this project touches:** <what, and how sensitive; or "nothing
sensitive: <why>">
**Rules or policies that apply:** <named by the person, "none", or "not sure
yet">

Words used: a **secret** is anything that proves who you are to a service (API
key, password, token). **Validate** means checking input is what you expect
before using it.

- [ ] 1. No secrets in code or git: keys live in environment variables; `.env` is in `.gitignore`.
- [ ] 2. All user input (forms, URLs, files) is validated, and anything shown back on a page is escaped.
- [ ] 3. Database queries use parameters; no string-joined SQL.
- [ ] 4. Passwords (if any) are hashed with a standard library such as bcrypt or argon2, never stored as plain text.
- [ ] 5. Users can only see and change their own data, and the server checks it (hiding a button is not a check).
- [ ] 6. Every package was checked before install: it exists, is maintained, and the name is spelled exactly right (AI tools sometimes invent or misspell package names).
- [ ] 7. Error messages shown to users do not reveal stack traces, file paths, or secrets.
- [ ] 8. Anything reachable beyond your own laptop uses HTTPS.
- [ ] 9. File uploads (if any) are limited by size and type, and uploaded files are never executed.
- [ ] 10. One scanner or audit tool was run and its result read (for example `npm audit`, `pip-audit`, or a linter's security rules).
```

Example ticked line with evidence:
`- [x] 3. Database queries use parameters - verified by manual: searched code for string-built SQL, none found`
Example not applicable:
`- [x] 4. Passwords hashed - N/A: this project has no accounts`

## Conditional line 11 (only if the project calls an AI model)

```markdown
- [ ] 11. Text from users or the web is treated as untrusted when sent to the model (it can contain instructions, called prompt injection); model output is checked before it is shown, stored, or acted on; API keys stay on the server.
```

## Dependency check (what item 6 means in practice)

Before installing any package an AI suggested:
1. Spell it from the package's official page, not from the chat.
2. Look it up on the registry (npm or PyPI page). Does it exist? When was it
   first published? Is there a recent release?
3. Does the linked repository exist, match the name, and look alive?
4. Is the name one letter away from a famous package? If yes, stop and ask.
Existence alone is not enough: attackers register the names AI tools tend to
invent. Log each new package in `docs/DECISIONS.md`.
