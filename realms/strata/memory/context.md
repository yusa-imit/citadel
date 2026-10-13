# strata — context

last_seen_at: 2026-10-13T12:00:00Z
rejected_plans: []

## Cycle 48 — 2026-10-13 — FEATURE
- Done: plan 004 approved (PR #47 merged); milestone issue #48 opened. Item 1 ADR-0003 WAL format v1
  (`docs/adr/0003-wal-format.md`, #49 merged, CI 7/7); PRD §4.5 links it, plan box and #48 ticked.
  Format: `wal-NNNNNNNN.log` (8 hex), 24 B segment header (`STWL`), 17 B frame `len|crc|lsn|type`,
  CRC32C seeded with expected LSN, byte-position LSNs, torn tail = `TornWrite` only (look-ahead over
  the rest of the newest segment), types record/page_image/checkpoint, golden bytes in §11 (CRCs
  re-verified in python).
- Review: skipped (docs only). Cost: architect (opus) ~ $2.3 of $4 — it ran ~10 min and a 475-line
  ADR; next ADR-sized items should ask for a tighter output or use sonnet.
- Next: item 2 `wal/frame.zig` per ADR §7/§13 (pin the golden frames; replace the stand-in decoder in
  `truncation_matrix_test.zig`). Open questions in ADR §Open (page 0 repair, directory sync in
  `file/platform.zig`) are for items 5/9.
- Blockers: none. Open questions: none.
- Note: `sleep N` foreground is blocked; use `run_in_background` sleeps and wait for the notification.
  macOS sed has no `0,/re/` range; use `1s/...`.

## Cycle 47 — 2026-10-13 — FEATURE
- Done: plan 003 item 11 — README page/cache Landed, 2A-2C ticked, CHANGELOG `[0.4.0]`, zon 0.4.0
  (#45, CI 7/7). Tagged v0.4.0 + GitHub release; milestone #34 closed; no consumers name strata
  in a `build.zig.zon`, so no migration issues. #46 ticked the last two boxes in the plan 003
  file (items 10/11 were only ticked in the issue). Plan 004 (Phase 3 WAL, 12 items, v0.5.0)
  drafted by planner (opus), proposed as PR #47, awaiting merge (citadel#50).
- Next: if #47 merged, open milestone issue for 004 and implement item 1 (ADR-0003 WAL format);
  if still open, one `/stabilize --one`. If closed unmerged, record the reason and re-plan.
- Blockers: none. Open questions: none.
- Note: `gh pr checks --watch` in the foreground cost ~$0.3 (context re-read); run it in the
  background. Bash guard rejects `&&` chains with `git tag`/`push` mixed with `/tmp` writes —
  one simple command per call. Planner output is HTML-escaped (`&gt;`); unescape before writing.
  PR implement skills should tick the plan file's box in the same PR as the item.

## Cycle 46 — 2026-10-12 — FEATURE
- Done: plan 003 item 10 — `bench/pool.zig` (new) + `bench/main.zig` wiring: `pool_hit` and
  `pool_miss_evict` (4 KiB, 256-frame pool over a 1024-page scratch file `strata-bench-<hex>.db`
  in cwd, removed on exit; `Result` now pub). Apple aarch64 ReleaseFast: hit ~197 M ops/s (5 ns),
  miss + clean eviction ~1.26 M ops/s (~795 ns, OS page cache). PRD §5 5M floor cleared ~40x.
  Figures in `000-inherited.md`; CHANGELOG Unreleased line. 411 tests.
- PRs: #44 merged (squash, CI 7/7, auto-merged). Issue #34 item 10 ticked.
- Review: none (bench only; zig-developer agent wrote tests+impl, ~$1.75 of $4 incl. idle polling).
- Next: item 11 — docs, module status, release v0.4.0: drop `NotImplemented` from `src/page.zig`/
  `src/cache.zig`, README page/cache rows -> Landed, tick 2A-2C in `000-inherited.md`, CHANGELOG +
  `.version = "0.4.0"` in one PR, then `/release strata minor`.
- Blockers: none. Open questions: none.
- Note: `ScheduleWakeup`/Workflow are not polling tools; wait for task notifications instead
  (`gh pr checks --watch` in background works).

## Cycle 45 — 2026-10-11 — FEATURE
- Done: plan 003 item 9 — page manager + buffer pool suites widened from 3 to all 8 page sizes
  (`fx.sizes_three` removed); new `src/testing/page_matrix_test.zig` (7 tests): CrashSink
  truncate/torn cuts at 8 sizes feed the real `header.decode`/`decode_file_header`,
  `PageManager.read` (-> TornWrite) and `open`; mutant decoders (no checksum, rejects intact) fail
  the sweep. Dense cuts to 4 KiB, sector-boundary +-1 and stride above. No non-test code changed.
- PRs: #43 merged (squash, CI 7/7, auto-merged). Issue #34 item 9 ticked.
- Review: none (tests only; zig-developer agent wrote it, ~$0.55 of $4). Inbox empty.
- Notes: `.torn` at a sector-aligned byte is a clean truncation; the file-header page is zero past
  byte 48 so cuts >= 48 pad back to the original (correct). Truncation stand-in in
  `truncation_matrix_test.zig` left as is (separate harness; real decoder lives in page_matrix_test).
  Polling a background agent with short sleeps costs ~$0.08 per poll; use one long background sleep.
- Next: item 10 — pool bench in `bench/main.zig` (fetch+release hit and miss-with-eviction at 4 KiB;
  add figures to `000-inherited.md`), then the docs/release v0.4.0 item.
- Blockers: none. Open questions: none.

## Cycle 44 — 2026-10-11 — FEATURE
- Done: plan 003 item 8 — `src/cache/guard.zig` (`PageGuard`: `bytes`, `bytes_mut`, `markDirty`,
  `set_lsn`, `id`, `release`), `BufferPool.fetchForUpdate/flushAll/discardAll`, `Stats.writebacks`,
  `dirty_count` in `check_invariants`; write-back runs in `victim_evict` before `table.remove`, a
  failed write keeps the frame resident and dirty. `header.peek/poke_lsn/type_valid` added. New
  `WriteBackError = WriteError || InvalidHeader` (illegal type byte caught at write-back in every
  build mode). Tests: `buffer_pool_dirty_test.zig` (11, 3 page sizes, FaultIo, seeded model).
- PRs: #42 merged (squash, CI 7/7, auto-merged). Issue #34 item 8 ticked.
- Review: code-reviewer 0 critical, 6 warnings; header-validity one fixed, rest documented.
  Cost ~ $2.1 of $4 (zig-developer wrote tests+impl, then reviewer, no test-writer).
- Follow-ups (not blocking): repo has no `stdx.assert_always` (deinit/discardAll pin and dirty checks
  are plain asserts, ReleaseSafe only); `BufferPool.frame_bytes/mark_dirty/Frame` are pub only for
  guard.zig; no `fetchNew` path to initialise a freshly allocated (Unwritten) page, needed before the
  B+Tree; flushAll cleans pinned frames so a later edit through an old slice needs `markDirty`; tests
  with dirty frames at `defer deinit` panic instead of reporting on an earlier failure.
- Next: item 9 — 2C page-size matrix (8 sizes for header/manager/pool) + torn-page sweep via the real
  page decoder in `src/testing/truncation_matrix_test.zig`.
- Blockers: none. Open questions: none.
- Note: Bash guard rejects `;`/`$VAR` chains; one simple command per call. Checking out main after a
  merge makes the editor report "changed on disk" for branch files; `git pull --ff-only` first.

## Cycle 43 — 2026-10-11 — FEATURE
- Done: plan 003 item 7 — `src/cache/buffer_pool.zig`: CLOCK `BufferPool` (`init` in place, `deinit(gpa)`,
  `fetch(io,id)`, `stats`, `pinned_count`, `check_invariants`), `PageGuard` (`bytes` const, `id`, `release`).
  Tests in `buffer_pool_test.zig` (scripted counts at 3 sizes, pins, typed load errors, FaultIo, failing
  allocator, churn, seeded model). cache.zig re-exports BufferPool/PageGuard/Options/Stats/FetchError.
- PRs: #41 merged (squash, CI 7/7, auto-merged). Issue #34 item 7 ticked.
- Review: code-reviewer 0 critical; fixed: table tombstone `rehash` every `frames_max` evictions,
  empty-frame search from the hand, no UB fallthrough, move-only guard doc, id-precondition doc, extra
  tests. Cost ~ $1.55 of $4 (author wrote tests+impl, no test-writer).
- Contract for item 8: `bytes()` is const on purpose (silent lost writes); add a writable view via
  `fetchForUpdate`/`markDirty`. Write-back must run inside `victim_evict` BEFORE `table.remove`; a failed
  load currently drops the victim (clean) — with dirty frames a failed write-back must keep it. `deinit`
  asserts zero pinned frames; add zero dirty. PageGuard lives in buffer_pool.zig (no guard.zig yet).
- Next: item 8 — dirty tracking + write-back + `flushAll`/`discardAll`.
- Blockers: none. Open questions: none.
- Note: `assert(x.remove())` is a side-effect-in-assert trap; `std.hash_map.AutoContext(u32){}` is the
  `rehash` ctx for AutoHashMapUnmanaged; macOS has no `timeout`.

## Cycle 42 — 2026-10-10 — FEATURE
- Done: plan 003 item 6 — `PageManager.allocate/free/sync` (`src/page/manager.zig`, tests in
  `manager_alloc_test.zig`: growth/limit, LIFO, trunk spill+drain at 512 B, reopen, corrupt head/
  entry/next, seeded 600-step model with reopen + full freelist-chain partition check).
- PRs: #40 merged (squash, CI 7/7, auto-merged). Issue #34 item 6 ticked.
- Review: code-reviewer 0 critical, 5 warnings fixed (crash-order doc: write order only holds if
  OS persists in order, WAL owns it; scratch reuse so free uses 128 KiB stack; head short read ->
  Corrupted; double-free doc; CHANGELOG). Cost ~ $1.55 of $4 (tests + impl by author, no test-writer).
- Contract for item 7+: `allocate` returns a reused page with stale bytes (trunk image) until written;
  grown pages read `Unwritten`; deeper-trunk double free is the caller's problem; `free` uses
  `wal_lsn` as page lsn. `page_count_max` bounds growth only.
- Next: item 7 — `cache/buffer_pool.zig` CLOCK fetch + pin (all alloc in init, PoolExhausted, stats).
- Blockers: none. Open questions: none.
- Note: `fixtures.id_of` asserts raw < 64; larger tests need a local id helper. Tidy density is per
  file incl. test helpers; Bash `sleep` loops of <=10 s work for waiting on a background agent.

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
