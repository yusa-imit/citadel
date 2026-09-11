# zuda — context

last_seen_at: 2026-09-11T00:00:00Z
rejected_plans: []

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

## Cycle 4 — 2026-09-09 — FEATURE
- Done: preflight found `fix/build-zig-016-linklibc` (cycle 3's dirty-tree carryover) already
  pushed as green, mergeable PR #34 — merged it (squash, branch deleted) before continuing.
  Inbox reconciled milestone #31: items 2 (#33) and 3 (#34) were merged in prior/this cycle but
  never ticked — ticked both. Implemented item 4 "mechanical renames" scoped to the subset
  that's dual-compatible with the repo's current 0.15.2 CI pin and 0.16:
  `heap.GeneralPurposeAllocator` → `heap.DebugAllocator` (7 files) and
  `ArrayListUnmanaged(T) = .{}` → `.empty` (2, `rabin_karp.zig`). Verified via toolchain probe
  (0.15.2 vs 0.16.0 std source) that `mem.indexOf*` → `find*` and
  `std.AutoArrayHashMap` → `AutoArrayHashMapUnmanaged` are NOT dual-compatible — 0.15.2 has no
  `find*` at all, and 0.16 removes managed `AutoArrayHashMap` outright (a call-site rewrite, not
  a rename) — split those into a new plan item paired with the toolchain-flip item (item 10)
  where the 0.16 target API can be verified directly instead of guessed at from behind the pin.
- PRs: #35 open (mechanical renames), CI still running (Build & Test pending) at the cycle
  deadline — left "awaiting CI; merge next cycle" comment, next cycle's inbox merges it.
- Next: merge #35 once green, then plan 001 item 5 ("Fix the public `io: Io` API shape + ADR" —
  the v3.0.0 signature break, call `architect` first).
- Blockers: none. Open questions: none.

## Cycle 3 — 2026-09-08 — DISK
- Done: preflight disk gate failed (16GB free < 20GB required) — cycle aborted before
  inbox/mode selection, before touching the repo. No commits, no PRs, no branch changes.
- PRs: none touched this cycle.
- Next: unchanged from cycle 2 — merge #33 once green, then plan 001 item 3 (already merged
  as of `40a620b`/`537b3aa` on `fix/build-zig-016-linklibc` per repo git log, not yet reflected
  in this memory — next cycle should verify PR state and reconcile before picking new work).
- Blockers: host disk space (16GB free); no action available to this session (unattended, no
  human wait). Open questions: none.

## Cycle 2 — 2026-09-06 — FEATURE
- Done: merged PR #32 (cycle 1's clear-the-decks work, CI was green), ticked milestone #31
  item 1. Implemented item 2: vendored the kingdom reference tidy lint
  (`citadel/templates/tidy/tidy.zig`) into `tools/tidy.zig`, wired as a standalone
  `zig build tidy` step. `tidy_baseline.txt` (620 entries) makes function-length clean (0
  findings); deliberately did NOT wire tidy into `test_step` — `main` has 4,608 pre-existing
  failing findings outside function-length (3,728 line-length, 575 ban-list, 301 missing `//!`
  headers). Amended `docs/plans/001-*.md` item 2 in the same PR to record this and added a new
  unchecked item for wiring tidy into `test` once later migration items shrink the count — see
  `decisions.md` for the full reasoning.
- PRs: #33 open, CI still pending (queued) at the cycle deadline — left a status comment,
  next cycle's inbox merges it once green.
- Next: merge #33, then plan 001 item 3 (`build.zig` 0.16 API pass, `linkLibC`).
- Blockers: none. Open questions: none.

## Cycle 1 — 2026-09-06 — FEATURE
- Done: plan 001 (Zig 0.16 migration) merged by owner before this cycle started. Opened
  milestone tracking issue #31. Implemented item 1 "Clear the decks" on PR #32: fixed
  `RandomForest.fit()` hardcoding `.gini` for regression forests (finished the preserved
  `wip/random-forest-regression-criterion` TDD cycle — branch fixed itself, wip branch still
  present, not deleted), dropped 9 orphaned distribution duplicates (kept 4 with real
  consumers, see `decisions.md`), removed dead `.claude/memory/**` `ci.yml` entry, synced
  `zr.toml`/`main.zig` version strings to 2.3.0.
- PRs: #32 open, Build & Test + wasm32-wasi green, 5 cross-compile targets still pending at
  the cycle deadline — left a status comment, next cycle's inbox merges it.
- Next: merge #32 once CI is green, then plan 001 item 2 (`tidy` build step).
- Blockers: none. Open questions: none.

## Cycle 0 — 2026-09-05 — RESTRUCTURE
- Realm created by citadel restructure. Memory migrated from the repo's former
  `.claude/memory/` (architecture.md, decisions.md, debugging.md, patterns.md,
  project-context.md — the retired `MEMORY.md` stub and one-off `session-186.md` were
  dropped; nothing durable in either was lost). First plan `001` prescribed by
  `citadel/docs/ROADMAP.md` (Zig 0.16 migration).
- Next: open plan 001 PR (if not open) -> await human merge.
- Open questions: none.

## Standing backlog (carried from the repo's former project-context.md)
- `catch unreachable` OOM-swallow audit: 69 sites remain (48 `distributions.zig`, 12
  `correlation.zig`, 3 `decision_tree.zig`, 6 misc across bayesian/deque/pairing_heap).
- Two leftover `p < 1e-300` f32-underflow sites in `distributions.zig` (~lines 71325, 81533).
- ~20 deferred `std.debug.assert` sites in `src/algorithms/` + private tree/hash helpers.
- `logFactorial` is exact only for `n < 20`, Stirling beyond — keep Binomial-family tests
  under n=20 or loosen tolerance; raising the cutoff is a real fix, cross-cutting, still open.
- Release: 92 commits since v2.3.0 (11 new distributions, 199->209, plus fixes) never
  triggered a release under the old per-repo protocol because catalog growth flips no
  milestone checkbox — cut v2.4.0 and backfill CHANGELOG 2.0.1-2.3.0 next release cycle.
- `RandomForest.fit()` hardcodes the Gini split criterion even for regression forests — see
  Preserved work below; this is the single most concrete next action.

## Next priority (feature vein, from the repo's own notes)
- Devroye (1993) discrete-stable triptych members beyond Sibuya (209th) — discrete
  Mittag-Leffler is the next candidate; Neyman Type B/C need HyperPoisson-style numeric
  architecture. Location-shift, vector-param, and bivariate-latent-variable veins are
  exhausted. Always grep `pub fn <Name>` in `distributions.zig` before implementing a new
  one — duplicate names (JohnsonSU, ExGaussian) have shipped before under time pressure.

## Preserved work
- `wip/random-forest-regression-criterion` (this repo's branch): a RED-phase test proving
  `RandomForest.fit()` calls `tree.fit(..., .gini)` unconditionally
  (`src/algorithms/machine_learning/random_forest.zig:161`), so regression forests with
  fractional targets collapse to the global mean. Finish this TDD cycle first — branch the
  criterion on `forest_type` (`.mse`/variance for regression), commit test + fix together,
  delete the stray 0-byte `random_forest` binary.
