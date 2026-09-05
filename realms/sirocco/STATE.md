# sirocco — State Survey (2026-09-05)

## What exists vs claimed

Claimed (README/old CLAUDE.md/PRD): a full completion-based event loop abstracting
kqueue/epoll/io_uring/IOCP, TCP/UDP/Unix sockets, DNS, connection pooling, TLS 1.3
client/server, HTTP/1.1 + HTTP/2 (HPACK), WebSocket (RFC 6455), and a task/thread-pool
layer — a substantial network stack.

Actually present: scaffolding only. All six top-level modules (`io`, `net`, `tls`, `http`,
`ws`, `task`) are verbatim-identical stubs — a doc comment naming planned sub-files, an
`Error{ NotImplemented }` set, one `test "<mod>: module compiles"` calling
`std.testing.refAllDecls`. `root.zig` re-exports the six modules and a SemanticVersion
0.1.0. `main.zig` is a ~36-line CLI supporting only `version`/`--help`. None of the nested
files listed in the old CLAUDE.md's repo tree or the PRD's per-module sketches exist:
no `io/backend/*`, no socket code, no TLS, no HTTP parser, no WS framing, no thread pool.
`docs/milestones.md` tracks this honestly — every Phase 1 ("Loop Core") checkbox is
unchecked. `tests/` and `examples/` hold only `.gitkeep`. `bench/main.zig` exists as a
scaffold (not inspected for depth). This is a well-documented, functionally empty skeleton.

## Sizes

- `src/`: 187 lines across 8 files (root, main, io, net, tls, http, ws, task).
- Tests: 7 per static grep of `src/` ("module compiles" placeholders); the 0.16 probe's
  `zig build test` run reported 8/8 passing — reconcile the count in the first work cycle
  (likely a root-level aggregate test the grep missed).
- Files over 800 lines: 0 (largest file is 36 lines).
- Git history: 2 commits total; working tree clean, no dirty files, no wip branch to keep
  (foundation repos preserve none this session).

## CI

- Latest run (33944433092, "ci: run tests on Linux only; macOS covered by cross-compile"):
  success, 1m24s.
- Prior run (33944341024, bootstrap commit): failed, 46s — presumably the macOS-runner
  issue the very next commit fixed by restricting tests to Linux and covering macOS only
  via cross-compile. Worth re-confirming once real OS-specific backend code (kqueue) lands,
  since cross-compiling does not catch runtime backend bugs.
- Only 2 CI runs exist (repo has only 2 commits).

## Open issues / PRs

- Issues: none open.
- PRs: none open.

## Docs / root hygiene (fixed by the hygiene PR)

- Root is already clean: `.gitignore`, `CLAUDE.md`, `LICENSE`, `README.md`, `build.zig`,
  `build.zig.zon` — nothing flagged in `root_files_to_remove_or_move` (empty list).
- `.claude/` scaffolding (6 agents, 8 commands, 5 memory files, `settings.json`) is the
  generic template set, not repo-unique beyond the domain text inside `CLAUDE.md`/PRD
  itself. Per the restructure, `CLAUDE.md` and `.claude/` are removed from the repo in the
  next step; durable content has been migrated into this realm's `REALM.md`/`memory/`.
- `docs/PRD.md` (Korean PRD) and `docs/milestones.md` (phase checklist, single source of
  truth for progress) both stay in the repo — they are code-adjacent docs, not AI scaffold.

## Tiger Style gap table

| Metric | Count | Note |
|---|---|---|
| `assert(...)` | 0 | No functional code yet — nothing to assert around. |
| `catch unreachable` | 0 | Same. |
| `@panic(` | 0 | Same. |
| `std.debug.print` | 0 | Same. |
| Unbounded `while (true)` | 0 | Same. |
| Files > 800 lines | 0 | Largest file is 36 lines. |
| Functions > 70 lines | not measured | Nothing exceeds a handful of lines to sample. |

**Caveat**: every zero above is an artifact of zero functional code existing, not evidence
of Tiger Style discipline. The real test (assertions, deadline params, no per-op alloc,
800-line cap) begins once Phase 1 (`io/backend/*`, timing wheel, loop dispatch) lands.

## Zig 0.16 probe summary

- Build stage reached: source compile. `build.zig`/`build.zig.zon` are accepted as-is by
  0.16.0 (only `minimum_zig_version = "0.15.2"` wants a cosmetic bump). `zig build test`
  already **passes** on 0.16.0 (5/5 steps, 8/8 tests) because library modules are pure
  stubs and `main()`'s body is not analyzed in test mode. `zig test src/root.zig` passes
  7/7.
- Surfaced compiler errors: 2 (`src/main.zig`, `bench/main.zig`; compiler stops at the
  first error per binary, so the true latent count is higher once each is fixed in turn).
- Error classes (4, ~7 call sites total across the 2 entry-point files):
  1. `std.heap.GeneralPurposeAllocator` removed → use `std.heap.DebugAllocator(.{}){}` or
     switch `main` to `pub fn main(init: std.process.Init) !void` and use `init.gpa`.
  2. `std.process.argsAlloc` removed → `init.minimal.args.toSlice(init.arena.allocator())`.
  3. `std.fs.File.stdout().writer(buf)` → `std.Io.File.stdout().writer(io, &buf)` — needs
     an `Io` handle threaded from `std.process.Init`.
  4. `std.time.Timer` removed (bench only) → `std.Io.Clock`/`Io.Timestamp`.
- Blocking dependencies: none. `build.zig.zon` has `.dependencies = .{}` — nothing else in
  the kingdom must migrate before sirocco.
- Effort estimate: trivial, <1h — a verified 0.16 rewrite of `main.zig` compiled and ran
  (`sirocco 0.1.0`) in the probe's scratchpad; same pattern applies to `bench/main.zig`.
- Note: sirocco's stated purpose (event loop, kqueue/epoll/io_uring backends, TLS, HTTP,
  WS) overlaps almost entirely with the new `std.Io` in 0.16 — per ROADMAP Phase 2 the PRD
  should be rewritten against `std.Io.VTable` before Phase 1 implementation starts, not
  just mechanically migrated.

## Next work candidates

1. Plan `001`: Zig 0.16 migration (trivial, <1h) + PRD rewrite to target `std.Io.VTable`
   directly, ahead of any Phase 1 implementation, per ROADMAP Phase 2.
2. 1A: `io/completion.zig` — `Op`/`Result` types + intrusive (non-allocating) completion
   queue; tests for push/pop/remove and `Op`-tag coverage.
3. 1B: `io/backend/kqueue.zig` (macOS/BSD), validated with loopback TCP
   accept/connect/read/write/close tests.
4. 1D: `io/timer.zig` as a hierarchical timing wheel, O(1) register/cancel, tested for
   expiry ordering and load (~100k timers).
5. 1C: `io/backend/epoll.zig` (Linux) to unblock CI's Linux-only lane exercising real I/O.
6. 1E: `io/loop.zig` — dispatch loop, run modes, cross-thread wakeup, `cancel()`.
7. 1F: integration tests (loopback echo, timer races, cancel races) once 1A–1E land.
