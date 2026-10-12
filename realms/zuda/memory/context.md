# zuda — context

last_seen_at: 2026-10-12T00:00:00Z
rejected_plans: []

## Cycle 23 — 2026-10-12 — FEATURE
- Done: inbox clean (CI green on 2847a19, no bugs, no plan PR, no OWNER comments; milestone #31).
  Plan 001 item "compile-clean": `kmeans`, `gmm`, `dqn`, `ddpg`, `tsne` ported per ADR 0001 D1
  (required `seed: u64` on `KMeansOptions`/`GMMOptions`/`TSNEOptions`/`DQN.Config`/`DDPG.Config`),
  all wired into `root.zig`. Tests that never ran exposed real bugs: t-SNE symmetrized P in place,
  left the P diagonal undefined, inverted the adaptive-gain sign (and 5 tests had n_samples /
  n_features swapped); kmeans collapsed empty clusters to the origin and leaked on OOM; gmm
  freed undefined rows on OOM (new `alloc_rows`/`free_rows`). Every file has a
  `checkAllAllocationFailures` test. Local `zig build test` exit 0, fmt clean, reviewer 0 critical.
- PRs: #67 (`fix/compile-clean-kmeans-gmm-rl-tsne`) open; Build & Test pending at report time (see
  tracking issue for the outcome). If still open next cycle, inbox merges it once all checks are
  green and no `hold` label is present.
- Next: FEATURE — finish the "compile-clean" item with a full `src/**` `zig test <file>` sweep
  (the plan's Verify line); then Thread sync, harness, assertion baseline, v3.0.0 (CHANGELOG must
  mention the required `seed` on five more types). Stabilize leftovers: `hamiltonian.zig` not
  OOM-audited; `dfa`, `dinic`, `edmonds_karp` not in test graph; `max_iterations == 0` and gmm
  per-point E-step alloc (reviewer suggestions).
- Blockers: none. Open questions: none. stabilize_streak: 0 (no file).
- Quirk: `read -t N </dev/zero` in a Monitor loop exits 1 (use `until ...; do :; done` or a
  poll with a real wait); an earlier `zig build test` left a build-runner child alive after
  `pkill` of the parent, kill it by pid before rerunning.

## Cycle 22 — 2026-10-11 — FEATURE
- Done: inbox clean (CI green on 01a9b7c, no bugs, no plan PR, no OWNER comments; milestone #31).
  Merged #65 (nfa/matrix_chain/ford_fulkerson; 7/7 green, `auto-merged`). Then plan 001 item
  "compile-clean": `bogosort.zig` ported per ADR 0001 D1 — `bogoSort*` take required `seed: u64`,
  `bogoSortBounded(.., seed, iterations_max: u32)` with explicit error set, no `std.posix`; three
  seed-determinism tests; wired into `root.zig` tests. `zig build test` exit 0, fmt clean.
- PRs: #65, #66 merged (squash, 7/7 checks, Build & Test ~6m, labeled `auto-merged`).
- Next: FEATURE — same item: `kmeans`, `gmm` (`seed: ?u64 = null` + `std.time.timestamp` ->
  required `seed: u64`; kmeans also has managed `ArrayList(..).init` at ~line 530), `dqn`, `ddpg`,
  `tsne`, then a full `src/**` `zig test <file>` sweep. Then Thread sync, harness, assertion
  baseline, v3.0.0. Stabilize leftovers: `hamiltonian.zig` not OOM-audited; `dfa`, `dinic`,
  `edmonds_karp` not in test graph (unprobed).
- Blockers: none. Open questions: none. stabilize_streak: 0 (no file).
- Quirk: guard rejects `sleep N` and compound `cd` commands; use a Monitor until-loop on a log
  file for the ~5 min `zig build test` run (run it with run_in_background).

## Cycle 21 — 2026-10-10 — FEATURE
- Done: inbox clean (CI green on 01a9b7c, no bugs, no plan PR, no OWNER comments; milestone #31).
  Plan 001 item "compile-clean files outside test graph": ported `nfa`, `matrix_chain`,
  `ford_fulkerson` to 0.16 and wired them into `root.zig`'s test block. Running them exposed real
  bugs: `NFA.fromWildcard` marked every state accepting and built Kleene stars wrongly (rewritten;
  `a*`, `.*`, `a.c` tests were red); OOM undefined-free + errdefer/defer double free in
  `matrix_chain` and `ford_fulkerson` (new `alloc_table`/`residual_init` helpers); `maxInt` on f64
  capacities. Each file has a `checkAllAllocationFailures` test. Local `zig build test` exit 0.
- PRs: #65 open (`fix/compile-clean-nfa-matrix-chain-ford-fulkerson`), Build & Test green 6m27s,
  cross-compile still pending at the 22-min deadline. NOT merged: next cycle's inbox merges it
  once all 7 checks are green (no `hold`), then ticks the plan progress line (already edited in PR).
- Next: FEATURE — remaining in that item: `bogosort` (seed shape per ADR 0001, no
  `std.posix.getrandom`), `kmeans`, `gmm`, `dqn`, `ddpg`, `tsne`, then a full `src/**` `zig test
  <file>` sweep. Then Thread sync, harness, assertion baseline, v3.0.0. Stabilize leftovers:
  `hamiltonian.zig` not OOM-audited; `dfa`, `dinic`, `edmonds_karp` not in test graph (unprobed).
- Blockers: none. Open questions: none. stabilize_streak: 0 (no file).
- Quirk: BSD sed lacks `\n` in replacements, use perl/python; a python `str.replace` with an empty
  slice corrupts the file (check `index()` ordering). `zig build test` ran ~9 min locally.

## Cycle 20 — 2026-10-09 — STABILIZATION
- Done: periodic (n%5==0) and open OWNER bug #63. Fixed it in PR #64 (squash, 7/7 checks, Build &
  Test 6m18s, labeled `auto-merged`; #63 closed by `Fixes #63`): OOM leaks and an undefined free in
  `palindrome_partition` (minCut rows, partition base case, dupe/append), `knights_tour` (both
  board setups), and append-failure leaks in `combination_sum`, `permutations`, `subsets`,
  `n_queens`. Each file has a `checkAllAllocationFailures` test, confirmed red against HEAD.
  Reviewer: 0 critical; fixed 2 warnings (line > 100 cols, camelCase runner fn names).
- Next: FEATURE — plan 001 item "compile-clean files outside test graph": `nfa`, `matrix_chain`,
  `ford_fulkerson`, `bogosort`, `kmeans`, `gmm`, `dqn`, `ddpg`, `tsne`, then a full `src/**`
  `zig test <file>` sweep. Then Thread sync, harness, assertion baseline, v3.0.0. Stabilize
  leftovers: hamiltonian.zig not OOM-audited; Tiger Style class audit not run this cycle.
- Blockers: none. Open questions: none. stabilize_streak: 0 (no file).
- Quirk: the `zig` on PATH is still 0.15.2; use `/Users/fn/.zr/toolchains/zig/0.16.0/zig` for
  every command (the 0.15 `zig build test` fails). The guard rejects `cd X; ...` and `for` loops
  mixing the repo path; run plain commands. zsh expands `==`, so avoid `echo == x`.

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
