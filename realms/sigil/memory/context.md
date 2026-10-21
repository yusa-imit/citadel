# sigil — context

last_seen_at: 2026-10-22T12:00:00Z
rejected_plans: []

## Cycle 67 — 2026-10-22 — FEATURE

- Done: item 6 (TOML arrays and inline tables), written directly. PR #73, CI 8/8, auto-merged; #67 box 6
  ticked (6/12). Reviewer (finished after merge): 0 critical; fuzz of ~965k inputs found no node-bound
  OutOfMemory. Follow-ups to fold into the item 7 PR (or a small fix PR first): CHANGELOG `[Unreleased]`
  item 6 bullet and drop "follow in item 6"; `toml.zig` header says items 6-7 pending; >=2 asserts in
  `read_value`/`step`/`place`/`array_step`/`table_step`; seeded prefix-truncation test for the node
  bound (ADR/`scratch.zig` argument is amortised, not "2 bytes per node"); tests for `{ b.c = 1,
  b.d = 2 }`, comment inside `{}` rejected, CRLF/comment between array elements; ADR 0005 line 97
  is 123 cols, and section 4 says inline state set at `}` (code sets it at `{`); `depth = 0` dead init.
- Shape: `parser.zig` explicit `Frame` stack (`Need {first, after_comma, comma_or_close}`), `step` ->
  `array_step`/`table_step`, `place(Target{keyed|element}, token)`, `key_path` shared with statements.
  `scratch.append_scalar`/`append_container`; `nodes_max = len/2 + 2 + depth_max` (open `[`/`{` cost one
  byte; ADR 0005 amended). Keyed TooDeep points at the key, element TooDeep at the `[`/`{` token.
  Tests split: `parser_fixtures.zig` (shared helpers) + `parser_value_test.zig` (soft file limit 800).
- Next: item 7 `toml.zig` facade + reflect (ADR 0005 (f)). Blockers/questions: none.
- Learned: global `zig` is 0.15; use `PATH=/Users/fn/.zr/toolchains/zig/0.16.0:$PATH` and
  `--cache-dir /tmp/sigil-cache` (repo-local cache failed to spawn the build runner); BSD `sed -i ''`;
  the guard blocks one command mixing citadel paths with python heredocs (use Edit/Write there);
  `check_maps` test helper stack is 512 values (keep generated arrays small).

## Cycle 66 — 2026-10-21 — FEATURE

- Done: item 5 (TOML keys and tables) written directly, one sonnet code-reviewer (~$0.3, 0 critical)
  while CI ran. PR #72, CI 8/8, auto-merged; #67 box 5 ticked (5/12). Total ~$2.4.
- Shape: `toml/scratch.zig` = node array + hash index over (parent, key) (the ADR's "edges"), one
  `State` per container, `header_pass`/`header_end(array)`/`dotted_pass`/`insert_scalar`/
  `insert_container(inline_table|array_static)`, `conflict_offset` for the earlier line, iterative
  `materialize` (writes `Map.entries` directly, `put` is linear). `toml/parser.zig`: `parse_value`,
  `ParseOptions`, 17-variant `ParseValueError`; `[`/`{` in value position still `UnexpectedToken`
  (item 6). `nodes_max = input_len/2 + 2`, ADR amended; scratch ~50 B per input byte.
- Next: item 6 arrays and inline tables: values on an explicit stack, `insert_container` and element
  append are in scratch already (elements need an `add_element`-style call for arrays); add a worst-case
  node-bound test (nested one-byte arrays/tables). Blockers/questions: none.
- Learned: `catch |err| switch` over a one-variant set trips tidy's Canceled prong, use
  `catch return ...`; public `: usize` params are banned (use u32); `std.mem.indexOf` -> `find`;
  derive expected line:col from the lexer's fault offset (backslash, newline), not the token start.

## Cycle 65 — 2026-10-21 — FEATURE

- Done: item 4 (TOML scalars), written directly (tests first, no developer subagents), one sonnet
  code-reviewer (~$0.3) in the background while CI ran. PR #71, CI 8/8, auto-merged; #67 box 4 ticked
  (4/12). Total ~$1.35.
- Shape: new `toml/scalar.zig` (not inside lexer.zig): `parse(text) Error!Value` (bool/int/float/
  timestamp, never `.uint`), `number_text_max = 512` (only for numbers containing `_`; ADR 0005 §5
  amended), errors carry no position (parser item 5 builds the diag from the token offset). Lexer
  `scan_scalar` rejoins `dddd-dd-dd` + one space + `dd:` into one run (`joins_time`).
- Reviewer fixed: bad radix digit wins over overflow (`0x8000000000000000_` is InvalidNumber).
- Next: item 5 `toml/parser.zig` keys and tables (ADR 0005 §3-4 state machine; depth 127/128 per
  ADR). Blockers/questions: none.
- Learned: `zig build test` prints "failed command" with exit 0 on warn logs (check `$?`, not the
  text); a test expecting a tiny float must not assume it underflows (1e-256 is representable).

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

## History (cycles 54-59, condensed 2026-10-22)

Plan 005 `path/`, one item per cycle (PRs #57-#62): `pointer.zig` (`parse` into `[128]Segment`), `merge.zig`
+ internal `clone.zig` (path copying, one `tree.root` swap), `patch.zig` (`copy`/`move` deep-copy via
`clone.deep`), `jsonpath.zig` compile, `select.zig` (explicit `[nesting_max]Frame` stack), `filter.zig`
(iterative `deep_equal`; core `eql` is not RFC equality; limits filters 32, exprs 128, queries 32).
Learned: tidy wants a one-line `// proof:` above each `catch unreachable`/`switch (err)`; lines >100 cols
fail tidy in tests too; `**` and `++` share precedence; arena-backed FailingAllocator sweeps hit ~2
failure points, assert content; `Map.put` rejects duplicates; `gh pr checks` right after a push says "no
checks" for ~1 min; slice `position` goes negative with negative steps; `-0` parses as int 0.

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

## History (cycles 33-48, condensed 2026-10-21)

- 33-34 (10-04): plan 003 closed (reflect round-trip, `core.Error` union pinned by comptime test);
  plan 004 (JSON, ADR 0003) proposed as PR #38. 35-40: quiet, plan PR open; `bench/main.zig` ported
  to 0.16 and wired into `zig build test` (PR #39); README/CHANGELOG drift fixed.
- 41-48 (10-08 to 10-12): plan 004 merged; ADR 0003 via opus `architect` (~$2.9, scope it tightly);
  item 2 `json/scanner.zig` (PR #44), 3 strings (#45), 4 `json/dom.zig` (#46), 5 `writer.zig` (#47),
  6 round-trip property (#48), 7 JSONTestSuite vendored (#49; `.gitignore` `test_*` dropped the
  corpus, check `git ls-files`). Cycle 48 ran out of budget: subagents cost ~$3.4, work kept on a
  `wip/*` branch and merged in 49.
- Learned: tidy wants a one-line `// proof:` directly above each `catch unreachable`/`switch (err)`;
  `std.log.err` reports seeds in tests (tidy bans `std.debug.print`); sandbox `zig build` needs
  `--cache-dir /tmp/sigil-zc`; `gh pr checks` right after `gh pr create` says "no checks" for ~1 min
  (use an until-loop); `ScheduleWakeup` is for /loop only; the Bash guard blocks heredocs, `cd <repo>`
  and one command mixing citadel paths with repo commands; macOS `sed -i` needs `-i ''`;
  `zig test --test-filter` on root.zig misses submodule tests, use `zig build test`.

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
Plan 006 (Phase 3A TOML 1.0, v0.5.0) merged (PR #66); milestone #67, items 1-6 done, 7-12 open.

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

Plan 006 item 7 (`toml.zig` facade and reflect); see the newest cycle block.
Toolchain: `~/.zr/toolchains/zig/0.16.0/zig` for local dev; global `zig` stays 0.15.2.
