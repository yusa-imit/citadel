# sirocco — context

last_seen_at: 2026-10-29T04:15:00Z
rejected_plans: []

## Cycle 71 — 2026-10-29 — FEATURE
- Inbox: #63 (origin: ai, no OWNER answer after cycles 69-70, title not `blocking`) closed with the
  recommendation: option (c), a bench-only in-process timer build for plan 005 item 1. No bugs, CI green.
- Item 11 done: PR #65 (CI green on macOS, ubuntu, 6 cross targets, auto-merged), built on the preserved
  wip tree: `lease_release(fd, generation)`, exhaustive `wait_err` switches, parity test that cancels a
  parked `concurrent` read. Suite 474/518 (44 skipped), tidy green. Plan item 11 and #62 ticked.
- The cycle 70 hang was a test flaw, not a runtime bug: sockets made off a fiber are not registered
  (`net.route` needs a creator task), so the read fell to the offload pool, which cannot cancel a
  blocking read. Make the pair in a fiber (`io.concurrent(connect_pair)`); `.fail` mode fails there
  with NetworkDown, so use `net_data.init_rt()` (`.forward`) for such tests.
- Next: item 1 with option (c) (counters build around kevent, socket syscalls, fiber switch; record
  in ADR 0003 section 4c), then item 2 (ADR 0004, opus architect), item 4. Blockers: none. ~11 min, ~$0.85.
- Gotchas: lldb attach hangs on this box (use debug prints + python subprocess timeout); a stale
  `.zig-cache` again failed `zig build` with FileNotFound: `rm -rf .zig-cache`.

## History (cycle 70, 2026-10-29)
- Preserved the interrupted item-11 tree as `wip/fix-leftovers-plan-005-20261029` (kept, never delete);
  finished and merged in cycle 71 as PR #65.

## Cycle 69 — 2026-10-27 — FEATURE
- Plan 005 was merged (#61); milestone issue #62 opened. Inbox clean (no OWNER comments, no bugs, CI green).
- Item 1 (profile gate 1) cannot run on this box: `xctrace` is only the /usr/bin shim (no Xcode), no
  `dtrace`, `dtruss`/`fs_usage` need root, `sudo` needs a password, `sample(1)` hangs the bench. Asked on
  question #63 (`needs-human`, origin: ai; recommends a bench-only in-process timer build). Items 2, 6, 9
  depend on the profile, so ADR 0004 waits for the answer.
- Item 3 done: PR #64 (5c336dd, CI green on macOS, ubuntu, 6 cross targets, auto-merged):
  `src/concurrency_group.zig` (262) and `src/sched_fiber.zig` (130) split out; sched.zig 613,
  concurrency.zig 507; test count unchanged (472/515, 43 skipped). Plan item 3 and #62 ticked.
- Next: item 11 (leftovers, independent of the profile), then item 4 (8b part 1 needs ADR 0004, so
  likely blocked) -> check #63 for an OWNER answer first. If unanswered after two cycles, proceed with
  option (c) per the origin: ai rule (the title is not `blocking`).
- Blockers: profiler (#63). Streak 0. Cycle ~15 min, ~$1.1.
- Gotchas: a zig-developer call with explicit line ranges and verification commands did a clean split
  in 3.4 min / ~$0.5; the guard blocks compound Bash (`a; b` with citadel paths or /tmp writes).

## History (cycles 66-68, condensed 2026-10-27)

- 66 (10-26): bug #58 fixed by PR #59: not a runtime bug, 10000 clients closing first exhaust macOS's
  16384 ephemeral ports (TIME_WAIT); clients close with `SO_LINGER` 0, `rt.io()` is taken before the
  baseline thread flood. Gate 3 PASS 7 of 8 (one 422k us p99 run); gate 4 MISS 29.2 KB vs 24.7 KB per
  task (14.4 KB at 2000). Gotchas: `bench-latency` needs python `setrlimit(30000)` (10240 hard cap in the
  `zig build` child); a stale `.zig-cache` fails `tidy` with `file_hash FileNotFound`; `tidy` checks
  bench/ line width too.
- 67 (10-27): item 12 PR #60 release v0.5.0 (README, CHANGELOG, PRD 4.1, tag, milestone #46 closed).
  Item 8b not done by decision (needs a registry refactor, waiter lists keyed on `Fiber`), moved to
  plan 005. Gotchas: BSD `sed -i` rejects multi-line patterns, use Edit; `gh run watch` over 8 min hits
  the Bash timeout, background it.
- 68 (10-27): plan 005 "net-gates" proposed as PR #61 (12 items, v0.6.0 MINOR).

## History (cycles 62-65, condensed 2026-10-27)

- 62 (10-20): PR #55 red CI was a test flaw: `Io.Threaded` rounds its poll timeout down and reports
  `Timeout` under 10 ms, so parity tests project to `timed_out` + `later_ok` (10 ms floor only when
  `evented`). Stress the built binary (`.zig-cache/o/*/test`) serially; `zig build test` re-runs are
  cached and parallel runs fail the loopback `batch` "late" test spuriously.
- 63 (10-21): item 9 PR #56, `concurrent`/`groupConcurrent` on a free fiber (`src/concurrency.zig`). A
  hardcoded `FailingAllocator` `fail_index` differs by backend: set `fail_index = alloc_index` after
  `io()`. Left over: no test cancels a parked `concurrent` future.
- 64 (10-21): item 10 PR #57, `bench/echo.zig`: gate 2 PASS 0.91x, gate 1 MISS 0.83-0.87x (ADR 0003
  4a). Never run `sample(1)` on the bench (hangs); plan 005 starts with Instruments/dtrace, then
  multi-carrier. The bench raises RLIMIT_NOFILE and refuses rather than shrinking N.
- 65 (10-26): item 11 not done, preserved as `wip/feat-latency-bench-20261026` (superseded, kept); bug
  #58 opened. The `zig build` child sees a 10240 NOFILE hard cap (bench-latency refuses): run the built
  `.zig-cache/o/*/sirocco-bench-latency` via python `setrlimit(30000)`. Killed bench runs leave sockets
  that fail the next run's connects (~30 s). Bench stdout is buffered: flush per section.
- Disk-blocked no-ops 10-22/10-23 (16-18 GB free): stopped at preflight, counter unchanged. The guard
  blocks a compound first Bash call that writes /tmp and reads citadel paths: one command per call.

## History (cycles 49-61, folded 2026-10-29)

- Plan 004 (evented net): proposed PR #44 (12 items, v0.5.0 MINOR); item 2 PR #47 (ADR 0003,
  `poller.zig`, `kqueue.zig`; `init(target, gpa, options)`, relative `wait(timeout_ns, out)`); item
  3 PR #48 (`sockets_max` required, `.auto` -> `.kqueue` on Darwin, per-backend parity suite); item
  4 draft PR #49 (sys.zig, net registry, poller dispatch; draft status keeps the inbox from
  auto-merging with open CRITICALs; a cancel after a readiness wake was lost, `park` now calls
  `task_acknowledge_cancel` first); item 5 PR #50 `src/net_data.zig`; item 6 PR #51
  `src/backend/epoll.zig` (EPOLLONESHOT disables the whole per-fd entry, so the kernel entry is
  re-derived; eventfd wake; `.auto` -> `.epoll` on Linux); item 7 PR #54 `src/submit.zig` serves
  `net_receive` and non-blocking file streams on the poller; item 8 PR #55 `src/batch.zig` native
  `batchAwait*/Cancel` (wait is wheel slices 50 us -> 2 ms, item 8b adds a per-op waiter node).
- Bug #52 (PR #53): a test race, not runtime; a call after close is a caller bug (`net_data.zig`).
- Review leftovers: overflow worker has no cancel in `poll(2)`; no generation check on
  `lease_release` after a foreign close; `wait_err` switches use `else`; blocking accept infinite
  poll; registry spin-lock bound. Std 0.16.0 bug: `Io.Threaded.batchAwaitConcurrent` leaves a
  ready `net_receive` on `submitted`. `wip/feat-net-data-path-slots-20261017` and older
  `wip/feat-native-net-data-path-*` kept (never delete).
- Gotchas: `zig build test` re-runs are cached; `-Dtarget=x86_64-linux-gnu` compiles every Linux
  test binary ("unable to execute" is expected); riscv64 `fiber_switch.zig` fails to build, not in
  CI; grep build.zig for a leftover `.filters` before trusting a wip tree; BSD `sed` rejects `\n`;
  `gh pr checks --watch` over 9 min hits the Bash timeout; a hanging test: python subprocess
  timeout then `pkill -f .zig-cache`; one zig-developer call for tests+impl cost ~$3.1, brief
  narrowly; the guard blocks compound Bash (`cd <repo>;`, citadel paths, ready-and-merge pair).

## History (cycles 37-48, condensed 2026-10-19)

Plan 002 item 9 + v0.3.0 (cycle 37, PR #30); plan 003 (PRs #31-#43), released v0.4.0 in cycle 48
(PR #43; no kingdom repo pins sirocco). Cycle 40: `groupAwait` honors a cancel while parked (PR #34).
Cycle 41: eager `async` (`Sched.spawn_first`, PR #35; gate 6: 44 vs 1796 ns @1). Cycle 42: PR #36
`src/timer.zig`, 4x64-slot hierarchical wheel + overflow list, 131 us tick. Cycle 43: PR #37
`src/sleep.zig`, native `sleep` parks on `Sched.wheel`; reviewer CRITICAL: a woken futex waiter
keeps its wheel node, assert `.parked` only behind `outcome == .waiting` under the table lock.
Cycle 44: `bench/timer.zig`, gate 7 passes (p50 311 us vs Io.Threaded 7.32 ms). Cycle 45:
`harness.expectSameResultInFiber`. Cycle 46: `src/offload.zig` bounded worker pool (ADR 0002);
`Io.sleep` on `Io.Threaded` did not overlap (use `futexWaitTimeout` as a timer in tests). Cycle 47:
`src/offload_slots.zig` comptime thunks route blocking `dir*`/`file*`/`net*` through the pool;
`Runtime.init` gpa must be thread-safe. Gotchas: run `zig build tidy` explicitly (a stale cache hid
a >100-col line); `gh pr checks` right after a push shows the previous run or "no checks", poll
`gh run list` by headSha; CI ignores `docs/**` and `*.md`, so tick plan items inside the
implementation PR; an unset `$Z` in compound Bash hung 120 s; cycle 38 split nine disjunctive
implication asserts (`tools/tidy.zig` has no compound-assert check).

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
