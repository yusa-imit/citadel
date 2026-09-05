# silica — debugging

_(migrated from the repo's former `.claude/memory/debugging.md`, condensed —
resolved ancient history like the session-258/265-267 GIN-page-layout and
test-suite-hang sagas is dropped; both are long fixed and superseded by the
current ~4,900-test, ~50s-green suite. Kept: still-relevant architecture
gotchas, unresolved items, and precise Zig-version facts.)_

## Closed but instructive: SAVEPOINT rollback didn't survive COMMIT (#125)

`ROLLBACK TO SAVEPOINT` + `COMMIT` silently un-did nothing — rolled-back
rows reappeared post-commit. Root cause: `rollbackToSavepoint` only reset
the transaction's CID counter; tuple-visibility hiding via the own-xid CID
rule (`isTupleVisibleWithTm`) only applies while the transaction is still
open — once it commits, the xid is globally visible and CID comparisons
never apply again. Fixed via a physical undo log (`UndoRecord`,
`TransactionContext.undo_log`, `Savepoint.undo_len` watermark,
`Database.recordUndo()`/`replayUndoTo()`) wired into every mutation path
(INSERT/DELETE/UPDATE/ON CONFLICT/MERGE), with `rollbackToSavepoint` calling
`replayUndoTo(txn, saved_undo_len)`. **Closed per session-507 memory** — not
reconfirmed in this restructure; if savepoint-adjacent bugs resurface, this
undo-log mechanism is where to look first.

**General lesson**: any SAVEPOINT/ROLLBACK test that never SELECTs the data
back afterward can hide this entire class of bug — assert on read-back
state, not just "the statement didn't error."

## Closed but instructive: column-level UNIQUE never enforced (#126)

`CREATE TABLE t (id INTEGER UNIQUE)` parsed `UNIQUE` into
`ColumnInfo.flags.unique` but `Catalog.createTableFromAst` only
auto-created a secondary index for `PRIMARY KEY`, never `UNIQUE` — so
nothing enforced it and duplicates inserted silently. Table-level
`UNIQUE (col1, col2, ...)` had the same gap. Workaround was an explicit
`CREATE UNIQUE INDEX`. **Closed per session-507 memory** — not reconfirmed;
if a UNIQUE-adjacent bug resurfaces, check whether table-level
`UNIQUE (...)` (as opposed to inline column `UNIQUE`) got the same fix.

## Recurring operational gotcha: host disk fills from `.zig-cache`

This host runs cron for 5 sibling Zig projects (silica, sailor, zuda, zr,
zoltraak), each accumulating `.zig-cache` unboundedly — one session hit
120Mi free out of 228Gi, ~71G of which was `.zig-cache/o` across all 5.
Any disk-writing tool (build, git, subagent I/O) can fail with `ENOSPC`.
Fix: `rm -rf .zig-cache` in the affected project only (gitignored,
regenerates on next `zig build` — this is the documented "Clean" command).
Diagnose with `df -h /` then `du -sh ~/codespace/*/.zig-cache`; only clean
silica's own cache unless explicitly asked to touch siblings.

## Unresolved: flaky test-order-dependent leak in optimizer/ast arena

`zig build test` intermittently (seen 1-in-3 runs) reports a GPA leak
inside `optimizer.zig:optimizeProject` → `ast.zig create` (arena-backed
`PlanNode` allocation), surfacing as the failure of an unrelated test
because Zig's randomized test order changes adjacency. Ruled out: not
caused by any specific recent file (reproduced with candidate files both
present and absent). Hypothesis, not confirmed: some execution path with a
`Project` node has a `try`/early-return between an arena `create()` call
and its matching cleanup, only hit under specific interleavings. Seed
`0x99f2cabb` reproduced it once — try that seed first when chasing this in
a stabilization session. Not blocking (CI green, most runs clean).

## Architectural: no safe multi-connection support (carried from session 40)

See `memory/architecture.md`'s Concurrency limitation section — same
finding, not reconfirmed since. Root mechanism: per-`Database.open()`
buffer pool + WAL instances, shared TransactionManager only.

## Architectural: MVCC UPDATE is delete+insert, not version chains

Concurrent readers can see `NoRows` for a row mid-UPDATE: `tree.delete()`
physically removes the old tuple, `tree.insert()` writes the new one with
an as-yet-uncommitted `xmin` — so between those two calls (and until the
new tuple's transaction commits and is visible), the row exists in neither
its old nor new form for a concurrent snapshot. SSI (`SsiTracker`,
`mvcc.zig`) is fully implemented and correct; the failures in this class
are a storage-architecture limitation, not an SSI bug. Real fix needs
version chains / delayed deletion / VACUUM-style reclamation — v2.0 scope,
tracked in `STATE.md`'s Next work candidates.

Related, already fixed (kept for the pattern, not the specific bug): a lost
update in READ COMMITTED where `UPDATE` evaluated assignment expressions
against a value read *before* lock acquisition — fixed by re-reading the
row from the B+Tree immediately after acquiring the row lock, before
evaluating assignment expressions. **Pattern**: always re-read under lock,
never trust a pre-lock snapshot for a value you're about to write back.

## Not a bug: `global_tm_registry` "leaks" in tests

`zig build test` can report ~6 leaked allocations in `SharedTmRegistry`
(`path_copy`, `TransactionManager`, `active_txns` HashMap). This is
intentional: the registry must persist across connection cycles for MVCC
correctness (if destroyed at refcount 0, new connections would restart at
XID=1). `release()` deliberately does not free at refcount 0; only process
exit or an explicit `cleanupGlobalTmRegistry()` call frees it. Production
CLI/server use long-lived allocators where this never triggers a leak
alarm — this is a test-harness-only artifact. Do not "fix" it by using
`page_allocator` (breaks ANALYZE tests, allocator mismatch) or a separate
GPA per registry (creates far more leaks, not fewer).

## Zig-version-specific facts (verified, keep verbatim)

- **Build API (0.15)**: `addStaticLibrary` is gone — use `b.addModule()` +
  `b.addLibrary(.{ .root_module = mod, .linkage = .static })`. `addTest`
  takes `.root_module`, not `.root_source_file`.
- **CRC32 (0.15)**: `Crc32WithPoly(.Castagnoli)` is gone — use
  `std.hash.crc.Crc32Iscsi` (CRC32C = Castagnoli = iSCSI).
- **`build.zig.zon` fingerprint**: Zig 0.14+ requires a top-level
  `fingerprint` field — use the value Zig's own error message suggests.
- `std.testing.allocator` detects leaks — always use it in tests.
- `@memcpy` panics on overlapping regions; for overlapping in-place shifts
  use `std.mem.copyForwards` (dst < src) or `std.mem.copyBackwards`
  (dst > src) — see `memory/patterns.md` for the exact call shape.
- Integer overflow in page-number arithmetic — use `std.math.add` for
  checked arithmetic.
- `.name = .silica` — a plain identifier does not need `.name = .@"silica"`
  quoting in `build.zig.zon`.
- Zig 0.15 `ArrayList`/`ArrayListUnmanaged` are init'd as `.{}`, not
  `.init(allocator)`; `deinit`/`append`/etc. take the allocator explicitly
  as the first arg. (0.16 changes this again — see `STATE.md`'s probe.)
- `std.Thread.sleep` takes **nanoseconds** in 0.15.2; `std.time.sleep` does
  not exist in 0.15.2.

<!-- Add new debugging notes above this line -->
