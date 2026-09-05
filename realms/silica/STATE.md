# silica — State survey — 2026-09-05

## Claimed vs present

README/PRD/CHANGELOG claim a "production-grade" full SQL:2016 RDBMS,
dual-mode (embedded + client-server), MVCC with all 4 isolation levels
(incl. serializable snapshot isolation), B+Tree/hash/GiST/GIN indexes,
full-text search, JSON/JSONB, PG wire v3 (SCRAM-SHA-256/TLS/RBAC/RLS), and
WAL streaming replication with automatic failover. v1.0.1 / CHANGELOG says
"all 12 phases complete."

Honest read: most of this is genuinely present and tested — SQL engine,
B+Tree storage + buffer pool, MVCC+WAL+locking+vacuum, a real PG-wire
server, real (non-stub) primary→replica physical WAL streaming with an
end-to-end loopback test, and a just-landed MATCH_RECOGNIZE (7 phases,
session 541). Several named subsystems are "partial/known-gap," not
"complete," despite the headline: GIN index (known instability, redesign
doc pending, integration tests skipped); GiST/GIN pre-native-wiring paths
(plain B+Tree fallback); index-only-scan / bitmap-index-scan (real but
scoped — single-table, flat AND/OR, no joins); MVCC UPDATE (delete+insert,
not true version chains — transient `NoRows` for concurrent readers,
deferred to v2.0); WAL checkpoint-vs-replication-retention (mid-
implementation, uncommitted, see Dirty tree below); logical
replication/CDC (future roadmap, not implemented).

## Size

- `src/` LOC: 184,278.
- Test count estimate: 4,936 (`test_count_estimate`); local run this session
  (against the dirty WIP tree): 4,222/4,244 passed, 21 skipped, 1 FAILED.
- Files over 800 lines: 41. Two extreme outliers: `src/sql/engine.zig`
  (43,242 lines), `src/sql/executor.zig` (35,253 lines) — both are prime
  decomposition targets before further feature work compounds them.

## Build / test (local, clean-ish tree except one WIP diff)

- `zig build` (~60s): succeeds, no warnings/errors.
- `zig build test` (~50s): 4,222/4,244 passed, 21 skipped, 1 FAILED —
  `tx.wal.test.Phase 6: regression proof` at `src/tx/wal.zig:2311`
  (`expectEqual` expected 17, found 3). This failure lives entirely inside
  the uncommitted `wip/wal-checkpoint-retention-phase2` diff to `wal.zig`
  (see Dirty tree) — the committed tree on `main` should pass cleanly.

## CI

Green. Last 3 runs on `main`: "fix: WAL replication restart_lsn never
advanced past zero-init" (`da6b054`, success, 16m5s); "chore: update session
memory" (`859d587`, success, 18m0s); "feat: MATCH_RECOGNIZE RUNNING/FINAL
semantics ... (phase 7 of 7)" (`c7ae6a3`, cancelled 3m55s — superseded by a
later push, not a failure).

## Open issues / PRs

0 open issues, 0 open PRs (`gh issue list` / `gh pr list`, both empty).

## Tiger Style gap table

| Metric | Count | Note |
|---|---|---|
| `assert(` | 12 | very low for 184k LOC |
| `catch unreachable` | 212 | convention requires a justified SAFETY |
| | | comment on each; coverage not verified this survey |
| `@panic(` | 7 | worth auditing given panic-removal CHANGELOG entries |
| debug `print` calls | 16 | |
| `while (true)` | 104 | convention: only in a top-level event loop |
| files > 800 lines | 41 | 2 extreme outliers, see Size above |
| functions > 70 lines | not measured | near-certain given the 2 outliers; |
| | | flagged as a follow-up static-analysis pass |

No secrets, no tracked giant binaries. Root tracked-file set is clean (10
files, all expected: README/LICENSE/CHANGELOG/CONTRIBUTING/SECURITY,
build.zig(.zon), .gitignore, zr.toml, silica.conf.example) —
`root_files_to_remove_or_move` is empty, nothing for the hygiene PR to move.

## Zig 0.16 probe summary

- `zig build` on Zig 0.15.2 (global toolchain): OK, clean.
- `zig build` / `zig build test` on 0.16: **blocked before reaching
  silica's own build.zig** — both sailor's and zuda's `build.zig` call the
  now-removed/changed `Compile.linkLibC()`. silica's own `build.zig` (61
  lines, plain `addModule`/`addLibrary`/`addExecutable`) shows no breakage
  on inspection.
- Probed silica's own source breakage via `zig test src/main.zig` (skips
  the dependency build graph, covers most of `src/` except
  `server/*`/`cli.zig`/`tui.zig`, which `main.zig` deliberately doesn't
  import): **275 errors**, effort estimate **medium (2-5 sessions)**,
  assuming sailor/zuda are fixed or vendored first.
- Error classes (source-level, ranked by count; 275 total):
  ArrayList/ArrayListUnmanaged struct-literal init 106 (mechanical: `T{}` →
  `.empty` + thread allocator through `append`); `std.fs.cwd()` removed
  (Io-based Dir API) 77 (**most invasive class** — needs an `Io` handle
  threaded through call chains, not find/replace); `std.time` timestamp
  helpers removed/renamed 23; Dir/File signatures gained an extra `Io` arg
  16; `std.heap.GeneralPurposeAllocator` removed 11 (→ `DebugAllocator`);
  `std.io` namespace restructured 10; `std.Thread.Mutex` relocated 10;
  `Io.Dir` missing `realpathAlloc` 6; `std.fs.File` type removed/renamed 4;
  `ArrayList.writer()` removed 3; `Io.Dir` missing `makePath` 1; misc
  one-offs (`posix.close`, `meta.intToEnum`, `crypto.random`, arg-count
  mismatches) 8.
- 70% of `src/` files (43/61) touch `std.fs`/`std.net`/`std.Thread`/
  `std.time`/`std.process`/`std.posix`/`std.http`/`std.io` — expected for a
  DB engine (storage, WAL, replication, wire server, CLI/TUI, config I/O).
- **Hard blocker, separate from silica's own migration effort**: sailor
  (v2.99.0) and zuda (v2.3.0) both fail to build under 0.16 at their own
  `build.zig` `linkLibC()` call — silica cannot get past dependency
  resolution (even for the library-only build path, since
  `buffer_pool.zig`/`tx/lock.zig` import zuda directly) until those repos
  ship 0.16-compatible releases, or silica vendors/patches them locally.
  Test-run stage was never reached in either probe path.

## Docs / root hygiene (for the hygiene PR)

`docs/` has 11 legitimate files (API reference, architecture guide,
configuration, getting-started, GIN redesign, known issues, operations
guide, packaging, PRD, SQL reference, milestones) — nothing to remove.
`.claude/` is fully tracked-generic (6 agents, 8 commands, all
generic-named; plus `memory/`, `settings.json`) — the hygiene PR should
delete the whole `.claude/` and `CLAUDE.md` tree per kingdom policy
(`citadel/protocol/DOCS.md`: repos hold code + `docs/` only). Untracked
junk under `.claude/` and an orphaned `src/.claude/scratchpad.md` are
already `.gitignore`d. `zig-pkg/` (untracked, NOT yet gitignored) is a
stray build/package byproduct — delete or gitignore, don't commit.

## Dirty tree (preserved as `wip/wal-checkpoint-retention-phase2`)

Uncommitted at survey time: `.claude/memory/architecture.md` and
`src/tx/wal.zig` (+415/-35) plus untracked `zig-pkg/`. Coherent, deliberate
mid-cycle work — Phase 2 of a 3-phase architect-designed plan (session 542)
adding WAL-checkpoint retention: new `min_retained_lsn_fn`/`ctx` fields +
`setRetentionCallback` on `Wal`, `checkpoint()` split into unconditional
flush vs. conditional reclaim/truncate (skipped/retried when a callback
reports a lagging replica). **Not safe to commit as-is** — introduces the
failing test above (looks like a one-line byte-offset bug in the new
truncation-skip path). Preserved on the branch, not committed or discarded.

## Next work candidates (priority order, per prior-session backlog)

1. Fix + land the WAL retention WIP (fix Phase 6 test, then Phase 3: wire a
   real `SlotManager` via `db.wal.?.setRetentionCallback`).
2. Redesign/re-enable GIN index per `docs/GIN_INDEX_REDESIGN.md`.
3. MVCC UPDATE limitation (delete+insert → true version chains) — v2.0-scope
   B+Tree/version-chain refactor.
4. Wire `SlotManager` into `server.zig` (zero wiring there today, confirmed
   by grep) so retention callbacks connect end-to-end.
5. Continue the sailor/zuda upgrade cadence; adopt unadopted sailor features
   (SQL-editor autocomplete v1.13.0, MockTerminal testing v1.5.0, audit
   logging v1.12.0, `arg.zig` subcommand dispatch).
6. Resolve the buffer-pool-LRU zuda-migration contradiction (REALM.md) by
   reading `src/storage/buffer_pool.zig` directly.
7. Zig 0.16 migration (plan `001`) — blocked on sailor/zuda v3.0.0 first.
