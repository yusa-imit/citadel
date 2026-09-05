# strata — Realm

| | |
|---|---|
| Layer | foundation |
| Path | `/Users/fn/codespace/strata` |
| GitHub | `yusa-imit/strata` |
| Version | 0.1.0 (`build.zig.zon`) · latest tag none (unreleased) |
| Zig | 0.15.2 — migrating to 0.16.0 under plan `001` (probe: 1 error, trivial, <1h) |
| Depends on | none — Zig std only (ADR-001) |
| Consumers | silica, zoltraak, synod (planned/adapter; per `citadel/docs/KINGDOM.md`) |
| blocked_by | — |
| CI | Linux tests + 6 cross-compile targets (`.github/workflows/ci.yml`) |

## What it is

strata is the kingdom's foundation storage-kernel library: platform file I/O with
caller-chosen fsync policy, a checksummed page layer under a CLOCK buffer pool, a segmented
write-ahead log with group commit and crash recovery, page-based B+Tree and LSM index
structures, an embedded KV engine (Db/WriteBatch/Snapshot), and a streaming snapshot format.
It is the general-purpose extraction of silica's storage layer; zoltraak's AOF/RDB, and
synod's LogStore are meant to sit on top of it as opt-in adapters. As of this survey
(2026-09-05) the repo is a freshly bootstrapped scaffold: every module (`codec`, `file`,
`page`, `cache`, `wal`, `btree`, `lsm`, `kv`, `snapshot`, `testing`) is a ~20-line stub —
a doc comment, an `Error = error{NotImplemented}` set, and one compile-check test. None of
the design in `docs/PRD.md` is implemented yet; `docs/milestones.md` Phase 1 has not started.

## Build and test

```bash
zig build              # library + CLI — a few seconds
zig build test         # unit tests (~5s; 11 compile-check / refAllDecls stubs today)
zig fmt --check src build.zig
```

Local-only: `zig build`, `zig build test`. CI-only: cross-compile, benchmarks, fuzz.
No servers, no ports, no background processes — strata is a pure library plus a tiny CLI
(`strata version` / `--help`). Tests use `std.testing.tmpDir`; nothing to kill between runs.
Once Phase 1 lands, expect longer runs from page-size matrix tests (512B–64KB) and WAL/
crash-injection suites — budget accordingly, this repo has no long-suite history yet.

## Realm-specific rules

- `docs/milestones.md` is the single source of truth for progress; `docs/PRD.md` is the
  single source of truth for requirements. Update milestone checkboxes as each item lands.
- Every disk-written byte must be checksummed — pages, WAL frames, SSTable blocks, snapshot
  chunks. No exceptions.
- fsync is a caller-chosen policy (`SyncPolicy`) — the library never silently skips it.
- Recovery must be idempotent: replaying the same WAL twice yields the same result.
- Every file format needs magic + version; a format change requires a version bump and
  migration notes.
- Borrowed values: `get()`-style accessors return a slice valid only until the next write —
  document the lifetime per function.
- Corruption is always a typed error (`error.Corrupted`, `error.ChecksumMismatch`,
  `error.TornWrite`), never `@panic` — this is stricter than the generic assert/return line,
  it names the exact error set callers must switch on.
- Must work correctly across page sizes 512B–64KB — requires matrix tests, not a single size.
- Platform-specific branching (`builtin.os.tag`) is confined to `file/` only, never in upper
  layers (page/cache/wal/btree/lsm/kv/snapshot).
- No `wip/*` branch was preserved this session — the tree was clean (foundation repos had no
  in-flight work at survey time).

## Layout

| Path | Lines | State |
|---|---|---|
| `src/root.zig` | 25 | library root, re-exports the 10 modules below |
| `src/main.zig` | 36 | CLI: `strata version` / `--help` |
| `src/codec.zig` (+ `codec/`) | 21 | stub — planned: varint/fixed/crc32c/xxhash |
| `src/file.zig` (+ `file/`) | 20 | stub — planned: file I/O, sync policies, mmap, locks |
| `src/page.zig` (+ `page/`) | 20 | stub — planned: page header/manager/freelist |
| `src/cache.zig` (+ `cache/`) | 19 | stub — planned: CLOCK buffer pool, pin/unpin guards |
| `src/wal.zig` (+ `wal/`) | 23 | stub — planned: segmented WAL, group commit, recovery |
| `src/btree.zig` (+ `btree/`) | 21 | stub — planned: B+Tree, cursors, overflow pages |
| `src/lsm.zig` (+ `lsm/`) | 21 | stub — planned: memtable/SSTable/compaction |
| `src/kv.zig` (+ `kv/`) | 21 | stub — planned: Db/WriteBatch/Snapshot |
| `src/snapshot.zig` (+ `snapshot/`) | 19 | stub — planned: streaming snapshot writer/reader |
| `src/testing.zig` (+ `testing/`) | 19 | stub — planned: crash-injection harness, diff model |
| `bench/main.zig` | — | benchmark harness placeholder |
| `examples/`, `tests/` | — | `.gitkeep` only, no content yet |

Total `src/` LOC: 265. Every nested subdirectory referenced above is currently empty.

## Known gaps (from STATE.md)

- All Tiger Style grep metrics read 0 (asserts, `catch unreachable`, `@panic`,
  `std.debug.print`, unbounded `while (true)`, files >800 lines) — not because the repo is
  clean, but because no real logic exists yet to violate anything. Re-check once Phase 1 lands.
- Scope/claim gap: README and the old CLAUDE.md advertised a fully-designed 10-module storage
  kernel; 0% of that logic is implemented today — stub files only.
- One CI run failed on the bootstrap commit itself, fixed one commit later; the fix has only
  ever been exercised on that single subsequent run.
- Single-maintainer, 2-commit repo, no open issues/PRs, no external review yet.
- Zig 0.16.0 probe: 1 error class (`GeneralPurposeAllocator` → `DebugAllocator` rename, plus
  latent `argsAlloc`/`argsFree` removal), confined to `src/main.zig`; the entire library
  (root.zig + all 10 stub modules) already compiles and passes on 0.16.0 unmodified.
