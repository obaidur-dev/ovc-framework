# OVC Framework

**Obaidur's Verified Coding Framework** — two Claude skills that turn a raw
idea into a build-ready spec set, in two deliberately separate passes:
discovery, then generation.

```
raw idea ──▶ ovc-discover ──▶ project-brief.md ──▶ (new chat) ──▶ ovc-specify ──▶ full spec set ──▶ coding agent
             (conversation)      (single file)                     (generation)      (PRD, architecture,
                                                                                       security, build plan…)
```

## Why two skills instead of one

A long discovery conversation and a long document-generation pass have
different failure modes, and cramming both into one chat lets the first
one's noise degrade the second one's quality. So the framework splits them:

- **`ovc-discover`** — has a short, adaptive conversation with you about a
  raw idea and distills it into one clean `<project>-brief.md` file. Ends
  with a hard gate: it shows you the draft and won't finalize anything
  until you confirm it's accurate.
- **`ovc-specify`** — run in a **fresh chat**, with no memory of the
  discovery conversation. It treats the brief as the only source of truth,
  and generates the full spec set a coding agent needs to actually build
  the thing: `PRD.md`, `ARCHITECTURE.md`, `SECURITY.md` (a full STRIDE
  threat model, generated for every project regardless of size),
  `BUILD_PLAN.md`, plus `DATA_MODEL.md` and `API_SPEC.md` when the project
  actually needs them. It never guesses at something the brief doesn't
  answer — it flags it as an open question instead and asks you directly.

Both skills also always generate `AGENTS.md` (the open, cross-tool
standard for giving a coding agent project context) and a short `CLAUDE.md`
stub pointing to it — because Claude Code currently reads `CLAUDE.md`
automatically but doesn't yet auto-read `AGENTS.md` the way some other
tools do, so the stub keeps that handoff from silently falling through.

## What's in this repo

```
ovc-framework/
├── README.md
├── ovc-discover/
│   ├── SKILL.md                    # discovery conversation logic
│   └── references/
│       └── ovc-templates.md        # canonical doc templates (shared)
├── ovc-specify/
│   ├── SKILL.md                    # spec-generation logic
│   └── references/
│       └── ovc-templates.md        # same file, kept identical
├── ovc-discover.skill               # packaged, ready to upload
└── ovc-specify.skill                # packaged, ready to upload
```

The two `references/ovc-templates.md` files are intentionally identical —
they're the single canonical source for every document shape in the
framework (the brief, the PRD, the STRIDE table, etc.), duplicated into
both skills so a brief `ovc-discover` produces always matches what
`ovc-specify` expects. If you ever edit one, copy the change into the
other so they don't drift apart.

## Is this Claude Code-only, Claude.ai-only, or does it work in other AI tools?

Both skills are built in the **Agent Skills format** — a `SKILL.md` file
with YAML frontmatter, no Claude-specific tool calls hardcoded into the
instructions. That format is Anthropic's, but it's increasingly being
treated as a de facto open standard (see
[agentskills.io](https://agentskills.io)) that other coding agents are
adopting too.

- **Claude.ai (web, desktop, mobile chat) and Claude Code** — both work
  natively, no changes needed. This is what the two skills were written
  and actually tested against, and the rest of this README assumes one of
  these two.
- **Other SKILL.md-compatible agents** (OpenAI Codex CLI, Gemini CLI,
  Cursor, and a growing list of others) — likely to work, since the
  `SKILL.md` files are plain instructions Claude follows, not Claude-only
  code. But each tool has its own way of *finding* skills — Codex CLI
  looks under `.agents/skills`, Gemini CLI wraps them as "extensions" via
  a `gemini-extension.json`, Cursor uses a plugin manifest — so you may
  need to add that tool's small manifest file alongside `SKILL.md`, or
  place the unzipped folder wherever that tool expects skills to live.
  We've only built and tested these against Claude, so treat other agents
  as "should work in principle," not verified.
- **Non-agentic tools** (plain ChatGPT web chat, a raw API call with no
  skills support) — won't auto-load these, but nothing stops you from just
  pasting a `SKILL.md`'s instructions into a prompt by hand; you'd lose
  the automatic triggering and the shared-template consistency, but the
  underlying instructions and templates in `references/ovc-templates.md`
  are just plain markdown and work as a manual guide too.

## Installing

Each `.skill` file is a self-contained zip archive — pick whichever of
these matches how you use Claude.

### Claude.ai (web, desktop, or mobile)

Skills work on Free, Pro, Max, Team, and Enterprise plans and just need
code execution enabled first.

1. **Settings → Capabilities** — turn on *Code execution and file
   creation* if it isn't already on. (Team/Enterprise: an org owner
   enables this in *Organization settings → Skills* first.)
2. **Customize → Skills → Upload a skill.**
3. Upload `ovc-discover.skill`, then repeat for `ovc-specify.skill`.
4. Make sure both are toggled on.

### Claude Code

Custom skills there are just files on disk — no upload step:

```bash
mkdir -p ~/.claude/skills
unzip ovc-discover.skill -d ~/.claude/skills/ovc-discover
unzip ovc-specify.skill -d ~/.claude/skills/ovc-specify
```

Use `.claude/skills/` (project-local, no `~`) instead if you want either
skill scoped to one repo rather than available everywhere.

## Using it

1. Open a chat and describe your idea — as little as one sentence, or as
   much as a full notes dump — and ask Claude to use `ovc-discover` (or
   just mention "OVC" / "project brief"; the description is written to
   trigger on its own for this kind of request).
2. Answer whatever it asks. It adapts to how much you've already given it
   — a detailed dump gets fewer questions than a one-liner.
3. Review the brief it drafts. Ask for changes if anything's off — it
   won't finalize the file until you confirm it.
4. Start a **new chat**, hand it the `<project>-brief.md` file, and ask
   Claude to use `ovc-specify`.
5. It generates the spec set, flags anything the brief left unclear as an
   open question, and asks you those directly before wrapping up.
6. Point your coding agent at the project root (`AGENTS.md` / `CLAUDE.md`)
   and start building. Treat the docs as living — update them as real
   decisions change mid-build instead of letting them go stale.

## Customizing

Both skills' behavior lives entirely in their `SKILL.md` files, and every
document shape lives in `references/ovc-templates.md`. To add a section to
every future PRD, for instance, edit the PRD template in
`ovc-templates.md` in *both* skill folders and repackage.

## License

Add whatever license you'd like this repo distributed under before
publishing — none is specified yet.
