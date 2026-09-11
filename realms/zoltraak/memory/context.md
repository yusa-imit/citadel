# zoltraak — context

last_seen_at: 2026-09-11T00:00:00Z
rejected_plans: []

## Cycle 8 — 2026-09-11 — FEATURE
- Found dirty at preflight: branch `refactor/strings-assertion-baseline-v2`
  (not `wip/*`, no open PR) with an uncommitted, unverified diff — a prior
  session's interrupted continuation of plan 001 item 11 onto
  `commands/strings.zig`. Preserved to `wip/strings-assertion-baseline-v2-
  20260911` per the no-discard rule, then verified and continued it rather
  than starting over: `zig build test` passed (1106/1106, only the 2
  documented signal-4 flakes) but `zig build tidy` failed — the prior
  session's `zig fmt` run had reformatted 4 command-lookup arrays
  (`read_commands`, `write_commands`, `single_key_commands`,
  `skip_redirect_cmds`) into a column-aligned grid, pushing the file from
  230 to 284 lines over the 100-column baseline (a real fmt-vs-tidy
  tension: multi-item-per-line arrays are only zig-fmt-stable as either
  one-item-per-line or a padded grid, and grid width scales with the
  longest item in the array). Repacked each array at the widest column
  count that still clears 100 columns (5-7, computed empirically) rather
  than one-per-line, which would have blown `getCommandAccessMode`/
  `getCommandKeyPositions`'s function-length baseline instead; merged two
  identical-body key-position branches (RENAME/RENAMENX,
  COPY/LMOVE/BLMOVE/BRPOPLPUSH/RPOPLPUSH/SMOVE) to claw back the last 2
  lines under `getCommandKeyPositions`'s 140-line baseline.
- Plan 001 item 11 (assertion baseline) now covers `commands/strings.zig`
  too (0 → 46 asserts: NX/XX and KEEPTTL/EX mutual exclusion, key-existence
  postconditions on SET/INCR/DECR family, i64 negation-overflow proof,
  NaN/Inf guards on INCRBYFLOAT, paired-arg-count invariants on MSET/HSET-
  style commands) — joining memory.zig (deferred), parser.zig, writer.zig,
  server.zig.
- Verified: `zig build test` 1106/1106 (only the 2 documented flakes),
  `zig build tidy` clean, `zig fmt --check src/commands/strings.zig` clean.
- PRs: #131 opened (`refactor/strings-assertion-baseline-v2`), CI pending
  at the cycle deadline — commented "awaiting CI; merge next cycle".
- Next: next cycle's inbox merges #131. Assertion baseline remaining:
  `storage/memory.zig` (deferred, large). Re-check zuda/sailor tags.
- Blockers: none beyond the standing zuda/sailor v3.0.0 gate (still
  v2.3.0/v2.99.0). Open questions: none.

## Cycle 7 — 2026-09-09 — FEATURE
- Done: inbox merged #129 (writer.zig assertion baseline, CI green,
  auto-merged). Re-confirmed items 4-9 of plan 001 still blocked: zuda at
  v2.3.0, sailor at v2.99.0, neither has hit v3.0.0 yet. Implemented plan
  001 item 11 continuation: assertion baseline on `server.zig` (~20
  asserts, up from 0) — `ServerStats` counter monotonicity, uptime
  non-negativity, `ShutdownState` requested/request-payload consistency,
  `GossipTask` running/thread-handle invariants, `Server.init`/`deinit`
  database-count postconditions, `performShutdown` precondition,
  `detectPsync` case-insensitive-match proof. `server.zig` had zero unit
  tests before this (own comment said the accept loop needs integration
  testing) — added 4 new unit tests for the testable pieces (ServerStats,
  ShutdownState, detectPsync, Server.init/deinit). Adding asserts to
  `start`/`handleConnection` pushed them 1-2 lines over their
  `tidy-baseline.zon` ceiling (shrink-only); reverted those two and left
  the accept loop covered by the shell integration suite instead.
- Verified: `zig build test` 1106/1106 (only the 2 documented signal-4
  RDB flakes), `zig build tidy` clean, `zig fmt --check src/server.zig`
  clean.
- PRs: #130 opened (`refactor/server-assertion-baseline`), CI pending at
  the cycle deadline — commented "awaiting CI; merge next cycle".
- Next: next cycle's inbox merges #130. Assertion baseline remaining:
  `storage/memory.zig`, `commands/strings.zig` (both large — may need
  more than one cycle each). Re-check zuda/sailor tags each cycle.
- Blockers: none this cycle beyond the standing zuda/sailor v3.0.0 gate.
  Open questions: none.

## History (cycles before 7)
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
