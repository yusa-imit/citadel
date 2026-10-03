# sigil — context

last_seen_at: 2026-10-04T12:00:00Z
rejected_plans: []

## Cycle 33 — 2026-10-04 — FEATURE

- Done: item 9 of plan 003, `reflect/roundtrip_test.zig` (seeded, 1,000 seeds, matrix of every kind
  incl. hook, Timestamp, Value, String maps, odd-width ints, renamed/deny_unknown structs, 5
  containers deep), via PR #36, CI 8/8, squash-merged; issue #27 at 9/10. tidy 0, fmt clean.
  Inbox: no OWNER activity.
- Process: wrote the test myself (no test-writer), mutation-checked (float `+1.0` in stringify
  fails at seed 0 with the seed logged), one `code-reviewer` (~$0.1): 0 critical / 4 warnings, all
  fixed (a `Coverage` tally fails the test if a matrix branch is never generated, comparator
  mutation tests per field kind, more matrix kinds, asserts). Cycle cost ~$1.5 of $4.
- Learned: `std.log.err` in a test reports the seed (tidy bans `std.debug.print`). `zig test
  --test-filter` on root.zig ran only 1 test; use `zig build test` for the real signal. Do not
  `git checkout` a file holding uncommitted wiring edits during a mutation check; back it up.
- Next: item 10 wire and close (`reflect.zig`/`core.zig` drop `error.NotImplemented`, tick 1A-1D
  in `docs/plans/000-inherited.md`), then plan 003 closes 10/10, version impact none (no tag).
  Blockers/questions: none.

## Cycle 32 — 2026-10-03 — FEATURE

- Done: item 8 of plan 003, `reflect/stringify.zig` (mirror of parse; hooks, options, string maps,
  `Value` deep copy, UTF-8 check), via PR #35, CI 8/8, squash-merged; issue #27 at 8/10. 277 tests
  in the module run, tidy 0, fmt clean. Inbox: no OWNER activity.
- Process: wrote tests myself first (no test-writer, ~$0.7 total before the reviewer), then
  `stringify.zig`; one `code-reviewer` (~$0.2): 0 critical / 5 warnings, all fixed (depth at 127/128
  per container kind via a pre-depthed `Context`, hook self-recursion, array `InputTooLarge`, OOM
  sweep for maps and `Value`, `clone_map` precondition doc). Cycle cost ~$2.3 of $4.
- Learned: `Context` gained `fail_stringify` + `stringify_child` (parse's `fail` stays
  ParseError-typed). `parse.has_hook/string_map_value/assert_supported` are now `pub`. Wire names
  and enum names in results are comptime statics (not copied). The `Value` deep copy is private
  to stringify.zig (not `ValueTree.clone_value` as ADR 0002 consequences said). A long
  `@typeName` of a test-local type truncates the fallback message: declare test types at file
  scope. tidy flags `switch (err)` without a `// proof:` on the same/previous line, and every `pub
  fn` (hooks in tests too) needs 2 asserts.
- Next: item 9 round-trip property test (seeded, 1,000 seeds, matrix of every kind nested 3 deep;
  `parse` -> `stringify` -> `eql`), then item 10 wire and close. Blockers/questions: none.

## Cycle 31 — 2026-10-03 — FEATURE

- Done: item 7 of plan 003, `reflect/parse.zig` tagged unions, `array_hash_map.String(V)` maps and
  the `sigilParse` hook, via PR #34, CI 8/8, squash-merged; issue #27 at 7/10. 296 tests, tidy 0,
  fmt clean. Inbox: no OWNER activity.
- Process: `test-writer` (~$1.1, 3 new `parse_{union,map,hook}_test.zig` + 5 compile-error
  fixtures), I implemented parse.zig myself (green on the first run), tight `code-reviewer`
  (~$0.2): 0 critical / 3 warnings, all fixed (hook + `sigil_options` check, `sigilStringify`
  signature check in `has_hook`, doc line > 100 cols), +2 fixtures.
- Learned: a hooked type never reaches `options.resolve`, so the hook-vs-options check lives in
  `parse.has_hook`. `String(V)` is detected by `T == std.array_hash_map.String(@FieldType(T.KV,
  "value"))`. A void union variant only counts as a container when written as a map.
- Next: item 8 `reflect/stringify.zig` (mirror of parse; `sigilStringify` signature already
  enforced by `parse.has_hook`; reuse it, do not re-derive). Blockers/questions: none.

## Cycle 30 — 2026-10-02 — FEATURE

- Done: item 6 of plan 003, `reflect/parse.zig` structs, `[N]T`, `[]T`, via PR #33, CI 8/8,
  squash-merged; issue #27 at 6/10. Inbox: no OWNER activity. tidy 0, fmt clean, all tests pass.
- Process: `test-writer` (~$1.4, split tests into `parse_rig.zig` + 3 `parse_*_test.zig` files for
  the 800-line limit), then I implemented `parse.zig` myself (no zig-developer, to save budget),
  then a tight `code-reviewer` (~$0.1, 0 critical / 3 warnings, all fixed): slice alignment/
  volatile/allowzero, std hash maps, arrays > `array_bytes_max` (64 KiB, stack bound).
- Learned: `Pointer.alignment` is `?usize` in 0.16 (null = natural). `assert_supported` must not
  recurse into struct fields (recursive `Node` never finishes); element types are checked when
  parsed. Container entry rule: `depth >= nesting_max` -> `TooDeep` (128 pass, 129 fail).
  Bash guard blocks heredocs and `cd <repo> ;` chains; write files with the Write tool.
  `git add` of an already-staged deletion fails the whole `&&` chain; omit that path.
- Next: item 7 `reflect/parse.zig` unions, string maps (`std.array_hash_map.String(V)`, currently
  a compile error via its raw pointer fields), `sigilParse` hook (structs declaring hooks are not
  yet guarded in `struct_supported`). Blockers/questions: none.

## Cycle 29 — 2026-10-02 — FEATURE

- Done: item 5 of plan 003, `reflect/parse.zig` scalars + `reflect/context.zig` (`Path`,
  `Segment`, `Context.fail`/`parse_child`, bounded path-only diagnostics, `position_none`) via
  PR #32, CI 8/8, squash-merged; issue #27 at 5/10. 217 tests, tidy 0, fmt clean. Inbox: no
  OWNER activity.
- Skipped the `code-reviewer` pass: test-writer + zig-developer agents cost ~$3 of the $4 cycle
  budget (test-writer alone ~$1.9). Next cycle: give agents tighter scopes, or review item 5
  alongside item 6.
- Learned: tests live in sibling `context_test.zig`/`parse_test.zig` (wired via `test { _ =
  @import(...) }`) to stay under the 800-line limit. `expect_errors` fixture messages must be
  the tail of the `@compileError` text, so unsupported types read "<T> is not supported".
- Next: item 6 `reflect/parse.zig` structs and sequences. It must delete the
  `tests/compile_errors/parse_struct.zig` fixture and its `build.zig` entry (structs become
  supported). `Context.fail` has no double-write guard; a later call overwrites diag.
- Blockers/questions: none.

## Cycle 28 — 2026-10-01 — FEATURE

- Done: item 4 of plan 003, `reflect/options.zig`, via PR #31 (CI 8/8, squash-merged); issue #27
  at 4/10. `resolve(T)` -> comptime `Table` of `Entry{zig_name, wire_name, has_default}` +
  `deny_unknown_fields`; `find_wire`. 17 compile-error fixtures in `tests/compile_errors/`, run
  as `b.addObject` + `expect_errors` steps from `build.zig` (`compile_error_cases` table).
- Learned: `expect_errors .contains` is really *ends-with* on one compiler output line, so the
  expected text must be the tail of the `@compileError` message. `@Struct(.auto, null, names,
  types, attrs)` builds test structs in 0.16. A non-`pub` `sigil_options` is invisible to
  `@hasDecl` (documented in `resolve`). Reviewer (sonnet) found 5 warnings, all applied.
- Note: a first Bash command mixing `$REALM` citadel paths with repo reads trips the guard;
  keep citadel reads to the Read tool. `/tmp/sigil_start` was never written (blocked), so the
  deadline clock was approximate.
- Next: item 5 `reflect/parse.zig` scalars (also needs `core.diagnostics.position_none`, `Context`,
  `Path` per ADR 0002). Blockers/questions: none.

## Cycle 27 — 2026-10-01 — FEATURE

- Done: item 3 of plan 003 (ADR 0002 reflect contract, design only) via PR #30, CI 8/8,
  squash-merged; issue #27 at 3/10. `architect` (opus) wrote the ADR + PRD 4.2 edit; I wrote
  the files (agent has no Write tool; its output had HTML-escaped `&lt;`/`&amp;` to decode).
- Decisions (in ADR 0002): hooks take `*reflect.Context` (tree, diag, path, depth) not
  `(tree, value, diag)`; `stringify` also takes `diag`; errors split into `ParseError` (11) and
  `StringifyError` (4); `deny_unknown_fields` defaults true; unions externally tagged; path-only
  diagnostics use `line = col = 0` (`core.diagnostics.position_none`, added in item 5);
  `ValueTree.clone_value` needed for `core.Value` fields (item 7/8).
- Next: item 4 `reflect/options.zig` (comptime table from `sigil_options`; compile-error tests
  under `tests/compile_errors/`). Blockers/questions: none.

## History

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

## Standing backlog

Plan 001 (issue #3) closed 11/11. Plan 002 (issue #20) closed 5/5 — Phase 1A/1B done, no tag
(release quirk still applies). Plan 003 (PR #26) awaits human merge — Phase 1C/1D:

- **1C** — `core/unicode.zig`: UTF-8 validation + escape/surrogate primitives.
- **1D** — `reflect/{options,parse,stringify}.zig`: comptime struct<->Value mapping, gated by
  a design-only ADR 0002 item (hook signatures, path-only diagnostics, numeric coercion rules).
- **2A-2C** (after Phase 1) — `json/{scanner,dom,writer}.zig`.
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

Plan 003 is approved (issue #27, 9/10 ticked). Next `/implement` target: item 10 (wire and
close); then close the milestone (version impact none) and `/plan` Phase 2 (json).
Toolchain: `~/.zr/toolchains/zig/0.16.0/zig` for local dev; global `zig` stays 0.15.2.
