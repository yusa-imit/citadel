# silica — architecture

_(migrated from the repo's former `.claude/memory/`; condensed, see git
history in silica itself for the full design-doc narrative this was cut
from)_

## Layered architecture

```
Client Layer      Zig API (embedded) | C FFI | PG wire protocol
SQL Frontend      Tokenizer -> Parser -> Semantic Analyzer
Query Engine      Planner -> Optimizer -> Executor (Volcano model)
Transaction Mgr   WAL Writer | Lock Manager | MVCC
Storage Engine    B+Tree | Page Manager | Buffer Pool
OS Layer          File I/O | fsync
```

Module build/dependency order: `util` (checksum, varint) → `storage` (page,
btree, buffer_pool) → `tx` (wal, lock) → `sql` (tokenizer, parser,
analyzer) → `query` (planner, optimizer, executor) → `server` (wire,
connection) → `replication`.

## File format

```
Page 0: Database Header — magic "SLCA" (4B), format version u32, page size
        u32, total page count u32, freelist head u32, schema version u32,
        WAL mode flag u8, padding to page_size.
Page 1: Schema table root (B+Tree).
Page 2..N: Data & index pages.
```

Pages are fixed-size (default 4KB, configurable 512B-64KB). B+Tree uses
doubly-linked leaf pages for range scans, overflow pages for large values.

## Concurrency limitation (CRITICAL, session-40 finding — not reconfirmed)

Each `Database.open()` creates its own Buffer Pool and its own WAL instance,
but shares the Transaction Manager via a global registry. Multiple `Wal`
instances writing the same file with no synchronization can interleave
frames and corrupt checksums; a stale buffer-pool cache can also serve one
connection another's already-modified page. Concurrent/Jepsen-style tests
were seen losing data under this. **Status unverified as of the 2026-09-05
restructure** — replication and further MVCC work have landed since; check
whether a shared buffer pool / serialized WAL writer has since been added
before assuming this is still true.

## MVCC

Snapshot isolation via row versioning. **UPDATE is delete+insert, not true
version chains** — a documented architectural limitation: concurrent
readers can briefly see `NoRows` between the delete and the insert. Fix
requires multi-version storage / delayed deletion / version chains,
deferred to v2.0 scope (needs a B+Tree refactor, not a local patch).
`SAVEPOINT` rollback + `COMMIT` also failed to undo rolled-back rows for
the same underlying reason (issue #125, physical-undo-log fix landed and
closed by session 507 — see the repo's own git history/CHANGELOG to
confirm status, this memory predates that closure being fully verified).

## Replication

Physical WAL streaming implemented end-to-end (sender/receiver/transport/
protocol/slot/monitor/cascade/promotion/standby/switchover/backup/sync).
LSN is packed as `(checkpoint_seq << 32 | frame_index)` in both
`wal.Lsn` and `protocol.LSN` — pack/unpack logic is currently duplicated in
`sender.zig`/`receiver.zig` (DRY cleanup not yet done). `Wal.checkpoint()`
truncates the file unconditionally today with **no** awareness of a
connected replication slot's `restart_lsn` (`slot.SlotManager
.getMinRestartLSN()` exists but nothing in `wal.zig` calls it) — a primary
that checkpoints while a replica lags can silently discard WAL data the
replica still needs. This is exactly what the in-flight
`wip/wal-checkpoint-retention-phase2` branch (see STATE.md) is fixing: a
type-erased `setRetentionCallback`/`clearRetentionCallback` on `Wal`
(callback avoids the storage layer importing the replication layer's
types), and `checkpoint()` split into an always-unconditional flush vs. a
conditional reclaim/truncate that defers when the callback reports the
min-retained-LSN is behind the epoch being discarded.

`server.zig`/`connection.zig` had **zero** `SlotManager` wiring as of the
last architect review that checked (grep-confirmed) — retention callbacks
and slot lifecycle are not yet connected end-to-end in the server binary.

## Known partial/gap subsystems (as of this restructure)

- **GIN index**: native storage wiring (array_ops/jsonb_ops/tsvector_ops)
  is feature-complete end-to-end via SQL for rowid tables (row_key packed
  bit-for-bit into GIN's `ItemPointer` u64 field). Text/composite-PK tables
  permanently fall back to B+Tree. Hard limit: the entry tree is
  single-page with **no split** — `insertNewEntry` returns `error.PageFull`
  on a full root; a real multi-level entry tree is needed before this is
  safe for high-cardinality columns, and must happen before (or via a full
  on-disk migration after) any wider rollout. `REINDEX` has no GIN branch —
  migrating an existing B+Tree-fallback `.gin` index to native is
  unimplemented (new-indexes-only scope).
- **Index-only scan**: feature-complete for `.btree`-only, single-column-key
  indexes (composite index keys aren't supported at all yet — `IndexInfo`
  is single-column-key only). Gated by `IndexInfo.covering_storage` (NOT
  `included_columns.len > 0` — that flag alone would misparse legacy
  row_key-only leaves as covering entries). `REINDEX` cannot upgrade an
  existing INCLUDE index into covering storage either (same new-indexes-
  only gap as GIN).
- **Bitmap index scan**: feature-complete for single-table flat AND/OR
  indexed-equality predicates over `.btree` indexes only. Explicitly out of
  scope: joins, mixed AND-of-OR/OR-of-AND trees, non-btree leaves,
  interaction with covering storage. Data structure: `RowKeySet`
  (`src/sql/bitmap.zig`) — sorted/deduped owned `row_key` copies, two-
  pointer O(n+m) intersect/union. A real, independent, user-facing
  correctness bug was found and fixed as a prerequisite (issue #128):
  non-unique `.btree` indexes rejected inserting a second row with a
  duplicate indexed value at all.
- **MATCH_RECOGNIZE** (SQL:2016 row pattern matching): all 7 phases done,
  feature-complete for realistic single-table use (PARTITION BY/ORDER BY/
  MEASURES/ONE OR ALL ROWS PER MATCH/AFTER MATCH SKIP/PATTERN with
  concat+alternation+grouping+`+`/`*`/`?`/DEFINE with PREV/NEXT/FIRST/LAST/
  MATCH_NUMBER/CLASSIFIER). A pure backtracking matcher lives in
  `src/sql/pattern_match.zig`, zero dependency on `Row`/`Value`/`Database`.
  Explicitly deferred: SUBSET, PERMUTE, exclusion syntax, reluctant/bounded
  quantifiers, `^`/`$` anchors, SKIP TO FIRST/LAST, WITH UNMATCHED ROWS.
  Known non-standard deviation: clause order (ORDER BY/MEASURES/ROWS-PER-
  MATCH/AFTER-MATCH-SKIP) was implemented as flexible-order rather than the
  SQL:2016-mandated fixed order — accepted as a safe permissive superset,
  not reverted; revisit if strict-spec conformance is ever required.
- **Replication real I/O**: sender/receiver/transport phases 1-3 of 5 are
  done (LSN type + raw-frame read API, real TCP transport reusing the
  server's thread-per-connection model, sender reads real WAL frames).
  Phase 4 (receiver applies real frames to its own local WAL+Pager,
  crash-safe via the existing `Wal.recover()`/`checkpoint()` path) and
  phase 5 (end-to-end loopback integration test) were not done as of the
  last architecture note — cross-check current git history, this may have
  progressed since.

## zuda / sailor migration notes

- Deadlock detection (`lock.zig`) migrated to `zuda.algorithms.graph
  .cycle_detection` — done.
- B+Tree: **not migrating** — disk-backed with WAL/MVCC integration; zuda's
  BTree is memory-only. Architect-reviewed, standing decision.
- Buffer pool LRU: **contradictory status in the repo's own memory** — see
  `context.md`'s Open questions. Treat as unresolved until verified against
  `src/storage/buffer_pool.zig` directly.
