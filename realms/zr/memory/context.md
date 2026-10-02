# zr — context

last_seen_at: 2026-10-03T00:00:00Z
rejected_plans: []

## Cycle 13 — 2026-10-03 — FEATURE
- Preflight: tree clean on `main`; CI green. Disk 73GB free. Inbox: no owner comments, no open
  PRs, only issue is milestone #155; zuda/sailor tags still v2.3.0 / v2.99.0, so items 5-11 stay
  blocked → one `/stabilize --one`.
- Fixed `plugin/builtin_git.zig`: four git queries read stdout with an unbounded `while (true)`.
  Extracted `collectStdout` + `readBounded` (16 MiB, bounded `for`, child killed on overflow,
  new `error.OutputTooLarge`; read error still = end of stream), 8 tests (fake source + real
  child), `//!` header. PR #175 merged, 8/8 green (~14 min). `zig build test` 1900/0, tidy 0
  failing; baseline: dropped builtin_git `doc-header`.
- Gotchas: Bash `grep --include` fails under zsh glob (use plain `grep -rn pat dir`); stopping a
  pipe read early without killing the child would deadlock `wait()`, so kill on overflow.
- Next: remaining `while (true)`: cli/add*.zig, show.zig, template.zig, exec/remote.zig x4,
  process.zig, config_editor.zig (watch/*, mcp/lsp/jsonrpc/registry servers are likely event
  loops — check); ~220 missing `//!` headers; zero-assert modules. Cycle 15 is STABILIZATION.
  Watch zuda/sailor v3.0.0 tags.
- Open questions: none.

## Cycle 12 — 2026-10-02 — FEATURE
- Preflight: tree clean on `main`; CI green (headSha matched origin/main). Disk 56GB free.
  Inbox: no comments, no open PRs, only issue is milestone #155; zuda/sailor tags still v2.3.0 /
  v2.99.0, so items 5-11 stay blocked → one `/stabilize --one`.
- Fixed `plugin/install.zig`: `installLocalPlugin` copied each file with an unbounded
  `while (true)`. Extracted `copyBounded` (64 MiB per file, bounded `for`, new
  `InstallError.FileTooLarge`), 6 fake-stream tests, added `//!` header. PR #174 merged, 8/8
  green (~14 min). `zig build test` 1892/0, tidy 0 failing; baseline: dropped install.zig
  `doc-header`. `cli/plugin.zig` falls into `else => return err` for the new variant (no
  friendly message yet).
- Gotchas: guard hook blocks compound `cd X; grep ...` commands; Grep tool unavailable, use
  `grep` via Bash plain. `for` loop over `bytes_max + 1` pattern works for generic `anytype`
  source/sink helpers.
- Next: remaining `while (true)`: builtin_git.zig x4, cli/add*.zig, show.zig, template.zig,
  exec/remote.zig x4, process.zig, config_editor.zig; ~220 missing `//!` headers; zero-assert
  modules. Cycle 15 is STABILIZATION. Watch zuda/sailor v3.0.0 tags.
- Open questions: none.

## Cycle 11 — 2026-10-01 — FEATURE
- Preflight: tree clean on `main`; CI green (headSha matched origin/main). Disk 46GB free. Only
  open issue is milestone #155; zuda/sailor tags still v2.3.0 / v2.99.0, so items 5-11 stay
  blocked → one `/stabilize --one`.
- Fixed `plugin/registry_client.zig`: `get` read the HTTP response with an unbounded
  `while (true)` (same defect as #172). Extracted `readResponseBounded` (8 MiB, bounded `for`,
  read error → `NetworkError`, oversize → `InvalidResponse`), 6 fake-stream tests, added `//!`
  header. PR #173 merged, 8/8 green. `zig build test` 1886/0, tidy 0 failing; baseline: dropped
  registry_client `doc-header`, `get` 85→76.
- Gotchas: a stale `.zig-cache` ("failed to spawn build runner ... FileNotFound") is fixed by
  `rm -rf .zig-cache` (gitignored). CI matrix took ~12 min from push; `gh pr checks` polls fine.
- Next: 18 remaining `while (true)` (plugin/install.zig:235 file copy, builtin_git.zig x4,
  cli/add*.zig, show.zig, template.zig, exec/remote.zig, process.zig), ~220 missing `//!`
  headers, zero-assert modules, `std.debug.print`. Watch zuda/sailor v3.0.0 tags.
- Open questions: none.

## Cycle 10 — 2026-09-30 — STABILIZATION (n%5==0)
- Preflight: tree clean on `fix/bound-topo-sort-level-loop` (= PR #171 head); CI green on main.
  Disk 42GB free. No open bugs/questions; milestone #155 items 5-11 still blocked (zuda v2.3.0,
  sailor v2.99.0).
- Merged #171 (all 8 checks green after last cycle's livereload flake re-run).
- Fixed `upgrade/checker.zig`: `getLatestRelease` read the GitHub response with an unbounded
  `while (true)` into a growing buffer (memory-exhaustion by a hostile server). Extracted
  `readResponseBounded` (8 MiB, `for (0..bytes_max + 1)` + proof comment), 6 tests via a fake
  stream (empty, under, exactly-at, limit+1, endless peer, read error), added `//!` header.
  PR #172 merged, 8/8 green. `zig build test` 1880/0, tidy 0 failing; baseline: dropped
  checker `doc-header`, `getLatestRelease` 100→92.
- Gotchas: Bash guard blocks compound commands that write under citadel paths (even `echo >
  /tmp` in the same line as citadel vars) — run simple commands. No `timeout` on macOS; use a
  sleep loop for CI waits. Don't add `auto-merged` label before merge. Stale tidy baseline
  entries fail tidy — remove them when a fix clears them.
- Next: audit backlog, smallest-diff-first: 19 remaining `while (true)` (plugin/install.zig:235,
  registry_client.zig:247, builtin_git.zig x4, cli/add*.zig, show.zig, template.zig), 222
  missing `//!` headers, zero-assert modules, `std.debug.print` in 15 files. Watch zuda/sailor
  v3.0.0 tags.
- Open questions: none.

## Cycle 9 — 2026-09-29 — FEATURE
- Preflight: tree clean on `fix/bound-cli-common-parent-walk` (= PR #170 head); CI green on
  main. Merged #170 (all 8 checks green, labelled `auto-merged`). No issues besides milestone
  #155; zuda/sailor still v2.3.0 / v2.99.0 so items 5-11 stay blocked → one `/stabilize --one`.
- Fixed `graph/topo_sort.zig` `getExecutionLevels` unbounded `while (true)` →
  `for (0..processed.count() + 1)` with `else unreachable` proof (PR #171), 2 new tests (40-node
  chain boundary, cycle after acyclic prefix). `zig build test` 1874/0, tidy 0 failing, function
  stays at its 87-line baseline. CI: Integration green; Build & Unit Test failed on the flaky
  `watch.livereload ... respects configured port across restarts` (AddressInUse, unrelated);
  re-ran failed job, left "merge next cycle" on #171.
- Gotchas: `graph/dag.zig` `addEdge` keeps edge endpoints by slice (only vertices are duped) —
  tests must pass long-lived names (arena), not stack buffers. Bash guard blocks heredocs and
  some `cd X; zig ...` compounds; use Edit tool / plain commands. `zig fmt --check src` on
  global zig 0.15.2 lists 57 files locally though main CI passes — pre-existing, unchanged.
- Next: merge #171 (re-check flake; if livereload flakes repeatedly, fix that test's port use as
  a stabilization task). Then: 223 missing `//!` headers, zero-assert modules,
  `upgrade/checker.zig:75`, `std.debug.print` decision. Watch for zuda/sailor v3.0.0.
- Open questions: none.

## Cycle 8 — 2026-09-28 — FEATURE
- Preflight: tree clean on `main`; CI green (headSha matched origin/main). Disk 85GB free.
- Inbox: no new owner actions since watermark — last cycle's PRs #168/#169 already merged,
  no bug/question/directive issues, no plan PR open, no new comments. Milestone #155 items
  5-11 all still `blocked_by zuda v3.0.0, sailor v3.0.0` (tags still v2.3.0 / v2.99.0) — every
  unblocked item is blocked, so ran one `/stabilize --one` task per protocol.
- tidy-auditor found a fresh instance of the same unbounded-parent-directory-walk defect
  already fixed twice this week (PR #168 timestamp loops, #169 `loader.zig`), this time in
  `cli/common.zig`'s `findConfigPath`. Fixed with the same `for (0..cwd.len + 1) |_|` bound
  pattern + an explicit fallthrough `return null;` (a `for` can exit normally, unlike the old
  `while (true)`). `tidy_baseline.txt`'s `loadConfig` entry bumped 74→86: the fmt-on-save hook
  reformatted 3 unrelated `color.printError(...)` calls in the same touched file (same
  precedent as cycle 2's `scheduler.zig` bump — real unavoidable growth, not new debt).
  code-reviewer: 0 CRITICAL/WARNING. `zig build test` 1872/0 failed, `zig build tidy` 0 failing.
- PR #170 opened; CI's ~12-min matrix still running past the cycle deadline — commented
  "awaiting CI; merge next cycle", left for next cycle's inbox.
- Next: merge #170, then re-run tidy-auditor for the next smallest-diff class (candidates:
  `graph/topo_sort.zig:173` while(true) bound by node count, 223 missing `//!` headers, 21
  zero-assert modules — `cli/` largest at 424 fns, `std.debug.print` ban-list decision for
  `config/parser.zig`/`exec/scheduler.zig`). Watch for zuda/sailor v3.0.0 tags to unblock 5-11.
- Open questions: none.

## Cycle 7 — 2026-09-27 — FEATURE
- Preflight: tree clean on `fix/bound-days-to-year-loops` (= PR #168 head, pushed); CI green.
- Done: merged #168 (bound days→year loops, all 8 checks green). Milestone #155 items 1-4 are
  ticked; items 5-12 are blocked on zuda/sailor v3.0.0 (tags still v2.3.0 / v2.99.0). Ran one
  `/stabilize --one`: PR #169 (bound loader.zig parent-walk `while (true)`), CI green, merged.
  `wip/*` remote branches remain (rule: never delete).
- Next: `topo_sort.zig:173` while(true), missing `//!` headers (223), zero-assertion modules,
  `std.debug.print` decision. Re-run tidy-auditor. Watch for zuda/sailor v3.0.0.
- Open questions: none.

## Cycle 6 — 2026-09-11 — FEATURE
- Preflight: tree clean on `fix/wasm-leb128-shift-overflow` (= PR #163's already-pushed head) —
  no preservation needed; checked out main. CI green (headSha matched origin/main).
- Inbox: merged PR #163 (LEB128 shift-overflow fix), all 7 checks green, `auto-merged` label,
  branch deleted. No bug/question/directive issues, no new comments since watermark. PR #30
  still draft/OWNER, untouched. No plan PR open; milestone #155 open.
- Implemented milestone #155/plan 001 item 3 continuation: assertion baseline for 11 more
  `config/parser.zig` private helpers — same stdx.assert/maybe pattern as PRs #158-160, 33 new
  characterization/boundary tests. `zig build test` 1844/0 failed, `zig build tidy` 0 failing.
  PR #164 opened at the cycle deadline; commented "awaiting CI", left for next cycle's inbox.
- Item 3 still unchecked: `flushProfile`, `flushCurrentTemplate`, `flushCurrentHook`, and
  `parseToml` itself (~5100 lines) remain uninstrumented. zuda/sailor still at v2.x — every
  item 5+ (0.16 migration proper) stays blocked.
- Next: merge #164 once green, then finish parser.zig's remaining 4 targets to close item 3.
- Open questions: none.

## Cycle 5 — 2026-09-11 — STABILIZATION
- Preflight: tree clean on `fix/tui-profiler-catch-unreachable-proof` (= PR #162's already-
  pushed head) — no preservation needed; checked out main. CI green.
- Inbox: merged PR #162 (last `catch unreachable` proof comment), all 7 checks green,
  `auto-merged`, branch deleted. PR #30 still draft/OWNER, untouched. zuda/sailor still v2.x.
- Cycle 5 of 5 forces STABILIZATION regardless of CI/bug state. Ran `tidy-auditor`: 12
  `catch unreachable` sites now all proven; found a **real safety bug**, not just a style gap
  — `plugin/wasm_runtime.zig`'s `readVarU32`/`readVarI32`/`readVarI64` LEB128 decoders used
  `while (true)` with a shift counter too narrow (`u5`/`u6`) for its own `+= 7` increment on
  the final byte of a maximal-width encoding — panics on ANY legitimate 5-byte SLEB128 `i32`
  or 10-byte SLEB128 `i64` value, not just malformed input. Fixed via TDD: 6 regression tests,
  widened `shift` to `u8`, bounded `while (true)` → `for (0..bytes_max)`, paired assertions.
  `zig build test` 1816/0 failed, `zig build tidy` 0 failing. PR #163 opened at the cycle
  deadline — commented "awaiting CI", left for next cycle's inbox.
- Next: merge #163. Remaining audit findings for future cycles, smallest-diff-first:
  `config/lock.zig:249`/`exec/cache_store.zig:257`/`versioning/changelog.zig:121` (unbounded
  days→year `while(true)`, same mechanical fix three times — since fixed via #168),
  `graph/topo_sort.zig:173`/`config/loader.zig:50` (bound by node count/path depth — loader
  fixed via #169), then 223 missing `//!` headers, then extend `assert(` coverage to the 23
  zero-assertion modules (`cli/` largest at 424 fns), then `std.debug.print` ban-list decision,
  then decomposing `parseToml`/`main.zig:run`.
- Open questions: none.

## History (cycles 0-4, 2026-09-05 to 2026-09-09)

Realm created by citadel restructure (cycle 0); memory migrated from the repo's former
`.claude/memory/`. First plan `001` (Zig 0.16 migration + Tiger Style baseline) merged as #154,
milestone tracking issue #155 opened. Cycle 1: `tidy` build step landed (#157) — found and fixed
a real use-after-free in vendored `tools/tidy.zig`'s `checkFunctionLength` (flagged upstream for
`citadel/templates/tidy`, see `debugging.md`). Cycles 2-4: assertion baseline (plan item 3)
landed via `src/stdx.zig`'s `assert`/`maybe` helpers across `graph/dag.zig`, `exec/scheduler.zig`
(#158 — found and fixed a real bug, a false postcondition on `scheduler.run` for
`deps_serial` tasks), `cache/store.zig` (#159), and most of `config/parser.zig` (#160).
Established patterns from this era: extract-a-helper to stay under the 70-line tidy ratchet
after adding assertions (`finalizeKey()`, `parseInlineParamsMap`, `splitTopLevelBraceTables`);
bump `tidy_baseline.txt` only for growth genuinely forced by the fmt-on-save hook reformatting
untouched code, never for growth from one's own additions (fix those instead). Also this era:
preserved dirty working trees to `wip/*` branches at least 3 times (interrupted sessions) —
resolved in `decisions.md` (retry-config landed via #167, PR #30 closed as superseded).

## Standing backlog

- `zuda` pinned by `git+...?ref=main#<hash>` instead of a tag, and at v2.0.4 while `silica`
  pins v2.3.0 — both violate kingdom rules (tag-only pins, one version kingdom-wide); already
  flagged in `citadel/docs/KINGDOM.md` ROADMAP Phase 0. Converges once zr/zoltraak land 0.16.
- Milestone #155 items 5-11 (0.16 migration proper: dependency unblock, mechanical renames,
  `ArrayList` sweep, `io: Io` conversion in 3 batches, tests, release) are entirely blocked on
  zuda v3.0.0 and sailor v3.0.0 tags. Nothing to do there until those land.

## Current priority

Every FEATURE cycle until zuda/sailor tag v3.0.0: inbox triage, then one `/stabilize --one`
Tiger Style fix (smallest-diff-first — see tidy-auditor backlog in Cycle 8/5 above). Once the
tags land: bump `build.zig.zon` (item 5), then mechanical renames → `ArrayList` sweep → `io: Io`
conversion (3 batches) → tests → release v1.115.0, in that order per the plan.
