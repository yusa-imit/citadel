# silica — context

last_seen_at: 2026-09-09T10:05:41Z
rejected_plans: []

## Cycle 7 — 2026-09-09 — FEATURE
- Inbox: merged PR #144 (batch 4 scratch-DB tmpDir), CI all green
  (build-and-test + 6 cross-compile), labeled auto-merged, branch deleted.
  No OWNER comments/directives/questions since watermark. No plan PR open,
  no plan_closed_unmerged. Milestone issue #137 still the only open issue.
- Implemented plan 001 item 2 part 2, batch 5: routed 54 scratch-DB literal
  path occurrences through `std.testing.tmpDir` — `storage/gin_index.zig`
  (33, uniform pattern) and `tx/wal_fuzz.zig` (21, the deferred
  paired-path variant: `wal_path = path ++ "-wal"` comptime concat became
  a runtime `std.fmt.bufPrint` concat since `path` is now a tmp-dir
  runtime string). Dropped 6 wal_fuzz.zig tests' now-dead `wal_path`
  locals (only prior use was the removed per-test defer deleteFile) rather
  than leave them unused. `zig build test` green, `zig fmt --check` clean
  on both files (22 other files have pre-existing fmt drift, unrelated).
- PR #145 opened, plan doc sub-checklist ticked (batch 5 done, remaining
  scope narrowed to 8 files / ~1,305 occurrences). CI pending at cycle
  deadline — commented "awaiting CI; merge next cycle", left for cycle 8's
  inbox.
- Next: cycle 8's inbox merges #145 if green, then picks the next batch
  from the remaining 8 files (largest `sql/engine.zig` 819 — likely needs
  its own multi-cycle sub-plan) or `zig build tidy` (no blocked_by).
- Blockers: none new. Standing blocker unchanged (plan 001 rest is
  blocked_by zuda v3.0.0, sailor v3.0.0).
- Open questions: unchanged (buffer-pool LRU zuda-migration contradiction;
  concurrent-connections WAL-corruption finding not reconfirmed).

## Cycle 6 — 2026-09-09 — FEATURE
- Inbox: merged PR #143 (stabilization-cycle SAFETY comments on 26 unjustified
  `catch unreachable` sites), CI all green (build-and-test + 6 cross-compile),
  labeled auto-merged, branch deleted. No OWNER directives/questions/comments
  since watermark beyond routine cycle summaries. No plan PR open, no
  plan_closed_unmerged.
- Counter: n=6, 6%5≠0, stabilize_streak empty — FEATURE, not forced.
- Implemented plan 001 item 2 part 2, batch 4: routed 54 scratch-DB literal
  path occurrences through `std.testing.tmpDir` — `storage/hash_index.zig`
  (26, uniform `Pager.init(allocator, path, .{})` pattern) and
  `sql/conformance_test.zig` (28, via the `createTestDb` helper). Same
  pattern as batches 1-3; mechanical, comment-only test scaffolding change,
  `zig build test` green (4724/4747 passed) both after each file and after
  the full batch, no stray scratch files under `git status --ignored`.
  `tx/wal_fuzz.zig` (21) deferred — its pattern derives a second `wal_path =
  path ++ "-wal"` per test, needs the tmp-dir treatment applied to both
  paths, not this batch's drop-in pattern.
- PR #144 opened, plan doc sub-checklist and CHANGELOG updated. CI still
  pending at the cycle deadline (historical ~13-18m runtime) — commented
  "awaiting CI; merge next cycle", left for cycle 7's inbox.
- Next: cycle 7's inbox merges #144 if green. Then either batch 5
  (`tx/wal_fuzz.zig`'s wal_path variant, 21 occurrences) or another
  unblocked item — 10 files (~1,359 occurrences) remain in the part-2
  sub-checklist after batch 4; largest is `sql/engine.zig` (819, likely
  needs its own multi-cycle sub-plan given size).
- Blockers: none new. Standing blocker unchanged (plan 001 rest is
  blocked_by zuda v3.0.0, sailor v3.0.0).
- Open questions: unchanged (buffer-pool LRU zuda-migration contradiction;
  concurrent-connections WAL-corruption finding not reconfirmed).

## Cycle 5 — 2026-09-08 — STABILIZATION
- Inbox: merged PR #142 (batch 3 scratch-DB tmpDir, plan 001 item 2 part 2),
  CI all green (build-and-test + 6 cross-compile targets), labeled
  auto-merged, branch deleted. No OWNER comments/directives/questions since
  last watermark. No plan PR open, no plan_closed_unmerged.
- Counter forces STABILIZATION this cycle (n=5, n%5==0); CI green, no bug
  issues open — not a forced-by-red-CI stabilization.
- Tidy audit (tidy-auditor, full report in agent transcript): assert(=19
  (not 12, STATE.md was stale), catch unreachable=212 (26 unjustified in
  real lib code), @panic=7 (all in test blocks, 0 lib violations),
  debug print=16, while(true)=104 (2 genuinely unguarded page-chain
  traversals: storage/hash_index.zig:275, storage/gin_index.zig:1284 — no
  cycle guard, flagged as next stabilization candidate), files>800=40
  (engine.zig 43,242 lines, executor.zig 35,253 lines unchanged),
  functions>70=150 (newly measured), usize-in-wire-format=0 (clean),
  missing `//!` header=17/61 files (all of replication/ + cli.zig,
  server/server.zig, tui.zig, sql/{parser,ast,tokenizer}.zig).
- Fixed smallest class: added SAFETY comments to the 26 unjustified
  `catch unreachable` sites (replication/slot.zig:98, storage/fuzz.zig:66,
  storage/btree.zig x4, sql/executor.zig x20 via one function-level
  comment on toCharTimestamp). Comment-only, zero behavior change.
  Editing executor.zig/btree.zig triggered the format-on-save hook, which
  incidentally fixed pre-existing (main-inherited) fmt drift in those two
  files — verified those files were NOT fmt-compliant on main before this
  touch (`zig fmt --check` against a pre-edit copy), so this wasn't
  scope creep, just unavoidable side effect of the hook.
- PR #143 opened, `zig build`/`zig build test` green locally, fmt-check
  clean on all 4 touched files. CI (build-and-test ~13m historically)
  still pending at the cycle deadline — commented "awaiting CI; merge
  next cycle", left for cycle 6's inbox.
- Next: cycle 6's inbox merges #143 if green. STATE.md Tiger Style table
  needs updating with the fresh audit counts above (not yet written to
  STATE.md this cycle — do in a future stabilization or docs pass).
  Next stabilization candidates in priority order: (1) `//!` headers for
  the 11 replication/*.zig files (comment-only, mechanical); (2) add
  iteration caps to the 2 unguarded page-chain loops (needs real logic +
  test, the only genuine "limit on everything" gap found).
- Blockers: none new. Standing blocker unchanged (plan 001 rest is
  blocked_by zuda v3.0.0, sailor v3.0.0).
- Open questions: unchanged (buffer-pool LRU zuda-migration contradiction;
  concurrent-connections WAL-corruption finding not reconfirmed).

## History (cycle 4 and earlier, folded)
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
  starting cycle 2.
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
