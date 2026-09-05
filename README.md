# citadel 🏰

> The control room of the Zig kingdom. Nine sibling repos hold code; citadel holds the brain,
> the protocol, the realm state, and the cron job definitions that drive autonomous development.

```
SERVICES     silica · zoltraak
TOOLING      zr
LIBRARIES    sailor · zuda
FOUNDATION   sigil · sirocco · strata · synod
```

Map and graph: [docs/KINGDOM.md](docs/KINGDOM.md) · cross-repo order: [docs/ROADMAP.md](docs/ROADMAP.md)

## How it works

- `core/KINGDOM.md` is symlinked to `/Users/fn/codespace/CLAUDE.md`, so every Claude Code session
  in any kingdom repo loads it. `core/rules/` is symlinked to `/Users/fn/codespace/.claude/rules`.
- A realm session is `cd <repo> && claude -p "/cycle <repo>" --add-dir citadel …`
  (`scripts/kingdom cycle <repo> -p`). The `/cycle` skill runs preflight → inbox → plan or
  implement or stabilize → report ([protocol/CYCLE.md](protocol/CYCLE.md)).
- The human is reached only through GitHub: plan PRs (merge = approve), issues (`bug`,
  `directive`, `question`), PR comments, and the `hold` label
  ([protocol/GITHUB.md](protocol/GITHUB.md)).
- Repos contain no AI files ([protocol/DOCS.md](protocol/DOCS.md)); realm-specific knowledge lives
  in `realms/<repo>/` (REALM.md, STATE.md, memory/).
- Engineering law: Tiger Style adapted for libraries (`core/rules/tiger-style.md`); Zig 0.16
  kingdom-wide (`core/rules/zig-0.16.md`).

## Daily use

```bash
scripts/kingdom shell silica            # interactive session in silica with the brain attached
scripts/kingdom cycle sigil -p          # run one unattended cycle now
python3 scripts/jobs.py plan            # drift between workflows/ and the cron server
python3 scripts/jobs.py apply           # push job definitions (asks first)
```

## License

MIT
