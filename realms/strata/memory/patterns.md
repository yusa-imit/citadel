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

## Test with temporary directory

```zig
test "x" {
    var tmp = std.testing.tmpDir(.{});
    defer tmp.cleanup();
    const path = try tmp.dir.realpathAlloc(std.testing.allocator, ".");
    defer std.testing.allocator.free(path);
}
```

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
