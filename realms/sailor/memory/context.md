# sailor — context

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
