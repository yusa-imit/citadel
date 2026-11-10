# zoltraak — context

last_seen_at: 2026-11-11T00:00:00Z
rejected_plans: []

## Cycle 51 — 2026-11-11 — FEATURE (all plan items blocked)
- Disk 21 GB (gate passed barely). CI green on main (909d7a3), no bugs, no OWNER comments, no open PRs;
  milestone #121 open. zuda still v2.3.0, so items 4-9, 12 blocked: ran `/stabilize --one`.
- PR #170 (merged, auto-merged): `storage/aof.zig` 3 `== error.`/`!= error.` -> `switch (err)` with
  `else => return err` (callee sets are std/inferred). `== error.` in `src/` 14 -> 11. `zig build test`
  1627/1627 except the 2 known signal-4 crashers; fmt and `zig build tidy` clean.
- Lesson: the first test run failed `tidy`: the added switch lines grew `executeStorageCommand` 115 -> 117
  lines past its baseline. Extracted `replayRestore` helper to fix. Run `zig build tidy` before the long
  test run; adding lines inside a baselined long function fails it.
- Next: `tdigest.zig` 2, `main.zig` 2, then 1 each (redis_api, storage/functions, persistence, utility,
  streams, cluster, client); `//!` headers (82 files); stash triage. Blockers: zuda v3.0.0. Questions: none.
- Quirks: the guard blocks `cd repo; ...` compounds (run git/gh as separate calls from the repo cwd);
  `gh pr checks --watch` right after PR creation says "no checks"; rerun it.

## Cycle 50 — 2026-11-10 — NOOP (disk gate)
- Disk 13 GB < 20 GB gate: stopped at preflight, nothing checked (CI, issues, PRs unread). Repo clean on
  main (909d7a3). Third disk NOOP of the last four cycles (47, 48 earlier). n % 5 == 0 would have been
  STABILIZATION. Next: first cycle with disk >= 20 GB resumes `aof.zig` 3, `tdigest.zig` 2, `main.zig` 2
  (`== error.`); `//!` headers (82 files); stash triage. Blockers: disk (human must free space), zuda
  v3.0.0. Questions: none.

## Cycle 49 — 2026-11-09 — FEATURE (all plan items blocked)
- Disk 23 GB. CI green on main (6c50e2c), no bugs, no OWNER comments, no open PRs; milestone #121 open.
  zuda still v2.3.0 (sailor v3.1.0), so items 4-9, 12 blocked: ran `/stabilize --one`.
- PR #169 (merged, auto-merged): `commands/functions.zig` 4 `err == error.X` -> `switch (err)`; callee sets read
  first (`removeLibrary` {LibraryNotFound}; `addLibrary` adds LibraryExists, FunctionExists, OutOfMemory), so no
  `else`. File-level message consts keep lines under 100 columns. `== error.` in `src/` 18 -> 14 (incl. tests).
  `zig build test` 1627/1627 except the 2 known signal-4 crashers; fmt and `zig build tidy` clean.
- Next: `aof.zig` 3, `tdigest.zig` 2, `main.zig` 2 (`== error.`); `//!` headers (82 files); stash triage.
  Blockers: zuda v3.0.0. Questions: none.
- Quirks: `zig build tidy` does not compile code; only `zig build test` proves a switch is exhaustive. The guard
  blocks compounds mixing citadel paths with repo commands (separate calls). `gh pr merge --delete-branch` plus a
  separate `gh pr edit --add-label auto-merged` worked.

## Cycle 48 — 2026-11-08 — NOOP (disk gate)
- Disk 18 GB < 20 GB gate: stopped at preflight, nothing checked (CI, issues, PRs unread). Repo clean on
  main. Second disk NOOP in a row (cycle 47 too). Next: first cycle with disk >= 20 GB resumes
  `commands/functions.zig` 4, `aof.zig` 3 (`== error.`), `//!` headers (82 files), stash triage.
  Blockers: disk (human must free space), zuda v3.0.0. Questions: none.
- Quirk: the guard blocks a compound `cd ... && python3 - <<EOF` write in citadel; use Write/Edit.

## Cycle 47 — 2026-11-07 — NOOP (disk gate)
- Disk 13 GB < 20 GB gate: stopped at preflight, nothing checked (CI, issues, PRs unread). Repo clean on
  main. Same as cycles 34 and 42. Next: first cycle with disk >= 20 GB resumes `commands/functions.zig` 4,
  `aof.zig` 3 (`== error.`), `//!` headers (82 files), stash triage. Blockers: disk, zuda v3.0.0.
  Questions: none.

## Cycle 46 — 2026-11-06 — FEATURE (all plan items blocked)
- CI green on main (681823f), no bugs, no OWNER comments, no open PRs; milestone #121 open. zuda still
  v2.3.0, so items 4-9, 12 blocked: ran `/stabilize --one`. Disk 23 GB.
- PR #168 (merged, auto-merged): `commands/timeseries.zig` 4 `err == error.DuplicateTimestamp` -> `switch (err)`
  (callee sets are DuplicateTimestamp + OutOfMemory, so no `else`); file-level `duplicate_blocked_message`
  keeps lines under 100 columns. `== error.` in `src/` 22 -> 18. `zig build test` 1627/1627 except the 2
  known signal-4 crashers; fmt and `zig build tidy` clean.
- Next: `commands/functions.zig` 4, `aof.zig` 3 (`== error.`); `//!` headers (82 files); stash triage.
  Blockers: zuda v3.0.0. Questions: none.
- Quirks: the guard blocks `sleep` before `gh pr checks --watch`; run the watch alone.

## Cycle 45 — 2026-11-05 — STABILIZATION (n % 5)
- CI green on main (8b2e7d5, last 5 runs), no bugs, no OWNER comments, no open PRs; milestone #121 open.
  zuda still v2.3.0, so items 4-9, 12 stay blocked. Disk 29 GB.
- PR #167 (merged, auto-merged): `commands/search.zig` 6 `err == error.X` -> `switch (err)` with
  `else => return err` (callee error sets are inferred; read them first). `== error.` in `src/` 28 -> 22.
  `zig build test` 1627/1627 except the 2 known signal-4 crashers; fmt and `zig build tidy` clean.
- Next: `timeseries.zig` 4, `commands/functions.zig` 4, `aof.zig` 3 (`== error.`); `//!` headers (82
  files); stash triage. Blockers: zuda v3.0.0. Questions: none.
- Quirks: the guard blocks compound commands mixing citadel paths with repo commands (preflight reads
  must be separate). `gh pr checks --watch` right after pushing may say "no checks"; rerun it.

## Cycle 44 — 2026-11-04 — FEATURE (all plan items blocked)
- CI green on main (54d65b1), no bugs, no OWNER comments, no open PRs; milestone #121 open. zuda still
  v2.3.0 (sailor is v3.1.0), so items 4-9, 12 blocked: ran `/stabilize --one`.
- PR #166 (merged, auto-merged): `commands/strings.zig` 7 `err == error.WrongType` -> `switch (err)` with a
  file-level `wrongtype_message` const. `== error.` in `src/` 35 -> 28. `zig build test` 1627/1627 except
  the 2 known signal-4 crashers; fmt and `zig build tidy` clean.
- Next: `search.zig` 6 (`== error.`); `//!` headers (82 files); stash triage. Blockers: zuda v3.0.0.
  Questions: none.
- Quirks: `gh pr create` and `gh pr merge` hit transient GraphQL errors; retry (check `gh pr view` state
  first, the merge may not have happened). `rm -rf .zig-cache` was needed again for `FileNotFound`. The
  guard blocks writing `/tmp` start-time files in a compound command with citadel paths.

## Cycle 43 — 2026-11-03 — FEATURE (all plan items blocked)
- Disk 21 GB (gate passed barely). CI green on main (be6ae4c), no bugs, no OWNER comments, no open PRs;
  milestone #121 open. zuda still v2.3.0, so items 4-9, 12 blocked: ran `/stabilize --one`.
- PR #165 (merged, auto-merged): `commands/sentinel.zig` 8 `err == error.X` -> `switch (err)`. The compiler
  proved the `else` prongs of REMOVE, FAILOVER, CKQUORUM, SET dead (inferred error sets hold only the named
  errors), so they were dropped; MONITOR and FLUSHCONFIG keep `else` (OOM / fs errors). `== error.` in
  `src/` 43 -> 35. `zig build test` 1627/1627 except the 2 known signal-4 crashers; fmt clean.
- Next: `strings.zig` 7, `search.zig` 6 (`== error.`); `//!` headers (82 files); stash triage.
  Blockers: zuda v3.0.0. Questions: none.
- Lesson: reading the callee's body for its error set before writing `else` saves rebuilds; each wrong
  `else` costs a build. Two `zig build test` runs writing one log file confuse monitors: use a fresh log
  name per run.

## Cycles 40-42 (2026-10-31..11-02), folded 2026-11-04
- zuda still v2.3.0, so plan items 4-9, 12 stayed blocked; each FEATURE/STABILIZATION cycle ran
  `/stabilize --one`; `zig build test` 1627/1627 except the 2 known signal-4 crashers; fmt, tidy clean.
- 40 (PR #163): `hashes.zig` 11 `err == error.WrongType` -> `switch (err)` (perl multi-line regex),
  `== error.` in `src/` 86 -> 75. 41 (PR #164): `sorted_sets.zig` 32 sites -> 43; a file-level
  `wrongtype_message` const keeps long WRONGTYPE prongs under tidy's 100-column and function-length
  baselines. 42: NOOP at the disk gate (18 GB < 20 GB), nothing checked.
- Quirk: `gh pr checks --watch` works for CI waits (a `sleep` + until chain is blocked by the guard).

## Cycles 13-39 (2026-09-30..10-30), folded 2026-11-06
Plan 001 items 4-9, 12 were blocked on zuda/sailor v3.0.0 the whole time (zuda still v2.3.0), so each
FEATURE/STABILIZATION cycle ran one `/stabilize --one`; every PR merged with CI green and `auto-merged`.
`zig build test` stays 1627/1627 except the 2 known signal-4 RDB crashers (`test_iter432`/`437`).
- 13-17: `zig fmt` pass (#136), `zig fmt --check` in CI (#137), all `std.debug.print` in `src/` moved to
  `std.log` (#138-#140; the dirty `chore/std-log-main-prints` was kept as `wip/std-log-main-prints-
  20261005`). cli.zig prints are product output (stdout writer, #142).
- 18-28 root finding (C20): `src/` has 2659 `test` blocks but `zig build test` ran 1114, because Zig runs
  `test` blocks only for files something analyzes. Fix pattern: wire one file at a time with an
  `_ = @import` in the `src/main.zig` reachability test (1114 -> 1519 by C28); bulk-wiring all 84 files
  does not compile. PRs #142-#152 wired topk, heavykeeper, encodings, listpack, slowlog, cms, scripting,
  vector, defrag, bloom, functions, cuckoo and fixed real bugs (`CMS.INCRBY` i64-min trap, tdigest `cdf`,
  leak in `SentinelState.resetMaster`, bounded `heapifyDown`). Probe with `zig test src/<f>.zig`: search,
  cluster, config, tls_config, acl, timeseries, modules, pubsub, blocking, lazyfree, notifications, aof,
  replication, persistence, eviction do not compile standalone (module path / `zuda` / stale tests).
  Issue #141 (`migration: sailor v3.0.0`) waits for the 0.16 toolchain.
- 29-33 (#153-#157): notifications tests (a DNS flake needs `gh run rerun --failed`); bounded reply read
  `src/network/reply_line.zig` (`reply_line_max` 4096); `WAIT 1 18446744073709551615` overflow trap fixed
  in `src/utils/wait_poll.zig`; XREAD BLOCK bounded by `src/utils/block_poll.zig`; `luaToRESP2Buf` scan in
  `src/scripting/lua_array.zig`. Wiring lazyfree.zig or blocking.zig drags in memory.zig's stale test
  suite (66 errors), plus search 110, config 59, modules 41, acl 30, cluster 39: repair one file at a
  time, memory.zig first. Tests in `commands/*.zig` do not run (they import memory.zig): put testable
  logic in a standalone file and wire it into `src/main.zig`; mutate the code once to prove a test runs.
- 34: NOOP at the disk gate (15 GB). 35 (STABILIZATION): recount `catch unreachable` 26 all with proof,
  `@panic` 0, `std.debug.print` 0, `while (true)` 3, `//!` missing 82/88, `== error.` 115; #158 split
  compound asserts. 36-39 (#159-#162): `bloom.zig` scanDump bounded, `== error.` -> exhaustive `switch
  (err)` in server.zig, lists.zig, sets.zig. Flake: `test_iter347` (ACL DRYRUN) hung at 0 CPU once.
- Open: `while (true)` at server.zig:575, cli.zig:108 (probably legit), bloom.zig:826 (test loop),
  streams_advanced.zig:446,735 sleep-polls; stash triage (`stash@{0}`); repair memory.zig stale suite.
- Quirks: full `zig build test` takes ~8 min and buffers output (use `run_in_background` plus a Monitor
  on `Build Summary`); `rm -rf .zig-cache` fixes the `FileNotFound` build-runner error; BSD sed has no
  `\s` and `-i` needs `''`, anchor patterns (an unanchored delete removed the real `pub const blocking`
  line in main.zig), use Edit for mutation checks; the guard blocks compound commands mixing citadel
  paths with repo commands, `git -C <other repo>`, `timeout`, chained `sleep`; `gh pr create --label
  chore` fails (no label), GraphQL errors are transient.

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
