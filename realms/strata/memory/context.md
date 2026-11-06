# strata — context

last_seen_at: 2026-11-05T05:30:00Z
rejected_plans: []

## Cycle 83 — 2026-11-05 — FEATURE
- Done: merged #82 (ADR-0005 kv layout v1, item 3) and #83 (plan 006 item 4: `src/kv/db.zig`, `errors.zig`,
  `db_fixtures.zig`, tests; create in empty dir, clean reopen, put/get/delete/flush/close). CI 7/7 both,
  milestone #79 ticked 1-4 (item 6 renamed). PRD 4.8 `Options` now the explicit-field struct.
- Review (sonnet): 0 critical, 4 warnings. Fixed: `close` leaked pending frees (now `release_frees` best
  effort; `Db.pending_frees()` diagnostic), `PoolExhausted/FreesPendingLimit` unreachable -> `Failed`,
  `Tree.open` error via `map`, `RecoveryRequired` doc.
- Open (for items 5/9): `open` accepts a log only if `writer.last_lsn == pm.wal_lsn`, else `Corrupted` (replay =
  item 5). `close` swallows a checkpoint failure (returns void). `errors.map` ends `else => InputOutput`; error
  subsets all equal `Error`; no test for failed-commit latch (needs a `FaultIo` that wraps `Db.open`, item 9);
  `delete` of an absent key still does `begin_write`. `Db.open` needs `batch_ops_max/bytes_max/wal_*` options.
- Next: item 5 recovery on open + `Db.checkpoint` (brief with ADR-0005 §4, §7, §11).
- Blockers: none. Open questions: none.
- Note: developer wrote tests after code in the first pass; red-first only on the fix. `gh pr checks` right
  after push says "no checks" for ~20 s: poll for pending|pass first. ~$2.4 of $4.

## Cycle 82 (2026-11-05), folded
- ADR-0005 kv layout v1 (#82, merged in 83): `pages.db` + `wal/`, lock = page-file `tryLock`; root = page 1,
  type-checked on open; half-created dir / WAL missing -> `Corrupted`; one-frame batch admits only 7 ops at
  4 KiB, so v1 uses a **`commit` frame (WAL type 4, reserved id, no WAL bump)** + commit-bounded recovery
  (`Recovery.truncate_after`, `CommitScan`). Item 6 is now "commit frame and commit-bounded recovery".
  Opus ADR ~$1.1; foreground `until` waits hit the 400 s tool timeout: poll in <=5 min calls.

## Cycles 80-81 (2026-11-03..04), folded
- 80: plan 006 approved (#78), milestone #79 (12 items). Item 1 (#80): live-file replay after `free_at`
  trunk stamps, failing `free_at` keeps ids queued, attached `insert`/`delete` assert `pool.gate_on`
  (fixtures/bench call `set_durable_lsn(0)` after `attach`); 3 mutants killed.
- 81: item 2 (#81): crafted-page `Corrupted` tests (`btree/cursor_corrupt_test.zig`,
  `delete_corrupt_test.zig`), cursor scans assert height 3 at 512 B. Preflight preserved the item as
  `wip/test-btree-corrupt-branches-20261104` (keep). Open: mutant check on those new tests.
- Notes: zig-developer ~8.5 min per small item; guard rejects compound commands in citadel (use
  Write/Edit there).

## Cycles 78-79 (2026-11-02..03), folded
- 78: NOOP at disk gate (19 GB). 79: plan wait, one `/stabilize --one` (CI green, README matches
  v0.6.0, no banned constructs; `page/header_test.zig` 794/800 lines, `btree/tree.zig` ~700). Plan 006
  PR #78 merged 2026-11-03. `/tmp/strata-zc` (1.9 GB) is the 0.16 zig cache.

## Cycle 77 — 2026-11-02 — FEATURE
- Done: plan 005 item 12 merged as #77 (CI 7/7, main CI green): `btree.Error`/`NotImplemented` dropped,
  README btree row Landed, CHANGELOG `[0.6.0]`, `.version = "0.6.0"`. Tagged + released **v0.6.0**
  (annotated tag, `gh release create`); no sibling names strata -> no migration issues. Milestone #63
  closed; plan 005 complete.
- PR: plan 006 proposed (Phase 4b kv engine on the B+Tree, 12 items, MINOR -> v0.7.0), PR #78, awaiting
  merge (citadel#91). Planner (opus) took ~6 min / ~$0.8-1.0; it flagged `FaultIo`/`CrashSink` cannot
  drop unsynced bytes (own item), `bulk_load` deferred to plan 007.
- Next: once #78 merges, open milestone issue and start item 1 (B+Tree durability debts); else one
  `/stabilize strata --one`.
- Blockers: none. Open questions: none.
- Note: ~$2.3 of $4, ~16 min. Guard rejects `;`-chained commands (tag + push + release must be
  separate calls). The Monitor tool works for CI waits but a plain `until` loop in Bash also works.

## Cycles 75-76 (2026-11-01), folded
- 75 (#75, plan 005 item 10): seeded model test `src/testing/btree_model_test.zig` + fixtures (sorted-array
  `Model`; unlogged 512 B/4 KiB/64 KiB x 3 seeds; logged crash/replay/torn variants); mutants died. Open
  suggestions: dedupe the two logged test loops, `check_each` dead flag, `///` on fixtures pub items; the
  FaultIo/CrashSink durable-boundary variant is a follow-up for the next plan.
- 76 (#76, item 11): `bench/btree.zig`: `btree_get` 5.1M ops/s (floor 5M, thin margin), `btree_insert_seq`
  1.27M (floor 1M), `btree_insert_logged` 0.23M (recorded). Figures in `docs/plans/000-inherited.md`; the
  bench never fails on a missed floor (manual check).
- Tool note: `until ! gh pr checks N | grep -q pending` works for CI waits.

## Cycles 72-74 (2026-10-30..31), folded
- Plan 005 item 9 (WAL integration) in three PRs, CI 7/7, auto-merged: #72 log side (`Type.page_images`=16,
  `PageRedo` whole-frame-validated idempotent redo, `PageManager.free_at(io,id,lsn)`, `Writer.append_parts`);
  #73 `Tree.attach(writer, track)` + logged insert (one `page_images` frame per op + `set_lsn`, chain logged
  first = rule C, `pages.sync` before frame when ids popped = rule A, append failure -> `discardAll` + latch
  `Failed`, `BufferPool.track_*`); #74 logged `delete` (merge/borrow/collapse in one frame, unlinked pages
  `discard`ed after the frame), `release_frees` frees via `free_at(durable_lsn)` only when
  `writer.durable_lsn >= Tree.frees_lsn` (rule B). `freelist.allocate/free` keep max(old,new) trunk lsn.
- Reviews found 1 CRITICAL (unlinked page stayed dirty with old lsn -> `discard_unlinked`) and several
  warnings, all fixed. Open: no test replays onto the LIVE file after `free_at` trunk stamps (rule B path c);
  `track_has` linear; `insert` should assert `pool.gate_on`; `ops_max` helper has 3 copies.
- Lessons: Bash guard rejects `cd ... && ...` and `;` chains (one command per call); zig-developer once took
  13 min -> brief a hard stop at 7 min; preflight preserved uncommitted work as `wip/feat-btree-wal-insert-
  20261031` (keep).

## Cycle 71 — 2026-10-29 — FEATURE
- Done: plan 005 item 8 — PR #71 merged (CI 7/7, 778 tests, auto-merged): `btree/overflow.zig`
  (`write/walk/read/collect_ids`, chain of type-18 pages), `Tree.get/insert/delete/validate` and `Cursor`
  handle overflow cells via caller-provided `value_buf` (new required param of `Tree.create/open`).
  Issue #63 item 8 ticked. Overwrite reserves old+new chain slots in `frees_pending`.
- Preflight found item-8 work uncommitted on `feat/btree-overflow` (it already passed 771 tests):
  preserved as `wip/feat-btree-overflow-20261029` (pushed, keep), then finished on `feat/btree-overflow`
  (local branch reused; it sat at main). Faster than a fresh implement: ~13 min, ~$1.3 of $4.
- Review: 0 critical, 5 warnings fixed: error after `prepare_value` now via `fail_put`, shared chain ids vs
  `frees_pending` -> Corrupted (`Tree.pending_has_any`), boundary and failure-path tests in new
  `overflow_fail_test.zig`. Not tested: fail_put after `cell_bytes` error (unreachable on valid pages).
- Next: item 9 WAL integration (one `page_images` frame per op, `set_lsn`, `release_frees` waits for
  durable_lsn, `PageRedo` type 16, pending frees persisted, id reserve). Big: split across cycles if needed;
  brief developer with ADR-0004 §8, §9, §13 and Rule C. Follow-ups from 69/70 still open (crafted-page
  negative tests in cursor/plan_merge, release_frees failure test). Review suggestions open: overflow `walk`
  does not check header page id == id; `value_buf` limit also rejects inline values.
- Blockers: none. Open questions: none.
- Note: tick `chore` label missing; `find -mmin` takes ints only on macOS - poll with `stat -f %m`.

## Cycles 67-70 (2026-10-26..28), folded
- Plan 005 B+Tree items 4-7, one PR each (CI 7/7, auto-merged, issue #63 ticked): 67 (#67)
  `BufferPool.fetchNew`, `btree/tree.zig` root-leaf `Tree`; 68 (#68) `split_tree.zig`, `descend.zig`,
  `validate.zig`; 69 (#69) `delete_tree.zig` (merge-first then borrow, bounded `frees_pending`,
  `BufferPool.discard`; `Tree.create/open` take `frees: []Id`); 70 (#70) `btree/cursor.zig` (one pin at
  a time; `prev` across a leaf re-descends; bad link/level/order -> `Corrupted`). 761 tests at 70.
- Reviews found real defects each time (u32 underflow on a crafted page, under-validated split plan,
  unbounded borrow separator, duplicate id in `frees_pending`): all fixed with tests.
- Open follow-ups: crafted-page negative tests for `Corrupted` branches in plan_merge/plan_level and
  cursor `step_back/left_sibling/next/prev`; deep-tree (height 3) assertion in scan tests;
  `release_frees` free-failure test; pool-level `discard` test; `Del` ~80 KiB stack; pending frees
  not persisted (item 9); plan item 8 overflow `Entry` must be handed to the cursor.
- Tool notes: `zig build test` hides `std.debug.print` and traces are stale: run the built test binary
  (path in `failed command:`) without `--listen`, grep `FAIL|failed|error:|tidy: [0-9]`; reviewer
  cannot run 0.16 tests (PATH zig is 0.15.2); developer wrote tests after code despite the brief:
  demand red-first or use test-writer; brief "stop at 8 min"; pipe: dev 6-12 min, reviewer 3 min in
  parallel with CI, fix 4 min. Preflight found uncommitted work twice: preserved as `wip/*`, keep.
- Cycles 64-66 were NOOPs at the disk gate (16-18 GB); `/tmp/strata-zc` is the 0.16 zig cache.

## Cycles 64-66 (2026-10-22..23, condensed 2026-10-26)
- Three NOOP cycles: disk gate failed (18, 17, 16 GB free); nothing changed. Host disk later recovered to 25 GB.
  `/tmp/strata-zc` (1.9 GB) is the zig cache for 0.16 builds.

## Cycles 25-63 (2026-10-01..21, folded 2026-11-06)
- Plan 002 (25-32): `file/file.zig` (`File` leaf value, no cached io; `direct` => `UnsupportedDirectIo`),
  `preallocate`, `lock`/`tryLock`; `file/platform.zig` is the only os-branching file; `file.zig` is
  788/800 lines, new `File` methods go in a new file. `FaultIo` must forward `checkCancel` and every
  slot `File`/`platform` reach (it cannot inject Canceled). Linux compile check: `zig test src/root.zig
  -target x86_64-linux --test-no-exec`. v0.3.0 tagged.
- Plan 003 (36-44, v0.4.0): ADR-0001 `Io` guards in tidy (`Io.Threaded`/`Evented`/
  `global_single_threaded` banned in `src/`); ADR-0002 page format v1 (24 B header, CRC32C seeded with
  u64 page id, `Id = enum(u32)` 0 = null, all-zero page -> `Unwritten`, trunk-only freelist);
  `page/header.zig`, `page/freelist.zig`, `PageManager` (exclusive tryLock, short/foreign file ->
  Corrupted, EOF inside a page -> TornWrite, `create` does not enforce `page_count_max`, `allocate`
  does), CLOCK `BufferPool` (all allocation in `init`, `PoolExhausted`, tombstone `rehash` every
  `frames_max` evictions), `PageGuard` (write-back before `table.remove`; failed write keeps the frame
  resident and dirty). `flushAll` cleans pinned frames: a later edit through an old slice needs
  `markDirty`.
- Plan 004 (45-60, v0.5.0, #50-#61): `wal/frame` (CRC32C seeded with expected LSN), `segment`,
  `reader`, `writer`, `group_commit`, `recovery` (`Apply` vtable), `redo` (`PageRedo`), `checkpoint`,
  seeded crash-recovery property test; ADR-0003 WAL format v1. `wip/test-wal-recovery-property-
  20261019` holds a deliberate mutant (`or true` in `wal/redo.zig`): never merge it. Left over:
  recovery repairs run after the whole log is read; `sync_dir` ignores the full-sync variant on
  darwin; `Segment.open` is read_write.
- Plan 005 (61-63): approved (#62), milestone #63. ADR-0004 B+Tree page format v1 (#64): types
  16/17/18, 24 B header, u16 payload offsets, dense ordered cells, varint lengths, key_len_max <= 1024,
  height_max 16..7 by page size, frame type 16 `page_images`; item 9 owns `PageManager.free_at`,
  `BufferPool.discard`, id reserve with page-file sync before a frame references a popped id, overflow
  chains logged first, `PageRedo` for frame 16; item 4 owns `BufferPool.fetchNew`. `btree/node.zig`
  leaf codec (#65): mutators are free fns over `[]u8` that leave the CRC stale, the caller ends with
  `seal(page, id, lsn)`; `leaf_insert` returns `NodeFull`/`Corrupted` before the first write.
  `btree/internal.zig` + `split.zig` (#66): `split_point` returns `Corrupted` on bad bytes, never
  asserts (ADR §13).
- Notes: tidy density counts `assert(` per fn per file incl. test helpers, `mem.indexOf` banned
  (`findScalar`), `catch unreachable` banned, 100 cols applies to comments, `assert(x.remove())` is a
  side-effect trap. Bash guard rejects compound commands, `sleep N` and `$VAR` paths into citadel;
  wait with `until ! gh pr checks N | grep -q pending`. PATH zig is 0.15.2: use
  `/Users/fn/.zr/toolchains/zig/0.16.0/zig` with `--cache-dir /tmp/strata-zc`. No `timeout` on macOS;
  no `chore` label in strata. Cost pattern (~$2.5 of $4 per item): one zig-developer for tests + impl
  (~$0.9), reviewer in parallel with CI, fixes via SendMessage; an opus ADR costs ~$1.6-2.3, brief
  developers with ADR sections only.
- Remaining audit sweeps: `std.debug.assert` alias across `tools/` (~65); assertion density in
  `tools/`; camelCase public API in `src/file/file.zig` (needs a plan).

## History
- Cycles 21-35 (2026-09-30..10-06): plan 002 approved (#16); `tools/tidy.zig` split into
  `tools/tidy/*.zig` (#18), `codec/fixed`+`varint` (#19), `codec/crc32c` (#20, x86 hw asm
  compile-checked only), `codec/xxhash` (#21); one `/stabilize --one` per cycle while plan PR
  #28 waited (#30-#32). Lessons: tidy assertion density is per file (>= 2 per fn), prefer one
  generic fn over many tiny wrappers; Zig 0.16 inline asm has no `%w[x]` on aarch64.
- Cycles 0-20 (2026-09-05..29): realm created; plan 001 (tidy checks, 0.16 migration PR #7,
  tmpDir round-trip via `std.testing.io`, `io: Io` convention + ADR-0001 #11: strata never
  constructs an `Io`, only `kv.Db` caches one; `wal.Reader.next()` null reserved strictly for
  EOF); v0.2.0 released (#15), plan 002 drafted (#16); cycles 13-20 were no-op stabilization
  while it waited (citadel issue #16 memory-commit lock pileup, fixed by the OWNER).
  `wip/chore-zig-0.16-migration-20260909` is superseded, kept per never-delete rule.

## Standing backlog
- Version 0.4.0 released (2026-10-13). `file/mmap.zig` deferred (out of scope of plans 003-004).
- `docs/milestones.md` is the single source of truth for progress; `docs/PRD.md` for requirements.
