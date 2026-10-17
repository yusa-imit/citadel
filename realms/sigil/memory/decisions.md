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

## 2026-10-16 — Patch copy/move deep-copy (ADR 0004 amendment, plan 005 item 4)

`copy` and `move` deep-copy their source (`clone.deep`) instead of sharing the subtree. **Why**: sharing
makes the tree a DAG, every depth check a walk of the expanded tree, and k doubling copies an
exponential walk. **How to apply**: no path code may assume a shared subtree; untouched siblings
are shared only between an old and a new spine.

- 2026-10-17 (cycle 59): JSONPath filter nesting uses recursion bounded by `filter_depth_max` (8), not an
  explicit suspended-evaluation machine; ADR 0004 section 6 amended in PR #62. Revisit only if a reviewer insists.
