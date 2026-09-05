# zoltraak — STATE

Survey date: 2026-09-05. Sources: repo survey + Zig 0.16 breakage probe, this session.

## What exists (claimed vs actually present)

Claimed (CLAUDE.md/docs/milestones.md): 452 iterations, 500+ Redis commands, full
RESP2/RESP3, RDB+AOF persistence, replication, pub/sub, transactions, a complete Lua
engine, ACL enforcement, multi-DB, single-node Cluster, Sentinel failover, TLS,
Functions, JSON, search (FT.*), time series, probabilistic types, vector sets.

Actually present, verified: a large buildable 141,060-LOC `src/` tree laid out exactly
along those lines (`commands/`, `storage/`, `protocol/`, `scripting/`, `network/`), a
clean `zig build`, CI green on the last 3 `main` runs, ~1098 unit tests passing plus a
226-file integration suite (estimator: ~5920 total tests). The claims are largely
corroborated. Two honest gaps: (1) all `BLOCK`-family commands still use a polling loop,
not the unwired `src/storage/blocking.zig` event infra; (2) manifest version (0.2.0) has
not tracked the claimed iteration count or the actual latest tag (see Risks).

## Sizes

- `src/`: 141,060 LOC across ~90 `.zig` files; `commands/` 41 files, `storage/` 34 files.
- Tests: 1098 unit/embedded tests (build), 226 integration test files, ~5920 estimated
  total. Full `zig build test` run: ~6s, 205/208 build steps succeeded, 3 failed (2
  known-flaky crashing binaries + their retry step).
- Files over 800 lines: 44 of ~90 (49%). Largest: `storage/memory.zig` 15,650,
  `commands/strings.zig` 7,869, `commands/json.zig` 5,417, `storage/cluster.zig` 5,733,
  `commands/sorted_sets.zig` 5,206, `commands/client.zig` 4,991, `commands/keys.zig`
  4,052, `commands/cluster.zig` 4,483.

## CI / issues / PRs

- CI: green. Last 3 `main` runs all `completed`/`success` (Iterations 452, 451, 450).
- Open issues: none. Open PRs: none.
- Uncommitted work found and preserved as `wip/migrate-real-dump-restore`: real
  `MIGRATE` (TCP DUMP/RESTORE) in `src/commands/cluster.zig`, 295+/56- lines, tests
  included, `zig build test` green with it applied — complete and ready to PR, not
  abandoned.

## Tiger Style gap table

| Check | Count | Note |
|---|---|---|
| Files over 800 lines | 44 / ~90 | `memory.zig` 15,650 is the extreme outlier |
| `std.debug.print` in `src/` | 105 | contradicts repo's own cleanup rule |
| `catch unreachable` | 17 | unaudited for client-input-reachable violations |
| Unbounded `while (true)` | 11 | some legit server loops, some the polling gap |
| `assert` | 5 | very low for 141K LOC under Tiger Style's own bar |
| `@panic` | 0 | — |
| Functions over 70 lines | not measured | flagged: strings.zig, memory.zig, client.zig |

## Zig 0.16 probe summary

- `zig build` on 0.15.2: succeeds cleanly.
- 0.16.0: fails at the build-script stage before any source compiles. `build.zig` (this
  repo) and both deps' `build.zig` (sailor, zuda) all fail identically on
  `Step.Compile.linkSystemLibrary`/`linkLibC`, which no longer exist in that form — 3
  errors, mechanical fix, but blocks everything downstream until sailor and zuda ship
  0.16-compatible build scripts.
- Once past the build script (probed via a temporary, deleted, untracked aggregator
  file), ~12 distinct 0.16 API-break classes across ~40 of 89 `src/` files:
  - `ArrayList(T){}` empty-literal removed — 63 hits, mechanical (`.empty` or
    `initCapacity`).
  - `std.time.*Timestamp` removed — 19 hits, needs `Io`-based clock threaded through.
  - `std.Thread.Mutex` moved to `std.Io.Mutex` — 9 hits.
  - `std.net` moved under `std.Io.net` — 8 hits, the hard architectural piece (TLS,
    replication, redis_api, core server networking).
  - `std.fs.cwd()`/`std.fs.File` reorganized — 8 hits (AOF persistence, Sentinel config).
  - `std.heap.GeneralPurposeAllocator` renamed `DebugAllocator` — 3 hits, trivial rename.
  - `ArrayList.writer()` removed — 1 hit, needs an `Io.Writer` adapter.
- Excluded from the above: ~730 "expected N argument(s)" errors are pre-existing broken
  test call sites, unrelated to Zig version (reproduce identically on 0.15.2).
- Blockers: sailor v2.99.0 and zuda v2.0.4 both fail their own `build.zig` on `linkLibC()`
  under 0.16 — zoltraak cannot fully build+test on 0.16 until both ship 0.16-compatible
  build scripts (tracked kingdom-wide as v3.0.0 for both, per `blocked_by` in REALM.md).
- Effort estimate: large, 5-15 sessions — the ArrayList class is bulk-mechanical, the
  `std.net`/`std.fs`/`std.time`/`Mutex` classes are the real architectural lift.

## Docs / root hygiene (next hygiene PR should fix)

- Root: delete tracked `.DS_Store` and the 0-byte tracked binary stub `test_cms_sig`;
  untrack the generated `.iteration` counter file; gitignore the untracked `zig-pkg/`
  dependency-cache directory left by a local build.
- `docs/`: stray `docs/.DS_Store`; 4 leftover `docs/iteration_52_checklist/_plan/_spec/
  _summary.md` files superseded by `docs/milestones.md`; 4 more leftover iteration-261
  working docs under `docs/iterations/`. `docs/PRD.md`, `docs/milestones.md`, and the
  named spec docs (TLS, XREAD BLOCK, keyspace notifications, JSON phase 12, BF.INSERT,
  bloom comparisons) are legitimate and should stay (move under `docs/specs/` or
  `docs/plans/` per `citadel/core/rules/docs.md` shape when the repo is reshaped).
- `.claude/` (being deleted this restructure): 9 bespoke agents (spec-analyzer →
  test-writer/implementor → quality/code reviewer → integration-orchestrator →
  compat/perf validators → commit-push) captured for context only, not carried forward
  as files; dozens of loose iteration/spec/summary `.md` files at `.claude/` root and
  `.claude/specs/` (14 files) are working-session artifacts, safe to drop — their durable
  content is either superseded by `docs/milestones.md` or captured in realm memory now.

## Next work candidates

1. Open the preserved `wip/migrate-real-dump-restore` branch as a PR (complete, tested).
2. Root/docs/`.claude` hygiene pass (listed above) — do this restructure's own PR.
3. Root-cause the two crashing RDB round-trip tests (`test_iter437`, `test_iter432`,
   signal 4) — the most concrete outstanding item in the project's own docs.
4. Reconcile the version 3-way divergence (zon 0.2.0 / old CLAUDE.md claim 0.2.13 /
   actual tag v0.2.14) against `citadel/protocol/VERSIONING.md` before any release.
5. Migrate Sorted Set to `zuda.compat.zoltraak_sortedset` (READY, ~1800 LOC removable).
6. Wire `src/storage/blocking.zig` into `server.zig`'s event loop for true blocking
   semantics (est. 3-4 iterations, plus a 5-6 iteration event-loop refactor prerequisite).
7. Reduce the 105 `std.debug.print` calls and begin splitting `memory.zig` (15,650
   lines) and `strings.zig` (7,869 lines).
8. Zig 0.16 migration — blocked on sailor/zuda v3.0.0; see probe summary above.

## Risks carried forward

- Version divergence across three sources (see Next work #4) — flagged, not yet fixed.
- Two illegal-instruction (signal 4) test crashes on RDB deserialize — plausible
  corruption/safety-check vector, not confirmed benign.
- 44/~90 files over 800 lines is a maintainability and merge-conflict risk at scale.
- Zero open GitHub issues/PRs on a codebase built entirely by unattended AI iterations —
  no external review surface visible on GitHub; worth periodic human spot-checks.
- No secrets found in tracked config; `zoltraak.conf`/`appendonly*` correctly untracked.
