# synod — architecture

_(migrated from the repo's former .claude/memory; keep under 200 lines)_

See `docs/PRD.md` §4 in the synod repo for the intended layering. Record here only what
**diverges** from or **refines** the PRD as modules actually land — nothing has landed yet.

## Layering (as built)

Nothing built yet (Phase 1 not started). Planned reference layout (from the repo's former
CLAUDE.md — file names/module boundaries may change during implementation; update this section
when they do):

```
src/types.zig        NodeId, Term, Index, Entry, HardState, Snapshot, Message union, ConfChange
src/interfaces.zig   Transport, LogStore, StateMachine, Clock, Rng vtables
src/log.zig          in-memory Raft log: append/truncate/term lookup, invariant validation
src/raft.zig         pure state machine: election(PreVote)/replication/progress/snapshot/
                      joint-consensus membership/ReadIndex+lease reads
  raft/node.zig, raft/progress.zig, raft/snapshot.zig, raft/membership.zig, raft/read.zig
src/driver.zig       executes Effects against Transport / LogStore / StateMachine
src/membership.zig   SWIM gossip: ping, ping-req, suspicion, incarnation numbers
  membership/swim.zig
src/detector.zig     phi-accrual failure detector
  detector/phi_accrual.zig
src/clock.zig        hybrid logical clock, Lamport clock, monotonic Clock interface
  clock/hlc.zig, clock/lamport.zig
src/store.zig        in-memory LogStore for tests and simulation
  store/memory.zig
src/sim.zig          deterministic simulation: virtual clock, virtual network (delay/loss/
                      partition/reorder), scenarios, Raft safety invariants, linearizability
  sim/clock.zig, sim/network.zig, sim/simulation.zig, sim/invariants.zig,
  sim/linearizability.zig
src/adapters.zig     opt-in adapters: sirocco Transport, strata LogStore (last, optional)
  adapters/sirocco_transport.zig, adapters/strata_logstore.zig
```

Build order matters: types → interfaces+log → store → raft (election, then replication, then
snapshot/membership, then ReadIndex) → driver → membership/detector/clock → sim → adapters.

## Interfaces

Not designed yet beyond the vtable shapes named above (Transport/LogStore/StateMachine/Clock/
Rng in `interfaces.zig`). Ownership and lifetime contracts to be recorded here once written.

## Formats

No wire or on-disk format defined yet. When one lands, record it here with a version number
and the bump rule (messages must carry a protocol-version field — see `REALM.md`).
