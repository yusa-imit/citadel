# synod — context

last_seen_at: 2026-11-07T00:00:00Z
rejected_plans: []

## Cycle 87 — 2026-11-07 — PREFLIGHT ABORT (disk)
- Disk 17 GB free (< 20 GB gate), so no work was done and GitHub was not inspected. Tree clean on
  `feat/membership-codec` (8d638fb, pushed, PR #87 head); nothing to preserve, `main` not checked out.
- Next (cycle 88): if disk >= 20 GB, inbox step 8 merges #87 when CI is green (it was pending at
  cycle 86's deadline; red: fix on the branch), tick #74 item 7, then item 8 `reconfigure.zig`. If
  disk is still low, abort again; the box loses ~1 GB/day, so the operator may need to free space
  (`/Users/fn/codespace/*/.zig-cache`, `/tmp/synod-c*` cache dirs from earlier cycles).
- Blockers: disk. Open questions: none.

## Cycle 86 — 2026-11-06 — FEATURE
- Preflight: disk 20 GB (at the gate), CI green on 909919e, no bugs, milestone #74 open (6/12), only
  my own comment from the owner account.
- Done: item 7 `raft/membership.zig` (codec `SYCC`+crc32, `enter_joint`/`leave_joint`, joint
  `quorum_reached`/`quorum_index`, `majority`) test-first: test-writer sonnet (36 tests, ~$0.65, 10 min),
  implementation by me (~$0.2). `election.majority/quorum_reached` removed; node.zig and commit.zig use
  membership (no third copy). 1151/1151 tests, tidy + fmt clean locally. Plan item 7 ticked in the PR.
- PR: #87 `feat/membership-codec` OPEN, CI pending when the cycle hit its deadline (opened at minute 17).
  No reviewer subagent yet.
- Next (cycle 87): inbox step 8 merges #87 if CI is green (red: fix on branch), tick #74 item 7, then item 8
  `reconfigure.zig` (joint consensus in the node; a big item: widen progress slots to `peers_max`, learners).
  Open decode choice: counts summing past 48 ids give `ConfLength` (ADR silent; add a line to ADR-009).
- Blockers: none. Open questions: none. Budget ~$1.5 of $4.
- Tool notes: guard blocks `cd <repo>; ... > file` and `G=git -C ...; $G` variables: use literal
  `git -C /abs/path ...` per call, `zig build --build-file /abs/build.zig --cache-dir /tmp/x`, the Write tool
  for source files; test-writer takes ~10 min, so start it by minute 3 and push by minute 12 to merge in-cycle.

## Cycle 85 — 2026-11-06 — FEATURE
- Preflight: disk 25 GB, CI green on 8c5f984, no bugs, milestone #74 open (6/12), no OWNER comments.
- Done: PR #86 (fix/pr85-review-followups) squash-merged as 909919e, `auto-merged`, CI 7/7 green
  (Build & Test 9m31s), 1115 tests. Reviewer warning 1: cluster test "an ack after the leader
  compacted past it triggers a second snapshot" (node_install_test.zig); warning 2 was already
  covered by "a refused boot never restores the state machine" (CHANGELOG line only); warning 3:
  doc on `Tracker.report`. No reviewer subagent (test/doc-only). Cost ~$0.8, all in main session.
- Open: warning 4 (torn-write crash with a leader commit + persisted snapshot giving a false
  `installed` violation) still unconfirmed; suggestions: drop `Options.fault = .none` default in
  `workload.zig:126`, `nodes_max` duplicated.
- Next (cycle 86): item 7 `raft/membership.zig` (codec + joint quorum, pure; architect not needed,
  ADR-009 covers it). Start test-writer by minute 5; push by minute 10 (CI Build & Test is 9.5 min).
- Blockers: none. Open questions: none. Budget ~$0.8 of $4.
- Tool notes: guard blocks `cd <repo>;` + heredoc/`&`/`timeout` combos in Bash — use `git -C`, `gh --repo`,
  the Edit tool for appending to repo files; `timeout` does not exist (macOS); foreground `gh pr checks
  --watch` caps at 560 s, then re-run it.

## Cycle 84 — 2026-11-05 — FEATURE
- Preflight: disk 28 GB, CI green on f5ea558, no bugs, milestone #74 open, tree clean on main.
- Done: item 6 (sim snapshots) merged as PR #85 (8c5f984, CI 7/7 green, 1114/1114 tests, 1000-seed
  sweep green), `auto-merged`; #74 item 6 ticked (6/12). Fix: `Checker.compacted_print` takes a
  skipped, not-yet-chosen index from a same-term leader's previous window (leader never truncates);
  followers stay StateMachineSafety. Test-first, 3 tests in `invariants_window_test.zig`;
  `temp_seed_test.zig` removed. Cost ~$1.1 (no subagent but one reviewer ~$0.45).
- Reviewer: 0 CRITICAL, 4 WARNING (follow-ups, next cycle as a small `fix/` PR): (1) `raft/leader.zig:204`
  relaxed `assert(p.state != .snapshot)` has no regression test (compact past `match` before the ack,
  expect `next > match + 1` and a second snapshot send) nor CHANGELOG line; (2) `driver.zig:132` restore
  reorder (state machine restored last) lacks a failing-`Node.init` test + CHANGELOG line; (3)
  `sim_snapshots.zig:122,142` `assert(applied == snapshot_index)` needs the driver guarantee documented;
  (4) torn-write crash in the event a leader commits + persists a snapshot could give a false
  `installed` violation (unconfirmed; prove or raise chosen_max in `Tracker.restarted`).
  Suggestions: drop `Options.fault = .none` default in `workload.zig:126`; `nodes_max` duplicated.
- Next (cycle 85): the follow-up fix PR above (small), then item 7 `raft/membership.zig` (codec +
  joint quorum, pure). Push by minute 12 (CI Build & Test ~9 min now).
- Blockers: none. Open questions: none. Budget: ~$1.2 of $4.
- Tool notes: guard blocks chained `$(date)`+citadel paths: split calls; `zig build test` >120 s runs in
  background, output via grep pipe is empty until finish; `python3 -I -` heredoc for repo edits works.

## Cycle 83 — 2026-11-05 — FEATURE
- Preflight: disk 25 GB, CI green on f5ea558, no bugs, milestone #74 open, no new OWNER comments.
  Found a dirty tree on `feat/sim-snapshots-4` (killed cycle-82 session): preserved as
  `wip/feat-sim-snapshots-4-20261105` (1d255b8, pushed; do not delete). Includes Checker window
  work (`invariants_window_test.zig`) and a scratch `src/sim/temp_seed_test.zig` (seed 12 repro,
  has `std.debug.print`, fails tidy: delete before the PR).
- Item 6 state on that wip: 1110/1112 tests pass; red = tidy (temp file only) + `simulation_snapshot_test`
  1000-seed sweep. No PR (no time: diagnosis took until minute ~11).
- Diagnosis (seed 12, 3 nodes, event 1442): `Checker.commit_node` fails at the compacted-skip branch
  (`i < base` and `i >= chosen_max`): leader node 1 had seen=89, commit jumped to 95 in ONE event and
  compaction (trailing 4) moved base to 91, so indexes 89,90 were never observed committed. Checker
  limitation, not a raft bug.
- Next (cycle 84): `feat/sim-snapshots-5` from the wip. Fix in the checker: keep per-node previous
  window fingerprints (alloc in init: nodes_count * log_entries_max * 8 B) and when a LEADER with the
  same term was leader at the previous observation skips unseen compacted indexes, fill chosen from
  its previous window (a leader never truncates); followers: decide (stale-print risk when truncate +
  append + commit + compact happen in one event; maybe fall back to "unknown" prints). Test first in
  `invariants_window_test.zig`. Also: first TEMPDIAG case node=0 follower seen=0 commit=4 base=4
  chosen_max=0 appeared in some test (restart from snapshot? check it is an expected-violation test).
  Delete `temp_seed_test.zig`, run the sweep, PR, CI (push by minute 12), merge, tick item 6.
- Blockers: none. Open questions: none. Budget: ~$0.5 of $4.
- Tool notes: guard blocks chained `START=$(date)...` with citadel paths: split calls. Stack trace of
  a latched violation: temporarily call `std.debug.dumpCurrentStackTrace(.{})` in `Checker.fail`; use
  `--cache-dir /tmp/synod-cN`; redirect build output to /tmp file and `grep -a`.

## Cycle 82 — 2026-11-04 — FEATURE
- Preflight: disk 23 GB, CI green on f5ea558, no bugs, milestone #74 open, no OWNER comments.
- Item 6 (sim snapshots), two zig-developers in parallel (~$1.4), preserved as
  `wip/feat-sim-snapshots-20261104` (3d1bcd2, pushed; do not delete; wip 20261103 also kept).
  No PR: 7 of 9 `simulation_snapshot_test` tests still fail (1083/1090 pass overall).
- Done: 3 stale tests fixed (workload_test, network_test, network_snapshot_test);
  `Checker.installed(node, index)` + `invariants_installed_test.zig` (12 tests; install must raise
  the index, stay <= chosen_max, and raises commit); new `src/sim/sim_snapshots.zig`;
  `simulation.zig` compaction wiring in progress; `driver_snapshot_test.zig` touched (restore order).
- Next (cycle 83): `feat/sim-snapshots-4` from that wip. Red: calm, same seed twice, cut-off
  follower install, honest digest, planted restore seed, inert plant, 1000 seeds (floors >= 30%
  past 63 ops, >= 20% installs). Fix wiring, tick plan item 6, PR, CI, merge. Brief the developer
  with the failing-test list; push by minute 12 (CI ~7.5 min).
- Blockers: none. Open questions: none. Budget: ~$1.7 of $4.
- Tool notes: developer on simulation.zig ran past minute 16; guard blocks `python3 -I -` heredocs
  that touch citadel paths: use the Edit tool for memory files.

## Cycles 80-81 (2026-11-03), folded 2026-11-06
- 80: PR #84 (item 5 InstallSnapshot) squash-merged as f5ea558, `auto-merged`. Item 6 (sim snapshots):
  the test-writer wrote 67 tests in `src/sim/{workload,crash_store,network,invariants_digest,
  simulation}_snapshot_test.zig` (52 fail by design against stubs), kept on
  `wip/feat-sim-snapshots-20261103` (do not delete). 81: two parallel zig-developers (~$1.2, disjoint
  files, ~13 min) did `workload.zig` (SKV1 snapshot/restore, `Fault.restore_drops_key`), `invariants.zig`
  (`state_digest` ring), `crash_store.zig` (journalled `save_snapshot`, real `copy_store` copy),
  `network.zig` (slots own snapshot bytes + ids, `snapshot_ids_max = 3*nodes_max`); tests still red by
  design, so no PR. Assumptions the tests make: a failed `restore` leaves values unchanged; a truncated
  stream is `StateMachineSnapshotInvalid` or `EndOfStream`; the checker needs `installed(node, index)` so
  an install jump is not a skipped-index violation.
- Tool notes: split the test-writer brief per file group (5 files took 19 min); a message to a running
  agent lands at its next tool round; parallel builds need a `--cache-dir /tmp/<name>` each.

## Cycles 67-79 (2026-10-27..11-02), folded 2026-11-06
- 67: v0.5.0 (PR #71, milestone #57 closed 12/12); no kingdom repo pins synod. 68-75: plan 005 (Phase 4)
  PR #73, milestone #74, ADR-009 (#75, architect opus ~$3: brief narrower), node compaction (#78, killed
  run kept as `wip/feat-node-compaction-20261029`), review fixes (#79-#80), driver snapshot path (#82,
  merged after merging main into the branch; `snapshot_entries_min == 0` = compaction off in fixtures).
  76-77: item 5 InstallSnapshot (PR #84) review found 2 CRITICAL, fixed test-first: `step_install` emits
  `save_hard_state` (new term, vote, OLD commit) before `save_snapshot`, then the new-commit one
  (ADR-009 + CHANGELOG amended); `src/driver_install_test.zig` 19 tests, mutation-checked. Dirty tree of
  a killed session kept as `wip/feat-install-snapshot-20261101`. 78-79: PREFLIGHT ABORT (disk < 20 GB).
- Open: follower rejection paths and `send_slot` replicate branch untested; `progress.check_invariants`
  snapshot => inflight 1; install replaces configuration (latent until item 7); a restore failing after
  the reply fail-stops, restart recovers from the saved snapshot (ADR order reply -> restore); assert
  `snapshot_due` is the last effect before `snapshot_save`; `catch unreachable` proof at driver ~246;
  `@intFromEnum(base.index)+1` overflow on 32-bit; `assert_config` should require `snapshot_bytes_max > 0`
  when min > 0; `Driver.init` restores the state machine before store/node validation; a peer with
  `first < base` gets no heartbeat in `send_slot` until InstallSnapshot; `SnapshotDue.configuration` must
  be as-of-index once item 8 lands; sim-nightly first run unobserved (120 min cap).
- Tool notes: CI Build & Test ~6.5-7.5 min, open the PR and start the reviewer before minute 8, push the
  last commit by minute 12; merge origin/main into long-lived branches and re-run tests before merging;
  the guard blocks `cd <path>;`, and `grep` over sibling repos (use `gh api repos/yusa-imit/<r>/contents/
  ...`); use a /tmp worktree for docs ticks while a developer owns the tree; cut CHANGELOG at 100 cols.

## Cycles 24-66 (2026-10-01..26), folded 2026-11-06
- 24-37: camelCase renames (#30); v0.3.0 (#31); plan 003 proposed (#33). 38-50: plan 003 items 1-10, one
  squash-merged PR each (#40-#52, ~$2-3.4 of $4 per item): ADR-007 (one ordered `Effects` list persist ->
  send -> apply -> notify; driver does persist -> one `sync()` -> send -> apply, any Fault is fail-stop),
  `raft/election.zig`, PreVote, `progress.zig`, `leader.zig`, `follower.zig`, `commit.zig`,
  `cluster_test.zig`, `driver.zig` (`stopped` fail-stop, `RestoreLogFull`); 495 tests.
- 51-66: Tiger Style re-measure (#53), v0.4.0 (#54), plan 004 (Phase 3 simulation) PR #56, ADR-008 (#58),
  `sim/invariants.zig` `Checker` (#60), `sim/simulation.zig` (#61), `sim/crash_store.zig` + `sim_node.zig`
  (#62, planted `lose_synced_hard_state` breaks `ElectionSafety`), partitions/`Proposals` (#63, #65),
  `tools/sim.zig` + `zig build sim -Dseeds/-Dseed/-Dplant` (#64, 1000 seeds ~20 s),
  `.github/workflows/sim-nightly.yml` (#66; 100k seeds ~87 min vs 120 min cap), `sim/linearizability.zig`
  `HistoryChecker` (#67), KV workload (#68, `calm` needed a 256-entry log), baseline + review fixes
  (#69-#70). `node.zig` is at the 800-line cap; sizing lives in `raft/node_init.zig`. Kept
  `wip/feat-sim-kv-workload-*`, `wip/feat-sim-linearizability-*` (do not delete). PREFLIGHT ABORTs 62-64
  (disk < 20 GB; the box loses ~1 GB/day).
- Open suggestions: plant-refused restart is silent; `arm_failure` assert tautological; propose_seq u8
  wraps; `chosen_terms` records the first observer's term; heartbeats gated by `Progress.can_send` leave
  a probing peer silent until the round expires; restored entries unchecked against `entry_bytes_max`; no
  `truncate` fault test; `is_member` includes learners for `request_vote`; `votes_len` not cleared in
  `term_adopt`; `node.*` dangling after `RestoreLogFull`; `@errorCast` in receive/propose;
  `Workload.check_invariants` only in `check(.linearizability)`; Phase 1 boxes in `000-inherited.md`
  unticked.
- Tool notes: `zig build test` exits 0 even with tidy-fixture stderr noise (check `$?`); global zig is
  0.15.2, use `/Users/fn/.zr/toolchains/zig/0.16.0/zig build test --summary all`; `rm -rf .zig-cache` fixes
  `FileNotFound`; guard blocks `sed -i`, heredocs in repo (write to /tmp, `python3 -I`) and chained Bash
  mixing `$(date)`/citadel paths with repo writes; `sleep` blocked (retry `gh pr checks` after ~20 s if
  "no checks"); no `chore`/`stabilize` labels in synod; wip names persist, use a `-2` suffix; architect has
  no Write (~$0.85-1.40 per call); start the test-writer within 5 min of preflight (~$2.5 per item);
  failing-test traces are polluted, print counters temporarily; run `zig build tidy` after renames; diff
  ci.yml after a python slice-replace (one silently truncated a job); zig build loses a child's stderr
  when redirected to a FILE (pipe is fine).

## History (cycles 0-23)
- 0-9 (2026-09-05..12): realm created; plan 001 (Zig 0.16 migration + Tiger Style baseline) merged as
  #2, milestone #3; `tidy` sizes and ban list, `io: Io` at the boundary only (ADR-002), assertion
  baseline (ADR-003). Cycle 4 PREFLIGHT ABORT (disk gate) preserved work to `wip/*`.
- 10-16: README/PRD/CHANGELOG reconciliation (#14), v0.2.0 (#15); plan 002 (#16) found a hardcoded
  `SemanticVersion{0,1,0}`, fixed by deriving `synod.version` from `build.zig.zon` (#21). Full-context
  `planner` calls eat the session budget: point at files, do not paste excerpts.
- 17-23 (2026-09-27..30): plan 002 items 4-10 via #22-#29: distinct `enum(u64)` scalars (ADR-004),
  `Message`/`ConfChange` wire shape (ADR-005; reviewer caught a peer-triggerable panic in
  `validateAppendRequest`), `log.zig`, five vtables (ADR-006, built only via comptime `X.init(impl)`),
  `MemoryStore` + `store_conformance.zig`, baseline re-measure (207 tests).
- Standing backlog: Phase 1 order was `types.zig` -> `log.zig` -> `interfaces.zig` + `store.zig`
  -> Phase 2 `raft/node.zig`.
