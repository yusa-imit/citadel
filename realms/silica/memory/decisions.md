# silica — decisions

_(migrated from the repo's former `.claude/memory/decisions.md`, condensed)_

> Format: Context | Decision | Rationale | Consequences

## Language — Zig
Need an embedded DB with no hidden allocations, C ABI interop,
cross-compilation. Chose Zig (0.15.x at last check; kingdom-wide target is
0.16.0 under plan `001`). Rationale: explicit memory control, comptime
metaprogramming, zero-overhead C FFI, no GC. Consequence: smaller ecosystem
than C/Rust, must track Zig releases closely (see the 0.16 probe in
`STATE.md` — non-trivial migration).

## File format — single-file, SQLite-style
Need simple deployment/backup for embedded use. Single database file, fixed-
size pages, magic `"SLCA"`. Rationale: SQLite's single-file model is proven
for embeddability. Consequence: WAL file is separate; page-level locking
must be careful.

## B+Tree as primary index structure
Need efficient point lookups and range scans. B+Tree with doubly-linked
leaf pages. Rationale: standard for OLTP; leaf links enable fast range
scans. Consequence: must handle splits/merges/overflow pages correctly.

## Buffer pool LRU — keep custom, do not migrate to zuda (session 27)
zuda provided `LRUCache` with pin/unpin. Evaluated replacing the custom
buffer-pool LRU with it. **Decision: do not migrate.** Four blockers: (1)
zuda's eviction callback is non-failable (`void`), but dirty-page flush can
fail — silent data-loss risk; (2) per-entry heap allocation vs. silica's
pre-allocated frame array — unacceptable allocation churn in the hot path;
(3) `BufferFrame.data` is directly accessed as raw `[]u8` by 12+ files — an
adapter layer would add overhead to every B+Tree operation; (4) the
replaceable LRU logic is only ~30 lines, not worth the coupling. Reviewed
by the architect agent, session 27.

**Caveat carried forward, unresolved**: a later note (session 46,
`architecture.md`) claims the opposite — that the buffer pool LRU *was*
migrated to `zuda.containers.cache.LRUCache(u32, u32, AutoContext, null)`,
with all tests green. The two notes were never reconciled in the source
repo's memory. **Read `src/storage/buffer_pool.zig` directly before relying
on either claim.**

## zuda-first policy — exceptions
General kingdom rule: check zuda before writing new infra, file a zuda
issue rather than build a local workaround. Silica's standing exceptions:
buffer pool (see above, contested) and the B+Tree itself (disk-backed with
deep WAL/MVCC integration; zuda's containers are in-memory only — not a
fit, and not worth an adapter layer per the same 12+-files-touch-raw-data
argument as the buffer pool).

## Version safety (release policy)
Versions are monotonic and never skip. A minor release is always current
`build.zig.zon` version + 1 minor, even if a milestone doc pre-assigned a
different number — milestones are tracked by theme/name, not by a
pre-reserved version. A patch release is tag-only (no `build.zig.zon`
bump) and must never carry feature commits, only fixes.

<!-- Add new decisions above this line -->
