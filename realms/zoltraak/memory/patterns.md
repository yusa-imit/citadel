# zoltraak — patterns

_(migrated and condensed from the repo's former CLAUDE.md and `.claude/memory/`)_

## Redis command implementation pattern (still the correct approach)

Adding or changing a command touches modules in this order:

1. **Storage layer** (`src/storage/memory.zig`): add the `Value` tagged-union variant and
   the ops it needs.
2. **Command handler** (`src/commands/<type>.zig`): parse args → validate → execute
   against storage → format the RESP response.
3. **Command routing** (`src/server.zig`): register the command in the dispatch table.
4. **WRONGTYPE check**: always verify the key's existing type matches before operating on
   it — do this before any mutation, not after.
5. **RESP3 awareness**: return native RESP3 types (maps, sets) when `protocol == 3`;
   RESP2 clients get the flattened array-based equivalent.

## Test-first, one-iteration-one-feature discipline

The repo's former 8-phase cycle (plan → write failing tests → implement → quality review
→ integration test → compat/perf validation → docs → cleanup → commit) is superseded as a
literal process by citadel's `implement`/`stabilize`/`review` skills, but the underlying
technical discipline it enforced is still the right shape for this codebase specifically:
- A failing test precedes every implementation, written against the Redis spec for the
  target command(s), not against the implementation once it exists.
- One iteration/PR = one feature or command group. No scope creep mid-change.
- Tests are meaningful: no `expect(true)`, no expected-values copied from the
  implementation, no assertion-free "does not crash" tests — this was a resurfacing
  problem serious enough that the repo ran a periodic dedicated test-quality audit.
- Differential testing against real Redis (byte-by-byte RESP comparison) and
  `redis-benchmark` throughput checks are the two forms of validation this codebase
  specifically needs beyond ordinary unit tests, given its whole purpose is
  Redis-protocol compatibility — both are CI/Docker-only, never local.

## Migration pattern for adopting a zuda module

1. Check `docs/milestones.md`'s zuda section for a `READY` migration before writing any
   new local data structure or algorithm.
2. Replace the local implementation with the zuda import; do not keep both in parallel
   longer than the one commit that does the swap.
3. Run `zig build test` (and the full integration suite) before considering it done.
4. Delete the now-dead local implementation code in the same change, and close any
   tracking issue.
5. If the zuda API shape doesn't fit Redis's on-wire semantics (as with HyperLogLog's
   allocator-based/error-returning shape vs. Redis's fixed-size no-error field, or
   Geohash's string encoding vs. Redis's binary integer), that is a real, durable BLOCKED
   state — file the mismatch upstream, do not paper over it locally, and do not keep
   retrying it every session.

## Zig 0.16 migration: check "true rename" vs. "0.16-only shape" before touching a site

Before applying any mechanical rename from `zig-0.16.md`'s mapping table, grep the *installed
0.15.2 stdlib* (`/opt/homebrew/Cellar/zig/0.15.2/lib/zig/std/`) for the 0.16-side name first.
Some renames are already present as aliases/methods in 0.15.2 (`std.ArrayList.empty`,
`std.heap.DebugAllocator`) — those are safe to apply now, verified real renames, and make the
code correct on both toolchains simultaneously. Others genuinely don't exist pre-0.16
(`std.process.Init`, `std.mem.find*` — 0.15.2 only has `indexOf*`) — applying those now would
break the toolchain still pinned in `build.zig.zon` (0.15.2 today; zoltraak can't bump this
until `zuda`/`sailor` tag v3.0.0, see plan 001 item 8's `blocked_by`). When a plan item bundles
both kinds (as item 4 did: `ArrayList`+`DebugAllocator` were safe, `main()`/`argsAlloc`/
`process.Init` were not), split it: do the safe part, leave the item's checkbox unchecked, and
note the deferred part inline in the plan file rather than blocking the whole item. Item 5
(`mem.indexOf*`→`find*`) will hit the same wall — expect to scope it down or skip to a
different unblocked item until the toolchain pin bumps.

## RESP protocol pattern

Every command handler is protocol-version-aware at the response-formatting step only —
parsing and validation logic does not branch on RESP2 vs RESP3; only `writer.zig`'s
serialization does. This keeps the RESP2/RESP3 duality from leaking into business logic.
