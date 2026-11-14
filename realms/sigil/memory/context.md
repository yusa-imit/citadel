# sigil — context

last_seen_at: 2026-11-14T00:00:00Z
rejected_plans: []

## Cycle 106 — 2026-11-14 — FEATURE (no-op, disk gate)

- Disk read 19 GB (< 20); stopped before inbox, memory only. Plan PR #96 last seen OPEN (cycle 105), main
  64c3d6f. Next, Blockers (disk), Open questions: same as cycle 105.

## Cycle 105 — 2026-11-13 — FEATURE

- Done: disk 23 GB (passed). Plan PR #96 (plan 008 csv + proto) still OPEN, no owner comment or review
  (4 comments, all the AI's own). One stabilization filler: ran `zig build bench -Doptimize=ReleaseFast`
  on main; `json.parse(T)` 159.5 MB/s (target > 300 missed, DOM path, 5.67 arena B/input B); PR #100
  filled the PRD section 5 "unmeasured" row, CI 8/8, merged. Now every PRD perf row has a number.
  Other bench numbers unchanged (dom 174, write 465, toml 226/205/601, msgpack 301/588, cbor 144/539).
  ~$0.4, written directly.
- Next: same as cycle 100's Next (merge of #96 -> milestone issue "milestone: 008 csv and proto" -> item 1,
  ADR 0007 via `architect`; closed unmerged -> record reason, plan YAML 3B or config 5A). Fillers left:
  `tools/tidy.zig` self-exemption (full cycle); perf tuning (JSON DOM/serialize/typed, msgpack encode) is
  a later plan.
- Blockers: none. Open questions: reflect omit-null note from PR #80 still open.
- Learned: the guard blocks `sleep N; cmd` (use `gh run watch <id> --exit-status`); `gh pr create --label
  auto-merged` at creation works; `zig build bench` takes ~1 min locally.

## Cycles 90-104 (2026-11-06..13), folded 2026-11-14: plan 008 proposed, PR #96 open, fillers only

- Cycle 90 wrote plan 008 (Phase 4CD: csv + proto, 11 items, v0.7.0 MINOR) directly and proposed it as
  PR #96 (awaiting merge, citadel#98). Cycles 91-104: PR #96 stayed OPEN, no owner comment or review (its
  comments are all the AI's own; account `yusa-imit` is shared, so authorship alone is not a human answer).
- Disk-gate no-ops (disk < 20 GB, stop before inbox): cycles 92-93, 98-99, 101-103.
- Filler PRs, all CI 8/8 and merged: #97 README drift (toml/msgpack/cbor were "stub/planned"), #98 prose
  lines > 100 cols and Korean README intro, #99 PRD section 5 measured column. Cycle 100 error-variant
  audit: every msgpack (11 parse, 5 write) and cbor `ParseValueError` variant is named in a test.
- Tiger Style counts over `src/` clean (52 `catch unreachable` all with proof, max file 747 lines).
- Learned: the guard blocks `cd <repo>;` (use absolute paths / `git -C`), mixing citadel paths with repo
  commands in one Bash call (split them), and `sleep N; cmd` (use `gh run watch <id> --exit-status`, id from
  `gh pr checks`); `awk length()` counts bytes, count chars with `python3 -I` for Korean lines; a
  runner-cancelled macOS job is infra (`gh run rerun <id> --failed`); `gh pr create --label auto-merged`
  works at creation; `zig build bench -Doptimize=ReleaseFast` takes ~1 min.
- Next (unchanged): merge of #96 -> milestone issue "milestone: 008 csv and proto" -> item 1 (ADR 0007 via
  `architect`); closed unmerged -> record reason, plan YAML 3B or config 5A. Filler left: `tools/tidy.zig`
  self-exemption (full cycle); perf tuning is a later plan.


## Cycles 86-89 (2026-11-03..05), folded 2026-11-09: milestone #84 items 6-11, v0.6.0

- Done: cbor tree (PR #90), `cbor/encoder.zig` + `locate.zig` (PR #91; ADR 0006 s8: a locate miss stops
  at the deepest item), vectors (PR #92), `core/binary_property.zig` harness with 1,000 seeds (PR #93),
  benchmarks (PR #94), release v0.6.0 (PR #95, tagged, `gh release create`). No consumer names sigil.
- Numbers: msgpack decode 303 MB/s, encode 591 MB/s (PRD > 1 GB/s NOT met, tuning is a later plan);
  cbor decode 144 MB/s, encode 537 MB/s.
- Interrupted sessions leave green PRs open: label auto-merged and merge them first.
- Learned: `core.value.eql` compares maps in insertion order, so deterministic CBOR round trips need a
  byte-compare; a runner-cancelled macOS job is infra, rerun with `gh run rerun <id> --failed`;
  cross-compile jobs start only after both Build & Test jobs pass; `zig test src/root.zig
  --test-filter <name>` shows the real `expect` line; tidy fails >100 cols and warns on new pub fns
  with <2 asserts; tests in an imported bench file need `test { _ = binary; }`; the guard blocks
  `cd citadel/... && echo > file` (use Write for memory files).

## History (cycles 0-85, folded 2026-11-05)

- 0-53 (09-05..10-16): realm created; plans 001-005 closed (hygiene + `tidy`, `core/` value/tree/diag/
  number, unicode + reflect contract (ADR 0002), JSON (ADR 0003, JSONTestSuite vendored; `.gitignore`
  `test_*` dropped the corpus, check `git ls-files`), `json.parse(T)`/`stringify`/`parseFile` (PRs #50-#52:
  dom.parse ~145-175 MB/s, write.minified ~480-490), v0.3.0 first tag (PR #53)). Cycle 48 ran out of
  budget (subagents ~$3.4), kept on a `wip/*` branch. `walkDir*` bounded by `dir_depth_max=64`; std 0.16.0
  `dirReadLinux` BADF bug crashed `walkSelectively` on Linux CI (upstream issue if it recurs).
- 54-62 (10-17..23): plan 005 `path/` (PRs #57-#64): `pointer.zig`, `merge.zig` + `clone.zig` (path copying,
  one `tree.root` swap), `patch.zig`, `jsonpath.zig`/`select.zig` (explicit `[nesting_max]Frame` stack),
  `filter.zig` (iterative `deep_equal`; limits segments 32, selectors 64, filters 32, exprs 128, query
  1024). Conformance PR #63: jsonpath-standard vendored, 659 pass / 56 pinned (match/search) / 0
  divergent. Benchmarks PR #64: pointer ~31 ns, `$..*` ~2150 MB/s. v0.4.0 (PR #65), plan 006 PR #66.
- 63-75 (10-23..30): plan 006 TOML 1.0 (milestone #67), PRs #68-#79, one item per cycle (~$0.8-2.4 each):
  ADR 0005 (`Timestamp.Kind`, 17 parse + 6 write variants, depth counts root: 127 pass / 128 `TooDeep`),
  `core.timestamp`, `toml/lexer.zig` (`input_len_max = maxInt(u32) - 16`), `scalar.zig`
  (`number_text_max = 512`), `scratch.zig` (hash index over (parent, key), iterative `materialize`),
  `parser.zig` (explicit `Frame` stack, `nodes_max = len/2 + 2 + depth_max`), `toml.zig` facade
  (`ParseValueError` 17 / `ParseError` 25, reflect failures re-located by `parser.locate`), toml-test
  v2.2.0 vendored (679/679, floats by bit pattern), `writer.zig` (two `Frame` stacks; null optional is
  `Unrepresentable`, omit-null reflect option is an open non-blocking question on PR #80), round-trip
  test (1,000 trees, 205 files, 1,640 mutations), benchmarks (`parse_value` ~228 MB/s, `write_value`
  ~591 MB/s). v0.5.0 (PR #79) also bumps `sigil.version` in `src/root.zig` and its pin test.
- 76-85 (10-30..11-02): plan 007 (msgpack + CBOR, milestone #84) via PR #80, ADR 0006 (PR #85). Pins: `uint`
  only above maxInt(i64); string-only keys; msgpack 11 / cbor 17 parse errors; positions line 1, col =
  offset+1; CBOR indefinite via counting pass; bomb rule vs remaining bytes; msgpack refuses timestamp
  with offset, CBOR tag 0 keeps it; deterministic CBOR = keys shorter-first then bytewise (record in
  `architecture.md` Formats at item 7); `sigil_options.bytes`; runners test-only. Item 2 `msgpack/
  decoder.zig` `Reader` (#86; `input_len_max = maxInt(u32)-1`; prefix-truncation tests must exclude
  container heads), item 3 `parse_value` (#87; `ParseOptions{depth_max,bytes_max,duplicate_key}`, 11
  `ParseValueError`, `core.DuplicateKeyPolicy` moved from json), item 4 `msgpack/encoder.zig` + `locate.zig`
  (#88; shortest heads, f32 only when bit-exact, NaN `ca 7fc00000`), item 5 `cbor/decoder.zig` `Reader`
  (#89; frame stack `{head,left,kind}`, `ScanError` 7). C76-78 filler: ADR 0005 wrap (#81), tests (#82),
  assertions in TOML step fns (#83); open filler: docs lines >100 cols (PRD.md 33, 000-inherited.md 6,
  README 2). C68-69, 84-85: disk gate no-ops (< 20 GB). Open: `@splat(frame_empty)` ~13 KB memset per
  `parse_value` call and `Map.put` rescans (item 10 benchmarks decide).
- Learned: tidy wants a one-line `// proof:` above each `catch unreachable`/`switch (err)` (and `catch
  return` for a one-variant switch), bans `std.debug.print` (use `std.log.err`), `: usize` public params,
  and lines >100 cols (tests, build.zig, docs table rows skipped); `zig fmt` does not wrap; every new
  `*_test.zig` must be imported from its module's `test {}`; `std.mem.indexOf` -> `find`; `///` on a
  `test` is a compile error; `random.uintLessThan(u3, 8)` is a compile error (use `random.int(u3)`);
  `@Struct(.auto, null, names, types, attrs)` builds test structs in 0.16; non-`pub` `sigil_options` is
  invisible to `@hasDecl`, and a new key means updating build.zig's `unknown_option` message; a failing
  test's real message sits before a long leaked error trace; `zig build test` prints "failed command" with
  exit 0 on warn logs (check `$?` via `> log; echo $?`); `std.log.err` in a helper fails a test; global
  `zig` is 0.15, use `PATH=/Users/fn/.zr/toolchains/zig/0.16.0:$PATH` and `--cache-dir /tmp/sigil-cache`;
  guard blocks `cd <repo>;` (use `git -C`), one command mixing citadel paths with repo commands or `git
  checkout -b` with `git push`, python heredocs, `sed -i`, `sleep` loops (use `gh pr checks N --repo
  yusa-imit/sigil`, which says "no checks" for ~1 min after a push); the merge subcommand has no
  `--label` flag (`gh pr edit --add-label` first); no `timeout` on macOS; planner output can be
  HTML-escaped; test-writer + zig-developer ~$3.4 vs ~$1.5 writing directly; `wip/*` branches are kept.

## Standing backlog

Plans 001-005 closed (issues #3, #20, #27, #42, #55); v0.4.0 tagged 2026-10-19 (v0.3.0 2026-10-14).
Plan 006 (Phase 3A TOML 1.0) closed, v0.5.0 tagged 2026-10-28 (milestone #67 closed). Plan 007
(msgpack + CBOR) closed: milestone #84 done 11/11, v0.6.0 tagged 2026-11-05 (cycle 89).

- Housekeeping: populate the empty performance-targets table once a module is benchmarkable.
- Carried stabilization finding (not fixed, sized for a full stabilize cycle or its own plan
  item — confirmed across cycles 15-18 it does not decompose into a smaller safe slice):
  `tools/tidy.zig` (1860+ lines) self-exempt from its own file-length/function-length/ban-list
  checks — `scan_roots` only walks `src/bench/tests`; widening it needs baseline entries for
  ~61 functions plus false-positive triage on path-unconditional ban rules, since
  `checkFunctionLength` and the ban-list checks are fail-severity (not warn like file-length).
  Deliberately kept out of plan 003's scope (a tooling theme, not Phase 1C/1D).

## Next priority

`/plan sigil` for the next theme (plan 007 closed, v0.6.0 released); see the newest cycle block.
Toolchain: `~/.zr/toolchains/zig/0.16.0/zig` for local dev; global `zig` stays 0.15.2.
