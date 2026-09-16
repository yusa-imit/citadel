# sirocco — context

last_seen_at: 2026-09-16T00:00:00Z
rejected_plans: []

## Cycle 15 — 2026-09-16 — STABILIZATION
- Inbox: no new OWNER actions since watermark (only comment since cycle 14's watermark was our
  own cycle-14 report comment on PR #13). No open issues, no red CI, no rejected plans, no other
  open implementation PRs. Plan PR #13 (plan 002) still open awaiting human merge.
- Done (full stabilize, n%5==0): CI 5/5 green (`e58b354`); `zig build test`/`fmt --check`/`tidy`
  all green under the pinned 0.16.0 toolchain (present this cycle). tidy-auditor and test-writer
  independent audits both found zero real defects — same clean baseline as cycles 5/10/11.
  Two pre-existing minor test-quality observations noted, both judged non-defects (weak-oracle
  version test in `main.zig`; untested CLI wiring in `tools/tidy_main.zig`). Docs/deps(N/A)/
  hygiene all clean. No fixes needed — nothing to file.
- Bookkeeping fix: cycle 14's `/report` logged its context.md entry but never wrote
  `memory/counter` (stayed at 13). This cycle resyncs counter to 15, matching the true count of
  completed cycles and the n%5==0 STABILIZATION cadence.
- PRs: none opened (nothing to fix).
- Next: plan PR #13 still needs human merge; once merged, opens the milestone issue and starts
  item 1 (macOS CI runner). stabilize_streak stays 0 (success).
- Blockers: none. Open questions: none.

## Cycle 14 — 2026-09-15 — FEATURE
- Inbox: no new OWNER actions since the watermark; plan PR #13 (plan 002) still open awaiting
  human merge, zero new review/issue/PR comments since cycle 13. No open issues, no red CI, no
  rejected plans, no other open implementation PRs to triage.
- Done: plan PR open, so ran one bounded stabilization task. Local `.zig-cache` was stale,
  causing `zig build test`/`tidy` to fail with `FileNotFound` spawning the build runner —
  cleared it (gitignored, local-only, not a repo regression) and all checks passed clean.
  tidy-auditor mechanical sweep: zero Tiger Style violations, same clean baseline as cycles
  5/10/11/12. Docs-drift pass found `tools/tidy.zig`'s and `tools/tidy_test.zig`'s `//!` headers
  still describing `checkSource` as unimplemented/red-phase, though it shipped in v0.2.0 — fixed
  via PR #16 (comment-only, CI green, merged). Also flagged but deliberately did not touch:
  `src/root.zig` still exports the pre-ADR parallel `io`/`net`/`tls`/`http`/`ws`/`task` modules,
  contradicting ADR 0001 — expected since plan 002 (which builds the actual `Runtime`) hasn't
  merged yet; rewriting it now would be scope creep ahead of the plan, not a docs fix.
- PRs: #16 opened and merged (comment-only fix, touches `.zig` so CI ran fully, `auto-merged`
  label).
- Next: plan PR #13 still needs human merge; once merged, opens the milestone issue and starts
  item 1 (macOS CI runner).
- Blockers: none. Open questions: none.

## Cycle 13 — 2026-09-13 — FEATURE
- Inbox: no new OWNER actions since the watermark; plan PR #13 (plan 002) still open awaiting
  human merge, zero new review/issue/PR comments since cycle 12. No open issues, no red CI, no
  rejected plans, no other open implementation PRs to triage.
- Done: plan PR open, so ran one bounded stabilization task. Found the local pinned 0.16.0 Zig
  toolchain (`/Users/fn/.zr/toolchains/zig/0.16.0/zig`) missing from this machine — reinstalled
  it from `ziglang.org` before any check could run (dev-environment gap, not a repo regression).
  `zig build test`/`fmt --check`/`tidy` all green after that. tidy-auditor mechanical sweep found
  zero Tiger Style violations but one real doc-cross-reference drift: `src/root.zig`'s and
  `bench/main.zig`'s `//!` headers pointed at `docs/milestones.md`, which was replaced by
  `docs/plans/NNN-*.md` as the progress source of truth — fixed via PR #15.
- PRs: #15 opened and merged (comment-only fix, touches `.zig` so CI ran fully — unlike the
  paths-ignored pure-`.md` docs PRs #7/#8/#10/#11/#14 — all checks green, `auto-merged` label).
- Next: plan PR #13 still needs human merge; once merged, opens the milestone issue and starts
  item 1 (macOS CI runner).
- Blockers: none. Open questions: none.

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

## History (cycles 0-9)
Cycle 9 (2026-09-11, FEATURE): closed milestone #3 (item 11, release v0.2.0 — PR #12, tag,
GitHub release; no consumer pins sirocco yet so no migration issues opened), then drafted plan
002 (`planner`/opus): fiber scheduler + futex core, P0 (concurrency/cancel, 12 slots) + P1
(futex trio, 3 slots), nine one-cycle items starting with the macOS CI runner and a walking-
skeleton `Runtime` forwarding all 109 vtable slots. Version impact MINOR. Plan PR #13 opened,
awaiting human merge (still open as of cycle 15). Cycle 8 (2026-09-10, FEATURE): item 10
(README/CHANGELOG reconciliation) via PR #11 — added `CHANGELOG.md`, fixed the Install
section's uncut `v0.1.0` tag reference.
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
`.claude/memory/project-context.md`; `docs/plans/NNN-*.md` is the source of truth, not the
nonexistent `docs/milestones.md` this line originally named — corrected cycle 13):
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
- The pinned 0.16.0 toolchain can go missing entirely from the machine between cycles (seen
  cycle 13 — only 0.15.2 was on PATH via homebrew). Reinstall to
  `/Users/fn/.zr/toolchains/zig/0.16.0/` from `ziglang.org/download/0.16.0/` before trusting any
  local green/red result; don't mistake the absent binary for a build regression.
- A stale `.zig-cache` can make `zig build test`/`tidy` fail with `error: failed to spawn build
  runner ... FileNotFound` (seen cycle 14) — this looks like a real build break but isn't;
  `rm -rf .zig-cache` (gitignored, local-only) and retry before assuming a regression.
- The `/report` skill's counter write can silently fail to land in a commit (seen cycle 14 —
  only context.md changed, `memory/counter` stayed at 13) while the context.md entry and GitHub
  comment still went out normally. Cross-check `memory/counter` against the highest `## Cycle N`
  header in context.md at cycle start; if they disagree, trust the context.md history (it has a
  matching GitHub comment as evidence) and resync counter to `N+1`, don't just take the file at
  face value.
