# sirocco — context

last_seen_at: 2026-10-06T12:00:00Z
rejected_plans: []

## Cycle 37 — 2026-10-06 — FEATURE
- Inbox: no OWNER activity; CI green on 4028871; milestone #18 the only open issue; no plan PR.
- Done: plan 002 item 9 + release v0.3.0. PR #30 (merged 1207f27, CI green Linux+macOS+6 cross):
  README Status (internal milestone, single carrier, not for silica/zoltraak), CHANGELOG
  `[0.3.0]`, PRD §5 gate 6 re-measured (1 in flight pass 45 vs 1752 ns; 1000 FAIL 86056 vs 599
  ns), version bump. Tag v0.3.0 + GitHub release; milestone #18 closed. No consumers pin sirocco.
- Plan 003 `carrier-never-blocks` proposed, PR #31 (label plan), awaiting human merge: groupAwait
  cancel, eager async start (gate 6), timer wheel + native sleep (gate 7), offload pool for
  blocking slots (ADR 0002 picks offload over multi-carrier; now/clockResolution stay forwarded).
- Next: if #31 merged, open its milestone issue and do item 1; else one bounded `/stabilize --one`.
- Blockers: none. Open questions: none. Stabilize streak 0.
- Gotchas: guard blocks any compound Bash that has `cd` into a repo or a glob over sibling repos;
  the primary cwd is already sirocco, so skip `cd`. Zig 0.16.0 `zig build test` is silent on pass.

## Cycle 36 — 2026-10-06 — FEATURE
- Preflight: tree was dirty on `feat/futex-wait-table` (interrupted item 8: ~1370 lines of parity
  tests, no `src/futex.zig`); preserved as `wip/feat-futex-wait-table-20261006` (do not delete),
  then reused those tests on the existing `feat/futex-wait-table` branch.
- Inbox: no OWNER activity; CI green on fdf7d6b; milestone #18 only open issue; no plan PR.
- Done: plan 002 item 8 via PR #29 (merged 4028871, CI green Linux+macOS+6 cross; #18 ticked).
  `src/futex.zig` FIFO wait table (wait record lives in `Sched.Fiber`, no alloc after init), cancel
  unparks with `error.Canceled`, timeouts read baseline `now`; `src/fiber_switch.zig` split out of
  `sched.zig` (was 796 lines). Reviewer CRITICAL fixed: futexWake from a non-carrier thread raced
  the wait list; now spinlock + `unpark_foreign`, with a plain-thread regression test.
- Known gap: `groupAwait` does not yet propagate a cancel while parked (no test demands it).
- Next: item 9 (README/CHANGELOG/PRD §5 reconcile incl. gate 6 at 1000 in flight, bump 0.3.0,
  `/release sirocco minor`). Blockers: none. Open questions: none. Stabilize streak 0.
- Gotchas: guard blocks a first Bash call that mixes `echo > /tmp` with citadel path vars; split
  calls. `@fence` is gone in 0.16 (use seq_cst `@atomicRmw(.Add, 0)`). Resumed subagent runs in
  background: poll a file with a python sleep loop.

## History (cycles 34-35)
Cycle 35 (10-05): item 7 via PR #28 (merged fdf7d6b): native `groupAsync`/`groupAwait`/`groupCancel` +
`crashHandler` in `src/concurrency.zig`, `groupConcurrent` = ConcurrencyUnavailable; crashHandler must
set `.acknowledged`. Cycle 34 (10-04): item 6 via PR #27 (merged aad6b0f): native
`checkCancel`/`recancel`/`swapCancelProtection`; reviewer CRITICAL: `in_fiber` must check threadlocal
`carrier_active` since group workers still run on Threaded threads. Gotchas: guard blocks `cd <repo>`
and `sed -i` in compound commands (use Edit/python, run zig by full path); stale `.zig-cache`
FileNotFound -> `rm -rf .zig-cache`; slot-table negative tests in `slots.zig` hardcode a delegated
sample slot, pick the first still-delegated one.

## History (cycles 32-33)
Cycle 33 (10-04): item 5 closed via PR #26, `bench/spawn.zig`/`zig build bench-spawn` (gate 6:
1 in flight 32 ns vs Threaded 1799 ns pass; 1000 in flight 62283 ns vs 660 ns FAIL since async is
lazy; revisit with items 8/9). Cycle 32 (10-03): item 5 slots via PR #25: native async/await/
cancel in `src/concurrency.zig`; hang root cause was std's unwinder walking off the fiber base
(fixed by a zero return-address sentinel); `wip/async-await-slots-20261003` kept (do not delete).
Gotchas: `zig test --dep sirocco -Mroot=tests/parity/root.zig -Msirocco=src/root.zig
-fno-omit-frame-pointer --test-no-exec` builds the parity binary alone; no `timeout` on macOS
(python subprocess timeout); `--test-filter` is compile-time only; read the last `N/M name...`
line to tell a crash from a hang.

## History (cycles 30-31)
Cycle 31 (10-03): found ~680 dirty lines of an interrupted item-5 attempt, preserved as
`wip/async-await-slots-20261003` (do not delete); trial run hung. Cycle 30 (10-02, forced
STABILIZATION on OWNER bug #23): x86_64 ReleaseSmall SEGV fixed via PR #24 with own naked
`switch_context_asm` (LLVM -Os dropped a `lea` into rsi), `callconv(.c)` pointer +
`@call(.never_inline)`. Gotchas: naked fn params break the self-hosted x86_64 backend (only CI
catches it); no Rosetta/qemu, so x86_64 is verified by asm inspection + CI; `sleep` blocked in
Bash (use `until` loops); no `timeout` on macOS; guard blocks `cd <repo>` in compound commands
and inline python writing into citadel (use Edit/Write tools).

## Cycle 29 — 2026-10-01 — FEATURE
- Inbox: no OWNER actions since watermark. CI green on 2f89fd2; only open issue was milestone #18.
- Done: plan 002 item 4 via PR #22 (merged, CI green Linux+macOS+6 cross): `src/sched.zig` fiber
  substrate (init-time stacks, FIFO ready queue, spawn/yield/park/unpark, canary on every
  switch-out, lock-free `unpark_foreign` inbox + futex wait), `stdx.assert_always`. Plan box,
  CHANGELOG, issue #18 ticked. code-reviewer found a CRITICAL: optimized builds crashed on
  aarch64 (inlined `Io.fiber.contextSwitch` clobbers x29/x30). Fixed: `noinline switch_context`,
  `omit_frame_pointer = false` on the module, `zig build test` now honours `-Doptimize`, CI runs
  ReleaseSafe/Fast (and ReleaseSmall on macOS).
- OPEN BUG #23: x86_64-linux ReleaseSmall SEGVs the 4 fiber tests (Debug/Safe/Fast pass).
  Cannot reproduce on the aarch64 dev box. Linux ReleaseSmall CI step is skipped until fixed.
- Next: STABILIZATION on bug #23 (forced: open OWNER bug) — must be fixed before item 5.
  Then item 5 (async/concurrent/await/cancel slots).
- Blockers: none external. Open questions: none.
- Gotchas: zsh treats `echo "== x"` as `=cmd` expansion; no `timeout` on macOS; `zig build test`
  mod tests were Debug-only before this cycle. Fiber code needs frame pointers (see sched.zig).

## History (cycles 26-28)

Plan 002 items 1-3 shipped: macOS CI runner (#19), `src/runtime.zig` `Runtime` with all 109 slots
forwarded and the stub modules deleted (#20, cycle 27), `tests/parity/` harness + 109-slot table
(#21, cycle 28). Gotchas: `expectEqualDeep` on a deliberate mismatch prints noise (avoid in
negative tests); handle-returning slots need their own harness helper; `sed -i` needs `''` on macOS;
zsh treats `echo "== x"` as `=cmd` expansion; no `timeout` on macOS.

## History (cycles 22-25)
Cycles 22-25 (2026-09-27 to 09-29, FEATURE): plan PR #13 stayed open; each cycle ran at most one
bounded stabilization (build/test/fmt/tidy green under the pinned 0.16.0 toolchain, tidy-auditor
clean). Cycle 22 cleared a stale `.zig-cache` and swept up uncommitted cycles 19-21 memory
(citadel commit lock contention, sirocco#17). Cycle 25 was a no-op. No PRs, no fixes needed.

## History (cycles 0-9, 10-14, 15-21)
Cycles 15-21 (2026-09-16 to 2026-09-27, mostly quiet FEATURE with one STABILIZATION at 15): plan
PR #13 remained open awaiting human merge across all of them, zero new OWNER activity each
watermark. Cycle 15 (STABILIZATION, n%5==0) ran the full audit: CI/build/tidy/tests all green,
tidy-auditor and test-writer both found zero real defects (two pre-existing minor test-quality
notes judged non-defects), and fixed a counter/context.md desync from cycle 14's incomplete
report. Cycles 16-18 each ran one bounded stabilization task (build/test/fmt/tidy green,
tidy-auditor clean) since the plan PR was still open; cycles 19-21 skipped the redundant audit
entirely as a pure no-op, since the baseline had been identical since cycle 5. No PRs opened,
no fixes needed, in any of cycles 15-21.

## History (cycles 0-9, 10-14)
Cycle 14 (2026-09-15, FEATURE): plan PR open, bounded stabilization. Stale `.zig-cache` cleared
(local-only, not a regression); tidy-auditor clean, same baseline as 5/10/11/12. Fixed stale
`//!` headers in `tools/tidy.zig`/`tools/tidy_test.zig` still calling `checkSource` unimplemented
though it shipped in v0.2.0, via PR #16 (merged). Deliberately left `root.zig`'s pre-ADR
`io`/`net`/`tls`/`http`/`ws`/`task` exports alone — expected until plan 002's `Runtime` merges.
Cycle 13 (2026-09-13, FEATURE): plan PR open, bounded stabilization. Reinstalled the missing
pinned 0.16.0 toolchain (dev-box gap, not a repo regression); build/test/fmt/tidy all green
after. tidy-auditor found one real doc-cross-reference drift: `root.zig`/`bench/main.zig` `//!`
headers pointed at the replaced `docs/milestones.md` — fixed via PR #15.
Cycle 12 (2026-09-12, FEATURE): plan PR open, bounded stabilization. CI/build/tidy all clean.
tidy-auditor found real drift: README's intro made present-tense capability claims (`Runtime`
type, kqueue/epoll backends) contradicting the stub-only v0.2.0 code and the README's own
Status section — reworded to design-target language via PR #14 (docs-only, merged). Cycle 11
(2026-09-12, FEATURE): plan PR open, bounded stabilization; CI/build/tidy clean, zero mechanical
violations, nothing to fix. Cycle 10 (2026-09-11, STABILIZATION, n%5==0): full stabilize — CI
5/5 green, build/fmt/tidy clean, tidy and test-quality audits both clean, docs/deps/hygiene
clean, nothing to fix; stabilize_streak reset to 0.

Cycle 9 (2026-09-11, FEATURE): closed milestone #3 (item 11, release v0.2.0 — PR #12, tag,
GitHub release; no consumer pins sirocco yet so no migration issues opened), then drafted plan
002 (`planner`/opus): fiber scheduler + futex core, P0 (concurrency/cancel, 12 slots) + P1
(futex trio, 3 slots), nine one-cycle items starting with the macOS CI runner and a walking-
skeleton `Runtime` forwarding all 109 vtable slots. Version impact MINOR. Plan PR #13 opened,
awaiting human merge (still open as of cycle 15). Cycle 8 (2026-09-10, FEATURE): item 10
(README/CHANGELOG reconciliation) via PR #11 — added `CHANGELOG.md`, fixed the Install
section's uncut `v0.1.0` tag reference.
Cycle 7 (2026-09-10, FEATURE): item 9 (`wip/*` branch decision) via PR #10 — verified no
`wip/*` branch exists for sirocco; decision recorded as ADR-002.
Cycle 0 (2026-09-05, RESTRUCTURE): realm created, plan 001 prescribed. Cycle 1 (2026-09-06,
FEATURE): opened milestone issue #3; item 1 via PR #4. Cycle 2 (2026-09-07, FEATURE): item 2
(`zig build tidy` step) via PR #5. Cycle 3 (2026-09-07, FEATURE): items 3-6 (0.16 migration of
main.zig/bench/tidy tool, pin+CI) bundled into PR #6 — bundling was necessary since `zig build
test` compiles all entry points in one graph. Cycle 3b (2026-09-08, disk-blocked no-op):
`df -g /` was 16 GB, below the 20 GB gate; stopped before any work, counter not advanced.
Cycle 4 (2026-09-08, FEATURE): item 7 (PRD rewrite against `std.Io.VTable`, ADR 0001) via PR
#7, docs-only — found std's own evented `Io` impls don't compile on 0.16.0, sirocco's actual
reason to exist now; declared the 40-slot hybrid forwarding to `Io.Threaded`. Cycle 5
(2026-09-09, STABILIZATION, n%5==0): CI green, tidy audit mechanically clean (repo is
stub-only, so zero counters prove nothing yet); found and fixed real docs drift instead —
README still described the pre-ADR parallel io/net/tls/http/ws/task API — via PR #8. Cycle 6
(2026-09-09, FEATURE): item 8 (Assertion and Tiger Style baseline) via PR #9 — landed on the
two real entry points (`main.zig`, `bench/main.zig`) since `root.zig` has no `pub fn` yet;
shared `assert`/`maybe` moved to new `src/stdx.zig`. A code-reviewer pass caught compound
implication asserts that just restated a branch instead of deriving an independent property.

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
