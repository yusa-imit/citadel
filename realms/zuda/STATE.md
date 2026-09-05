# zuda — STATE (survey 2026-09-05)

## Claimed vs present

- CLAIMED (README/PRD/`docs/milestones.md`): "100+ data structures, 80+ algorithms"; v2.0
  scientific platform (NDArray, BLAS L1-3+SIMD, LU/QR/SVD/Cholesky/Eigen, solvers); "8
  probability distributions"; FFT/filters; integration/ODE/interpolation; optimization
  (BFGS/L-BFGS/Nelder-Mead/QP/LP/autodiff); C FFI; "4600+ tests"; milestones say phases 6-12
  COMPLETE and 198 distributions.
- PRESENT (verified in `src/`): all claimed modules exist; `zig build` passes locally (Zig
  0.15.2). Actual scale is far larger than claimed: 445 `.zig` files, 461,635 LOC, ~22,364
  `test "` blocks, **209** distribution types in one 128,392-line file
  (`src/stats/distributions.zig`, 11,713 test blocks in that file alone), 70+ ML algorithms
  (regressors, boosting, clustering, RL incl. DQN/PPO/SAC/TD3/TRPO), 24 algorithm categories,
  ~60 containers, compat shims for silica/zoltraak/zr, C API + header. `tests/` adds 2
  integration files (43 tests). 13 legacy per-file distributions in
  `src/stats/distributions/` duplicate names already in `distributions.zig`, referenced only
  from `root.zig`'s test block. `.disabled/` holds 3 dead files untouched by the build.
- README/CHANGELOG are stale (CHANGELOG's last entry is 2.0.0; README says 8 distributions,
  4600 tests). `docs/milestones.md` is closer (198 distributions, 14k tests) but also lags.
  92 commits since tag v2.3.0 are all catalog growth (+11 distributions, 199->209) plus small
  fixes; zero CHANGELOG entries because the release protocol only fires on a milestone
  checkbox flip and open-ended catalog work has none.

## Size

| Metric | Value |
|---|---|
| `.zig` files | 445 |
| Lines in `src/` | 461,635 |
| `test "` blocks (grep) | ~22,364 |
| Tests per `zig build test --summary` (last run) | ~14.7k |
| Files > 800 lines | 76 (repo's own rule targets < 800) |
| Largest files | `distributions.zig` 128,392 · `ndarray.zig` 24.5k · `blas.zig` 16.6k · |
| | `simd_blas.zig` 10.7k |
| Integration tests (`tests/`) | 43, in 2 files |

## Build/test status (local, Zig 0.15.2)

- `zig build`: **PASS**, exit 0, well under 3 min.
- `zig build test`: not attempted locally this survey — CI measures 8m34s-10m34s for the full
  suite (`distributions.zig` alone dominates compile+test time).
- Targeted run of the one uncommitted test (`random_forest.zig --test-filter "MSE not
  Gini"`): **FAILS** as intended — the RED phase of an interrupted TDD cycle, see Dirty tree.

## CI

GitHub Actions (build+test, then 6-target cross-compile). Latest 3 runs on `main`: success
(chore commit, 8m34s), cancelled (feat commit, superseded by concurrency cancel-in-progress),
success (10m34s). Effective HEAD conclusion: **GREEN**. `ci.yml`'s `paths-ignore` covers
`.claude/memory/**` and `*.md` but **not** `.claude/logs/` or `.claude/session-counter`, so
every routine "chore: update session counter/agent log" push burned a full ~10 min CI run —
moot once `.claude/` itself is removed from the repo by the hygiene PR.

## Open issues / PRs

None open on either.

## Dirty tree (session start, preserved as `wip/random-forest-regression-criterion`)

`random_forest.zig` gained one failing test proving `RandomForest.fit()` calls
`tree.fit(bootstrap_X, bootstrap_y, .gini)` unconditionally (line 161) even for regression
forests, so fractional targets truncate to class 0 and the forest collapses to the mean. Real
bug, well-formed RED-phase test — finish the cycle (branch to `.mse`/variance for
`forest_type == .regression`) rather than discarding it. `.claude/session-counter` and
`.claude/logs/agent-activity.jsonl` diffs are routine bookkeeping, moot once `.claude/` is
removed. A stray 0-byte `random_forest` binary should be deleted.

## Tiger Style gap table

| Check | Count | Note |
|---|---|---|
| `std.debug.assert` | 31 | ~20 knowingly deferred in `src/algorithms/` + private helpers |
| `catch unreachable` | 69 | 48 `distributions.zig`, 12 `correlation.zig`, 3 `decision_tree.zig` |
| `@panic` | 0 | clean |
| `std.debug.print` | 17 | 3 in `main.zig` (fine); 14 are library violations |
| `while (true)` | 111 | mostly bounded by `MAX_K`-style constants; 2 unfixed `p<1e-300` sites |
| Files > 800 lines | 76 | `distributions.zig` is ~160x the limit |
| Fns > 70 lines (sample) | ~96 | `double_array_trie.zig:init` 195, `pca.zig:fit` 176 |
| Recursive helpers | ~109 | depth bounded by input size, no explicit depth caps |
| `Bounded*` fixed-cap variants | ~0 of 206 files using `ArrayList` | asked for, none seen |

## Zig 0.16 migration probe

- `zig build`/`zig build test` on global 0.16: **build.zig fails immediately** —
  `Compile.linkLibC` no longer callable that way (needs `.root_module.link_libc = true`).
- Past that (probed via `zig test src/root.zig` directly): **44 concrete errors**, 5 classes:
  `std.time` timestamp APIs removed (21 sites, needs an `Io`-threaded clock or
  `std.time.Instant`), `ArrayList` unmanaged-literal shape changed (18, `.{}` ->
  `.empty`/`initCapacity`), `std.fs.cwd()` removed from root `fs` (14, all in `ndarray.zig`
  save/load, needs `Io.Dir`/`File`), `std.AutoArrayHashMap` moved out of `std` root (2, use
  `std.array_hash_map.AutoArrayHashMap`), `std.io.fixedBufferStream` gone (1, `utils/perf.zig`,
  needs the new `Io.Writer`/`Reader` fixed-buffer constructor).
- 20 files touch `std.fs`/`std.net`/`std.Thread`/`std.time`/`std.process`/`std.posix`/`std.io`
  outside what `root.zig`'s test graph reaches (ML/parallel modules) — the true error count
  once `build.zig` is fixed and every module compiles will be **higher than 44**.
- No blocking dependencies (`build.zig.zon` has zero `.dependencies` — self-contained).
- Effort estimate: **medium, 2-5 sessions** — fix `build.zig` first, then the `std.time`/
  `std.fs` changes likely need threading an `Io` context through several signatures, not a
  pure find/replace.

## Docs/root hygiene (fixed by the hygiene PR)

- Root: delete `find_max`/`simple_test`/`verify_mp` (~1.25 MB compiled binaries each) and
  `knapsack` (0-byte stub); move-or-delete `find_max.zig`/`verify_mp.zig` (throwaway numeric
  probes); delete/archive `SESSION_340.md` (superseded by memory).
- `docs/sources.tar` (14.8 MB, zig-autodoc input) and `docs/{index.html,main.js,main.wasm}`
  (autodoc output, generated) — untrack.
- `.disabled/` (3 files, 350 KB dead legacy code) — delete.
- `src/.claude/logs/agent-activity.jsonl` — stray mis-pathed log copy inside `src/` — delete.
- `.claude/` itself (38 tracked files: agents, commands, memory, 12 orphan `*_tests.zig`
  totalling ~5.6k lines, 3 stray reports, `DISK_FULL_CLEANUP.sh`) — removed by the next step
  per kingdom docs policy; this survey carried its durable memory into `citadel/realms/zuda/`.
- Repo pack is 13 MB, loose objects 94 MB; ~30 MB of gitignored scratch binaries/logs sit in
  the working tree, harmless but worth a periodic `git clean`.

## Next work candidates (unordered)

1. Finish `wip/random-forest-regression-criterion` (real regression-vs-Gini bug, test written).
2. Resume the `catch unreachable` OOM audit (69 sites) + 2 leftover `p < 1e-300` f32 sites +
   ~20 deferred `std.debug.assert` sites.
3. Cut v2.4.0: 92 unreleased commits, backfill `CHANGELOG.md` 2.0.1-2.3.0, sync version
   strings (`zr.toml` 0.0.0, `main.zig` "2.0.4", README, `root.zig` doc header).
4. Repo hygiene PR (see above).
5. Split `distributions.zig` (128k lines / 4.5 MB / 11.7k tests in one compilation unit) by
   family — the single biggest lever on the 8-10 min CI/test time.
6. Start the Zig 0.16 migration (plan `001`) — build.zig fix, then the 44+ source errors.
7. Consumer migrations still open: zr (zr#21-25), silica (silica#4-5), zoltraak
   (zoltraak#1-3).
