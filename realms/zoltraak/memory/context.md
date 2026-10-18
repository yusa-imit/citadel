# zoltraak — context

last_seen_at: 2026-10-19T00:00:00Z
rejected_plans: []

## Cycle 31 — 2026-10-19 — FEATURE (all plan items blocked)
- Preflight clean (main, CI green on 71a674c), no bugs, no plan PR, milestone #121 open. zuda
  still v2.3.0 (items 4-9, 12 blocked); sailor is v3.1.0 (owner note on #141: target v3.1.0, the
  pin bump still waits for the 0.16 toolchain). No other owner actions.
- `/stabilize --one`: PR #155 (merged, CI green). `WAIT 1 18446744073709551615` overflowed
  `timeout_ms * 1_000_000` and trapped the server in safe builds; WAITAOF had the same code.
  New `src/utils/wait_poll.zig` (saturating `deadline_ms`, `expired`, `poll_count_max`), 6 tests
  wired into `src/main.zig`; both loops now `for (0..poll_count_max)`. `zig build test` 1616/1616
  except the 2 known signal-4 crashers; fmt and tidy clean. `while (true)` 8 -> 6.
- A command-level WAIT regression test was added to `commands/replication.zig` but does not run
  (that file imports memory.zig; stale suites). Pure helper tests carry the coverage.
- Next: streams_advanced.zig:446,735 sleep-polls; stash triage (stash@{0}); repair memory.zig
  stale suite so commands/*.zig tests run. Items 4-9, 12 unblock on zuda v3.0.0.
- Blockers: zuda v3.0.0. Open questions: none.

## Cycle 30 — 2026-10-18 — STABILIZATION (periodic, n % 5 == 0)
- Preflight clean (main, CI green on 28ee7b5), no bugs, no plan PR, milestone #121 open, no
  owner actions (the only new comment on #121 was our own cycle-29 report). zuda still v2.3.0.
- Audit: `catch unreachable` all carry proof comments (memory.zig:6164,6234 are asserts on a
  just-formatted value); 9 `while (true)` in `src/`, one was an unbounded read.
- PR #154 (merged, CI green): `sendAndReadReply` in `commands/cluster.zig` appended bytes until
  `\n`, so a hostile MIGRATE target could grow the source's buffer without limit. Read moved to
  new `src/network/reply_line.zig` (`read_reply_line`, `reply_line_max` = 4096, `ReplyTooLong`);
  5 loopback tests (mock peer thread), wired into the `src/main.zig` test root, mutation-checked
  (bound x100 makes the over-limit tests fail). `zig build test` 1610/1610 pass except the 2
  known signal-4 crashers; fmt and tidy clean. STATE.md: `while (true)` 9 -> 8.
- Lesson: tests in `commands/*.zig` do not run (they import memory.zig, whose stale suites do
  not compile); the migrate mock-server tests there are in that group. Put testable logic in a
  standalone file with no memory.zig import and wire that. Check a new test actually runs by
  mutating the code under test once.
- Next: remaining `while (true)`: streams_advanced.zig:446,735, replication.zig:290,388,
  bloom.zig:826 (test loop); stash triage (stash@{0}); repair memory.zig stale suite. Items 4-9,
  12 unblock on zuda v3.0.0.
- Blockers: zuda v3.0.0. Open questions: none.

## Cycle 29 — 2026-10-16 — FEATURE (all plan items blocked)
- Preflight clean (main, CI green on b8d35e1), no bugs, no plan PR, milestone #121 open, no
  owner comments. zuda still v2.3.0, so items 4-9, 12 blocked.
- `/stabilize --one`: PR #153. notifications.zig tests passed `PubSub` by value (compile error,
  never ran) and asserted nothing; now real subscribers + exact RESP2 frame comparison + a
  no-flags negative case, wired into the `src/main.zig` reachability test. Only the 2 known
  signal-4 crashers fail locally. First CI run died on a DNS flake fetching deps
  (TemporaryNameServerFailure); `gh run rerun --failed` went green (6m54s / 57s), merged.
- Finding: wiring lazyfree.zig or blocking.zig fails, not by their own tests: any wired file that
  `@import`s `storage/memory.zig` drags in memory.zig's stale test suite (66 errors) plus
  search (110), config (59), modules (41), acl (30), cluster (39). Those suites must be repaired
  first (a big task: one file at a time, memory.zig first). persistence/aof/replication not tried;
  check their imports for memory.zig before wiring.
- Careful: `sed '/storage\/blocking.zig/d'` also deleted the real `pub const blocking` line in
  main.zig; use anchored patterns.
- Next: try aof/replication/persistence (if they avoid memory.zig); commands/*.zig stale tests;
  stash triage (stash@{0}). Items 4-9, 12 unblock on zuda v3.0.0.
- Blockers: zuda v3.0.0. Open questions: none.

## Cycles 25-28 (2026-10-13..15, condensed 2026-10-17)
- All `/stabilize --one`, zuda still v2.3.0 (items 4-9, 12 blocked). Each wired a file into the
  `src/main.zig` reachability test after fixing it; `zig build test` 1344 -> 1519, only the 2 known
  signal-4 crashers fail. #149 cuckoo (test ignored `insert`'s bool, compile error); #150 tdigest
  (`cdf` mid-point convention like Redis; stale merge test pinned replace semantics); #151 real
  leak in `SentinelState.resetMaster` (ids never freed, now `SentinelInfo.deinit`; `zuda` import
  added to the unit-test root in build.zig); #152 `LFUCounter` seeded from the wall clock, now
  `initWithSeed` + deterministic tests, eviction wired.
- Lessons: wire by appending one `_ = @import` and running `zig build test`; use anchored sed
  patterns (an unanchored delete removed the real `pub const blocking` line in main.zig); the
  guard blocks python heredocs containing `rm -rf` and compound `cd repo; ...` (plain commands);
  `./zig-out/bin/zoltraak` pid 80225 is not ours, left alone.

## Cycles 23-24 (2026-10-11..12, condensed 2026-10-15)
- Both FEATURE, all plan items blocked; each ran `/stabilize --one`: #147 fixed legacy JSON
  paths (`.a.b` returned InvalidPathSyntax; `scan_start` helper in `storage/jsonpath.zig`;
  `parse` keeps its 91-line tidy baseline) and wired jsonpath; #148 fixed bloom `LoadContext`
  tests and wired bloom + functions.
- Probe (`zig test src/storage/<f>.zig`) found cuckoo/tdigest/sentinel issues (done in 25-27);
  search, cluster, config, tls_config, acl, timeseries, modules, pubsub do not compile
  standalone (module path or stale tests). Deleting `.zig-cache` fixes the `FileNotFound`
  build-runner error.

## Cycles 21-22 (2026-10-09..10, condensed 2026-10-14)
- Both FEATURE cycles had every plan item blocked (zuda still v2.3.0, items 4-9, 12), so each ran
  one `/stabilize --one`: #145 wired encodings, listpack, memory_tracker, slowlog, intset, latency
  into the `src/main.zig` reachability test (`zig build test` 1160 -> 1207); #146 fixed a real bug
  (`CMS.INCRBY key item -9223372036854775808` trapped on `-delta`, now `@abs` and returns
  CounterUnderflow, regression test first) and wired cms, scripting, json_value, vector, defrag
  (1207 -> 1275). Only the 2 known signal-4 crashers fail locally. #144 (topk/heavykeeper) merged.
- Probe trick: `zig test src/<f>.zig` standalone shows whether a file's tests compile; blocking,
  lazyfree, notifications, aof, replication, persistence, eviction fail there (import outside
  module path / `zuda`) and need build-module wiring, not a bare import-test.
- Not mine: `./zig-out/bin/zoltraak` pid 80225 running for days; left alone.
- Next: stash triage (stash@{0}); commands/*.zig stale tests. Blockers: zuda v3.0.0.

## Cycles 18-20 (2026-10-06..08, condensed 2026-10-17)
- 18: #142 `zoltraak-cli` printed via `std.debug.print` (stderr), so `--json/--csv/--raw` could
  not be piped; now a buffered stdout writer, formatters take `*std.Io.Writer`, `run_repl`
  extracted; `std.debug.print` in `src/` is 0. Issue #141 (`migration: sailor v3.0.0`) opened by
  the release cycle: pin bump waits for the 0.16 toolchain, so items 4-9, 12 stay blocked.
- 19: #143 bounded `TopKValue`/`HeavyKeeper` `heapifyDown` (`for (0..@bitSizeOf(usize))`).
- 20 (STABILIZATION): finding that `src/` has 2659 `test` blocks but `zig build test` ran 1114;
  Zig runs `test` blocks only for files something analyzes. #144 references topk + heavykeeper
  from a `src/main.zig` test block (1160/1160). Bulk-referencing all 84 other files does not
  compile (stale tests, e.g. commands/acl.zig arity, `**Storage`, a 32-arg format limit): wire one
  file at a time; a full-tree error dump took >10 min, so grep one file.
- Lessons: `gh pr create --label chore` fails (no label); `gh pr create` can hit a transient
  GraphQL error, retry; the guard blocks chained `gh pr merge ...; ...`.

## History (cycles 13-17, condensed 2026-10-10)

All FEATURE/STABILIZATION cycles with plan 001 items 4-9, 12 blocked on zuda/sailor v3.0.0; each
ran `/stabilize --one`:
- **13 (09-30)**: PR #136 applied `zig fmt` to 13 files (no logic change); function-length
  baselines raised for fmt-split `cmd*` functions. Local `zig build test`: 1106/1106 except the
  2 known signal-4 RDB crashers (`test_iter432`/`437`).
- **14 (10-01)**: PR #137 added `zig fmt --check src build.zig` to CI (merged next cycle).
  Local build failed with `FileNotFound` build-runner error: `rm -rf .zig-cache` fixes it.
- **15 (10-02)**: PR #138 moved 13 `std.debug.print` calls to `std.log` (storage, commands,
  scripting).
- **16 (10-03)**: PR #139 moved server.zig's 26 prints to `std.log`. A leaked hung test binary
  (not ours, pid 68879) sat at 0% CPU for days; did not recur.
- **17 (10-05)**: tree was dirty on `chore/std-log-main-prints`; preserved on
  `wip/std-log-main-prints-20261005`, landed as PR #140 (main.zig 21 prints, pure `usageText`).
  Remaining `debug.print`: cli.zig 45 (CLI output is product: needs a stdout-writer decision).
- Lessons: `gh pr create --label chore` fails (no `chore` label in the repo); guard hook blocks
  compound `cd repo; ...`, `timeout`, chained `sleep`: run plain commands.

## History (cycles 1-9, folded)
- Cycle 1: opened milestone #121; item 1 split into #122 (hygiene) and #123 (real MIGRATE via
  DUMP/RESTORE, from `wip/migrate-real-dump-restore`). Found 3 untriaged `git stash` entries,
  none verified against `main`: `stash@{0}` (4f38643) DUMP/RESTORE type-byte fix for stream +
  hyperloglog (`build.zig`, `storage/memory.zig`; plausibly fixes the signal-4 crashers
  `test_iter432`/`test_iter437`, try first on a fresh branch); `stash@{1}` (a73d2a4) RDB for
  Time Series + Vector Set (may overlap {0}); `stash@{2}` (41a2e07) `BF.LOADCHUNK` refactor in
  `commands/bloom.zig` (smallest, independent).
- Cycles 2-3: `tidy` build step (#124, `tools/tidy.zig`, shrink-only `tidy-baseline.zon`);
  `build.zig` on 0.16 with a `link_luajit()` helper (#125). Items 1-3 done.
- Cycle 4: renamed 471 `.empty` ArrayList literal-inits and `GeneralPurposeAllocator` ->
  `DebugAllocator` (#126). `main(init: std.process.Init)` deferred: absent in 0.15.2.
- Cycles 5-9: assertion baseline (item 11) on parser.zig (#127), writer.zig (#129),
  server.zig (#130), strings.zig (#131), memory.zig (#132); 17 unproven `catch unreachable`
  fixed (#128). Items 4-9 confirmed blocked by probing both toolchains. Lessons: code-reviewer
  caught that parser-side limits (`bulk_len_max`) must not be asserted on writer output; a
  `zig fmt` run reflowed command arrays past 100 columns (repack at a computed width); never
  run bare `git stash`/`stash pop` here without listing existing entries first.

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
