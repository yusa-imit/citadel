# zr — context

last_seen_at: 2026-10-19T00:00:00Z
rejected_plans: []

## Cycle 29 — 2026-10-19 — FEATURE
- Preflight: tree clean on `main`; CI green; no bugs. Inbox: OWNER comment on #178 (2026-10-18)
  says sailor v3.1.0 is released, target the newest tag (not v3.0.0) when migrating; only break:
  `Editor.init`, `MultiCursorEditor.init`, `LocalSource.init` now return `error{OutOfMemory}!T`.
  zuda still v2.3.0 (no v3.0.0) → items 5-11 blocked → one `/stabilize --one`.
- Added `//!` headers to `exec/notification.zig` (`send` only delivers on Linux), `lsp/document.zig`,
  `ci/templates/types.zig`; deleted dead `util/object_pool.zig` (no importers, 0.14 API); removed 5
  baseline entries. PR #194 merged, 8/8 green (~13 min). Tests 1944/0, tidy 0 failing.
- Found: `lsp/document.zig` `DocumentStore.open` on an already-open URI overwrites the entry and
  leaks the earlier copy (documented in the header); candidate fix (close-then-open or error).
- Next: ~183 headers left (next smallest: lsp/position, cli/context, lsp/diagnostics, cli/help).
  Item 5 should bump to sailor v3.1.0 + zuda v3.x. Cycle 30 STABILIZATION.
- Gotchas: stale `.zig-cache` again → `rm -rf .zig-cache`; `git rm`'d files are already staged, do
  not list them in `git add`.
- Open questions: none.

## Cycle 28 — 2026-10-18 — FEATURE
- Preflight: tree clean on `main`; CI green; inbox clear (no new comments; #155 milestone, #178
  informational). zuda still v2.3.0 (no v3.0.0 tag) → items 5-11 blocked → one `/stabilize --one`.
- Added `//!` headers to `bench/formatter.zig`, `migrate/report.zig`, `cli/which.zig`,
  `context/yaml.zig` (yaml header records unescaped values) + removed 4 `doc-header` baseline
  entries. `cli/which.zig` was already failing `zig fmt --check` on main; ran `zig fmt` on it
  (one call reflowed). PR #193 merged, 8/8 green (~13 min). Tests 1944/0, tidy 0 failing.
- Next: ~187 headers left (next smallest: check `wc -l` over the baseline files). Watch zuda
  v3.0.0. Cycle 29 FEATURE; cycle 30 STABILIZATION.
- Gotchas: the guard blocks compound `A=..; cmd` bash lines (use plain commands, one per call);
  insert headers with `perl -0pi -e 's/\A/…/'`.
- Open questions: none.

## Cycle 27 — 2026-10-17 — FEATURE
- Preflight: tree clean on `main`; CI green; inbox clear (#155 milestone, #178 informational; no
  comments since watermark). zuda still v2.3.0 (sailor v3.0.0) → items 5-11 blocked → one
  `/stabilize --one`.
- Added `//!` headers to `analytics/json.zig`, `lang/registry.zig`, `lang/provider.zig`,
  `versioning/types.zig` + removed 4 `doc-header` baseline entries. PR #192 merged, 8/8 green
  (~13 min). Tests 1944/0, tidy 0 failing.
- Gotchas: `gh pr checks | awk` with ternary breaks on macOS awk; use `cut -f1,2`. `analytics/json.zig`
  writes task names unescaped (documented in its header; possible JSON-escape fix later).
- Next: ~191 headers left (next smallest: bench/formatter, migrate/report, cli/which, context/yaml).
  Watch zuda v3.0.0. Cycle 28 FEATURE; cycle 30 STABILIZATION.
- Open questions: none.

## Cycles 21-26 (2026-10-11..16, condensed 2026-10-17)
- All FEATURE with zuda still v2.3.0 (sailor v3.0.0), items 5-11 blocked, so one
  `/stabilize --one` each; each PR merged with 8/8 green (~13 min); tests 1944/0, tidy 0 failing.
- 21 (#186): `mcp/server.zig` `serve` read stdin byte by byte into an unbounded `ArrayList`; now
  `cli/line_input.readLine` with one 1 MiB buffer (`line_input.buffer_bytes_max`), `RequestLine`
  helper, over-long request skipped and logged; an unterminated final line at EOF is no longer
  processed. 22: remaining `while (true)` re-checked (`registry/server.zig:43` is the accept
  loop; task_picker, tui, run.zig:1427, watch/*, show.zig:458 are event/tail loops); only
  add.zig/add_interactive prompt loops need a source seam. 22-26 (#187-#191): `//!` headers
  (217 -> ~191 left) with the matching `doc-header` baseline entries removed; deleted dead
  `template/loader.zig` (0.14 `ArrayList.init`, no importers).
- Open: `analytics/json.zig` writes task names unescaped (documented in its header). Next
  smallest header files: bench/formatter, migrate/report, cli/which, context/yaml.
- Gotchas: `gh pr merge` does not add `auto-merged` (`gh pr edit N --add-label auto-merged`);
  `gh pr checks | awk` ternary breaks on macOS awk (use `cut -f1,2`); `until gh pr checks |
  grep -qv pending` exits early, use `until ! ... | grep -q pending`; a foreground wait over 10
  min is backgrounded (bounded `for` loop with sleep 30); adding a header makes the file's
  `doc-header` baseline entry stale (delete it in the same PR; `sed -i '' -e 'Nd' -e 'Md'`,
  highest line first); `grep -c doc-header tidy_baseline.txt` counts the comment line too;
  stale `.zig-cache` -> `rm -rf .zig-cache`; a flaky `cache_test.test.690` passed on rerun.

## Cycles 19-20 (2026-10-09), folded
- Both: tree clean, CI green, inbox clear; zuda still v2.3.0 (sailor v3.0.0 tagged) so items 5-11
  stayed blocked, one `/stabilize --one` each.
- 19: removed dead `src/jsonrpc/transport.zig` (228 lines, 0.14 `ArrayList(u8).init`, never
  compiled) + import + 2 tidy baseline entries (#184, 8/8 green ~13 min). `docs/PRD.md` still
  lists it in a planned layout (also nonexistent `json.zig`); left as design text.
- 20: `lsp/server.zig` `run` had an unbounded header list and attacker-chosen `Content-Length`;
  new `lsp/message_reader.zig` `MessageReader.next(gpa, source)` (8 KiB header, 64 MiB body cap
  before alloc, `HeaderTooLarge`/`MessageTooLarge`/`MissingContentLength`, 11 tests; #185).
- Remaining `while (true)`: add.zig 275/379 and add_interactive.zig 380 are stdin prompt loops
  (need a `prompt` source injection before a cap is testable); `mcp/server.zig:39,42` reads stdin
  byte-by-byte into an unbounded ArrayList (reuse the `cli/line_input.zig` pattern, 1 MiB cap);
  check task_picker, tui.zig:379, run.zig:1427, registry/server.zig:43. ~220 missing `//!`.
- Gotchas: `gh pr create --label fix` fails (label absent); tidy `stale-baseline` fails when a fix
  shrinks a function under 70 lines, remove the entry; guard blocks `cd X; ...` and `sleep N; cmd`
  chains (use plain commands and `until` loops).

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
