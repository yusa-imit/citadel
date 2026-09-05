Bootstrap a new kingdom component named: $ARGUMENTS

1. Call `kingdom-architect` to confirm the layer, consumers, and that no existing repo already owns this
2. Write `specs/<name>.PRD.md` (copy structure from an existing PRD: background, goals, non-goals, architecture, performance targets, phases, principles, testing, risks) and `specs/<name>.json` (modules, rules, checklists, phases, first_tasks)
3. `python3 scripts/scaffold.py <name>` then `cd ../<name> && zig build test`
4. Add the repo to `zr-repos.toml`, `docs/KINGDOM.md` (table + graph + name rationale), and a job in `workflows/jobs.toml` + `workflows/prompts/<name>-dev-v1.md` + `workflows/system/<name>-dev-v1.md`
5. Do NOT create the GitHub repo or apply the cron job without explicit user confirmation — list the exact commands instead
