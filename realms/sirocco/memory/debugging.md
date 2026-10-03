# sirocco — debugging

_(migrated from the repo's former `.claude/memory/debugging.md`; keep under 200 lines)_

Format: `## <symptom>` / **Cause** / **Fix** / **How to detect next time**

## Fiber tests SEGV only in an optimized mode on one arch (bug #23, cycle 30)
**Cause**: std's inline-asm `Io.fiber.contextSwitch` is fragile under LLVM: aarch64 inlined it
into a caller holding x29/x30 (cycle 29); x86_64 `-Os` never moved the stack-built message
address into `rsi` (cycle 30). Calling a naked function through a C pointer without
`never_inline` lets LLVM splice its asm body into the caller with no clobber list.
**Fix**: own naked `switch_context_asm` in `src/sched.zig`, `@call(.never_inline)` through a
`callconv(.c)` pointer; no Zig params on the naked fn (self-hosted x86_64 Debug backend TODO).
**Detect**: `zig test src/sched.zig -target x86_64-linux -OReleaseSmall -fno-emit-bin
-femit-asm=.zig-cache/x.s --test-no-exec` and read `switch_context*` and the asm register setup;
count asm bodies (should be one). Run `zig build test -Doptimize=<mode>` for all four modes.

_(Earlier: the first CI run (33944341024) failed before a Linux-only restriction fixed it; the
cause was never written up.)_

## Fiber test "hangs" (cycles 31-32)
**Cause**: not a deadlock: a SEGV at address 0x8 inside a fiber, then Zig's crash handler wedges
(it unwinds on the fiber stack). The trigger was std's stack-trace capture (DebugAllocator on
every alloc) walking past `fiber_main` through a stale return address with fp = 0.
**Fix**: zero return address at fiber entry (aarch64 `mov x30, xzr` in `fiber_entry`; x86_64 zero
word below `Start` in `spawn`), so the unwinder reads ra <= 1 and stops.
**Detect**: run the test binary under a subprocess timeout and read the last `N/M name...` line;
add `std.debug.print` probes in `task_entry`/`task_finish` (lldb cannot attach here).
