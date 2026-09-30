# sailor — context

last_seen_at: 2026-09-30T08:40:00Z
rejected_plans: []

## Migration window

- 2026-09-29 (sailor-migration, run 2): errors 207→0; PR #40 squash-merged (10/10 CI green),
  #34 closed, plan 001 items 4, 6-10 ticked (#19). Landed: env access via `environ_map:
  *const std.process.Environ.Map` (first param after the receiver, before `io`); time/sleep/
  Mutex/fs/isatty via `io: std.Io` (long-lived structs cache `io` at `init`); `src/term/win32.zig`
  shim for the console externs 0.16 std dropped (kernel32 BOOL returns `c_int`); `build_support/
  tidy_main.zig` on `process.Init`; `zig fmt` applied to src+build.zig (reflow tripped the tidy
  ratchet, fixed by tightening files, baseline untouched); examples/benchmarks/scripts migrated;
  before/after table in `docs/API.md`. Local Windows check that works: `zig build test
  -Dtarget=x86_64-windows-gnu` (msvc libc is unavailable locally; run-step failures are noise,
  only `error:` lines from `compile test` count). Windows quirk: stat needs a read-access handle.
- Not landed / follow-ups: widgets never referenced by any test still use removed
  `ArrayList(T).init` (websocket, theme_editor, metricspanel, debugger, richtext, multicursor,
  virtuallist, streaming_table) so `bench-large-data` and `examples/clipboard_demo.zig` fail to
  build; `tests/*.zig` (~78 files) are not `zig fmt` clean; docs other than API.md still show old
  signatures (item 12). v3.0.0 not tagged: needs items 11 (assertion baseline, 2/5) and 12.
- Earlier run (2026-09-28): errors 696→207; mechanical renames, Io wave 1 sinks, started wave 2.

## Cycle 19 — 2026-09-30 — STABILIZATION

- Done: main was red (run on eec7af2, the 0.16 migration merge), Windows job only:
  `tests/error_recovery_test.zig` asserted wall-clock bounds after real `io.sleep` (`>= 1ms`,
  `>= 5ms`, 2ms sleep vs 1ms budget); Windows wakes early vs the QPC awake clock. Fix, PR #41
  (merged, 10/10 green): `VirtualClock` Io double built from `std.Io.failing.vtable.*` with
  `sleep` (advances virtual ns) and `now` overridden; tests assert requested sleeps and
  BudgetExceeded deterministically. See [[patterns]].
- Fixing one Windows test exposed the next (CI round-trip ~9 min): audit the whole file for the
  same pattern before pushing. Still real-time in that file: `elapsed < 1ms` (low-quality
  render), `< 10ms` snapshot, async-hook sleeps (~L800); upper bounds can flake on loaded CI.
- PRs: #41 (merged).
- Next: item 11 remaining: `tui/buffer.zig`, `tui/layout.zig`, `fmt.zig`; item 12 docs; then
  v3.0.0. Local 0.16 zig: /Users/fn/.zr/toolchains/zig/0.16.0/zig.
- Blockers: none. Open questions: none.
- Guard quirk: `cd <repo>; gh run view ... | ...` compounds were blocked; run gh without `cd`,
  redirect logs to /tmp. Memory writes: use Write/Edit, not bash heredocs.

## Cycle 18 — 2026-09-29 — FEATURE

- Done: preflight clean (PR #38 already merged, CI green). Inbox: no OWNER action; #34 window
  is ON (sailor-migration owns items 4/6-10; do not touch). Item 11 (2/5): `arg.zig` assertion
  baseline as PR #39, merged 10/10 green. Reused the preserved
  `wip/arg-assertion-baseline-20260928` `arg.zig` (25 asserts + 10 tests); `maybe` kept private
  (no `src/stdx.zig` yet — create it once when a second module needs it). Tidy ratchet bit: asserts
  grew `Parser`/`Commands` over baseline, so extracted `writeFlagHelp`/`writeCommandHelp` to file
  scope (Parser 312→296, Commands 97→94). code-reviewer caught: `std.io.fixedBufferStream` in new
  tests (use `std.Io.Writer.fixed`), tautological asserts, weak `if (suggestion)` tests — fixed.
- PRs: #39 (merged).
- Next: item 11 remaining, in order: `tui/buffer.zig`, `tui/layout.zig`, `fmt.zig`; then tick item.
  Stabilization item: `zig fmt --check src` flags 78 pre-existing files (CI doesn't run it).
  Stale local branch `test/arg-assertion-baseline` (== old main) left in place.
- Blockers: none. Open questions: none (#34 is the window switch; do not close).

## Cycle 17 — 2026-09-27 — FEATURE

- Done: preflight found repo on PR #37's branch, clean, pushed; merged it (10/10 green) before
  switching to main. CI green. Inbox: no new OWNER input on #34, no plan PR. Fixed stale
  milestone-19 bookkeeping: ticked the `wip/timeline-description-rendering` checkbox (it was
  actually finished/merged in cycle 3 as PR #22, box was never ticked) and commented explaining
  the stale `wip/timeline-description-rendering` branch stays undeleted per the kingdom
  contract's unconditional "never delete a wip/* branch" rule (overrides the plan's "remote
  branch deleted" verify line). Since items 4/6-10 stay blocked on #34 (still open, no new OWNER
  reply), picked item 11 ("assertion baseline on hot modules") as unblocked work — it needs no
  0.16 migration. Scoped to `term.zig` (first in module order, had zero asserts). test-writer
  pinned ~25 contract tests first; zig-developer added 43 asserts across `isatty`, `getSize`
  family, focus/paste predicates, `hexEncode`/`hexDecode`, xtgettcap query/response,
  `MockTerminal` — and fixed a latent gap where `getSizeWindows` had no bounds gate before
  returning raw console dimensions (now returns the existing `Error.TerminalSizeUnavailable`
  instead of asserting on OS-supplied data). `zig build test` green (348/348), `zig fmt`/tidy
  clean. Opened PR #38; CI pending at cycle deadline — left for next cycle's inbox, same
  recurring pattern as #21/#25/#26/#29/#30/#31/#32/#33/#35/#36/#37.
- PRs: #37 (merged), #38 (open, CI pending).
- Next: inbox merges #38 once green. Item 11 remaining files, in order: `arg.zig`,
  `tui/buffer.zig`, `tui/layout.zig`, `fmt.zig` — same test-writer-then-zig-developer pattern
  worked well for `term.zig`, reuse it. Milestone checkbox for item 11 stays unticked until all
  five files are done.
- Blockers: #34 still open (OWNER's 2026-09-18 reply about cron access answered a different
  framing; cycle 16 already flagged that granting the exception is outside the sailor realm's
  own edit scope and needs an operator). No new comment since.
- Open questions: #34 (unchanged).

## Cycle 16 — 2026-09-26 — FEATURE

- Done: preflight found repo on PR #36's branch, switched to main. CI green, no bugs. Merged
  PR #36 (10/10 green). Milestone #19 items still blocked on the toolchain switch; did one
  bounded stabilize task: proof-commented `src/tui/inspector.zig`'s 2 `catch unreachable`
  test-visitor sites (comment kept short so line stays <=100 cols), baseline 358->357. PR #37.
- PRs: #36 (merged), #37 (open, CI pending).
- Next: inbox merges #37 once green. Remaining candidates: `src/tui/async_loop.zig`
  (563,685,733,792,887; verify each callback's task always succeeds).
- Blockers: #34 got an OWNER reply 2026-09-18: "Access to cron, add exception for work from
  cleanup schedule. After work done, roll back exception from cleanup schedule." Needs operator
  action on cron (outside sailor realm; AI cannot edit it). Issue left open.
- Open questions: #34.

## History (cycles 13-15, condensed 2026-09-29)

Cycle 15 (STABILIZATION, 2026-09-17): merged PR #35 (nested `ArrayList` `.empty` sweep).
`tidy-auditor` found zero baseline drift. Proof-commented `src/arg.zig:590` as PR #36 (tidy
baseline 359→358). Next provable candidates: `src/tui/inspector.zig:941,966` and
`src/tui/async_loop.zig:563,685,733,792,887`. NOT provable, need typed-error redesign:
`event_metrics.zig`/`render_metrics.zig` (4 sites), `bench.zig` (5, `Timer.start()` can fail),
`smart_autocomplete.zig` (2).

Cycle 14 (FEATURE, 2026-09-16): merged PR #33 (closes the `//!` header sweep). Re-probed
milestone #19 items 4/6-10 with `zig test src/sailor.zig` on 0.16.0 (347 errors): no partial
rename can land on the pinned 0.15.2 build. Filed question+needs-human issue #34 (long session
vs multi-cycle `wip/*` migration branch). Found PR #28's `ArrayList` sweep missed 65 nested-field
sites in 34 files (see [[patterns]] "Caution on done mechanical sweeps"); fixed as PR #35.

Cycle 13 (FEATURE, 2026-09-15): merged PR #32; `//!` headers for `src/tui/widgets/` (38 files)
as PR #33 (tidy baseline 397→359). Items 4/6/7 confirmed toolchain-blocked; do not re-check.
Remaining tidy gaps then: 52 files >800 lines, `while (true)` loops, function length,
`assert(` density.

## History (cycles 0-10, condensed 2026-09-17)

Cycle 12 (FEATURE, 2026-09-15): merged PR #31; `//!` header sweep of `src/tui/` core (35 files)
as PR #32. #19 items 4/6/7 blocked (toolchain switch + `std.Io` rewrite); do not re-check.

Cycle 11 (FEATURE, 2026-09-12): merged PR #30; added `//!` headers to 13 top-level `src/*.zig`
files as PR #31 (tidy baseline 446→433, cross-checked with a second binary).


Cycle 10 (STABILIZATION, 2026-09-12): merged PR #29. `tidy-auditor` found zero baseline drift.
Proof-commented `pipeline.zig`'s 2 `catch_unreachable` sites (progress formatters) as PR #30.

Cycle 9 (FEATURE, 2026-09-11): re-verified item 4's remainder still has no 0.15.2-compatible
spelling (direct stdlib read, same conclusion as cycles 6-8). Fell back to stabilize: proof-
commented `countdown_timer.zig`'s 3 `catch unreachable` sites as PR #29.

Cycle 8 (FEATURE, 2026-09-11): checked item 5 (`ArrayList` literal sweep) the same way cycle 6
found item 4's safe half — confirmed `.empty` is 0.15.2-compatible, mechanically replaced all 132
`= .{}` sites across 34 files as PR #28 (merged). See [[patterns]] for the reusable
"check for a 0.15.2-compatible spelling before assuming toolchain-blocked" pattern.

Cycle 7 (FEATURE, 2026-09-10): merged PR #26 (safe-half renames). Confirmed item 4's remainder
(`Io.Mutex`, env access, `posix.isatty`, `mem.indexOf*`→`find*`, ~500 sites) has zero
0.15.2-compatible spelling, unsafe to land blind. Proof-commented `eventbus.zig`'s 3 test-only
`catch unreachable` sites as PR #27.

## History (cycles 0-6, condensed 2026-09-12)

Cycle 6 (FEATURE, 2026-09-10): merged PR #25 (`crypto_random` tidy tracking). Read 0.15.2 and
0.16.0 stdlib directly and found item 4's six renames split cleanly: `GeneralPurposeAllocator`→
`DebugAllocator` and `linkLibC()`→`.link_libc = true` are safe under 0.15.2 now; `Io.Mutex`, env
access, `posix.isatty`, `mem.indexOf*`→`find*` (478 sites) have no 0.15.2-compatible spelling and
need the actual toolchain switch — this is the finding cycles 7/9/11 kept re-confirming. Landed
the safe half as PR #26 (left open for cycle 7's inbox); item 4 left unticked.

Cycle 5 (STABILIZATION, 2026-09-09): merged PR #24 (`@panic` tidy tracking, all 8 sites
proof-commented). `tidy-auditor` found zero baseline drift; added a new `crypto_random` tidy
check (mirroring `time_usage`) as PR #25, left open for next cycle.

Cycle 4 (STABILIZATION, 2026-09-08): CI red on `main` (flaky `avg_ns` perf assertion) forced
STABILIZATION; merged cycle 3's already-prepared fix PR #23, confirmed green. `tidy-auditor`
found `zig build tidy` passing cleanly (447 entries); flagged `@panic` (8, 2 files) as next
target.

Cycle 3 (FEATURE, 2026-09-07): fixed a Windows-only CRLF bug in the tidy step's
`countLongLines` (PR #21) — see [[debugging]] for the durable pattern. Rebased
`wip/timeline-description-rendering` onto main as PR #22, merged.

Cycle 2 (FEATURE, 2026-09-06): implemented plan 001 item 2, the `tidy` build step —
`build_support/tidy.zig` (line/function length, missing `//!` header, unproven
`catch unreachable`, `std.debug.print`/`std.time.*`, `usize` in wire formats; 30 TDD tests) plus
`build_support/tidy_main.zig` CLI, wired into `zig build test`; generated `tidy_baseline.txt`
(447 entries) as the starting ratchet. PR #21 opened (merged next cycle after a Windows-only
CRLF fix — see [[debugging]]).

Cycle 0 (RESTRUCTURE, 2026-09-05): realm created; memory migrated from the repo's former
`.claude/memory/`; plan `001` prescribed (Zig 0.16 migration, MAJOR → v3.0.0, 368 probe errors +
`linkLibC`). `wip/timeline-description-rendering` preserved mid-cycle TDD work (finished as PR
#22 in cycle 3). Standing backlog carried forward, still partly open: the v2.100.0
"Widget Doc-Comment Audit Round 3" milestone has `terminal.zig` (`AnsiParseState` wiring),
`pager.zig` (soft-wrap), `metrics_dashboard.zig`/`richtext.zig` (scope decisions), and
`paragraph.zig` (word/char wrap + RTL/bidi, architect pass, do last) still unaddressed —
separate from plan `001`/milestone #19, not yet resumed. Repo hygiene backlog (stale
`README.md`/`docs/PRD.md`, 52 files >800 lines) also still open, tracked in STATE.md.

Cycle 1 (FEATURE, 2026-09-05): plan `001` merged as #18; opened tracking issue #19 (12-item
checklist). Implemented item 1 (hygiene leftovers) as PR #20, merged.
