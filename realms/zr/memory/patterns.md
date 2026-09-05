# zr — patterns

_(migrated + condensed from the repo's former .claude/memory/patterns.md, 2026-09-05)_

Verified code patterns for Zig 0.15.x, cross-platform. Keep formulas/snippets verbatim.

## I/O & process (Zig 0.15)

**stdout/stderr writer** (flush before `std.process.exit()`):
```zig
var buf: [4096]u8 = undefined;
var writer = std.fs.File.stdout().writer(&buf);
```

**Process execution** — read pipes BEFORE `wait()`; no `defer child.deinit()`:
```zig
var child = std.process.Child.init(&[_][]const u8{"sh", "-c", cmd}, allocator);
child.stdout_behavior = .Pipe;
try child.spawn();
var output = child.stdout.?.readToEndAlloc(allocator, 1_000_000) catch "";
const term = try child.wait();
const exit_code = switch (term) { .Exited => |c| c, else => 1 };
```

**Incremental stdout capture** (streaming): loop `stdout.read(&buf)` into an
`ArrayListUnmanaged(u8)` via `appendSlice(allocator, buf[0..bytes_read])` until 0 bytes read.

## JSON (Zig 0.15, no `std.json.stringify` convenience API)

Parse: `std.json.parseFromSlice(std.json.Value, allocator, json_str, .{})`, `defer .deinit()`,
then `.value.object.get("field")` and check `.string`/`.object` on the tag.

Build manually via a writer: `writer.writeAll("{\"key\":\"")`, `writer.writeAll(value)`,
`writer.print("{d}", .{num})` — escape quotes/backslashes by hand if the value isn't trusted.

## Memory management

**HashMap double-free**: when the key equals `value.name` (same allocation), don't free the key
separately — `value.deinit()` already frees it.

**Owned key-value pair slice** (`Task.env: [][2][]const u8`): dupe both `[0]` and `[1]` at
construction with partial-cleanup tracking; `deinit` loops the pairs freeing both, then frees
the outer slice.

## Cross-platform

**Windows color**: MUST call `SetConsoleOutputCP(CP_UTF8)` BEFORE setting the VT-mode flag
`0x0004` via `SetConsoleMode` — wrong order produces garbled escape codes.

**Extern C functions**: `@extern(*const fn (...) callconv(.c) RetType, .{ .name = "symbol" })`
— `.c` is lowercase in 0.15.

## TOML parser

Multi-section parser: flush pending state on EVERY section header change; reset ALL pending
flags (`task_matrix_raw = null`, `task_cache = false`, ...) in every reset branch — trivially
forgotten when adding a new field to one branch but not the others. More-specific section
patterns (e.g. `[[...stages]]`) must be checked before less-specific ones (`[workflows.X]`).

**Inline table split** must respect nesting/quotes (`splitTopLevelFields()`, not a naive
`splitScalar(',')`) — see REALM.md "API patterns" for why (`retry_on_codes=[1,2]` breaks a
naive comma split).

## Scheduler & worker threads

```zig
fn workerFn(ctx: WorkerCtx) void {
    defer ctx.semaphore.post();               // release concurrency slot
    defer allocator.free(ctx.task_name);       // owned name
    ctx.results_mutex.lock(); defer ctx.results_mutex.unlock();
    // ... run task, append to shared results ...
}
```
Semaphore pattern: `Semaphore{ .permits = max_jobs }`; `wait()` before spawning a worker,
`post()` in a `defer` so it always releases.

**Retry loop** (inline, not a separate thread):
```zig
var delay_ms = task.retry_delay_ms;
while (!success and attempt < task.retry_max) : (attempt += 1) {
    if (delay_ms > 0) std.Thread.sleep(delay_ms * std.time.ns_per_ms);
    // retry...
    if (task.retry_backoff) delay_ms *= 2;
}
```

## Matrix task expansion (config/loader.zig)

Cartesian product via little-endian increment over per-dimension value counts:
```zig
var di = n_dims;
while (di > 0) {
    di -= 1;
    combo[di] += 1;
    if (combo[di] < dims[di].values.len) break;
    combo[di] = 0;
}
```
Variant name: `basename:key1=val1:key2=val2` (keys alphabetically sorted). Meta-task = original
name, all variants listed as its dependencies.

## Testing patterns

**tmpDir**: `std.testing.tmpDir(.{})`, `defer tmp.cleanup()`,
`tmp.dir.realpathAlloc(allocator, ".")` for an absolute path (avoids cwd sensitivity — build
patterns like glob targets from this absolute path, not a relative one).

**Fixed-buffer writer**: `std.Io.Writer.fixed(&buf)`, then read back `buf[0..writer.end]`.

**Mock config file**: `tmp.dir.writeFile(.{ .sub_path = "zr.toml", .data = toml_content })`.

**Git tests**: `git init -b main` + `git config user.name/email` inside the temp repo (a fresh
CI runner has no global git identity configured).

**Platform-specific test skip**: `if (comptime builtin.os.tag != .linux) return
error.SkipZigTest;`

**Slice coercion gotcha**: `&patterns` (array) gives the wrong type for a `[]const T` field —
use `patterns[0..]` to coerce to a slice.

## Expression evaluator (config/expr.zig)

Fail-open: unknown/unparsed expressions evaluate to `true` (task runs anyway — see
architecture.md for rationale). Lookup order: task_env pairs → process env → `""` (not found).
Operators: `&&`, `||` (short-circuit), `==`, `!=`. Literals: `true`, `false`, `env.VAR`,
`platform == "linux"`, `file.exists("path")`.

## Remote execution task config

```zig
remote: ?[]const u8 = null,          // "user@host:port" | "ssh://..." | "http(s)://..."
remote_cwd: ?[]const u8 = null,
remote_env: [][2][]const u8 = &.{},  // separate from local env
```
`Task.deinit()` must free `remote_cwd` and every `remote_env` pair plus the pair slice itself.
Parser extracts the inline-table body and splits on comma respecting nesting (same
`splitTopLevelFields` concern as above).

## Module extraction

Import siblings with a relative path (`@import("sibling.zig")`); re-export from the parent for
backward compatibility. Add `_ = @import("submodule.zig");` at a comptime site so the new
module's tests are included in `zig build test`. Move shared types to a new module and
re-export from both parents rather than introducing a circular import.

## Plugin system

**DynLib**: `std.DynLib.open(path) catch return error.NotFound;`

**Registry install**: `registry:org/name@version` → `https://github.com/<org>/zr-plugin-<name>`
(skip doubling the `zr-plugin-` prefix if the user's `name` already includes it).

**Git clone**: `git clone --depth=1 <url> <dest>`; treat `.spawn()` failure as "git not on
PATH", not a generic error.

## zuda migration pattern

zuda's `root.zig` exports functions directly, not nested structs —
`zuda.algorithms.string.globMatch(pattern, str)` is already the call, not
`....globMatch.match(...)`. Wrapper pattern for compatibility during migration:
```zig
const zuda = @import("zuda");
pub fn match(pattern: []const u8, str: []const u8) bool {
    return zuda.algorithms.string.globMatch(pattern, str);
}
```
zuda provides algorithms (pattern matching, edit distance), not filesystem traversal — keep
local FS-walking logic, delegate only the core algorithm. Verify a migration with
`zig build integration-test` (faster than the full unit suite) before/after, check for 0
failures.

## Parsing `/proc` files (Linux system metrics)

Colon-separated `key: value [kB]` format (some fields space- some tab-separated) — trim the
value, then trim a trailing `"kB"` unit before `parseInt`. `/proc/[pid]/stat` is
space-tokenized; utime/stime are 1-indexed fields 14 and 15 (0-indexed 13 and 14) — read in a
single pass with a field counter, `break` once both are captured.

## Integration test pattern for composition features (mixins, workspace inheritance)

Standard shape (`tests/*_test.zig`, spawns the real binary via `runZr()`):
write a TOML string literal to a tmp dir with `writeTmpConfig()` → get `tmp.dir.realpathAlloc()`
→ `runZr(allocator, &.{...args}, tmp_path)` → assert `exit_code` and `stdout`/`stderr` substring
presence/absence/ordering (`indexOf()` twice, compare positions for "X ran before Y").
Composition-specific cases worth remembering as a checklist for any new "inherits/composes"
feature: single- and multi-source inheritance (order = left-to-right), field-merge semantics
(scalar override vs. list concatenation vs. set union with dedup), circular-reference detection
(expect non-zero exit), referencing a nonexistent name (expect a stderr message), and multi-
level nesting (verify the whole chain resolves, not just one hop). Keep each test under ~50
lines and name it `test "NNNN: descriptive claim"` — never `test "basic"` — so a failure message
alone tells you what broke.
