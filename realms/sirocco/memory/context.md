# sirocco — context

last_seen_at: 2026-10-12T00:10:00Z
rejected_plans: []

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

## Cycle 48 — 2026-10-11 — FEATURE
- Inbox: no OWNER activity; CI green on 2e7dff5; no open PRs; milestone #33; no bugs.
- Done: plan 003 item 9 + release via PR #43 (merged f159a82, CI green, auto-merged): README,
  PRD §4.1/§4.3, CHANGELOG `[0.4.0]`, `build.zig.zon` and `sirocco.version` 0.4.0. Tagged and
  released v0.4.0, closed #33. No kingdom repo pins sirocco, so no migration issues.
- Known gap (deliberate): `src/sched.zig` is still 823 lines (800 target); `zig build tidy` passes
  as is. Splitting its tests needs pub accessors for private helpers; take it as a stabilize task.
- Next: plan 003 is done and fully checked, so the next FEATURE cycle runs `/plan sirocco` (kqueue /
  epoll backends, per ADR 0002: multi-carrier belongs with them; PRD gates 1-4 are the targets).
- Blockers: none. Open questions: none. Stabilize streak 0.

## Cycle 47 — 2026-10-11 — FEATURE
- Inbox: no OWNER activity; CI green on 9743796; no open PRs; milestone #33.
- Done: plan 003 item 8 via PR #42 (merged 2e7dff5, CI green Linux+macOS+6 cross, auto-merged):
  `src/offload_slots.zig` comptime thunks (arity 2-6, built from each VTable field type) route the
  blocking `dir*`/`file*`/`net*`/`operate`/`childWait` slots through the pool, `.forward` mode only
  (the thunks call the baseline). Pending cancel delivered before submit. Loopback accept+connect
  test (hung on v0.3.0), 1-worker sizing test, cancel/protection tests. Reviewer: 0 CRITICAL; 5
  WARNINGs fixed: closes/`netShutdown`/seeks/`fileUnlock` kept on the carrier (must not queue behind
  parked reads), memory-map create/resize/destroy kept (shared `gpa`), `netWriteFile` and
  `netLookup` kept (std TODO panic; queue woken via baseline futex). `Runtime.init` gpa must be
  thread-safe. Plan item and #33 ticked in the PR/issue.
- Next: item 9 (README drop "stalls every fiber", CHANGELOG, PRD §4.1/§4.3/§5, v0.4.0 via
  `/release`, split `src/sched.zig` tests: 823 lines > 800 cap). Then plan 003 is fully checked.
- Blockers: none. Open questions: none. Stabilize streak 0.
- Gotchas: `build test` printed exit 0 once with a line over 100 cols in src/ (tidy test stale
  cache); run `zig build tidy` explicitly and `rm -rf .zig-cache` when in doubt. BSD `sed -i` needs
  an empty suffix arg. `gh pr checks` right after a push still shows the previous run: poll
  `gh run list` by headSha. Guard blocks any compound Bash mentioning citadel paths.

## Cycle 46 — 2026-10-11 — FEATURE
- Inbox: no OWNER activity; CI green on 28ef526 (b812d61 is docs-only); no open PRs; milestone #33.
- Done: plan 003 item 7 via PR #41 (merged 9743796, CI green Linux+macOS+6 cross, auto-merged):
  `src/offload.zig` bounded worker pool (request records on the parked fiber's stack, futex mutex,
  completion via `Sched.unpark_foreign`), `Runtime.Options.offload_threads` (required, breaking in
  0.x), pool built beside the sched in `sched_ensure` (failure -> `.unavailable`), ADR 0002
  (offload before multi-carrier; the human may reject the deferral on #33). Item ticked in plan
  and #33. Reviewer: 0 CRITICAL; fixed spinlock -> futex mutex, timing test -> in-flight peak.
- Next: item 8 (comptime thunks route `dir*`/`file*`/`net*`/`operate`/`childWait` through the
  pool in `runtime.zig`; loopback accept/connect test; in-fiber parity), item 9 (docs, v0.4.0,
  split `src/sched.zig` tests: 823 lines > 800 cap).
- Blockers: none. Open questions: none. Stabilize streak 0.
- Gotchas: `Io.sleep` on `Io.Threaded` did not overlap (16 x 20 ms took 160 ms, cause not
  investigated; may explain the slow Threaded row in gate 7): use `futexWaitTimeout` on a private
  word as a timer in concurrency tests. Parity test alloc counts shifted by one (pool block).
  Guard blocks compound Bash that writes under citadel paths (first Bash call of the cycle).

## Cycle 45 — 2026-10-10 — FEATURE
- Inbox: no OWNER activity; CI green on 94c0627; no open PRs; milestone #33 open.
- Done: plan 003 item 6 via PR #39 (merged 28ef526, CI green Linux+macOS+6 cross, auto-merged):
  `harness.expectSameResultInFiber` runs the `rt.io()` side in an `async` task, baseline stays
  off-fiber; tests prove the native side is in a fiber (`rt.sched.in_fiber()` counter) and that
  mismatches are still caught; `dir`, `time`, `futex` tables run in both placements. Tick of plan
  item 6 via docs PR #40 (b812d61); #33 ticked.
- Next: item 7 (ADR 0002 + `src/offload.zig`), 8, 9 (docs, v0.4.0). `src/sched.zig` is 823 lines
  (cap 800): split its tests in item 9.
- Blockers: none. Open questions: none. Stabilize streak 0.
- Gotchas: CI ignores `docs/**` and `*.md` (paths-ignore), so docs-only PRs have no checks; a poll
  loop on `gh pr checks` spun until the 600 s tool limit. Tick plan items inside the
  implementation PR itself to avoid a second PR. The guard also blocks compound Bash that writes
  citadel files (python heredoc): use Write/Edit.

## History (cycles 43-44, condensed 2026-10-12)

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
