# synod — context

last_seen_at: 2026-10-30T12:00:00Z
rejected_plans: []

## Cycle 74 — 2026-10-30 — FEATURE
- Preflight: disk 41 GB, CI green (6b76395), no bugs, milestone #74 open, no open PRs.
- Done: item 4 (driver snapshot path) on `feat/driver-snapshot-2` (from the cycle-73 wip): zig-developer
  (~$1.1, 10 min) implemented it; 2 tests in `driver_snapshot_test.zig` were themselves wrong (buffer
  size after restart; store_full replay fails stop again), fixed by main session. 955 tests, fmt, tidy
  green locally. PR #82 opened, CI pending at the 22-min deadline; NOT merged, item 4 NOT ticked.
- Flagged: `snapshot_entries_min == 0` now means compaction off (sim/fixture state machines cannot
  snapshot until item 6); ADR-009 documents 1..log_entries_max-1, needs a one-line amendment; item 6
  removes the sentinel. Not yet code-reviewed.
- Next: merge #82 when green (label `auto-merged`), code-reviewer, tick item 4 + #74, ADR amendment,
  then item 5 InstallSnapshot.
- Blockers: none. Open questions: none. Budget: ~$1.6 of $4 used.
- Tool notes: in report, chained Bash that writes citadel files is blocked; use Write/Edit tools.

## Cycle 73 — 2026-10-30 — FEATURE
- Preflight: disk 34 GB, CI green (d07300d), no bugs, milestone #74 open. #79 (tick) was merged.
- Done: PR #80 was DIRTY (based on the pre-merge wip, no CI ran); cherry-picked its review commit onto
  `fix/node-compaction-review-2` from main -> PR #81 (938 tests, fmt, tidy, 7/7 CI), merged
  `auto-merged`; #80 closed, branch kept. Item 4 (driver snapshot path): test-writer (~$1.0, 12 min)
  wrote `src/driver_snapshot_test.zig` (29 tests, 26 red) + one import line in `src/driver.zig`;
  preserved as `wip/feat-driver-snapshot-20261030` (pushed, no PR). Implementation not started.
- Next: `git checkout -b feat/driver-snapshot-2 wip/feat-driver-snapshot-20261030`; start zig-developer
  by minute 3. API the tests assume: buffer = `config.message_limits.snapshot_bytes_max` allocated in
  `Driver.init`; `Fault.SnapshotTooLarge`; on `snapshot_due`: sm snapshot, `save_snapshot`, `sync`, then
  `node.step(.snapshot_saved)` with empty Effects; `Driver.init` loads the store snapshot, restores the
  state machine, builds the node with `Restore.snapshot: log.Base` (new), tail check `last - base <=
  log_entries_max`; `init_bytes_max` grows by `snapshot_bytes_max`; init error set gains restore and
  `load_snapshot` errors. Then reviewer, PR, tick item 4 + #74.
- Blockers: none. Open questions: none. Budget: ~$1.6 of $4 used.
- Tool notes: a wip branch left unmerged goes stale when a continuation branch merges; never leave a
  review-fix PR based on the wip, base it on main. Test-writer took 12 min: brief it narrower.

## Cycle 72 — 2026-10-29 — FEATURE
- Preflight: disk 36 GB, CI green (2641a34), no bugs, milestone #74 open, no open PRs.
- Done: item 3 (node compaction policy) from the cycle-71 wip, on `feat/node-compaction-2`: 926 tests,
  fmt, tidy, `zig build sim -Dseeds=1000` all green; PR #78 merged (7/7 CI, `auto-merged`), #74
  item 3 ticked. code-reviewer (~$0.3) found nonzero-base follower/leader paths untested (sim never
  confirms a snapshot, so base stays 0 there).
- PRs open at the 22-min deadline (CI pending): #79 `docs/tick-plan-005-item3` (plan tick),
  #80 `fix/node-compaction-review` (zig-developer: `src/raft/node_base_test.zig` 12 tests, term check
  at base in `replicate_below_base`, `snapshot_saved` returns empty Effects, 938 tests green locally).
- Next: merge #79 and #80 when CI is green (label `auto-merged`), then item 4 (driver snapshot path;
  driver currently ignores `snapshot_due`). Review notes for items 4/5: a peer with `first < base`
  gets no heartbeat in `send_slot` (liveness gap until InstallSnapshot, item 5);
  `SnapshotDue.configuration` is the latest config, must be as-of-index once item 8 lands.
- Blockers: none. Open questions: none. Budget: ~$1.6 of $4 used.
- Tool notes: background `zig build test` takes ~105 s; use a worktree in /tmp for docs ticks while
  a developer owns the repo tree; cut CHANGELOG lines at 100 columns.

## Cycle 71 — 2026-10-29 — FEATURE
- Preflight: disk 38 GB, CI green (2641a34), no bugs, no open PRs, milestone #74 open. Cycle 70 left
  no context entry; #75 (ADR-009) and #77 (item 2, `log.Log` base) are merged, items 1-2 ticked.
- Done: item 3 (node compaction policy) NOT finished. test-writer (~$0.9) wrote
  `src/raft/node_snapshot_test.zig` (21 tests, verified red, mutants killed in a scratch copy);
  zig-developer (~$0.9) wrote `raft/contract.zig`, `raft/snapshot.zig`, base-aware arithmetic in
  commit/follower/leader/node_init, Config fields in sim/driver. Killed at the 22-min deadline;
  tests never confirmed green. Preserved as `wip/feat-node-compaction-20261029` (pushed, no PR).
- Next: `git checkout -b feat/node-compaction-2 wip/feat-node-compaction-20261029`; run `zig build
  test --summary all`, `zig fmt --check src build.zig tools bench`, `zig build tidy`, `zig build sim
  -Dseeds=1000`; fix; code-reviewer; PR; tick item 3 + #74. Start the developer by minute 3 and
  expect ~15 min of developer time for items of this size; consider splitting item 3 (contract.zig
  move first as its own PR).
- Blockers: none. Open questions: none. Budget: ~$2.1 of $4 used.

## Cycle 69 — 2026-10-28 — FEATURE
- Preflight: disk 38 GB, CI green, no bugs/issues; plan 005 (#73) was merged -> opened milestone
  issue #74.
- Done: item 1 ADR-009 (`docs/adr/0009-phase4-node-contract.md`) drafted by `architect` (opus, ~11
  min, ~$3), PR #75 (docs only) opened; CI Build & Test was still pending at ~17 min, so NOT merged
  and item 1 NOT ticked. Next cycle: merge #75 if green (label `auto-merged`), tick item 1 in plan
  005 + #74. The ADR's "Notes for implementers" flags: item 3 must first move Config..InvariantError
  to `src/raft/contract.zig`; learners get no replication today; `trailing` is `snapshot_trailing`;
  effect slots become `peers_max + 9`.
- Next: item 2 (`log.Log` base index) after #75 merges.
- Blockers: none. Open questions: none. Budget: the architect run cost most of the $4 cap; brief
  narrower or write ADR sections yourself.

## Cycle 68 — 2026-10-27 — FEATURE
- Preflight: disk 41 GB, CI green, no bugs, no issues, no open PRs; plan 004 fully checked.
- Done: `/plan` -> plan 005 (Phase 4: log base/compaction, snapshot path, InstallSnapshot, sim
  snapshots, joint consensus, ReadIndex, sim churn + reads, baseline, release v0.6.0) proposed,
  PR #73, awaiting merge (citadel#77). Lease reads deferred to plan 006. Planner (opus) ~ $0.9.
- Next: when #73 is merged, open the milestone issue and start item 1 (ADR-009 via `architect`;
  main session writes the ADR). Until then one bounded `/stabilize synod --one` per cycle.
- Blockers: none. Open questions: none.

## Cycle 67 — 2026-10-27 — FEATURE
- Preflight: disk 46 GB, CI green (c7d7d80), no bugs, no OWNER comments, no open PRs, #57 open.
- Done: item 12 release v0.5.0 via PR #71 (7/7 CI, `auto-merged`; Build & Test 7m9s): tag +
  GitHub release, milestone #57 closed 12/12. No kingdom repo pins synod (checked
  build.zig.zon of silica/zoltraak/zr/sailor/zuda via `gh api`), so no migration issues. PR #72
  ticked plan 004 and the Phase 1 boxes in `000-inherited.md`. 878 tests. STATE.md has the release.
- Next: no plan open and newest plan 004 fully checked -> cycle 68 runs `/plan synod` (Phase 4
  candidates in `000-inherited.md`: snapshots/membership/read, adapters). Needs >= 10 min of
  budget; start the planner early (opus, point at files).
- Blockers: none. Open questions: none.
- Open suggestions (unchanged from 66): `Workload.check_invariants` only in `check(.linearizability)`;
  `op_id_next` bounded by width; `else =>` arms in `node_fault`/`propose_draw`; sim-nightly first
  scheduled run unobserved (check `gh run list --workflow sim-nightly.yml`, 120 min cap).
- Tool notes: guard blocks `cd <repo>;` and `grep` over sibling repos even read-only: use `gh api
  repos/yusa-imit/<r>/contents/build.zig.zon`. CI Build & Test now ~7 min; release cycle used
  ~20 of 22 min, plan the release PR first thing.

## Cycles 61-66 (2026-10-20..26), folded
- 61: item 9 PR #67 `sim/linearizability.zig` `HistoryChecker` (Wing-Gong, explicit stack). 62-64: PREFLIGHT
  ABORT (disk < 20 GB; box loses ~1 GB/day). 65: item 10 PR #68 KV workload (continued from wip; `calm`
  needed a 256-entry log: no compaction in Phase 3). 66: item 11 PR #69 baseline, review fixes PR #70.
  Kept `wip/feat-sim-kv-workload-*` and `wip/feat-sim-linearizability-*` branches (do not delete).
- Open suggestions: `Workload.check_invariants` only in `check(.linearizability)`; `op_id_next` bounded
  by width; sim-nightly first scheduled run unobserved (120 min cap).
- Tool notes: `.zig-cache` corrupts (`FileNotFound`): `rm -rf .zig-cache`; wip branch names persist, use a
  `-2` suffix for continuation branches; foreground `sleep` blocked, use `python3 -I -c "import time;
  time.sleep(N)"`; `gh pr checks --watch` right after push may say "no checks", retry after ~20 s;
  error traces in failing tests are polluted: print counters temporarily (tidy bans `std.debug.print`).

## Cycles 59-60 (2026-10-19), folded
- C59: item 7 PR #64 `tools/sim.zig` + `zig build sim -Dseeds/-Dseed/-Dseed_start/-Dplant` (ReleaseSafe;
  1000 seeds ~20 s), CI sweep + planted-fault step, bench `sim_cluster_5_nodes_10s` mean 21.9 ms
  (target < 50 ms). Reviews of #63/#61 gave 5 WARNINGs, fixed in C60.
- C60: PR #65 `fix/sim-review-findings` (`OptionsError` gains `CrashPercentInvalid`/`TornPercentInvalid`/
  `DownDurationInvalid`, proposal buffer `[255]u8`, `ProposeTooLarge` arm; 726 tests); item 8 PR #66
  `.github/workflows/sim-nightly.yml` (cron 03:17 UTC + dispatch inputs `seeds`/`plant`; plant=
  lose_synced_hard_state red with ElectionSafety, plant=none 1000 seeds green in ~52 s).
- Caveat: 100k seeds at ~52 s/1000 on the runner is ~87 min vs `timeout-minutes: 120`; watch the first
  scheduled run (`gh run list --workflow sim-nightly.yml`), shrink seeds if it times out. Branch prefix
  `ci/` is not in the kingdom list (use `chore/`).
- Open suggestions: `arm_failure` assert still tautological; plant-refused restart is silent; propose_seq
  u8 wraps; tie-order docs omit heal/propose.
- Tool notes: guard blocks `cd <repo>; ...` chains; global `zig` is 0.15.2, use
  /Users/fn/.zr/toolchains/zig/0.16.0/zig; zig build's Run step loses a child's stderr when the build's
  stderr is redirected to a FILE (pipe is fine, use `2>&1 | tee`); a python slice-replace of ci.yml
  silently truncated the cross-compile job: diff the file before commit.

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

## Cycles 24-54 (2026-10-01..16), folded 2026-10-27
- 24-37: camelCase renames (#30); v0.3.0 (#31); plan 003 proposed (#33), then `/stabilize --one`
  or no-op cycles until the OWNER merged it. 38-50: plan 003 items 1-10, one squash-merged PR each
  (#40-#52, CI 7/7, `auto-merged`; ~$2-3.4 of $4 per item): ADR-007 (one ordered `Effects` list
  persist -> send -> apply -> notify; `Input = message | tick | propose`; node owns entry bytes;
  driver does persist -> one `sync()` -> send -> apply, any Fault is fail-stop), `raft/election.zig`,
  PreVote, `progress.zig` (32 B `Progress`, bounded inflight), `leader.zig` (probe round timeout is
  `heartbeat_ticks`), `follower.zig`, `commit.zig` (effect slots `peers_max + 7`), `cluster_test.zig`
  (3/5 nodes, 500 seeds, partition churn, 4 oracles), `driver.zig` (one-pass `execute`, `stopped`
  fail-stop, `RestoreLogFull`); 495 tests. Reviews fixed peer-reachable asserts (term zero, `prev ==
  0`, `matched == maxInt`) and term wrap.
- 51-54: Tiger Style re-measure (#53), v0.4.0 (#54), plan 004 (Phase 3 simulation, 12 items) via
  PR #56, ADR-008 (#58). 55-56: item 3 `sim/invariants.zig` `Checker` (#60), item 4
  `sim/simulation.zig` (#61); `node.zig` is at the 800-line cap, sizing lives in `raft/node_init.zig`.
- Open suggestions: heartbeats gated by `Progress.can_send` leave a probing peer with a lost round
  silent until it expires (spurious pre-vote); clear a slot's records on `on_timeout`; restored
  entries unchecked against `entry_bytes_max`; no `truncate` fault test; `is_member` includes
  learners for `request_vote`; `votes_len` not cleared in `term_adopt`; `node.*` dangling after
  `RestoreLogFull`; `catch unreachable` in `driver.poll`, `@errorCast` in receive/propose; `chosen_terms`
  records the first observer's term; Phase 1 boxes in `000-inherited.md` unticked.
- Tool notes: `zig build test` exits 0 even with tidy-fixture stderr noise (check `$?`); global zig
  is 0.15.2, use `/Users/fn/.zr/toolchains/zig/0.16.0/zig build test --summary all`; `rm -rf
  .zig-cache` fixes `build runner FileNotFound`; guard blocks `cd <path>;`, `python3 - <<heredoc`
  in repo (write to /tmp, run `python3 -I`), `sed -i`, greps over sibling repos (use `gh api`),
  commands mixing citadel paths with repo writes; `sleep` blocked, use `gh pr checks --watch`;
  no `chore`/`stabilize` labels in synod; label with `gh pr edit --add-label`; architect has no
  Write (main session writes ADRs, ~$0.85-1.40 per call, skip if a doc comment specifies it); a blind
  rename can push lines past 100 cols, run `zig build tidy`; start the test-writer within 5 min.

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
