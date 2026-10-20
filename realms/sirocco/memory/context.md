# sirocco — context

last_seen_at: 2026-10-20T04:30:00Z
rejected_plans: []

## Cycle 62 — 2026-10-20 — FEATURE
- Inbox: milestone #46 open, no OWNER comments, no bugs, main CI green; PR #55 had red CI (both OS jobs).
- Done: PR #55 fixed and squash-merged as 7687892 (`auto-merged`); item 8 ticked on #46. Cause was a test
  flaw, not the runtime: `Io.Threaded` rounds its poll timeout down and reports `Timeout` under 10 ms, so
  the idle parity test (a) compared `waited` against that oracle, (b) asserted `waited` on `rt.io()` for the
  `.threaded` backend where `rt.io()` IS the baseline (the 42-skip binary). Fix 7a12aba: parity projects
  to `timed_out` + `later_ok`; the 10 ms floor is asserted only when `evented`.
- Verified by running the parity binaries 36x each, 6-way parallel: 0 failures (was ~20-30%).
- Next: FEATURE, item 9 (`concurrent`/`groupConcurrent`), then 8b (per-op waiter node), 10, 11, 12.
- Blockers: none. Open questions: none. Streak 0. Cycle used ~16 min, ~$1.
- Gotchas: a parity test whose oracle is `Io.Threaded` is unsound for any timing floor. Running one test
  binary many times in parallel makes the loopback `batch` "late" test fail (a datagram from another
  process lands in a rebound ephemeral port); serial runs are clean, so do not read that as a bug. Run a
  stress of the built binary (`.zig-cache/o/*/test`), since `zig build test` re-runs are cached. Stale
  `.zig-cache` gave `failed to spawn build runner` again (rm -rf it).

## Cycle 61 — 2026-10-20 — FEATURE
- Inbox: milestone #46 open, no OWNER comments (only our own reports), no bugs, CI green, no plan PR.
- Done: item 8 as PR #55 (`feat/batch-poller`, ready, not yet merged): `src/batch.zig` native
  `batchAwaitAsync/Concurrent/Cancel` for fiber-awaited batches of one-message registered-socket
  `net_receive` and non-blocking file streams, else the whole batch goes to `Io.Threaded`. The wait is
  wheel slices (50 us -> 2 ms), NOT a poller park (a fiber sits on one waiter list only), so no
  `ConcurrencyUnavailable`; plan item 8b added for a per-op waiter node. ADR 0003 section 2c.
- Review (code-reviewer): 0 CRITICAL, 4 WARNING all fixed: a socket closed mid-wait now completes with
  `SocketUnconnected` (new test), stale ADR/header text, empty-batch cancel, plan deviation noted.
  Std 0.16.0 bug: `Io.Threaded.batchAwaitConcurrent` leaves a ready `net_receive` on `submitted`.
- Next: first thing, `gh pr checks 55`; green + no hold -> squash-merge, label `auto-merged`, tick item 8
  on #46 (plan file already ticked in the PR). Then item 9 (`concurrent`/`groupConcurrent`).
- Blockers: none. Open questions: none. Streak 0. Epoll batch tests only cross-compiled (ubuntu CI is
  their first run). CI was still pending at the 22-min deadline (macOS + ubuntu queued).
- Gotchas: one zig-developer call for item 8 took ~9 min / ~$1.4 with a narrow brief and a 14-min cap;
  `gh pr checks --watch` of 9 min hits the Bash timeout; the guard blocks compound Bash writing citadel
  files (use Write/Edit); the sweep needs `rt` to consult the registry.

## Cycle 60 — 2026-10-19 — FEATURE
- Inbox: milestone #46 open, no OWNER comments, no bugs, CI green, only draft PR #54 open.
- Done: reviewed #54 (code-reviewer, 2.6 min): 0 CRITICAL, 4 WARNING. Fixed in a2d2ed5: file read/write
  syscall switches list every `sys.FileError` member (no `else`), CHANGELOG `[Unreleased]` entry, overflow
  doc states the uncancellable-worker bound. CI green (ubuntu epoll first run, macOS, 6 cross). Ready +
  squash-merged #54 (`auto-merged`); item 7 ticked in plan 004 and on #46.
- Review leftovers (not blocking): overflow worker sits in `poll(2)` with no cancel when the registry is
  full; lease taken before the first syscall (two lock holds when data is ready); no test for a cancel
  between readiness wake and resume; `lease_release` has no generation check against fd reuse after a
  foreign close; `wakeups_max` exhaustion returns `WouldBlock`; `wait_err` switches still use `else`.
- Next: FEATURE, item 8 (`batchAwaitAsync`/`batchAwaitConcurrent`/`batchCancel` in `submit.zig`); brief the
  developer narrowly, item 7 took a full cycle. Streak 0.
- Blockers: none. Open questions: none.
- Gotchas: never `until ...; pgrep` wait loops in Bash (30 s cap moves them to background); wait for the
  agent notification instead. The ready/merge pair must be two commands.

## Cycle 59 — 2026-10-19 — FEATURE
- Inbox: milestone #46 open, no OWNER comments (only our own), no bugs, CI green, no plan PR.
- Done: item 7 implemented and pushed as DRAFT PR #54 (`feat/operate-poller`, 7904917):
  `src/submit.zig` serves `net_receive` and non-blocking `file_read/write_streaming` on the poller;
  non-blocking files are leased into the registry per call (refcount, counts against `sockets_max`);
  ADR 0003 section 2b; tests in `tests/parity/operate.zig` + `operate_files.zig`; `operate` moved to
  `divergent` in `slots.zig`. Local `zig build test` (Debug/ReleaseSafe/ReleaseFast), `tidy`, `fmt`
  green; x86_64-linux compiles. Item 7 NOT ticked yet (not merged).
- Not done: no reviewer run, CI not awaited. The subagent took 18.7 min of the 22-min budget, so
  the cycle ended at the PR. Draft keeps the inbox from auto-merging an unreviewed PR.
- Next: FEATURE. Run `/review` on #54, fix findings, `gh pr ready`, wait for CI (epoll path has only
  been compile-checked; ubuntu is its first run), merge, tick item 7 on #46 and in the plan. Then item 8.
  Check `Io.Threaded` `device_io_control` FIONREAD on a pipe (-ENOTTY in ReleaseSafe, macOS arm64;
  positive path untested).
- Blockers: none. Open questions: none. Streak 0.
- Gotchas: a single zig-developer call for tests+impl of an item this size ran 18.7 min and ~$3.1;
  brief future agents with a narrower scope (e.g. net_receive first) or split item 7/8 over two cycles.

## Cycle 58 — 2026-10-18 — STABILIZATION
- Inbox: bug #52 (OWNER account), milestone #46 open, no plan PR, CI green; the only new comment was ours.
- Done: #52 fixed via PR #53 (2b63d9b, CI green macOS + ubuntu + 6 cross, `auto-merged`). Root cause was a
  test race, not a runtime bug: a late ACK woke the parked writer, `write_until_error` then made a fresh
  `netWrite` after the closer had removed the handle from the registry, so it routed as foreign into
  `Io.Threaded` (BADF). A call that starts after a close is a caller bug (now stated in `net_data.zig`
  header). The test joins the closer before the carrier runs (carrier only runs inside `await`), so the
  close always lands on a parked writer. Issue closed by the merge.
- Tiger Style spot check: `catch unreachable` 3 (all with proof comments), `while (true)` 1, largest file
  697 lines. STATE.md refreshed.
- Next: FEATURE, milestone 004 item 7 (`operate` on the poller: `net_receive`, non-blocking file streams);
  #49 follow-ups still open. Streak 0.
- Blockers: none. Open questions: none.
- Gotchas: `zig build test` re-runs are cached, so a loop of identical runs under load tests nothing after
  the first; change an input or use `--summary all` with `-Dno-cache`-style invalidation. Cycle cost ~$0.7.

## History (cycles 56-57, condensed 2026-10-19)

Cycle 57 (10-18): item 6 via PR #51: `src/backend/epoll.zig` (table is the truth, kernel entry
re-derived because EPOLLONESHOT disables the whole per-fd entry; eventfd wake; ms-rounded timeout),
`.auto` -> `.epoll` on Linux, ADR 0003 section 2a. Opened bug #52 (fixed in cycle 58). Gotchas:
`zig build test -Dtarget=x86_64-linux-gnu` compiles every Linux test binary though the host cannot
run them (the "unable to execute" lines are expected); riscv64 `fiber_switch.zig` fails to build
(naked fn safety check), not in CI; BSD `sed` rejects `\n`, use python for edits.

Cycle 56 (10-17): item 5 via PR #50: `src/net_data.zig` (netRead/netWrite/netSend/netShutdown).
Interrupted tree preserved as `wip/feat-net-data-path-slots-20261017` (do not delete; older
`wip/feat-native-net-data-path-*` and `feat/native-net-data-path` are kept too). Always grep
build.zig for a leftover `.filters` before trusting a wip tree (the parity step ran ONE test).
`Registry.count()` read undefined on a disabled registry (returns 0 now). Leftovers: comptime check
on `data_fail`'s `closed` arg, `setsockopt` asserts in test helpers, foreign-handle test strength,
#49 follow-ups (blocking accept infinite poll, registry spin-lock bound, `catch unreachable` at
net_registry.zig:160, errno gaps). The guard blocks a ready-and-merge pair in one command.

## History (cycles 49-55, condensed 2026-10-19)

Cycle 55 (10-15): re-reviewed #49, CRITICAL = a cancel arriving after a readiness wake was lost; fix
`park` calls `task_acknowledge_cancel` first, `close_on_carrier` returns bool. Wake order is
most-recent-joiner first. Cycle 54: item 4 as draft PR #49 (sys.zig, net.zig registry, sched_io.zig
poller dispatch); too big for one cycle with a fix round (~$2.6); draft status keeps the inbox from
auto-merging a PR with open CRITICALs. Cycle 53: item 3 via PR #48 (`sockets_max` required,
`.auto` -> `.kqueue` on Darwin, parity suite per backend); gate 7 on kqueue p50 0.31 ms / p99
0.39 ms. Cycle 52 (10-13): plan 004 merged, milestone #46; item 2 via PR #47 (ADR 0003, `poller.zig`,
`kqueue.zig`; `init(target, gpa, options)`, relative `wait(timeout_ns, out)`). One subagent for
tests+impl is cheaper than architect + two agents. Cycles 49-51: plan 004 proposed as PR #44 (12
items, v0.5.0 MINOR); PR #45 split `src/sched.zig` tests. Gotchas: a hanging `zig build test`:
python subprocess timeout then `pkill -f .zig-cache`; no `stabilize` label in the repo; the guard
blocks compound Bash (`cd <repo>;`, citadel paths): run commands alone, use Read/Write/Edit.

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
