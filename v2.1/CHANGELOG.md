# Changelog

All notable changes to the OVC Framework. Format follows
[Keep a Changelog](https://keepachangelog.com); versions follow semver.

## [2.1.1]

### Fixed (research claims; see `EVIDENCE.md`)
Every figure was re-read in its primary source and corrected to match its scope.
- **94% type errors:** the figure is real (Mündler et al., Section 1; it is not in
  the abstract) but it comes from six open-weight models writing small TypeScript
  functions, and counts compile errors only. The wording now says so.
- **Quiz gap:** was written "about 17% lower". The study reports 50% vs 67%, which
  is **17 percentage points** (about a quarter lower in relative terms), with
  n = 52. Corrected everywhere, with the study's limits.
- **AI code speed:** the 3.12x figure is for **GPT-4** on LeetCode-style problems
  (worst case 13.89x), not for "AI code". Removed the claim that newer models have
  narrowed the gap, which could not be re-verified.
- **Language speed:** the original energy study's ratios are accurate, but a
  follow-up found language has no significant energy effect beyond execution
  time. The guide now relies on the time ratios, as an order of magnitude.
- **Language accuracy ranking:** removed the claim that cited MultiPL-E, McEval,
  and PROBE results, which could not be re-checked. The only language-gap
  evidence now used is what the type-constrained paper itself reports.
- **Veracode 2026:** "about 44%" was my arithmetic from the stated 56% average
  pass rate; it is now labelled as derived.
- **Package hallucination:** scope added (16 models, Python and JavaScript, "at
  least").

### Added
- `EVIDENCE.md`: a claim register with exact wording, location, scope, and
  verification status for every number used.
- Regression tests that fail if a figure appears without its scope (for example
  "94%" without "open-weight", or "17% lower" without "percentage points").

## [2.1.0]

### Added
- **Levels: beginner, intermediate, expert.** Chosen in the same first question
  as the size and stored as `level:` in the brief header. Level controls how
  much is explained, how many questions are asked per batch, whether the agent
  recommends or the person decides, and how deep the final guide goes. It is
  independent of the track (project size).
- **Stack advisor** (`ovc-discover/references/stack-guide.md`): separates "fast
  on the CPU", "fewest AI mistakes", and "something I can read"; sourced
  evidence with its limits; default stacks by project type; "boring technology"
  rules. Plus `concept-cards.md` for beginners.
- **Performance** (`ovc-specify/references/performance.md`): turn "fast" into
  numbers, starting budgets, what AI-written code tends to get wrong, a
  measure-first process, an escalation ladder, and quality guardrails. The
  brief gains a "Performance & efficiency goals" section.
- **AI reliability** (`ai-reliability.md`): feedback loop, small phases,
  three-strikes rule, level-specific `AGENTS.md` rules.
- **`ovc-explain`, a third skill:** writes `docs/GUIDE.md` from the real code:
  file tour, flows traced to line numbers, requirement coverage with honest
  statuses, measured performance, security status, concepts, limits, safe-change
  recipes, and check-yourself questions. Includes an interactive tour and quiz.
- **`check_guide.py`:** verifies the guide against the project (paths and
  `file:line` references exist, cited tests exist, every requirement covered,
  `Done` has evidence, performance numbers have evidence or say `Not measured`,
  the security section cannot hide open items).
- The brief gains "Builder & learning goals".
- `check_specs.py` now enforces a **handover step** (the plan and `AGENTS.md`
  must require `docs/GUIDE.md`), validates `level`, and warns when no
  non-functional requirement has a number.
- A real, tested Lite example app (13 passing tests) with a complete guide.
- Evals 4 (beginner stack advice) and 5 (explain what was built).

### Changed
- "Lite coaching" is now "beginner coaching": the explain-as-you-go behaviour
  follows the person's level, not the project size.
- `AGENTS.md` template adds Type check, Versions, Feedback loop, a level rule,
  and a final-task Definition-of-done item.
- Brief format remains `ovc-brief-version: 2`. Revision 2.1 is **additive**:
  briefs without `level` or the two new sections remain valid.

### Fixed
- Discovered while building the Lite example: ES-module pages cannot be opened
  by double-clicking the file, so run instructions now use a local server.

## [2.0.0]

### Breaking
- Brief format version 2 with a machine-readable header (`ovc-brief-version`,
  `track`, `project`) and the sections "Success looks like" and
  "Assumptions & risks". `ovc-specify` rejects unknown versions and offers to
  upgrade v1 briefs.
- `CLAUDE.md` is no longer always generated; a pointer file is created only for
  the tool the person names and only if that tool needs one.

### Added
- Tracks (Lite, Standard, Full); verification chain (requirement IDs,
  traceability, threat IDs, typed evidence, four-status key);
  `scripts/check_specs.py`; brownfield mode; `docs/DECISIONS.md`; security
  content (sourced AI-code risk evidence, dependency check, AI-feature rows,
  compliance question); `AGENTS.md` Definition of done; handoff options;
  negative triggers; README, MIT licence, examples, evals, tests.

### Changed
- Tool-neutral wording; one shared brief template; one reference file per
  document; all tool facts in `tool-compat.md` with a "last verified" date.
  Corrected the v1 claim that Claude Code does not read `AGENTS.md`.

### Migrating from v1
1. Re-run `ovc-discover`, or ask `ovc-specify` to upgrade your v1 brief.
2. Keep an old `CLAUDE.md` only if you use that tool, with first line
   `@AGENTS.md`.
3. Re-run `ovc-specify` for requirement IDs, traceability, and evidence.
