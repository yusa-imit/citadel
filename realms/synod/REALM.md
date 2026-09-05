# synod — Realm

| | |
|---|---|
| Layer | foundation |
| Path | `/Users/fn/codespace/synod` |
| GitHub | `yusa-imit/synod` |
| Version | 0.1.0 (`build.zig.zon`) · latest tag none yet |
| Zig | 0.15.2 (migrating to 0.16.0 under plan 001) |
| Depends on | none — Zig std only (ADR-001); kingdom integrations are opt-in adapters |
| Consumers | silica (replication/failover), zoltraak (cluster/sentinel) |
| blocked_by | — |
| CI | Linux tests + 6 cross-compile targets (`.github/workflows/ci.yml`) |

## What it is

synod is the Zig kingdom's foundation consensus core: a pure, I/O-free Raft state machine
(PreVote election, log replication, snapshots, joint-consensus membership changes,
ReadIndex/lease reads) plus SWIM gossip membership, a phi-accrual failure detector, and hybrid
logical / Lamport clocks. Network, disk, and time are injected via vtables so the same core can
be driven, byte-for-byte deterministically, by a simulator across millions of scenarios before
it ever touches a real socket. silica ports its replication/failover onto this core; zoltraak
ports its cluster/sentinel behavior onto it. As of this survey (2026-09-05) the repo is
scaffold-only: the PRD, milestone checklist, and module layout are fully designed, but every
`src/*.zig` file is an 18-26 line stub (doc comment, `Error{NotImplemented}`, one
`refAllDecls` test) — see `STATE.md` for the honest implemented-vs-claimed breakdown.

No `wip/*` branch was preserved for synod this session — its working tree was already clean
(nothing to stash). Sibling foundation repos (sigil, sirocco, strata) likewise got none this
cycle; that pattern is foundation-specific — silica, sailor, zoltraak, zr, and zuda each had
in-progress work stashed to a `wip/*` branch elsewhere in the kingdom this session.

## Build and test

```bash
zig build              # library + CLI
zig build test         # unit tests (a few seconds — currently 12 trivial "compiles" stubs)
zig fmt --check src build.zig
```

Local-only: `zig build`, `zig build test`. CI-only: cross-compile, benchmarks, fuzz.
No local servers or ports to manage — synod never opens a socket, file, or clock itself
(all are injected vtables), so there is nothing to kill between runs. `zig build test` finishes
in seconds today; even once Phase 3's deterministic simulator lands, simulation runs stay
in-process (virtual clock/network) rather than spawning anything — unlike zuda/silica's
long-running local suites, synod should never need a "run this overnight" local test policy.

## Realm-specific rules

- **Module build order** (respect this dependency order; each phase's tests gate the next):
  `types` → `interfaces` + `log` → `store` (in-memory `LogStore`) → `raft` (election, then
  replication, then snapshot/joint-consensus, then ReadIndex) → `driver` → `membership`
  (SWIM) / `detector` (phi-accrual) / `clock` (HLC, Lamport) → `sim` (deterministic harness,
  needs everything above) → `adapters` (sirocco transport, strata logstore — last, optional).
- **Consumer registry**: silica adopts synod for replication/failover; zoltraak adopts it for
  cluster/sentinel. No other kingdom repo depends on synod. Foundation layering means synod
  itself may depend on nothing above it — not even via the general zuda-first rule: general
  data structures/algorithms normally come from zuda (`00-kingdom.md`), but synod cannot
  depend on zuda at all (libraries sit above foundation), so write anything it needs in-tree.
- **Release quirks**: version bumps are monotonic — next minor unless the change is fix-only
  (then patch); MAJOR only on explicit user instruction. Release requires `zig build test` at
  0 failures, all 6 cross-compile targets green, and 0 open `bug` issues. No CHANGELOG.md
  exists yet — add one before the first tagged release.
- **Core-is-pure-state-machine API pattern** (the load-bearing design rule; enforce by grep in
  review, not just convention):
  - `raft/`, `membership/`, `detector/` never import `std.net`, `std.fs`, or `std.time`
    directly — no I/O in the core.
  - Clock and RNG are always injected (`Clock`/`Rng` vtables); never call
    `std.time.milliTimestamp()` (or its 0.16 `Io.Clock` equivalent) from core code.
  - All state transitions happen only via `step()` / `tick()`; nothing mutates a core struct's
    fields from outside.
  - Effects are returned by value; the core never calls a callback.
  - Membership changes go through joint consensus only — no single-server add/remove path.
  - Invariant violations return `error.Invariant*` so the simulator can report the failing
    seed, rather than asserting/panicking mid-run.
  - Every wire message carries a protocol-version field, for rolling upgrades.

## Layout

| Module | Status |
|---|---|
| `src/root.zig` | Library root — re-exports all public modules, has `refAllDecls` test |
| `src/main.zig` | CLI entry point stub (36 lines) |
| `src/types.zig` | Stub — `NodeId`/`Term`/`Index`/`Entry`/`HardState`/`Snapshot`/`Message` |
| `src/interfaces.zig` | Stub — `Transport`/`LogStore`/`StateMachine`/`Clock`/`Rng` vtables |
| `src/log.zig` | Stub — in-memory Raft log: append/truncate/term lookup |
| `src/raft.zig` | Stub — pure Raft: election/replication/snapshot/membership/ReadIndex |
| `src/driver.zig` | Stub — executes Effects against Transport/LogStore/StateMachine |
| `src/membership.zig` | Stub — SWIM gossip protocol |
| `src/detector.zig` | Stub — phi-accrual failure detector |
| `src/clock.zig` | Stub — HLC/Lamport/monotonic clock |
| `src/store.zig` | Stub — in-memory `LogStore` |
| `src/sim.zig` | Stub — deterministic simulation harness |
| `src/adapters.zig` | Stub — opt-in sirocco/strata adapters |
| `src/{adapters,detector,raft,sim,membership,clock,store}/` | Empty — no files yet |
| `bench/main.zig` | One no-op benchmark |
| `tests/`, `examples/` | Empty |

## Known gaps (from STATE.md)

- Tiger Style greps (asserts, `catch unreachable`, `@panic`, `std.debug.print`, unbounded
  `while (true)`, files > 800 lines) all read 0 — but that measures a scaffold with no real
  logic yet, not disciplined code under load. Re-measure once Phase 1 lands.
- README/PRD read as if a full Raft+SWIM+detector+HLC+simulator library exists; 0% of that
  logic is written and `docs/milestones.md`'s 24-item checklist is 100% unchecked. Do not treat
  this repo as usable or as a real dependency yet.
- No CHANGELOG.md.
