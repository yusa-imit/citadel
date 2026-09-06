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

## Zig version quirk: this machine's 0.15.2 has unmanaged-only ArrayList

`/opt/homebrew/bin/zig` (0.15.2 as actually installed here) ships `std.ArrayList(T)` as
unmanaged-only: no `.init(gpa)`, use `.empty` plus pass `gpa` explicitly per call
(`list.append(gpa, item)`, `list.deinit(gpa)`). This looks like the 0.16 shape but is present
already on 0.15.2 on this box — don't assume managed-style ArrayList compiles pre-migration;
check before writing runtime string-building code (`tools/tidy.zig`, cycle 2, hit this).

## `tools/` is a build tool, not library `src/` core

The "no I/O in core" rule (`REALM.md`) applies to `src/`, not `tools/*.zig` (tidy, and any
future codegen/lint scripts) — those may use `std.fs.cwd()` etc. freely since they run at
build time on the host, never ship in the library, and are not under the Zig 0.16 `io: Io`
convention either (that's a `src/` boundary rule). See `tools/tidy.zig` (plan 001 item 2).
