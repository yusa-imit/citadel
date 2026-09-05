# sailor — Realm

| | |
|---|---|
| Layer | library |
| Path | `/Users/fn/codespace/sailor` |
| GitHub | `yusa-imit/sailor` |
| Version | 2.99.0 (`build.zig.zon`) · latest tag v2.99.0 (matches; 7 unreleased commits on main) |
| Zig | 0.15.2 (migrating to 0.16.0 under plan `001`; see `citadel/docs/ROADMAP.md`) |
| Depends on | none (zero-dependency library; `build.zig.zon` has no `.dependencies`) |
| Consumers | zr, silica, zoltraak |
| blocked_by | — |
| cycle_minutes_max | 22 |
| test_command | `zig build test` takes ~50 s locally; run at most twice per cycle |
| CI | Linux tests + macOS ARM64 (macos-15 pinned) + Windows + 6 cross-compile targets |

## What it is

Zero-dependency Zig 0.15.x TUI framework and CLI toolkit: a CLI layer (`term`, `color`, `arg`
with subcommands and did-you-mean, `repl` with history/completion, `progress`, `fmt` table/
JSON/CSV/Plain formatters) plus an immediate-mode, ratatui-style TUI core (buffer, constraint
layout solver, flexbox/grid, theming, sixel/kitty/iterm2 image protocols, async event loop,
input/mouse/gamepad handling) and 140 widget files (charts, editors, file/hex browsers, kanban,
gantt, DAG, timeline, pipeline, and more). 150k LOC, ~13.9k tests. Shared library consumed by
zr, silica, and zoltraak via `build.zig.zon`. All 6 original PRD phases are complete; current
work is a "doc-comment-vs-implementation" audit (v2.97.0–v2.100.0) closing gaps where a widget's
doc comment promises behavior `render()` never wired up.

## Build and test

```bash
zig build              # library + CLI
zig build test         # unit tests (~47s wall / 144s CPU; ~13.9k tests, 173 registered steps)
zig fmt --check src build.zig
```

Local-only: `zig build`, `zig build test`, examples. CI-only: 6-target cross-compile, benchmarks
— except a STABILIZATION cycle (every 5th session, tracked by a session counter), which may run
them locally, sequentially (one target at a time), and only after confirming
`pgrep -f "zig build"` shows no other kingdom repo mid-build: concurrent heavy Zig builds across
sibling repos have triggered kernel panics on this host before.

No ports, no servers — sailor is a client-side library with nothing to kill between sessions.
A `wip/timeline-description-rendering` branch preserves this session's mid-cycle TDD work
(`timeline.zig` renders `TimelineEvent.description`; tests were green, `zig build test` passed
on the dirty tree) from before the restructure — finish or discard it explicitly in the first
post-restructure cycle rather than losing it silently.

## Realm-specific rules

- **Module dependency order** (implement/fix in this order): `term → color → arg → repl →
  progress → fmt → tui`; lower layers never import higher ones.
- **Consumer registry** (never edit these repos directly; changes reach them only via a
  `migration,from:sailor` issue after a release): zr uses `arg`/`color`/`progress` (migrating to
  `tui`); zoltraak uses `arg`/`color`/`repl` (migrating to `tui` for its redis-cli); silica uses
  `arg`/`color`/`repl`/`fmt` (migrating to `tui` for its SQL shell). Every API change must
  consider all three.
- **Release quirks**: version must be exactly the next minor/patch of the current
  `build.zig.zon` value — never skip, never downgrade; check
  `git tag -l 'v*' --sort=-v:refname` before tagging. MINOR only when a milestone checklist is
  fully `[x]`; PATCH for fix-only commits (tag only, no `.zon` bump). After every release, file
  a `migration,from:sailor` issue in each consumer repo.
- **Local test policy**: local sessions run `zig build`/`zig build test`/examples only; the
  6-target cross-compile and benchmarks are CI-only except STABILIZATION cycles (see Build and
  test above), which must also run a test-quality audit (weak `or countNonEmptyCells(...)>N`
  disjunctions, placeholder `expect(true)`, whole-area scans, zero-coverage widgets).
- **zuda-first exceptions**: TUI-specific structures (cell buffer, layout solver, grid, unicode
  width) stay in sailor — `docs/zuda-audit.md` already concluded no migration applies here;
  only genuinely general-purpose structures/algorithms should look to zuda first.
- **API patterns**: immediate-mode rendering, no persistent widget tree, double-buffered diff
  per frame (ratatui-inspired). Widgets are plain structs with
  `render(self, buf: *Buffer, area: Rect)` — no vtables, comptime type checking instead. All
  output goes through a caller-supplied `std.io.Writer` (0.16: `std.Io.Writer`) — never stdout/
  stderr. Builder methods (`withX`) take `self` by value, mutate a copy, return it, enabling
  chaining (`Menu.init(items).withSelected(1).withBlock(block)`).

## Layout

| Module | Files | Notes |
|---|---|---|
| `src/sailor.zig` | 1 | Root module, re-exports everything |
| `src/term.zig` + `src/term/windows.zig` | 2 | Raw mode, key reading, TTY detect; Windows backend |
| `src/color.zig` | 1 | ANSI/256/truecolor, `NO_COLOR` |
| `src/arg.zig` | 1 | Flag/subcommand parser, auto-help, did-you-mean |
| `src/repl.zig` | 1 | Line editor, history, completion, multi-line validator |
| `src/progress.zig` | 1 | Bar/spinner/multi-progress |
| `src/fmt.zig` | 1 | Table/JSON/CSV/Plain result formatters |
| `src/tui/` core (`tui.zig` + ~68 files) | ~69 | Buffer, layout solver, style, flexbox/grid, |
| | | theming, sixel/kitty/iterm2, async loop, input/mouse/ |
| | | gamepad, inspector, router, error recovery |
| `src/tui/widgets/` | 140 | Block/Paragraph/List/Table/Input/TextArea/Tree/Tabs/ |
| | | Dialog, ~50 chart types, editors, browsers, kanban, |
| | | gantt, DAG, timeline, pipeline, tooltip, etc. |
| `src/testing/` + `src/testing.zig` | ~6 | Mock terminal, snapshot, property, visual regression |
| `src/{accessibility,aria,focus,...}.zig` | several | Accessibility and focus management |
| `src/{clipboard,paste,env,signal,...}.zig` | several | Platform/service utilities |
| `src/{eventbus,command,store,thunk,...}.zig` | several | State management |
| `src/{fuzzy,grapheme,unicode,bidi,...}.zig` | several | Text/utility helpers |
| `src/{profiler,bench,render_metrics,...}.zig` | several | Tooling/metrics |
| `src/{llm_client,natural_language_commands,...}.zig` | several | AI/async extras |
| `tests/` | 178 | Standalone `*_test.zig` roots registered in `build.zig` |
| `examples/` | 18 | hello, counter, dashboards, gallery, form/plugin/profile |
| `benchmarks/`, `scripts/` | — | Render benchmark, test-quality audit, migration scripts |

## Known gaps (from STATE.md)

Tiger Style baseline (plan `001` will address): only 9 `assert`s across 150k LOC; 28
`catch unreachable` (violates the library's own no-panic rule); 8 `@panic` (7 in intentional GPA
leak tests, 1 real helper); 34 `std.debug.print` (debug/test helpers, not render paths); 13
unbounded `while (true)` (mostly bounded-by-geometry line-drawing/read loops, no explicit caps);
52 files over 800 lines (rule targets 500; worst: `layout.zig` 3002, `style.zig` 2223); ~105
functions over 70 lines.

Top risks: two 1.2MB test binaries and several zero-byte binaries/logs tracked in git (root
hygiene PR will `git rm --cached` them); `README.md`/`docs/PRD.md` badly stale versus the real
v2.99.0/140-widget/~14k-test state; a green `zig build test` has repeatedly not proven every
widget's tests actually compiled (orphaned-from-analysis-graph bugs found 3 times in memory);
Zig 0.16 migration is a MAJOR bump (v3.0.0) at 368 probe errors, dominated by the `std.io` →
`std.Io` rewrite (155 errors) and the `ArrayList` unmanaged-literal fixup (115 errors).
