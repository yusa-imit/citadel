# zoltraak — architecture

_(migrated and condensed from the repo's former CLAUDE.md and `.claude/memory/`)_

## Layer shape

- `src/main.zig` → `src/server.zig` (TCP server, connection handling, command dispatch).
- `src/protocol/{parser,writer}.zig` — RESP2/RESP3 parse/serialize, protocol-version aware.
- `src/commands/` (41 files, one per Redis command family) — parse → validate → execute
  against storage → format RESP. Never touches storage internals directly beyond calling
  `src/storage/memory.zig`'s public ops.
- `src/storage/` (34 files) — `memory.zig` (15,650 lines) is the core engine: a tagged-union
  `Value` type plus per-type ops, backing every command family. Persistence (`persistence.zig`
  RDB, `aof.zig` AOF), replication, pub/sub, ACL, cluster, sentinel, config, and scripting
  state each get their own storage file; probabilistic/advanced types (bloom, cuckoo, cms,
  topk, tdigest, vector, timeseries, json_value/jsonpath) likewise.
- `src/scripting/` — embedded Lua interpreter + FFI + cjson/cmsgpack/struct/bit libraries +
  the `redis.call`/`pcall` API surface backing EVAL/EVALSHA.
- `src/network/tls.zig` — TLS/SSL. `src/cli.zig` + `src/tui_advanced.zig` — `zoltraak-cli`
  REPL client, built on sailor's TUI framework.

## Blocking-command architecture (the largest known gap)

Every `BLOCK`-family command (XREAD BLOCK, XREADGROUP BLOCK, BLPOP, BRPOP, BLMOVE, BLMPOP,
BZPOPMIN, BZPOPMAX, BZMPOP) currently runs this polling shape, verbatim from the codebase:

```zig
while (true) {
    const elapsed = std.time.milliTimestamp() - start_time;
    if (timeout_ms > 0 and elapsed >= timeout_ms) {
        return w.writeNull();
    }
    std.time.sleep(check_interval_ms * std.time.ns_per_ms);
    // Retry data check
}
```

A real, unused, event-driven replacement already exists at `src/storage/blocking.zig` (431
lines): `BlockedClient` / `BlockedXreadgroupClient` structs, a `pending_responses` hashmap for
async response delivery, and `unblock_requests` for `CLIENT UNBLOCK` support. It is not wired
into `server.zig`. Wiring it needs: (1) event-loop integration in `server.zig`, (2) per-
connection state beyond the current model, (3) an async response-delivery mechanism, (4) a
wake-up notification fired from XADD/XREADGROUP-style writers when new data lands that a
blocked client is waiting on. Estimated 3-4 iterations to wire, plus a 5-6 iteration general
event-loop refactor (epoll/kqueue) as a prerequisite — this refactor is also most of the
`std.net`/`std.Io.net` work the Zig 0.16 migration needs, so the two efforts should likely be
sequenced together rather than done twice.

## zuda integration boundary

`build.zig.zon` pins `zuda@2.0.4`. Three migrations attempted, two landed:
- Glob pattern matching → `zuda.algorithms.string.globMatch` (done).
- Haversine distance → `zuda.algorithms.geometry.haversineDistanceM` (done).
- HyperLogLog → `zuda.containers.probabilistic.HyperLogLog` (done per CLAUDE.md; note the
  historical Session 135 audit still listed it BLOCKED at that time over an allocator-based/
  error-returning API vs. Redis needing a fixed-size embedded `[16384]u8` with no error path —
  if it now reads DONE, confirm the shape actually matches before relying on it).
- Geohash encoding — permanently BLOCKED: zuda encodes geohashes as base32 strings, Redis
  sorted-set storage needs a 52-bit binary integer. Keep the local ~1400 LOC implementation;
  do not retry without a zuda-side API change.
- Sorted Set (~1800 LOC local skip-list) — READY, deferred behind the two above being
  resolved. Target: `zuda.compat.zoltraak_sortedset` or `zuda.containers.lists.SkipList`
  (needs `(score, member)` composite ordering plus rank/score range queries).

## Persistence

RDB (`storage/persistence.zig`) and AOF (`storage/aof.zig`) are separate paths. RDB save/load
round-trips are exercised per data type in `tests/`; two of those round-trip tests currently
crash the test binary (signal 4, illegal instruction) rather than failing an assertion — see
`debugging.md`. `WAITAOF` is a stub: AOF fsync tracking for it is not fully implemented.

## Cluster

Single-node topology with the full `CLUSTER` subcommand surface. `MIGRATE` was, until this
session, a stub that validated arguments and returned OK without doing network I/O; it now
opens a real TCP connection to the destination, applies the timeout as a socket
send/recv timeout, sends AUTH/AUTH2 if given, SELECTs the destination DB, and does
DUMP+RESTORE per key over the wire, tracking per-key success/failure and deleting migrated
keys from the source unless COPY was passed (preserved on `wip/migrate-real-dump-restore`).
