# silica — patterns

_(migrated from the repo's former `.claude/memory/patterns.md`, condensed —
snippets kept verbatim where they're precise Zig 0.15.2 API shapes)_

## Allocator patterns

Transaction-scoped arena:
```zig
var arena = std.heap.ArenaAllocator.init(backing_allocator);
defer arena.deinit();
const alloc = arena.allocator();
// All transaction allocations use `alloc` — freed on commit/rollback
```

Testing with leak detection:
```zig
test "no leaks" {
    const allocator = std.testing.allocator;
    var obj = try MyStruct.init(allocator);
    defer obj.deinit();
}
```

## Resource safety patterns

Pin/unpin for buffer pool pages:
```zig
const frame = try pool.fetchPage(page_num);
defer pool.unpinPage(page_num, false); // unpin on exit
```

File handle safety:
```zig
const file = try std.fs.cwd().openFile(path, .{});
defer file.close();
```

## Database patterns — VERIFIED

Page checksum (CRC32C):
```zig
const Crc32c = std.hash.crc.Crc32Iscsi;  // Zig 0.15 API
const crc = Crc32c.hash(buf[PAGE_HEADER_SIZE..page_size]);
std.mem.writeInt(u32, buf[12..16], crc, .little);
```

Pager alloc/write/read:
```zig
var pager = try Pager.init(allocator, path, .{});
defer pager.deinit();
const page_id = try pager.allocPage();
const buf = try pager.allocPageBuf();
defer pager.freePageBuf(buf);
@memset(buf, 0);
header.serialize(buf[0..PAGE_HEADER_SIZE]);
try pager.writePage(page_id, buf);  // auto-checksums
try pager.readPage(page_id, buf);   // auto-verifies checksum
```

Zig 0.15 build pattern:
```zig
const mod = b.addModule("silica", .{
    .root_source_file = b.path("src/main.zig"),
    .target = target, .optimize = optimize,
});
const lib = b.addLibrary(.{ .name = "silica", .root_module = mod, .linkage = .static });
const tests = b.addTest(.{ .root_module = mod });
```

Buffer pool pin/unpin (zuda `LRUCache` — see `decisions.md`'s contested
status before trusting this is the current implementation):
```zig
var pool = try buffer_pool.BufferPool.init(allocator, &pager, 0); // 0 = default 2000
defer pool.deinit();
const frame = try pool.fetchPage(page_id);
defer pool.unpinPage(page_id, false);
frame.markDirty(); // or pass dirty=true to unpinPage
// New pages: fetchNewPage(new_pid) is already dirty; unpinPage(new_pid, true); flushAll()
// Internal: zuda.containers.cache.LRUCache(u32, u32, AutoContext, null) if migrated,
// tracking unpinned page_id -> frame_index; getEvictableFrame() = oldest unpinned.
```

B+Tree usage:
```zig
var tree = btree.BTree.init(&pool, root_id);
try tree.insert("key", "value");
const val = try tree.get(allocator, "key"); // owned slice or null
if (val) |v| defer allocator.free(v);
try tree.delete("key");
// tree.root_page_id may change after insert (root split)
```

B+Tree page layout (slotted page design, cells grow from page end
backward, cell pointers are u16 offsets sorted by key order):
- Leaf: `[PageHeader 16B][prev_leaf 4B][next_leaf 4B][cell_ptrs...] ...
  [cells<-]`
- Internal: `[PageHeader 16B][right_child 4B][cell_ptrs...] ... [cells<-]`
- Leaf cell: `[key_len varint][key_data][value_len varint][value_data]`
- Internal cell: `[left_child u32 LE][key_len varint][key_data]`

`@memcpy` aliasing — panics if src/dst overlap:
- `std.mem.copyForwards` when dst < src (deleting/shifting left)
- `std.mem.copyBackwards` when dst > src (inserting/shifting right)

Lock Manager:
```zig
var lm = LockManager.init(allocator);
defer lm.deinit();
const target = LockTarget{ .table_page_id = 5, .row_key = 100 };
try lm.acquireRowLock(xid, target, .exclusive);
defer lm.releaseRowLock(xid, target);
try lm.acquireTableLock(xid, table_page_id, .row_exclusive);
lm.releaseAllLocks(xid); // on transaction end
if (lm.hasConflict(xid, target, .exclusive)) return error.LockConflict;
```
Conflict rules: shared locks share; exclusive conflicts with all; upgrade
shared->exclusive only if sole holder; table locks follow the PostgreSQL
7-mode conflict matrix.

Zig 0.15 `ArrayList`:
```zig
var list = std.ArrayList(u8){}; // NOT ArrayList.init(allocator)
defer list.deinit(allocator);   // deinit takes allocator
try list.append(allocator, value);
const slice = try list.toOwnedSlice(allocator);
```

`std.Thread.Mutex`:
```zig
var mutex = std.Thread.Mutex{};
{ mutex.lock(); defer mutex.unlock(); /* protected code */ }
```

Zig 0.15.2 thread sleep — **nanoseconds**, not milliseconds:
```zig
std.Thread.sleep(100); // 100 nanoseconds — CORRECT for 0.15.2
// std.time.sleep does not exist in 0.15.2 — do not use it
```

GiST operator-class interface:
```zig
pub const OpClass = struct {
    consistent: *const fn (allocator, entry_pred: []const u8, query: []const u8,
        strategy: u8) Error!bool,
    union_fn: *const fn (allocator, entries: []const []const u8) Error![]u8,
    penalty: *const fn (allocator, current_pred: []const u8, new_pred: []const u8) Error!u64,
    picksplit: *const fn (allocator, entries: []const []const u8)
        Error!struct { group_a: []usize, group_b: []usize },
    same: *const fn (allocator, pred_a: []const u8, pred_b: []const u8) Error!bool,
};
```
GiST page layout mirrors B+Tree's slotted design: leaf entries are
`[pred_size u16][tuple_id u32]` (6B fixed header) + variable predicate
stored from page end backward; internal entries substitute `child_id` for
`tuple_id`.

## Stress-testing shape (used across lock/buffer-pool/WAL stress tests)

```zig
test "concurrent stress test" {
    const allocator = std.testing.allocator;
    var manager = SlotManager.init(allocator);
    defer manager.deinit();
    var threads: [10]std.Thread = undefined;
    for (&threads) |*t| t.* = try std.Thread.spawn(.{}, workerFunction, .{&manager});
    for (threads) |t| t.join();
    // Verify final state consistency
}
```
Sequential lifecycle stress tests must clean up between iterations (e.g.
`coordinator.cleanup()` each loop) or state leaks across the whole run.

<!-- Add new patterns as they are verified through implementation -->
