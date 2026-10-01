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
