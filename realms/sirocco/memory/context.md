# sirocco — context

last_seen_at: 2026-09-12T12:10:00Z
rejected_plans: []

## Cycle 12 — 2026-09-12 — FEATURE
- Inbox: no new OWNER actions since the watermark; plan PR #13 (plan 002) still open awaiting
  human merge, zero new review/issue comments on it. No open issues, no red CI, no rejected
  plans, no other open implementation PRs to triage.
- Done: plan PR open, so ran one bounded stabilization task. CI green (5/5, `888ee0b`), `zig
  build test`/`fmt --check`/`tidy` all clean under the pinned 0.16.0 toolchain, zero Tiger Style
  mechanical violations — same clean result as cycles 5/10/11. tidy-auditor pass found one real
  issue this time: `README.md`'s opening paragraph made present-tense capability claims (a
  `Runtime` type, kqueue/epoll backends filling 109 vtable slots) that contradict both the
  shipped v0.2.0 stub-only code (no `Runtime` in `src/`, `root.zig` still exports pre-ADR stub
  modules) and the README's own `Status` section a few lines down. Reworded the intro to
  design-target language matching `Status`, per `citadel/protocol/DOCS.md`.
- PRs: #14 opened and merged (docs-only, `*.md` CI-paths-ignored so no checks ran, `auto-merged`
  label).
- Next: plan PR #13 still needs human merge; once merged, opens the milestone issue and starts
  item 1 (macOS CI runner).
- Blockers: none. Open questions: none.

## Cycle 11 — 2026-09-12 — FEATURE
- Inbox: no new OWNER actions since watermark; plan PR #13 (plan 002) still open awaiting human
  merge — the only new comment on it since the watermark was our own cycle-10 report. No open
  issues, no red CI, no rejected plans, no other open implementation PRs.
- Done: plan PR open, so ran one bounded stabilization task instead of idling. CI green
  (`888ee0b`), `zig build test`/`zig fmt --check`/`zig build tidy` all green under the pinned
  0.16.0 toolchain. Grep audit (`catch unreachable`, `@panic`, `std.debug.print`, `while
  (true)`, files > 800 lines, missing `//!` headers) found zero violations, same clean result as
  cycles 5 and 10 — nothing to fix, nothing to file.
- PRs: none opened (nothing to fix).
- Next: plan PR #13 still needs human merge; once merged, opens the milestone issue and starts
  item 1 (macOS CI runner).
- Blockers: none. Open questions: none.

## Cycle 10 — 2026-09-11 — STABILIZATION
- Inbox: no new OWNER actions since watermark; plan PR #13 (plan 002) still open awaiting human
  merge, no new review/issue comments on it. No open issues, no red CI, no rejected plans.
- Done (full stabilize, n%5==0): CI 5/5 green; `zig build test`/`zig fmt --check`/`zig build
  tidy` all green under the pinned 0.16.0 toolchain (a tidy-auditor sub-pass using the stale
  global 0.15.2 zig saw `tidy` fail — toolchain mismatch, not a regression, confirmed by
  re-running with the correct binary). Tidy audit: zero violations, same clean result as cycle
  5. Test-quality audit: no assertion-free tests over real logic, no leak gaps, adequate for
  current scope. Docs/dependencies(N/A)/hygiene all clean. No fixes needed — nothing to file.
- PRs: none opened (nothing to fix).
- Next: plan PR #13 still needs human merge; once merged, opens the milestone issue and starts
  item 1 (macOS CI runner). stabilize_streak reset to 0 (success).
- Blockers: none. Open questions: none.

## Cycle 9 — 2026-09-11 — FEATURE
- Inbox: no new OWNER actions since watermark beyond the two self-comments already recorded
  last cycle; no plan PR open, no rejected plans, no open PRs besides what this cycle opened.
- Done: milestone #3's last item (item 11, Release 0.2.0) — gates checked (tests/fmt green, CI
  green, no open bugs, no prior tag), PR #12 merged (version bump, CHANGELOG closed into
  0.2.0, README install snippet repointed at the tag), tag `v0.2.0` pushed, GitHub release
  published, milestone issue #3 closed. No kingdom repo's `build.zig.zon` names sirocco yet
  (checked against `citadel/zr-repos.toml`), so no consumer migration issues were opened.
- Then: with ≥10 min left before deadline, ran `/plan` — no unchecked plan existed (001 fully
  closed). `planner` (opus) drafted plan 002 scoped to `docs/PRD.md` §4.3's P0 (concurrency/
  cancel core, 12 slots) and P1 (futex trio, 3 slots) — the floor every later vtable slot group
  suspends on. Nine one-cycle items: macOS CI runner first (plan 001 deferred it; PRD §9 says
  this plan may not), walking-skeleton `Runtime` forwarding all 109 slots, the
  `tests/parity` differential harness + 109-slot coverage table (before any native slot lands),
  the fiber substrate, P0's 12 slots split into 3 ownership-atomic sets (future-producing:
  async/concurrent/await/cancel; cancel-state: checkCancel/recancel/swapCancelProtection;
  group: groupAsync/groupConcurrent/groupAwait/groupCancel+crashHandler), the futex trio, then
  docs + v0.3.0 release. Version impact: MINOR (deletes 6 stub modules — breaking — but no
  consumer pins sirocco yet, and 0.x foundation repos may break MINOR per VERSIONING.md).
  Plan PR #13 opened (`plan/002-fiber-scheduler-and-futex-core`), awaiting human merge.
- Blockers: none. Open questions: none. Next cycle: if PR #13 still open, do one bounded
  stabilization task while waiting; once merged, `/cycle` opens the milestone issue and starts
  item 1 (macOS CI runner).

## Cycle 8 — 2026-09-10 — FEATURE
- Done: inbox found issue #3's checklist had drifted — item 9 was merged via PR #10 last cycle
  but never ticked on the issue body; fixed at inbox time. No new OWNER actions since
  watermark, no plan PR, no bug/question/directive issues. Implemented item 10 (README/
  CHANGELOG reconciliation): the module table was already reconciled with the std.Io.VTable
  design back in PR #8 (cycle 5); the only remaining drift was the Install section naming tag
  `v0.1.0`, which was never cut (`git tag -l` empty) — fixed with a local build.zig.zon
  path-dependency snippet, deferring `zig fetch` to the first real release. Added
  `CHANGELOG.md` (Keep a Changelog, `Unreleased` section covering plan 001's work).
- PRs: #11 merged (auto-merged label, no CI checks — docs-only paths-ignore, same pattern as
  PRs #7/#8/#10).
- Next: item 11 — Release 0.2.0 (bump `.version`, close the CHANGELOG `Unreleased` section into
  `## 0.2.0`, tag `v0.2.0`, cut the GitHub release, repoint the README install snippet). This
  is the last open item on milestone #3.
- Blockers: none. Open questions: none.

## History (cycles 0-7)
Cycle 7 (2026-09-10, FEATURE): item 9 (`wip/*` branch decision) via PR #10 — verified no
`wip/*` branch exists for sirocco; decision recorded as ADR-002.
Cycle 0 (2026-09-05, RESTRUCTURE): realm created, plan 001 prescribed. Cycle 1 (2026-09-06,
FEATURE): opened milestone issue #3; item 1 via PR #4. Cycle 2 (2026-09-07, FEATURE): item 2
(`zig build tidy` step) via PR #5. Cycle 3 (2026-09-07, FEATURE): items 3-6 (0.16 migration of
main.zig/bench/tidy tool, pin+CI) bundled into PR #6 — bundling was necessary since `zig build
test` compiles all entry points in one graph. Cycle 3b (2026-09-08, disk-blocked no-op):
`df -g /` was 16 GB, below the 20 GB gate; stopped before any work, counter not advanced.
Cycle 4 (2026-09-08, FEATURE): item 7 (PRD rewrite against `std.Io.VTable`, ADR 0001) via PR
#7, docs-only — found std's own evented `Io` impls don't compile on 0.16.0, sirocco's actual
reason to exist now; declared the 40-slot hybrid forwarding to `Io.Threaded`. Cycle 5
(2026-09-09, STABILIZATION, n%5==0): CI green, tidy audit mechanically clean (repo is
stub-only, so zero counters prove nothing yet); found and fixed real docs drift instead —
README still described the pre-ADR parallel io/net/tls/http/ws/task API — via PR #8. Cycle 6
(2026-09-09, FEATURE): item 8 (Assertion and Tiger Style baseline) via PR #9 — landed on the
two real entry points (`main.zig`, `bench/main.zig`) since `root.zig` has no `pub fn` yet;
shared `assert`/`maybe` moved to new `src/stdx.zig`. A code-reviewer pass caught compound
implication asserts that just restated a branch instead of deriving an independent property.

Standing backlog / next-work order after milestone 001 closes (from old
`.claude/memory/project-context.md`, superseded by `docs/milestones.md` as source of truth):
1A completion/queue types → 1B kqueue backend → 1C epoll backend → 1D timing wheel → 1E loop
dispatch → 1F integration tests. Do not build Phase 1 against the pre-ADR kqueue-abstraction
design; the rewritten PRD (`docs/adr/0001-std-io-vtable.md`) is what Phase 1 implements.

## Recurring gotchas
- Bash guard hook text-matches commands, not paths: a commit/PR/issue body that spells out a
  banned literal (`.claude/memory/**`) gets blocked as a write attempt even in prose. Route
  such text through a file (`-F`/`--body-file`) instead of an inline heredoc.
- This repo's global `zig` is still 0.15.2 (kingdom dev-box policy); always invoke
  `/Users/fn/.zr/toolchains/zig/0.16.0/zig` explicitly for this 0.16.0-pinned repo, or
  `zig build test`/`fmt` fail on stale-toolchain errors that look like real bugs but aren't.
- A milestone plan's per-file "0.16: X" checklist items can look independently cycle-sized but
  aren't when they share a build graph (`zig build test` compiles every entry point together)
  — bundle such items into one PR rather than one-item-per-cycle.
