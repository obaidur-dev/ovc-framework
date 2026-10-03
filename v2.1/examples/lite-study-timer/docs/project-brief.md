---
ovc-brief-version: 2
track: lite
level: beginner
project: Study Timer
---

# Project Brief: Study Timer

## Problem
I lose focus when I study for long stretches. I want a simple timer that
alternates 25-minute focus blocks with 5-minute breaks and shows how many
focus blocks I finished today, so I can see my progress.

## Users
Me, and one friend. Both are students using a laptop browser. No admin or
second user type.

## Scope
**In scope (v1):** 25-minute focus countdown, automatic 5-minute break, a beep
when a block ends (with a mute button), a count of completed focus blocks for
today that survives a page reload, and an optional "what I'm studying" label
shown next to the timer.
**Explicitly out of scope (for now):** logins or accounts, syncing between
devices, statistics over weeks, custom durations. Deferred to keep v1 small.

## Success looks like
I use it on at least five study days in a row. The timer is accurate to
within a second over 25 minutes, and my session count is still correct after
I close and reopen the tab.

## Constraints
Plain HTML, CSS, and JavaScript only (what the course teaches). No build
tools. Free hosting (GitHub Pages). Built with Codex. Needs to finish in
about two weekends.

## Performance & efficiency goals
Defaults chosen for a tiny static page (the person had no specific need): the
whole page stays under 50 KB with no dependencies, and the countdown stays
accurate to within 1 second over 25 minutes even when the tab is in the
background.

## Key decisions (with reasoning)
- No framework: the course only covers plain JS, and the app is one page.
- Technology: plain HTML, CSS, and JavaScript modules; tests with the
  runtime's built-in test runner.
  Why: the course requires plain JS, and the page is tiny, so any framework
  would add more download and more for the AI to get wrong.
  Main alternative: TypeScript (rejected for now: not taught yet, adds a build
  step). Revisit if the project grows past a few files.
- Store the session count in the browser (localStorage): there are no
  accounts, so there is nowhere else to store it and no need for one.

## Builder & learning goals
Option (c): I want to understand every part and be able to explain it to my
friend. I will maintain it myself.

## Security & privacy concerns already raised
No accounts, no personal data sent anywhere. The only stored data is a number
and a free-text label in the user's own browser. The label is typed by the
user and displayed on the page, so it must be displayed safely. Rules or
policies: none that I know of; the person answered "none".

## Assumptions & risks
**Assumptions:** the friend uses a recent Chrome or Firefox; browsers keep
timers running well enough in a background tab (not yet checked).
**Risks:** browsers slow down timers in background tabs, so the countdown
could drift. Mitigation: compute remaining time from the clock, not from
counting ticks.

## Open questions
None.

## Raw notes
"pomodoro thing for studying", "little beep when time is up", friend wants it
too.
