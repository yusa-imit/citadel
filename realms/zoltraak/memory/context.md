# zoltraak — context

last_seen_at: 2026-09-08T11:22:00Z
rejected_plans: []

## Cycle 5 — 2026-09-08 — STABILIZATION
- Done: inbox merged #127 (parser.zig assertion baseline, plan 001 item
  10 partial — 35 asserts + `ParseError.LengthTooLarge` bound; CI green).
  Mode forced to STABILIZATION by `n % 5 == 0`. `tidy-auditor` produced a
  fresh full audit (see `STATE.md` for the table): 49/~90 files >800
  lines, 155 functions >70 lines, 40 `assert`s total (85% still
  concentrated in `parser.zig` from #127), 88/88 files missing `//!`
  headers, 17 `catch unreachable` sites without the same-line proof
  comment `zig build tidy` requires. Picked the smallest mechanical class
  (17 proof comments, 6 files: `storage/memory.zig`, `storage/modules.zig`,
  `commands/{bitfield,cluster,client}.zig`, `scripting/lua_libraries.zig`)
  — all bufPrint-into-sized-buffer or test-only guarded-deinit sites.
  Adding the comment pushed several lines over the 100-column tidy
  baseline; reflowed those calls to multi-line, and extracted
  `Storage.formatHexByte` out of `memory.zig`'s `init` to keep it under
  its 148-line function-length baseline after the reflow (net -6 lines).
- Verified: `zig build test` 1032/1032 (same 2 documented signal-4 RDB
  crashes, no new regressions), `zig build tidy` green (was previously
  green only because these 17 sites were pre-baselined debt — now a real
  reduction), `zig fmt --check` clean on all 6 touched files.
- PRs: #128 opened (`fix/tidy-catch-unreachable-proofs`), CI pending at
  the cycle deadline — commented "awaiting CI; merge next cycle".
- Next: next cycle's inbox merges #128. Next-cheapest tidy class after
  this one is the 88 files missing `//!` headers (mechanical to detect,
  more editorial effort per file than proof comments). Plan 001 item 10
  continuation (assertion baseline on `protocol/writer.zig`, next-
  smallest hot module) still pending from cycle 5's FEATURE half. The 3
  untriaged `git stash` entries from cycle 1 (see History) still need
  triage — `stash@{0}` plausibly fixes the two signal-4 RDB crashes.
- Blockers: none this cycle. Open questions: none.

## History (cycles before 5)
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
