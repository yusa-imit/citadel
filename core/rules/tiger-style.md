---
paths:
  - "**/*.zig"
  - "**/build.zig"
  - "**/build.zig.zon"
---

# Tiger Style

Design goals, in order: **safety**, then **performance**, then **developer experience**. All
three matter; the ordering is what settles arguments. Simplicity is not a fourth goal — it is
how the three are met at once, and it is the hardest revision, not the first attempt.

**Assert programmer error, return operating error.** A caller's contract violation — an index
past length, overlapping slices, `read` before `open`, an incoherent options struct — is
asserted and documented as a precondition. The data the library exists to process — malformed
JSON, a truncated file, a resized terminal — is a typed error, returned, never asserted. A
library that panics on user data has misapplied Tiger Style; one that asserts nothing about its
callers continues silently with corrupt state.

Testing: `testing.md`. Layering and dependencies: `00-kingdom.md`. Commits and PRs:
`git-github.md`. Docs: `docs.md`. This file is the code law.

## 1. Safety

1. **Assert every argument, return value, precondition, postcondition, and invariant, averaging
   at least two assertions per function.** Assertions detect programmer error; they downgrade a
   correctness bug into a crash, and each one is a tripwire a fuzzer can trip.
1b. **Two kinds of checks.** `assert` is a programmer-error tripwire and is compiled out in
   ReleaseFast/ReleaseSmall; an invariant that must hold in a shipped build (checksum before write,
   page bounds, quorum math) uses `assert_always` — a check that unconditionally returns an error
   or panics, defined once per repo in `src/stdx.zig`. Never protect user data with plain
   `assert` alone. Libraries recommend ReleaseSafe and never `@setRuntimeSafety(false)` without a
   benchmark.

2. **Assert each property on at least two different code paths.** One assertion proves only that
   one path is self-consistent; two independent derivations form an airlock, so a refactor that
   breaks the invariant on one side is caught on the other.
   ```zig
   assert(!self.opened);
   defer assert(self.opened);
   ```
3. **Assert the positive space you expect and the negative space you do not.** Bugs cluster at
   the boundary, and asserting only the expected leaves the whole complement unchecked.
4. **Split compound assertions and compound conditions.** The split form says which half failed,
   and nesting `if/else` instead of chaining `else if` exposes the missing branch.
   ```zig
   assert(a);
   assert(b); // Not assert(a and b).
   if (a) assert(b); // A single-line if asserts an implication.
   ```
5. **Comptime-assert constant relationships, type sizes, and layout.** Free at runtime, fails at
   build time rather than in a user's deployment, and documents the design constraint.
   ```zig
   comptime assert(@sizeOf(Header) == 64);
   comptime assert(no_padding(Header)); // Anything hashed, written, or sent.
   comptime assert(capacity > 0 and math.isPowerOfTwo(capacity)); // User comptime config.
   ```
6. **Write `maybe(input.len == 0);` where a condition is legitimately sometimes true.** (`maybe`
   is a one-line no-op each repo defines in `src/stdx.zig`: `pub fn maybe(ok: bool) void {
   _ = ok; }` — until zuda ships it.) `assert`
   documents *always*, `maybe` documents *sometimes*; together they mean silence no longer reads
   as "nobody thought about it", and the next reader will not add a wrong `assert`.
7. **Put a limit on everything, named `*_max`.** Every loop, queue, retry count, nesting depth,
   token length, and capacity gets a fixed upper bound, because in reality everything has one;
   unbounded loops become hangs, unbounded queues become memory exhaustion, and components that
   honour each other's limits get backpressure for free. `while (true)` is banned outside a
   top-level event loop, where non-termination is asserted; elsewhere `for (0..iterations_max)`.
8. **Do not use recursion; use an explicit bounded stack** — a fixed array plus a length
   (`var frames: [nesting_max]Frame = undefined; var depth: u32 = 0;` with `assert(depth <
   nesting_max)` on push); `std.BoundedArray` is gone in 0.16 and zuda's `BoundedArrayType` is
   the shared home once it exists. Recursion hides an input-dependent
   bound inside the machine stack, where it can be neither asserted nor fuzzed, and turns a data
   bug into stack overflow under hostile input. Comptime type-level recursion is exempt.
9. **Allocate at `init` from explicit limits; never store an allocator for later growth.** Take
   `gpa: Allocator` plus the limits in `init`, allocate the worst case there, and guarantee that
   no method allocates afterwards — state that contract in the `//!` header and test it with a
   failing allocator. Where the bound genuinely cannot be known, take the caller's buffer and
   return `error.OutOfSpace`; the caller is the only one who knows the bound.
   ```zig
   pub fn init(target: *Parser, gpa: Allocator, options: Options) !void
   pub fn parse(input: []const u8, scratch: []u8) error{ OutOfSpace, InvalidSyntax }!Value
   ```
10. **Use explicitly-sized types and show division intent.** We compile for targets we never test
    (wasm32, 32-bit ARM), and `usize` in a public struct or a wire format silently differs across
    them; a bare `/` on integers hides whether you meant to round.
    ```zig
    const blocks: u32 = @divExact(bytes_len, block_size); // Or @divFloor / div_ceil.
    const offset = 1 + (index << 3); // Never mix bitwise and arithmetic unparenthesized.
    ```
11. **Handle every error with an exhaustive `switch`, and declare explicit error sets.** 92% of
    catastrophic failures in data-intensive systems come from mishandling errors the software
    itself signalled. `== error.X` upcasts to `anyerror` and deletes exhaustiveness, so a new
    variant falls through silently instead of failing the build. Never return `anyerror` from a
    `pub fn`; `catch unreachable` and `catch {}` each need a comment proving impossibility.
    ```zig
    const value = parse(input) catch |err| switch (err) {
        error.InvalidSyntax => return .invalid,
        error.OutOfSpace => return err,
    };
    ```
12. **Never leave memory `undefined` in anything hashed, checksummed, compared, written, or
    sent.** Uninitialized padding leaks whatever was there (Heartbleed) and makes checksums
    non-deterministic. `@memset(buf, 0)` before a partial fill; assert the type has no padding.
13. **Use only a minimum of excellent abstractions.** They are never zero cost and every seam is
    a chance to be wrong. One comptime parameterization is excellent; three stacked ones leak.
    Name the second implementation or delete the interface — a test double counts, because that
    seam is exactly what makes deterministic testing possible.
14. **Run at your own pace; do not react directly to external events.** Expose `tick()`/`poll()`
    and let the caller decide when work happens, instead of invoking user callbacks from inside
    an I/O completion: control flow stays yours, work per interval stays bounded, and the clock
    becomes an argument. Inject clock, PRNG, allocator, and `Io`; never reach for `std.time.*`,
    `std.crypto.random`, or a global allocator. A function runs to completion without suspending
    — split at the suspension point into `x` / `x_callback` and re-assert there.
15. **Pass options explicitly at every call site; never rely on defaults.** A default you did not
    write down is a decision nobody reviewed, and it changes under you when the callee changes.
    As an author, omit defaults for anything safety- or performance-relevant so users must
    choose; defaults are acceptable only in test fixtures.

## 2. Performance

1. **Sketch before you implement.** Back-of-the-envelope numbers for the four resources (network,
   disk, memory, CPU) against bandwidth and latency. The 1000x wins are available only in design,
   exactly when you cannot profile yet. Put the sketch — bytes touched, allocations, syscalls,
   cache lines per operation — in the module doc, so a benchmark step can falsify it.
2. **Optimize the slowest resource first, weighted by frequency.** Network, disk, memory, CPU —
   but the ranking is latency times frequency, not latency. A cache miss can cost as much as an
   fsync when it happens ten thousand times more often. For a pure-CPU library the order
   collapses to memory then CPU: count cache lines touched, not instructions.
3. **Separate the control plane from the data plane with batching.** One low-frequency control
   decision amortized over thousands of data items is what buys aggressive assertions *and* speed
   instead of trading them. Give every hot operation a plural form (`write_all(cells)`,
   `get_many(keys)`), assert heavily at the batch boundary, keep the per-item loop lean and
   bounded, and neither copy nor serialize in the data plane: view the caller's buffer.
4. **Be explicit in hot loops.** Extract the hot kernel into a free function over primitives —
   `fn encode(input: []const u8, output: []u8) u32` — with no `self`, so the compiler need not
   prove it can keep fields in registers, and so the kernel is independently testable, fuzzable,
   and benchmarkable. Fixed-size structs, aligned to their largest field.

## 3. Developer experience

1. **70 lines per function, 100 columns per line, 4 spaces, `zig fmt`.** Both limits are
   physical: a function that fits on one screen, a line narrow enough to show two copies of the
   code side by side. Braces on every `if` that does not fit on one line. The cap is hard for
   every function; existing offenders live in a checked-in `tidy_baseline.txt`
   (`path:function:lines`) that may only shrink — a listed function that grows, or a new long
   function, fails `tidy`. Reference: `citadel/templates/tidy/`.
2. **Push `if`s up and `for`s down.** The parent owns every `switch` and `if`; helpers take
   resolved primitives and return values the parent applies, rather than mutating `self`.
   Branching smeared across a call chain makes the state machine invisible; concentrated, it is
   one readable place, and the pure leaves are trivially testable.
3. **Declare variables at the smallest possible scope, and do not alias them.** Most bugs are a
   semantic gap opened by distance in time or space between a check and its use. One cursor,
   never a shadow copy; recompute `items.len` rather than caching it across a mutation.
4. **Initialize large structs in place through an out pointer.** `fn init(target: *T, ...) !void`
   removes copy-moves and stack growth, lets the caller decide where the object lives, and is
   required for any type with self-references or registered callbacks. In-place init is viral
   through the container. Pass arguments over 16 bytes as `*const`.
5. **Reduce dimensionality at the call site:** `void` > `bool` > `u64` > `?u64` > `!u64`, because
   every branch you force on the caller is viral up the whole chain. For each `?` and `!` in a
   public signature, ask whether an asserted precondition removes the case. Public surface is
   permanent from v0; keep it enumerable on one screen.
6. **`snake_case` for functions, variables, and files — including files that define a type.** No
   abbreviations (one saved today is read a million times), long-form flags (`--force`), and
   properly capitalized acronyms (`VSRState`, not `VsrState`).
7. **Units and qualifiers last, sorted by descending significance:** `latency_ms_max`, never
   `max_latency_ms`, so `latency_ms_min` sorts beside it and options structs group by subject.
   Give related names equal length (`source`/`target`, not `src`/`dest`) so derived identifiers
   line up in slices and arithmetic.
8. **Name allocators by discipline: `gpa`, `arena`, `scratch` — not `allocator`.** The name tells
   the caller who calls `deinit`; that is the ownership contract written into the signature.
9. **A function returning a `type` is `CamelCase` and ends in `Type`.** `RingBufferType(u8, 64)`
   is then instantly distinguishable from the type `RingBuffer` at every call site.
10. **Never write `const Self = @This();`** — use the real name, `const Tracer = @This();`, which
    reads better at call sites and in compiler error messages.
11. **Order a file top-down: entry point first, then fields, then types, then methods.** A reader
    should stop after twenty lines knowing what the module does. Imports at the bottom; a
    complex nested type becomes a top-level struct; absent a right order, sort alphabetically.
12. **Treat `index`, `count`, and `size` as distinct types.** Index to count adds one; count to
    size multiplies by the unit. The type system will not catch `u32` against `u32`, so every
    numeric parameter carries `_index`, `_count`, `_size`, `_offset`, or a unit, and the doc
    comment says whether a range is inclusive or exclusive.
13. **Follow every `defer` with a blank line, and group each acquisition with its release.**
    Leaks are found by eye, scanning for an acquire with no matching release; the whitespace
    makes the pair visually atomic. Every `alloc`/`open` in `init` gets an adjacent `errdefer`.
14. **Say why.** Rationale is the only part of a decision unrecoverable from the code, and it
    hands the reader criteria to judge it. Comments are sentences: space after the slashes,
    capital, full stop. Every file opens with a `//!` header stating purpose, invariants, and the
    allocation and ownership contract; every `pub fn` states its preconditions in `///`.
15. **Show call history and disambiguate arguments.** A helper is prefixed with its caller
    (`read_sector` / `read_sector_callback`); callbacks go last, mirroring control flow; two
    same-typed scalars become an `options: struct` (a swap bug the type system cannot catch, and
    a new field stays non-breaking). Unique dependency types stay positional, general to specific.
16. **Zero technical debt.** Fix the showstopper; do not file it. Ask "what could go wrong?"
    rather than "what's wrong?" — code, like steel, is cheapest to change while hot, and a
    library's debt is paid by every consumer. No `FIXME`, no debug print, no dead declaration, no
    `@panic("TODO")` in a merged commit. We ship fewer features; all of them meet the goals.

## 4. Library adaptation

Roughly 85% of Tiger Style transfers to an allocator-first Zig library unchanged. Five deltas:

1. **Static allocation becomes allocator-first with a documented no-allocation contract.** A
   library cannot derive worst-case counts from CLI arguments, because it does not own the
   process. Allocate the worst case in `init` from caller-supplied limits, guarantee no method
   allocates after that, and push genuinely unknowable bounds to the caller as a `scratch: []u8`
   plus `error.OutOfSpace`. The spirit survives: every limit is still visible in a signature.
2. **"No recursion" is the rule libraries break most and need most.** Parsers, layout engines,
   and trees beg for it, and a library's input is entirely user- or attacker-controlled. An
   explicit bounded stack makes the depth limit documented, assertable, and fuzzable, and removes
   stack overflow under load — the worst failure a library can hand its user.
3. **Interface discipline is release-blocking, not merely good practice.** A service can refactor
   a seam any Tuesday; a public signature is permanent from v0. Dimensionality, options structs,
   explicit error sets, and minimal surface area become blocking review items; conversely a
   service may lean on internal assertions where a library must guarantee.
4. **The assert-versus-return line is sharper.** Garbage *state* asserts; garbage *data* returns.
   Wrong in one direction you crash your user's process over their input; wrong in the other you
   continue with corrupt internal state.
5. **The simulator becomes a model-based seeded test, and the fakes ship.** Drive a seeded
   operation stream into the structure and a trivially-correct reference, compare after every
   step, inject faults through the seams (failing allocator, short reads, torn writes), and
   reproduce from `(seed, commit)`. Export the fakes and fixtures as a public `testing`
   sub-module so users get deterministic tests too — a feature, not scaffolding.

Stricter for libraries than the original text implies: zero dependencies (yours become your
users' transitively, and they cannot opt out), explicitly-sized types, building in all four
optimization modes (your user picks the mode), and `///` discipline (it is the whole contract).

## 5. Mechanical checks

A reviewer runs these by hand; a `tidy` test runs them in CI, alongside dead declarations, dead
files, untracked imports, and `defer` newlines. Every hit is a finding until a comment says why.

| Pattern (over `src/`) | Flags | Replacement |
|---|---|---|
| `assert(.* and .*)` | compound assertion | `assert(a); assert(b);` |
| `== error.` / `!= error.` | silent `anyerror` upcast | exhaustive `switch (err)` |
| `anyerror` in a `pub fn` | unswitchable public error | explicit error set |
| `catch unreachable` / `catch {}` | unproven impossibility | typed error, or a proof comment |
| `@panic(` in a library | panic on user data | typed error returned to the caller |
| `while (true)` | unbounded loop | `for (0..iterations_max)`, or the event loop |
| `std.debug.print` / `dbg(` / `FIXME` | debug leftovers | delete before merge |
| `std.time.` / `std.crypto.random` | hidden non-determinism | injected clock, PRNG, `Io` |
| `: usize` in a public, serialized or wire struct | width varies | `u32`/`u64`; `usize` only at std slice boundaries |
| bare `/` on integers | unstated rounding | `@divExact` / `@divFloor` / `div_ceil` |
| `= undefined` | uninitialized bytes | complete init, or `@memset(buf, 0)` |
| `Self = @This()` | anonymous type alias | `const Tracer = @This();` |
| `debug.assert(` / `usingnamespace` | banned spellings | `const assert = std.debug.assert;` once per file, then `assert(` |
| `.{}` at a call site (not fixtures) | implicit defaults | spell out every option |
| `allocator:` as a parameter name | undeclared discipline | `gpa:` / `arena:` / `scratch:` |
| `max_` / `min_` / `total_` prefix | little-endian naming | suffix: `latency_ms_max` |
| `fn [A-Z]` not ending in `Type` | type function misnamed | `RingBufferType` |
| `*.zig` filename with `[A-Z]` | CamelCase filename | `snake_case` |
| first line is not `//!` | module states no contract | add the `//!` header |
| `alloc`/`append` outside `init` | allocation after init | pre-allocate, or `error.OutOfSpace` |
| `setRuntimeSafety(false)` | safety off without evidence | benchmark and comment, or revert |
| line > 100 chars, function > 70 lines | limits | split; old offenders only via a shrinking baseline |

Stronger than grep: run the suite under a `FailingAllocator` past `init` to prove the
no-allocation contract, and run one seed twice diffing byte-for-byte to prove determinism.

## 6. What we deliberately do not adopt

- **Byte-identical replicas and physical determinism.** Cluster-shaped. We require *logical*
  determinism (same input, same result, reproducible from a seed) and byte-stable serialization;
  we do not require two processes to produce identical data files.
- **"Assertions stay on in ReleaseFast."** A library cannot make that call for its user. We keep
  assertions on in `ReleaseSafe`, recommend `ReleaseSafe` to consumers, test all four modes, and
  never `@setRuntimeSafety(false)` without a benchmark and a comment. The binary owner — a
  service or `zr` — chooses its own mode, and records that choice in its `REALM.md`.
- **Worst-case static allocation derived from CLI arguments.** Only a binary knows its process's
  bounds; libraries take limits at `init`, so the limit still exists, visible in a signature.
