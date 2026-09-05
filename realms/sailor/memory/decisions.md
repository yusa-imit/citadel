# sailor — decisions

_(migrated from the repo's former .claude/memory/decisions.md, 2026-09-05)_

## Decision: project name
- **Date**: 2026-02-27
- **Context**: needed a name for the Zig CLI/TUI library shared by zr, zoltraak, silica.
- **Decision**: "sailor".
- **Rationale**: short, memorable, no namespace conflicts in the Zig ecosystem.

## Decision: library architecture (ratatui-inspired)
- **Date**: 2026-02-27
- **Context**: retained mode (bubbletea/Elm style) vs. immediate mode (ratatui style) for TUI.
- **Decision**: immediate-mode rendering with double-buffered diff.
- **Rationale**: simpler mental model, no hidden state management, better fit for Zig's
  explicit style. Widget = plain struct with a `render` method, no vtable overhead.

## Decision: module independence
- **Date**: 2026-02-27
- **Context**: should modules be tightly integrated or independently usable?
- **Decision**: each module is independently importable — `sailor.arg` works without
  `sailor.tui`.
- **Rationale**: consumer projects have different needs. zoltraak's server only needs
  arg+color. silica's shell needs arg+repl+fmt+tui.

## Decision: no migration of TUI-specific data structures to zuda
- **Context**: kingdom-wide zuda-first policy for general-purpose data structures.
- **Decision**: cell buffer, layout solver, grid, and unicode-width structures stay local to
  sailor — see `docs/zuda-audit.md` in the repo for the full audit and reasoning.
- **Status**: audit complete, conclusion holds as of the 2026-09-05 survey (zero migrations).

Full history (superseded/one-off decisions) lives in `git log` — this file keeps only
decisions with ongoing relevance to future work.
