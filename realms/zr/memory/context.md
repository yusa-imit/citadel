# zr — context

last_seen_at: 2026-09-11T00:20:00Z
rejected_plans: []

## Cycle 6 — 2026-09-11 — FEATURE
- Preflight: tree clean on `fix/wasm-leb128-shift-overflow` (= PR #163's already-pushed head) —
  no preservation needed; checked out main. CI green (headSha matched origin/main).
- Inbox: merged PR #163 (LEB128 shift-overflow fix), all 7 checks green, `auto-merged` label,
  branch deleted. No bug/question/directive issues, no new comments since watermark. PR #30
  still draft/OWNER, untouched. No plan PR open; milestone #155 open.
- Implemented milestone #155/plan 001 item 3 continuation: assertion baseline for 11 more
  `config/parser.zig` private helpers (`validateSectionHeader`, `dupeDeps`, `dupeEnv`,
  `parseSettingsTaskArray`, `parseInlineTableField`, `stripQuotes`, `unescapeTomlString`,
  `finalizeWorkflowMatrix`, `bracketDelta`, `countTripleQuotes`, `joinMultilineValues`) — same
  stdx.assert/maybe pattern as PRs #158-160, 33 new characterization/boundary tests added
  before the assertions. `zig build test` 1844/0 failed, `zig build tidy` 0 failing. PR #164
  opened at the cycle deadline; commented "awaiting CI", left for next cycle's inbox to merge.
- Item 3 still unchecked: `flushProfile`, `flushCurrentTemplate`, `flushCurrentHook` (all in
  `parser.zig`, lines ~6165-8300), and `parseToml` itself (~5100 lines, the file's one `pub fn`)
  remain uninstrumented. zuda/sailor still at v2.x (v2.3.0/v2.99.0) — every item 5+ (0.16
  migration proper) stays blocked.
- Next: merge #164 once green (or fix if red), then finish parser.zig's remaining 4 targets
  (the 3 `flush*` helpers, then decide how to bound `parseToml` itself — likely targeted
  entry/exit assertions rather than per-line coverage of a 5100-line function) to close item 3.
- Open questions: none.

## Cycle 5 — 2026-09-11 — STABILIZATION
- Preflight: tree clean on `fix/tui-profiler-catch-unreachable-proof` (= PR #162's already-
  pushed head) — no preservation needed; checked out main. CI green.
- Inbox: merged PR #162 (last `catch unreachable` proof comment, `tui_profiler.zig`), all 7
  checks green, `auto-merged` label, branch deleted. No bug/question/directive issues, no new
  comments since watermark. PR #30 still draft/OWNER, untouched. zuda/sailor still at v2.x —
  0.16 migration (plan 001 item 3 continuation) stays blocked.
- Cycle 5 of 5 forces STABILIZATION regardless of CI/bug state. Ran `tidy-auditor`: 12
  `catch unreachable` sites now all proven (PR #162 landed the last one); found a **real
  safety bug**, not just a style gap — `plugin/wasm_runtime.zig`'s `readVarU32`/`readVarI32`/
  `readVarI64` LEB128 decoders used `while (true)` with a shift counter too narrow (`u5`/`u6`)
  for its own `+= 7` increment on the final byte of a maximal-width encoding. For the signed
  decoders this panics on ANY legitimate 5-byte SLEB128 `i32` or 10-byte SLEB128 `i64` value
  (not just malformed input) — reproduced with a test before fixing (bytes for `i32` min
  panicked at the increment). Fixed via TDD: 6 regression tests (max-width boundary + one-
  byte-too-many negative space for u32/i32/i64), widened `shift` to `u8`, bounded
  `while (true)` → `for (0..bytes_max)`, added shift-bound + buffer-position assertions.
  Code-reviewer caught one WARNING (assertions weren't paired pre/post) — added a
  `self.pos <= self.data.len` postcondition before each return. `zig build test` 1816/0
  failed, `zig build tidy` 0 failing. PR #163 opened at the cycle deadline (3 min left after
  the audit/fix/review round-trip) — commented "awaiting CI", left for next cycle's inbox.
- Next: merge #163 once green (or fix if red). Remaining audit findings for future cycles,
  smallest-diff-first: `config/lock.zig:249`/`exec/cache_store.zig:257`/
  `versioning/changelog.zig:121` (unbounded days→year `while(true)`, same mechanical fix
  three times), `graph/topo_sort.zig:173`/`config/loader.zig:50` (bound by node count/path
  depth), then 223 missing `//!` headers (batch by directory), then extend `assert(` coverage
  to the 23 zero-assertion modules (`cli/` largest at 424 fns), then `std.debug.print` in
  `config/parser.zig`/`exec/scheduler.zig` (logger-injection vs. ban-list decision), then
  decomposing `parseToml`/`main.zig:run`. Full audit detail not preserved verbatim — re-run
  `tidy-auditor` next stabilization cycle rather than trusting this list to stay current.
- Open questions: none.

## Cycle 4 — 2026-09-09 — FEATURE
- Preflight: tree dirty on `feat/assertion-baseline-parser-toml` (= main, uncommitted-only,
  interrupted mid-session assertion-baseline work on `config/parser.zig`) — preserved to
  `wip/feat-assertion-baseline-parser-toml-20260909`, pushed, then returned to main. CI green.
- Inbox: no bug/question/directive issues, no comments since watermark, no plan PR open.
  Milestone #155 open; PR #30 still draft/OWNER, untouched.
- Cherry-picked the preserved wip commit onto a fresh `feat/assertion-baseline-parser-toml-v2`
  and finished it: continued milestone #155/plan 001 item 3 onto `config/parser.zig` (the last
  file for that item) — stdx assert/maybe on `parseTaskParamsArray`, `tryAddGroupConfig`,
  `parseScopeValue`, `dupeConstraintScope`, `copyConditionalDep`, `copyTaskHook`,
  `flushPendingStage`, `parseTasksArrayWithParams`; extracted `parseInlineParamsMap` (out of
  `parseTasksArrayWithParams`) and `splitTopLevelBraceTables` (out of `parseTaskParamsArray`,
  needed to keep it under the 70-line tidy ratchet after adding assertions — same
  extract-to-satisfy-tidy pattern as cycle 3's `finalizeKey()`); both new helpers carry their
  own assertions. 4 new characterization tests (`stripQuotes`/`bracketDelta`/
  `countTripleQuotes`/`parseInlineTableField`). `zig build test` 1810/0 failed, `zig build
  tidy` 0 failing. PR #160 opened; Build & Unit Test and Integration Test passed, cross-compile
  matrix still running at the cycle deadline — commented, left for next cycle's inbox to merge.
  Milestone item 3 stays unchecked: `parser.zig` still has ~18 private helpers plus the
  5,100-line `parseToml` itself without assertions, and the plan's 12 `catch unreachable` proof
  comments (all still in `util/tui_profiler.zig`, `output/man.zig`, `cli/list.zig`,
  `cli/plugin.zig` — untouched by any cycle so far) are separate, real remaining work.
- Next: merge #160 once green (or fix if red), then either finish the rest of `parser.zig`'s
  assertion coverage or start on the 12 `catch unreachable` proof comments — both still count
  as item 3, not yet checked off.
- Open questions: none.

## Cycle 3 — 2026-09-08 — FEATURE
- Preflight: tree clean on `feat/assertion-baseline-dag-scheduler` (= PR #158's head, already
  pushed) — no preservation needed; checked out main after confirming. CI green on main.
- Inbox: merged PR #158 (assertion baseline for dag.zig/scheduler.zig), squash + auto-merged
  label, branch deleted. No bug/question/directive issues. PR #30 still draft/OWNER, untouched.
- Implemented milestone #155 item 3 continuation: assertion baseline for `src/cache/store.zig`
  (the file plan 001 calls `cache/local.zig`, which doesn't exist — `store.zig` is the actual
  local-cache module; `remote.zig` is the S3/GCS/Azure/HTTP one). Same stdx pattern as #158 on
  all 10 public `CacheStore` fns, 2 new characterization tests (empty-cmd boundary, glob-miss
  negative space), and a `finalizeKey()` extraction to keep `computeKeyWithSources` under the
  70-line tidy ratchet after adding assertions (was 74 lines, would have needed a baseline bump).
  Deliberately dropped a `hasHit(key)` postcondition on `recordHit` I initially added — assert
  arguments are always evaluated even in ReleaseFast, so it would add a real stat() syscall on
  every task-completion call; removed rather than accepted as hidden cost. `zig build test`
  (1804/0 failed) and `zig build tidy` (0 failing) green locally. PR #159 opened, CI running,
  left for next cycle's inbox (cycle deadline reached before checks completed).
- Next: merge #159 once green (or fix if red), then item 3's last file (`config/parser.zig`,
  8194 lines / one 5112-line `parseToml` — will need real scoping thought, not a straight port
  of the same per-function pattern).
- Open questions: none.

## Cycle 2 — 2026-09-08 — FEATURE
- Preflight: tree dirty on `feat/assertion-baseline-hot-modules` (scheduler.zig/dag.zig,
  low-quality padding assertions + unrelated fmt churn from an interrupted session) —
  preserved to `wip/feat-assertion-baseline-hot-modules-20260908`, pushed, not reused.
- Inbox: CI green, no bug/question/directive issues, plan 001 (#154) merged, PR #30 still
  draft/untouched. Ticked milestone #155 item 2 (tidy step, #157 merged last cycle).
- Implemented item 3 partial: added `src/stdx.zig` (assert/assert_always/maybe helpers) and
  clean pre/post/invariant assertions to every public fn of `graph/dag.zig` (+
  `checkInvariants()`) and `exec/scheduler.zig`. Found a real bug while doing it: an
  `assert(results.items.len <= needed.count())` postcondition on `scheduler.run` was **false**
  for `deps_serial` tasks (serial-chain deps aren't in `needed`, so results can exceed it) —
  caught by a panic in an existing test, fixed by replacing the wrong assert with `stdx.maybe`.
  PR #158 opened; awaiting CI. `config/parser.zig`/`cache/local.zig` remain for item 3.
- `zig build tidy`'s ratchet-only-shrink baseline caught 2 real issues: `dag.zig` line-length
  grew past its 3-violation baseline from my own additions (fixed by shortening lines, not
  bumping baseline); `scheduler.zig`'s `run`/`loadAndMergeEnvFiles` function-length grew from
  the repo's auto-fmt-on-save hook reformatting unrelated code in a touched file (baseline
  bumped, since that's real growth I can't avoid, not hidden debt).
- Next: merge #158 once green (or fix if red), then item 3 remainder (parser.zig, cache/local.zig).
- Open questions: none.

## Cycle 1 — 2026-09-06 — FEATURE
- Preflight found the tree dirty on `feat/tidy-build-step` (uncommitted `tidy` build-step work
  from a prior session: `tools/tidy.zig`, `build.zig` wiring, `tidy_baseline.txt`) — preserved
  to `wip/feat-tidy-build-step-20260907`, pushed, then returned to `main`.
- Inbox: CI green, no bug issues, no plan PR open, plan 001 (#154) merged, milestone #155 open
  with item 1 done. PR #30 (zuda graph migration) still draft/OWNER — untouched per rule
  (never touch draft PRs); listed for a future cycle's decision, not acted on.
- Implemented milestone #155 item 2 (`tidy` build step): finished the wip work into
  `feat/tidy-build-step-lint`. Found and fixed a real **use-after-free** in the vendored
  `tools/tidy.zig`'s `checkFunctionLength` — see `debugging.md`. Same bug lives in
  `citadel/templates/tidy` upstream; not fixed here (out of scope for a realm session — only
  `/report` may touch citadel — but flagged for a citadel cycle).
- PR #157 opened; `Build & Unit Test` and `Integration Test` green, 6-target cross-compile
  matrix still running at the cycle deadline. Comment posted on the PR; left for next cycle's
  `/inbox` to merge once green (or fix if red).
- Next: merge #157 once CI is green, tick milestone #155 item 2, then item 3 (assertion
  baseline) or item 4 (wip/advanced-retry-config + PR #30 decision) — both unblocked.
- Open questions: none.

## Cycle 0 — 2026-09-05 — RESTRUCTURE
- Realm created by citadel restructure. Memory migrated from the repo's former
  `.claude/memory/` (MEMORY.md, project-context.md, architecture.md, decisions.md,
  debugging.md, patterns.md, zig-0.15-migration.md — condensed into this directory).
- Working tree at survey time was dirty with a finished, tested feature (advanced retry
  config: backoff multiplier, jitter, max backoff, retry-on codes/patterns in
  `src/config/parser.zig`/`types.zig`) — preserved on branch `wip/advanced-retry-config`
  rather than committed directly or discarded. Land it via a real PR in an early cycle.
- First plan `001` (Zig 0.16.0 migration) prescribed by `citadel/docs/ROADMAP.md` — blocked
  on zuda v3.0.0 and sailor v3.0.0 (their own `build.zig` must migrate off `linkLibC()`
  first). Do not start 0.16 migration work until that unblocks; do not write new 0.15-only
  code in the meantime either (kingdom convention).
- Next: open plan 001 PR if not already open → await human merge. In parallel (not gated on
  the plan), triage: PR #30 (zuda graph-algorithm migration, decide merge vs close), the
  root/docs hygiene cleanup (see STATE.md), and the zuda dependency's non-tag git pin.
- Open questions: none.

## Standing backlog (carried from the repo's old project-context.md)

- Decide open PR #30 "chore: migrate to zuda for graph algorithms" (yusa-imit/zr) — recorded
  decision already keeps topo sort / cycle detection / work-stealing deque custom for perf,
  so this PR may be supersedable rather than mergeable as-is; check its diff against that.
- Commit or formally supersede the advanced-retry-config work on `wip/advanced-retry-config`
  (finished and tested, was never committed).
- `zuda` pinned by `git+...?ref=main#<hash>` instead of a tag, and at v2.0.4 while `silica`
  pins v2.3.0 — both violate kingdom rules (tag-only pins, one version kingdom-wide); already
  flagged in `citadel/docs/KINGDOM.md` ROADMAP Phase 0.
- README/CLAUDE.md-era docs had stale version numbers (README badge v1.84.0 vs actual
  v1.114.0) and a stale module-structure diagram — resolved by this restructure replacing
  `CLAUDE.md` with `REALM.md`/`STATE.md`; keep those current going forward instead.
- Milestone backlog was empty at survey time ("READY milestones: 0") — establish the next
  milestone via a plan PR rather than free-form feature work.

## Current priority

Root/docs hygiene PR first (delete tracked `.o` binary, move root release-notes/scripts,
remove `.claude`/`CLAUDE.md`, drop or gitignore stray `zig-pkg/`), then PR #30 triage and the
retry-config branch, then begin plan `001` prep once zuda/sailor v3.0.0 land.
