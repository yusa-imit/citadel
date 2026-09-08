# sigil — context

last_seen_at: 2026-09-09T00:00:00Z
rejected_plans: []

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

## Cycle 4 — 2026-09-07 — FEATURE

- Preflight found a memory drift: `memory/counter` was stuck at 2 even though a "Cycle 3"
  entry was already logged (commit cd502ac) and PR #5 (item 2) was merged. The prior cycle's
  report must have failed to persist the counter write. Corrected here: this cycle is 4.
- Inbox: no new owner actions (only my own prior status comments on issue #3).
- Done: implemented plan 001 item 3 (`tidy` step in `build.zig`) — vendored the kingdom
  reference `citadel/templates/tidy/tidy.zig` into `tools/tidy.zig`, added a sigil-only
  `wire_usize` ban rule (bans `usize` on struct fields inside wire-format modules, scoped to
  avoid flagging locals/params), wired its 23 unit tests into `zig build test`, and added a
  standalone `zig build tidy` step for the real repo scan (not yet a hard `test` dependency —
  it already finds 9 real findings, deferred to item 4). code-reviewer found 2 WARNINGs
  (`wire_usize` too broad; a silent buffer-skip instead of an assertion) — both fixed and
  reverified before merge.
- PRs: #6 opened, CI green (7/7 jobs), squash-merged, branch deleted, labelled `auto-merged`.
- Tracking issue #3 checklist updated: 3/11 done.
- Next: item 4 (Make `tidy` green) — fix the 9 findings `zig build tidy` now reports (8 known
  >100-column `//!`/build.zig lines + a newly discovered missing `//!` header in
  `src/main.zig`), then flip `tidy` into a hard dependency of `test`.
- Blockers: none.
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
did not persist `memory/counter`; corrected in cycle 4 above.)

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

Finish plan 001 (issue #3), one checklist item per cycle, before starting Phase 1A. Item 4
(Make `tidy` green) is next, no `blocked_by`: fix the 9 findings `zig build tidy` reports
today — 8 lines over 100 columns (the `//!` headers of `core`, `reflect`, `json`, `path`,
`proto`, `yaml`, `config`, worst 164 cols, plus one `build.zig` doc-comment line) and a
missing `//!` header in `src/main.zig` — then change `tools/tidy.zig`'s `run_tidy` step from
a standalone `zig build tidy` into a hard dependency of `test_step` in `build.zig`'s
`addTidyStep` helper.
