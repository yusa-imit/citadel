# strata — State survey

Surveyed 2026-09-05, as part of the citadel restructure. Source: repo inspection + a Zig
0.16.0 compile probe. This file is the honest baseline the `001` plan works from.

## What exists (claimed vs. present)

README.md and the (now-removed) CLAUDE.md describe an ambitious 10-module storage kernel:
codec, file I/O, checksummed pages + CLOCK buffer pool, segmented WAL with group commit and
crash recovery, B+Tree, LSM, an embedded KV engine, and a streaming snapshot format.
`docs/PRD.md` (186 lines, Korean) fully specifies that design. **None of it is implemented.**

Every one of the 10 module files (`src/{codec,file,page,cache,wal,btree,lsm,kv,snapshot,
testing}.zig`) is a ~19–23 line stub: a `//!` doc comment, `pub const Error =
error{NotImplemented};`, and a single `test "<mod>: module compiles" {
std.testing.refAllDecls(@This()); }`. Every nested subdirectory the docs describe (`codec/
varint.zig`, `file/mmap.zig`, `wal/segment.zig`, etc.) exists as an **empty directory** —
zero files in any of them. `src/root.zig` (25 lines) re-exports the 10 stubs; `src/main.zig`
(36 lines) is a minimal CLI (`strata version` / `--help`). `bench/main.zig` is a placeholder;
`examples/` and `tests/` hold only `.gitkeep`. `docs/milestones.md` lists Phase 1–6, every
checkbox unchecked, phase noted as "Bootstrap complete → Phase 1 starting".

This is a 2-commit-old bootstrap. Claimed scope vastly exceeds present scope — treat the
README/PRD as a design document, not a status report, until milestones.md says otherwise.

## Sizes

- `src/` total: 265 LOC across 12 files (10 stub modules + root.zig + main.zig).
- Tests: 11, all trivial (`refAllDecls` compile-checks plus one CLI version assertion).
- Files over 800 lines: 0 (nothing is over 40 lines yet).
- `docs/PRD.md`: 186 lines. `docs/milestones.md`: phase checklist, all unchecked.

## Build / CI

- `zig build`: exit 0, a few seconds, no errors (Zig 0.15.2, matches
  `minimum_zig_version`).
- `zig build test`: exit 0, 11/11 pass, well under any time budget.
- CI (`gh run list`, 2 runs total — one per commit): HEAD (`1a32aaf`, "ci: run tests on Linux
  only; macOS covered by cross-compile") = success (56s). Prior commit (`46a8b85`, bootstrap)
  = **failure** (46s), fixed by the very next commit. Current HEAD is green, but the fix has
  only been exercised on that one subsequent run — no long track record yet.
- Open issues: none. Open PRs: none.
- Working tree: clean at survey time (no dirty state, no `wip/*` branch to preserve for the
  foundation repos, strata included).

## Tiger Style gap table

| Metric | Count | Note |
|---|---|---|
| `assert(` | 0 | no logic of substance exists to assert over yet |
| `catch unreachable` | 0 | — |
| `@panic(` | 0 | — |
| `std.debug.print` | 0 | — |
| unbounded `while (true)` | 0 | — |
| files > 800 lines | 0 | largest file is 36 lines (`main.zig`) |
| functions > 70 lines | not measured | no function bodies of substance exist |

All metrics read clean only because there is nothing yet to violate. CLAUDE.md already
codified strong domain rules for when Phase 1 lands (checksum every disk byte, fsync as
policy, idempotent recovery, magic+version formats, no `@panic`/`catch unreachable`, page-size
matrix 512B–64KB) — carried into `REALM.md`; **re-audit this table once real code lands.**

## Zig 0.16 probe summary

- `zig build` (0.16.0): fails at **source compile**, not at `build.zig` — the build script
  itself is already 0.16-clean (no `std.Build` API breakage).
- `zig build test` (0.16.0): **passes**, 11/11 — `main()`'s body is never semantically
  analyzed in test mode, so the bug below is invisible to `zig build test` but fatal to
  `zig build` / `zig build run`.
- `zig test src/root.zig` (0.16.0): all 11 tests pass — the entire library (root.zig + all 10
  stub modules) is already 0.16-clean with zero changes needed.
- Error count: **1 class**, confined to `src/main.zig` (32 lines):
  1. `std.heap.GeneralPurposeAllocator` removed → rename to `std.heap.DebugAllocator` (same
     usage pattern, confirmed present in 0.16.0 `lib/std/heap.zig`).
  2. (latent, not yet hit by the compiler) `std.process.argsAlloc`/`argsFree` removed →
     replace with the new iterator-style `std.process.Args` API.
- `main.zig`'s stdout call already uses the new `File.stdout().writer(&buf)` pattern — no
  Reader/Writer migration needed there.
- Effort estimate: **trivial, under 1 hour**. Blocking dependencies: none (`.dependencies =
  .{}` — no kingdom deps to wait on). This is the cleanest of the repos probed so far.

## Docs / root hygiene (for the hygiene PR)

- `.claude/` (20 tracked files: settings.json, 6 agents, 8 commands, 5 memory files) is
  generic citadel-template scaffolding, not repo-unique tooling — safe to remove per
  `citadel/protocol/DOCS.md`. Its only repo-specific substance (decisions.md, project-
  context.md facts) has been migrated into `citadel/realms/strata/memory/`.
- `CLAUDE.md` at repo root: its unique, still-true content (kingdom role, dependency rule,
  strata-specific safety rules) is now in `citadel/realms/strata/REALM.md`; the file itself
  is due for removal — no `CLAUDE.md` belongs in a kingdom repo per policy.
- No other root-file hygiene issues: `root_files_to_remove_or_move` came back empty (only
  `.gitignore`, `LICENSE`, `README.md`, `build.zig`, `build.zig.zon` remain, all expected).
- `docs/PRD.md` and `docs/milestones.md` are correctly placed and should stay as-is.

## Next work candidates (unordered until plan 001 sequences them)

1. Phase 1A — `src/codec/{varint,fixed,crc32c,xxhash}.zig`: LEB128/zigzag varint, LE
   fixed-width, hardware-accelerated CRC32C with software fallback, xxhash64; standard-vector
   and boundary tests.
2. Phase 1B — `src/file/file.zig`: `File` + `SyncPolicy` (fdatasync/fsync/F_FULLFSYNC),
   preallocate, locks; `std.testing.tmpDir`-based writeAt/readAt/sync/preallocate/lock tests.
3. Phase 1C — `src/file/mmap.zig`: mmap abstraction.
4. Phase 1D — `src/testing/crash.zig`: crash-injection harness (torn writes, truncation at
   arbitrary offsets) and a differential model; later phases (WAL, B+Tree) depend on this.
5. Populate `docs/milestones.md` checkboxes and `memory/architecture.md` as each item lands.
6. Populate `examples/` and `tests/` (currently `.gitkeep` only) once Phase 1 APIs stabilize.
7. Zig 0.16 migration (plan `001`): trivial, <1h — GPA rename + `process.Args` rewrite in
   `src/main.zig` only; do in the same cycle as, or just before, Phase 1A so new code is
   written against 0.16 shapes from the start (per `citadel/core/rules/zig-0.16.md`).

## Risks

- Scope/claim gap: README's own install instructions (`zig fetch`) would hand a consumer zero
  working functionality today — nothing beyond compile-check stubs exists.
- The one CI failure-then-fix on the bootstrap commit has only run green once since; confirm
  robustness across the full cross-compile matrix, not just the single subsequent run.
- Single-maintainer, 2-commit repo, no external review yet — no track record beyond this
  snapshot to assess process health.
- No secrets, no oversized files, no version drift, no failing tests observed — nothing
  acutely alarming beyond the claimed-vs-actual gap above.
