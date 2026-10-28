# sigil — context

last_seen_at: 2026-10-29T06:00:00Z
rejected_plans: []

## Cycle 76 — 2026-10-29 — FEATURE

- Done: plan PR #80 still open (no owner comments), no milestone issue -> `/stabilize --one`: ADR 0005
  docs fix (4 lines >100 cols wrapped; section 4 now says inline state is set at `{`, as the code does).
  PR #81, CI 8/8, auto-merged. Cycle 67 ADR follow-ups (line 97, inline-state wording, `depth = 0`
  dead init check) -> ADR ones done. CI green, inbox empty, disk 38 GB. Cost ~$0.5, no subagents.
- Next: once #80 is merged, open milestone issue for 007 and do item 1 (ADR 0006). Else another
  `/stabilize --one`: asserts in parser step fns, prefix-truncation test, inline-table tests;
  docs lines >100 cols remain in PRD.md (33), plans/000-inherited.md (6), README (2). Blockers: none.
- Learned: the guard blocks `cd <repo> && ...` in a compound with `;` too — use `git -C`/absolute paths.

## Cycle 75 — 2026-10-28 — FEATURE

- Done: plan 006 item 12, release v0.5.0 (PR #79, CI 8/8, auto-merged, tag + GitHub release);
  milestone #67 closed 12/12. No sibling `build.zig.zon` names sigil -> no migration issues.
  Then `/plan`: plan 007 "Phase 4AB MessagePack + CBOR" (v0.6.0, 11 items, item 1 = ADR 0006)
  written via `planner` (opus, ~$0.9), PR #80 awaiting merge (citadel#81). Cost ~$1.6 total.
- Next: once #80 is merged, open milestone issue for 007 and do item 1 (ADR 0006, architect
  or directly). If not merged: one `/stabilize sigil --one` filler (cycle 67 follow-ups:
  asserts in parser step fns, truncation test, inline-table tests). Blockers: none.
- Open question (on PR #80, non-blocking): reflect option to omit null optionals in
  `toml.stringify`.
- Learned: release PR must also bump `sigil.version` in `src/root.zig` and its pin test; the
  guard rejects one command mixing citadel paths with repo work (split); planner output came
  back HTML-escaped (`-&gt;`), unescape before writing the plan file.

## Cycle 74 — 2026-10-28 — FEATURE

- Done: plan 006 item 11 (TOML benchmarks), written directly (~$0.7, no subagents). PR #78, CI 8/8,
  auto-merged; #67 box 11 ticked (11/12). Inbox empty, CI green, disk 38 GB.
- Shape: `bench/main.zig` got `Format {json, toml}` per `Bench`, a seeded ~100 KB `[[records]]`
  document (`generate_toml_document`, seed 0x7031), 256 iterations, `ms/iter` column for TOML rows.
  ReleaseFast: `toml.parse_value` 0.44 ms (~228 MB/s, arena 4.73 B/B), `toml.parse(T)` 0.48 ms (~208
  MB/s, 8.53 B/B), `toml.write_value` 0.17 ms (~591 MB/s). PRD <1 ms met. Recorded in
  `docs/plans/000-inherited.md`; CHANGELOG bullet added. Plan-file boxes 7-10 were unticked, ticked here.
- Next: item 12 release v0.5.0 (`/release`: tick 3A in 000-inherited, CHANGELOG [0.5.0], zon +
  `sigil.version` 0.4.0 -> 0.5.0, tag, `gh release create`, close #67). Then `/plan`; cycle 67
  follow-ups (asserts in parser step fns, truncation test, inline-table tests) still open. Blockers: none.
- Learned: guard blocks a command mixing `git checkout -b` with `git push` (and `sed -i` chains with
  them): run branch/commit and push as separate Bash calls; no `timeout` binary on macOS.

## Cycle 73 — 2026-10-27 — FEATURE

- Done: plan 006 item 10 (`toml/roundtrip_test.zig`), written directly (~$0.9, no subagents). PR #77,
  CI 8/8, auto-merged; #67 box 10 ticked (10/12). Inbox empty, CI green, disk 43 GB.
- Shape: 1,000 seeded trees write -> parse -> eql + byte-identical 2nd write (coverage asserted:
  1574 maps, 411 arrays, 455 timestamps, 125 w/ tables, 61 w/ `[[`); 205 valid corpus files parse ->
  write -> parse; 1,640 seeded mutations (663 accepted, 977 rejected, bounds asserted not exact);
  `std.testing.fuzz` entry + 6-doc corpus; one oracle `check_input`. No parser/writer bug found.
  `conformance_test.read_case`/`valid_count` made `pub`.
- Next: item 11 benchmarks (`zig build bench`: ~100 KB seeded TOML parse, `toml.parse(T)`, writer;
  record in `docs/plans/000-inherited.md`), then 12 release v0.5.0. Cycle 67 follow-ups still open
  (asserts in parser step fns, truncation test, inline-table tests) as filler. Blockers: none.
- Learned: mutually recursive generators need an explicit error set (inferred sets loop);
  `random.uintLessThan(u3, 8)` is a compile error (use `random.int(u3)`); a "failed" test can print
  an unrelated leaked error-return trace, read the `expect` line, not the trace.

## Cycle 72 — 2026-10-27 — FEATURE

- Done: plan 006 item 9 (`toml/writer.zig`), written directly (tests + impl, no subagents, no
  reviewer). PR #76, CI 8/8, auto-merged; #67 box 9 ticked (9/12). 701 tests, tidy 0.
- Shape: two explicit `[nesting_max]Frame` stacks (header-form `table`/`tables`, inline
  `array`/`map`); key path for diags derived from frames' current members (no live Path). Trailing
  run = suffix of table-like entries (map, or non-empty array of maps) -> `[a.b]`/`[[a]]`; every
  earlier map/array-of-maps inline; blank line before each non-first header; `[a]` emitted even
  when it holds only sub-tables. `toml.write_value`/`stringify`/`StringifyOptions`/
  `WriteValueError` (6)/`StringifyError` (7, comptime-pinned). `format_float` moved to
  `core.number` (json/writer calls it). ADR 0005 s8 amended.
- Open design note: a null optional from reflect is `Unrepresentable` in `toml.stringify`; omitting
  unset optionals would be a reflect option (maybe fold into a later plan / question to owner).
- Next: item 10 round-trip property + seeded mutation + `std.testing.fuzz` entry (0.16 Smith API).
  Cycle 67 follow-ups still open (asserts in parser step fns, truncation test, inline-table tests).
  Blockers/questions: none.
- Learned: `zig build test` exit 0 with "failed command" line is just warn logs; guard blocks
  `sleep` chains, use `until gh pr checks ...; do sleep 10; done` then `--watch`.

## History (cycles 68-71, condensed 2026-10-28)

C68-69: disk gate failed (18/16 GB, need 20), no work. C70: item 7 PR #74, `toml.zig` facade:
`parse_value`/`parse(T, ...)`, `ParseValueError` (17) / `ParseError` (25, comptime-pinned); reflect
failures re-located by `parser.locate` (second parse into throwaway scratch, error path only);
reflect messages are "{path}: {reason}", tests match with `find`. `write_value`/`stringify` landed
with item 9. C71: item 8 PR #75, toml-test v2.2.0 (MIT) vendored in `tests/toml-test/` (887
files); 679 cases, 679 pass, 0 pinned; floats compared by bit pattern, datetimes as
`core.timestamp.parse` values (ADR 0005 s9). `gh api repos/<o>/<r>/tarball/<tag>` into /tmp
fetches a corpus. Cycle 67 follow-ups still open: see cycle 67 below.

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

## History (cycles 63-66, condensed 2026-10-23)

Plan 006 (TOML 1.0, milestone #67) items 1-5, one per cycle, written directly (~$0.8-2.4 each, one sonnet
reviewer while CI runs). C63: ADR 0005 TOML contract (PR #68): `Timestamp.Kind {instant, local_datetime,
local_date, local_time}`; scratch node/edge arrays from `gpa` then exact `new_map` copy; one state per
table; errors `DuplicateKey`/`TableRedefined`/`TypeConflict`; 17 parse + 6 write variants; depth counts the
root (127 pass / 128 `TooDeep`). C64: `core.timestamp` (PR #69) and `toml/lexer.zig` (PR #70):
`Lexer.next(diag, Mode{key,value})`, `input_len_max = maxInt(u32) - 16`. C65: `toml/scalar.zig` (PR #71):
`parse(text) Error!Value`, `number_text_max = 512`, bad radix digit wins over overflow. C66:
`toml/scratch.zig` node array + hash index over (parent, key), `header_pass`/`dotted_pass`/`insert_*`,
iterative `materialize`; `parse_value(gpa, tree, input, opts, diag)` (PR #72).
Learned: global `zig` is 0.15, use `PATH=/Users/fn/.zr/toolchains/zig/0.16.0:$PATH` and `--cache-dir
/tmp/sigil-cache`; `zig build test` prints "failed command" with exit 0 on warn logs (check `$?`); `///`
on a `test` is a compile error; tidy wants a one-line `// proof:` above `switch (err)`/`catch unreachable`,
and `catch return` instead of a one-variant `catch |err| switch`; public `: usize` params are banned (u32);
`std.mem.indexOf` -> `find`, `indexOfScalar` -> `findScalar`; the guard blocks one command mixing citadel
paths with repo commands or python heredocs (split, or use Edit/Write); foreground `gh pr checks` retry
loop works (~6 min); >100-col check on docs must skip table rows.

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

## History (cycles 0-53, folded 2026-10-27)

- 0-32 (09-05 to 10-03): realm created (285 LOC stubs); plan 001 (hygiene, `tidy` step, 0.16 sweep,
  ADR 0001 `io: Io`, assertion baseline, 0.2.0 no release); plans 002 (`core/` value, tree,
  diagnostics, number) and 003 (unicode, ADR 0002 reflect contract, `reflect/` options, context,
  parse, stringify) closed. `walkDir*` bounded by `dir_depth_max=64`; std 0.16.0 `dirReadLinux`
  BADF bug crashed `walkSelectively` on Linux CI (upstream issue if it recurs).
- 33-48 (10-04 to 10-12): plan 004 (JSON, ADR 0003) merged; `json/` scanner, strings, dom, writer,
  round-trip property, JSONTestSuite vendored (`.gitignore` `test_*` dropped the corpus, check
  `git ls-files`). Cycle 48 ran out of budget (subagents ~$3.4); work kept on a `wip/*` branch.
- 49-53 (10-14 to 10-16): `json.parse(T)`/`stringify` (PR #50; unwired test files found), `parseFile`/
  `stringifyFile` (PR #51), benchmarks (PR #52: dom.parse ~145-175 MB/s, write.minified ~480-490),
  release PR #53, v0.3.0 first tag, milestone #42 closed; plan 005 merged (PR #54), ADR 0004:
  reads borrow `*const Value`, Patch/Merge use path copying + one `tree.root` swap, JSONPath =
  `compile(*Program)` + `select` with fixed limits (segments 32, selectors 64, filter depth 8,
  query 1024), `match`/`search` unsupported.
- Learned: tidy wants a one-line `// proof:` above each `catch unreachable`/`switch (err)`; tidy bans
  `std.debug.print` (use `std.log.err`) and lines >100 cols, tests included; every new `*_test.zig`
  must be imported from its module's `test {}` block; `@Struct(.auto, null, names, types, attrs)`
  builds test structs in 0.16; non-`pub` `sigil_options` is invisible to `@hasDecl`; sandbox `zig
  build` needs `--cache-dir /tmp/sigil-zc`; `gh pr checks` right after a push says "no checks" for
  ~1 min (use an until-loop); Bash guard blocks heredocs, `cd <repo>` and one command mixing citadel
  paths with repo commands; macOS `sed -i` needs `-i ''`; `ScheduleWakeup` is for /loop only; `wip/*`
  branches are kept; test-writer + zig-developer cost ~$3.4 vs ~$1.5 writing directly.

## Standing backlog

Plans 001-005 closed (issues #3, #20, #27, #42, #55); v0.4.0 tagged 2026-10-19 (v0.3.0 2026-10-14).
Plan 006 (Phase 3A TOML 1.0) closed, v0.5.0 tagged 2026-10-28 (milestone #67 closed). Plan 007
(msgpack + CBOR, v0.6.0) proposed in PR #80, awaiting human merge.

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

Plan 007 PR #80 merge, then its item 1 (ADR 0006); see the newest cycle block.
Toolchain: `~/.zr/toolchains/zig/0.16.0/zig` for local dev; global `zig` stays 0.15.2.
