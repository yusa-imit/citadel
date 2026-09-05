# zr — Realm

| | |
|---|---|
| Layer | Tooling |
| Path | `/Users/fn/codespace/zr` |
| GitHub | `yusa-imit/zr` |
| Version | 1.114.0 (`build.zig.zon`) · latest tag v1.114.0 |
| Zig | 0.15.2 — migrating to 0.16.0 under plan `001` |
| Depends on | sailor v2.99.0 (tag tarball); zuda v2.0.4 (git ref, not a tag — see Known gaps) |
| Consumers | none — no kingdom repo depends on zr |
| blocked_by | zuda v3.0.0, sailor v3.0.0 (both need their own `build.zig` migrated to 0.16 |
| | before zr's `zig build` can even start resolving deps on 0.16.0) |
| CI | Linux tests + cross-compile release matrix (`.github/workflows/{ci,release}.yml`) |

## What it is

zr (zig-runner) is a Zig-based all-in-one developer platform: a task runner (make/just/task
replacement), toolchain manager (nvm/pyenv/asdf-style, ~8 languages), monorepo orchestrator
(Nx/Turborepo-style affected-detection), plus MCP and LSP server integration, shipped as a single
~1.2MB binary. It is a real, working, actively-tested codebase (112.5K LOC across ~30 `src/`
modules — config/TOML+expression engine, graph/DAG scheduling, exec/scheduler+worker
pool+remote SSH+retry/circuit-breaker, cache with S3/GCS/Azure/HTTP backends, plugin system
with native+WASM runtimes, file watcher, MCP/LSP/JSON-RPC servers) — not vaporware, but with the
usual drift of a fast-iterating solo project: stale version numbers in docs, an uncommitted
finished feature sitting in the working tree, and zero use of `std.debug.assert` anywhere.

## Build and test

```bash
zig build                    # library + CLI, succeeds cleanly (no warnings)
zig build test               # unit tests: 1799 passed, 8 skipped, 0 failed (~1-2 min)
zig build integration-test   # integration tests: 2087 passed, 44 skipped (~4-5 min)
zig fmt --check src build.zig
```

Local-only: `zig build`, `zig build test`, `zig build integration-test`. CI-only: 6-target
cross-compile, benchmarks, fuzz.

Run notes:
- No fixed ports to reserve; `watch/livereload.zig` tests bind ephemeral localhost sockets only.
- `deps_test.test.800` fails **locally only** on this dev machine (has `python3`, not a bare
  `python` on `PATH`, and `zr deps check` looks for the literal `python` binary) — passes in CI;
  environment quirk, not a bug, ignore it here.
- An untracked `zig-pkg/` directory appears at repo root from build/dependency-resolution runs;
  it is not gitignored — do not `git add` it.
- GPA leak detection can make `zig build test` exit non-zero even when every log line says
  "0 failed" — always grep the log for `leaked` separately from `FAIL` (see STATE.md history).

## Realm-specific rules

(Kingdom-wide zuda-first policy, no-local-workaround-for-upstream-bugs, and the opus/sonnet/haiku
subagent model split are already covered by `citadel/core/rules/00-kingdom.md` and
`citadel/core/KINGDOM.md` — not repeated here. Only what is unique to zr follows.)

- **Module dependency order**: `CLI → Config → Graph → Exec → Plugin`, with `Output` shared
  across all layers for terminal rendering. Config is independent (no dependency on execution);
  Graph takes parsed config and produces an execution plan; Exec takes the plan and manages
  processes.
- **zuda migration status**: DAG, Levenshtein edit-distance, and Glob matching are migrated to
  zuda. Topological sort, cycle detection, and the work-stealing deque are **intentionally kept
  as local, hand-rolled code** for performance (wrapped for API compatibility via
  `zuda.compat.zr_dag`) — this is a deliberate exception, not unmigrated debt.
- **zuda API shape**: zuda's `root.zig` exports plain functions, not nested structs/methods.
  `zuda.algorithms.string.globMatch(pattern, str)` is correct; `globMatch.match(...)` is not —
  `globMatch` already *is* the callable.
- **String ownership**: `allocator.dupe()` at parse time; each type's own `deinit()` frees every
  owned slice; no partial frees inline. `Task.deinit()` is the canonical example — when adding a
  new heap-allocated field to `Task`, it must be freed there or it leaks (see debugging.md
  history of exactly this class of bug in `copyTask()`/workspace inheritance).
- **No `@panic` in library code**: explicit error sets; the CLI layer is the only place allowed
  to fail loudly. Condition evaluator (`config/expr.zig`) is a deliberate fail-open exception —
  a parse error evaluates to `true` rather than breaking a pipeline.

## Layout

| Path | What |
|---|---|
| `src/main.zig` | CLI entry + dispatcher (3299 lines — grew far past CLAUDE.md's stale "~550") |
| `src/cli/` | ~30+ subcommands: run, list, show, graph, validate, workspace, repo, tui, plugin |
| `src/config/` | TOML parser (8299 lines), schema types (3565 lines), loader, expr engine |
| `src/exec/` | scheduler (3755 lines), worker pool, remote SSH exec, retry/circuit breaker |
| `src/graph/` | DAG, Kahn's-algorithm topo sort, cycle detection, ASCII graph renderer |
| `src/cache/` | local + remote cache: S3/GCS/Azure/HTTP backends (`remote.zig`, 1862 lines) |
| `src/toolchain/` | toolchain manager, ~8 languages (node/python/go/rust/etc.) |
| `src/multirepo/` | monorepo orchestration, affected-package detection |
| `src/plugin/` | native + WASM plugin runtime; built-in Docker/Git/Env/Notify/Cache plugins |
| `src/watch/` | polling file watcher (500ms) + live-reload server |
| `src/output/`, `src/history/` | terminal rendering/colors/progress; execution history |
| `src/mcp/`, `src/lsp/`, `src/jsonrpc/` | MCP server, LSP server, shared JSON-RPC transport |
| `src/util/` | glob, duration, semver, hash, platform, numa, string_pool, object_pool |
| others | `lang/`, `analytics/`, `ci/`, `codeowners/`, `conformance/`, `context/`, `migrate/`, |
| | `registry/`, `template/`, `upgrade/`, `versioning/`, `bench/`, `root.zig` |

## Known gaps (from STATE.md)

- **Zero `std.debug.assert`** in 112.5K LOC of `src/` — no runtime invariant-checking discipline
  anywhere; the standout Tiger Style gap for this realm going into 0.16 migration work.
- 24 files over 800 lines; `config/parser.zig`'s `parseToml` alone is ~5112 lines in one function.
- 12 `catch unreachable` sites — each a latent panic if the "impossible" error occurs.
- `zuda` is pinned by a git ref (`main#4ff2325`), not a tag, and at v2.0.4 while `silica` pins
  v2.3.0 — both violate kingdom rules (tag-only pins, one version kingdom-wide); flagged in
  `citadel/docs/KINGDOM.md` ROADMAP Phase 0 already.
- Zig 0.16 migration is blocked cold: both `sailor` and `zuda` `build.zig` call the now-removed
  `Step.Compile.linkLibC()`, so `zig build` on 0.16 fails before reaching any zr source. See
  STATE.md for the full probe (79/200 files independently fail, large ArrayList/fs-Io/std.time
  rewrite once unblocked). Effort estimate: large (5-15 sessions), most of it after the deps
  unblock.
- A finished-but-uncommitted feature (advanced retry config: backoff multiplier, jitter,
  max backoff, retry-on codes/patterns) sits in the working tree on `wip/advanced-retry-config`,
  preserved this session rather than lost — see memory/context.md.
