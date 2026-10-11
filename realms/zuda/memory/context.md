# zuda — context

last_seen_at: 2026-10-11T00:00:00Z
rejected_plans: []

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

## Cycle 19 — 2026-10-08 — FEATURE
- Done: preflight found uncommitted backtracking work on `fix/backtracking-0.16-compile` (the
  interrupted prior cycle); preserved it as `wip/fix-backtracking-0.16-compile-20261008` (the
  `...20261007` wip is an older, smaller subset), then restored those files onto
  `fix/compile-clean-outside-test-graph`, verified on 0.16 (`zig test` each file, `zig build
  test` exit 0, fmt clean) and merged PR #62: all 9 `algorithms/backtracking/*` compile,
  wired into `root.zig` tests; sudoku invalid-board hang + `isValidSudoku` OOB fixed; two wrong
  `word_search` expectations (2 -> 4). Squash, 7/7 checks, labeled `auto-merged`.
- Found: reviewer's OOM harness showed pre-existing alloc-failure leaks in palindrome_partition
  (undefined free in `minCut`), knights_tour, combination_sum, permutations, n_queens, subsets.
  Filed bug #63 (OWNER-account bug, forces STABILIZATION next cycle; fix with the word_search
  pattern + `checkAllAllocationFailures` tests per file).
- Next: fix #63, then finish plan item "compile-clean files outside test graph": `nfa`,
  `matrix_chain`, `ford_fulkerson`, `bogosort`, `kmeans`, `gmm`, `dqn`, `ddpg`, `tsne`, then a
  full `src/**` `zig test <file>` sweep. Then Thread sync, harness, assertion baseline, v3.0.0.
- Blockers: none. Open questions: none. stabilize_streak: 0 (no file).
- Quirk: stale `.zig-cache` gave "failed to spawn build runner: FileNotFound"; use
  `zig build test --cache-dir /tmp/zuda-zcache`. CI Build & Test now ~9.5 min. Shell writes
  into citadel are blocked by the guard; use Write/Edit there. Main CI for 82fe3fc was still in
  flight at preflight.

## Cycle 18 — 2026-10-05 — FEATURE
- Done: preflight found branch `chore/zig-0.16-flip` (PR #60, clean, pushed, 7/7 checks green,
  no hold). Inbox merged #60 (squash, labeled `auto-merged`): flip to 0.16.0 plus ndarray
  `Io.Dir`, Io.Mutex, PriorityQueue unmanaged, bench `Io`. #56 was closed by cycle 17. Main CI
  on the merge commit: green. Then plan 001 item `mem.indexOf*` -> `find*`: 43 sites, 13 files,
  PR #61 (`zig build`, `zig build test` exit 0 on 0.16; formatted 5 touched files that already
  failed fmt). Ticked plan items done by #60 (indexOf/AutoArrayHashMap, ndarray fs, flip).
- Found: many files outside `root.zig`'s test graph still fail on 0.16 (managed
  `ArrayList(T).init`, `.writer()`, `std.time.timestamp`, `std.posix.getrandom` in bogosort,
  kmeans/gmm/dqn/ddpg/tsne). Added a plan item for it. `zig fmt --check src` still fails on
  `max_sum_rectangle.zig` and `target_sum.zig` (parse errors, `anytype`) and ~160 unformatted
  files; CI has no fmt gate.
- PRs: #60 merged. #61 open, Build & Test pending at the deadline; next inbox merges it.
- Next: merge #61, then the new hidden-red 0.16 plan item; then `Thread` sync/bogosort,
  harness `internal/testing.zig` (`std.time.milliTimestamp`), assertion baseline, v3.0.0.
- Blockers: none. Open questions: none. stabilize_streak: 0 (no file).
- Quirk: zsh has no PIPESTATUS (use `pipestatus`); `zig build test` prints a "failed command"
  block from stderr-printing tests yet exits 0, trust the exit code and Build Summary.

## Cycle 17 — 2026-10-03 — STABILIZATION
- Done: forced by open bug #57 (CI green, n%5 != 0). Inbox merged #58 (ILU init double free +
  sparse/preconditioner tests wired into `root.zig`, left open by the interrupted cycle 16
  tail). Fixed #57 in #59: `iterative.zig` tests had stale gmres/bicgstab arity; once running,
  8 were red from a REAL GMRES bug (lucky breakdown `h(j+1,j)~0` exited before rotating col j,
  so exactly-solved systems never updated x, converged=false). Also CG read `norm2(r)` after
  `free(r)`; zero pivot now `error.SingularMatrix`; ILU(0) asserts ascending CSR columns
  (tests skipped `coo.sort()`; `CSR.fromCOO` requires sorted COO and does NOT sort).
- PRs: #58, #59 merged (squash, 7/7 checks green), labeled `auto-merged`. #57 closed.
- Next: FEATURE — plan 001 `std.fs.cwd()` -> `Io.Dir` in `ndarray.zig`, but it is 0.16-only and
  CI is pinned 0.15.2: see question #56 (origin: ai, non-blocking, unanswered, filed 2026-10-01;
  after two cycles with no answer, proceed with its option 1 = big-bang flip PR, cycle 19+).
  Stabilize leftovers: `bagging.zig` fit (73 lines, tests don't compile), 3-4 type-fn tidy
  baseline entries grew (Cuckoo/RobinHood/ConcurrentSkipList/ILUPreconditioner), more
  hidden-red probes via scratch `src/scratch.zig` (works with `zig test`, delete after).
- Blockers: none. Open questions: #56. stabilize_streak: 0 (no file).
- Quirk: full `zig build test` took ~4 min locally this time; CI Build & Test 7 min.

## Cycle 16 — 2026-10-01 — STABILIZATION
- Done: forced by open bug #53 (n%5 != 0, CI green). Inbox found no new OWNER comments, no plan
  PR; `milestone_issue: 31`. #53 root cause: the *test* was wrong, not `findFirst` — "or" ends
  at 9, "world" at 11, and `findFirst` returns the first match to complete, so "or" (index 1,
  pos 7) is right. Corrected the expectation and added `aho_corasick.zig` to `root.zig`'s test
  block (39 filtered / whole suite `zig build test` exit 0, fmt clean).
- PRs: #55 merged (squash, all 7 checks green), labeled `auto-merged`; #53 closed. No open bugs.
- Next: FEATURE — plan 001 `std.fs.cwd()` -> `Io.Dir`/`Io.File` in `ndarray.zig` (14 sites).
  Stabilize leftovers: `preconditioner.zig` init (135 lines), `bagging.zig` fit (73; tests do not
  compile on 0.15.2), 3 type-fn baseline entries that grew; probe for more hidden-red files
  (scratch `src/scratch.zig` with `test { _ = @import(...); }`, delete after).
- Blockers: none. Open questions: none. stabilize_streak: 0 (no file).
- Quirk: bash guard rejects `cd <repo>; ...` compound commands and `timeout` does not exist on
  this box; run plain commands (cwd is already the repo) and use Edit for multi-line changes.

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
