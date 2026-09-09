# sigil — patterns

_(migrated from the repo's former `.claude/memory/patterns.md`)_

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

## 0.16 migration: probe both toolchains, don't trust the plan's checklist boundaries

`std.process.Init` (0.16) and `std.process.argsAlloc`/`GeneralPurposeAllocator` (0.15.2) are
mutually exclusive — one toolchain's std lacks the other's symbol entirely, so a source file
using either shape hard-fails to compile on the other toolchain (not just a runtime mismatch).
Before assuming a plan's checklist items are independently mergeable, probe: does `zig build`
(the *install* step, not just `zig build test`) already pass clean on the target toolchain for
every other file? If yes, an item that touches the one remaining broken file may require
pulling forward a "later" item's prerequisite (here, item 8's `minimum_zig_version`/CI bump)
into the same PR — CI cannot go green otherwise, and kingdom rules never allow merging red CI.
`zig build test` alone can be a false-green signal here: it doesn't build/link the actual
`main()` entry point unless something references it, so it can pass while `zig build` fails.

## tidy: reuse the `// proof:` escape hatch for any new heuristic ban/check

A line- or block-based lint check (substring ban, brace-matched block scan) is a heuristic, not
a compiler — it will eventually misfire on a legitimate case the author didn't anticipate (e.g.
`checkErrorCanceledProng` flagging a `switch (err)` over a parser's own non-I/O error set, which
never carries `error.Canceled`). Every such check needs an escape hatch or it becomes permanent
friction. Don't invent a new comment convention per check — reuse `hasProof` (a `// proof:`
comment on the flagged line or the line above), the same mechanism `catch_unreachable` already
uses. One convention, one thing for a future author to remember. Caught in code review, cycle 7,
plan 001 item 6 (`tools/tidy.zig`).

## Error set per module

Define `pub const Error = error{ ... }` at module top; public functions return `Error!T`
or a narrow union of it. Every one of the 10 current stub modules already follows this —
keep it when replacing `error{NotImplemented}` with real error variants.
