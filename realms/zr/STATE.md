# zr — State survey (2026-09-05)

Full citadel restructure survey, ahead of the repo's `.claude/`/`CLAUDE.md` removal. Sources:
kingdom survey + a Zig 0.16 breakage probe, both read-only, no repo state changed.

## What exists — claimed vs present

README/CHANGELOG claim zr is a mature "universal developer platform" (v1.114.0) unifying task
running, toolchain management, and monorepo tooling in one small binary, with MCP/LSP servers.
This is **substantiated**: 112.5K LOC across ~30 real `src/` modules (config/TOML+expr engine,
graph/DAG scheduling, exec/scheduler+worker pool+remote SSH+retry/circuit-breaker, cache with
S3/GCS/Azure/HTTP backends, native+WASM plugin system, file watcher, MCP/LSP/JSON-RPC servers).
1799 unit tests pass, `zig build`/`zig build test` both clean — not vaporware.

Drift found, not missing functionality:
- README badge shows v1.84.0; actual is v1.114.0 (build.zig.zon / latest tag).
- Old CLAUDE.md's repo-structure diagram is stale (main.zig claimed ~550 lines, actually 3299).
- `.claude/memory/project-context.md`'s "Next Action" section still references v1.89.0 planning
  despite the project being at v1.114.0 — automated sessions were working from stale priorities.
- CHANGELOG records a real prior CI-red incident (~270 integration failures pre-v1.113.1),
  resolved; current tree is green.

## Sizes

- `loc_src`: 112,502 lines. Module count: ~30 top-level `src/` directories + `main.zig`/`root.zig`.
- Tests: 1799 unit tests passed / 8 skipped / 0 failed. Integration: 2087 passed / 44 skipped
  (per last recorded run in `.claude/memory/project-context.md`; not re-run this survey).
- Files over 800 lines: **24**. Largest: `config/parser.zig` 8299 (single `parseToml` fn
  ~5112 lines), `exec/scheduler.zig` 3755, `config/types.zig` 3565, `main.zig` 3299,
  `cli/run.zig` 3098.

## CI / issues / PRs

- CI: green. Last 3 runs on `main`/tags: CI success (12m12s), Release v1.114.0 success (5m28s),
  one earlier CI run cancelled (superseded push).
- Open issues: 0.
- Open PRs: #30 "chore: migrate to zuda for graph algorithms" — needs a decision (merge or
  close as superseded by the "kept custom for perf" decision already recorded in memory).

## Tiger Style gap table

| Gap | Count | Note |
|---|---|---|
| `std.debug.assert` | 0 | Standout gap: zero runtime invariant checking in 112.5K LOC. |
| `catch unreachable` | 12 | Each a latent panic if the "impossible" error occurs. |
| `@panic` | 0 | Consistent with "no @panic in library code" decision. |
| `std.debug.print` | 93 | Plausible intentional CLI/stderr output; not individually audited. |
| `while (true)` | 46 | Not individually audited for bounded exit; some are legit service |
| | | loops (worker threads, 500ms watch poll) per architecture notes. |
| Functions > 70 lines | many | `parseToml` (~5112), `flushCurrentHook` (~1970), `workerFn` |
| | | (~1128) — measured on the 3 largest files only, not exhaustive. |

None of this was audited to "clean" — it is what a grep-level pass found, not a proof of absence
of worse patterns (e.g. allocation-in-hot-loop in `exec/scheduler.zig` or `cache/remote.zig` was
not specifically checked).

## Zig 0.16 probe summary

- `zig build` (0.15.2, global): OK, no errors.
- `zig build` / `zig build test` on 0.16.0: **fail immediately**, before reaching any zr source.
  Both `sailor`'s and `zuda`'s own `build.zig` call `Step.Compile.linkLibC()`, removed in 0.16.
  zr's own `build.zig` already uses the modern `createModule`/`root_module` pattern and is never
  reached. This is a hard, upstream-only block — not fixable inside zr.
- To gauge zr's own breakage past that block, 200/227 `src/*.zig` files (skipping ~28 that
  `@import` sailor/zuda directly) were `zig test`'d standalone against 0.16.0: **79/200 failed**.
  A large share of raw errors is a single-file-testing artifact (imports outside module path,
  not real under the real build graph); genuine std-API breakage hits roughly 30-40 of the 200.
- Error classes found (grep across full 227-file tree, `files_touching_fs_net_thread_time_
  process`: 149/227, 66%): ArrayList unmanaged-only construction (31 hits, e.g.
  `std.ArrayList(u8){}` missing `items`/`capacity`), `std.fs.cwd()`/File Io-redesign (8),
  `std.heap.GeneralPurposeAllocator` removed → `DebugAllocator` (3), `std.posix.getenv`/
  `std.process.getEnvVarOwned` removed (4), `std.time.timestamp`/`milliTimestamp` removed (2),
  `std.io.fixedBufferStream` moved (2), `std.process.Child.init` removed (3), switch-prong
  capture discard tightened — trivial, 5 occurrences (`=> |_| 1,` → `=> 1,`).
- Effort estimate: **large (5-15 sessions)**, comparable to or larger than the already-tracked
  0.14→0.15 migration, once sailor/zuda unblock the build. Blocking dependencies: zuda v3.0.0,
  sailor v3.0.0 (both must migrate their own `build.zig` first).

## Docs / root hygiene (for the hygiene PR)

- Tracked binary artifact: `env_file_test.o` at repo root — `*.o` is gitignored but this file
  was tracked before the rule existed; delete + untrack.
- 4 `RELEASE_NOTES_v*.md` files at repo root → move under `docs/` (or `docs/releases/`).
- `debug_lsp.sh`, `test_lsp_simple.sh` ad hoc scripts at repo root → move to `scripts/`.
- Untracked `zig-pkg/` directory at root, not gitignored — do not commit; add to `.gitignore` or
  remove.
- Per kingdom docs policy, `CLAUDE.md` and `.claude/` (58 tracked files: agents, commands,
  memory, ~20+ ad hoc session-summary/cycle diary files, 3 zr-specific mixin-feature docs) are
  removed from the repo entirely in the next step; durable content is migrated into this realm's
  `REALM.md`/`memory/` (done — see `citadel/realms/zr/memory/`).
- `.claude/logs/agent-activity.jsonl` was a tracked, churny auto-updated log (not gitignored) —
  will no longer exist once `.claude/` is removed.

## Dirty tree preserved

Uncommitted working-tree changes (parser.zig +115/-3, types.zig +46/-5, docs/milestones.md,
plus routine `.claude/` log churn) implement a complete, tested feature — advanced retry config
(`retry_backoff_multiplier`, `retry_jitter`, `max_backoff_ms`, `retry_on_codes`,
`retry_on_patterns`) with a passing test. Full suite still green (1799/1799 non-skipped).
Preserved this session on branch `wip/advanced-retry-config` rather than discarded or committed
directly to `main`.

## Next work candidates

1. Decide open PR #30 (zuda graph-algorithm migration) — merge, or close given the recorded
   "topo sort / cycle detection / work-stealing deque kept custom for perf" decision.
2. Land or formally supersede the `wip/advanced-retry-config` branch via a real PR.
3. Fix `zuda` dependency to a tagged release (currently a `git+...?ref=main` pin — violates the
   kingdom's tag-only rule) and align its version with `silica`'s (2.0.4 vs 2.3.0 mismatch).
4. Root/docs hygiene PR (see above list).
5. Begin Zig 0.16 migration plan `001` — blocked until zuda v3.0.0 / sailor v3.0.0 land; until
   then, no new 0.15-only code per kingdom convention.
