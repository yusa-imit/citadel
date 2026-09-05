# zoltraak — Realm

| | |
|---|---|
| Layer | service |
| Path | `/Users/fn/codespace/zoltraak` |
| GitHub | `yusa-imit/zoltraak` |
| Version | 0.2.0 (`build.zig.zon`) · latest tag v0.2.14 |
| Zig | 0.15.2 — migrating to 0.16.0 under plan `001` |
| Depends on | sailor v2.99.0, zuda v2.0.4 |
| Consumers | none (leaf service) |
| blocked_by | zuda v3.0.0, sailor v3.0.0 |
| CI | Linux build + unit tests + shell integration tests; **no cross-compile job yet** (plan 001 adds it) |

## What it is

A from-scratch, Redis-compatible in-memory data store server written in Zig: RESP2/RESP3
protocol, 500+ commands across strings/lists/sets/hashes/sorted sets/streams/bitmaps/geo/
probabilistic types/JSON/search/time series/vector sets, RDB+AOF persistence, replication,
pub/sub, transactions, a real embedded Lua engine, ACL enforcement, multi-DB, single-node
Cluster (including a just-finished real `MIGRATE` over DUMP/RESTORE), and Sentinel failover.
141K LOC in `src/`, ~1100 unit tests plus a 226-file integration suite, clean build, CI green.
The main honest gap is that all `BLOCK`-family commands (XREAD/XREADGROUP/B*) still use a
polling loop rather than the unused `src/storage/blocking.zig` event-driven infrastructure.

## Build and test

```bash
zig build              # server + zoltraak-cli
zig build test         # unit tests (~6s; 1098/1098 pass, 205/208 build steps)
zig fmt --check src build.zig
```

Local-only: `zig build`, `zig build test`. CI-only: cross-compile, benchmarks, fuzz.

Run notes:
- Default server binds `127.0.0.1:6379`. Before committing or ending a session, kill any
  server this session started and free the port: `pkill -f zoltraak; lsof -ti :6379 | xargs
  kill 2>/dev/null`.
- `zig build test` occasionally spawns 2 known-flaky crashing test binaries (`test_iter437`
  time-series RDB round-trip, `test_iter432` streams RDB round-trip — signal 4, illegal
  instruction on deserialize). Pre-existing, documented, unrelated to any given change; do
  not treat a run that hits only these two as a new regression, but do not ignore a third.
- Cross-compile (6 targets), `redis-benchmark` throughput/latency, stress tests, and shell/
  differential tests against real Redis are CI/Docker-only — never run them from a local cron
  session; they can exhaust local resources when multiple kingdom repos' cron jobs overlap.
- `zig-pkg/` (extracted dependency sources from a local build) is a build artifact; ensure
  it stays out of git.

## Realm-specific rules

- **Command implementation pattern** (module touch order for any new/changed Redis command):
  (1) storage layer — add the `Value` variant + ops in `src/storage/memory.zig`; (2) command
  handler in `src/commands/<type>.zig` — parse args, validate, execute against storage, format
  RESP; (3) register in `src/server.zig`'s dispatch table; (4) always WRONGTYPE-check the key's
  type before operating; (5) return native RESP3 map/set types when `protocol == 3`.
- **Zig 0.15 gotchas specific to this codebase** (until the 0.16 migration lands):
  `ArrayListUnmanaged` mutation methods take the allocator as their first argument;
  `std.io.getStdOut().writer(&buf)` + `.interface.print()`, flush before exit;
  `std.builtin.Type` tags are lowercase (`.int`, `.@"struct"`); use `b.createModule()` for
  exe/test build targets.
- **zuda migration state is pinned, not aspirational**: HyperLogLog and Geohash migrations are
  permanently BLOCKED on real API mismatches (HyperLogLog: zuda's container is allocator-based
  and returns errors, Redis needs a fixed-size embedded `[16384]u8` with no error path; Geohash:
  zuda encodes to a base32 string, Redis needs a 52-bit binary integer for sorted-set storage) —
  do not retry either without a zuda-side API change. Sorted Set (~1800 LOC local skip-list) is
  READY to migrate to `zuda.compat.zoltraak_sortedset` once picked up.
- **Consumer registry**: no other kingdom realm imports zoltraak today, so a breaking API
  change here needs no cross-repo `migration` issues — it is still bound by the kingdom's
  single-branch/no-force-push rules, but there is no consumer fallout to manage.
- **Version bookkeeping was already 3-way divergent before this restructure**: `build.zig.zon`
  said `0.2.0`, the last CLAUDE.md said `v0.2.13`, and the actual latest tag is `v0.2.14`.
  Reconcile all three against `protocol/VERSIONING.md` at the next release rather than trusting
  any single source.

## Layout

| Path | What |
|---|---|
| `src/main.zig` | server process entry point |
| `src/server.zig` | TCP server, connection handling, command dispatch/routing |
| `src/cli.zig` (970 lines) | `zoltraak-cli` REPL client built on sailor |
| `src/tui_advanced.zig` (1228 lines) | advanced TUI features for the CLI |
| `src/protocol/{parser,writer}.zig` | RESP2/RESP3 request parsing and response serialization |
| `src/network/tls.zig` | TLS/SSL connection support |
| `src/scripting/*.zig` | embedded Lua interpreter, FFI, cjson/cmsgpack/struct/bit, redis.call API |
| `src/utils/glob.zig` | glob pattern matching (partially migrated to zuda) |
| `src/commands/` (41 files) | one file per Redis command family (strings … auth) |
| `src/storage/` (34 files) | data/persistence layer; `memory.zig` (15650 lines) is the core |
| `tests/` (226 files) | integration suite |
| `docs/PRD.md`, `docs/milestones.md` | 1.0 roadmap; authoritative per-iteration changelog |

## Known gaps (from STATE.md)

- Blocking commands (XREAD/XREADGROUP BLOCK, BLPOP/BRPOP/BLMOVE/BLMPOP/BZPOPMIN/BZPOPMAX/
  BZMPOP) use a polling-loop-with-sleep; `src/storage/blocking.zig` (431 lines, real queue
  infra) exists unwired. Est. 3-4 iterations to wire + 5-6 for the event-loop refactor it needs.
- Two RDB round-trip test binaries crash with signal 4 on deserialize: `test_iter437`
  (time series), `test_iter432` (streams) — known, unresolved, worth root-causing as a possible
  safety-check trip (bounds/overflow) rather than a benign flake.
- 44 of ~90 `src/*.zig` files exceed 800 lines (Tiger Style file-size violation at scale):
  `memory.zig` 15650, `strings.zig` 7869, `json.zig` 5417, `sorted_sets.zig` 5206,
  `cluster.zig` (storage) 5733, `client.zig` 4991, `keys.zig` 4052, `cluster.zig` (commands)
  4483. 105 `std.debug.print` calls remain in `src/` (contradicts the repo's own cleanup rule).
  17 `catch unreachable` sites unaudited for client-input-reachable violations. 11 unbounded
  `while (true)` loops (some are legitimate server loops, some are the polling-blocking gap
  above).
- Zig 0.16 migration: `build.zig` fails first (3 errors, `linkSystemLibrary`/`linkLibC` no
  longer exist on `Step.Compile`) — mechanical, but blocks reaching source at all. Once past
  that, ~a dozen 0.16 API classes touch ~40 of 89 `src/` files: `ArrayList(T){}` literal removal
  (63 hits, mechanical), `std.time.*Timestamp` removed (19 hits, needs `Io` threading),
  `std.Thread.Mutex` moved to `std.Io.Mutex` (9), `std.net` moved under `std.Io.net` (8, the
  hard architectural piece — TLS/replication/redis_api networking core), `std.fs.cwd()`/`File`
  reorganized (8), `GeneralPurposeAllocator` renamed `DebugAllocator` (3),
  `ArrayList.writer()` removed (1). Blocked on sailor and zuda shipping 0.16-compatible
  `build.zig` first (both fail identically on `linkLibC()`). Effort: large, 5-15 sessions.
  (~730 additional "expected N argument(s)" errors are pre-existing broken test signatures,
  reproduce under 0.15.2 too, and are excluded from the above.)
- Hygiene (next PR): untrack `.DS_Store` (root, `src/`, `docs/`, `.claude/`), delete tracked
  0-byte `test_cms_sig` stub, untrack generated `.iteration`, gitignore `zig-pkg/`, and
  consolidate ~30+ loose iteration/spec/summary `.md` files scattered in `.claude/` root and
  `.claude/specs/` (superseded by `docs/milestones.md`) — see STATE.md for the full list.
- A complete, tested, uncommitted change was preserved this session on `wip/migrate-real-dump-
  restore`: real `MIGRATE` via TCP DUMP/RESTORE in `src/commands/cluster.zig` (295+/56- lines,
  matching tests included, `zig build test` green with it applied) — ready to open as a PR,
  not abandoned or broken.
