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

Re-audited 2026-09-09 (cycle 5, stabilization) via `tidy-auditor` + a live `zig build test`
run on the 0.16.0 toolchain (`tools/tidy.zig`, landed by plan 001 items 2–3, now enforces this
mechanically on every `zig build test`).

| Metric | Count | Note |
|---|---|---|
| `assert(` | 0 in `src/`; 59 in `tools/tidy.zig` (the lint tool itself) | `src/` stubs still have no logic to assert over |
| `catch unreachable` w/o proof | 0 | — |
| `@panic(` in library code | 0 | — |
| `std.debug.print` in library code | 0 | — |
| unbounded `while (true)` | 0 | — |
| files > 800 lines | 1 | `tools/tidy.zig` — 1452 lines (no file-length rule exists yet to catch this) |
| functions > 70 lines | 0 | — |
| `usize` in wire-format structs | 0 | no format structs exist yet (codec/page/wal/snapshot still stubs) |
| `zig build tidy` | 0 findings | run against live tree 2026-09-09 |

`tools/tidy.zig` does not lint itself (`scan_roots = .{ "src", "bench", "tests" }` excludes
`tools/`) — a self-hosting gap flagged for a future stabilization cycle, alongside adding the
missing 800-line file-length rule. Confirmed via a local (reverted) experiment: extending
`scan_roots` to include `tools/` currently crashes on a stale `assert(scan_roots.len == 3)` in
`collectFiles` — that assert itself needs updating first if this is picked up.
CLAUDE.md-era domain rules (checksum every disk byte, fsync as policy, idempotent recovery,
magic+version formats, no `@panic`/`catch unreachable`, page-size matrix 512B–64KB) are now in
`REALM.md`; **re-audit this table once real Phase 1 code lands.**

## Zig 0.16 probe summary (historical — migration landed 2026-09-08 via PR #7)

`build.zig.zon` `.minimum_zig_version` is `"0.16.0"`; `zig build`/`zig build test` both pass
clean on the 0.16.0 toolchain as of cycle 4. The probe below is kept for history.

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
- `docs/PRD.md` and `docs/plans/` are correctly placed and should stay as-is.
- README/CHANGELOG reconciled with post-0.16 reality 2026-09-09 (PR #8, plan 001 item ticked):
  Zig badge `0.15.x` → `0.16.x`; module table now labels all ten modules `Planned` (none
  landed); install snippet repointed at the not-yet-released `v0.2.0` (the old `v0.1.0`
  snippet pointed at a tag that never existed — no tags exist yet).

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
