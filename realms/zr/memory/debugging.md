# zr — debugging

Solutions to tricky bugs, carried over and condensed from the repo's old `.claude/memory/`.
Check here before re-debugging something that already has a known fix.

## `tools/tidy.zig` (vendored) — use-after-free on repeated function names

- **[2026-09-06] `checkFunctionLength` false "unbaselined" failures**: on landing the tidy
  build step (plan 001 item 2), `zig build tidy` failed 2 findings whose baseline entries
  visibly matched (`src/config/types.zig:deinit:142`, `src/watch/native.zig:waitForEvent:74`).
  Root cause: both files declare many same-named methods across sibling structs (10+
  `deinit`s, 7 `waitForEvent`s). `checkFunctionLength`'s per-occurrence loop called
  `allocator.free(key)` on the second+ occurrence's `getOrPut` hit, then read that same freed
  `key` on the very next line via `baseline.get(key)` — under `std.testing.allocator` the freed
  bytes get poisoned, the hash changes, and the lookup misses even though the baseline has the
  right entry. Fix: defer the free until after the `baseline.get` read. Reproduced first with a
  regression test (two same-named functions, second one baselined) before fixing — see
  `tools/tidy.zig` test "checkFunctionLength passes the second of two same-named baselined
  functions". **The identical bug is present in `citadel/templates/tidy` upstream** (the file
  this was vendored from) — not fixed there this cycle (only `/report` may touch citadel from a
  realm session); worth a citadel cycle picking it up so newly-vendoring realms don't repeat it.

## CI red history (context for the "0 failed but still red" trap)

- **[2026-08-28] "0 failed" but CI still exited 1**: GPA leak detection (23 tests leaked memory)
  was the real cause, hidden behind "0 failed" in the log. Root cause: discarding
  `writeTmpConfigPath()`'s or `helpers.runCommand()`'s (`ZrResult`, owns heap stdout/stderr)
  return value without freeing/`.deinit()`-ing it in three integration test files. **Lesson**:
  when GPA reports "N tests leaked memory" alongside "0 failed", the build still exits 1 —
  grep the log for `leaked` separately from `FAIL`, don't trust "0 failed" alone.
- **[2026-07-11] ~270 integration failures, mostly untriaged, on `main` since v1.113.0**: `zig
  build test` (unit) stayed green throughout — only `zig build integration-test` caught it.
  Two confirmed root causes: (1) workflow matrix TOML (`[workflows.X.matrix]`/inline) was
  completely unwired in the parser — `addWorkflow()` never set `Workflow.matrix`; (2)
  `copyTask()` in `config/loader.zig` only deep-copies ~8 of `Task`'s ~40 heap-allocated
  fields, the rest are shallow pointer copies — latent while workspace configs stayed alive
  for the whole command, but a real use-after-free once a caller loads-then-deinits the parent
  config early. **Lesson**: a stabilization session must budget time for
  `zig build integration-test` (~4-5 min), not just unit tests; 270 failures spanning many
  files needs multiple sessions to triage, don't try it all in one cycle.

## Zig 0.15-specific gotchas (verify against 0.16 mapping before reusing post-migration)

- **ArrayList is unmanaged**: `std.ArrayList(T)` maps to `array_list.Aligned(T, null)`. Fix:
  `std.ArrayList(T){}` (not `.init(allocator)`), pass allocator to every mutation method
  (`.deinit(allocator)`, `.append(allocator, item)`, `.appendSlice(allocator, items)`).
  `clearRetainingCapacity()` still takes no allocator; `pop()` now returns `?T`. **Using the
  old `.init(allocator)`-less bare struct wrong compiles but segfaults at runtime (exit 139)**.
- **`ArrayList.deinit` does not zero `items`**: after `list.deinit(allocator)`, `items` still
  points at freed memory (0xaa fill in debug builds) with non-zero len. An `errdefer` that
  iterates `items` after an early `deinit()` reads freed memory. Fix: reset to `list = .{};`
  immediately after any manual `deinit()` so a later `errdefer` sees `len == 0`.
- **`std.posix.setenv` does not exist**: use `@extern` with a comptime platform guard:
  ```zig
  fn posixSetenv(name_z: [*:0]const u8, val_z: [*:0]const u8, overwrite: bool) void {
      if (comptime native_os == .windows) return;
      const c_setenv = @extern(*const fn ([*:0]const u8, [*:0]const u8, c_int)
          callconv(.c) c_int, .{ .name = "setenv" });
      _ = c_setenv(name_z, val_z, if (overwrite) 1 else 0);
  }
  ```
  `@extern` does **not** trigger automatic libc linking — `.link_libc = true` is still required.
- **`std.time.sleep` removed** → use `std.Thread.sleep(ns)`.
- **Windows cross-compile**: `std.posix.*` doesn't exist for Windows targets — centralize ALL
  POSIX-only calls in `src/util/platform.zig` behind `if (comptime native_os == .windows)
  return;` guards. Never call `std.posix.*` directly from module code.
- **`link_libc = true` breaks Windows cross-compile** (`unable to provide libc for target
  'aarch64-windows-msvc'` — Zig doesn't bundle MSVC libc). Fix:
  `.link_libc = if (target.result.os.tag != .windows) true else null`.
- **`std.fmt.allocPrint` needs a comptime format string** — embed the configurable part as a
  runtime *argument*, never as the format string itself.
- **`file.writer(&buf)` is unreliable for appending**: `fw.interface.flush()` did not reliably
  flush all data when appending via `seekFromEnd`. Fix: `std.fmt.bufPrint()` + `file.writeAll()`
  for direct, unbuffered writes when appending to a file.

## Concurrency / process-lifecycle bugs

- **`.Inherit` stdio deadlocks in background test runs**: a child process with `.Inherit`
  inherits the test harness's own stdin/stdout/stderr pipes and deadlocks against it when the
  harness itself runs as a background task. Fix: add `inherit_stdio: bool` to `ProcessConfig`;
  tests always use `.Pipe` (false), production uses `.Inherit` (true, unless output > ~64KB).
- **`addRunArtifact()` hangs `zig build integration-test`**: it uses the `--listen=-` protocol
  (build system talks to the test binary over stdin/stdout). A test binary that itself spawns a
  child process capturing stdout/stderr corrupts that protocol → deadlock. Fix: use
  `std.Build.Step.Run.create()` + `addArtifactArg()` for any test step that spawns children or
  writes to `std.fs.File.stdout()` — this bypasses `--listen=-` entirely. Also: **never** call
  `std.fs.File.stdout()` from test code for this reason.
- **`runSerialChain` vs. worker threads — shared results race**: `runSerialChain` runs on the
  main thread and appended to a shared `results` list without holding the same mutex worker
  threads use. Fix: `runTaskSync` must accept and hold `results_mutex` before any append — any
  shared mutable state touched from multiple threads needs the same lock on every path.
- **`deps_serial` tasks double-ran**: `collectDeps` was traversing `deps_serial` edges too,
  putting those tasks in the DAG's needed set, so the DAG level-runner ran them *and* the serial
  chain ran them. Fix: `collectDeps` only traverses `deps` (parallel edges); `deps_serial` tasks
  run exclusively via `runSerialChain` on demand. Keep DAG-scheduled and serial-chain tasks as
  disjoint sets.
- **`std.process.exit` bypasses defers**: a buffered writer never got flushed before exit
  because `process.exit()` skips all pending defers. Fix: return exit codes from inner
  functions, flush every writer in `main()` before the single `process.exit()` call — never
  call `process.exit` from a helper function.

## Memory-safety bugs (patterns worth re-checking on any new Task/HashMap field)

- **Returning a pointer to a stack-allocated array** (`registry.zig`,
  `getAllProviders()`): `const providers = [_]*const T{...}; return &providers;` is UB — the
  array dies when the function returns; happened to work locally, crashed in CI (exit 255,
  different stack layout). Fix: `const providers = &[_]*const T{...}; return providers;` — the
  `&[_]` form is a compile-time constant living in static storage. **Never return `&local_var`.**
- **`HashMap.get()` returns a copy**: calling `.deinit()` on the result of `.get(name)` frees
  the *copy*, not the map's actual entry, then `.remove(name)` drops the real entry with its
  allocations never freed (leak, plus a potential use-after-free if anything else held a
  pointer). Fix: use `.getPtr(name)` to get a pointer to the real entry before `.deinit()`.
- **`StringHashMap.deinit()` only frees the map structure**, never the values or the owned
  keys. Always iterate and free values (and `entry.key_ptr.*` if keys are owned/duped)
  manually before calling the map's own `.deinit()`.
- **Partial-loop leak on dupe failure**: in multi-field alloc+dupe loops (e.g. `addTaskImpl`'s
  deps/serial-deps arrays), an `errdefer` that only frees the *outer* slice misses already-duped
  inner strings if a later dupe fails mid-loop. Fix: track a duped-count and free
  `slice[0..count]` in the `errdefer`.
- **Bus error freeing string literals**: a test inserted string literals directly into a
  `HashMap` whose `deinit()` calls `allocator.free()` on every key — freeing non-heap memory.
  Fix: always `allocator.dupe()` before inserting into a container whose deinit frees entries.
- **Double free via a stored slice**: a function (`calculateStats()`) stored the `runs` slice
  it received inside its return struct, and that struct's `.deinit()` freed it — a caller-side
  `defer allocator.free(runs)` on the original slice was a double free. Fix: check whether a
  callee's return value already took ownership before adding your own `defer free`.
- **u32 → u8 cast without bounds checking**: casting a UTF-8 codepoint (`cell.char`, u32)
  straight to u8 overflowed for codepoints > 255 (box-drawing chars), panicking with "integer
  does not fit in destination type". Fix: `std.unicode.utf8Encode(@as(u21, @intCast(...)),
  &buf)` and write the resulting bytes, falling back to `"?"` on encode failure.
- **Optional-field pointer is fragile**: `&x.?.field` after `var x: ?T = null; x = value;` may
  point at a copy produced by the `.?` unwrap, not a stable reference. Fix: unwrap to a plain
  (non-optional) variable first, then take `&plain.field`.

## Correctness bugs

- **Kahn's algorithm direction inverted**: in-degree was counting "how many nodes depend on
  this node" (backwards) instead of "how many deps this node has". Fix: seed
  `in_degree[node] = node.dependencies.items.len`; a node with 0 deps runs first. Edge model:
  `X -> Y` means `X` depends on `Y`.
- **Inverted control flow around `access()`**: putting the happy path inside a `catch` block
  (`access() catch |err| { if not-found {...}; ...; return 0; }; return 1;`) reads backwards.
  Fix: extract to a labeled-block bool (`const exists: bool = blk: { ...; break :blk true/false;
  };`) then branch explicitly on it — never bury the success path inside error handling.
- **Weak/tautological test assertions**: e.g. `expect(exit_code != 0)` "verifying" a retry
  feature — passes even with no retry at all; `expect(a or b or c == 0)` always true. **Lesson**:
  every assertion must be able to fail if the implementation is wrong; smoke tests that only
  check "didn't crash" must never claim to verify a specific feature.

## Environment / infra quirks (this dev machine and its launchd/cron setup)

- **macOS TCC blocks `getcwd()` under `~/Desktop/`**: a launchd-spawned process (no TTY) with a
  cwd under a TCC-protected directory (`~/Desktop/`, `~/Documents/`, `~/Downloads/`) hangs
  forever inside `getcwd()`'s `open$NOCANCEL` syscall instead of returning `EPERM`. Diagnosed
  via `sample <pid>`. Fix/prevention: never use a TCC-protected directory as a working
  directory for a launchd agent or background daemon — use `~/codespace/` or similar.
- **`openclaw` not on `PATH`** in autonomous sessions (installed via fnm/npm, not symlinked) —
  use its full path if invoking it directly.
- **CI infinite trigger loop**: `on: push: branches: ["**"]` plus an hourly automated push plus
  a test that could hang produced 6+ simultaneous in-progress runs. Fix: restrict to
  `branches: [main]`, add `paths-ignore` for non-code files, add a `concurrency` group with
  `cancel-in-progress: true`.
