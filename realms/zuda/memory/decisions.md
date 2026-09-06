# zuda — decisions

_(migrated from the repo's former `.claude/memory/decisions.md`, 2026-09-05)_

## Decision: project scope -- complement std, don't replace
- **Date**: 2026-03-07
- **Context**: need to decide relationship with Zig standard library containers.
- **Decision**: zuda complements std. It does not reimplement ArrayList, HashMap, etc. It
  offers *alternative* structures with different trade-offs.
- **Rationale**: avoids ecosystem fragmentation. Users import zuda for structures std
  doesn't provide.
- **Consequences**: must document when to use std vs zuda for each category.

## Decision: module-per-file organization
- **Date**: 2026-03-07
- **Context**: how to organize 100+ data structures.
- **Decision**: one data structure per file, grouped in category directories
  (`containers/trees/`, `algorithms/sorting/`, etc.).
- **Rationale**: easy navigation, clear ownership, manageable file sizes (< 800 lines).
- **Consequences**: root module must re-export all public types. More files to manage.
  (Since violated 76x by the scientific-computing modules -- see `STATE.md`.)

## Decision: Zig 0.15.2 as minimum version
- **Date**: 2026-03-07
- **Context**: which Zig version to target.
- **Decision**: minimum Zig 0.15.2.
- **Rationale**: latest stable at the time. Use modern APIs (unmanaged ArrayList, etc.)
- **Consequences**: must follow 0.15.x patterns; cannot use unreleased features.
  (Superseded kingdom-wide by the 0.16.0 migration, plan `001` -- see `REALM.md`.)

## Decision: PersistentRBTree without reference counting
- **Date**: 2026-03-14
- **Context**: how to handle structural sharing in persistent data structures.
- **Decision**: use path copying with shared subtrees, WITHOUT automatic reference counting.
- **Rationale**:
  - Simpler implementation (no refcount overhead on every node).
  - Better performance (no atomic operations for thread-safety).
  - Most use cases only need a single active version (undo/redo, transactions).
  - Users needing concurrent versions can use an arena allocator for version sets.
- **Trade-off**: requires careful version lifetime management -- old versions must be
  deinit'd before creating new ones.
- **Documentation**: clear doc comments with safe/unsafe pattern examples.
- **Future**: can add a reference-counted variant if demand arises (`PersistentRBTreeRC`).

## Decision: keep 4 of the 13 legacy per-file distribution duplicates, drop 9
- **Date**: 2026-09-06
- **Context**: `src/stats/distributions/*.zig` had 13 files duplicating (or, for
  `multivariate_normal`, never reaching) names already in the canonical
  `src/stats/distributions.zig` catalog — REALM.md/STATE.md described all 13 as reachable only
  from `root.zig`'s test-trigger block, but a pre-delete grep showed `chi_squared.zig`,
  `student_t.zig`, `f_distribution.zig` are real dependencies of `stats/hypothesis.zig` and
  `stats/correlation.zig`, and `chi_squared.zig` internally imports `gamma.zig`.
- **Decision**: deleted the 9 files with zero real consumers (`uniform`, `normal`,
  `exponential`, `poisson`, `binomial`, `bernoulli`, `geometric`, `beta`,
  `multivariate_normal`) plus their `root.zig` test-import lines (PR #32). Kept `gamma`,
  `chi_squared`, `student_t`, `f_distribution` in place.
- **Consequence / follow-up**: `hypothesis.zig`/`correlation.zig` still depend on the legacy
  per-file `StudentT`/`ChiSquared`/`FDistribution` instead of `distributions.zig`'s versions —
  migrating those two call sites to the canonical catalog (then deleting the last 4 legacy
  files) is separate follow-up work, not done this cycle.

## Decision: ship `zig build tidy` standalone, don't gate `test` on it yet
- **Date**: 2026-09-06
- **Context**: plan 001 item 2 said "add a tidy step ... wired into `zig build test`" and its
  verify line assumed `zig build tidy` would exit 0 on `main`. Vendoring the kingdom reference
  lint (`citadel/templates/tidy/tidy.zig` → `tools/tidy.zig`, PR #33) and running it against
  `main` found **4,608 failing findings** outside function-length: 3,728 line-length (>100
  cols), 575 ban-list (mostly `catch unreachable`, `std.time.*`, `anyerror` on `pub fn`), 301
  missing `//!` headers — the accumulated cost of 445 files written before this lint existed.
  Function-length is the one check with a baseline mechanism (shrink-only ratchet); the other
  four checks have no such escape hatch in the reference tool.
- **Decision**: wired `tidy` as its own `zig build tidy` step, not a dependency of `test_step`.
  Populated `tidy_baseline.txt` with all 620 pre-existing over-length functions so that check is
  clean today. Amended `docs/plans/001-*.md` in the same PR: item 2's text and verify line now
  describe what shipped, and a new unchecked item tracks gating `test` on tidy once later
  migration items (mechanical renames; `std.time`/`std.fs`/`std.Thread` → `Io`) remove most
  ban-list sources, plus a dedicated line-length/doc-header cleanup pass.
- **Rationale**: rule 6 (every commit passes `zig build test`) forbids landing a change that
  turns CI red; gating `test` on 4,608 pre-existing findings now would do exactly that, for a
  scope far larger than one cycle's item. This is a judgment call, not something the plan text
  anticipated — flagged here rather than silently deviating.
- **Known tool limitation found while generating the baseline**: `tidy.zig`'s function-length
  baseline keys on `"path:function_name"` — a file with two functions sharing a name (found in
  `btree.zig`, `skip_list.zig`, `concurrent_skip_list.zig`, all a private `compare` helper, and
  `dueling_dqn.zig`'s `init`) collide on one key, so the baseline can't cleanly cover both. Left
  as 4 residual unbaselined findings (harmless while tidy isn't gating anything) rather than
  reworking the vendored reference tool; worth an upstream citadel fix (per-line-number keys, or
  first-occurrence-only actual tracking) before tidy is made to gate `test`.
