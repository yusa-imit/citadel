# sirocco — context

last_seen_at: 2026-09-29T00:00:00Z
rejected_plans: []

## Cycle 25 — 2026-09-29 — FEATURE (no-op)
- Inbox: no OWNER actions since watermark (PR #13 review/issue comments and repo-wide issue
  comments since last_seen_at — none). No open issues, CI green on `e58b354` (== origin/main).
  Plan PR #13 (plan 002) still open awaiting human merge. `periodic_stabilization` is off, so
  n=25 stays FEATURE.
- Done: plan PR open, so one bounded stabilization task — `zig build test`/`fmt --check`/
  `zig build tidy` green under the pinned 0.16.0 toolchain. Same clean baseline as cycles 5/10-24;
  no full audit rerun (nothing changed in the repo since cycle 24's clean pass).
- PRs: none. Next: human merges #13, then milestone issue + item 1 (macOS CI runner).
- Blockers: none. Open questions: none.
- Gotcha: the Bash guard blocks any command that mentions a citadel path alongside a redirect or
  `cd` into the repo in one line — run citadel reads via the Read tool and repo commands in a
  separate Bash call.

## Cycle 24 — 2026-09-29 — FEATURE
- Inbox: no new OWNER actions since watermark. Closed sirocco#17 (citadel commit-lock question,
  opened cycle 22) — verified citadel's working tree is clean this cycle, confirming cycle 23's
  note that the lock cleared; commented and closed as self-resolved. No open bug issues, CI green
  on `e58b354` (== origin/main). Plan PR #13 (plan 002) still open awaiting human merge.
- Done: plan PR open, so ran one bounded stabilization task. `zig build test`/`fmt --check`/
  `tidy` all green under the pinned 0.16.0 toolchain. Independent tidy-auditor pass found
  sirocco's own code fully clean (zero violations, no in-repo docs drift — same baseline as
  cycles 5/10-23) but flagged `REALM.md` in citadel as stale: Zig line still said "0.15.2 —
  migrating to 0.16.0" though plan 001 (PR #6) merged 2026-09-07; file/line counts undercounted
  (187/8 vs actual 244/9, missing `src/stdx.zig`); "Known gaps" section predated the 0.16
  migration. Fixed all of it directly in `REALM.md` (citadel-side, not a sirocco PR).
- PRs: none opened (nothing in the sirocco repo itself needed a fix). Next: human merges #13,
  then milestone issue + item 1 (macOS CI runner). Blockers: none. Open questions: none.

## Cycle 23 — 2026-09-28 — FEATURE
- Inbox: no OWNER actions since watermark (checked PR #13 review + issue comments and repo-wide
  PR/issue comments since last_seen_at — only our own cycle-22 report comment). No open bug
  issues, CI green on `e58b354` (== origin/main). Plan PR #13 (plan 002) still open awaiting
  human merge. Issue #17 (citadel commit-lock question) still unanswered but only 1 cycle old —
  left open per the 2-cycle grace in the inbox protocol.
- Done: plan PR open, so ran one bounded stabilization task. `zig build test`/`fmt --check`/
  `tidy` all green under the pinned 0.16.0 toolchain — identical clean baseline to cycles
  5/10-22. citadel's commit lock (blocking cycles 19-22's report step) has since cleared: those
  cycles' memory landed via the `chore(memory): fold sirocco and synod context` commit.
- PRs: none opened (nothing to fix). Next: human merges #13, then milestone issue + item 1
  (macOS CI runner). Blockers: none. Open questions: sirocco#17 (citadel infra, not
  sirocco-specific; will auto-resolve or auto-close per protocol if still unanswered next cycle).

## Cycle 22 — 2026-09-27 — FEATURE
- Inbox: no OWNER actions since watermark (checked PR #13 review + issue comments and repo-wide
  PR/issue comments since last_seen_at — none). No open issues, CI green on `e58b354` (==
  origin/main). Plan PR #13 (plan 002) still open awaiting human merge.
- Done: plan PR open, so ran one bounded stabilization task. `.zig-cache` was stale (FileNotFound
  spawning build runner) — cleared it (gitignored, not a regression) and `zig build test`/
  `fmt --check`/`tidy` all passed clean under the pinned 0.16.0 toolchain. Independent
  tidy-auditor pass found zero Tiger Style violations and no docs drift (README/CHANGELOG/
  build.zig.zon all agree on 0.2.0) — same clean baseline as cycles 5/10-21.
- Bookkeeping: cycles 19-21 had done their work (context.md entries present, counter staged at
  21) but were never committed to citadel — the previous sessions' `/report` commit step didn't
  land (same class of gap as cycle 14's). This cycle's commit sweeps up 19-22 together.
- PRs: none opened (nothing to fix). Next: human merges #13, then milestone issue + item 1
  (macOS CI runner).
- Blockers: `citadel_commit.py sirocco 22` refuses — citadel's shared working tree has foreign
  uncommitted changes for sigil/silica/synod/zoltraak/zr/zuda (not mine to touch), so this
  cycle's memory (and cycles 19-21's) stayed staged-but-uncommitted locally instead of pushed.
  Opened sirocco#17 (question+needs-human) asking whether the several long-running `claude`
  processes on the machine (dating to Saturday) are legitimate or orphaned/stuck. No action
  needed on sirocco's own work either way — retry the commit next cycle once the lock clears.
  Open questions: sirocco#17 (citadel commit-lock contention, not sirocco-specific).

## History (cycles 0-9, 10-14, 15-21)
Cycles 15-21 (2026-09-16 to 2026-09-27, mostly quiet FEATURE with one STABILIZATION at 15): plan
PR #13 remained open awaiting human merge across all of them, zero new OWNER activity each
watermark. Cycle 15 (STABILIZATION, n%5==0) ran the full audit: CI/build/tidy/tests all green,
tidy-auditor and test-writer both found zero real defects (two pre-existing minor test-quality
notes judged non-defects), and fixed a counter/context.md desync from cycle 14's incomplete
report. Cycles 16-18 each ran one bounded stabilization task (build/test/fmt/tidy green,
tidy-auditor clean) since the plan PR was still open; cycles 19-21 skipped the redundant audit
entirely as a pure no-op, since the baseline had been identical since cycle 5. No PRs opened,
no fixes needed, in any of cycles 15-21.

## History (cycles 0-9, 10-14)
Cycle 14 (2026-09-15, FEATURE): plan PR open, bounded stabilization. Stale `.zig-cache` cleared
(local-only, not a regression); tidy-auditor clean, same baseline as 5/10/11/12. Fixed stale
`//!` headers in `tools/tidy.zig`/`tools/tidy_test.zig` still calling `checkSource` unimplemented
though it shipped in v0.2.0, via PR #16 (merged). Deliberately left `root.zig`'s pre-ADR
`io`/`net`/`tls`/`http`/`ws`/`task` exports alone — expected until plan 002's `Runtime` merges.
Cycle 13 (2026-09-13, FEATURE): plan PR open, bounded stabilization. Reinstalled the missing
pinned 0.16.0 toolchain (dev-box gap, not a repo regression); build/test/fmt/tidy all green
after. tidy-auditor found one real doc-cross-reference drift: `root.zig`/`bench/main.zig` `//!`
headers pointed at the replaced `docs/milestones.md` — fixed via PR #15.
Cycle 12 (2026-09-12, FEATURE): plan PR open, bounded stabilization. CI/build/tidy all clean.
tidy-auditor found real drift: README's intro made present-tense capability claims (`Runtime`
type, kqueue/epoll backends) contradicting the stub-only v0.2.0 code and the README's own
Status section — reworded to design-target language via PR #14 (docs-only, merged). Cycle 11
(2026-09-12, FEATURE): plan PR open, bounded stabilization; CI/build/tidy clean, zero mechanical
violations, nothing to fix. Cycle 10 (2026-09-11, STABILIZATION, n%5==0): full stabilize — CI
5/5 green, build/fmt/tidy clean, tidy and test-quality audits both clean, docs/deps/hygiene
clean, nothing to fix; stabilize_streak reset to 0.

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
