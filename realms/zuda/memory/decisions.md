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
