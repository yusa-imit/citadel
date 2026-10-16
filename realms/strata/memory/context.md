# strata — context

last_seen_at: 2026-10-16T08:30:00Z
rejected_plans: []

## Cycle 53 — 2026-10-16 — FEATURE
- Done: plan 004 item 5 — `src/wal/writer.zig` (+ fixtures, `writer_test`, `writer_tail_test`,
  `writer_fault_test`; 545 tests, tidy 0): init via reader, torn tail -> `RecoveryRequired`, one
  `frame_bytes_max` batch buffer, `durable_lsn` advances only after sync, failure latch, rotate syncs
  old segment + `platform.sync_dir` (ADR Q4 resolved), `FaultIo` `sync_fail_after` + `dirRead`.
  Reviewer: critical (offset assert on reopen with smaller segment limit) and warning (init syncs a
  non-empty tail so durable_lsn is true) fixed in 351bba5.
- PRs: #54 OPEN, CI not yet seen (deadline hit). Item 5 box ticked in the plan file on the branch, NOT
  yet in issue #48. Next cycle: `gh pr checks 54`, merge if green (squash, label auto-merged), tick #48.
- Left (non-blocking): `sync_dir` ignores full-sync variant on darwin (fix doc/ADR or route through
  sync_full); rotation-fault test lacks `durable_lsn` check at create/dir-sync step; stale sentence in
  `segment.zig` header about directory sync; `live_count` needs a reclaim hook for item 10.
- Next: merge #54, then item 6 group commit (`Writer.commit`; batch buffer grows there).
- Blockers: none. Open questions: none.
- Note: cost ~ $3.4 of $4; zig-developer 13.5 min for writer + 4.7 min for fixes, review 1.3 min. Spawn
  the reviewer BEFORE waiting on anything and start work earlier: the 22-min budget fits only one agent
  round plus one fix round; for big items brief the agent to stop at 10 min.

## Cycle 52 — 2026-10-15 — FEATURE
- Done: the 3 cycle-51 reader warnings fixed in PR #53 (merged, squash, CI 7/7, 509 tests): `read_frame`
  reads the 17 B header then exactly the frame (irregular header -> old full window); `enter` opens
  the next segment before closing the previous (lock handoff, `cross` no longer closes first);
  `fail()` closes `current` on any `next` error, `check_invariants` requires `current == null` in
  `.failed`. Reviewer: 0 critical. Left: (W) no test for `Segment.open`/`length` failing mid-crossing
  while the old segment is held (hold seg 2 with a second open -> WouldBlock, check seg 1 released);
  CHANGELOG Unreleased `wal.reader` entry lacks the locking/handoff note.
- Next: item 5 `wal/writer.zig` (append, sync, rotate); do it in a fresh cycle with >= 15 min left.
  Torn/absent newest header case is the writer's to close; dir sync after `Segment.create` (ADR Q4).
- Blockers: none. Open questions: none.
- Note: cost ~ $1.1 of $4; zig-developer for a 3-fix brief took 3.5 min. Guard blocks compound Bash
  and `$VAR`/`date` chains in the first call; use `until ...; do sleep 20; done` foreground, once.
  `chore` label does not exist in strata (gh pr create --label fails); skip labels except auto-merged.

## Cycle 51 — 2026-10-14 — FEATURE
- Done: plan 004 item 4 — `src/wal/reader.zig` (+ `reader_fixtures`, `reader_test`, `reader_tail_test`,
  33 tests; 505 total): `Reader.open(target, io, gpa, dir, segment.Options)` (dir needs `.iterate`),
  `next(io)` (null = sticky clean EOF), `position()`, `deinit`, `check_invariants`. Index + strictly
  increasing first-LSN at open, exact `first_lsn == end LSN` when `next` crosses; Unwritten/torn tail
  legal only in the newest segment (a torn/absent newest header is treated as absent); LSN >= 2^63 ->
  Corrupted before decode; short read -> Corrupted. No `from_lsn` seek yet (recovery, item 7).
- PRs: #52 merged (squash, CI 7/7). Issue #48 item 4 ticked.
- Review (code-reviewer): 0 critical, 3 warnings NOT yet fixed (deadline): (1) `read_frame` (reader.zig
  ~369) reads min(remaining, frame_bytes_max) per frame -> read 17 B header then 17+len; (2) lock doc
  claims writer exclusion but lock is per-segment and dropped between segments in `cross` (open next
  before closing current; reword doc); (3) errdefer `.failed` leaves `current` open (close it or reword).
  Suggestions: skip non-file entries in `list_segments`; `Segment.open` is read_write (read-only dirs).
- Next: small fix PR for warnings 1-3 first, then item 5 `wal/writer.zig`. Writer must close the
  torn-header-on-newest case (recovery inspects that file itself).
- Blockers: none. Open questions: none.
- Note: cost ~ $2.6 of $4; zig-developer took 14 min. Each idle wakeup re-reads context (~$0.3): use ONE
  long foreground wait. `gh pr merge` has no `-q`; run merge and `gh pr edit --add-label` separately.

## Cycle 50 — 2026-10-14 — FEATURE
- Done: plan 004 item 3 — `src/wal/segment.zig` (+ `segment_test.zig`, `segment_file_test.zig`,
  `segment_fixtures.zig`, 40 tests): `format_name`/`parse_name` (`error{Corrupted}!?u32`, index 0 =
  Corrupted), 24 B header codec, `Segment{file,index,first_lsn}` create/open/append/length/sync/close,
  exclusive `tryLock`, `index_next`/`live_count_check` -> `SegmentLimit`/`SegmentIndexExhausted`.
  `open` scans an all-zero file (Unwritten) in 64 KiB chunks. ADR §13 signatures updated.
- PRs: #51 merged (squash, CI 7/7, auto-merged). Issue #48 item 3 ticked.
- Review: code-reviewer 0 critical, 4 warnings: fixed chunk size (4->64 KiB), unused import, ADR §13,
  create WouldBlock doc. Left: `read_exact` has `else => |other| return other` (pass-through of
  the std set); `FaultIo` cannot fail sync so `create`'s sync-fail cleanup is unproven (add a sync
  fault when the writer needs it, item 5). Cost ~ $2.55 of $4 (zig-developer 10 min ~ $1.6).
- Next: item 4 `wal/reader.zig` (list segments bounded by `segments_max`, `live_count_check`,
  index + first-LSN continuity -> Corrupted; Unwritten/TornWrite only legal in the newest segment;
  segment header first_lsn out of [1,2^63) -> Corrupted before `frame.decode`). Directory sync after
  `Segment.create` is still the writer's job (ADR open question 4).
- Blockers: none. Open questions: none.
- Note: brief the zig-developer for ONE item with tests+impl, it takes ~10 min; run
  `until gh pr checks N | grep -qv pending...` foreground for CI.

## Cycle 49 — 2026-10-14 — FEATURE
- Done: plan 004 item 2 — `src/wal/frame.zig` (+ `frame_test.zig`, 17 tests): 17 B header, CRC32C seeded
  with the expected LSN, `TornWrite`/`ChecksumMismatch`/`Corrupted`, `lsn_limit = 2^63`, golden frames
  pinned; truncation matrix now runs the real decoder (no-CRC mutant rebuilt as len-only, still caught).
  ADR-0003 §11 negative pin corrected (frame 1 under seed 2 = 0x2E5419B8, verified independently).
- PRs: #50 merged (squash, CI 7/7, auto-merged). Issue #48 item 2 ticked.
- Review: code-reviewer 0 critical, 2 warnings fixed (decode doc: reader must range-check first LSN
  before deriving `lsn_expected` — decode asserts it; page_image test sizes 256/131072 added).
  Cost ~ $1.5 of $4 (zig-developer wrote tests+impl ~$0.8, reviewer ~$0.3).
- Next: item 3 `wal/segment.zig` (header codec over `file.File`, tryLock, `segments_max`). Reader (item 4)
  must return `Corrupted` for a segment header whose first LSN is out of [1, 2^63) before calling decode.
- Blockers: none. Open questions: none.
- Note: a foreground `sleep 1` background task wastes a turn; use `until gh pr checks ... ; do sleep 20; done`
  in one foreground call (timeout 480000) instead of `--watch` + idle polling.

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
