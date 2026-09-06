# zuda — context

last_seen_at: 2026-09-06T07:30:00Z
rejected_plans: []

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
