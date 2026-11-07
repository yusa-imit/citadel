# sigil — context

last_seen_at: 2026-11-08T00:00:00Z
rejected_plans: []

## Cycle 94 — 2026-11-08 — FEATURE

- Done: plan PR #96 (plan 008 csv + proto) still OPEN; inbox read it: only 2 comments, both the AI's own
  status notes (account `yusa-imit` is shared, so authorship alone does not make a comment a human
  answer; none is a change request). One stabilization filler: PR #98 wrapped the remaining prose lines
  >100 cols (PRD 4, README intro, 000-inherited 2) and rewrote the Korean README intro (it called
  JSON/TOML/msgpack/CBOR "planned"). CI 8/8, merged (bec2f49). Written directly, ~$0.45.
- State: disk gate 20 GB (passed, minimum), CI green on main, no issues, repo clean on main.
- Next: once #96 is merged, open "milestone: 008 csv and proto" and do item 1 (ADR 0007 via `architect`);
  if closed unmerged, record reason, plan YAML 3B or config 5A. Docs >100 col filler is done (only the
  README badge URL line and table rows remain, both exempt).
- Blockers: none. Open questions: reflect omit-null note from PR #80 still open.
- Learned: `awk length()` counts bytes, so Korean lines show as false >100 col hits; count chars with
  `python3 -I`. `git checkout -b` with a separate `git push` call works fine.

## Cycle 93 — 2026-11-07 — FEATURE (no-op: disk gate)

- Done: nothing. Preflight disk gate read 18 GB (< 20), so the cycle stopped before inbox. Memory only.
- State: plan PR #96 (plan 008 csv + proto) last seen OPEN with 2 comments, still unread (gate stops
  before inbox; only `yusa-imit` counts). Repo clean on main at 7987f20.
- Next: when disk >= 20 GB, inbox first and read #96's comments; if merged, open "milestone: 008 csv and
  proto" and do item 1 (ADR 0007 via `architect`); if closed unmerged, record reason, plan YAML 3B or
  config 5A.
- Blockers: disk 18 GB free on /. Open questions: reflect omit-null note from PR #80 still open.

## Cycle 92 — 2026-11-06 — FEATURE (no-op: disk gate)

- Done: nothing. Preflight disk gate read 17 GB (< 20), so the cycle stopped before inbox. Memory only.
- State: plan PR #96 (plan 008 csv + proto) still OPEN (2 comments, not read this cycle: the gate
  stopped the cycle first; next cycle's inbox must read them, only `yusa-imit` counts).
- Next: when disk >= 20 GB, inbox; if #96 merged, open "milestone: 008 csv and proto" and do item 1
  (ADR 0007 via `architect`); if closed unmerged, record reason and plan YAML 3B or config 5A.
- Blockers: disk 17 GB free on /. Open questions: reflect omit-null note from PR #80 still open.

## Cycle 91 — 2026-11-06 — FEATURE

- Done: plan PR #96 (plan 008 csv + proto) still open, no comments; so one stabilization filler: README
  docs drift (toml/msgpack/cbor were "stub/planned", install tag said v0.4.0): PR #97, CI 8/8, merged
  (7987f20). Written directly. ~$0.4.
- State at start: CI green on 6d8f7ba, no open issues, repo clean on main, disk gate 20 GB (exactly the
  minimum, passed).
- Next: once #96 is merged by the human, open milestone issue "milestone: 008 csv and proto" and implement
  item 1 (ADR 0007 via `architect`). If #96 closed unmerged, record reason in decisions.md and plan YAML 3B
  or config 5A. Filler left: docs lines >100 cols (PRD.md ~33, 000-inherited.md 6; README line 5 Korean
  intro still says "planned" and is 532 cols).
- Blockers: none. Open questions: reflect omit-null note from PR #80 still open.
- Learned: `gh run watch <id> --interval 20 --exit-status` is the way to wait for CI; get the id from
  `gh pr checks`/`gh run list --branch`.

## Cycle 90 — 2026-11-06 — FEATURE

- Done: plan 008 (Phase 4CD: csv + proto, 11 items, v0.7.0 MINOR) written directly (no planner
  subagent, cheaper) and proposed as PR #96, awaiting merge (citadel#98). ~$0.45.
- State at start: CI green on 6d8f7ba, no open PRs/issues, repo clean on main, disk 26 GB.
- Next: once #96 is merged by the human, next cycle opens milestone issue "milestone: 008 csv and
  proto" and implements item 1 (ADR 0007, design via `architect`). If #96 is closed unmerged,
  record the reason in decisions.md and plan a different theme (YAML 3B or config 5A).
- Blockers: none. Open questions: none new (reflect omit-null note from PR #80 still open).
- Learned: the guard blocks a Bash command mixing citadel paths with repo commands (split them).

## Cycle 89 — 2026-11-05 — FEATURE

- Done: milestone #84 items 10 and 11 (11/11, closed). PR #94 (benchmarks) macOS job had been cancelled
  by the runner; `gh run rerun --failed`, then CI 8/8, labelled auto-merged, merged. Item 11 PR #95
  (`chore: release v0.6.0`: build.zig.zon + `sigil.version` 0.6.0, CHANGELOG [0.6.0], 4A/4B ticked, plan
  item ticked), CI 8/8, merged; `v0.6.0` tagged and `gh release create` done. No consumer names sigil, so
  no migration issue. Written directly, no subagents. ~$0.65.
- Next: no open plan and no milestone issue: `/plan sigil` (newest plan 007 fully checked). Candidate
  themes: msgpack encode tuning (591 MB/s vs PRD 1 GB/s), YAML (3B), CSV (4D), proto (4C), `config`
  loader, tools/tidy.zig self-exemption. Blockers: none.
- Learned: a runner-cancelled macOS job (no steps, "cancelled") is infra, not red; `gh run rerun <id>
  --failed` re-runs it, cross-compile jobs start only after both Build & Test jobs pass (wait for all 8);
  the guard blocks `cd citadel/... && echo > file` (use Write for memory files).

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
