# sirocco — decisions

_(migrated from the repo's former `.claude/memory/decisions.md`; keep under 200 lines)_

Format: `## ADR-NNN: Title` / **Date** / **Context** / **Decision** / **Consequences**

## ADR-001: Zero external dependencies

**Date**: 2026-09-05
**Context**: sirocco is a foundation layer of the Zig kingdom; every other component may
depend on it.
**Decision**: Depend only on the Zig standard library. Integrations with other kingdom
components live under `src/adapters/` and are opt-in.
**Consequences**: No dependency cycles across the kingdom. Some functionality (e.g.
compression, event-driven watchers) is deferred until it can be implemented in-tree or
provided through an adapter.

_(Note: this decision is now also stated kingdom-wide in `citadel/core/rules/00-kingdom.md`
— foundation `build.zig.zon` has no `.dependencies`; kept here verbatim since it predates
that file and gives sirocco's own rationale.)_

## ADR-002: No `wip/*` branch to finish or close (plan 001 item 9)

**Date**: 2026-09-10
**Context**: Plan 001 item 9 asks for a decision on any preserved `wip/*` branch from the
kingdom restructure.
**Decision**: `git branch -a` shows no `wip/*` branch was ever preserved for sirocco —
foundation repos (sigil, sirocco, strata, synod) had no interrupted work at restructure time.
The only other non-main branch, `chore/kingdom-restructure`, already merged as PR #1 and is
plan 001's base. Nothing to finish or close.
**Consequences**: None — item 9 is closed as a no-op. Recorded here per the plan's own verify
criterion (PR #10).

## 2026-10-09 — timers: one wheel in `Sched`, futex expiry by callback (plan 003 item 4)

**Decision**: the timing wheel lives in `Sched` (node = fiber index); `sleep.fire` fires it before
every dispatch. A due sleeper is unparked by the scheduler; a due futex waiter goes to
`Sched.Expiry.futex_timeout` because only the futex table can unlink under its lock. Wake and cancel
leave the wheel node linked until the fiber runs and calls `sleep.disarm`, so `fire` may pop a node of
a ready fiber: handlers must re-check the outcome before touching the fiber.
**Consequences**: `Sched.timers` is gone; `Sched.init` needs `now_ns`; wall `sleep` is measured on
`Clock.awake` (a wall-clock step does not move it); CPU clocks forward and still block the carrier.

## ADR-NNN-less: plan 004 item 8b moved to plan 005 (cycle 67, 2026-10-27)

**Context**: 8b (per-operation waiter node so an idle batch wakes on the poller, not on 2 ms wheel
slices) was added to plan 004 by the item-8 PR #55, not by the human-approved plan PR #44.
**Decision**: Not implemented; item 12 released v0.5.0 without it and plan 004 marks 8b `[~]` (moved
to plan 005). Design sketch: `Registry` waiter lists hold a `Waiter` node (prev, next, fiber, outcome)
instead of `*Fiber` (`Fiber.wait`); nodes come from a pool sized at `Runtime.init` (no allocation after
init); `cancel`, `close_on_carrier`, `close_off_carrier`, `closing_finish` and `on_event` change with it.
**Consequences**: an idle `batchAwait*` costs one `recvmsg` per op per slice and wakes within 2 ms.
Needs an architect pass and its own PR round (epoll is CI-only); do not start it inside a release cycle.
