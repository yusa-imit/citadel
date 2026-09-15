# zuda — context

last_seen_at: 2026-09-15T07:05:59Z
rejected_plans: []

## Cycle 10 — 2026-09-15 — STABILIZATION
- Done: forced (n=10, n%5==0), no red CI/bug forcing condition otherwise. Inbox merged PR #42
  (CuckooHashMap seed injection, plan 001 rollout), labeled `auto-merged`. Tiger Style audit
  (tidy-auditor): most counts flat since 2026-09-10; `std.time.*` in src 21->19
  (robin_hood_hash_map/cuckoo_hash_map/concurrent_skip_list now clean, skip_list.zig still
  open); `zig fmt --check` regressed ~20->170 files + 2 files with genuine parse errors
  (`max_sum_rectangle.zig`, `target_sum.zig`, `anytype` outside generic-fn position) —
  re-audit needed. Fixed `tools/tidy.zig`'s comment-unaware function-length scanner
  (`extractFnName` mis-parsed `fn` signatures inside `///` doc-comment examples as real code,
  3 confirmed false positives) — RED-first test, all 21/21 tool tests pass, `zig build tidy`
  confirmed the 3 false positives gone (5 real violations remain, separate issue). STATE.md
  refreshed with full 2026-09-15 numbers and candidate list.
- PRs: #43 open (tidy comment-aware fn scanner), Build & Test in progress at the cycle deadline
  — left "awaiting CI; merge next cycle" comment. #42 merged.
- Next: merge #43 once green, then FEATURE resumes with plan 001's last io/seed rollout item
  (`skip_list.zig`). Stabilize candidates queued: `tools/tidy.zig` baseline key-collision
  (`bagging.zig:fit` confirmed colliding, needs a baseline-format decision), 5 now-verified
  real function-length violations to baseline/shorten, `zig fmt` regression + its 2 parse
  errors, `tidy_baseline.txt` root-placement hygiene.
- Blockers: none. Open questions: none.

## Cycle 9 — 2026-09-12 — FEATURE
- Done: inbox found no new owner actions beyond the known "awaiting CI; merge next cycle" note
  on #41 (already accounted for). Merged PR #41 (RobinHoodHashMap seed injection, CI fully
  green across all 7 checks), branch deleted. Continued plan 001's io/seed rollout with
  `cuckoo_hash_map.zig` (ADR 0001 D1): added a stored `prng: std.Random.DefaultPrng` field
  seeded once at `init`/`initCapacity` from a required `Options{ seed: u64 }` (no default);
  `rehash()` now draws `seed1`/`seed2` from that stored prng instead of re-seeding from
  `std.time.nanoTimestamp()` on every max-displacement rehash. 3 new determinism tests (same
  seed → identical seed1/seed2 at init and post-rehash; different seeds diverge). 2 external
  call sites updated (`bench/hashing.zig`, `tests/memory_safety_audit.zig`, 3 call sites
  there). `code-reviewer` found the change correct (Xoshiro256 is a plain value type, no
  self-referential pointer, safe to copy in `clone()`) with one doc-comment suggestion, applied.
- PRs: #42 open (CuckooHashMap seed injection), Build & Test + wasm32-wasi green, 5
  cross-compile targets pending at the cycle deadline — left "awaiting CI; merge next cycle"
  comment, next cycle's inbox merges it. #41 merged.
- Next: merge #42 once green, then finish plan 001's io/seed rollout item with `skip_list.zig`
  (the last file in scope — has both a time-seeded `init` and an existing `initWithSeed` escape
  hatch to consolidate into one `Options`-taking `init`, plus a wider consumer footprint:
  `src/compat/zoltraak_sortedset.zig`, `src/utils/builder.zig`'s `toSkipList`,
  `src/utils/debug.zig`, 3 examples, 2 benches). Once done, this plan item can be ticked.
- Blockers: none. Open questions: none.

## Cycle 8 — 2026-09-11 — FEATURE
- Done: inbox merged PR #40 (fix: ConcurrentSkipList reader-count-quiescence reclamation, all 7
  CI checks green), auto-closed bug #38, checked out main. Implemented plan 001's next io/seed
  rollout item: `RobinHoodHashMap.init`/`.initCapacity` now take a required `Options{ seed: u64
  }` (ADR 0001 D1), removing the `std.time.timestamp()` seed derivation; `SliceBuilder.toHashMap`
  threaded the same shape (new trailing `seed` param); 2 new determinism tests; 5 external call
  sites updated (bench/hashing.zig, tests/memory_safety_audit.zig, utils/hash.zig doc+test).
  Discovered `work_stealing_deque.zig` (also named in this plan item) has zero
  `std.time`/`std.crypto.random` sites — nothing to do, dropped from scope. `cuckoo_hash_map.zig`
  (reseeds `seed1`/`seed2` from the clock on every max-displacement `rehash()`, not just at
  init — needs a stored `prng` field) and `skip_list.zig` (already has an `initWithSeed` escape
  hatch to consolidate, plus a wide consumer footprint: `compat/zoltraak_sortedset.zig`,
  `utils/builder.zig`'s `toSkipList`, 3 examples, 2 benches) remain unchecked, deferred to a
  following cycle — recorded as a scope note in the plan file itself.
  Verification note: `builder.zig`/`hash.zig` are unreachable from `zig build test`'s
  non-recursive `refAllDecls` allowlist (issue #38's finding) — used a throwaway scratch driver
  (`_ = @import("utils/builder.zig"); _ = @import("utils/hash.zig");`, deleted before commit) to
  confirm their `RobinHoodHashMap`-touching tests actually compile and pass (135/135) since CI
  wouldn't have caught a break there today.
- PRs: #41 open (RobinHoodHashMap seed injection), CI still running (Build & Test pending) at
  the cycle deadline — left "awaiting CI; merge next cycle" comment, next cycle's inbox merges
  it. #40 merged.
- Next: merge #41 once green, then continue plan 001's io/seed rollout with `cuckoo_hash_map.zig`
  (store a `prng` field, seed once at init, draw from it in `rehash()` instead of re-seeding from
  `std.time.nanoTimestamp()`) or `skip_list.zig` (consolidate `init`/`initWithSeed` into one
  `Options`-taking `init`, update the wider consumer set) — either is a reasonable next pick.
- Blockers: none. Open questions: none.

## Cycle 7 — 2026-09-11 — STABILIZATION
- Done: inbox merged PR #39 (ConcurrentSkipList `io`/seed injection, plan 001 positive-space
  proof, fully green across all 7 checks), branch deleted, labeled `auto-merged`. Synced
  tracking issue #31's checklist with the plan file (item 5 "io API shape + ADR" was done in
  cycle 6/PR #37 but never ticked on the issue; added the missing concurrent_skip_list.zig
  sub-item, still unchecked — 4 more containers pending). Open `bug` issue #38
  (ConcurrentSkipList leak, OWNER, no `needs-human`) forced STABILIZATION despite green CI.
  Called `architect` (opus) to design a real fix — the node can't be freed immediately after
  unlink since concurrent readers may hold raw pointers into it (lock-free structure). Chose
  reader-count quiescence + bounded retire list over hazard pointers/full EBR (no thread
  registry needed, fits in one file, tractable in one cycle). `test-writer` wrote 5 RED-phase
  tests + force-imported the file into `root.zig`'s test block (issue #38 itself found this
  file's 24 tests were invisible to `zig build test` — non-recursive `refAllDecls`).
  `zig-developer` implemented `Reclaim` (atomic readers counter, mutex-guarded intrusive retired
  list), made `remove()` idempotent (only the CAS-winning thread retires), a bounded
  (`unlink_attempts_max=4`) re-confirm-unlinked pass before retiring, and bounded draining
  (cheap check every retire, escalating to `drain_attempts_max=8` yield-retry only past
  `Options.retired_max`, default 64). One deliberate design deviation: drain is attempted on
  every retire (cheap atomic load), not gated purely on `retired_max`, so a single-threaded
  `remove()` reclaims promptly — recorded in the PR body. `zig test` on the file: 24/24 pass,
  leak-free, stable across 5 runs incl. the threaded smoke test; `zig build` and
  `zig fmt --check` clean. Full `zig build test` deferred to CI per repo convention.
- PRs: #40 open (fixes #38), CI pending at the cycle deadline — left "awaiting CI; merge next
  cycle" comment, next cycle's inbox merges it. #39 merged.
- Next: merge #40 once green; if the bug is confirmed closed by CI, stabilize_streak stays 0
  and FEATURE resumes with plan 001's remaining io/seed rollout (`robin_hood_hash_map.zig`,
  `cuckoo_hash_map.zig`, `skip_list.zig`, `work_stealing_deque.zig`) as the next milestone item.
  If CI surfaces a real failure on #40, that's this cycle's stabilize task carrying over —
  do not increment `stabilize_streak` until a genuine second failed attempt.
- Blockers: none. Open questions: none.

## Cycle 6 — 2026-09-10 — FEATURE
- Done: inbox merged PR #36 (LICENSE, auto-merged, branch deleted); no other owner actions since
  watermark. Milestone #31 next unchecked item was "Fix the public io: Io API shape + ADR" —
  called `architect` (opus) first per plan risk note. It measured real exposure (21
  `std.time.*`, only 15 are PRNG seeding not timekeeping; 4 lib + 29 test `fs.cwd()` all in
  `ndarray.zig`; 2 `Thread.Mutex`; `parallel/*` has zero real `std.Thread` today) and wrote
  `docs/adr/0001-io-injection-and-seed-determinism.md`: clock-derived seeds become a required
  `seed: u64` option (not `io`); `io` is never stored in a container (Managed's allocator
  carve-out does NOT extend to `io` — ownership vs execution-context distinction, see ADR D2);
  `Io.Mutex.lockUncancelable` keeps `error.Canceled` out of container error sets. Net: `io`
  lands on ~18 public fns, not ~40. Spike target `bloom_filter.zig` turned out to need **no**
  public-API change (its one `std.time.*` site was a test-only wall-clock assertion) — fixed
  that test to assert pure arithmetic instead, removed the `std.time.Timer` dependency. Amended
  plan 001: ticked item 5, added a new item for the positive-space proof
  (`concurrent_skip_list.zig` + 4 other time-using containers) since bloom_filter alone doesn't
  exercise the design (see ADR + `decisions.md`'s 2026-09-10 entry for the full reasoning).
- PRs: #36 merged. #37 open (ADR + bloom_filter test fix), Build & Test + 2/6 cross-compile
  green, 4 cross-compile targets still pending at the cycle deadline — left "awaiting CI; merge
  next cycle" comment, next cycle's inbox merges it.
- Next: merge #37 once green, then the new plan 001 item — apply the `io`/`seed` shape to
  `concurrent_skip_list.zig` (positive-space proof), then `robin_hood_hash_map.zig`,
  `cuckoo_hash_map.zig`, `skip_list.zig`, `work_stealing_deque.zig`.
- Blockers: none. Open questions: none.

## Cycle 5 — 2026-09-10 — STABILIZATION
- Done: inbox merged PR #35 (mechanical renames, plan 001 item 4) and ticked it on tracking
  issue #31. Forced STABILIZATION (n=5, n%5==0). CI on `main` green, no red-CI/bug forcing
  condition otherwise. Ran a fresh Tiger Style audit (`tidy-auditor`): `catch unreachable`
  69→60 (decision_tree.zig's old hits are now just comments), `std.debug.print` library-code
  finding was a false positive (all 14 hits are inside doc-comment examples, 0 real),
  `while(true)` 111→108 (37 real unbounded ones in `distributions.zig`), files>800 76→74.
  New findings: `tools/tidy.zig`'s function-length scanner isn't comment-aware (3 false
  positives) plus a baseline key-collision bug; ~20 files fail `zig fmt --check` on `main`
  with no CI gate for it; 9 ML files seed PRNGs from wall-clock time instead of an injected
  seed (Tiger Style rule 7/14 gap); the 2 `usize`-in-struct candidates (`bwt.zig`,
  `arithmetic.zig`) were reviewed and judged NOT real wire-format violations (never actually
  serialized) — don't re-flag. Picked the smallest safe fix: zuda was the only kingdom repo
  missing a `LICENSE` file — added MIT matching all 7 siblings (PR #36). Also caught that the
  audit's "4 scratch files in root" finding was a false positive — those are gitignored/
  untracked (`.gitignore` has `test_*`), not a real repo violation. `STATE.md` gap table and
  candidate list refreshed with all of the above.
- PRs: #36 open (LICENSE), CI pending at the cycle deadline — left "awaiting CI; merge next
  cycle" comment, next cycle's inbox merges it.
- Next: merge #36 once green, then resume plan 001 item 5 ("Fix the public `io: Io` API shape
  + ADR" — the v3.0.0 signature break, call `architect` first) since FEATURE resumes next
  cycle (n=6, not a multiple of 5, no red CI/bug). New stabilize candidates for future cycles:
  `tools/tidy.zig` comment-parsing + baseline key-collision fix, `zig fmt --check` drift (~20
  files, no CI gate), PRNG seed injection in 9 ML files — see `STATE.md` items 8-10.
- Blockers: none. Open questions: none.

## History (cycles 0-4, folded 2026-09-15 to keep this file under 200 lines)
Realm created 2026-09-05 by the citadel restructure (memory migrated from the repo's old
`.claude/memory/`); plan 001 (Zig 0.16 migration) merged by the owner, milestone issue #31
opened. Cycle 1 (PR #32): finished the preserved `wip/random-forest-regression-criterion`
TDD cycle (`RandomForest.fit()` now uses `.mse` for regression forests, not always `.gini`),
dropped 9 orphaned distribution duplicates, synced version strings. Cycle 2 (PR #33): vendored
the kingdom reference tidy lint into `tools/tidy.zig` as a standalone `zig build tidy` step
(not yet a `test` dependency — `main` had 4,608 pre-existing non-function-length findings).
Cycle 3: disk gate failed (16GB free), aborted before touching the repo. Cycle 4 (PR #35):
merged #34 (build.zig linkLibC fix), reconciled milestone #31 checklist (items 2-3 ticked
late), implemented the dual-toolchain-compatible half of mechanical renames
(`GeneralPurposeAllocator`→`DebugAllocator` 7 files, `ArrayListUnmanaged{}`→`.empty` 2 files);
split `mem.indexOf*`→`find*` and `AutoArrayHashMap`→`AutoArrayHashMapUnmanaged` into a later
item since neither is dual-compatible under the 0.15.2 CI pin.
Resolved backlog items no longer tracked: the RandomForest bug (fixed cycle 1), the
`wip/random-forest-regression-criterion` branch (finished cycle 1). Still-open backlog folded
here: `catch unreachable` OOM-swallow audit (69→60 sites, see cycle 5's STATE.md refresh);
2 leftover `p < 1e-300` f32-underflow sites in `distributions.zig`; ~20 deferred
`std.debug.assert` sites in `src/algorithms/`; `logFactorial` exact only for `n < 20`; a v2.4.0
release backfilling CHANGELOG 2.0.1-2.3.0 is still owed once plan 001 lands. Next distribution
vein (if catalog work resumes): Devroye (1993) discrete-stable triptych beyond Sibuya (209th),
discrete Mittag-Leffler next — always grep `pub fn <Name>` in `distributions.zig` first
(JohnsonSU, ExGaussian shipped as duplicates before).
