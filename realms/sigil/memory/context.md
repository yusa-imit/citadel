# sigil — context

last_seen_at: 2026-09-12T01:00:00Z
rejected_plans: []

## Cycle 11 — 2026-09-12 — FEATURE

- Preflight: clean tree, on main, CI green (265ce20), no red CI or open bug — FEATURE mode
  (11 % 5 != 0, no stabilize_streak). Inbox: no new OWNER actions since watermark.
- Implemented plan 001 item 10 (README reconciled with reality) directly — a docs-only change,
  no code contract to TDD. Added a `Status` column to the module table (all `Planned`; `json`
  and `config` flagged `Planned (signature stub)` since item 7 gave them final `io: Io` shapes);
  Zig badge → 0.16.x; `Install` no longer points `zig fetch` at the never-cut `v0.1.0` tag;
  dropped `sailor` from the consumer list in both the Korean intro and "Part of the Zig Kingdom"
  (neither `REALM.md`'s registry nor `citadel/docs/KINGDOM.md`'s graph list it — zr, zoltraak,
  silica, synod are the real four). PR #15, CI 8/8 green, squash-merged, `auto-merged`.
- Also caught and fixed a tracking-issue bookkeeping gap: item 9 (assertion baseline, merged in
  #13/#14 last cycle) was never checked off in issue #3's checklist — ticked it retroactively.
  Plan 001 now 10/11; only item 11 (CHANGELOG + version bump) remains.
- Next: item 11 (CHANGELOG.md + `build.zig.zon` 0.1.0 → 0.2.0, no tag per the release quirk),
  then `/plan sigil` opens plan 002 (Phase 1A).
- Blockers: none. Open questions: none.

## History

Cycle 0 (2026-09-05, RESTRUCTURE): realm created; scaffold survey (285 LOC, all stub modules).
Zig 0.16 probe found sigil nearly migration-ready. Plan 001 PR opened.

Cycles 1-4 (2026-09-05 to 09-07, FEATURE): plan 001 merged (PR #2), tracking issue #3 opened.
Item 1 hygiene leftovers (PR #4), item 2 branch decision — no `wip/*` needed (PR #5), item 3
`tidy` build step vendored from `citadel/templates/tidy/` (PR #6). Tracking issue reached 3/11.

Cycle 5 (2026-09-09, STABILIZATION, forced by counter%5==0): `tidy-auditor` found 9 real
findings (item 4's known scope), fixed via PR #7, `test_step` now hard-depends on tidy. Found
but didn't fix: `tools/tidy.zig` self-exempt from its own checks, unbounded dir-walk recursion,
misplaced `tidy_baseline.txt`, 2 unproven `catch unreachable` — all tracked in `STATE.md`,
resurfaced and partly fixed in cycle 10.

Cycles 6-7 (2026-09-09, FEATURE): item 5 (0.16 main/args/allocators, `process.Init` rewrite,
bundled the `minimum_zig_version` bump from item 8) via PR #8; item 6 (0.16 library sweep — 9
new `tidy` ban rules for removed 0.15 APIs, `error.Canceled` prong check) via PR #9. Both CI
7/7, squash-merged. Tracking issue reached 6/11.

Cycle 8 (2026-09-10, FEATURE): item 7 (`io: Io` convention on the public API, the kingdom
spike other realms copy) — `architect` (opus) pinned `config.load(comptime T, io, arena,
options)`, poll-based `Watcher` (not a callback, per Tiger Style 1.14), `json.parseFile`/
`stringifyFile` as the format-module shape; `docs/adr/0001-io-convention.md` records two
deviations from the plan sketch. **Budget note**: one thorough `architect` call cost ~$3 of a
$4 session — keep interface-design prompts tight or skip later review passes. PR #10 opened;
CI still pending at session end, merged next cycle's inbox. Follow-up still open: `citadel/
core/rules/zig-0.16.md`'s io convention section is missing a clause about `comptime T: type`
occupying the receiver slot — a realm session can't edit citadel rules, only note it here.

Cycle 9 (2026-09-11, FEATURE): resumed an incomplete prior run (merged #11 + #12, item 8 done,
8/11). Implemented item 9 (assertion baseline: `main.zig`/`root.zig` real assertions, new
`checkAssertionBaseline` tidy check). Background `code-reviewer` caught 1 CRITICAL (never
assert an upper bound on argv — shell data, not a caller contract) + 3 WARNING, all fixed with
regression tests before PR #13 opened; CI still running at session end, merged next cycle.

Cycle 10 (2026-09-12, STABILIZATION, forced by counter%5==0): resumed cycle 9's unfinished
`/report` (counter still 9), merged PR #13, ticked plan 001 to 9/11. `tidy-auditor` re-swept the
repo — all fresh checks read 0 (`src/` still stub-stage) — and re-verified 4 carried-forward
findings. Fixed the smallest via PR #14 (`isWireFormatPath`'s 2nd `catch unreachable` needed its
own `// proof:` comment). 3 findings still open: `tidy_baseline.txt` at repo root (outside
`DOCS.md`'s allowed list), `tools/tidy.zig` (1770 lines) exempt from its own file-length/`//!`
checks, unbounded mutual recursion in `walkDir15`/`descendDir16` families.

## Standing backlog (Phase 1, plan 002 — unchanged since bootstrap)

Plan 001 (issue #3) is 10/11; item 11 (CHANGELOG + version) remains before Phase 1 work starts.
Phase 1 scope, in milestone order:

- **1A** — `core/{value,tree,diagnostics}.zig`: `Value` union, arena-owned `ValueTree`,
  `Diagnostics{line,col,message}`. Tests: arena release, equality, Map insertion-order.
- **1B** — `core/number.zig`: i64/u64/f64 boundary handling, `-0`, exponents, overflow errors.
- **1C** — `core/unicode.zig`: UTF-8/escape utilities.
- **1D** — `reflect/{parse,stringify,options}.zig`: comptime struct<->Value mapping.
- **2A-2C** (after Phase 1) — `json/{scanner,dom,writer}.zig`.
- Housekeeping: populate the empty performance-targets table once a module is benchmarkable.
- Carried from cycle 10 stabilization (unfixed, next stabilization candidates): misplaced
  `tidy_baseline.txt`, `tools/tidy.zig` self-exempt from file-length/`//!` checks, unbounded
  recursion in its directory-walk pairs.

## Next priority

Finish plan 001 (issue #3, 10/11): item 11 (CHANGELOG.md + `build.zig.zon` 0.1.0 → 0.2.0, no
tag per the release quirk) is next, `blocked_by: none`. Then `/plan sigil` opens plan 002
(Phase 1A). Toolchain: `~/.zr/toolchains/zig/0.16.0/zig` for all local dev commands; the global
`zig` alias on this machine stays 0.15.2 per `zig-0.16.md`.
