# zr — patterns

Verified code patterns, carried over and condensed from the repo's old `.claude/memory/`.
Zig-0.15-era; re-verify each against `citadel/core/rules/zig-0.16.md` before reuse post-migration.

## I/O & process (Zig 0.15)

**stdout/stderr writer**:
```zig
var buf: [4096]u8 = undefined;
var writer = std.fs.File.stdout().writer(&buf);
// Always call .interface.flush() before std.process.exit()
```

**Process execution** — read pipes BEFORE `wait()` (`wait()` closes stdout); no `child.deinit()`:
```zig
var child = std.process.Child.init(&[_][]const u8{"sh", "-c", cmd}, allocator);
child.stdin_behavior = .Inherit;
child.stdout_behavior = .Pipe;
try child.spawn();
var output = child.stdout.?.readToEndAlloc(allocator, 1_000_000) catch "";
const term = try child.wait();
const exit_code = switch (term) { .Exited => |c| c, else => 1 };
```

**Stream stdout incrementally**:
```zig
var list: std.ArrayListUnmanaged(u8) = .{};
var buf: [4096]u8 = undefined;
if (child.stdout) |stdout| {
    while (true) {
        const n = try stdout.read(&buf);
        if (n == 0) break;
        try list.appendSlice(allocator, buf[0..n]);
    }
}
```

## JSON (manual, no stringify API used in this codebase)

```zig
var parsed = try std.json.parseFromSlice(std.json.Value, allocator, json_str, .{});
defer parsed.deinit();
if (parsed.value.object.get("field")) |v| { if (v == .string) { const s = v.string; } }
```
Manual building: append literal fragments (`"{\"key\":\""`) via an `ArrayListUnmanaged(u8)`
writer; escape special chars manually for anything not already a known-safe string slice.

## Memory management

**ArrayList (unmanaged API)**: `var list = std.ArrayList(u8){}; defer list.deinit(allocator);`

**Partial-alloc cleanup**, tracking how far a loop got before erroring:
```zig
var duped: usize = 0;
errdefer { for (slice[0..duped]) |s| allocator.free(s); allocator.free(slice); }
for (items, 0..) |item, i| { slice[i] = try allocator.dupe(u8, item); duped += 1; }
```

**HashMap double-free**: when a key is the same allocation as `value.name`, don't free the key
separately — freeing the value already frees it.

## Cross-platform

- All POSIX calls go through `src/util/platform.zig` wrappers with comptime OS guards.
- Windows color: call `SetConsoleOutputCP(CP_UTF8)` **before** setting the VT-mode flag
  `0x0004` on the console (fixes garbled codes if done in the other order).
- PID types differ: `std.os.windows.HANDLE` on Windows, `std.posix.pid_t` on POSIX — switch on
  `builtin.os.tag == .windows`.
- Extern C functions: `@extern(*const fn (...) callconv(.c) RetType, .{ .name = "symbol" })`
  (lowercase `.c` in 0.15).

## TOML parser

Multi-section parser: flush pending state on **every** section-header change; reset every
`*_raw`/pending flag on every reset path (easy to miss one). More specific branches
(`[[...stages]]`) must be checked before less specific ones (`[workflows.X]`).

Inline table parsing pattern (bracket-depth/quote-aware in the real parser, illustrated here
in simplified form):
```zig
if (std.mem.startsWith(u8, value, "{") and std.mem.endsWith(u8, value, "}")) {
    var it = std.mem.splitScalar(u8, inner[1..len-1], ',');
    while (it.next()) |pair| {
        const eq = std.mem.indexOf(u8, pair, "=").?;
        const k = std.mem.trim(u8, pair[0..eq], " \t\"");
        const v = std.mem.trim(u8, pair[eq+1..], " \t\"");
    }
}
```

## Scheduler & worker threads

```zig
const WorkerCtx = struct { allocator, task_name /* owned */, results, mutex, semaphore, failed };
fn workerFn(ctx: WorkerCtx) void {
    defer ctx.semaphore.post();          // release slot
    defer ctx.allocator.free(ctx.task_name);
    ctx.results_mutex.lock(); defer ctx.results_mutex.unlock();
}
```
Semaphore pattern: `Semaphore{ .permits = max_jobs }`; `wait()` before spawn, `post()` in defer.

**Retry loop** (inline, not a separate thread — see decisions.md):
```zig
var delay_ms = task.retry_delay_ms;
while (!success and attempt < task.retry_max) : (attempt += 1) {
    if (delay_ms > 0) std.Thread.sleep(delay_ms * std.time.ns_per_ms);
    // retry ...
    if (task.retry_backoff) delay_ms *= 2;
}
```

## Testing

```zig
var tmp = std.testing.tmpDir(.{});
defer tmp.cleanup();
const tmp_path = try tmp.dir.realpathAlloc(allocator, ".");
defer allocator.free(tmp_path);
try tmp.dir.writeFile(.{ .sub_path = "zr.toml", .data = toml_content });
```
Fixed-buffer writer: `var w = std.Io.Writer.fixed(&buf); /* ... */ const out = buf[0..w.end];`

Git-dependent tests: `git init -b main` + `git config user.name/email` inside the temp repo.

Platform-specific: `if (comptime builtin.os.tag != .linux) return error.SkipZigTest;`

**Composition-feature integration tests** (mixins 8000s, workspace 6000s): write TOML as a
string literal → `writeTmpConfig()` → `runZr()` a real binary invocation → assert on
`exit_code` and `stdout`/`stderr` substrings via `indexOf`, never a tautological
`expect(true)`. For ordering, compare two `indexOf()` results directly rather than re-deriving
positions. Keep each test under ~50 lines, one clearly named behavior per test.

## Expression evaluator (`config/expr.zig`)

Fail-open: an unknown/unparseable expression evaluates to `true` (task runs anyway — see
decisions.md). Env lookup order: task-level `env` pairs → process env → `""` if not found.
Operators: `&&`/`||` (short-circuit), `==`, `!=`. Literals: `true`/`false`, `env.VAR`,
`platform == "linux"`, `file.exists("path")`.

## Color output (`output/color.zig`)

TTY check: `color.isTty(std.fs.File.stdout())`. Always go through the semantic helpers
(`printSuccess`/`printError`/`printInfo`/`printBold`/`printDim`) — never embed raw ANSI codes.

## File operations

Existence check without burying the happy path in a catch (see debugging.md's inverted-control-
flow entry):
```zig
const exists: bool = blk: {
    dir.access(path, .{}) catch |err| {
        if (err == error.FileNotFound) break :blk false;
        return err;
    };
    break :blk true;
};
```
Prefer accepting a `std.fs.Dir` parameter over calling `std.fs.cwd()` directly, for testability.

## zuda migration

- Access via `@import("zuda")`; root.zig exports **functions**, not nested struct methods —
  `zuda.algorithms.string.globMatch(pattern, str)` is correct as-is, it is not
  `globMatch.match(...)`.
- Wrapper pattern for compatibility: keep the local function signature, delegate the body:
  ```zig
  const zuda = @import("zuda");
  pub fn match(pattern: []const u8, str: []const u8) bool {
      return zuda.algorithms.string.globMatch(pattern, str);
  }
  ```
- zuda provides algorithms (pattern matching, edit distance), not filesystem traversal — keep
  local FS-walking logic, delegate only the core algorithm call.
- Verify a migration with `zig build integration-test` (faster than the full unit suite) and
  confirm 0 failures.

## Parsing `/proc` files (Linux system metrics)

Generic `key: value[kB]` extractor — tokenize on `\n`, match line prefix, split on `:`, trim
`"kB \t"` from the value, `parseInt`. For `/proc/[pid]/stat`, fields are space-separated and
1-indexed; utime/stime (CPU jiffies) are fields 14/15 (index 13/14). Always test presence,
absence, empty content, and malformed input; remember to convert kB → bytes (`* 1024`) when the
caller needs bytes.

## Module extraction

Import siblings via relative `@import("sibling.zig")`; re-export from the parent module for
backward compatibility. Register new test files with `_ = @import("submodule.zig");` in the
parent so `zig build test` picks them up. Move shared types to a new module and re-export rather
than creating circular imports.

## Workspace resolution

`&patterns` (where `patterns` is `[N][]const u8`) gives the wrong type for a slice parameter —
use `patterns[0..]` to coerce to a slice. Build test patterns with absolute temp-dir paths to
avoid cwd sensitivity.
