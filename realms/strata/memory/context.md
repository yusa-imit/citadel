# strata — context

last_seen_at: 2026-11-12T12:00:00Z
rejected_plans: []

## Cycle 96 — 2026-11-12 — NOOP (disk gate)
- Done: gate read 18 GB (need 20); repo untouched on main at 417ce09, inbox and CI not checked.
  `/tmp/strata-zc` is 1.6 GB: deleting it would reach ~19.6 GB, still short, so it was not deleted.
- Next: item 10 `src/testing/kv_model_test.zig` plus cycle 93's 5 review warnings, once the gate clears.
- Blockers: disk (18 GB free; NOOP at the gate in cycles 94-96). Open questions: none.

## Cycles 94-95 (2026-11-11..12), folded: NOOPs at the disk gate
- Gate read 18 -> 16 GB (need 20); repo untouched on main at 417ce09, inbox and CI not checked.

## Cycle 93 — 2026-11-11 — FEATURE
- Done: disk gate passed (23 GB). Inbox clean, CI green. Merged #88 (plan 006 item 9): `src/testing/durable.zig`
  `Durable` undo log (caller buffers, pre-images + old length, dropped at a successful `fileSync`, `FaultIo.crash()`
  restores newest->oldest; `UndoFull`/`FileClosed` typed); WAL property also runs through it (`.fsync` mode,
  `.fdatasync` bypasses the vtable on Linux). CI 7/7, 979 tests. Milestone #79 items 1-9 ticked. ~$1.6 of $4,
  ~19 min (dev 7.5 min, reviewer 8 min: it ran mutants, so brief a 4 min cap).
- Review (sonnet): 0 critical, 5 warnings NOT fixed (deadline), fold into item 10's PR: (1)
  `durable.zig` `inner_failed(anyerror)` ends `else => InputOutput` (take concrete sets / comment lossy maps);
  (2) `fileSetLength` forwarded unrecorded (document in headers+CHANGELOG, or record); (3) `restore` clears the log
  even when a restore step fails midway (keep log or document); (4) no tests: Restore/Capture `Canceled`/IO paths,
  closed-clean-file leaves `closed_dirty` false, handle reuse after clean close, `n == 0` shrink branch;
  (5) tautological assert `durable.zig:175` and `durable_test.zig:47`. Suggestions: name the `512 * size` undo
  budget, one construction path for `Run.init`/`init_mode`, document the file must be opened readable.
- Notes: mutate on a copy with a fresh `--cache-dir` (reusing /tmp/strata-zc gave stale "cached" passes).
- Next: item 10 `src/testing/kv_model_test.zig` (seeded put/delete/batch/scan/checkpoint/reopen vs a model,
  crash through `FaultIo.crash()`), plus the 5 warnings and cycle 89's open kv tests.
- Blockers: none. Open questions: none.

## Cycles 90-92 (2026-11-09..10), folded: NOOPs at the disk gate
- Gate read 17 -> 15 -> 17 GB (need 20); `/tmp/strata-zc` (1.6-1.8 GB zig cache) could not close the gap
  and was not deleted; repo untouched on main at 149a155, inbox and CI not checked. Cleared in cycle 93.

## Cycle 89 — 2026-11-09 — FEATURE
- Done: inbox clean (no OWNER comments, CI green). Merged #87 (plan 006 item 8): `kv/iterator.zig`
  `Range`/`Iterator`, `Db.scan`, `Db.generation()` (a method: `Db` is a by-value handle, counter lives in
  `State`; `Iterator` holds `*const Io` into State because tidy bans a stored `Io`). `get` during a scan is
  allowed (pin asserts are `== scans_live`); `Shared.bump` asserts no live scan. CI 7/7, 961 tests.
  Milestone #79 items 1-8 ticked. ~$1.3 of $4, ~15 min (dev 5 min, reviewer 1 min, dev fix 3 min).
- Review (sonnet): 2 CRITICAL, fixed: `scan` then `get` clobbered the first overflow value in the shared
  `value_buf` (first `next` now re-seeks, one extra descent per scan); `Db.close` with a live iterator now
  asserts `scans_live == 0` (deinit before close, documented).
- Open: no error-path test for `next` (read fault -> pin released, `scans_live` 0; needs item 9 `FaultIo`);
  no death test for the write-during-scan assert; no test that a failed write bumps the generation or that
  `scan` works after `Failed`; the earlier open mutant/rotation tests from cycle 88 still stand.
- Next: item 9 durable-boundary `FaultIo` (`src/testing/`), then fold the open tests into 9/10.
- Blockers: none. Open questions: none.

## Cycles 87-88 (2026-11-08), folded: plan 006 items 6-7
- 87 (#85): `frame.Type.commit`=4, `Recovery.truncate_after` (`wal/truncate.zig`), `CommitScan`
  (`wal/commit_scan.zig`); `kv.Db` open = CommitScan, truncate past K, redo <= K; put/delete append a
  commit frame, gate = last commit lsn; `node.op_pages_max` folded the `ops_max` copies. 937 tests.
- 88 (#86): `kv/batch.zig` `WriteBatch` (storage allocated in `init` with the caller's `gpa`; `commit` ->
  `Db.commit_ops` -> one `begin_write`, one commit frame; `State.fail_group` latches once frames were
  logged). Review found a REAL bug in #85: `Db.put`/`delete` did not latch after a clean tree rejection
  following logged chain frames (orphans after the last commit -> Corrupted on reopen); both now go
  through `fail_group`. The 3 cycle-87 warnings were folded (strict `run_checkpoint` assert, `truncate.zig`
  for/else -> assert, CHANGELOG). 951 tests. CI is ~2 min, so review + fix fits in a cycle.
- Open (fold into 9/10): no mutant test for "drop the latch in fail_group", "gate = durable_lsn", nor a
  `SegmentLimit`-mid-group/rotation crash test; a group can rotate twice (images + commit) -> `SegmentLimit`
  with tiny `wal_segments_max`; no kv test for bad `commit.first_lsn`, K=0 with torn header, open-from-
  checkpoint + unfinished group; no `pool_frames_min` slack-0 worst-case batch test; `CommitError = Error`;
  `Db.close` leaves live batches dangling (doc only).

## Cycles 75-86 (2026-11-01..07), folded 2026-11-09: plan 005 close, plan 006 start (kv engine)

- 75 (#75): seeded B+Tree model test `src/testing/btree_model_test.zig` (sorted-array `Model`; unlogged
  512 B/4 KiB/64 KiB x 3 seeds; logged crash/replay/torn variants); mutants died. Follow-ups: dedupe the
  two logged test loops, `check_each` dead flag, `///` on fixtures pub items, FaultIo/CrashSink
  durable-boundary variant.
- 77 (#77): plan 005 item 12; **v0.6.0** tagged and released; no sibling names strata; milestone #63
  closed. Plan 006 proposed (kv engine on the B+Tree, 12 items, v0.7.0), PR #78 merged 2026-11-03;
  `FaultIo`/`CrashSink` cannot drop unsynced bytes, `bulk_load` deferred to plan 007.
- 78-79: NOOP at the disk gate (19 GB); one `/stabilize --one` (CI green, README matches v0.6.0, no
  banned constructs; `page/header_test.zig` 794/800 lines, `btree/tree.zig` ~700).
- 80: milestone #79 (12 items). Item 1 (#80): live-file replay after `free_at` trunk stamps, failing
  `free_at` keeps ids queued, attached `insert`/`delete` assert `pool.gate_on` (fixtures/bench call
  `set_durable_lsn(0)` after `attach`). 81: item 2 (#81) crafted-page `Corrupted` tests
  (`btree/cursor_corrupt_test.zig`, `delete_corrupt_test.zig`); open: mutant check on them; preserved
  `wip/test-btree-corrupt-branches-20261104` (keep).
- 82: ADR-0005 kv layout v1 (#82): `pages.db` + `wal/`, lock = page-file `tryLock`, root = page 1; a
  **`commit` frame (WAL type 4)** + commit-bounded recovery (`truncate_after`, `CommitScan`).
- 83: item 4 (#83) `src/kv/db.zig`, `errors.zig`, `db_fixtures.zig`. Open: `close` swallows a checkpoint
  failure; `errors.map` ends `else => InputOutput`; error subsets all equal `Error`; no failed-commit
  latch test (item 9 `FaultIo`); absent-key `delete` still does `begin_write`; `Db.open` lacks
  `batch_ops_max/bytes_max/wal_*` options.
- 84: item 5 (#84) recovery on open + `Db.checkpoint`; preserved `wip/feat-kv-recovery-20261106` (keep).
  Open: mid-log damaged frame leaves `pages.db` partly redone (idempotent); no tests for `wal_lsn`
  naming no checkpoint frame, crash points inside `checkpoint`, header-only torn segment,
  `page_count_max` below the log need; "redo ignores page lsn" mutant deferred to item 10.
- 85-86: NOOP at the disk gate (17-18 GB, need 20); `/tmp/strata-zc` (1-2 GB zig cache) alone could not
  close the gap. Next after the gate: item 6 commit frame (WAL type 4) and commit-bounded recovery.
- Notes: `perl -e 'sleep N'` works for waits; `gh pr checks` says "no checks" ~20 s after push; the
  developer writes tests after code unless forced; foreground waits cap at 400 s; zig-developer ~8.5 min
  per small item; the guard rejects `;`-chained commands (tag + push + release: separate calls) and
  compound commands in citadel (use Write/Edit there).

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

## Cycle 71 (2026-10-29), folded
- Plan 005 item 8 (#71): `btree/overflow.zig` chain of type-18 pages, caller-provided `value_buf`
  (required param of `Tree.create/open`), overwrite reserves old+new chain slots in `frees_pending`;
  review warnings fixed (`fail_put`, shared chain ids -> Corrupted, `overflow_fail_test.zig`). Open:
  overflow `walk` does not check header page id == id; `value_buf` limit also rejects inline values.
  Preflight preserved uncommitted work as `wip/feat-btree-overflow-20261029` (keep).

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
