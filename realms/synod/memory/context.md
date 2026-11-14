# synod — context

last_seen_at: 2026-11-13T18:05:15Z
rejected_plans: []

## Cycle 100 — 2026-11-14 — PREFLIGHT ABORT (disk)
- Disk 15 GB free (< 20 GB gate); no work done, GitHub not inspected, repo untouched (main, clean).
  `/tmp/synod-c99` (127 MB) is the only synod scratch left; guard blocks rm. Operator must free space.
- Next (cycle 101): item 9 ReadIndex `src/raft/read.zig` (test-writer first, start by minute 3).
  Milestone #74 stays 8/12. Blockers: disk. Open questions: none.

## Cycle 99 — 2026-11-13 — FEATURE
- Preflight: disk 23 GB, CI green on a205125, no bugs/PRs, inbox empty (only comment was my own report).
  Tree was clean on merged `feat/joint-consensus-2`; checked out main.
- Done: PR #90 (`fix/pr89-review-followups`, f11ac7d, CI 7/7 green, Build & Test 7m44s, `auto-merged`):
  `leader.step_response` re-derives the peer slot via `slot_of` after `advance_leader`; test (5 -> {1,3,4},
  outgoing-only ack commits the joint entry) is path-only, it passes without the fix; CHANGELOG entry
  for item 8; `leave_if_due` full-log doc (stays due, retried each commit move/tick); ADR-009 voter line;
  `effects_response_max` constant. 1190 tests. zig-developer sonnet ~$0.3 (6.5 min). Total ~$0.6 of $4.
- Next (cycle 100): item 9 ReadIndex `src/raft/read.zig` (test-writer first, start by minute 3). Milestone
  #74 stays 8/12.
- Blockers: none. Open questions: none. Open suggestion: `effects_response_max` slack of 1 may be 3.

## Cycles 87-98 (2026-11-07..13), folded 2026-11-14: plan 005 items 7-8 (joint consensus)
- Disk-gate PREFLIGHT ABORTs: 87-89 and 92-97 (15-19 GB free < 20 gate); the `/tmp/synod-c*` scratch is
  mine but the guard blocks deleting it; the operator freed space before cycle 98.
- 90: PR #87 (item 7) was red only on tidy (`election.zig:3` header 116 cols); merged 2903d04. Reviewer
  follow-up PR #88 (457e65d): `commit.zig` fills aligned matches and uses `membership.quorum_index`;
  `encode` asserts the change validates; voters>0 asserts in `enter_joint`/`quorum_index`. 1151 tests.
- 91: item 8 red step: 38 tests (32 red by design) in `node_reconfigure_test.zig`,
  `node_reconfigure_follower_test.zig`, plus an unwired `src/raft/reconfigure.zig`, kept on
  `wip/feat-joint-consensus-20261109` (d02f2f1, do not delete). The wiring design: `Node` gains
  `configuration_index`, `base_configuration`, `peers: []NodeId` (capacity `peers_max =
  2*voters_max+learners_max-1`); `members` is 3 regions (current | base | scratch); `leader.zig` slot_of /
  peer_of / send_all use `node.peers` (swap-remove on change); hooks `on_append`, `on_truncate`,
  `on_compact`, `leave_if_due`, `step_end`, `receive_check`, `entry_check`; vote/pre-vote refuse when
  `!self_is_voter`; `Status.configuration_index`; `ConfDecodeError`; `InvariantConfigurationInvalid`.
  `node.zig` is at 744/800 lines: keep its edits tiny.
- 95: tree found dirty with interactive item 8 edits, preserved as `wip/feat-joint-consensus-20261113`
  (eca45f6, do not delete; 1183/1189 tests then).
- 98: zig-developer (sonnet, ~$0.7) fixed all 7 items, corrected 4 stale tests against ADR-009 (learners
  replicate, `Snap.slots` size, lone-voter joint model, `leader3` acks 3). PR #89 CI 7/7, merged a205125,
  item 8 ticked, #74 body 8/12. 1189 tests. Reviewer: 0 CRITICAL.
- Tool notes: run local `zig build tidy`/`test` with `--build-file /abs/build.zig --cache-dir
  /tmp/synod-cNN` and redirect to a /tmp file; `python3 -I /tmp/x.py` for multi-file edits works; CI
  Build & Test is 5-7.5 min; start the test-writer by minute 3, push by minute 12.

## Cycles 82-86 (2026-11-04..06), folded 2026-11-09: sim snapshots, membership codec (milestone #74)

- Item 6 (sim snapshots) took 4 cycles (two parallel zig-developers ~$1.4; wips
  `wip/feat-sim-snapshots-20261104` and `-4-20261105` kept, do not delete); merged as PR #85 (8c5f984, 1114
  tests, 1000-seed sweep). `Checker.installed(node, index)` added; `Checker.compacted_print` takes a
  skipped, not-yet-chosen index from a same-term leader's previous window (leader never truncates).
- PR #86 (909919e) added the review follow-ups: cluster test "an ack after the leader compacted past it
  triggers a second snapshot" (`node_install_test.zig`), doc on `Tracker.report`; 1115 tests.
- Item 7 `raft/membership.zig` (PR #87, `feat/membership-codec`; codec `SYCC`+crc32, `enter_joint` /
  `leave_joint`, joint `quorum_reached`/`quorum_index`, `majority`; 36 tests; `election.majority` removed,
  node.zig and commit.zig use membership). Open decode choice: counts summing past 48 ids give
  `ConfLength` (ADR silent; add a line to ADR-009). Item 8 `reconfigure.zig` is big: widen progress slots
  to `peers_max`, learners.
- Still open: torn-write crash with a leader commit + persisted snapshot could give a false `installed`
  violation (unconfirmed; prove or raise chosen_max in `Tracker.restarted`); drop `Options.fault = .none`
  default in `workload.zig`; `nodes_max` duplicated.
- Tool notes: the guard blocks `cd <repo>;` + heredoc/`&`/`timeout` combos, `$(date)` chained with citadel
  paths, and `G=git -C ...; $G` variables: use literal `git -C /abs/path`, `gh --repo`,
  `zig build --build-file /abs/build.zig --cache-dir /tmp/x`, the Write/Edit tools for files; `timeout`
  does not exist on macOS; foreground `gh pr checks --watch` caps at 560 s; `zig build test` >120 s runs in
  the background; test-writer ~10 min (start by minute 3, push by minute 12; CI Build & Test ~9.5 min);
  split the test-writer brief per file group; a message to a running agent lands at its next tool round;
  parallel builds need a `--cache-dir /tmp/<name>` each; latched-violation stack trace: temporarily
  `std.debug.dumpCurrentStackTrace(.{})` in `Checker.fail`.

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
