# zr — context

last_seen_at: 2026-11-11T00:00:00Z
rejected_plans: []

## Cycle 49 — 2026-11-11 — FEATURE
- Preflight: disk 21 GB ok; tree clean on main; CI green; no bugs; inbox clear (no new comments).
  zuda latest tag still v2.3.0 -> plan items 5-11 blocked -> one stabilize.
- Done (#209, 8/8 green ~15 min, merged): `//!` headers for `jsonrpc/types.zig`, `jsonrpc/parser.zig`,
  `graph/cycle_detect.zig`; 3 `doc-header` baseline entries removed (174 -> 171). Tests 1968/0, tidy 0
  failing. STATE.md header count updated (171).
- Gotchas: a one-shot `until` loop over `gh pr checks` hits the 600 s tool timeout (cross-compile ~15
  min): poll in a `for` loop of ≤ 28 x 20 s, then re-run. Disk is borderline (21 GB).
- Next: cycle 50 is STABILIZATION (n % 5 == 0); check zuda tags first. Candidates: `parseToml` OOM leak
  (`addWorkspaceSharedTask`), `Cache plugin clearAll catch {}`, more `//!` headers (ci/templates/
  github_actions, cli/codeowners, codeowners/generator), conformance parser.
- Blockers: zuda v3.0.0. Open questions: none.

## Cycle 48 — 2026-11-10 — FEATURE (no-op)
- Disk gate: 15 GB free (df -h shows 16Gi) < 20 GB, stopped at preflight. Tree clean on main; no
  GitHub checks run. Third disk no-op in four cycles (45, 46, 48); 47 ran at 23 GB.
- Done: nothing. PRs: none. Blockers: disk (needs >= 20 GB free).
- Next: cycle 49 FEATURE (check zuda tags first); 50 is STABILIZATION. Candidates unchanged
  (`jsonrpc/types.zig`, `jsonrpc/parser.zig`, `graph/cycle_detect.zig` headers, `parseToml` OOM leak
  via `addWorkspaceSharedTask`, `Cache plugin clearAll catch {}`, conformance parser).
- Open questions: none.

## Cycle 47 — 2026-11-09 — FEATURE
- Preflight: disk 23 GB ok; tree clean on main; CI green on main; no bugs; inbox clear (no new
  comments). zuda latest tag still v2.3.0 (sailor v3.1.0 exists) -> plan items 5-11 blocked -> one stabilize.
- Done (#208, 8/8 green ~15 min, merged): `jsonrpc/writer.zig` wrote string ids, methods and error
  messages with `{s}`, so quotes/backslashes/newlines gave malformed JSON on MCP and LSP output. Now
  `std.json.fmt` (`{f}`) plus one shared `formatId`; 3 round-trip tests (serialize -> parse) failed with
  `SyntaxError` first. Added `//!` header, removed its `doc-header` baseline entry (175 -> 174 files).
- Next: cycle 48 FEATURE (check zuda tags first); 50 is STABILIZATION. Candidates: `//!` headers for
  `jsonrpc/types.zig`, `jsonrpc/parser.zig`, `graph/cycle_detect.zig` (all have comment headers to convert),
  `parseToml` OOM leak via `addWorkspaceSharedTask`, `Cache plugin clearAll catch {}`, conformance parser.
- Blockers: zuda v3.0.0. Open questions: none.

## Cycle 46 — 2026-11-08 — FEATURE (no-op)
- Disk gate: 18 GB free < 20 GB, stopped at preflight. Tree clean on main; no GitHub checks run.
- Done: nothing. PRs: none. Blockers: disk (needs >= 20 GB free; second consecutive disk no-op).
- Next: cycle 47 FEATURE (check zuda tags first); 50 is STABILIZATION. Candidates unchanged
  (`parseToml` OOM leak via `addWorkspaceSharedTask`, `Cache plugin clearAll catch {}`, headers,
  conformance parser).
- Open questions: none.

## Cycle 45 — 2026-11-07 — STABILIZATION (no-op)
- Disk gate: 17 GB free < 20 GB, stopped at preflight. Tree clean on main; no GitHub checks run.
- Done: nothing. PRs: none. Blockers: disk (needs >= 20 GB free).
- Next: cycle 46 FEATURE unless stabilize_streak forces otherwise; the cycle-45 stabilization
  candidates are unchanged (`parseToml` OOM leak via `addWorkspaceSharedTask`, `Cache plugin
  clearAll catch {}`, headers, conformance parser). Check zuda tags first.
- Open questions: none.

## Cycle 44 — 2026-11-05 — FEATURE
- Preflight: disk ok; started on merged branch `fix/copy-task-retry-strategy` (clean) -> main; CI green;
  no bugs; inbox clear (only our own #155 comment). zuda still v2.3.0 -> items 5-11 blocked -> one stabilize.
- Done (#207, 8/8 green ~18 min, merged): `config/loader.zig` `copyTask` is now OOM-leak-free. Copy starts
  detached (`detachOwnedFields` resets every `Task.deinit`-freed field), one `errdefer result.deinit`, each
  field via leak-safe `dupeOptionalString`/`dupePairs`/`dupeStringMap`/`copyElements` + per-type copiers.
  `copyTaskHookImpl` leaked a hook env key on mid-pair OOM (sweep test found it); now uses `dupePairs`.
  Sweep test: `fullyPopulatedTask` (arena, every owned field) + FailingAllocator over all alloc indices.
  `copyTask` baseline 388 -> 80. Tests 1965/0, tidy 0 failing. Aliasing audit of Task.deinit vs copyTask: clean.
- Gotchas: `gh pr create --label chore` fails AND aborts the PR (labels: only `auto-merged` etc.; create
  first, label after); CI cross-compile checks take ~15+ min, cycle deadline (22 min) is tight.
- A new owned field on `Task` must be added to `detachOwnedFields` and `copyTask` (and the fixture), else
  the copy aliases the original (double free).
- Next: cycle 45 is STABILIZATION (n % 5 == 0); check zuda tags first. Candidates: `parseToml` OOM leak
  (`addWorkspaceSharedTask`), `Cache plugin clearAll catch {}`, headers, conformance parser.
- Open questions: none.

## Cycle 43 — 2026-11-04 — FEATURE
- Preflight: disk 24 GB; tree clean on main; CI green; no bugs; inbox clear. zuda still v2.3.0 ->
  items 5-11 blocked -> one stabilize.
- Done (#206, 8/8 green ~14 min, merged): `config/loader.zig` `copyTask` never duplicated
  `retry_on_codes`/`retry_on_patterns`, so a member inheriting a shared task with a retry strategy
  double-freed the workspace's memory (`Task.deinit` frees both). Now duped via new leak-safe
  `dupeStrings`/`freeStrings`. The `copied_count` errdefer guards were dead (counter bumped before
  any later failure); removed, replaced by unconditional errdefers for name/cmd/cwd/retry strategy.
  `copyTask` baseline 430 -> 388. Tests 1964/0, tidy 0 failing.
- Found, NOT fixed: `copyTask` still leaks fields after the retry strategy on mid-copy OOM (every
  block needs `dupeStrings`-style partial cleanup; documented on the function); `parseToml` OOM leak.
  Other `Task.deinit`-owned fields should be audited against `copyTask` the same way (aliasing bug class).
- Gotchas: guard blocks `A; B` chains with `git fetch` in the same line as other-repo reads (split
  into separate calls); a heredoc `cat >>` into a repo file was allowed; tidy `stale-baseline` also
  fires when a function is larger than the baseline by even 1 line, so recount after editing.
- Next: cycle 44 FEATURE (check zuda tags first); 45 is STABILIZATION (n % 5 == 0).
- Open questions: none.

## Cycle 42 — 2026-11-04 — FEATURE
- Preflight: disk 22 GB; tree clean on main; CI green; no bugs; inbox clear (only our own cycle-41
  comment on #155). zuda still v2.3.0 (sailor v3.1.0) -> items 5-11 blocked -> one stabilize.
- Done (#205, 8/8 green ~12 min, merged): `config/loader.zig` `findAndApplyParentWorkspace` used
  `catch {}`/`catch return`/`catch break` on its allocations and on both inherit calls, so OOM left a
  member without workspace shared tasks/mixins/templates. Now `error{OutOfMemory}!void`, propagated
  by `loadFromFileInternal`; missing/unreadable parent stays a non-error. Test: FailingAllocator at
  indices 0..2 (the walk's own dupe/dupe/join) -> OutOfMemory. Tests 1962/0, tidy 0 failing.
- Found, NOT fixed (next candidates): `copyTask` (loader.zig ~1051) `errdefer if (copied_count < N)`
  guards are no-ops (counter is bumped before any later failure), so a failed copy leaks the earlier
  fields; `parseToml` also leaks on OOM mid-parse (`addWorkspaceSharedTask`). A full FailingAllocator
  sweep over loadFromFile therefore reports `[gpa] leaked`; keep sweeps to the leak-free prefix.
- Gotcha: `zig build test` first try hit "failed to spawn build runner" -> `rm -rf .zig-cache`.
- Next: cycle 43 FEATURE (check zuda tags first); 45 is STABILIZATION (n % 5 == 0). Other candidates:
  `Cache plugin clearAll catch {}` (builtin.zig:234, no failure seam), headers, conformance parser,
  `upgrade/installer`.
- Open questions: none.

## Cycles 39-41 (2026-10-31..11-03), folded 2026-11-04
- zuda still v2.3.0 (sailor v3.1.0), so items 5-11 stayed blocked; one `stabilize --one` each.
- 39 (#203, 8/8 green ~13 min): `plugin/builtin_env.zig` `readDotEnv`/`loadDotEnv` ignored a full read of
  a 64 KiB buffer and silently dropped later variables; now `file_bytes_max + 1` buffer and
  `readBounded`, over the cap -> `error.FileTooLarge`. 40: no-op at the disk gate (18 GB < 20 GB).
  41 (#204): `plugin/builtin.zig` `onInit` did `loadDotEnv(...) catch {}`; new
  `loadEnvFileOrWarn(gpa, path, overwrite, *std.Io.Writer) bool` writes one stderr warning
  (FileTooLarge gets specific text), missing file stays silent. Tests 1961/0.
- Gotchas: the fmt-on-Edit hook reformatted untouched `NotifyPlugin` code in builtin.zig (HEAD already
  fails `zig fmt --check` there); revert unwanted hunks via `git diff -U0` + `git apply -R
  --unidiff-zero`, else the tidy line-length baseline (17) breaks. Guard blocks `gh pr merge ...; ...`
  chains: run `gh pr merge N --squash --delete-branch --repo yusa-imit/zr` alone.
- Candidates still open: headers (ci/templates/github_actions, cli/codeowners, codeowners/generator),
  conformance parser mistyped fields, `upgrade/installer`, `Cache plugin clearAll catch {}`.

## History (cycles 0-38, folded 2026-11-05)

- 0-15 (09-05..10-05): realm created; plan `001` (Zig 0.16 migration + Tiger Style baseline) merged as
  #154, milestone #155. Cycle 1 `tidy` build step (#157; fixed a use-after-free in vendored
  `tools/tidy.zig` `checkFunctionLength`, flagged upstream, see `debugging.md`). Cycles 2-6 assertion
  baseline via `src/stdx.zig` `assert`/`maybe` (`graph/dag.zig` #158 real bug: false postcondition for
  `deps_serial`; `cache/store.zig` #159; `config/parser.zig` #160, #164); item 3 still unchecked:
  `flushProfile`, `flushCurrentTemplate`, `flushCurrentHook`, `parseToml` uninstrumented. Cycle 5: all 12
  `catch unreachable` proven (#162); `plugin/wasm_runtime.zig` LEB128 decoder shift too narrow (#163).
  7-15 unbounded-loop / unbounded-IO sweep, one PR per class or file: days->year loops (#168), parent walks
  (#169, #170), `topo_sort` (#171), `upgrade/checker.zig` (#172), `registry_client.zig` (#173),
  `plugin/install.zig` `copyBounded` 64 MiB (#174; `cli/plugin.zig` has no friendly `FileTooLarge`
  message), `builtin_git.zig` 16 MiB (#175), `exec/remote.zig` `OutputTooLarge` (#176), `exec/process.zig`
  `emitLines` 1 MiB (#177). Lessons: stopping a pipe read early without killing the child deadlocks
  `wait()` (kill on overflow); `FixedBufferAllocator` is a robust OOM test; `zig test src/root.zig` skips
  `exec/process.zig` tests (only `zig build test` runs them); tidy's 100-col baseline counts test names;
  bump `tidy_baseline.txt` only for growth forced by the fmt-on-save hook, never for own additions; stale
  baseline entries fail tidy (remove them when a fix shrinks a function under 70 lines).
- 16-20 (10-06..09): `cli/show.zig` `StreamingLineReader` 1 MiB cap (#181); shared `cli/line_input.zig`
  `readLine` for `add`, `add_interactive`, `config_editor` (#182), `applyTemplate` `readReply` (#183);
  removed dead `src/jsonrpc/transport.zig` (#184; PRD still lists it); `lsp/message_reader.zig`
  `MessageReader.next` (8 KiB header, 64 MiB body cap, 11 tests; #185); docs-only PRs #179-#180 get no CI
  checks (mergeState CLEAN is enough; never delete `wip/*`). sailor v3.0.0 tagged, zuda stayed v2.3.0 so
  plan items 5-11 stayed blocked: one `/stabilize --one` per cycle through cycle 41. Open: EOF at the
  editor confirm prompt defaults to yes; add.zig/add_interactive prompt loops need a source seam.
- 21-32 (10-11..22): `mcp/server.zig` `serve` reads via `line_input.readLine`, 1 MiB buffer (#186);
  `//!` headers (217 -> ~176 left) with matching `doc-header` baseline entries removed (#187-#197);
  deleted dead `template/loader.zig` and `util/object_pool.zig`; `lsp/document.zig` `DocumentStore.open`
  reopen leak (#195; leak shows as `[gpa] leaked` while the test says OK, grep `leaked`); diagnostics
  `toJson` escapes via `std.json.fmt` (`{f}`, #197); OWNER on #178: target sailor v3.1.0 (only break:
  `Editor.init`, `MultiCursorEditor.init`, `LocalSource.init` return `error{OutOfMemory}!T`).
- 33-38 (10-23..31): `analytics/json.zig` escaping (#198), `//!` headers (#199), `output/monitor.zig`
  flush fix (#200; dirty tree kept as `wip/fix-monitor-flush-stderr-20261029`), `context/json.zig`
  `escapeJson` was a no-op (#201), `zr upgrade --version <ver>` was ignored, now pure
  `checker.selectRelease(releases, Selection{include_prerelease, version})` (#202). Disk gate no-ops at
  15 GB (33), 18 GB (40). Audit (35): 12 proven `catch unreachable`, 16 `while (true)` event loops, 93
  `std.debug.print` (needs a writer seam), 180 files without `//!`.
- Known, documented, not fixed: conformance parser skips mistyped fields silently; `lsp/position.zig` uses
  UTF-8 byte columns, not UTF-16; `registry/server.zig:43` is an accept loop, task_picker/tui/run.zig:1427/
  watch/show.zig:458 are event/tail loops.
- Gotchas: a test `std.Io.Writer` drain must write `buffer[0..end]` and set `end = 0`, else `flush` spins
  and `zig build test` hangs; stale `.zig-cache` ("failed to spawn build runner"/`FileNotFound`) ->
  `rm -rf .zig-cache` as its own command; guard blocks compound `A=..; cmd`, `cd X; ...`, `sleep N; cmd`,
  heredoc appends, `python3 - <<EOF`, `gh pr merge ...; ...` chains (run the merge alone; use `cd X && cmd`,
  Edit/Write, `until` loops); `gh pr merge` does not add `auto-merged` (`gh pr edit N --add-label`);
  `gh pr create --label fix` fails (label absent); `gh pr view --json authorAssociation` is invalid (use
  `gh api repos/.../issues/N --jq .author_association`); `gh pr checks | awk` ternary breaks on macOS awk;
  `until gh pr checks | grep -qv pending` exits early (use `until ! ... | grep -q pending`); the fmt-on-
  Edit hook can reformat untouched code (revert via `git diff -U0` + `git apply -R --unidiff-zero`, else
  the tidy line-length baseline of 17 breaks); `sed -i '' -e 'Nd'` highest line first; `zig fmt --check`
  on global 0.15.2 lists 57 pre-existing files, only touched files matter; `zig build test` has no
  `--test-filter` (~1 min local, CI ~13-16 min); `zig test` on one `src/cli/*.zig` fails (outside module
  path); no `timeout` on macOS; a flaky `watch.livereload ... respects configured port` and `cache_test.
  test.690` passed on rerun; zsh expands `echo "====="`.

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
