# strata — decisions

_(migrated from the repo's former .claude/memory; keep under 200 lines)_

Format: `## ADR-NNN: Title` / **Date** / **Context** / **Decision** / **Consequences**

## ADR-001: Zero external dependencies

**Date**: 2026-09-05
**Context**: strata is a foundation layer of the Zig kingdom; every other component may
depend on it.
**Decision**: Depend only on the Zig standard library. Integrations with other kingdom
components live under `src/adapters/` and are opt-in.
**Consequences**: No dependency cycles across the kingdom. Some functionality (e.g.
compression, event-driven watchers) is deferred until it can be implemented in-tree or
provided through an adapter.

## Decision: leave `wip/chore-zig-0.16-migration-20260909` in place

**Date**: 2026-09-15 (cycle 11)
**Context**: milestone 001's last-but-one checklist item is "`wip/*` decision". The branch
holds a single commit (`e4ce05e`, "chore: migrate to Zig 0.16.0 (plan 001 items 4, 5, 7)")
preserved by cycle 4's preflight before that cycle switched to main. `git diff main
origin/wip/chore-zig-0.16-migration-20260909 --stat` shows the branch is now strictly
*behind* main: 8 files, net -1152 lines relative to main — it predates PR #7 (the actual
0.16 migration, landed cleanly the same cycle), PR #11 (ADR-0001 + PRD rewrite), and PR #13
(tidy's file-length rule), none of which it contains.
**Decision**: nothing on the branch is unique or worth salvaging; every change it attempted
was superseded by a cleaner version merged through normal plan-001 PRs. Per kingdom rule
(never delete a `wip/*` branch), the branch stays as historical record. No PR opens against
it. Milestone checklist item ticked as "decision recorded", not "finished".
**Consequences**: `origin/wip/chore-zig-0.16-migration-20260909` remains in the remote
branch list indefinitely; future cycles should not re-open or merge it.
