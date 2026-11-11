# sailor — context

last_seen_at: 2026-11-11T00:00:00Z
rejected_plans: []

## Aborted attempt — 2026-11-11 — disk gate, fifth in a row (counter stays 51)

- Disk gate read 17 GB free (< 20) on `/` (16 GB on 11-10, 12 GB on 11-09). Cycle stopped at preflight:
  no repo changes, no GitHub calls. Repo clean on main.
- Next: n=52 STABILIZATION unchanged (#75 batch 7: taskrunner + terminal + textarea; textarea own agent).
  Open question #78 (needs-human, non-blocking). Streak 0.
- Blockers: operator must free disk or lower the gate; nothing sailor-side can fix it.

## Aborted attempt — 2026-11-10 — disk gate, fourth in a row (counter stays 51)

- Disk gate read 16 GB free (< 20) on `/` (12 GB on 11-09, 15 GB on 11-07, 19 GB on 11-06). Cycle
  stopped at preflight: no repo changes, no GitHub calls. Repo clean on main.
- Next: n=52 STABILIZATION unchanged (#75 batch 7: taskrunner + terminal + textarea; textarea own agent).
  Open question #78 (needs-human, non-blocking). Streak 0.
- Blockers: operator must free disk or lower the gate; nothing sailor-side can fix it.

## Aborted attempt — 2026-11-09 — disk gate, third in a row (counter stays 51)

- Disk gate read 12 GB free (< 20) on `/` (15 GB on 11-07, 19 GB on 11-06): falling each time. Cycle
  stopped before any work; no repo changes, no GitHub calls.
- Next: n=52 STABILIZATION unchanged (#75 batch 7: taskrunner + terminal + textarea; textarea own agent).
  Open question #78 (needs-human, non-blocking). Streak 0.
- Blockers: operator must free disk (or lower the gate); nothing sailor-side can fix it.

## Aborted attempt — 2026-11-07 — disk gate again (counter stays 51)

- Disk gate read 15 GB free (< 20) on `/` (down from 19 GB yesterday); cycle stopped before any work.
  Second consecutive disk abort. `/tmp/sailor-zig-cache` is 2.1 GB; deleting it would not clear the gate.
- Next: n=52 STABILIZATION unchanged (#75 batch 7: taskrunner + terminal + textarea). Operator must
  free disk or lower the gate; nothing sailor-side can fix it.

## Aborted attempt — 2026-11-06 — disk gate (counter stays 51)

- Preflight disk gate read 19 GB free (< 20) on `/`; cycle stopped before any work, no repo changes.
  `/tmp/sailor-zig-cache` holds 2.1 GB (own scratch cache) but deleting it was not done: the gate says stop.
- Next: n=52 STABILIZATION (#75 open): batch 7, taskrunner + terminal + textarea (textarea own agent).
  Open question #78 (needs-human, non-blocking). Streak 0. Operator: free disk or lower the gate.

## Cycle 51 — 2026-11-05 — STABILIZATION

- Done: **PR #82** (batch 6 of bug #75, CI 10/10, auto-merged, `635bcae`): form, metrics_dashboard,
  profiler, record_editor imported in the `tui.zig` test block (141 tests). Fixed u16 overflows on far or
  oversized areas (all four), byte-wise drawing and cursors (form, record_editor), multibyte `deleteChar`,
  record_editor border overwrite / off-screen selection, metrics_dashboard section clipping, `render`
  functions split under 70 lines. Two sonnet zig-developers ~$1.4 total. Merged at minute ~24 (CI ~14 min;
  PR opened at minute ~12: open it by minute ~8 to make the deadline).
- Stale `tidy_baseline.txt` entries now (form `render`, profiler `renderFrameTimes`): ratchet down.
- Remaining in #75: taskrunner terminal textarea (3) + failing `splitpane`, `chunkedbuffer`. Known
  unfixed: 7 assertion-free tests in `tests/record_editor_test.zig`, 4 in `tests/profiler_widget_test.zig`.
- Next: n=52 STABILIZATION (#75 open): batch 7, taskrunner + terminal + textarea (textarea is 1136
  lines: give it its own agent). Blockers: none. Open question #78 (needs-human, no reply, non-blocking).
  Streak 0.

## Cycle 50 — 2026-11-04 — STABILIZATION

- Done: **PR #81** (batch 5 of bug #75, CI 10/10, auto-merged, `029f411`): httpclient, menu, linechart,
  markdown imported in the `tui.zig` test block (209 tests). Fixed httpclient page_allocator free of
  literals and u16/u64 overflows, `Menu.render` now infallible (callers in tests/ updated), linechart
  last point never drawn and markers overwritten by lines, markdown unclosed spans duplicating text,
  bounded list number/indent, per-codepoint rendering. Two sonnet zig-developers, ~$2.4 total, merged at
  minute ~23 (slightly over the 22 min deadline: open PR by minute ~7).
- Lesson: changing a `render` signature to void breaks `try x.render` callers in `tests/*_test.zig`;
  `zig build test` lists them, fix with `sed` on the flagged lines.
- Remaining in #75: form metrics_dashboard profiler record_editor taskrunner terminal textarea (7) +
  failing `splitpane`, `chunkedbuffer`. Known unfixed: `gauge.zig` `@intCast` past u16; markdown inline
  spans each take a row; stale `tidy_baseline.txt` entries for old linechart/markdown (ratchet down).
- Next: n=51 STABILIZATION (#75 open): batch 6, 4 files via 2 agents. Blockers: none. Open question #78
  (needs-human, no reply, non-blocking). Streak 0.

## Cycle 49 — 2026-11-03 — STABILIZATION

- Done: **PR #80** (batch 4 of bug #75, CI 10/10, auto-merged, `cfb8cb7`): select, tree, scatterplot,
  timeseries imported in the `tui.zig` test block (116 tests). Fixed Select/Tree byte-wise drawing,
  scroll_offset panic, Tree indent u16 overflow and 256-node cap (recursion -> bounded walk, depth 64),
  scatterplot multi-char/truncated markers and NaN/Inf, timeseries i64 range/calendar overflow and
  marker overwrite, out-of-buffer area u16 overflow in both charts. Two sonnet zig-developers (2 files
  each) cost ~$1.0 total, ~4 min: this split is the sweet spot. Earlier abort (disk 19 GB) is resolved.
- Tidy: growing `render` past its baseline fails `zig build tidy`; extracted `plotPoints` and `drawXAxis`.
- Remaining in #75: form httpclient linechart markdown menu metrics_dashboard profiler record_editor
  taskrunner terminal textarea (11) + failing `splitpane`, `chunkedbuffer`. Known unfixed: long
  `y_axis_label` overwrites mid Y label (scatterplot, timeseries); BarChart max==0; `Block.renderTitle` bytes.
- Next: n=50 STABILIZATION (n%5 and #75 open): batch 5, 4 files via 2 agents; open the PR by minute ~7
  (PR CI took ~13 min; merged at minute ~21). Blockers: none. Open question #78 (needs-human, no reply,
  non-blocking). Streak 0.

## Cycle 48 — 2026-11-01 — STABILIZATION

- Done: PR #79 (batch 3 of bug #75, CI 10/10, auto-merged): autocomplete, barchart, completion_popup,
  configeditor, context_menu, editable_table imported in the `tui.zig` test block; fixed
  `ContextMenu.moveUp/Down` infinite loop, BarChart overflow, CompletionPopup huge-item panic,
  ConfigEditor 256-node cap, EditableTable border overwrite. Three parallel sonnet test-writers cost
  ~$2.7 (budget $4/cycle: use fewer files per batch).
- Remaining in #75: form httpclient linechart markdown menu metrics_dashboard profiler record_editor
  scatterplot select taskrunner terminal textarea timeseries tree (15) + failing `splitpane`,
  `chunkedbuffer`. Known unfixed: BarChart max==0 draws nothing; `Block.renderTitle` cuts by bytes.
- Next: n=49 STABILIZATION (#75 open): batch 4 of ~4 files; open the PR by minute ~7. Blockers: none.
  Open question #78 (needs-human, non-blocking). Streak 0.
- Quirks: agents running `zig fmt src/tui/widgets/*.zig` touch siblings' files (fmt only own files).

## History (cycles 0-47, folded 2026-11-05)

- 0-24 (09-05..10-05): realm created; plan `001` (#18); `tidy` build step (`build_support/tidy.zig`,
  `tidy_baseline.txt` ratchet) in `zig build test`; `wip/timeline-description-rendering` finished as PR #22
  (never delete `wip/*`); Windows-only CRLF bug in `countLongLines` (PR #21, [[debugging]]). A nested
  `ArrayList` sweep missed 65 sites (PR #35, [[patterns]] "Caution on done mechanical sweeps"); reviewer
  lessons: `std.Io.Writer.fixed`, no tautological asserts. Question #34: OWNER granted the cron exception.
- Migration (09-28/29): errors 696 -> 0, PR #40 (10/10 CI). Env via `environ_map: *const
  std.process.Environ.Map` (first param after the receiver, before `io`); time/sleep/Mutex/fs/isatty via
  `io: std.Io` (long-lived structs cache `io` at `init`); `src/term/win32.zig` shim for console externs;
  `build_support/tidy_main.zig` on `process.Init`; before/after table in `docs/API.md`. Local Windows check:
  `zig build test -Dtarget=x86_64-windows-gnu` (only `error:` lines from `compile test` count).
- 19-23: main red on Windows only (wall-clock bounds after real `io.sleep`), PR #41 `VirtualClock` Io double
  ([[patterns]]); real-time asserts remain in `tests/error_recovery_test.zig` (~L800). PR #42 baseline
  359 -> 334. Item 11 assertion baseline: `tui/buffer.zig` #43 (`Buffer.fill` u16 overflow, `src/stdx.zig`),
  `tui/layout.zig` #44 (`Rect` u16 overflow; lone `.min` larger than span honored), `fmt.zig` #45
  (`Table.render` segfault on alloc failure, `max_width = 0` loop, caps 2^20 config / 2^30 cell, errors
  `InvalidConfig`/`CellTooLong`/`NonFiniteNumber`). Review caught `Csv.init` asserting on user config.
  24: README + CHANGELOG (#46), release PR #47, tag v3.0.0; migration issues zr#178, silica#163,
  zoltraak#141; milestone #19 closed.
- 25-35: Windows-only mindmap runner timeout was a flake; `async_loop` test callbacks off `catch
  unreachable` (#48); `Treemap` NaN/+Inf (#49); plan 002 (#50): off `ArrayList.init` (#52), `zig build
  build-all` compiles every example and benchmark (#53), `zig fmt tests` (#54), metrics stats sort in
  place (#55), `area_chart_test` tightened (#56, #62), `TerminalWidget.render` interprets CSI/SGR via
  `AnsiParseState` (#57), `Pager.withWrap()` (#58; a match straddling a wrap point is not highlighted),
  `metrics_dashboard` "No data" fix (#59), richtext `~~strike~~`/`<u>` (#60), `Editor.init`,
  `MultiCursorEditor.init`, `LocalSource.init` return `error{OutOfMemory}!T` (#61). Cycle 35 counts: 11
  `catch unreachable`, 8 `@panic`, 35 `debug.print`, 13 `while (true)`, 53 files >800, 263 asserts.
- 36-43: v3.1.0 released (#63; consumer issues get one comment, rule: one open issue per consumer). Plan 003
  "Tiger Style bounds and test honesty" (-> v3.2.0) PR #64, owner merged, milestone #65. Item 1 #66
  (`deleteCharAll` shifts cursors via `shiftCursorsLeft`; plan-file tick is easy to miss, fold it into the
  next PR); item 2 #67 `src/tui/line_iter.zig` (`LineIter`, i64 internally) used by six chart widgets;
  item 3 #69 `while (true)` sites bounded (focus/workspace walks, `getResultWithTimeout`, Windows
  `readByteWindows` poll cap), `// top-level loop:` kept in repl.zig and validation.zig worker, tidy
  `unbounded_while` baseline 0; item 4 #70 `tidy.countAssertionFreeTests` (838 assertion-free tests in 115
  files baselined, tidy entries 323 -> 438; helper-based asserts `verify*`/`check*` are invisible to the
  ratchet); item 5 #71 area/bullet tests assert exact cells (`BulletChart` `show_values` never drew text,
  fixed). C40 sunburst PR #68: `resolveNode` never set the top-level index, so `withFocused(n >= 1)` styled
  nothing; weak asserts hide bugs. Latent: the 4 clipped widgets `@intCast` an i32 point to u16 before the
  area check (unreachable today).
- 44: item 6 PR #72 ADR 0001 (paragraph wrap + bidi): stack `RowScratch` 512 columns in
  `paragraph_wrap.zig`, width via `unicode.zig`, `scroll` = visual rows, wrap first then run-based bidi
  (UAX #9 subset), `.word` default, `Paragraph.rowCount(area)` added, `render()` unchanged (MINOR). Architect
  opus ~$2.5 / 12.5 min: brief it to stay under ~5 min. Item 8 also widens `charType`/`detectDirection`/
  `charWidth`.
- 45-47: bug #73 (`Dialog.render` built nonexistent `Paragraph` fields; widget `test` blocks only run if a
  test root imports the file) fixed in #74; bug #75: 33 more widget files do not compile in a test root.
  Probe: `zig test --dep build_options -Mroot=src/sailor.zig -Mbuild_options=/tmp/bo/build_options.zig`
  (stub: `pub const deprecation_mode: []const u8 = "warn";`). Batch 1 PR #76 (canvas, popup, scrollview,
  sparkline, statusbar, tabs; ~$1.3) and batch 2 PR #77 (checkbox, radio, histogram, piechart, heatmap,
  input; ~$1.6) fixed byte-vs-cell advances, u16/u64 overflows, input far-cursor/truncated UTF-8 panics.
  Question #78 asks whether to interleave plan item 7; #75 is not labelled needs-human so it keeps forcing
  STABILIZATION. Known unfixed: StatusBar byte widths; popup.zig:112 >100 cols; BulletChart target == max
  tick; Heatmap `CellMode.numeric` draws blanks; Input draws CJK one cell per codepoint.
- Quirks: global `zig` is 0.15.2, put `/Users/fn/.zr/toolchains/zig/0.16.0` first on PATH every call; stale
  `.zig-cache` gives bogus `FileNotFound` (use `--cache-dir /tmp/sailor-zig-cache`; agents each use their
  own); "failed command: .../test --listen" is noise at exit 0; `zig test src/tui/widgets/X.zig` fails with
  "import outside module path" (probe through `src/sailor.zig` with `--test-filter`); tidy counts BYTES >100
  (multibyte arrows need a wrap), `std.debug.assert(` is banned (alias `const assert = std.debug.assert;`),
  a `function_length` baseline entry may not grow, tidy shows failures only in the summary tail (run `zig
  build tidy`); PR CI ~14 min (Windows 7-10), open the PR by minute ~7; `gh pr checks --watch` hits the 540 s
  tool cap, poll with python `time.sleep` in <=400 s slices; guard blocks Bash containing `cd <repo>`,
  `sleep N; cmd`, `pgrep -c`, `cat >> file <<EOF`, bash writes to citadel (use Write/Edit), `gh` with `cd`;
  zsh has `$pipestatus`, `echo == x` errors; macOS `sed -i` needs `''`, no `timeout`; no ScheduleWakeup in a
  /cycle session; agents running `zig fmt src/tui/widgets/*.zig` touch siblings (fmt only own files).
- Backlog since cycle 0: v2.100.0 "Widget Doc-Comment Audit Round 3" (`terminal.zig` `AnsiParseState`,
  `pager.zig`, `metrics_dashboard.zig`/`richtext.zig`, `paragraph.zig` last); stale-doc and 52-files->800-
  lines hygiene tracked in STATE.md.
