---
name: new-realm
description: Bootstrap a new kingdom component repo from citadel specs and templates, register it as a realm, and prepare its cron job (repo creation and job apply need explicit human confirmation).
argument-hint: <name>
---

1. `kingdom-architect` confirms layer, consumers, and that no realm already owns this.
2. Write `specs/<name>.PRD.md` and `specs/<name>.json`; `python3 scripts/scaffold.py <name>`;
   `cd ../<name> && zig build test`.
3. `realms/<name>/REALM.md` from the template in `realms/_template/`; add to `zr-repos.toml`,
   `docs/KINGDOM.md`, `workflows/jobs.toml`; `python3 scripts/jobs.py render`.
4. Print the exact `gh repo create` and `jobs.py apply` commands; do not run them.
