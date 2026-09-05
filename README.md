# citadel 🏰

> The command post of the Zig kingdom — one place that maps every repo, drives every autonomous
> development loop, and owns the templates the foundation repos are rendered from.

```
  SERVICES     silica · zoltraak
  TOOLING      zr
  LIBRARIES    sailor · zuda
  FOUNDATION   sigil · sirocco · strata · synod
```

Full map and dependency graph: [docs/KINGDOM.md](docs/KINGDOM.md) · cross-repo plan: [docs/ROADMAP.md](docs/ROADMAP.md)

## What lives here

| Path | Purpose |
|---|---|
| `zr-repos.toml` | Multi-repo registry for [zr](https://github.com/yusa-imit/zr): `zr repo sync / status / run` |
| `zr.toml` | Kingdom-level tasks (`zr test`, `zr foundation-test`, `zr jobs-plan`, …) |
| `workflows/jobs.toml` | Every autonomous-development cron job: schedule, cwd, model, budget |
| `workflows/prompts/<job>.md` | The `claude -p` prompt each job runs — **version-controlled source of truth** |
| `workflows/system/<job>.md` | Optional `--append-system-prompt` per job |
| `scripts/jobs.py` | `export` (server → files), `plan` (diff), `apply` (files → server) against the [cron](../cron) server |
| `scripts/session.sh <job>` | Run one cycle locally exactly as cron would |
| `templates/repo/` | The canonical shape of a kingdom repo (CLAUDE.md, agents, commands, CI, …) |
| `specs/<name>.json` + `<name>.PRD.md` | Component specs; `scripts/scaffold.py <name>` renders a repo from them |
| `scripts/sync-templates.sh` | Re-render template-owned files into all foundation repos after editing a template |

## Daily use

```bash
# see everything
zr status                      # git status across 9 repos
zr test                        # zig build test everywhere, dependency order

# AI workflow management
python3 scripts/jobs.py plan   # what differs between workflows/ and the running cron server
python3 scripts/jobs.py apply  # push changes (asks first)
scripts/session.sh strata-dev-v1   # run one strata cycle right now, in the foreground

# templates
vim templates/repo/agents/code-reviewer.md
scripts/sync-templates.sh      # propagate to sigil/sirocco/strata/synod, then review & commit each
```

`zr` binary: `../zr/zig-out/bin/zr` or `curl -fsSL https://raw.githubusercontent.com/yusa-imit/zr/main/install.sh | sh`.

## Adding a component

1. Write `specs/<name>.json` and `specs/<name>.PRD.md` (copy an existing pair)
2. `python3 scripts/scaffold.py <name>` → `../<name>` with a fresh Zig fingerprint
3. `cd ../<name> && zig build test && git init && git add . && git commit -m "chore: bootstrap"`
4. `gh repo create yusa-imit/<name> --public --source . --push`
5. Add it to `zr-repos.toml`, `docs/KINGDOM.md`, and a job in `workflows/`

## License

MIT
