# zuda — context

last_seen_at: 2026-09-17T00:00:00Z
rejected_plans: []

## Cycle 12 — 2026-09-17 — STABILIZATION
- Done: forced by open bug #44 (OWNER-filed, no `needs-human`) per the forcing rule, despite
  green CI and n%5 != 0. Inbox merged PR #45 (SkipList seed injection, all 7 checks green),
  labeled `auto-merged` — this completes plan 001's io/seed rollout item entirely. Fixed #44:
  `zoltraak_sortedset.zig`'s `range()`/`rangeByScore()` called `ArrayList.append` (and
  `deinit`/`toOwnedSlice`) with the pre-unification arity; this repo's pinned Zig 0.15.2
  `std.ArrayList` needs the allocator per call. Verifying the fix (via a scratch driver, since
  this file's tests are still unreachable from `zig build test`, issue #38's gap) surfaced a
  real use-after-free: `remove()`/`add()`'s update path freed the SkipList entry's owned member
  string before unlinking that same allocation from `StringHashMap` (both share the one
  `dupe()`'d string), segfaulting on the next lookup — reordered to unlink first, fixed in the
  same PR. Verification also surfaced a third, separate bug: `score_to_member` (keyed by `f64`
  score alone) silently overwrites and leaks entries when two members share a score, which
  zoltraak's Sorted Set API requires supporting (Redis ZSET semantics) — filed as #46 with a fix
  sketch (composite `{score, member}` SkipList key), deliberately not fixed here to keep #47
  scoped and avoid turning CI red on an unrelated, pre-existing failure. Kept the file out of
  `root.zig`'s `refAllDecls` for the same reason; #46 says to re-wire it once fixed.
- PRs: #47 open (fixes #44), Build & Test green, cross-compile matrix still running at the
  cycle deadline — left "awaiting CI; merge next cycle" comment. #45 merged.
- Next: merge #47 once green (closes #44). Then FEATURE resumes: plan 001's io/seed rollout is
  fully done, so pick the next unchecked plan 001 item — `std.time.*` → `Io.Clock` in the
  container layer, or the `mem.indexOf*`/`AutoArrayHashMap` mechanical-rename item, either is a
  reasonable pick. #46 (duplicate-score SkipList key redesign) is unscheduled — call `architect`
  before implementing given the internal-representation change.
- Blockers: none. Open questions: none. stabilize_streak: not incremented (fix succeeded and is
  verified; only slower cross-compile CI jobs were still pending at the deadline, not a failed
  attempt).

## Cycle 11 — 2026-09-16 — FEATURE
- Done: inbox merged PR #43 (tidy comment-aware fn scanner, all 7 checks green), labeled
  `auto-merged`. No new OWNER comments/questions/directives beyond routine cycle-report notes.
  Completed plan 001's io/seed rollout item (ADR 0001 D1): applied seed injection to
  `skip_list.zig`, the last file in scope (`concurrent_skip_list.zig`, `robin_hood_hash_map.zig`,
  `cuckoo_hash_map.zig` done in cycles 7-9; `work_stealing_deque.zig` dropped, zero
  `std.time`/`std.crypto.random` sites). Consolidated `init`/`initWithSeed` into one
  `init(allocator, ctx, Options{ seed: u64 })`, no default; `initDefault()` now uses a fixed
  seed constant instead of the clock; `fromSlice()` gained `Options`; `clone()` copies the
  source's `prng` value directly (Xoshiro256 is a plain value type) to continue its sequence.
  2 new determinism tests mirroring `concurrent_skip_list.zig`'s pattern. Updated external call
  sites: `builder.zig`'s `toSkipList` (trailing `seed: u64`, matches `toHashMap`),
  `zoltraak_sortedset.zig` (fixed seed constant — also fixed a pre-existing arity bug at this
  call site, `InnerSkipList.init(allocator)` was missing its `ctx` arg entirely, invisible to CI
  via the same non-recursive-`refAllDecls` gap issue #38 found), `bench/lists.zig`,
  `bench/memory_profile.zig`, `examples/skip_list_demo.zig`, `tests/memory_safety_audit.zig`.
  Verified via `zig test` on the touched file plus a scratch driver importing `builder.zig`
  (137/137 pass, transitively covers `skip_list.zig`); `zig build` and `zig fmt --check` clean.
  Ticked the plan item. Filed #44 (not fixed — separate, unrelated bug) for
  `zoltraak_sortedset.zig`'s `range()`/`rangeByScore()` calling `ArrayList.append` with the wrong
  arity, found incidentally while compile-checking that file, same test-invisibility root cause
  as issue #38.
- PRs: #45 open (SkipList seed injection), Build & Test pending at the cycle deadline — left
  "awaiting CI; merge next cycle" comment, next cycle's inbox merges it. #43 merged.
- Next: merge #45 once green. Plan 001's io/seed rollout item (line 101) is now fully complete —
  advance to the next unchecked item: `std.time.*` → `Io.Clock` in the container layer (21
  sites) or the `mem.indexOf*`/`AutoArrayHashMap` mechanical-rename item (line 78, also unchecked
  and independent) — either is a reasonable next pick.
- Blockers: none. Open questions: none.

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
