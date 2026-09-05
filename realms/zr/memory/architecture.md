# zr — architecture

_(migrated from the repo's former .claude/memory/architecture.md + decisions.md, 2026-09-05)_

## Module dependency graph

```
CLI → Config → Graph → Exec → Plugin
              ↘ Output (shared)
```

- `config` is independent; no dependency on execution.
- `graph` takes parsed config, produces an execution plan.
- `exec` takes the execution plan, manages processes.
- `output` is shared across all layers for terminal rendering.

Full module dependency order for implement/fix work: `config → graph → exec → plugin`
(see `REALM.md`).

## Key architectural decisions

### TOML + expression engine
- Config format: TOML for readability.
- Expression engine for conditions, matrix expansion, retry logic.
- Keeps config declarative while still supporting dynamic behavior.

### Worker pool (`std.Thread`, not async)
- OS threads via `std.Thread` — Zig's async was experimental, deliberately avoided.
- Default worker count = logical CPU cores.
- Parallel execution model: `std.Thread.Semaphore` per global + per-task (`max_concurrent`).
  Execution levels (from the DAG topo sort) run sequentially; tasks within a level run in
  parallel. Per-task semaphore prevents thundering-herd on a single expensive task.

### DAG for dependencies
- Kahn's algorithm for topological sort and cycle detection.
- Execution levels group independent tasks for deterministic parallel scheduling without an
  external scheduler.
- `deps` (parallel) and `deps_serial` (serial-chain) edges are disjoint sets — `deps_serial`
  tasks are never also scheduled via the DAG level runner (see debugging.md for the bug this
  guards against).

### Fail-open condition evaluator
- `config/expr.zig` returns `true` on parse error.
- Rationale: a misconfigured condition should not silently break an entire pipeline. Per-task
  env is checked before process env (isolation for tests).

### Polling-based file watcher
- 500ms interval in `src/watch/`, cross-platform via `std.fs.Dir.walk()`.
- Skips `.git`, `node_modules`, `zig-out`, `.zig-cache`.
- Deliberately not inotify/kqueue-native — cross-platform simplicity over lower latency;
  500ms is sufficient for a dev workflow.

### Task output caching
- File-based cache under `~/.zr/cache/`.
- Key = `Wyhash64(cmd+env)`; hit is a `.ok` marker file.
- Cross-process, no locking needed; a marker file is trivially clearable by hand.

### TOML parser state machine
- Section flags (`in_task_matrix`/`env`/`toolchain`, `pending_*` buffers) reset FULLY on every
  new section header — prevents subsection state leaking into the next section. Easy to miss
  when adding a new field; see `patterns.md` for the concrete gotcha.

### Matrix task expansion (parse-time, not runtime)
- Cartesian product via a little-endian counter.
- Variant naming: `basename:key1=val1:key2=val2` (alphabetically sorted keys).
- A meta-task (original name, echo command) depends on every expanded variant, so it stays
  visible in `zr list`/`zr graph`.

### Profile system (in-place mutation)
- `Config.applyProfile(name)` mutates task env/cmd/cwd in place.
- CLI flag overrides the `ZR_PROFILE` env var.

### Plugin system
- Three source kinds: local path, `git:URL`, `registry:org/name@version` (registry resolves to
  `https://github.com/org/zr-plugin-name`, version = git tag).
- 5 built-in native plugins (Env/Git/Notify/Cache/Docker) compiled into the binary — avoids
  `.so` distribution; uses a C `setenv()` extern plus curl/git subprocesses for external tools.
- `plugin.toml` (flat key=value) stores `git_url`/`registry_ref` for auto-update.

### Execution reliability features
- Retry: exponential backoff inline in `workerFn`/`runTaskSync` (not a separate thread); delay
  doubles when `retry_backoff = true`.
- Circuit breaker: per-task state machine (closed → open → half-open), driven by
  `failure_threshold`/`window_ms`/`min_attempts`/`reset_timeout_ms`.
- Workflow-level `retry_budget` shared across all stages via `RetryBudgetTracker`.
- Checkpoint/resume: task emits `CHECKPOINT: <data>` to stdout; scheduler saves to
  `~/.zr/checkpoints/`, restores via the `ZR_CHECKPOINT` env var on the next run.
- Output capture: 3 modes (stream/buffer/discard); buffer mode uses FIFO eviction at a size
  limit.

### Cross-cutting
- String ownership: `allocator.dupe()` at parse time; a centralized `deinit()` frees every
  owned slice — never partial frees inline.
- Error handling: no `@panic` in library code; explicit error sets; fail-open only for
  non-critical paths (expr, history, output).
