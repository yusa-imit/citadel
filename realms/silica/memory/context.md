# silica — context

last_seen_at: 2026-10-26T10:00:00Z
rejected_plans: []

## Cycle 41 — 2026-10-26 — FEATURE
- Preflight: disk 41 GB (gate passed again), main clean, CI green (f5026b6), no bug/question issues,
  no open PRs; inbox nothing new. zuda still v2.3.0, so every unchecked plan 001 item is blocked.
- Done: one `/stabilize --one` filler, PR #180 (merged, `auto-merged`, CI 7/7): `radarFractions`
  helper extracted from renderRadarChart (73) with two tests (mixed kinds + errors, empty history);
  verb match now case-insensitive; baseline `function_length` 36 -> 35. Local fmt + tidy + test green.
  No subagents, ~$0.5.
- Next: fillers run 73, readAndExecuteFile 74. Cycle 45 is the next n%5==0. Migration waits for
  zuda v3.0.0 (target sailor v3.1.0).
- Blockers: zuda v3.0.0. Open questions unchanged (buffer-pool LRU contradiction; WAL concurrency).
- Tooling: guard rejects compound Bash lines touching citadel (even `START=$(date)`); run each
  command separately. Tidy counts bytes AND lines: keep test array literals under 100 columns.

## Cycle 40 — 2026-10-25 — NOOP (disk gate)
- Preflight stopped at the disk gate: `df -g /` showed 13 GB free (14Gi in `df -h`), below the 20 GB
  required (cycle 39 saw 16 GB, so free space is still shrinking). No repo state, CI, or inbox check
  was done; no PRs opened or merged.
- Mode would have been STABILIZATION (n=40, n%5==0).
- Next: when disk allows, STABILIZATION; fillers renderRadarChart 73, run 73, readAndExecuteFile 74.
  Migration waits for zuda v3.0.0 (target sailor v3.1.0).
- Blockers: disk < 20 GB free on the dev box, two cycles in a row. Needs a human to free space, or
  prune /tmp/silica-zc-* and zig caches. zuda v3.0.0 still pending. Open questions unchanged.

## Cycle 39 — 2026-10-22 — NOOP (disk gate)
- Preflight stopped at the disk gate: `df -g /` showed 16 GB free (17Gi in `df -h`), below the 20 GB
  required. No repo state, CI, or inbox check was done; no PRs opened or merged.
- Mode would have been FEATURE (n=39, streak 0). Cycle 40 is n%5==0 (STABILIZATION) if disk allows.
- Next: fillers renderRadarChart 73, run 73, readAndExecuteFile 74. Migration waits for zuda v3.0.0
  (target sailor v3.1.0).
- Blockers: disk < 20 GB free on the dev box (needs a human to free space, or cache dirs under
  /tmp/silica-zc-* and zig caches to be pruned). zuda v3.0.0 still pending. Open questions unchanged.

## Cycle 38 — 2026-10-21 — FEATURE
- Preflight: main clean, CI green (ef4887c), no bug/question issues, no open PRs; inbox nothing new
  (only own comments on #137, #163). zuda still v2.3.0, so every unchecked plan 001 item is blocked.
- Done: one `/stabilize --one` filler, PR #179 (merged, `auto-merged`, CI 7/7): `bracketMatch` helper
  extracted from renderBracketViewer (73) with a boundary test; baseline `function_length` 37 -> 36.
  Local tidy + `zig build test` + fmt green. No subagents, ~$0.4.
- Next: fillers renderRadarChart 73, run 73, readAndExecuteFile 74. Cycle 40 is the next n%5==0.
  Migration waits for zuda v3.0.0 (target sailor v3.1.0).
- Blockers: zuda v3.0.0. Open questions unchanged (buffer-pool LRU contradiction; WAL concurrency).
- Tooling: `zig build tidy|test --cache-dir /tmp/silica-zc-tidy` both exit 0 silently; CI ~11 min.

## Cycle 37 — 2026-10-20 — FEATURE
- Preflight: main clean, CI green (489f94c), no bug/question issues, no open PRs; inbox nothing new
  (only own comments on #137, #163). zuda still v2.3.0, so every unchecked plan 001 item is blocked.
- Done: one `/stabilize --one` filler, PR #178 (merged, `auto-merged`, CI 7/7): keyword help table
  hoisted to file-scope `sql_keyword_help` in tui.zig, `getSqlKeywordHelp` (73) now uses a 16-byte
  stack buffer instead of page_allocator (over-length input returns null; comptime check on key
  lengths); boundary test added; baseline `function_length` 38 -> 37. No subagents, ~$0.4.
- Next: fillers renderBracketViewer 73, renderRadarChart 73, run 73, readAndExecuteFile 74. Cycle 40
  is the next n%5==0. Migration waits for zuda v3.0.0 (target sailor v3.1.0).
- Blockers: zuda v3.0.0. Open questions unchanged (buffer-pool LRU contradiction; WAL concurrency).
- Tooling: `zig build test` prints nothing on success (check exit code); CI ~10.5 min, cycle ~17 min.

## History (cycles 32-36, condensed 2026-10-21)

Cycle 35 (STABILIZATION, 2026-10-18): audit clean (0 `expect(true)`, 0 `@panic(` in src, hygiene ok;
root *.o/*.a/test_output.txt untracked+gitignored); #176 split showIndexes (77); #163 sailor v3.1.0
notice: target v3.1.0 not v3.0.0 when migrating, Editor/MultiCursorEditor/LocalSource init now return
error{OutOfMemory}; std_time_in_lib 17. Cycle 36: #177 `matrixRowIndex` from renderMatrixView (verb
match now case-insensitive). Tooling: guard blocks `sed -i` on citadel (use Edit) and multi-command
lines mixing grep with citadel paths; run counts as separate Bash calls. CI ~10.5-12 min.
Cycles 32-34 (2026-10-15 to 10-17, FEATURE, all blocked on zuda v3.0.0): one `/stabilize --one`
filler each, auto-merged CI 7/7. #173 helpers `applyIntervalUnit`/`hasFormatToken` (parseIntervalString,
toNumber); #174 baseline ratchet (re-derive limits by running `zig build tidy` with the `function_length:`
lines removed; 58 -> 43 entries); #175 `jsonScalarToTextValue` (evalJsonExtract). `zig-pkg/` is already
gitignored (REALM.md note stale). Global zig is 0.15.2: use `std.mem.trimRight`. Guard rejects compound
lines mixing git/grep/writes or citadel reads; run steps as separate Bash calls.

## Cycle 31 — 2026-10-14 — FEATURE
- Preflight: main clean, CI green (9c457f8), no bug/question issues, no open PRs, inbox nothing new
  (only own comments on #137). zuda still v2.3.0, so migration items stay blocked.
- Done: PR #172 (merged, `auto-merged`, CI 7/7): all 1,184 long lines in engine.zig wrapped; last
  `line_length:` baseline entry dropped (baseline has none left); plan 001 tidy part 2 ticked.
  Local tidy + fmt + `zig build test` (4772+500 passed) green. No subagents, ~$1.1.
- Method (reusable): /tmp python splitter (not committed): break depth-0 call/struct-brace pairs one
  arg per line, `++` string splits, `=>`/`=`/catch/orelse/and/or breaks, comment re-wrap; then
  `zig fmt`; ~200 leftovers via an exact-line table. Only zero-indented non-test `fn` count for
  function_length, so wrapping inside `Database` methods and tests is free. `zig fmt` re-joins
  `X =>\n expr` when it fits; use `error.Name` instead of long qualified error names.
- Next: zuda v3.0.0 not tagged, so migration items remain blocked. Fillers: shrink `function_length`
  baseline (58 entries), `std_time_in_lib` waits on 0.16 clock. Consider ticking nothing else.
- Blockers: zuda v3.0.0. Open questions unchanged (buffer-pool LRU contradiction; WAL concurrency).
- Tooling: CI 10.6 min, cycle took ~21 min; poll loops with `sleep 10` x24 stay under tool timeout.

## Cycle 30 — 2026-10-13 — STABILIZATION (n%5==0)
- Preflight: main clean, CI green (993b6f5), no bug/question issues, no open PRs; inbox nothing new
  (only own comment on #137). zuda still v2.3.0 (sailor v3.0.0 tagged), so migration stays blocked.
- Done: PR #171 (merged, `auto-merged`, CI 7/7): the 10 `std.debug.print` sites in server.zig (8) and
  engine.zig (2) became scoped `std.log` (warn for failures, info otherwise); both `debug_print_in_lib`
  baseline entries dropped (tidy.zig keeps 3, those are its own test fixtures). No subagents, ~$0.4.
- Remaining tidy baseline: `std_time_in_lib` (17 files, blocked on 0.16 clock migration), function_length
  58 entries, `line_length:engine.zig` 1186, `catch_unreachable_no_safety:tidy.zig` 1.
- Next: engine.zig line-length (1186; split over 2 cycles by line range, baselined functions may not
  grow). Migration items wait for zuda v3.0.0.
- Flake: `tx.jepsen_test` "non-repeatable read (SERIALIZABLE prevents)" aborted (signal 6) once in a
  local `zig build test` on this change, then passed twice on rerun and in CI. Watch for recurrence.
- Tooling: guard rejects `cd repo; cat > file <<EOF` compound lines; write helper scripts with Write to
  /tmp then run `python3 -I` alone (cwd persists between Bash calls). CI ~10.5 min; cycle took ~19 min.

## Cycle 29 — 2026-10-12 — FEATURE
- Preflight: repo was dirty on `chore/line-length-executor` (executor.zig fully wrapped, baseline entry
  dropped, untested). Preserved as `wip/line-length-executor-20261012` (21244a4, pushed), then main
  pulled; CI green (791eb3d), no bug/question issues, inbox nothing new (only own comments on #137).
- Done: PR #170 (merged, `auto-merged`, CI 7/7): executor.zig 598 long lines wrapped. Local tidy +
  `zig build test` (4272+500 passed) + fmt green before commit. No subagents, ~$0.5.
  `line_length:` baseline now only engine.zig (1186).
- Preserved: `wip/line-length-executor-20261012` is superseded by #170 but stays (never delete wip).
- Next: engine.zig line-length (1186 long lines; baselined functions may not grow, expect helper
  extraction; consider 2 cycles split by line range). That finishes the tidy part-2 item.
- Blockers: zuda v3.0.0 (still v2.3.0); migration items blocked. Open questions unchanged.
- Tooling: a stale local branch `chore/line-length-executor` (== main) existed; reused via checkout.
  CI build-and-test ~10.5 min; a poll loop of `sleep 10` x40 stays under the 590s tool timeout.
  Guard blocks `cd citadel/...; python heredoc` compound lines: use Write/Edit for memory files.

## History (cycles 27-28, condensed 2026-10-18)

Cycle 28 (2026-10-10): line-length batch 5c, PR #169 (auto-merged, CI 7/7): finished the wip
cli+tui work (20 grown functions extracted back under baseline; `showTableSchema`/`dumpTable` share
`printCreateTable`); `line_length:` baseline 4 -> 2 files (engine 1186, executor 598).
Cycle 27 (2026-10-09): batch 5b, PR #168: catalog + parser wrapped, baseline 6 -> 4 files. Wrapping
cli/tui grew 20 baselined functions past `function_length:`, so tidy went red; preserved on
`wip/line-length-cli-tui-20261009` (superseded by #169, never delete wip).
Learned: tell wrapping agents up front that baselined functions may not grow; concurrent `zig build`
needs separate `--cache-dir`; CI ~12 min, `gh pr checks --watch` times out at 590s, poll instead.
Next: engine.zig (split over 2 cycles) then executor.zig. Blockers: zuda v3.0.0.

## History (cycles 25-26, condensed 2026-10-16)

Cycle 26 (2026-10-08): line-length batch 5a, PR #167 (11 -> 6 files, one zig-developer subagent).
Tooling: no `timeout` binary on macOS; `sleep N; cmd` chains are blocked; merge with `gh pr merge N
-R yusa-imit/silica --squash --delete-branch` then `gh pr edit N --add-label auto-merged`; CI ~10
min, so subagent work must finish within ~8 min.
Cycle 25: STABILIZATION (n%5==0), PR #166 (auto-merged, CI 7/7): the 18 `catch unreachable` sites in
`toCharTimestamp` were baselined as unjustified because the shared SAFETY comment sat outside the
tidy 3-line window; a short `// SAFETY:` on each `var buf` line removed the
`catch_unreachable_no_safety:src/sql/executor.zig:18` baseline entry. Put SAFETY comments on the
line above within the window; trailing comments risk the line_length ratchet. @panic hits in
replication/{slot,sync}.zig are test-only. Remaining tidy classes: debug_print_in_lib
(server.zig 8, engine 2), std_time_in_lib (17 files, blocked on the 0.16 clock migration).

## History (cycles 23-24, condensed 2026-10-09)

Cycle 24 (2026-10-06): line-length batch 4 (PR #165): 11 files wrapped, baseline 22 -> 11;
pattern_match.zig gained 3 private helpers because wrapping pushed functions past limits. Guard hook
rejects compound `cd; cmd` and env-assign lines; `gh pr checks --watch` backgrounds past 480s.
Cycle 23 (2026-10-05): line-length batch 3 (PR #164, auto-merged): 12 files wrapped, `line_length:`
baseline 34 -> 22 files; two baselined functions (watchFileInotify, parseConfigFile) needed blank-line
or comment trims to stay under function_length limits. Remaining 22 files (engine 1186, executor 598,
cli 262, parser 207, ...) go in batch 4, smallest first. Migration (#163 + plan 001 rest) waits for
zuda v3.0.0. `zig build test` may need `--cache-dir /tmp/silica-zc-tidy`.

## History (cycles 21-22, condensed 2026-10-08)

Cycles 21-22 (2026-10-03 to 10-04, FEATURE): plan 001 tidy part 2, line-length batches 1-2 (PRs
#161, #162, CI 7/7, auto-merged): 26 files wrapped, `line_length:` baseline 60 -> 34 files. Next:
batch 3 (files with 13-30 long lines: server/server, wire, transport, config/file, overflow, lock,
mvcc, selectivity, crash_test, gist/hash_index, pattern_match, parser_fuzz...). Rest of plan 001
blocked_by zuda/sailor v3.0.0. Learned: tidy counts BYTES, so `// ── X ───` banners (3-byte dashes)
trip the gate, trim the dash run instead of wrapping; a python script with an explicit line-number
replacement table worked well; `gh pr checks` right after `gh pr create` says "no checks", retry;
guard blocks compound `cd repo; cmd` lines. Open questions unchanged (buffer-pool LRU
contradiction; WAL concurrent connections; tidy scans textual).

## History (cycles 19-20, condensed 2026-10-07)

Cycle 20 (STABILIZATION, 2026-10-02): hygiene clean, deps at newest tags (sailor v2.99.0, zuda
v2.3.0), 0 `expect(true)`. PR #160 added `//!` headers to 17 files. Guard hook rejects compound
`gh pr view; gh pr merge` lines; run the merge as its own command with `-R yusa-imit/silica`.
Cycle 19 (2026-10-01): plan 001 tidy part 2, PR #159: `line_too_long` ratchets per file via
`line_length:<path>:<max_line_count>` baseline entries (60 files, 3,620 long lines); `run_tidy` is
a dependency of `test_step`. Guard hook blocks Bash lines that touch other repos or mix writes;
BSD `sed -i` misparsed, use python. Rest of plan 001 blocked_by zuda/sailor v3.0.0.

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
