# strata — context

last_seen_at: 2026-09-10T12:00:00Z
rejected_plans: []

## Cycle 6 — 2026-09-10 — FEATURE
- Done: preflight found leftover empty local branch `test/tidy-0.16-banlist-sweep` (0 commits
  ahead, clean) — left in place (nothing to preserve). Inbox clean (no owner actions, CI
  green, milestone #3 open). Implemented plan 001 item 5 (0.16 library sweep, then freeze
  it): extended `tools/tidy.zig`'s ban list with 5 more 0.15-only spellings (bare `ArrayList`
  `.{}` init, `mem.indexOf`/`lastIndexOf`, `std.net.*`, all 7 `std.Thread.*` sync
  primitives, `fs.cwd()`) via test-writer → zig-developer → code-reviewer. Review caught 4
  over-100-col lines, a false-positive in the `ArrayList` compound check (comment mentioning
  "ArrayList" + unrelated `.{}` on the same line), a missing `mem.lastIndexOf` variant, and
  an inaccurate `fs.cwd()` replacement message — all fixed before commit. 71/71 tidy tests
  green, tidy still reports 0 findings over `src`/`bench`/`tests` (confirms zero real 0.15
  spellings in the stub codebase, as expected).
- PRs: #9 opened, plan item ticked, CHANGELOG updated. CI still `pending` at the 22-min
  cycle deadline — commented "awaiting CI; merge next cycle"; next cycle's inbox merges it.
- Next: next cycle's inbox must merge #9 once CI is green. Then plan 001 item 6 (0.16
  tests: `std.testing.io`, real `tmpDir` round-trip) or item 7 (`io: Io` convention in PRD +
  ADR 0001).
- Blockers: none.
- Open questions: none.

## Cycle 5 — 2026-09-09 — STABILIZATION
- Done: CI green (last 5 runs). tidy-auditor ran a Tiger Style audit; `src/` is still all
  stubs post-0.16-migration, `zig build test` (0.16.0 toolchain) reports 0 tidy findings.
  Its one flagged line-length violation (`src/lsm.zig:1`) was a false positive — naive byte
  counting vs. the tool's correct Unicode-code-point counting (99 ≤ 100); verified by
  rerunning the real tool. Found real docs drift instead: README Zig badge still `0.15.x`
  post-migration, module table implied modules were built, install snippet pointed at an
  unpublished `v0.1.0` tag. Fixed via PR #8; plan 001 "README/CHANGELOG reconciled" item
  ticked; tracking issue #3 commented.
- PRs: #8 merged (auto-merged label), all 7 CI checks green.
- Next: plan 001 item 5 (library sweep — ban-list extension for 0.15-only spellings) or
  item 6 (0.16 tests: `std.testing.io`, real `tmpDir` round-trip) for the next FEATURE
  cycle. For a future STABILIZATION cycle: `tools/tidy.zig` doesn't lint itself
  (`scan_roots` excludes `tools/`) and has no 800-line file-length rule yet (it is itself
  1452 lines) — both recorded in STATE.md.
- Blockers: none.
- Open questions: none.

## Cycle 4 — 2026-09-09 — FEATURE
- Done: preflight found the repo dirty on non-`wip/*` branch `chore/zig-0.16-migration`
  (staged, uncommitted 0.16 migration work) → preserved it to
  `wip/chore-zig-0.16-migration-20260909` (pushed) before switching to main, per protocol.
  Inbox clean (no owner actions, CI green, milestone issue #3 open). Implemented plan 001
  items 4 (`main`, args, allocators) and 7 (pin and CI) as one PR — the two are coupled
  because item 4's `std.process.Init` signature only exists under 0.16.0, and CI still
  pinned 0.15.2, so shipping item 4 alone would go red. Also had to migrate
  `tools/tidy.zig` and `bench/main.zig` (not explicit plan items, but both compile as
  part of `zig build test`/`bench`) — `std.fs.Dir`→`std.Io.Dir`, `std.time.Timer`→
  `std.Io.Clock.Timestamp`, `mem.indexOf`→`mem.find`. code-reviewer caught one CRITICAL
  (a >100-col line tidy couldn't self-lint, since `tools/` isn't in `scan_roots`) and two
  WARNINGs (swallowed `error.Canceled` in tidy's directory-walk `catch return`/`catch
  continue`) — fixed before merge.
- PRs: #7 merged (auto-merged label), all 7 CI checks green.
- Next: plan 001 item 5 (library sweep — ban-list extension for 0.15-only spellings in
  `tools/tidy.zig`; confirm `root.zig`/modules stay clean) or item 6 (0.16 tests:
  `std.testing.io`, real `tmpDir` round-trip).
- Blockers: none.
- Open questions: none.
- Note: local branch `chore/zig-0.16-migration` (pre-cycle, never pushed) and remote
  `wip/chore-zig-0.16-migration-20260909` are now redundant with merged PR #7 but were
  left in place per the "never delete a `wip/*` branch" / "only delete PR-head branches
  you're merging now" rules — safe to prune manually if the owner wants.

## Cycle 3 attempt — 2026-09-08 — PREFLIGHT ABORT (disk)
- Done: nothing — preflight disk gate failed before mode/inbox: `df -g /` reported 17 GB
  available (< 20 GB required). Stopped before touching the repo or GitHub, per the cycle
  preflight rule, to avoid a `zig build` running the host out of space mid-write.
- PRs: none.
- Next: retry plan 001 item 3 (`tidy` step, part 2 — function length ratchet + ban list)
  once disk headroom recovers; counter was not advanced (no cycle work was completed).
- Blockers: host disk space (17 GB avail, need ≥ 20 GB) — not a strata-repo issue, no
  action possible from within this realm.
- Open questions: none.

## Cycle 2 — 2026-09-07 — FEATURE
- Done: inbox clean (no owner actions, CI green on main, milestone issue #3 open with
  plan 001 in progress). Implemented plan 001 item 2 (`tidy` step, part 1 — shape):
  vendored a trimmed subset of the kingdom reference `tidy.zig`
  (`citadel/templates/tidy/tidy.zig`) into `tools/tidy.zig` — line length (≤100 Unicode
  code points) and doc header (`.zig` files under `src/` open with `//!`) — wired into
  `zig build test` via a new `zig build tidy` step. TDD: test-writer wrote 17 in-memory
  unit tests against stub bodies (confirmed 9/17 red), zig-developer implemented
  splitLines/checkLineLength/checkDocHeader/formatFindings + a bounded non-recursive
  directory walk + main() to turn them green. Wiring tidy in surfaced 6 pre-existing
  shape violations in src/ (missing header in main.zig, 5 over-100-column doc comments)
  — fixed in the same PR.
- PRs: #5 merged (auto-merged label), all 7 CI checks green.
- Next: plan 001 item 3 (`tidy` step, part 2 — function length ratchet + ban list).
- Blockers: none.
- Open questions: none.

## Cycle 1 — 2026-09-06 — FEATURE
- Done: plan 001 (PR #2, merged prior cycle) had unchecked items and no milestone issue →
  opened tracking issue #3. Implemented plan 001 item 1 (hygiene leftovers: fixed
  `src/root.zig` doc comment pointing at renamed `docs/milestones.md` → `docs/plans/`;
  added `CHANGELOG.md`) via PR #4, all 7 CI checks green, squash-merged, item ticked on #3.
- PRs: #4 merged (auto-merged label).
- Next: plan 001 item 2 (`tidy` step, part 1 — shape: line length ≤100, `//!` headers).
- Blockers: none.
- Open questions: none.

## History
- Cycle 0 (2026-09-05, RESTRUCTURE): realm created by citadel restructure; memory migrated
  from the repo's former `.claude/memory/`; plan 001 prescribed by ROADMAP.md.

## Standing backlog (carried from the repo's former project-context.md)

- Phase: Bootstrap complete. Next: Phase 1 (`docs/milestones.md` is the single source of
  truth for progress; `docs/PRD.md` is the single source of truth for requirements).
- Version: 0.1.0, unreleased. No git tags yet.
- `zig build test` green on the skeleton (11 trivial compile-check tests); CI registered,
  one fix-up commit already landed (Linux-only test job, macOS covered by cross-compile).
- Queued Phase 1 items, in dependency order:
  1. 1A — codec: CRC32C (hardware-detect + software fallback) and varint; test standard
     vectors, boundary values, hw/sw parity.
  2. 1B — `File` with `SyncPolicy`; test via `tmpDir`: writeAt/readAt/sync/preallocate/lock.
  3. 1D — crash-injection harness; test enumerated truncation points, generated file ends at
     the specified offset. (1D is listed ahead of 1C/mmap because later phases — WAL,
     B+Tree — need the harness before they need mmap.)
- Zig 0.16 migration (plan 001) is trivial for this repo (<1h, one file, one error class —
  see `STATE.md` and `citadel/core/rules/zig-0.16.md`); sequence it with or just before 1A so
  new Phase 1 code is written directly against 0.16 shapes.

## Next priority

Phase 1A (codec) is the next concrete implementation step once plan 001 is approved — it has
no internal dependencies and later phases (page, wal) depend on it.
