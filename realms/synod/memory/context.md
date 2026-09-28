# synod — context

last_seen_at: 2026-09-28T00:00:00Z
rejected_plans: []

## Cycle 18 — 2026-09-28 — FEATURE
- Inbox: no new OWNER actions since watermark (only the AI's own cycle-16/17 report comments
  on issues #20/plan history). No plan PR, no plan_closed_unmerged, no bug/directive/question
  issues, CI green (matches origin/main).
- Item 5 (1A-ii `types.zig` — `Message` union and `ConfChange`) via PR #23: `architect` (opus)
  designed the wire shape first — `Header` (protocol_version/term/from/to) fronts every
  `Message` payload; PreVote gets its own tag rather than a `pre_vote: bool` (a forgotten bool
  compiles, a forgotten switch arm does not); `AppendResponse` carries a Raft-thesis-§5.3
  conflict hint for fast backtrack; `Configuration`/`ConfChange` are joint-consensus-only,
  absolute (not delta). Recorded as ADR-005. Wrote tests and implementation directly (budget
  after the architect call was tight — same pattern as cycle 17): ~30 new tests (exhaustive
  switch, one negative test per named error, borrow-identity, a seeded model test for
  `Configuration.validate`).
- `code-reviewer` (sonnet) caught 1 CRITICAL before merge: `validateAppendRequest`'s
  contiguity loop called `Index.next()` on an unranged peer-supplied index — panics the
  process at `maxInt(u64)` per `Index.next`'s own documented precondition, a peer-triggerable
  crash in a foundation library. Fixed with a range guard + regression test. Also fixed 2
  WARNINGs: entry-term ordering skipped comparing the first entry against `prev_log_term`
  (seeded `previous_term` wrong); `validateSnapshotRequest` collapsed a bad `Configuration`'s
  specific `ConfError` into a generic `MessageSnapshotInvalid` instead of propagating it.
  `zig build test`/`tidy`/`fmt --check` all green after fixes. CHANGELOG updated, plan 002
  item 1A-ii ticked.
- Budget ran very tight this cycle (architect call alone was ~$0.85 of $4; a third
  consecutive cycle where a wire-format architect call dominates the budget — see cycle 12/17
  notes). PR #23 pushed but **not watched to green or merged this cycle** — commented
  "awaiting CI; merge next cycle" per protocol; next cycle's `/inbox` should merge it if CI is
  green and no `hold` label. **Recommendation for future cycles**: when synod's remaining
  budget after an architect call drops below ~$1, skip the `gh pr checks --watch` step
  entirely (as done here) rather than trimming test/review depth — correctness work (which
  caught a real peer-triggerable panic this cycle) is worth more than a same-cycle merge.
- Next: cycle 19's inbox merges PR #23 if green, then continues with item 6 (1B-i `log.zig` —
  `Log` with append/truncate/termAt/lastIndex).
- Open questions: none.

## Cycle 17 — 2026-09-27 — FEATURE
- Inbox: no new OWNER actions since watermark (only the AI's own cycle-16 report comment on
  issue #20). No plan PR, no plan_closed_unmerged, no bug/directive/question issues, CI green.
- Item 4 (1A-i `types.zig` — scalars, `Entry`, `HardState`, `Snapshot`) via PR #22: `architect`
  (opus) designed the wire shape first (interface/wire-format change per the implement skill) —
  `NodeId`/`Term`/`Index` as distinct non-exhaustive `enum(u64)` types (never `usize`, each with
  a named zero sentinel: `NodeId.none`, `Term.zero`, `Index.zero`), `EntryKind`/`Entry`,
  `HardState` (24-byte `extern struct`, no padding, `eql()`, `validateTransition()` returning
  `error.Invariant*` per REALM.md), `Snapshot`. Recorded as ADR-004
  (`docs/adr/0004-distinct-scalar-types.md`). Also fixed a tidy gap the architect found:
  `findWireDeclEnd` only matched bare `struct`/`union`, so `HardState`'s `extern struct` would
  have silently skipped the wire-`usize` check — widened to recognize `extern`/`packed`
  qualifiers, with 2 new tidy tests. Wrote tests and implementation directly (budget-conscious:
  skipped separate test-writer/zig-developer/code-reviewer subagent delegation this cycle after
  the architect call — see budget note below) — TDD still followed (tests against the
  not-yet-existing API written first, confirmed red via compile failure, then implemented green).
  ~30 new tests (fixed cases, boundaries, seeded model tests against `std.math.order` and a
  field-wise/predicate reference). `zig build test` 100/100 passing, `zig build tidy` clean,
  `zig fmt --check` clean. All 7 CI jobs green, squash-merged, branch deleted. Ticked item 4 in
  the plan doc and issue #20.
- Budget note: the single `architect` agent call for this item's design consumed roughly $1.20
  of the session's $4 budget (72K subagent tokens) — the second cycle in a row this has happened
  (see cycle 12's note). Future cycles needing `architect` for a wire-format decision should keep
  the prompt pointed at specific files/sections to read rather than asking for a from-scratch
  survey, and consider whether the plan item's own bullet (often already detailed, as here) is
  specific enough to skip the architect call entirely for smaller follow-on items like 1A-ii.
- Next: item 5 (1A-ii `types.zig` — `Message` union and `ConfChange`, with `protocol_version`
  on every variant per REALM.md).
- Open questions: none.

## Cycle 16 — 2026-09-27 — FEATURE
- Inbox: plan 002 (PR #16) was merged by the OWNER; no issues, CI green (main head cd8cada is a
  docs-only merge, CI paths-ignore, not red).
- Opened milestone issue #20; ticked plan items 2 and 3 (already landed as #17-#19).
- Item 1 via PR #21: `synod.version` derived from `build.zig.zon` (`b.addOptions` →
  `build_options` → comptime `SemanticVersion.parse`); fixes v0.2.0 reporting 0.1.0. 7/7 CI
  green, 75/75 tests, merged, labeled `auto-merged`.
- Note: the guard hook blocked a Bash command that redirected to a citadel path; use the
  Write/Edit tools for citadel memory files.
- Next: item 4, `types.zig` 1A-i (scalars, Entry, HardState, Snapshot).
- Open questions: none.

## Cycle 15 — 2026-09-17 — FEATURE
- Inbox: no new owner actions since watermark — only the AI's own cycle-14 report comment on
  plan PR #16. No plan_closed_unmerged, no milestone issue, no bug/directive/question issues,
  CI green (matches origin/main).
- Plan PR #16 (plan 002) still open awaiting OWNER merge → ran one bounded stabilization task:
  widened `zig build tidy`'s size checks (line-length, function-length, missing-`//!` header) to
  `tools/*.zig` and `build.zig` via a new `checkFileSizeOnly`, replacing the build.zig-only
  `checkBuildZigHeader`. Deliberately did NOT widen the ban-list checks to `tools/`: grepped and
  confirmed `tools/tidy.zig`'s own source contains `"catch unreachable"`, `"std.debug.print"`,
  `"std.time."` as string literals implementing those checks, and `tools/tidy_test.zig` has
  matching fixture strings to test them — the naive substring scan would false-positive on its
  own code. TDD (test-writer: 7 failing tests confirmed red; zig-developer: green); code-reviewer
  found 0 CRITICAL / 2 WARNING (missing postcondition assertion; `files_seen` tripwire didn't
  count the `build.zig` check) / 4 SUGGESTION — both WARNINGs fixed before merge. PR #19: 7/7 CI
  jobs green, squash-merged, branch deleted, labeled `auto-merged`. `zig build test` 74/74
  passing, `zig build tidy` clean (including on `tools/tidy.zig`/`tools/tidy_test.zig`
  themselves), `zig fmt --check` clean.
- Updated `STATE.md`: recorded step 3's size dimension as done, with the ban-list-exclusion
  rationale for future cycles; 4 SUGGESTION-level cosmetic follow-ups (dedupe shared logic
  between `checkFile`/`checkFileSizeOnly`, explicit error set) left for a future cycle.
- Next: awaiting OWNER merge of plan 002 (PR #16). Once merged, opens the milestone issue and
  starts item 1 (fix `src/root.zig`'s hardcoded `SemanticVersion{0,1,0}`).
- Open questions: none.

## Cycle 14 — 2026-09-16 — FEATURE
- Inbox: no new owner actions since watermark — the only comment on plan PR #16 since cycle 13
  was the AI's own cycle-13 report (posted under the authenticated OWNER account, not a real
  instruction). No plan_closed_unmerged, no milestone issue, no bug issues, CI green (matches
  origin/main).
- Plan PR #16 (plan 002) still open awaiting OWNER merge → ran one bounded stabilization task
  per protocol instead of idling: step 1 of the `tools/tidy.zig` size-violation fix order
  recorded in `STATE.md` since cycle 5 — split the file's ~550 lines of inline tests into
  `tools/tidy_test.zig` (pulled into `zig build test` via `test { _ = @import("tidy_test.zig");
  }`, no build.zig change needed). `tools/tidy.zig` dropped from 1266 to 676 lines, clearing the
  800-line violation. No behavior change: same 50 tidy tests, same public checker API. PR #18:
  all 7 CI jobs green, squash-merged, branch deleted, labeled `auto-merged`.
- Updated `STATE.md`: recorded this fix; step 3 (widening `tidy`'s own walk to cover
  `tools/`/`build.zig`) remains deferred but is now safe to attempt on its own since tidy.zig is
  under the floor already.
- Next: awaiting OWNER merge of plan 002 (PR #16). Once merged, opens the milestone issue and
  starts item 1 (fix `src/root.zig`'s hardcoded `SemanticVersion{0,1,0}`).
- Open questions: none.

## Cycle 13 — 2026-09-16 — FEATURE
- Inbox: no new owner actions since watermark. Plan PR #16 (plan 002) still open awaiting OWNER
  merge, no comments/reviews on it yet. No plan_closed_unmerged, no open milestone issue, no
  bug issues, CI green (matches origin/main).
- Plan PR open → per CYCLE.md, ran one bounded stabilization task instead of idling: split
  `build.zig`'s 87-line `build()` into 7 single-purpose helpers (`addLibraryModule`,
  `addCliExecutable`, `addRunStep`, `addTestStep`, `addTidyStep`, `addBenchStep`, `addDocsStep`);
  `build()` is now 23 lines. No behavior change (same artifacts/steps/wiring). Clears the
  function-length violation flagged in `STATE.md` since cycle 10 (2026-09-12). PR #17: all 7 CI
  jobs green, squash-merged, branch deleted, labeled `auto-merged`.
- Updated `STATE.md`: recorded this fix; `tools/tidy.zig` (1266 lines) split and widening its
  walk to cover itself/`build.zig` remain deferred (steps 1 and 3 of the recorded order) — doing
  step 3 before step 1 would turn `zig build tidy` red immediately.
- Next: awaiting OWNER merge of plan 002 (PR #16). Once merged, opens the milestone issue and
  starts item 1 (fix `src/root.zig`'s hardcoded `SemanticVersion{0,1,0}` — a real version-drift
  bug the planner caught last cycle, made plan 002's first item).
- Open questions: none.

## History (cycles 0-12)
Cycle 12 (2026-09-16, FEATURE): item 11 (release v0.2.0, milestone 001's last item) via PR #15
— tagged, released, milestone #3 closed (no consumers pinned synod yet, so no migration issues).
Opened plan 002 (PR #16, Phase 1: types/interfaces/log/store) via `planner`; caught a live bug
— `src/root.zig:11` hardcoded `SemanticVersion{0,1,0}`, so v0.2.0 still reported `0.1.0` —
made it plan 002 item 1. Budget note: the full-context `planner` call consumed most of the
session's budget; keep future planner prompts pointed at files rather than pasted excerpts.
Cycle 11 (2026-09-15, FEATURE): item 10 (README/PRD/CHANGELOG reconciliation) via PR #14 —
docs-only: Zig badge bump, module table gained a `Status` column (all `planned`), install
snippet pointed at unreleased `v0.2.0`. `CHANGELOG.md` entry added under `[Unreleased]` per
`VERSIONING.md` (versioned section lands with the release PR, not before). code-reviewer caught
2 line-length WARNINGs, both fixed before merge.
Cycle 10 (2026-09-12, STABILIZATION): found and fixed a bookkeeping bug — cycle 9's `/report`
never wrote `memory/counter` (stayed at 8); resynced to 10. tidy-auditor fixed two
`assert(a or b)` implication-style asserts (`bench/main.zig:48`, `tools/tidy.zig:605`) via PR
#13. Deferred `build.zig`'s `build()` (87 lines) and `tools/tidy.zig` (1266 lines) size
violations, both unenforced since `tidy.zig`'s walk only covers `src/`; fix order recorded in
`STATE.md`. Corrected stale "no CHANGELOG.md yet" claims in `REALM.md`/`STATE.md`.
- Cycle 0 (2026-09-05, RESTRUCTURE): realm created by citadel restructure; plan 001 (Zig 0.16
  migration + Tiger Style baseline) prescribed by ROADMAP.
- Cycle 1 (2026-09-06, FEATURE): plan 001 merged as #2; opened milestone tracking issue #3
  (11-item checklist). Item 1 (hygiene leftovers) via PR #4.
- Cycle 2 (2026-09-06, FEATURE): item 2 (`tidy` step part 1, sizes) via PR #5.
- Cycle 3 (2026-09-07, FEATURE): item 3 (`tidy` step part 2, ban list) via PR #6; code-reviewer
  caught `tools/tidy.zig`'s own tests weren't wired into `zig build test` and a real off-by-one
  bug it then surfaced — both fixed.
- Cycle 4 attempt (2026-09-08, PREFLIGHT ABORT): disk gate failed (16 GB < 20 GB); in-progress
  item-4 work committed to `wip/fix-0.16-main-entry-20260908` before stopping.
- Cycle 4 (2026-09-08, FEATURE): cherry-picked the preserved wip branch; merged #7 (0.16
  migration of `src/main.zig` and `tools/tidy.zig`, `minimum_zig_version` bump). Ticked items 4
  and 7.
- Cycle 5 (2026-09-09, STABILIZATION): tidy-auditor found one fix (compound assert →
  `if (a) assert(b);` idiom), merged as #8. Confirmed `zig build bench` still broken under 0.16.
- Cycle 6 (2026-09-10, FEATURE): item 5 (0.16 — `bench/main.zig`) via PR #9: `Io.Clock`-based
  timing, `init.gpa`, `matchesFilter` replacing `std.mem.indexOf`; also closed a CI gap (bench
  executable was never built by CI). Forgot the `Co-Authored-By` trailer on PR #9's commit — a
  force-push to fix it is blocked by the guard hook, so left as-is; include the trailer in the
  *first* commit going forward (done correctly again since cycle 8).
- Cycle 7 (2026-09-11, FEATURE): item 6 (0.16 — library-core sweep) via PR #10: confirmation
  task, zero hits found for every remaining 0.15-only pattern in `src/`.
- Cycle 8 (2026-09-11, FEATURE): item 8 (`io: Io` at the boundary only) via PR #11:
  `docs/adr/0002-io-at-the-boundary.md` + `tools/tidy.zig`'s `core_purity_files` check. Also
  fixed a tracking-drift bug — item 6 was ticked in the plan doc but not in issue #3's checklist.
- Cycle 9 (2026-09-12, FEATURE): item 9 (assertion baseline) via PR #12: docs-only,
  `docs/adr/0003-assertion-baseline.md`; `main.zig`/`bench/main.zig` already met the contract.
- Standing backlog (from the old `.claude/memory/project-context.md`): after milestone #3 closes
  (item 11, release v0.2.0), Phase 1 real work starts at `src/types.zig` (NodeId/Term/Index/
  Entry/HardState/Snapshot/Message/ConfChange), then `src/log.zig` (append/truncate/termAt/
  conflict search), then `src/interfaces.zig` + `src/store.zig` (vtables + in-memory LogStore),
  then Phase 2's `raft/node.zig` election state machine.

Full per-cycle detail for cycles 0-9 (PR numbers, code-reviewer findings, the disk-gate abort)
lived here before this fold; see git history of this file if needed.
