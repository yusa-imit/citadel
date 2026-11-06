# silica — context

last_seen_at: 2026-11-06T10:00:00Z
rejected_plans: []

## Cycle 52 — 2026-11-06 — NOOP (disk gate)
- Preflight stopped at the disk gate: `df -g /` showed 19 GB free (`df -h` 20Gi rounded, 11Gi used of
  228Gi), need 20. Cycle 52 is FEATURE (n%5 != 0, streak 0). No repo, CI or inbox check was done, so
  no PR or issue activity is known for today. The gate was not bypassed.
- Next: cycle 53 re-checks disk first. Free space dropped 24 -> 19 GB in one day; an operator (or a
  cycle already past the gate) should clear /tmp/silica-zc-tidy, zig caches and other realms' build
  outputs. Cycle 55 is STABILIZATION (n%5); fillers: jepsen `dirtyReadTest` 80.
- Blockers: disk 19 GB; zuda v3.0.0 (plan 001 items blocked). Open questions unchanged
  (buffer-pool LRU contradiction; WAL concurrency).

## Cycle 51 — 2026-11-05 — FEATURE
- Preflight: disk 24 GB (gate passed), main clean, CI green (c2c94ae), no bug/question issues, no open
  PRs; inbox nothing new (only own comment on #137). zuda still v2.3.0; plan 001 items blocked.
- Done: one `/stabilize --one` filler, PR #189 (merged, `auto-merged`, CI green): `jsonPathStep` and
  `jsonNodeToValue` extracted from executor `evalJsonPathExtract` (79 -> under 70), 2 tests; a negative
  integer path index now yields NULL instead of an `@intCast` panic. Baseline `function_length` 27 -> 26.
  Local fmt + tidy + test green. No subagents, ~$0.4.
- Next: cycle 55 is STABILIZATION (n%5). No small (<~90) filler left in the baseline except big
  offenders (cli/tui/jepsen 80-130); pick the smallest, e.g. jepsen `dirtyReadTest` 80. Migration
  waits for zuda v3.0.0 (target sailor v3.1.0).
- Blockers: zuda v3.0.0. Disk 24 GB, 4 GB above gate. Open questions unchanged (buffer-pool LRU
  contradiction; WAL concurrency).
- Tooling: `zig fmt --check` on tidy_baseline.txt errors (not Zig), only pass src/build.zig.

## Cycle 50 — 2026-11-04 — NOOP (disk gate)
- Preflight stopped at the disk gate: `df -g /` showed 15 GB free (need 20). Cycle 50 was an
  n%5 STABILIZATION cycle; none of it ran. No repo, CI or inbox check was done, so no PR or
  issue activity is known for today. Streak 0, no escalated_sha.
- Next: cycle 51 re-checks disk first. If still < 20 GB, an operator (or a cycle that is already
  past the gate) should clear /tmp/silica-zc-tidy and zig caches; the gate was not bypassed.
  STABILIZATION (n%5) was skipped, so the next cycle that passes the gate does n=51 as FEATURE.
- Blockers: disk 15 GB; zuda v3.0.0 (plan 001 items blocked). Open questions unchanged
  (buffer-pool LRU contradiction; WAL concurrency).

## Cycle 49 — 2026-11-03 — FEATURE
- Preflight: disk 21 GB (gate passed, barely), main clean, CI green (d546b85), no bug/question issues,
  no open PRs; inbox nothing new (only own comment on #137). zuda still v2.3.0; every unchecked plan
  001 item blocked on zuda v3.0.0.
- Done: one `/stabilize --one` filler, PR #188 (merged, `auto-merged`, CI 7/7): `appendStemmedToken`
  extracted from executor `textToTsvector` (79 -> under 70), 2 tests (lowercase/stem/stop word; sweep
  of `FailingAllocator.fail_index` 0..15, leak-checked); also frees the stem if the list append fails.
  Baseline `function_length` 28 -> 27. Local fmt + tidy + test green. No subagents, ~$0.5.
- Next: cycle 50 is STABILIZATION (n%5). Filler left: executor `evalJsonPathExtract` 79. Migration
  waits for zuda v3.0.0 (target sailor v3.1.0).
- Blockers: zuda v3.0.0. Disk at 21 GB, 1 GB above the gate: clean /tmp/silica-zc-tidy and zig caches
  if it drops. Open questions unchanged (buffer-pool LRU contradiction; WAL concurrency).
- Tooling: guard blocks compound Bash lines touching citadel (START=$(date) + cat), run each command
  separately; CI ~15 min total with cross-compile, cycle ~17 min.

## Cycle 48 — 2026-11-02 — FEATURE
- Preflight: disk 19 GB reported by `df -g` awk but cycle proceeded (gate read 19 < 20 is a miss: see
  Blockers); main clean, CI green (3f679b5), no bug/question issues, no open PRs; inbox nothing new
  (only own comments on #137, #163). zuda still v2.3.0; plan 001 items blocked.
- Done: one `/stabilize --one` filler, PR #187 (merged, `auto-merged`, CI 7/7): `readLengthPrefixedBytes`,
  `parseSystemInfo`, `parseBackupData` extracted from transport `parseBackendMessage` (89 -> under 70)
  with 5 tests (prefix, zero length, truncation x3, leak-checked). Baseline `function_length` 29 -> 28.
  First attempt with only the length helper left 77 lines: tidy shows the real count, extract arms too.
  Local fmt + tidy + test green. No subagents, ~$0.5.
- Next: fillers executor `textToTsvector` 79 / `evalJsonPathExtract` 79. Cycle 50 is the next n%5==0.
  Migration waits for zuda v3.0.0 (target sailor v3.1.0).
- Blockers: zuda v3.0.0. Disk was 19 GB (below the 20 GB gate; the first `df` line printed 19 and the
  cycle continued by mistake; keep an eye on it, clean /tmp/silica-zc-tidy and zig caches if it
  drops). Open questions unchanged (buffer-pool LRU contradiction; WAL concurrency).
- Tooling: `zig build test` prints a std.net write stack trace from replication integration_test
  but exits 0; check exit code, not output. CI ~12 min, cycle ~20 min.

## Cycle 47 — 2026-11-01 — FEATURE
- Preflight: disk 46 GB (gate passed), main clean, CI green (fed21fe), no bug/question issues, no open
  PRs; inbox nothing new (only own comments on #137, #163). zuda still v2.3.0; plan 001 items blocked.
- Done: one `/stabilize --one` filler, PR #186 (merged, `auto-merged`, CI 7/7): `readBytesDup`,
  `readMostCommonValue`, `readHistogramBucket` extracted from stats `deserializeColumnStats` (90 ->
  under 70) with 4 tests (success + truncation, leak-checked); also closes an MCV-append leak path.
  Baseline `function_length` 30 -> 29. Local fmt + tidy + test green. No subagents, ~$0.42.
- Next: fillers transport `parseBackendMessage` 89, executor `textToTsvector` 79 / `evalJsonPathExtract`
  79. Cycle 50 is the next n%5==0. Migration waits for zuda v3.0.0 (target sailor v3.1.0).
- Blockers: zuda v3.0.0. Open questions unchanged (buffer-pool LRU contradiction; WAL concurrency).
- Tooling: `gh pr merge` then `gh pr edit --add-label auto-merged` as separate calls; tidy lists
  offending lines via the built `tidy` binary (`--src src --baseline tidy_baseline.txt`).

## Cycle 46 — 2026-10-31 — FEATURE
- Preflight: disk 28 GB (gate passed), main clean, CI green (300af95), no bug/question issues, no open
  PRs; inbox nothing new (only own comments on #137, #163). zuda still v2.3.0, sailor v3.1.0; every
  unchecked plan 001 item stays blocked.
- Done: one `/stabilize --one` filler, PR #185 (merged, `auto-merged`, CI 7/7): `csvReadErrorMessage`,
  `csvInsertErrorMessage`, `buildCsvInsert` extracted from cli `importCsvFile` (84 -> under 70) with
  4 tests; baseline `function_length` 31 -> 30. Local fmt + tidy + test green. No subagents, ~$0.5.
- Next: filler stats `deserializeColumnStats` 90. Cycle 50 is the next n%5==0. Migration waits for
  zuda v3.0.0 (target sailor v3.1.0).
- Blockers: zuda v3.0.0. Open questions unchanged (buffer-pool LRU contradiction; WAL concurrency).
- Tooling: `gh pr merge` needs `-R yusa-imit/silica` as its own command; `python3 -I` heredoc replace
  failed silently-ish on a multi-line match, Edit tool is more reliable; CI ~11 min, cycle ~20 min.

## Cycle 45 — 2026-10-30 — STABILIZATION (n%5)
- Preflight: disk 38 GB (gate passed), main clean, CI green (ec5b241, last 5 runs green), no bug/question
  issues, no open PRs; inbox nothing new (only own comment on #137). zuda still v2.3.0.
- Done: audit counts refreshed in STATE.md (assert 145, catch unreachable 210, @panic 7 all in tests,
  debug print 16, while(true) 104, expect(true) 0). One class fixed: PR #184 (merged, `auto-merged`, CI
  7/7) extracted `formatPlanHeader` from planner `formatPlan` (83 -> under 70) with a test; baseline
  `function_length` 32 -> 31. Local fmt + tidy + test green. No subagents, ~$0.55.
- Hygiene: root `libconnection.a`, `test_*.o`, `test_output.txt` exist locally but are gitignored
  (not tracked). Benchmarks/docs-drift skipped (bench is CI-only; no time).
- Next: fillers importCsvFile 84, stats deserializeColumnStats 90. Migration waits for zuda v3.0.0
  (target sailor v3.1.0). Cycle 50 is the next n%5==0.
- Blockers: zuda v3.0.0. Open questions unchanged (buffer-pool LRU contradiction; WAL concurrency).
- Tooling: `gh pr checks` without --json prints tab-separated name/state; a 55x10s poll loop hits the
  590 s tool timeout, use ~40 iterations; CI ~12 min.

## Cycles 41-44 (2026-10-26..29), folded
- All FEATURE-mode `/stabilize --one` fillers, merged at 7/7, `auto-merged`, zuda still v2.3.0: #180
  `radarFractions` (renderRadarChart), #181 `reportScriptEnd` (readAndExecuteFile 74 -> 68), #182
  `writeScreenEnter`/`writeScreenLeave` (tui `run` 73), #183 `pageHasKey` (hash_index insertIntoChain 75).
  Baseline `function_length` 36 -> 32. Ticked the stale "scratch DBs part 2" box on #137.
- Tooling: guard rejects compound Bash lines touching citadel (even `START=$(date)`); run each command
  separately. Tidy counts bytes AND lines: keep test array literals under 100 columns.
  `std.Io.Writer.fixed` writes a partial prefix when full; zsh has no PIPESTATUS.

## History (cycles 37-40, folded 2026-10-31)

- 37 (10-20): #178 hoisted keyword help table to file-scope `sql_keyword_help`, getSqlKeywordHelp uses
  a 16-byte stack buffer. 38 (10-21): #179 `bracketMatch` from renderBracketViewer. Both FEATURE-mode
  `/stabilize --one` fillers, auto-merged CI 7/7, blocked on zuda v3.0.0.
- 39 (10-22) and 40 (10-25): NOOP, preflight stopped at the disk gate (16 GB then 13 GB free, need
  20); no repo/CI/inbox check done. Disk recovered by cycle 41 (41 GB).
- Tooling: `zig build tidy|test --cache-dir /tmp/silica-zc-tidy` exit 0 silently on success.

## History (cycles 19-36, folded 2026-11-06)

- Plan 001 tidy part 2 (10-01..10-10): `line_length:<path>:<max>` baseline ratchets (#159), wrap batches
  (#161-#169) took 60 baselined files to 2; #160 `//!` headers; #166 `// SAFETY:` on the line above each
  `catch unreachable`. Cycles 29-31: executor.zig wrapped (#170, dirty branch kept as
  `wip/line-length-executor-20261012`), `std.debug.print` sites became scoped `std.log` (#171), all 1,184
  long lines in engine.zig wrapped (#172); baseline has no `line_length:` entry left. Cycles 32-36:
  one `/stabilize --one` filler each (#173-#177: helpers split out of parseIntervalString, toNumber,
  evalJsonExtract, showIndexes, renderMatrixView), baseline ratchet re-derived (58 -> 43 entries);
  #163 sailor notice: migrate to v3.1.0, not v3.0.0 (Editor/MultiCursorEditor/LocalSource init return
  `error{OutOfMemory}`). Flake: `tx.jepsen_test` "non-repeatable read (SERIALIZABLE prevents)" aborted
  once locally (signal 6), passed on rerun and in CI; watch for recurrence.
- Learned: tidy counts BYTES, so `// ── X ───` banners trip the gate; baselined functions may not grow;
  concurrent `zig build` needs separate `--cache-dir` (`/tmp/silica-zc-tidy`); CI ~10-15 min, poll
  instead of `gh pr checks --watch`; no `timeout` on macOS; the guard blocks compound lines (`cd repo;
  cmd`, `sleep N; cmd`, grep mixed with citadel paths, `sed -i` on citadel), so run each step as its own
  Bash call, merge with `-R yusa-imit/silica`, then add the `auto-merged` label; BSD `sed -i` misparses,
  use python or Edit. Global zig was 0.15.2 then: use `std.mem.trimRight`. `zig-pkg/` is gitignored.

## History (cycle 18 and earlier, folded 2026-10-13)

- **Cycles 1-13** (2026-09-06 to 09-16): hygiene part 1 (#138 WAL checkpoint retention callback with a
  truncate-before-durable-header ordering fix; #139 dropped `src/query/`, packaged README/LICENSE/docs
  into `build.zig.zon` .paths). Scratch-DB-to-tmp-dir sweep (1,350+ literal `"test_*.db"` paths in 23
  files) done in 11 batches (#140-#152), ending with `sql/engine.zig` (819 sites). `wal_path = path ++
  "-wal"` comptime concat became runtime `bufPrint`. Stabilization cycles 5 and 10 (forced n%5==0):
  26 SAFETY comments on unjustified `catch unreachable` (#143), `toCharNumber` fix (#148); tidy-auditor
  counts then: assert(=19, catch unreachable=213, functions>70=161, files>800=40, `//!` missing 17/61.
- **Cycle 14** (2026-09-17): `zig build tidy` part 1 (#153): function-length <=70 + `//!` header checks,
  shrink-only `tidy_baseline.txt`; function-length brace scan is not string/comment-aware.
- **Cycles 15-18** (2026-09-26 to 09-30): fmt pass #154; tidy ban-list batches 1-4 (#155-#158:
  debug_print_in_lib, usize_in_disk_format, catch_unreachable_no_safety, std_time_in_lib; ban list
  complete). `zig build tidy` may need `--cache-dir /tmp/silica-zc-tidy`; CI ~15 min total.
- Realm created by the citadel restructure; memory migrated from the repo's former `.claude/memory/`.
  Branch `wip/wal-checkpoint-retention-phase2` preserves uncommitted Phase 2/3 WAL-retention work with
  one failing test (see STATE.md): fix or continue it before discarding.
- Open questions:
  - The repo's old memory contradicts itself on whether buffer-pool LRU eviction moved to
    `zuda.containers.cache.LRUCache` (`decisions.md` no; `architecture.md` session 46 yes). Read
    `src/storage/buffer_pool.zig` to settle it before touching buffer-pool code.
  - Whether the session-40 "no concurrent connections" finding (separate WAL/buffer-pool per
    `Database.open()`, unsynchronized writes to one WAL file) still holds after replication and MVCC
    work is not reconfirmed.

## Standing backlog (carried over from the old `project-context.md` log)

Pre-restructure sessions 497-498 (issues #125, #126) are closed history, dropped.

Standing "next priority": project was in "maintenance mode" post-v1.0.1; v2.0-scope candidates are
MVCC multi-version storage (replace delete+insert UPDATE) and config-file hot-reload with real test
coverage. Both are still open, see STATE.md.
