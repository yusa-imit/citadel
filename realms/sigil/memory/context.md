# sigil — context

last_seen_at: 2026-10-20T00:00:00Z
rejected_plans: []

## Cycle 64 — 2026-10-20 — FEATURE

- Done: found leftover PR #69 (plan 006 item 2 `core.timestamp`, CI 8/8, left open by an interrupted
  cycle 63 on `feat/core-timestamp-plan-006-item-2`) and merged it. Then item 3 `toml/lexer.zig` +
  `lexer_test.zig` written directly (no developer subagents): PR #70, CI 8/8, auto-merged. Boxes 2-3 of
  #67 ticked. Total cost ~$1.7 incl. one sonnet code-reviewer (~$0.3).
- Lexer shape: `Lexer.next(diag, mode)` with `Mode {key, value}`; key mode splits `.`, returns `[[`/`]]`
  and `bare_key`; value mode returns one `.scalar` run (up to ws, newline, `, ] } #`) so item 4 must
  classify it AND rejoin `1979-05-27 07:32:00` (two scalars today). Strings: 4 kinds, `raw` = body,
  `decode_string(kind, raw, out)` no error set. `ScanError` 6 variants. `Lexer.input_len_max =
  maxInt(u32) - 16` (reviewer: `offset + 8` could wrap; ADR 0005 section 5 amended).
- Next: item 4 lexer scalars (integers via `core.number`, `0x/0o/0b`, floats, bools, datetimes via
  `core.timestamp`). Blockers/questions: none.
- Learned: the guard blocks one command mixing citadel paths and repo commands (split them); `///` on a
  `test` is a compile error; tidy wants a `// proof:` above `switch (err)` even in tests; after a
  failing test the runner prints an unrelated json/writer stack (noise); `findScalar` replaces
  `indexOfScalar` in 0.16.

## Cycle 63 — 2026-10-19 — FEATURE

- Done: owner merged plan 006 (PR #66); opened milestone #67 (12 items). Item 1 ADR 0005 TOML contract
  written by me directly (no `architect`; ~$0.8 whole cycle vs ~$2.9): PR #68, docs-only, CI 8/8,
  auto-merged. Plan item and issue #67 box 1 ticked, PRD 4.3 TOML row amended.
- ADR 0005 pins: `Timestamp.Kind {instant, local_datetime, local_date, local_time}` + `kind` field
  (no default); scratch node/edge arrays from `gpa` (`input.len/2+1`), then exact `new_map` copy; one
  state per table (implicit/header/dotted/inline/array_static/array_tables), errors `DuplicateKey`,
  `TableRedefined`, `TypeConflict`; 17 parse + 6 write variants; `parse_value(gpa, tree, input, opts,
  diag)`; writer inlines a table followed by a scalar so round-trip `eql` holds; runner decodes
  toml-test JSON with `std.json`. Depth counts the root: 127 header segments pass / 128 `TooDeep`
  (plan said 128/129; tests use 127/128).
- Next: item 2 `core/timestamp.zig` (Kind field, civil date <-> days, RFC 3339 parse/format, 1,000-seed
  model test; update `reflect`, `json.writer`, `path/clone.zig` test literals). Blockers/questions: none.
- Learned: >100-col check on docs must skip table rows; foreground `gh pr checks` retry loop works (~6 min).
Cycle 62: plan 005 item 10 release, PR #65, v0.4.0 tagged, milestone #55 closed; plan 006 PR #66
(planner opus ~$0.65). Guard blocks grepping sibling `build.zig.zon` together with `git tag`/`push`.

## History (cycles 60-61, condensed 2026-10-19)

Cycle 61: item 9 path benchmarks (PR #64): `path.pointer.resolve` ~31 ns/lookup, `$..*` ~2150 MB/s
(~5 ns/node), filter ~2200 MB/s (~109 ns/match); `Result.matches_total`, `ns/match` column.
Cycle 60: item 8 conformance (PR #63): vendored jsonpath-standard `tests/jsonpath/` (BSD-2, 20ebdcc),
`path/conformance_test.zig`; counts 715 / 249 invalid / 466 valid / 659 pass / 56 pinned unsupported
(match/search) / 0 divergent. Learned: `std.log.err` in a helper fails a test (probe tests need a `report`
flag); warn logs make `zig build` print "failed command" but exit 0; a `// proof:` must be one line above
the switch.

## History (cycles 58-59, condensed 2026-10-18)

Cycle 59: item 7 JSONPath filters (PR #62): `path/filter.zig` (Expr tree, flat eval, exact int/uint/float
order), `filter_parse.zig` (`length`/`count`/`value`; match/search = UnsupportedFunction); limits filters 32,
exprs 128, queries 32; ADR 0004 section 6 amended (filter nesting = recursion bounded by
`filter_depth_max`); reviewer found core `eql` is not RFC equality (fixed with iterative `deep_equal`).
Cycle 58: item 6 `path/select.zig` (PR #61): explicit `[nesting_max]Frame` stack, descendant DFS equals
RFC nodelist order. Learned: slice `position` goes negative with negative steps; a model test whose `out`
always fits proves nothing about OutOfSpace; `zig test --test-filter` on root.zig misses path tests; the
guard blocks python heredocs touching citadel paths (use Read/Edit); `-0` parses as int 0; tidy wants one
`// proof:` line above each `catch unreachable`/`switch (err)`.

## History (cycles 54-57, condensed 2026-10-19)

Cycle 57: item 5 `path/jsonpath.zig` parse (PR #60): `compile(*Program, query, diag)`, fixed struct,
byte-column diags. Cycle 56: item 4 `path/patch.zig` (PR #59): `apply(tree, ops, diag)` per-op spine
rebuild, one `tree.root` assignment, `op <i>: <reason>` diags; `copy`/`move` deep-copy via `clone.deep`
(a shared subtree makes a DAG with exponential depth walk); index past end is `IndexOutOfRange`, `-` is
`PathNotFound`. Cycle 55: item 3 `path/merge.zig` (PR #58; path copying, one `tree.root` swap, internal
`path/clone.zig`). Cycle 54: item 2 `path/pointer.zig` (PR #57; `parse` into `[128]Segment`, `resolve`,
`format`, `index_of`, `segment_eql`). Learned: tidy wants `// proof:` above a multi-line
`catch |err| switch (err)`; lines >100 cols fail tidy in tests too; `**` and `++` share precedence,
parenthesize; `node = .{ .map = try f(node) }` aliases the result location (use a temp); arena-backed
FailingAllocator sweeps hit only ~2 failure points, assert content; `Map.put` rejects duplicate keys;
tests build documents inside out with `tree.new_map(n)`; `gh pr checks` right after a push says "no
checks" for ~1 min (until-loop); a trailing `Monitor sleep` placeholder is wasted money.

## History (cycles 52-53, condensed 2026-10-16)

Cycle 52 (2026-10-14): plan 004 item 11, release PR #53, v0.3.0 tagged (first tag), milestone #42
closed 11/11, no consumer pins sigil. Cycle 53: owner merged plan 005 (PR #54), milestone #55 opened;
item 1 ADR 0004 (PR #56): reads borrow `*const Value`, Patch/Merge use path copying + one
`tree.root` swap, JSONPath = `compile(*Program)` + `select(program, root, out)` with fixed limits
(segments 32, selectors 64, filter depth 8, query 1024), `match`/`search` pinned unsupported.

## History (cycles 49-51, condensed 2026-10-15)
- 49: plan 004 item 8 `json.parse(T)`/`json.stringify` (PR #50); `parse_error_test.zig` and `stringify_test.zig`
  had never been wired into `json.zig` (476 -> 503 tests). Open nit: `reflect.parse` lacks the
  `errdefer assert(diag_written)` that `parse_traced` has.
- 50: item 9 `json.parseFile`/`stringifyFile` (PR #51, `src/json/file.zig`): `arena` + final `diag`, `bytes_max`
  inclusive via `readFileAlloc(.limited64(bytes_max + 1))`, std errors collapsed by `map_*_error`;
  `ParseFileError` 27 variants, `StringifyFileError` 10; 518 tests.
- 51: item 10 benchmarks (PR #52): seeded ~1 MiB doc; `json.dom.parse` ~145-175 MB/s, `write.minified`
  ~480-490, `json.parse(T)` ~165; CI `Bench` step (`zig build bench`); numbers in `000-inherited.md`.
- Lessons: every new `*_test.zig` must be imported from its module's `test {}` block; writing tests+impl
  directly cost ~$1.5 vs ~$3.4 with test-writer + zig-developer; first bench in a run is ~20% slower; use
  `--cache-dir /tmp/sigil-zc` if `.zig-cache` is stale; the Bash guard blocks one command mixing citadel
  paths with repo commands; `wip/*` branches are kept; do not use ScheduleWakeup.

## History (cycles 46-48, condensed 2026-10-14)

Cycle 48 (2026-10-12, budget exhausted, no PR): subagents (zig-developer + test-writer) cost ~$3.4; work
preserved on `wip/json-parse-stringify-*`, merged in cycle 49. Learned: do not poll; launch and end the turn.
Cycle 47 (2026-10-11): item 7 JSONTestSuite vendored (PR #49); `.gitignore` `test_*` dropped the corpus
(check `git ls-files`); strict parser rejects 33 of 35 `i_`; `Value` map variant is `.map`.
Cycle 46 (2026-10-10): item 6 round-trip property (PR #48); macOS `sed -i` needs `-i ''`.


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

Plans 001-005 closed (issues #3, #20, #27, #42, #55); v0.4.0 tagged 2026-10-19 (v0.3.0 2026-10-14).
Plan 006 (Phase 3A TOML 1.0, v0.5.0) merged (PR #66); milestone #67, item 1 done, items 2-12 open.

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

Plan 006 item 2 (`core/timestamp.zig`); see the newest cycle block.
Toolchain: `~/.zr/toolchains/zig/0.16.0/zig` for local dev; global `zig` stays 0.15.2.
