# zuda — context

last_seen_at: 2026-11-13T00:00:00Z
rejected_plans: []

## Cycle 52 — 2026-11-13 — ABORTED (disk gate)
- Done: nothing. Disk gate read 16 GB free (needs >= 20), stopped in preflight. Repo untouched: main, clean
  (c24c7f3, #89 merged in cycle 50). Mode would have been FEATURE (n=52, no stabilize_streak).
- PRs: none open from this realm; GitHub inbox/CI not read this cycle (gate stopped before step 5).
- Next: assertion baseline for `blas.zig`, `ndarray.zig`, distributions sampling; aggregators 8; ML 34;
  `//!` headers graph 21, string 18, trees 14, dp 44, ML 67; `BlockSort` stores its allocator; v3.0.0 release.
- Blockers: disk (16 GB free; realm caches are small, space is held elsewhere on the machine). Needs the
  operator to free ~4 GB+; the realm cannot fix it. Disk aborts so far: cycles 3, 33, 41, 46, 47, 49, 51, 52.
- Open questions: none. stabilize_streak: 0 (no file).
- Quirks: the guard blocks any Bash call that mixes a `/tmp` write or `date`/`$START` setup with citadel
  paths: read citadel files with the Read tool and run `df`/`date` in their own calls.

## Cycle 50 — 2026-11-11 — STABILIZATION (n % 5)
- Done: disk gate passed (22 GB). CI green on main, no bugs, inbox clean (no OWNER comments). Merged #88
  (BLAS compile + 917 tests, 7/7, no `hold`), labelled `auto-merged`.
- PR #89 `fix/blocksort-oom-error`: `BlockSort.sort` swallowed OOM (`catch return`/`continue`) and could return
  a half-sorted slice silently. Failing-allocator test (fail index 0..7: sorted or `error.OutOfMemory`) written
  first; `sort` now `error{OutOfMemory}!void`, run list compacted in place so only `findRuns` allocates.
  Breaking (CHANGELOG, v3.0.0). Full `zig build test` exit 0 (~3 min warm), CI 7/7, merged, `auto-merged`.
- Next: assertion baseline for `blas.zig`, `ndarray.zig`, distributions sampling; aggregators 8; ML 34;
  `//!` headers graph 21, string 18, trees 14, dp 44, ML 67; `BlockSort` still stores its allocator (header
  says so); v3.0.0 release.
- Blockers: none. Open questions: none. stabilize_streak: 0 (no file).
- Quirks: the guard blocks `cd <repo> && ...` and `cd` + `;` chains: run repo commands from the cwd. CI cross
  jobs finished ~17 min after the PR opened; the cycle used 18 of 22 min.

## Cycles 49, 51 (2026-11-10, 11-12), folded: ABORTED at the disk gate
- Disk read 15-16 GB free (needs >= 20), stopped in preflight; repo untouched, clean; inbox and CI not
  read. Cycle 49 left #88 open (merged in cycle 50). Resume list: see cycle 52.

## Cycle 48 — 2026-11-09 — FEATURE
- Done: disk gate passed (24 GB). Inbox clean (CI green on 4a6e772, no bugs, no OWNER comments, milestone #31).
  Sweep slice `linalg/blas.zig` + `simd_blas.zig` (the blocker of the "assertion baseline" item): 77 compile
  errors fixed (error sets missing OutOfMemory/NotSquare, runtime vector index -> `inline for`, `for (arr) |*v|`
  needs `&arr`, `rotmg` not an error union, `math.isInf`, dispatch to a nonexistent `syr2_simd` removed, local
  `cloneArray` since NDArray has no clone). Both files wired into the `root.zig` test block: 917 tests pass.
- Real bug: `rotg` overflowed/underflowed at 1e200/1e-200 (c=0, s=inf), now scaled. 40 of 49 red tests had
  wrong expectations (rot signs, band storage, hand sums, zero-length NDArray is unrepresentable, `fromSlice`
  length != prod(shape) gives CapacityExceeded). `syrk` mirrors the opposite triangle (netlib leaves it).
- PR: #88 `fix/compile-clean-blas-zig-016` open; local `zig build test` exit 0, Build & Test green (7m13s);
  3 of 6 cross-compile jobs pending at the deadline. Next cycle merges at 7/7, no `hold`, adds `auto-merged`.
- Next: merge #88; then assertion baseline for `blas.zig` (now unblocked), `ndarray.zig`, distributions sampling;
  aggregators 8; ML 34; headers graph 21, string 18, trees 14, dp 44, ML 67; blocksort OOM swallow; v3.0.0.
- Blockers: none. Open questions: none. stabilize_streak: 0 (no file).
- Quirks: 3 sonnet agents (one slice per BLAS level, failing-test lists in the brief) cost ~$0.9 and finished in
  ~3 min each; two used whole-file python rewrites on the shared files, nothing was lost (full 917 re-run
  green). The guard blocks `cd <repo> && ...` chains. Full-suite blas run takes ~2 min warm.

## Cycles 46-47 (2026-11-07..08, folded 2026-11-09)
- Both ABORTED by the disk gate (17-18 GB free, needs >= 20; with 3, 33, 41 that is five aborts). Realm caches
  are small (~750 MB), the space was held elsewhere; it recovered by 48 (24 GB).

## Cycles 43-45 (2026-11-04..06, folded 2026-11-10)
- 43 linalg sweep (#85, 443 tests): svd sign bug (now one-sided Jacobi), eig QR (now cyclic Jacobi),
  `solveOverdetermined` double free; many wrong tests. 44 iterators sweep (#86, 281 tests): flat_map helpers
  returned slices of their own stack frames (now comptime tables). 45 STABILIZATION (#87): `//!` headers on
  18 sorting files, `zig fmt` applied; missing header now 259 of 436. All merged at 7/7, `auto-merged`.
- Noticed, not fixed: `blocksort.zig` `sort` swallows OOM (`catch continue` / `catch return` on run-list
  appends), so it can return unsorted without an error: needs a failing test, then a typed error.
- Quirks: stale `.zig-cache` "failed to spawn build runner": use `--cache-dir /tmp/zuda-zcache`. Run
  `zig fmt` after bulk edits and `git checkout` unrelated files it reformats. The guard blocks
  `cd <repo> && ...` chains. A leaking test aborts the whole `zig test` run (ABRT): fix leaks first.
  `zig test` on a file importing `linalg/*` needs `--test-filter "linalg."` and a `_sweep_*.zig` root.

## Cycles 41-42 (2026-11-02..03, folded 2026-11-06)
- 41 ABORTED by the disk gate; 42 was the first linalg pass (finished in #85). Quirk: `zig test` on a file
  importing `linalg/*` runs the whole suite: pass `--test-filter "linalg."`, use a `_sweep_*.zig` root.

## Cycles 39-40 (2026-10-31..11-01, folded 2026-11-05)
- 39 (#82 compression, 8 of 11 files red): delta unsigned overflow, lz77 stray byte/no overlap, lzss
  `u3` flag overflow and 12-bit offset (window 4095), snappy lost data on matches > 64, `rle.wouldCompress`
  wrong element. `deflate` only does stored blocks (docs honest). 40 (STABILIZATION): merged #82, #83 (README
  claims match code), #84 (compression `//!` headers). Audit: `catch unreachable` in library 0 unproven,
  `@panic` 0, `std.debug.print` 1 (RBT test errdefer). Missing `//!` header: 277 of 436 files (ML 67, dp 44,
  graph 21, string 18, sorting 18, trees 14).
- Quirks: `zig fmt --check src` is red on ~126 pre-existing files (CI does not run fmt): format only the
  slice you touch. A header is a prepend (`//! ` prefix, blank line after, <= 100 columns); `zig test
  -fno-emit-bin <file>` is a 20 s compile check for comment-only edits.

## Cycles 36-38 (2026-10-28..30, folded 2026-11-03)
- 38 (#81 containers/trees, 15 files, 8 were red): `WaveletTree.rank0` subtracted all set bits, not
  those before `i`; `RadixTree` iterators read `frame.node` after `stack.pop()` (0.16 poisons the
  popped slot: read before pop); `VanEmdeBoasTree` sized clusters by sqrt(u), wrong for odd log2(u).
- 36 (#79 geometry) and 37 (#80 sorting) merged at 7/7, `auto-merged`. Real bugs: Bentley-Ottmann
  use-after-free and wrong status (rewritten as active-set sweep), ear clipping through a reflex
  vertex, `strandSort` unstable ties; 22 of 23 sorting files were only reachable via `pub const`.
- Quirks: the guard blocks chaining `cd` with `perl -pi`/`cat >` writes and mixing `/tmp` writes with
  citadel paths; keep them in separate Bash calls. Perl `s///` eats `@as(`/`@divExact` (escape `\@`).
  `perl -pi script.pl a b c` keeps state across files: run once per file. Cross-compile CI jobs
  queue ~10 min after Build & Test (9 min); whole cycle to PR ~10 min, so open the PR by minute ~11.

## Cycles 34-35 (2026-10-26..27, folded 2026-11-01)
- 34 (#76 string, 12 files ported; 8 wired): `longestCommonPrefixDivideConquer` returned a view of
  its input; `lzw` leaked dictionary keys and double-freed `previous`; `trie`/`manacher` leaked.
  Compile-clean but UNWIRED (their never-run tests fail, real bugs; fix each with TDD, then wire):
  `boyer_moore` (hangs), `kmp` (`count` 3 not 2), `trie` (delete/size), `suffix_array` (search
  finds 0), `manacher` (overflow panic), `metaphone`, `soundex`, `damerau_levenshtein`,
  `jaro_winkler` (prefix length 4), `lzw` (ratio). Run per-file tests under `perl -e 'alarm 90; exec @ARGV'`.
- 35 (STABILIZATION, #77 #78): subnormal `nu`/`beta` passed `init` but made `sample()` panic on
  `Gamma.init(...) catch unreachable` in StudentT, F, SkewT, GeneralizedNormal,
  HalfGeneralizedNormal; `init` rejects them. Look two lines up for a proof comment when scanning.

## Cycles 30-33 (2026-10-20..23, folded 2026-11-06)
- 30: #74 proof comments on 21 `catch unreachable` sites. 33 ABORTED by the disk gate. 31-32 merged #75
  (btree, adjacency_list, topological_sort, compat shims) and #76 (graph, bitwise, combinatorics, dp).
- Sweep method: ONE scratch root per file `src/_sweep_J.zig` = `test { _ = @import("rel/x.zig"); }`,
  `zig test -fno-emit-bin` with per-job `--cache-dir`/`--global-cache-dir`. Cost lesson: 4 parallel sonnet
  agents burned ~$2.2 in ~6 min; do mechanical edits with perl directly. Delete `src/_sweep*` before commit.
  dp still red: max_sum_rectangle, scramble_string, stock_trading, subset_sum, target_sum.

## Cycles 10-29 (2026-10-01..19, folded 2026-11-06)
All merged by squash with 7/7 checks, labeled `auto-merged`.
- 10-15: seed injection finished (ADR 0001 D1); time -> `Io.Clock` (#49); tidy baseline to `tools/` (#50);
  `deque.zig` tests found never running (#54). Recurring cause: files reached only via nested `pub const`
  re-exports are invisible to `refAllDecls` (issue #38): probe with a scratch `src/scratch.zig` and wire
  fixed files into the test block.
- 16-17 (bugs #53, #57): `AhoCorasickASCII.findFirst` test was wrong; ILU init double free; a REAL GMRES
  bug (lucky breakdown `h(j+1,j)~0` exited before rotating col j, x never updated); CG read `norm2(r)`
  after `free(r)`; zero pivot is `error.SingularMatrix`; ILU(0) asserts ascending CSR columns
  (`CSR.fromCOO` does NOT sort). Question #56 went unanswered; option 1 (big-bang 0.16 flip) taken.
- 18-19: #60 flip to 0.16.0 + ndarray `Io.Dir`/`Io.Mutex`; #61 `mem.indexOf*` -> `find*`; #62
  backtracking compiles (kept `wip/fix-backtracking-0.16-compile-20261008`); OOM harness found leaks in
  six files (bug #63).
- 20-26: #64 OOM leaks in palindrome_partition, knights_tour, combination_sum, permutations, subsets,
  n_queens; ported `nfa`, `matrix_chain`, `ford_fulkerson`, `bogosort` (#65-#66), `kmeans`/`gmm`/`dqn`/
  `ddpg`/`tsne` per ADR 0001 D1 (#67), `approximation/*`, `greedy/*`, `automata/dfa`, `graph_coloring/*`
  (#68, `dsatur` infinite loop on isolated vertices; kept `wip/compile-clean-greedy-automata-approx-
  20261014`); user-data asserts became typed errors (#69: `vertex_cover` `InvalidEdge`, `knapsack`,
  `bin_packing` `InvalidInput`, v3.0.0 break in CHANGELOG); #70 `WorkStealingDeque`, `parallel_sort`
  (rewritten), `prefix_sum` fixed and wired.
- 27-29: #71 `map_reduce.zig` redesigned (bounded `EmitterType`, `PairsLimitExceeded`, stable sort);
  #72 `internal/testing.zig` seeds from `std.testing.random_seed`, `internal/bench.zig` fixed (warmup,
  `MemoryTracker.reset`); #73 `red_black_tree.zig` assertion baseline. `linalg/blas.zig` had 77 errors on
  0.16 (finished in #85).
- Leftovers: `preconditioner.zig` init (135 lines), `bagging.zig` fit (73), 3-4 type-fn tidy baseline
  entries grew (Cuckoo/RobinHood/ConcurrentSkipList/ILUPreconditioner), `greedy_coloring` Tiger cleanup,
  DFA stores an allocator, `hamiltonian.zig` not OOM-audited, `dinic`/`edmonds_karp` not in the test
  graph, `Benchmark` stores its allocator, `generateUniqueRandomIntegers` unbounded loop, deque resize
  concurrent with steal still unsafe (documented in header).
- Quirks: `zig` on PATH is 0.15.2, use `/Users/fn/.zr/toolchains/zig/0.16.0/zig`; stale `.zig-cache`
  gives "failed to spawn build runner: FileNotFound" (use `--cache-dir /tmp/zuda-zcache`); `zig build test`
  prints "failed command" noise yet exits 0; BSD sed lacks `\n` (use `perl -0pi`, escape `\@`); zsh has no
  PIPESTATUS; no `timeout` binary; CI Build & Test 7-9.5 min, cross-compile jobs queue late (>15 min), so
  open the PR by minute ~8 and never poll `gh pr checks` in a foreground loop (600 s tool cap).

## History (cycles 0-9, folded 2026-09-17 to keep this file under 200 lines)
Realm created 2026-09-05; plan 001 (Zig 0.16 migration) merged, milestone issue #31 opened.
Cycles 1-5: fixed the preserved RandomForest MSE-criterion bug, vendored `zig build tidy`,
merged `build.zig` linkLibC fix, dual-compatible mechanical renames, added the missing LICENSE.
Cycle 6 (FEATURE): `architect` wrote `docs/adr/0001-io-injection-and-seed-determinism.md` — the
basis for every seed-injection PR since: clock-derived PRNG seeds become a required
`seed: u64` option (never `io` itself); `io` is never stored in a container;
`Io.Mutex.lockUncancelable` keeps `error.Canceled` out of container error sets.
`bloom_filter.zig` needed no public-API change (PR #37). Cycle 7 (STABILIZATION, forced by bug
#38): fixed a real ConcurrentSkipList `remove()` leak with reader-count-quiescence + bounded
retire list (PR #40) — the node can't free immediately after unlink since lock-free readers may
hold raw pointers into it. This is also where issue #38's root cause was found: `root.zig`'s
`refAllDecls` is non-recursive, so any container reached only through a nested pub-const
re-export (`compat/*`, `utils/builder.zig`, `containers/lists/concurrent_skip_list.zig`, etc.)
has its tests silently invisible to `zig build test` — recurring theme through cycle 12's #44/
#46. Cycles 8-9 (FEATURE): applied the ADR 0001 D1 seed-injection shape to
`robin_hood_hash_map.zig` (PR #41) and `cuckoo_hash_map.zig` (PR #42) — required `Options{ seed:
u64 }` at init, no default, stored `prng` field drawn from instead of re-seeding from the clock
on every operation; `work_stealing_deque.zig` dropped from scope (zero time/crypto-random
sites). Each PR used a throwaway scratch driver to compile-check otherwise-unreachable call
sites (`builder.zig`, `hash.zig`) since CI wouldn't catch a break there.

Cycle 3: disk gate failed (16GB free), aborted before touching the repo (folded from the
cycles 0-4 history block, otherwise fully absorbed into cycles 0-9 above).
Still-open backlog folded here: `catch unreachable` OOM-swallow audit (69→60 sites); 2
leftover `p < 1e-300` f32-underflow sites in `distributions.zig`; ~20 deferred
`std.debug.assert` sites in `src/algorithms/`; `logFactorial` exact only for `n < 20`; a v2.4.0
release backfilling CHANGELOG 2.0.1-2.3.0 is still owed once plan 001 lands. Next distribution
vein (if catalog work resumes): Devroye (1993) discrete-stable triptych beyond Sibuya (209th),
discrete Mittag-Leffler next — always grep `pub fn <Name>` in `distributions.zig` first
(JohnsonSU, ExGaussian shipped as duplicates before).
