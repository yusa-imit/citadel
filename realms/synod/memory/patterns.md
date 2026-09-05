# synod — patterns

_(migrated from the repo's former .claude/memory; keep under 200 lines)_

## vtable interface

Used for `interfaces.zig` (Transport/LogStore/StateMachine/Clock/Rng) and anywhere else a
core module needs an injected dependency instead of a concrete type.

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

Define `pub const Error = error{ ... }` at module top; public functions return `Error!T` or
a narrow union of it. (Consistent with the kingdom-wide rule of declaring explicit error sets
and switching on them exhaustively — see `citadel/core/rules/tiger-style.md`.)
