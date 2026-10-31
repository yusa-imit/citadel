# zuda — context

last_seen_at: 2026-11-01T00:20:00Z
rejected_plans: []

## Cycle 40 — 2026-11-01 — STABILIZATION (periodic, n % 5 == 0)
- Done: merged #82 (compression sweep, 7/7, `auto-merged`). Audit: `catch unreachable` in library code
  0 unproven (the rest are in tests: `correlation.zig` 12, `lru_cache`, `crf`), `@panic` 0,
  `std.debug.print` 1 (seed-report `errdefer` in an RBT test). Missing `//!` header: 277 of 436 files
  (ML 67, dp 44, graph 21, string 18, sorting 18, trees 14). Docs drift fixed in README.
- PRs: #83 `docs/readme-claims-match-code` (Zig 0.16, 209 distributions, ~22k test blocks, install note
  v2.3.0=0.15.2 vs main=0.16.0, v2.0 roadmap ticked) and #84 `docs/compression-module-headers` (9 files).
  Both merged this cycle at 7/7 (~17 min after push), no `hold`, `auto-merged`.
- Next: `//!` headers slice by slice (ML 67 and dp 44 are the big ones); sweep: linalg 6, iterators 5,
  aggregators 8, ML 34 last; 10 unwired string files; 5 dp leftovers; v3.0.0.
- Blockers: none. Open questions: none. stabilize_streak: 0 (no file).
- Quirks: a header is a prepend, not a rewrite: `/tmp/zhdr.sh` style (`//! ` prefix, end with blank
  line); keep each line <= 100 columns (awk 'length>100' catches it). `zig test -fno-emit-bin <file>`
  is a 20 s compile check for comment-only edits. Guard blocks one Bash call that mixes `cd` into
  citadel with other commands: keep citadel reads in their own call.

## Cycle 39 — 2026-10-31 — FEATURE
- Done: inbox clean (CI green on bbf95d4, no bugs, no OWNER comments, milestone #31). Sweep slice
  `algorithms/compression`: 8 of 11 files red (bwt, deflate, delta, huffman, lz77, lzss, rle,
  snappy); all 11 now imported from the `root.zig` test block and pass. Real bugs: delta unsigned
  overflow (now wrapping), lz77 stray byte + no overlap + unchecked decode, lzss `u3` flag overflow
  and 4096 offset not fitting 12 bits (window capped at 4095), snappy lost data on matches > 64 and
  never emitted a copy after literals, `rle.wouldCompress` wrong element, `huffman.Node.right`
  type. `deflate` only does stored blocks (docs honest now, empty input valid, final block required).
- PR: #82 (`fix/compile-clean-compression-zig-016`) open; local full `zig build test` exit 0; Build &
  Test still running at the 22-min deadline. Cycle 40 merges at 7/7, no `hold`, adds `auto-merged`.
- Next: merge #82; linalg 6, iterators 5, aggregators 8, ML 34 last; 10 unwired string files; 5 dp
  leftovers; real fixed-Huffman deflate/inflate (stored only today); assertion baseline; v3.0.0.
- Blockers: none. Open questions: none. stabilize_streak: 0 (no file).
- Quirks: `zig fmt --check src` is red on ~126 pre-existing files (CI does not run fmt); format only
  the slice you touch (`zig fmt src/algorithms/<dir>`). Sweep scripts need `zsh`, run from repo root.

## Cycle 38 — 2026-10-30 — FEATURE
- Done: inbox clean (CI green, no bugs, no OWNER comments, milestone #31). Merged #80 (sorting, 7/7,
  `auto-merged`). Sweep slice `containers/trees`: 8 of 15 red (aa, avl, interval, radix,
  scapegoat, splay, trie, wavelet), fixed (`.empty`, unmanaged lists, `swapRemove` on
  `AutoArrayHashMapUnmanaged`); all 15 now imported from the `root.zig` test block.
  Real bugs: `WaveletTree.rank0` subtracted all set bits, not those before `i`; `RadixTree`
  `PrefixIterator`/`Iterator` read `frame.node` after `stack.pop()` (0.16 poisons the popped slot
  with 0xaa: read before pop); `VanEmdeBoasTree` sized clusters and summary by sqrt(u), wrong
  when log2(u) is odd (now `cluster_count = u / sqrt_u`, `u >= 2` comptime check).
- PR: #81 (`fix/compile-clean-trees-zig-016`) merged at 7/7, `auto-merged`.
- Next: compression (8 red: bwt, deflate, delta, huffman, lz77, lzss, rle, snappy; arithmetic,
  lz4, zstd compile clean, check if wired), linalg 6, iterators 5, ML 34 last; 10 unwired string
  files; 5 dp leftovers; assertion baseline; v3.0.0. Cycle 39 is FEATURE.
- Blockers: none. Open questions: none. stabilize_streak: 0 (no file).
- Quirks: perl `s///` with `@as(` eats `@as` (escape `\@`) — bit again; sweep scripts
  `/tmp/zsweep/run.sh` (compile) and `runtest.sh` (run tests) work, take rel path under src;
  CI Build&Test 9 min, cross-compile done ~17 min after push; whole cycle ~20 min.

## Cycles 36-37 (2026-10-28..29, folded 2026-10-31)
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

## Cycles 30-33 (2026-10-20..23, folded 2026-10-28)
- 30 (STABILIZATION): #74 proof comments on 21 `catch unreachable` sites; ~24
  `Gamma/StudentT/Lindley/GeneralizedNormal.init(self.param) catch unreachable` sites in
  `distributions.zig` need the owner's init validation as proof. No `chore` label in the repo.
- 33: ABORTED by the disk gate (16 GB free < 20 GB); nothing touched.
- 31-32:
  Merged #75 (btree, adjacency_list, topological_sort, silica/zr compat shims; BTree reverse
  iterator, shim ownership bugs) and #76 (graph 20, bitwise 4, combinatorics 8, dp 15 files).
- Sweep method: ONE scratch root per file, `src/_sweep_J.zig` = `test { _ = @import("rel/x.zig"); }`,
  `zig test -fno-emit-bin` with per-job `--cache-dir`/`--global-cache-dir` (`zig test <file>` cannot
  import across dirs). Red dirs then: ML 34, graph 20, dp 17, string 12, trees 8, geometry 8,
  compression 8, aggregators 8, linalg 6, sorting 6, iterators 5, then 1-3 each.
- Cost lesson: 4 parallel sonnet agents burned ~$2.2 in ~6 min; do mechanical `.{}` -> `.empty`
  with perl directly. Agents leave `src/_sweep*`; delete before commit. dp still red:
  max_sum_rectangle, scramble_string, stock_trading, subset_sum, target_sum.
- Quirks: `read -t` on /dev/null does not wait (use `perl -e 'select(undef,undef,undef,N)'`); the
  guard blocks `cd <repo>; ...` and `git push -u origin HEAD` chained after checkout.

## Cycles 27-29 (2026-10-17..19, condensed 2026-10-21)
- All merged by squash at 7/7 green, labeled `auto-merged`.
- 27 (#71): `map_reduce.zig` redesigned (bounded `EmitterType` with `pairs_max`/`PairsLimitExceeded`,
  comptime `key_order`, stable sort, results without a stored allocator); "Thread sync" item done.
- 28 (#72): `internal/testing.zig` seeds from `std.testing.random_seed`; `internal/bench.zig` fixed
  (warmup counted in memory stats; `MemoryTracker.reset` must keep live bytes). Leftovers:
  `Benchmark` stores its allocator and grows `times` after init, `generateUniqueRandomIntegers`
  unbounded loop, global `prng` with no init assert.
- 29 (#73): `red_black_tree.zig` assertion baseline (size delta, root state, `validate` up to 512
  nodes after each mutation; file had been invisible to `zig build test`). `linalg/blas.zig` has 77
  errors on 0.16 (`OutOfMemory` escaping `NDArray.Error` in trmv/trmm/syrk, `clone` missing); asserts
  there reverted as unverifiable. RBT size-delta assert is weak (pair with return value).
- Quirks: `gh pr checks` foreground loop hits the 600 s tool cap; cross-compile jobs queue late
  (>15 min), so open the PR by minute ~8; `zig fmt --check src/utils` flags pre-existing
  `compare.zig`; Monitor/`until` via Bash run_in_background works for waiting on a log.

## Cycles 20-26 (2026-10-09..16, condensed 2026-10-17)
- All merged by squash with 7/7 checks, labeled `auto-merged`. Plan 001 "compile-clean" and
  "Thread sync" slices:
- 20 (STABILIZATION, bug #63, PR #64): OOM leaks and an undefined free in `palindrome_partition`,
  `knights_tour`, `combination_sum`, `permutations`, `subsets`, `n_queens`; a
  `checkAllAllocationFailures` test per file. 21-22: ported `nfa`, `matrix_chain`,
  `ford_fulkerson` (#65; never-run tests exposed a wrong `NFA.fromWildcard`) and `bogosort`
  (#66, required `seed: u64`). 23: `kmeans`, `gmm`, `dqn`, `ddpg`, `tsne` per ADR 0001 D1 (#67;
  t-SNE, kmeans, gmm bugs found).
- 24-25: `approximation/*`, `greedy/*`, `automata/dfa`, `graph_coloring/*` ported and wired
  (#68; real `dsatur` infinite loop on isolated vertices fixed); user-data asserts became typed
  errors in #69 (`vertex_cover` `InvalidEdge`; `knapsack`, `bin_packing` `InvalidInput`;
  CHANGELOG notes the v3.0.0 break). Interrupted work was preserved as
  `wip/compile-clean-greedy-automata-approx-20261014`.
- 26: #70 `WorkStealingDeque` (phantom item after resize, wrapping `t < b`) and `parallel_sort`
  (merge sort corrupted 100+ elements, quick sort partition OOB; rewritten) and `prefix_sum`
  (Blelloch wrong for non-power-of-two n), all wired into `root.zig`.
- Leftovers: `greedy_coloring` Tiger cleanup, `backtracking_coloring` contract docs, DFA stores
  an allocator (note an exception), huffman stack-depth assert, `hamiltonian.zig` not OOM-
  audited, `dinic`/`edmonds_karp` not in the test graph, gmm per-point E-step alloc, deque resize
  concurrent with steal still unsafe (documented in header).
- Quirks: `zig` on PATH is 0.15.2, use `/Users/fn/.zr/toolchains/zig/0.16.0/zig`; BSD sed lacks `\n`
  (use `perl -0pi`; escape `\@` in replacements); cross-compile CI jobs queue late (>15 min).

## Cycles 10-19 (2026-10-01..10-08, folded 2026-10-30)
All merged by squash with 7/7 checks, labeled `auto-merged`.
- 10-15: seed injection finished (ADR 0001 D1); time -> `Io.Clock` (#49); tidy baseline to `tools/`
  (#50); long fns fixed (#52); `deque.zig` tests found never running (#54). Recurring cause: files
  reached only via nested `pub const` re-exports are invisible to `refAllDecls` (issue #38), so
  probe with a scratch `src/scratch.zig` and wire fixed files into the test block.
- 16 (bug #53, #55): the *test* was wrong, not `AhoCorasickASCII.findFirst` (first match to
  complete); `aho_corasick.zig` wired into `root.zig`.
- 17 (bug #57, #58 #59): ILU init double free; stale gmres/bicgstab arity in `iterative.zig`
  tests exposed a REAL GMRES bug (lucky breakdown `h(j+1,j)~0` exited before rotating col j, so x
  never updated); CG read `norm2(r)` after `free(r)`; zero pivot is `error.SingularMatrix`; ILU(0)
  asserts ascending CSR columns (`CSR.fromCOO` does NOT sort). Question #56 (0.16 flip vs CI
  pinned 0.15.2) went unanswered; option 1 (big-bang flip) taken.
- 18: #60 flip to 0.16.0 + ndarray `Io.Dir`/`Io.Mutex`; #61 `mem.indexOf*` -> `find*`. Many files
  outside `root.zig`'s test graph were still red on 0.16 (-> the sweep plan item).
- 19 (#62): interrupted work preserved as `wip/fix-backtracking-0.16-compile-20261008`; all 9
  `algorithms/backtracking/*` compile (sudoku hang, `isValidSudoku` OOB fixed); OOM harness found
  leaks in six files -> bug #63.
- Leftovers: `preconditioner.zig` init (135 lines), `bagging.zig` fit (73 lines), 3-4 type-fn tidy
  baseline entries grew (Cuckoo/RobinHood/ConcurrentSkipList/ILUPreconditioner).
- Quirks: stale `.zig-cache` gives "failed to spawn build runner: FileNotFound" (use `--cache-dir
  /tmp/zuda-zcache`); `zig build test` prints "failed command" noise yet exits 0; zsh has no
  PIPESTATUS (`pipestatus`); no `timeout` binary; CI Build & Test 7-9.5 min.

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
