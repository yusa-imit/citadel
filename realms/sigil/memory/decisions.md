# sigil — decisions

_(migrated from the repo's former `.claude/memory/decisions.md`)_

Format: `## ADR-NNN: Title` / **Date** / **Context** / **Decision** / **Consequences**

## ADR-001: Zero external dependencies

**Date**: 2026-09-05

**Context**: sigil is a foundation layer of the Zig kingdom; every other component may
depend on it.

**Decision**: Depend only on the Zig standard library. Integrations with other kingdom
components live under `src/adapters/` and are opt-in.

**Consequences**: No dependency cycles across the kingdom. Some functionality (e.g.
compression, event-driven watchers) is deferred until it can be implemented in-tree or
provided through an adapter. `build.zig.zon` `.dependencies = .{}` is expected to stay
empty for foundation-layer work; adding a real dependency here would need a new ADR and a
plan, per `citadel/core/rules/00-kingdom.md`.
