# sigil — context

## Cycle 0 — 2026-09-05 — RESTRUCTURE

- Realm created by citadel restructure. Memory migrated from the repo's former
  `.claude/memory/`. First plan `001` prescribed by `citadel/docs/ROADMAP.md`.
- Survey found: pure scaffold, nothing functional yet (285 LOC, all stub modules). Zig
  0.16 probe found sigil is nearly migration-ready — 1 trivial error (`main.zig`'s
  `GeneralPurposeAllocator` rename), library surface already compiles clean on 0.16.
  Full detail in `REALM.md` and `STATE.md`.
- Next: open plan 001 PR (if not open) -> await human merge. Plan 001 should cover both
  the Zig 0.16 migration (trivial, see `STATE.md`) and/or Phase 1 (core + reflect) — the
  Zig 0.16 migration skill can likely close it in one cycle since the fix is one line.
- Open questions: none.

## Standing backlog (carried over from repo's former `project-context.md`)

In milestone order (`docs/milestones.md` Phase 1, unchanged since bootstrap):

- **1A** — `core/{value,tree,diagnostics}.zig`: `Value` union, arena-owned `ValueTree`,
  `Diagnostics{line,col,message}`. Tests: arena release, equality, Map insertion-order
  preservation.
- **1B** — `core/number.zig`: i64/u64/f64 boundary handling, `-0`, exponents, explicit
  overflow errors.
- **1C** — `core/unicode.zig`: UTF-8/escape utilities.
- **1D** — `reflect/{parse,stringify,options}.zig`: comptime struct<->Value mapping;
  field rename/defaults/deny-unknown-fields options.
- **2A-2C** (after Phase 1) — `json/{scanner,dom,writer}.zig`: RFC 8259 pull scanner,
  DOM builder, pretty/minify writer.
- Housekeeping: populate the empty performance-targets table in `docs/milestones.md` and
  `docs/PRD.md` §5 once any module is benchmarkable.

## Next priority

Phase 1A (`core/value.zig` + `ValueTree` + `Diagnostics`) is the actual next priority once
the repo's own `.claude/`/`CLAUDE.md` files are removed and the Zig 0.16 migration (or a
decision to defer it past Phase 1) is settled — nothing in Phase 1-6 has dependencies
outside `core/`, so 1A can start immediately either way.
