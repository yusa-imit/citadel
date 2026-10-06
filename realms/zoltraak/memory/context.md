# zoltraak — context

last_seen_at: 2026-10-07T00:00:00Z
rejected_plans: []

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

## Cycle 17 — 2026-10-05 — FEATURE (all plan items blocked)
- Preflight: tree was dirty on `chore/std-log-main-prints` (main.zig std.log work). Preserved
  on `wip/std-log-main-prints-20261005` (pushed), then landed as PR #140 from a fresh branch.
  main CI green on 53e76c1, no bugs, no plan PR, milestone #121 open, no owner comments.
- Items 4-9, 12 blocked (zuda v2.3.0, sailor v2.99.0; need v3.0.0).
- `/stabilize --one`: PR #140 moved main.zig's 21 `std.debug.print` to `std.log`; usage text via
  pure `usageText` (+2 tests). CI green, merged, labeled auto-merged. tidy `debug_print`
  main.zig = 0. Remaining `debug.print`: cli.zig 45 only. Local `zig build test`: 1108/1108,
  only the 2 known signal-4 RDB crashers (test_iter432/437).
- `FileNotFound` build-runner error recurred on a stale `.zig-cache`; `rm -rf .zig-cache` fixed
  it. Last cycle's hung local test did not recur.
- Next: cli.zig 45 debug.print (CLI output is product, not diagnostics: needs a stdout writer
  decision); stash triage (stash@{0} may fix the signal-4 crashers). Cycle 20 is forced
  STABILIZATION.
- Blockers: plan 001 items 4-9, 12 need zuda/sailor v3.0.0. Open questions: none.

## Cycle 16 — 2026-10-03 — FEATURE (all plan items blocked)
- Preflight clean (main, CI green on b866a4d), no bugs, no plan PR, milestone #121 open, no
  owner comments since watermark. Items 4-9, 12 blocked (zuda v2.3.0, sailor v2.99.0).
- `/stabilize --one`: PR #139 moved server.zig's 26 `std.debug.print` to `std.log`
  (warn/info, ANSI banner dropped), tidy baseline server.zig debug_print = 0. CI green
  (5m6s / 56s), merged, labeled auto-merged. Remaining `debug.print`: cli 45, main 21.
- Local `zig build test` HUNG: a test binary sat at 0% CPU for 14+ min (a leaked binary from
  `.zig-cache2` is hung 2 days too; pid 68879, not mine, left alone — kill it). Cause unknown;
  not caused by #139 (CI passed). Triage next stabilize: find the hanging test.
- README still says "Zig 0.15.0 or later"/"Planned Features"; rewrite is plan item 12.
- Next: main.zig/cli.zig debug.print; stash triage; hung local test.
- Blockers: plan 001 items 4-9, 12 need zuda/sailor v3.0.0. Open questions: none.

## Cycle 15 — 2026-10-02 — STABILIZATION (forced, n%5==0)
- Preflight clean (main, CI green on 5338de8), no bugs, no plan PR, milestone #121 open, no
  owner comments since watermark.
- Merged #137 (CI runs `zig fmt --check src build.zig`; green 6m50s / 50s), labeled auto-merged.
- Stabilize task: PR #138 moved 13 `std.debug.print` calls (storage, commands, scripting) to
  `std.log.warn/info`; tidy baseline `debug_print` = 0 for those 7 files. CI green, merged.
  Remaining `std.debug.print`: cli 45, server 26, main 21 (92 total). STATE.md updated.
- Local `zig build test` fixed by `rm -rf .zig-cache` (cycle 14's FileNotFound): 1106/1106,
  only the 2 known signal-4 RDB crashers (test_iter432/437) fail.
- Next: items 4-9, 12 still blocked (zuda/sailor need v3.0.0). Standing backlog: stash triage
  (stash@{0} may fix signal-4 crashers); debug.print in server.zig/main.zig/cli.zig.
- Guard hook: compound `cd repo; ...` / `timeout` / chained `sleep` blocked; run plain commands.
- Blockers: plan 001 items 4-9, 12 need zuda/sailor v3.0.0. Open questions: none.

## Cycle 14 — 2026-10-01 — FEATURE (all plan items blocked)
- Preflight clean (main, CI green on 5338de8), no bugs, no plan PR, milestone #121 open, no
  owner actions (only comment since watermark was our own cycle-13 report). Items 4-9, 12
  blocked (zuda v2.3.0, sailor v2.99.0; need v3.0.0).
- Ran `/stabilize --one`: PR #137 (`ci/zig-fmt-check`) adds `zig fmt --check src build.zig` to
  the Build & Test job. CI was still IN_PROGRESS at the deadline — NOT merged. Next cycle's
  inbox step 8 must merge #137 if green (label auto-merged), else fix.
- Local `zig build test` could not run: default cache failed "failed to spawn build runner
  ... FileNotFound"; deleting that cache entry did not help; a fresh `--cache-dir` build did
  not finish in 10 min. `zig fmt --check src build.zig` passed locally. Source tree identical
  to green main; only ci.yml changed. Next cycle: if it recurs, `rm -rf .zig-cache` (ignored).
- Standing backlog: stash triage (stash@{0} may fix signal-4 RDB crashes); 105
  `std.debug.print` (cli 45, server 26, main 21). Cycle 15 is forced STABILIZATION.
- Blockers: plan 001 items 4-9, 12 need zuda/sailor v3.0.0. Open questions: none.

## Cycle 13 — 2026-09-30 — FEATURE (all plan items blocked)
- Preflight clean (main, CI green on 165f481), no bugs, no plan PR, milestone #121 open, no
  owner comments since watermark. Items 4-9, 12 blocked (zuda v2.3.0, sailor v2.99.0).
- Ran `/stabilize --one`: PR #136 applied `zig fmt` to the 13 files that failed
  `zig fmt --check` (no logic change). `zig fmt --check src build.zig` now clean on main.
  eviction.zig WRITE_COMMANDS repacked 4/row (long_lines baseline 5 -> 2); baseline function
  lengths raised for cmdFtSpellcheck 158, cmdObject 270, cmdHexpire 119, cmdHpexpire 115,
  cmdHexpireat 112, cmdHpexpireat 110 (fmt split packed `a; b;` statements; no new code).
  CI green (5m19s / 49s), merged, labeled auto-merged.
- Local `zig build test` (0.15.2): 1106/1106 tests pass; only the 2 known signal-4 RDB
  crashers (test_iter432/437) fail.
- Next: fmt is still not a CI step — consider adding `zig fmt --check` to ci.yml (CI edit in
  a realm pre-migration is allowed only as a targeted fix; keep separate PR). Triage the 3
  cycle-1 stashes (stash@{0} may fix signal-4 crashes). Cycle 15 is forced STABILIZATION.
- Blockers: plan 001 items 4-9, 12 need zuda/sailor v3.0.0. Open questions: none.
- `gh pr create --label chore` fails: no `chore` label exists in the repo; omit it.

## Cycle 12 — 2026-09-29 — FEATURE (all plan items blocked)
- Preflight: dirty tree on main (six files with new `//!` headers, interrupted work).
  Preserved on `wip/module-headers-20260929`, then landed as PR #135 (+ tidy-baseline
  `header_missing` shrink for those 6 files). CI green (6m55s / 59s), merged.
- Inbox: no owner actions, no plan PR, milestone #121. Synced its checkboxes (items 3, 11 done).
- Items 4-9, 12 still blocked (zuda v2.3.0, sailor v2.99.0; need v3.0.0).
- Found: `zig fmt --check src build.zig` fails on 13 files on main (storage: search, jsonpath,
  functions, eviction, listpack, tls_config; commands: search, keys, json, sets, timeseries,
  hashes, cms). CI does not run fmt. Next stabilize task: fix them, mind the 100-col tidy
  baseline (cycle 8 lesson: fmt reflows command arrays).
- Guard hook blocks compound `cd repo; ...` and heredoc writes to citadel; use Write/Edit tools.
- Next: fmt fix PR; stash triage (stash@{0} may fix signal-4 RDB crashes). Open questions: none.

- Cycles 10-14 (2026-09-17 to 10-01): plan 001 items 4-9, 12 stay blocked on zuda/sailor v3.0.0.
  Cycle 10 tidy-auditor caught 2 unproven `catch unreachable` in `storage/memory.zig` (PR #133).
  Cycle 11 removed 2 stale TODO blocks (PR #134). Cycle 12 landed `//!` headers (PR #135, via
  `wip/module-headers-20260929`). Cycle 13 ran `zig fmt` on 13 files (PR #136; baseline function
  lengths raised for the fmt-split `cmd*` functions). Cycle 14 opened PR #137 adding
  `zig fmt --check src build.zig` to CI (merge if green). `memory.zig` is 16,248 lines.
  Quirks: local `zig build test` hits 2 signal-4 RDB crashers (test_iter432/437) while CI
  passes; 3 cycle-1 stashes untriaged (stash@{0} may fix them); if the build runner fails with
  FileNotFound, `rm -rf .zig-cache`; `gh pr create --label chore` fails (no such label); the guard
  hook blocks compound `cd`, heredocs and `>` redirects to /tmp.

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
