# zoltraak — debugging

_(migrated and condensed from the repo's former CLAUDE.md and `.claude/memory/`)_

## Zig 0.15 API gotchas (verbatim, still active until the 0.16 migration lands)

- `ArrayListUnmanaged` mutation methods take the allocator as their **first** argument.
- `std.io.getStdOut().writer(&buf)` then `.interface.print(...)` — must flush before exit.
- `std.builtin.Type` tags are lowercase: `.int`, `.@"struct"`, etc.
- Use `b.createModule()` for exe/test build targets in `build.zig`.

## Known crash: RDB round-trip tests (signal 4)

`test_iter437` (time-series RDB save/load round-trip) and `test_iter432` (stream entries
RDB save/load round-trip) crash their test binaries with signal 4 (illegal instruction)
rather than failing an assertion. This has been true across multiple sessions and is
already documented in the repo's own `docs/milestones.md` Iteration 452 notes as "not
investigated further this iteration ... flagged for a future stability pass." Signal 4 is
often a Zig safety-check trip (index out of bounds, integer overflow) rather than a normal
logic-error assertion — worth checking specifically for a corrupted-buffer or recursion
issue during RDB deserialization of these two types before assuming it's a benign flake.
Confirmed unrelated to unrelated concurrent changes (e.g. the cluster.zig MIGRATE diff this
session) — reproduces in isolation.

## Lead: git stash may already contain a fix for the RDB round-trip crash

Cycle 1 (2026-09-06) found 3 pre-existing local `git stash` entries (not visible on any
branch, `git stash list` only) that predate the citadel restructure and were never
triaged into `wip/*` branches like `wip/migrate-real-dump-restore` was. `stash@{0}`
(hash `4f38643`, message "WIP on main: f3ef58a chore(sailor)... Iteration 438") is
titled as a DUMP/RESTORE type-byte mismatch fix for stream + hyperloglog, touching
`build.zig` and `src/storage/memory.zig` — directly plausible as the root cause of the
signal-4 crashes above, since both are RDB/DUMP serialization bugs in the same subsystem
(streams). Not yet built or tested against current `main`. See `context.md` Cycle 1 for
the other two stashes (`stash@{1}` time-series/vector RDB serialization, `stash@{2}`
`BF.LOADCHUNK` refactor) and the full recovery note (a `git stash pop` accidentally
triggered a conflict this cycle; resolved without losing any stash — do not `git stash
drop` any of the three without first extracting on a branch and testing).

## Test hang policy

If `zig build test` runs longer than 60 seconds locally, treat it as hung and kill it —
this was the repo's own explicit local-cron safety rule (heavy resource use from multiple
kingdom repos' cron jobs running concurrently was the original reason). A full local run
normally completes in well under 10 seconds (~6s observed for 1098 tests).

## Areas flagged but not yet root-caused

- 17 `catch unreachable` sites in `src/` are unaudited for cases where the "unreachable"
  assumption could actually be reached via malformed client input at a deep call path —
  worth a systematic pass, not confirmed as bugs yet.
- No systematic hot-loop/allocator audit has been done across the 141K LOC codebase; spot
  checks did not find allocation inside a tight per-iteration loop, but this was not
  exhaustive.
- `struct 'storage.config.Config' has no member named 'default'` surfaced during the Zig
  0.16 probe (47 hits) — not yet classified as a genuine 0.16 API removal vs. pre-existing
  test/source drift; needs direct source inspection before the 0.16 migration relies on it
  either way.

## Version bookkeeping bug

`build.zig.zon` said `version = "0.2.0"` while the former CLAUDE.md's Project Status header
claimed `v0.2.13`, and the actual latest git tag is `v0.2.14`. This is a 3-way mismatch, not
a 2-way one — the manifest was never bumped in step with tagged releases at some point.
Before trusting any single version string in this repo, check all three: `build.zig.zon`,
`git tag -l 'v*' --sort=-v:refname | head -1`, and whatever the current docs claim.
