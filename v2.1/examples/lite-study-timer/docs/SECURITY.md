# SECURITY: Study Timer (Lite checklist)

*Track: Lite. State after the build. Tick a box only when you can point to evidence.*

**Why this page exists:** AI tools write working code fast, and independent
benchmarks keep finding known security weaknesses in a large share of what
they write unless someone checks. This is the "someone checks" step, shrunk
to ten lines.

**Data this project touches:** a number (today's completed blocks) and a
short typed label, both stored only in the user's own browser. Nothing
sensitive.
**Rules or policies that apply:** none (the person said "none").

Words used: a **secret** is anything that proves who you are to a service (API
key, password, token). **Validate** means checking input is what you expect
before using it.

- [x] 1. No secrets in code or git: keys live in environment variables; `.env` is in `.gitignore`. - verified by scan: grep for api key, secret, password, token in src/, index.html, package.json found no matches
- [x] 2. All user input (forms, URLs, files) is validated, and anything shown back on a page is escaped. - verified by test: tests/label.test.js::label_is_shown_as_text_not_html and tests/timer.test.js::debug_value_must_be_a_small_whole_number
- [x] 3. Database queries use parameters; no string-joined SQL. - N/A: there is no database
- [x] 4. Passwords (if any) are hashed with a standard library such as bcrypt or argon2, never stored as plain text. - N/A: there are no accounts or passwords
- [x] 5. Users can only see and change their own data, and the server checks it. - N/A: no server and no shared data; each browser holds only its own
- [x] 6. Every package was checked before install: it exists, is maintained, and the name is spelled exactly right. - verified by manual: package.json has no dependencies and no node_modules folder exists; nothing was installed
- [x] 7. Error messages shown to users do not reveal stack traces, file paths, or secrets. - verified by manual: the page has no error screen; storage and audio failures are caught silently (src/store.js, src/app.js:22)
- [ ] 8. Anything reachable beyond your own laptop uses HTTPS. (Not done: the app is not published yet. Tick after deploying to GitHub Pages and confirming the padlock.)
- [x] 9. File uploads (if any) are limited by size and type, and uploaded files are never executed. - N/A: there are no uploads
- [x] 10. One scanner or audit tool was run and its result read (for example `npm audit` or a linter's security rules). - verified by scan: node --check passed on every file; a grep for innerHTML, eval, and document.write matched only a comment at src/label.js:2
