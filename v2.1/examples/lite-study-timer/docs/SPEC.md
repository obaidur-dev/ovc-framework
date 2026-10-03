# SPEC: Study Timer

*Track: Lite. Source of truth: `docs/project-brief.md`.*

**Why this page exists:** it is the contract between you and the AI. It says
what to build and how you will check each part works. Without the last
column, "done" only means "the AI stopped typing".

## What we are building
A one-page web timer for students. It counts down 25 minutes of focus, then a
5-minute break, beeps when each ends, and shows how many focus blocks you
finished today (kept after a reload). You can type what you are studying and
it shows next to the timer.

## Requirements
Each row says what the app must do and how you will check it.

| ID | The app must... | How we will check it |
|---|---|---|
| FR-001 | Count down 25:00 to 00:00 when you press Start, and let you press Pause. | test: tests/timer.test.js::counts_down_from_25_minutes, then manual: press Start and Pause in a browser |
| FR-002 | Switch to a 5-minute break automatically when focus reaches 00:00, and back to focus when the break ends. | test: tests/timer.test.js::switches_phase_at_zero |
| FR-003 | Play a short beep when a block ends, with a Mute button that silences it. | manual: open the page with ?debug=5, hear the beep after 5 seconds; press Mute, repeat, hear nothing |
| FR-004 | Show today's completed focus blocks and keep the number after reloading the page. | test: tests/store.test.js::count_survives_reload, then manual: finish a ?debug=5 block, reload, count still shows 1 |
| FR-005 | Show the typed study label next to the timer as plain text. | test: tests/label.test.js::label_is_shown_as_text_not_html |
| NFR-001 | Stay accurate to within 1 second over 25 minutes, even in a background tab. | test: tests/timer.test.js::remaining_time_follows_the_clock |
| NFR-002 | Work in the latest Chrome and Firefox. | manual: run the FR-001 to FR-004 checks in both browsers |
| NFR-003 | Keep the whole page (HTML and scripts) at 50 KB or less, with no dependencies. | scan: total bytes of index.html and src/*.js |

(Checks start with `test:` for automated checks, `scan:` for a tool or command
result, or `manual:` for steps you do by hand.)

## Not included in v1
- Logins and syncing between devices: no accounts keeps v1 small and private.
- Weekly statistics and custom durations: nice later, not needed to start.

## Build steps
1. Timer logic as a plain function that works from the clock, plus unit tests. Done when: the tests pass (covers FR-001, FR-002, NFR-001).
2. Page layout and controls. Done when: Start, Pause, and the display work by hand (covers FR-001, NFR-002).
3. Beep and Mute. Done when: you hear it in the debug URL (covers FR-003).
4. Save today's count and the label in the browser. Done when: reload keeps the count and the label shows safely (covers FR-004, FR-005).
5. Run the security checklist, the cross-browser check, and the size check. Done when: every box is ticked with evidence (covers NFR-002, NFR-003).
6. Handover: write `docs/GUIDE.md` with the `ovc-explain` skill and run its checker. Done when: the guide passes and you can answer its questions.

## Security
See `docs/SECURITY.md`: a 10-line checklist. Tick items only with evidence.

## Understanding what you built
The final build step produces `docs/GUIDE.md` with the `ovc-explain` skill: a
guide to what exists, what each part does, and what is and is not proven.

## Decisions
Big choices and changes are logged in `docs/DECISIONS.md`.

## Open questions
None.

## Words used
- **v1**: the smallest useful version.
- **Requirement**: something the app must do, written so you can check it.
- **Test**: a check that can be repeated. Automated tests run by a command;
  manual checks are steps you follow.
