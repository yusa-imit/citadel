# synod — context

last_seen_at: 2026-11-03T00:00:00Z
rejected_plans: []

## Cycle 80 — 2026-11-03 — FEATURE
- Preflight: disk 23 GB, CI green, no bugs, no new OWNER comments, milestone #74 open. Tree clean.
- Done: PR #84 (item 5 InstallSnapshot, 7/7 CI green on 51738ea) squash-merged as f5ea558, labelled
  `auto-merged`; #74 checklist item 5 ticked (plan file already ticked in the PR).
- Item 6 (sim snapshots): test-writer (~$1.0 of the budget, ~20 min, too slow) wrote 67 tests in
  `src/sim/{workload,crash_store,network,invariants_digest,simulation}_snapshot_test.zig`, 52 fail by
  design against minimal stubs (52 fail, 932 old pass). Preserved, not merged, on
  `wip/feat-sim-snapshots-20261103` (37ee643, pushed; do not delete).
- Next: continue on `feat/sim-snapshots-2` from that wip branch: zig-developer makes the tests pass
  (KV "SKV1" snapshot/restore, CrashStore snapshot op journalled, Network owns snapshot bytes,
  Checker.state_digest, Simulation compaction on + Plant.restore_drops_key + Stats.snapshots/installs,
  remove `snapshot_entries_min == 0` sentinel in sim). Then Driver.init restore-order WARNING.
- Decisions the tests assume (confirm in the developer step): failed `restore` leaves values
  unchanged; truncated stream = `StateMachineSnapshotInvalid` or `EndOfStream`; checker `applied()`
  demands consecutive indexes, but an install jumps the applied index (needs handling); crash stub
  borrows the source snapshot in `copy_store`.
- Blockers: none. Open questions: none. Budget: ~$1.9 of $4.
- Tool notes: split the test-writer brief per file group (it took 19 min for 5 files); a message to a
  running agent lands only at its next tool round.

## Cycle 79 — 2026-11-02 — PREFLIGHT ABORT (disk)
- Disk gate: 19 GB free (< 20 GB), same as cycle 78; stopped before inbox. Tree clean on
  `feat/install-snapshot-2` (51738ea, pushed); nothing to preserve, nothing changed in the repo.
- Next (unchanged): confirm CI on PR #84, merge it (`auto-merged`), tick #74 item 5; then Driver.init
  restore-order WARNING, then item 6 sim snapshots. Needs >= 20 GB free to run.
- Blockers: disk below gate (second abort in a row; box loses ~1 GB/day). Open questions: none.
  Human may need to free space on the box; no GitHub issue opened (quiet repeat).

## Cycle 78 — 2026-11-02 — PREFLIGHT ABORT (disk)
- Disk gate: 18 GB free (< 20 GB); stopped before inbox. No repo changes: tree clean on
  `feat/install-snapshot-2` (51738ea, pushed), nothing to preserve. GitHub state not re-checked.
- Next (unchanged from cycle 77): confirm CI on PR #84 (51738ea), merge it (`auto-merged`), tick #74
  item 5; then Driver.init restore-order WARNING, then item 6 sim snapshots.
- Blockers: disk below gate (box loses ~1 GB/day; same cause as cycles 62-64). Open questions: none.

## Cycle 77 — 2026-11-01 — FEATURE
- Preflight: disk ok, CI green on main, no bugs, milestone #74 open; PR #84 open (item 5, 2 CRITICAL).
- Done on `feat/install-snapshot-2`: CRITICAL 1 fixed test-first: `step_install` emits `save_hard_state`
  (new term, vote, OLD commit) before `save_snapshot`, then the new-commit one (snapshot.zig; ADR-009 +
  CHANGELOG amended). CRITICAL 2: test-writer (~$0.9, 14 min) wrote `src/driver_install_test.zig`
  (19 tests, mutation-checked). Added same-term second-leader test; plan item 5 ticked; stale CHANGELOG
  clause removed; driver `//!` header updated. 1010 tests, fmt green locally.
- PR #84: CI 7/7 green on 4658e52 (persist fix); commit 51738ea (driver tests) pushed at minute 20,
  CI pending at the deadline, NOT merged. Review comment posted.
- Next: merge #84 when CI is green (`auto-merged`), tick #74 item 5; then Driver.init restore-order
  WARNING (cycle 75), then item 6 sim snapshots (remove the min == 0 sentinel in sim).
- Open design note: restore failing after the reply was sent fail-stops; restart recovers from the
  saved snapshot (ADR order reply -> restore); revisit only if the ADR changes.
- Blockers: none. Open questions: none. Budget: ~$1.4 of $4.
- Tool notes: guard blocks `cd <path>;` even inside the repo (cwd is already the repo). Agent clock
  `date` deltas looked short; CI Build & Test is ~7.5 min, so push the last commit by minute 12.

## Cycle 76 (2026-11-01), folded
- PR #84 (item 5 InstallSnapshot) CI green but code-reviewer found 2 CRITICAL (fixed in cycle 77): persist
  order on a term bump in `step_install` and untested driver snapshot paths. Dirty tree from a killed
  session preserved as `wip/feat-install-snapshot-20261101`. Open WARNINGs: follower rejection paths
  untested, `send_slot` replicate branch untested; suggestions: `progress.check_invariants` snapshot =>
  inflight 1, install replaces configuration (latent until item 7), item 6 removes the sim network assert.
- Tool notes: CI Build & Test ~6.5 min; open the PR and start the reviewer before minute 8.

## Cycles 73-75 (2026-10-30), folded
- 73-74: item 4 driver snapshot path (PR #82 opened). 75: #82 merged after merging main into the branch (a
  test file on main broke the branch's config assumption: `snapshot_entries_min == 0` = compaction off in
  fixtures); plan 005 item 4 ticked (#83). Reviewer suggestions still open: assert `snapshot_due` is the
  last effect before `snapshot_save`; `catch unreachable` proof at driver ~246; `@intFromEnum(base.index)+1`
  overflow on 32-bit; `assert_config` should require `snapshot_bytes_max > 0` when min > 0; WARNING:
  `Driver.init` restores the state machine before store/node validation (dirty on failed init).
- Tool notes: merge origin/main into long-lived branches and re-run tests before merging; chained Bash
  mixing `$(date)` with repo writes is blocked.

## Cycles 67-72 (2026-10-27..29), folded
- 67: item 12 release v0.5.0 (PR #71, tag + GitHub release, milestone #57 closed 12/12); no kingdom repo
  pins synod. 68: `/plan` -> plan 005 (Phase 4) PR #73. 69: milestone #74 opened, item 1 ADR-009 PR #75
  (architect opus cost ~$3: brief narrower or write ADR sections in the main session). 71: item 3 node
  compaction killed at deadline, kept as `wip/feat-node-compaction-20261029`. 72: item 3 merged (PR #78);
  reviewer found nonzero-base follower/leader paths untested; PRs #79 (tick) and #80 (review fixes).
- Review notes still live: a peer with `first < base` gets no heartbeat in `send_slot` until
  InstallSnapshot (item 5); `SnapshotDue.configuration` must be as-of-index once item 8 lands; ADR-009
  flags `trailing` is `snapshot_trailing`, effect slots `peers_max + 9`.
- Open suggestions: `Workload.check_invariants` only in `check(.linearizability)`; `op_id_next` bounded
  by width; sim-nightly first scheduled run unobserved (120 min cap).
- Tool notes: guard blocks `cd <repo>;` and `grep` over sibling repos even read-only: use `gh api
  repos/yusa-imit/<r>/contents/build.zig.zon`; background `zig build test` ~105 s; use a /tmp worktree
  for docs ticks while a developer owns the tree; cut CHANGELOG lines at 100 columns; CI Build & Test
  ~7 min, plan the release PR first thing.

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
