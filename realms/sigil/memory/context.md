# sigil — context

last_seen_at: 2026-09-17T15:05:45Z
rejected_plans: []

## Cycle 18 — 2026-09-17 — FEATURE

- Done: preflight clean (main, CI green HEAD 42f5a4f, no bug issues). Inbox: no new OWNER
  activity since watermark (plan PR #17 comments/reviews, repo-wide PR/issue comments) —
  nothing to action. Stabilization slot: verified `zig build test`/`tidy`/`fmt --check` all
  clean, no regressions. Investigated whether the carried `tools/tidy.zig` self-exemption
  finding decomposes into a smaller safe fix — confirmed no: `tools/` isn't walked by
  `scan_roots` at all, so any fix must add it there, which cascades into fail-severity
  `checkFunctionLength` and ban-list checks (not just the warn-severity file-length check),
  so it stays sized for a dedicated stabilize cycle or plan-003 scope, not `--one`.
- PRs: none opened this cycle.
- Next: awaiting human merge of plan 002 (#17). This finding should be scoped as plan 003's
  first item once 002 merges, or done as a full non-`--one` `/stabilize sigil` cycle.
- Blockers: none. Open questions: none.
- Quiet cycle (4th in a row: plan PR open, no owner actions, no PR opened, CI green) — GitHub
  comment and Discord heartbeat both skipped per CONTRACT rule 8 carve-out.

## History

Cycle 0 (2026-09-05, RESTRUCTURE): realm created; scaffold survey (285 LOC, all stub modules).
Zig 0.16 probe found sigil nearly migration-ready. Plan 001 PR opened.

Cycles 1-4 (2026-09-05 to 09-07, FEATURE): plan 001 merged (PR #2), tracking issue #3 opened.
Item 1 hygiene leftovers (PR #4), item 2 branch decision — no `wip/*` needed (PR #5), item 3
`tidy` build step vendored from `citadel/templates/tidy/` (PR #6). Tracking issue reached 3/11.

Cycle 5 (2026-09-09, STABILIZATION, forced by counter%5==0): `tidy-auditor` found 9 real
findings (item 4's known scope), fixed via PR #7, `test_step` now hard-depends on tidy. Found
but didn't fix: `tools/tidy.zig` self-exempt from its own checks, unbounded dir-walk recursion,
misplaced `tidy_baseline.txt`, 2 unproven `catch unreachable` — all tracked in `STATE.md`.

Cycles 6-7 (2026-09-09, FEATURE): item 5 (0.16 main/args/allocators, `process.Init` rewrite,
bundled `minimum_zig_version` bump) via PR #8; item 6 (0.16 library sweep — 9 new `tidy` ban
rules, `error.Canceled` prong check) via PR #9. Both CI green, squash-merged. Issue #3 at 6/11.

Cycle 8 (2026-09-10, FEATURE): item 7 (`io: Io` convention on the public API) — `architect`
pinned `config.load(comptime T, io, arena, options)`, poll-based `Watcher`, `json.parseFile`/
`stringifyFile` shape; `docs/adr/0001-io-convention.md`. PR #10.

Cycle 9 (2026-09-11, FEATURE): item 9 (assertion baseline: real assertions in `main.zig`/
`root.zig`, new `checkAssertionBaseline` tidy check). Background review caught 1 CRITICAL
(argv upper-bound assert — shell data, not a caller contract) + 3 WARNING, all fixed with
regression tests before PR #13.

Cycle 10 (2026-09-12, STABILIZATION, forced by counter%5==0): merged PR #13, issue #3 to 9/11.
Re-swept the repo — fresh checks all 0 (`src/` still stub-stage). Fixed smallest carried
finding via PR #14 (`isWireFormatPath`'s 2nd `catch unreachable` needed its own proof comment).
3 findings left: misplaced `tidy_baseline.txt`, tidy.zig's self-exemption, unbounded recursion.

Cycles 11-12 (2026-09-12, FEATURE): item 10 (README reconciled with reality) via PR #15; item
11 (CHANGELOG.md + version bump 0.1.0→0.2.0) via PR #16. Plan 001 closed at 11/11 (version
impact `none`, no release). Opened plan 002 (Phase 1A: `core/value.zig`, `core/tree.zig`,
`core/diagnostics.zig`, folded in `core/number.zig`) as PR #17, still awaiting human merge.
Noted: local sandbox sometimes lacks the 0.16.0 toolchain — CI is the real gate.

Cycle 13 (2026-09-15, FEATURE): plan PR #17 open, no OWNER activity → one stabilization task:
fixed carried finding 1/3 (moved `tidy_baseline.txt` from repo root to `tools/`, TDD'd via the
`parseArgs` pinning test). PR #18, CI green, squash-merged. 2 findings remain.

Cycle 14 (2026-09-15, FEATURE): plan PR #17 still open → bounded recursion in
`walkDir15`/`descendDir15`/`walkDir16`/`descendDir16` with `dir_depth_max=64`. Tried
`std.Io.Dir.walkSelectively` first (std's own explicit stack) — reverted after it crashed
Linux CI with a std 0.16.0 bug in deep directory iteration (`dirReadLinux` "BADF"), reproduced
with plain `dir.iterate()` too; worth a Zig upstream issue if it recurs. Final fix: depth-bounded
recursion (documented Tiger Style 1.8 trade-off); regression test skipped on Linux only. PR #19
opened, merged in cycle 15 (fully green 8/8).

Cycles 15-17 (2026-09-16 to 09-17, FEATURE): plan PR #17 still open each cycle, no OWNER
activity → repeated `--one` stabilization slots all confirmed no finding smaller than the
carried `tools/tidy.zig` self-exemption exists (1860 lines, ~61 undocumented functions, 15
ban-list hits to triage). No PR opened in any of the three cycles — diminishing value from
identical repeated sweeps; quiet-cycle GitHub-comment carve-out used starting cycle 16.

## Standing backlog (Phase 1, plan 002 — unchanged since bootstrap)

Plan 001 (issue #3) closed 11/11. Plan 002 (PR #17) awaits human merge. Phase 1 scope, in
milestone order:

- **1A** — `core/{value,tree,diagnostics}.zig`: `Value` union, arena-owned `ValueTree`,
  `Diagnostics{line,col,message}`. Tests: arena release, equality, Map insertion-order.
- **1B** — `core/number.zig`: i64/u64/f64 boundary handling, `-0`, exponents, overflow errors.
- **1C** — `core/unicode.zig`: UTF-8/escape utilities.
- **1D** — `reflect/{parse,stringify,options}.zig`: comptime struct<->Value mapping.
- **2A-2C** (after Phase 1) — `json/{scanner,dom,writer}.zig`.
- Housekeeping: populate the empty performance-targets table once a module is benchmarkable.
- Carried stabilization finding (not fixed, sized for a full stabilize cycle or its own plan
  item — confirmed cycle 18 it does not decompose into a smaller safe slice): `tools/tidy.zig`
  (1860 lines) self-exempt from its own file-length/function-length/ban-list checks —
  `scan_roots` only walks `src/bench/tests`; widening it needs baseline entries for ~61
  functions plus false-positive triage on path-unconditional ban rules, since
  `checkFunctionLength` and the ban-list checks are fail-severity (not warn like file-length).

## Next priority

Awaiting human merge of plan 002 (PR #17). Once merged, `/cycle` opens its tracking issue and
item 1 (`core/value.zig`) becomes the next `/implement` target. The tidy.zig self-exemption
finding should become plan 003's first scope item (or a dedicated non-`--one` `/stabilize
sigil` cycle) rather than continuing to occupy the `--one` slot with no-op re-verification.
Toolchain: `~/.zr/toolchains/zig/0.16.0/zig` for local dev; global `zig` stays 0.15.2.
