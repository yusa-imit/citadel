# synod — context

last_seen_at: 2026-09-16T00:00:00Z
rejected_plans: []

## Cycle 12 — 2026-09-16 — FEATURE
- Inbox: no new owner actions since watermark (only the AI's own cycle-11 report comments on
  issue #3). No plan PR, no bug issues, no red CI (last completed CI run's headSha didn't match
  origin/main because PR #14 was docs-only and CI has a paths-ignore for docs — not a failure).
- Item 11 (release v0.2.0), the last item in milestone 001: PR #15 (build.zig.zon bump,
  CHANGELOG `[Unreleased]` → `[0.2.0]`, plan checklist ticked), merged, all 7 CI jobs green.
  Tagged `v0.2.0`, pushed, `gh release create` published with the changelog section as notes.
  No real consumers pin synod yet (grepped all 8 sibling `build.zig.zon` files — zero hits), so
  no migration issues opened. Closed milestone issue #3 with the release link. Recorded the
  release in `STATE.md` under a new "Releases" section.
- ~17 min remained before the 22-min deadline, so opened plan 002 (PR #16,
  `docs/plans/002-phase1-types-log-store.md`): Phase 1 real logic — types, interfaces, log,
  in-memory store, per REALM.md's module build order — released as v0.3.0. Drafted via the
  `planner` agent (opus), which also caught a live bug worth flagging: `src/root.zig:11`
  hardcodes `SemanticVersion{0,1,0}`, so the just-released v0.2.0 binary still reports `synod
  0.1.0` (the version isn't derived from `build.zig.zon`); made it plan 002's first item since
  it's a real defect, not scope creep, and fixing the manifest-drift risk now (before Phase 1
  adds real wire types) is cheap. Plan also splits PRD 1A/1B into two items each (types-scalars
  vs Message-union; log-append vs conflict-search+validate) to fit the 22-min cycle cap, and
  flags two Tiger Style size violations (`tools/tidy.zig` 1266 lines, `build.zig`'s `build()` 87
  lines) that have escaped detection since cycle 5 because tidy's own walk only covers `src/`.
- Next: awaiting OWNER merge of plan 002 (PR #16). Once merged, cycle 13 opens the milestone
  issue and starts item 1 (the version-drift bug fix).
- Open questions: none.
- Budget note: this cycle's planner-agent delegation (opus, full PRD+ADR+REALM.md context
  bundled into the prompt) consumed most of the session's USD budget in one call — future
  cycles should keep planner prompts tighter (point at files to read rather than pasting large
  excerpts) if budget pressure recurs.

## Cycle 11 — 2026-09-15 — FEATURE
- Inbox: no new owner actions since watermark — the only new item since cycle 10 was the AI's
  own cycle-10 report comment on issue #3, not a new OWNER instruction. No plan PR, no bug
  issues, no red CI.
- Implemented item 10 (README/PRD/CHANGELOG reconciliation) via PR #14 (merged, CI green all 7
  jobs), docs-only: Zig badge `0.15.x` → `0.16.0`; module table gained a `Status` column, every
  row marked `planned`; Status section and intro paragraph now say plainly this is a scaffold;
  install snippet points at the not-yet-tagged `v0.2.0` instead of the never-published `v0.1.0`.
  `docs/PRD.md` needed no change — it already reads as a forward-looking design doc, not a
  claim of current implementation. `CHANGELOG.md` already existed since PR #4; added this PR's
  own entry under `[Unreleased]` rather than a premature `0.2.0` section (`VERSIONING.md`
  requires the versioned section and the `build.zig.zon` bump to land together in the release
  PR, i.e. item 11, not before). code-reviewer caught 2 line-length WARNINGs (my own edit grew
  an already-overlong Korean intro line further, plus a new 101-char plan-doc line); both fixed
  before merge — remaining pre-existing overages (badge URL, module table rows) left as
  out-of-scope debt per the reviewer's own note. Ticked item 10 in the plan doc and issue #3.
- Next: item 11, release v0.2.0 (MINOR bump, gate: `zig build test` 0 failures, all 6
  cross-compile targets green, 0 open `bug` issues) — the last item in milestone #3. Once that
  merges/tags, milestone #3 closes and cycle 12 opens plan 002 (Phase 1 real logic:
  `src/types.zig` first, per the standing backlog below).
- Open questions: none.

## Cycle 10 — 2026-09-12 — STABILIZATION
- **Bookkeeping bug found and fixed**: cycle 9's `/report` updated this file but never wrote
  `memory/counter` (stayed at 8 despite cycle 9 fully completing). Corrected `counter` to 10 so
  the every-5th-cycle cadence self-heals; if a future cycle's mode looks off, check for another
  skipped counter write.
- tidy-auditor full pass (see `STATE.md` "Superseded 2026-09-12" table): fixed one class — two
  `assert(a or b)` implication-style asserts rewritten to `if (!a) assert(b);` in
  `bench/main.zig:48` and `tools/tidy.zig:605`, via PR #13 (merged, CI green). Deferred:
  `build.zig`'s `pub fn build` (87 lines, limit 70) and `tools/tidy.zig` (1266 lines, limit
  800), both unenforced because `tidy.zig`'s `main()` only walks `src/`; recommended fix order
  recorded in `STATE.md` (split tidy's inline tests out first, extract build.zig helpers, only
  then widen tidy's scope — all in one PR so CI never goes red mid-fix).
- Docs hygiene: `REALM.md`/`STATE.md` both claimed "no CHANGELOG.md yet" — stale (it has existed
  since PR #4); corrected in both files.

## History (cycles 0-9)
- Cycle 0 (2026-09-05, RESTRUCTURE): realm created by citadel restructure; plan 001 (Zig 0.16
  migration + Tiger Style baseline) prescribed by ROADMAP.
- Cycle 1 (2026-09-06, FEATURE): plan 001 merged as #2; opened milestone tracking issue #3
  (11-item checklist). Item 1 (hygiene leftovers) via PR #4.
- Cycle 2 (2026-09-06, FEATURE): item 2 (`tidy` step part 1, sizes) via PR #5.
- Cycle 3 (2026-09-07, FEATURE): item 3 (`tidy` step part 2, ban list) via PR #6; code-reviewer
  caught `tools/tidy.zig`'s own tests weren't wired into `zig build test` and a real off-by-one
  bug it then surfaced — both fixed.
- Cycle 4 attempt (2026-09-08, PREFLIGHT ABORT): disk gate failed (16 GB < 20 GB); in-progress
  item-4 work committed to `wip/fix-0.16-main-entry-20260908` before stopping.
- Cycle 4 (2026-09-08, FEATURE): cherry-picked the preserved wip branch; merged #7 (0.16
  migration of `src/main.zig` and `tools/tidy.zig`, `minimum_zig_version` bump). Ticked items 4
  and 7.
- Cycle 5 (2026-09-09, STABILIZATION): tidy-auditor found one fix (compound assert →
  `if (a) assert(b);` idiom), merged as #8. Confirmed `zig build bench` still broken under 0.16.
- Cycle 6 (2026-09-10, FEATURE): item 5 (0.16 — `bench/main.zig`) via PR #9: `Io.Clock`-based
  timing, `init.gpa`, `matchesFilter` replacing `std.mem.indexOf`; also closed a CI gap (bench
  executable was never built by CI). Forgot the `Co-Authored-By` trailer on PR #9's commit — a
  force-push to fix it is blocked by the guard hook, so left as-is; include the trailer in the
  *first* commit going forward (done correctly again since cycle 8).
- Cycle 7 (2026-09-11, FEATURE): item 6 (0.16 — library-core sweep) via PR #10: confirmation
  task, zero hits found for every remaining 0.15-only pattern in `src/`.
- Cycle 8 (2026-09-11, FEATURE): item 8 (`io: Io` at the boundary only) via PR #11:
  `docs/adr/0002-io-at-the-boundary.md` + `tools/tidy.zig`'s `core_purity_files` check. Also
  fixed a tracking-drift bug — item 6 was ticked in the plan doc but not in issue #3's checklist.
- Cycle 9 (2026-09-12, FEATURE): item 9 (assertion baseline) via PR #12: docs-only,
  `docs/adr/0003-assertion-baseline.md`; `main.zig`/`bench/main.zig` already met the contract.
- Standing backlog (from the old `.claude/memory/project-context.md`): after milestone #3 closes
  (item 11, release v0.2.0), Phase 1 real work starts at `src/types.zig` (NodeId/Term/Index/
  Entry/HardState/Snapshot/Message/ConfChange), then `src/log.zig` (append/truncate/termAt/
  conflict search), then `src/interfaces.zig` + `src/store.zig` (vtables + in-memory LogStore),
  then Phase 2's `raft/node.zig` election state machine.

Full per-cycle detail for cycles 0-9 (PR numbers, code-reviewer findings, the disk-gate abort)
lived here before this fold; see git history of this file if needed.
