# zuda — debugging

_(migrated + condensed from the repo's former `.claude/memory/debugging.md`, 2026-09-05; full
narrative for each fix lives in the zuda repo's git history under that file's old path)_

## Known Zig 0.15.x gotchas (until the 0.16 migration lands, see `REALM.md`)
- `std.ArrayList(T){}` not `.init(allocator)` -- unmanaged API.
- `std.Thread.sleep(ns)` not `std.time.sleep`.
- `child.wait()` closes stdout -- read stdout BEFORE `wait()`.
- `callconv(.c)` lowercase in 0.15.
- Buffered writers: flush before `std.process.exit()`.
- File-scope: `const X = expr;` (no `comptime` keyword -- redundant error).
- `zig build test` uses the `--listen=-` protocol -- NEVER use `stdout()` in test code.
- **`std.atomic.fence()` removed** (issue #7, fixed 44bf1f6): replace with stronger memory
  ordering on atomic ops (`.seq_cst`); for lock-free structures, upgrade `.acquire`/`.release`
  to `.seq_cst` where a fence was used; alternative: a dummy atomic RMW with `.seq_cst`.
- **Generic functions can't be comptime params** (issue #8, fixed 44bf1f6): a
  `fn hash(ctx: Context, key: anytype)` can't be passed as `comptime hashFn: fn(Context, K) u64`
  -- create a concrete wrapper inside the factory function with a known `K` type (move the
  `AutoContext` struct INSIDE the `Auto*` factory, not as a top-level export).
- **128-bit atomics NOT universally supported** (fixed e67fe1b):
  `std.atomic.Value(u128)` requires CMPXCHG16B (x86-64) or CASP (ARM64). NOT supported on
  Windows (max 64-bit), WASM (max 32-bit), Linux (not guaranteed). Supported on macOS
  x86-64/ARM64 (Apple enforces the CPU requirement). Error symptom: "expected 64-bit integer
  type or smaller; found 128-bit integer type". Fix: comptime-restrict to macOS-only, or
  rewrite using two separate atomics. Affected: `LockFreeStack`, `LockFreeQueue` (now
  macOS-only). Portable alternative: `WorkStealingDeque` (uses `usize` atomics).

## f32-underflow epsilon bug class (full audit, session 770)
`1e-300` as a literal, compared or used at `T = f32`, underflows to exact `0.0` at compile
time (f32's smallest subnormal is ~1.4e-45). This silently breaks several distinct idioms in
`distributions.zig`, first found as the PolyaAeppli `quantile()`/`entropy()` O(MAX_K^2) hang
(session 767, fixed 524ead7): a truncated-series convergence check `if (p < 1e-300) break;`
became `if (p < 0.0) break;` -- never true for a non-negative PMF -- so the loop ran the full
`MAX_K = 50000` iterations at O(k) each, ~2.5 billion ops.

18 `1e-300` sites audited this session, four idioms found broken:
- **`x < 1e-300` break checks** in unbounded-but-capped loops: becomes `x < 0.0`, never true.
  Fixed in `Borel.entropy()`, `GeneralizedPoisson.entropy()` -- now `if (p == 0.0) break`.
- **`x < 1e-300` division guards** (e.g. `ExponentiatedWeibull.hMode()`): vacuous for f32.
  Fixed -- now `if (g == 0.0) return ...`.
- **`x == 0.0 ? 1e-300 : x` zero-replacement** before `@log(x)` (Box-Muller sampling in
  `LogitNormal.sample()`, `ExponentialModifiedGaussian.sample()`): the replacement itself
  underflows to `0.0` in f32. Fixed -- use `std.math.floatMin(T)` instead.
- **`@max(x, 1e-300)` clamp** before `@log(x)` (`gigLogBesselK`, used by
  `GeneralizedInverseGaussian`/`NormalInverseGaussian`): same issue. Fixed -- `@max(x,
  std.math.floatMin(T))`.
- **Safe, left unchanged**: `x > 1e-300` guards (underflowing to `x > 0.0` still correctly
  excludes the one bad case `x == 0`), and break checks inside loops with a small fixed bound
  (<= ~500 iterations) where a vacuous check just runs to the bound instead of exiting early.

**Generalizable lesson**: never use a hardcoded absolute epsilon literal (`1e-300`, `1e-15`,
...) to detect "this float value has become negligible" when the code is generic over float
type `T` -- for narrower types the literal can underflow to `0.0` at compile time and
silently disable the check. Use `== 0.0` for "has this series converged to nothing", or a
tolerance relative to another value of the same type for "are these close". `mode()` was
already safe in this file because its tolerance (`best_pmf * 1e-12`) is relative, not
absolute. **Two sites remain unfixed** as of this survey (~lines 71325, 81533 of
`distributions.zig`) -- flagged for a future stabilization audit, not currently exercised by
f32 test coverage so no live bug, but latent.

Verification method worth repeating: don't just reason about whether an f32 path is broken --
compile and run it (a throwaway `zig run` snippet confirming `@as(f32, 1e-300) == 0.0`, then a
harness exercising the fixed paths at `T = f32` for 200k samples each, checking 0 NaN/Inf).

## Verified formulas (recompute, don't trust memory)
- **YuleSimon variance** = `rho^2 / ((rho-1)^2 * (rho-2))`; entropy at rho=1 ~= 2.026 nats.
  Wikipedia sometimes lists `rho^2*(rho+1)/((rho-1)^2*(rho-2))`, which is wrong. For rho=3 the
  correct value is 2.25, not 9.0 -- verified via partial-fraction decomposition of
  `E[X^2] = sum 18k/((k+3)(k+2)(k+1))`, which telescopes to a finite constant.
- **Binomial-family `logFactorial` precision cliff at n>=20**: exact for `n<20`, then
  Stirling (`n*log(n)-n+0.5*log(2*pi*n)`), accurate to only ~4e-3 in log-space right at the
  boundary. Any Binomial-derived distribution with `n>=20` fails a tight (`1e-12`)
  normalization test for reasons unrelated to its own formula -- keep new tests under n=20,
  or loosen tolerance. Raising the exact-computation cutoff is a real, cross-cutting fix, not
  yet done (see `context.md` standing backlog).
- **Gamma sampler for shape<1** (Ahrens-Dieter): must be `G * U^(1/alpha)`, not
  `xi * U^(1/alpha)` -- a real bug found and fixed at session 680.

## Structural bugs, condensed
- **SuffixTree edge splitting** (issue #1, fixed d17ca50): pattern search exhausted exactly
  at `j == edge.label.len` must move `node` to `edge.target` (else `collectLeaves()` reads
  the wrong subtree); LRS detection must also count nodes with `suffix_index != null` AND
  `children.count() >= 1`, not only `children.count() >= 2`. Lesson: in compressed suffix
  trees, pattern search must explicitly handle all three cases (continues / ends mid-edge /
  ends at boundary).
- **FibonacciHeap self-referential pointer** (fixed 6485859): `Node.init()` returns a
  stack-allocated struct with `node.prev = &node`; after `node.* = Node.init(value)` onto a
  heap allocation, `prev`/`next` still point at the stack copy. Fix: re-point
  `node.prev = node; node.next = node;` immediately after the heap copy. Lesson: a struct
  initializer with self-referential pointers must be re-pointed after copying to the heap.
- **Push-Relabel infinite loop** (fixed 02a920b): without a height bound, vertices that can't
  reach the sink relabel forever. Fix: `max_height = 2 * vertex_count` (2V is the theoretical
  bound); skip a vertex once its height reaches that bound.
- **CI timeout from excessive test compilation** (issue #3, fixed fd8a3cf): `main.zig`
  importing `zuda` forced semantic analysis of all 195 imports for the demo exe, and
  `root.zig`'s test block manually referenced 80+ types. Fix: drop the unused import in
  `main.zig`, rely on `std.testing.refAllDecls(@This())` alone in `root.zig`. Build time
  30min+ (timeout) -> under 3min. Lesson: don't import the whole library into a binary that
  doesn't use it, and `refAllDecls` is sufficient -- no manual reference list.
- **`@panic` in library code** (session 570, 2026-05-24): 4 sites (bitonicsort non-power-of-2,
  bogosort getrandom failure, subsets k>n or n>63, random.zig lambda<=0) converted to typed
  errors. Also found dead code: `subsets.zig` checked `n > 63` but the param is `u6` (max 63),
  so the branch was unreachable -- removed.

## Performance (open)
- **RedBlackTree below target** (identified 2026-03-14, commit 232f2ad, still open): insert
  269 ns/op vs a 200 ns/op target (+34.5%), lookup 552 ns/op vs 150 ns/op target (+268%) for
  1M random keys. Suspects: cache locality of random-key traversal, allocator overhead per
  node, rotation frequency, comparator overhead. Next steps if picked up: profile the hot
  path, compare against sequential-key workload to isolate cache effects, consider node
  pooling.

## Resolved code-quality sweeps (don't re-discover as new findings)
- **Allocator-first violations**: all fixed by session 554 (`grep -r
  "std\.heap\.page_allocator" src | grep -v "///"` returns 0; the two remaining hits are a
  doc-comment example and the FFI layer's intentional `c_allocator`).
- **`@panic` sweep**: 0 remaining in `src` as of session 570 (see above).
