# zr — STATE

Survey date: 2026-09-05 (citadel restructure). Sources: repo survey + Zig 0.16 breakage probe.

## What exists (claimed vs present)

Present and real: README/CHANGELOG claim a mature "universal developer platform" (v1.114.0)
unifying task running, toolchain management, and monorepo tooling with MCP/LSP integration in a
single ~1.2MB binary. This is substantiated: config/TOML+expr engine, graph/DAG scheduling,
exec/scheduler+worker-pool+remote(SSH)+retry/circuit-breaker/checkpoint, cache (local + S3/GCS/
Azure/HTTP), toolchain (~8 languages), multirepo, plugin (native+WASM+5 built-ins), watch,
history, mcp/lsp/jsonrpc, analytics/ci/codeowners/conformance/migrate/registry/template/upgrade
are all real, sized modules. 1798 unit + 2087 integration tests pass; not vaporware.

Claimed vs present gap: README's version badge still shows v1.84.0 vs actual v1.114.0.
CLAUDE.md's repo-structure diagram is stale (`main.zig` claimed ~550 lines, actually 3299;
"~34 modules" is a generic leftover). CHANGELOG shows continuous small-feature churn, including
a v1.113.1 entry citing "~270 failures across many unrelated test files, now fully resolved" —
a recent CI-red period, even though the current tree is green. `.claude/memory/project-
context.md`'s "Next Action" section referenced v1.89.0-era planning despite the repo being at
v1.114.0 — stale enough that an automated session reading it for priority would be misled.

## Sizes

| Metric | Value |
|---|---|
| `src/` LOC | 112,502 |
| Test count (estimate) | 4,023 (1798 unit + 2087 integration + skipped, per test-file scan) |
| Files > 800 lines | 24 (worst: `config/parser.zig` 8299, `exec/scheduler.zig` 3755) |
| Tracked root files | 17 (4 are historical `RELEASE_NOTES_*.md`, 1 is a tracked `.o` binary) |
| `docs/guides/` | 24 guides + `PRD.md`, `PLUGIN_DEV_GUIDE.md`, `plugin-registry-api.md` |
| `.claude/` (pre-restructure) | 58 tracked files, ~20+ ad hoc session-summary/cycle diary files |

## Build / test / CI

- Local (Zig 0.15.2, matches CI pin): `zig build` OK, no errors/warnings. `zig build test`:
  PASS, 1798 passed / 8 skipped / 0 failed, ~49s wall (measured this session).
- CI: GREEN — last 3 runs via `gh run list`: CI on `main` success (12m12s); Release on
  `v1.114.0` tag success (5m28s); one CI run cancelled as superseded (not a failure).
- Open issues: 0. Open PRs: 1 (`#30 chore: migrate to zuda for graph algorithms`).
- Dirty tree (preserved on `wip/advanced-retry-config`, not discarded): a complete, tested
  feature — `splitTopLevelFields()` bracket/quote-aware comma-splitter for inline TOML tables,
  replacing a naive `splitScalar(',')` at 2 call sites, plus 5 new retry-template fields
  (`retry_backoff_multiplier`, `retry_jitter`, `max_backoff_ms`, `retry_on_codes`,
  `retry_on_patterns`) threaded end-to-end with a passing test. Full suite was green on the
  dirty tree (1799/1799 non-skipped).

## Tiger Style gaps

| Check | Count | Note |
|---|---|---|
| `assert` | 0 | Across 112.5k LOC — no runtime precondition/invariant checking at all |
| `catch unreachable` | 12 | Each a potential panic if the "impossible" error occurs |
| `@panic` | 0 | — |
| `std.debug.print` | 93 | Plausibly intentional CLI/stderr output, not individually classified |
| `while (true)` (unbounded) | 46 | Not individually audited; some are legitimate service loops |
| Files > 800 lines | 24 | `parser.zig` 8299 (one ~5100-line `parseToml`), `scheduler.zig` 3755 |

Also noted: `functions_over_70_lines` sample found `parseToml` (~5112 lines) and
`flushCurrentHook` (~1970 lines) in `parser.zig` alone, plus `workerFn` (~1128 lines) in
`scheduler.zig` — measured via a rough heuristic over the 3 largest files only, so exact
boundaries may be imprecise but the population is clearly large kingdom-wide.

## Zig 0.16 probe summary

- `zig015_build_ok`: ok — `zig build` (global 0.15.2) completes cleanly.
- 0.16.0: **hard-blocked before reaching zr's own code.** Both `zig build` and
  `zig build test` fail immediately inside sailor's and zuda's own `build.zig` (each calls
  `<Step.Compile>.linkLibC()`, removed in 0.16.0) — zr's `build.zig` already uses the modern
  `createModule`/`root_module` pattern but is never reached, since `b.dependency("sailor"/
  "zuda", ...)` runs at the top of `build()`. zr cannot migrate to 0.16 until both deps ship a
  0.16-compatible `build.zig` (their own MAJOR bumps to v3.0.0 per `citadel/docs/ROADMAP.md`).
- **Error count** (methodology caveat below): 79 of 200 individually-`zig test`-ed src files
  failed standalone (28 more `@import` sailor/zuda directly and can't be tested standalone).
- **Error classes**: `ArrayList` unmanaged-literal rewrite — 31 files (`{}` needs
  `.initCapacity`/`.empty`, allocator threaded through every mutation); `std.fs.cwd()`/File/
  Io-based fs redesign — 8 files (`Dir.createFile` needs an extra `Io` arg, `realpathAlloc`
  gone); `std.heap.GeneralPurposeAllocator` → `DebugAllocator` — 3 files;
  `std.posix.getenv`/`std.process.getEnvVarOwned` removed — 4 files; `std.time.timestamp()`/
  `milliTimestamp()` removed — 2 files; `std.io` module gutted (`fixedBufferStream` moved) — 2
  files; `std.process.Child.init` removed — 3 files; switch-prong `|_|` capture now rejected —
  5 sites (trivial, remove the capture). 66% of the 227-file tree (149 files) touches at least
  one of fs/net/thread/time/process/posix/http/io.
- **Effort**: large (5-15 sessions), gated entirely on zuda/sailor landing their own 0.16
  `build.zig` first. Once unblocked: the `ArrayList` sweep is mechanical (largest single class);
  the fs→`Io` redesign is real design work touching a majority of files, comparable in scope to
  the already-tracked 0.14→0.15 migration, likely larger.
- Methodology caveat: standalone single-file `zig test` produces ~150 "import outside module
  path" false positives (an artifact of not using the real build graph) on top of genuine API
  breakage — the 79/200 figure and error-class counts above already exclude that noise.

## Docs / root hygiene (hygiene PR will fix)

- `env_file_test.o` (root): compiled object file tracked in git despite `*.o` being gitignored
  — delete and untrack.
- `RELEASE_NOTES_v1.57.0.md`, `v1.58.0.md`, `v1.60.0.md`, `v1.7.0.md` (root): historical release
  notes: move under `docs/` (or `docs/releases/`).
- `debug_lsp.sh`, `test_lsp_simple.sh` (root): ad hoc dev/test scripts — move to `scripts/`.
- Untracked `zig-pkg/` at repo root, not covered by `.gitignore` — could get committed by
  accident; add an ignore rule or remove it.
- Old `.claude/` carried zr-unique material now migrated into `citadel/realms/zr/memory/`:
  the TOML-mixin implementation checklist/summary/test-requirements docs (condensed into
  `patterns.md`), and durable architecture/decisions/debugging content. The ~20+ dated
  `session-summary-*.md`/`session-memory*.md`/`RELEASE_NOTES_*` diary files under `.claude/`
  were a running autonomous-session log, not migrated (superseded by GitHub history + this
  survey).

## Next work candidates

1. Decide on open PR #30 ("migrate to zuda for graph algorithms").
2. Finish or discard the `wip/advanced-retry-config` branch (feature is complete and tested).
3. Root/docs hygiene PR (see above).
4. Reconcile stale version claims: README badge (v1.84.0), `CLAUDE.md` line counts — largely
   moot post-restructure since `CLAUDE.md` itself is being retired in favor of this realm memory.
5. Establish a new feature milestone — `docs/milestones.md` had 0 READY milestones queued.
