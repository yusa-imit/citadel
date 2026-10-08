# zr — context

last_seen_at: 2026-10-08T21:19:00Z
rejected_plans: []

## Cycle 19 — 2026-10-09 — FEATURE
- Preflight: tree clean on `main`; CI green; inbox clear (#155 milestone, #178 informational; only
  new comment was my own report). sailor v3.0.0 tagged, zuda still v2.3.0 → items 5-11 blocked
  → one `/stabilize --one`.
- Removed dead `src/jsonrpc/transport.zig` (228 lines, 0.14 `ArrayList(u8).init` API, imported but
  unused by `mcp/server.zig` so never compiled) + the import + 2 tidy baseline entries. PR #184
  merged, 8/8 green (~13 min). Tests 1928/0, tidy 0 failing. `docs/PRD.md` still lists it in a
  planned layout (also lists nonexistent `json.zig`); left as design text.
- Remaining `while (true)`: add.zig 275/379 and add_interactive.zig 380 are stdin prompt loops that
  end on EOF/empty line but grow unbounded on an endless piped stream; a cap needs a testable seam
  (prompt reads real stdin) — design a `prompt` source injection first. Others (task_picker, tui,
  run.zig:1427, watch/*, servers, process.zig:416, show.zig:458) are event/tail loops or
  EOF-bounded — check each. ~220 missing `//!` headers.
- Gotchas: guard hook blocks `cd X; ...` chains even into the realm repo — use plain commands from
  cwd; `sleep N; cmd` chains are blocked — use `until` loops.
- Next: watch zuda v3.0.0 tag. Cycle 20 STABILIZATION.
- Open questions: none.

## Cycle 18 — 2026-10-07 — FEATURE
- Preflight: tree clean on `main`; CI green; inbox clear (#155 milestone, #178 informational).
  sailor v3.0.0 tagged, zuda still v2.3.0 → items 5-11 blocked → one `/stabilize --one`.
- Fixed `cli/template.zig` `applyTemplate`: two unbounded byte-by-byte stdin loops (param value,
  confirm) → `readReply` helper over shared `line_input.readLine` (4096-byte buffer). Over-long
  param → error, exit 1; over-long confirm → cancelled. 4 tests. PR #183 merged, 8/8 green
  (~13 min). Tests 1928/0, tidy 0 failing, baseline `applyTemplate` 167→137.
- Gotchas: guard hook blocks heredoc appends into the repo (`cat >> file <<EOF`) — use Edit;
  a test-only `anytype` source struct used by `line_input.readLine` from another file needs
  `pub fn read`; `zig test` on a single `src/cli/*.zig` fails (outside module path).
- Next: `while (true)` left: cli/add.zig 275/379 (prompt loops, check bound), task_picker.zig,
  tui.zig, run.zig:1427 (watch loop), process.zig:416 (EOF-bounded), server/watch event loops,
  dead `jsonrpc/transport.zig` (delete vs fix). ~220 missing `//!` headers. Watch zuda
  v3.0.0. Cycle 19 FEATURE; cycle 20 STABILIZATION.
- Open questions: none.

## Cycle 17 — 2026-10-07 — FEATURE
- Preflight: cwd was on `fix/bound-show-line-reader` (clean) → `main`; CI green; PR #181 8/8 green,
  no `hold` → merged. Inbox clear (issue #178 `migration: sailor v3.0.0` is informational,
  origin ai; no owner comments). sailor v3.0.0 tagged, zuda still v2.3.0 → items 5-11 blocked.
- Stabilize --one: three copies of an unbounded byte-by-byte stdin loop (`cli/add.zig`,
  `add_interactive.zig`, `config_editor.zig` x2) → shared `cli/line_input.zig` `readLine`
  (4096-byte caller buffer, `error.LineTooLong`, tail discard ≤ 1 MiB, bounded `for`), 9 tests.
  PR #182 merged, 8/8 green (~12 min CI). Tests 1924/0, tidy 0 failing, `config_editor run`
  baseline 133→113. EOF at the editor confirm prompt still defaults to yes.
- Found: `src/jsonrpc/transport.zig` is dead code (imported by `mcp/server.zig` but unused, uses
  the 0.14 `ArrayList(u8).init` API, never compiled) — decide delete vs fix in a later cycle.
- Gotchas: the fmt-on-save hook reformatted all of `src/main.zig` (+293/-269) on an Edit; undo
  with `git checkout` and insert via `perl -0pi` instead. Only `zig fmt --check` on the files
  you touched is meaningful (dir-wide lists 57 pre-existing).
- Next: remaining `while (true)`: template.zig (245, 299), task_picker.zig, tui.zig,
  run.zig:1427, registry/server.zig:43 (likely event loops — check); ~220 missing `//!` headers.
  Watch zuda v3.0.0 tag. Cycle 18 FEATURE, cycle 20 STABILIZATION.
- Open questions: none.

## Cycle 16 — 2026-10-06 — FEATURE
- Preflight: tree clean on PR #177's branch → `main`; CI green; inbox: only new issue #178
  (`migration: sailor v3.0.0`, origin: ai). sailor v3.0.0 is tagged; zuda still v2.3.0, so
  plan items 5-11 stay blocked (need BOTH tags).
- Merged #177 (stream reader line cap, 8/8 green). Plan 001 items 3 and 4 were done but the
  plan file still showed them unchecked (issue #155 had them ticked): docs PRs #179, #180
  merged (docs-only PRs get no CI checks; mergeState CLEAN is enough). Item 4's `wip/*`
  "no remote branch" verify can't be met (never delete wip/*); noted inline in the plan.
- Stabilize --one: `cli/show.zig` `StreamingLineReader.next` had an unbounded per-line buffer →
  1 MiB `line_bytes_max`, pieces for longer lines, bounded `for`. `followOutput` `while (true)`
  is a tail -f event loop, left. PR #181 OPEN: Build & Unit green, Integration + cross-compile
  pending at deadline. NEXT CYCLE: `gh pr checks 181 -R yusa-imit/zr`; green and no `hold` →
  squash-merge, label `auto-merged`; red → fix. Tests 1914/0, tidy 0 failing; baseline
  `cmdShow` 299→309 (zig fmt reflow of untouched printError calls).
- Gotchas: guard hook blocks compound commands starting with variable assignments / `cd`
  chains — use plain commands; `zig build test` has no `--test-filter` (full suite ~1 min
  locally now, CI ~13 min); `gh pr view --json authorAssociation` is invalid, use
  `gh api repos/.../issues/N --jq .author_association`.
- Next: `while (true)` left in cli/add*.zig, template.zig, config_editor.zig, task_picker.zig,
  tui.zig, run.zig:1427, jsonrpc/transport.zig:67, registry/server.zig:43, process.zig:416
  (check which are event loops); ~220 missing `//!` headers. Watch zuda v3.0.0 tag.
  Cycle 17 FEATURE; cycle 20 STABILIZATION.
- Open questions: none.

## Cycle 15 — 2026-10-05 — STABILIZATION
- Preflight: tree clean, CI green (5/5), inbox clear (only milestone #155); zuda v2.3.0 /
  sailor v2.99.0 still the newest tags, so items 5-11 stay blocked.
- Fixed `exec/process.zig` `streamReader`: per-line buffer was unbounded and `append catch {}`
  dropped bytes silently. Extracted `emitLines` (1 MiB `line_bytes_max`, over-long line
  delivered in pieces; on OOM the pending tail is delivered, pipe keeps draining), 4 tests.
  Local: `zig build test` 1911/0, tidy 0 failing, fmt clean.
- PR #177 OPEN, not merged: Build & Unit + Integration green, 6 cross-compile jobs pending at
  the 22 min deadline (suite took ~6 min locally + ~8 min CI). NEXT CYCLE: first
  `gh pr checks 177 -R yusa-imit/zr`; if green and no `hold`, merge (squash), label
  `auto-merged`; if red, fix it.
- Gotchas: stale `.zig-cache` again ("failed to spawn build runner") → `rm -rf .zig-cache`;
  BSD sed has no `\n` in replacement (use Edit); `zig test src/root.zig` does not include
  `exec/process.zig` tests, only `zig build test` runs them; the 100-col tidy line-length
  baseline counts test names — keep test names short; FixedBufferAllocator makes a robust OOM
  test (FailingAllocator indices were unpredictable with ArrayList growth/remap).
- Next: remaining `while (true)` in cli/show.zig (159 follow loop, 441 tail), add*.zig,
  template.zig, config_editor.zig; ~220 missing `//!` headers; process.zig still has
  doc-header baseline entry. Watch zuda/sailor v3.0.0 tags.
- Open questions: none.

## Cycle 14 — 2026-10-04 — FEATURE
- Preflight: tree clean on `main`; CI green (latest completed run on ea14a07). Disk 66GB free.
  Inbox: no owner comments, no open PRs, only issue is milestone #155; zuda/sailor tags still
  v2.3.0 / v2.99.0, so items 5-11 stay blocked → one `/stabilize --one`.
- Fixed `exec/remote.zig`: `SSHExecutor.execute` and `captureOutput` read ssh stdout/stderr with
  four unbounded `while (true)` loops. Extracted `collectPipes` + `readBounded` (16 MiB per
  stream, bounded `for`, child killed on error, new `RemoteExecutorError.OutputTooLarge`; read
  error now → `NetworkError` instead of propagating the raw error), 7 tests, `//!` header. PR
  #176 merged, 8/8 green (~13 min). `zig build test` 1907/0, tidy 0 failing; baseline: dropped
  remote.zig `doc-header`.
- Gotchas: guard hook blocks `python3 - <<EOF` and compound `echo $(date)...; cd` commands —
  use the Edit tool and plain commands. Foreground polling loops over 600s move to background
  (fine; re-check with `gh pr checks 176 -R yusa-imit/zr`).
- Next: remaining `while (true)`: cli/add*.zig, show.zig, template.zig, process.zig:367,
  config_editor.zig (watch/*, mcp/lsp/jsonrpc/registry servers are likely event loops — check);
  ~220 missing `//!` headers; zero-assert modules. Cycle 15 is STABILIZATION. Watch zuda/sailor
  v3.0.0 tags.
- Open questions: none.

## Cycle 13 — 2026-10-03 — FEATURE
- Tree clean, CI green, inbox clear; items 5-11 blocked → one `/stabilize --one`.
- Fixed `plugin/builtin_git.zig`: four unbounded stdout read loops → `collectStdout` +
  `readBounded` (16 MiB, child killed on overflow, `error.OutputTooLarge`), 8 tests. PR #175
  merged, 8/8 green. Tests 1900/0, tidy 0 failing.
- Gotchas: Bash `grep --include` fails under zsh glob; stopping a pipe read early without
  killing the child deadlocks `wait()`, so kill on overflow.
- Open questions: none.

## Cycle 12 — 2026-10-02 — FEATURE
- Fixed `plugin/install.zig`: unbounded per-file copy → `copyBounded` (64 MiB, new
  `InstallError.FileTooLarge`), 6 tests. PR #174 merged. `cli/plugin.zig` falls into
  `else => return err` for the new variant (no friendly message yet).
- Gotchas: `for` over `bytes_max + 1` works for generic `anytype` source/sink helpers.
- Open questions: none.

## History (cycles 0-11, 2026-09-05 to 2026-10-01)

Realm created by citadel restructure (cycle 0); memory migrated from the repo's former
`.claude/memory/`. Plan `001` (Zig 0.16 migration + Tiger Style baseline) merged as #154,
milestone issue #155. Cycle 1: `tidy` build step (#157) — fixed a use-after-free in vendored
`tools/tidy.zig` `checkFunctionLength` (flagged upstream for `citadel/templates/tidy`, see
`debugging.md`). Cycles 2-4, 6: assertion baseline (plan item 3) via `src/stdx.zig`
`assert`/`maybe` across `graph/dag.zig`, `exec/scheduler.zig` (#158, real bug: false
postcondition for `deps_serial`), `cache/store.zig` (#159), `config/parser.zig` (#160, #164).
Item 3 still unchecked: `flushProfile`, `flushCurrentTemplate`, `flushCurrentHook`, `parseToml`
(~5100 lines) uninstrumented. Cycle 5 (stabilization): all 12 `catch unreachable` proven (#162);
real bug in `plugin/wasm_runtime.zig` LEB128 decoders (shift counter too narrow, panics on valid
max-width values) fixed (#163). Cycles 7-11: unbounded-loop sweep, one PR per class — days→year
loops (#168), `loader.zig` and `cli/common.zig` parent walks (#169, #170), `topo_sort`
`getExecutionLevels` (#171), `upgrade/checker.zig` response read (#172, cycle 10),
`registry_client.zig` (#173, cycle 11). Patterns: extract-a-helper to stay under the 70-line tidy
ratchet; bump `tidy_baseline.txt` only for growth forced by the fmt-on-save hook reformatting
untouched code (cycle 2 scheduler.zig, cycle 8 loadConfig 74→86), never for own additions;
stale baseline entries fail tidy, remove them when a fix clears them. A flaky
`watch.livereload ... respects configured port across restarts` (AddressInUse) failed CI once
(cycle 9); re-run passed. A stale `.zig-cache` ("failed to spawn build runner") is fixed by
`rm -rf .zig-cache`. No `timeout` on macOS; use sleep loops. `graph/dag.zig` `addEdge` keeps
edge endpoints by slice — tests must pass long-lived names. `zig fmt --check src` on global zig
0.15.2 lists 57 files locally though main CI passes — pre-existing. Preserved dirty working trees
to `wip/*` at least 3 times (resolved in `decisions.md`: retry-config landed via #167, PR #30
closed as superseded).

## Standing backlog

- `zuda` pinned by `git+...?ref=main#<hash>` instead of a tag, and at v2.0.4 while `silica`
  pins v2.3.0 — both violate kingdom rules; flagged in `citadel/docs/KINGDOM.md` ROADMAP
  Phase 0. Converges once zr/zoltraak land 0.16.
- Milestone #155 items 5-11 (0.16 migration proper) are entirely blocked on zuda v3.0.0 and
  sailor v3.0.0 tags. Nothing to do there until those land.

## Current priority

Every FEATURE cycle until zuda/sailor tag v3.0.0: inbox triage, then one `/stabilize --one`
Tiger Style fix (smallest-diff-first). Once the tags land: bump `build.zig.zon` (item 5), then
mechanical renames → `ArrayList` sweep → `io: Io` conversion (3 batches) → tests → release
v1.115.0, in that order per the plan.
