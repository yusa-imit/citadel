# synod — context

last_seen_at: 2026-09-12T06:06:59Z
rejected_plans: []

## Cycle 10 — 2026-09-12 — STABILIZATION
- **Bookkeeping bug found and fixed**: cycle 9's `/report` updated this file but never wrote
  `memory/counter` (stayed at 8 despite cycle 9 fully completing — PR #12 merged, item 9 ticked).
  True completed-cycle count was 9, making this session cycle 10 (not 9 as the stale counter
  implied), which lands on the every-5th-cycle STABILIZATION cadence. Corrected `counter` to 10
  so the cadence self-heals; if a future cycle's mode looks off, check for another skipped write.
- Inbox: no new owner actions since watermark — the only new items were the AI's own cycle-9
  report comments on issue #3, not new OWNER instructions. No plan PR, no bug issues, no red CI
  (the last push-CI run's older SHA is expected: PR #12 was docs-only and matched CI's
  `paths-ignore`, so no push-triggered run was expected for that merge).
- tidy-auditor full pass (see `STATE.md` "Superseded 2026-09-12" table): fixed one class,
  smallest-diff-first — two `assert(a or b)` implication-style asserts rewritten to
  `if (!a) assert(b);` in `bench/main.zig:48` and `tools/tidy.zig:605`, via PR #13 (merged, CI
  green). Deferred: `build.zig`'s `pub fn build` now 87 lines (limit 70) and `tools/tidy.zig` now
  1266 lines (limit 800), both still unenforced because `tidy.zig`'s `main()` only walks `src/`;
  full recommended fix order recorded in `STATE.md` (split tidy's inline tests out first, extract
  build.zig helpers, only then widen tidy's scope — all in one PR so CI never goes red mid-fix).
- Docs hygiene: `REALM.md`/`STATE.md` both claimed "no CHANGELOG.md yet" — stale, it has existed
  since PR #4 (cycle 1); corrected in both files. Left README's `zig-0.15.x` badge alone even
  though it's stale (repo's been on 0.16.0 since PR #7) — it's already scoped as milestone item
  10, not a stray stabilization fix.
- Next: FEATURE cycle 11 → item 10 (README/PRD/CHANGELOG reconciliation), then item 11 (release
  v0.2.0).
- Open questions: none.

## Cycle 9 — 2026-09-12 — FEATURE
- Inbox: no new owner actions since watermark; no plan PR open; no bug/red-CI; milestone #3
  unchanged apart from ticking item 9 this cycle.
- Implemented item 9 (Assertion baseline) via PR #12 (merged, CI green all 7 jobs): docs-only —
  `docs/adr/0003-assertion-baseline.md` records the Tiger Style two-assertions-per-function
  contract. `src/main.zig`/`bench/main.zig` already met it from prior cycles' review passes
  (`grep -c assert` = 3, 6), so no code changed; `types`/`interfaces`/`log`/`store` get the same
  contract applied once real logic lands, with `log.validate()` required at the end of every
  log-mutating test. Declined a new mechanical tidy check — nothing to measure on stub modules.
  code-reviewer caught 2 warnings pre-merge (wrong line-count claim "34" vs actual 38 lines;
  `interfaces.zig` missing from the module list vs `REALM.md`'s actual build order
  `types → interfaces + log → store`), both fixed before opening the PR. Ticked item 9 in the
  plan doc and issue #3.
- Next: item 10 (README/PRD/CHANGELOG reconciliation), then item 11 (release v0.2.0).
- Open questions: none.

## Cycle 8 — 2026-09-11 — FEATURE
- Inbox: no new owner actions since watermark; no plan PR open; found and fixed a tracking-drift
  bug — item 6 was ticked in the plan doc via #10 last cycle but the GitHub issue #3 checklist
  itself was never updated to match; reconciled with a housekeeping comment before continuing.
- Implemented item 8 (`io: Io` at the boundary only) via PR #11 (merged, CI green all 7 jobs):
  `docs/adr/0002-io-at-the-boundary.md` records the rule (`io: Io` first param after receiver on
  `driver`/`adapters`/CLI/bench; `raft`/`membership`/`detector`/`clock`/`log` never reference
  `std.Io`, keep injected `Clock`/`Rng` vtables); `tools/tidy.zig` gained `core_purity_files` +
  `isCorePurityFile()` wired into `checkFile()` so `zig build tidy` mechanically fails on any
  `std.Io` hit in those five files. TDD throughout; code-reviewer caught 2 warnings (stale
  RED-phase doc comment, missing CHANGELOG/plan-checklist entries), both fixed before merge.
  Ticked item 8 in the plan doc and issue #3.
- Next: item 9, the assertion baseline (`src/main.zig` arg handling, `bench/main.zig` ops math,
  ADR-003), then item 10 (README/PRD/CHANGELOG reconciliation) and item 11 (release v0.2.0).
- Open questions: none.

## Cycle 7 — 2026-09-11 — FEATURE
- Inbox: no new owner actions since watermark; no plan PR open; milestone #3 unchanged apart
  from ticking item 6 this cycle.
- Implemented item 6 (0.16 — library-core sweep) via PR #10 (merged, CI green all 7 jobs): a
  confirmation task, not a code change — grepped `src/` for every `zig-0.16.md` steps (2)-(5)
  pattern (bare `= .{}`, `indexOf*`/`lastIndexOf*`, `fs.cwd`/`std.fs.`, `std.net`, `Thread.*`,
  `std.once`/`@Type(`, `else => unreachable`, `std.time`) and found zero hits, matching the
  original migration probe's finding that `src/` is still 12 stub modules with no I/O. Evidence
  recorded in the plan doc and CHANGELOG. `zig test src/root.zig` 12/12 green, `zig build test`
  and `zig fmt --check` both clean.
- Process note: CI took ~3 min longer than usual to register a run against the new PR branch
  (no `workflow_runs` entry at all for ~2-3 min after push+PR-create, before the run appeared as
  `in_progress`) — not a repo problem, just budget more CI-registration slack than prior cycles
  when watching checks.
- Next: item 8, `io: Io` at the boundary only (item 7 is already ticked — `minimum_zig_version`
  and CI landed in cycle 4's PR #7). After that: item 9, assertion baseline.
- Open questions: none.

## History (cycles 0-6)
- Cycle 0 (2026-09-05, RESTRUCTURE): realm created by citadel restructure; memory migrated from
  the repo's old `.claude/memory/`; plan 001 (Zig 0.16 migration + Tiger Style baseline)
  prescribed by ROADMAP.
- Cycle 1 (2026-09-06, FEATURE): plan 001 merged as #2; opened milestone tracking issue #3
  (11-item checklist). Implemented item 1 (hygiene leftovers) via PR #4.
- Cycle 2 (2026-09-06, FEATURE): item 2 (`tidy` step part 1, sizes) via PR #5.
- Cycle 3 (2026-09-07, FEATURE): item 3 (`tidy` step part 2, ban list) via PR #6; a
  code-reviewer pass caught `tools/tidy.zig`'s own tests weren't wired into `zig build test`
  and a real off-by-one bug it then surfaced — both fixed.
- Cycle 4 attempt (2026-09-08, PREFLIGHT ABORT): disk gate failed (16 GB < 20 GB required);
  in-progress item-4 work committed to `wip/fix-0.16-main-entry-20260908` before stopping.
- Cycle 4 (2026-09-08, FEATURE): reviewed and cherry-picked the preserved wip branch; merged #7
  (0.16 migration of `src/main.zig` and `tools/tidy.zig`, `minimum_zig_version` bump). Ticked
  items 4 and 7.
- Cycle 5 (2026-09-09, STABILIZATION, every-5th-cycle cadence): tidy-auditor found one real fix
  (compound assert → `if (a) assert(b);` idiom), merged as #8. Confirmed `zig build bench` still
  broken under 0.16 (became cycle 6's item). stabilize_streak stayed 0.
- Cycle 6 (2026-09-10, FEATURE): item 5 (0.16 — `bench/main.zig`) via PR #9: `Io.Clock`-based
  timing, `init.gpa`, `matchesFilter` replacing `std.mem.indexOf`; also closed a real CI gap
  (bench executable was never built by CI). Forgot the `Co-Authored-By` trailer on PR #9's
  commit — a force-push to fix it is blocked by the guard hook, so it was left as-is; include
  the trailer in the *first* commit next time.
- Standing backlog (from the old `.claude/memory/project-context.md`): after item 6 (library-core
  sweep), Phase 1 real work starts at `src/types.zig` (NodeId/Term/Index/Entry/HardState/
  Snapshot/Message/ConfChange), then `src/log.zig` (append/truncate/termAt/conflict search),
  then `src/interfaces.zig` + `src/store.zig` (vtables + in-memory LogStore), then Phase 2's
  `raft/node.zig` election state machine.

Full per-cycle detail for cycles 0-5 (PR numbers, code-reviewer findings, the disk-gate abort)
lived here before this fold; see git history of this file if needed.
