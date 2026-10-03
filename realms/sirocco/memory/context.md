# sirocco — context

last_seen_at: 2026-10-04T00:00:00Z
rejected_plans: []

## Cycle 33 — 2026-10-04 — FEATURE
- Inbox: no OWNER activity; CI green on d312de3; milestone #18 only open issue.
- Done: plan 002 item 5 closed via PR #26 (merged 2f6c447, CI green Linux+macOS+6 cross):
  `bench/spawn.zig` / `zig build bench-spawn` (gate 6). Numbers (arm64 mac, ReleaseFast): 1 in
  flight sirocco 32 ns vs Threaded 1799 ns (pass); 1000 in flight 62283 ns vs 660 ns (FAIL: async
  is lazy, bodies start at first await). Recorded in PRD §5 table; tracking issue ticked.
- Next: item 6 (checkCancel/recancel/swapCancelProtection) + PR #25 review warnings (await outside
  a fiber -> run only until task done; checked adds in task_create; zero-size ctx/result tests;
  cancel-after-done). Revisit gate 6 at 1000 with items 8/9 (eager start or batch-aware).
- Blockers: none. Open questions: none. Stabilize streak 0.
- Gotchas: global `zig` is 0.15.2; use /Users/fn/.zr/toolchains/zig/0.16.0/zig by full path.
  No `timeout`/`sysctl` on this box. Skipped code-reviewer (bench-only change, tight budget).

## Cycle 32 — 2026-10-03 — FEATURE
- Inbox: no OWNER activity since watermark; CI green on edb1a36; milestone #18 only open issue.
- Done: plan 002 item 5 slots via PR #25 (merged d312de3, CI green Linux+macOS+6 cross):
  native `async`/`await`/`cancel` (`src/concurrency.zig`), `concurrent` = ConcurrencyUnavailable
  (divergence cited in slots.zig), 16 parity tests. Hang root cause: std's unwinder (DebugAllocator
  captures a trace on every alloc) walked off the fiber base via a stale return address and read
  addr 0x8; fixed by a zero return-address sentinel (x30 / word below Start). Killed stale hung
  test pid 68879. `wip/async-await-slots-20261003` kept (do not delete).
- Item 5 box left OPEN: `bench/spawn.zig` (PRD §5 gate 6 at 1 and 1000 in flight) still missing.
- Next: (a) bench/spawn.zig + tick item 5; (b) code-reviewer warnings from PR #25: `await` outside a
  fiber should `run_until(task.done)` not drain all fibers; guard pages or deeper canary; checked
  adds in `task_create`; tests for zero-size ctx/result under `.fail`, cancel-after-done; x86_64 test
  calling a stack-trace capture inside a fiber. Then item 6 (cancel state).
- Blockers: none. Open questions: none. Stabilize streak 0.
- Gotchas: `zig test --dep sirocco -Mroot=tests/parity/root.zig -Msirocco=src/root.zig -fno-omit-
  frame-pointer --test-no-exec -femit-bin=/tmp/..` builds the parity binary alone; run it under a
  python subprocess timeout (no `timeout`, lldb cannot attach). `--test-filter` is compile-time
  only. Guard blocks `cd <repo>` in compound commands. Tests name an item-5 failure as hang when it
  is really a crash in the Zig handler: read the last `N/M name...` line.

## Cycle 31 — 2026-10-03 — FEATURE
- Inbox: no OWNER activity since watermark; CI green on edb1a36; only open issue milestone #18.
- Preflight found the repo dirty on `feat/async-await-slots`: ~680 lines of an interrupted item-5
  attempt (`src/concurrency.zig`, `tests/parity/concurrency.zig`, edits to runtime/sched/parity).
  Preserved as `wip/async-await-slots-20261003` (pushed, commit may not be green). Do not delete.
- Trial: restored those files onto `feat/async-await-slots` and ran `zig build test` — it hung
  >400s (hung runner + test binary; likely a fiber deadlock/park-without-unpark in the new slots).
  Killed it, restored the branch to clean main. No PR, no merge. Time budget ran out for debugging.
- Next: item 5. `git checkout wip/async-await-slots-20261003 -- <those 7 files>` onto
  `feat/async-await-slots` (local branch == main), find the hanging test by running parity
  tests filtered one at a time under a manual kill timer, fix, PR.
- Blockers: none. Open questions: none. Stabilize streak 0.
- Gotchas: zsh `Z=...; $Z build` fails in a `&&` chain — use the full path. A stale hung test
  binary from Oct 1 (pid 68879, `.zig-cache2`) was still running in the sirocco repo; I did not
  start it and left it — kill it if still present. Guard blocks compound commands mixing /tmp
  writes with citadel paths; split them.

## Cycle 30 — 2026-10-02 — STABILIZATION (forced: open OWNER bug #23)
- Inbox: only OWNER item was bug #23; CI green on 337931a; milestone #18 open, no plan PR.
- Done: fixed #23 via PR #24 (merged as edb1a36, CI green Linux+macOS+6 cross, #23 auto-closed).
  Root cause from x86_64 `-femit-asm`: LLVM -Os emitted `lea rax,[rbp-56]` but never copied it to
  `rsi`, so std's inline-asm `Io.fiber.contextSwitch` read the wrong context. Replaced by own
  naked `switch_context_asm` (push callee-saved, save sp/fp/pc, jump), called via a
  `callconv(.c)` pointer with `@call(.never_inline)` (else LLVM splices the asm into `run`).
  `sched.supported` now false on Windows; comptime Context-layout assert; Linux ReleaseSmall CI
  step restored. code-reviewer: 0 critical; warnings (Windows ABI, stale docs) fixed.
- Next: plan 002 item 5 (async/concurrent/await/cancel slots) — no longer blocked.
- Blockers: none. Open questions: none. Stabilize streak 0.
- Gotchas: naked fn params break the self-hosted x86_64 backend (Debug on Linux CI) — declare none.
  `zig test -target x86_64-linux -fno-emit-bin` does not run that backend, only CI catches it.
  No Rosetta/qemu here: x86_64 is verifiable by asm inspection + CI only. `sleep` in Bash is
  blocked; wait with `until` loops. The guard blocks any command containing `cd <repo>`.

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
