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
  0 failures, ~47s wall / 144s CPU.
- CI: GREEN as of 2026-09-09 (main @ `2989cb4`, PR #24 merged — added the unproven-`@panic`
  tidy check and proof-commented all 8 existing sites). Linux x86_64 / macOS ARM64 (macos-15
  pinned) / Windows x86_64 native tests + 6-target cross-compile. `paths-ignore` skips
  `.claude/memory`, `docs/`, `*.md`.
- Open issues: #19 (milestone 001 tracking, 3/12 checked). Open PRs: #30 (`pipeline.zig`
  `catch_unreachable` proof-comment fix, CI running at cycle end — next cycle's inbox merges
  when green).

## Tiger Style gaps

As of 2026-09-12 (cycle 10 tidy-auditor re-check, pre-PR #30): `zig build tidy` **passes** (446
baseline entries on `main` after PR #29 merged, byte-for-byte diffed clean against a fresh
regeneration — zero drift) — `catch_unreachable`, `panic`, `debug_print`,
`usize_in_wire_format`, `missing_header`, `function_length`, `line_length`, `time_usage`, and
`crypto_random` are tracked with a shrinking baseline in `build_support/tidy.zig` /
`tidy_baseline.txt`. `while (true)` and file length (>800 lines) are still untracked by tidy —
both need per-site/per-file judgment, not a mechanical sweep.

| Check | Count | Tracked by tidy? | Note |
|---|---|---|---|
| `catch unreachable` | 28 raw (22 across 9 files pre-PR#30; drops by 2, `pipeline.zig`'s entry removed entirely, once #30 merges) | yes | `eventbus.zig` (PR #27), `countdown_timer.zig` (PR #29), `pipeline.zig` (PR #30, open) proof-commented; rest have proof comments already |
| `@panic` | 0 unproven (8 total, all now proof-commented) | yes | fixed cycle 5 preflight via PR #24 |
| `std.debug.print` | 34 raw (6 baseline entries) | yes | all inside test blocks / debug helper modules |
| `std.crypto.random` | 1 (1 baseline entry) | yes | fixed cycle 5 via PR #25 (`llm_client.zig` jitter; tracked-not-fixed, like `time_usage`, pending Io/PRNG migration) |
| `while (true)` (unbounded) | 13 | no | 6 geometry-bounded (Bresenham), 2 wall-clock-timeout-bounded, 2 array-traversal-bounded, ~2-3 plausibly-legitimate top-level loops (`repl.zig:198`, `validation.zig:441`) |
| Files > 800 lines | 52 | no | worst: `layout.zig` 3002, `style.zig` 2223, `tooltip.zig` 2094, `sixel.zig` 1864, `multicursor.zig` 1850 |
| Functions > 70 lines | 122 baseline entries | yes | `build.zig:build` 1954, `docgen.zig:parseFunctionDeclaration` 360, `arg.zig:Parser` 312 |
| `usize` in wire format | 4 file entries | yes | see `tidy_baseline.txt`; `termcap.zig:33-35` is the clearest genuine wire-format risk |
| Missing `//!` header | 86 | yes | e.g. `accessibility.zig`, `aria.zig`, `bidi.zig` |
| `assert(` density | 9 total across ~4700+ `fn` in `src/` | no | Tiger Style's "≥2 per function" is essentially unmet kingdom-wide here; needs per-function judgment, not mechanical |

Smallest-diff-first recommendation for the next stabilization cycle: `event_metrics.zig`/
`render_metrics.zig`'s 4 `catch_unreachable` sites are genuinely NOT provable (caller-supplied
general allocator, real OOM possible) — a real fix needs the call to return a typed error, not a
proof comment; do not paper over with a false claim. `//!` headers on the 86 missing files
(purely additive, zero risk, can split by directory) is next in line for a purely mechanical
target. `while (true)` and the 52 over-800-line files stay deferred — both need per-site/
per-file judgment calls. Repo-wide `zig fmt --check` pre-existing-failure count: 83 → 82 after
PR #29 (`countdown_timer.zig` cleaned incidentally), → 81 on PR #30's branch (`pipeline.zig`
cleaned incidentally by the repo's zig-fmt hook while editing the file) — a side effect of
touching flagged files, not a dedicated fmt pass; still 81 files away from repo-wide clean.

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
