# zr — decisions

Decisions that affect future development, carried over from the repo's old `.claude/memory/`.
(Kingdom-wide policy — zuda-first, no local workaround for upstream bugs, opus/sonnet/haiku
subagent split, Zig 0.16 `std.Io` conventions — lives in `citadel/core/rules/`, not repeated
here.)

## Architecture & core systems

- **[2026-02-17] Parallel execution model**: thread-based, `std.Thread.Semaphore` per global
  + per-task (`max_concurrent`). Levels run sequentially, tasks within a level run in parallel;
  per-task semaphore prevents thundering herd.
- **[2026-02-18] Execution levels for DAG**: Kahn's algorithm for topo sort; execution levels
  group independent tasks — deterministic parallel scheduling without an external scheduler.
- **[2026-02-17] Fail-open condition evaluator**: `config/expr.zig` returns `true` on parse
  error; per-task env checked before process env. Prevents a misconfigured condition from
  silently breaking a whole pipeline; narrow, deliberate exception to "no silent failures".
- **[2026-02-18] Polling-based file watcher**: 500ms interval in `src/watch/watcher.zig`,
  cross-platform via `std.fs.Dir.walk()`, skips `.git`/`node_modules`/`zig-out`/`.zig-cache`.
  Chosen over inotify/kqueue for cross-platform simplicity; no external daemon.
- **[2026-02-19] Task output caching**: file-based (`~/.zr/cache/`); key = `Wyhash64(cmd+env)`;
  hit = `.ok` marker file. Cross-process, simple, no locking; marker trivially clearable.
- **[2026-02-19] TOML parser state machine**: section flags (`in_task_matrix`/`env`/
  `toolchain`, `pending_*` buffers) reset fully on every new section header — prevents
  subsection state leaking into the next `[tasks.x]` block.

## Parser & config

- **[2026-02-19] Matrix task expansion at parse time**: Cartesian product via little-endian
  counter; variant naming `basename:key1=val1:key2=val2` (alphabetical keys); meta-task =
  original name with an echo cmd. Parse-time expansion is simpler than runtime; names are
  deterministic; the meta-task stays visible in `list`/`graph`.
- **[2026-02-18] Profile system, in-place mutation**: `Config.applyProfile(name)` mutates task
  env/cmd/cwd in place; CLI flag beats `ZR_PROFILE` env. Enables CI/dev/prod without separate
  config files; mutation keeps the rest of the pipeline unchanged.
- **[2026-02-19] Inline table parsing** (env, retry, hooks, etc.): bracket-depth-aware scanner
  for nested structures, quote-aware to avoid false delimiters. Avoids pulling in an external
  TOML dependency; Zig comptime constraints favor explicit hand-rolled parsing here.

## Plugin system

- **[2026-02-19] Plugin source kinds**: three — local path, `git:URL`,
  `registry:org/name@version` (registry resolves to `https://github.com/org/zr-plugin-name`).
  GitHub as de-facto registry; git tags pin versions; local path covers dev workflows.
- **[2026-02-19] Built-in plugins compiled into the binary**: `src/plugin/builtin.zig` —
  EnvPlugin, GitPlugin, NotifyPlugin, CachePlugin, DockerPlugin; uses a C `setenv()` extern,
  curl/git subprocesses. Avoids `.so` distribution and linking libgit2/libcurl.
- **[2026-02-19] Plugin metadata storage**: `plugin.toml`, flat key=value, in the plugin root;
  stores `git_url`/`registry_ref` after install for auto-update. Keeps source of truth local.

## Execution

- **[2026-02-17] Retry with exponential backoff**: `retry_max`/`retry_delay_ms`/`retry_backoff`
  on `Task`; inline loop in `workerFn`/`runTaskSync`; delay doubles if `backoff=true`. Simpler
  than a separate retry thread; exponential backoff is the standard fault-tolerance default.
- **[2026-02-18] Circuit breaker for error recovery (v1.30)**: per-task `CircuitBreakerConfig`;
  state machine closed→open→half-open; `failure_threshold`, `window_ms`, `min_attempts`,
  `reset_timeout_ms`. Per-task isolation avoids one failing task affecting unrelated ones.
- **[2026-02-18] Workflow retry budget (v1.34)**: optional `retry_budget` on `Workflow`, shared
  across all stages via `RetryBudgetTracker`. Prevents unbounded retries in multi-stage flows.
- **[2026-03-14] Checkpoint/resume via stdout markers**: task emits `CHECKPOINT: <data>` to
  stdout; scheduler saves state to `~/.zr/checkpoints/`, provides it back via `ZR_CHECKPOINT`
  on resume. Lightweight, human-readable; stdout is treated as the canonical IPC channel.
- **[2026-03-16] Output capture (stream/buffer/discard)**: three modes via `OutputCapture`
  struct, keyed by task name + run ID; buffering has FIFO eviction at a size limit.

## CLI & output

- **[2026-02-18] Global flags parsed in the dispatcher**: `--jobs`/`--config`/`--no-color`/
  `--quiet`/`--verbose` validated in `run()` before command dispatch, then passed down —
  centralizes validation, keeps flags available to every command.
- **[2026-02-18] JSON output (`--format`)**: a separate output code path per command with its
  own schema (list/graph/run/history); control chars escaped as `\uXXXX`. Keeps machine-
  readable output from entangling with the text-rendering code path.
- **[2026-02-17] TTY-aware color**: `output/color.zig`, TTY detection via
  `std.fs.File.isTty()`, overridable via `--no-color` and a task-level `output: false`. Avoids
  ANSI codes leaking into CI logs; per-task override supports piping.
- **[2026-02-18] Dry-run via a flag, not a separate command**: `dry_run: bool` in
  `SchedulerConfig` skips execution but still tracks results (`skipped=true`); a separate
  `planDryRun()` returns a `DryRunPlan`. Reuses the existing scheduler rather than forking it.

## Cross-cutting

- **[2026-02-17] String ownership**: `Allocator.dupe()` at parse time; `Task.deinit()` frees
  every owned slice; no partial frees inside individual functions. Central deinit prevents
  use-after-free across the many optional/variant fields on `Task`.
- **[2026-02-18] No `@panic` in library code**: explicit error sets; fail-open is reserved for
  non-critical paths only (expressions, history, output) — everything else propagates errors.
- **[2026-03-14] Zig 0.15 ArrayList is unmanaged**: use `ArrayList(T){}`, not `.init(allocator)`
  — pass the allocator to every mutation (`.append()`, `.deinit()`). This shape changes again
  under the Zig 0.16 migration (`.empty`/`.initCapacity`, see `citadel/core/rules/zig-0.16.md`)
  — do not write new 0.15-only `ArrayList(T){}` code once that migration starts.
