//! Kingdom standard extras: assertion vocabulary and a bounded stack. Every repo carries this
//! file until zuda ships the shared versions (citadel/core/rules/tiger-style.md §1).
//!
//! Invariants: `assert` is a programmer-error tripwire (compiled out in ReleaseFast/Small);
//! `assert_always` guards data that must hold in shipped builds; `maybe` documents a condition
//! that is legitimately sometimes true.

const std = @import("std");

/// Programmer-error tripwire. Same as `std.debug.assert`; use this spelling everywhere.
pub const assert = std.debug.assert;

/// Invariant that must hold in every build mode. Returns an error instead of being compiled out.
pub fn assert_always(ok: bool) error{InvariantViolated}!void {
    if (!ok) return error.InvariantViolated;
}

/// The dual of `assert`: documents that `ok` is sometimes true and sometimes false.
pub fn maybe(ok: bool) void {
    _ = ok;
}

/// Fixed-capacity stack, the replacement for recursion (Tiger Style §1.8).
pub fn BoundedStackType(comptime T: type, comptime capacity_max: u32) type {
    return struct {
        items: [capacity_max]T = undefined,
        len: u32 = 0,

        const Stack = @This();

        /// Time: O(1). Fails instead of growing.
        pub fn push(stack: *Stack, item: T) error{StackFull}!void {
            assert(stack.len <= capacity_max);
            if (stack.len == capacity_max) return error.StackFull;
            stack.items[stack.len] = item;
            stack.len += 1;
        }

        /// Time: O(1). Returns null when empty.
        pub fn pop(stack: *Stack) ?T {
            assert(stack.len <= capacity_max);
            if (stack.len == 0) return null;
            stack.len -= 1;
            return stack.items[stack.len];
        }

        pub fn is_empty(stack: *const Stack) bool {
            return stack.len == 0;
        }
    };
}

test "stdx: bounded stack push/pop respects capacity" {
    var stack: BoundedStackType(u8, 2) = .{};
    try stack.push(1);
    try stack.push(2);
    try std.testing.expectError(error.StackFull, stack.push(3));
    try std.testing.expectEqual(@as(?u8, 2), stack.pop());
    try std.testing.expectEqual(@as(?u8, 1), stack.pop());
    try std.testing.expectEqual(@as(?u8, null), stack.pop());
    try std.testing.expect(stack.is_empty());
}

test "stdx: assert_always returns an error instead of vanishing" {
    try assert_always(true);
    try std.testing.expectError(error.InvariantViolated, assert_always(false));
    maybe(true);
}
