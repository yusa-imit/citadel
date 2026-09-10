# sirocco — State Survey (2026-09-05, refreshed 2026-09-11)

## Refresh 2026-09-11 (cycle 8, FEATURE) — Release v0.2.0

Milestone `001` (Zig 0.16 migration and Tiger Style baseline) complete and released.
`build.zig.zon`/`root.zig` version `0.1.0 -> 0.2.0`, tag `v0.2.0` pushed, GitHub release
published (https://github.com/yusa-imit/sirocco/releases/tag/v0.2.0) via PR #12. Milestone
issue #3 closed. No consumer repo's `build.zig.zon` names sirocco yet (checked against
`citadel/zr-repos.toml` — sailor/zr/silica/zoltraak list it only as a planned dep), so no
migration issues were opened. Next cycle has no open plan or milestone — expect `/plan` to
scope plan `002` (Phase 2: `std.Io.VTable` implementation per ROADMAP).

## Refresh 2026-09-09 (cycle 5, STABILIZATION)

- CI: last 5 runs on main all green (success). No red CI, no open bug issues.
- Tidy audit (tidy-auditor agent, independent grep pass + `zig build tidy`): zero violations
  in every category — `catch unreachable` (0 outside tools/tidy_test.zig's own fixtures),
  `@panic`/`std.debug.print`/`while (true)` in src/ (0 each), functions > 70 lines (0; only
  `pub fn` in src/ is `main.zig:10`, ~25 lines), files > 800 lines (0; largest is 36 lines),
  `usize` in wire formats (0; no structs exist yet), missing `//!` headers (0/8 — all 8 src/
  files confirmed to have one), `assert(` count (0 — no functions to assert around besides
  `main`), `== error.`/`anyerror` in pub fn (0 each). Repo is mechanically clean.
- Milestone #3 item "Assertion and Tiger Style baseline" is **not yet actionable as worded**:
  `root.zig` currently declares no `pub fn` at all (only `pub const version` and re-exports),
  so there is nothing to add pre/post-condition assertions to yet. Reframe this item once
  actual `Runtime` functions land (per the ADR/PRD), not before.
- Docs drift found and fixed: `README.md` still described the superseded parallel
  `io`/`net`/`tls`/`http`/`ws`/`task` public-module design (kqueue/epoll/io_uring/IOCP
  abstraction) that PR #7 already replaced in `docs/PRD.md` and
  `docs/adr/0001-std-io-vtable.md` — the README rewrite in that PR only touched `docs/PRD.md`,
  not `README.md`. Fixed via PR #8 (merged, docs-only, `*.md` CI-paths-ignored, no checks
  applied — same as PR #7): reconciled module table into the single `Runtime.io() -> std.Io`
  surface, updated Status, added a Design section. Milestone item 10 ("README and CHANGELOG
  reconciled with reality") is now half-done — no `CHANGELOG.md` exists yet and creating one
  before a first release would be premature; leave the checkbox open until release time.
- Dependencies: N/A — `build.zig.zon` `.dependencies = .{}`, zero-dependency foundation repo.
- Benchmarks: not run this cycle (repo has no functional I/O yet — `bench/main.zig` is a
  scaffold; nothing meaningful to measure before Phase 1 lands).
- Hygiene: root directory clean (`.gitignore`, `LICENSE`, `README.md`, `build.zig`,
  `build.zig.zon`, `docs/`, `src/`, `bench/`, `tools/`, `tests/`, `examples/` — nothing
  flagged against `citadel/protocol/DOCS.md`).

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
