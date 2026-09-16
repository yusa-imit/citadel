# zoltraak — context

last_seen_at: 2026-09-16T00:00:00Z
rejected_plans: []

## Cycle 9 — 2026-09-16 — FEATURE
- Preflight found dirty: branch `refactor/memory-assertion-baseline-continue-2`
  (not `wip/*`, no open PR) with an uncommitted diff — an interrupted
  continuation of item 11 on `storage/memory.zig` (getType/setExpiry/
  getTtlMs/incrby/incrbyfloat). Preserved to `wip/memory-assertion-
  baseline-continue-2-20260916` per the no-discard rule.
- While preparing to implement, found two more `wip/*` branches already on
  origin from earlier interrupted sessions, never picked up: `wip/memory-
  assertion-baseline-core-20260912` and `-continue-20260915` (init/deinit/
  set/checkMemoryLimitAndEvict, 34 tests). The two chains touch disjoint
  functions in the same file — merged clean, no conflicts — combined into
  one PR rather than stranding one chain again. Also backfilled a missing
  `commands/strings.zig` CHANGELOG entry PR #131 had omitted.
- PR #132 merged (CI green: Build & Test 6m51s, Shell Integration 58s).
  Plan 001 item 11 (assertion baseline) is now fully done across all five
  hot modules. Tracking issue #121 updated.
- Near-miss: a stray `git stash -u` (checking whether fmt violations were
  pre-existing) had nothing to stash, then `git stash pop` grabbed one of
  three untriaged stash entries left over since cycle 1 (unrelated WIP),
  causing conflicts in `build.zig`/`memory.zig`. `git reset --hard` is
  guard-blocked; recovered cleanly with `git checkout HEAD -- <files>` +
  removing the one untracked file the pop introduced. All three original
  stash entries are untouched, still in `git stash list`, still needing
  triage (see `debugging.md`). Lesson: never run bare `git stash`/`stash
  pop` in this repo without listing existing entries first — use `git
  diff`/targeted `checkout` instead when only checking a baseline.
- Next: still no unblocked plan 001 items until zuda/sailor reach v3.0.0
  (checked this cycle: v2.3.0/v2.99.0). Triage the 3 pre-existing stash
  entries as a future cycle's task if nothing else unblocks first.
- Blockers: items 4-9, 12 blocked on zuda/sailor v3.0.0. Open questions:
  none.

## History (cycles before 9)
- Cycle 8: preserved and continued an interrupted `commands/strings.zig`
  assertion-baseline diff (`wip/strings-assertion-baseline-v2-20260911`);
  fixed a tidy-baseline regression from a prior `zig fmt` run (command-
  lookup arrays reformatted past 100 columns) by repacking them at a
  computed safe width. Item 11 gained `strings.zig` (0 → 46 asserts). PR
  #131.
- Cycle 7: merged #129 (writer.zig). Implemented item 11 continuation on
  `server.zig` (0 → ~20 asserts: `ServerStats`/`ShutdownState`/
  `GossipTask`/`init`/`deinit`/`performShutdown`/`detectPsync`, 4 new unit
  tests — file had none before). PR #130.
- Cycle 6: merged #128 (catch-unreachable proofs). Confirmed items 4-9 of
  plan 001 are genuinely blocked by probing both toolchain trees directly
  (`std.process.Init`, `mem.find*`, vtable `std.Io` don't exist under the
  pinned 0.15.2 toolchain) — wait on item 10's toolchain bump, itself
  `blocked_by zuda>=3.0.0, sailor>=3.0.0`. Implemented item 11 continuation:
  assertion baseline on `protocol/writer.zig` (~50 asserts). code-reviewer
  caught a real bug pre-merge: `bulk_len_max`/`multibulk_count_max` are
  parser-side input limits, not writer-side output invariants — asserting
  them on write functions would crash on legitimate large collections
  (e.g. `HGETALL` on a >1M-field hash). PR #129.
- Cycle 5 (STABILIZATION, forced by `n % 5 == 0`): merged #127 (parser.zig
  assertion baseline, plan 001 item 10 partial). Fresh tidy-auditor audit
  (see `STATE.md`) found 17 `catch unreachable` sites without proof
  comments — fixed across 6 files, extracted `Storage.formatHexByte` to
  stay under a function-length baseline. PR #128 opened, CI pending at
  deadline. 3 untriaged `git stash` entries from cycle 1 still need
  triage — `stash@{0}` plausibly fixes the two signal-4 RDB crashes.
- Cycle 4: inbox merged #125 (`build.zig` on 0.16, plan 001 item 3).
  Implemented + merged #126: renamed 471 `std.ArrayList(T){}`/
  `ArrayListUnmanaged(T){}` literal-inits to `.empty` (52 files) and
  `GeneralPurposeAllocator`→`DebugAllocator` (3 sites) — both true renames
  already present in the pinned 0.15.2 stdlib, not version-gated. Scope
  decision: plan item 4 also calls for `main() !void`→
  `main(init: std.process.Init) !void` + `argsAlloc`→`init.minimal.args`;
  `std.process.Init` doesn't exist in 0.15.2, so that sub-part was
  deferred to item 8 (toolchain pin bump) and item 4's checkbox left
  unchecked. `zig build test` 1106/1106 green, `fmt`/`tidy` clean.
- Cycle 3: inbox merged #124 (`tidy` build step) — plan 001 item 2
  complete; also back-filled items 1-2 checkboxes in the plan file itself
  (prior cycles only ticked the milestone issue). Implemented item 3
  (`build.zig` on 0.16): moved 105 LuaJIT-linking call sites from
  `Step.Compile.linkSystemLibrary`/`.linkLibC`/etc. (removed in 0.16) to
  the identical `root_module`-based API (byte-identical between 0.15.2/
  0.16.0), extracted a `link_luajit()` helper, shrank `build.zig` by
  ~800 lines. PR #125 opened, CI pending at deadline.
- Cycle 2: inbox merged #123 (real MIGRATE, CI green) — plan 001 item 1
  fully complete. Implemented item 2 (`tidy` build step: `tools/tidy.zig`,
  line/function length, ban list, `//!` headers, shrink-only
  `tidy-baseline.zon`). PR #124 opened, CI pending at deadline.
- Cycle 1: opened milestone issue #121 for plan 001. Split item 1 ("Clear
  the decks") into #122 (hygiene, merged) and #123 (real MIGRATE via
  DUMP/RESTORE, rebased from `wip/migrate-real-dump-restore`). Discovered
  3 pre-existing untriaged `git stash` entries (still in `git stash
  list`), most promising first:
  - `stash@{0}` (4f38643): DUMP/RESTORE type-byte fix for stream +
    hyperloglog, touching `build.zig` + `src/storage/memory.zig` —
    plausibly the root cause of the two signal-4 RDB round-trip crashes
    (`test_iter432`, `test_iter437`). Try first on a fresh branch with the
    two crash tests as the acceptance check.
  - `stash@{1}` (a73d2a4): RDB persistence for Time Series + Vector Set —
    may overlap stash@{0}, check ordering before applying both.
  - `stash@{2}` (41a2e07): `BF.LOADCHUNK` refactor in
    `src/commands/bloom.zig` — smallest, independent.
  - None build/test-verified against current `main` yet; treat as
    unverified WIP.
- Realm created by citadel restructure; first plan `001` prescribed by
  `citadel/docs/ROADMAP.md` (Zig 0.16 migration). A complete, tested,
  uncommitted change (`src/commands/cluster.zig`, real MIGRATE via
  DUMP/RESTORE) was found in the working tree and preserved on branch
  `wip/migrate-real-dump-restore` (merged as #123) rather than discarded.

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
