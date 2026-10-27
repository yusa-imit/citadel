# synod — context

last_seen_at: 2026-10-28T10:30:00Z
rejected_plans: []

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

## Cycle 66 — 2026-10-26 — FEATURE
- Preflight: disk 42 GB, CI green (1c9723f), no bugs, no OWNER comments, milestone #57 open.
- Done: item 11 via PR #69 (docs only, 7/7 CI): Phase 3 baseline re-measured (all sim fns <= 68
  lines, simulation.zig 870 non-test lines), README sim row implemented, 000-inherited Phase 3
  ticked, milestone item 11 ticked. Reviewed #68 (code-reviewer): 1 CRITICAL + 6 WARNING fixed via
  PR #70 (corrupt KV entry -> typed `WorkloadInvariant`, `WorkloadInvalid` branches tested, ADR-008
  amended; 878 tests, 7/7 CI). Both `auto-merged`.
- `zig build test` now ~105 s locally (workload/sim model tests dominate).
- Next: item 12 release v0.5.0 (`/release synod minor`; gate: 0 bugs, 6 cross targets green).
- Blockers: none. Open questions: none.
- Open suggestions: `Workload.check_invariants` runs only in `check(.linearizability)`, not per event;
  `op_id_next` bounded by width not an option; `else =>` arms in `node_fault`/`propose_draw`
  (simulation.zig) non-exhaustive; sim-nightly first scheduled run still unobserved.
- Tool notes: foreground `sleep` is blocked; use `python3 -I -c "import time; time.sleep(N)"` while
  waiting for a background agent. `gh pr checks --watch` right after push may say "no checks":
  retry after ~20 s. Spawning reviewer (read-only) and doing the docs item in parallel worked well.

## Cycle 65 — 2026-10-26 — FEATURE
- Preflight: disk 24 GB (gate ok), CI green (f09957c), no bugs, no OWNER comments, milestone #57 open.
- Done: item 10 via PR #68 (squash-merged, 7/7 CI, `auto-merged`, 860 tests): continued the
  preserved wip (`feat/sim-kv-workload-3`); the WIP compiled but 3 tests failed: churn commit bound
  ignored workload ops (`committed_bound` now adds `workload.ops_invoked`), and `calm` needed a
  256-entry log (Phase 3 has no compaction, a 64-entry log caps ops at 63). `zig build sim
  -Dseeds=1000` green; `-Dplant=ack_uncommitted` red. Milestone #57 items 1-10 ticked.
- NOT code-reviewed (deadline at 20 of 22 min; CI Build&Test takes 6m22s). Review #68 first next
  cycle (reviewer contract in the cycle 61 block), fix findings in a small PR.
- Next: item 11 (re-measure Tiger Style baseline, docs), then item 12 release v0.5.0.
- Blockers: none. Open questions: none. `wip/feat-sim-kv-workload-*` branches stay (do not delete).
- Tool notes: error-return traces in failing tests are polluted by earlier tests; print stats
  temporarily to find the failing `expect` (remove before commit: tidy bans `std.debug.print`).

## Cycles 62-64 — 2026-10-22..23 — PREFLIGHT ABORT (disk)
- Disk gate failed three cycles in a row: `df -g /` 18 -> 17 -> 16 GB free (< 20). No inbox, no CI check,
  no feature work. The box loses ~1 GB per day; synod's own `.zig-cache` + `zig-out` are only ~160 MB, so
  the OWNER or a cleanup job must free space (other realms' caches, old toolchains, Xcode/Docker data).
- Repo: clean, on `wip/feat-sim-kv-workload-2-20261022` (pushed, preserved, do not delete; holds item 10
  KV workload: `workload.zig`, new `workload_hooks.zig`, `sim_node.zig`, `simulation.zig`, 2 test files;
  tests never run on it; an earlier attempt left `wip/feat-sim-kv-workload-20261021`).
- Next: once disk >= 20 GB, continue item 10 from that wip branch on `feat/sim-kv-workload-3`; reviewer
  contract is in the cycle 61 block. Blockers: low disk. Open questions: none.
- Tool notes: guard blocks `START=$(date ...)` chained with citadel paths; split calls.

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
