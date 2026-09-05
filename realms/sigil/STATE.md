# sigil — State survey (2026-09-05)

## What exists (claimed vs present)

- **Claimed** (README module table, `CLAUDE.md`): a working Value IR + reflection library
  covering JSON/JSONPath/Pointer/Patch, TOML, YAML, MessagePack, CBOR, Protobuf, CSV, and a
  layered config loader.
- **Present**: nothing functional. 2 commits total (bootstrap + a CI fix). All 10 top-level
  modules (`core`, `reflect`, `json`, `path`, `toml`, `yaml`, `msgpack`, `cbor`, `proto`,
  `csv`) are identical ~19-26 line stubs: doc comment + `Error = error{NotImplemented}` +
  one trivial compile-check test. Their planned submodule directories exist but are empty
  (zero files). `src/config.zig` is likewise a stub. `src/root.zig` re-exports the 10 stubs
  plus `sigil.version`. `src/main.zig` (36 lines) is the only real code: a version/--help
  CLI, with 1 real test.
- `docs/milestones.md` is honest: every checkbox in Phases 1-6 is unchecked, current phase
  is "Bootstrap complete -> Phase 1 starting". `docs/PRD.md` (192 lines) is design-only.
  README's module table is aspirational, not a description of present code.

## Sizes

- **LOC (src)**: 285 total, across 13 `.zig` files.
- **Tests**: 12 test blocks estimated; 11 are "module compiles" / `refAllDecls` placeholders,
  1 is `main.zig`'s real "cli: version is exposed" test. No substantive functional coverage.
- **Files > 800 lines**: 0 (largest file is 36 lines).
- **`bench/main.zig`** exists and is wired into the `bench` build step; no benchmarks written.
- **`examples/`, `tests/`**: `.gitkeep` only.

## Build / CI

- `zig build`: succeeds (exit 0).
- `zig build test`: succeeds (exit 0), all 12 tests pass, completes in well under 3 minutes
  (effectively instant given the code size).
- CI (`gh run list`, 2 runs total — brand new repo): HEAD ("ci: run tests on Linux only;
  macOS covered by cross-compile") -> success, 1m2s. Prior run, the original bootstrap
  commit's CI -> failure, 41s, fixed same-day by the next commit. **Current HEAD CI is green.**
- Open issues: none. Open PRs: none.

## Tiger Style gap table

| Metric | Count | Note |
|---|---:|---|
| `assert` | 0 | no logic exists yet to assert over |
| `catch unreachable` | 0 | " |
| `@panic` | 0 | " |
| `std.debug.print` | 0 | " |
| unbounded `while (true)` | 0 | " |
| files > 800 lines | 0 | largest file is 36 lines |
| functions > 70 lines | not measured | too small to be meaningful yet |

All-zero is a **non-finding due to project stage**, not a clean bill of health — 285 LOC of
stub files has no hot loops, recursion, or allocation to critique. Re-audit once Phase 1-2
(core/json) land real parsing code.

## Zig 0.16 probe summary

- **Zig 0.15.2 build**: OK (exit 0). **Zig 0.16.0 build**: fails at stage (c) source compile
  — `build.zig` itself (stages a/b) is fine.
- **Error count**: 1. **Error class**: `std.heap.GeneralPurposeAllocator` removed in 0.16,
  hit at `src/main.zig:7`. Fix pattern: swap for `std.heap.DebugAllocator(.{})` (or
  `smp_allocator` / `page_allocator` depending on desired semantics) and update the
  `.deinit()` call site.
- **Effort estimate**: trivial, under 1 hour.
- **Blocking dependencies**: none (foundation layer, zero `.dependencies`).
- **Scope of exposure**: only 1 of 13 `.zig` files (`src/main.zig`) touches any fs/net/
  thread/time/process-adjacent std API. `zig test src/root.zig` — the entire library
  surface (core/json/path/toml/yaml/msgpack/cbor/proto/csv/config/reflect) — already
  compiles and passes all 12 tests cleanly under 0.16.0 with zero errors.
- `main.zig` already uses 0.16-shaped APIs in places (`std.fs.File.stdout().writer(&buf)`,
  `.interface`/`.flush()`, the `{f}` format specifier) — it reads as written against a 0.16
  nightly with only the allocator rename missed. Overall: **sigil is essentially 0.16-ready
  already**; the single-line allocator swap is very likely the entire migration.

## Docs / root hygiene (for the hygiene PR)

- Root files are all expected/clean: `.gitignore`, `CLAUDE.md`, `LICENSE`, `README.md`,
  `build.zig`, `build.zig.zon`. No files flagged to remove or move.
- `CLAUDE.md` + `.claude/` (21 tracked files: 6 agents, 8 commands, 5 memory files, 1
  settings.json) are the generic citadel scaffold template with no repo-unique content
  beyond substituted project name — these are slated for removal per kingdom docs policy
  (`citadel/protocol/DOCS.md`); durable content has been carried into this realm's
  `REALM.md` and `memory/` before that happens.
- `docs/PRD.md` and `docs/milestones.md` stay in the repo — they are legitimate `docs/`
  content, not AI-orchestration files.
- Working tree is clean (`git status --short` empty, `git diff --stat` empty) — no
  mid-cycle work to preserve. No `wip/*` branch needed for this repo.
- No committed secrets, no giant files, no build artifacts committed, no divergent version
  numbers — repo hygiene is otherwise clean for an early-stage scaffold.

## Next work candidates (from `docs/milestones.md` / `project-context.md`)

1. Phase 1A — `core/{value,tree,diagnostics}.zig`: `Value` union, arena-owned `ValueTree`,
   `Diagnostics{line,col,message}`; tests for arena release, equality, Map
   insertion-order preservation.
2. Phase 1B — `core/number.zig`: i64/u64/f64 boundary handling, `-0`, exponents, explicit
   overflow errors.
3. Phase 1C — `core/unicode.zig`: UTF-8/escape utilities.
4. Phase 1D — `reflect/{parse,stringify,options}.zig`: comptime struct<->Value mapping,
   field rename/defaults/deny-unknown-fields options.
5. Phase 2A-2C (after Phase 1) — `json/{scanner,dom,writer}.zig`: RFC 8259 pull scanner,
   DOM builder, pretty/minify writer.
6. Housekeeping: populate the empty performance-targets table in `docs/milestones.md` and
   `docs/PRD.md` §5 once any module is benchmarkable.
