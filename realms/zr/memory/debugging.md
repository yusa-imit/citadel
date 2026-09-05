# zr — debugging

_(migrated + condensed from the repo's former .claude/memory/debugging.md, 2026-09-05)_

## Known Zig 0.15.x gotchas

- `std.ArrayList(T){}` not `.init(allocator)` — unmanaged API; pass the allocator to every
  mutation (`.append(allocator, item)`, `.deinit(allocator)`); `clearRetainingCapacity()` still
  takes none; `pop()` now returns `?T`.
- `std.time.sleep` removed — use `std.Thread.sleep(nanoseconds)`.
- `std.posix.setenv` doesn't exist — use `@extern` with a comptime platform guard:
  ```zig
  fn posixSetenv(name_z: [*:0]const u8, val_z: [*:0]const u8, overwrite: bool) void {
      if (comptime native_os == .windows) return;
      const c_setenv = @extern(*const fn ([*:0]const u8, [*:0]const u8, c_int)
          callconv(.c) c_int, .{ .name = "setenv" });
      _ = c_setenv(name_z, val_z, if (overwrite) 1 else 0);
  }
  ```
  `@extern` does NOT trigger automatic libc linking — `.link_libc = true` is still required.
- `std.fmt.allocPrint(allocator, runtime_string, .{...})` fails to compile — the format string
  must be comptime-known; keep it fixed and pass the variable part as an argument.
- `child.wait()` closes stdout — always read pipes BEFORE calling `wait()`. `Child` needs no
  `deinit()`.
- `std.process.exit()` bypasses defers — buffered writers are never flushed. Return exit codes
  from inner functions, flush all writers in `main()`, call `exit()` only there.
- `HashMap.get()` returns a VALUE (copy), not a pointer — for structs with allocated fields,
  always use `getPtr()` before calling `.deinit()` on the entry, or you leak/free-then-remove
  the wrong copy.
- `StringHashMap.deinit()` only frees the map structure, never the values — iterate and free
  values manually first.
- After manually calling `list.deinit(allocator)`, `items` still points at freed (0xaa-filled
  in debug builds) memory with its old `len` — immediately reset with `list = .{};` so a
  following `errdefer` doesn't read freed memory.
- `file.writer(&buf)` + `.interface.flush()` is unreliable for append-with-seek; prefer
  `std.fmt.bufPrint()` + `file.writeAll()` for direct, unbuffered file writes.
- NEVER return `&local_var` from a function — even an array. Use a compile-time constant:
  `const providers = &[_]T{...}; return providers;`, not
  `const providers = [_]T{...}; return &providers;` (dangling stack pointer; can pass locally
  and crash only in CI due to different stack/optimization layout — exit code 255 is a common
  symptom of this class of UB).
- `zig build test` / `zig build integration-test` hang with no output: `addRunArtifact()` uses
  the `--listen=-` build-server protocol over the test binary's stdin/stdout; a test (or a
  spawned child process under integration tests) that writes to `std.fs.File.stdout()` corrupts
  that protocol and deadlocks both sides. Fix: use `std.Build.Step.Run.create()` +
  `addArtifactArg()` instead of `addRunArtifact()` for any test binary that touches stdout, and
  never call `std.fs.File.stdout()` from test code.
- `.Inherit` stdio in a child process spawned from a test deadlocks when the test harness itself
  runs as a background task (e.g. backgrounded Bash, CI) — the child inherits the harness's own
  pipes. Use `.Pipe` for stdout/stderr in tests (`inherit_stdio: false`); only production code
  should use `.Inherit`.
- Windows cross-compile: `std.posix` doesn't exist for Windows targets — centralize ALL
  POSIX-only calls behind `src/util/platform.zig` with `if (comptime native_os == .windows)`
  guards; never call `std.posix.*` directly from feature code. `.link_libc = true`
  unconditionally breaks Windows cross-compile (no bundled MSVC libc) — condition it:
  `.link_libc = if (target.result.os.tag != .windows) true else null`. PID type also differs:
  `std.posix.pid_t` (POSIX) vs `std.os.windows.HANDLE` (Windows) — branch on
  `builtin.os.tag == .windows` for the type signature, not just the value.

## Precise bugs worth remembering verbatim

- **Kahn's algorithm direction inverted**: in-degree must count "how many deps does this node
  have" (`in_degree[node] = node.dependencies.items.len`), not "how many nodes depend on this
  node". Leaf tasks (0 deps) must have in-degree 0 and run first — if the topo-sort tests fail
  an `a_idx < b_idx` ordering assertion, check this first.
- **`deps_serial` tasks must be disjoint from the DAG**: `collectDeps` must only traverse `deps`
  (parallel edges) — if it also follows `deps_serial`, those tasks get scheduled twice (once via
  the serial chain, once via the DAG level runner). See architecture.md.
- **Hard resource limits (cgroups/Job Objects)**: create-before-spawn, apply-after-spawn.
  1) `createHardLimits()` before `child.spawn()` (Linux: cgroup dir + control files; Windows:
  Job Object). 2) `spawn()`. 3) `applyHardLimits(&handle, child.id)` after spawn (Linux: write
  PID to `cgroup.procs`; Windows: `AssignProcessToJobObject`). Fall back to a no-op handle plus
  the `ResourceMonitor` polling-thread soft-limit killer (`killProcess()`, SIGKILL/
  `TerminateProcess`) if hard limits are unavailable (permissions, macOS has no cgroups).
  `child.id` type differs by platform — same POSIX/Windows split as above.
- **Inverted control flow with `access()`**: don't bury the happy path inside a `catch` block.
  Extract a labeled-block boolean first, then branch explicitly:
  ```zig
  const exists: bool = blk: {
      dir.access(file, .{}) catch |err| {
          if (err == error.FileNotFound) break :blk false;
          return err;
      };
      break :blk true;
  };
  if (exists) { /* refuse */ } else { /* happy path */ }
  ```
- **Optional-field pointer is fragile**: never take `&optional.?.field` — the `.?` unwrap may
  return a copy, so the pointer can point at a temporary. Unwrap to a plain (non-optional)
  variable first, then take the address of that variable's field.
- **Partial-allocation cleanup in a dupe loop**: track a `duped` count and free only
  `slice[0..duped]` in `errdefer`, plus the outer slice — freeing the full slice on a mid-loop
  failure double-frees or frees uninitialized memory.

## Test-quality anti-patterns (recurring across sessions)

1. Trivially-true assertions: `expect(a.len > 0 or b.len > 0 or exit_code == 0)` passes
   regardless of behavior. A "smoke test" that only checks `exit_code != 0` for a
   retry/feature-specific test passes even with the feature entirely absent.
2. Copying the implementation's own output as the expected value
   (`const expected = computeHash(input); expectEqual(expected, computeHash(input))`) — use a
   known literal expected value instead.
3. `deinit()` tests that call deinit without first asserting on the fields it's about to free —
   only catches leaks, never correctness.
4. UTF-8: never cast a `u32` codepoint to `u8` directly (`@intCast` overflow panic on
   box-drawing/wide chars) — use `std.unicode.utf8Encode()`.

## Resolved / historical (compressed)

- CI red since v1.113.0 (~270 integration failures, issue #124, resolved 2026-08-28): root
  cause was mixed — (a) 23 tests leaked memory via discarded `ZrResult`/path-allocation return
  values that own heap memory (GPA reports "N leaked" alongside "0 failed" — the build **still
  exits 1**; always grep logs for `leaked` separately from `FAIL`); (b) workflow `matrix` TOML
  was silently unwired in the parser (`addWorkflow()` never set `.matrix`); (c) `copyTask()` in
  `loader.zig` only deep-copied ~8 of Task's ~40 heap-allocated fields, latent until a new
  (v1.114.0) code path started `deinit()`-ing the source config while a shallow-copied pointer
  was still live — a real use-after-free. All three fixed; full suite green.
- Memory leaks in `loader.zig`'s `parseToml`: was duping temp strings that `addTask` also duped
  (double-owned copies). Fix: delay allocation until data is actually stored in a persistent
  struct; only the final store site dupes.
- Memory leak in `dag.zig`: `deinit` freed node values but not `StringHashMap` keys (separately
  `allocator.dupe()`'d strings) — free `entry.key_ptr.*` too.
- `runSerialChain` (main thread) appended to the shared results list without holding
  `results_mutex` while worker threads did — any shared mutable state across threads needs the
  same lock on every access path, not just the "obvious" ones.
- `analytics_tui` UTF-8 crash, `Schedule remove`/`Schedule` command bugs (both HashMap-copy and
  missing-persistence classes), and a double-free/bus-error pair in early test code are all
  folded into the gotcha list above — see `git log` for the original commits if full repro
  detail is ever needed.
- CI infinite trigger loop (2026-02-24): `on: push: branches: ["**"]` plus an hourly cron push
  plus a test hang queued 6+ concurrent runs. Fixed by restricting to `branches: [main]`, adding
  `paths-ignore` for memory/docs, and a `concurrency` group with `cancel-in-progress: true` —
  already reflected in the current `ci.yml`.

## Open issue

- **#100, intermittent argv joining on macOS arm64** (since 2026-06-25): `zr cache status` is
  occasionally received as one joined argv (`"cache status"`) instead of two args; consistent
  within a process tree, flips between independent shell sessions, no deterministic reproducer.
  Suspected macOS arm64 / Zig 0.15 `std.os.argv` startup interaction with `link_libc = true`,
  not confirmed. A workaround detects a space in an unknown command and prints a hint to retry
  without quotes. Still open — verify against future Zig 0.15.x release notes for an argv fix.
