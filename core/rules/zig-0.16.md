---
paths: ["**/*.zig", "**/build.zig", "**/build.zig.zon", "**/.github/workflows/*.yml"]
---

# Zig 0.16 migration rules

**Status.** Kingdom target: Zig **0.16.0**. Toolchain: `/Users/fn/.zr/toolchains/zig/0.16.0/zig`.
Global `zig` on dev boxes stays **0.15.2** until a realm has actually migrated and gone green —
do not bump a repo's toolchain pin speculatively. Never write new 0.15-only code in any repo
after this file lands: new code should already assume the 0.16 shapes below even before that
repo's own migration lands, so the migration diff stays a rename, not a rewrite.

## The std.Io model, in 12 lines

`std.Io` is a runtime vtable value (`Io = struct { userdata: ?*anyopaque, vtable: *const VTable }`),
not a compile-time trait — anything that can block, race, or need canceling takes an `io: Io`
argument. `std.net`, most of `std.fs`, most of `std.time`, and every `std.Thread` sync primitive
are deleted from those namespaces and reborn as `Io.net`, `Io.Dir`/`Io.File`, `Io.Clock` /
`Io.Timestamp` / `Io.Duration`, and `Io.Mutex` / `Io.Condition` / `Io.Event` / `Io.Group` /
`Io.Queue` respectively — all dispatched through the same vtable. `io.async(fn, args)` returns a
`Future` and only promises completion (may run inline); `io.concurrent(fn, args)` demands real
concurrency or `error.ConcurrencyUnavailable`. `Io.Group` is the spawn-N-await-all idiom;
`Io.failing` is a fully-stubbed reference `Io` (great as a test double or vtable skeleton).
Cancelation is a first-class, refusable protocol: `error.Canceled` (one `l`) rides in almost
every I/O error set now. Ship code takes `Io.Threaded` (feature-complete, thread-pool-backed) —
`Io.Evented` (io_uring/kqueue/GCD) is experimental and has no networking yet. `main` becomes
`pub fn main(init: std.process.Init) !void`, handing you `init.{gpa, arena, io, environ_map,
preopens, minimal}` pre-built; tests get their `Io` from `std.testing.io`.

## THE KINGDOM CONVENTION for `io: Io`

- `io: Io` is the **first parameter after the receiver** on every public function that touches
  filesystem, network, time, sleep, sync, or process APIs — `fn readAll(self: *T, io: Io, ...)`.
- Leaf/free functions take `io` **per call**; do not stash it just to save a parameter.
- A long-lived owning struct (a connection pool, an `http.Client`-shaped service object) MAY
  cache an `io: Io` field set once at construction — mirror `std.http.Client`'s own pattern.
- Tests use `std.testing.io`, never anything else, and never a helper shared between test and
  non-test code (`std.testing.io` is a `@compileError` outside `builtin.is_test`).
- **Never** use `std.Io.Threaded.global_single_threaded` (if referenced anywhere) or hand-roll
  a package-level "default runtime" in library code — it is a debugging escape hatch only.
- Binaries obtain their `Io` from `init.io` in `main(init: std.process.Init)`. **Libraries never
  construct an `Io`** (no `Io.Threaded.init(...)` inside library code) — the binary chooses the
  implementation at `main` and injects it down; this is the whole point of the interface.

## Mapping: 0.15 → 0.16

Each entry: before → after, then a one-line note. Grep the exact spelling in
`/Users/fn/.zr/toolchains/zig/0.16.0/lib/std` before relying on it verbatim.

- **main/args**: `main() !void` + `argsAlloc(gpa)` → `main(init: process.Init) !void` +
  `init.minimal.args.toSlice(arena)`. `init` also carries `.gpa`, `.arena`, `.io`.
- **Allocators**: `heap.GeneralPurposeAllocator(.{})` → `heap.DebugAllocator(.{})`; a shared
  allocator is `heap.smp_allocator`. `ThreadSafeAllocator` has no replacement — delete the
  wrapper; `ArenaAllocator` is natively lock-free and threadsafe now.
- **fs open/read**: `fs.cwd().openFile(p, .{})` → `Io.Dir.cwd().openFile(io, p, .{})`;
  `file.read(&buf)`/`.write(&buf)` → `file.readStreaming(io, &.{&buf})` /
  `.writeStreaming(io, hdr, &.{buf}, n)` — both are **vectored** (`[]const []u8`).
- **fs misc renames**: `getEndPos`/`setEndPos` → `length`/`setLength`; `makeDir`/`makePath` →
  `createDir`/`createDirPath`; `pread`/`pwrite` → `readPositional`/`writePositional`.
- **time**: `time.Instant.now()`, `.sleep(ns)`, `Timer` → `Io.Clock.awake.now(io)`,
  `io.sleep(.fromMilliseconds(n), .awake)`, `start.untilNow(io)`. `time.zig` keeps only unit
  constants (`ns_per_s`, ...) and `time.epoch` — no clock left there.
- **Thread sync**: `Thread.Mutex/Condition/Semaphore/RwLock/ResetEvent/WaitGroup/Pool` →
  `Io.Mutex/Io.Condition/Io.Semaphore/Io.RwLock/Io.Event/Io.Group`. `std.once` is removed with
  **no replacement** — restructure away from global lazy init, or hand-roll on `std.atomic`.
- **net**: `std.net` does not exist — hard error, not a deprecation. `net.Address.parseIp` →
  `Io.net.IpAddress.parse`; `addr.listen(.{})`/`server.accept()` → `addr.listen(io, .{})` /
  `server.accept(io)`; `Stream.Reader`/`Writer` expose `.interface: *Io.Reader`/`*Io.Writer`.
- **stdout/stderr**: `io.getStdOut().writer()` → `File.stdout().writer(io, &buf)` giving
  `w = &fw.interface`; call `w.print(...)` then **`try w.flush()`** (buffered — easy to forget).
- **ArrayList**: `var l: T = .{};` (bare literal) is now a missing-field error → `var l: T =
  .empty;` or `.initCapacity(gpa, n)`. `.writer()` is removed — build a `*Io.Writer` adapter
  over the list's buffer instead, or append directly.
- **mem search**: `indexOf`/`lastIndexOf`/`indexOfPos`/`indexOfAny` → `find`/`findLast`/
  `findPos`/`findAny`. **Not** a safe blind regex: `indexOfPosLinear`→`findPosLinear`,
  `lastIndexOf`→`findLast` (not `findLastIndex`) — use the mapping list, not `s/indexOf/find/`.
- **format**: custom `pub fn format(...)` now takes `w: *std.Io.Writer`; `fmt.format` and
  `fmt.Formatter` are gone (`Formatter` → `fmt.Alt`); use `Writer.print` to render.
- **@Type**: removed outright → `@Int`/`@Tuple`/`@Pointer`/`@Fn`/`@Struct`/`@Union`/`@Enum`.
  `@intFromFloat(f)` is deprecated in favor of `@trunc(f)` (int result types now allowed there).
- **Cancelation**: any exhaustive `switch (err) { ... }` over an I/O error set now needs an
  `error.Canceled => ...` prong — propagate it, don't swallow with `else => unreachable`.
- **posix**: most mid-level `std.posix.*` convenience wrappers (env access, `isatty`, ...) are
  gone — use the `std.Io`-level equivalent, or drop to `posix.system` directly.
- **http.Client**: now requires an `io: Io` field alongside `.allocator` at construction.
- **crypto.tls.Client**: `init(stream, options)` → `init(reader: *Io.Reader, writer: *Io.Writer,
  options)` — decoupled from any socket type, so it's unit-testable over `Io.Reader.fixed`.
- **build.zig linking**: `exe.linkLibC()`/`exe.linkSystemLibrary("x")` no longer exist on
  `Step.Compile` → set `exe.root_module.link_libc = true` /
  `exe.root_module.linkSystemLibrary("x", .{})` (confirmed: these live on `Module` now).
- **fuzzing**: `testing.fuzz(ctx, testOne, .{})` over raw `[]const u8` → `testOne(ctx, smith:
  *testing.Smith) !void` using `smith.value(T)`/`.bytes()`/`.eos()` — a rewrite, not a rename.
- **testing.tmpDir**: options type changed from `fs.Dir.OpenDirOptions` to `Io.Dir.OpenOptions`.
- **test timeouts**: new `Step.Run.unit_test_timeout_ns` — a hung test now reports as a timeout
  against that test index instead of wedging the whole build; fuzz tests are exempt by default.

## Per-repo error classes (probes: `zig test`/`zig build` against 0.16.0)

| Repo | Errs | Top error classes | Blocked by |
|---|---|---|---|
| sigil | 1 | GPA rename only; rest of lib already clean | — |
| strata | 1 | GPA + `argsAlloc`; lib (11 tests) clean | — |
| synod | 1 | GPA (latent: `argsAlloc`, `fs.File`, `Timer`) | — |
| sirocco | 2 | GPA + `argsAlloc` (latent: stdout writer, `Timer`) | — |
| zuda | 44+1 | `time.*`(21) `ArrayList{}`(18) `fs.cwd`(14) | — |
| sailor | 368 | `std.io`(155) `ArrayList{}`(115) `.writer()`(25) | — |
| silica | 275 | `ArrayList{}`(106) `fs.cwd`(77) `time.*`(23) | sailor, zuda |
| zr | 79 | `ArrayList{}`(31) `fs.cwd/File`(8) `Child.init`(3) | sailor, zuda |
| zoltraak | 3+ | build.zig link fix; then `ArrayList{}`(63) `net`(8) | sailor, zuda |

Counts undercount true breakage (compiler stops each unit at its first error). zoltraak's raw
total also includes ~730 pre-existing broken tests unrelated to 0.16 — excluded above. silica,
zr, and zoltraak get no real `zig build` signal until sailor and zuda fix their own `build.zig`
(`linkLibC`/`linkSystemLibrary`) — use `zig test src/root.zig` to probe past that wall meanwhile.

## Migration order

**Inside a repo:** (1) fix `build.zig` first if it's on the blocked list above; nothing else is
visible until it compiles. (2) mechanical renames: GPA→DebugAllocator, `argsAlloc`→
`process.Init`, `mem.indexOf*`→`find*`, `ArrayList{}`→`.empty`. (3) Io-threading rewrites:
`fs`→`Io.Dir/File`, `net`→`Io.net`, `time`→`Io.Clock`, `Thread.*` sync→`Io.*`. (4) add
`error.Canceled` prongs everywhere this surfaces. (5) tests: `std.testing.io`, `tmpDir`
options, fuzz `Smith` rewrites if any. (6) bump `.minimum_zig_version = "0.16.0"` and tag.

**Across the kingdom:** sigil (spike, smallest foundation repo — settles the `io: Io`
convention above) → strata / synod / sirocco in parallel (foundation, trivial/zero-dep) →
zuda / sailor (libraries — fix the shared `linkLibC` break, tag **v3.0.0**) → zr (tooling,
depends on both libs) → silica (service) → zoltraak (service, largest, last). Do not bump a
consumer's dependency hash until the producer is tagged; use the 0.16 local-package-override
feature to point at an unpublished foundation/library checkout while it's still in flight.

## CI

Use `mlugg/setup-zig@v2` and let it resolve from `build.zig.zon` — do not hardcode `version:`
once a repo's `minimum_zig_version = "0.16.0"` is set:

```yaml
- uses: actions/checkout@v4
- uses: mlugg/setup-zig@v2   # resolves 0.16.0 from build.zig.zon minimum_zig_version
- run: zig build test
```

A repo still on 0.15.2 keeps `minimum_zig_version = "0.15.2"` and an untouched workflow — don't
edit a realm's CI file as part of an unrelated change before that realm has migrated.

## Gotchas

- `error.Canceled` is **one `l`**. Resist `else => unreachable` on I/O error switches — a
  swallowed cancelation is a resource leak, not a rare path.
- `io.async` guarantees completion, not concurrency — it may run inline. If two tasks must
  make simultaneous progress (producer/consumer on an unbuffered `Io.Queue`), use
  `io.concurrent` and handle `error.ConcurrencyUnavailable`; `async` there deadlocks under load.
- `Io.Group` idiom: `var g: Io.Group = .init; defer g.cancel(io);` right after `.init`, then
  `g.async(io, f, .{...})`, then `try g.await(io);` — `cancel` is a no-op once `await` ran.
- `File.Writer` is buffered — forgetting `try w.flush()` silently drops output on short CLIs.
- `readStreaming`/`writeStreaming` are **vectored**: `[]const []u8`, not `[]u8`. Wrap one
  buffer as `&.{&buf}`, or use the `*All` convenience wrapper for the simple case.
- `Io.Evented` is `void` on platforms without fiber support — an unconditional reference fails
  to compile there; guard with `if (fiber.supported)`.
- The `indexOf`→`find` rename is not a safe blind regex — the `Linear` and `Last` variants
  don't follow the simple pattern; use the mapping table above, not `s/indexOf/find/`.
- `ArenaAllocator` is threadsafe and lock-free now — delete `ThreadSafeAllocator` wrappers (the
  type is gone anyway); don't assume every other allocator gained that property.
- LLVM loop vectorization is disabled in 0.16 (an LLVM 21 regression workaround) — expect some
  numeric benchmark drift in CI that is not your code's fault; don't chase it as a bug.

## Sirocco note

Sirocco's target shape changed with 0.16: it should become an **implementation of
`std.Io.VTable`**, not a parallel I/O API — every consumer already speaks `Io`, so filling in
the vtable transparently powers `Io.Dir/File/net`, `http.Client`, and `crypto.tls.Client` for
free. Start from `Io.failing` as the skeleton and replace stubs in priority order (async/group/
await/cancel, futex, sleep/clock, `net*`, `file*`, `lockStderr`). Build a **hybrid vtable**:
forward `dir*`/`process*`/`randomSecure` to an embedded `Io.Threaded` until sirocco has its own
— legitimate, and it shortens the path to usable. Don't reinvent cancelation semantics
(`Io.Cancelable`/`recancel`/`swapCancelProtection`) — std already assumes them. Differential-test
every slot against `Io.Threaded`; treat swapping the `Io` at one service's `main` as the acceptance
test, not a side effect.
