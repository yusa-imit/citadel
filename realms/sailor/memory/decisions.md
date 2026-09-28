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

## Decision: dedicated `sailor-migration` cron job owns milestone 001 items 4/6-10
- **Date**: 2026-09-28 (OWNER comment on #34).
- **Context**: items 4 and 6-10 (Zig 0.16 toolchain switch + `std.Io` rewrite) were confirmed
  blocked across 7+ regular cycles — no partial rename lands without breaking the pinned 0.15.2
  CI build, and the full switch is multi-cycle work that doesn't fit a 22-minute cycle.
- **Decision**: a new nightly cron job `sailor-migration` (20:05-23:05 KST, 3h timeout, starts
  2026-09-28 night) works `wip/zig-016-migration` on the 0.16.0 toolchain, merging
  `origin/main` each run; checkpoint commits on that branch may be red (OWNER-approved
  exception). It opens the PR to main only once green on 0.16.0, and closes #34 after that PR
  merges.
- **How to apply**: regular `sailor` cycles keep working unblocked milestone items (11 onward)
  and must NOT touch items 4/6-10 and must NOT build from `wip/zig-016-migration` — if a cycle's
  preflight checkout happens to be on that branch, preserve it there (CYCLE.md 0.3) and switch
  to main without building it. Issue #34 itself must stay open (it's the on/off switch for the
  migration job and its cleanup exceptions); only the migration job closes it, after its PR
  merges.

Full history (superseded/one-off decisions) lives in `git log` — this file keeps only
decisions with ongoing relevance to future work.
