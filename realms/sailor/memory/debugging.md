# sailor — debugging

_(migrated + merged from the repo's former .claude/memory/debugging.md and
zig-015-compat.md, 2026-09-05; further compressed from the 2026-07-17 version)_

## Known Zig 0.15.x gotchas

- `std.ArrayList(T){}` not `.init(allocator)` — unmanaged API. Methods need the allocator:
  `list.deinit(allocator)`, `list.append(allocator, item)`, `list.writer(allocator)`.
- `std.Thread.sleep(ns)` not `std.time.sleep`.
- `child.wait()` closes stdout — read stdout BEFORE calling `wait()`.
- `callconv(.c)` is lowercase in 0.15.
- Buffered writers: flush before `std.process.exit()`.
- File-scope: `const X = expr;` — no `comptime` keyword (redundant, errors).
- `zig build test` uses the `--listen=-` protocol — NEVER use `stdout()` in test code.
- Ambiguous type references: use module-level references (`const mod = @This()`) when
  re-exporting types.
- On Windows, `posix.fd_t` is `*anyopaque` (HANDLE), not `i32` — don't treat handles as ints.
- `std.posix.getenv()` doesn't exist on Windows — guard with
  `if (windows) return false; else { getenv() }`, NOT an early return before the call (the
  compiler still analyzes the "unreachable" branch and fails to compile it for Windows targets).
- `@floatFromInt` in struct literals needs explicit `@as(f32, ...)` wrapping.
- Pin macOS ARM64 CI runner to `macos-15` — `macos-latest`→26 broke Zig 0.15.2 linking.
- `builtin.strip` removed → use `builtin.mode != .Debug`.
- `builtin.stack_protector` removed — safety is mode-dependent.
- `builtin.sanitize_c` removed → use `@hasDecl` check.
- `builtin.object_format`: `.pe` removed, use `.coff` for Windows.
- `builtin.target.cpu.arch.ptrBitWidth()` removed → use `@bitSizeOf(usize)`.
- `builtin.dynamic_linker` → now `builtin.target.dynamic_linker.get()`.
- `std.mem.page_size` removed → use a constant or runtime detection.
- `std.mem.Allocator.alignedAlloc(T, comptime alignment: usize, n)` →
  `alignedAlloc(T, alignment: std.mem.Alignment, n)`; use `@enumFromInt(log2_alignment)` to
  convert (e.g. `@enumFromInt(4)` for 16-byte alignment).
- Windows CI checks out the repo with CRLF line endings; any line-length/byte-counting check
  that splits `text` on `'\n'` alone (`std.mem.splitScalar(u8, text, '\n')`) picks up a trailing
  `\r` as part of the line, inflating counts by 1+ byte per line versus a Linux/macOS checkout.
  Hit sailor's own `tidy` line-length checker this way (PR #21, cycle 3): a baseline generated
  on a LF checkout failed on Windows alone. Fix: `std.mem.trimRight(u8, line, "\r")`
  after splitting, before measuring length — applies to any future line-oriented text check.

## Precise formulas / overflow findings (keep verbatim)

- `value * bar_count / (max + 1)` style scaling math on `u64` inputs can genuinely overflow
  (integer-overflow panic, not just UB) when `value` is near `u64::max` — widen to `u128` for
  the multiply/divide rather than clamping `value` first (`sparkline.zig getBarChar`); `u128`
  safely holds the product since the other operand (an on-screen glyph count) is always small.
- `std.math.clamp(val, lo, hi)` does NOT sanitize `NaN` — `NaN < lo` and `NaN > hi` are both
  false, so `NaN` passes through unclamped into a later `@intFromFloat` cast.
- **On this project's pinned Zig 0.15.2**, a *runtime* (not comptime-known) `NaN` fed into
  `@intFromFloat` does **NOT** panic — verified empirically (`@intFromFloat` on a runtime NaN
  silently returns `0`). Only `±Infinity` reliably panics ("integer part of floating point
  value out of bounds"). **Any RED test for this bug class must construct reachability with
  `std.math.inf(T)`/`-std.math.inf(T)`, never `std.math.nan(T)`** — a NaN-based "does not
  panic" test is vacuous on this toolchain (still a real bug: NaN silently produces garbage 0,
  UB per the language reference, not guaranteed stable across versions/targets/opt modes).
- NaN/Infinity audit of 34 chart widgets is complete: 4 confirmed reachable and fixed
  (`box_plot.zig`, `funnel_chart.zig`, `particles.zig`, `metricspanel.zig` — direct
  multiplication of a user value with no intervening clamp). The other 30 are safe via one of
  three patterns, worth recognizing on future audits of this bug class: (1) an explicit
  `@max(lo, @min(x, hi))` clamp sits directly before the cast; (2) the float is purely
  geometric (int-derived area/index/count, bounded trig ∈ [-1,1]) — Infinity has no path in;
  (3) a **self-cancelling pattern** (`waterfall_chart.zig`, `stream_graph.zig`, `sankey.zig`,
  `mosaic_plot.zig`, `icicle_chart.zig`): a running total/max computed in a first pass includes
  the same field a caller could set to Infinity, so a later division's numerator AND
  denominator both become Infinity — `Infinity/Infinity = NaN`, and `@intFromFloat(NaN)`
  doesn't panic per the finding above. Pattern (3) is fragile to refactors that decouple the
  two passes — regression tests exist for all 5 widgets; check this pattern explicitly before
  concluding an unguarded-looking division site is a bug.

## Test-quality anti-patterns (audit every STABILIZATION session)

1. **Weak disjunction**: `<specific_claim> or countNonEmptyCells(...) > N` lets a test pass
   even when the specific claimed behavior never renders, as long as unrelated content occupies
   the area. Fix: assert the specific claim directly; drop the fallback unless the test name
   itself is genuinely generic with no specific claim to check. Swept clean project-wide.
2. **Placeholder `expect(true)`**: literal no-op assertions (e.g. "Placeholder; implementation
   will set style") that always pass regardless of implementation. Detect via
   `grep -rn "expect(true)\|expect(1 == 1)" tests/*.zig`.
3. **Whole-area scans**: geometric/symmetry assertions over the entire `area` (including
   label/border columns) can be satisfied by unrelated content landing there by coincidence.
   Fix: restrict scans to the data-plot sub-rect, or render with labels/block disabled when
   asserting a geometric property of plotted data itself.
4. An "uncommitted but `zig build test` green" widget is NOT evidence its tests are meaningful
   — apply the same weak-assertion scrutiny to newly-found work as to old files.
5. A `pub const` re-export that no `tests/*_test.zig` root ever references means its inline
   tests silently never compile or run, even though overall `zig build test` reports success —
   confirmed 3 separate times (`ConfigEditor` s441, `DonutChart` s380, others). **When a widget
   has substantial inline tests but no cross-referenced `tests/*_test.zig` file, verify
   reachability directly**: append a throwaway `comptime { @compileError("PROBE"); }`, confirm
   it fires under `zig build test`, then remove it — don't trust a green exit code alone.

## Resolved compilation/API migrations (compressed, do not re-investigate)

- Zig 0.15 `ArrayList`/`Thread` API migration: unmanaged `ArrayList`, explicit allocator params,
  `std.Thread.sleep` — see the gotchas list above; all call sites fixed.
- Windows `fd_t`/`getenv` compilation failures: fully resolved, all 6 cross-compile targets
  green.
- UTF-8 byte-vs-codepoint bugs (`Buffer.setString`, menu submenu indicator): iterating
  `for (str) |c|` treats UTF-8 multi-byte sequences as individual bytes — always decode via
  `std.unicode.Utf8View`/`utf8Decode()` for user-facing text.
- A once-reported "test suite hangs" issue never recurred in 280+ sessions after — considered
  stale; re-open only if an actual hang recurs.
