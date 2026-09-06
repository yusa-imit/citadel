# zoltraak — context

last_seen_at: 2026-09-06T00:00:00Z
rejected_plans: []

## Cycle 1 — 2026-09-06 — FEATURE
- Done: opened milestone tracking issue #121 for plan 001 (12 items, checklist mirrors
  `docs/plans/001-zig-0.16-and-tiger-baseline.md`). Picked item 1 ("Clear the decks") and
  split it into two independent PRs since it bundled an unrelated code change with pure
  hygiene: #122 (untrack `src/.DS_Store`, drop stale `.gitignore` entries `check_existing`/
  `main`/`verify_*`/`/test_*`, add `CHANGELOG.md`) — CI green, **merged**. #123 (real
  `MIGRATE` via TCP DUMP/RESTORE, rebased `wip/migrate-real-dump-restore` cleanly onto
  main) — CI still running at the cycle deadline, commented "awaiting CI; merge next
  cycle" per protocol.
- Discovery (important, not yet acted on): 3 pre-existing local `git stash` entries
  predate this session, untriaged, still safely in `git stash list` (not applied, not
  lost) — a `git stash`/`pop` I ran to test `zig fmt` baseline against main accidentally
  tried to apply stash@{0} and hit merge conflicts (`build.zig`, `src/storage/memory.zig`);
  resolved by `git checkout HEAD --` on the conflicted files and deleting the
  stash-introduced untracked file — the stash entry itself was preserved throughout
  (`git stash pop` never drops on conflict). Contents, most promising first:
  - `stash@{0}` (4f38643, "WIP on main: f3ef58a chore(sailor)... Iteration 438"): a DUMP/
    RESTORE type-byte mismatch fix for **stream + hyperloglog**, touching `build.zig` +
    `src/storage/memory.zig` — plausibly the actual root cause of the two documented
    signal-4 crashes (`test_iter432` streams, `test_iter437` time series RDB round-trip).
    Worth trying first on a fresh branch with the two crash tests as the acceptance check.
  - `stash@{1}` (a73d2a4, "WIP on main: 78ba691 fix(sort)..."): RDB persistence for
    Time Series + Vector Set real serialization (`persistence.zig` +88, `timeseries.zig`
    +195, `vector.zig` +109) — also RDB-round-trip-shaped, may overlap or conflict with
    stash@{0}; check ordering/overlap before applying both.
  - `stash@{2}` (41a2e07, "WIP on main: 823d615 feat(sentinel)..."): `BF.LOADCHUNK` bloom
    filter refactor in `src/commands/bloom.zig` (+`src/storage/memory.zig` +11) — smallest,
    independent of the other two.
  - None of the three have been build/test-verified against current `main` yet — treat as
    unverified WIP, not "ready to merge" like `wip/migrate-real-dump-restore` was.
- Next: merge #123 once CI is green (next cycle's inbox step 8). Then continue plan 001
  item 2 (`tidy` build step). Separately, triage the 3 stashes above as their own
  bounded task(s) — `stash@{0}` looks highest-value (directly targets a documented,
  unresolved bug).
- Blockers: none. Open questions: none.

## History (cycles before 1)
- Realm created by citadel restructure. Memory migrated from the repo's former
  `.claude/memory/` (only `session_135_findings.md` existed there) and from the repo's
  former `CLAUDE.md`. First plan `001` prescribed by `citadel/docs/ROADMAP.md` (Zig 0.16
  migration, per `blocked_by: zuda v3.0.0, sailor v3.0.0` in REALM.md).
- A complete, tested, uncommitted change (`src/commands/cluster.zig`, real MIGRATE via
  DUMP/RESTORE) was found in the working tree and preserved on branch
  `wip/migrate-real-dump-restore` rather than discarded or committed to `main` directly.
- Next: open plan 001 PR (if not open) → await human merge. Separately, a repo-hygiene
  PR is owed (see STATE.md "Docs / root hygiene") and the preserved wip branch should
  become its own PR once picked up.
- Open questions: none.

## Standing backlog (carried from the repo's former CLAUDE.md / project memory)

Ordered by what the repo's own docs called out as most concrete/highest-impact first:

1. Open `wip/migrate-real-dump-restore` as a PR — it's finished, not a fragment.
2. Hygiene: untrack `.DS_Store`/`test_cms_sig`/`.iteration`, gitignore `zig-pkg/`,
   prune/relocate the ~30+ loose iteration/spec/summary `.md` files under the former
   `.claude/` and `docs/iterations/` (superseded by `docs/milestones.md`).
3. Root-cause the two RDB round-trip test crashes (`test_iter437` time-series,
   `test_iter432` streams — signal 4 / illegal instruction on deserialize). Documented
   as unresolved in the repo's own `docs/milestones.md` Iteration 452 notes.
4. Reconcile the 3-way version divergence (`build.zig.zon` 0.2.0, old CLAUDE.md claim
   0.2.13, actual latest tag v0.2.14) against `citadel/protocol/VERSIONING.md`.
5. Sorted Set → `zuda.compat.zoltraak_sortedset` migration (status: READY, ~1800 LOC of
   local skip-list code removable). HyperLogLog and Geohash are permanently BLOCKED on
   real zuda API mismatches — do not retry those without a zuda-side change.
6. Wire `src/storage/blocking.zig` (already written, 431 lines, unused) into
   `server.zig`'s event loop for true `BLOCK`-family semantics — est. 3-4 iterations,
   plus a 5-6 iteration event-loop refactor prerequisite. This is the single largest
   architectural gap between "claimed" and "actual" in the whole project.
7. Reduce 105 `std.debug.print` calls in `src/`; begin splitting `storage/memory.zig`
   (15,650 lines) and `commands/strings.zig` (7,869 lines) — 44 of ~90 files exceed 800
   lines total.
8. Zig 0.16 migration itself (plan 001) — blocked on sailor and zuda shipping
   0.16-compatible `build.zig` first; see STATE.md for the full probe breakdown.

## Next priority (as of the last durable audit, Session 135, superseded on items 1-3)

Session 135's own top-3 recommendations (Lua engine, ACL enforcement, full client
commands) are now DONE per current `docs/milestones.md` — CLAUDE.md claims all three
phases 100% complete. The two architecture notes from that audit that are **still**
accurate today: blocking semantics remain polling-based (item 6 above), and the
Geohash zuda migration remains permanently blocked by API shape (item 5 above). No
other content from that session survives as current-state fact.
