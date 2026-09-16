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

## Stabilization update (2026-09-09, cycle 5)

- `zig build tidy`: **0 findings** (was 9 — 8 line-length, 1 missing `//!` header), fixed via
  PR #7. `test_step` now hard-depends on the repo-wide tidy scan, not just its own unit tests —
  plan 001 item 4 done (4/11).
- Remaining findings from this cycle's `tidy-auditor` sweep, not yet fixed (smallest-diff item
  already taken this cycle; these carry forward):
  - `tools/tidy.zig` (1274 lines) is exempt from its own file-length and `//!`-doc-header
    checks — `scan_roots` only walks `src/bench/tests`, and `checkDocHeader` hard-scopes to
    `src/`-prefixed paths. Not a violation of any rule as currently written, but a scope gap
    worth closing before `tools/` grows further.
  - `tools/tidy.zig`'s directory walk (`walkDir15`/`descendDir15`, and the 0.16-variant pair)
    is mutually recursive with no explicit depth bound — low real risk (shallow repo trees)
    but violates the "no recursion, explicit bounded stack" rule literally.
  - `tidy_baseline.txt` is tracked at repo root, outside `citadel/protocol/DOCS.md`'s allowed
    root-file list; candidate fix is moving it under `tools/` (touches `build.zig.zon` `.paths`
    and any relative-path read in `tools/tidy.zig` — verify before moving).
  - 2 `catch unreachable` in `tools/tidy.zig` (lines ~199, ~201) are provably safe (buffer
    sized via a preceding `assert`) but lack the `// proof:` comment the rule wants.
- `src/` is still stub-stage: 0 real functions outside `main.zig`, so assertion-density and
  most Tiger Style function-level checks remain not-yet-applicable (see "Known gaps" above).

## Stabilization update (2026-09-12, cycle 10)

- `tidy-auditor` re-swept `tools/tidy.zig` (now 1770 lines, up from 1274 at cycle 5) plus a
  fresh full pass (`@panic`, `std.debug.print`, `while (true)`, function/file length, `usize`
  in wire formats, missing `//!`, `std.time.*`/`std.crypto.random` in `src/`) — all fresh checks
  read 0, consistent with `src/` still being stub-stage.
- Fixed the cheapest of the 4 carried-forward findings: `isWireFormatPath`'s second
  `catch unreachable` (the `dir_prefix` bufPrint) had no `// proof:` comment of its own — the
  shared comment above the first call didn't cover it, since `hasProof` only checks the
  same/previous line. `catch_unreachable`'s `banApplies` is unconditionally true (not gated by
  `isUnderSrc` like most rules), so this file is bound by its own rule even though the repo-wide
  scan doesn't walk `tools/` yet. Fixed via PR #14 (squash-merged, CI 8/8 green) with a pinning
  test mirroring the real function body against `checkBanList`, verified red before / green after.
- Remaining 2 carried-forward findings, still not fixed (next stabilization cycle candidates,
  ordered smallest-diff-first per the auditor):
  1. `tools/tidy.zig` exempt from its own file-length (now 1770 lines, >2x the 800-line limit)
     and `//!`-header checks: `scan_roots` (`tools/tidy.zig:938`, was ~938) only walks
     `src/bench/tests`; `checkDocHeader` (`tools/tidy.zig:271`) hard-scopes to `src/`-prefixed
     paths. Adding `"tools"` to `scan_roots` will immediately surface tidy.zig's own
     801+-line overage — needs a baseline entry or a follow-up split in the same PR, so this is
     a bigger diff than it looks.
  2. Unbounded mutual recursion in `walkDir15`/`descendDir15` (`tools/tidy.zig:948`/`965`) and
     the 0.16-variant pair `walkDir16`/`descendDir16` (`tools/tidy.zig:1068`/`1086`) — needs a
     `depth: usize` parameter threaded through all four functions plus a bounded-recursion test.
     Largest diff of the remaining two; low real risk given the repo's shallow tree.

## Stabilization update (2026-09-15, cycle 13)

- Fixed carried-forward finding 1 of 3: `tidy_baseline.txt` moved from repo root to `tools/`
  (was outside `citadel/protocol/DOCS.md`'s allowed root-file list). `tools/tidy.zig`'s
  `Options.baseline_path` default now `"./tools/tidy_baseline.txt"`; pinning test updated
  (verified red before the code change, green after). PR #18, CI 8/8 green, squash-merged.
  No behavior change — the baseline is opened relative to `opts.root` (always the repo root),
  not process cwd, so this was purely a path-string move.
- Local toolchain note: `~/.zr/toolchains/zig/0.16.0/zig` was present and working this cycle
  (cycle 12's "missing toolchain" note did not reproduce) — `zig build test` ran fully locally.

## Stabilization update (2026-09-16, cycle 15)

- CI: last 5 completed runs on main all green; no red CI, no open bug issues — FEATURE mode
  (periodic_stabilization is off for sigil; `n % 5` trigger doesn't apply).
- Inbox: merged PR #19 (bounded `tools/tidy.zig` dir-walk recursion, `dir_depth_max=64`) — CI
  went fully green (8/8, including the previously-pending cross-compile matrix and the
  Linux-skip on the depth-bound regression test) since last cycle's report. Plan PR #17
  (plan 002, Phase 1A) still open, no new OWNER activity.
- Plan PR open → ran one bounded stabilization task. Re-verified the sole remaining
  carried-forward finding (tidy.zig self-exempt from its own file-length/function-length/
  ban-list checks) rather than attempting it: file is now **1860 lines** (up from 1798 at
  cycle 14, +62 from the recursion-bound PR). Manual scan of what adding `"tools"` to
  `scan_roots` would surface: 2 lines > 100 cols, ~61 `fn`/`pub fn` declarations (many almost
  certainly > 70 lines, none baselined), and `checkBanList`'s path-unconditional rules
  (`catch_unreachable`, `eq_error`/`neq_error`, `usingnamespace_kw`, `fixme_comment`, `dbg_call`)
  would run against tidy.zig's own source for the first time — 15 raw substring hits to
  triage for false positives (string literals describing the patterns, e.g. rule messages
  that mention `@panic(` as text) before any real count is known. The 2 real `catch
  unreachable` calls (in `isWireFormatPath`) already carry proof comments (PR #14) and are
  not a factor. This confirms the finding is a genuinely large diff (baseline entries or a
  file split, plus false-positive triage on the ban-list hits), not a ≤10 min task — no
  smaller candidate finding exists elsewhere (test quality and docs drift are both
  not-yet-applicable at stub stage per "Known gaps" above; hygiene, `.gitignore`, and
  dependencies all re-checked clean this cycle).
- No PR opened this cycle's stabilization slot — genuinely nothing smaller to fix. Candidate
  for a future **non-`--one`** stabilization cycle (or its own plan item) given the size.

## Stabilization update (2026-09-17, cycle 16)

- CI: last 5 completed runs on main all green (HEAD 42f5a4f). No open bug issues, no new OWNER
  activity on plan PR #17 since the cycle 15 watermark — FEATURE mode, one bounded stabilization
  task per §2 of the cycle protocol.
- Fresh `tidy-auditor` sweep (via `zig build tidy` on the 0.16.0 toolchain, plus manual grep for
  `catch unreachable`/`@panic`/`std.debug.print`/`while (true)`/`FIXME`/`dbg(`/function-length/
  file-length/`usize`-in-wire-structs/`//!` headers/hygiene/docs drift): **0 findings, nothing
  new**. `src/` totals 719 lines (largest file `config.zig` at 264), well under the 800-line
  limit; no function exceeds 70 lines. Root hygiene, `.gitignore`, and `build.zig.zon`
  dependencies all re-checked clean.
- The sole carried-forward finding (`tools/tidy.zig`, now past 1860 lines, self-exempt from its
  own file-length/function-length/ban-list checks) was deliberately not re-investigated this
  cycle — already confirmed too large for `--one` across cycles 15 and 16. No PR opened.

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
