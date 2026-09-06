# sailor — context

last_seen_at: 2026-09-07T00:00:00Z
rejected_plans: []

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

## Cycle 1 — 2026-09-05 — FEATURE

- Done: plan `001` (Zig 0.16 migration + Tiger Style baseline) was already merged (#18) when
  this cycle started; opened tracking issue #19 with its 12-item checklist. Implemented item 1
  (hygiene leftovers): dropped the dead memory-dir entry from `ci.yml` `paths-ignore`, fixed 3
  dangling doc links (a removed root config doc, a `memory-profiling.md` that never existed, a
  mistyped `benchmark_runner.zig`). PR #20, CI green on all 3 native runners + 6 cross-compile +
  benchmarks, squash-merged, labelled `auto-merged`, checklist item 1 ticked on #19.
- PRs: #20 (merged).
- Next: item 2 — `tidy` step in `build.zig` (line/function-length limits, ban list, `//!`
  header check), wired into `zig build test`.
- Blockers: none. `wip/timeline-description-rendering` still undecided — plan item 3, not yet
  reached.
- Open questions: none.

## Cycle 0 — 2026-09-05 — RESTRUCTURE

- Realm created by citadel restructure. Memory migrated from the repo's former
  `.claude/memory/` (architecture.md, decisions.md, debugging.md, patterns.md,
  zig-015-compat.md, project-context.md's durable facts). Stale one-off snapshots
  (session-48.md, session-94.md) and a stray scratchpad.zig.md were dropped, not migrated.
  First plan `001` prescribed by `citadel/docs/ROADMAP.md` (Zig 0.16 migration, MAJOR → v3.0.0,
  368 probe errors + `linkLibC`).
- A `wip/timeline-description-rendering` branch preserves session 444's mid-cycle TDD work
  (`timeline.zig` renders `TimelineEvent.description`; `zig build test` was green on the dirty
  tree including 8 new tests) — decide finish-or-discard in the first post-restructure cycle.
- Standing backlog (carried from the old `project-context.md`, most recent sessions first):
  - v2.100.0 "Widget Doc-Comment Audit Round 3" milestone, in progress. Fixed so far:
    hex_editor.zig (`modified_style`), filebrowser.zig (preview pane), configeditor.zig
    (scalar editing + test-reachability fix), toggle_switch.zig (label rendering),
    pipeline.zig (progress %), timeline.zig (description — see wip branch above, uncommitted).
  - Remaining in that milestone: terminal.zig (wire existing `AnsiParseState` into `addLine()`),
    pager.zig (real soft-wrap using the existing `wrap` setting), metrics_dashboard.zig
    (`show_graphs` sparklines — needs a scope decision: implement or drop the doc claim),
    richtext.zig (emoji search — same scope-decision shape), paragraph.zig (true word/char
    wrap + RTL/bidi — largest item, flagged for an `architect` pass, do last). Then
    re-regenerate the unswept-widget list and bundle release v2.100.0.
  - 6 unreleased commits sat on `main` as of session 444, above the project's own
    "4-5 commits, worth reconsidering" bundling threshold — every actual release in this
    project's history has gated on milestone completion, not commit count alone; a future
    cycle should make an explicit call on bundling partway vs. finishing all remaining gaps.
  - Repo hygiene (STATE.md has the full list): `git rm --cached` the tracked test binaries,
    move/drop `AUDIT_DOC_COMMENTS.md`, fix `.gitignore` (bare `test`, `verify_*`, `*.log`),
    refresh stale `README.md`/`docs/PRD.md` version claims, split files over 800 lines.
- Next: open plan `001` PR (if not open) → await human merge.
- Open questions: none.
