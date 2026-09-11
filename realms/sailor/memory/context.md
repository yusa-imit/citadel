# sailor — context

last_seen_at: 2026-09-11T00:00:00Z
rejected_plans: []

## Cycle 8 — 2026-09-11 — FEATURE

- Done: inbox found no open PRs and no bug/question/directive issues with new OWNER activity
  since the watermark — nothing to merge or triage. Milestone #19's item 4 remainder still had
  no 0.15.2-compatible spelling (per cycle 7), so instead checked item 5 (`ArrayList` literal
  sweep) the same way cycle 6 found item 4's "safe half": read 0.15.2 and 0.16.0's
  `array_list.zig` directly and confirmed `.empty` is already a static value in 0.15.2 — only
  the struct's default field values are dropped in 0.16.0, turning bare `.{}` into a
  missing-field error there. Mechanically replaced all 132 `ArrayList`/`ArrayListUnmanaged`
  `= .{}` sites across 34 files (`src/`, `tests/`, `examples/`) with `= .empty` as PR #28.
  Verified via `git diff --stat` (132/132, no incidental changes) and `git stash` (the 83
  pre-existing `zig fmt --check` failures unchanged). `zig build test` green, tidy clean. All 10
  CI checks green, squash-merged, branch deleted, `auto-merged`. Confirmed post-merge CI on
  `main` @ `df0c427` reached `success`. Ticked item 5 on #19; see [[patterns]] for the reusable
  "check for a 0.15.2-compatible spelling before assuming toolchain-blocked" pattern.
- PRs: #28 (merged).
- Next: item 4's remainder (`Io.Mutex`, env access, `posix.isatty`, `mem.indexOf*`→`find*`, ~500
  sites) is still practically blocked on pairing the toolchain switch with the `std.Io` rewrite
  (items 6-7) — multi-cycle work. No other item on #19 has been checked yet for a similar
  0.15.2-compatible-spelling escape hatch; worth a quick check each cycle before assuming block.
- Blockers: item 4/6/7's full scope needs a dedicated multi-cycle session, not a formal
  `blocked_by` tag.
- Open questions: none.

## Cycle 7 — 2026-09-10 — FEATURE

- Done: inbox merged PR #26 (forward-compat Zig 0.16 renames: `linkLibC` + `GeneralPurposeAllocator`
  →`DebugAllocator`), confirmed CI green on `main` @ `38252aa` post-merge. Picked item 4 on #19
  next but its remaining scope (`Io.Mutex` 6, env access 14, `posix.isatty` 4, `mem.indexOf*`
  →`find*` ~478 — confirmed by reading 0.16.0's `mem.zig` directly: `indexOf`/`lastIndexOf` etc.
  have **no** alias or deprecated wrapper, fully removed) has zero 0.15.2-compatible spelling and
  can't be verified without switching the pinned toolchain to 0.16.0 — which would still leave
  `zig build`/`zig test` broken repo-wide on the separate, unstarted `std.Io` rewrite (155 sites,
  its own checklist items). Landing ~500 unverifiable renames blind was judged unsafe; did not
  attempt it. Fell back to CYCLE.md's "every remaining item practically blocked → one bounded
  stabilize task" clause: proof-commented the 3 test-only `catch unreachable` sites in
  `eventbus.zig` (single-element `std.testing.allocator` appends in a priority-ordering test
  callback — provably safe) as PR #27; all 10 CI checks green pre-merge, squash-merged,
  `tidy_baseline.txt` shrunk 448→447. Deliberately did **not** proof-comment
  `event_metrics.zig`/`render_metrics.zig`'s 4 sites (caller-supplied general `Allocator`, genuine
  OOM possibility — a proof comment there would be a false claim; needs an actual typed-error
  return, a separate fix) nor `countdown_timer.zig`'s 3 (provably safe but 2 lines already exceed
  100 cols, need reformatting to keep the proof comment on the same line as `catch unreachable`).
  Updated `STATE.md`'s Tiger Style table with these findings.
- PRs: #26 (merged), #27 (merged).
- Next: item 4 on #19 needs a dedicated larger session (not a normal 22-min cycle) that pairs the
  toolchain switch with enough of the `std.Io` rewrite to reach a compiling `zig build` — until
  then it will keep being practically blocked. In the meantime, smaller STATE.md-tracked
  stabilization slices remain available: `countdown_timer.zig` reformat + proof-comment (3 sites),
  `//!` headers on the 86 missing files (purely additive).
- Blockers: item 4's full scope is practically blocked on a multi-cycle toolchain migration, not
  a formal `blocked_by` tag — STATE.md's Zig 0.16 probe summary has the error-class breakdown.
- Open questions: none.

## Cycle 6 — 2026-09-10 — FEATURE

- Done: inbox merged PR #25 (`crypto_random` tidy tracking) — CI on `main` @ `07c8a97` confirmed
  `success` before treating main as green. Picked item 4 on #19 (`build.zig` fix + mechanical
  renames). Read both 0.15.2 and 0.16.0 stdlib sources directly and found the item's own six
  renames split cleanly: `GeneralPurposeAllocator`→`DebugAllocator` and `linkLibC()`→
  `.link_libc = true` are pure aliases in 0.15.2 (safe to land now, no toolchain switch needed);
  `Io.Mutex`, env access, `posix.isatty`, and `mem.indexOf*`→`find*` (478 sites) have no
  0.15.2-compatible spelling and need the actual toolchain switch. Landed the safe half:
  `linkLibC` fix (1 site) + GPA rename repo-wide (44 sites across `src/`, `tests/`, `examples/`,
  `benchmarks/`, `scripts/`) as PR #26. Verified via `git stash` that the 8 pre-existing `zig fmt`
  failures and 10 pre-existing example-build failures (e.g. `examples/hello.zig:39` calling
  `layout.split` with a stale arg count) are unchanged by the diff. `zig build test` green,
  `code-reviewer` clean. CI still running at cycle deadline (~8 min budget left after the
  implementation work) — left PR #26 open for next cycle's inbox, same pattern as #21/#25.
  Checklist item 4 left unticked: the item's own `Verify` line requires the build to compile
  *on 0.16.0*, which this slice doesn't reach alone.
- PRs: #25 (merged), #26 (open, CI pending).
- Next: inbox should merge #26 once green (does not tick item 4 — that needs a follow-up cycle
  to do the toolchain-dependent renames: `Io.Mutex` (6), env access (14), `posix.isatty` (4),
  `mem.indexOf*`→`find*` (478, use the mapping table in `zig-0.16.md`, not a blind regex) —
  likely paired with actually bumping `minimum_zig_version` to `0.16.0` in the same PR, since
  none of those four compile under 0.15.2 in isolation).
- Blockers: none.
- Open questions: none.

## Cycle 5 — 2026-09-09 — STABILIZATION

- Done: preflight/inbox found PR #24 (`@panic` tidy tracking) already open and fully green
  (10/10 checks, `mergeStateStatus: CLEAN`) from an interrupted prior session — not recorded in
  cycle 4's memory, so this cycle's inbox merged it (squash, branch deleted, labelled
  `auto-merged`) and confirmed the post-merge CI run on `main` @ `2989cb4` reached `success`
  before treating main as green. Ran `tidy-auditor` for a fresh count (see STATE.md): baseline
  regeneration diffed byte-for-byte clean against the checked-in file (no drift). Auditor's
  smallest-diff recommendation was a new `crypto_random` tidy check mirroring `time_usage` (one
  real site, `llm_client.zig`'s `RateLimiter` jitter) — implemented with a TDD test first,
  confirmed the check failed against the unmodified baseline (proving it catches the site),
  regenerated the baseline (+1 entry, 448 total), `zig build test` green, `zig fmt --check`
  clean. Opened as PR #25; CI was still running at cycle deadline (~15 min in) — left open for
  next cycle's inbox to merge, same pattern as cycle 2's PR #21.
- PRs: #24 (merged), #25 (open, CI pending).
- Next: inbox should merge #25 once green, then STATE.md's next smallest-diff pick is
  proof-commenting the 3 remaining unproven `catch_unreachable` clusters (`eventbus.zig`,
  `countdown_timer.zig`, `event_metrics.zig`/`render_metrics.zig`) — same mechanical pattern as
  the `@panic` PR. FEATURE-mode work remains item 4 on #19 (`build.zig` `linkLibC` fix +
  mechanical Zig 0.16 renames).
- Blockers: none.
- Open questions: none.

## Cycle 4 — 2026-09-08 — STABILIZATION

- Done: preflight found CI red on `main` (`headSha` f2a1ba0, the flaky `avg_ns` perf assertion
  in `type_aggregation accuracy` test) with no `escalated_sha` recorded — forced STABILIZATION.
  Cycle 3 had already prepared the fix as open PR #23 (all 10 checks green, `mergeStateStatus:
  CLEAN`); merged it (squash, branch deleted), watched the new CI run on `main` @ `fabab3c`
  through to `success`. Inbox: no new owner actions, no plan PR, milestone issue #19 unchanged
  (3/12 checked). Re-ran `tidy-auditor` for a fresh Tiger Style count (see STATE.md): `zig build
  tidy` now passes cleanly (447 baseline entries); `@panic` (8, 2 files) is the smallest
  untracked category and the recommended next stabilization target. Did not open a new fix PR
  this cycle — only ~14 min remained after the CI-green wait, not enough to safely land a TDD
  fix plus another CI round-trip within the deadline.
- PRs: #23 (merged).
- Next: item 4 on #19 (`build.zig` `linkLibC` fix + mechanical Zig 0.16 renames) is next
  FEATURE-mode work; alternatively a STABILIZATION cycle could take the `@panic` cleanup
  (`src/stack_trace.zig:30` + 7 test-only guards in `src/clipboard.zig`) as a quick single-class
  fix.
- Blockers: none.
- Open questions: none.

## Cycle 3 — 2026-09-07 — FEATURE

- Done: inbox found PR #21 (item 2, tidy step) red on Windows CI only — root-caused to a CRLF
  bug in `countLongLines` (git checks out `\r\n` on Windows, inflating byte-counted line lengths
  past the LF-computed baseline). Wrote a regression test, fixed with `trimRight(..., "\r")`,
  CI went green on all 10 checks, merged. Then picked item 3: rebased
  `wip/timeline-description-rendering` onto main as PR #22 (dropped a stray pre-restructure
  `.claude/logs/` file that conflicted with the delete already on main; also ran `zig fmt` on
  `timeline.zig`'s pre-existing comment-alignment drift while touching the file), CI green,
  merged. Both ticked on issue #19. See [[debugging]] for the CRLF finding (durable pattern for
  any future line-oriented text check).
- PRs: #21 (merged), #22 (merged).
- Next: item 4 — `build.zig` fix (`linkLibC` rename) + mechanical Zig 0.16 renames
  (GPA→DebugAllocator, `ArrayList{}`→`.empty`, `mem.indexOf*`→`find*`).
- Blockers: none.
- Open questions: none.

## Cycle 2 — 2026-09-06 — FEATURE

- Done: implemented plan 001 item 2 (`tidy` build step). Pure checker (line length, function
  length w/ shrinking baseline, missing `//!` header, unproven `catch unreachable`,
  `std.debug.print`/`std.time.*` usage, `usize` in known wire-format files) in
  `build_support/tidy.zig` with 30 TDD unit tests; CLI/walker in `build_support/tidy_main.zig`;
  wired into `zig build test` via new `tidy` step. Generated `tidy_baseline.txt` (447 entries)
  from real `src/`+`build.zig` so `zig build tidy` is green today; only new debt or growth fails.
  Fixed one off-by-one bug in a test-writer-authored test (`findFunctions` "two functions" case
  expected 4 lines for a 5-line function) before committing.
- PRs: #21 (open, CI still running at cycle deadline — comment left asking next cycle's inbox
  to merge when green).
- Next: inbox should merge #21 once CI is green, tick item 2 on issue #19, then pick item 3
  (`wip/timeline-description-rendering` decision) or item 4 (`build.zig` fix + mechanical
  renames) as the next unblocked item.
- Blockers: none.
- Open questions: none.

## History (cycles 0-1, condensed 2026-09-11)

Cycle 0 (RESTRUCTURE, 2026-09-05): realm created; memory migrated from the repo's former
`.claude/memory/`; plan `001` prescribed (Zig 0.16 migration, MAJOR → v3.0.0, 368 probe errors +
`linkLibC`). `wip/timeline-description-rendering` preserved mid-cycle TDD work (finished as PR
#22 in cycle 3). Standing backlog carried forward, still partly open: the v2.100.0
"Widget Doc-Comment Audit Round 3" milestone has `terminal.zig` (`AnsiParseState` wiring),
`pager.zig` (soft-wrap), `metrics_dashboard.zig`/`richtext.zig` (scope decisions), and
`paragraph.zig` (word/char wrap + RTL/bidi, architect pass, do last) still unaddressed —
separate from plan `001`/milestone #19, not yet resumed. Repo hygiene backlog (stale
`README.md`/`docs/PRD.md`, 52 files >800 lines) also still open, tracked in STATE.md.

Cycle 1 (FEATURE, 2026-09-05): plan `001` merged as #18; opened tracking issue #19 (12-item
checklist). Implemented item 1 (hygiene leftovers) as PR #20, merged.
