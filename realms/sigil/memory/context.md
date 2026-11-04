# sigil — context

last_seen_at: 2026-11-05T00:00:00Z
rejected_plans: []

## Cycle 88 — 2026-11-05 — FEATURE

- Done: milestone #84 item 10 (benchmarks), PR #94 opened (not yet merged): `bench/binary.zig` (msgpack/cbor
  decode + encode over the JSON tree re-encoded per format, 739/733 KB), `Inputs.get(format)` in main.zig,
  numbers in 000-inherited.md, plan item ticked, CHANGELOG. Written directly, no subagents. ~$0.75.
- Numbers: msgpack decode 303 MB/s (8.44 arena B/B), encode 591 MB/s (PRD target > 1 GB/s NOT met, recorded,
  tuning is a later plan); cbor decode 144 MB/s (8.53), encode 537 MB/s.
- Next: merge PR #94 first (ubuntu green, macos was queued at the deadline; inbox step 8 merges it: label
  auto-merged, tick item 10 in #84), then item 11 release v0.6.0 (tick 4A/4B in 000-inherited.md, CHANGELOG
  [0.6.0], build.zig.zon + sigil.version 0.5.0 -> 0.6.0, tag, gh release create). Blockers: none.
- Learned: tests in an imported bench file only run via `test { _ = binary; }`; `core.value.eql` returns an
  error union (`try`); `codec: type` params need `.ParseOptions` options built per codec; CI checks listed for
  the PR were only 2 (ubuntu, macos) with macos slow to start.

## Cycle 87 — 2026-11-04 — FEATURE

- Done: milestone #84 items 8 and 9 (9/11). Found PR #92 (item 8 vectors, CI 8/8, left open by an
  interrupted session; repo was on its branch, clean): labelled auto-merged and merged. Then item 9,
  PR #93 (CI 8/8, merged), written directly, no subagents. Cost ~$1.4, ~12 min.
- Shape: `core/binary_property.zig` test-only harness, free fns with `comptime codec: type` (a generic
  `PropertyType` wrapper broke the 70-line tidy cap): `random_root`, `check_tree` (explicit stack),
  `round_trip(mode generated|decoded)`, `check_input` oracle, `mutate`, `run_seeds`, `run_mutations`,
  `fuzz_input`. `msgpack/roundtrip_test.zig` and `cbor/roundtrip_test.zig` supply the codec (CBOR also
  `Deterministic`: byte-stable, no `eql`) + vector bases. 1,000 seeds, 3,464 / 2,256 mutations, arena
  bound 96 B/input byte + 16 KiB passed. No decoder/encoder bug found.
- Next: item 10 benchmarks (`zig build bench`, ~1 MB seeded record tree, record in 000-inherited.md,
  PRD msgpack encode > 1 GB/s), then item 11 release v0.6.0. Blockers: none.
- Learned: `zig test src/root.zig --test-filter <name>` shows the real `expect` line when `zig build
  test` buries it under a leaked json error trace; `zig fmt` does not wrap, tidy fails >100 cols;
  tidy assertion baseline warns on new pub fns with <2 asserts; coverage thresholds must be calibrated
  (generated trees are small, ~4 nodes/seed).

## Cycle 86 — 2026-11-03 — FEATURE

- Done: milestone #84 items 6 and 7 (7/11). Found PR #90 (item 6, cbor tree) open, CI 8/8, left by an
  interrupted session: labelled auto-merged and merged. Then item 7, PR #91 (CI 8/8, merged): written
  directly + one sonnet `code-reviewer` (0 critical, 2 warnings fixed). Cost ~$2.1, ~13 min.
- Shape: `cbor/encoder.zig` (`write`, `StringifyOptions{depth_max, deterministic}`, shortest heads, f16/f32/f64
  by bit-exact test, NaN = `f9 7e00`, deterministic = selection sort shorter-first then bytewise, tag 0 text
  when offset else tag 1 int / exact f64; a timestamp counts as one depth level like the decoder's tag;
  `Refusal` local_kind/text_range/fraction); `cbor.zig` facade; `cbor/locate.zig` (reader-depth based
  `skip_item`, indefinite maps/keys, tags folded into the item offset). ADR 0006 s8 now says a locate miss
  stops at the deepest item (not 1:1).
- Next: item 8 official test vectors (vendor RFC 8949 Appendix A + msgpack-test-suite subset with SOURCE and
  license, runners per ADR s10, assert counts). Blockers: none (disk gate passed at 25 GB).
- Learned: `core.value.eql` compares maps in insertion order, so a sorted (deterministic) round trip needs a
  byte-compare, not `eql`; disk gate recovered (C84-85 no-ops were disk).
- Reviewer suggestions not taken: empty key under deterministic, empty array at depth_max, 128-level decode of
  encoder output, locate first-match under `.last` duplicate policy untested.

## History (cycles 84-85, 2026-11-02)

Disk gate no-ops (19 GB free, need 20); nothing done. Cycle 86 detail above condensed: items 6-7 done.

## History (cycles 82-83, folded 2026-11-03)

C82 item 4 (PR #88): `msgpack/encoder.zig` shortest heads, f32 only when bit-exact, NaN `ca 7fc00000`,
`msgpack/locate.zig`, reflect `sigil_options.bytes`. C83 item 5 (PR #89): `cbor/decoder.zig` `Reader` (frame
stack `{head,left,kind}`, string mode, `complete()` pops finished tags/definite containers; `ScanError` 7).
Learned: tidy flags test/build.zig lines >100 cols and requires `// proof:` above `switch (err)`; `zig fmt`
does not wrap long lines; a test failure's real message sits before a long leaked error trace; a new
`sigil_options` key means updating the `unknown_option` message in build.zig.

## History (cycles 80-81, folded 2026-11-02)

- C80 (10-31): milestone #84 item 2, `msgpack/decoder.zig` pull `Reader` (PR #86): `Token{offset,item}`,
  `Item` union, `ScanError` = UnexpectedEnd, ReservedByte, InvalidUtf8; `input_len_max = maxInt(u32)-1`;
  bomb rule in u64; diag "byte N: reason", line 1 col offset+1. Prefix-truncation tests must exclude
  container heads (a header alone is valid once the bomb rule is met).
- C81 (10-31): item 3 `parse_value` tree build (PR #87): `ParseOptions{depth_max,bytes_max,duplicate_key}`,
  11 `ParseValueError`; `Builder` on `[nesting_max]Frame`; end of input inside a container = `UnexpectedEnd`
  at the innermost open head; ext length (4/8/12) decides the timestamp form; `core.DuplicateKeyPolicy`
  moved from json (re-exported). Open: `@splat(frame_empty)` ~13 KB memset per call and `Map.put`
  rescans (item 10 benchmarks decide). Guard blocks `cd <repo>` mixed with chains: use `git -C`.

## Cycle 79 (folded) — 2026-10-30

Plan PR #80 merged -> milestone #84 (007, 11 items); item 1 ADR 0006 (PR #85, written directly). Pins:
`uint` only above maxInt(i64); string-only keys; msgpack 11 / cbor 17 parse errors; positions line 1, col =
offset+1; CBOR indefinite via counting pass (bound = count of 5f 7f 9f bf); bomb rule vs remaining bytes;
msgpack refuses timestamp with offset, CBOR tag 0 keeps it; deterministic CBOR = keys shorter-first then
bytewise (record in `architecture.md` Formats at item 7); `sigil_options.bytes`; runners test-only.
Learned: `zig build test` exit code via `> log; echo $?` (a pipe hides it).

## History (cycles 76-78, condensed 2026-10-31)

While plan PR #80 waited: C76 PR #81 (ADR 0005 wrapped to 100 cols, inline state set at `{`); C77 PR #82
(tests: inline-table dotted keys, array comments/CRLF, prefix truncation); C78 PR #83 (>=2 asserts in the
TOML parser step fns; open stabilize filler: docs lines >100 cols in PRD.md 33, 000-inherited.md 6,
README 2). Learned: `gh pr merge --label` does not exist (`gh pr edit --add-label` first); guard blocks `cd <repo>;`
compounds and `sleep` loops (use `git -C`, `gh pr checks N --repo yusa-imit/sigil` in an until loop);
python heredoc `\r\n` replace silently misses; tidy flags test lines >100 cols.

## History (cycles 67 and 75, folded 2026-11-01)

C67: item 6 TOML arrays and inline tables (PR #73): `parser.zig` explicit `Frame` stack
(`Need {first, after_comma, comma_or_close}`), `nodes_max = len/2 + 2 + depth_max`; tests split into
`parser_fixtures.zig` + `parser_value_test.zig` (soft file limit 800). Its follow-ups were done in C76-78.
C75: item 12 release v0.5.0 (PR #79), milestone #67 closed 12/12; plan 007 written via `planner`
(PR #80). Open question on PR #80 (non-blocking): reflect option to omit null optionals in
`toml.stringify`. Learned: a release PR also bumps `sigil.version` in `src/root.zig` and its pin test;
planner output can come back HTML-escaped (unescape before writing); global `zig` is 0.15, use
`PATH=/Users/fn/.zr/toolchains/zig/0.16.0:$PATH` and `--cache-dir /tmp/sigil-cache`.

## History (cycles 72-75, condensed 2026-10-29)

C72: item 9 `toml/writer.zig` (PR #76): two explicit `[nesting_max]Frame` stacks (header-form, inline);
trailing run of table-like entries -> `[a.b]`/`[[a]]`, earlier ones inline; `toml.write_value`/`stringify`;
`format_float` moved to `core.number`. Open design note: a null optional is `Unrepresentable` in
`toml.stringify` (omit-null reflect option = question on PR #80). C73: item 10 `roundtrip_test.zig`
(PR #77): 1,000 seeded trees, 205 corpus files, 1,640 mutations, `std.testing.fuzz` entry; no bug found.
C74: item 11 TOML benchmarks (PR #78): `toml.parse_value` 0.44 ms (~228 MB/s), `parse(T)` ~208 MB/s,
`write_value` ~591 MB/s, recorded in `docs/plans/000-inherited.md`. C75: item 12 release v0.5.0
(PR #79), milestone #67 closed; plan 007 written (PR #80).
Learned: mutually recursive generators need an explicit error set; `random.uintLessThan(u3, 8)` is a
compile error (use `random.int(u3)`); a failed test may print an unrelated leaked error-return trace, read
the `expect` line; guard blocks `git checkout -b` mixed with `git push` and `sed -i` chains with them
(separate Bash calls); no `timeout` binary on macOS; `sleep` chains blocked.

## History (cycles 68-71, condensed 2026-10-28)

C68-69: disk gate failed (18/16 GB, need 20), no work. C70: item 7 PR #74, `toml.zig` facade:
`parse_value`/`parse(T, ...)`, `ParseValueError` (17) / `ParseError` (25, comptime-pinned); reflect
failures re-located by `parser.locate` (second parse into throwaway scratch, error path only);
reflect messages are "{path}: {reason}", tests match with `find`. `write_value`/`stringify` landed
with item 9. C71: item 8 PR #75, toml-test v2.2.0 (MIT) vendored in `tests/toml-test/` (887
files); 679 cases, 679 pass, 0 pinned; floats compared by bit pattern, datetimes as
`core.timestamp.parse` values (ADR 0005 s9). `gh api repos/<o>/<r>/tarball/<tag>` into /tmp
fetches a corpus. Cycle 67 follow-ups still open: see cycle 67 below.

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

## History (cycles 54-61, folded 2026-10-29)

Plan 005 `path/`, one item per cycle (PRs #57-#64): `pointer.zig` (`parse` into `[128]Segment`),
`merge.zig` + internal `clone.zig` (path copying, one `tree.root` swap), `patch.zig`, `jsonpath.zig`
compile, `select.zig` (explicit `[nesting_max]Frame` stack), `filter.zig` (iterative `deep_equal`;
core `eql` is not RFC equality; limits filters 32, exprs 128, queries 32). C60 conformance (PR #63):
vendored jsonpath-standard `tests/jsonpath/` (BSD-2, 20ebdcc), 659 pass / 56 pinned unsupported
(match/search) / 0 divergent. C61 benchmarks (PR #64): pointer ~31 ns/lookup, `$..*` ~2150 MB/s.
Learned: `std.log.err` in a helper fails a test (probe tests need a `report` flag); `**` and `++`
share precedence; arena-backed FailingAllocator sweeps hit ~2 failure points, assert content;
`Map.put` rejects duplicates; slice `position` goes negative with negative steps; `-0` parses as 0.

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
(msgpack + CBOR, v0.6.0) merged; milestone #84, items 1-10 done (10/11, item 10 in PR #94).

- Housekeeping: populate the empty performance-targets table once a module is benchmarkable.
- Carried stabilization finding (not fixed, sized for a full stabilize cycle or its own plan
  item — confirmed across cycles 15-18 it does not decompose into a smaller safe slice):
  `tools/tidy.zig` (1860+ lines) self-exempt from its own file-length/function-length/ban-list
  checks — `scan_roots` only walks `src/bench/tests`; widening it needs baseline entries for
  ~61 functions plus false-positive triage on path-unconditional ban rules, since
  `checkFunctionLength` and the ban-list checks are fail-severity (not warn like file-length).
  Deliberately kept out of plan 003's scope (a tooling theme, not Phase 1C/1D).

## Next priority

Plan 007 item 10 (benchmarks), then 11 (release v0.6.0); see the newest cycle block.
Toolchain: `~/.zr/toolchains/zig/0.16.0/zig` for local dev; global `zig` stays 0.15.2.
