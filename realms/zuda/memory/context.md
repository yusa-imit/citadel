# zuda — context

last_seen_at: 2026-10-29T00:00:00Z
rejected_plans: []

## Cycle 37 — 2026-10-29 — FEATURE
- Done: inbox clean (CI green, no bugs, no OWNER comments, milestone #31). Merged #79 (geometry,
  7/7, `auto-merged`). Sweep slice `algorithms/sorting`: 6 of 23 files red (bitonicsort, blocksort,
  mergesort, pancakesort, pigeonholesort, strandsort), ported to unmanaged `ArrayList`; the other
  22 were only reachable through `pub const` re-exports so their tests never ran; all 23 now
  imported from the `root.zig` test block and pass. Real bug: `strandSort` merge took the right
  element on ties (unstable; the existing stability test failed). Breaking: `pancakeSortSequence`,
  `getAllStrands` return unmanaged lists.
- PR: #80 (`fix/compile-clean-sorting-zig-016`) open; local full `zig build test` exit 0; CI not yet
  finished at report time. Next cycle merges at 7/7, no `hold`, adds `auto-merged`.
- Next: merge #80; sweep trees, compression, linalg, iterators, aggregators, ML (34) last; 10
  unwired string files; 5 dp leftovers; assertion baseline; v3.0.0. Cycle 38 is FEATURE.
- Blockers: none. Open questions: none. stabilize_streak: 0 (no file).
- Quirks: first Bash call was blocked because it mixed `/tmp` writes with the citadel path; keep
  citadel reads in separate calls. Sweep script lives in /tmp/zsweep (per-file scratch root
  `src/_sweep_X.zig`, `-fno-emit-bin` for compile, no flag to run tests); full build ~4 min.

## Cycle 36 — 2026-10-28 — FEATURE
- Done: inbox clean (CI green on 5bdaf02, no bugs, no OWNER comments, milestone #31). Plan 001
  compile-clean, geometry slice: 7 of 13 files red, all 13 wired into `root.zig`.
  Real bugs: Bentley-Ottmann iterated `events.items` while appending (use-after-free) and
  its neighbour-only status found 10 of 100 intersections -> rewritten as an active-set sweep
  (honest header); ear clipping used an open triangle and clipped through a reflex vertex
  (L-shape area 100, not 75); `Delaunay(f32)` never compiled; orientation and zigzag tests
  had wrong expectations. Result lists are unmanaged (`deinit(allocator)`), v3.0.0 break.
- PR: #79 (`fix/compile-clean-geometry-zig-016`) open; Build & Test green (9m25s), 6 cross-compile
  jobs queued at the 22-min deadline; local full `zig build test` exit 0. Next cycle merges at
  7/7, no `hold`, adds `auto-merged`.
- Next: merge #79; 10 unwired string files; sweep trees, compression, sorting, linalg, iterators,
  aggregators, ML last; 5 dp leftovers; assertion baseline; v3.0.0. Cycle 37 is FEATURE.
- Blockers: none. Open questions: none. stabilize_streak: 0 (no file).
- Quirks: tool calls are fast, whole cycle to PR took ~10 min; CI cross-compile queues ~10 min more.
  A perl `s///` swallowed `@divExact` (interpolated as array): escape `\@` in perl replacements.

## Cycle 35 — 2026-10-27 — STABILIZATION (periodic), folded 2026-10-29
- Merged #77, #78 (7/7). Real bug: subnormal `nu`/`beta` passed `init` but made `sample()` panic on
  `Gamma.init(...) catch unreachable` in StudentT, F, SkewT, GeneralizedNormal,
  HalfGeneralizedNormal; `init` now rejects them; proof comments added. Check two lines up for a
  proof comment when scanning `catch unreachable`.

## Cycle 34 — 2026-10-26 — FEATURE
- Done: inbox clean (CI green, no bugs, no OWNER comments). Merged #76 (7/7, `auto-merged`).
  Sweep slice `algorithms/string`: 12 files ported to 0.16 (unmanaged `ArrayList`, `.empty`).
  Real bugs: `longestCommonPrefixDivideConquer` returned a view of its input, not an owned copy;
  `lzw` leaked dictionary keys on a failed put and double-freed `previous`; `trie`/`manacher`
  leaked on append failure. Wired 8 passing files into `root.zig` (anagrams, double_metaphone,
  glob_match, longest_common_prefix, rabin_karp, run_length_encoding, smith_waterman, z_algorithm).
- PR: #77 (`fix/compile-clean-string-zig-016`) open; Build & Test green (7m27s), 6 cross-compile
  jobs still queued at the 22-min deadline. Next cycle merges at 7/7, no `hold`, adds `auto-merged`.
- Compile-clean but UNWIRED (never-run tests fail; real algorithm bugs): `boyer_moore` (hangs),
  `kmp` (`count` returns 3, expected 2), `trie` (delete/size), `suffix_array` (search finds 0),
  `manacher` (integer overflow panic), `metaphone`, `soundex`, `damerau_levenshtein`,
  `jaro_winkler` (max prefix length 4), `lzw` (compression ratio). Fix each with TDD, then wire.
- Next: merge #77; fix those 10 string files; continue sweep (trees, geometry, compression,
  sorting, linalg, iterators, aggregators, ML last), 5 dp leftovers, assertion baseline, v3.0.0.
- Blockers: none. Open questions: none. stabilize_streak: 0 (no file).
- Quirks: a hung test binary (boyer_moore) burned 7 min of the cycle: always run per-file tests
  under `perl -e 'alarm 90; exec @ARGV'`, never one combined root first. Guard rejects a chained
  command that mixes `cd` with `perl -pi` on files; run edits from the repo cwd without `cd`.

## Cycle 33 — 2026-10-23 — ABORTED (disk gate: 16 GB free < 20 GB; nothing touched)

## Cycles 31-32 (2026-10-21..22, folded 2026-10-28)
- Merged #75 (btree, adjacency_list, topological_sort, silica/zr compat shims; BTree reverse
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

## Cycle 30 — 2026-10-20 — STABILIZATION (periodic)
- #74 merged: proof comments on 21 `catch unreachable` sites (quantile in sample/median, Deque
  iterator). Left: ~24 `Gamma/StudentT/Lindley/GeneralizedNormal.init(self.param) catch
  unreachable` sites in `distributions.zig` need the owner's init validation as proof. The
  `chore` label does not exist in the repo.

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
- Quirks: the `zig` on PATH is 0.15.2, use `/Users/fn/.zr/toolchains/zig/0.16.0/zig`; stale
  `.zig-cache` -> `--cache-dir /tmp/zuda-zcache`; `zig fmt --check src` lists ~160 pre-existing
  unformatted files (check touched paths only); the guard rejects `cd X; ...`, `sleep N`, and
  shell redirects in a command mentioning the citadel path; BSD sed lacks `\n` (use `perl -0pi`);
  zsh expands `==`; a build-runner child can outlive `pkill` of its parent (kill by pid);
  cross-compile CI jobs queue late (>15 min): open the PR by minute ~8.

## Cycles 16-19 (2026-10-01 to 10-08), folded
All merged by squash with 7/7 checks, labeled `auto-merged`.
- 16 (STABILIZATION, bug #53, PR #55): the *test* was wrong, not `findFirst` (it returns the first
  match to complete); fixed the expectation, wired `aho_corasick.zig` into `root.zig` tests.
- 17 (STABILIZATION, bug #57, PRs #58 #59): ILU init double free + sparse/preconditioner tests
  wired in; `iterative.zig` tests had stale gmres/bicgstab arity, exposing a REAL GMRES bug (lucky
  breakdown `h(j+1,j)~0` exited before rotating col j, so x never updated); CG read `norm2(r)`
  after `free(r)`; zero pivot is `error.SingularMatrix`; ILU(0) asserts ascending CSR columns
  (`CSR.fromCOO` requires sorted COO and does NOT sort). Question #56 (0.16 flip vs CI pinned
  0.15.2) went unanswered; option 1 (big-bang flip) taken.
- 18 (FEATURE): #60 flip to 0.16.0 + ndarray `Io.Dir`/`Io.Mutex`; #61 `mem.indexOf*` -> `find*`.
  Many files outside `root.zig`'s test graph were still red on 0.16 (-> the sweep plan item).
  `zig fmt --check src` lists ~160 unformatted files; CI has no fmt gate.
- 19 (FEATURE, PR #62): interrupted work preserved as `wip/fix-backtracking-0.16-compile-20261008`;
  all 9 `algorithms/backtracking/*` compile (sudoku hang, `isValidSudoku` OOB fixed); the OOM
  harness found leaks in six files -> bug #63.
- Stabilize leftovers: 3-4 type-fn tidy baseline entries grew (Cuckoo/RobinHood/
  ConcurrentSkipList/ILUPreconditioner).
- Quirks: stale `.zig-cache` gives "failed to spawn build runner: FileNotFound" (use `--cache-dir
  /tmp/zuda-zcache`); `zig build test` prints "failed command" noise yet exits 0 (trust the exit
  code); zsh has no PIPESTATUS (`pipestatus`); guard rejects `cd <repo>; ...` and shell writes
  into citadel (use Write/Edit); no `timeout` binary; CI Build & Test 7-9.5 min.

## History cycles 14-15 (folded 2026-10-11)

Cycles 14-15: time -> `Io.Clock` already done (#49); tidy baseline to `tools/` (#50); long fns
fixed (#52); `deque.zig` tests found never running (#54); `AhoCorasickASCII.findFirst` red (#53).
Leftovers: `preconditioner.zig` init (135 lines), `bagging.zig` fit (73 lines).

## History cycles 10-13 (folded 2026-10-05)
Cycles 10-13: seed injection finished (ADR 0001 D1); #44/#46 fixed (#47, #48). Recurring
cause: files reached only via nested `pub const` re-exports are invisible to `refAllDecls`
(issue #38), so probe with a scratch `src/scratch.zig` and wire fixed files into the test block.

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
