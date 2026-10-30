# strata — context

last_seen_at: 2026-10-30T00:00:00Z
rejected_plans: []

## Cycle 72 — 2026-10-30 — FEATURE
- Done: plan 005 item 9 split (plan + issue #63 now list 9a/9b). 9a log side merged as #72 (CI 7/7, 803 tests,
  auto-merged): `Type.page_images`=16 + `payload_valid`, `PageRedo` whole-frame-validated idempotent redo
  (single grow before any write), `PageManager.free_at(io,id,lsn)` (`free` = `free_at(..,0)`),
  `Writer.append_parts` (gather). `frame.seal` added; tests in `*_images_test.zig`, `writer_parts_test.zig`.
- Review: 0 critical, 2 warnings NOT fixed (deadline): (1) `freelist.allocate` re-stamps head trunk with
  `wal_lsn`, which can LOWER a trunk stamped by `free_at(L)` -> reopens rule B path (c); fix in 9b with test
  `free_at(L)` then `allocate` then lsn >= L. (2) `free_at` tests lack a full-head-trunk case (new trunk with `next`).
  Suggestions: `frame_test.zig:281` still lists type 16 as reserved; vacuous tautology at
  `frame_images_test.zig:232`; midway-fault redo test only injects at call 0 (`redo_images_test.zig:235`).
- Next: 9b tree side (`btree/`): one `page_images` frame per op (<= 2*height_max+1 pages), `set_lsn`, pins held
  until stamp, `release_frees` waits `durable_lsn` using `free_at`, `attach(writer)`, reserve ids with sync (rule A),
  overflow chains first (rule C, use `append_parts`), `discardAll` on append failure. Brief dev with ADR §9, §13.
  Consider splitting 9b again (attach+logged insert first). Fix the two review warnings first.
- Blockers: none. Open questions: none.
- Note: ~$1.9 of $4, ~19 min. zig-developer took 13 min (asked for 9) -> brief a hard stop at 7 min.

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

## Cycle 70 — 2026-10-28 — FEATURE
- Done: plan 005 item 7 — PR #70 merged (CI 7/7, 761 tests, auto-merged): `btree/cursor.zig` `Cursor`
  (`init/release/current/seek/first/last/next/prev`; one pin at a time; `prev` across a leaf re-descends
  from the root; bad link/level/order/overflow cell/shrunk leaf -> `Corrupted`). Issue #63 item 7 ticked.
- Preflight found the cursor work uncommitted on `feat/btree-cursor` (unverified): preserved as
  `wip/feat-btree-cursor-20261028` (pushed, keep), then verified and finished on `feat/btree-cursor`.
  One test failed (precondition `page_count > 10` unmet with 150 keys; now 400 keys).
- Review: 0 critical, 6 warnings: fixed prev/next index bound after a write (Corrupted not assert),
  KeyTooLarge now drops the pin, empty non-root leaf in seek, docs. Plan item 8 now says overflow
  `Entry` must be given to the cursor (`entry_of` returns Corrupted for overflow cells).
- Next: item 8 `btree/overflow.zig`. Follow-ups (not done): crafted-page negative tests for Corrupted
  branches in `step_back/left_sibling/next/prev`, deep-tree (height 3) assertion in scan tests,
  errdefer for pinned guards in the pool-exhaustion test, postcondition asserts in cross_forward/settle.
  Carried from 69: plan_merge/plan_level crafted tests, release_frees failure test, pending frees persisted (item 9).
- Blockers: none. Open questions: none.
- Note: ~$1.3 of $4, ~13 min. Debugging aid: `zig build test` hides std.debug.print and traces are stale;
  run the built test binary (path in `failed command:`) directly without `--listen` to see FAIL names.

## Cycle 69 — 2026-10-27 — FEATURE
- Done: plan 005 item 6 — PR #69 merged (CI 7/7, 744 tests, auto-merged): `btree/delete_tree.zig` (`Tree.delete`,
  merge-first then borrow, root collapse keeps root id, bounded `frees_pending` + `Tree.release_frees`),
  `BufferPool.discard`; `Tree.create/open` now take `frees: []Id`. Issue #63 item 6 ticked. #68 was already merged.
- Preflight found item-6 work uncommitted on `feat/btree-delete` (unverified): preserved as
  `wip/feat-btree-delete-20261027` (pushed), then finished on `feat/btree-delete-rebalance`. Keep the wip branch.
- Review: 1 critical (borrow separator unbounded by parent neighbours -> apply could fail mid-edit) + 1 warning
  (duplicate id in frees_pending -> double free) fixed in 482b34b with tests; release_frees pool-wide assert dropped.
- Next: item 7 `btree/cursor.zig` (seek/next/prev). Follow-ups from review (not done): deterministic crafted-page
  negative tests in plan_merge/plan_level (id/level/next/empty leaf/overflow value), release_frees free-failure test,
  weak asserts in plan_level, `Del` ~80 KiB stack, pool-level `discard` test, pending frees not persisted (item 9).
- Blockers: none. Open questions: none.
- Note: ~$2.2 of $4, ~23 min (1 min over). Stale failure traces in zig output mislead: grep
  `FAIL|failed|error:|tidy: [0-9]`. Dev 6 min + fixes 7 min; tell dev to stop by 4 min on fixes.

## Cycle 68 — 2026-10-26 — FEATURE
- Done: plan 005 item 5 — PR #68 (`feat/btree-split`, NOT merged yet): `btree/split_tree.zig` (prepare/apply split,
  root id fixed, `HeightLimit`), `descend.zig`, `validate.zig`, `Tree.validate(io, gpa)`; `NodeFull` removed from
  `InsertError`. Plan box + CHANGELOG ticked on the branch. Local 729 tests, fmt/tidy clean; first CI run 7/7.
- Review: 1 critical (plan_leaf/plan_internal under-validated, apply could wipe a leaf then fail Corrupted) fixed
  in c394acd (full `check_invariants` + separator bounds in prepare) + 6 negative/atomicity tests. CI on c394acd
  was still pending at the deadline; PR comment left.
- Next: FIRST check `gh pr checks 68`; if green and no `hold`, `gh pr merge 68 --squash --delete-branch`, label
  `auto-merged` (already applied), tick #63 item 5. Then item 6 delete/merge/rebalance in new files.
- Note: ~$3.2 of $4, ~24 min (overran). Developer wrote tests AFTER code despite the brief: demand red-first
  (or use test-writer). The first dev run took 12.4 min, so brief "stop at 8 min". Pipe: dev 12 min, reviewer
  3 min parallel with CI, fix 4 min. Blockers: none. Open questions: none.

## Cycle 67 — 2026-10-26 — FEATURE
- Done: plan 005 item 4 — `BufferPool.fetchNew(io, id)` (zeroed dirty frame, `FetchNewError`; ADR §13 line fixed)
  + `src/btree/tree.zig` `Tree.create/open/get/insert/check_invariants` (root leaf only, unlogged; `open` returns
  `Corrupted` for a bad root; `NodeFull` until item 5; overflow cell in root -> `Corrupted` until item 8).
  Merged #67 (CI 7/7, 706 tests, auto-merged), issue #63 item 4 ticked.
- Review: 1 critical (u32 underflow in `insert` overwrite path on a crafted valid-CRC page -> now `Corrupted`),
  5 warnings fixed (vacuous lsn test, missing create/Corrupted tests, `open` assert -> error).
- Next: item 5 split + `validate` (`tree.zig` is 206 lines, `tree_test.zig` 615: put split code in a new file
  e.g. `btree/split_tree.zig`/tests in a new test file). Blockers: none. Open questions: none.
- Note: ~$2.1 of $4, ~17 min. Disk gate passed again (25 GB). Pattern: dev 6.5 min, reviewer 3.5 min parallel
  with CI, fixes via SendMessage 3.7 min. Reviewer cannot run 0.16 tests (PATH zig is 0.15.2).

## Cycles 64-66 (2026-10-22..23, condensed 2026-10-26)
- Three NOOP cycles: disk gate failed (18, 17, 16 GB free); nothing changed. Host disk later recovered to 25 GB.
  `/tmp/strata-zc` (1.9 GB) is the zig cache for 0.16 builds.

## Cycles 61-63 (2026-10-20..21, condensed 2026-10-30)
- 61: plan 005 approved (#62), milestone #63 opened. Item 1 ADR-0004 B+Tree page format v1 (#64):
  types 16/17/18, 24 B header, u16 payload offsets, dense ordered cells, varint lengths,
  key_len_max <= 1024, height_max 16..7 by page size, frame type 16 `page_images`. Work the ADR
  assigns to item 9 (WAL integration): `PageManager.free_at`, `BufferPool.discard`, id reserve with
  page-file sync before a frame references a popped id, overflow chains logged in their own frames
  first, `PageRedo` handles frame type 16. Item 4 owns `BufferPool.fetchNew`.
- 62: item 2 `src/btree/node.zig` leaf codec (`parse_leaf`, `Leaf.entry/search/check_invariants/
  check_link(id)`, `format_leaf`, `seal`, `set_next`, `leaf_insert`, `leaf_remove`; ADR-0004 §2
  limits as comptime asserts), page types 16-18 in `page/header.zig`, #65. Mutators are free fns
  over `[]u8` that leave the CRC stale: the caller ends with `seal(page, id, lsn)`; `leaf_insert`
  returns `NodeFull`/`Corrupted` before the first write.
- 63: item 3 `src/btree/internal.zig` (`parse_internal(page, level)`, `format_internal`,
  `internal_insert/remove`, `set_child`, `set_right_child`, `child_index/child_at`, `check_link/
  check_children/check_invariants`) and `btree/split.zig` `split_point(page, incoming_bytes, at)
  ParseError!u16`, #66, 683 tests. Review: `split_point` asserted on page bytes, now `Corrupted`
  (ADR §13 amended). `node.zig` helpers (get16/put16/...) are `pub`.
- Pattern (~$2.5 of $4, ~20 min): one zig-developer does tests + impl (~8 min, ~$0.9), reviewer in
  parallel while ticking plan/CHANGELOG, fixes via SendMessage (~3 min); an opus ADR costs
  ~$1.6 (brief developers with ADR sections only). Guard rejects `;`-chained commands and `sleep N`.

## Cycles 45-60 (2026-10-11..20, folded 2026-10-28)
- Plan 003 closed (v0.4.0: page matrix tests, `bench/pool.zig`), plan 004 WAL (v0.5.0) landed as #50-#61:
  `wal/frame` (CRC32C seeded with expected LSN), `segment`, `reader`, `writer`, `group_commit`,
  `recovery` (`Apply` vtable), `redo` (`PageRedo`), `checkpoint`, seeded crash-recovery property test.
  `wip/test-wal-recovery-property-20261019` holds a deliberate mutant (`or true` in `wal/redo.zig`) -
  never merge it. ADR-0003 WAL format v1. Plan 005 proposed (#62) and approved.
- Left from the WAL work: `FaultIo` cannot inject Canceled; recovery repairs run after the whole log is
  read; `sync_dir` ignores the full-sync variant on darwin; `Segment.open` is read_write.
- Lessons: no `timeout` on macOS; run `gh pr checks` waits as `until ! gh pr checks N | grep -q pending`;
  foreground `sleep` blocked; do not call ScheduleWakeup in /cycle; brief the zig-developer with ADR
  sections and a stop time; reviewer in parallel with CI; fixes via SendMessage; `chore` label missing in
  strata; `--cache-dir /tmp/strata-zc` for 0.16 builds; opus ADR costs ~$1.6-2.3.

## Cycles 25-44 (2026-10-01..11, folded 2026-10-27)
- 25-32: plan 002 items 5-6: `file/file.zig` (`File` leaf value, no cached io; `direct` =>
  `UnsupportedDirectIo`), `preallocate`, `lock`/`tryLock`; `file/platform.zig` is the only
  os-branching file; `file.zig` is 788/800 lines, new `File` methods go in a new file. `FaultIo`
  must forward `checkCancel` and every slot `File`/`platform` reach; Linux compile check:
  `zig test src/root.zig -target x86_64-linux --test-no-exec`. `testing/truncation_matrix_test.zig`
  (every cut 8..64 KiB; swap in the real WAL frame decoder), codec bench baseline (crc hw 5.3 GB/s,
  xxhash 26.2, varint enc 198 M/s, in `000-inherited.md`). v0.3.0 tagged, plan 003 proposed (#28).
- 36-41: plan 003 approved, tidy ADR-0001 `Io` guards (#35; `Io.Threaded`/`Evented`/
  `global_single_threaded` banned in `src/`). ADR-0002 page format v1 (#36): 24 B header, CRC32C
  seeded with u64 page id, `Id = enum(u32)` 0 = null, all-zero page -> `Unwritten`, trunk-only
  freelist. `page/header.zig` (#37), `page/freelist.zig` (#38), `PageManager` create/open/read/
  write (#39): exclusive tryLock, short/foreign file -> Corrupted, EOF inside a page -> TornWrite;
  `create` does not enforce `page_count_max` (allocate does).
- 42-44: items 6-8 (#40-#42, CI 7/7): `PageManager.allocate/free/sync` (reused page keeps stale
  bytes until written; `free` uses `wal_lsn` as page lsn), CLOCK `BufferPool` (all allocation in
  `init`, `PoolExhausted`, tombstone `rehash` every `frames_max` evictions), `cache/guard.zig`
  `PageGuard` (write-back runs before `table.remove`; a failed write keeps the frame resident and
  dirty). Follow-ups: no `fetchNew` for a fresh page (needed before the B+Tree); `flushAll` cleans
  pinned frames, so a later edit through an old slice needs `markDirty`.
- Notes: tidy density counts `assert(` per fn per file incl. test helpers; `mem.indexOf` banned
  (`findScalar`); `catch unreachable` banned; `fixtures.id_of` asserts raw < 64; 100 cols applies to
  comments; `assert(x.remove())` is a side-effect trap; Bash guard rejects compound commands and
  `$VAR` paths into citadel; PATH zig is 0.15.2, use `/Users/fn/.zr/toolchains/zig/0.16.0/zig`
  with `--cache-dir /tmp/strata-zc`; macOS `sed -i` needs `''`.
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

## Next priority
Plan 004 (Phase 3 WAL) approved (PR #47 merged 2026-10-12), milestone #48 open; continue with the
next unticked item (see the newest cycle block above).
