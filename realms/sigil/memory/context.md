# sigil — context

last_seen_at: 2026-10-01T00:00:00Z
rejected_plans: []

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

## Cycle 26 — 2026-09-30 — FEATURE

- Done: plan 003 (PR #26) had been merged and milestone issue #27 opened (by cycle 25's tail).
  Merged PR #28 (item 1, `core/unicode.zig` UTF-8 validation; CI 8/8 had passed the day
  before). Implemented item 2 via PR #29, CI 8/8, squash-merged: `core/unicode_escape.zig`
  (`encode`, `parse_hex4`, `decode_utf16`, `write_escaped` with `minimal`/`ascii_only`).
  Issue #27 at 2/10. Local: 144 tests, tidy 0/0, fmt clean.
- Decisions: escape primitives live in `unicode_escape.zig`, not `unicode.zig` (that file was
  already 740 lines; adding them pushed it past the 800 soft limit and tidy's line/ban/assert
  checks failed). `core.zig` re-exports both. DEL (U+007F) is escaped as `\u007f` because TOML
  and YAML forbid it raw; reviewer (sonnet) caught it. `catch unreachable` needs `// proof:` on
  the same line or the one before, and the line must stay <= 100 columns.
- Process slip: wrote the implementation before the tests for item 2 (no red step); recovered
  by a mutation check (weakening `decode_utf16` made a test fail). Do the red step first.
- Note: `timeout` is absent on this macOS; use `gh pr checks --watch` directly. Bash `cd` into
  the repo trips the guard hook; the session cwd is already the repo.
- Next: item 3, ADR 0002 reflect contract (design only, `architect`/opus), then item 4
  `reflect/options.zig`. Blockers/questions: none.

## Cycle 25 — 2026-09-29 — FEATURE (quiet; counter was 23 at start, cycle 24's report had not written it)

- Done: plan PR #26 (plan 003) still open, no OWNER activity; CI green on main `18ebb6f`; no
  open issues. Ran one `/stabilize --one` slot: test-quality audit of `core/*` — every declared
  error variant (OutOfMemory, OutOfSpace, DuplicateKey, TooDeep, IntegerAboveMax,
  IntegerBelowMin, FloatOutOfRange) is provoked by a test, no always-pass assertions. No PR.
- Note: guard hook rejects Bash commands that mix reads of citadel paths with a `cd` into the
  repo; use the Read tool for citadel files.
- Next: awaiting human merge of plan 003 (#26). Blockers/questions: none.

## Cycle 24 — 2026-09-29 — FEATURE

- Done: merged PR #24 (item 4, cycle 23's `core/number.zig`; CI 8/8 green). Closed out plan
  002 item 5 "wire into root.zig and tidy" via PR #25: wiring was already a side effect of
  #24 (`core.zig` re-exports `value`/`tree`/`diagnostics`/`number`); fixed the one remaining
  gap — `is_decimal_literal` had 0/2 assertions (tidy warning) — by asserting the loop-cursor
  invariant `i <= text.len` on both the early- and late-return paths. Assertion baseline now
  23/23, `zig build tidy` 0 findings (was 1 warning), 96/96 tests green, CI 8/8.
- Plan 002 (issue #20) closed 5/5. Version impact is MINOR in the abstract semver sense, but
  both the plan's own text and `REALM.md`'s release quirk say explicitly: no tag until a
  format module (JSON, Phase 2) makes the library fetchable in practice — closed the issue
  with a summary instead of running `/release`.
- Opened plan 003 (PR #26, `planner`/opus): Phase 1C `core/unicode.zig` (UTF-8 validation +
  escape primitives) and Phase 1D `reflect/{options,parse,stringify}.zig`, gated by a
  design-only ADR 0002 item (reflect hook/error/coercion contract) before any reflect code.
  10 items total. Version impact MINOR, folded into unreleased 0.3.0, no tag (same reasoning
  as above — nothing turns bytes into `Value` yet). Flagged: plan 002's own "Done when" wanted
  1A/1B ticked in `docs/plans/000-inherited.md` but they're still unticked on main — plan 003's
  last item fixes it (not worth a standalone PR).
- Next: awaiting human merge of plan 003 (#26). Once merged, item 1 (`core/unicode.zig`
  validation) is the next `/implement` target. Blockers/questions: none.

## Cycle 23 — 2026-09-28 — FEATURE

- Done: item 4 `core/number.zig` (decimal literal text -> `.int`/`.uint`/`.float`, no silent
  coercion: prefer `.int`, widen to `.uint` only past `maxInt(i64)`, typed overflow only past
  `maxInt(u64)`/`minInt(i64)`) via architect design pass + test-writer + zig-developer +
  code-reviewer (0 CRITICAL/WARNING). Wired into `sigil.core`; plan doc corrected (architect
  found the plan's "one past i64::MAX overflows" was wrong — it's lossless in u64). Local:
  96/96 tests, tidy 0 failing, fmt clean.
- PR #23 (cycle 22) merged since last watermark, per issue #20 comments. PR #24 opened this
  cycle for item 4; CI had not reported by the cycle deadline — commented "awaiting CI; merge
  next cycle" for the next cycle's inbox to pick up. Issue #20 not yet ticked for item 4
  (deferred to the merge, so the checklist matches reality).
- Next: once #24 merges, item 5 "wire into root.zig and tidy" (mostly done as a side effect —
  confirm assertion-baseline count and close out the plan). Blockers/questions: none.

## Cycle 22 — 2026-09-28 — FEATURE

- Done: item 3 `core/diagnostics.zig` (`Diagnostics{line,col,message,snippet}`,
  `DiagnosticsType(comptime limits: Limits)` sizing fixed inline buffers at comptime,
  truncation-with-marker never silent) via PR #23, CI 8/8 green, squash-merged; issue #20 at
  3/5. Re-exported `Diagnostics`/`DiagnosticsType` from `sigil.core`.
- Note: inline generic-struct self-reference can't be named the same as the file-scope public
  alias (`Diagnostics`) — ambiguous reference; named it `DiagnosticsRecord` instead, still a
  real name per Tiger Style 3.10 (no bare `Self`).
- Next: item 4 `core/number.zig` (i64/u64/f64 boundaries), then wiring. Blockers/questions: none.

## Cycle 21 — 2026-09-27 — FEATURE

- Done: item 2 `core/tree.zig` (`ValueTree` arena + dupe_string/bytes/array/key, new_map) via
  PR #22, CI 8/8 green, squash-merged; issue #20 at 2/5. Tidy assertion baseline needs >= 2
  asserts per pub fn (13/13 now).
- Note: guard hook blocks heredoc bash commands; use Write/Edit tools and the absolute zig path
  `/Users/fn/.zr/toolchains/zig/0.16.0/zig`; `rm -rf .zig-cache` fixed a stale build runner.
- Next: item 3 `core/diagnostics.zig`, then number, wiring. Blockers/questions: none.

## Cycle 20 — 2026-09-27 — FEATURE

- Done: plan 002 (#17) was merged by the owner; opened milestone issue #20. Implemented
  item 1 `core/value.zig` (Value, Timestamp, insertion-ordered Map over a caller buffer, bounded
  `eql` returning `TooDeep`) via PR #21, CI 8/8 green, squash-merged. Local 0.16.0 toolchain
  now present at ~/.zr/toolchains/zig/0.16.0.
- Review (sonnet) fixed: eql depth overflow now a typed error (was assert), `put` no longer
  runs O(n^2) `check_invariants`. Note: Map.get is O(n); a hash index may be needed for large
  maps.
- Next: item 2 `core/tree.zig` (ValueTree), then diagnostics, number, wiring. Issue #20 at 1/5.
- Blockers/questions: none.

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

Plan 003 is approved (issue #27, 2/10 ticked). Next `/implement` target: item 3, ADR 0002
(reflect contract, design only), then `reflect/options.zig`.
Toolchain: `~/.zr/toolchains/zig/0.16.0/zig` for local dev; global `zig` stays 0.15.2.
