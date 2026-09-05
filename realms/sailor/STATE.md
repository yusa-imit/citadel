# sailor — STATE

Survey date: 2026-09-05 (citadel restructure). Sources: repo survey + Zig 0.16 breakage probe.

## What exists (claimed vs present)

Present and real: full CLI layer (term/color/arg/repl/progress/fmt), a large TUI core under
`src/tui/` (buffer, layout, style, flexbox, grid, sixel/kitty/iterm2, async loop, router,
keybinding, mouse/touch/gamepad, syntax highlighting, inspector), 140 widget files, plus a long
tail of utility modules (a11y, clipboard, fuzzy, unicode/bidi, llm_client, state_persist, store/
thunk/middleware). `src/testing/` has mock terminal, snapshot, property, visual regression. 173
`addTest` steps in `build.zig`; local `zig build test` passes with 0 failures.

Claimed vs present gap: `README.md` is stale — still describes "v0.1.0..v1.8.0", "40+ widgets",
"720+ tests", and a "Network & Async (HttpClient, WebSocket, ...)" module that isn't a real
top-level module. `docs/PRD.md` header still says "Version: 0.1.0". `CLAUDE.md`'s repo map still
says "17 widgets". Actual: v2.99.0, 140 widget files, ~13.9k test blocks. All 6 original PRD
phases are done; ~444 autonomous cron sessions have run since v1.0, adding widgets and closing a
recurring "doc comment promises X, `render()` never wired it" gap class (current milestone
v2.100.0, round 3 of this audit). No `CHANGELOG.md` — release notes live only in
`docs/milestones.md`.

## Sizes

| Metric | Value |
|---|---|
| `src/` LOC | 150,321 |
| Test count (estimate) | 13,926 |
| Files > 800 lines | 52 (worst: `layout.zig` 3002, `style.zig` 2223, `tooltip.zig` 2094) |
| Widget files | 140 |
| `tests/*_test.zig` | 178 |
| `examples/` | 18 |
| `docs/milestones.md` | 224 KB, 2380 lines (doubles as the changelog) |
| `.claude/memory/project-context.md` (pre-restructure) | 75.7 KB, 135 lines (session log) |

## Build / test / CI

- Local (Zig 0.15.2, matches CI pin): `zig build` OK (cached, exit 0). `zig build test`: PASS,
  0 failures, ~47s wall / 144s CPU — including the dirty-tree `timeline.zig` change below.
- CI: GREEN — last 3 runs on `main` all `completed success`. Linux x86_64 / macOS ARM64
  (macos-15 pinned) / Windows x86_64 native tests + 6-target cross-compile. `paths-ignore` skips
  `.claude/memory`, `docs/`, `*.md` (memory-only commits are unverified by CI — acceptable).
- Open issues: none. Open PRs: none.

## Tiger Style gaps

| Check | Count | Note |
|---|---|---|
| `assert` | 9 | Across 150k LOC — essentially no precondition checking |
| `catch unreachable` | 28 | Violates the repo's own "no catch unreachable" rule |
| `@panic` | 8 | 7 inside `clipboard.zig` GPA-leak tests, 1 real (`stack_trace.zig:30`) |
| `std.debug.print` | 34 | In debug/bench/test helpers, not render paths — still shipped |
| `while (true)` (unbounded) | 13 | Bresenham/line-drawing loops, terminal reads, focus cycling |
| Files > 800 lines | 52 | vs. the 500-line target in the old `CLAUDE.md` |
| Functions > 70 lines | ~105 (sample) | `repl.zig:handleKey` 275, `waterfall_chart.zig` 232 |

Also noted: 14 widget files allocate inside `render()` (138 `ArrayList`/alloc references across
widgets); recursion with no explicit depth limit in docgen's directory walk, `layout_intelligence`
child traversal, the inspector visitor, and tree/mindmap/DAG-style widgets; unbounded-growth
`ArrayList`-backed logs/feeds (activity feed, log viewer, chunked buffer, history) not measured
in depth.

## Zig 0.16 probe summary

- `zig015_build_ok`: ok. 0.16.0: `build.zig` needs exactly **one** fix
  (`Compile.linkLibC()` removed → `compile.root_module.link_libc = true`); applied only in a
  scratch copy, not the tracked repo. After that fix, `zig build` (install step) succeeds with
  no further `build.zig` errors — `build.zig.zon` has zero `.dependencies`, so this migration is
  **not blocked** on zuda/sirocco landing first.
- **Error count**: 368 (via `zig test src/sailor.zig`, the library root — a better single-number
  proxy than any one test target, since each test unit stops at its own first error).
- **Error classes** (by count): `std.io` namespace removed / new `std.Io` interface — 155 (>40%
  of all errors; the dominant, architecturally different rewrite — threading an `Io` capability
  through file/dir/writer/reader call sites, not a pure rename); `ArrayList` init literal missing
  `capacity` field — 115 (mostly mechanical, `.{}` → `.empty`/init-call, concentrated in a few
  files like `arg.zig`); `ArrayList.writer()` removed — 25; `std.time.Timer`/timestamp APIs
  removed — 21; `std.heap.GeneralPurposeAllocator` removed — 14 (→ `DebugAllocator`);
  `std.process.getEnvVarOwned`/`std.posix.getenv` moved — 14;
  `std.Thread.Mutex` → `std.Io.Mutex` — 6; `std.fs.Dir`/`File` now needs an explicit `Io` param
  — 4; `std.posix.isatty` and other posix surface changes — 4.
- **Effort**: medium (2–5 sessions). `build.zig` + easy renames (GPA/Mutex/env/time): ~1 session.
  `ArrayList`-literal mechanical sweep (sed-able once the 0.16 idiom is confirmed): 1–2 sessions.
  `std.io` → `std.Io` rewrite (real design work, not a rename; care needed in `hotreload.zig`,
  `fmt.zig`): 1–2 sessions. Per `citadel/docs/ROADMAP.md`, sailor's migration is a **MAJOR** bump
  to v3.0.0 (368 errors + `linkLibC`), same tier as zuda; zr/silica/zoltraak wait on it.

## Docs / root hygiene (hygiene PR will fix)

- Tracked build artifacts in git root: `test` (0 bytes), `test_escapes` (1.2MB Mach-O),
  `test_parser` (1.2MB Mach-O), `test_output.txt` (0 bytes), `test_raw_string` (0 bytes),
  `verify_parser` (0 bytes) — `.gitignore`'s `test_*` pattern misses the bare names `test` and
  `verify_parser`. Also untracked-but-present junk: `.DS_Store`, ~16 `lib*.a` files, a dozen
  ad-hoc `test_*`/`*_test` binaries (3 more 1.2MB Mach-O), `.zig-cache/`.
- `AUDIT_DOC_COMMENTS.md` at repo root (v1.27.0 doc-comment audit report) — move into `docs/` or
  drop as superseded by `docs/milestones.md`'s own audit-round history.
- `docs/API.md`, `docs/PRD.md`, `README.md` are stale relative to code (see "Claimed vs present"
  above) — a STABILIZATION cycle should reconcile them or flag them for a docs pass.
- Old `.claude/` carried repo-unique memory (`filebrowser_test_design.md`, `zig-015-compat.md`)
  now migrated into `citadel/realms/sailor/memory/`; stale one-off snapshots (`session-48.md`,
  `session-94.md`) and a stray `scratchpad.zig.md` were dropped, not migrated.
- Per kingdom docs policy (`citadel/protocol/DOCS.md`), the repo should end up holding only code
  and `docs/` — no `CLAUDE.md`, no `.claude/` — once the hygiene PR lands.

## Next work candidates

1. Root hygiene PR: `git rm --cached` the tracked test binaries, move/drop
   `AUDIT_DOC_COMMENTS.md`, fix `.gitignore` (bare `test`, `verify_*`, `*.log`).
2. Decide the `wip/timeline-description-rendering` branch (finish committing the green
   description-rendering work, or discard) before starting new feature work.
3. Plan `001`: Zig 0.16 migration (MAJOR → v3.0.0) plus a Tiger Style assertion baseline for the
   hottest modules (`term`, `arg`, `tui/buffer`, `tui/layout`).
4. Finish the v2.100.0 doc-comment audit: `terminal.zig` `AnsiParseState` wiring, `pager.zig`
   soft-wrap, `metrics_dashboard.zig`/`richtext.zig` scope decisions, `paragraph.zig` word/char
   wrap + RTL/bidi (architect pass, do last) — then bundle the v2.100.0 release.
5. Refresh `README.md` and `docs/PRD.md` version/feature claims to match v2.99.0 reality.
6. Split the worst offenders among the 52 files over 800 lines toward the 500-line target.
