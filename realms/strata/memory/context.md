# strata — context

last_seen_at: 2026-10-26T12:00:00Z
rejected_plans: []

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

## Cycle 63 — 2026-10-21 — FEATURE
- Done: plan 005 item 3 — `src/btree/internal.zig` (`Internal`, `parse_internal(page, level)`, `parse_internal_raw`,
  `format_internal`, `internal_insert/remove`, `set_child`, `set_right_child`, `child_index/child_at`,
  `check_link/check_children/check_invariants`) + `src/btree/split.zig` `split_point(page, incoming_bytes, at)
  ParseError!u16` (leaf: first index of right node; internal: index of cell that moves up). Merged #66 (CI 7/7,
  683 tests, auto-merged), issue #63 item 3 ticked. ADR §11 internal golden matched first time.
- Review: 1 critical (split_point asserted on page bytes -> now `Corrupted`; ADR §13 amended), 7 warnings fixed
  (vacuous tests, sweep bias, added `set_child`). `node.zig` helpers (get16/put16/...) widened to `pub`.
- Next: item 4 `btree/tree.zig` create/get/insert-into-root-leaf + `BufferPool.fetchNew`. Brief the developer with
  ADR §8, §9, §13 and node/internal/split API. Blockers: none. Open questions: none.
- Note: ~$2.4 of $4, ~20 min. Same pattern (dev ~7 min $0.9, reviewer parallel, fixes via SendMessage ~4.5 min).
  `internal_test.zig` 692 / `split_test.zig` 397 lines; `internal.zig` 334.

## Cycle 62 — 2026-10-21 — FEATURE
- Done: plan 005 item 2 — `src/btree/node.zig` leaf codec (`parse_leaf`, `Leaf.entry/search/check_invariants/
  check_link(id)`, `format_leaf`, `seal`, `set_next`, `leaf_insert`, `leaf_remove`; ADR-0004 §2 limits with
  comptime asserts) + page types 16-18 in `page/header.zig`. Merged as #65 (squash, CI 7/7, auto-merged),
  issue #63 item 2 ticked, 652 tests. ADR §11 golden bytes reproduced from the encoder (no erratum).
- Deviations: own-id link rule is `Leaf.check_link(id)` (parse_leaf has no id); mutators are free fns over
  `[]u8` that leave the CRC stale - caller ends with `seal(page, id, lsn)`; `leaf_insert` returns
  `NodeFull`/`Corrupted` before the first write (count >= cell_count_max, neighbour order checked, not asserted).
- Review: 0 critical, 5 warnings fixed pre-merge (insert mutated before erroring, asserts on page bytes, vacuous
  sweep, missing negative tests). Left: model test uses 4 B keys/1 B varints only; `copyForwards/Backwards` fine on 0.16 CI.
- Next: item 3 internal cells + `split_point`. `node.zig` is 453 lines and `header_test.zig` 794/800 - put
  internal code in a new file (e.g. `btree/internal.zig`) and new header tests in a new test file.
  Blockers: none. Open questions: none.
- Note: ~$2.5 of $4, ~20 min. Pattern that worked: one zig-developer does tests+impl (9 min, ~$0.9), reviewer
  in parallel while ticking plan/CHANGELOG, fixes via SendMessage (2.5 min), PR CI 1m.

## Cycle 61 — 2026-10-20 — FEATURE
- Done: plan 005 approved (#62 merged, no owner comments). Milestone issue #63 opened. Item 1
  ADR-0004 B+Tree page format v1 merged as #64 (docs only, CI 7/7, auto-merged): types 16/17/18,
  24 B header + `cell_count|level|reserved|link`, u16 payload offsets, dense ordered cells,
  varint lengths, key_len_max <= 1024, height_max 16..7 by page size, frame type 16 `page_images`.
- ADR adds work beyond the plan text, owned by item 9 (WAL integration): `PageManager.free_at`,
  `BufferPool.discard`, id reserve with page-file sync before a frame references a popped id,
  overflow chains logged in their own frames first, `PageRedo` handles frame type 16. Item 4
  owns `BufferPool.fetchNew`. PRD §4.6 links the ADR; `parseLeaf` lost `page_size`.
- Next: item 2 `btree/node.zig` leaf cells (+ register types in `page/header.zig`; ADR §11 golden
  bytes are hand-derived, re-derive from the encoder and fix the ADR on mismatch).
  Blockers: none. Open questions: none (ADR OQ 1-7 are recommendations).
- Note: ~$2.7 of $4, ~14 min; the opus architect alone cost ~$1.6 and 11 min for a 325-line ADR,
  and its output had HTML-escaped `&lt;` that I had to decode while retyping. Next cycles: brief
  the zig-developer with ADR sections only. Guard rejects `;`-chained commands and `sleep N`.

## Cycles 58-60 (2026-10-18..20, condensed 2026-10-21)
- Plan 004 items 10-12 merged: `wal/checkpoint.zig` (#59; `redo_start` 0 when wal_lsn == 0, `reclaim` before
  `run` -> `NotCheckpointed`), seeded crash-recovery property `src/testing/wal_recovery_test.zig` (#60), docs +
  v0.5.0 tagged (#61), milestone #48 closed. `wip/test-wal-recovery-property-20261019` holds a deliberate
  mutant (`or true` in `wal/redo.zig`) - never merge it. Plan 005 proposed (#62), approved, milestone #63.
- Left: reclaim after a failed run is guarded; `Reader.validate` rejects index holes; recovery mutants for
  dropped sync not run; weak spot: pool gate off only fails at 64 KiB in the property test.
- Lessons: no `timeout` on macOS; `gh pr checks --watch` in background or `until ! gh pr checks N | grep -q
  pending`; do not call ScheduleWakeup in /cycle; opus ADR cost ~$1.6; brief zig-developer with ADR sections.

## Cycles 55-57 (2026-10-17..18, condensed 2026-10-20)
- Plan 004 items 7-9 merged (#56 `wal/recovery.zig` `Recovery.replay` + `Apply` vtable; #57 `BufferPool.
  set_durable_lsn` WAL-before-data gate; #58 `wal/redo.zig` `PageRedo` + `PageManager.ensure_page_count`;
  CI 7/7, auto-merged, reviews 0 critical). Left: recovery repairs run after the whole log is read; redo
  does not sync (caller syncs); every I/O error incl. Canceled maps to `Failed`; `deinit` asserts zero dirty
  so gated frames need a raised bound or `discardAll`; `docs/milestones.md` does not exist.
- Lessons: brief the zig-developer with ADR sections + "stop at 11 min"; reviewer in parallel with CI;
  fixes via SendMessage; Bash guard wants one simple command per call.

## Cycles 49-54 (2026-10-14..16, condensed 2026-10-17)
- Plan 004 items 2-6 merged (PRs #50-#55, squash, CI 7/7, auto-merged; tests 505 -> 554):
  `wal/frame.zig` (17 B header, CRC32C seeded with the expected LSN, `lsn_limit = 2^63`, golden
  frames; the reader must range-check the first LSN before `decode`), `wal/segment.zig` (24 B
  header, `format_name`/`parse_name`, exclusive `tryLock`, `SegmentLimit`/`SegmentIndexExhausted`),
  `wal/reader.zig` (`Reader.open/next/position`; Unwritten/torn tail legal only in the newest
  segment; opens the next segment before closing the previous; `fail()` closes `current`),
  `wal/writer.zig` (init via reader, torn tail -> `RecoveryRequired`, `durable_lsn` advances only
  after sync, failure latch, rotate syncs old segment + `platform.sync_dir`), and
  `wal/group_commit.zig` (`Group.enter/finish`, `Writer.commit(io, upto)`, `Stats`, Options
  `group_commit_window`/`_bytes_max`; `FaultIo` forwards futexWait/Wake + sleep).
- Left (non-blocking): `FaultIo` `Plan` cannot inject Canceled (no canceled-sync / canceled-
  follower test); no deterministic blocked-follower test; `append`/`sync`/`deinit` must be
  serialized against `commit` by the caller (documented); group-commit window does not wake early;
  `Options` defaults less explicit than Tiger Style wants; `sync_dir` ignores the full-sync variant
  on darwin; rotation-fault test lacks a `durable_lsn` check at the create/dir-sync step; stale
  sentence in `segment.zig` header about directory sync; `live_count` needs a reclaim hook for
  item 10; no test for `Segment.open`/`length` failing mid-crossing while the old segment is held;
  `Segment.open` is read_write (read-only dirs); `list_segments` should skip non-file entries.
- Lessons: brief the zig-developer for ONE item with tests + impl (~10 min, ~$1.5-2.5 of $4);
  resume the same agent via SendMessage for review fixes; spawn the reviewer in parallel with CI;
  wait with one `until ...; do sleep 20; done` foreground loop; `chore` label does not exist in
  strata (`gh pr create --label` fails, use only `auto-merged`); `gh pr merge` has no `-q`; use
  `--cache-dir /tmp/strata-cache` if `.zig-cache` fails to spawn the build runner.

## Cycles 45-48 (2026-10-11..13, condensed 2026-10-15)
- 45: page manager + buffer pool suites widened to all 8 page sizes; `src/testing/page_matrix_test.zig`
  (7 tests) feeds CrashSink truncate/torn cuts to the real `header.decode`, `PageManager.read`, `open`.
- 46: `bench/pool.zig` (`pool_hit` ~197 M ops/s, `pool_miss_evict` ~1.26 M ops/s, 4 KiB, 256 frames);
  figures in `000-inherited.md`; PRD §5 5M floor cleared ~40x.
- 47: plan 003 item 11 — README, CHANGELOG `[0.4.0]`, zon 0.4.0, tag v0.4.0, milestone #34 closed; plan 004
  (Phase 3 WAL, 12 items, v0.5.0) proposed as PR #47. No consumer pins strata.
- 48: plan 004 approved; milestone #48 opened; item 1 ADR-0003 WAL format v1 (#49): `wal-NNNNNNNN.log`,
  24 B segment header (`STWL`), 17 B frame `len|crc|lsn|type`, CRC32C seeded with expected LSN, byte-position
  LSNs, torn tail = `TornWrite` only, golden bytes in §11. Open questions in ADR §Open (page 0 repair,
  directory sync) are for items 5/9.
- Lessons: run `gh pr checks --watch` in the background, never foreground (~$0.3); foreground `sleep` is
  blocked; one long background sleep beats short polls (~$0.08 each); tick the plan file's box in the same
  PR as the item; ask architect for a tight ADR (opus ADR cost ~$2.3); macOS sed has no `0,/re/`.


## Cycles 42-44 (2026-10-10..11, condensed 2026-10-14)
- Plan 003 items 6-8 merged (#40, #41, #42; CI 7/7, auto-merged, reviewer 0 critical each).
  Item 6 `PageManager.allocate/free/sync` (`page/manager.zig`): `allocate` returns a reused page
  with stale bytes until written, grown pages read `Unwritten`, `free` uses `wal_lsn` as page lsn,
  deeper-trunk double free is the caller's problem, `page_count_max` bounds growth only.
  Item 7 CLOCK `BufferPool` (`cache/buffer_pool.zig`): all allocation in `init`, `PoolExhausted`,
  table tombstone `rehash` every `frames_max` evictions. Item 8 `cache/guard.zig` `PageGuard`,
  `fetchForUpdate/flushAll/discardAll`, `Stats.writebacks`, `WriteBackError`; write-back runs in
  `victim_evict` before `table.remove`, a failed write keeps the frame resident and dirty.
- Follow-ups not blocking: no `stdx.assert_always` (plain asserts are ReleaseSafe only);
  `BufferPool.frame_bytes/mark_dirty/Frame` are pub only for guard.zig; no `fetchNew` for a
  freshly allocated page (needed before the B+Tree); `flushAll` cleans pinned frames, so a later
  edit through an old slice needs `markDirty`.
- Gotchas: `fixtures.id_of` asserts raw < 64; tidy density counts test helpers; `assert(x.remove())`
  is a side-effect-in-assert trap; Bash guard rejects `;`/`$VAR` chains, one command per call;
  `git pull --ff-only` after checking out main to avoid editor "changed on disk".

## Cycles 25-41 (2026-10-01..10, condensed 2026-10-16)
- 25-26: plan 002 items 5-6: `src/file/file.zig` (`File` leaf value, no cached io; `direct` =>
  `UnsupportedDirectIo`; `sync` exhaustive on `SyncPolicy`), `preallocate`, `lock`/`tryLock`;
  `src/file/platform.zig` is the only os-branching file; `file.zig` is 788/800 lines, new `File`
  methods go in a new file. 28: `FaultIo` must forward `checkCancel` (Linux `sync_data` calls it);
  any new `Io` wrapper forwards every slot `File`/`platform` reach; compile-check Linux with
  `zig test src/root.zig -target x86_64-linux --test-no-exec`.
- 29-30: `src/testing/truncation_matrix_test.zig` (CRC32C-framed records, every cut 8..64 KiB; swap
  in the real WAL frame decoder when it lands); `bench/main.zig` codec baseline (crc hw 5.3 GB/s,
  sw 0.58, xxhash 26.2, varint enc 198 M/s, dec 151 M/s; in `000-inherited.md`).
- 31-32: v0.3.0 tagged, milestone #17 closed; plan 003 proposed (#28): trunk-list freelist only,
  bitmap deferred. `src/main.zig` returns the stdout flush error (#29); 412 asserts / 197 fns.
- 36-37: `allocator:` -> `gpa` in `tools/tidy/*.zig` (#33); plan 003 approved, milestone #34,
  item 1 tidy ADR-0001 `Io` guards (#35; `Io.Threaded`/`Evented`/`global_single_threaded` banned
  in `src/`).
- 38: ADR-0002 page format v1 (#36): 24-byte header, CRC32C seeded with u64 page id, `Id =
  enum(u32)` 0 = null, page 0 = ordinary page + 48-byte file header, all-zero page ->
  `Unwritten`, decode order magic/version/checksum/type, trunk-only freelist. 39: `page/header.zig`
  (#37). 40: `page/freelist.zig` (#38). 41: `PageManager` create/open/read/write (#39):
  exclusive tryLock, short/foreign file -> Corrupted, EOF inside a page -> TornWrite, page-0 bad
  CRC -> ChecksumMismatch; `create` does not enforce `page_count_max` (allocate does).
- Notes: tidy density counts `assert(` per fn per file incl. test helpers; `mem.indexOf` banned
  (`findScalar`); tidy bans `catch unreachable`; `fixtures.id_of` asserts raw < 64; tidy line
  limit is 100 cols for comments too; Bash guard rejects compound commands and `$VAR` paths into
  citadel (one simple command per call); PATH zig is 0.15.2, use
  `/Users/fn/.zr/toolchains/zig/0.16.0/zig` with `--cache-dir /tmp/strata-zc`; macOS `sed -i`
  needs `''`; `gh pr checks --watch` right after PR create may say "no checks reported".
- Remaining audit sweeps: `std.debug.assert` alias across `tools/` (~65, tidy ban check does not
  flag it); assertion density in `tools/` (density gate covers `src/` only); camelCase public API
  in `src/file/file.zig` (needs a plan).

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
