# sailor — context

last_seen_at: 2026-10-29T00:00:00Z
rejected_plans: []

## Cycle 45 — 2026-10-29 — STABILIZATION

- Preflight: main clean (81695bc), CI green, bug #73 open (forced STABILIZATION). Inbox: no owner
  comments.
- Done: **PR #74** `fix/dialog-render-compiles` closes #73: `Dialog.render` uses
  `Paragraph.fromLines`; five exact-cell tests replace the stale ones; `dialog.zig` and ten more
  orphaned widget files (breadcrumb, color_picker, command_bar, command_palette, debug,
  filebrowser, filter_bar, keymap, scrollbar, timeline) imported in the `tui.zig` test block. Cause
  of #73: widget `test` blocks only run if a test root imports the file.
- Found: **bug #75** 33 more widget files do not compile in a test root (257 errors, ~800 dark tests:
  stale `Buffer.init(alloc, rect)`/`getCell`/`try render`), plus `splitpane` (`calculatePanes
  conflicting constraints` 60 vs 39) and `chunkedbuffer` (wide char `世界` line 0) tests fail.
  Probe: `zig test --dep build_options -Mroot=src/sailor.zig -Mbuild_options=/tmp/bo/build_options.zig`
  (stub: `pub const deprecation_mode: []const u8 = "warn";`) prints every analysed test.
- Next: n=46 STABILIZATION (open bug #75): fix files in batches of ~6 (test-writer sonnet agents in
  parallel), one PR per batch, add a tidy check that every widget file with a `test` is imported by
  a test root. Item 7 (wrap) and 8 wait; #65 at 6/9. Also unfixed: BulletChart target == max tick.
- Blockers: none. Open questions: none. Stabilize streak 0.
- Quirks: a probe edit to `tui.zig` is undone with `cp` from a backup; whole-suite probe runs in
  ~1 min; PR CI ~14 min so a PR must open by minute ~7.

## Cycle 44 — 2026-10-28 — FEATURE

- Preflight: tree clean on main, CI green (b1e19cd), inbox clear; only open issue was milestone #65.
- Done: plan 003 item 6, **PR #72** `docs/adr-0001-paragraph-wrap-bidi` (docs only, CI 10/10,
  merged, `auto-merged`). One architect agent (opus, ~$2.5, 12.5 min: too slow, brief it to stay
  under ~5 min next time). ADR decisions: stack `RowScratch` 512 columns in new
  `paragraph_wrap.zig`; width via `unicode.zig`; `scroll` = visual rows; wrap first, then per-row
  run-based bidi (UAX #9 subset); `.word` stays default; `Paragraph.rowCount(area)` added;
  `render()` signature unchanged (MINOR). Item 8 also widens `charType`/`detectDirection`/
  `charWidth`. #65 at 6/9.
- Found: **bug #73** `Dialog.render` (dialog.zig:175) builds `Paragraph{.text,.style}` fields that
  do not exist; never referenced so build stays green. Fix before item 7.
- Next: n=45 STABILIZATION (forced by n%5): fix #73 (and why dialog tests never compile), BulletChart
  target==max_value tick. Then item 7 (wrap per ADR test list), item 8, release v3.2.0.
- Blockers: none. Open questions: none. Stabilize streak 0.
- Quirks: PR CI (incl. Windows + benchmarks) takes ~14 min; start the PR by minute ~7 to merge in
  budget. Foreground `sleep` is blocked; wait with a background loop. Architect agent probe left
  `/tmp/adr_probe`.

## History (cycles 36-43, condensed 2026-10-29)

C43: item 5 PR #71, area/bullet chart tests assert exact cells (two parallel sonnet test-writers,
~$0.9, 4 min); exposed `BulletChart` `show_values` never drawing text (fixed, `valueTextReserve`).
Unfixed: `BulletChart` target == `max_value` draws no tick (`target_col == bar_width`).
Quirks: guard blocks Bash containing `cd <repo>` or `date; cat citadel/...` combos (read citadel
files with Read, run git/zig without `cd`); a `function_length` baseline entry may not grow, extract
a helper; do not call ScheduleWakeup in a /cycle session.

C42: item 4 PR #70, `tidy.countAssertionFreeTests` (brace matching skips comments/strings;
`expect*`/`assert*`/`check_invariants` idents count); `tidy_main` takes `check src tests build.zig
baseline`; 838 assertion-free tests in 115 files baselined, tidy entries 323 -> 438. Helper-based
assertions (`verify*`, `check*`) are invisible to the ratchet: add a direct assertion instead.
C41: item 3 PR #69, `while (true)` sites bounded (focus/workspace walks, `getResultWithTimeout`,
Windows `readByteWindows` poll cap `timeout/poll_ms + 2`), `// top-level loop:` kept in repl.zig and
validation.zig worker; tidy `unbounded_while` baseline 0; CHANGELOG has `[Unreleased]`. A frozen-clock
test needs a manually spawned blocker thread assigned to `validator.thread`.
Quirks: poll `gh pr checks` with python in <=400 s slices (PR CI ~13 min); Windows cross-target test
on macOS prints only run-step noise.

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

## History (cycles 25-31, folded 2026-10-29)

- 25 (STABILIZATION): Windows-only mindmap runner timeout was a flake; PR #48 async_loop test
  callbacks off `catch unreachable`; PR #49 `Treemap` no longer blanks on NaN/+Inf. 26: plan 002
  proposed (#50). 27: plan 002 item 1 (PR #52) moved eight widgets, `grapheme.wrapText`,
  `parseAnsiSegments` and two examples off `ArrayList.init`; `MultiCursorEditor.deleteCharAll`
  shifts all cursors by 1, untested, NOT fixed. 28: item 2 (PR #53) `zig build build-all`
  compiles every example and benchmark, CI runs it plus `zig fmt --check`. 29: item 3 (PR #54)
  `zig fmt tests`, 69 files whitespace only.
- 30 (STABILIZATION): PR #55 metrics stats sort in place (4 `catch unreachable` gone); PR #56
  `area_chart_test` tightened. 31: item 4 PR #57, `TerminalWidget.render` interprets CSI/SGR via
  `AnsiParseState`; style does not carry across scrollback lines.
- Quirks: global `zig` is 0.15.2, put `/Users/fn/.zr/toolchains/zig/0.16.0` first on PATH; probe
  one tests/ file with `zig test --dep sailor -Mroot=tests/X_test.zig -Msailor=src/sailor.zig
  --cache-dir /tmp/sailor-zig-cache`; stale `.zig-cache` gives bogus `FileNotFound`; tidy ratchet
  counts `build.zig` length, new build code goes into helper fns; `gh pr checks --watch` hits the
  540 s tool cap (Windows CI ~9 min), poll with python `time.sleep`; guard blocks `sleep N; cmd`
  and `cat >> file <<EOF`; always `gh run list -R yusa-imit/sailor`, never with `cd` in the same
  Bash call; macOS `sed -i` needs `''`; no `timeout` binary; no `zig build test -Dtest-filter`.

## History (cycles 0-24, folded 2026-10-30)

- **Cycles 0-18 (2026-09-05..29)**: realm created; plan `001` merged (#18, tracking #19); `tidy`
  build step (`build_support/tidy.zig`, `tidy_baseline.txt` ratchet) wired into `zig build test`;
  `wip/timeline-description-rendering` finished as PR #22 (never delete `wip/*`). Windows-only CRLF
  bug in `countLongLines` (PR #21, see [[debugging]]). 0.16 work split early: `DebugAllocator` and
  `.link_libc = true` landed first, the rest waited for the toolchain switch ([[patterns]] "check
  for a 0.15.2-compatible spelling"). A nested `ArrayList` sweep missed 65 sites (PR #35, see
  [[patterns]] "Caution on done mechanical sweeps"). Reviewer lessons: `std.Io.Writer.fixed`, not
  `std.io.fixedBufferStream`; no tautological asserts. Question #34 got the OWNER's cron-exception
  reply (migration window ON).
- **Migration (2026-09-28/29)**: errors 696→207→0; PR #40 merged (10/10 CI). Env access via
  `environ_map: *const std.process.Environ.Map` (first param after the receiver, before `io`);
  time/sleep/Mutex/fs/isatty via `io: std.Io` (long-lived structs cache `io` at `init`);
  `src/term/win32.zig` shim for console externs 0.16 std dropped; `build_support/tidy_main.zig` on
  `process.Init`; before/after table in `docs/API.md`. Local Windows check: `zig build test
  -Dtarget=x86_64-windows-gnu` (run-step failures are noise, only `error:` lines from `compile
  test` count); Windows stat needs a read-access handle.
- **Cycles 19-23 (2026-09-30..10-04)**: 19 main red on Windows only (wall-clock bounds after real
  `io.sleep`), PR #41 `VirtualClock` Io double ([[patterns]]); real-time asserts remain in
  `tests/error_recovery_test.zig` (~L800). 20 PR #42 regenerated `tidy_baseline.txt` (359->334).
  21-23 item 11 assertion baseline: `tui/buffer.zig` #43 (`Buffer.fill` u16 overflow, shared
  `src/stdx.zig`), `tui/layout.zig` #44 (`Rect` u16 overflow; a lone `.min` larger than the span is
  honored, others squeezed to 0), `fmt.zig` #45 (`Table.render` segfault on alloc failure,
  `max_width = 0` loop, width caps 2^20 config / 2^30 cell, new errors `InvalidConfig`/
  `CellTooLong`/`NonFiniteNumber`). Review caught `Csv.init` asserting on user config.
- **Cycle 24 (2026-10-05)**: README rewrite + CHANGELOG (PR #46), release PR #47, tag v3.0.0;
  migration issues zr#178, silica#163, zoltraak#141; milestone #19 closed.
- Quirks: stale `.zig-cache` -> `--cache-dir /tmp/sailor-zig-cache`; "failed command: .../test
  --listen" is noise at exit 0; fast loop `zig test -Mroot=src/sailor.zig --test-filter X`; CI
  Windows ~7-9 min so a release PR must open by minute ~11 (docs-only PRs still run full CI);
  `gh run list` without `--workflow` (a stale run once appeared); guard blocks bash writes to
  citadel (use Write/Edit), `gh` with `cd`, and heredocs; zsh `echo == x` errors (quote it).
- **Backlog since cycle 0**: v2.100.0 "Widget Doc-Comment Audit Round 3" (`terminal.zig`
  `AnsiParseState`, `pager.zig`, `metrics_dashboard.zig`/`richtext.zig`, `paragraph.zig` last);
  stale-doc and 52-files->800-lines hygiene tracked in STATE.md.
