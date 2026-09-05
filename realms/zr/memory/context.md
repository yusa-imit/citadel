# zr — context

## Cycle 0 — 2026-09-05 — RESTRUCTURE

- Realm created by citadel restructure. Memory migrated from the repo's former
  `.claude/memory/` (architecture.md, decisions.md, debugging.md, patterns.md,
  project-context.md's durable facts). The ~20+ dated session-summary/cycle diary files and
  loose TOML-mixin scratch docs under the old `.claude/` were condensed, not migrated whole.
  First plan `001` prescribed by `citadel/docs/ROADMAP.md` (Zig 0.16 migration — blocked on
  zuda and sailor shipping a 0.16-compatible `build.zig` first; see STATE.md probe summary).
- A `wip/advanced-retry-config` branch preserves this session's dirty-tree work: a complete,
  tested feature (bracket/quote-aware `splitTopLevelFields()` inline-table parser, 5 new retry
  fields threaded end-to-end) that a prior session finished but never committed — decide
  finish-or-discard in the first post-restructure cycle rather than losing it silently.
- Standing backlog (carried from the old `project-context.md`, most recent facts first):
  - Version is v1.114.0 (Cycle 451, 2026-09-05); the old memory file's own "Next Action"
    section was stale, still describing v1.89.0-era planning — do not trust the literal text
    of the old file for "what's next", only the facts captured in STATE.md/this file.
  - `docs/milestones.md` had 0 READY milestones queued as of the last survey — establishing a
    new feature milestone is open work (see STATE.md "Next work candidates").
  - Open PR #30 "chore: migrate to zuda for graph algorithms" needs a decision (merge or close
    with reasoning) before other zuda-related work proceeds.
  - Dependency versions at survey time: sailor v2.99.0 (no pending breaking changes), zuda
    `main@4ff2325` / declared `2.0.4` in `build.zig.zon` (behind silica's `2.3.0` pin — a
    kingdom-wide drift `citadel/docs/KINGDOM.md` flags for ROADMAP Phase 0, not zr's to fix
    unilaterally).
  - Repo hygiene backlog (full list in STATE.md): untrack `env_file_test.o`, move 4
    `RELEASE_NOTES_*.md` files and 2 debug shell scripts out of repo root, add a `.gitignore`
    rule for the untracked `zig-pkg/` directory.
- Next: open plan `001` PR (if not open) → await human merge.
- Open questions: none.
