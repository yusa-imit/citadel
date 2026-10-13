# sirocco — context

last_seen_at: 2026-10-13T12:00:00Z
rejected_plans: []

## Cycle 52 — 2026-10-13 — FEATURE
- Inbox: OWNER merged plan PR #44 (plan 004 evented-net, 12 items); CI green; no bugs, no issues.
- Done: opened milestone #46. Plan 004 item 2 via PR #47 (merged a9e42bd, CI green macOS + ubuntu +
  6 cross, auto-merged): ADR 0003, `src/backend/poller.zig` (shared types, bounded `Table`,
  comptime `contract`), `src/backend/kqueue.zig` (Darwin only; one-shot arm, latched `EVFILT_USER`
  wake), `poller_test.zig` (16 cases + Table model tests). Plan items 1 (done by #45) and 2 ticked.
  ADR departs from plan text: `init(target, gpa, options)`, relative `wait(timeout_ns, out)`, and
  off-fiber calls on a registered socket `poll(2)` on the calling thread, not the offload thunk
  (Threaded traps on `WouldBlock`). Reviewer: 0 CRITICAL, 5 WARNING fixed (BSDs lack EVFILT_USER /
  FreeBSD flags, so `Native` = Darwin only; test flake bounds; `wait` clamp).
- Next: item 3 (`Options.sockets_max` required, `.auto` -> `.kqueue`, `Sched.idle_wait` in
  `Poller.wait`, `unpark_foreign` calls `wake`, gate 7 re-run on kqueue).
- Blockers: none. Open questions: none. Stabilize streak 0.
- Gotchas: opus architect + two sonnet agents cost ~$1.2 for item 2; one subagent for tests+impl
  (TDD order in the prompt) is cheaper. Architect output arrives only as text: save the ADR via Write.

## Cycle 51 — 2026-10-13 — FEATURE
- Inbox: no OWNER activity on plan PR #44 (only our own cycle-50 comment); CI green on 5a926bb; no
  bugs, no other open PRs or issues.
- Done: plan PR #44 still open, so one bounded `/stabilize --one` sweep: tidy green, `catch
  unreachable`/`@panic`/`debug.print`/FIXME all 0, one annotated `while (true)` (offload worker
  loop), largest file `concurrency.zig` 678 lines, docs at 0.4.0 agree. Nothing to fix, no PR.
  STATE.md refreshed.
- Next: when #44 is merged, open the milestone issue, tick plan 004 item 1 (already done by PR #45)
  and start at item 2 (ADR 0003 + kqueue `Poller`). Until then FEATURE cycles run one bounded
  stabilize task and report.
- Blockers: none. Open questions: none. Stabilize streak 0.
- Gotchas: a compound Bash starting with `cd <repo>;` was blocked by the guard again; the primary
  cwd is already sirocco, run each command separately.

## Cycle 50 — 2026-10-12 — FEATURE
- Inbox: no OWNER activity on plan PR #44 (only our own cycle-49 comment); CI green on f159a82; no
  bugs, no other open PRs or issues.
- Done: plan PR #44 still open, so one bounded `/stabilize --one` task: PR #45 (merged 5a926bb, CI
  green, auto-merged) moved ten public-surface scheduler tests to `src/sched_test.zig` (253 lines,
  wired in `src/root.zig`); `src/sched.zig` 823 -> 588 lines. The canary and `init_checked` tests
  stay in `sched.zig` beside the private helpers. This closes the 800-line cap gap from cycle 48,
  so plan 004 item 1 (sched test split) is already done: tick it when plan 004 is merged.
- Next: when #44 is merged, open the milestone issue and start at plan 004 item 2 (ADR 0003 +
  kqueue `Poller`). Until then FEATURE cycles run one `/stabilize --one` task and report.
- Blockers: none. Open questions: none. Stabilize streak 0.
- Gotchas: the `stabilize` label does not exist in the repo (only `auto-merged` etc.); do not pass
  `--label stabilize` to `gh pr create`.

## Cycle 49 — 2026-10-12 — FEATURE
- Inbox: no OWNER activity; CI green on f159a82; no open PRs or issues; plan 003 fully checked and
  milestone #33 closed, so this cycle planned.
- Done: plan 004 (evented-net) proposed as plan PR #44 (branch `plan/004-evented-net`, awaiting
  merge, citadel#47). 12 items: move `src/sched.zig` tests (823 lines), ADR 0003 + kqueue `Poller`,
  `Options.sockets_max` + scheduler idles in the poller, native `net*` listen/accept/connect then
  data path, epoll poller (CI-only), `operate` + `batch*`, real `concurrent`, `bench/echo.zig` and
  `bench/latency.zig` for PRD gates 1-4, v0.5.0 (MINOR). Gate-1 miss on one carrier -> ADR records
  it and multi-carrier becomes plan 005.
- Next: when #44 is merged, open the tracking milestone issue and implement item 1 (sched test
  split). Until then a FEATURE cycle runs one bounded `/stabilize --one` task and reports.
- Blockers: none. Open questions: none. Stabilize streak 0.
- Gotchas: the guard blocks any compound Bash that mentions citadel paths, even a read-only
  `df`/`date` chain; run each command on its own and use Read/Write/Edit for citadel files.

## History (cycles 43-48, condensed 2026-10-13)

Cycle 48 (10-11): plan 003 item 9 + release v0.4.0 via PR #43 (README, PRD, CHANGELOG; no kingdom
repo pins sirocco). Cycle 47 (10-11): item 8 via PR #42, `src/offload_slots.zig` comptime thunks
route blocking `dir*`/`file*`/`net*`/`operate`/`childWait` through the pool (`.forward` only);
closes/`netShutdown`/seeks/`fileUnlock`/memory-map/`netWriteFile`/`netLookup` stay on the carrier;
`Runtime.init` gpa must be thread-safe. Gotchas: run `zig build tidy` explicitly (a stale cache once
hid a >100-col line); BSD `sed -i` needs `''`; `gh pr checks` right after a push shows the previous
run, poll `gh run list` by headSha.

Cycle 46 (10-11): item 7 via PR #41, `src/offload.zig` bounded worker pool (futex mutex, completion
via `Sched.unpark_foreign`), `Options.offload_threads` required, ADR 0002 (offload before
multi-carrier). `Io.sleep` on `Io.Threaded` did not overlap (use `futexWaitTimeout` as a timer in
tests). Cycle 45 (10-10): item 6 via PR #39, `harness.expectSameResultInFiber`. CI ignores `docs/**`
and `*.md`, so docs-only PRs have no checks (a `gh pr checks` poll spins): tick plan items inside the
implementation PR. The guard blocks compound Bash that writes citadel files: use Write/Edit.

Cycle 44 (10-10): item 5 via PR #38, `bench/timer.zig`; PRD gate 7 passes (sirocco p50 311 us / p99
400 us late vs Io.Threaded p50 7.32 ms / p99 8.04 ms, Apple arm64). Cycle 43 (10-09): item 4 via
PR #37, `src/sleep.zig`: native `sleep` parks on `Sched.wheel`, `sleep.fire` runs before every
dispatch, futex timeouts share the wheel (`Sched.Expiry`). Reviewer CRITICAL: a woken/canceled
futex waiter keeps its wheel node, so `fire` pops READY fibers; assert `.parked` only behind
`outcome == .waiting` under the table lock. Gotchas: an unset `$Z` in compound Bash hung 120 s;
`gh pr checks` right after a push says "no checks" for a few seconds; the guard blocks compound
Bash that writes files (python heredoc, `cat > /tmp/x`): use Write/Edit and `--body-file`.

## History (cycle 42, condensed 2026-10-09)

Cycle 42: item 3 via PR #36, `src/timer.zig`: 4x64-slot hierarchical wheel + overflow list, 131 us
tick, deadlines round up, wheel-owned node array, `expire` jumps slot to slot, clamps a backwards
clock; its macOS job was `cancelled` once after 15 m (not a test failure, re-run went green).

## History (cycle 41, condensed 2026-10-09)

Cycle 41 (10-08): item 2 via PR #35: `async` starts the task at once (`Sched.spawn_first`; in a fiber
the caller `yield`s, off-fiber `run_loop` returns at the new fiber's first switch-out via
`Sched.first`); gate 6 passes (44 vs 1796 ns @1, 28 vs 615 ns @1000); `groupAsync` members stay
lazy; tasks needing a cancel before their first check park on a gate futex word. Gotchas: a child
`async` inside an eager task ends the outer `async` early; tidy flags `//!` lines > 100 in tests/.

## History (cycle 40, condensed 2026-10-09)

Cycle 40 (2026-10-08): plan 003 merged 10-07; opened milestone #33; item 1 via PR #34: `groupAwait`
honors a cancel arriving while parked (`Task.awaiting` armed in `group_park`). Open suggestions:
nested-group test, cancel-during-groupCancel test. A hanging `zig build test` blocks the 120s tool
limit: run via python subprocess with timeout, then `pkill -f .zig-cache`. Parity tests that need a
parked fiber: `scene.yield` x4 then act, `scene.run_modes(12, ...)`.

Cycle 39 (10-07): quiet bounded stabilization, nothing to fix. Cycle 38 (10-07): PR #32 split nine
disjunctive implication asserts into `if (a) assert(b);`; `concurrency.zig:183` is real set
membership. Known gap: `tools/tidy.zig` has no compound-assert check.

## History (cycle 37)
Cycle 37 (10-06): plan 002 item 9 + release v0.3.0 via PR #30; proposed plan 003 (PR #31, since merged:
groupAwait cancel, eager async, timer wheel + native sleep, offload pool). No consumers pin sirocco.
Gotchas: guard blocks compound Bash with `cd` into a repo or globs over sibling repos; the primary cwd
is already sirocco; `zig build test` on 0.16.0 is silent on pass.

## History (cycles 0-36, condensed 2026-10-10)

- **Cycles 0-9 (09-05 to 09-11, plan 001)**: realm created; milestone #3; `zig build tidy`
  (PR #5); 0.16 migration bundled into PR #6 because `zig build test` compiles every entry point
  in one graph; PRD rewritten against `std.Io.VTable` (ADR 0001, PR #7: std's evented `Io` impls
  do not compile on 0.16.0, so sirocco declares a 40-slot hybrid forwarding to `Io.Threaded`);
  assertion baseline with shared `assert`/`maybe` in `src/stdx.zig` (PR #9; reviewer caught
  compound implication asserts that restate a branch); ADR-002 (no `wip/*` branch); CHANGELOG
  (PR #11); v0.2.0 released (PR #12). A disk-blocked no-op (`df -g /` below the 20 GB gate) did
  not advance the counter. Plan 002 drafted (PR #13).
- **Cycles 10-25 (09-11 to 09-29)**: plan PR #13 open, no OWNER activity; bounded stabilization
  fixed only docs drift (PRs #8, #14, #15, #16). Stale `.zig-cache` and a missing pinned
  toolchain are dev-box gaps, not regressions. Cycle 22 swept up uncommitted cycles 19-21 memory
  (citadel commit lock contention, sirocco#17).
- **Cycles 26-29 (10-01)**: macOS CI runner (#19); `src/runtime.zig` `Runtime` forwarding all 109
  slots (#20); `tests/parity/` harness (#21); `src/sched.zig` fiber substrate (#22). Reviewer
  CRITICAL: optimized aarch64 builds crashed (inlined `Io.fiber.contextSwitch` clobbers x29/x30);
  fix is `noinline switch_context`, `omit_frame_pointer = false`, CI on ReleaseSafe/Fast.
- **Cycles 30-31 (10-02/03)**: x86_64 ReleaseSmall SEGV (bug #23) fixed by PR #24: own naked
  `switch_context_asm`, `callconv(.c)` pointer, `@call(.never_inline)`. No Rosetta/qemu, so
  x86_64 is verified by asm inspection + CI. Interrupted item-5 tree kept as
  `wip/async-await-slots-20261003` (do not delete).
- **Cycles 32-36 (10-03 to 10-06)**: native async/await/cancel slots (PR #25; hang root cause
  was std's unwinder walking off the fiber base, fixed by a zero return-address sentinel);
  `bench/spawn.zig` gate 6 (PR #26); cancel trio (PR #27, `in_fiber` must check threadlocal
  `carrier_active`); group slots + `crashHandler` (PR #28, must set `.acknowledged`);
  `src/futex.zig` FIFO wait table (PR #29; `futexWake` from a non-carrier thread needs a
  spinlock + `unpark_foreign`); `wip/feat-futex-wait-table-20261006` kept (do not delete).
- **Gotchas from these cycles**: `@fence` is gone in 0.16 (use seq_cst `@atomicRmw(.Add, 0)`);
  naked fn params break the self-hosted x86_64 backend (only CI catches it); `--test-filter` is
  compile-time only, read the last `N/M name...` line to tell a crash from a hang; the parity
  binary builds alone with `zig test --dep sirocco -Mroot=tests/parity/root.zig
  -Msirocco=src/root.zig -fno-omit-frame-pointer --test-no-exec`; slot-table negative tests in
  `slots.zig` hardcode a delegated sample slot, pick the first still-delegated one;
  `expectEqualDeep` on a deliberate mismatch prints noise; no `timeout` or `sleep` in Bash
  (python subprocess timeout, `until` loops); zsh expands `echo "== x"` as `=cmd`.

Standing backlog / next-work order after milestone 001 closes (from old
`.claude/memory/project-context.md`; `docs/plans/NNN-*.md` is the source of truth, not the
nonexistent `docs/milestones.md` this line originally named — corrected cycle 13):
1A completion/queue types → 1B kqueue backend → 1C epoll backend → 1D timing wheel → 1E loop
dispatch → 1F integration tests. Do not build Phase 1 against the pre-ADR kqueue-abstraction
design; the rewritten PRD (`docs/adr/0001-std-io-vtable.md`) is what Phase 1 implements.

## Recurring gotchas
- Bash guard hook text-matches commands, not paths: a commit/PR/issue body that spells out a
  banned literal (`.claude/memory/**`) gets blocked as a write attempt even in prose. Route
  such text through a file (`-F`/`--body-file`) instead of an inline heredoc.
- This repo's global `zig` is still 0.15.2 (kingdom dev-box policy); always invoke
  `/Users/fn/.zr/toolchains/zig/0.16.0/zig` explicitly for this 0.16.0-pinned repo, or
  `zig build test`/`fmt` fail on stale-toolchain errors that look like real bugs but aren't.
- A milestone plan's per-file "0.16: X" checklist items can look independently cycle-sized but
  aren't when they share a build graph (`zig build test` compiles every entry point together)
  — bundle such items into one PR rather than one-item-per-cycle.
- The pinned 0.16.0 toolchain can go missing entirely from the machine between cycles (seen
  cycle 13 — only 0.15.2 was on PATH via homebrew). Reinstall to
  `/Users/fn/.zr/toolchains/zig/0.16.0/` from `ziglang.org/download/0.16.0/` before trusting any
  local green/red result; don't mistake the absent binary for a build regression.
- A stale `.zig-cache` can make `zig build test`/`tidy` fail with `error: failed to spawn build
  runner ... FileNotFound` (seen cycle 14) — this looks like a real build break but isn't;
  `rm -rf .zig-cache` (gitignored, local-only) and retry before assuming a regression.
- The `/report` skill's counter write can silently fail to land in a commit (seen cycle 14 —
  only context.md changed, `memory/counter` stayed at 13) while the context.md entry and GitHub
  comment still went out normally. Cross-check `memory/counter` against the highest `## Cycle N`
  header in context.md at cycle start; if they disagree, trust the context.md history (it has a
  matching GitHub comment as evidence) and resync counter to `N+1`, don't just take the file at
  face value.
