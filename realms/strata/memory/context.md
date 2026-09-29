# strata — context

last_seen_at: 2026-09-30T02:20:00Z
rejected_plans: []

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

## Cycle 19 — 2026-09-29 — FEATURE (no-op)
- Housekeeping: `memory/counter` was found stuck at 17 even though a cycle-18 entry already
  existed in this file — the prior cycle's `/report` wrote context.md but its counter write
  never landed (citadel commit for that cycle touched only context.md). Self-corrected: this
  run is cycle 19, counter now written as 19. No other memory files were affected.
- Done: preflight clean, on main, CI green at c17c5c9 (last 5 runs, all success). Plan PR #16
  still open, no new OWNER comments since watermark, no bug/question/directive issues, no open
  implementation PRs. One stabilize --one tidy-auditor pass (pinned 0.16.0 toolchain): 0 new
  findings across all mechanical checks (catch unreachable, @panic, debug.print, unbounded
  while, recursion, function/file length, usize in formats, missing //! headers, std.time/
  crypto.random in src/); `zig build test`/`fmt --check`/`tidy` all green. Only the pre-
  existing, deliberately-deferred gap remains: `tools/tidy.zig` (2100 lines) still excluded
  from its own `scan_roots` and over the 800-line limit — needs a design decision, not a fix.
- PRs: none opened or merged.
- Next: when #16 (plan PR) merges, open milestone 002 issue, implement tidy self-hosting fix.
- Blockers: none. Open questions: none.
- Report: quiet cycle (identical block to 15-18: plan PR open, no owner actions, no PR) —
  skipped the plan-PR GitHub comment per quiet-mode carve-out.

## Cycle 18 — 2026-09-28 — FEATURE (no-op)
- Done: preflight clean, CI green at c17c5c9 (last 5 runs, all success). Plan PR #16 still
  open, no new OWNER comments since watermark, no open issues, no comments on merged PRs.
  One stabilize --one tidy-auditor pass: 0 new findings across all mechanical checks (catch
  unreachable, @panic, debug.print, unbounded while, function/file length, usize in formats,
  missing //! headers); `zig build test`/`fmt --check`/`tidy` all green on pinned 0.16.0
  toolchain; README/CHANGELOG match released v0.2.0. Only the pre-existing, intentionally-
  deferred gap remains: `tools/tidy.zig` (2100 lines) still excluded from its own
  `scan_roots` and still over the 800-line limit — unchanged, needs a design decision, not
  fixed ad-hoc.
- PRs: none opened or merged.
- Next: when #16 (plan PR) merges, open milestone 002 issue, implement tidy self-hosting fix.
- Blockers: none — citadel issue #16 (cross-realm memory-commit lock pileup) was root-caused
  and fixed by the OWNER in citadel PR #20 (rewrote `citadel_commit.py` to build each commit
  from `origin/main` + the calling realm's own files in a private index, independent of other
  realms' dirt or the shared checkout's branch). Open questions: none.
- Report: quiet cycle (identical block to 15/16/17: plan PR open, no owner actions, no PR
  opened/merged) — skipped the plan-PR GitHub comment per quiet-mode carve-out; sending one
  Discord heartbeat since none logged for strata yet today (2026-09-28).

## Cycle 17 — 2026-09-27 — FEATURE (no-op)
- Done: preflight clean, CI green at c17c5c9 (last 5 runs). Plan PR #16 still open, no new
  OWNER comments, no bug/question/directive issues. One stabilize --one audit: tidy-auditor
  clean pass — 0 findings across all mechanical checks; `zig build test`/`fmt --check`/
  `tidy` all green; README/CHANGELOG match released v0.2.0. Nothing to fix. citadel-side:
  `citadel_commit.py strata 17` hit the pre-existing cross-realm lock pileup tracked in
  citadel issue #16 (opened by sigil cycle 22) — 6-7 other realms' memory staged-but-
  uncommitted in the shared citadel index, unchanged across a 6-attempt/2-min retry. Strata's
  own cycle-17 memory edit is now staged in that same index (no data lost, just unpushed —
  will commit automatically once #16 is resolved by a human or a citadel cycle). Added a
  confirmation comment to #16 rather than opening a duplicate.
- PRs: none opened or merged.
- Next: when #16 (plan PR) merges, open milestone 002 issue, implement tidy self-hosting fix.
  Separately, watch citadel issue #16 (lock pileup) — once resolved, this and prior cycles'
  memory commits should push through.
- Blockers: citadel-side memory commit blocked by citadel issue #16 (cross-realm lock
  pileup) — needs-human, not strata-specific. Open questions: none.
- Report: quiet cycle (identical block to 15/16, no owner actions, no PR) — skipped the
  plan-PR GitHub comment; skipped Discord heartbeat too (6 sends logged kingdom-wide on
  2026-09-27 UTC already, likely including strata's own cycle 15/16 heartbeat — erred
  against re-sending same-day).

## Cycle 16 — 2026-09-27 — FEATURE (no-op)
- Done: preflight clean, CI green at c17c5c9. Plan PR #16 still open, no comments. One
  stabilize --one audit: 0 banned constructs, files <800 lines, headers ok; nothing to fix.
- PRs: none opened or merged.
- Next: when #16 merges, open milestone 002 issue, implement tidy self-hosting fix.
- Blockers: none. Open questions: none.

## Cycle 15 — 2026-09-27 — FEATURE (no-op)
- Done: preflight clean, CI green at c17c5c9. Plan PR #16 (plan 002) still open, no comments.
  One stabilize check: `zig build test`, `zig fmt --check`, banned-construct grep all clean.
- PRs: none opened or merged.
- Next: when #16 merges, open milestone 002 issue, implement tidy self-hosting fix.
- Blockers: none. Open questions: none.

## History
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
