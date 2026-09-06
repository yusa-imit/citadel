# zr — context

last_seen_at: 2026-09-06T21:06:26Z
rejected_plans: []

## Cycle 1 — 2026-09-06 — FEATURE
- Preflight found the tree dirty on `feat/tidy-build-step` (uncommitted `tidy` build-step work
  from a prior session: `tools/tidy.zig`, `build.zig` wiring, `tidy_baseline.txt`) — preserved
  to `wip/feat-tidy-build-step-20260907`, pushed, then returned to `main`.
- Inbox: CI green, no bug issues, no plan PR open, plan 001 (#154) merged, milestone #155 open
  with item 1 done. PR #30 (zuda graph migration) still draft/OWNER — untouched per rule
  (never touch draft PRs); listed for a future cycle's decision, not acted on.
- Implemented milestone #155 item 2 (`tidy` build step): finished the wip work into
  `feat/tidy-build-step-lint`. Found and fixed a real **use-after-free** in the vendored
  `tools/tidy.zig`'s `checkFunctionLength` — see `debugging.md`. Same bug lives in
  `citadel/templates/tidy` upstream; not fixed here (out of scope for a realm session — only
  `/report` may touch citadel — but flagged for a citadel cycle).
- PR #157 opened; `Build & Unit Test` and `Integration Test` green, 6-target cross-compile
  matrix still running at the cycle deadline. Comment posted on the PR; left for next cycle's
  `/inbox` to merge once green (or fix if red).
- Next: merge #157 once CI is green, tick milestone #155 item 2, then item 3 (assertion
  baseline) or item 4 (wip/advanced-retry-config + PR #30 decision) — both unblocked.
- Open questions: none.

## Cycle 0 — 2026-09-05 — RESTRUCTURE
- Realm created by citadel restructure. Memory migrated from the repo's former
  `.claude/memory/` (MEMORY.md, project-context.md, architecture.md, decisions.md,
  debugging.md, patterns.md, zig-0.15-migration.md — condensed into this directory).
- Working tree at survey time was dirty with a finished, tested feature (advanced retry
  config: backoff multiplier, jitter, max backoff, retry-on codes/patterns in
  `src/config/parser.zig`/`types.zig`) — preserved on branch `wip/advanced-retry-config`
  rather than committed directly or discarded. Land it via a real PR in an early cycle.
- First plan `001` (Zig 0.16.0 migration) prescribed by `citadel/docs/ROADMAP.md` — blocked
  on zuda v3.0.0 and sailor v3.0.0 (their own `build.zig` must migrate off `linkLibC()`
  first). Do not start 0.16 migration work until that unblocks; do not write new 0.15-only
  code in the meantime either (kingdom convention).
- Next: open plan 001 PR if not already open → await human merge. In parallel (not gated on
  the plan), triage: PR #30 (zuda graph-algorithm migration, decide merge vs close), the
  root/docs hygiene cleanup (see STATE.md), and the zuda dependency's non-tag git pin.
- Open questions: none.

## Standing backlog (carried from the repo's old project-context.md)

- Decide open PR #30 "chore: migrate to zuda for graph algorithms" (yusa-imit/zr) — recorded
  decision already keeps topo sort / cycle detection / work-stealing deque custom for perf,
  so this PR may be supersedable rather than mergeable as-is; check its diff against that.
- Commit or formally supersede the advanced-retry-config work on `wip/advanced-retry-config`
  (finished and tested, was never committed).
- `zuda` pinned by `git+...?ref=main#<hash>` instead of a tag, and at v2.0.4 while `silica`
  pins v2.3.0 — both violate kingdom rules (tag-only pins, one version kingdom-wide); already
  flagged in `citadel/docs/KINGDOM.md` ROADMAP Phase 0.
- README/CLAUDE.md-era docs had stale version numbers (README badge v1.84.0 vs actual
  v1.114.0) and a stale module-structure diagram — resolved by this restructure replacing
  `CLAUDE.md` with `REALM.md`/`STATE.md`; keep those current going forward instead.
- Milestone backlog was empty at survey time ("READY milestones: 0") — establish the next
  milestone via a plan PR rather than free-form feature work.

## Current priority

Root/docs hygiene PR first (delete tracked `.o` binary, move root release-notes/scripts,
remove `.claude`/`CLAUDE.md`, drop or gitignore stray `zig-pkg/`), then PR #30 triage and the
retry-config branch, then begin plan `001` prep once zuda/sailor v3.0.0 land.
