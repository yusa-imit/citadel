# sirocco — context

## Cycle 0 — 2026-09-05 — RESTRUCTURE
- Realm created by citadel restructure. Memory migrated from the repo's former
  `.claude/memory/`. First plan `001` prescribed by `citadel/docs/ROADMAP.md`.
- Next: open plan 001 PR (if not open) → await human merge.
- Open questions: none.

## Standing backlog (from old `.claude/memory/project-context.md`)

Phase: Bootstrap complete. Phase 1 ("Loop Core") not started — `docs/milestones.md` is the
single source of truth for progress, not this file. Version 0.1.0, unreleased. Work order:

1. **1A** — `Completion`/`Op`/`Result` types + intrusive (non-allocating) queue. Tests:
   queue push/pop/remove, `Op`-tag coverage.
2. **1B** — kqueue backend. Tests: loopback TCP accept/connect/read/write/close.
3. **1C** — epoll backend (unblocks CI's Linux-only I/O lane).
4. **1D** — hierarchical timing wheel. Tests: register/cancel/expiry ordering, load
   (~100k timers).
5. **1E** — loop dispatch (run modes, cross-thread wakeup, `cancel()`).
6. **1F** — integration tests (loopback echo, timer races, cancel races) once 1A–1E land.

Ahead of 1A: plan `001` should land the Zig 0.16 migration (trivial, <1h — see
`STATE.md`) and, per `citadel/docs/ROADMAP.md` Phase 2, a PRD rewrite targeting
`std.Io.VTable` directly, since sirocco's whole purpose now overlaps the 0.16 `std.Io`
model. Do not build Phase 1 against the old kqueue/epoll-abstraction design without first
reconciling it against `std.Io.VTable`.
