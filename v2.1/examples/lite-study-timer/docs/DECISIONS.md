# Decision log

Append-only. Newest at the bottom. Never edit past entries.

## D-001 - Lite track, plain JavaScript, no framework (project start)
- Decision: build as a single static page in plain HTML, CSS, and JavaScript; keep state in the browser.
- Why: the course only covers plain JS; there are no accounts, so no server is needed.
- Alternatives: React (rejected: not taught, adds a build step); a small backend (rejected: no data worth storing centrally).
- Affects: FR-004, SECURITY items 3, 4, 5
- Docs updated: yes
- Supersedes: none

## D-002 - Compute time from the clock, not by counting ticks (build, step 1)
- Decision: remaining time is always `endsAt - now`; the 250 ms interval only redraws.
- Why: browsers slow timers in background tabs; counting ticks would drift (the risk in the brief).
- Alternatives: count one second per tick (rejected: drifts when the tab sleeps).
- Affects: NFR-001, src/timer.js
- Docs updated: yes
- Supersedes: none

## D-003 - Serve over a local web server, not by opening the file (build, step 2)
- Decision: run the page with `python3 -m http.server`; the run instructions say so.
- Why: browsers block JavaScript modules on pages opened as local files.
- Alternatives: bundle everything into one script (rejected: adds a build step).
- Affects: AGENTS.md Commands, docs/GUIDE.md How to run
- Docs updated: yes
- Supersedes: none

## D-004 - Handover guide produced (build, step 6)
- Decision: wrote docs/GUIDE.md from the code with ovc-explain.
- Why: the plan's final step; the builder wanted to understand every part.
- Differences found between plan and code: the day count keeps running across midnight if the page stays open (not in the spec; listed under Limits in the guide).
- Affects: docs/GUIDE.md
- Docs updated: yes
- Supersedes: none
