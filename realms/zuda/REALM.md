# zuda — Realm

| | |
|---|---|
| Layer | Library |
| Path | `/Users/fn/codespace/zuda` |
| GitHub | `yusa-imit/zuda` |
| Version | 2.3.0 (`build.zig.zon`) · latest tag v2.3.0 (92 commits ahead, unreleased) |
| Zig | 0.15.2 (migrating to 0.16.0 under plan `001`) |
| Depends on | none (`build.zig.zon` `.dependencies` is empty — self-contained) |
| Consumers | zr, silica, zoltraak (sailor: reference only, not a dependent) |
| blocked_by | — |
| CI | Linux tests (8–10 min) + 6 cross-compile targets (`.github/workflows/ci.yml`) |
| cycle_minutes_max | 22 (full `zig build test` takes 8–10 min locally: run it at most once per cycle) |
| test_command | `zig test src/<touched file>.zig` (module-level) during the cycle; CI runs the full suite |

## What it is

zuda is a very large Zig 0.15.2 library of data structures, algorithms, and a NumPy/SciPy-style
scientific-computing stack: ~60 containers, 24 algorithm families (sorting, graph, DP, string,
geometry, ML, compression, ...), an `NDArray` with BLAS L1-3 + SIMD auto-dispatch and
LU/QR/SVD/Cholesky/Eigen, 209 probability distributions, FFT/signal processing, numeric
integration/ODE/interpolation, and optimization (BFGS/L-BFGS/Nelder-Mead/QP/LP/autodiff), grown
mostly by an autonomous session loop that adds roughly one new distribution per FEATURE cycle.
Actual scale (445 files, 461,635 LOC in `src/`) is far larger than the stale README/CHANGELOG
claim (8 distributions, 4600 tests — real numbers are 209 and ~22.3k `test "` blocks); `zig
build` and `zig build test` both pass locally under Zig 0.15.2 today. Full survey: `STATE.md`.

## Build and test

```bash
zig build              # library + CLI, well under 3 min
zig build test         # unit tests (~8-10 min for the full ~22k-test suite; CI-measured)
zig fmt --check src build.zig
```

Local-only: `zig build`, `zig build test`. CI-only: cross-compile, benchmarks, fuzz.
Pure library — no servers or ports to manage. `LockFreeStack`/`LockFreeQueue` need 128-bit
atomics and are macOS-only by design; CI cross-compiles 6 targets but only ever *runs* tests on
the CI host's own architecture, so non-macOS correctness of those two types is unverified beyond
compilation — don't "fix" that without reading `memory/debugging.md` first. A branch preserved
from this session's dirty working tree, `wip/random-forest-regression-criterion`, holds an
uncommitted RED-phase test proving `RandomForest.fit()` hardcodes the Gini split criterion even
for regression forests (`src/algorithms/machine_learning/random_forest.zig:161`) — finish that
TDD cycle (branch the criterion on `forest_type`) before other work touches that file.

## Realm-specific rules

- **Container API shape** (all ~60 containers, predates and is denser than kingdom Tiger Style
  in places — e.g. the Managed variant intentionally stores an allocator): allocator-first,
  Managed variant stores the allocator and Unmanaged takes it per call (mirrors
  `std.ArrayListUnmanaged`); comptime-parameterize comparators/hash/branching, never runtime
  dispatch; iterator protocol `next() -> ?T`; every container ships `validate()` asserting
  internal invariants; every public fn's doc comment states `/// Time: O(..) | Space: O(..)`.
  Follow the existing file's convention when touching a container — don't silently rewrite it to
  bare Tiger Style mid-feature; a full naming/API pass is its own plan item, not a side effect.
- **File template order**: type def -> lifecycle (init/deinit/clone) -> capacity -> modification
  -> lookup -> iteration -> bulk -> debug (format/validate) -> tests at bottom. One structure per
  file; target < 800 lines (violated 76x today — see Known gaps).
- **Error naming**: descriptive, never generic — `error.KeyNotFound`, `error.TreeInvariant`,
  `error.CapacityExceeded`, `error.CycleDetected`.
- **Distribution catalog discipline** (`src/stats/distributions.zig`, 209 types in one file):
  grep `pub fn <Name>` before implementing any new distribution — the duplicate-name pattern has
  already happened twice (JohnsonSU, ExGaussian). Verify obscure formulas via WebSearch/mpmath
  before coding, never from memory alone. Never add a `std.fmt("{f}", ...)` smoke test against a
  distribution's `format()` — all ~209 still use the legacy 3-arg signature and such a test fails
  to compile; this is an accepted, file-wide, currently-open gap (see `memory/patterns.md`).
- **Consumer registry** (drives zuda-first priority beyond the generic kingdom rule in
  `core/rules/00-kingdom.md`): `zr` needs DAG + Kahn topological sort + cycle detection +
  Chase-Lev work-stealing deque + Levenshtein distance + glob matching; `silica` needs a B+Tree
  (4300 LOC today) + LRU buffer pool + deadlock-detection DFS; `zoltraak` needs
  SortedSet->SkipList/RBTree + HyperLogLog + geohash/haversine + glob + LRU expiry; `sailor` is
  TUI-specific and reference-only, not a migration target. Protocol: read the consumer's current
  implementation first, design for a minimal-diff migration, then file
  `chore: migrate to zuda for <DS>` on the consumer repo, labels `migration,from:zuda`.
- **Local `zr` tool**: `zr.toml` at repo root drives `zr run build|test|check` as an optional
  local convenience; it is independent of the citadel cycle, which drives this repo with plain
  `zig build`/`zig build test`. File `zr` bugs found while using it on `yusa-imit/zr`, labels
  `bug,from:zuda` / `feature-request,from:zuda`.

## Layout

| Path | What's there |
|---|---|
| `src/root.zig` | library root; re-exports every public type; `refAllDecls` test |
| `src/main.zig` | trivial demo exe, deliberately import-free to keep exe compile fast |
| `src/containers/` | ~60 data structures across 13 subdirs (trees, heaps, hashing, spatial...) |
| `src/algorithms/` | 24 category dirs (sorting, graph, DP, geometry, compression, greedy...) |
| `src/algorithms/machine_learning/` | 72 files: regressors, boosting, clustering, RL (DQN..TRPO) |
| `src/ndarray/` | `NDArray(T, ndim)` — broadcasting, slicing, reductions, SIMD (24.5k LOC) |
| `src/linalg/` | BLAS L1-3 + SIMD auto-dispatch, LU/QR/Cholesky/SVD/Eigen, sparse, iterative |
| `src/stats/` | 209 distributions in one 128k-line file; descriptive/hypothesis/regression/RNG |
| `src/signal/` | FFT/DCT/windows/convolution/FIR-IIR filters |
| `src/numeric/` | integration, differentiation, root finding, interpolation, ODE, curve fit |
| `src/optimize/` | GD/BFGS/L-BFGS/Nelder-Mead, constrained (QP/LP), least squares, autodiff |
| `src/iterators/` | Map/Filter/Chain/Zip/Take/Skip/FlatMap/Enumerate/Partition/collect |
| `src/compat/` | API-parity shims for silica (BTree), zoltraak (SortedSet), zr (DAG) |
| `src/ffi/` + `include/zuda.h` | C ABI exports |
| `src/internal/` | `testing.zig`, `bench.zig` — property-test helpers, not public |
| `src/utils/` | builder, compare, debug, hash, perf helpers |
| `tests/` | 2 integration files, 43 tests |
| `bench/` | 16 benchmark suites |
| `examples/` | 42 files incl. python/nodejs bindings, migration demos |
| `.disabled/` | 3 tracked dead legacy files — removed by the hygiene PR |

## Known gaps (from STATE.md)

- 76 files > 800 lines (`distributions.zig` 128,392 lines, `ndarray.zig` 24.5k, `blas.zig`
  16.6k, `simd_blas.zig` 10.7k) — dominates the 8-10 min full test suite.
- 69 `catch unreachable` (48 `distributions.zig`, 12 `correlation.zig`, 3 `decision_tree.zig`,
  6 misc), 31 `std.debug.assert` (~20 knowingly deferred), 17 `std.debug.print` (14 are library
  violations), 111 `while (true)` (mostly bounded, 2 unfixed `p < 1e-300` f32-underflow sites).
- Zig 0.16 migration: `build.zig` fails first (`Compile.linkLibC`), then 44 concrete source
  errors across 5 classes (`std.time`, `ArrayList` literal shape, `std.fs.cwd()`,
  `AutoArrayHashMap`, `std.io`); true count is higher once every module compiles. No blocking
  kingdom dependencies. Effort estimate: medium, 2-5 sessions.
- Version/doc drift: `build.zig.zon` 2.3.0, `zr.toml` 0.0.0, `main.zig` banner "2.0.4",
  CHANGELOG stops at 2.0.0, README claims 8 distributions/4600 tests (actual 209/~22k); 92
  unreleased commits with a release protocol that structurally never fires for catalog growth.
- Root/docs hygiene: tracked binaries, `docs/sources.tar` (14.8 MB), autodoc output,
  `.disabled/`, and the old `.claude/` tree (38 files, 12 orphan test files) — full list and
  disposition in `STATE.md`, cleared by the hygiene PR.
- `wip/random-forest-regression-criterion` preserved this session — see Build and test above.
