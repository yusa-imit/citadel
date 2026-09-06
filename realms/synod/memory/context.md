# synod — context

last_seen_at: 2026-09-06T01:00:00Z
rejected_plans: []

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
