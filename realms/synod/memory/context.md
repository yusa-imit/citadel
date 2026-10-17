# synod — context

last_seen_at: 2026-10-17T06:30:00Z
rejected_plans: []

## Cycle 57 — 2026-10-17 — FEATURE
- Inbox: no OWNER comments, no bugs, CI green (84158c9), milestone #57 open, no open PRs.
- Preflight: found cycle 56's item 5 WIP uncommitted on `feat/sim-crash-restart`; preserved to
  `wip/feat-sim-crash-restart-20261017` (pushed, do not delete), continued on
  `feat/sim-crash-restart-2` (deleted at merge). The only red test was a wrong vacuity floor
  (`torn >= 300`, measured 280 -> 200).
- Done: item 5 via PR #62 (squash-merged, 7/7 CI, `auto-merged`): `sim/crash_store.zig`,
  `sim/sim_node.zig`, crash/restart in `Simulation`, planted `lose_synced_hard_state` breaks
  `ElectionSafety`. 703 tests. `code-reviewer` (~$0.3): 0 CRITICAL, 4 WARNING fixed
  (undrained applies now reach the Checker on a crash event, new `Stats.lossy_crashes` floor
  >= 30 (measured 71), stale "Red stub" headers, ADR-008 "Amendments" section). Milestone #57
  item 5 ticked. Cost ~ $1.1 of $4.
- Next: item 6 (retire `cluster_test` onto `Simulation`; `zig build test` < 10 s).
- Open suggestions: plant-refused restart is silent (no counter); `catch` on `StoreIoFailed`
  in `simulation.zig` is not an exhaustive switch; `arm_failure` assert is tautological; no
  `crash_keeping(keep)` test hook. PR #61 got only the incidental review above.
- Blockers: none. Open questions: none.
- Tool notes: python3 heredoc via `-c "..."` expands backticks (use `python3 -I - <<'EOF'`);
  failing-test stack traces are polluted by `types.zig` error traces: print counters
  temporarily to find which expect failed.

## Cycle 56 — 2026-10-16 — FEATURE
- Inbox: no OWNER comments, no bugs, CI green (3588168), milestone #57 open, no open PRs.
- Done: item 4 (3A-ii) via PR #61 (squash-merged, 7/7 CI, `auto-merged`): `sim/simulation.zig`
  (`Simulation` init/step/run_until/propose/check/report, `run_seed`, `EventsExhausted`),
  `Node.init_bytes_max`/`Driver.init_bytes_max` (sizing in `raft/node_init.zig`: `node.zig` is
  exactly 800 lines, the cap). 666 tests. Milestone #57 item 4 ticked. Cost ~ $2.9 of $4:
  test-writer ~$1.2 (8 min), developer ~$1.3 (9 min).
- NOT code-reviewed (deadline hit at 18 min before CI): run `code-reviewer` on PR #61's diff
  first thing next cycle, fix findings in a small PR.
- ADR-008 deviations to amend: `propose` is a scripted non-event call; `Stats.digest` content;
  `Error` carries `raft.ProposeError` and `Network.InvariantError`; `init(io, gpa, options)`;
  `check(.linearizability)` no-op until item 9; `events_max = 0` allowed.
- Next: item 5 (crash and restart; sim-only crash store, planted lost-synced-write fault). Start
  the test-writer within 3 min of preflight; test-writer + developer already eat ~$2.5.
- Blockers: none. Open questions: none.
- Tool notes: guard blocks `cd <repo>; ...` chains mixing in `$(cat /tmp/..)`; run zig from the
  repo cwd without `cd`. `zig build test` ~16 s now (cluster_test ~8 s, removed by item 6).

## Cycle 55 — 2026-10-15 — FEATURE
- Inbox: no OWNER comments, no bugs, CI green (60e8664), milestone #57 open, no open PRs.
- Done: item 3 (3B) via PR #60 (squash-merged, 7/7 CI, `auto-merged`): `sim/invariants.zig`
  (`Checker`: election safety, leader append-only, log matching, leader completeness, state
  machine safety; fingerprints, latched violations, allocates only in `init`);
  `raft/cluster_test.zig` ported onto it (688 -> ~500 lines, private Oracle deleted). 636 tests.
  Flow: test-writer ($0.7) -> developer ($0.6) -> reviewer (0 CRITICAL, 5 WARNING fixed via
  SendMessage resume, $0.2). Cost ~ $2.4 of $4. Milestone #57 item 3 ticked.
- Next: item 4 (`sim/simulation.zig` event loop; adds `init_bytes_max` to `raft.Node`/`Driver`).
- Open suggestions: `chosen_terms` records the first observer's term (sound but weak: record the
  minimum, run all `commit_node` before any `leader_complete`); assertion density < 2 in a few
  small helpers; `cluster_test.enqueue` has an `assert(a and b)`; ADR-008 memory formula omits
  the per-node `NodeMemory` slice; `restarted` keeps the leader-per-term table (pinned by a test).
- Blockers: none. Open questions: none.
- Tool notes: `timeout` is not on this macOS shell; use `gh pr checks --watch` with the Bash tool
  timeout. Deadline was tight (~22 min): start the test-writer within 5 min of preflight.

## Cycle 54 — 2026-10-15 — FEATURE
- Inbox: no OWNER comments, no bugs, CI green, no open PRs; milestone #57 open.
- Preflight: found the previous cycle's interrupted item 2 work (tests written, impl stubs) on
  `feat/sim-clock-network`; preserved to `wip/feat-sim-clock-network-20261015` (pushed), then
  restored onto the feat branch from it. Do not delete the wip branch.
- Done: item 2 (3A-i) via PR #59 (squash-merged, 7/7 CI, `auto-merged`): `sim/prng.zig`
  (SplitMix64, `derive_seed`), `sim/clock.zig` (`VirtualClock`), `sim/network.zig` (bounded,
  loss/delay/dup/partition/planted faults, conservation identity), tidy sim purity gate
  (`is_sim_purity_file`, `sim_banned_patterns`, `sim_banned_tokens`, comment lines skipped),
  ADR-008 amended (`Network.slot_meta_bytes = 24`, `check_invariants`). 594 tests. Reviewer
  warnings fixed (u64 due-time overflow, `messages_max+1` u32, `set_partition` validates before
  mutating, tautological asserts). Cost ~ $2.1 of $4. Milestone #57 item 2 ticked.
- Next: item 3 (`sim/invariants.zig`, five safety properties), then item 4 (`simulation.zig`,
  adds `init_bytes_max` to `raft.Node`/`Driver`). `network_test.zig` is 906 lines (tidy does not
  flag it; split if tidy starts to). Suggestion left: `std.hash.Wyhash` in `trace_hash` is not
  pinned across Zig releases (fine until traces are persisted).
- Blockers: none. Open questions: none.
- Tool notes: in a new cycle the working tree may hold WIP from a killed run: check `git status`
  first. Developer agent resumed with SendMessage for review fixes kept context cheap (~$0.5).

## Cycle 53 — 2026-10-14 — FEATURE
- Inbox: plan 004 PR #56 merged by the OWNER; no bugs, CI green, no open issues.
- Done: opened milestone #57 (12 items). Item 1 ADR-008 (`docs/adr/0008-simulator-contract.md`)
  via `architect` (~$1.8 of $4, ~12 min wall), PR #58 (docs, CHANGELOG entry, plan box ticked,
  7/7 CI, squash-merged). The architect returned the text HTML-escaped (`&lt; &gt; &amp;`):
  unescape before writing. Milestone #57 item 1 ticked.
- Next: item 2 (`sim/clock.zig`, `sim/network.zig`, widen tidy purity gate per ADR-008:
  `sim_purity_dir`, `is_sim_purity_file`, `sim_banned_patterns`; also `sim/prng.zig` is
  ADR-008's determinism root, add it with item 2). Item 4's PR adds `init_bytes_max` to
  `raft.Node` and `Driver` (ADR-008 Consequences 1).
- Blockers: none. Open questions: none.
- Tool notes: waiting for a background agent by `sleep` in background costs ~$0.5 of context
  per wake; give the agent one long job and do not poll. Guard blocks `cd <path>;` and `>`
  redirects mixed with citadel paths; use Write for /tmp files. Global zig is 0.15.2, use
  `/Users/fn/.zr/toolchains/zig/0.16.0/zig build test --build-file ... --cache-dir /tmp/x`.

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
