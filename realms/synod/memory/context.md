# synod — context

last_seen_at: 2026-09-07T00:00:00Z
rejected_plans: []

## Cycle 3 — 2026-09-07 — FEATURE
- Inbox: merged PR #5 (item 2, tidy sizes) — CI was green; ticked item 2 in #3.
- Implemented item 3 (`tidy` step, part 2 — ban list): `tools/tidy.zig` gained
  `checkCatchUnreachable` (no `catch unreachable` without `// proof:` same/previous line),
  `checkBannedPattern` (`std.debug.print`, `std.time.*` in `src/`), `checkWireUsize` (no
  `usize` field inside `Message`/`Entry`/`HardState`/`Snapshot`), `hasModuleHeader` (every
  `.zig` file needs `//!`); added missing headers to `build.zig`/`src/main.zig`. TDD: 25 tests.
  Opened PR #6, merged after CI green on all 7 jobs.
- A code-reviewer pass (before merge) caught two real bugs a first "all green" pass missed:
  `zig build test` never actually ran `tools/tidy.zig`'s own `test` blocks — only `main()`'s
  repo scan was wired into the build graph, so the file's 42 tests were silently dead weight.
  Fixed by adding `b.addTest(.{.root_module = tidy_exe.root_module})` + `dependOn` from
  `test_step` (see `patterns.md`). That then surfaced a genuine off-by-one in
  `checkWireUsize`'s reported line number, plus 4 lines over 100 cols the tool wasn't checking
  against itself (tidy only walks `src/`, self-exempting `tools/`). Lesson: don't trust
  "zig build test is green" for a new executable target without confirming its own tests are
  actually wired into a `b.addTest`, not just `addRunArtifact` of the binary's `main()`.
- Next: item 4, 0.16 migration starting at `src/main.zig` (trivial — see `STATE.md`).
- Open questions: none.

## Cycle 2 — 2026-09-06 — FEATURE
- Inbox: no new owner actions since the watermark; milestone #3 open, item 1 done.
- Implemented item 2 (`tidy` step, part 1 — sizes): `tools/tidy.zig` (line length ≤ 100 cols,
  function length ≤ 70 lines / 72 red-zone via `tools/tidy_baseline.txt`, empty today), wired
  as a `zig build tidy` step that `zig build test` now depends on. Also wrapped the 5
  pre-existing overlong doc-comment lines (`build.zig`, `src/{main,raft,root,sim}.zig`) so
  tidy passes clean. TDD: 25 tests red (stub `@panic`) → green. Opened PR #5.
- Ran out of the 22-minute cycle budget before CI finished (test-writer + zig-developer
  subagent turns took ~16 min combined); skipped a dedicated code-reviewer pass this cycle to
  stay inside budget — PR #5 is unreviewed by a fresh pair of eyes, left for next cycle's inbox
  to merge once CI is green (or to review first if that feels warranted).
- Next: next cycle's inbox merges PR #5 if CI green, ticks item 2 in #3; then item 3, `tidy`
  step part 2 (ban list).
- Open questions: none.

## Cycle 1 — 2026-09-06 — FEATURE
- Plan 001 (merged as #2) approved by merge; opened milestone tracking issue #3 with its
  11-item checklist. Implemented item 1 (hygiene leftovers from the restructure PR) via PR #4:
  dropped the stale `.claude/memory/**` CI path-ignore, fixed `root.zig`/`bench/main.zig` doc
  references to `docs/plans/000-inherited.md`, added `docs/adr/0001-zero-dependency-core.md`
  and `CHANGELOG.md`. CI green on all 7 jobs; squash-merged, branch deleted.
- Next: item 2, `tidy` step part 1 (sizes) — `tools/tidy.zig` + `zig build tidy` gating
  `zig build test`, per plan 001.
- Open questions: none.

## Cycle 0 — 2026-09-05 — RESTRUCTURE
- Realm created by citadel restructure. Memory migrated from the repo's former
  `.claude/memory/` (`CLAUDE.md` + `.claude/` are removed from the repo by the hygiene PR;
  everything durable is now here and in `REALM.md`/`STATE.md`). First plan `001` prescribed
  by `citadel/docs/ROADMAP.md` (Zig 0.16 migration — trivial for synod, see `STATE.md`).
- Next: open plan 001 PR (if not open) → await human merge.
- Open questions: none.

## Standing backlog (carried from the old `.claude/memory/project-context.md`)

- Phase: Bootstrap complete. Phase 1 (Core Types & Log) not yet started. Version 0.1.0,
  unreleased. `zig build test` green on the skeleton (12 trivial stub tests); CI green.
- Next priority, in order:
  1. **1A** — `src/types.zig`: `NodeId`/`Term`/`Index`/`Entry`/`HardState`/`Snapshot`/
     `Message` union/`ConfChange`. Tests: Message union tag exhaustiveness, HardState
     comparison.
  2. **1B** — in-memory Raft log (`src/log.zig`): append/truncate/`termAt`, conflict-point
     search, `validate()`.
  3. **1C+1D** — vtable interfaces (`src/interfaces.zig`: Transport/LogStore/StateMachine/
     Clock/Rng) and an in-memory `LogStore` (`src/store.zig`). Tests: save/restore
     round-trip.
- After 1A-1D: Phase 2, `raft/node.zig` — election state machine (Follower/Candidate/Leader,
  PreVote).
