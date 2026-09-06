# silica — context

last_seen_at: 2026-09-06T22:06:48Z
rejected_plans: []

## Cycle 2 — 2026-09-06 — FEATURE
- Done: inbox merged PR #139 (hygiene part 1 — dropped `src/query/`, packaged
  README/LICENSE/docs into `build.zig.zon` .paths), ticked milestone #137's
  part-1 checklist item. Implemented plan 001 item 2 part 2 batch 1: routed 9
  scratch-DB path occurrences across 4 files (`storage/gist_index.zig`,
  `replication/integration_test.zig`, `tui.zig`, `replication/receiver.zig`)
  through `std.testing.tmpDir`, matching `config/file.zig`/`tx/jepsen_test.zig`.
  Side effect: `zig fmt` hook fixed 3 of those files' pre-existing fmt-check
  failures (whitespace only, confirmed via `git stash` diff).
- PRs: #139 merged. #140 opened (item 2 part 2 batch 1) — CI still pending at
  the 22-min deadline; commented "awaiting CI; merge next cycle", left for
  next cycle's inbox.
- Split: added a part-2 sub-checklist to the plan doc tracking batch 1 done,
  ~19 files (~1,340 occurrences) remaining — largest: `sql/engine.zig` (819),
  `sql/catalog.zig` (152), `cli.zig` (105), `server/connection.zig` (72),
  `sql/executor.zig` (65).
- Next: cycle 3's inbox merges #140 if green, then continues part-2 batches
  (pick a few more files by size) or picks up `zig build tidy` (no
  blocked_by) — the rest of plan 001 is `blocked_by: zuda v3.0.0, sailor
  v3.0.0`.
- Blockers: none new. Standing blocker unchanged.
- Open questions: unchanged (buffer-pool LRU zuda-migration contradiction;
  concurrent-connections WAL-corruption finding not reconfirmed) — see
  History below.

## History (cycle 1 and earlier, folded)
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
