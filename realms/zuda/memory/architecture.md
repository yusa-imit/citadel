# zuda — architecture

_(migrated from the repo's former `.claude/memory/architecture.md`, 2026-09-05)_

## Module organization

```
zuda (root.zig -- re-exports all public types)
+-- containers/
|   +-- lists/          Sequential containers (SkipList, XorLinkedList, UnrolledLinkedList)
|   +-- trees/          Tree-based containers (RedBlackTree, AVLTree, BTree, Trie, ...)
|   +-- heaps/          Heap variants (FibonacciHeap, BinomialHeap, PairingHeap, DaryHeap)
|   +-- hashing/        Hash containers (CuckooHashMap, RobinHoodHashMap, SwissTable)
|   +-- queues/         Queue variants (Deque, StealingQueue)
|   +-- graphs/         Graph representations (AdjacencyList, AdjacencyMatrix, CSR)
|   +-- strings/        String structures (SuffixArray, SuffixTree, DoubleArrayTrie)
|   +-- spatial/        Spatial indices (KDTree, RTree, QuadTree, OctTree)
|   +-- probabilistic/  Probabilistic (BloomFilter, CountMinSketch, HyperLogLog)
+-- algorithms/
|   +-- sorting/        Sorting algorithms on []T slices
|   +-- searching/      Search algorithms
|   +-- graph/          Graph algorithms (generic over Graph concept)
|   +-- string/         String matching algorithms
|   +-- math/           Number theory, combinatorics
|   +-- geometry/       Computational geometry
|   +-- dynamic_programming/
+-- iterators/          Composable iterator adaptors
+-- internal/           testing.zig, bench.zig (not public)
```

(Grown considerably since this was written -- see `REALM.md` Layout for the current, much
larger module list: `ndarray/`, `linalg/`, `stats/`, `signal/`, `numeric/`, `optimize/`,
`compat/`, `ffi/` were all added later under the v2.0 scientific-computing track.)

## Key design decisions

### Allocator-first pattern
Every heap-allocating container accepts `std.mem.Allocator`. Managed variants store the
allocator; Unmanaged variants require it per-call. Matches `std.ArrayListUnmanaged`.

### Comptime generics
All type parameterization happens at comptime. Comparators, hash functions, branching
factors -- no vtables, no runtime dispatch. Full monomorphization.

### Iterator protocol
Standard `next() -> ?T` pattern compatible with `while (iter.next()) |item|`. Iterators are
lazy and composable.

### Graph algorithm interface
Graph algorithms are generic over a duck-typed `Graph` concept via comptime. Any type
providing `.neighbors()` and `.nodeCount()` works.

### Complexity contracts
Every public function's doc comment states Big-O time and space. Verified via benchmark
regression tests.

### Double-array trie implementation (v1.8.0)
`DoubleArrayTrie(T)` uses the Aoe (1989) algorithm for space-efficient pattern storage:
- `BASE[state]` = transition base address or next unallocated state ID
- `CHECK[pos]` = parent state verification (`0xFFFFFFFF` marks empty slots)
- `is_leaf[state]` = separate array tracking pattern endings (no BASE negation)
- Current implementation uses naive 256-slot allocation per state for simplicity
- Future optimization: bitmap-based conflict resolution for 50-100x memory reduction
- Trade-off: construction O(|V| x |Sigma|) vs search O(1) per character

### SIMD BLAS auto-dispatch architecture (v2.0.x, session 496+)
Level 2 BLAS routines (gemv, trmv, trsv) include SIMD-optimized implementations with
auto-dispatch:

**File organization**:
- `src/linalg/blas.zig` -- public API, scalar implementations + dispatch logic
- `src/linalg/simd_blas.zig` -- SIMD-optimized implementations (`_simd` suffix)
- Import: `const simd_blas = @import("simd_blas.zig");` in blas.zig

**Dispatch pattern** (threshold: n >= 64):
```zig
pub fn trmv(...) !void {
    // ... validation ...
    const n = A.shape[0];
    if (n >= 64) {
        return try simd_blas.trmv_simd(...);  // SIMD path
    }
    // ... scalar fallback for n < 64 ...
}
```

**Implementations** (session 496-497):
1. `gemv_simd` (session 481) -- matrix-vector multiply: y = aAx + by
2. `trmv_simd` (session 496) -- triangular matrix-vector multiply: x = Ax
3. `trsv_simd` (session 497) -- triangular solve: Ax = b or A^T*x = b
4. `ger_simd` -- rank-1 update: A += axy^T

**SIMD vectorization mechanics**:
- Vector width: 4 for f64, 8 for f32 (256-bit SIMD, AVX/AVX2)
- Main loop: process `vec_width` elements using `@Vector(width, T)` + `@reduce(.Add, ...)`
- Tail loop: scalar for `n % vec_width` remainder
- Temporary buffers: used to preserve input during in-place operations (e.g. trsv, trmv)

**Performance characteristics**:
- Threshold n=64 chosen empirically (SIMD overhead ~= speedup at this point)
- Expected speedup: 2-4x over scalar for n >= 256
- Memory overhead: O(n) for temporary buffers
- Small matrices (n < 64): no performance regression (scalar path has lower overhead)
