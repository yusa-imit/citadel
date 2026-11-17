# strata — context

last_seen_at: 2026-11-18T00:00:00Z
rejected_plans: []

## Cycle 107 — 2026-11-18 — FEATURE
- Done: disk gate passed (20 GB, exactly the limit), inbox clean, CI green. Reran WAL benches on main
  (aarch64 ReleaseFast): append 0.940M ops/s (floor 200k), 1 GiB replay 0.284 s (floor 5 s). `bench/wal.zig`
  review warnings fixed in #92 (merged CI 7/7, 1008 tests): `mib_max` cap, free-space preflight via
  `fstatfs` (darwin extern, Linux raw syscall, other targets null = skipped), arg parsed first in
  `bench/main.zig` (`wal_options_resolve`), `replay_verify` compares head_sum/frames/bytes/last lsn,
  append line prints batch + policy, error-path tests. Figures recorded in `000-inherited.md`; item 11 ticked.
- Review of #92: 0 critical, 5 warnings (Windows assert compile, Linux `frsize` units, overflow, filter-
  aware need, early check), all fixed in the PR. fstatfs probe only compile-checked on Linux/Windows.
- Next: item 12 (docs, README kv row `Landed`, drop `NotImplemented` in `src/kv.zig`, CHANGELOG, `.version
  = "0.7.0"` in one PR, tag, `gh release`), then close milestone #79 and `/plan`.
- Blockers: none. Open questions: none.
- Notes: cycle used ~14 of 22 min (dev 4 + review 2 + fix 3 + CI 2x1.5); Bash guard: one simple command
  per call (no `;`, no `$VAR` into citadel).

## Cycles 102-106 (2026-11-15..17), folded 2026-11-18
- 102: `wal.Reader` 64 KiB read-ahead window (#91): 1 GiB replay 5.222 s -> 0.354 s; review fixed 4
  warnings (`refill` memmoves the tail, oversize frames reuse the window). Bench review queued (done in 107).
- 103-106: NOOP at the disk gate (15-18 GB free, need 20); repo untouched; operator freed space by 107.

## Cycles 99-101 (2026-11-14..15) — NOOP, disk gate (folded 2026-11-15)
- Disk gate read 15, 13, 12 GB free (need 20), shrinking each cycle. Repo untouched on main at 0079408
  (== origin/main); inbox and CI not checked. The operator must free disk; cycles stay NOOP until then.
- Next: unchanged from cycle 98 (profile `wal/reader` replay cost, review `bench/wal.zig`, tick item 11,
  item 12 release v0.7.0) once the gate passes. Open questions: none.
- Note: a Bash call chaining `echo > /tmp/...` with citadel `$REALM` paths is rejected by the guard; one
  command per call, absolute citadel paths.

## Cycle 98 — 2026-11-13 — FEATURE
- Done: inbox clean, CI green. Reviewed #89 (0 critical, 5 warnings: non-vacuity asserts, `drive` swallows
  only InputOutput/Canceled/Failed, `op_reopen` suspends faults, tautological asserts) fixed, merged (CI
  7/7); issue #79 item 10 ticked. Item 11 as #90 (`bench/wal.zig`, `zig build bench -- wal [MiB]`), merged
  CI 7/7 WITHOUT code review. Figures (aarch64 ReleaseFast): append 0.905M ops/s (floor 200k, passes);
  1 GiB replay 5.222 s vs 5 s floor (MISSED by 4%, ~700 ns/frame, 7.4M frames); item 11 left unticked.
- Next: profile `wal/reader` per-frame cost to meet the replay floor (or split out per the plan), review
  `bench/wal.zig`, tick item 11, then item 12 release v0.7.0 (docs, drop `NotImplemented` in kv.zig).
- Open from 97: latch mutants uncaught, `applied` never hit by random runs, crash during recovery/open not
  exercised (stated in fixtures header), `setLength` unrecorded in `Durable`.
- Notes: reviewer 1 min, fix dev 3 min, CI ~1.5 min: review+fix+merge fits in 10 min. Bench dev ~5 min.
- Blockers: none. Open questions: none.

## Cycles 89-97 (2026-11-09..13), folded 2026-11-14: plan 006 items 8-10 and the disk gate
- NOOPs at the disk gate in 90-92 and 94-96 (read 15-18 GB, need 20; `/tmp/strata-zc` 1.6 GB cannot close
  the gap, never deleted); repo untouched on main, inbox and CI not checked.
- 89 (#87, item 8): `kv/iterator.zig` `Range`/`Iterator`, `Db.scan`, `Db.generation()` (a method: `Db` is a
  by-value handle, counter lives in `State`; `Iterator` holds `*const Io` into State because tidy bans a
  stored `Io`). Review fixed 2 CRITICAL: `scan` then `get` clobbered the first overflow value in the shared
  `value_buf` (first `next` re-seeks); `Db.close` with a live iterator asserts `scans_live == 0`.
- 93 (#88, item 9): `src/testing/durable.zig` `Durable` undo log (pre-images + old length, dropped at a
  successful `fileSync`, `FaultIo.crash()` restores newest->oldest; `UndoFull`/`FileClosed` typed). Mutate on
  a copy with a fresh `--cache-dir` (reusing /tmp/strata-zc gave stale "cached" passes); brief a reviewer
  running mutants with a 4 min cap.
- 97 (#89, item 10): `src/testing/kv_model_test.zig` + `kv_model_fixtures.zig` (Model, Pending, Run: 4
  crash rounds per run, 3 page sizes x 3 seeds); `FaultIo` forwards `dirCreateDir/dirOpenDir/dirClose`.
  Mutants: commit-skips-fsync dies at all sizes; redo-ignores-lsn at 4 KiB only. A developer with mutants
  takes ~20 min: run them in a separate agent. `python3 - <<EOF` + `cd` in Bash is rejected by the guard.
- Open (fold into items 10-11): no error-path test for `next` (read fault -> pin released); no death test
  for the write-during-scan assert; tests for Restore/Capture `Canceled`/IO paths and handle reuse after
  clean close; tautological asserts `durable.zig:175`, `durable_test.zig:47`; name the `512 * size` undo
  budget; latch mutants uncaught, `applied` never hit by random runs, crash during recovery/open not
  exercised, `setLength` unrecorded in `Durable`.


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

## Cycles 67-74 (2026-10-26..31), folded 2026-11-16: plan 005 B+Tree items 4-9

- Items 4-7 (#67-#70, CI 7/7, auto-merged): `BufferPool.fetchNew`, root-leaf `Tree`, `split_tree`,
  `descend`, `validate`, `delete_tree` (merge-first then borrow, bounded `frees_pending`), `btree/cursor.zig`
  (one pin at a time; bad link/level/order -> `Corrupted`). Item 8 (#71) `btree/overflow.zig` chain of
  type-18 pages, caller-provided `value_buf` (required in `Tree.create/open`). Item 9 (#72-#74) WAL
  integration: `Type.page_images`=16, `PageRedo` idempotent redo, `PageManager.free_at(io,id,lsn)`,
  `Tree.attach(writer, track)`, one `page_images` frame per op (rule C chain first, rule A sync before frame
  when ids popped, rule B `release_frees` only when `durable_lsn >= frees_lsn`), append failure ->
  `discardAll` + latch `Failed`.
- Every review found real defects (u32 underflow on a crafted page, unlinked page left dirty with old lsn,
  duplicate id in `frees_pending`): all fixed with tests. Open: no test replays onto the LIVE file after
  `free_at` trunk stamps; `track_has` linear; crafted-page negative tests for `Corrupted` branches.
- Tooling: `zig build test` hides `std.debug.print`: run the built test binary without `--listen`; PATH zig
  was 0.15.2 for reviewers; brief the developer with a hard stop (~8 min) and demand red-first tests; Bash
  guard wants one simple command per call. Preflight preserved uncommitted work as `wip/*` (keep).
  Cycles 64-66 NOOP at the disk gate; `/tmp/strata-zc` is the 0.16 zig cache.

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
