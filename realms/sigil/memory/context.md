# sigil — context

## Cycle 1 — 2026-09-05 — FEATURE

- Done: preflight (CI green, no bug/question issues, tree clean); inbox found nothing
  actionable — plan PR #2 has zero review comments, just awaiting human merge.
- PRs: none opened this cycle.
- Next: same as cycle 0 — once #2 merges, run plan 001 (Zig 0.16 migration + tidy step +
  `io: Io` convention spike). Until then, no milestone issue exists so no implementation
  work is possible.
- Blockers: plan 001 PR #2 awaiting human merge (no action needed from us — GitHub
  protocol says merge=approve, comment=request changes, close=reject).
- Open questions: none.

## History

Cycle 0 (2026-09-05, RESTRUCTURE): realm created by the citadel restructure; memory
migrated from the repo's former `.claude/memory/`. Survey found a pure scaffold (285 LOC,
all stub modules, 2 commits). Zig 0.16 probe found sigil nearly migration-ready — 1 trivial
error (`main.zig`'s `GeneralPurposeAllocator` rename), library surface already compiles
clean on 0.16. Full detail in `REALM.md`/`STATE.md`. Plan 001 PR opened, awaiting merge.

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
