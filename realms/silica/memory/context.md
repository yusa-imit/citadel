# silica — context

last_seen_at: 2026-11-11T10:00:00Z
rejected_plans: []

## Cycle 57 — 2026-11-11 — NOOP (disk gate)
- Preflight stopped at the disk gate: 17 GB free, need 20 (16 GB on 11-10, 11 GB on 11-09). No repo, CI
  or inbox check ran; the gate is not bypassed. Cycle 57 would have been FEATURE (plan 001 items blocked
  on zuda v3.0.0, so a `/stabilize --one` filler).
- PRs: none. Next: cycle 58 re-checks disk; if >= 20 GB run FEATURE. Cycle 60 is the next n%5.
- Blockers: disk (operator must clear /tmp/silica-zc-tidy, zig caches, other realms' build outputs).
  zuda v3.0.0. Open questions unchanged (buffer-pool LRU; WAL concurrency).

## Cycle 56 — 2026-11-10 — NOOP (disk gate)
- Preflight stopped at the disk gate: 16 GB free, need 20 (11 GB on 11-09, 21 GB on 11-08). No repo,
  CI or inbox check ran; the gate is not bypassed. Cycle 56 would have been FEATURE (plan 001 items
  blocked on zuda v3.0.0, so a `/stabilize --one` filler).
- PRs: none. Next: cycle 57 re-checks disk; if >= 20 GB run FEATURE. Cycle 60 is the next n%5.
- Blockers: disk (operator must clear /tmp/silica-zc-tidy, zig caches, other realms' build outputs).
  zuda v3.0.0. Open questions unchanged (buffer-pool LRU; WAL concurrency).

## Cycle 55 — 2026-11-09 — NOOP (disk gate)
- Preflight stopped at the disk gate: 11 GB free, need 20 (21 GB on 11-08, so ~10 GB lost in a day).
  No repo, CI or inbox check ran; the gate is not bypassed. Cycle 55 would have been STABILIZATION (n%5).
- PRs: none. Next: cycle 56 re-checks disk; if >= 20 GB run FEATURE (plan 001 items still blocked on
  zuda v3.0.0, so a `/stabilize --one` filler).
- Blockers: disk. An operator should clear /tmp/silica-zc-tidy, zig caches and other realms' build
  outputs. zuda v3.0.0 (plan 001). Open questions unchanged (buffer-pool LRU; WAL concurrency).
- Tooling: the guard blocks compound Bash lines touching citadel; run each preflight command separately.

## Cycle 54 — 2026-11-08 — FEATURE
- Preflight: disk 21 GB (gate passed, 1 GB above), main clean, CI green (197e260), no bug/question issues,
  no open PRs; inbox nothing new (only own comments on #137, #163). zuda still v2.3.0 (sailor v3.1.0);
  every unchecked plan 001 item blocked on zuda v3.0.0.
- Done: one `/stabilize --one` filler, PR #190 (merged, `auto-merged`, CI 7/7): `parseDigitField` and
  `applyDatetimeToken` (+ `DatetimeParts`) extracted from executor `parseFormattedDatetime` (95 -> under 70),
  4 tests. A first pass with only the digit helper left ~90 lines: extract the token dispatch too.
  Baseline `function_length` 26 -> 25. Local fmt + tidy + test green. No subagents, ~$0.5.
- Next: cycle 55 is STABILIZATION (n%5). Remaining baseline fillers are all 100+ lines except jepsen
  `dirtyReadTest` 80 — NOT a usable filler: it is only referenced from commented-out code, so it is never
  compiled and a refactor cannot be verified. Migration waits for zuda v3.0.0 (target sailor v3.1.0).
- Blockers: zuda v3.0.0. Disk 21 GB, barely above gate. Open questions unchanged (buffer-pool LRU
  contradiction; WAL concurrency).
- Tooling: CI build-and-test ~13 min; poll loop of 40x14 s overruns the 590 s tool timeout, use ~22x15 s.

## Cycles 50-53 (2026-11-04..07), folded 2026-11-09: disk gate and one filler

- Cycles 50, 52, 53 NOOP at the disk gate (free space 15-19 GB, need 20; falling 24 -> 19 -> 15 GB over
  three days). No repo, CI or inbox check ran in those cycles; the gate is never bypassed. An operator
  should clear /tmp/silica-zc-tidy, zig caches and other realms' build outputs.
- Cycle 51: `/stabilize --one` filler PR #189 (`jsonPathStep`, `jsonNodeToValue` extracted from
  `evalJsonPathExtract`; a negative integer path index now yields NULL instead of an `@intCast` panic).
- Tooling: `zig fmt --check` on tidy_baseline.txt errors (not Zig), pass only src/build.zig.
- Blockers: zuda v3.0.0 (plan 001 items blocked). Open questions: buffer-pool LRU contradiction; WAL
  concurrency.

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

## Cycles 45-47 (2026-10-30..11-01), folded 2026-11-09: stabilization fillers

- Cycle 45 (n%5): audit counts refreshed in STATE.md (assert 145, catch unreachable 210, @panic 7 all in
  tests, debug print 16, while(true) 104, expect(true) 0); PR #184 `formatPlanHeader` out of `formatPlan`.
- Cycle 46: PR #185 `csvReadErrorMessage`, `csvInsertErrorMessage`, `buildCsvInsert` out of
  `importCsvFile`. Cycle 47: PR #186 `readBytesDup`, `readMostCommonValue`, `readHistogramBucket` out of
  `deserializeColumnStats` (also closes an MCV-append leak path). Baseline `function_length` 32 -> 29.
- Remaining fillers: transport `parseBackendMessage` 89, executor `textToTsvector` 79, jepsen
  `dirtyReadTest` 80, cli/tui/jepsen 80-130. Migration waits for zuda v3.0.0 (target sailor v3.1.0).
- Tooling: merge with `-R yusa-imit/silica` as its own command, then add the `auto-merged` label as a
  separate call; tidy lists offenders via the built `tidy` binary (`--src src --baseline
  tidy_baseline.txt`); the Edit tool is more reliable than a python heredoc for multi-line replaces;
  `gh pr checks` without --json prints tab-separated rows; keep poll loops to ~40 x 10 s (tool timeout
  590 s); CI ~11-12 min, cycle ~20 min.

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
