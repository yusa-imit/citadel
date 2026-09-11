# strata — context

last_seen_at: 2026-09-12T00:00:00Z
rejected_plans: []

## Cycle 9 — 2026-09-12 — FEATURE
- Done: preflight clean tree on main, CI green (last run success, not matching origin/main
  SHA only because of paths-ignore on docs-only #11 — not red per rule). Inbox: no owner
  actions since watermark beyond our own prior cycle-report comments, no plan PR, milestone
  #3 open. Implemented plan 001 item "Assertion baseline": new `assertion-density` check
  in `tools/tidy.zig` — a `src/` file with >=1 function-with-a-body must average >= 2
  `assert(`/`assert_always(` calls per function (comment text stripped before matching);
  `zig build test`/`tidy` now print a per-file density report unconditionally. Applied the
  worked-example pair to `src/main.zig`'s `main` (precondition + `defer` postcondition on
  `args`). Implemented directly (TDD by hand, no subagents for red/green) given the tight
  22-min cycle deadline; used code-reviewer (sonnet) before opening the PR, which caught
  and got fixed two real bugs pre-merge: a draft `assert(cmd.len > 0)` on `args[1]` would
  have panicked strata on legitimate empty-string CLI input (Tiger Style: never assert
  user data) — replaced with the args-based pair instead; the density counter counted
  `assert(` mentioned inside `//` comments, defeating the ratchet's purpose — fixed with a
  `stripLineComment` helper (mirrors `braceDelta`'s string/char tracking) plus a regression
  test. Also fixed 5 new >100-col test lines the reviewer caught (tidy doesn't lint its own
  `tools/` dir, so these slipped `zig build tidy`).
- PRs: #12 merged (auto-merged, 7/7 CI green, squash + branch deleted).
- Next: milestone #3 remaining — `wip/*` decision (confirm `git branch -r` clean, delete
  merged `chore/kingdom-restructure`), then release v0.2.0.
- Blockers: none.
- Open questions: none.

## Cycle 8 — 2026-09-11 — FEATURE
- Done: preflight clean tree on main, CI green, no bug/question/directive issues, no open
  PRs. Inbox: no owner actions, watermark advanced, no plan PR/closed-unmerged plans.
  Milestone #3 open with unchecked items → implemented plan 001 item `io: Io` convention
  in the public API (ADR-0001). architect (opus) decided the io-placement rule: strata
  never constructs an `Io` (binary injects at `main`); exactly one type, `kv.Db`, caches
  it (set once at `open`, never reassigned); every other module
  (file/page/cache/wal/btree/lsm/snapshot) takes `io: Io` per call, first parameter after
  the receiver. Wrote `docs/adr/0001-io-injection.md`, rewrote `docs/PRD.md` §4.2/§4.4-§4.9
  signatures onto `Io.Dir`/`Io.File`; `snapshot.Writer`/`Reader` now take
  `*Io.Writer`/`*Io.Reader` instead of `anytype`. code-reviewer (sonnet) found and I fixed:
  >100-col markdown lines in the new ADR table + a PRD bullet, an ADR "Applies to" line
  omitting the touched §4.3, an ADR-0001-vs-memory-ADR-001 numbering ambiguity, and a real
  design gap — `wal.Reader.next()` returning `null` was ambiguous between clean EOF and a
  torn/corrupted frame, which would have broken idempotent-recovery verification in Phase
  3; fixed by reserving `null` strictly for EOF and routing corruption through `NextError`.
  Documentation-only, no Zig source touched (all 10 modules still stubs).
- PRs: #11 merged (auto-merged, 7/7 CI green, squash + branch deleted).
- Next: milestone #3 remaining — assertion baseline (tidy density check + `src/main.zig`
  worked example), `wip/*` decision (confirm `git branch -r` clean, delete merged
  `chore/kingdom-restructure`), then release v0.2.0.
- Blockers: none.
- Open questions: none.

## Cycle 7 — 2026-09-11 — FEATURE
- Done: preflight clean tree on `test/0.16-library-sweep-banlist` (open PR #9 head, nothing
  to preserve) → switched to main. Inbox: no bug/question/directive issues, CI green (last
  matrix run predates the docs-only #8 merge commit due to paths-ignore — not red per rule).
  Merged PR #9 (held from cycle 6, CI had gone green: 7/7 checks) — plan 001 item 5 ticked.
  Implemented plan 001 item 6 (0.16 tests): test-writer → code-reviewer (no zig-developer
  needed, no new production code) added one real `std.testing.tmpDir` round-trip test in
  `src/testing.zig` — write/read through `std.testing.io` + `Io.Dir.{writeFile,
  readFileAlloc}`, plus a negative-space `error.FileNotFound` check added per the reviewer's
  SUGGESTION. First I/O-touching test in the repo (prior 12 were `refAllDecls` stubs).
  Used the pinned 0.16.0 toolchain directly (`/Users/fn/.zr/toolchains/zig/0.16.0/zig`) since
  the system `zig` is still 0.15.2 and strata has already migrated.
- PRs: #9 merged (auto-merged), #10 opened+merged same cycle (auto-merged), both 7/7 CI
  green. Milestone #3 now 8/12 checked.
- Next: milestone #3 remaining items — `io: Io` convention in the public API + ADR-0001
  (needs `architect`, PRD.md §4.2/4.4-4.9 rewrite), assertion baseline (tidy density check
  + `src/main.zig` worked example), `wip/*` decision (confirm `git branch -r` clean, delete
  merged `chore/kingdom-restructure`), then release v0.2.0.
- Blockers: none.
- Open questions: none.

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

## History
- Cycle 1 (2026-09-06, FEATURE): opened tracking issue #3 for plan 001 (PR #2, merged);
  implemented item 1 (hygiene leftovers — `src/root.zig` doc comment, `CHANGELOG.md`) via
  PR #4, item ticked.
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
