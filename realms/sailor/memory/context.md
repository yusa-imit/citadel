# sailor — context

last_seen_at: 2026-10-27T00:00:00Z
rejected_plans: []

## Cycle 43 — 2026-10-27 — FEATURE

- Preflight: tree clean on main, CI green (37c2fa1), inbox clear; only open issue is milestone #65.
- Done: plan 003 item 5, **PR #71** `test/honest-area-bullet-chart` (CI 10/10, merged,
  `auto-merged`). Two parallel test-writer agents (sonnet, ~$0.9 total, ~4 min) gave 14 + 29
  assertion-free tests exact-cell assertions; both files left the tidy baseline. Tightening exposed
  a real bug: `BulletChart` `show_values` never drew text (`text_x` always past the right edge);
  fixed, bar now reserves `len+1` cells via `valueTextReserve`, text dropped if no bar cell
  would remain. #65 at 5/9.
- Next: n=44 FEATURE: item 6 ADR 0001 paragraph wrap and bidi (architect, opus; PR is an ADR doc
  under `docs/adr/`). n=45 is STABILIZATION.
- Noticed, unfixed: `BulletChart` target == `max_value` draws no tick (`target_col == bar_width`
  fails `target_col < bar_width`); pick up in stabilization or a small fix PR.
- Blockers: none. Open questions: none. Stabilize streak 0.
- Quirks: guard blocks Bash `cd <repo>; python3 - <<EOF` heredoc edits (use Edit/Write; `cd repo &&
  zig ...` without writes is fine); raising a `function_length` baseline entry is not allowed,
  so extract a helper (render 124 lines must not grow); `/tmp/af.py` lists assertion-free tests
  per file (recreate with Write if gone); do not call ScheduleWakeup in a /cycle session.

## Cycle 42 — 2026-10-26 — FEATURE

- Preflight: tree clean on main, CI green (3d423d6), inbox clear; only open issue is milestone #65.
- Done: plan 003 item 4, **PR #70** `test/assertion-free-ratchet` (CI 10/10, merged, `auto-merged`).
  `tidy.countAssertionFreeTests` (brace matching skips comments/strings/chars/multiline strings;
  `expect*`/`assert*`/`checkInvariants`/`check_invariants` idents count, `expected` does not);
  `tidy_main` now takes `check src tests build.zig baseline`; 838 assertion-free tests in 115
  files baselined (`assertion_free_test|-`), tidy entries 323 -> 438. 11 tidy unit tests. #65 at 4/9.
- Next: n=43 FEATURE: item 5 (`area_chart_test`, `bullet_chart_test` reach 0 in the baseline;
  regenerate with `zig run build_support/tidy_main.zig -- generate src tests build.zig
  tidy_baseline.txt`). n=45 is STABILIZATION.
- Blockers: none. Open questions: none. Stabilize streak 0.
- Quirks: no agents, ~11 min; CI was all-green ~7 min after the PR opened. Python heredoc edits
  to the repo worked from Bash. Helper-based assertions (`verify*`, `check*`) are not seen by the
  ratchet; fix those tests with a direct assertion rather than widening the list.

## Cycle 41 — 2026-10-25 — FEATURE

- Preflight: tree clean on main, CI green (99ddd3b), inbox clear; only open issue is milestone #65.
- Done: plan 003 item 3, **PR #69** `fix/bounded-while-sites` (CI 10/10, merged, `auto-merged`).
  focus.zig/workspace.zig walks bounded; `getResultWithTimeout` and Windows `readByteWindows`
  pipe poll get a `timeout/poll_ms + 2` cap; repl.zig and validation.zig worker keep
  `while (true)` with `// top-level loop:`; tidy `unbounded_while` (`countUnboundedWhile`, proof
  comment on same or previous line), baseline 0, tidy entries 329 -> 323. CHANGELOG now has an
  `[Unreleased]` section (items 1-3 + sunburst); plan item 3 ticked; #65 at 3/9. No agents, ~14 min.
- Next: n=42 FEATURE: item 4 (`assertion_free_test` ratchet in tidy, walks `tests/`). n=45 is
  STABILIZATION.
- Blockers: none. Open questions: none. Stabilize streak 0.
- Quirks: a frozen-clock test needs a manually spawned blocker thread assigned to
  `validator.thread` (a worker using the frozen `Io` would spin); `FrozenClock` double lives in
  validation.zig tests (same shape as `VirtualClock`). `zig build test -Dtarget=x86_64-windows-gnu`
  on macOS only prints run-step "unable to execute" noise. Poll `gh pr checks` with python in
  <=400 s slices; PR CI took ~13 min wall to reach all-green.

## History (cycles 36-40, condensed 2026-10-26)

C40 (STABILIZATION): PR #68 sunburst: tightening the last `a > 0 or b > 0` focus tests exposed that
`resolveNode` never set the top-level index, so `withFocused(n >= 1)` styled nothing; fixed. Counts
then: 11 `catch unreachable` (commented), 8 `@panic`, 35 debug.print, 7 `while (true)`, 52 files >800.
Stale `.zig-cache` gives `FileNotFound`; use `--cache-dir /tmp/sailor-zig-cache`. Weak asserts hide bugs.

C36: v3.1.0 released (PR #63, tag, milestone #51 closed; consumer issues zr#178, silica#163, zoltraak#141
got a comment, rule: one open issue per consumer). C37: plan 003 "Tiger Style bounds and test honesty"
(-> v3.2.0) proposed, PR #64; items: `deleteCharAll` fix, shared line rasterizer, remaining 7 `while
(true)` + tidy `unbounded_while`, tidy `assertion_free_test` ratchet, area/bullet test honesty, ADR 0001
(paragraph wrap + bidi), wrap, RTL, release. Planner output had HTML entities to un-escape. C38: owner
merged #64, milestone #65 opened; item 1 PR #66 (`deleteCharAll` shifts cursors via `shiftCursorsLeft`;
plan-file tick is easy to miss, fold it into the next PR). C39: item 2 PR #67, `src/tui/line_iter.zig`
(`LineIter`, i64 internally, 11 tests) used by canvas, linechart, radar_chart, parallel_coordinates,
slope_chart, chord_diagram.
Open for item 3 (seven `while (true)`): focus.zig:336, workspace.zig:194/211 -> `for`; term.zig:482 and
validation.zig:517 poll caps; repl.zig:240 and validation.zig:453 `// top-level loop:` comments.
Latent: the 4 clipped widgets `@intCast` an i32 point to u16 before the area check (a point > 65535 would
trap; unreachable today, clamp if raw coordinates are ever fed).
Quirks: tidy ratchet counts lines >100 in src (wrap comments); `std.debug.assert(` is banned, alias
`const assert = std.debug.assert;` per file; zsh has `$pipestatus`, not `$PIPESTATUS`; `zig test
src/sailor.zig --test-filter X` runs a new tui file's tests; tidy baseline 329 entries.

## History (cycles 32-35, condensed 2026-10-19)

- 32: plan 002 item 5, PR #58: `Pager.withWrap()` splits at the column count (1 col per code
  point), numbers only the first row, `scroll_y` = logical lines; a search match straddling a wrap
  point is not highlighted (documented). `render` split into `renderLine`/`renderRow`.
- 33: item 6, PR #59 (`metrics_dashboard` always said "No data": `getTypeStats("")`; now aggregates
  all types, memory peak = sum of per-type peaks) and PR #60 (`richtext` preview renders
  `~~strike~~` and `<u>underline</u>`).
- 34: item 7, PR #61: `Editor.init`, `MultiCursorEditor.init`, `LocalSource.init` return
  `error{OutOfMemory}!T` (callers need `try`; no consumer uses them). `grep Editor.init` missed
  `multicursor.zig`; compile errors find missed callers in ~1 min.
- 35 (STABILIZATION): PR #62, `area_chart_test` block tests assert corner glyphs (last
  `or countNonEmptyCells` disjunction gone). Tiger counts: 11 `catch unreachable` (proof-commented),
  8 `@panic`, 35 `debug.print`, 13 `while (true)`, 53 files >800, 263 asserts. Leftover test debt:
  many "does not crash" tests without assertions (`area_chart_test` NaN/Inf, tiny-area);
  `MultiCursorEditor.deleteCharAll` shifts all cursors (untested, unfixed).
- Quirks: `zig build test` ~4 min wall when CI is also running; Windows CI 6-10 min, open the PR by
  minute ~8; `zig build tidy` alone is a fast check; `zig build test` prints nothing on success;
  tidy ratchet counts lines >100 in src (wrap new long lines); `@FieldType` exists in 0.16; the
  guard blocks Bash containing `cd <repo>`; PATH needs the 0.16 toolchain each call.

## History (cycles 30-31, condensed 2026-10-16)
- 30 (STABILIZATION): PR #55 metrics stats queries sort in place and `rebuildTypeStats` refills retained
  capacity (4 `catch unreachable` gone, no API change); PR #56 `area_chart_test` fill_char tightened.
  Tiger counts then: 7 bare `catch unreachable`, 8 `@panic`, 35 debug.print, 13 `while (true)`, 53 files
  >800, 243 asserts.
- 31: item 4 PR #57, `TerminalWidget.render` interprets CSI/SGR via `AnsiParseState.escapeLength`/
  `applySgr`/`style`; style does not carry across scrollback lines; truncated seq ends the line.
- Quirks: probe one tests/ file in ~10 s with `zig test --dep sailor -Mroot=tests/X_test.zig
  -Msailor=src/sailor.zig --cache-dir /tmp/sailor-zig-cache`; `gh pr checks --watch` can exceed the 540 s
  tool cap, poll with python `time.sleep`; guard blocks `cat >> file <<EOF` (use Edit/Write).

## History (cycles 27-29, condensed 2026-10-15)
- 27: plan 002 item 1 (PR #52): eight widgets + `grapheme.wrapText`, `term/windows.parseAnsiSegments`,
  `clipboard_demo`, `large_data_bench` moved off `ArrayList.init`; wip branch
  `wip/fix-unbuilt-arraylist-sweep-20261009` kept. Fixed `MultiCursorEditor.insertCharAll`; `deleteCharAll`
  has the same class of bug (shifts all cursors by 1), untested, NOT fixed.
- 28: item 2 (PR #53): `zig build build-all` compiles every example and benchmark; CI runs it on all OSes
  plus `zig fmt --check` on Linux. `examples/clipboard_demo.zig` rewritten.
- 29: item 3 (PR #54): `zig fmt tests` touched 69 files (whitespace only); CI fmt covers `tests`.
- Quirks: global `zig` is 0.15.2, put `/Users/fn/.zr/toolchains/zig/0.16.0` first on PATH; stale
  `.zig-cache` gives bogus `FileNotFound` (use `--cache-dir /tmp/sailor-zig-cache`); tidy ratchet counts
  `build.zig` line/function length, so new build code goes into helper fns; `sleep N; cmd` blocked by the
  guard; `gh pr checks --watch` hits the 540s tool limit (Windows CI ~9 min), open the PR by minute ~8;
  macOS `sed -i` needs `''`; no `timeout` binary; `gh pr create` has no `--json`.

## History (cycles 25-26, condensed 2026-10-13)

Cycle 26 (2026-10-07): plan 002 proposed (#50). Cycle 25 (STABILIZATION, 2026-10-06): Windows-only
mindmap runner timeout on main was a flake (rerun green); PR #48 async_loop test callbacks off
`catch unreachable`, PR #49 `Treemap` no longer blanks on NaN/+Inf items. Quirks: `gh` with `-R`
must not share a Bash call with `cd <repo>`; subagent `isolation: worktree` is blocked by
guard_write; always `gh run list -R yusa-imit/sailor` (without `-R` returns stale runs); no
`zig build test -Dtest-filter`. Stray empty local branch `test/treemap-nonfinite-assertions`.

## Cycle 24 — 2026-10-05 — FEATURE

- Done: preflight clean, CI green, inbox clear (only our own comments). Merged #45 (fmt.zig
  assertion baseline, 10/10 CI) and ticked item 11. Item 12: PR #46 (README rewrite, PRD header
  3.0.0/0.16.0, new CHANGELOG.md) merged; release PR #47 merged, tag v3.0.0 + GitHub release.
  Migration issues zr#178, silica#163, zoltraak#141. Milestone #19 closed.
- Next: n=25 STABILIZATION (periodic). Then `/plan` 002: doc-comment audit round 3 backlog
  (terminal, pager, metrics_dashboard, richtext, paragraph), 8 orphaned widgets still on
  `ArrayList(T).init` (bench-large-data, clipboard_demo don't build), ~78 files not
  `zig fmt` clean, 52 files >800 lines. README claims "6 cross-compile" only via CI.
- Blockers: none. Open questions: none.
- Quirks: guard hook blocks bash writes to citadel (use Write/Edit); CI Windows ~7-9 min so a
  release PR needs to open by minute ~11; zsh `echo == x` errors (quote it). The docs-only PR
  still runs full CI (paths-ignore is push-only).

## History (cycles 19-23, condensed 2026-10-07)

Cycle 23 (2026-10-04): item 11 (5/5) `src/fmt.zig` assertion baseline, PR #45. Fixed `Table.render`
segfault on alloc failure, `max_width = 0` infinite loop, short `alignments` OOB, unbounded width
math (caps 2^20 config / 2^30 cell), `addNumber` nan/inf, unquoted CSV `\r`; new error values
`InvalidConfig`/`CellTooLong`/`NonFiniteNumber` (consumers note in migration issues). Review caught
`Csv.init` asserting on user config (added `csv_config_valid`). Pace: start CI by minute ~12.
Cycle 22 (2026-10-03): item 11 (4/5) `tui/layout.zig`, PR #44. `Rect` u16 overflow and `split`
fixes; behavior change: a lone `.min` larger than the span is honored, others squeezed to 0.
One zig-developer agent for the whole TDD cycle (~$1.4, ~10 min) worked.
Cycle 21 (2026-10-02): item 11 (3/5) `tui/buffer.zig`, PR #43; `Buffer.fill` u16 overflow, shared
`src/stdx.zig` (`maybe`). Quirks: stale `.zig-cache` -> `--cache-dir /tmp/sailor-zig-cache`;
"failed command: .../test --listen" is noise at exit 0; fast loop `zig test -Mroot=src/sailor.zig
--test-filter X`; macOS has no `timeout`; zsh `echo == x` errors (quote it).
Cycle 20 (STABILIZATION, 2026-10-01): PR #42 regenerated `tidy_baseline.txt` post-0.16 (359->334).
`gh run list --workflow CI --branch main` once returned a stale run; list without `--workflow`.
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

## History (cycles 0-18, condensed 2026-10-10)

- **Cycles 0-2 (2026-09-05/06)**: realm created; plan `001` merged (#18, tracking issue #19);
  hygiene PR #20; `tidy` build step (`build_support/tidy.zig`, 30 TDD tests, 447-entry
  `tidy_baseline.txt` ratchet) wired into `zig build test`. `wip/timeline-description-rendering`
  preserved, finished as PR #22 (never delete `wip/*`).
- **Cycles 3-5 (09-07 to 09-09)**: Windows-only CRLF bug in `countLongLines` (PR #21, see
  [[debugging]]); flaky `avg_ns` perf assertion fixed (PR #23); `@panic` sites proof-commented
  (PR #24); `crypto_random` tidy check (PR #25).
- **Cycles 6-9 (09-10/11)**: read both stdlibs and split item 4: `DebugAllocator` and
  `.link_libc = true` landed early (PR #26); `Io.Mutex`, env access, `posix.isatty`, `find*`
  renames had no 0.15.2 spelling and waited for the toolchain switch. `ArrayList` `.empty` sweep
  (PR #28). See [[patterns]] "check for a 0.15.2-compatible spelling".
- **Cycles 10-15 (09-12 to 09-17)**: `//!` header sweeps (top-level, `tui/`, `tui/widgets/`;
  baseline 446→359); `catch unreachable` proof comments; nested `ArrayList` sweep missed 65
  sites (PR #35, see [[patterns]] "Caution on done mechanical sweeps"); question issue #34
  filed on the migration branch vs long session.
- **Cycles 16-18 (09-26 to 09-29)**: item 11 assertion baseline started (`term.zig` #38,
  `arg.zig` #39); #34 got the OWNER's cron-exception reply (migration window ON). Reviewer
  lesson: use `std.Io.Writer.fixed`, not `std.io.fixedBufferStream`; no tautological asserts.
- **Backlog carried since cycle 0, still open**: v2.100.0 "Widget Doc-Comment Audit Round 3"
  (`terminal.zig` `AnsiParseState`, `pager.zig` soft-wrap, `metrics_dashboard.zig`/`richtext.zig`
  scope decisions, `paragraph.zig` wrap + RTL last); stale-doc and 52-files->800-lines hygiene
  tracked in STATE.md; `zig fmt --check src` flags 78 old files (CI does not run it).
