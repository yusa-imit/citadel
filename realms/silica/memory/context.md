# silica — context

last_seen_at: 2026-09-27T10:05:31Z
rejected_plans: []

## Cycle 16 — 2026-09-27 — FEATURE
- Preflight: repo clean on main; CI green (matches origin/main SHA); no open bug/question/
  directive issues; no open PRs.
- Inbox: only a routine cycle-15 status comment from OWNER on #137 since watermark — no
  actionable items. No plan PR open, milestone #137 still the only open issue.
- Implemented plan 001's "`zig build tidy` step, part 2", ban-list batch 1: added the
  `debug_print_in_lib` check to `src/tidy.zig` — flags `std.debug.print(` in library code,
  skips whole test/fuzz-named harness files and in-file top-level `test` blocks, ratchets
  per-file via a path-keyed `tidy_baseline.txt` entry (same shape as `function_too_long`).
  Baselined the 3 current non-harness offenders: `server/server.zig` 8, `sql/engine.zig` 2,
  `tidy.zig` 3 (self-match — its own doc comments/string literals contain the search string
  `"std.debug.print("`, same known textual-scan limitation as `checkFunctionLength`). 8 new
  unit tests (positive/negative space, harness-file skip, test-block skip, ratchet
  over/under/no-match). Code-reviewer found 2 WARNING (3 new lines over 100 cols — fixed) and
  3 SUGGESTION (stale doc comments, missing count-field doc, missing no-match test — all
  fixed). `zig build test`, `zig fmt --check src build.zig`, `zig build tidy` (zero
  `debug_print_in_lib` leaks) all green.
- PR #155 opened, plan sub-checklist and CHANGELOG updated (checklist item stays unchecked —
  batch 1 of N, same precedent as the scratch-DB item). CI still running at cycle deadline
  (historical 13-18m) — commented "awaiting CI; merge next cycle", left for cycle 17's inbox.
- Next: cycle 17's inbox merges #155 if green, then FEATURE resumes on plan 001's tidy step
  part 2, ban-list batch 2 — pick from the remaining 3 ban-list checks (`catch unreachable`
  without `SAFETY:` — 213 sites, most already covered by blanket comments from PR #143, needs
  a proximity-window design decision; `std.time.*` in lib — 18 files, will conflict with the
  deferred 0.16 clock-migration item, needs per-file baseline like this batch; `usize` in
  on-disk formats — STATE.md says already 0 hits, likely fast) or start the 3,521-violation
  line-length reduction batches.
- Blockers: none new. Standing: plan 001 rest blocked_by zuda v3.0.0, sailor v3.0.0.
- Open questions: unchanged — buffer-pool LRU zuda contradiction; WAL concurrent-connections
  finding; tidy.zig function-length scan not string/comment-aware (now also true of the new
  debug-print check, documented inline).

## Cycle 15 — 2026-09-26 — STABILIZATION (forced n%5==0)
- Preflight: repo clean on `feat/zig-build-tidy-step` (PR #153 head); main CI green.
- Inbox: PR #153 CI all green, no hold → squash-merged, labeled `auto-merged`.
- Stabilization: fixed the open question from cycle 12 — `zig fmt` pass over the 17 files that
  failed `zig fmt --check` on main (PR #154, pure formatting, `zig build test` green, CI green,
  merged). `zig fmt --check src build.zig` now clean repo-wide.
- Next: FEATURE on plan 001 "`zig build tidy` step, part 2" (3,521 line-length violations,
  wire tidy into `zig build test`, remaining ban-list checks).
- Blockers: none new. Standing: plan 001 rest blocked_by zuda v3.0.0, sailor v3.0.0.
- Open questions: buffer-pool LRU zuda contradiction; WAL concurrent-connections finding;
  tidy.zig function-length scan not string/comment-aware. (fmt question resolved.)

## Cycle 14 — 2026-09-17 — FEATURE
- Preflight found the repo dirty and off main on branch `feat/zig-build-tidy-step`: an
  uncommitted, coherent diff (`build.zig`, `src/main.zig`, `docs/plans/001-...md` +
  untracked `src/tidy.zig`, `tidy_baseline.txt`) — an interrupted `/implement` session whose
  branch name matched exactly the next planned item. Verified in place rather than shunting to
  `wip/*` (same precedent as cycle 12): `zig build test` green (4738/4761 passed, 23 skipped, 0
  failed), `zig fmt --check` clean on the changed files.
- Inbox: no open PRs, no new OWNER comments/issues since watermark. Milestone #137 still the
  only open issue.
- Implemented/finished plan 001's "`zig build tidy` step, part 1": `src/tidy.zig` (checker +
  `zig build tidy` CLI) enforces function length ≤70 lines and missing `//!` headers against a
  shrink-only baseline (`tidy_baseline.txt`, 58+17 entries). Line-length check implemented but
  not yet gated (3,521 pre-existing violations, deferred to part 2). Corrected an inaccurate
  "green" claim in the plan doc (the full `zig build tidy` command still exits 1 today because
  line-length is un-baselined by design) and documented a known measurement bug: the
  function-length brace scan is not string/comment-aware, so `evalFunctionCall`'s baseline entry
  is inflated to 31,568 (real ~3,758) — matches the kingdom `tidy-auditor` agent's own grep-based
  approach, safe (never too low) but doesn't meaningfully ratchet that one function yet.
- PR #153 opened, plan checklist part 1 ticked, CHANGELOG updated. CI still pending at cycle
  deadline (historical 13-18m) — commented "awaiting CI; merge next cycle", left for cycle 15's
  inbox.
- Next: cycle 15's inbox merges #153 if green, then FEATURE resumes on plan 001's "`zig build
  tidy` step, part 2": reduce the 3,521 line-length violations to zero, wire `tidy` as a
  dependency of `zig build test`, add the remaining ban-list checks (`catch unreachable` without
  `SAFETY:`, `std.debug.print`/`std.time.*` in lib, `usize` in on-disk formats).
- Blockers: none new. Standing blocker unchanged (plan 001 rest blocked_by zuda v3.0.0, sailor
  v3.0.0).
- Open questions: unchanged (repo-wide `zig fmt --check` fails on 18 pre-existing files even at
  clean main HEAD — worth a stabilization fix; buffer-pool LRU zuda-migration contradiction;
  concurrent-connections WAL-corruption finding not reconfirmed). New: `tidy.zig`'s
  function-length scan needs a string/comment-aware rewrite to be meaningful on
  `evalFunctionCall`-sized functions — candidate for a future stabilization cycle, not blocking.

## History (cycle 13 and earlier, folded)

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
