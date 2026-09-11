# sailor — patterns

_(migrated + condensed from the repo's former .claude/memory/patterns.md, 2026-09-05; the
extensive per-widget test-code dumps in the original are summarized, not reproduced — the
underlying widget files and their `tests/*_test.zig` counterparts are the source of truth)_

## Widget testing pattern (TDD)

1. Create the widget struct with a stub `render()`.
2. Write tests covering: init with default config; builder methods (`withX`); pure
   threshold/evaluation functions first; edge cases (zero dimensions, negative values,
   overflow); memory safety (allocator usage, no leaks); rendering (stub first, then assert
   cells once implemented).
3. Run tests — should compile, pass against the stub.
4. Implement `render()` logic until the meaningful assertions pass.

```zig
test "MetricsPanel.evaluateThreshold warning zone" {
    const metric = Metric{
        .name = "Test", .value = 75.0, .max_value = 100.0,
        .thresholds = .{ .warning = 70.0, .critical = 90.0 },
    };
    try std.testing.expectEqual(ThresholdStatus.warning, MetricsPanel.evaluateThreshold(metric));
}
```

## Library output pattern

```zig
// WRONG: direct stdout
std.debug.print("hello\n", .{});

// RIGHT: writer-based
pub fn render(self: Self, writer: anytype) !void {
    try writer.print("hello\n", .{});
}
```

## Test output capture pattern

```zig
test "renders correctly" {
    var buf: [4096]u8 = undefined;
    var stream = std.io.fixedBufferStream(&buf);
    try myModule.render(stream.writer());
    try std.testing.expectEqualStrings("expected output", stream.getWritten());
}
```

## Cross-platform guard pattern

```zig
const builtin = @import("builtin");

pub fn enableRawMode() !RawMode {
    if (comptime builtin.os.tag == .windows) {
        return enableRawModeWindows();
    } else {
        return enableRawModePosix();
    }
}
```

## RAII cleanup pattern

```zig
pub fn init(allocator: Allocator) !Self {
    const buf = try allocator.alloc(Cell, width * height);
    return .{ .allocator = allocator, .cells = buf };
}
pub fn deinit(self: *Self) void {
    self.allocator.free(self.cells);
}
// Caller: var obj = try Thing.init(allocator); defer obj.deinit();
```

## Memory safety patterns

```zig
// GPA leak detection
test "no leaks" {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer {
        const leaked = gpa.deinit();
        testing.expect(leaked == .ok) catch @panic("memory leak detected");
    }
    const allocator = gpa.allocator();
}

// Arena for request-scoped work
var arena = std.heap.ArenaAllocator.init(gpa.allocator());
defer arena.deinit();
const allocator = arena.allocator();

// Error cleanup
const buf = try allocator.alloc(u8, 100);
errdefer allocator.free(buf);
```

## Builder pattern (widget API)

Widgets use a fluent builder pattern: `init` creates the widget with required fields; `withX`
methods take `self` by value, modify a copy, return it, enabling chaining and immutability.

```zig
pub const Menu = struct {
    items: []const MenuItem,
    selected: usize = 0,

    pub fn init(items: []const MenuItem) Menu { return .{ .items = items }; }
    pub fn withSelected(self: Menu, index: usize) Menu {
        var result = self; result.selected = index; return result;
    }
};
// Usage: Menu.init(items).withSelected(1).withBlock(block);
```

## Date arithmetic pattern (Zeller's congruence)

Calendar widgets use Zeller's congruence for day-of-week (keep this formula verbatim):

```zig
// Returns 0=Sunday, 1=Monday, ..., 6=Saturday
pub fn dayOfWeek(self: Date) u3 {
    var m = self.month;
    var y = self.year;
    if (m < 3) { m += 12; y -= 1; } // Jan=13, Feb=14 of prior year
    const q = self.day;
    const k = y % 100; // year of century
    const j = y / 100; // century
    const h = (q + (13 * (m + 1)) / 5 + k + k / 4 + j / 4 - 2 * j) % 7; // 0=Saturday
    const day_val = @as(i8, @intCast(h)) - 1; // convert Zeller (0=Sat) to 0=Sun
    return @intCast(@mod(day_val, 7));
}
```

Valid for the Gregorian calendar (1582+). `@mod(negative_i8, 7)` handles negatives correctly in
Zig (unlike `%`/`rem`) — use `u3` for the 3-bit day-of-week result.

## Calendar grid rendering pattern

```zig
const first_day = Date.init(year, month, 1).dayOfWeek();
const offset = (first_day - first_day_of_week + 7) % 7; // columns before month starts

for (0..6) |week| {
    for (0..7) |dow| {
        const total_cells = week * 7 + dow;
        const day_to_show = total_cells + 1 - offset; // can be < 1 or > days_in_month
        // day_to_show < 1 => previous month; > days_in_month => next month; else current
    }
}
```

Style precedence when rendering a cell: `selected > today > in_range > out_of_bounds > default`.

## Environment variable testing pattern

Zig 0.15.x has no `setenv`/`unsetenv` — bind the C functions directly for test isolation:

```zig
extern "c" fn setenv(key: [*:0]const u8, value: [*:0]const u8, overwrite: c_int) c_int;
extern "c" fn unsetenv(key: [*:0]const u8) c_int;

test "env var with cleanup" {
    _ = setenv("TEST_VAR", "value", 1);
    defer _ = unsetenv("TEST_VAR");
    try std.testing.expectEqualStrings("value", getEnvVar("TEST_VAR"));
}
```

Test both set/unset conditions; for booleans test all true/false spellings plus
case-insensitivity; for integers test overflow/underflow, boundaries, invalid format,
whitespace rejection.

## Widget test coverage shape (reference sizing, not a rule)

Comprehensive widget suites cover: init/memory, builder/config API, listing/sorting or
evaluation logic, navigation/movement, selection/state, rendering (empty/content/wrapped/
offset), edge cases (zero area, invalid input, rapid updates), and search/filter/performance
where relevant. `FileBrowser`, `TerminalWidget` (+ its `AnsiParseState` state machine), and the
env module are representative templates; read the actual test file for current counts.

## Zig 0.16 forward-compat rename pattern (safe to land on 0.15.2 today)

Before assuming a 0.16 rename needs the toolchain switch, check whether the 0.15.2-pinned
stdlib *already* ships the new spelling as an alias alongside the old one — land those now,
verified by `zig build test` + `git stash` diff of pre-existing `zig fmt` failures. Confirmed:
`GeneralPurposeAllocator`→`DebugAllocator`, `Compile.linkLibC()`→`.root_module.link_libc = true`
(PR #26); `ArrayList(Unmanaged) = .{}`→`= .empty` (PR #28 — `.empty` already exists in 0.15.2's
`array_list.zig`; only the default field values on `items`/`capacity` are dropped in 0.16.0).
Renames with **no** 0.15.2-compatible spelling (confirmed absent) — `Io.Mutex`, env access,
`posix.isatty`, `mem.indexOf*`→`find*` (~478 sites) — stay blocked on the toolchain switch;
extend this list when a new class is checked, don't re-derive it. See [[decisions]].

## Verified cross-compile targets

`x86_64`/`aarch64` × `linux-gnu`/`macos`, `x86_64-windows-{gnu,msvc}` — all pass as of the
2026-09-05 survey.
