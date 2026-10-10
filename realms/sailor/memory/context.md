# sailor — context

last_seen_at: 2026-10-09T00:00:00Z
rejected_plans: []

## Cycle 27 — 2026-10-09 — FEATURE

- Preflight: tree was dirty on `fix/unbuilt-arraylist-sweep` (cycle 26's unfinished item 1); preserved
  as `wip/fix-unbuilt-arraylist-sweep-20261009` (pushed, keep). Plan 002 (#50) merged; milestone
  issue #51 already open. Inbox clear (only our own comment); CI green.
- Done: item 1 finished on `fix/unbuilt-arraylist-sweep-2` -> **PR #52** (milestone 002 item 1).
  Eight widgets + `grapheme.wrapText`, `term/windows.parseAnsiSegments` (returns `.empty` list,
  caller `deinit(allocator)`), `clipboard_demo`, `large_data_bench` callbacks off
  `ArrayList.init`; widgets added to the `tui` test root; `widgets/text_clip.zig` helper. Fixed
  `MultiCursorEditor.insertCharAll` cursor shift (shifted left-of-insert cursors, not right-of).
  `deleteCharAll` has the same class of bug (shifts all cursors by 1), untested, NOT fixed: put
  it in plan 003 or fix when touching multicursor.
- Update after the report: #52 CI went 10/10 green; squash-merged, labelled `auto-merged`, item 1
  ticked in #51. The plan file's own checkbox for item 1 is still unticked: tick it in item 2's PR.
- Next: n=28 FEATURE. Item 2 (CI builds examples/benchmarks,
  `zig fmt --check` on Linux job). Item 3 (fmt `tests/`) must wait until no other PR is open.
- Blockers: none. Open questions: none.
- Quirks: global `zig` is 0.15.2, put `/Users/fn/.zr/toolchains/zig/0.16.0` first on PATH or
  every result is bogus. Do NOT run `zig fmt` over `tests/` outside item 3 (touches 69 files).
  macOS `sed -i` needs `''`; no `timeout` binary; `gh pr checks --watch` hits the 540s tool
  limit (CI Windows ~9 min, cross-compile jobs queue late), so open the PR by minute ~8.
  `ChunkedBuffer.LineCallback` is declared with an `anytype` writer (odd API, left alone).

## Cycle 26 — 2026-10-07 — FEATURE

- Plan 002 "post-v3 cleanup" proposed, PR #50 (branch `plan/002-tails-and-hygiene`), awaiting
  merge. Scope: 9 files still on `ArrayList(T).init` (8 widgets + `term/windows.zig:554`), CI
  compiling examples/benchmarks + `zig fmt --check`, fmt of 69 `tests/` files, doc-comment audit
  tail (terminal, pager, metrics_dashboard/richtext), typed errors for 4 non-provable
  `catch unreachable` sites; MINOR v3.1.0. Inbox clear; CI green; no open issues/PRs before it.
- Next: n=27 FEATURE. If #50 still open -> one `/stabilize --one` task; if merged -> open
  milestone issue for 002 and implement item 1.
- Quirk: guard blocked `cd /Users/fn/codespace/sailor; ...` (cwd already the repo; run git with
  no cd). `gh run list --branch main` returned a headSha != origin/main again; trust `-R` runs.

## Cycle 25 — 2026-10-06 — STABILIZATION

- Done: main @ a1772f8 was red (Windows only: `mindmap_tests` "test runner failed to respond for
  1m", Linux/macOS green); rerun of the failed job went green, so a flake, no code cause found
  (mindmap loops are bounded). Inbox clear. Tidy counts: 12 bare `catch unreachable`, 8 `@panic`,
  35 debug.print, 13 `while (true)`, 53 files >800, 229 asserts. Test-quality audit: 6
  `expect(true)` (all treemap NaN/Inf), 0 weak `or` disjunctions.
- PRs merged (CI 10/10): #48 `async_loop` 5 test callbacks record success in the flag instead of
  `catch unreachable` (baseline 332->331 lines); #49 fix `Treemap` blanking whole widget when one
  item is NaN/+Inf (items weigh 0 unless finite and positive; negatives now weigh 0 too), six
  `expect(true)` tests assert rendered output.
- Next: n=26 FEATURE, no plan open -> `/plan` 002 (doc-comment audit round 3 backlog, 8
  orphaned widgets on `ArrayList(T).init`, ~78 files not fmt-clean, 52 files >800 lines). Remaining
  bare `catch unreachable`: event_metrics 181,248; render_metrics 186,255; smart_autocomplete
  41,43; editor 97 (need typed-error redesign or proof).
- Blockers: none. Open questions: none. Stabilize streak 0.
- Quirks: `gh` calls with `-R` must not share a Bash call with `cd <repo>` (guard hook blocked);
  a subagent with `isolation: worktree` is blocked by guard_write (path contains `.claude`), so
  do small edits in the main checkout. `gh run list --branch main` without `-R` returned stale
  runs once; use `-R yusa-imit/sailor`. No `zig build test -Dtest-filter`; probe via a temporary
  test + full run (~50s). Stray empty local branch `test/treemap-nonfinite-assertions` left.

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
