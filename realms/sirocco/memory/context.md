# sirocco — context

last_seen_at: 2026-10-15T04:25:00Z
rejected_plans: []

## Cycle 55 — 2026-10-15 — FEATURE
- Inbox: milestone #46 open, no OWNER comments; CI green on 1f197af; no bugs. PR #49 had been fixed
  and marked ready between cycles (3 fix commits, CI green) without a memory entry.
- Done: re-reviewed #49 (sonnet code-reviewer, ~$0.5): the 7 first-review items were fixed; 1 new
  CRITICAL = a cancel arriving after a readiness wake (fiber `.woken`) was lost and the retry parked
  forever. Fix 3f9f122: `park` calls `task_acknowledge_cancel` first (regression test in
  `tests/parity/net_close.zig` hangs without it); `close_on_carrier` returns bool, a second close of a
  closing slot is a no-op. Merged #49 (30ea8af, CI green macOS + ubuntu + 6 cross, `auto-merged`);
  item 4 ticked on #46 (plan file already ticked on the branch).
- Next: item 5 (data-path slots). Fold in the deferred #49 follow-ups: `.blocking` accept polls with
  infinite timeout and never rechecks `still_open` (foreign close cannot wake it); registry spin lock
  aborts after 2^28 spins while held across kevent calls; assertion density in `src/net.zig` < 2/fn;
  `catch unreachable` at `net_registry.zig:160`; errno gaps (`EPROTO`, `EPERM`, `EINVAL` on
  bind/connect), unchecked `SO_ERROR` cast; cancel-during-connect test can skip.
- Blockers: none. Open questions: none. Stabilize streak 0.
- Gotchas: wake order is most-recent-joiner first (list head); a hanging `zig build test` needs a
  python subprocess timeout then `pkill -f .zig-cache`; to run one test temporarily add `.filters` to
  the parity `addTest` in build.zig (restore it before committing).

## Cycle 54 — 2026-10-14 — FEATURE
- Inbox: milestone #46 open, no OWNER comments; CI green on 1f197af; no bugs, no other PRs.
- Done: plan 004 item 4 as DRAFT PR #49 (branch `feat/native-listen-accept-connect`, commit 5312185):
  `src/backend/sys.zig`, `src/net.zig` (sockets_max registry + 8 native slots incl. `netClose`),
  `src/sched_io.zig` (poller event dispatch + fairness `wait(0)`), `tests/parity/net.zig`; local test/
  fmt/tidy green. Reviewer: 2 CRITICAL + 5 WARNING (full list in the PR comment). Not merged; item 4
  stays unticked on #46 (the plan file is ticked on the branch only).
- Next: fix on #49 first, then `gh pr ready 49`, wait for CI, merge. CRITICAL 1: `slot_close` off the
  carrier races waiter lists/poller/`unpark` (hand waiters to the carrier via `unpark_foreign`).
  CRITICAL 2: `enroll`'s `register catch unreachable` is false (`slot_accept` blocking route registers
  from other threads). WARNINGs: stale-entry replace leaves waiters/poller armed; close wakes waiters
  onto a reused fd (needs a closed outcome); EINTR unmapped; accept fabricates 127.0.0.1:0; tests for
  close-with-waiters, off-fiber route, bind/Unix, cancel during connect. Then item 5.
- Blockers: none. Open questions: none. Stabilize streak 0. CI on PR #49 was still running at report.
- Gotchas: item 4 cost ~$2.6 (developer ~$1.9, reviewer ~$0.3); too big for one 22-min cycle with a
  fix round: split item 4 (sys.zig + listen/accept, then connect/close) if it repeats. Draft status
  keeps the next inbox from auto-merging a PR with open CRITICALs.

## Cycle 53 — 2026-10-14 — FEATURE
- Inbox: milestone #46 open, no OWNER comments; CI green on a9e42bd; no bugs, no other PRs.
- Done: plan 004 item 3 via PR #48 (merged 1f197af, CI green macOS + ubuntu + 6 cross, auto-merged):
  `Options.sockets_max` required; `.auto` -> `.kqueue` on Darwin (`.threaded` elsewhere, `.kqueue`
  refused off Darwin); `Sched.Options.idle` (`.futex`|`.poller`), `idle_wait_poller` blocks in
  `Poller.wait`, `unpark_foreign` calls `Poller.wake`; parity suite compiled once per backend via a
  `parity_config` module. Fixed `sleep.fire` trap when every deadline came due in one pass (loop
  bound `fibers.len + 1`). Gate 7 on kqueue: p50 0.31 ms / p99 0.39 ms (no regression). Reviewer: 0
  CRITICAL, 1 WARNING (CHANGELOG entry) fixed. Items 1-3 ticked on #46 and in plan 004.
- Next: item 4 (`src/backend/sys.zig` + native listen/accept/connect). `idle_wait_poller` asserts
  zero events and the ADR's fairness `wait(0)` per `fibers_max` dispatches is deferred: item 4 must
  replace both with event dispatch. Poller-create failure at first `io()` leaves the runtime
  `.unavailable` (hides EMFILE).
- Blockers: none. Open questions: none. Stabilize streak 0.
- Gotchas: item 3 cost ~$1.9 (one sonnet zig-developer ~$1.3 + reviewer ~$0.2); the 22 min deadline
  is tight with a 10-min implementation plus a 5-min CI; start the PR before the reviewer.

Cycle 52 (10-13): plan 004 merged, milestone #46 opened; item 2 via PR #47 (ADR 0003, `poller.zig`,
`kqueue.zig`, Darwin-only `Native`; `init(target, gpa, options)`, relative `wait(timeout_ns, out)`,
off-fiber calls on a registered socket `poll(2)` on the calling thread). One subagent for tests+impl
(TDD order in the prompt) is cheaper than architect + two agents; architect output is text only.

Cycles 49-51 (10-12/13): plan 004 proposed as PR #44 (12 items, v0.5.0 MINOR; a gate-1 miss on one
carrier becomes plan 005); PR #45 split `src/sched.zig` tests (823 -> 588 lines); cycle 51 sweep found
nothing. Gotchas: no `stabilize` label in the repo; the guard blocks compound Bash (`cd <repo>;`, citadel
paths): run each command alone and use Read/Write/Edit for citadel files.

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
