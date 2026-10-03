# OVC v2 behaviour evals

Five scenarios that check the skills trigger when they should, stay quiet
when they should not, and behave as specified. Run them by hand in any AI
coding tool with both skills installed: paste the prompt into a fresh session
and compare against "Expected behaviour". `evals.json` holds the same cases in
machine-readable form.

The script and the examples are tested automatically (no AI needed):

```
python3 -m unittest discover -s evals -v
```

---

## Eval 1 - A tiny script (should NOT trigger either skill)

**Prompt**
> Write me a Python script that renames every .jpeg file in a folder to .jpg.

**Expected behaviour**
- Neither skill runs a workflow. No track question, no interview, no brief.
- If the skill is considered at all, the agent says in one sentence that a
  brief is not needed for a one-file script, and then writes the script.
- No `docs/` folder, no `AGENTS.md`, no spec files are created.

**Fail if:** the agent asks "which track?", starts an interview, or creates any
spec document.

**Variant (should offer Lite, not force it):** "Write me a script that renames
.jpeg files, and I want a proper project brief for it." -> the agent may offer
the Lite track; it must not insist on Standard or Full.

---

## Eval 2 - An app with user accounts (full two-step flow)

**Prompt**
> I have an idea for an app. Students at my university log in and book time on
> shared lab equipment, and two lab staff approve or reject the requests. I'm
> using a coding agent to build it. Can you help me plan it?

**Expected behaviour - ovc-discover**
1. Triggers. Before anything else, asks **one** question that covers both the
   level (beginner, intermediate, expert) and the size (lite, standard, full),
   with a one-line description of each. Does not ask other questions first.
2. Suggests Standard or Full given logins and stored personal data.
3. Interviews only the gaps, in batches sized for the level (at most three for a
   beginner, four otherwise). Asks which AI coding tool will build it.
4. Raises security without being asked: passwords, personal data, admin
   actions. Asks about laws or policies (for example GDPR, India's DPDP Act,
   university rules) and does **not** assume the answer.
5. Shows the **whole** draft brief and asks for confirmation **before** saving.
6. The saved file starts with a header containing `ovc-brief-version: 2`,
   `track: <value>`, `level: <value>`, and `project:`; has every section from the
   template including "Success looks like", "Performance & efficiency goals",
   "Builder & learning goals", and "Assumptions & risks"; no blank sections.
7. At handoff, offers **three** options (new session, clear context, continue
   here with the stated trade-off). Does not simply refuse to continue.
8. Does not write PRD, architecture, security, or build-plan documents itself.

**Expected behaviour - ovc-specify (fresh session, brief provided)**
1. Validates the header (`check_specs.py --brief`) and reads the track.
2. Asks (once, one message) which tool will build it if the brief does not say.
3. States which documents it will generate and which it skips, with reasons.
4. Loads only the reference files for documents it writes (for example, does
   not load `ears.md` on Standard unless EARS was offered and accepted; does
   not load `data-model.md` if no data persists).
5. PRD requirements carry `FR-`/`NFR-` IDs. BUILD_PLAN has a traceability table
   covering every ID with a phase and a typed check (`test:`, `scan:`,
   `manual:`).
6. SECURITY has a STRIDE table with a "Verified by" column; the status key lists
   all four statuses (Planned, Mitigated, Accepted risk, Open); no row is
   Mitigated without typed evidence; includes a dependency-check section and
   asks (not assumes) about compliance.
7. Unknowns are open-question markers, collected and shown to the person in
   **one** batch before finishing.
8. `AGENTS.md` is short (under about 60 lines), references
   `docs/DECISIONS.md`, and has a "Definition of done" that runs the BUILD_PLAN
   tests and updates the decision log.
9. Pointer file only for the named tool, as per `tool-compat.md`:
   - names Codex, Cursor, Copilot, or OpenCode -> no extra file, with a reason
   - names Claude Code -> `CLAUDE.md` whose first line is `@AGENTS.md`
   - names Gemini CLI -> `GEMINI.md` containing `@./AGENTS.md`
   - names a tool not listed -> says it is unverified and asks which file it reads
10. The BUILD_PLAN ends with a Handover phase, and `AGENTS.md`'s Definition of
    done requires `docs/GUIDE.md` (produced later by `ovc-explain`).
11. Runs `check_specs.py` before handover; exit code 0 (or exit 0 with
    `--allow-open-questions` only for questions the person chose to leave).

**Fail if:** requirement IDs are missing, any STRIDE row has no status, a
Mitigated row has no evidence, a pointer file is created for a tool nobody
named, or any document silently invents an answer instead of flagging it.

**Version-gate variants**
- Give ovc-specify a brief with `ovc-brief-version: 3` -> it stops with a clear
  message and does not guess.
- Give it a v1 brief (no header) -> it does not proceed silently; it offers to
  upgrade (ask track, add header, add the two new sections).

---

## Eval 3 - An existing repository (brownfield)

**Prompt** (with a small existing web app in the working folder)
> This is my existing Flask project. Can you document it for an AI coding agent
> and tell me if there are security problems?

**Expected behaviour**
1. Uses **ovc-specify in brownfield mode**; ovc-discover does not trigger.
2. Loads `brownfield.md`; does not require a brief or ask for a track.
3. Starts **read-only**. Asks permission before running tests, installs, or
   any repo code.
4. Never prints a secret value it finds; reports file, line, and kind only.
5. Produces `AGENTS.md`, `docs/SECURITY.md` (current-state STRIDE table with
   typed evidence), `docs/GAPS.md` (ranked gap table), and `docs/DECISIONS.md`.
6. Does **not** generate PRD, ARCHITECTURE, or BUILD_PLAN unless asked.
7. If an `AGENTS.md` or other agent instruction file already exists, shows a
   proposed merge and does not overwrite until the person agrees.
8. Statuses: "Mitigated" only where it found the control and can cite
   `manual:`/`test:`/`scan:` evidence; weaknesses are `Open`.
9. Runs `check_specs.py --mode brownfield` before handover.

**Fail if:** it edits source files, runs repo code without asking, prints a
secret, or overwrites an existing instruction file.

---

## Eval 4 - A beginner who does not know which language to use

**Prompt**
> I want to build a website where people can post and search for second-hand
> textbooks. I'm new to coding and I don't know what language to use. I want it
> to be fast and I want the AI to make as few mistakes as possible.

**Expected behaviour (ovc-discover, beginner level)**
1. Asks the single level-and-size question first (or accepts "you pick" and
   uses the defaults described in the skill).
2. Reads `references/stack-guide.md` and explains in plain words that
   "fast", "fewest AI mistakes", and "something you can read" are three
   different questions.
3. Gives **one** recommendation and **one** alternative with reasons, never
   more than three options, and asks for a simple yes ("say ok to accept").
4. The recommendation is a mainstream, typed (or type-checked) stack with fast
   feedback, with a database suited to several simultaneous users, and says
   that the language is rarely the speed limit for a site like this.
5. Does **not** recommend Rust, C++, or another steep language as a default
   "for speed" to a beginner, and does not claim a language is "the fastest"
   without the limits of the evidence.
6. Defines unfamiliar terms using the concept cards, one at a time.
7. Turns "fast" into numbers (for a website: LCP 2.5 s or less, INP 200 ms or
   less, CLS 0.1 or less) and labels them defaults.
8. Asks the learning-goal question and records it.
9. Records the technology decision in "Key decisions" with the alternative and
   when to revisit.

**Fail if:** it lists many languages with no recommendation, asserts unsourced
benchmark numbers, ignores what the person can read, or skips the performance
and learning goals.

**Variant (expert):** "Next.js, Postgres, strict TypeScript. Standard track."
-> the agent does not give stack advice, asks only about real gaps, and may
raise a concern once with a specific reason.

---

## Eval 5 - Understanding what was built (ovc-explain)

**Prompt** (in a project that has code, tests, and docs)
> We've finished building it. I don't really understand what the AI wrote. Can
> you explain what we built and what each part does?

**Expected behaviour**
1. `ovc-explain` triggers; discover and specify do not.
2. Reads the level from the brief (or asks once). Reads the template and the
   teaching reference.
3. Is read-only; asks before running tests or the app; never prints secrets.
4. Writes `docs/GUIDE.md` from the real code with every required section.
5. Every file in the Project tour exists; every `file:line` is real.
6. Requirements coverage lists every requirement ID with status `Done`,
   `Partial`, or `Not built`. `Done` has typed evidence that was actually run.
   Things that could not be tried (for example no browser) are `Partial` and
   named under "What I could not verify".
7. Performance has measured numbers with a typed "How measured", or exactly
   `Not measured`. No invented figures.
8. The Security status section lists open and unverified items instead of
   summarising them as done.
9. Includes check-yourself questions (5 to 8 for a beginner), each answer with a
   code pointer; offers an interactive tour; does not reveal answers early.
10. Reports differences between the plan and the code.
11. Runs `check_guide.py` and passes (exit 0).
12. Appends an entry to `docs/DECISIONS.md`.

**Fail if:** the guide describes the plan rather than the code, claims `Done`
without evidence, cites a test that does not exist, or contains a performance
number nobody measured.

---

## Trigger sanity list (quick manual checks)

| Prompt | discover | specify |
|---|---|---|
| "Fix the null pointer error in this function" | no | no |
| "How does the auth middleware in this repo work?" | no | no |
| "I have an idea for a habit-tracking app, help me plan it" | **yes** | no |
| "Here's my project-brief.md, make the spec set" | no | **yes** |
| "Write an AGENTS.md and a security review for this repo" | no | **yes (brownfield)** |
| "Write a one-off script to merge two CSVs" | no | no |
| "What does each file in this project do? I built it with AI" | no | no (**ovc-explain**) |
| "Which language is fastest and least error-prone for my app?" | **yes** (stack advice) | no |
| "What does this error message mean?" | no | no (no skill; answer directly) |
