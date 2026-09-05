# citadel — Kingdom Orchestrator

> citadel는 코드를 갖지 않는다. 왕국의 **지도, 규칙, 템플릿, 그리고 AI 개발 루프의 정의**를 가진다.
> 여기서 하는 일은 레포 하나가 아니라 **레포 사이**의 일이다.

## When you are here

You are in the control room of nine sibling repos, all checked out as `../<name>` (see `zr-repos.toml`).
Typical tasks:

1. **Cross-repo status** — `zr repo status` (or `for d in ../sigil ../sirocco ...; do git -C $d log -1 --oneline; done`)
2. **Change how every repo is developed** — edit `templates/repo/**`, run `scripts/sync-templates.sh`, review each repo's diff, commit in each repo
3. **Change what a cron job does** — edit `workflows/prompts/<job>.md` or `workflows/jobs.toml`, run `python3 scripts/jobs.py plan`, then `apply`. Never edit prompts directly on the cron server; citadel is the source of truth
4. **Add a component** — `specs/` + `scripts/scaffold.py` (README "Adding a component")
5. **Plan integrations** — `docs/ROADMAP.md`. An integration task touches ≥2 repos; write the plan here, then do the work inside each repo following that repo's CLAUDE.md
6. **Keep the map honest** — when a `build.zig.zon` dependency changes anywhere, update `zr-repos.toml [deps]` and the mermaid graph in `docs/KINGDOM.md`

## Rules

- Foundation repos (sigil, sirocco, strata, synod) depend on Zig std only. Do not add kingdom deps to their `build.zig.zon`; integrations go in `src/adapters/` of the *consumer* or as opt-in adapters documented in the PRD
- Dependencies point down: service → tool → library → foundation. Never up
- One version per dependency across the kingdom; consumers depend on foundation by **tag**, never git ref
- Template-owned files in foundation repos (`CLAUDE.md`, `.claude/agents|commands`, `ci.yml`, `README.md`, `docs/milestones.md` header, `build.zig`) are edited **here** and propagated. Editing them in-repo is fine for a hotfix but must be back-ported to `templates/`
- `workflows/` changes that alter cost (schedule, model, budget, timeout) are applied only with explicit user confirmation — `jobs.py apply` prompts; do not pass `--yes` on the user's behalf
- Zig 0.15.2 kingdom-wide

## Layout

```
citadel/
├── CLAUDE.md               # this file
├── README.md
├── zr-repos.toml           # repo registry + cross-repo deps
├── zr.toml                 # kingdom tasks
├── docs/KINGDOM.md         # map, layers, dependency graph, names
├── docs/ROADMAP.md         # cross-repo integration phases
├── workflows/
│   ├── jobs.toml           # schedule/model/budget per job
│   ├── prompts/<job>.md    # claude -p prompt per job
│   └── system/<job>.md     # --append-system-prompt per job
├── scripts/
│   ├── jobs.py             # export / plan / apply against ../cron server
│   ├── session.sh          # run one cycle locally
│   ├── scaffold.py         # render a repo from specs + templates
│   └── sync-templates.sh   # re-render template-owned files into foundation repos
├── specs/<name>.json, <name>.PRD.md
├── templates/repo/         # canonical repo shape
└── .claude/                # kingdom-level agents & commands
```

## Agents

| Agent | Purpose |
|---|---|
| kingdom-architect (opus) | Cross-repo API decisions: which layer owns what, adapter boundaries, migration plans |

## Commands

`/kingdom-status` · `/jobs-plan` · `/integrate <consumer> <foundation>` · `/new-component <name>`
