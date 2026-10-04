# silica — context

last_seen_at: 2026-10-04T00:00:00Z
rejected_plans: []

## Cycle 22 — 2026-10-04 — FEATURE
- Preflight: repo clean on main, CI green on main (60340e9), no bug/question issues, no open PRs.
  Inbox: only our own status comment on #137; nothing actionable.
- Done: plan 001 tidy part 2, line-length batch 2 (PR #162, merged, labeled `auto-merged`): 10 files
  with 6-12 long lines each (index_entry, stats, tokenizer, integration_test, monitor, auth,
  buffer_pool, fsm, vacuum, regex) wrapped; `line_length:` baseline 44 -> 34 files. CI 7/7 green
  (build-and-test 5m24s). Done via one zig-developer subagent (~$0.35), no function-length growth.
- Next: line-length batch 3 (files with 13-30 long lines: server/server, wire, transport, config/file,
  overflow, lock, mvcc, selectivity, crash_test, gist/hash_index, pattern_match, parser_fuzz...).
  Rest of plan 001 blocked_by zuda/sailor v3.0.0 (tags still v2.3.0 / v2.99.0).
- Tooling notes: guard hook blocks compound `cd repo; cmd` lines — cwd is already the repo, use
  simple commands. `gh pr checks --watch` right after create says "no checks"; retry once.
- Blockers: none. Open questions unchanged (buffer-pool LRU contradiction; WAL concurrent
  connections; tidy scans textual).

## Cycle 21 — 2026-10-03 — FEATURE
- Preflight: repo clean on main, CI green on main (650e327), no bug/question issues, no open PRs.
  Inbox: only our own status comment on #137; nothing actionable.
- Done: plan 001 tidy part 2, line-length batch 1 (PR #161, merged, labeled `auto-merged`): 16 files
  with <= 4 long lines each wrapped; `line_length:` baseline 60 -> 44 files. CI 7/7 green.
- Learned: tidy counts BYTES, so `// ── X ───` banner comments (3-byte dashes) trip the gate —
  trim the dash run instead of wrapping. Remaining baseline: 44 files, largest first is cheapest in
  tokens per file only for banner-heavy files; a python script for bannners + explicit line-number
  replacement table worked well (`/tmp/wrap.py` pattern).
- Next: line-length batch 2 (files with 6-20 long lines: replication/monitor, sql/stats,
  storage/fsm, server/auth, util/regex, etc.). Rest of plan 001 blocked_by zuda/sailor v3.0.0
  (tags still v2.3.0 / v2.99.0).
- Tooling notes: `gh pr checks` right after `gh pr create` reports "no checks" — retry. Chained
  `sleep` is blocked by the harness.
- Blockers: none. Open questions unchanged (buffer-pool LRU contradiction; WAL concurrent
  connections; tidy scans textual).

## Cycle 20 — 2026-10-02 — STABILIZATION (n%5==0)
- Preflight: repo clean on main, CI green on main (ddb8f92), no bug/question issues, no open PRs.
  Inbox: no comments since watermark; only milestone #137 open.
- Audit (hand-run, no subagent): hygiene clean (`zig-pkg/` already gitignored, no tracked
  artifacts), deps at newest tags (sailor v2.99.0, zuda v2.3.0), 0 `expect(true)`, `@panic(` only in
  test blocks. Fixed one class: 17 files lacking `//!` headers (PR #160, comment-only; baseline
  entries removed). CI 7/7 green, merged, labeled `auto-merged`. STATE.md header row 17 -> 0.
- Next: shrink line-length baseline (60 files, 3,620 lines) in batches; plan 001 rest blocked_by
  zuda/sailor v3.0.0. Stabilize streak stays 0.
- Tooling notes: guard hook rejects compound `gh pr view; gh pr merge` lines — run `gh pr merge N -R
  yusa-imit/silica` alone. `timeout` is not installed on this box; use `gh pr checks --watch`.
- Blockers: none. Open questions unchanged (buffer-pool LRU contradiction; WAL concurrent
  connections; tidy scans textual).

## Cycle 19 — 2026-10-01 — FEATURE
- Preflight: repo clean on main, CI not red, no bug/question issues, no open PRs. Inbox: only our
  own status comment on #137; nothing actionable.
- Implemented plan 001 tidy step part 2, line-length gate: `line_too_long` now ratchets per file
  via `line_length:<path>:<max_line_count>` baseline entries (60 files, 3,620 long lines), and
  `run_tidy` is a dependency of `test_step` (`zig build test` enforces tidy). 3 new tests;
  planted violation verified to fail. PR #159: build-and-test 9m14s + 6 cross-compile green,
  merged. Plan sub-checklist and CHANGELOG updated.
- Next: shrink the line-length baseline to zero in batches (largest files first; hand wrapping,
  `zig fmt` does not wrap). Checklist item stays unchecked until zero. Rest of plan blocked_by
  zuda/sailor v3.0.0 (tags still v2.3.0 / v2.99.0).
- Tooling notes: guard hook blocks Bash lines that touch other repos or mix writes — use simple
  commands and the Edit/Write tools for memory. BSD `sed -i` misparsed; use python for edits.
- Blockers: none. Open questions unchanged (buffer-pool LRU contradiction; WAL concurrent
  connections; tidy scans textual).

## History (cycle 18 and earlier, folded)

- **Cycles 17-18** (2026-09-29..30): tidy ban-list batches 3-4 (#157 catch_unreachable_no_safety, #158 std_time_in_lib; ban list complete; fixed planner.zig:resolveExprType ratchet regression). Tooling: `zig build tidy` may need `--cache-dir /tmp/silica-zc-tidy`; CI ~15 min total.
- **Cycles 15-17** (2026-09-26..29): C15 stabilization — merged #153, fmt pass #154. C16/17 tidy ban-list batches 1-3 (#155-#157: debug_print_in_lib, usize_in_disk_format, catch_unreachable_no_safety).
- **Cycle 14** (2026-09-17, FEATURE): finished interrupted `feat/zig-build-tidy-step` in place; PR #153 (`zig build tidy` part 1: function-length ≤70 + `//!` header checks, shrink-only `tidy_baseline.txt`; line-length checked but ungated, 3,521 violations). Known: function-length brace scan not string/comment-aware.
- **Cycle 13** (2026-09-16, FEATURE): merged #151 (batch 10). Implemented batch 11 (final):
  819 scratch-DB occurrences in `sql/engine.zig` across 6 variant shapes, completing the
  entire scratch-DB-to-tmp-dir sub-item (11 batches total). Opened #152.
- **Cycle 12** (2026-09-15, FEATURE): recovered an interrupted `chore/scratch-db-tmpdir-batch10`
  diff in place (`src/cli.zig`, 105 scratch-DB paths), opened #151. Only `sql/engine.zig` (819
  sites) remains in plan 001 item 2 part 2. Found `zig fmt --check` failing on 18 files on main
  (pre-existing; see standing backlog).
- **Cycle 11** (2026-09-12, FEATURE): inbox merged #149 (batch 8). Implemented batch 9:
  `sql/catalog.zig`'s 152 scratch-DB paths via the shared `TestCatalog` helper. Opened #150,
  left pending for cycle 12.
- **Cycle 10** (2026-09-11, STABILIZATION, forced n%5==0): inbox merged #147 (batch 7).
  Tidy-auditor refresh found 22 flagged `catch unreachable` in `executor.zig`, 20 false
  positives (already covered by PR #143), fixed the 2 genuine ones (`toCharNumber`, PR #148).
  Refreshed STATE.md's Tiger Style gap table (assert=19, catch unreachable=213, functions>70=161,
  worst `evalFunctionCall` ~3758 lines by the tidy-auditor's own count — see cycle 14's tidy.zig
  finding of 31,568 by the mechanical scan, a known simplification, not a contradiction).
- **Cycle 9** (2026-09-10, FEATURE): inbox merged #146 (batch 6). Implemented batch 7 (110
  occurrences: `storage/btree.zig` 45 uniform, `sql/executor.zig` 65 across four path-count
  variants). Opened #147, left pending for cycle 10.
- **Cycle 8** (2026-09-09, FEATURE): inbox merged #145 (batch 5). Implemented batch 6 (71
  occurrences: `storage/buffer_pool.zig` 33 uniform, `tx/wal.zig` 38 across four shapes
  including comptime-concat `wal_path` sites converted to runtime `bufPrint`). Backfilled a
  missed batch-5 CHANGELOG entry. Opened #146, left pending for cycle 9.
- **Cycle 7** (2026-09-09, FEATURE): inbox merged #144 (batch 4). Implemented batch 5 (54
  occurrences: `gin_index.zig` 33 uniform, `wal_fuzz.zig` 21 deferred paired-path variant —
  `wal_path = path ++ "-wal"` comptime concat became runtime `bufPrint`; dropped 6 now-dead
  `wal_path` locals). Opened #145, left pending for cycle 8.
- **Cycle 6** (2026-09-09, FEATURE): inbox merged #143 (26 SAFETY comments on unjustified
  `catch unreachable`, stabilization cycle 5). Implemented batch 4 (54 occurrences:
  `hash_index.zig`, `conformance_test.zig`). `wal_fuzz.zig` (21) deferred to batch 5 — needs
  tmp-dir treatment on a second derived `wal_path`. Opened #144, left pending for cycle 7.
- **Cycle 5** (2026-09-08, STABILIZATION, forced n%5==0): inbox merged #142 (batch 3). Tidy
  audit (tidy-auditor): assert(=19, catch unreachable=212 (26 unjustified), @panic=7 (test-only),
  debug print=16, while(true)=104 (2 unguarded page-chain loops:
  `storage/hash_index.zig:275`, `storage/gin_index.zig:1284` — next stabilization candidate),
  files>800=40, functions>70=150, missing `//!` header=17/61 files. Fixed smallest class: SAFETY
  comments on the 26 unjustified `catch unreachable` sites (PR #143, comment-only). STATE.md
  Tiger Style table still needs updating with these fresh counts (not done yet).
- **Cycle 4** (2026-09-07, FEATURE): inbox merged #141 (batch 2). Implemented
  batch 3 (44 occurrences: page.zig, overflow.zig, fuzz.zig). Opened #142,
  left pending for next cycle.
- **Cycle 3** (2026-09-07, FEATURE): inbox merged #140 (batch 1: gist_index,
  integration_test, tui, receiver — 9 occurrences). Implemented batch 2 (30
  occurrences: fsm.zig, vacuum.zig, server.zig). Confirmed jepsen_test.zig
  needs no change. Opened #141, left pending for next cycle.
- **Cycle 2** (2026-09-06, FEATURE): inbox merged #139 (hygiene part 1 —
  dropped `src/query/`, packaged README/LICENSE/docs into `build.zig.zon`
  .paths), ticked milestone #137's part-1 item. Implemented item 2 part 2
  batch 1: 9 scratch-DB occurrences across 4 files through `tmpDir`. Split
  off a part-2 sub-checklist tracking remaining files by size.
- **Cycle 1** (2026-09-06, FEATURE): inbox merged #138 (WAL checkpoint
  retention callback, plan 001 item 1; root-cause was a test bug plus a real
  truncate-before-durable-header-write ordering fix), ticked milestone #137
  item 1. Implemented plan 001 item 2 part 1 (deleted empty `src/query/`,
  added README/LICENSE/docs to `build.zig.zon` .paths) as PR #139. Found and
  split off the scratch-DB-to-tmp-dir part (1,350+ literal `"test_*.db"`
  paths across 23 files) into its own checklist item, done in batches
  starting cycle 2, completed at cycle 13 (batch 11, `sql/engine.zig`).
- Realm created by citadel restructure. Memory migrated from the repo's
  former `.claude/memory/` (project-context.md, architecture.md,
  decisions.md, debugging.md, patterns.md, MEMORY.md). First plan `001`
  (Zig 0.16 migration) prescribed by `citadel/docs/ROADMAP.md`.
- Preserved WIP: branch `wip/wal-checkpoint-retention-phase2` (uncommitted
  Phase 2/3 WAL-retention work, one failing test — see STATE.md). Fix or
  continue it before anything else in this realm; do not discard.
- Open questions:
  - The repo's own memory contradicts itself on whether the buffer pool's
    LRU eviction was migrated to `zuda.containers.cache.LRUCache`
    (`decisions.md` says no, keep custom, session 27; `architecture.md`
    session 46 note says yes, migrated, all tests green). Not resolved yet —
    read `src/storage/buffer_pool.zig` to settle it before touching
    buffer-pool code.
  - Whether the session-40 "no concurrent connections" finding (separate
    WAL/buffer-pool instances per `Database.open()`, unsynchronized writes
    to the same WAL file) is still true given replication and MVCC work
    landed since — not reconfirmed by this survey.

## Standing backlog (carried over from the old `project-context.md` log)

Last 2 logged sessions before this restructure (durable facts only):
- **Session 498** (2026-08-24, FEATURE): issue #125's physical-undo-log fix,
  step 3/8 — wired DELETE to `Database.recordUndo(table, key, before, null)`
  before the physical `tree.delete()`; required keeping pre-delete row bytes
  alive through the whole cursor loop (`DeleteEntry.raw_value`). Commit
  `c26d340`. Tests 4524/4546, 22 skipped, 0 failed.
- **Session 497** (2026-08-24, FEATURE): issue #125 step 2/8 — wired plain
  INSERT to `recordUndo()`; added `via_on_conflict_update` guard so ON
  CONFLICT DO UPDATE gets its own undo wiring later. Found and filed
  **issue #126**: column-level `UNIQUE` is parsed but never enforced
  (`Catalog.createTableFromAst` only indexes `PRIMARY KEY`, not `UNIQUE`).
  Commit `8a437b1`. Tests 4521/4543, 22 skipped, 0 failed.
  (Both #125 and #126 were later closed — commits `ca74a32`, `d24bb5e`,
  per `MEMORY.md`'s session-507 note — so this is historical, not open.)

Standing "next priority" (superseded by, but consistent with, STATE.md's
Next work candidates — kept here for the pre-restructure framing):
project was in "maintenance mode" post-v1.0.1; v2.0-scope candidates were
MVCC multi-version storage (replace delete+insert UPDATE) and config-file
hot-reload with real test coverage. Both are still open — see STATE.md.
