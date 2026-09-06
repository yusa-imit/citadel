# strata — context

last_seen_at: 2026-09-06T05:08:21Z
rejected_plans: []

## Cycle 1 — 2026-09-06 — FEATURE
- Done: plan 001 (PR #2, merged prior cycle) had unchecked items and no milestone issue →
  opened tracking issue #3. Implemented plan 001 item 1 (hygiene leftovers: fixed
  `src/root.zig` doc comment pointing at renamed `docs/milestones.md` → `docs/plans/`;
  added `CHANGELOG.md`) via PR #4, all 7 CI checks green, squash-merged, item ticked on #3.
- PRs: #4 merged (auto-merged label).
- Next: plan 001 item 2 (`tidy` step, part 1 — shape: line length ≤100, `//!` headers).
- Blockers: none.
- Open questions: none.

## History
- Cycle 0 (2026-09-05, RESTRUCTURE): realm created by citadel restructure; memory migrated
  from the repo's former `.claude/memory/`; plan 001 prescribed by ROADMAP.md.

## Standing backlog (carried from the repo's former project-context.md)

- Phase: Bootstrap complete. Next: Phase 1 (`docs/milestones.md` is the single source of
  truth for progress; `docs/PRD.md` is the single source of truth for requirements).
- Version: 0.1.0, unreleased. No git tags yet.
- `zig build test` green on the skeleton (11 trivial compile-check tests); CI registered,
  one fix-up commit already landed (Linux-only test job, macOS covered by cross-compile).
- Queued Phase 1 items, in dependency order:
  1. 1A — codec: CRC32C (hardware-detect + software fallback) and varint; test standard
     vectors, boundary values, hw/sw parity.
  2. 1B — `File` with `SyncPolicy`; test via `tmpDir`: writeAt/readAt/sync/preallocate/lock.
  3. 1D — crash-injection harness; test enumerated truncation points, generated file ends at
     the specified offset. (1D is listed ahead of 1C/mmap because later phases — WAL,
     B+Tree — need the harness before they need mmap.)
- Zig 0.16 migration (plan 001) is trivial for this repo (<1h, one file, one error class —
  see `STATE.md` and `citadel/core/rules/zig-0.16.md`); sequence it with or just before 1A so
  new Phase 1 code is written directly against 0.16 shapes.

## Next priority

Phase 1A (codec) is the next concrete implementation step once plan 001 is approved — it has
no internal dependencies and later phases (page, wal) depend on it.
