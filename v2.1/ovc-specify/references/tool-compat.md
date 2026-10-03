# Tool compatibility (the only file with tool-specific facts)

**last verified: 2026-10-01**

Everything below was checked against the tool's own documentation on that
date, except where marked `UNVERIFIED`. Tools change; if you can search the
web, re-check the source for the tool the person named before relying on a
detail. Never invent tool behaviour: if a tool is not listed here, say you
have not verified it and ask the person which instruction file it reads.

## How to use this file

1. Ask the person **once**: "Which AI coding tool will build this?" (skip if
   the brief's Constraints already say).
2. Look the tool up in the table below.
3. Create a pointer file **only** for that tool, and only if the table says one
   is needed. If it is not needed, create nothing extra and tell the person
   why. Never create pointer files for tools the person did not name.
4. If several tools were named, handle each in turn.

## Instruction files: does the tool read AGENTS.md?

| Tool | Reads `AGENTS.md`? | Pointer file to create | Source |
|---|---|---|---|
| Claude Code | Yes on v2.1.277+, **but only when no `CLAUDE.md` exists** in the working directory or any parent (`CLAUDE.md`, `.claude/CLAUDE.md`, and `CLAUDE.local.md` all count). If both files exist and `CLAUDE.md` does not import `AGENTS.md`, `AGENTS.md` is ignored. Older versions, and some sessions before v2.1.281 (for example Amazon Bedrock or telemetry disabled), read `CLAUDE.md` only. | `CLAUDE.md` whose **first line** is `@AGENTS.md` (an import). Works on old and new versions; keeping the import never loads `AGENTS.md` twice. | code.claude.com/docs/en/memory |
| Gemini CLI | **Not by default.** Default context file is `GEMINI.md`. It can be set to read `AGENTS.md` through `context.fileName` in `settings.json` (user: `~/.gemini/settings.json`; project: `.gemini/settings.json`), for example `{"context": {"fileName": ["AGENTS.md", "GEMINI.md"]}}`. `GEMINI.md` supports `@file.md` imports with relative paths. | `GEMINI.md` containing `@./AGENTS.md` (needs no settings change). Alternative: the settings entry above, if the person prefers no extra file. | geminicli.com/docs/cli/gemini-md |
| OpenAI Codex (CLI, IDE, app) | Yes. Per directory it checks `AGENTS.override.md`, then `AGENTS.md`. Combined size is capped (default 32 KiB), so keep the file short. | None | developers.openai.com/codex/guides/agents-md |
| Cursor | Yes. A root `AGENTS.md` is picked up automatically. It also reads `CLAUDE.md`. Nested-file behaviour: see Cursor docs (not re-checked). | None | cursor.com/help/customization/rules |
| GitHub Copilot | Yes. Coding agent, VS Code agent modes, and Copilot CLI read `AGENTS.md`; they also read `.github/copilot-instructions.md`, `CLAUDE.md`, and `GEMINI.md`. | None | docs.github.com (repository custom instructions) |
| OpenCode | Yes. Reads project `AGENTS.md`; falls back to `CLAUDE.md` **only if no `AGENTS.md` exists**. If both exist, only `AGENTS.md` is used. | None | opencode.ai/docs/rules |
| Windsurf, Aider, Cline, Roo Code, Zed, Kiro, Amp, JetBrains AI, Antigravity, others | `UNVERIFIED` (not checked against primary docs) | None created. Ask the person which file their tool reads, and tell them it is unverified. | n/a |

**Why the Claude Code and OpenCode rows matter together.** The two tools
resolve "both files exist" in opposite ways (Claude Code prefers `CLAUDE.md`;
OpenCode prefers `AGENTS.md`). A `CLAUDE.md` containing only `@AGENTS.md` is
correct for both, so it is safe to create for a Claude Code user even if the
person also uses other tools.

### Exact pointer file contents

`CLAUDE.md` (Claude Code):
```
@AGENTS.md
```
Claude-specific instructions, if the person wants any, go **below** that
line. Do not copy `AGENTS.md` content into it.

`GEMINI.md` (Gemini CLI):
```
@./AGENTS.md
```

## Skill install locations (where the OVC skills go)

The Agent Skills format (a folder with `SKILL.md`) is an open standard used by
all tools below. Copy or symlink the **folders** `ovc-discover/`,
`ovc-specify/`, and `ovc-explain/` into one of these. Restart the tool if a new skill does not
appear.

| Tool | Project (this repo only) | Personal (all repos) | Source |
|---|---|---|---|
| Claude Code | `.claude/skills/<name>/` | `~/.claude/skills/<name>/` | code.claude.com/docs/en/skills |
| OpenAI Codex | `.agents/skills/<name>/` (scans from the working directory up to the repo root) | `$HOME/.agents/skills/<name>/` | developers.openai.com/codex/skills |
| Cursor | `.agents/skills/` (also reads `.claude/skills/`, `.codex/skills/`) | `~/.agents/skills/` (also `~/.claude/skills/`, `~/.codex/skills/`) | cursor.com/docs/skills |
| GitHub Copilot | `.github/skills/`, `.claude/skills/`, or `.agents/skills/` | `~/.copilot/skills/` or `~/.agents/skills/` (VS Code docs also list `~/.claude/skills/`) | docs.github.com (Copilot agent skills); code.visualstudio.com |
| Gemini CLI | `.gemini/skills/` or the alias `.agents/skills/` | `~/.gemini/skills/` or the alias `~/.agents/skills/`; also `gemini skills install <url>` | geminicli.com/docs/cli/using-agent-skills |
| OpenCode | `.opencode/skills/`, `.claude/skills/`, or `.agents/skills/` | `~/.config/opencode/skills/`, `~/.claude/skills/`, or `~/.agents/skills/` | opencode.ai/docs/skills |
| Claude.ai web or desktop (skill upload) | `UNVERIFIED` here | `UNVERIFIED` here | check Anthropic's Help Center |
| Any other tool | `UNVERIFIED` | `UNVERIFIED` | If it supports the Agent Skills standard, `.agents/skills/` is the most widely shared path; otherwise paste the `SKILL.md` contents into the session. |

Practical note: `.agents/skills/` is read by Codex, Cursor, Copilot, Gemini
CLI, and OpenCode per their docs, but Claude Code's documentation lists only
`.claude/skills/`. For a team using both, keep one copy and symlink it into the
other path (on Windows, copy instead of symlinking).

## Behaviours that affect how these skills are written

- **Codex may shorten skill descriptions** when many skills are installed,
  to fit a budget. The OVC descriptions therefore put the main trigger phrases
  first.
- **Running `scripts/check_specs.py`** needs a tool that can run shell
  commands and Python 3. If the tool cannot, perform the same checks by hand
  using the list in `ovc-specify/SKILL.md` Step 7.
- **Clearing context.** Command names for clearing or compacting a
  conversation differ by tool and are `UNVERIFIED` here. Starting a new
  session always works.

## How to refresh this file

For each tool, re-read the source named in the table, update the rows and the
`last verified` date at the top, and mark anything you could not confirm
`UNVERIFIED`. Do not copy tool facts into any other file in these skills.
