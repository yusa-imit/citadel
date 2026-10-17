# zuda — context

last_seen_at: 2026-10-17T00:00:00Z
rejected_plans: []

## Cycle 27 — 2026-10-17 — FEATURE
- Done: inbox clean (CI green on d88ca14, #70 already merged, no bugs, no plan PR, no OWNER
  comments; milestone #31). Plan 001 "Thread sync" item finished. `map_reduce.zig` redesigned:
  mapper emits into a bounded `EmitterType` (`pairs_max`, `error.PairsLimitExceeded`, pre-reserved
  so `emit` never allocates), comptime `key_order` comparator (slice keys work), stable
  `std.sort.block`, `groupBy`/`mapReduce`/`partition` results without a stored allocator
  (`deinit(gpa)`), `GroupByResult` keeps its `flat` buffer. 16 tests (OOM, seeded model, stability
  at 600 elements, case-folded equal keys); wired into `root.zig`. `concurrent_skip_list`
  (`Thread.yield`) already compiled, 24/24 pass; no `error.Canceled` switches exist in these
  modules. Reviewer: 1 critical (CHANGELOG, fixed), 6 warnings addressed. Plan item ticked in PR.
- PRs: #71 (`fix/map-reduce-api-zig-016`) open; Build & Test green 8m32s, 6 cross-compile checks
  pending at the deadline (same as cycle 26). Next inbox merges it at 7/7 green, no `hold`, then
  adds the `auto-merged` label (I removed it early) and ticks the "Thread sync" box on issue #31.
- Next: FEATURE — Test/bench harness item (`internal/testing.zig`, `internal/bench.zig`,
  `utils/perf.zig` fixedBufferStream, Smith fuzz); full `src/**` `zig test <file>` sweep; assertion
  baseline; v3.0.0. Deque resize concurrent with steal still unsafe (documented in header).
- Blockers: none. Open questions: none. stabilize_streak: 0 (no file).
- Quirk: `gh pr checks` waiting loop in the foreground hit the 600s tool cap; cross-compile jobs
  queue late (>15 min). Plan the cycle so the PR is open by minute ~8.

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
- 18 (FEATURE): inbox merged PR #60 (flip to 0.16.0 + ndarray `Io.Dir`, Io.Mutex, PriorityQueue
  unmanaged, bench `Io`); PR #61 `mem.indexOf*` -> `find*` (43 sites, 13 files). Found many files
  outside `root.zig`'s test graph still red on 0.16 (managed `ArrayList(T).init`, `.writer()`,
  `std.time.timestamp`, `std.posix.getrandom`; bogosort, kmeans, gmm, dqn, ddpg, tsne); added a
  plan item. `zig fmt --check src` fails on `max_sum_rectangle.zig`, `target_sum.zig` (parse
  errors) and ~160 unformatted files; CI has no fmt gate.
- 19 (FEATURE, PR #62): preflight found uncommitted work from an interrupted cycle; preserved as
  `wip/fix-backtracking-0.16-compile-20261008`, then merged all 9 `algorithms/backtracking/*`
  compiling on 0.16 (sudoku invalid-board hang + `isValidSudoku` OOB fixed, two wrong
  `word_search` expectations). Reviewer's OOM harness found alloc-failure leaks in
  palindrome_partition (undefined free in `minCut`), knights_tour, combination_sum, permutations,
  n_queens, subsets -> bug #63 (fix with `checkAllAllocationFailures` tests per file).
- Remaining after 19: compile-clean files outside the test graph (`nfa`, `matrix_chain`,
  `ford_fulkerson`, `bogosort`, `kmeans`, `gmm`, `dqn`, `ddpg`, `tsne`), then a `src/**`
  `zig test <file>` sweep, Thread sync, harness, assertion baseline, v3.0.0. Stabilize leftovers:
  `bagging.zig` fit (73 lines, tests don't compile), 3-4 type-fn tidy baseline entries grew
  (Cuckoo/RobinHood/ConcurrentSkipList/ILUPreconditioner); probe hidden-red files via a scratch
  `src/scratch.zig` with `test { _ = @import(...); }` (delete after).
- Quirks: stale `.zig-cache` gives "failed to spawn build runner: FileNotFound" (use `--cache-dir
  /tmp/zuda-zcache`); `zig build test` prints "failed command" noise yet exits 0 (trust the exit
  code); zsh has no PIPESTATUS (`pipestatus`); guard rejects `cd <repo>; ...` and shell writes
  into citadel (use Write/Edit); no `timeout` binary; CI Build & Test 7-9.5 min.

## History cycles 14-15 (folded 2026-10-11)

Cycle 14 (FEATURE): plan 001 `std.time.*` -> `Io.Clock` in containers was already done by the
ADR 0001 seed-injection rollout (cycles 8-11); only a `bloom_filter.zig` prose comment tripped
the plan's literal verify grep, reworded (PR #49). Cycle 15 (STABILIZATION): `tidy_baseline.txt`
moved under `tools/` (#50); functions > 70 lines fixed (#52: dueling_dqn `xavier_fill`,
aho_corasick `failureTarget`, builder loops). Verifying #52 exposed that `deque.zig` tests never
ran under `zig build test` (#51 -> #54: `validate()` wrong for empty/full ring, `shrinkToFit`
left tail==capacity, off-by-one stress test; wired into `root.zig`); the same probe found
`AhoCorasickASCII.findFirst` red (#53). Lesson: files reachable only via `pub const`
re-exports are untested; probe with a scratch `src/scratch.zig` `test { _ = @import(...); }`
and delete it after. Leftovers: `preconditioner.zig` init (135 lines), `bagging.zig` fit (73;
its tests do not compile on 0.15.2).

## History cycles 10-13 (folded 2026-10-05)
Cycle 10: tidy comment-aware fn scanner (PR #43); CuckooHashMap seed injection (#42). Cycle 11:
SkipList seed injection (#45) completed the ADR 0001 D1 rollout; filed #44. Cycle 12: fixed #44
(`zoltraak_sortedset` ArrayList arity + remove() use-after-free, #47); filed #46. Cycle 13: #46
fixed in #48 (SkipList keyed by `{score, member}`, file wired into `root.zig` tests). Recurring
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
