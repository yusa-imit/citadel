# sirocco — decisions

_(migrated from the repo's former `.claude/memory/decisions.md`; keep under 200 lines)_

Format: `## ADR-NNN: Title` / **Date** / **Context** / **Decision** / **Consequences**

## ADR-001: Zero external dependencies

**Date**: 2026-09-05
**Context**: sirocco is a foundation layer of the Zig kingdom; every other component may
depend on it.
**Decision**: Depend only on the Zig standard library. Integrations with other kingdom
components live under `src/adapters/` and are opt-in.
**Consequences**: No dependency cycles across the kingdom. Some functionality (e.g.
compression, event-driven watchers) is deferred until it can be implemented in-tree or
provided through an adapter.

_(Note: this decision is now also stated kingdom-wide in `citadel/core/rules/00-kingdom.md`
— foundation `build.zig.zon` has no `.dependencies`; kept here verbatim since it predates
that file and gives sirocco's own rationale.)_

## ADR-002: No `wip/*` branch to finish or close (plan 001 item 9)

**Date**: 2026-09-10
**Context**: Plan 001 item 9 asks for a decision on any preserved `wip/*` branch from the
kingdom restructure.
**Decision**: `git branch -a` shows no `wip/*` branch was ever preserved for sirocco —
foundation repos (sigil, sirocco, strata, synod) had no interrupted work at restructure time.
The only other non-main branch, `chore/kingdom-restructure`, already merged as PR #1 and is
plan 001's base. Nothing to finish or close.
**Consequences**: None — item 9 is closed as a no-op. Recorded here per the plan's own verify
criterion (PR #10).
