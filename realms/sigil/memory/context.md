# sigil — context

last_seen_at: 2026-09-09T01:00:00Z
rejected_plans: []

## Cycle 6 — 2026-09-09 — FEATURE

- Preflight: clean tree on main, CI green (HEAD sha matched), no open bug issues, counter 5→6,
  6%5≠0 and no stabilize_streak → FEATURE. Inbox: no owner actions since watermark.
- Picked plan 001 item 5 (0.16 · main, args, allocators), next unchecked item, `blocked_by: none`.
- **Finding**: probed both toolchains' `std/process.zig` directly — `std.process.Init` (0.16)
  and `argsAlloc` (0.15.2) are mutually exclusive APIs, and `zig build` (not just `test`) already
  passed clean under 0.16.0 for every file except `main.zig`. Item 5 as scoped (full
  `main(init: std.process.Init)` rewrite) therefore cannot merge with green CI unless item 8's
  manifest/CI version bump lands in the same PR — bundled that sub-piece in (`minimum_zig_version`
  → `0.16.0`, dropped hardcoded `version: 0.15.2` from both CI jobs). See [[patterns]].
- Rewrote `src/main.zig`: args via `init.minimal.args.toSlice(init.arena.allocator())` (no manual
  `DebugAllocator` needed — `init.arena` replaces the removed GPA/argsAlloc pairing entirely),
  stdout via `std.Io.File.stdout().writer(init.io, &buf)`. Verified with a real build/run (not a
  grep) under `~/.zr/toolchains/zig/0.16.0/zig`: `zig build`, `zig build run -- version|--help`,
  `zig build test`, `zig fmt --check`. code-reviewer: 0 CRITICAL, 2 WARNING (stale CI comment
  reworded; CI-resolution mechanism left for CI itself to confirm), 3 SUGGESTION (deferred —
  already scoped to later plan items).
- PR #8 opened, CI 7/7 green (Linux build-and-test + 6 cross-compile targets, all resolved
  0.16.0 from the manifest correctly), squash-merged, `auto-merged` labelled. Tracking issue #3
  updated to 5/11, with a note that item 8's remaining scope (macOS-native-job re-verification,
  `testing.io` audit) is unchanged.
- Next: item 6 (0.16 · library sweep and lock-in) — probe already found zero hits for the banned
  0.15 API classes in the other 12 `src/*.zig` files; this item is mostly banning those classes
  in `tidy` plus requiring an `error.Canceled` prong, verified via `zig test src/root.zig` +
  `zig build tidy` on 0.16.0.
- Blockers: none. Open questions: none.

## Cycle 5 — 2026-09-09 — STABILIZATION

- Preflight: disk 60 GB free (gate cleared, unlike prior cycle's 16 GB block). Clean tree on
  main, CI last 5 runs green, no bug issues. Counter was 4 → n=5, 5%5==0 forced STABILIZATION.
- Inbox: no OWNER comments since watermark, no plan PR open, milestone issue #3 the only open
  issue. No actions needed.
- `tidy-auditor` swept `src/`, `tools/`, `bench/`, `build.zig`: 9 real `zig build tidy`
  findings (8 line-length, 1 missing `//!` header) — exactly plan 001 item 4's known scope.
  Fixed via PR #7 (rewrapped 8 headers, added `src/main.zig`'s header, flipped `test_step` to
  hard-depend on the tidy scan). Verified the gate works: a planted violation fails
  `zig build test`; reverting it goes green. CI 7/7, squash-merged, `auto-merged` labelled.
  Tracking issue #3 updated to 4/11.
- Remaining audit findings (not fixed this cycle, recorded in `STATE.md`): `tools/tidy.zig`
  self-exempt from file-length/doc-header checks; mutual recursion in its dir-walk with no
  depth bound; `tidy_baseline.txt` at repo root outside `DOCS.md`'s allowed list; 2
  `catch unreachable` missing `// proof:` comments (provably safe via a preceding assert).
- Next: item 5 (0.16 · main, args, allocators) is next in plan 001 — trivial per the probe
  (single `GeneralPurposeAllocator` → `DebugAllocator` rename plus `process.Init` main shape).
- Blockers: none. Open questions: none.

## Blocked attempt (disk, not counted) — 2026-09-08

- Preflight disk gate failed: `df -g /` reported 16 GB available on `/` (`/dev/disk3s1s1`,
  228Gi total, 17Gi used, 51% capacity), below the 20 GB minimum required by CYCLE.md step
  0.2. This is a machine-wide constraint, not sigil-specific — no cleanup attempted (not
  authorized to free disk space unattended).
- Stopped before inbox triage / mode selection; no GitHub or repo state read this cycle.
- Next: retry next scheduled cycle; if disk is still < 20 GB after repeated cycles, this may
  need a human to clear space or the cron server to be told to prune other realms' checkouts.
- Blockers: host disk space.
- Open questions: none.

## History

Cycle 0 (2026-09-05, RESTRUCTURE): realm created by the citadel restructure; memory
migrated from the repo's former `.claude/memory/`. Survey found a pure scaffold (285 LOC,
all stub modules, 2 commits). Zig 0.16 probe found sigil nearly migration-ready — 1 trivial
error (`main.zig`'s `GeneralPurposeAllocator` rename), library surface already compiles
clean on 0.16. Full detail in `REALM.md`/`STATE.md`. Plan 001 PR opened, awaiting merge.

Cycle 1 (2026-09-05, FEATURE): plan 001 PR #2 still open awaiting human merge, zero review
comments; no milestone issue existed yet so no implementation work was possible. No action
taken beyond a status comment on the PR.

Cycle 2 (2026-09-06, FEATURE): plan 001 (PR #2) had merged since last cycle — opened tracking
issue #3 (11-item checklist). Implemented + merged item 1 (Hygiene leftovers) via PR #4, CI
green (7/7).

Cycle 3 (2026-09-06, FEATURE): implemented + merged item 2 (Branch decision — no `wip/*`
exists for sigil) via PR #5, CI green (7/7). Tracking issue updated to 2/11. (Its `/report`
did not persist `memory/counter`; corrected in cycle 4.)

Cycle 4 (2026-09-07, FEATURE): item 3 (`tidy` step in `build.zig`) via PR #6 — vendored
`citadel/templates/tidy/tidy.zig`, added a sigil-only `wire_usize` ban rule, wired its 23 unit
tests into `zig build test`; standalone `zig build tidy` found 9 real findings, deferred to
item 4. CI green (7/7), squash-merged. Tracking issue 3/11.

## Standing backlog (carried over from repo's former `project-context.md`)

Plan 001 (Zig 0.16 migration + Tiger Style baseline) is now the active milestone, tracked in
issue #3. In milestone order for the *next* plan (002, Phase 1 — unchanged since bootstrap):

- **1A** — `core/{value,tree,diagnostics}.zig`: `Value` union, arena-owned `ValueTree`,
  `Diagnostics{line,col,message}`. Tests: arena release, equality, Map insertion-order
  preservation.
- **1B** — `core/number.zig`: i64/u64/f64 boundary handling, `-0`, exponents, explicit
  overflow errors.
- **1C** — `core/unicode.zig`: UTF-8/escape utilities.
- **1D** — `reflect/{parse,stringify,options}.zig`: comptime struct<->Value mapping;
  field rename/defaults/deny-unknown-fields options.
- **2A-2C** (after Phase 1) — `json/{scanner,dom,writer}.zig`: RFC 8259 pull scanner,
  DOM builder, pretty/minify writer.
- Housekeeping: populate the empty performance-targets table in `docs/plans/` and
  `docs/PRD.md` §5 once any module is benchmarkable.

## Next priority

Finish plan 001 (issue #3, 5/11), one checklist item per cycle, before starting Phase 1A.
Item 6 (0.16 · library sweep and lock-in) is next, no `blocked_by`: the probe already found
zero hits for the banned 0.15 API classes (`fs`, `net`, `time`, `Thread` sync, `ArrayList{}`,
`indexOf`) in the 12 non-`main.zig` `src/*.zig` files — this item bans those classes in `tidy`
in 0.16 spelling and requires an `error.Canceled` prong in exhaustive I/O-error switches.
Verify: `zig test src/root.zig` + `zig build tidy` on the 0.16.0 toolchain, both green. Note:
`build.zig.zon`'s `minimum_zig_version` is now `"0.16.0"` and CI resolves it from the manifest
(landed early, cycle 6) — local dev commands in this file assume the 0.16.0 toolchain going
forward; the global `zig` alias on this machine is still 0.15.2 per `zig-0.16.md`.
