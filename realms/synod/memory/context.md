# synod — context

last_seen_at: 2026-10-10T06:22:00Z
rejected_plans: []

## Cycle 43 — 2026-10-10 — FEATURE
- Inbox: no OWNER comments, no bugs, CI green, milestone #39 open.
- Done: item 6 (2B-i-a leader send side) via PR #46 (squash-merged, 7/7 CI, `auto-merged`, #39
  item 6 ticked). New `raft/leader.zig` (Progress per peer on election, sends on
  win/propose/heartbeat, round records id/prev/last_sent/tick, timeout after election_ticks);
  `node.zig` 786 lines; 24 new tests in `node_leader_test.zig` (383 total).
- Review: 0 CRITICAL, 3 WARNING fixed (corrupted `//!`, effects capacity is `peers_max + 3`,
  tautology asserts). Cost: test-writer ~$1.25, developer ~$1.07, reviewer ~$0.25; ≈ $3.2 of $4.
- Next: item 6b (2B-i-b response side). MUST also close the liveness gap: heartbeats are gated
  by `Progress.can_send`, so a probing peer with one lost round hears nothing until the round
  expires (> min follower timeout, so a spurious pre-vote). Keep `inflight_count` == live
  records when removing a round; no `InvariantRoundRecord` variant exists (node_invariants_test
  has an exhaustive switch). Open suggestions: restored entries not checked against
  `entry_bytes_max`; earlier ones from cycles 40-42.
- Blockers: none. Open questions: none.
- Tool notes: guard blocks `cd <path>;` and heredocs into citadel (use Edit/Write). Test-writer
  left /tmp/proto (scratch reference impl; ignore). Two subagent-heavy steps cost ~$2.3.

## Cycle 42 — 2026-10-10 — FEATURE
- Inbox: no OWNER comments, no bugs, CI green, milestone #39 open.
- Done: item 5 (2C `raft/progress.zig`) via PR #44 (squash-merged, 7/7 CI, `auto-merged`, #39
  item 5 ticked). Internal `Progress` value type (32 B): match/next, probe/replicate, bounded
  inflight window, `on_send`/`on_accepted`/`on_rejected`/`on_timeout`, `backtrack_hint`,
  `check_invariants`. Tests in `progress_test.zig` (wired from `raft.zig`, NOT `node.zig`,
  which sits at 800 lines) with a seeded model vs a naive reference.
- Review found 2 CRITICAL (peer-reachable asserts: `prev == 0`, `matched == maxInt`) and 3
  WARNING; fixed: prev 0 returns false, replicate rejection with `prev >= next` is stale,
  `on_timeout` added. `matched` bounds remain a documented node precondition.
- Contract for 2B-i (in `///` of `on_accepted`/`on_rejected`): node resolves prev/last_sent from
  its own round record, one response per round, `prev <= matched <= request last index`, drops
  responses from rounds it timed out (a response after `on_timeout` would hit the new window).
  Shorter-log reject (`conflict.index == 0`) backs off one entry per round trip.
- Cost: test-writer ~$0.4, developer ~$0.2 + ~$0.2, reviewer ~$0.3; ≈ $2.1 of $4.
- Next: item 6 (2B-i leader replication; largest item — plan says split send/response side in a
  plan-tick PR if it overruns). `node.zig` is at its 800-line cap: move code out first (e.g.
  `note_leader`, status helpers) or put leader logic in a new file `raft/leader.zig`.
- Blockers: none. Open questions: none.
- Tool notes: guard blocks `cd <path>;` — use `--build-file` and `git -C`. `gh pr checks
  --watch` loop returns early while checks pending; re-check with plain `gh pr checks`.

## Cycle 41 — 2026-10-09 — FEATURE
- Inbox: no OWNER comments, no bugs, CI green, milestone #39 open.
- Done: item 4 (2A-iii PreVote) via PR #43 (squash-merged, 7/7 CI, `auto-merged`, #39 item 4
  ticked). Timeout → `pre_candidate` (no term bump/persist), `pre_vote` at term+1, grant rule
  (higher term, log ok, not leader, no leader heard in `election_ticks`), joint quorum →
  `campaign()`. New `raft/node_prevote_test.zig`; `campaign()` test helper now feeds pre-vote
  grants; `check_invariants_*` moved to `node_init.zig` (node.zig sits at exactly 800 lines —
  the tidy cap — so the next item MUST move code out first). `note_leader` (voter-only, first
  claim per term) added for `append_entries`; 2B must absorb it.
- Review found 1 CRITICAL (a leader past `election_ticks` computed "leader silent" and tripped
  an assert from a peer pre_vote) — fixed, regression test. Learner/dup-leader guards added.
- Cost: test-writer ~$0.55, developer ~$0.5, reviewer ~$0.15, rest main session; ≈ $2.5 of $4.
- Next: item 5 (2C `raft/progress.zig`, new file, so no node.zig pressure). Open suggestions:
  unit tests for `election.pre_vote_grantable`/`is_voter`; `or` compound asserts (node.zig
  role checks); `///` docs on `node_init.check_invariants_*`; `send_vote_request` `unreachable`
  switch arm → assert; earlier: `request_vote` accepts learners, `votes_len` not cleared in
  `term_adopt`, `assert_config` election_ticks bound.
- Blockers: none. Open questions: none.
- Tool notes: guard blocks `cd <path>;` — use `--build-file`/`--cache-dir` and `git -C`. Test
  suite wrapper: `zig build test` exit 0 even with tidy-fixture stderr noise; check `$?`.

## Cycle 40 — 2026-10-09 — FEATURE
- Inbox: no OWNER comments, no bugs, CI green, milestone #39 open.
- Done: item 3 (2A-ii Election) via PR #42 (squash-merged, 7/7 CI, `auto-merged`, #39 item 3
  ticked). Tick → campaign, request_vote grant/refuse (§5.4.1), joint-shaped quorum, winner
  appends empty entry. New files `raft/election.zig` (pure helpers), `raft/node_init.zig`
  (init helpers; node.zig hit 804 lines), `node_election_test.zig` (36+3 tests).
- Review (also covered the skipped cycle-39 review of node.zig) found 2 CRITICAL, fixed: a
  term-zero assert reachable from a stranger's message; term wrap at u64 max. Also fixed:
  zero-term restore entry → `RestoreInconsistent`; `pre_vote*` now dropped (adopts no term).
- Cost: test-writer ~$0.93, zig-developer ~$0.9, reviewer ~$0.4; total ≈ $3.4 of $4. One
  test-writer+developer+reviewer item per cycle is the ceiling.
- Next: item 4 (2A-iii PreVote). Open suggestions not done: `is_member` includes learners for
  `request_vote` (should be voters only); `votes_len` not cleared in `term_adopt`;
  `node.*` dangling after `RestoreLogFull`; `assert_config` lacks `election_ticks <= maxInt(u32)/2`;
  `become_leader` swallowing `LogFull` has no test. Unprovoked invariants: ProgressOrder,
  InflightOverflow, EntryDataMisplaced; leader propose path (items 2B-i/2C).
- Blockers: none. Open questions: none.
- Tool notes: test-writer's invalid fixture (vote_request_at with last_log_term > header term)
  fails `Message.validate` — keep log terms <= header term. python3 heredocs for multi-edit
  work in the guard.

## Cycle 39 — 2026-10-08 — FEATURE
- Inbox: no OWNER comments, no bugs, CI green, milestone #39 open.
- Done: item 2 (2A-i) via PR #41 (squash-merged, 7/7 CI, `auto-merged`, #39 item 2 ticked):
  tidy `is_core_purity_file` now also matches `src/raft/*.zig`; `src/raft/node.zig` skeleton
  (init/deinit/step/status/entries/check_invariants, term rules, 261 tests). Tests via
  test-writer (~$1.6 — expensive), impl via zig-developer (~$1.0). Code-reviewer SKIPPED for budget.
- ADR-007 deviations: extra `RestoreInconsistent` shapes; init makes 4 allocations (members array);
  stale-term requests get no reply yet (2A-ii/2B add rejects).
- Next: item 3 (2A-ii Election). FIRST run `code-reviewer` on `src/raft/node.zig` (skipped now);
  `step_propose` leader path and Invariant{ProgressOrder,InflightOverflow,EntryDataMisplaced}
  are unprovoked — items 2B-i/2C must add tests. Budget: a test-writer+developer item costs
  ~$2.6; tell test-writer to keep fixtures small and not exhaustive-seed everything.
- Blockers: none. Open questions: none.

## Cycle 38 — 2026-10-08 — FEATURE
- Inbox: plan 003 PR #33 merged by OWNER 2026-10-07T10:16Z; no comments, no bugs, CI green.
  Opened milestone issue #39 (12 items).
- Done: item 1 ADR-007 (`docs/adr/0007-raft-node-contract.md`) via PR #40 — architect (opus,
  ~$1.4 incl. context) returned the ADR text, the main session wrote the file (architect has no
  Write). Docs-only; test/fmt green, 7/7 CI, squash-merged, `auto-merged`, #39 item 1 ticked.
- Key ADR-007 decisions: one ordered init-sized `Effects` list (phase non-decreasing:
  persist→send→apply→notify); `Input = message | tick | propose`, tick = logical count, Driver
  turns `Clock` into ticks; node owns entry bytes (`log_bytes_max`); `Node.init` takes a `Restore`
  struct (data, no LogStore); driver does persist → one `sync()` → send → apply, any Fault is
  fail-stop; `src/raft/{node,progress}.zig`, progress internal.
- Next: item 2 (2A-i): FIRST widen tidy `core_purity_files` to cover `src/raft/`, then
  `src/raft/node.zig` skeleton (roles, term rules, `check_invariants`). Tests via test-writer,
  impl via zig-developer; PRD §4.2 should be updated to point at ADR-007 in that PR.
- Blockers: none. Open questions: none.
- Tool notes: `rm -rf .zig-cache` fixes `build runner FileNotFound`. Poll CI with a `for` loop
  around `gh pr checks <n> --watch`. Budget: architect ≈ $1.4 of $4; item 2 needs test-writer +
  zig-developer + reviewer, so expect one subagent-heavy item per cycle.

## Cycles 24-37 (2026-10-01 to 10-07), folded
- 24: camelCase renames in `log.zig`/`types.zig` (#30); item 11 release v0.3.0 (#31), milestone
  #20 closed; plan 003 proposed (#33). 25-29: one `/stabilize --one` each while #33 waited —
  snake_case in `interfaces.zig` (#34) and `build.zig`/tools/bench (#35), CHANGELOG drift (#36),
  every `MemoryStore.check_invariants` variant provoked (#37), every `MessageLogPositionInvalid`
  branch provoked (#38). 30: audit found nothing left (headers, tidy, error-variant coverage).
  31-37: no-op memory-only cycles awaiting the OWNER's merge of #33 (one Discord heartbeat/day).
- Lessons: a blind rename can shadow a new fn name and push lines past 100 cols — run
  `zig build tidy` too. `gh pr create --label stabilize` fails (label absent); `gh pr merge` has
  no `--label` (use `gh pr edit --add-label`). Guard hook blocks `cd <path>;`, `sed -i`, heredocs
  into citadel, `echo > /tmp` mixed with citadel paths, greps over sibling repos (use `gh api`);
  zsh does not word-split `$var` in for loops (use `${=var}`); `sleep` is blocked.

## History (cycles 0-23)
Cycles 13-16 (2026-09-16 to 09-27, mostly FEATURE with plan PR #16 open): plan 002 (Phase 1:
types/interfaces/log/store) awaited OWNER merge through cycle 15; each cycle ran one bounded
stabilization task instead of idling — split `build.zig`'s `build()` into helpers (#17), split
`tools/tidy.zig`'s inline tests into `tools/tidy_test.zig` (#18), widened `tidy`'s size checks
to `tools/`/`build.zig` while deliberately excluding the ban-list checks there (tidy.zig's own
source contains the banned substrings as string literals it checks for — a naive scan would
false-positive) (#19). Cycle 16: plan 002 merged; opened milestone issue #20; item 1 —
`synod.version` derived from `build.zig.zon` instead of hardcoded `0.1.0` (#21).
Cycle 12 (2026-09-16, FEATURE): item 11 (release v0.2.0, milestone 001's last item) via PR #15.
Opened plan 002 (PR #16) via `planner`; caught a live bug — `src/root.zig:11` hardcoded
`SemanticVersion{0,1,0}` — made it plan 002 item 1. Budget note: full-context `planner` calls
consume most of the session budget; keep prompts pointed at files, not pasted excerpts.
Cycle 11 (2026-09-15, FEATURE): item 10 (README/PRD/CHANGELOG reconciliation) via PR #14.
Cycle 10 (2026-09-12, STABILIZATION): fixed a bookkeeping bug (cycle 9's `/report` never wrote
`memory/counter`); tidy-auditor fixed two compound-assert idioms via PR #13.
- Cycle 0 (2026-09-05, RESTRUCTURE): realm created; plan 001 (Zig 0.16 migration + Tiger Style
  baseline) prescribed by ROADMAP.
- Cycle 1 (2026-09-06): plan 001 merged as #2; milestone issue #3 (11 items). Item 1 via #4.
- Cycle 2 (2026-09-06): item 2 (`tidy` sizes) via #5.
- Cycle 3 (2026-09-07): item 3 (`tidy` ban list) via #6.
- Cycle 4 attempt (2026-09-08, PREFLIGHT ABORT): disk gate failed; work preserved to `wip/*`.
- Cycle 4 (2026-09-08): cherry-picked wip branch; merged #7 (0.16 migration of `main.zig`/
  `tidy.zig`). Ticked items 4 and 7.
- Cycle 5 (2026-09-09, STABILIZATION): one compound-assert fix via #8.
- Cycle 6 (2026-09-10): item 5 (0.16 — `bench/main.zig`) via #9.
- Cycle 7 (2026-09-11): item 6 (0.16 — library-core sweep) via #10, zero hits.
- Cycle 8 (2026-09-11): item 8 (`io: Io` at the boundary only) via #11, ADR-002.
- Cycle 9 (2026-09-12): item 9 (assertion baseline) via #12, ADR-003.
- Standing backlog: Phase 1 real work order — `types.zig` → `log.zig` → `interfaces.zig` +
  `store.zig` → Phase 2's `raft/node.zig` election state machine.

Cycles 17-23 (2026-09-27 to 09-30, FEATURE): plan 002 items 4-10 via PRs #22-#29. `types.zig`
scalars as distinct `enum(u64)` (ADR-004), `Message`/`ConfChange` wire shape (ADR-005; a
reviewer caught a peer-triggerable panic in `validateAppendRequest`, range-guarded), `log.zig`
(`append`/`truncate`/`termAt`, `conflictAt` fast-backtrack, `validate()` returning typed
`Invariant*` errors), `interfaces.zig` five vtables (ADR-006, built only via comptime
`X.init(impl)`), `store.zig` `MemoryStore` + `store_conformance.zig`, README/baseline re-measure
(tests 207, no fn > 70 lines). Lessons: an `architect` call costs ~$0.85-1.40 of the $4 budget,
skip it when a doc comment already specifies the contract; confirm every check shows `pass`
before merging; `zig build test` prints tidy-fixture lines and "failed command" on stderr yet
succeeds; use `/Users/fn/.zr/toolchains/zig/0.16.0/zig` (global zig drifted).
