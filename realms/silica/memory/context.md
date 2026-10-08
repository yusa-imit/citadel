# silica — context

last_seen_at: 2026-10-08T00:00:00Z
rejected_plans: []

## Cycle 26 — 2026-10-08 — FEATURE
- Preflight: main clean, CI green (b65f3bd), no bug/question issues, no open PRs. Inbox: nothing new
  (#137 milestone, #163 sailor pin bump open, not actionable: zuda still v2.3.0, sailor v3.0.0 tagged).
- Done: line-length batch 5a (PR #167, merged, `auto-merged`): optimizer, btree, gin_index, planner,
  analyzer wrapped; `line_length:` baseline 11 -> 6 files. CI 7/7 green (build-and-test 7m50s). One
  zig-developer subagent (~$0.7). planner.zig gained helpers `appendTableFields`, `setOpDisplayName`;
  two analyzer test names shortened (names cannot wrap).
- Next: batch 5b: cli 262, catalog 118, parser 207, tui 117; then engine 1186 and executor 598
  (probably one cycle each). Migration items once zuda v3.0.0 is tagged.
- Blockers: zuda v3.0.0. Open questions unchanged.
- Tooling notes: no `timeout` binary on macOS; `gh pr checks --watch` backgrounds past 590s, re-run
  it. `sleep N; cmd` chains are blocked by the harness. Merge with `gh pr merge N -R yusa-imit/silica
  --squash --delete-branch` then `gh pr edit N --add-label auto-merged` (`--label` not a merge flag).
  Cycle took ~19 min; CI ~10 min, so subagent work must finish within ~8 min.

## Cycle 25 — 2026-10-07 — STABILIZATION (n%5==0)
- Preflight: main clean, CI green, no bug/question issues, no open PRs. Inbox: nothing new (no comments
  since watermark); #137 milestone and #163 (sailor v3.0.0 pin bump) open, not actionable.
- Done: PR #166 (merged, `auto-merged`): the 18 `catch unreachable` sites in `toCharTimestamp` were
  baselined as unjustified because the shared SAFETY comment sat outside the tidy window (3 lines);
  put a short `// SAFETY:` on each `var buf` line (no new lines/long lines), removed the
  `catch_unreachable_no_safety:src/sql/executor.zig:18` baseline entry. CI 7/7 green (9m55s).
  STATE.md Tiger Style table refreshed. @panic hits in replication/{slot,sync}.zig are test-only.
- Next: line-length batch 5, the last 11 files (engine 1186, executor 598, cli 262, parser 207,
  analyzer 139, planner 136, catalog 118, tui 117, gin 94, btree 87, optimizer 69). Remaining tidy
  classes for stabilization: debug_print_in_lib (server.zig 8, engine 2), std_time_in_lib (17 files,
  blocked on 0.16 clock migration).
- Blockers: sailor v3.0.0 is now tagged, zuda v3.0.0 still is not (latest v2.3.0): plan 001 migration
  items need both. Open questions unchanged.
- Tooling notes: quote `--include='*.zig'` (zsh globbing); put SAFETY comments on the line above
  within the 3-line window, trailing comments risk the line_length ratchet. Guard hook blocks
  compound Bash writes into citadel: use Write/Edit tools.

## Cycle 24 — 2026-10-06 — FEATURE
- Preflight: main clean, CI green (4064f5f), no bug/question issues, no open PRs. Inbox: only
  #163 (sailor v3.0.0 pin bump, owner migration issue) — not actionable: zuda still v2.3.0.
- Done: line-length batch 4 (PR #165, merged, `auto-merged`): wal_fuzz, tokenizer_fuzz, connection,
  mvcc, gist_index, conformance_test, parser_fuzz, hash_index, pattern_match, wal, jepsen_test
  wrapped; `line_length:` baseline 22 -> 11 files. CI 7/7 green (build-and-test 9m46s — slower
  than before). One zig-developer subagent (~$1.1). pattern_match.zig gained three private helpers
  (tryMatchAlternation, tryMatchConcatQuantified, filterEndpointsByMinCount) because wrapping
  pushed functions past their length limit; moved verbatim, reviewed by diff.
- Next: line-length batch 5, the last 11 files (engine 1186, executor 598, cli 262, parser 207,
  analyzer 139, planner 136, catalog 118, tui 117, gin 94, btree 87, optimizer 69). The big ones
  (engine, executor) may need splitting across two cycles. Migration (#163 + plan 001 rest) once
  zuda v3.0.0 is tagged.
- Tooling notes: guard hook rejects compound `cd; cmd` and env-assign lines — use one simple command
  per Bash call; `gh pr checks --watch` exceeds 480s foreground timeout and backgrounds, re-run it.
- Blockers: zuda v3.0.0. Open questions unchanged.

## Cycle 23 — 2026-10-05 — FEATURE
- Preflight: main clean (local was one commit behind; ff-pulled to e642ff0), CI green, no bug/question
  issues, no open PRs. Inbox: only our own comment on #137 plus new OWNER-labelled migration issue
  #163 (sailor v3.0.0 pin bump) — acted on nothing: zuda still v2.3.0, plan 001 migration items need
  both (blocked_by zuda>=3.0.0, sailor>=3.0.0).
- Done: line-length batch 3 (PR #164, merged, `auto-merged`): server, page, selectivity, crash_test,
  overflow, config/file, transport, wire, lock, parser_error_tests, storage/fuzz, tidy.zig wrapped;
  `line_length:` baseline 34 -> 22 files. CI 7/7 green (build-and-test 5m31s). One zig-developer
  subagent (~$0.40). Two baselined functions (watchFileInotify, parseConfigFile) needed blank-line /
  comment trims to stay under their function_length limits after wrapping.
- Next: line-length batch 4 (remaining 22 files: engine 1186, executor 598, cli 262, parser 207,
  analyzer 139, planner 136, catalog 118, tui 117, gin 94, btree 87, optimizer 69, jepsen 46, wal 34,
  pattern_match 32, hash_index 30, parser_fuzz 28, conformance 27, gist 26, connection 25, mvcc 25,
  tokenizer_fuzz 22, wal_fuzz 21) — start with the 21-34-line files. Migration (#163 + plan 001
  rest) once zuda v3.0.0 is tagged; then bump sailor pin together with 0.16 migration.
- Tooling notes: `zig build test` may need `--cache-dir /tmp/silica-zc-tidy` (runner FileNotFound
  otherwise). `gh pr checks --watch` works for the full CI wait.
- Blockers: zuda v3.0.0. Open questions unchanged.

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
