# Performance: fast without losing quality

Load this when writing the PRD (or SPEC) non-functional requirements and the
BUILD_PLAN on Standard and Full, and on Lite when the brief's "Performance &
efficiency goals" holds a real target. It turns a vague wish ("make it fast")
into numbers, checks, and habits.

Sources last verified: 2026-10-02 (the studies behind these rules, with their
scope, are in the stack guide in `ovc-discover` and in `EVIDENCE.md` at the
repository root).

## The one rule

**Make it correct and tested first. Measure. Fix the biggest bottleneck.
Measure again.** Never optimise without a baseline number, and never trade away
tests, security, or readability for a speed-up you did not measure.

Why: AI-written code is often correct but naive. In one 2024 benchmark
(EffiBench, 1,000 LeetCode-style problems), code from GPT-4 averaged 3.12 times
the execution time of the best human solutions, with a worst case of 13.89
times; an earlier version of that paper reported 1.69 times for GPT-4-turbo.
Those are small puzzles and 2024-era models, so they say nothing exact about
your app or about today's models. That is the point: **measure**.

## Step 1: turn the goal into numbers

Start from the brief's "Performance & efficiency goals". If the person gave
none, use these **starting budgets** (judgment, adjust to the project; say they
are defaults):

| Project type | Starting targets | How to check |
|---|---|---|
| Website or web app (in the browser) | At the 75th percentile of real visits: largest content visible in 2.5 s or less (LCP), interactions respond in 200 ms or less (INP), layout shift 0.1 or less (CLS). These are the published "good" thresholds. Keep total download small: set a page-weight budget (for example 1 MB for a simple page) | `scan:` Lighthouse or PageSpeed run on a throttled mobile profile; real-user data once live |
| API or backend service | 95th-percentile response under 300 to 500 ms for simple reads, at the stated number of concurrent users | `scan:` load test (for example k6, wrk, or Locust) with the user count and result recorded |
| Command-line tool | Starts in under 1 s; finishes the typical job within the time the person names | `test:` timing test, or `manual:` stopwatch on a standard input |
| Batch or data job | A throughput target (rows per second) or a deadline for the usual input size | `scan:` timed run on a realistic file |
| Mobile app | Cold start and screen transitions feel immediate on a low-end device the person names | `manual:` on that device; platform profiler for numbers |

Write each as an NFR with a measurable target (`prd.md`, NFR table), and a
typed check in the build plan traceability table. A target without a way to
check it is a wish.

## Step 2: build the simple correct version first

Tell the AI coding agent (in `AGENTS.md`): write the simplest correct solution
with a test, then stop. Optimise only against a measured budget miss.

## Step 3: what AI-written code tends to get wrong (review for these)

These cause most real slowness. Look for them in every review and profile:

| Pattern | Why it is slow | Fix |
|---|---|---|
| Loop that runs a database query per item ("N+1") | One query becomes hundreds | Fetch in one query or batch |
| Loading a whole table or file into memory | Memory and time grow with data | Pagination, limits, streaming |
| Missing database index on a searched or joined column | Every lookup scans everything | Add the index; check with the database's `EXPLAIN` |
| Nested loops over big lists, or searching a list repeatedly | Work grows with the square of the size | Use a dictionary/set/map for lookups |
| Waiting on input/output one item at a time | Idle CPU, slow total | Run independent I/O concurrently with the language's async tools, with a bound |
| Polling in a tight loop or short timer | Wakes the CPU constantly and burns battery | Events, callbacks, or timers with backoff |
| Recomputing the same thing | Wasted work | Compute once; cache with a clear way to expire it |
| Building strings or arrays by repeated copying | Hidden quadratic cost | Use the language's builder/join/append-in-place idiom |
| Pure-language loops over large numeric data | Interpreted loops are slow | Use vectorised libraries so the work runs in compiled code |
| Pattern matching (regular expressions) on untrusted input with nested repeats | Can freeze the server, also a security risk | Simplify the pattern; cap input length |
| No limits on concurrency, request size, or retries | Overload and runaway cost | Set explicit bounds |

Web-specific quick wins: serve images at the size shown and in a modern
format; defer or lazy-load what is off-screen; ship less JavaScript; set
caching headers; compress text responses; reserve space for images and ads to
avoid layout shift; avoid re-rendering large lists.

## Step 4: add performance to the build plan

- Each phase that adds user-facing work gets a budget check in its
  Verification block, using the typed checks above.
- Add a final **performance pass** (before the handover phase): record
  baseline numbers, profile (browser performance panel, the language's
  profiler, or the database's `EXPLAIN`), fix the single biggest cost, measure
  again, repeat while a target is still missed.
- Log each before/after pair in `docs/DECISIONS.md` ("report query: 2.4 s ->
  0.3 s after adding index on bookings.instrument_id"). Those numbers also feed
  the project guide's Performance table.

## Step 5: if a hot spot stays slow (escalation ladder)

Try in this order, stopping at the first that meets the target:
1. A better algorithm or data structure.
2. Less work: caching, batching, limiting the data.
3. A library whose core runs in compiled code.
4. Move only the measured hot path to a faster language.
5. Rewrite the whole system (almost never justified).

A language change is step 4 or 5, not step 1. The studies behind the stack
guide show compiled languages are far faster on heavy computation, but most
apps never reach that wall.

## Quality guardrails for every optimisation

- All tests still pass. Add a test for the behaviour you touched.
- The change is explained in one line in `docs/DECISIONS.md` with before/after
  numbers.
- Readability: prefer the clear version unless the measured gain is needed to
  meet a stated target.
- Security rows in `docs/SECURITY.md` are not weakened (for example caching must
  not leak one user's data to another).
