# synod — context

last_seen_at: 2026-09-28T18:20:14Z
rejected_plans: []

## Cycle 20 — 2026-09-28 — FEATURE
- Inbox: no new OWNER actions since watermark (only the AI's own cycle-19 report comment on
  issue #20). No plan PR, no plan_closed_unmerged, no bug/directive/question issues, CI green
  (matches origin/main). `periodic_stabilization: off` confirmed still in effect (REALM.md),
  so cycle 20's `n % 5 == 0` did not force STABILIZATION.
- Item 7 (1B-ii `log.zig` — conflict-point search and `validate()`) via PR #25: skipped the
  `architect` call — `Conflict{index,term}` was already fully specified by its doc comment in
  `types.zig` (item 1A-ii, PR #23), so this was implementing an already-designed contract, not
  a new interface decision. Designed directly, then `test-writer`/`zig-developer`/
  `code-reviewer` (all sonnet). `Log.conflictAt()`: Raft thesis §5.3 fast-backtrack search —
  `.zero` prev-index always matches; a shorter follower log reports `Conflict{.zero,.zero}`;
  a term mismatch reports the conflicting term plus the first index of its run (bounded
  backward scan, floored at index 1). `Log.validate()`/`InvariantError`: defense-in-depth
  corruption checker (index contiguity, non-decreasing terms, no snapshot-boundary gap) over
  the entries array — returns typed `error.Invariant*` rather than asserting, since it exists
  to catch hand-corrupted data for Phase 3's simulator, not caller bugs (REALM.md's
  assert-vs-return rule). Wired `log.validate()` into every existing log-mutating test per
  ADR-003. 13 new tests incl. a seeded property test against an independent backward-scan
  reference for `conflictAt`, and one negative test per `InvariantError` variant using
  hand-corrupted entry arrays.
- `code-reviewer` found 0 CRITICAL, 2 WARNING (both fixed before merge): a postcondition
  assert in `validate()` was tautological (compared `lastIndex()`'s own read to itself instead
  of independently re-deriving the property — Tiger Style §1.2, fixed to check
  `@intFromEnum(entries[count-1].index) == count`); missing CHANGELOG entry. `zig build test`
  153/153, `zig fmt --check` clean, 7/7 CI jobs green, squash-merged, labeled `auto-merged`.
- Toolchain note (from zig-developer/code-reviewer): the global `/opt/homebrew/bin/zig`
  reports 0.15.2 but has drifted further and produces spurious unrelated errors on this repo;
  always use `/Users/fn/.zr/toolchains/zig/0.16.0/zig` for synod (REALM.md's own "Known gaps"
  section already flags the repo has been on 0.16.0 since PR #7 — not a new issue, just a
  reminder of which binary to invoke).
- Milestone issue #20: 7/11 items done. Next: item 8 (1C `interfaces.zig` — the five vtables:
  `Transport`/`LogStore`/`StateMachine`/`Clock`/`Rng`; plan doc flags a PRD §4.1 correction —
  named error sets per method, `*std.Io.Writer`/`*std.Io.Reader` for `snapshot()` since
  `interfaces.zig` sits outside tidy's `core_purity_files`). This is an interface/wire-shape
  decision (five public vtables) — budget for an `architect` call next cycle.
- Open questions: none.

## Cycle 19 — 2026-09-28 — FEATURE
- Inbox: no new OWNER actions since watermark. PR #23 (item 5, held over from cycle 18) was
  all-green with no `hold` label → merged via inbox rule 8, labeled `auto-merged`.
- Item 6 (1B-i `log.zig` — `Log` with `append`/`truncate`/`termAt`/`lastIndex`) via PR #24:
  `Log` allocates `entries_max` slots once at `init`, never grows; `append` returns
  `error.LogFull` at capacity (typed error) while monotonic-index and in-range-`termAt` are
  asserted caller preconditions. 11 new tests incl. a seeded append/truncate model test.
  `code-reviewer`: 0 CRITICAL, 3 WARNING (all fixed) — `termAt`'s doc didn't warn about
  range-checking peer-supplied indices first; no CHANGELOG entry; import placement. 7/7 CI
  green, squash-merged.
- Milestone issue #20: 6/11 items done.

## Cycle 18 — 2026-09-28 — FEATURE
- Item 5 (1A-ii `types.zig` — `Message` union and `ConfChange`) via PR #23: `architect` (opus)
  designed the wire shape — `Header` fronts every `Message`; PreVote gets its own tag;
  `AppendResponse` carries the §5.3 conflict hint; `Configuration`/`ConfChange` joint-consensus
  only, absolute. ADR-005. `code-reviewer` caught 1 CRITICAL: `validateAppendRequest`'s
  contiguity loop called `Index.next()` on an unranged peer-supplied index — a
  peer-triggerable panic, fixed with a range guard. 2 WARNINGs also fixed.
- Budget note (recurring, see cycle 12/17): a wire-format `architect` call alone can consume
  ~$0.85-1.20 of the $4 budget — PR #23 was pushed but not watched to merge this cycle;
  cycle 19's inbox merged it. Keep `architect` prompts pointed at specific files, and skip the
  call entirely when a plan bullet or an already-defined type's doc comment (as in cycle 20)
  fully specifies the contract.

## Cycle 17 — 2026-09-27 — FEATURE
- Item 4 (1A-i `types.zig` — scalars, `Entry`, `HardState`, `Snapshot`) via PR #22: `architect`
  (opus) designed `NodeId`/`Term`/`Index` as distinct non-exhaustive `enum(u64)` types (never
  `usize`, named zero sentinels), `HardState` (24-byte `extern struct`, no padding). ADR-004.
  Also fixed a tidy gap: `findWireDeclEnd` only matched bare `struct`/`union`, missing
  `extern`/`packed` — widened, 2 new tidy tests. ~30 new tests. 7/7 CI green.

## History (cycles 0-16)
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

Full per-cycle detail for cycles 0-16 (PR numbers, code-reviewer findings, the disk-gate abort)
lived here before this fold; see git history of this file if needed.
