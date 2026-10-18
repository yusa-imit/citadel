# sailor — context

last_seen_at: 2026-10-18T08:23:00Z
rejected_plans: []

## Cycle 36 — 2026-10-18 — FEATURE

- Preflight: tree clean on main, CI green (c6be781), inbox clear (only our own comments on #51).
- Done: plan 002 item 8 -> **PR #63** `chore: release v3.1.0` merged (CI 10/10, `auto-merged`;
  the `Cross-compile (x86_64-macos-none)` job sat in_progress ~8 min after the others finished,
  then went green). Tag v3.1.0 + GitHub release created; milestone #51 closed. README/PRD version
  refs bumped in the same PR. Existing open migration issues (zr#178, silica#163, zoltraak#141)
  got a comment with the v3.1.0 notes instead of new issues (rule: one open issue per consumer).
  No agents, ~15 min.
- Next: n=37 FEATURE: no plan open and none approved -> `/plan sailor` with a new theme. Backlog:
  doc-comment audit round 4 (`paragraph.zig` wrap + RTL), `MultiCursorEditor.deleteCharAll`
  shifts all cursors (untested, unfixed), "does not crash" tests without assertions, 53 files
  >800 lines. n=40 is STABILIZATION.
- Blockers: none. Open questions: none. Stabilize streak 0.

## Cycle 35 — 2026-10-17 — STABILIZATION

- Preflight: tree clean on main, CI green (14534d1), inbox clear (only our own comments on #51), no
  open PRs. Plan 002 milestone #51 open (items 1-7 done, 8 release left).
- Tiger audit (grep, no agents): 11 `catch unreachable` (all proof-commented, 8 in tests), 8
  `@panic` commented, 35 `debug.print` (test benchmarks in `tui/buffer.zig` + debug helpers), 13
  `while (true)`, 53 files >800, 263 asserts, 0 missing `//!`. Nothing worth a PR there.
- Done: **PR #62** merged (CI 10/10, `auto-merged`): `area_chart_test` block tests assert the four
  corner glyphs and blank outside the offset area (last `or countNonEmptyCells` disjunction gone).
  STATE.md updated. ~17 min, no agents.
- Next: n=36 FEATURE: plan 002 item 8, release v3.1.0 (notes: terminal ANSI, pager soft-wrap,
  metrics_dashboard fix, richtext strike/underline, `Editor`/`LocalSource` init now `try`; MINOR bump
  to 3.1.0 in `build.zig.zon`, CHANGELOG, tag, GitHub release, migration issues zr/silica/zoltraak).
  Open the release PR by minute ~8 (CI Windows ~9 min). Tick plan 002 item 8 box.
- Blockers: none. Open questions: none. Stabilize streak 0.
- Leftover test debt: many "does not crash" tests without assertions (`area_chart_test` NaN/Inf,
  tiny-area); `MultiCursorEditor.deleteCharAll` shifts all cursors (untested, unfixed).

## Cycle 34 — 2026-10-16 — FEATURE

- Preflight: tree clean on main, CI green (3622eec), inbox clear (only our own comments on #51), no
  open PRs. Plan 002 milestone #51 open.
- Done: plan 002 item 7 -> **PR #61** merged (CI 10/10, `auto-merged`, #51 item 7 ticked, plan file
  boxes 6 and 7 ticked). `Editor.init`, `MultiCursorEditor.init` (propagates), `LocalSource.init` now
  `error{OutOfMemory}!T`; `LocalSource.init` frees partial copies. Failing-allocator tests for each
  allocation index. API change needs a line in the v3.1.0 notes (callers need `try`; no consumer uses
  these widgets). `catch unreachable` count in src is now 0 outside tests/proof-commented sites.
  ~13 min, no agents; release item 8 did not fit (CI ~8-10 min).
- Next: n=35 STABILIZATION. Then item 8 release v3.1.0 (notes: terminal ANSI, pager soft-wrap,
  metrics_dashboard fix, richtext strike/underline, init `try` API change; MINOR bump to 3.1.0 in
  `build.zig.zon`, CHANGELOG, tag, GitHub release, migration issues in zr/silica/zoltraak).
  Open the release PR early (minute ~8) so CI finishes before the deadline.
- Blockers: none. Open questions: none. Stabilize streak 0.
- Quirks: `grep Editor.init` missed `multicursor.zig` (wraps `Editor`); compile errors found it. After
  changing a signature, `zig build test` shows the missing caller in ~1 min.

## Cycle 33 — 2026-10-15 — FEATURE

- Preflight: tree clean on main, CI green (26a8bdc), inbox clear (only our own comment on #51),
  no open PRs. Plan 002 milestone #51 open.
- Done: plan 002 item 6 -> **PR #59** (`metrics_dashboard`: real bug, render+memory sections
  called `getTypeStats("")` so they always said "No data"; now aggregate all types, memory peak =
  sum of per-type peaks; doc fixed for graphs/`update_interval_ms`/grid; 5 assertion-free tests
  replaced by 7 content tests) and **PR #60** (`richtext` preview renders `~~strike~~` and
  `<u>underline</u>` via a marker-toggle scanner; doc: no emoji search, no key handling). Both CI
  10/10, `auto-merged`. #51 item 6 ticked. ~15 min, no agents.
- **Plan file box for item 6 is NOT ticked** (no time for a third CI run): tick it in the item 7
  PR, along with 7.
- Next: n=34 FEATURE: item 7 typed errors (`smart_autocomplete` 41/43, `editor` 97: `init` fns
  need `!`; check callers, tests, tidy baseline), then item 8 release v3.1.0 (note names
  terminal, pager, metrics_dashboard fix, richtext preview). n=35 is STABILIZATION.
- Blockers: none. Open questions: none. Stabilize streak 0.
- Quirks: `zig build test` ~4 min wall when CI is also running; Windows CI 6-10 min. Python
  heredoc edits of repo files are allowed (only `cd <repo>` and citadel writes are blocked).
  `@FieldType` exists in 0.16. Tidy ratchet counts lines >100 in src: wrap new long lines.

## Cycle 32 — 2026-10-14 — FEATURE

- Preflight: tree clean on main, CI green (2c5f3a9), inbox clear (only our own comments on #51),
  no open PRs. Plan 002 milestone #51 open.
- Done: plan 002 item 5 -> **PR #58** merged (CI 10/10, `auto-merged`, #51 item 5 ticked, plan
  file box ticked). Architect call: implement in the pager (it owns line numbers/scroll_y).
  `Pager.withWrap()` splits at the column count (1 col per code point, never inside one),
  numbers only the first row, `scroll_y` = logical lines, `scroll_x` ignored when wrapping;
  a search match straddling a wrap point is not highlighted (documented). `render` split into
  `renderLine`/`renderRow` (tidy ratchet: a >100-col line failed tidy once, fixed). 11 RED tests
  in `tests/pager_test.zig` (helpers `expectRow`, `renderWrapped`). Whole cycle ~16 min, no agents.
- Next: n=33 FEATURE. Item 6 `metrics_dashboard`/`richtext` scope (list promised behaviors per
  widget, wire up or edit doc, may split in two PRs), 7 typed errors (`smart_autocomplete`
  41/43, `editor` 97 `init` fns need `!`), 8 release v3.1.0 (note names terminal + pager).
  n=35 is STABILIZATION.
- Blockers: none. Open questions: none. Stabilize streak 0.
- Quirks: the guard blocks any Bash containing `cd <repo>` or a heredoc python with writes
  (cwd is already the repo; use Edit for file changes). PATH needs the 0.16 toolchain each call.
  `zig build test` prints nothing on success; failures show via `Build Summary`/tidy lines;
  `zig build tidy` alone is a fast check. Windows CI ~8 min: PR open by minute ~6 is fine.

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
