# zoltraak — context

last_seen_at: 2026-09-07T00:00:00Z
rejected_plans: []

## Cycle 3 — 2026-09-07 — FEATURE
- Done: inbox merged #124 (`tidy` build step, CI green) — plan 001 item 2 complete.
  Also ticked items 1-2 in `docs/plans/001-...md` itself (prior cycles only ticked
  the milestone issue, not the plan file — fixed). Implemented item 3 (`build.zig`
  on 0.16): moved all 105 LuaJIT-linking call sites from `Step.Compile.
  linkSystemLibrary`/`.linkLibC`/`.addIncludePath`/`.addLibraryPath` (removed in
  0.16) to the identical `root_module`-based API (verified byte-identical between
  0.15.2 and 0.16.0 std source — no toolchain pin bump needed). Extracted the
  repeated 8-line block into a `link_luajit()` helper after code-reviewer caught
  the naive substitution pushing ~111 lines past the 100-column `tidy` limit;
  shrank `build.zig` by ~800 lines as a side effect.
- Verified: zoltraak's own `build.zig` compiles cleanly under the pinned 0.16.0
  toolchain (`zig build --help` no longer errors on this repo's file — remaining
  0.16 errors are confined to vendored `zig-pkg/sailor`/`zig-pkg/zuda` build
  scripts, the documented `blocked_by`). `zig build test` 1106/1106 real tests
  green under 0.15.2 (two documented signal-4 crashes unchanged), `tidy` green,
  `fmt` clean.
- PRs: #124 merged (auto-merged). #125 opened (item 3), CI pending at cycle
  deadline — commented "awaiting CI; merge next cycle".
- Next: merge #125 once CI green (next cycle's inbox), then plan 001 item 4
  (mechanical renames A). The 3 untriaged `git stash` entries from cycle 1 (see
  History) still need triage — `stash@{0}` plausibly fixes the two signal-4 RDB
  crashes.
- Blockers: none. Open questions: none.

## History (cycles before 3)
- Cycle 2: inbox merged #123 (real MIGRATE, CI green) — plan 001 item 1 fully
  complete. Implemented item 2 (`tidy` build step: `tools/tidy.zig`, line/function
  length, ban list, `//!` headers, shrink-only `tidy-baseline.zon`). PR #124
  opened, CI pending at deadline.
- Cycle 1: opened milestone issue #121 for plan 001. Split item 1 ("Clear the
  decks") into #122 (hygiene, merged) and #123 (real MIGRATE via DUMP/RESTORE,
  rebased from `wip/migrate-real-dump-restore`). Discovered 3 pre-existing
  untriaged `git stash` entries (not lost, still in `git stash list`), most
  promising first:
  - `stash@{0}` (4f38643): DUMP/RESTORE type-byte fix for stream + hyperloglog,
    touching `build.zig` + `src/storage/memory.zig` — plausibly the root cause of
    the two documented signal-4 RDB round-trip crashes (`test_iter432`,
    `test_iter437`). Try first on a fresh branch with the two crash tests as the
    acceptance check.
  - `stash@{1}` (a73d2a4): RDB persistence for Time Series + Vector Set
    (`persistence.zig`/`timeseries.zig`/`vector.zig`) — may overlap stash@{0},
    check ordering before applying both.
  - `stash@{2}` (41a2e07): `BF.LOADCHUNK` refactor in `src/commands/bloom.zig` —
    smallest, independent.
  - None build/test-verified against current `main` yet; treat as unverified WIP.
- Realm created by citadel restructure. Memory migrated from the repo's former
  `.claude/memory/` and `CLAUDE.md`. First plan `001` prescribed by
  `citadel/docs/ROADMAP.md` (Zig 0.16 migration, `blocked_by: zuda v3.0.0, sailor
  v3.0.0`).
- A complete, tested, uncommitted change (`src/commands/cluster.zig`, real MIGRATE
  via DUMP/RESTORE) was found in the working tree and preserved on branch
  `wip/migrate-real-dump-restore` (now merged as #123) rather than discarded.

## Standing backlog (carried from the repo's former CLAUDE.md / project memory)

Ordered by what the repo's own docs called out as most concrete/highest-impact
first — items 1, 2 done (see History); items 3-8 still open:

1. ~~Open `wip/migrate-real-dump-restore` as a PR~~ — done, merged as #123.
2. ~~Hygiene: untrack `.DS_Store`/etc.~~ — done, merged as #122.
3. Root-cause the two RDB round-trip test crashes (`test_iter437` time-series,
   `test_iter432` streams — signal 4 / illegal instruction on deserialize).
4. Reconcile the 3-way version divergence (`build.zig.zon` 0.2.0, old CLAUDE.md
   claim 0.2.13, actual latest tag v0.2.14) against `citadel/protocol/
   VERSIONING.md` — plan 001's "Docs and release" item covers this.
5. Sorted Set → `zuda.compat.zoltraak_sortedset` migration (status: READY, ~1800
   LOC of local skip-list code removable). HyperLogLog and Geohash are
   permanently BLOCKED on real zuda API mismatches — do not retry without a
   zuda-side change.
6. Wire `src/storage/blocking.zig` (431 lines, unused) into `server.zig`'s event
   loop for true `BLOCK`-family semantics — est. 3-4 iterations, plus a 5-6
   iteration event-loop refactor prerequisite. Largest architectural gap between
   "claimed" and "actual" in the whole project.
7. Reduce 105 `std.debug.print` calls in `src/`; begin splitting
   `storage/memory.zig` (15,650 lines) and `commands/strings.zig` (7,869 lines).
8. Zig 0.16 migration itself (plan 001, in progress — items 1-3 done as of cycle
   3) — items 9 (`std.net`→`Io.net`) and beyond blocked on sailor/zuda v3.0.0.

## Next priority (as of the last durable audit, Session 135, superseded on 1-3)

Session 135's own top-3 recommendations (Lua engine, ACL enforcement, full client
commands) are DONE per `docs/milestones.md`. Two notes still accurate: blocking
semantics remain polling-based (item 6 above), Geohash zuda migration remains
permanently blocked by API shape (item 5 above).
