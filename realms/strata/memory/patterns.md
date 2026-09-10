# strata — patterns

_(migrated from the repo's former .claude/memory; keep under 200 lines)_

## vtable interface

```zig
pub const Thing = struct {
    ptr: *anyopaque,
    vtable: *const VTable,
    pub const VTable = struct {
        doIt: *const fn (*anyopaque, arg: u32) anyerror!void,
    };
    pub fn doIt(self: Thing, arg: u32) !void {
        return self.vtable.doIt(self.ptr, arg);
    }
};
```

## Test with temporary directory (0.16 shape)

`tmp.dir` is an `Io.Dir`; every operation on it now takes `io` as an explicit argument, and
`io` in a test must always be `std.testing.io` (module-level, never a hand-built `Io.Threaded`)
— confirmed 2026-09-11 (cycle 7), the repo's first real I/O-touching test:

```zig
test "x" {
    var tmp = std.testing.tmpDir(.{});
    defer tmp.cleanup();
    const io = std.testing.io;

    try tmp.dir.writeFile(io, .{ .sub_path = "f.txt", .data = "hi" });
    const result = try tmp.dir.readFileAlloc(io, "f.txt", std.testing.allocator, .limited(64));
    defer std.testing.allocator.free(result);
}
```

## Local zig toolchain pin

The system `zig` (`/opt/homebrew/bin/zig`, via `which zig`) is still 0.15.2 kingdom-wide by
policy (`citadel/core/rules/zig-0.16.md`: "Global `zig` on dev boxes stays 0.15.2 until a realm
has actually migrated and gone green"). strata migrated in cycle 4 (PR #7), so every cycle since
must prepend the pinned 0.16.0 toolchain before any `zig` command: `export
PATH=/Users/fn/.zr/toolchains/zig/0.16.0:$PATH` — the bare `zig build`/`zig build test` on PATH
will silently run under 0.15.2 and give misleading local results (CI already resolves 0.16.0
correctly via `mlugg/setup-zig@v2` from `build.zig.zon`, so this only affects local dev).

## Error set per module

Define `pub const Error = error{ ... }` at module top; public functions return `Error!T` or a
narrow union of it.

## Line-length audits: count code points, not bytes

`tools/tidy.zig`'s line-length check correctly measures Unicode **code points**, not bytes
(doc comment: "at most 100 Unicode code points"). A shell one-liner like `awk '{print
length}'` or naive `wc -L` counts bytes, so a line with any multi-byte UTF-8 character (e.g.
an em dash `—`, 3 bytes/1 code point) will overcount and produce a false positive. Always
verify a suspected line-length violation by rerunning the actual `zig build tidy` (or the
compiled `tidy` binary), not a shell/grep byte count — confirmed 2026-09-09 (cycle 5) when a
tidy-auditor subagent flagged `src/lsm.zig:1` as 101 cols; the real tool measured 99.
