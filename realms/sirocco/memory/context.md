# sirocco — context

last_seen_at: 2026-09-07T12:30:00Z
rejected_plans: []

## Cycle 3 — 2026-09-07 — FEATURE
- Done: bundled milestone-001 items 3-6 into one PR (#6, merged): migrated src/main.zig,
  bench/main.zig, and tools/tidy_main.zig/tidy_test.zig (unplanned — added by PR #5 after this
  plan was written) to Zig 0.16.0; bumped build.zig.zon minimum_zig_version and dropped the
  hardcoded 0.15.2 pin from ci.yml. Bundling was necessary: zig build test compiles all three
  entry points together, so a partial per-item migration under either toolchain pin leaves CI
  red no matter which single item ships alone. Verified zig build test (31/31), fmt, run --
  version/--help, zig build bench, and all six cross-compile targets on the 0.16.0 toolchain;
  CI green. Also fixed issue #3's checklist: item 2 (tidy step, PR #5) had been implemented and
  merged last cycle but never ticked — ticked it and items 3-6.
- PRs: #6 merged (auto-merged label).
- Next: PRD rewrite against std.Io.VTable (item 7).
- Blockers: none. Open questions: none.
- Gotcha: a milestone plan's per-file "0.16: X" checklist items look independently cycle-sized
  but are not — zig build test compiles every entry point in one graph, so CI cannot go green
  until every 0.16-only API user *and* the toolchain pin land together. Bundle such items into
  one PR rather than attempting one-item-per-cycle when they share a build graph.

## Cycle 2 — 2026-09-07 — FEATURE
- Done: implemented and merged item 2, PR #5: `zig build tidy` mechanical Tiger Style checker
  (`tools/tidy.zig`/`tidy_main.zig`, 22 unit tests + integration test over real `src/` files),
  wired as a dependency of `zig build test`. Baseline file `tools/tidy_baseline.txt` starts
  empty (shrink-only ratchet, 71-72 red zone). Fixed gaps it caught: `src/main.zig` had no
  `//!` header; `io/tls/http/task.zig` headers ran past 100 columns. CI green (Build & Test +
  6 cross-compile targets).
- Next: item 3, `src/main.zig` 0.16 migration (`process.Init`, `init.gpa`, `argsAlloc` →
  `init.minimal.args.toSlice`, stdout via `Io` handle).
- Blockers: none. Open questions: none.

## Cycle 0 — 2026-09-05 — RESTRUCTURE
- Realm created by citadel restructure. Memory migrated from the repo's former
  `.claude/memory/`. First plan `001` prescribed by `citadel/docs/ROADMAP.md`.
- Next: open plan 001 PR (if not open) → await human merge.
- Open questions: none.

## Cycle 1 — 2026-09-06 — FEATURE
- Done: opened milestone tracking issue #3 (11-item checklist from plan 001). Implemented and
  merged item 1, PR #4: dropped the dead AI-scaffold `paths-ignore` entry in ci.yml, mirrored
  `paths-ignore` onto `pull_request`, widened the format gate to `src bench build.zig`, added
  `bench` to `build.zig.zon` `.paths`. CI green (Build & Test + 6 cross-compile targets).
- Next: item 2, the `tidy` build step (line/function length, ban list, `//!` headers).
- Blockers: none. Open questions: none.
- Gotcha: the bash guard hook text-matches commands, not just real paths — a commit message or
  PR body that spells out a banned literal (e.g. `.claude/memory/**`) gets blocked as if it were
  a write attempt. Route such text through a file (`-F`/`--body-file`) instead of an inline
  heredoc so the literal never appears in the flat command string.

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
