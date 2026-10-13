# sigil — context

last_seen_at: 2026-10-12T15:13:00Z
rejected_plans: []

## Cycle 50 — 2026-10-13 — FEATURE

- Done: plan 004 item 9 `json.parseFile`/`stringifyFile` merged. New `src/json/file.zig` (re-exported by
  `json.zig`; `Error` lost `NotImplemented`, `scratch_bytes_min` deleted); both take `arena` + final
  `diag` (ADR 0003 section 9); `bytes_max` inclusive via `readFileAlloc(.limited64(bytes_max + 1))`;
  std errors collapsed by `map_read_error`/`map_create_error`/`map_write_error` (`else` = ReadFailed/
  WriteFailed). `ParseFileError` 27 variants, `StringifyFileError` 10. PR #51, CI 8/8, squash-merged;
  518 tests, tidy 0; milestone #42 at 9/11. I wrote tests and impl myself (no subagents but one
  sonnet code-reviewer: 0 critical, 5 warnings, all fixed: directory read/write gives ReadFailed/
  WriteFailed end to end, OOM, writer-stage TooDeep, doc said 26). Cost ~$1.5.
- Next: item 10 benchmarks (JSON benches in `bench/main.zig`, CI build step for `bench`, record MB/s in
  `docs/plans/000-inherited.md`), then item 11 release v0.3.0 (`/release sigil minor`). Blockers: none.
- Learned: writing tests+impl directly was far cheaper than test-writer + zig-developer (~$1.5 vs ~$3.4).
  Only reflect errors precede the file open in `stringifyFile`; writer-stage errors (NaN, TooDeep)
  truncate first, now documented. `testing.tmpDir` + `dir.createDir(io, "sub", .default_dir)` gives a
  directory for IsDir cases. Open nit: `reflect.parse` lacks `errdefer assert(diag_written)`.

## Cycle 49 — 2026-10-12 — FEATURE

- Done: plan 004 item 8 `json.parse(T)`/`json.stringify` merged. The cycle 48 wip work was branched to
  `feat/json-parse-stringify-item-8`; `parse_error_test.zig` and `stringify_test.zig` had never been
  wired into `json.zig` (added: 476 -> 503 tests, all green first time). One code-reviewer (sonnet): 0
  critical, 3 warnings: locate cost doc said O(input) (really O(depth_max x input)) and the hook
  obligation was unwritten (both doc-fixed); `reflect.parse` lacks the `errdefer assert(diag_written)`
  that `parse_traced` has (skipped, outside item 8; candidate stabilization nit). PR #50, CI 8/8,
  squash-merged; milestone #42 at 8/11. Cost ~$1.
- Next: item 9 `parseFile`/`stringifyFile` (ADR 0001 shapes over item 8; `Io.Dir` read/write names
  still unverified; changes the root.zig parity test and retires the stub error sets), then item 10
  benchmarks, item 11 release v0.3.0. Blockers/questions: none.
- Learned: check that every new `*_test.zig` is imported from its module's `test {}` block (tests
  silently not running is how 27 tests sat unwired); `wip/json-parse-stringify-*` branches are
  superseded by the merge but kept (never delete wip branches). The cycle ran on budget: launching
  the reviewer and a CI Monitor then ending the turn worked well.

## Cycle 48 — 2026-10-12 — FEATURE (budget exhausted, no PR)

- Done: preflight found 4 untracked red item-8 test files on `feat/json-parse-stringify-plan-004-item-8`;
  preserved on `wip/json-parse-stringify-plan-004-item-8-20261012`. Ran zig-developer + test-writer in
  parallel (~$3.4 of the $4 cycle budget; subagent runs plus my own polling turns were far costlier than
  estimated): implementation (raw_eql, `scanner.locate` in new `json/locate.zig`, `parse_traced`,
  `Context.trace`, `json.parse/stringify/parse_value/write_value`, 23/6-variant error sets) reported
  476/476 green and fmt ok BEFORE `parse_error_test.zig` (14 tests) and `stringify_test.zig` (13 tests)
  were wired into json.zig. All of it is committed on `wip/json-parse-stringify-item-8-impl-20261012`
  (a431e63, pushed), unreviewed, wired suite not run, NO PR, item 8 box still open.
- Next: check out that wip branch into `feat/json-parse-stringify-plan-004-item-8`, run `zig build test`
  (--cache-dir /tmp/sigil-zc) + `zig fmt --check`, fix anything in the 2 new test files, run one
  code-reviewer, tick plan item 8 + CHANGELOG, open PR, merge on green. Dev patched 3 red test files
  (inline for in raw_eql_test, `const first = context.fail(..)` in parse_trace_test, BuildError alias in
  locate_test) with no assertion changes. json.StringifyOptions is now the writer's; stubs
  parseFile/stringifyFile keep old error sets until item 9. Blockers/questions: none.
- Learned: budget is $4 per cycle and each of my own turns costs ~$0.07-0.10 once the context is large:
  do not poll or Monitor-wait; launch agents and end the turn, and do /report before the money is gone.
  Counter written to 48; GitHub comment and Discord summary NOT sent (no budget). Watermark unchanged.

## Cycle 47 — 2026-10-11 — FEATURE

- Done: plan 004 item 7 JSONTestSuite: vendored `tests/json/test_parsing` (318 files, 354 KB) +
  `LICENSE`; `src/json/suite_test.zig` reads it at run time via `std.testing.io` (95 `y_` parse under
  `.last`, 188 `n_` fail with line/col >= 1 and a message, 35 `i_` pinned in `pinned_accepted` (2) /
  `pinned_rejected` (33); counts asserted). `build.zig` `run_mod_tests.setCwd(b.path("."))`. PR #49,
  CI 8/8, squash-merged; #42 at 7/11. Local 377+ tests, tidy 0, fmt ok. Mutation (`.last` -> `.reject`)
  caught. Reviewer (1 sonnet): 0 critical, 3 warnings (2 fixed: weak dup-key checks; `else` prong proof
  reworded; build cache does not track corpus files, accepted). ~$1.6.
- Next: item 8 `json.parse(T)`/`json.stringify` (fold json.zig stub `ParseOptions` into
  `dom.ParseOptions`; `parse_traced`, `Context.trace`, `scanner.locate` per ADR 0003), then item 9.
  Blockers/questions: none.
- Learned: `.gitignore` has `test_*` which silently dropped `tests/json/test_parsing` (CI saw
  FileNotFound while local passed): check `git ls-files` count after vendoring; fixed with
  `!/tests/json/test_parsing/`. Strict parser rejects 33 of 35 `i_` (surrogates, bad UTF-8, BOM,
  out-of-range numbers, depth 129). `Value` map variant is `.map` (not `.object`), `Map.count`.
  The Bash guard blocks `sleep N` chained before a command; use Monitor.

## History (cycle 46, 2026-10-10)

Cycle 46: item 6 `json/roundtrip_test.zig` (PR #48): 1,000 seeds x 4 layouts + number edges, sorted
output checked by iterative `eql_sorted`; generator `pub` in `writer_test.zig`; reviewer fixed 3
warnings. macOS `sed -i` needs `-i ''`. Round-trip root is a scalar 75% of seeds (tally asserts
containers are reached).

## History (cycles 43-45, condensed 2026-10-10)

Cycle 45 (2026-10-10): item 5 `json/writer.zig` (PR #47): `write(w, value, options, diag)`, `Layout`
minified|pretty, `sort_keys`, floats forced to re-parse as `.float`, `Unrepresentable` for
bytes/timestamp/NaN/inf, key-path diag via public `reflect.context.write_diagnostic`. Learned:
reflect's path renderer emits raw non-ASCII key bytes (diag may hold invalid UTF-8, not fixed);
`ScheduleWakeup` is for /loop only; do not use it to wait on CI.
Cycle 43 (2026-10-09): item 3 scanner strings (PR #45): `.key`/`.string` validated whole, 4 new
`ScanError` variants, `decode_string`; tests in `scanner_string_test.zig` (500-seed model + corpus
differential vs `std.json.validate`). Cycle 44 (2026-10-09): item 4 `json/dom.zig` (PR #46): two scans,
exact `Map` sizes, `dom.ParseOptions {depth_max, duplicate_key}`, `DuplicateKeyPolicy {reject, last}`,
`core.Map.index_of`. Learned: tidy wants `// proof:` on ONE line directly above each `catch
unreachable`/`switch (err)`; `scanner.zig` is 580 lines so tests go in sibling files; `Weight` lives in
`std.testing.Smith.Weight`; a truncated UTF-8 sequence at an unterminated string is `InvalidUtf8`;
`ArenaAllocator.resize` of the newest allocation shrinks it. Open: item 8 should fold json.zig's stub
`ParseOptions` into `dom.ParseOptions`. Background reviewer + CI until-loop in parallel works well;
commit/push/PR before the reviewer returns, fix on the branch.

## History (cycles 39-42, condensed 2026-10-09)

Cycle 42 (2026-10-08): item 2 `json/scanner.zig` + `core.diagnostics.Position/position_of/snippet_of`
(PR #44); `+`/`.` leading bytes route to `scan_number`; guards block heredocs, `cd <repo>`, `sleep`.
Cycles 39-40 (2026-10-07, quiet): plan PR #38 open, no OWNER activity, no PR; the only stabilization
candidate is the `tools/tidy.zig` self-exemption, which does not decompose. Learned: the guard blocks
a Bash command mixing citadel paths with repo commands; read citadel files with Read.
Cycle 41 (2026-10-08): owner merged plan 004 (PR #38); opened milestone #42; item 1 (ADR 0003 JSON
contract) via `architect` (opus, ~$2.9, expensive: give it a tight scope, it must return the full
file text) landed in PR #43 with PRD 4.2/4.3/5 amendments. Open risk: 0.16 `ArenaAllocator` in-place
shrink (ADR 0003 section 4 fallback = three scans); `Io.Dir` read/write names unverified until item 9.
New APIs per ADR 0003: `Map.index_of` (item 4), `reflect.context.write_diagnostic` (item 5),
`parse_traced`/`Context.trace`/`scanner.locate` (item 8); item 9 changes the root.zig parity test.

## History (cycles 35-38, condensed 2026-10-08)

Cycles 35-38 (2026-10-05 to 10-06, FEATURE, plan PR #38 open, no OWNER activity): one `--one`
stabilization slot each. 35: `bench/main.zig` ported to 0.16 and wired into `zig build test` (PR
#39; bench had been broken since the migration because nothing compiled it). 36: README drift fixed
(PR #40). 37: CHANGELOG Unreleased gaps for `core.Error` (#37) and the bench port (PR #41). 38:
quiet sweep, nothing to fix (Tiger Style greps 0, max file 740 lines). The only candidate left is
the `tools/tidy.zig` self-exemption, which does not decompose. Learned: `gh pr checks --watch`
right after `gh pr create` says "no checks reported" for over a minute, use a Monitor until-loop;
docs-only PRs still get full PR CI; the guard blocks `echo > /tmp/...` and any command starting
`cd <repo>`.

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

## History (cycles 0-32, condensed 2026-10-13)

Cycles 0-12 (2026-09-05 to 09-12): realm created (285 LOC stubs). Plan 001 (PR #2, issue #3) closed
11/11: hygiene, `tidy` build step from citadel templates (PR #6), 0.16 main/args/allocators sweep
(PRs #8-#9), ADR 0001 `io: Io` (PR #10), assertion baseline (PR #13; an argv assert was shell data,
not a caller contract), version 0.2.0 (no release). Plan 002 opened as PR #17.
Cycles 13-19 (2026-09-15 to 09-26): plan PR #17 open, no OWNER activity; `tidy_baseline.txt` moved
to `tools/` (PR #18); `walkDir*` recursion bounded by `dir_depth_max=64` (PR #19; `walkSelectively`
crashed Linux CI with a std 0.16.0 `dirReadLinux` BADF bug, worth an upstream issue if it recurs).
Repeated sweeps found nothing smaller than the carried `tools/tidy.zig` finding (see backlog).
Cycles 20-26 (2026-09-27 to 09-30): plan 002 items 1-5 (PRs #21-#25): `core/value.zig` (bounded
`eql` -> `TooDeep`), `core/tree.zig`, `core/diagnostics.zig`, `core/number.zig` (prefer `.int`,
widen to `.uint`, typed overflow); plan 002 closed 5/5, no tag. Plan 003 items 1-2 (PRs #28-#29):
`core/unicode.zig`, `core/unicode_escape.zig` (DEL escaped as `\u007f`).
Cycles 27-32 (2026-10-01 to 10-03): plan 003 items 3-8 (PRs #30-#35): ADR 0002 reflect contract,
`reflect/options.zig` (17 compile-error fixtures via `b.addObject` + `expect_errors`; `.contains`
is really ends-with on one compiler line), `reflect/{context,parse,stringify}.zig`. Learned:
`catch unreachable`/`switch (err)` need a one-line `// proof:`; `@Struct(.auto, null, names, types,
attrs)` builds test structs in 0.16; non-`pub` `sigil_options` is invisible to `@hasDecl`;
`Pointer.alignment` is `?usize`; declare test types at file scope; tests go in sibling `*_test.zig`
files for the 800-line limit. Guard: read citadel files with Read, never mix with repo `cd`;
heredocs blocked, use Write; `timeout` absent on macOS, use `gh pr checks --watch`.


## Standing backlog

Plans 001-003 closed (issues #3, #20, #27); no tag yet (release quirk still applies).
Plan 004 (Phase 2A-2C `json/{scanner,dom,writer}.zig`, first tag) merged (PR #38), milestone #42.

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

Plan 004 (Phase 2A-2C JSON, first tag v0.3.0) is in progress on milestone #42; see the newest cycle
block above for the next item.
Toolchain: `~/.zr/toolchains/zig/0.16.0/zig` for local dev; global `zig` stays 0.15.2.
