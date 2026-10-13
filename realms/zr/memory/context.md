# zr — context

last_seen_at: 2026-10-12T21:19:00Z
rejected_plans: []

## Cycle 23 — 2026-10-12 — FEATURE
- Preflight: tree clean on `main`; CI green; inbox clear (#155 milestone, #178 informational; only
  comment since watermark was my own report). zuda still v2.3.0 → items 5-11 blocked → one
  `/stabilize --one`.
- Added `//!` headers to `template/engine.zig`, `builtin/build.zig`, `builtin/test.zig`; deleted
  dead `template/loader.zig` (no importers, 0.14 `ArrayList.init`, never compiled) and 5 tidy
  baseline entries. PR #188 merged, 8/8 green (~14 min). Tests 1944/0, tidy 0 failing.
- Gotchas: stale `.zig-cache` ("failed to spawn build runner") hit again → `rm -rf .zig-cache`;
  `git rm` stages the delete, so do not list the removed path in a later `git add`.
- Next: ~207 `//!` headers left (small files by size: multirepo.zig, upgrade/types.zig,
  codeowners/types.zig, util/platform.zig). Watch zuda v3.0.0. Cycle 24 FEATURE; cycle 25
  STABILIZATION.
- Open questions: none.

## Cycle 22 — 2026-10-11 — FEATURE
- Preflight: tree clean on `main`; CI green; inbox clear (#155 milestone, #178 informational; only
  comments were my own reports). zuda still v2.3.0 → items 5-11 blocked → one `/stabilize --one`.
- Remaining `while (true)` re-checked: `registry/server.zig:43` is the top-level accept loop; the
  rest (task_picker, tui, run.zig:1427, watch/*, show.zig:458) are event/tail loops. Unbounded-IO
  class is done except add.zig/add_interactive prompt loops (need a source seam).
- Switched to missing `//!` headers (217 before): 6 `src/template` files (types, registry,
  builtin ci/release/deploy/lint) + 6 `doc-header` baseline entries removed. PR #187 merged, 8/8
  green after rerunning a flaky `cache_test.test.690` (concurrent writes, expected 0 found 1;
  docs-only diff, passed on rerun). Tests 1944/0, tidy 0 failing.
- Gotchas: guard blocks `cd X; ...` chains (use plain commands); adding a header makes the file's
  `doc-header` tidy baseline entry stale → delete it from `tidy_baseline.txt` in the same PR
  (`sed -i '' 'Nd'` works).
- Next: ~211 headers left (`template/builtin/{build,test}.zig`, `engine.zig`, `loader.zig`, then
  small files by size: multirepo.zig, upgrade/types.zig, codeowners/types.zig, util/platform.zig).
  Watch zuda v3.0.0. Cycle 23 FEATURE; cycle 25 STABILIZATION.
- Open questions: none.

## Cycle 21 — 2026-10-11 — FEATURE
- Preflight: tree clean on `main`; CI green; inbox clear (#155 milestone, #178 informational; only
  new comment was my own report). zuda still v2.3.0 (sailor v3.0.0) → items 5-11 blocked → one
  `/stabilize --one`.
- `mcp/server.zig` `serve` read stdin byte by byte into an unbounded `ArrayList`. Now uses shared
  `cli/line_input.readLine` with one 1 MiB buffer allocated at start (new
  `line_input.buffer_bytes_max`; `readLine` assert relaxed to it). New `next_request_line` helper
  (`RequestLine` text/end/too_long), 5 tests. Over-long request is skipped and logged; an
  unterminated final line at EOF is no longer processed (behavior note). PR #186 merged, 8/8
  green (~13 min). Tests 1944/0, tidy 0 failing.
- Gotchas: guard blocks `cd X; ...` chains and heredoc appends (use Edit, plain commands);
  `gh pr create` has no `--json`; test sources passed to `readLine` need `pub fn read`; a hand-
  rolled `until gh pr checks | grep -qv pending` loop exits early (any passed line matches) — use
  `until ! ... | grep -q pending`. tidy line-length baseline counts debug-print lines > 100 cols.
- Next: task_picker, tui.zig:379, run.zig:1427, registry/server.zig:43 (check each is an event
  loop or EOF-bounded); `mcp/server.zig serve` baseline (90) can shrink. ~220 missing `//!`
  headers. Watch zuda v3.0.0. Cycle 22 FEATURE; cycle 25 STABILIZATION.
- Open questions: none.

## Cycle 20 — 2026-10-09 — STABILIZATION
- Preflight: tree clean on `main`; CI green; inbox clear (#155 milestone, #178 informational; only
  new comment was my own report). zuda still v2.3.0 (sailor v3.0.0 tagged) → items 5-11 blocked.
- `lsp/server.zig` `run` had an unbounded header `ArrayList` and allocated an attacker-chosen
  `Content-Length`. New `lsp/message_reader.zig` `MessageReader.next(gpa, source)`: 8 KiB header
  array, 64 MiB body cap before alloc, `HeaderTooLarge`/`MessageTooLarge`/`MissingContentLength`
  (missing length skipped as before), 11 tests via a chunked `anytype` source. Registered in the
  `main.zig` test block. PR #185 merged, 8/8 green (~11 min). Tests 1939/0, tidy 0 failing,
  baseline `lsp/server.zig:run:89` removed.
- Gotchas: `gh pr create --label fix` fails (no such label; only `auto-merged` etc. exist) — omit
  it; tidy `stale-baseline` fails when a fix shrinks a function under 70 lines; remove the entry.
- Next: `mcp/server.zig:39,42` reads stdin byte-by-byte into an unbounded ArrayList — reuse
  `cli/line_input.zig` pattern with a larger cap (requests are small, 1 MiB). Then task_picker,
  tui.zig:379, run.zig:1427, registry/server.zig:43 (check). Watch zuda v3.0.0.
  Cycle 21 FEATURE.
- Open questions: none.

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

## History (cycles 16-18, folded 2026-10-13)

Cycles 16-18 (2026-10-06 to 10-07, FEATURE; sailor v3.0.0 tagged, zuda still v2.3.0 so plan items
5-11 stayed blocked, one `/stabilize --one` each): #177 stream reader line cap merged; docs PRs #179,
#180 ticked plan items 3 and 4 (docs-only PRs get no CI checks, mergeState CLEAN is enough; item 4's
`wip/*` "no remote branch" verify can't be met, never delete `wip/*`). Cycle 16 `cli/show.zig`
`StreamingLineReader.next` capped at 1 MiB `line_bytes_max` (#181). Cycle 17 three unbounded stdin
loops (`add`, `add_interactive`, `config_editor` x2) -> shared `cli/line_input.zig` `readLine` (4096-byte
buffer, `error.LineTooLong`, tail discard <= 1 MiB; #182). Cycle 18 `cli/template.zig` `applyTemplate`
-> `readReply` over `readLine` (over-long param -> error, over-long confirm -> cancelled; #183).
Found: `src/jsonrpc/transport.zig` is dead code (imported by `mcp/server.zig`, unused, 0.14
`ArrayList(u8).init` API, never compiled): decide delete vs fix. EOF at the editor confirm prompt
still defaults to yes. `while (true)` left to check (event loops?): cli/add.zig 275/379,
task_picker.zig, tui.zig, run.zig:1427 (watch), process.zig:416 (EOF-bounded), server/watch loops,
registry/server.zig:43; ~220 missing `//!` headers. Gotchas: the guard blocks heredoc appends and
compound `cd`/assignment lines (use Edit); the fmt-on-save hook can reformat a whole file on Edit
(undo with `git checkout`, insert via `perl -0pi`); only `zig fmt --check` on touched files is
meaningful (57 pre-existing dir-wide); `zig build test` has no `--test-filter`, ~1 min locally, CI
~13 min; `gh pr view --json authorAssociation` is invalid, use `gh api repos/.../issues/N --jq
.author_association`; `zig test` on one `src/cli/*.zig` fails (outside module path).

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

Cycles 12-15 (2026-10-02 to 2026-10-05): unbounded-IO sweep continued, one PR per file.
`plugin/install.zig` `copyBounded` 64 MiB, `InstallError.FileTooLarge` (#174; `cli/plugin.zig`
has no friendly message for it yet); `plugin/builtin_git.zig` `collectStdout` + `readBounded`
16 MiB (#175); `exec/remote.zig` `collectPipes` + `readBounded`, `OutputTooLarge` (#176);
`exec/process.zig` `emitLines` 1 MiB `line_bytes_max` (#177, left open at the deadline, merged
next cycle). Lessons: stopping a pipe read early without killing the child deadlocks `wait()`,
so kill on overflow; a `for` over `bytes_max + 1` works for generic `anytype` helpers;
`FixedBufferAllocator` is a robust OOM test (FailingAllocator indices drift with ArrayList
remap); `zig test src/root.zig` skips `exec/process.zig` tests, only `zig build test` runs
them; tidy's 100-col baseline counts test names, keep them short; the guard hook blocks
`python3 - <<EOF` and compound `cd` chains, use Edit and plain commands.

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
