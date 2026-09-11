# synod — context

last_seen_at: 2026-09-11T00:00:00Z
rejected_plans: []

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

## Cycle 6 — 2026-09-10 — FEATURE
- Inbox: no new owner actions since watermark; no plan PR open; milestone #3 unchanged apart
  from ticking item 5 this cycle.
- Implemented item 5 (0.16 — `bench/main.zig`) via PR #9 (merged, CI green all 7 jobs):
  `pub fn main(init: std.process.Init) !void`, `init.gpa`, `Io.Clock.Timestamp.now(io, .awake)`/
  `.untilNow(io)` replacing `std.time.Timer`, `std.mem.find` replacing the removed
  `std.mem.indexOf` via a new `matchesFilter` helper (4 unit tests, wired into `zig build test`
  via a `bench_tests` step mirroring `tidy_tests`).
- Found and closed a real CI gap while doing this: the bench executable was never built by CI at
  all — not part of `zig build`'s default install step, and (per the 0.16 probe caveat in
  STATE.md) `zig build test`'s test binary never actually analyzes a `pub fn main` body, so unit
  tests alone would not have caught the `Io.Clock` migration errors. Added a "Bench (compile +
  smoke run)" CI step (`zig build bench -- __ci_no_match__`) that builds and runs the real
  executable. Also extended `zig fmt --check` to cover `bench/` (previously only `src build.zig`).
- code-reviewer pass before merge caught 3 warnings, all fixed: `@intCast` on the clock delta
  could UB in ReleaseFast if the monotonic-clock contract were ever violated (added an
  `assert` + `@max(…, 0)` clamp); `matchesFilter`/`main` were under the 2-assertions-per-function
  target (added a postcondition assert on the found index in `matchesFilter`, and
  `ops > 0 or ns_per_op == 0` in `main`); `zig fmt --check` gap noted above.
- Process note: forgot the `Co-Authored-By` trailer on the PR #9 commit before pushing; realized
  after push, but amending would require a force-push, which the kingdom guard hook blocks
  unconditionally — left as-is rather than rewrite history. Remember to include the trailer in
  the *first* commit message next time, not add it after the fact.
- Next: item 6, the 0.16 library-core sweep (expected near-no-op per the probe — `src/` has 0
  fs/net/time hits already), then `io: Io`-at-the-boundary and the assertion baseline.
- Open questions: none.

## History (cycles 0-5)
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
- Standing backlog (from the old `.claude/memory/project-context.md`): after item 6 (library-core
  sweep), Phase 1 real work starts at `src/types.zig` (NodeId/Term/Index/Entry/HardState/
  Snapshot/Message/ConfChange), then `src/log.zig` (append/truncate/termAt/conflict search),
  then `src/interfaces.zig` + `src/store.zig` (vtables + in-memory LogStore), then Phase 2's
  `raft/node.zig` election state machine.

Full per-cycle detail for cycles 0-5 (PR numbers, code-reviewer findings, the disk-gate abort)
lived here before this fold; see git history of this file if needed.
