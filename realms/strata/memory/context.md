# strata — context

last_seen_at: 2026-10-10T00:00:00Z
rejected_plans: []

## Cycle 41 — 2026-10-10 — FEATURE
- Done: plan 003 item 5 — `src/page/manager.zig`: `PageManager` create/open/read/write (exclusive
  tryLock, ADR-0002 §5 open sequence, short/foreign file -> Corrupted, EOF inside a page ->
  TornWrite, page-0 bad CRC -> ChecksumMismatch). `Options{page_size, page_count_max,
  sync_policy}`; fields page_size/page_count/freelist_head/wal_lsn/page_count_max are public.
  Tests in `manager_{test,page_test,model_test,fixtures}.zig` (167 tests incl. FaultIo, model, fuzz).
- PRs: #39 merged (squash, CI 7/7, auto-merged). Issue #34 item 5 ticked.
- Review: no code-reviewer pass (cost: test-writer alone ~$1.5 of $4 — it hand-built a reference
  impl and mutants). Reused that reference as the base of manager.zig. Do the reviewer on item 6.
- Contract for item 6: `read`/`write` assert 0 < id < page_count; page 0 is manager-owned, so item 6
  needs an internal file-header writer (page_count/freelist_head update, trunk first then page 0).
  `create` does not enforce `page_count_max` (allocate does). Open does not check page_count vs max.
- Next: item 6 — `allocate`/`free`/`sync`/reopen (seeded model with reopen between rounds).
- Blockers: none. Open questions: none.
- Note: for test-writer prompts, cap scope (it spent ~7 min / $0.85+); the Bash guard rejects
  `;`/`cd`/`$VAR` chains, run one simple command per call. `zig test` cannot take a `_test.zig`
  root outside the module path.

## Cycle 40 — 2026-10-09 — FEATURE
- Done: plan 003 item 4 — `src/page/freelist.zig` (trunk codec per ADR-0002 §7): `format_trunk`,
  `decode_trunk`, `free(head, head_page, freed, freed_page, lsn) -> Release{head, written}`,
  `allocate(head, head_page, lsn) -> Allocation{id, head, head_dirty}`, `trunk_capacity`. Tests in
  `freelist_test.zig` (seeded 10k-op model at 512 B/4 KiB, 8-size matrix, every Corrupted case).
- PRs: #38 merged (squash, CI 7/7, auto-merged). Issue #34 item 4 ticked.
- Review: code-reviewer 0 critical, 5 warnings fixed (double-free assert before the full-head
  branch, trunk listing itself rejected in decode, size matrix, untouched-page + lsn checks).
  Tests were written alongside the implementation, not strictly red-first (cost control, ~$1.1).
- Contract for item 5/6: the manager maps file-header 0 <-> null for `head`, range-checks ids
  against `page_count`, rejects double free of non-head pages, writes trunk first then page 0.
  Duplicate ids across trunks are NOT detected by decode; the manager's bounded walk owns it.
- Next: item 5 — `page/manager.zig` create/open/read/write (`File`, io per call, tryLock on open,
  `peek_page_size` then full decode; no new `File` methods, file.zig is 788/800 lines).
- Blockers: none. Open questions: none.
- Note: tidy density counts `assert(` per fn per file (>= 2), incl. test helpers; `mem.indexOf`
  is banned (use `findScalar`); python3 heredoc edits work in strata (Bash guard only blocks citadel).

## Cycle 39 — 2026-10-09 — FEATURE
- Done: plan 003 item 3 — `src/page/header.zig` (page header, file header, `peek_page_size`,
  id-seeded CRC32C) per ADR-0002. `page.Id` lives in header.zig, re-exported by `page.zig`.
  Tests (29) are in `src/page/header_test.zig` (tests + code exceeded the 800-line tidy limit
  in one file); test-writer mutation-checked them (8 mutants caught).
- PRs: #37 merged (squash, CI 7/7, auto-merged). Issue #34 item 3 ticked.
- Next: item 4 — `page/freelist.zig` trunk codec (ADR-0002 §7; tests first: capacity at 8
  sizes, seeded 10k-op model, spill/drain, the three Corrupted cases).
- Blockers: none. Open questions: none.
- Note: no independent code-reviewer pass this cycle (budget: test-writer + developer agents
  cost ~$1.8 of $4); author read the diff against the ADR. Do the reviewer on item 4 if budget
  allows. Tidy bans `catch unreachable`; use `catch |err| switch (err) { ... => unreachable }`
  with a proof comment. Guard hook rejects `cd`/`;` chains in Bash; `git -C` works.

## Cycle 38 — 2026-10-08 — FEATURE
- Done: plan 003 item 2 — ADR-0002 page format v1 (`docs/adr/0002-page-format.md`, drafted by the
  architect agent). Fixes: 24-byte header (magic, type, flags, version, checksum@8, reserved@12,
  lsn@16), CRC32C seeded with u64 page id and checksum field read as zero, `Id = enum(u32)` with
  0 = null, page 0 = ordinary page + 48-byte file header, all-zero page decodes to
  `error.Unwritten`, decode order magic/version/checksum/then type, trunk-only freelist
  (`capacity = (page_size-32)/4`). PRD §4.3 links it; plan items 1 and 2 ticked.
- PRs: #36 merged (squash, CI 7/7, auto-merged). Issue #34 item 2 ticked.
- Next: item 3 — `src/page/header.zig` codecs per ADR-0002 §9 (tests first: golden image, all
  bit flips at 512 B, other-id decode, zero page at 8 sizes).
- Blockers: none. Open questions: none.
- Note: agent output may arrive HTML-escaped (`&lt;`); unescape before writing. macOS has no
  `timeout`; use `gh pr checks --watch` directly. Plan item 1 had never been ticked in the plan
  file; fixed in #36.

## Cycle 37 — 2026-10-08 — FEATURE
- Done: plan 003 approved (PR #28 merged by OWNER); opened milestone issue #34. Item 1 done: tidy
  ADR-0001 `Io` guards — `Io.Threaded`/`Io.Evented`/`global_single_threaded` banned under `src/`,
  new `io-field` rule (Io struct field only in `src/kv/db.zig`, `src/testing/fault_io.zig`;
  multi-line param lists skipped via paren depth).
- PRs: #35 merged (squash, CI 7/7, auto-merged). Issue #34 item 1 ticked.
- Next: item 2 — ADR-0002 page format v1 (`docs/adr/0002-page-format.md`), then item 3 header codec.
- Blockers: none. Open questions: none.
- Note: PATH zig is 0.15.2; use the 0.16.0 toolchain with `--cache-dir /tmp/strata-zc`. macOS
  `sed -i` needs `''`. A failed `&&` skips a following `Z=...` assignment. The guard hook blocks
  compound Bash that writes into citadel; use Write/Edit for memory files.

## Cycle 36 — 2026-10-07 — FEATURE
- Done: plan PR #28 still open (CI 7/7 green, only our own status note, no OWNER feedback, no open
  issues), so one `/stabilize --one`: `allocator:` params renamed `gpa` across `tools/tidy/*.zig`.
- PRs: #33 merged (squash, CI 7/7, auto-merged).
- Remaining audit sweeps: `std.debug.assert` alias across `tools/` (~65; tidy ban check does not flag
  it); assertion density elsewhere in `tools/` (tidy density gate covers `src/` only); camelCase
  public API in `src/file/file.zig` (needs a plan).
- Next: when #28 merges, open "milestone: 003 ..." and start item 1 (tidy ADR-0001 Io guards).
- Blockers: none. Open questions: none (freelist trunk-list-only call is in #28 for the OWNER).
- Note: the `gh pr checks --watch` call right after PR create may say "no checks reported"; rerun.

## Cycle 32 — 2026-10-05 — FEATURE
- Done: plan PR #28 still open (CI green, no new OWNER comment; only our own status note), so one
  `/stabilize --one`: tidy-auditor re-audit of the v0.3.0 tree, STATE.md Tiger Style table
  replaced (412 asserts / 197 fns = 2.09; 0 files > 800; 0 fns > 70; nothing banned in `src/`).
- PRs: #29 merged (squash, CI 7/7, auto-merged): `src/main.zig` returns the stdout flush error
  instead of `catch {}`, and aliases `assert` once.
- Remaining audit sweeps, smallest first: `//!` header on `build.zig`; assertion density in
  `tools/tidy/baseline.zig` (1.08) and `checks_ban.zig` (1.33); `allocator:` -> `gpa:` and the
  `std.debug.assert` alias across `tools/` (~88, tidy ban check does not flag it); camelCase
  public API in `src/file/file.zig` (needs a plan, it is public).
- Next: when #28 merges, open "milestone: 003 ..." and start item 1 (tidy ADR-0001 Io guards).
- Blockers: none. Open questions: none (freelist trunk-list-only call is in #28 for the OWNER).
- Note: the guard hook rejects compound Bash; run one simple command per call.

## Cycle 31 — 2026-10-05 — FEATURE
- Done: plan 002 item 10 — PR #27 merged (docs, `NotImplemented` dropped from codec/file/testing,
  README rows Landed, `strata.version` fixed 0.1.0→0.3.0, CHANGELOG + zon 0.3.0); tag v0.3.0 +
  GitHub release created; milestone #17 closed. No consumers, no migration issues. STATE.md has
  the v0.3.0 entry; its Tiger Style table is still the pre-Phase-1 audit (re-audit pending).
- Plan 003 proposed (Phase 2 page + CLOCK buffer pool, ends v0.4.0), PR #28, awaiting merge.
  Scope cut for the human: freelist is trunk-list only, bitmap deferred. Plan item 1 adds the
  ADR-0001 tidy guards (never landed). `file.zig` is 788/800 lines: no new `File` methods.
- Next: when #28 merges, open milestone issue "milestone: 003 ..." and start item 1.
- Note: guard hook rejects compound Bash and `$VAR` paths into citadel; use simple commands.

## Cycle 30 — 2026-10-04 — FEATURE
- Done: plan 002 item 9 — `bench/main.zig` codec baseline: crc32c software + hardware (hardware
  only when `hardware_available`, else a "skipped" line), xxhash64, varint encode/decode over a
  seeded fixture (1 MiB buffer, 64 Ki values, 256 passes); prints GB/s, ops/s, ns/op. Kernels and
  report formatting are unit-tested (`bench_tests` in build.zig) and the ReleaseFast bench exe is
  compiled by `zig build test`. Figures on Apple aarch64 recorded in `docs/plans/000-inherited.md`
  (crc hw 5.3 GB/s, sw 0.58, xxhash 26.2, varint enc 198 M/s, dec 151 M/s). code-reviewer: 0
  critical, 6 warnings fixed pre-commit (decode hoisting guard, restore values[0], real
  StreamLengthMismatch error instead of ReleaseFast-erased assert, overflow asserts, pinned
  boundary values 0/127/128/maxInt, compile gate for bench exe).
- PRs: #26 merged (squash, CI 7/7 green, labelled auto-merged). Issue #17 item 9 ticked.
- Next: item 10 — docs, module status, release v0.3.0 (drop `NotImplemented` from codec.zig/file.zig,
  README rows Planned→Landed, tick 1A/1B/1D in 000-inherited, re-audit STATE.md, CHANGELOG +
  `.version = "0.3.0"`, tag). Then `/release strata minor` closes #17.
- Blockers: none. Open questions: none.
- Note: guard hook rejects compound Bash (`;`, `&&`-heavy, $VAR paths into citadel); run simple
  commands. Waiting on a background agent works with a bounded `for … sleep 10` loop grepping
  the output file for `"stop_reason":"end_turn"`.

## Cycle 29 — 2026-10-04 — FEATURE
- Done: plan 002 item 8 — `src/testing/truncation_matrix_test.zig`: CRC32C-framed record
  `[u32 len][payload][u32 crc]`, every `.truncate`/`.torn` cut at all points for sizes 8..64 KiB;
  each damaged prefix must be TornWrite or ChecksumMismatch; broken decoders fail the sweep.
- PRs: #25 merged (CI 7/7). Note: a torn cut one byte past a sector boundary is a clean truncation.
  Replace the fixed-frame test decoder with the real WAL/page frame decoder when those land.

## Cycle 28 — 2026-10-03 — FEATURE
- Done: fixed PR #24's Linux-red CI (`FaultIo` must forward `checkCancel`; Linux `sync_data`
  calls it, macOS never does). Plan 002 item 7 (`testing/crash.zig` + `FaultIo`) done.
- Note: counter had been stuck at 26 (cycle 27's report ran out of budget). Use
  `/Users/fn/.zr/toolchains/zig/0.16.0/zig` (PATH zig is 0.15.2). Any new `Io` wrapper must forward
  every slot `File`/`platform` reach; compile-check Linux with
  `zig test src/root.zig -target x86_64-linux --test-no-exec`. Builds need `--cache-dir /tmp/strata-zc`.

## Cycle 26 — 2026-10-02 — FEATURE
- Done: plan 002 item 6 — `File.sync` (exhaustive on `SyncPolicy`), `preallocate`, `lock`/`tryLock`/
  `unlock`; `src/file/platform.zig` is the only os-branching file. Reviewer CRITICAL fixed
  (`sync_full` fallback only for OPNOTSUPP/NOTTY/INVAL/NODEV).
- Note: `file.zig` is 788/800 lines — further `File` methods go in a new file. `sync_data` (linux)
  and `reserve` bypass `Io` via raw syscalls. Windows locks are mandatory; lock tests skip there.

## Cycle 25 — 2026-10-01 — FEATURE
- Done: plan 002 item 5 — `src/file/file.zig` core (`File` leaf value, no cached io; open/close/
  readAt/readAtAll/writeAt/writeAtAll/length/setLength; `SyncPolicy`, `OpenOptions`; `direct` =>
  `UnsupportedDirectIo`). `PageSizeUnaligned` declared but unreturned until direct-IO.
  1<<40 sparse tests assume a sparse-file FS.

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

Plan 003 approved; milestone issue #34. Items 1-5 done; implement item 6 (manager allocate/free/sync).
