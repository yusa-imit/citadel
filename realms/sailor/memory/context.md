# sailor — context

last_seen_at: 2026-10-04T00:00:00Z
rejected_plans: []

## Cycle 23 — 2026-10-04 — FEATURE

- Done: preflight clean, CI green on main (a938d5f), inbox clear (only comment was our own on
  #19). Item 11 (5/5): `src/fmt.zig` assertion baseline, PR #45 opened (zig-developer, ~11 min).
  37 asserts + 20 `maybe`, `Table.check_invariants()`. Defects fixed: `Table.render` segfault on
  alloc failure (freed uninitialised lists), `max_width = 0` infinite loop, short `alignments`
  OOB, unbounded width math (caps 2^20 config / 2^30 cell), `addNumber` nan/inf (invalid JSON),
  CSV fields with `\r` unquoted. Five-module assert total 175 (plan asks 80), zero unproven
  `catch unreachable`, Debug + ReleaseSafe `zig build test` green locally. renderRow split; both
  fmt.zig tidy baseline entries removed. Plan item 11 ticked in the PR branch.
- Review (sonnet): 0 critical; fixed `Csv.init` asserts firing on user config (added
  `csv_config_valid`) and a compound assert (2nd commit). Left: huge-slice test only reads `.len`;
  `Error` set stale / `!T` signatures (suggest `TableError`/`JsonError`); `allocator` param name.
- PRs: #45 OPEN, CI pending at end of cycle (Linux green on 1st commit; 2nd commit re-running).
  Cycle deadline hit before Windows finished; commented "merge next cycle".
- Next: n=24 FEATURE: inbox step 8 merges #45 if CI green (squash, `auto-merged`), tick item 11
  in #19. Then item 12 docs + v3.0.0 (README, PRD header, CHANGELOG, `/release major`). n=25 is
  stabilization. Consumers: note new error values `InvalidConfig`/`CellTooLong`/
  `NonFiniteNumber` from fmt Table/JSON and `layout.split` lone-min change in the migration issues.
- Blockers: none. Open questions: none.
- Quirks: macOS has no `timeout` binary (exit 127). Pace: all-in-one zig-developer then CI
  ~9 min means start CI by minute ~12 or the PR waits a cycle.

## Cycle 22 — 2026-10-03 — FEATURE

- Done: preflight clean, CI green on main (6f5d27a), inbox clear (only comment since watermark was
  our own on #19). Item 11 (4/5): `src/tui/layout.zig` assertion baseline, PR #44 merged 10/10
  (Windows 9m3s). 54 asserts + 20 `maybe`, `Rect.check_invariants()`, u16 overflow fixes in
  `Rect` edge math, `split` fixes (u32 overflow, over-commit, offset overflow), 19 new tests incl.
  seeded model test. Behavior change: lone `.min` larger than span is honored fully, others
  squeezed to 0; `split` asserts area edges <= 65536. tidy baseline layout.zig 22 -> 13.
- PRs: #44 (merged). Tracking issue #19 commented; item 11 stays unticked (4/5).
- Next: item 11 last module `fmt.zig` (0 asserts, 1387 lines; check u16/u32 overflow in table
  width math); then tick item 11, item 12 docs + v3.0.0. n=23 FEATURE (n=25 stabilization).
- Blockers: none. Open questions: none.
- Quirks: delegating the whole TDD cycle to one zig-developer agent (~$1.4, ~10 min) worked;
  ran PR-to-merge in ~11 min. Consumers (zr tui migration) should note the `split` lone-min change.

## History (cycles 19-21, condensed 2026-10-04)

Cycle 21 (2026-10-02): item 11 (3/5) `tui/buffer.zig`, PR #43; fixed `Buffer.fill` u16 overflow and
`renderDiff` uninitialized byte; new shared `src/stdx.zig` (`maybe`). Quirks: `cd <repo> && cmd`
in one Bash call; stale `.zig-cache` -> `--cache-dir /tmp/sailor-zig-cache`; "failed command:
.../test --listen" is noise at exit 0; fast loop `zig test -Mroot=src/sailor.zig --test-filter X`.
Cycle 20 (STABILIZATION, 2026-10-01): PR #42 regenerated `tidy_baseline.txt` post-0.16 (359->334).
`gh run list --workflow CI --branch main` once returned a stale run; list without `--workflow`.
Live counts then: 12 bare `catch unreachable` (async_loop 566,688,736,795,890; event_metrics
181,248; render_metrics 186,255; smart_autocomplete 41,43; editor 97), 35 `std.debug.print`,
13 `while (true)`, 53 files >800 lines. README drift goes with item 12.
Cycle 19 (STABILIZATION, 2026-09-30): main red on Windows only (wall-clock bounds after real
`io.sleep`); PR #41 `VirtualClock` Io double, see [[patterns]]. Still real-time in
`tests/error_recovery_test.zig`: `elapsed < 1ms`, `< 10ms` snapshot, async-hook sleeps (~L800).
Guard quirk: run `gh` without `cd`; memory writes via Write/Edit, not heredocs.

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

## History (cycles 16-18, condensed 2026-10-04)

Cycles 16-18 (2026-09-26 to 09-29, FEATURE): merged PR #36 and proof-commented
`inspector.zig`'s 2 `catch unreachable` test-visitor sites (PR #37). Ticked the stale
`wip/timeline-description-rendering` checkbox (branch stays, never delete `wip/*`). Item 11
(assertion baseline) started: `term.zig` PR #38 (`getSizeWindows` returns
`TerminalSizeUnavailable`), `arg.zig` PR #39 from the preserved
`wip/arg-assertion-baseline-20260928` (`maybe` later moved to `src/stdx.zig`). The tidy ratchet
bites when asserts grow a function over baseline: extract helpers to file scope. Reviewer caught
`std.io.fixedBufferStream` in new tests (use `std.Io.Writer.fixed`) and tautological asserts.
#34 got the OWNER's cron-exception reply; its window is ON (sailor-migration owned items 4/6-10).
Open: `zig fmt --check src` flags 78 pre-existing files (CI does not run it).


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
