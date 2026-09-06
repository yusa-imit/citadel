# silica — context

last_seen_at: 2026-09-06T00:00:00Z
rejected_plans: []

## Cycle 1 — 2026-09-06 — FEATURE
- Done: inbox merged PR #138 (WAL checkpoint retention callback, plan 001
  item 1) — CI was green/clean, ticked milestone #137 item 1, commented with
  the summary (root-cause was a test bug, not prod; also fixed a real
  truncate-before-durable-header-write ordering bug). Then implemented plan
  001 item 2 part 1: deleted the empty untracked `src/query/`, added
  README/LICENSE/docs to `build.zig.zon` .paths.
- PRs: #138 merged. #139 opened (item 2 part 1) — CI still pending at the
  22-min cycle deadline (build-and-test alone historically ~12-16 min);
  commented "awaiting CI; merge next cycle", left for next cycle's inbox.
- Split: item 2's scratch-DB-to-tmp-dir part turned out to be 1,350+ literal
  `"test_*.db"` paths across 23 files (`storage/btree.zig`, `page.zig`,
  `sql/engine.zig`, `sql/executor.zig`, ...) — an order of magnitude past one
  cycle. Split into its own checklist item in
  `docs/plans/001-zig-0.16-and-tiger-baseline.md`; do it in batches of a few
  files per cycle, pattern already used in `config/file.zig`/
  `tx/jepsen_test.zig` (`std.testing.tmpDir`).
- Next: cycle 2's inbox should merge #139 if green, then pick the next
  unblocked item — `zig build tidy` step (no blocked_by) or the new
  scratch-DB tmp-dir item; the rest of the plan's items are
  `blocked_by: zuda v3.0.0, sailor v3.0.0`.
- Blockers: none new. Standing blocker unchanged — most of plan 001 past the
  mechanical-rename stage needs zuda v3.0.0 + sailor v3.0.0.
- Open questions: unchanged (buffer-pool LRU zuda-migration contradiction;
  concurrent-connections WAL-corruption finding not reconfirmed) — see
  History below.

## History (cycle 0 and earlier, folded)
- Realm created by citadel restructure. Memory migrated from the repo's
  former `.claude/memory/` (project-context.md, architecture.md,
  decisions.md, debugging.md, patterns.md, MEMORY.md). First plan `001`
  (Zig 0.16 migration) prescribed by `citadel/docs/ROADMAP.md`.
- Preserved WIP: branch `wip/wal-checkpoint-retention-phase2` (uncommitted
  Phase 2/3 WAL-retention work, one failing test — see STATE.md). Fix or
  continue it before anything else in this realm; do not discard.
- Next: open plan 001 PR (if not open) → await human merge. In parallel,
  bugs/CI-red always come first per kingdom law — currently CI is green
  and there are 0 open issues, so the WIP branch above is the standing
  priority-1 item.
- Open questions:
  - The repo's own memory contradicts itself on whether the buffer pool's
    LRU eviction was migrated to `zuda.containers.cache.LRUCache`
    (`decisions.md` says no, keep custom, session 27; `architecture.md`
    session 46 note says yes, migrated, all tests green). Not resolved by
    this migration — read `src/storage/buffer_pool.zig` to settle it
    before touching buffer-pool code.
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
