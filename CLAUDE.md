# citadel — operator instructions

**Scope**: only for sessions whose cwd is `citadel`. A realm session sees this file because citadel
is attached with `--add-dir`; in that case ignore it and follow `core/KINGDOM.md`.

citadel is the control room of the Zig kingdom. The shared brain is `core/KINGDOM.md`, reached
by every realm session through the symlink `/Users/fn/codespace/CLAUDE.md`; shared rules are
`core/rules/` via `/Users/fn/codespace/.claude/rules`. This file is only for sessions whose cwd
is citadel (the daily `citadel-cycle` job and interactive operator work).

## Layout

```
core/KINGDOM.md          the core consciousness (loads everywhere)
core/CONTRACT.md         system-prompt hard rules (appended to every realm session)
core/rules/*.md          kingdom rules; tiger-style.md and zig-0.16.md are path-scoped to Zig
core/fleet-settings.json permissions + hooks for realm sessions (rendered per realm)
protocol/                CYCLE.md · GITHUB.md · DOCS.md · VERSIONING.md
.claude/agents/          planner · architect · zig-developer · test-writer · code-reviewer ·
                         tidy-auditor · migrator · git-manager · ci-cd · kingdom-architect
.claude/skills/          cycle · inbox · plan · implement · stabilize · review · release ·
                         report · migrate-zig · status · integrate · new-realm
realms/<repo>/           REALM.md · STATE.md · memory/ · settings.json · auto-memory/
workflows/               jobs.toml · prompts/ · system/ (source of truth for the cron server)
scripts/kingdom          launcher: kingdom cycle|shell|argv <realm>
scripts/jobs.py          render · export · plan · apply (cron server)
scripts/scaffold.py      new component repo from specs/ + templates/
docs/KINGDOM.md          map · docs/ROADMAP.md cross-repo order
```

## How a realm session is launched

```
cd /Users/fn/codespace/<realm>
claude -p "/cycle <realm>" --add-dir /Users/fn/codespace/citadel \
  --settings citadel/realms/<realm>/settings.json --strict-mcp-config \
  --append-system-prompt-file citadel/realms/<realm>/system.md \
  --permission-mode bypassPermissions --permission-prompts none --effort high --model sonnet
```

What reaches the session, and how (each channel was probed on 2026-09-06):
- `core/KINGDOM.md` — via the symlink `/Users/fn/codespace/CLAUDE.md` (ancestor CLAUDE.md files
  load; ancestor `.claude/rules` do NOT, even with `--add-dir` + env flags).
- `core/CONTRACT.md` + all `core/rules/*.md` — rendered into `realms/<realm>/system.md` by
  `scripts/jobs.py render` and appended to the system prompt (≈ 38 KB). Re-run `render` after
  editing a rule or the contract; the cron job's `appendSystemPrompt` carries the same text.
- Agents and skills — `--add-dir citadel` (verified in the `system/init` event).
- Guard hooks, `zig fmt` hook, auto-memory dir — `--settings realms/<realm>/settings.json`.
`python3 scripts/jobs.py argv <realm>` is the single source of the flag list; `plan` fails on
drift.

## Operator rules

- Edit the brain here, never in a realm. After editing `core/rules/` or `core/CONTRACT.md`, run
  `python3 scripts/jobs.py render` (system prompts) and `jobs.py apply` (cron copies); KINGDOM.md,
  agents and skills are read live.
- After editing `workflows/`, run `python3 scripts/jobs.py render`, then `plan`; `apply` only
  when the human asked for it in this session.
- Realm memory is written by realm cycles; the citadel cycle only compacts it.
- Foundation repo skeletons come from `templates/repo` (code and docs only, no AI files).
- Never push to `main` of a realm from citadel; open a PR in that repo.
