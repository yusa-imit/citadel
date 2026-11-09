# sirocco — context

last_seen_at: 2026-11-09T02:00:00Z
rejected_plans: []

## Cycle 87 — 2026-11-09 — FEATURE
- Preflight: disk 21 GB, CI green, no bugs, no plan PR, inbox empty (milestone #62 open).
- Merged #82 (`test/parity-four-carriers`, labelled auto-merged): `build.zig` builds the parity suite at
  carriers 1, 2 and 4 (was 1, 2); no test needed a change, 196/196 per binary, tidy+fmt clean. 40 serial
  runs per binary: only the known "64 idle sockets" flake (`expected 64, found 63` / std `Io.Batch`
  union panic). CI macOS 6 min, Ubuntu ~12 min.
- Item 7 stays UNCHECKED. Remaining: model for await and group waits, group cancel from another carrier
  (cancel mail per member), awaiter on a peer, atomic `run_until` stop flag, 1000 serial runs.
- Gotchas: a bare `python3 -I -` in Bash waits on stdin and hangs the call (never write it); heredoc
  scripts to /tmp must be written in their own call; `sed -i ''` worked on build.zig and citadel files.
  ~21 min wall (CI wait dominates), ~$0.55, no subagent.
- Next: cycle 88: model test for await/group waits across peers, or group cancel from another carrier.

## Cycle 86 — 2026-11-09 — FEATURE
- Preflight: disk 25 GB, CI green, no bugs, no plan PR, inbox empty.
- Merged #81 (`test/futex-model-peers`, labelled auto-merged): `src/futex_model_peers_test.zig`, a seeded
  4-carrier model of futex wake and cancel (16 fixed seeds; up to 24 waiters homed on peers 1..3 over
  3 words; released from the test thread or a fiber mailed to a peer, or canceled on their home; the
  plan is the reference model: outcome, wake count per word, resumed on home). 880/967, tidy+fmt clean,
  200 serial runs of the library binary clean. Passed first run (pins existing behavior).
- Item 7 stays UNCHECKED. Remaining: model for await and group waits, group cancel from another carrier
  (cancel mail per member), awaiter on a peer, atomic `run_until` stop flag, parity at 4 carriers,
  1000 serial runs.
- Gotchas: the guard blocks compound `cd repo; ...` Bash (use `git -C` or absolute paths); a nohup
  stress script in /tmp works; the library test binary (156 tests) is found by running the newest
  `.zig-cache/o/*/test` candidates. ~12 min, ~$0.65, no subagent.
- Next: cycle 87: parity suite at 4 carriers, then the await/group model.

## Cycle 85 — 2026-11-08 — FEATURE
- Preflight: disk 24 GB, CI green, no bugs, no plan PR, inbox empty (periodic stabilization off).
- Merged #80 (`feat/group-lock`, labelled auto-merged): `GroupRec.lock` spinlock (`rec_acquire`,
  `rec_release`, `rec_link`, `rec_take_waiter`, `rec_is_idle`) over list/pending/idle/waiter; a
  member can end on a peer, the last one wakes the awaiter via `join.wake_fiber`; `group_park`
  rechecks `idle` and registers the waiter under the lock. `src/group_peer_test.zig`: 24 hand-made
  members on peers 1..3 (seeded yields), plus an awaiter fiber on carrier 0 woken by a peer. 878/965,
  tidy+fmt clean, 200 serial runs of the library binary clean.
- Item 7 stays UNCHECKED. Remaining: group cancel from another carrier (needs cancel mail per
  member; `group_request_cancel` asserts members are on the awaiter's carrier), awaiter on a peer
  (`current_task`/`slot_group_await` still assume carrier 0), atomic `run_until` stop flag, seeded
  4-carrier model test, parity at 4 carriers, 1000 serial runs.
- Gotchas: tidy wants lowercase `proof` in a `catch unreachable` comment (same/prev line); a hand-made
  GroupRec passed to `groupAwait` must be heap-allocated with `rt.threaded.allocator` (it is freed);
  `groupAwait` frees the rec, so do not read it after. `sed -i ''` was allowed by the guard this time.
  Done in ~15 min, ~$1.1, no subagent.
- Next: cycle 86: the seeded 4-carrier model test (futex wake/cancel/await/group across peers), then
  parity at 4 carriers and the 1000-run stress; group cancel from another carrier with item 8.

## Cycle 84 — 2026-11-08 — FEATURE
- Preflight: disk exactly 20 GB (gate >= 20; two disk-blocked no-ops on 11-07 at 17-18 GB did not
  advance the counter), CI green, no bugs, no plan PR, inbox empty (only the AI's own comment).
- Merged #79 (`test/close-from-peer-carrier`, labelled auto-merged): `src/net_close_peer_test.zig`,
  two tests: a fiber mailed to peer 1 closes a listener with an accept parked on carrier 0 (waiter
  wakes `.closing`, last waiter closes the fd), and a close with no waiter frees the slot. No source
  change: `close_registered` uses `rt.sched.in_fiber()` which is false on a peer thread, so it already
  takes `close_off_carrier`; only carrier 0 arms the poller until item 8 placement. 876/963, tidy+fmt
  clean, 150 serial runs of the library binary clean (parity binary still has the known 64-idle flake).
- Item 7 stays UNCHECKED. Remaining: `GroupRec` lock/join + group cancel from another carrier, atomic
  `run_until` stop flag, seeded 4-carrier model test, parity at 4 carriers, 1000 serial runs. The
  per-slot lock + armed mask (ADR 0004 section 4) is only needed once item 8 places sockets on peers.
- Gotchas: `Registry` is built by the first `io()`, so check `rt.sockets.enabled()` after `io()`
  (before it the tests silently skipped; compare pass vs total in the summary). Stale `.zig-cache`
  gave `failed to spawn build runner` again. A one-off `nohup` stress script in /tmp works.
  Done in ~10 min, ~$0.85, no subagent.
- Next: cycle 85: `GroupRec` lock + join + group cancel from another carrier (tests first), then the
  seeded 4-carrier model test.

## Cycles 79-83 (2026-11-04..06), folded 2026-11-09: plan 005 item 7 (multi-carrier join/cancel)

- Merged: #73 mailbox, #74 `Table.wake` (resumes each claimed waiter on `fiber.home`: direct if
  `home.in_fiber()`, else `home.unpark_foreign`), #75 futex timeout/cancel claim on home, #76 wake/timeout
  race tests (two tests in `futex_home_test.zig`, order made deterministic by mailing a fiber to the home
  carrier), #77 `src/join.zig` (running/done/driver/`*Fiber` atomic word; `Task.join` + `driver_stop`;
  `task_publish` wakes the awaiter on `fiber.home`), #78 `src/cancel_mail.zig` (`Slot`, `is_remote`,
  `request`, `settle`, handler fiber on the home; `Task.rt` + `Task.cancel_slot`; `join.wake_fiber`;
  `task_publish` no longer reads the record after waking the awaiter). ADR 0004 "as built": the cancel
  flag stays home-owned, the canceller is the UAF guard.
- Item 7 stays UNCHECKED. Remaining: `GroupRec` join + lock + group cancel from another carrier, close
  from another carrier (registry `close_locked` + armed mask), seeded 4-carrier model test, parity at 4
  carriers, 1000 serial runs. `task_finish` still asserts `task.sched == &rt.sched`; await from other
  carriers waits for item 8. Nothing places tasks on peers yet, so cross-carrier await/cancel is tested
  with mailed fibers only.
- Gotchas: futex slots (`slot_futex_wait` etc.) still use `rt.sched` (carrier 0), so running tasks on
  peers needs them generalized to `Sched.here()` (item 8); `run_until` returns at once when the carrier
  has no live fiber (sleep in the baseline futex instead of waiting on carrier 0); a main-CI "failure"
  with the macOS job "not acquired by Runner" and no steps is runner capacity, `gh run rerun <id>
  --failed`; known flake: parity "64 idle sockets" (`expected 64, found 63`, or a panic in std
  `Io.Batch.cancel`); the newest `.zig-cache/o/*/test` is often the 196-test parity binary, the library
  binary has ~140; a 300-run loop overruns Bash (nohup + file); in `python3 -c "..."` backticks are
  shell-expanded (use a file); the guard blocks `cd <repo> && ...` compounds and `sed -i ''` (use
  `git -C` and Edit); `lldb` is allowed but hangs (bisect instead); CI Build & Test ~11 min after a
  ~2 min queue, push once.

## History (cycles 0-77, folded 2026-11-05)

- 80 (11-05): #75 futex timeout/cancel claim on the home carrier: `Table.timeout`/`cancel_wait` end the wait
  with `assert_always(Sched.claim(..))` AFTER `table.remove` (`remove` asserts outcome `.waiting`).
  macOS runner capacity can end CI "cancelled" with no steps: rerun failed jobs, not a code bug.
- 0-36 (09-05..10-06): realm created, `zig build tidy` (PR #5), 0.16 migration in PR #6, PRD against
  `std.Io.VTable` (ADR 0001: std's evented `Io` impls do not compile on 0.16.0, so sirocco forwards to
  `Io.Threaded`), shared `assert`/`maybe` in `src/stdx.zig`, v0.2.0 (PR #12). Plan PR #13 sat open without
  OWNER activity. macOS CI (#19), `Runtime` forwarding 109 slots (#20), parity harness (#21), fiber
  substrate (#22). CRITICAL: optimized aarch64 crashed (inlined context switch clobbers x29/x30):
  `noinline switch_context`; x86_64 ReleaseSmall SEGV (bug #23, PR #24): own naked `switch_context_asm`
  (no Rosetta/qemu, verify by asm inspection + CI). Native async/await/cancel (#25; zero return-address
  sentinel), `bench/spawn.zig` (#26), cancel trio (#27), group slots (#28), `src/futex.zig` (#29;
  non-carrier `futexWake` needs a spinlock + `unpark_foreign`).
- 37-48: plan 002 item 9 + v0.3.0 (#30); plan 003 (#31-#43), v0.4.0 (#43). `groupAwait` honors a cancel
  while parked (#34); eager `async` (`Sched.spawn_first`, #35; gate 6: 44 vs 1796 ns @1); `src/timer.zig`
  4x64-slot hierarchical wheel, 131 us tick (#36); native `sleep` (#37; a woken futex waiter keeps its wheel
  node: assert `.parked` only behind `outcome == .waiting` under the table lock); `bench/timer.zig` gate 7
  (p50 311 us vs 7.32 ms); `src/offload.zig` bounded worker pool (ADR 0002; `Io.sleep` on `Io.Threaded`
  did not overlap, use `futexWaitTimeout` as a timer in tests); `src/offload_slots.zig` comptime thunks
  (`Runtime.init` gpa must be thread-safe).
- 49-61: plan 004 (evented net, PR #44): ADR 0003 + `poller.zig` + `kqueue.zig` (#47; `init(target, gpa,
  options)`, relative `wait(timeout_ns, out)`), `sockets_max` required, `.auto` -> `.kqueue` on Darwin
  (#48), sys.zig + net registry (#49; a cancel after a readiness wake was lost, `park` now calls
  `task_acknowledge_cancel` first; draft status keeps the inbox from auto-merging with open CRITICALs),
  `src/net_data.zig` (#50), `epoll.zig` (#51; EPOLLONESHOT disables the whole per-fd entry), `src/
  submit.zig` (#54), `src/batch.zig` native `batchAwait*/Cancel` (#55). Bug #52 (#53) a test race.
  Review leftovers: overflow worker has no cancel in `poll(2)`; no generation check on `lease_release`
  after a foreign close; blocking accept infinite poll; registry spin-lock bound. Std 0.16.0 bug:
  `Io.Threaded.batchAwaitConcurrent` leaves a ready `net_receive` on `submitted`.
- 62-68: #55 red CI was a test flaw (`Io.Threaded` rounds poll timeouts down; parity tests project to
  `timed_out` + `later_ok`); `concurrent`/`groupConcurrent` (#56; set `FailingAllocator` `fail_index =
  alloc_index` after `io()`; no test cancels a parked `concurrent` future); `bench/echo.zig` (#57: gate 2
  PASS 0.91x, gate 1 MISS 0.83-0.87x); bug #58 (#59) was not a runtime bug: 10000 clients closing first
  exhaust macOS's 16384 ephemeral ports (clients close with `SO_LINGER` 0); gate 3 PASS 7/8, gate 4 MISS
  29.2 KB vs 24.7 KB per task; v0.5.0 (#60; item 8b moved to plan 005); plan 005 "net-gates" (#61,
  v0.6.0). `bench-latency` needs python `setrlimit(30000)` (the `zig build` child has a 10240 NOFILE cap);
  killed bench runs leave sockets that fail the next run for ~30 s; bench stdout is buffered.
- 69-77 (10-27..11-03): plan 005 milestone #62. Item 1 profile (#66; `src/profile.zig` only when the root
  declares `sirocco_profile`; 78% of CPU in the kernel, so multi-carrier stays; no usable profiler on this
  box, `sample(1)` and lldb attach hang); question #63 closed unanswered, option (c). Item 3 (#64) split
  `sched_fiber.zig`/`concurrency_group.zig`; item 11 (#65): sockets made off a fiber are not registered,
  make the pair via `io.concurrent(connect_pair)` and use `net_data.init_rt()`; item 2 ADR 0004
  multi-carrier (#67; `Options.carriers` required, `carriers_max` 64, one futex table, one shared registry,
  no work stealing, `5N+4` blocks evented; architect/opus 12 min / ~$1.5, brief narrower, output arrives
  HTML-escaped); item 4 (#68) `src/waiter.zig` registry waiter lists (open SUGGESTIONs: `waiter_remove`
  asserts nothing, tests for cancel head/tail, `.gone`, node re-entry); item 5 (#69) `batch_park.zig`/
  `batch_sweep.zig` (`ops_max` 128; flaky ~1/40 "64 idle sockets wake the batch" panics in std
  `Io.Batch.cancel` on the baseline side; no end-to-end foreign-close race test); item 6 (#70)
  `Options.carriers`, `src/carriers.zig`, `Sched.notify`, parity suite at 1 and 2 carriers (open: `.auto`
  not swept under a failing allocator, no spawn-failure unwind seam); item 6 gate 7 on 2 carriers p99
  316792 ns vs 8.01 ms (#71); item 7 first steps (#72): `Sched.index`, `Fiber.home`, threadlocal
  `Sched.here()` (a `Fiber` literal in tests needs `.home`). Item 78: `src/mail.zig` (#73; `outstanding_max`
  65536; mail to a `run`-only carrier can be stranded; serve drops mail left at stop). Kept `wip/*`:
  `feat-net-data-path-slots-20261017`, `feat-native-net-data-path-*`, `async-await-slots-20261003`,
  `feat-futex-wait-table-20261006`, `feat-latency-bench-20261026`, `fix-leftovers-plan-005-20261029`,
  `feat-batch-waiter-plumbing-20261101`. Disk-blocked no-ops (< 20 GB) do not advance the counter.
- Gotchas: tidy flags `std.time.` in src and bench/ lines > 100 cols, so run `zig build tidy` explicitly
  (a stale cache hid one; stale `.zig-cache` -> `rm -rf .zig-cache`); `zig build test` re-runs are cached,
  stress the built `.zig-cache/o/*/test` serially; `-Dtarget=x86_64-linux-gnu` compiles Linux tests
  ("unable to execute" expected); riscv64 `fiber_switch.zig` does not build (not in CI); `@fence` is gone
  in 0.16; naked fn params break the self-hosted x86_64 backend (only CI catches it); `--test-filter` is
  compile-time only; BSD `sed` rejects multi-line patterns (use Edit); no `timeout`/`sleep` in Bash (python
  subprocess timeout, `until` loops); `gh run watch`/`pr checks --watch` over 8-9 min hits the Bash
  timeout; a second push cancels the first CI run (poll `gh run list` by headSha); CI ignores `docs/**`
  and `*.md`, so tick plan items inside the implementation PR; after a squash-merge cherry-pick follow-ups
  onto a fresh branch from origin/main; `gh pr create` can hit a transient GraphQL 500; the guard blocks
  `python3 - <<EOF`, compound `cd <repo>;`, mixing /tmp writes with citadel reads; one zig-developer call
  for tests+impl ~$3.1 (a call with explicit line ranges and verification commands did a split in ~$0.5);
  the architect agent has no Write tool; zsh expands `echo "== x"`.

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
