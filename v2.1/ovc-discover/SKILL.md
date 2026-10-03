---
name: ovc-discover
description: Turns a raw or half-formed idea for a NEW app, tool, or product into a structured project-brief.md through a short guided interview, before any spec or code exists. Works for beginners (explains concepts, recommends a fast and AI-reliable tech stack) through experts (terse, you decide). Use when someone says "I have an idea for an app", "help me plan what to build", "which language should I use", "write a project brief", pastes messy notes to organize, or mentions OVC or the discovery phase. First asks the level (beginner, intermediate, expert) and size (lite, standard, full). Do NOT use for tiny one-off scripts, bug fixes, refactors, code review, or questions about an existing codebase. The brief feeds the ovc-specify skill. Part 1 of 3 of the OVC Framework (Obaidur's Verified Coding Framework).
license: MIT
metadata:
  version: "2.1.1"
  framework: "OVC (Obaidur's Verified Coding Framework)"
  part: "1 of 3"
---

# OVC Discover (part 1 of 3)

The OVC flow has three parts: **discover** (this skill: idea to brief),
**specify** (brief to verified spec set), **explain** (finished build to a
guide the builder can actually understand). This skill turns a rough idea into
one file, `project-brief.md`, through a short conversation.

**Why separate skills?** A long discovery conversation fills the session with
false starts and superseded ideas. If specs are generated in that same
context, they can quietly lean on the noise instead of on what the person
agreed to. Ending discovery with one short, human-approved file means the next
step starts from a clean source of truth.

## Step 0 - Is this the right skill?

Use it for a **new project** with several features, or one that touches user
accounts, stored data, payments, uploads, or an AI model.

Do not use it (just help directly, saying why in one sentence) for:

- a tiny one-off script: one file, no stored data, nobody but the author uses it
- a bug fix, refactor, or one feature inside an existing codebase
- a question about how existing code works

If the person has an **existing repository** and wants docs, a security review,
or an `AGENTS.md` for it, point them to `ovc-specify` (brownfield mode). If they
want an existing or finished project *explained*, point them to `ovc-explain`.

If unsure whether the idea is tiny, ask once: "Will anyone besides you use it,
or will it store any data?" If both answers are no and it is one file, build it
directly. If they still want a brief, offer Lite.

## Step 1 - Ask level and size (always the first question)

Skip any part the person already stated. Otherwise ask this as **one**
question, answerable in one reply (or "you pick"):

> Two quick choices:
>
> **How much guidance do you want?**
> 1. **Beginner**: I'm new to building software. Explain things as we go,
>    recommend what to use, keep choices simple.
> 2. **Intermediate**: I've built a few things. Give me options with
>    trade-offs and your recommendation.
> 3. **Expert**: I know what I want. Be brief, follow my decisions, flag only
>    real gaps.
>
> **How big is the project?**
> A. **Lite**: small or learning project. Brief, one-page spec, short security
>    checklist.
> B. **Standard**: a real app (logins, data, maybe a team). Full spec set.
> C. **Full**: capstone or high-rigor work. Standard plus formal requirements,
>    decision records, data-flow diagram, full threat model, traceability.

Save them as `level:` and `track:` in the brief header. They are independent:
an expert may want Lite; a beginner may be doing a Full capstone.

**If they say "you pick":**
- Level: use `intermediate`. If they ask what a term means twice, say you will
  switch to beginner mode and do so.
- Size: first project, one person, no logins or private data -> Lite. Logins,
  stored personal data, payments, or more than one developer -> Standard.
  Capstone, thesis, graded design review, or regulated data -> Full.

Either can change later; update the header if it does.

### What each level changes

| | Beginner | Intermediate | Expert |
|---|---|---|---|
| Questions per batch | at most 3 | at most 4 | at most 4, only real gaps |
| Jargon | defined on first use (see `references/concept-cards.md`) | only unusual terms | none defined |
| Decisions | you recommend one default plus one alternative, with reasons | 2-3 options with trade-offs and your pick | they decide; you flag a concern once, with evidence |
| Unknown answers | "I'll pick a sensible default and tell you why" | record as assumption or open question | record as open question |
| "Why this step" notes | yes, one line per step | no | no |
| Technology step | full stack advice | trade-off summary | only if asked |

Never lecture an expert. Never leave a beginner to decide something they have
no way to judge: recommend, explain, and let them say yes.

## Step 2 - Read the input, then interview only the gaps

Take whatever they gave you: one line, a wall of notes, an uploaded document.
Work out what is already known before asking anything.

- **Detailed input:** draft as much of the brief as you can first, then ask only
  about fields you cannot fill.
- **One sentence:** start with the problem and who it is for.
- **In between:** the test is "can I draft something the person will recognise
  as accurate?", not "did I ask everything?".

Ask in **batches** (sizes in the table above), never a long form.

| Topic | Ask (all) | Add for Standard | Add for Full |
|---|---|---|---|
| Problem and users | What is the problem, and for whom? | User types and where needs conflict | Stakeholders; who approves the result |
| Scope | Smallest useful v1? What is NOT in v1? | Integrations; migrations | Out-of-scope list with reasons |
| Success | How will you know it worked? (one observable outcome) | Numbers where possible | Evidence a reviewer will expect |
| Constraints | Fixed requirements, deadline, who builds, **which AI coding tool will build it** | Platform, budget, team skills | Availability, scale, accessibility |
| Assumptions and risks | What are you assuming? What could go wrong? | A mitigation per risk | Owner and fallback per risk |

Accept "I don't know". Record it as an assumption or open question rather than
pressing.

## Step 3 - Choose the technology (skip if fixed, or for experts)

If a course, employer, or existing codebase fixes the technology, record it
under Constraints and move on. Otherwise read `references/stack-guide.md` and
follow its decision procedure and the level rules above.

The recommendation must weigh three things: what runs fast enough, what an AI
coding agent gets wrong least often (mainstream, typed, fast feedback), and
what **this person can read and debug**. Record the choice in "Key decisions"
using the template at the end of the guide, including the main alternative and
when to revisit.

When a beginner meets an unfamiliar word, give the matching card from
`references/concept-cards.md`, one at a time.

## Step 4 - Performance goals and learning goals (two short questions)

**Performance.** "How fast should it feel?"
- Beginner: offer three plain choices: (a) just works, no special speed need;
  (b) feels instant for me and a few users; (c) must handle many people at
  once. Turn the answer into numbers using the defaults in the stack guide
  (for a website: LCP 2.5 s or less, INP 200 ms or less, CLS 0.1 or less) and
  label them "defaults".
- Intermediate: ask for targets or propose them.
- Expert: ask for their budget only if not already stated.
Write the result under "Performance & efficiency goals".

**Learning.** "By the end, which sounds most like you? (a) I just want it to
work and to know how to run it; (b) I want to understand it well enough to fix
small things; (c) I want to understand every part and be able to explain it;
(d) I'll maintain and extend it." Write the answer under "Builder & learning
goals". It decides how deep the final guide goes. Experts: skip unless unclear.

## Step 5 - Raise security early; ask about rules, do not assume

If the idea involves accounts, passwords, payments, uploads, anyone's personal
data, children, health data, or a feature that calls an AI model, capture it
now, briefly. You are not threat-modelling here; you are making sure it is not
forgotten.

Ask once: "Does this need to follow any law or policy, for example GDPR,
India's DPDP Act, or your university's or employer's rules? Tell me which, or
'none', or 'not sure'." Do not guess the answer. Record it, including "not
sure".

If nothing sensitive applies, write that and why. Never leave the section blank.

## Step 6 - Stop interviewing and draft

Do not chase 100% certainty. Once you have problem, users, a scope line, a
success outcome, the constraints that matter, a technology choice (or the
reason none was needed), and the two goals above, write the draft. Put anything
still unclear in "Open questions". If you notice you are asking nice-to-know
questions, that is the cue to draft.

Read `references/brief-template.md` before drafting. Its shape is fixed and
shared with the other skills; do not improvise sections. Header example:

```
---
ovc-brief-version: 2
track: lite
level: beginner
project: My Project
---
```

## Step 7 - The hard gate: show it before you save it

Show the **whole** draft in the conversation and ask directly: "Here is the
brief. Does it capture your idea, or is something off?"

- If they want changes, make them and show the revised version again.
- Write the file only after they confirm.
- If they say "looks good" without reading closely, that is their call. Your
  job is to make sure an accurate version was shown.

## Step 8 - Save the file

Save as `project-brief.md` in the working folder (or where they ask). If one
already exists, ask before overwriting. If your environment cannot write files,
output the complete markdown in one clearly delimited block.

Do not delete sections that do not apply; write "Not applicable: <reason>".

## Step 9 - Hand off (give options; do not just refuse)

Tell the person the brief is done and name the ways forward:

1. **New session (recommended).** Start a fresh session and run `ovc-specify`
   with `project-brief.md`. Cleanest context.
2. **Clear the context.** If the tool can clear or compact the conversation,
   use it, then run `ovc-specify`.
3. **Continue here.** Allowed if they accept the trade-off: this session still
   holds discovery noise, so `ovc-specify` must read `project-brief.md` from
   disk and treat only that file as true.

Explain *why* the file is the single source of truth: if something matters and
is not in the brief, the next step cannot know about it.

Also tell them the third step exists: **after the project is built, run
`ovc-explain`** to get a guide to what was actually built.

Do not write PRD, architecture, security, or build-plan documents inside this
skill. If they choose option 3, hand over to `ovc-specify`.

## Beginner coaching (level: beginner)

Open each step with a one-line "Why this step" note, using these:

| Step | Why this step |
|---|---|
| Level and size | A weekend project and a capstone need different amounts of paperwork, and people need different amounts of explanation. |
| Questions | The AI builds what you describe. A vague idea in gives a vague app out. |
| Technology | The language you pick changes how fast it runs and how often the AI makes mistakes. |
| Security | Mistakes found now cost minutes. Found after launch they cost trust. |
| Show the draft | This file is all the next step will read. If it is wrong here, everything built on it is wrong. |
| Save | A file survives; a conversation does not. |

Plain words for common terms:

| Term | Plain meaning |
|---|---|
| v1 / MVP | The smallest version that is actually useful. |
| Scope | What the project includes, and just as important, what it does not. |
| Constraint | A fixed limit: deadline, tools, budget, rules. |
| Assumption | Something you are treating as true but have not checked. |
| Success criterion | A way to tell, from outside, that it worked. |
