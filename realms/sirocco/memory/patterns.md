# sirocco — patterns

_(migrated from the repo's former `.claude/memory/patterns.md`; keep under 200 lines)_

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

Note: under Zig 0.16, `std.testing.tmpDir`'s options type changes from
`fs.Dir.OpenDirOptions` to `Io.Dir.OpenOptions` — update this pattern when sirocco migrates
(see `citadel/core/rules/zig-0.16.md`).

## Error set per module

Define `pub const Error = error{ ... }` at module top; public functions return `Error!T` or
a narrow union of it.

## Zig 0.15.x gotchas (until migrated to 0.16 under plan 001)

Carried from the old `CLAUDE.md`; these are current-toolchain (0.15.2) facts, not kingdom
policy — superseded by `citadel/core/rules/zig-0.16.md` once sirocco's `001` plan lands.

- `std.ArrayList(T)` is unmanaged: initialize with `.empty`, pass the allocator to every
  mutating method.
- `child.wait()` closes the child's stdout — read it before calling `wait()`.
- `callconv(.c)` is lowercase.
- Flush buffered writers before calling `std.process.exit()`.
- File-scope `const X = expr;` needs no `comptime` keyword.
