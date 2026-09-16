# silica — context

last_seen_at: 2026-09-16T00:00:00Z
rejected_plans: []

## Cycle 13 — 2026-09-16 — FEATURE
- Inbox: merged PR #151 (batch 10, `cli.zig`), CI all green, labeled `auto-merged`, branch
  deleted, `main` fast-forwarded. No new OWNER directives/questions since watermark (only
  routine cycle-report comments). No plan PR open, no plan_closed_unmerged. Milestone issue
  #137 still the only open issue.
- Implemented plan 001 item 2 part 2, batch 11 (final batch): converted all 819 remaining
  scratch-DB path occurrences in `sql/engine.zig` to `std.testing.tmpDir`, across 6 variant
  shapes not seen in prior batches — simple deferred-delete (616), fed into the `createTestDb`
  helper (140), pre-open non-deferred cleanup + deferred cleanup (45), direct `Database.open`
  with a combined `defer { db.close(); deleteFile(path); }` block unwrapped to plain `defer
  db.close();` (11), WAL-mode tests with a companion `-wal` path rebuilt from the same
  `dir_path` (8), and CSV import/export tests with a second `csv_path` and a dynamically built
  `COPY` SQL literal (7). `zig build test` green (4724/4747 passed, 23 skipped, 0 failed, no
  regression), `zig fmt --check src/sql/engine.zig` clean, no new scratch files after a full
  test run. Completes the entire scratch-DB-to-tmp-dir sub-item (11 batches total) and its
  parent checklist item in full.
- PR #152 opened, plan sub-checklist and CHANGELOG updated. CI still pending at cycle deadline
  (historical 13-18m) — commented "awaiting CI; merge next cycle", left for cycle 14's inbox.
- Next: cycle 14's inbox merges #152 if green, then FEATURE resumes on plan 001's next
  unblocked unchecked item: the `zig build tidy` step (line-length/function-length/ban-list
  gate with a checked-in baseline, before the renames/collections/Io items which are all
  `blocked_by zuda v3.0.0, sailor v3.0.0`).
- Blockers: none new. Standing blocker unchanged (plan 001 rest blocked_by zuda v3.0.0, sailor
  v3.0.0).
- Open questions: unchanged — repo-wide `zig fmt --check` fails on 18 pre-existing files even
  at clean `main` HEAD (worth a stabilization fix); buffer-pool LRU zuda-migration
  contradiction; concurrent-connections WAL-corruption finding not reconfirmed.

## Cycle 12 — 2026-09-15 — FEATURE
- Inbox: PR #150 (batch 9) already merged before this cycle started, CI green on main
  (`b965e83`, matches origin/main). No new OWNER directives/questions/comments since watermark.
  No plan PR open, no plan_closed_unmerged. Milestone issue #137 still the only open issue.
- Preflight found the repo dirty and off main: an uncommitted `src/cli.zig` diff (872+/270-) on
  branch `chore/scratch-db-tmpdir-batch10` — an interrupted `/implement` session from a prior
  cycle that never committed. Branch was already properly named and matched the exact next
  planned batch, so rather than shunting to a `wip/*` branch and redoing the work, verified it
  in place: functionally complete (all 105 occurrences — 98 uniform + 7 multi-path variants:
  backup source/dest, save-memory/exists, save source/dest, open original/new — correctly
  route through `dir_path` from a tmp dir), `zig build test` green (4724/4747 passed, 23
  skipped, 0 failed), `zig fmt --check src/cli.zig` clean (confirmed the repo-wide fmt-check
  failures on 18 other files are pre-existing on main, unrelated to this diff — see Open
  questions). Ticked the plan checklist and CHANGELOG, committed, pushed, opened PR #151.
- PR #151 CI still pending at cycle deadline (historical 13-18m) — commented "awaiting CI;
  merge next cycle", left for cycle 13's inbox.
- Next: cycle 13's inbox merges #151 if green. Only 1 file remains in plan 001 item 2 part 2:
  `sql/engine.zig` (819 occurrences) — likely needs its own multi-cycle sub-plan given size.
- Blockers: none new. Standing blocker unchanged (plan 001 rest blocked_by zuda v3.0.0,
  sailor v3.0.0).
- Open questions: **new** — `zig fmt --check src build.zig` fails on 18 files repo-wide
  (`util/varint.zig`, `util/regex.zig`, `config/file.zig`, `tx/lock.zig`,
  `replication/{cascade,sender}.zig`, `sql/{analyzer,parser,engine,ast,index_entry,cost,
  tokenizer_fuzz,optimizer,tokenizer,planner,pattern_match,selectivity}.zig`) even at the
  clean `main` HEAD (`b965e83`) — confirmed via `git stash`. Contradicts kingdom rule "every
  commit passes `zig fmt --check`"; STATE.md's CI section doesn't mention it (CI may not run
  `zig fmt --check` today, or this drifted since the last STATE.md refresh). Worth a
  stabilization-cycle fix (mechanical `zig fmt` pass, one PR) — not fixed this cycle to keep
  scope to the one planned item. Unchanged from prior cycles: buffer-pool LRU zuda-migration
  contradiction; concurrent-connections WAL-corruption finding not reconfirmed.

## Cycle 11 — 2026-09-12 — FEATURE
- Inbox: merged PR #149 (batch 8 scratch-DB tmpDir), CI all green (build-and-test + 6
  cross-compile). No new OWNER directives/questions since watermark. No plan PR open, no
  plan_closed_unmerged. Milestone issue #137 still the only open issue.
- Implemented plan 001 item 2 part 2 batch 9: `sql/catalog.zig`'s 152 test scratch-DB paths, all
  funneled through the shared `TestCatalog` helper — converted `setup(allocator, path)` into
  `setup(allocator, name)` owning a `std.testing.TmpDir` and building the path internally, so
  all 152 call sites converted at once (mechanical sed on the uniform `const path = "...";` /
  `TestCatalog.setup(allocator, path)` two-line pattern). `zig build test` green (4724/4747
  passed, 23 skipped, 0 failed), `zig fmt --check` clean on catalog.zig, no new
  `test_catalog_*.db` files at repo root.
- PR #150 opened, plan doc sub-checklist ticked (batch 9 done, remaining scope narrowed to 2
  files / ~924 occurrences: `sql/engine.zig` 819, `cli.zig` 105). CI still pending at cycle
  deadline (historical 13-18m) — commented "awaiting CI; merge next cycle", left for cycle 12's
  inbox.
- Next: cycle 12's inbox merges #150 if green, then batch 10 on the remaining 2 files —
  `cli.zig` (105, has 7 multi-path variants alongside the uniform 98, needs per-variant care
  like batch 6/7) or start `sql/engine.zig` (819, likely needs its own multi-cycle sub-plan
  given size, per prior-cycle notes).
- Blockers: none new. Standing blocker unchanged (plan 001 rest blocked_by zuda v3.0.0,
  sailor v3.0.0).
- Open questions: unchanged (buffer-pool LRU zuda-migration contradiction; concurrent-
  connections WAL-corruption finding not reconfirmed).

## Cycle 10 — 2026-09-11 — STABILIZATION (forced, n%5==0)
- Inbox: merged PR #147 (batch 7 scratch-DB tmpDir), CI green (build-and-test + 6
  cross-compile). No new OWNER directives/questions since watermark. No plan PR open, no
  plan_closed_unmerged. Milestone issue #137 still the only open issue.
- Tidy-auditor refresh found the 2026-09-05 baseline stale (executor.zig/btree.zig grew from
  scratch-DB batches). Flagged 22 `catch unreachable` sites in `sql/executor.zig` as
  unjustified; investigation found 20 were a false positive — already covered by PR #143's
  blanket SAFETY comment above `toCharTimestamp` (line 3568), just further than the audit's
  2-line proximity check. Only 2, in the separate `toCharNumber` function, were genuinely
  unjustified (bufPrint of i64 into 32-byte buffers). Fixed those 2 with inline SAFETY
  comments, PR #148. `zig build test` green, `zig fmt` clean.
- PR #148 CI still pending at cycle deadline (historical 13-18m) — commented "awaiting CI;
  merge next cycle", left for cycle 11's inbox.
- Refreshed STATE.md's Tiger Style gap table: assert=19, catch unreachable=213, @panic in
  lib=0 (2026-09-05 count miscounted test-block panics in replication/{slot,sync}.zig),
  debug print in lib=14, while(true)=104 (~90 bounded inner loops, not reclassified per-site),
  files>800=40, functions>70=161 (newly measured; worst `executor.zig:evalFunctionCall`
  ~3758 lines), missing `//!` header=17/61 unchanged, bare usize in wire/disk structs=0.
- Next: cycle 11's inbox merges #148 if green, then FEATURE resumes on plan 001 item 2 part 2
  batch 8 — 4 files (~1,148 occurrences) remain: `sql/catalog.zig` (152), `cli.zig` (105),
  `server/connection.zig` (72), `sql/engine.zig` (819, likely needs its own sub-plan).
- Blockers: none new. Standing blocker unchanged (plan 001 rest blocked_by zuda v3.0.0,
  sailor v3.0.0).
- Open questions: unchanged (buffer-pool LRU zuda-migration contradiction; concurrent-
  connections WAL-corruption finding not reconfirmed).

## History (cycle 9 and earlier, folded)
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
