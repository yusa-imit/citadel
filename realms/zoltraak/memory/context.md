# zoltraak — context

last_seen_at: 2026-10-10T00:00:00Z
rejected_plans: []

## Cycle 22 — 2026-10-10 — FEATURE (all plan items blocked)
- Preflight clean (main, CI green on 57cacc9), no bugs, no plan PR, milestone #121 open, no
  owner comments. zuda still v2.3.0, so items 4-9, 12 blocked.
- `/stabilize --one`: PR #146. Real bug: `CMS.INCRBY key item -9223372036854775808` trapped on
  `-delta` (integer overflow) in `CountMinSketchValue.incrBy`; now `@abs`, returns
  CounterUnderflow (regression test first). Stale overflow test fixed (counters are u64).
  Wired cms, scripting, json_value, vector, defrag into the `src/main.zig` reachability test:
  `zig build test` 1207 -> 1275, only the 2 known signal-4 crashers. CI green (4m22s / 47s),
  merged, labeled auto-merged.
- Probe results (`zig test src/storage/<f>.zig`): jsonpath has 1 stale failing test (parse
  ".a.b" -> InvalidPathSyntax; decide test vs parser); bloom has a compile error
  (LoadContext); aof/replication/persistence/eviction need module wiring (import outside
  module path).
- Not mine: `./zig-out/bin/zoltraak` pid 80225 still running; left alone.
- Next: jsonpath/bloom repair then wire; commands/*.zig stale tests; stash triage
  (stash@{0}); cycle 25 is forced STABILIZATION. Items 4-9, 12 unblock on zuda v3.0.0.
- Blockers: zuda v3.0.0. Open questions: none.

## Cycle 21 — 2026-10-09 — FEATURE (all plan items blocked)
- Preflight clean (main, CI green on 6e5a6e3), no bugs, no plan PR, milestone #121 open, no
  owner comments. zuda still v2.3.0 (GitHub + local), so items 4-9, 12 blocked.
- Inbox: merged #144 (CI had passed; labeled auto-merged) — topk/heavykeeper tests now run.
- `/stabilize --one`: PR #145 added encodings, listpack, memory_tracker, slowlog, intset,
  latency to the `src/main.zig` reachability test: `zig build test` 1160 -> 1207, all pass,
  only the 2 known signal-4 crashers locally. CI green (6m52s / 1m28s), merged, labeled.
- Probe trick: `zig test src/<f>.zig` standalone shows whether a file's tests compile; blocking,
  lazyfree, notifications fail there (import outside module path / `zuda`) so they need
  build-module wiring, not a bare import-test.
- Not mine: `./zig-out/bin/zoltraak` pid 80225 running 3 days; left alone.
- Next: wire further files one at a time (commands/*.zig stale tests need repair); stash triage
  (stash@{0}); cycle 25 is forced STABILIZATION. Items 4-9, 12 unblock on zuda v3.0.0.
- Blockers: zuda v3.0.0. Open questions: none.

## Cycle 20 — 2026-10-08 — STABILIZATION (forced, n%5==0)
- Preflight clean (main, CI green on 6e5a6e3), no bugs, no plan PR, milestone #121 open, no
  owner comments. zuda still v2.3.0 (sailor v3.0.0 tagged, #141 open), items 4-9, 12 blocked.
- Finding: Zig runs `test` blocks only for files something analyzes. `src/` has 2659 `test`
  blocks but `zig build test` runs 1114. Referencing storage/topk.zig + heavykeeper.zig from a
  `src/main.zig` test block gave 1160/1160 (+45; includes #143's heap-order tests).
- PR #144 (`test/unit-test-reachability`) does exactly that. Local green (1160/1160, only the 2
  known signal-4 crashers); CI was still pending at the deadline — NOT merged. Next cycle's
  inbox step 8 must merge it if green, else fix.
- Bulk-referencing all 84 other src files does NOT compile: stale tests (commands/acl.zig:
  arity, `**Storage`, const-ptr, plus a 32-arg format limit error). Wire one file at a time and
  repair its tests; a full-tree `zig build test` error dump took >10 min, so grep one file.
- Guard hook blocks compound `cd repo; ...`; `gh pr create` hit a transient GraphQL error, retry.
- Next: merge #144; wire next file (smallest test counts first); stash triage (stash@{0}).
- Blockers: zuda v3.0.0. Open questions: none.

## Cycle 19 — 2026-10-07 — FEATURE (all plan items blocked)
- Preflight clean (main, CI green on b49036f), no bugs, no plan PR, milestone #121 open, no
  owner comments since watermark. zuda still v2.3.0 (GitHub + local), so items 4-9, 12 blocked.
- `/stabilize --one`: PR #143 bounded `TopKValue.heapifyDown` and `HeavyKeeper.heapifyDown`
  (`for (0..@bitSizeOf(usize))` + `else unreachable` with proof comment), +1 heap-order test
  each. CI green (6m54s / 1m6s), merged, labeled auto-merged. `while (true)` in `src/`: 11 -> 9.
  Local `zig build test`: 1114/1114, only the 2 known signal-4 crashers; tidy clean.
- Finding: the new unit tests pass under `zig test src/storage/topk.zig` but the `zig build test`
  total did not grow, so `storage/topk.zig` and `storage/heavykeeper.zig` unit tests may not be
  reachable from the `src/main.zig` test root. Verify and wire them in (could apply to more files).
- Guard hook blocks `git -C <other repo> fetch` and `echo > /tmp/..` in a realm session; plain
  read-only `git -C zuda tag -l` or `gh api repos/.../tags` works. BSD sed: no multi-line patterns.
- Next: cycle 20 is forced STABILIZATION (n%5==0): verify unit-test reachability; stash triage
  (stash@{0} may fix the signal-4 RDB crashers). Items 4-9, 12 unblock on zuda v3.0.0.
- Blockers: zuda v3.0.0. Open questions: none.

## Cycle 18 — 2026-10-06 — FEATURE (all plan items blocked)
- Preflight clean (main, CI green on cca0098), no bugs, no plan PR, milestone #121 open, no
  owner comments. New issue #141 (`migration: sailor v3.0.0`, opened by the release cycle):
  sailor v3.0.0 is tagged, but zuda is still v2.3.0, and the pin bump needs the 0.16
  toolchain, so items 4-9, 12 stay blocked (item 10 needs both tags).
- `/stabilize --one`: PR #142 — `zoltraak-cli` printed replies via `std.debug.print` (stderr),
  so `--json/--csv/--raw` could not be piped. Replies/prompts now use a buffered stdout writer;
  formatters take `*std.Io.Writer`; `run_repl` extracted (tidy ceiling on `main`). `cli.zig` is
  now in `zig build test` (6 formatter tests). tidy `debug_print` cli.zig 45 -> 0, so the
  kingdom-wide `std.debug.print` count in `src/` is 0. CI green (4m17s / 58s), merged,
  labeled auto-merged. Local `zig build test`: 1114/1114, only the 2 known signal-4 crashers.
- Guard hook blocks chained `gh pr merge ...; ...` commands; run merge/label/checkout as
  separate plain commands.
- Next: stash triage (stash@{0} may fix the signal-4 RDB crashers). Items 4-9, 12 unblock when
  zuda v3.0.0 is tagged; then bump both pins together (#141 has the sailor migration notes).
  Cycle 20 is forced STABILIZATION.
- Blockers: zuda v3.0.0. Open questions: none.

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
