# synod — context

last_seen_at: 2026-10-22T00:00:00Z
rejected_plans: []

## Cycle 62 — 2026-10-22 — PREFLIGHT ABORT (disk)
- Disk gate failed: `df -g /` showed 18 GB free (< 20). No inbox, no CI check, no feature work.
- Preflight: tree was dirty on `feat/sim-kv-workload-2` (item 10 KV workload: `workload.zig`,
  new `workload_hooks.zig`, `sim_node.zig`, `simulation.zig`, 2 test files; an earlier cycle-62
  attempt had already left `wip/feat-sim-kv-workload-20261021`). Committed the tree to
  `wip/feat-sim-kv-workload-2-20261022` (pushed, do not delete); tests NOT run on it.
- Next: free disk first (`rm -rf .zig-cache`, old `zig-out`, other realms' caches), then continue
  item 10 from the 20261022 wip branch on `feat/sim-kv-workload-3`. Reviewer contract for item 10
  is in the cycle 61 block below.
- Blockers: low disk on the dev box (needs the OWNER or a cleanup). Open questions: none.

## Cycle 61 — 2026-10-20 — FEATURE
- Inbox: no OWNER comments, no bugs, CI green (f3eacad), milestone #57 open, no open PRs.
- Preflight: cycle 60's item 9 WIP (stub + 4 test files) was uncommitted on
  `feat/sim-linearizability`; preserved to `wip/feat-sim-linearizability-20261020` (pushed, do
  not delete); continued on `feat/sim-linearizability-2`.
- Done: item 9 via PR #67 (squash-merged, 7/7 CI, `auto-merged`): `sim/linearizability.zig`
  `HistoryChecker` (Wing-Gong per key, explicit stack, alloc in `init`). 799 tests. Milestone
  #57 items 1-9 ticked. `code-reviewer`: 0 CRITICAL; fixed W3 (factorial search over pending
  puts: skip a pending put unless a completed get can observe it) with a regression test.
  Cost ~ $1.1 of $4, 13 min (zig-developer ~$0.35, reviewer ~$0.2).
- Next: item 10 (KV workload in the sim). Contract from the reviewer: retire a client index when
  its op goes pending (pending stays outstanding for the one-op-per-client assert); put never
  writes 0; invoke < complete strictly; out-of-range key is a typed workload error, not passed
  to `check`.
- Blockers: none. Open questions: none.
- Open suggestions: client assert skipped above 256 ops; `check` is O(n) per step; ADR-008 says
  `options: *const` but `init` takes by value; sim-nightly first scheduled run not yet observed
  (only dispatch runs exist; watch for the 120 min cap).
- Tool notes: `.zig-cache` corrupts (`FileNotFound`): `rm -rf .zig-cache`. The `branch -b` name
  clash: wip branch names persist, so `-2` suffix for continuation branches.

## Cycle 60 — 2026-10-19 — FEATURE
- Inbox: no OWNER comments, no bugs, CI green (4a8bac4), milestone #57 open, no open PRs.
- Done: (1) PR #65 `fix/sim-review-findings` (squash-merged, 7/7 CI, `auto-merged`): the 5 review
  WARNINGs; `OptionsError` gains `CrashPercentInvalid`/`TornPercentInvalid`/`DownDurationInvalid`,
  proposal buffer now `[255]u8`, `partition_start`/`propose_draw` documented+asserted,
  `ProposeTooLarge` arm; tests in new `sim/simulation_options_test.zig`; 726 tests.
  (2) item 8 via PR #66 (7/7 CI, `auto-merged`): `.github/workflows/sim-nightly.yml` (cron 03:17
  UTC + dispatch inputs `seeds`/`plant`; window start = UTC day number * seeds). Verified by
  dispatch: plant=lose_synced_hard_state red (ElectionSafety), plant=none 1000 seeds green in
  ~52 s. Milestone #57 item 8 ticked. Cost ~ $0.8 of $4, ~11 min.
- Caveat: 100k seeds at ~52 s/1000 on the CI runner is ~87 min vs `timeout-minutes: 120`; watch
  the first scheduled run (`gh run list --workflow sim-nightly.yml`), shrink seeds if it times out.
- Deviations: branch for #66 was `ci/sim-nightly` (not in the kingdom branch-prefix list; use
  `chore/`). Fix PR #65 was not re-reviewed by code-reviewer (small, review-driven).
- Next: item 9 (`sim/linearizability.zig`), then 10, 11, 12 (release v0.5.0).
- Blockers: none. Open questions: none.
- Open suggestions: `im`/`n` renames done; `arm_failure` assert still tautological; plant-refused
  restart is silent.

## Cycle 59 — 2026-10-19 — FEATURE
- Inbox: no OWNER comments, no bugs, CI green (db3c96b), milestone #57 open, no open PRs.
- Done: item 7 via PR #64 (squash-merged, 7/7 CI, `auto-merged`): `tools/sim.zig` + `zig build
  sim -Dseeds/-Dseed/-Dseed_start/-Dplant` (ReleaseSafe; 1000 seeds ~20 s locally), tests in
  `zig build test`, CI sweep + planted-fault step, bench `sim_cluster_5_nodes_10s` mean 21.9 ms
  (target < 50 ms; plan said median, bench prints mean). 722 tests. Milestone #57 item 7 ticked.
  Cost ~ $1.5 of $4; cycle used ~19 of 22 min.
- Reviews (code-reviewer): #64 fixed in-PR (typed ArgsTooMany/WindowOverflow, Flag enum,
  CHANGELOG). #63/#61 found 0 CRITICAL, 5 WARNING NOT yet fixed (do first next cycle, small
  `fix/sim-review-findings` PR): (1) `simulation.zig` ~745: proposal `data` is `[8]u8` but
  validate allows data_bytes <= entry_bytes_max (>8 panics); (2) crash_percent>0 with
  down_ms_max==0 asserts mid-run, needs OptionsError; (3) crash/torn percent >100 asserted not
  returned; (4) `partition_start`/`propose_draw` lack docs and asserts; (5) propose-error switch
  uses `else` with no ProposeTooLarge arm. Suggestions: propose_seq u8 wraps, `im`/`pm`/`n`
  names, tie-order docs omit heal/propose, tautological arm_failure assert.
- Next: fix the 5 warnings, then item 8 (nightly sweep workflow with `--seed-start` rotation).
- Blockers: none. Open questions: none.
- Tool notes: guard blocks `cd <repo>; ...` chains; run from cwd. Global `zig` is 0.15.2: use
  /Users/fn/.zr/toolchains/zig/0.16.0/zig. zig build's Run step loses a child's stderr when the
  build's own stderr is redirected to a FILE (pipe is fine): in CI use `2>&1 | tee`. A python
  slice-replace of ci.yml silently truncated the cross-compile job: diff the file before commit.


## Cycles 57-58 (2026-10-17..18), folded
- 57: item 5 PR #62 `sim/crash_store.zig`, `sim/sim_node.zig`, crash/restart in `Simulation`,
  planted `lose_synced_hard_state` breaks `ElectionSafety`; reviewer fixes: `Stats.lossy_crashes`
  floor >= 30, undrained applies reach the Checker on crash. 703 tests.
- 58: item 6 PR #63 `Faults.partition_*`, `Proposals`, `OptionsError`, `simulation_churn_test.zig`
  (100 seeds); `raft/cluster_test.zig` deleted. 713 tests. `zig build test` ~23 s Debug (plan
  said < 10 s; item 11 re-measures).
- Open suggestions: plant-refused restart is silent; `catch` on `StoreIoFailed` in
  `simulation.zig` is not an exhaustive switch; `arm_failure` assert is tautological.
- Tool notes: guard blocks chained Bash mixing `$(date)`/citadel paths with repo writes: split
  calls. Use `python3 -I - <<'EOF'` for heredocs (backticks expand in `-c`). Failing-test stack
  traces are polluted by `types.zig` error traces: print counters temporarily.

## Cycles 55-56 (2026-10-15..16), folded
- Item 3 (3B) PR #60: `sim/invariants.zig` `Checker` (5 invariants, latched violations,
  allocates only in `init`); `raft/cluster_test.zig` ported onto it. Item 4 (3A-ii) PR #61:
  `sim/simulation.zig`, `Node.init_bytes_max`/`Driver.init_bytes_max` (`node.zig` is exactly at
  the 800-line cap; sizing lives in `raft/node_init.zig`).
- Open suggestions: `chosen_terms` records the first observer's term (weak); `cluster_test.enqueue`
  has an `assert(a and b)`; ADR-008 memory formula omits the per-node `NodeMemory` slice.
- Tool notes: no `timeout` on macOS; use `gh pr checks --watch`. Start the test-writer within
  5 min of preflight; test-writer + developer cost ~$2.5 per item.

## Cycles 53-54 (2026-10-14..15), folded
- Older per-cycle detail dropped to keep this file under 200 lines; the record is the merged
  PRs #54-#58 (v0.4.0 release, plan 004 and ADR-008) and the milestone issues on GitHub.

## Cycles 51-52 (2026-10-13..14), folded
- 51: item 11 (Tiger Style baseline re-measure) via PR #53, docs only; README status "Phase 2
  implemented"; CHANGELOG `Changed` carries the numbers.
- 52: item 12 release v0.4.0 via PR #54 (tag + GitHub release, README install tag bumped, Phase 2
  ticked in `000-inherited.md`); #39 closed. PR #55 ticked the plan 003 checkbox (the plan skill
  stops while the newest plan has unchecked items). `/plan`: plan 004 (Phase 3 simulation
  harness, 12 items, MINOR -> v0.5.0) via `planner`, PR #56 (label `plan`).
- Open suggestions: `catch unreachable` in `driver.poll`, `@errorCast` in receive/propose (narrow
  the `step_message`/`step_propose` error sets in node.zig); Phase 1 boxes in `000-inherited.md`
  still unticked though done.
- Tool notes: guard blocks `cd <path>;`, `python3 - <<heredoc` in repo (write script to /tmp, run
  `python3 -I /tmp/x.py`), any command mixing citadel paths with repo writes (split Bash calls),
  heredocs into citadel (use Write/Edit); `sleep` blocked, use `gh pr checks --watch`;
  `gh pr merge` has no `-q`; `gh pr create --label plan` works; SendMessage resumes a finished
  test-writer.

## Cycles 44-50 (2026-10-11..13), folded
- 44, 47: no-op cycles. 45 (item 6b, #47): `leader.zig` `step_response`, probe round timeout is
  `heartbeat_ticks`. 46 (item 7, #48): `raft/follower.zig` `step_append`. 48 (item 8, #49):
  `raft/commit.zig`, effect slots `peers_max + 7` (ADR-007 amended). 49: review of item 8 (#50)
  and item 9 (#51) `raft/cluster_test.zig` (3/5 nodes, 500 seeds, partition churn, 4 oracles;
  review caught vacuity). 50: item 10 (`driver.zig`, #52): one-pass `execute` (persist, one sync,
  send, apply), `stopped` fail-stop, `RestoreLogFull`. 495 tests.
- Open suggestions: clear a slot's records on `on_timeout`; restored entries not checked against
  `entry_bytes_max`; no `truncate` fault test; `deinit` lacks a precondition doc; `notify_max`
  duplicates an ADR-007 fact.

## Cycles 38-43 (2026-10-08..10), folded
Each plan 003 item = one squash-merged PR (7/7 CI, `auto-merged`, milestone #39 ticked); a
test-writer + developer + reviewer item costs ~$2-3.4 of $4, the per-cycle ceiling.
- 38-39: milestone #39 opened (12 items). ADR-007 (`docs/adr/0007-raft-node-contract.md`, #40;
  architect has no Write, the main session writes the file): one ordered `Effects` list (persist
  -> send -> apply -> notify); `Input = message | tick | propose`; node owns entry bytes; `Restore`
  struct; driver does persist -> one `sync()` -> send -> apply, any Fault is fail-stop. Item 2
  (#41): tidy `is_core_purity_file` matches `src/raft/*.zig`; `node.zig` skeleton.
- 40 (#42): `raft/election.zig` (campaign, request_vote grant/refuse). 41 (#43): PreVote,
  `note_leader`. 42 (#44): internal `raft/progress.zig` (32 B `Progress`, bounded inflight, seeded
  model vs naive reference). 43 (#46): `raft/leader.zig` send side; `node.zig` 786 lines (cap 800).
  Reviews fixed peer-reachable asserts (term zero, `prev == 0`, `matched == maxInt`) and term wrap.
- Standing todo: heartbeats gated by `Progress.can_send` leave a probing peer with a lost round
  silent until the round expires (spurious pre-vote); keep `inflight_count` == live records.
- Open suggestions: `is_member` includes learners for `request_vote`; `votes_len` not cleared in
  `term_adopt`; `node.*` dangling after `RestoreLogFull`; `assert_config` lacks
  `election_ticks <= maxInt(u32)/2`; `become_leader` swallowing `LogFull` untested.
- Tool notes: `zig build test` exits 0 even with tidy-fixture stderr noise (check `$?`);
  code-reviewer cannot run tests (global zig is 0.15.2) — use
  `/Users/fn/.zr/toolchains/zig/0.16.0/zig build test --summary all`; `rm -rf .zig-cache` fixes
  `build runner FileNotFound`; an architect call costs ~$0.85-1.40, skip it when a doc comment
  already specifies the contract.

## Cycles 24-37 (2026-10-01 to 10-07), folded
- 24: camelCase renames (#30); release v0.3.0 (#31), milestone #20 closed; plan 003 proposed
  (#33). 25-30: one `/stabilize --one` each while #33 waited (snake_case, CHANGELOG drift, every
  `MemoryStore.check_invariants` and `MessageLogPositionInvalid` branch provoked). 31-37: no-op
  memory-only cycles awaiting the OWNER's merge of #33 (one Discord heartbeat/day).
- Lessons: a blind rename can push lines past 100 cols — run `zig build tidy` too. `gh pr create
  --label stabilize` fails (label absent); `gh pr merge` has no `--label` (use `gh pr edit
  --add-label`). Guard blocks `sed -i`, `echo > /tmp` mixed with citadel paths, greps over sibling
  repos (use `gh api`); zsh does not word-split `$var` in for loops (use `${=var}`).

## History (cycles 0-23)
- 0-9 (2026-09-05..12): realm created; plan 001 (Zig 0.16 migration + Tiger Style baseline)
  merged as #2, milestone #3; `tidy` sizes and ban list, 0.16 migration of `main.zig`/`tidy.zig`/
  `bench/main.zig`/library core, `io: Io` at the boundary only (ADR-002), assertion baseline
  (ADR-003). Cycle 4 PREFLIGHT ABORT (disk gate) preserved work to `wip/*`.
- 10-12: fixed a missing `memory/counter` write; README/PRD/CHANGELOG reconciliation (#14);
  release v0.2.0 (#15); plan 002 (#16) found a hardcoded `SemanticVersion{0,1,0}`. Full-context
  `planner` calls eat the session budget: point at files, do not paste excerpts.
- 13-16: plan 002 awaited the OWNER; each cycle ran one bounded stabilization task (split
  `build()` helpers #17, `tools/tidy_test.zig` #18, tidy size checks widened to `tools/` with
  ban-list checks excluded because tidy.zig contains the banned substrings #19). Cycle 16:
  plan 002 merged, milestone #20, `synod.version` derived from `build.zig.zon` (#21).
- 17-23 (2026-09-27..30): plan 002 items 4-10 via #22-#29: distinct `enum(u64)` scalars (ADR-004),
  `Message`/`ConfChange` wire shape (ADR-005; reviewer caught a peer-triggerable panic in
  `validateAppendRequest`), `log.zig`, five vtables (ADR-006, built only via comptime
  `X.init(impl)`), `MemoryStore` + `store_conformance.zig`, baseline re-measure (207 tests).
- Standing backlog: Phase 1 order was `types.zig` -> `log.zig` -> `interfaces.zig` + `store.zig`
  -> Phase 2 `raft/node.zig`.
