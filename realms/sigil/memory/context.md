# sigil — context

last_seen_at: 2026-10-31T15:19:00Z
rejected_plans: []

## Cycle 82 — 2026-11-01 — FEATURE

- Done: milestone #84 item 4 (PR #88, CI 8/8, auto-merged; #84 box 4 and plan box ticked, 4/11).
  Written directly + one sonnet `code-reviewer` (1 critical fixed: ADR s8 relocation was missing).
  Cost ~$2.4, ~14 min.
- Shape: `msgpack/encoder.zig` (`write`, `StringifyOptions{depth_max}`, 5-variant `WriteValueError`,
  frame stack, shortest heads, f32 only when bit-exact, NaN = `ca 7fc00000`, ext 4/8/12 timestamps,
  offset/local = `Unrepresentable`; `InputTooLarge` declared but never returned, over-long = Unrepresentable);
  `msgpack.zig` facade; `msgpack/locate.zig` (`parse(T)` reflect errors -> "byte N: {reflect msg}",
  line 1 col N+1, deepest reachable item on a miss); reflect `sigil_options.bytes` (`Entry.is_bytes`,
  `Context.parse_bytes_child`/`stringify_bytes_child`, `options.bytes_capable`, 7 compile-error fixtures).
  json/toml bytes-field refusal tests added.
- Next: item 5 `cbor/decoder.zig` reader (heads 0-7, ai 0-27, 28-30 refused, indefinite + break, f16,
  UTF-8 text; RFC 8949 App. A items and App. F classes). Blockers: none.
- Reviewer suggestions not taken: bytes_child duplicates parse_child prologue; encoder `run` loop bound is
  maxInt(usize); no reflect-level tests of `parse_bytes_value`/`stringify_bytes_value` (facade covers);
  float subnormal and `local_time`/`local_datetime`/array-map `too_long` encoder cases untested.
  Fold into a small test PR or item 9.
- Learned: tidy flags test/build.zig lines >100 cols (also `.message` strings in build.zig); new
  `sigil_options` key means updating the `unknown_option` message in build.zig; `/tmp/sigil_start` written
  in preflight works.

## Cycle 81 — 2026-10-31 — FEATURE

- Done: milestone #84 item 3, `msgpack/decoder.zig` `parse_value` tree build (PR #87, CI 8/8, auto-merged;
  #84 box 3 ticked, 3/11; plan checkbox ticked in the PR). Written directly + one sonnet `code-reviewer`
  (0 critical; fixed: ext-length-decides test, key-copy test, mixed array/map depth 128, prefix offsets,
  OOM message). `core.DuplicateKeyPolicy` moved from json (re-exported). Cost ~$1.8. ~13 min used.
- Shape: `ParseOptions{depth_max,bytes_max,duplicate_key}`, `BuildError` (8) + `ScanError` + `InputTooLarge`
  = 11 `ParseValueError`; `Builder` with `[nesting_max]Frame{head,left,fill,key,slot,key_pending}`; empty
  container finishes at once; `finish` closes full parents in a bounded loop; end-of-input inside a
  container = `UnexpectedEnd` at the innermost open head; `TrailingBytes` checked via `reader.offset`
  (no extra token read); `.last` skips `dupe_key`; ext length (4/8/12) decides the timestamp form, not the
  head width; `set_diag` shared with `Reader.fail`.
- Next: item 4 `msgpack/encoder.zig` + `msgpack.zig` facade (`parse_value`/`write_value`/`parse`/`stringify`,
  shortest heads, `sigil_options.bytes` in reflect is item 4 too per plan; check the plan text). Blockers: none.
- Reviewer suggestions not taken: `@splat(frame_empty)` costs ~13 KB memset per call (could use undefined;
  benchmark in item 10 decides); `Map.put` rescans (3 scans per member; also item 10).
- Learned: guard blocks `cd <repo>` mixed with chains; use `git -C` or one `cd X && cmd` (worked for zig
  build); `sed -i ''` fine for single-file edits.

## Cycle 80 — 2026-10-31 — FEATURE

- Done: milestone #84 item 2, `msgpack/decoder.zig` pull `Reader` (PR #86, CI 8/8, auto-merged; #84 box 2
  ticked, 2/11). Written directly + one sonnet `code-reviewer` (0 critical, 4 warnings fixed: more tests for
  signed ints, NaN signs, every length form, bomb forms; `///` docs). Cost ~$1.3.
- Shape: `Reader.init/next(diag)`, `Token{offset,item}`, `Item` union (nil, bool, int, uint [only > maxInt(i64)],
  float, str [UTF-8 checked], bin, ext{type,data}, array/map count, end); `ScanError` = UnexpectedEnd,
  ReservedByte, InvalidUtf8; `input_len_max = maxInt(u32)-1`; bomb rule in u64; diag "byte N: reason",
  line 1 col offset+1; `msgpack.decoder` exported, stub `Error` kept until item 4.
- Next: item 3 msgpack tree on `[nesting_max]Frame` (ext -1 timestamps 32/64/96, NonStringKey, DuplicateKey;
  move `DuplicateKeyPolicy` to `core.value`, json re-exports). Blockers: none.
- Learned: the guard blocks one Bash call mixing citadel paths with repo work (split calls); `/tmp/sigil_start`
  was stale, read `date +%s` directly; prefix-truncation tests must exclude container heads (a header alone
  is valid once the bomb rule is met).

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
(msgpack + CBOR, v0.6.0) merged; milestone #84, items 1-3 done (3/11).

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

Plan 007 item 4 (`msgpack/encoder.zig` + facade); see the newest cycle block.
Toolchain: `~/.zr/toolchains/zig/0.16.0/zig` for local dev; global `zig` stays 0.15.2.
