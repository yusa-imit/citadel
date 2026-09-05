# zr — Realm

| | |
|---|---|
| Layer | tooling |
| Path | `/Users/fn/codespace/zr` |
| GitHub | `yusa-imit/zr` |
| Version | 1.114.0 (`build.zig.zon`) · latest tag v1.114.0 (matches; 1 unreleased WIP commit) |
| Zig | 0.15.2 (migrating to 0.16.0 under plan `001`; see `citadel/docs/ROADMAP.md`) |
| Depends on | sailor 2.99.0 (tarball), zuda 2.0.4 (git ref, pinned commit `4ff2325`) |
| Consumers | none (zr is the tooling layer; nothing in the kingdom imports it) |
| blocked_by | zuda v3.0.0, sailor v3.0.0 |
| CI | Linux unit + integration tests + 6 cross-compile targets (`.github/workflows/ci.yml`) |

## What it is

zr is a Zig 0.15.x all-in-one developer platform: a task runner/workflow manager (TOML config
plus a built-in expression engine) with a DAG scheduler, worker pool, retry/circuit-breaker/
checkpoint execution, local + remote (S3/GCS/Azure/HTTP) task-output caching, a toolchain
manager for ~8 languages, monorepo/multi-repo orchestration, a native plugin system (WASM +
built-in Docker/Git/Env/Notify/Cache plugins), a file watcher, and MCP/LSP/JSON-RPC servers —
aiming to replace make/just/task + nvm/pyenv/asdf + Nx/Turborepo with a single ~1.2MB binary.
112.5k LOC, 1798 unit + 2087 integration tests, all passing. All 13 original PRD phases are
complete (v1.0.0, 2026-02-28); current work is post-v1.0 incremental features. Depends on sailor
(CLI/TUI, no direct current usage found beyond the pin) and zuda (DAG/Levenshtein/Glob
algorithms via a compat wrapper).

## Build and test

```bash
zig build                  # library + CLI
zig build test             # unit tests (~49s wall; 1798 passed, 8 skipped, 0 failed)
zig build integration-test # black-box CLI tests (~4-5 min; 2087 passed, 44 skipped)
zig fmt --check src build.zig
```

Local-only: `zig build`, `zig build test`, `zig build integration-test`. CI-only: 6-target
cross-compile, benchmarks, fuzz — except a STABILIZATION cycle, which may run them locally,
sequentially, and only after confirming `pgrep -f "zig build"` shows no other kingdom repo
mid-build: concurrent heavy Zig builds across sibling repos have triggered kernel panics on this
host before.

No ports, no servers to kill between sessions — zr's MCP/LSP servers only run when a task
explicitly starts them, not as session-persistent daemons. A `wip/advanced-retry-config` branch
preserves this session's dirty-tree work (`splitTopLevelFields()` bracket/quote-aware inline-
table comma splitting, wired into retry-config and mixin-env parsing, plus 5 new retry template
fields end-to-end with a passing test; full suite was green on the dirty tree) from before the
restructure — finish or discard it explicitly in the first post-restructure cycle.

## Realm-specific rules

- **Module dependency order**: `config → graph → exec → plugin`, with `output` shared across
  all layers for terminal rendering. `config` has no dependency on execution; `graph` takes
  parsed config and produces an execution plan; `exec` takes the plan and manages processes.
  Never let `config` depend on `exec`/`plugin`.
- **Dependency-pin registry**: zr pins `sailor@2.99.0` (matches sailor's latest tag) and
  `zuda@2.0.4` via a git ref, not a release tag — this is behind silica's `zuda@2.3.0` pin, the
  exact drift `citadel/docs/KINGDOM.md` flags as a kingdom-wide "fix in ROADMAP Phase 0" item;
  don't independently bump zr's zuda pin without checking that ROADMAP item first.
- **Release quirks**: a minor release version must be the current `build.zig.zon` version's
  *next* minor — never a version number pre-assigned in `docs/milestones.md` (e.g. current
  1.114.0 → next is 1.115.0, not whatever a stale milestone entry says). Minor release requires
  a completed milestone checklist item with tests, full suite green, and 0 open `bug`-labeled
  issues. Verify against `git tag -l 'v*' --sort=-v:refname` before tagging.
- **Local test policy**: `zig build`/`zig build test` (~49s) are cheap enough for every cycle;
  `zig build integration-test` (~4-5 min, 2131 tests) should be budgeted deliberately (e.g. once
  per stabilization cycle, not skipped indefinitely) — a past regression (`~270 failures`,
  resolved 2026-08-28) went undetected for weeks because sessions only ran unit tests.
- **zuda-first exceptions**: DAG, Levenshtein, and Glob are migrated to zuda (via
  `zuda.compat.zr_dag` for DAG/topo-sort/cycle-detection call sites). Topological sort, cycle
  detection, and the work-stealing deque are intentionally kept as custom perf-critical code —
  not a zuda-first violation, a deliberate prior decision. `string_pool.zig`, `object_pool.zig`,
  and the ASCII graph renderer are zr-domain-specific and out of scope for zuda migration.
- **API patterns**: the TOML parser resets ALL section-state flags on every new section header
  (`task_matrix_raw`, `task_cache`, etc.) to prevent state leaking across sections — easy to
  miss when adding a new field. Inline-table parsing (`retry = {...}`, `mixin_env = {...}`) must
  use the bracket/quote-aware `splitTopLevelFields()` helper, not a naive `splitScalar(',')` —
  a naive split mis-parses nested arrays like `retry_on_codes=[1,2]`. Matrix task variants are
  named `basename:key1=val1:key2=val2` (alphabetically sorted keys) with a meta-task depending
  on every variant. Checkpoint/resume uses `CHECKPOINT: <data>` stdout markers, restored via the
  `ZR_CHECKPOINT` env var on the next run.

## Layout

| Module | Notes |
|---|---|
| `src/main.zig` (3299 lines) | CLI entry point + command dispatcher |
| `src/cli/` | ~30+ subcommands (run, list, show, graph, validate, workspace, repo, tui, ...) |
| `src/config/` | TOML parser (8299 lines), schema types (3565 lines), expr engine, lock file |
| `src/graph/` | DAG, Kahn's-algorithm topo sort, cycle detection, ASCII graph renderer |
| `src/exec/` | scheduler.zig (3755 lines), worker pool, remote(SSH) exec, retry/circuit breaker |
| `src/cache/` | local + remote cache backends (S3/GCS/Azure/HTTP); `remote.zig` 1862 lines |
| `src/toolchain/` | toolchain manager for ~8 languages (node/python/go/rust/etc.) |
| `src/multirepo/` | multi-repo/monorepo orchestration, affected-package detection |
| `src/plugin/` | native + WASM plugin runtime (1520 lines); built-in Docker/Git/Env/Notify/Cache |
| `src/watch/` | polling file watcher + live-reload (946 lines) |
| `src/mcp/`, `src/lsp/`, `src/jsonrpc/` | MCP server (890 lines), LSP server, shared transport |
| `src/output/`, `src/history/` | terminal rendering/colors/progress; execution history |
| `src/analytics/`, `src/ci/`, `src/codeowners/`, `src/conformance/`, `src/context/` | smaller |
| `src/migrate/`, `src/registry/`, `src/template/`, `src/upgrade/`, `src/versioning/` | support |
| `src/util/` | glob, duration, semver, hash, platform, numa.zig (1487), string/object pool |
| `src/lang/`, `src/bench/`, `src/root.zig` | toolchain-language glue, bench harness, module root |
| `tests/` | integration tests (black-box CLI, spawns the real `zr` binary) |
| `examples/` | 15 language-specific example projects |
| `docs/guides/` | ~24 user guides (config, plugins, caching, watch mode, MCP, LSP, ...) |

## Known gaps (from STATE.md)

0 `std.debug.assert` across 112.5k LOC (no runtime invariant checking); 12 `catch unreachable`;
24 files over 800 lines (worst: `config/parser.zig` 8299 with a single ~5100-line `parseToml`);
46 unbounded `while (true)` loops (not individually audited); 93 `std.debug.print` (plausibly
intentional CLI output, not classified). Top risks: `env_file_test.o` binary tracked in git
despite `*.o` being gitignored; README badge shows v1.84.0 vs actual v1.114.0; a history of a
~270-failure CI-red period before v1.113.1 despite current green state; untracked `zig-pkg/` at
repo root not covered by `.gitignore`.
