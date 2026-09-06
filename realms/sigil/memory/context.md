# sigil — context

last_seen_at: 2026-09-07T00:00:00Z
rejected_plans: []

## Cycle 3 — 2026-09-07 — FEATURE

- Done: implemented plan 001 item 2 (Branch decision) — recorded that no `wip/*` branch exists
  for sigil and the stale local ref for the merged `chore/kingdom-restructure` (PR #1) was
  already absent; ticked the checklist box in `docs/plans/001-*.md`.
- PRs: #5 opened, CI green (7/7 jobs), squash-merged, branch deleted, labelled `auto-merged`.
- Tracking issue #3 checklist updated: 2/11 done.
- Next: item 3 (`tidy` step in `build.zig`) — the first real implementation work on this plan;
  no `blocked_by`.
- Blockers: none.
- Open questions: none.

## History

Cycle 0 (2026-09-05, RESTRUCTURE): realm created by the citadel restructure; memory
migrated from the repo's former `.claude/memory/`. Survey found a pure scaffold (285 LOC,
all stub modules, 2 commits). Zig 0.16 probe found sigil nearly migration-ready — 1 trivial
error (`main.zig`'s `GeneralPurposeAllocator` rename), library surface already compiles
clean on 0.16. Full detail in `REALM.md`/`STATE.md`. Plan 001 PR opened, awaiting merge.

Cycle 1 (2026-09-05, FEATURE): plan 001 PR #2 still open awaiting human merge, zero review
comments; no milestone issue existed yet so no implementation work was possible. No action
taken beyond a status comment on the PR.

Cycle 2 (2026-09-06, FEATURE): plan 001 (PR #2) had merged since last cycle — opened tracking
issue #3 (11-item checklist). Implemented + merged item 1 (Hygiene leftovers) via PR #4, CI
green (7/7).

## Standing backlog (carried over from repo's former `project-context.md`)

Plan 001 (Zig 0.16 migration + Tiger Style baseline) is now the active milestone, tracked in
issue #3. In milestone order for the *next* plan (002, Phase 1 — unchanged since bootstrap):

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
- Housekeeping: populate the empty performance-targets table in `docs/plans/` and
  `docs/PRD.md` §5 once any module is benchmarkable.

## Next priority

Finish plan 001 (issue #3), one checklist item per cycle, before starting Phase 1A. Item 3
(`tidy` step in `build.zig`) is next — the first real implementation work on this plan, no
`blocked_by`: a `zig build tidy` step over `src/**.zig` + `build.zig` + `bench/**.zig` failing
on the seven rules listed in `docs/plans/001-*.md` (line length, function length, `catch
unreachable` without proof, `std.debug.print` outside main.zig, `std.time.*` in lib, `usize`
in wire formats, missing `//!` headers).
