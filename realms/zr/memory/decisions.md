# zr — decisions

_(migrated from the repo's former .claude/memory/decisions.md, 2026-09-05)_

Format: Context (why) → Decision (what) → Rationale (why this choice matters).

## Parser & config

### [2026-02-19] Matrix task expansion (parse-time)
- Decision: Cartesian product via little-endian counter; variant naming
  `basename:key1=val1:key2=val2` (alphabetical keys); meta-task = original name with echo cmd.
- Rationale: parse-time expansion is simpler than runtime; deterministic names; meta-task stays
  visible in `zr list`/`zr graph`.

### [2026-02-18] Profile system (in-place mutation)
- Decision: `Config.applyProfile(name)` mutates task env/cmd/cwd in place; CLI flag overrides
  the `ZR_PROFILE` env var.
- Rationale: profiles enable CI/dev/prod variants without separate config files; in-place
  mutation keeps the rest of the pipeline unchanged.

### [2026-02-19] Inline table parsing (env, retry, hooks, mixin_env)
- Decision: bracket-depth-aware, quote-aware scanner for nested structures
  (`splitTopLevelFields()`), not an external TOML parser.
- Rationale: Zig comptime constraints favor explicit parsing; bracket/quote awareness is
  required to correctly split values like `retry_on_codes=[1,2]` inside an inline table.

## Plugin system

### [2026-02-19] Plugin source kinds
- Decision: three kinds — local path, `git:URL`, `registry:org/name@version` (registry resolves
  to `https://github.com/org/zr-plugin-name`, version = git tag).
- Rationale: GitHub as a de-facto registry; git tags pin versions; local path covers dev
  workflows.

### [2026-02-19] Built-in plugins compiled into the binary
- Decision: `src/plugin/builtin.zig` ships EnvPlugin, GitPlugin, NotifyPlugin, CachePlugin,
  DockerPlugin; uses a C `setenv()` extern plus curl/git subprocesses.
- Rationale: avoids `.so` distribution and linking libgit2/libcurl; subprocesses are pragmatic
  for wrapping external tools.

### [2026-02-19] Plugin metadata storage
- Decision: `plugin.toml` — flat key=value in the plugin root, storing `git_url`/`registry_ref`
  after install, for auto-update.
- Rationale: metadata lives with the plugin, no separate manifest file needed.

## Execution

### [2026-02-17] Parallel execution model
- Decision: thread-based via `std.Thread.Semaphore`, one global + one per-task
  (`max_concurrent`); DAG levels run sequentially, tasks within a level run in parallel.
- Rationale: CPU-bound tasks parallelize naturally; per-task semaphore prevents a single
  expensive task from causing a thundering herd.

### [2026-02-18] Execution levels for the DAG
- Decision: Kahn's algorithm for topo sort; execution levels group independent tasks.
- Rationale: deterministic parallel scheduling without an external scheduler dependency.

### [2026-02-18] Circuit breaker for error recovery (v1.30)
- Decision: per-task `CircuitBreakerConfig`; state machine closed → open → half-open, driven by
  `failure_threshold`/`window_ms`/`min_attempts`/`reset_timeout_ms`.
- Rationale: prevents cascading failures; per-task isolation avoids penalizing unrelated tasks.

### [2026-02-18] Workflow retry budget (v1.34)
- Decision: optional `retry_budget` on a Workflow, shared across all stages via
  `RetryBudgetTracker`.
- Rationale: workflow-level limit prevents unbounded total retries across a multi-stage run.

### [2026-03-14] Checkpoint/resume via stdout markers
- Decision: a task emits `CHECKPOINT: <data>` to stdout; the scheduler detects the marker,
  saves state under `~/.zr/checkpoints/`, and provides it via `ZR_CHECKPOINT` env on resume.
- Rationale: markers are lightweight and human-readable; stdout is the canonical IPC channel
  already available to every task.

### [2026-03-16] Output capture: stream / buffer / discard
- Decision: three modes via `OutputCapture`, keyed by task name + run ID; buffer mode uses FIFO
  eviction at a size limit.
- Rationale: flexible enough for logs, failure inspection, and remote submission, while FIFO
  eviction bounds memory for long-running or noisy tasks.

## CLI & output

### [2026-02-18] Global flags parsed centrally in the dispatcher
- Decision: `--jobs`/`--config`/`--no-color`/`--quiet`/`--verbose` are parsed and validated in
  `run()` before command dispatch, then passed down to loaders/schedulers.
- Rationale: centralized parsing keeps behavior consistent across every command and catches
  invalid flags before any command-specific logic runs.

### [2026-02-18] JSON output as a separate code path (`--format`)
- Decision: dedicated JSON output path per command, with schemas for list/graph/run/history and
  `\uXXXX`-based control-char escaping.
- Rationale: machine-readable output enables tool integration without entangling the format
  with text-output logic.

### [2026-02-17] TTY-aware color output
- Decision: `output/color.zig`, TTY detection via `std.fs.File.isTty()`, overridable with
  `--no-color` and a task-level `output: false` field.
- Rationale: colors improve interactive UX; TTY detection keeps ANSI codes out of CI logs;
  task-level override supports piping.

### [2026-02-18] Dry-run as a separate plan function
- Decision: `dry_run: bool` on `SchedulerConfig` skips execution but tracks results as
  `skipped=true`; a separate `planDryRun()` returns a `DryRunPlan` structure.
- Rationale: a dedicated plan function is cleaner than threading a writer through the real
  scheduler just to suppress side effects.

Full history (superseded/one-off decisions) lives in `git log` — this file keeps only decisions
with ongoing relevance to future work.
