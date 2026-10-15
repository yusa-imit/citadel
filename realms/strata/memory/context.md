# strata — context

last_seen_at: 2026-10-15T08:50:00Z
rejected_plans: []

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

## Cycles 38-41 (2026-10-08..10, condensed 2026-10-11)
- 38: ADR-0002 page format v1 (#36): 24-byte header, CRC32C seeded with u64 page id, `Id = enum(u32)`
  0 = null, page 0 = ordinary page + 48-byte file header, all-zero page -> `error.Unwritten`,
  decode order magic/version/checksum/type, trunk-only freelist (`(page_size-32)/4`).
- 39: `page/header.zig` codecs (#37); `page.Id` lives in header.zig. Tests split into `header_test.zig`.
- 40: `page/freelist.zig` trunk codec (#38); manager maps file-header 0 <-> null, range-checks ids,
  writes trunk first then page 0; duplicate ids across trunks are the manager's bounded walk.
- 41: `PageManager` create/open/read/write (#39): exclusive tryLock, short/foreign file -> Corrupted,
  EOF inside a page -> TornWrite, page-0 bad CRC -> ChecksumMismatch; `read`/`write` assert
  0 < id < page_count; `create` does not enforce `page_count_max` (allocate does).
- Notes: tidy density counts `assert(` per fn per file incl. test helpers; `mem.indexOf` banned
  (`findScalar`); tidy bans `catch unreachable`; `fixtures.id_of` asserts raw < 64; Bash guard rejects
  `;`/`cd`/`$VAR` chains; agent output may be HTML-escaped; macOS has no `timeout`.

## Cycles 36-37 (2026-10-07..08, condensed 2026-10-11)
- 36: plan PR #28 open, one `/stabilize --one`: `allocator:` -> `gpa` in `tools/tidy/*.zig` (#33).
- 37: plan 003 approved (PR #28), milestone issue #34, item 1 tidy ADR-0001 `Io` guards (#35;
  `Io.Threaded`/`Evented`/`global_single_threaded` banned in `src/`, `io-field` rule).
- Notes: PATH zig is 0.15.2, use the 0.16.0 toolchain with `--cache-dir /tmp/strata-zc`; macOS
  `sed -i` needs `''`; use Write/Edit for memory files. Remaining audit sweeps: `std.debug.assert`
  alias across `tools/`; assertion density in `tools/`; camelCase API in `src/file/file.zig`.

## Cycles 25-32 (2026-10-01 to 10-05, condensed 2026-10-10)

- **25-26**: plan 002 items 5-6: `src/file/file.zig` core (`File` leaf value, no cached io;
  `direct` => `UnsupportedDirectIo`), `sync` (exhaustive on `SyncPolicy`; `sync_full` fallback
  only for OPNOTSUPP/NOTTY/INVAL/NODEV), `preallocate`, `lock`/`tryLock`/`unlock`;
  `src/file/platform.zig` is the only os-branching file. `file.zig` is 788/800 lines: new `File`
  methods go in a new file. `sync_data` (linux) and `reserve` bypass `Io` via raw syscalls.
- **28**: PR #24 Linux-red CI: `FaultIo` must forward `checkCancel` (Linux `sync_data` calls it,
  macOS never does). Any new `Io` wrapper must forward every slot `File`/`platform` reach;
  compile-check Linux with `zig test src/root.zig -target x86_64-linux --test-no-exec`. Use
  `/Users/fn/.zr/toolchains/zig/0.16.0/zig` (PATH zig is 0.15.2) and `--cache-dir /tmp/strata-zc`.
- **29**: `src/testing/truncation_matrix_test.zig` (CRC32C-framed records, every cut at 8..64 KiB;
  replace the fixed-frame decoder with the real WAL/page frame decoder when those land). A torn
  cut one byte past a sector boundary is a clean truncation.
- **30**: `bench/main.zig` codec baseline (Apple aarch64: crc hw 5.3 GB/s, sw 0.58, xxhash 26.2,
  varint enc 198 M/s, dec 151 M/s; recorded in `docs/plans/000-inherited.md`).
- **31**: plan 002 item 10: v0.3.0 tagged, released, milestone #17 closed; no consumers. Plan 003
  (Phase 2 page + CLOCK buffer pool, ends v0.4.0) proposed as PR #28: freelist is trunk-list
  only, bitmap deferred; item 1 adds the ADR-0001 tidy guards.
- **32**: `src/main.zig` returns the stdout flush error instead of `catch {}` (PR #29);
  STATE.md Tiger Style table refreshed (412 asserts / 197 fns = 2.09).
- Remaining audit sweeps: `std.debug.assert` alias across `tools/` (~65, tidy ban check does
  not flag it); assertion density in `tools/` (tidy density gate covers `src/` only); camelCase
  public API in `src/file/file.zig` (needs a plan).
- Notes: the guard hook rejects compound Bash and `$VAR` paths into citadel (one simple command
  per call); `gh pr checks --watch` right after PR create may say "no checks reported", rerun.

## History
- Cycles 33-35 (2026-10-06, FEATURE, plan PR #28 open): one `/stabilize --one` each: `build.zig` `//!`
  header (#30), tidy baseline assertion density + empty-key baseline-line bug fix (#31), tidy
  checks_ban density + `gpa:` naming (#32). Lesson: tidy line limit is 100 cols for comments too.
- Cycles 21–24 (2026-09-30..10-01, FEATURE): plan 002 approved by OWNER (merged PR #16); issue
  #17 opened. Item 1 `tools/tidy.zig` split into `tools/tidy/*.zig` (#18), `tools` in scan_roots;
  item 2 `codec/fixed`+`varint` (#19); item 3 `codec/crc32c` (#20, hw/sw by CPU feature set;
  x86 hw asm compile-checked only); item 4 `codec/xxhash` (#21). Lessons: tidy assertion density
  is per file (>= 2 per fn incl. comptime asserts), so prefer one generic fn over many tiny
  wrappers; Zig 0.16 inline asm has no `%w[x]` on aarch64 and no tied input on x86; a
  recursion-by-accident inside an assert is a trap.
- Cycles 13–20 (2026-09-16..29, FEATURE, no-op): plan PR #16 open awaiting human merge; each ran
  one `/stabilize --one` tidy-auditor pass (always clean). Cycle 17 hit citadel issue #16
  (memory-commit lock pileup), fixed by OWNER in citadel PR #20; cycle 19 self-corrected a stuck
  counter.
- Cycle 12 (2026-09-16): milestone #3's last item — v0.2.0 released (PR #15). Plan 002 drafted
  (PR #16).
- Cycle 11: `wip/chore-zig-0.16-migration-20260909` confirmed superseded by PRs #7/#11/#13; kept
  per never-delete rule.
- Cycle 10 (STABILIZATION): merged #13 (800-line file rule) and #14; flagged tidy self-lint gap
  (since fixed by item 1).
- Cycle 9: plan 001 assertion baseline (#12); reviewer caught an assert on user CLI input and a
  density miscount of `assert(` in comments.
- Cycle 8: `io: Io` convention + ADR-0001 (#11): strata never constructs an `Io`; only `kv.Db`
  caches one. `wal.Reader.next()` null reserved strictly for EOF.
- Cycles 1–7: plan 001 (tidy shape/limit/ban checks, 0.16 migration PR #7, tmpDir round-trip test
  via `std.testing.io`). Cycle 5 STABILIZATION: README drift fix. Cycle 3: disk gate abort.
  Cycle 0: realm created by citadel restructure.

## Standing backlog

- Version: 0.3.0 released (2026-10-05). `file/mmap.zig` deferred again (plan 003 out of scope).
- `docs/milestones.md` is the single source of truth for progress; `docs/PRD.md` for requirements.

## Next priority

Plan 003 complete (v0.4.0 released 2026-10-13). Plan 004 (WAL) is PR #47, awaiting human merge.
