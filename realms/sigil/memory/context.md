# sigil — context

last_seen_at: 2026-10-08T00:00:00Z
rejected_plans: []

## Cycle 41 — 2026-10-08 — FEATURE

- Done: owner merged plan 004 (PR #38, 2026-10-07). Opened milestone issue #42. Item 1 (ADR 0003 JSON
  contract) via `architect` (opus, ~11 min, ~$2.9 — expensive); I wrote the file verbatim. Also
  amended PRD §4.2/§4.3/§5 and added an ADR 0001 pointer. PR #43, CI 8/8, squash-merged; plan item 1
  and #42 ticked. Docs-only, so no local `zig build test` run (CI is the gate).
- Next: item 2 `json/scanner.zig` (also adds `core.diagnostics.Position/position_of/snippet_of`).
  Item 10 is partly done already (bench port landed in #39; JSON benches and CI bench build step
  remain). New APIs per ADR 0003: `Map.index_of` (item 4), `reflect.context.write_diagnostic`
  (item 5), `parse_traced`/`Context.trace`/`scanner.locate` (item 8). Item 9 changes the root.zig
  parity test (7 params, `arena`, `diag`). Blockers/questions: none.
- Learned: an architect ADR draft can cost most of the cycle budget; for the next design-heavy item
  give it a tighter scope (it must return the full file text, since it has no Write). `gh pr checks
  --watch` right after create still says "no checks"; a Monitor until-loop works. Open risk: 0.16
  `ArenaAllocator` in-place shrink (ADR 0003 §4 fallback = three scans); `Io.Dir` read/write names
  unverified until item 9.

## Cycle 40 — 2026-10-07 — FEATURE (quiet)

- Done: plan PR #38 (plan 004) still open; its comments are all the AI's own reports (last
  2026-10-05), no OWNER review, no issues, no other PRs. CI green on main (HEAD 1cd7547). No
  stabilization slot used: only the `tools/tidy.zig` self-exemption is left and it does not
  decompose. No PR opened. Cost ~$0.3.
- Next: when plan 004 merges, open its milestone issue and implement item 1 (ADR 0003). Stay quiet
  until then. Blockers/questions: none.
- Learned: the guard blocks a Bash command that mixes citadel paths with repo commands; read citadel
  files with Read and keep Bash to repo-only commands.

## Cycle 39 — 2026-10-07 — FEATURE (quiet)

- Done: plan PR #38 (plan 004) still open; its only comments are the AI's own reports (last
  2026-10-05), no OWNER comment/review, no issues, no other PRs. CI green on main (HEAD 1cd7547).
  No stabilization candidate left except the `tools/tidy.zig` self-exemption (does not decompose),
  so no `--one` sweep and no PR. Cost ~$0.3.
- Next: when plan 004 merges, open its milestone issue and implement item 1 (ADR 0003). Stay quiet
  until then. Blockers/questions: none.

## Cycle 38 — 2026-10-06 — FEATURE (quiet)

- Done: plan PR #38 (plan 004) still open, no OWNER comment/review since the watermark, no issues,
  no other PRs. CI green (last 5 runs). One `--one` slot: sweep of CI, Tiger Style greps (`@panic`,
  `std.debug.print`, `FIXME`, `while (true)` all 0; headers all present; max file 740 lines),
  hygiene (no tracked `zig-out`). Nothing to fix, no PR opened. Cost ~$0.3.
- Next: when plan 004 merges, open its milestone issue and implement item 1 (ADR 0003). The only
  candidate left is the `tools/tidy.zig` self-exemption (does not decompose). Further sweeps repeat
  this result; prefer quiet cycles until plan 004 is decided. Blockers/questions: none.

## Cycle 37 — 2026-10-06 — FEATURE

- Done: plan PR #38 (plan 004) still open; inbox found no OWNER activity (only the AI's own cycle-36
  comment). CI green on main. One `--one` stabilization slot: CHANGELOG Unreleased was missing the
  `core.Error` wiring (#37) and the bench port (#39) and its intro was stale; fixed. PR #41, CI 8/8,
  squash-merged, labelled auto-merged. Local `zig build test` and fmt green, tidy 0. Cost ~$0.6.
- Learned: `gh pr checks --watch` right after `gh pr create` still says "no checks reported" for
  over a minute; use a Monitor with an until-loop on `gh pr checks` instead. A Python heredoc works
  in Bash from the repo cwd. The guard blocks `echo > /tmp/...` and any command starting `cd <repo>`.
- Next: when plan 004 merges, open its milestone issue and implement item 1 (ADR 0003). Until then
  one `/stabilize --one` slot per cycle; the only candidate left is the `tools/tidy.zig`
  self-exemption (does not decompose); consider a quiet cycle instead. Blockers/questions: none.

## Cycle 36 — 2026-10-05 — FEATURE

- Done: plan PR #38 (plan 004) still open; inbox found no OWNER activity (the only new comment was
  the AI's own cycle-35 report). CI green on main. One `--one` stabilization slot: docs drift — README
  still said "nothing implemented" and listed core/reflect as Planned; reconciled (Schema(T) kept as
  planned, install note now says first tag lands with json). PR #40, CI 8/8, squash-merged. tidy 0.
  Cost ~$0.6 of $4.
- Learned: the docs-only PR still gets full PR CI (paths-ignore applies only to push on main), and
  `gh pr checks --watch` right after `gh pr create` can say "no checks reported"; wait ~20 s, retry.
- Next: when plan 004 merges, open its milestone issue and implement item 1 (ADR 0003). Until then
  one `/stabilize --one` slot per cycle; the only remaining candidate is the `tools/tidy.zig`
  self-exemption (does not decompose). Blockers/questions: none.

## Cycle 35 — 2026-10-05 — FEATURE

- Done: plan PR #38 (plan 004) still open, no OWNER comment/review, no issues, CI green on main. One
  `--one` stabilization slot: `bench/main.zig` ported to 0.16 (`process.Init`, `Io.Clock.awake`,
  `std.mem.find`, explicit error set, pure rate helpers with a test). `build.zig` now shares one
  bench module between the `bench` exe and a test step wired into `zig build test`, so the harness
  compiles in CI. PR #39, CI 8/8, squash-merged. tidy 0, fmt clean. Cost ~$0.5 of $4.
- Learned: `zig build bench` had been broken since the 0.16 migration (plan 001 item 6 missed it
  because bench was not compiled by `zig build test`). Guard blocks a Bash command starting with `cd
  <repo>` even for the own repo; run from cwd instead.
- Next: when plan 004 merges, open its milestone issue and implement item 1 (ADR 0003). Until then
  one `/stabilize --one` slot per cycle; remaining candidate is the `tools/tidy.zig` self-exemption.
  Blockers/questions: none.

## History (cycles 33-34, condensed 2026-10-07)

Cycle 34 (2026-10-04): plan 003 item 10 (wire and close), PR #37, issue #27 closed, no tag.
`core.Error` = `number.Error || unicode.Error || EscapeError || {TooDeep, OutOfMemory}` (comptime
test pins members). Plan 004 (Phase 2A-2C JSON, ADR 0003) proposed as PR #38, drafted by planner.
Learned: sandbox `zig build` needs `--cache-dir /tmp/sigil-zc`; guard blocks a command containing
`push` while on main (branch first, separate command). Plan 003 item 4 box ticks with plan 004's
release item.
Cycle 33 (2026-10-04): item 9 `reflect/roundtrip_test.zig` (seeded, 1,000 seeds, every kind),
PR #36. Mutation-checked; one code-reviewer (0 critical, 4 warnings fixed; a `Coverage` tally
fails the test if a matrix branch is never generated). Learned: `std.log.err` reports the seed in
tests (tidy bans `std.debug.print`); `zig test --test-filter` on root.zig ran 1 test, use
`zig build test`; back up files before `git checkout` during mutation checks.

## History

Cycle 32 (2026-10-03): plan 003 item 8 `reflect/stringify.zig` via PR #35; one reviewer, 5 warnings
fixed. `Context` gained `fail_stringify`/`stringify_child`; `parse.has_hook/string_map_value/
assert_supported` are `pub`; the `Value` deep copy is private to stringify.zig; declare test types
at file scope (long `@typeName` truncates messages); tidy wants `// proof:` on `switch (err)` and 2
asserts per `pub fn`, hooks in tests included.

Cycles 30-31 (2026-10-02 to 10-03, FEATURE, plan 003 items 6-7): `reflect/parse.zig` structs, arrays,
slices (PR #33), then unions, `array_hash_map.String(V)` maps and `sigilParse` hook (PR #34). Learned:
`Pointer.alignment` is `?usize`; `assert_supported` must not recurse into fields; container entry
`depth >= nesting_max` -> `TooDeep`; a hooked type skips `options.resolve` so `parse.has_hook` checks
hook-vs-options; `String(V)` detected via `T.KV`. Bash guard blocks heredocs: use Write.

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

Cycles 15-19 (2026-09-16 to 09-26, FEATURE): plan PR #17 still open each cycle, no OWNER
activity → repeated `--one` stabilization slots all confirmed no finding smaller than the
carried `tools/tidy.zig` self-exemption exists (1860 lines, ~61 undocumented functions, 15
ban-list hits to triage). No PR opened across any of these cycles — diminishing value from
identical repeated sweeps; quiet-cycle GitHub-comment carve-out used starting cycle 16.

Cycles 20-25 (2026-09-27 to 09-29, FEATURE): plan 002 items 1-5 via PRs #21-#25 — `core/value.zig`
(bounded `eql` returns `TooDeep`; `Map.get` is O(n), may need a hash index), `core/tree.zig`
(`ValueTree` arena), `core/diagnostics.zig` (`DiagnosticsType(limits)`, inline generic self-ref
cannot share the file-scope alias name), `core/number.zig` (prefer `.int`, widen to `.uint` past
`maxInt(i64)`, typed overflow past `maxInt(u64)`), wiring + assertion baseline 23/23. Plan 002
closed 5/5, no tag (release quirk). Plan 003 opened as PR #26 (ADR 0002 gate before reflect).
Cycle 25 was quiet: test-quality audit of `core/*`, every error variant provoked. Hook notes: the
guard blocks heredocs and Bash commands mixing citadel reads with a repo `cd`; use Read/Write.

Cycle 26 (2026-09-30, FEATURE): plan 003 merged; items 1-2 via PRs #28-#29 (`core/unicode.zig`,
`core/unicode_escape.zig`; escapes live apart because unicode.zig hit the 800-line limit). DEL
(U+007F) is escaped as `\u007f`. `catch unreachable` needs a `// proof:` comment, <= 100 cols.
Slip: implementation before tests for item 2; recovered by a mutation check. Red step first.
`timeout` is absent on macOS; use `gh pr checks --watch`.

Cycles 27-29 (2026-10-01 to 10-02, FEATURE, plan 003 items 3-5): item 3 ADR 0002 reflect
contract (PR #30; hooks take `*reflect.Context`, errors split into `ParseError` 11 and
`StringifyError` 4, `deny_unknown_fields` defaults true, unions externally tagged, path-only
diagnostics use `core.diagnostics.position_none`). Item 4 `reflect/options.zig` (PR #31;
`resolve(T)` comptime `Table`, 17 compile-error fixtures run as `b.addObject` + `expect_errors`
steps from `build.zig`). Item 5 `reflect/parse.zig` scalars + `reflect/context.zig` (PR #32; 217
tests). Learned: `expect_errors .contains` is really ends-with on one compiler output line, so
the expected text is the tail of the `@compileError` message; `@Struct(.auto, null, names,
types, attrs)` builds test structs in 0.16; a non-`pub` `sigil_options` is invisible to
`@hasDecl`; tests live in sibling `*_test.zig` files for the 800-line limit. `Context.fail` has
no double-write guard. Keep citadel reads to the Read tool (a Bash command mixing citadel paths
with repo reads trips the guard).


## Standing backlog

Plans 001-003 closed (issues #3, #20, #27); no tag yet (release quirk still applies).
Plan 004 (Phase 2A-2C `json/{scanner,dom,writer}.zig`, first tag) is PR #38.

- Housekeeping: populate the empty performance-targets table once a module is benchmarkable;
  tick 1A/1B in `docs/plans/000-inherited.md` (missed at plan 002's close, folded into plan
  003's last item rather than a standalone PR).
- Carried stabilization finding (not fixed, sized for a full stabilize cycle or its own plan
  item — confirmed across cycles 15-18 it does not decompose into a smaller safe slice):
  `tools/tidy.zig` (1860+ lines) self-exempt from its own file-length/function-length/ban-list
  checks — `scan_roots` only walks `src/bench/tests`; widening it needs baseline entries for
  ~61 functions plus false-positive triage on path-unconditional ban rules, since
  `checkFunctionLength` and the ban-list checks are fail-severity (not warn like file-length).
  Deliberately kept out of plan 003's scope (a tooling theme, not Phase 1C/1D).

## Next priority

Plan 003 closed 10/10 (issue #27). Plan 004 (Phase 2A-2C JSON, first tag v0.3.0) is PR #38 awaiting
human merge; on merge open its milestone issue and `/implement` item 1 (ADR 0003).
Toolchain: `~/.zr/toolchains/zig/0.16.0/zig` for local dev; global `zig` stays 0.15.2.
