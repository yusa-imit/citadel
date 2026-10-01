# strata — context

last_seen_at: 2026-10-01T12:00:00Z
rejected_plans: []

## Cycle 24 — 2026-10-01 — FEATURE
- Done: plan 002 item 4 — `src/codec/xxhash.zig` (asserted `std.hash.XxHash64` wrapper: `hash`,
  streaming `Hasher`, `digest_write`/`digest_read` as 8 LE bytes, explicit seed) plus test-only
  `src/codec/xxhash_reference.zig` (XXH64 from the spec). Tests: published vectors, lengths
  0..130 and 1023..4103 vs reference, chunked streaming, short-buffer error. code-reviewer: 0
  critical; 3 warnings (costly asserts on hot `hash`, test gaps, redundant Hasher state) fixed.
- PRs: #21 merged (squash, CI 7/7 green, labelled auto-merged). Issue #17 item 4 ticked.
- Next: item 5 — `file/file.zig` core (open/close/readAt/writeAt/length/setLength, PRD §4.2).
- Blockers: none. Open questions: none.
- Note: tests were written together with the impl, not strictly red-first (small wrapper); the
  reviewer-found gaps were closed. Guard hook rejects compound Bash (`;`, heredocs) in the repo —
  run zig/git/gh as single simple commands. Tidy density: a test-only reference file needs ≥2
  asserts per fn too; recursion-by-accident in an assert is a trap (caught before commit).

## Cycle 23 — 2026-10-01 — FEATURE
- Done: plan 002 item 3 — `src/codec/crc32c.zig`: `checksum`, streaming `Hasher`, `Path`
  (software table / hardware SSE4.2+ARMv8 chosen at compile time by CPU feature set, not os tag),
  `path_default`. RFC 3720 B.4 vectors, std parity, hw/sw parity at every alignment. code-reviewer:
  0 critical; 2 warnings (costly recompute asserts, duplicated dispatch) fixed pre-merge.
- PRs: #20 merged (squash, CI 7/7 green, labelled auto-merged). Issue #17 item 3 ticked.
- Next: item 4 — `codec/xxhash.zig` (wrapper over `std.hash.XxHash64`, frozen LE digest).
- Blockers: none. Open questions: none.
- Note: x86_64 hw asm is compile-checked only (`-mcpu x86_64+sse4_2`), never executed in CI (CI
  builds generic CPU → software). Zig 0.16 inline asm: no `%w[x]` modifier on aarch64 (use fixed
  `{w9}` regs); no tied `"[name]"` input on x86 (use `"0"`); byte form needs plain `crc32`
  mnemonic with a u32 dest. Tidy density counts `comptime assert` lines; fold wrappers into
  one generic fn (here `checksum_path(comptime path, ...)`).

## Cycle 22 — 2026-09-30 — FEATURE
- Done: plan 002 item 2 implemented — `src/codec/fixed.zig` (generic `read(T, buf)`/
  `write(T, buf, v)` for u16/u32/u64 LE, `error.BufferTooSmall`) and `src/codec/varint.zig`
  (canonical LEB128 u64, zigzag i64, 10-byte cap, `Truncated`/`Overlong`/`BufferTooSmall`;
  decoder rejects non-canonical trailing-zero spellings). code-reviewer: 0 critical, 3
  warnings (unreachable tail, missing Overlong vectors, weak reference) all fixed pre-merge.
- PRs: #19 merged (squash, CI 7/7 green, labelled auto-merged). Issue #17 item 2 ticked.
- Next: item 3 — `codec/crc32c.zig` (hw/sw parity, feature detection not `builtin.os.tag`).
- Blockers: none. Open questions: none.
- Note: tidy's assertion-density is per file (>= 2 per fn incl. comptime asserts, counted by
  line), so tiny wrapper fns hurt — prefer one generic fn over many wrappers. Guard hook
  blocks Bash heredocs/python writing into the repo; use Write/Edit tools. BSD sed has no `\n`.

## Cycle 21 — 2026-09-30 — FEATURE
- Done: plan 002 (PR #16) was merged by the OWNER = approved. Opened milestone issue #17. Item 1
  (`tools/tidy.zig` self-hosting) implemented: zig-developer split it into `tools/tidy/
  {scanner,checks_file,baseline,checks_ban,checks_density,report,walk,lint}.zig` (largest 530
  lines) + 99-line `tools/tidy.zig`; `tools` added to `scan_roots` (assert 3→4), no exemption
  table. `zig build test` now also runs tidy's own 89 unit tests (never ran before; 102 total).
  code-reviewer: 0 critical/warning; fixed its tautology-assert suggestion. Ban needles in
  tidy's own source are spelled with `++` splits so tidy doesn't flag itself.
- PRs: #18 merged (squash, CI 7/7 green, labelled auto-merged).
- Next: item 2 — `codec/fixed.zig` + `codec/varint.zig` (plan 002, issue #17).
- Blockers: none. Open questions: none.
- Note: guard hook blocks compound Bash commands touching citadel paths and `timeout` is absent
  on this box; use separate simple commands. Issue #17's checklist box for item 1 still needs
  ticking (a sed edit failed to match).

## Cycle 20 — 2026-09-29 — FEATURE (no-op)
- Done: preflight clean (disk 65 GB, on main, HEAD c17c5c9, CI green last 5). Plan PR #16
  still open, no reviews/comments since watermark, no issues, no implementation PRs. One
  stabilize --one pass run directly (no subagent; tree unchanged since cycle 19's audit):
  `zig build test`, `zig fmt --check`, `zig build tidy` (0 findings) all green on pinned
  0.16.0 toolchain. Standing gap unchanged: `tools/tidy.zig` (2100 lines) outside `scan_roots`.
- PRs: none opened or merged.
- Next: when #16 merges, open milestone 002 issue, implement tidy self-hosting fix.
- Blockers: none. Open questions: none.
- Note: the guard hook blocked two Bash commands that used `$VAR` toolchain paths, redirects
  to /tmp, or citadel paths in a compound command; plain absolute-path commands work.
- Report: quiet cycle — skipped plan-PR comment per quiet-mode carve-out.

## History
- Cycles 15–19 (2026-09-27..29, FEATURE, no-op): plan PR #16 open awaiting human merge; each ran
  one `/stabilize --one` tidy-auditor pass (always clean: 0 findings, test/fmt/tidy green).
  Cycle 17 hit citadel issue #16 (cross-realm memory-commit lock pileup), fixed by the OWNER in
  citadel PR #20. Cycle 19 self-corrected a stuck `counter` (17 → 19).
- Cycles 13–14 (2026-09-16/17, FEATURE, no-op): plan PR #16 still open awaiting human merge;
  each ran one bounded `/stabilize --one` (tidy-auditor + docs cross-check, always clean).
  Cycle 14 finalized a cycle-13-numbered attempt that crashed before `/report`.
- Cycle 12 (2026-09-16, FEATURE): milestone #3's last item — `/release strata minor` (PR #15,
  tagged v0.2.0, GitHub release published; no consumers yet so no migration issues). Drafted
  and opened plan 002 (PR #16): Phase 1 scope — `tools/tidy.zig` self-hosting fix, codec
  (fixed/varint/crc32c/xxhash), `file/file.zig`, crash-injection harness, bench baseline,
  release v0.3.0 (`file/mmap.zig` deferred to plan 003).
- Cycle 11 (2026-09-15, FEATURE): `wip/*` decision — diffed
  `wip/chore-zig-0.16-migration-20260909` vs main, confirmed strictly superseded by PRs
  #7/#11/#13; left in place per never-delete rule, recorded in decisions.md.
- Cycle 10 (2026-09-13, STABILIZATION, forced n%5==0): merged leftover PR #13
  (`checkFileLength` 800-line rule) and PR #14 (changelog fix for it). Flagged
  `tools/tidy.zig`'s self-lint gap (2100 lines, excluded from `scan_roots`, needs a design
  decision — baseline-exemption mechanism or file split) as a standing STATE.md item, not an
  ad-hoc fix.
- Cycle 9 (2026-09-12, FEATURE): plan 001 "Assertion baseline" — `tidy`'s assertion-density
  check (PR #12). code-reviewer caught two real bugs pre-merge: a draft assert on user CLI
  input that would have panicked on empty strings, and a density counter miscounting
  `assert(` inside comments.
- Cycle 8 (2026-09-11, FEATURE): `io: Io` convention + ADR-0001 (PR #11, docs-only).
  architect: strata never constructs an `Io`; only `kv.Db` caches one (set once at `open`).
  code-reviewer caught a design gap — `wal.Reader.next()` null was ambiguous between EOF and
  a torn frame; fixed by reserving null strictly for EOF.
- Cycle 7 (2026-09-11, FEATURE): first real I/O test (`std.testing.tmpDir` round-trip via
  `std.testing.io`), PRs #9–#10.
- Cycle 6 (2026-09-10, FEATURE): plan 001 item 5 — extended tidy's ban list with 5 more
  0.15-only spellings (PR #9).
- Cycle 5 (2026-09-09, STABILIZATION): docs drift fix (README badge/module table/install
  snippet) via PR #8; flagged tools/tidy.zig's missing self-lint and file-length rule.
- Cycle 4 (2026-09-09, FEATURE): preserved dirty branch to
  `wip/chore-zig-0.16-migration-20260909`; real 0.16 migration landed via PR #7.
- Cycle 3 attempt (2026-09-08): disk gate failed (17 GB < 20 GB); aborted, counter not
  advanced.
- Cycle 2 (2026-09-07, FEATURE): tidy shape checks (line length, `//!` headers) via PR #5.
- Cycle 1 (2026-09-06, FEATURE): opened tracking issue #3 for plan 001 (PR #2); hygiene
  leftovers via PR #4.
- Cycle 0 (2026-09-05, RESTRUCTURE): realm created by citadel restructure; plan 001
  prescribed by ROADMAP.md.

## Standing backlog (carried from the repo's former project-context.md)

- Phase: Bootstrap complete. Next: Phase 1 (`docs/milestones.md` is the single source of
  truth for progress; `docs/PRD.md` is the single source of truth for requirements).
- Version: 0.1.0, unreleased. No git tags yet.
- Queued Phase 1 items, in dependency order:
  1. 1A — codec: CRC32C (hardware-detect + software fallback) and varint; test standard
     vectors, boundary values, hw/sw parity.
  2. 1B — `File` with `SyncPolicy`; test via `tmpDir`: writeAt/readAt/sync/preallocate/lock.
  3. 1D — crash-injection harness; test enumerated truncation points, generated file ends at
     the specified offset. (1D is listed ahead of 1C/mmap because later phases — WAL,
     B+Tree — need the harness before they need mmap.)

## Next priority

Milestone 001 closed cycle 12 (v0.2.0 released, tag + GitHub release live). Plan 002 (PR #16)
is open for human approval, scoping Phase 1: `tools/tidy.zig` self-hosting fix first, then
codec (fixed/varint/crc32c/xxhash), `file/file.zig`, the crash-injection harness, a bench
baseline, and release v0.3.0. Once #16 merges, `/cycle` opens the milestone 002 tracking issue
and implementation starts with the tidy fix (blocks nothing else, unblocks a clean lint for
every feature PR after it).
