# synod — State

Survey date: 2026-09-05. Source: repo survey + a Zig 0.16 compile probe run against a scratch
copy (no tracked files touched). See `REALM.md` for the durable realm summary this feeds.

## What exists vs. what is claimed

- Claimed (README/PRD/old CLAUDE.md): a full I/O-free Raft core (PreVote election, log
  replication, snapshots, joint-consensus membership, ReadIndex/lease reads) plus SWIM gossip,
  phi-accrual failure detection, and HLC/Lamport clocks, verified in a deterministic simulator
  across millions of scenarios.
- Actually present: a scaffold. Every `src/*.zig` top-level module (types, interfaces, log,
  raft, driver, membership, detector, clock, store, sim, adapters) is an 18-26 line stub — a
  doc comment, an empty `Error{NotImplemented}` set, and one placeholder
  `test "<module>: module compiles"` using `std.testing.refAllDecls`. The nested files the
  PRD/old CLAUDE.md describe (`raft/node.zig`, `sim/network.zig`, `membership/swim.zig`,
  `adapters/sirocco_transport.zig`, etc.) are empty directories with zero files.
  `docs/milestones.md`'s 24-item phase checklist is 100% unchecked — it agrees with the code,
  not with the README's tone. `src/main.zig` (36 lines) is a minimal CLI stub. `bench/main.zig`
  has one no-op benchmark. `tests/` and `examples/` are empty. No `CHANGELOG.md`.
- Repo is 2 commits old (bootstrapped this session, 2026-09-05).

## Sizes

- `src/` LOC: ~270 (no file over 36 lines; nothing close to the 800-line Tiger Style limit).
- Tests: 12, all trivial `refAllDecls` "compiles" stubs — no functional code is exercised yet.
- Files > 800 lines: 0.

## Build / CI

- Local (Zig 0.15.2): `zig build` succeeds cleanly; `zig build test` succeeds, 0 failures,
  completes in a few seconds.
- CI: 2 runs total (repo has 2 commits). Most recent (`33944435693`, "run tests on Linux only;
  macOS covered by cross-compile") — success, 56s. Prior run failed (macOS native-link issue),
  fixed by the next commit. Current HEAD's CI is green.
- Open issues: none. Open PRs: none.

## Tiger Style gap table

| Check | Count | Note |
|---|---|---|
| `assert` | 0 | No logic exists yet to assert over. |
| `catch unreachable` | 0 | — |
| `@panic` | 0 | — |
| `std.debug.print` | 0 | — |
| unbounded `while (true)` | 0 | — |
| files > 800 lines | 0 | Largest file is 36 lines. |
| functions > 70 lines | n/a | No function of substance exists to sample. |

All-zero here is a scaffold measurement, not evidence of discipline under load — re-run this
table once Phase 1 (types/log) lands and treat the first real numbers as the baseline.

## Zig 0.16 probe summary

- `zig build` on 0.16.0: **build.zig itself compiles clean** against the 0.16 `std.Build` API —
  zero breakage in the build script.
- Compile stage reached: source compile fails in `src/main.zig` (CLI entry point), not the
  build graph.
- 4 error classes, all in files outside the library core:
  1. `std.heap.GeneralPurposeAllocator` removed → `std.heap.DebugAllocator` (2 sites,
     `src/main.zig`). Mechanical rename; better fixed by adopting
     `pub fn main(init: std.process.Init) !void` and using `init.gpa`.
  2. `std.process.argsAlloc`/`argsFree` removed → `init.minimal.args.iterate()` (2 sites,
     `src/main.zig`).
  3. `std.fs.File` moved to `std.Io.File`; `.writer()` now takes an `Io` (2 sites,
     `src/main.zig`).
  4. `std.time.Timer` removed/moved under `std.Io` (1 site, `bench/main.zig`) — not yet
     resolved in the probe, only diagnosed; needs an `Io`-based timer.
- I/O surface is tiny: only `src/main.zig` and `bench/main.zig` touch
  fs/time/process/net/thread APIs at all; 0 hits anywhere else in `src/`.
- **The library core (types/interfaces/log/raft/driver/membership/detector/clock/store/sim/
  adapters) already compiles and passes all 12 module tests under 0.16 untouched** — synod's
  own "core never does I/O" rule paid off completely for this migration.
- Effort estimate: trivial, well under 1 hour. No blocking dependencies (`.dependencies = .{}`
  in `build.zig.zon`; `adapters.zig` is still a stub with no real sirocco/strata imports, so
  there is no cross-repo blocker either).
- Caveat: `zig build test` alone reports 13/13 passing on 0.16 even *before* any fix, because
  `zig test` never calls `main()` and Zig's lazy top-level analysis skips the broken lines
  entirely. Only `zig build` (builds the real exe) or `zig test src/main.zig` surfaces the
  actual errors — don't trust `zig build test` alone as a 0.16-readiness signal here.
- A scratch-copy fix (main.zig rewritten to `main(init: std.process.Init)`, DebugAllocator,
  `init.minimal.args.iterate()`, `std.Io.File.stdout().writer(init.io, &buf)`) compiled, ran
  (`synod version` printed `synod 0.1.0`), and kept 13/13 tests green. No tracked file in the
  real repo was touched.

## Docs / root hygiene (for the hygiene PR)

- `CLAUDE.md` and `.claude/` (20 tracked files: settings, 6 agents, 8 commands, 6 memory files)
  sit at repo root — `citadel/core/rules/docs.md` forbids both; the brain now lives at
  `citadel/realms/synod/`. The hygiene PR removes `CLAUDE.md` and `.claude/` from the repo.
  Everything durable inside them has been carried into this realm's `REALM.md`/`memory/*.md`.
- No other stray root files found — `.gitignore`, `LICENSE`, `README.md`, `build.zig`,
  `build.zig.zon` are all expected and stay.
- `docs/` only holds `PRD.md` and `milestones.md`; that's fine — `docs/adr/`, `docs/guides/`
  simply aren't needed yet. No `CHANGELOG.md` yet; add one before the first tagged release.
- Working tree is clean (no dirty-tree items to stash/discard); nothing tracked as modified.

## Next work candidates

1. Phase 1A — `src/types.zig`: `NodeId`/`Term`/`Index`/`Entry`/`HardState`/`Snapshot`/
   `Message` union/`ConfChange`; tests for Message tag exhaustiveness and HardState comparison.
2. Phase 1B — in-memory Raft log (`src/log.zig`): append/truncate/`termAt`, conflict-point
   search, `validate()`.
3. Phase 1C+1D — vtable interfaces (`src/interfaces.zig`) and in-memory `LogStore`
   (`src/store.zig`) with save/restore round-trip tests.
4. Phase 2 — `raft/node.zig`: core election state machine (Follower/Candidate/Leader, PreVote),
   once types/log/interfaces land.
5. Zig 0.16 migration (plan 001): trivial, <1h — fix `src/main.zig` (allocator, args, stdout
   writer) and `bench/main.zig` (timer); can happen any time, does not block Phase 1/2.
6. Add `CHANGELOG.md` before the first release.
