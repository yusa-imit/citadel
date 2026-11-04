# sirocco — context

last_seen_at: 2026-11-04T05:00:00Z
rejected_plans: []

## Cycle 78 — 2026-11-04 — FEATURE
- Preflight: disk 23 GB, tree clean on main, CI green, no bugs, no OWNER comments, no plan PR;
  milestone #62 open.
- PR #73 (feat/sched-post-mailbox, c6f6789) OPEN, CI pending at the deadline, comment says merge
  next cycle: `src/mail.zig` (`Mail`, `Mailbox`, `post`, `drain`, `serve` moved out of
  `sched.zig`, which was at 791/800 lines and is now 776). `run_loop` drains mail next to the
  inbox; a peer `serve` runs the fibers it is mailed. Pending FIFO when all fibers are alive;
  `outstanding_max` 65536. Tests in `src/mail_test.zig` (futex and poller idle, FIFO with no
  free fiber, mail while a fiber is parked, 3 producer threads, empty after stop). Item 7 stays
  UNCHECKED; plan note and CHANGELOG updated.
- Reviewer (sonnet): 0 CRITICAL. Fixed: plain load before the Xchg, carrier 0 contract
  documented (mail posted to a `run`-only carrier can be stranded), stale header. Open: serve
  drops mail left at stop; `idle_wait` is now pub.
- Next: cycle 79 merges #73 if CI is green (no `hold`), then item 7 remainder: claim CAS on
  `wait.outcome`, join word, cancel mail, `Table.wake` routing by home, close from another
  carrier, seeded 4-carrier model test, 1000 serial runs. Make `run_until`'s stop atomic.
- Gotchas: the newest `.zig-cache/o/*/test` is often the parity binary (196 tests, has the known
  `batch` "64 idle sockets" flake, slow); the library binary has ~134 tests. Identify it by
  running it, not by `strings`. A 300-run loop of it overran the 500 s Bash timeout: background
  it. Cycle spent ~$1.3 and hit the 22 min deadline before CI finished.

## History (cycles 76-77, folded 2026-11-04)

- 77 (11-03): `bench/timer.zig` gates on a 2-carrier runtime (gate 7 p99 316792 ns vs Io.Threaded
  8.01 ms), item 6 ticked (PR #71). Item 7 first steps (PR #72): `Sched.index`, `Fiber.home`,
  threadlocal `Sched.here()`, futex expiry and poller `events` on peer scheds. After a squash-merge,
  cherry-pick follow-up commits onto a fresh branch from origin/main. A `Fiber` literal in tests
  needs `.home`.
- 76 (11-03): item 5 PR #69 merged; item 6 PR #70: `Options.carriers` required (`carriers_max` 64),
  `src/carriers.zig` builds carriers-1 peer `Sched`s, `Sched.notify`, parity suite at 1 and 2
  carriers. Reviewer WARNINGs: `.auto` not swept under a failing allocator; spawn-failure unwind has
  no test seam. `gh pr create` can hit a transient GraphQL 500: check `gh pr list --head`, retry.

## History (cycles 69-75, folded 2026-11-03)

- 75 (11-01): item 5 PR #69 (`src/batch_park.zig`, `batch_sweep.zig`: an all-net_receive batch parks
  on poller+wheel, one Waiter per op; file-op batches keep `wait_sliced`; `ops_max` 128). Reviewer
  CRITICALs fixed: a lost claim after `.gone`/`.resources` now parks; pool-short round naps 100 us
  and sweeps. No end-to-end test of the foreign-close race. Preserved interrupted tree as
  `wip/feat-batch-waiter-plumbing-20261101` (kept). Flaky ~1/40 parity test "64 idle sockets wake
  the batch" panics in std `Io.Batch.cancel` on the baseline side (pre-existing, from #55).
  Guard blocks `python3 - <<EOF` heredocs touching citadel paths: use Edit/Write.
- Disk-blocked no-ops 11-02 (18-19 GB free): stopped at preflight, counter unchanged.

- 74 (10-31): item 4 PR #68 (ff04e14, auto-merged): registry waiter lists link `Waiter` nodes
  (`src/waiter.zig`, `Sched.Waiter`), one node per fiber; `waiter_enter` records slot+generation
  under the lock; `src/net_registry_test.zig`. Suite 480/524, tidy green. Open SUGGESTIONs: `waiter_remove`
  asserts nothing; tests for cancel head/tail, `close_on_carrier` both interests, `.gone`, node
  re-entry. A second push cancels the first CI run: poll `gh run list` by the new headSha.
- 73 (10-31): item 2 `docs/adr/0004-multi-carrier.md` (architect/opus, 12 min / ~$1.5, brief it
  narrower; result arrives HTML-escaped, unescape before writing) merged as PR #67. Decisions:
  `Options.carriers` required, `carriers_max` 64, `fibers_max` per carrier, new `batch_ops_max`;
  `concurrent` round robin, `async` creator-local; `fiber.wait.outcome` CAS is the claim; one futex
  table; one shared registry (`table_lock` + per-slot lock, `armed: [2]u64`); no work stealing;
  `Runtime.init` allocates everything (`5N+4` blocks evented).

- 72 (10-30): item 1 PR #66 (d99f63b): `src/profile.zig` counters on only when the root declares
  `sirocco_profile` (`zig build bench-echo-profile`); ADR 0003 4c: 78% of CPU in the kernel, no
  user-space hot spot, avoidable EAGAIN reads+arms only ~1.3x, so multi-carrier stays. Gotchas: tidy
  flags `std.time.` in src and bench lines > 100 cols; the architect agent has no Write tool.
- 69 (10-27): plan 005 merged (#61), milestone #62 opened. Item 1 blocked: no usable profiler on this
  box (`xctrace` shim only, no `dtrace`, `sample(1)` hangs); question #63 opened. Item 3 PR #64 split
  `sched_fiber.zig` and `concurrency_group.zig` out (a zig-developer call with explicit line ranges
  and verification commands did it in 3.4 min / ~$0.5).
- 70 (10-28): interrupted item 11 tree preserved as `wip/fix-leftovers-plan-005-20261029` (kept,
  never delete); a parity test hung in `cancel`.
- 71 (10-29): #63 closed after no OWNER answer, option (c) chosen. Item 11 PR #65: the hang was a test
  flaw (sockets made off a fiber are not registered, `net.route` needs a creator task; make the pair
  in a fiber via `io.concurrent(connect_pair)`, and use `net_data.init_rt()` (`.forward`) because `.fail`
  mode fails there with NetworkDown). Gotchas: lldb attach hangs on this box; stale `.zig-cache`
  gives FileNotFound, `rm -rf .zig-cache`.

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

## History (cycles 0-36, condensed 2026-10-10, folded 2026-11-04)

- **Cycles 0-25 (09-05 to 09-29, plan 001)**: realm created, `zig build tidy` (PR #5), 0.16 migration
  bundled into PR #6 (`zig build test` compiles every entry point in one graph), PRD against
  `std.Io.VTable` (ADR 0001: std's evented `Io` impls do not compile on 0.16.0, so sirocco forwards
  to `Io.Threaded`), shared `assert`/`maybe` in `src/stdx.zig`, v0.2.0 (PR #12). Plan PR #13 sat
  open without OWNER activity; stabilization fixed docs drift only. A disk-blocked no-op (`df -g /`
  below the 20 GB gate) does not advance the counter.
- **Cycles 26-36 (10-01 to 10-06)**: macOS CI (#19), `Runtime` forwarding 109 slots (#20), parity
  harness (#21), fiber substrate (#22). CRITICAL: optimized aarch64 crashed (inlined context switch
  clobbers x29/x30): `noinline switch_context`, frame pointers kept. x86_64 ReleaseSmall SEGV (bug
  #23, PR #24): own naked `switch_context_asm`; no Rosetta/qemu, verify by asm inspection + CI.
  Native async/await/cancel (PR #25; the unwinder walked off the fiber base: zero return-address
  sentinel), `bench/spawn.zig` (#26), cancel trio (#27), group slots (#28), `src/futex.zig` (#29;
  non-carrier `futexWake` needs a spinlock + `unpark_foreign`). `wip/async-await-slots-20261003` and
  `wip/feat-futex-wait-table-20261006` kept (never delete).
- **Gotchas**: `@fence` is gone in 0.16 (seq_cst `@atomicRmw(.Add, 0)`); naked fn params break the
  self-hosted x86_64 backend (only CI catches it); `--test-filter` is compile-time only, read the
  last `N/M name...` line to tell a crash from a hang; no `timeout` or `sleep` in Bash (python
  subprocess timeout, `until` loops); zsh expands `echo "== x"` as `=cmd`.

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
