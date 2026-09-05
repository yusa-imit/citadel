# zr — architecture

## Module dependency flow

```
CLI → Config → Graph → Exec → Plugin
              ↘ Output (shared)
```

- Config engine is independent; no dependency on execution.
- Graph engine takes parsed config, produces an execution plan.
- Exec engine takes the execution plan, manages processes.
- Output module is shared across all layers for terminal rendering.

## Core design choices

- **Config**: TOML for readability + a built-in expression engine for conditions/matrix/retry,
  keeping config declarative while allowing dynamic behavior. Hand-rolled state-machine parser
  (no external TOML dep) — section flags reset fully on every new section header to avoid state
  leakage across `[tasks.x]`/`[tasks.y]` boundaries; a bracket-depth + quote-aware scanner
  handles inline tables/arrays (`{ a = 1, b = [1,2] }`) so nested commas don't mis-split.
- **Execution**: `std.Thread`-based worker pool (not async — considered too experimental at the
  time), default worker count = logical CPU cores, per-task concurrency via semaphores. DAG
  execution levels via Kahn's-algorithm topo sort: tasks within a level run in parallel, levels
  run sequentially. Retry is an inline exponential-backoff loop inside `workerFn`/
  `runTaskSync`, not a separate thread; a per-task circuit breaker (closed→open→half-open) sits
  alongside it, plus an optional workflow-level shared retry budget across all stages.
- **Matrix task expansion** happens at parse time (Cartesian product via little-endian counter),
  not at runtime — deterministic `basename:key=val` naming (alphabetical keys), with a
  meta-task (original name, cmd = echo) depending on all expanded variants.
- **Profiles**: `Config.applyProfile(name)` mutates task env/cmd/cwd in place; CLI flag takes
  priority over the `ZR_PROFILE` env var.
- **File watcher**: polling-based, 500ms interval, `std.fs.Dir.walk()`, skips
  `.git`/`node_modules`/`zig-out`/`.zig-cache` — deliberately not inotify/kqueue-native, for
  cross-platform simplicity; sufficient for dev workflows, avoids an external daemon.
- **Task output cache**: file-based (`~/.zr/cache/`), key = `Wyhash64(cmd+env)`, cache hit is
  signaled by a `.ok` marker file. Cross-process, no locking needed.
- **Checkpoint/resume**: a task emits `CHECKPOINT: <data>` to stdout; the scheduler detects the
  marker, saves state under `~/.zr/checkpoints/`, and a resumed run receives it back via the
  `ZR_CHECKPOINT` env var. Deliberately simple (stdout as canonical IPC) over a richer protocol.
- **Output capture**: three modes (stream to file / buffer in memory with FIFO eviction at a
  limit / discard), keyed by task name + run ID.
- **Plugin system**: three source kinds — local path, `git:URL`, `registry:org/name@version`
  (registry resolves to `https://github.com/org/zr-plugin-name`, version = git tag). Five
  built-in native plugins (Env/Git/Notify/Cache/Docker) are compiled directly into the binary to
  avoid `.so` distribution; a WASM runtime exists alongside for external/sandboxed plugins.
  `plugin.toml` (flat key=value) stores `git_url`/`registry_ref` for auto-update.
- **Remote execution**: tasks carry `remote`/`remote_cwd`/`remote_env` fields for SSH-style
  remote execution, independent from local `env`.

## Ownership and error-handling conventions

- String ownership: `allocator.dupe()` at parse time; each type's own centralized `deinit()`
  frees every owned slice — never partial frees inline. `Task.deinit()` is canonical; a new
  heap-allocated `Task` field that isn't added there leaks (this exact bug recurred via
  `copyTask()` during workspace-inheritance work — see debugging.md).
- No `@panic` in library code: explicit error sets everywhere; fail-open is a deliberate,
  narrow exception for non-critical paths only (`config/expr.zig` condition evaluation,
  history, output) — a parse error there evaluates to `true`/best-effort rather than breaking
  the whole pipeline. This is a policy choice, not a place to add new panics.
