# silica — Realm

| | |
|---|---|
| Layer | Service |
| Path | `/Users/fn/codespace/silica` |
| GitHub | `yusa-imit/silica` |
| Version | 1.0.1 (`build.zig.zon`) · latest tag v1.0.1 |
| Zig | 0.15.2 — migrating to 0.16.0 under plan `001` |
| Depends on | sailor v2.99.0, zuda v2.3.0 |
| Consumers | none — service layer; nothing in the kingdom depends on silica |
| blocked_by | zuda v3.0.0, sailor v3.0.0 (0.16-compatible releases) |
| CI | Linux tests + 6 cross-compile targets (`.github/workflows/ci.yml`) |

## What it is

A Zig-native, PostgreSQL/SQLite-inspired embedded + client-server relational
database engine (184k LOC) targeting SQL:2016, MVCC, and WAL-based streaming
replication. Dual-mode: embedded library (Zig API + C FFI) and a standalone
server speaking the PostgreSQL wire protocol v3 (SCRAM-SHA-256, TLS, RBAC,
RLS). Core is genuinely implemented and tested — SQL engine (tokenizer through
cost-based optimizer), B+Tree storage with a buffer pool, WAL + locking +
vacuum, and real (non-stub) primary→replica physical WAL streaming with an
end-to-end loopback test. Several named subsystems remain partial despite the
v1.0.1 "all 12 phases complete" headline: GIN index (unstable, redesign
pending), GiST (B+Tree-fallback semantics only), index-only-scan (partial),
and MVCC UPDATE (delete+insert, not true version chains — deferred to a
v2.0-scope B+Tree refactor). See `STATE.md` for the full honest inventory.

## Build and test

```bash
zig build              # library + CLI, clean build ~60s
zig build test         # unit tests, ~50s, ~4900 tests
zig fmt --check src build.zig
```

Local-only: `zig build`, `zig build test`. CI-only: 6-target cross-compile,
`zig build bench`, fuzz targets (`fuzz.zig`, `wal_fuzz.zig`, `wire_fuzz.zig`)
and stress/Jepsen-style concurrent tests — these are resource-intensive
enough that running them locally alongside other kingdom repos' cron jobs has
previously caused system instability; never run them outside CI/Docker.

Stray build/test artifacts accumulate under the repo root (`test_*.db`,
`*.o`, `.DS_Store`) and are `.gitignore`d; an untracked `zig-pkg/` directory
was observed this session and is not yet covered by `.gitignore` — add it or
delete it, don't commit it.

## Run notes

- No server/ports are involved in the normal build/test loop. The PG-wire
  server (`zig build run -- server --port 5433`) and the TUI browser
  (`zig build run -- --tui`) are separate run modes, not exercised by
  `zig build test`; nothing needs to be killed between cron sessions under
  normal (non-server-mode) operation.
- **Concurrency limitation (carried over, not reconfirmed this survey)**: an
  older architecture note states silica does not support concurrent
  connections safely — each `Database.open()` gets its own buffer pool and
  WAL instance, and multiple WAL instances writing the same file can
  interleave frames and corrupt checksums. If this is still true, any future
  multi-connection server work must serialize WAL writes or share one buffer
  pool first (see `memory/architecture.md`).
- **Preserved WIP**: branch `wip/wal-checkpoint-retention-phase2` holds
  in-progress, architect-planned Phase 2/3 work (WAL checkpoint truncation
  deferred when a replication slot lags). It has one failing test
  (`tx.wal.test.Phase 6: regression proof`, `src/tx/wal.zig:2311`, expected
  17 got 3) — do not merge until that's fixed; the logic bug looks like a
  small byte-offset error in the new truncation-skip path.

## Realm-specific rules

- **Module build/dependency order** (still the convention for planning
  feature work): `util` (checksum, varint) → `storage` (page, btree,
  buffer_pool) → `tx` (wal, lock, mvcc, vacuum) → `sql` (tokenizer through
  engine) → `server` (wire, connection) → `replication`.
- **Consumer registry**: none. Silica has no in-kingdom downstream — no
  migration-issue obligations to file when silica's own API changes.
- **zuda-first exceptions**: the B+Tree is deliberately **not** migrating to
  a zuda container — it's disk-backed with WAL/MVCC integration, and zuda's
  in-memory containers don't fit (architect review, session 27). The buffer
  pool's LRU eviction has conflicting history in the repo's own memory: an
  architect decision (session 27) said keep it custom (zuda's eviction
  callback is non-failable — risk of silently swallowing a flush failure);
  a later note (session 46, `architecture.md`) says it *was* migrated to
  `zuda.containers.cache.LRUCache` and all tests passed. **Unresolved
  contradiction, not verified by this survey** — check
  `src/storage/buffer_pool.zig` directly before trusting either note.
- **Release quirks**: versions are monotonic and never skip — a release
  always bumps to current `build.zig.zon` version + 1 minor (or a bare tag
  for a patch), even if a milestone doc pre-assigned a different number.
  Minor release requires: current-phase checklist complete, `zig build
  test` green, 6-target cross-compile green, zero open `bug`-labeled
  issues. Patch releases are tag-only (no `build.zig.zon` bump) and must
  not carry feature commits.
- **Local test policy**: cross-compile (6 targets), `zig build bench`, and
  fuzz/stress tests never run outside CI — historically linked to local
  system instability when run alongside other kingdom repos' heavy
  processes.
- **API patterns that are load-bearing, not style**: WAL-first writes only
  (never touch the main DB file directly); every returned tuple must pass
  an MVCC visibility check first; PG wire protocol byte-compatibility is
  required, not just "close enough"; page writes must be atomic (partial
  page write = corruption).

## Layout

| Module | Notes |
|---|---|
| `src/main.zig` | entrypoint / mode dispatch (embedded shell, TUI, server) |
| `src/cli.zig` (8.3k lines) | CLI parsing, embedded SQL shell/REPL |
| `src/tui.zig` (9.5k lines) | terminal UI browser (on sailor's TUI library) |
| `src/sql/` (19 files, ~90k+ LOC) | tokenizer, parser, analyzer, planner, |
| | optimizer, catalog, execution engine (`engine.zig` 43.2k, |
| | `executor.zig` 35.3k lines — see Known gaps), MATCH_RECOGNIZE |
| `src/storage/` (9 files) | page, btree (4.5k lines), buffer_pool, fsm, |
| | overflow, hash/gist/gin index, fuzz |
| `src/tx/` (7 files) | mvcc, wal, lock (deadlock detection), vacuum, |
| | wal_fuzz, jepsen_test, crash_test |
| `src/server/` (5 files) | server, connection, wire (PG wire v3), auth, |
| | wire_fuzz |
| `src/replication/` (13 files) | sender, receiver, transport, protocol, |
| | slot, monitor, cascade, promotion, standby, switchover, backup, |
| | sync, integration_test |
| `src/config/` (2 files) | file, manager (`silica.conf` parse/hot-reload) |
| `src/util/` (3 files) | checksum (CRC32C), varint (LEB128), regex |
| `src/query/` | empty directory, no files |

## Known gaps (from STATE.md)

Tiger Style grep counts (not a full audit): 41 files over 800 lines, with two
extreme outliers (`engine.zig` 43,242 lines, `executor.zig` 35,253 lines);
212 `catch unreachable`; 104 unbounded `while (true)`; 7 `@panic(`; 16 debug
prints; only 12 `assert`s repo-wide. Functions-over-70-lines was not measured
but is near-certain given the two outlier files.

Top risks: (1) the uncommitted WAL-retention WIP has one failing test — see
Run notes; (2) GIN index instability with a pending redesign
(`docs/GIN_INDEX_REDESIGN.md`), integration tests skipped; (3) MVCC UPDATE is
delete+insert, not true version chains — transient `NoRows` for concurrent
readers, deferred to v2.0 scope; (4) the buffer-pool-LRU zuda-migration
contradiction above needs a source read to resolve; (5) `zig-pkg/` untracked
directory not yet gitignored.
