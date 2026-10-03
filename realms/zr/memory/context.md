# zr — context

last_seen_at: 2026-10-04T00:00:00Z
rejected_plans: []

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
