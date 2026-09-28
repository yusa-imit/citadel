# sailor — context

last_seen_at: 2026-09-28T01:14:07Z
rejected_plans: []

## Migration window

- 2026-09-28 (sailor-migration): errors (`$Z16 build test 2>&1 | grep -c 'error:'`) 696→207.
  Preserved a dirty non-migration tree (`test/arg-assertion-baseline`'s in-progress `arg.zig`
  assertion sweep) to `wip/arg-assertion-baseline-20260928` before starting; created
  `wip/zig-016-migration` from main (didn't exist yet), 4 checkpoint commits pushed. Landed:
  item 4 remainder (mem.indexOf*→find* 479 sites, ArrayList(T){}/ArrayListUnmanaged(T){}→.empty
  ~90 sites across 3 sweeps — same recurring under-match bug as cycles 8/14, grep for bare
  `= .{}` on an ArrayList-typed field only surfaces once an earlier error in the same struct
  literal clears, so expect more strays next run too); item 6 (wave 1) essentially done:
  fixedBufferStream→Io.Writer/Reader.fixed (352 sites via 4 parallel subagents, caught+fixed one
  real regression — a subagent's blind writer→&fbs regex corrupted 3 production fns in
  tui/style.zig, reverted), ArrayList.writer()→Io.Writer.Allocating (~155 sites via 4 more
  subagents, clean this time), AnyWriter/AnyReader→*std.Io.Writer/*Reader (term.zig, repl.zig,
  state_persist.zig, tui/error_recovery.zig — repl.zig's Highlighter/readLine/handleKey/
  printPrompt/redraw narrowed from anytype, 33 null_writer test sites→Writer.Discarding). Item 7
  (wave 2) started: filebrowser_test.zig's std.fs.cwd()-as-receiver test sites →
  Io.Dir.cwd()+std.testing.io (166 sites) but createTestDir()'s tmp_dir.makePath/createFile/
  file.close() method calls (not std.fs.cwd() call sites, so the sweep script didn't reach them)
  and the file→writer(io,buf) buffered-write construction are still broken — same gap will recur
  in session.zig/audit.zig/hotreload.zig/theme_loader.zig/docgen.zig test helpers, none touched
  yet. Not landed (no PR opened yet, stayed in draft-checkpoint mode per amendment step 5): items
  4's isatty/env-access remainder, all of items 8 (time/Thread.Mutex/error.Canceled — ~7 files,
  ~50 lock/unlock call sites, needs io: Io threaded through Pool/Progress/EventBus/AsyncLoop/
  DeveloperConsole's public APIs, a real cascading design change) and 9 (io: Io convention,
  blocked on 8). Key API findings for next run (verified against 0.16.0 std source): env access
  has no simple replacement — `std.process.Environ.Map` must be built once (from
  `process.Init.environ_map` at a binary's main, or `Environ.createMap(environ, gpa)`) and
  injected, there is no global getenv anymore, so env.zig's public functions need an `environ:
  *const Environ.Map`-shaped parameter (a sibling convention to `io: Io`, needs an architect
  decision, not yet made); `posix.isatty`→`Io.File.isTty(file, io) Io.Cancelable!bool` needs an
  `Io.File`, not a raw fd, so term.zig's `isatty(fd: anytype) bool` signature must change;
  `Io.Mutex.lock/unlock(io)` need io threaded to every caller. Branch `wip/zig-016-migration`
  pushed, not merged (not green yet). Next: architect pass on the env-access convention +
  isatty/File signature change, then the Thread.Mutex→Io.Mutex threading (biggest remaining
  single item), then finish wave 2's file-write pattern and roll it out to the other 4 test
  files, then time/Clock, then io:Io on the public API, then tests+CI+version pin.

## Cycle 17 — 2026-09-27 — FEATURE

- Done: preflight found repo on PR #37's branch, clean, pushed; merged it (10/10 green) before
  switching to main. CI green. Inbox: no new OWNER input on #34, no plan PR. Fixed stale
  milestone-19 bookkeeping: ticked the `wip/timeline-description-rendering` checkbox (it was
  actually finished/merged in cycle 3 as PR #22, box was never ticked) and commented explaining
  the stale `wip/timeline-description-rendering` branch stays undeleted per the kingdom
  contract's unconditional "never delete a wip/* branch" rule (overrides the plan's "remote
  branch deleted" verify line). Since items 4/6-10 stay blocked on #34 (still open, no new OWNER
  reply), picked item 11 ("assertion baseline on hot modules") as unblocked work — it needs no
  0.16 migration. Scoped to `term.zig` (first in module order, had zero asserts). test-writer
  pinned ~25 contract tests first; zig-developer added 43 asserts across `isatty`, `getSize`
  family, focus/paste predicates, `hexEncode`/`hexDecode`, xtgettcap query/response,
  `MockTerminal` — and fixed a latent gap where `getSizeWindows` had no bounds gate before
  returning raw console dimensions (now returns the existing `Error.TerminalSizeUnavailable`
  instead of asserting on OS-supplied data). `zig build test` green (348/348), `zig fmt`/tidy
  clean. Opened PR #38; CI pending at cycle deadline — left for next cycle's inbox, same
  recurring pattern as #21/#25/#26/#29/#30/#31/#32/#33/#35/#36/#37.
- PRs: #37 (merged), #38 (open, CI pending).
- Next: inbox merges #38 once green. Item 11 remaining files, in order: `arg.zig`,
  `tui/buffer.zig`, `tui/layout.zig`, `fmt.zig` — same test-writer-then-zig-developer pattern
  worked well for `term.zig`, reuse it. Milestone checkbox for item 11 stays unticked until all
  five files are done.
- Blockers: #34 still open (OWNER's 2026-09-18 reply about cron access answered a different
  framing; cycle 16 already flagged that granting the exception is outside the sailor realm's
  own edit scope and needs an operator). No new comment since.
- Open questions: #34 (unchanged).

## Cycle 16 — 2026-09-26 — FEATURE

- Done: preflight found repo on PR #36's branch, switched to main. CI green, no bugs. Merged
  PR #36 (10/10 green). Milestone #19 items still blocked on the toolchain switch; did one
  bounded stabilize task: proof-commented `src/tui/inspector.zig`'s 2 `catch unreachable`
  test-visitor sites (comment kept short so line stays <=100 cols), baseline 358->357. PR #37.
- PRs: #36 (merged), #37 (open, CI pending).
- Next: inbox merges #37 once green. Remaining candidates: `src/tui/async_loop.zig`
  (563,685,733,792,887; verify each callback's task always succeeds).
- Blockers: #34 got an OWNER reply 2026-09-18: "Access to cron, add exception for work from
  cleanup schedule. After work done, roll back exception from cleanup schedule." Needs operator
  action on cron (outside sailor realm; AI cannot edit it). Issue left open.
- Open questions: #34.

## Cycle 15 — 2026-09-17 — STABILIZATION

- Done: preflight found repo clean on main. GitHub truth: CI green on main @ `847ced6`, no bug
  issues, no plan PR, issue #34 (question+needs-human) still open with no new OWNER comment.
  Cycle 15 forced STABILIZATION via the periodic trigger (`15 % 5 == 0`). Inbox merged PR #35
  (10/10 green, CLEAN) completing the `ArrayList` `.empty` sweep. `tidy-auditor` fresh pass:
  zero baseline drift, every cycle-13 STATE.md count still accurate (359 tracked entries).
  Recommended `src/arg.zig:590` as the single smallest remaining unproven `catch unreachable`
  (test declares the flag `.type = .bool`, so `asBool()` can't hit `TypeMismatch`) — same
  provable pattern as `eventbus.zig`/`countdown_timer.zig`/`pipeline.zig` (#27/#29/#30). Fixed it
  myself: proof comment on the same line (tidy only exempts same-line `//`), regenerated
  `tidy_baseline.txt` (359→358, diff limited to the one expected line), `zig build test` green,
  `zig fmt --check` clean (one incidental pre-existing double-space fix from the repo's fmt hook,
  same side effect noted in #29/#30). Opened as PR #36; CI still pending at cycle deadline — left
  open for next cycle's inbox, same recurring pattern as #21/#25/#26/#29/#30/#31/#32/#33/#35.
  Updated STATE.md's Tiger Style table and next-target recommendation.
- PRs: #35 (merged), #36 (open, CI pending).
- Next: inbox should merge #36 once green. Next provable-proof-comment candidates:
  `src/tui/inspector.zig:941,966` (2 sites) and `src/tui/async_loop.zig:563,685,733,792,887`
  (5 sites, verify each test callback's task always succeeds first). Do NOT attempt
  `event_metrics.zig`/`render_metrics.zig` (4 sites) or `bench.zig` (5 sites, `Timer.start()` can
  legitimately fail) or `smart_autocomplete.zig` (2 sites) as mechanical proof comments — all
  genuinely not provable, need typed-error redesign instead.
- Blockers: #34 still open, awaiting OWNER decision on how to structure the Io migration session
  — no new comment this cycle, not yet eligible for AI auto-action (no `origin: ai` tag, only
  1 cycle old).
- Open questions: #34 (unchanged).

## Cycle 14 — 2026-09-16 — FEATURE

- Done: preflight found repo clean on PR #33's branch, switched to main. GitHub truth: CI green,
  no bug/question issues, no plan PR. Inbox merged PR #33 (10/10 green, `mergeStateStatus: CLEAN`)
  — closes the `//!` header sweep entirely. Milestone #19 items 4/6-10 (Io renames + both `std.Io`
  waves) re-checked with a fresh `zig test src/sailor.zig` probe on the 0.16.0 toolchain (347
  errors remain) — reconfirmed for the 7th cycle running that no partial rename can land without
  breaking the pinned 0.15.2 build (not a formal cross-repo blocker, just a hard
  atomicity/sequencing wall). Filed question+needs-human issue #34 asking the owner to pick: a
  longer continuous session, or explicit approval for a multi-cycle `wip/*` migration branch whose
  intermediate commits don't need to pass `zig build test`. The same probe surfaced that item 5
  ("`ArrayList` literal sweep", marked done by PR #28) was incomplete — PR #28's pattern only
  matched bare top-level `= .{}` and missed 65 nested-field-position sites across 34 files.
  Delegated the fix to a zig-developer subagent (see [[patterns]] "Caution on done mechanical
  sweeps"); verified the diff myself (exactly 34 files/65 lines, `zig build test` green, `zig fmt
  --check` unchanged, 0.16-probe count for these sites 65→0), opened as PR #35.
- PRs: #33 (merged), #35 (open, CI running at cycle deadline).
- Next: inbox merges #35 once green. Milestone items 4/6-10 stay off-limits for per-cycle
  implementation until issue #34 is answered or an alternative is picked; do not re-probe every
  cycle now that the finding is filed — check #34 for an OWNER reply instead. 3 new `ArrayList`
  sites surfaced deeper in the 0.16 compile graph once PR #35's sites cleared
  (`docgen.zig:288`, `event_metrics.zig:131`, `profiler.zig:115`) — small follow-up sweep, low
  priority next to #34's answer.
- Blockers: #34 open, awaiting OWNER decision on how to structure the Io migration session.
- Open questions: #34 (filed this cycle).

## Cycle 13 — 2026-09-15 — FEATURE

- Done: preflight found repo clean on PR #32's branch (`docs/module-headers-tui-core`), switched
  to main directly. GitHub truth: CI green on main, no bug/question/directive issues, no plan PR.
  Inbox merged PR #32 (10/10 checks green, `mergeStateStatus: CLEAN`) — squash, branch deleted,
  `auto-merged`. Milestone #19's blocked toolchain items (4/6/7) confirmed blocked for the 6th
  cycle running (6, 7, 9, 11, 12, 13) — not re-checking further per standing memory guidance.
  Fell back to bounded stabilize task: completed the `//!` header sweep's final slice,
  `src/tui/widgets/` (38 files), via a zig-developer subagent. Verified the diff directly
  (`git diff --stat`: exactly 38 `src/tui/widgets/*.zig` files + `tidy_baseline.txt`, 397→359
  tracked entries), spot-checked 4 header lines for content accuracy (not generic placeholders),
  ran `zig build test` myself (exit 0, green) and `zig fmt --check` (no new drift, byte-identical
  failing-file list). Opened as PR #33; CI still pending (cross-compile/benchmark jobs not yet
  started) at cycle deadline — left open for next cycle's inbox, same recurring pattern as
  #21/#25/#26/#29/#30/#31/#32. Updated STATE.md's Tiger Style table (`//!` header count 38→0,
  sweep complete once #33 merges).
- PRs: #32 (merged), #33 (open, CI pending).
- Next: inbox should merge #33 once green. This closes out the `//!` header sweep entirely — no
  more `missing_header` tidy entries will remain. Next stabilize target should be picked fresh
  from STATE.md's remaining gaps (52 files >800 lines, `while (true)` unbounded loops, function
  length, `assert(` density) — none are as mechanically simple as the header sweep was, so expect
  the next few stabilize cycles to need more per-site judgment.
- Blockers: #19 items 4/6/7 need a dedicated multi-cycle session pairing the Zig 0.16 toolchain
  switch with the `std.Io` rewrite — verified blocked 6 cycles running; do not re-check.
- Open questions: none.

## History (cycles 0-10, condensed 2026-09-17)

Cycle 12 (FEATURE, 2026-09-15): merged PR #31; `//!` header sweep of `src/tui/` core (35 files)
as PR #32. #19 items 4/6/7 blocked (toolchain switch + `std.Io` rewrite); do not re-check.

Cycle 11 (FEATURE, 2026-09-12): merged PR #30; added `//!` headers to 13 top-level `src/*.zig`
files as PR #31 (tidy baseline 446→433, cross-checked with a second binary).


Cycle 10 (STABILIZATION, 2026-09-12): merged PR #29. `tidy-auditor` found zero baseline drift.
Proof-commented `pipeline.zig`'s 2 `catch_unreachable` sites (progress formatters) as PR #30.

Cycle 9 (FEATURE, 2026-09-11): re-verified item 4's remainder still has no 0.15.2-compatible
spelling (direct stdlib read, same conclusion as cycles 6-8). Fell back to stabilize: proof-
commented `countdown_timer.zig`'s 3 `catch unreachable` sites as PR #29.

Cycle 8 (FEATURE, 2026-09-11): checked item 5 (`ArrayList` literal sweep) the same way cycle 6
found item 4's safe half — confirmed `.empty` is 0.15.2-compatible, mechanically replaced all 132
`= .{}` sites across 34 files as PR #28 (merged). See [[patterns]] for the reusable
"check for a 0.15.2-compatible spelling before assuming toolchain-blocked" pattern.

Cycle 7 (FEATURE, 2026-09-10): merged PR #26 (safe-half renames). Confirmed item 4's remainder
(`Io.Mutex`, env access, `posix.isatty`, `mem.indexOf*`→`find*`, ~500 sites) has zero
0.15.2-compatible spelling, unsafe to land blind. Proof-commented `eventbus.zig`'s 3 test-only
`catch unreachable` sites as PR #27.

## History (cycles 0-6, condensed 2026-09-12)

Cycle 6 (FEATURE, 2026-09-10): merged PR #25 (`crypto_random` tidy tracking). Read 0.15.2 and
0.16.0 stdlib directly and found item 4's six renames split cleanly: `GeneralPurposeAllocator`→
`DebugAllocator` and `linkLibC()`→`.link_libc = true` are safe under 0.15.2 now; `Io.Mutex`, env
access, `posix.isatty`, `mem.indexOf*`→`find*` (478 sites) have no 0.15.2-compatible spelling and
need the actual toolchain switch — this is the finding cycles 7/9/11 kept re-confirming. Landed
the safe half as PR #26 (left open for cycle 7's inbox); item 4 left unticked.

Cycle 5 (STABILIZATION, 2026-09-09): merged PR #24 (`@panic` tidy tracking, all 8 sites
proof-commented). `tidy-auditor` found zero baseline drift; added a new `crypto_random` tidy
check (mirroring `time_usage`) as PR #25, left open for next cycle.

Cycle 4 (STABILIZATION, 2026-09-08): CI red on `main` (flaky `avg_ns` perf assertion) forced
STABILIZATION; merged cycle 3's already-prepared fix PR #23, confirmed green. `tidy-auditor`
found `zig build tidy` passing cleanly (447 entries); flagged `@panic` (8, 2 files) as next
target.

Cycle 3 (FEATURE, 2026-09-07): fixed a Windows-only CRLF bug in the tidy step's
`countLongLines` (PR #21) — see [[debugging]] for the durable pattern. Rebased
`wip/timeline-description-rendering` onto main as PR #22, merged.

Cycle 2 (FEATURE, 2026-09-06): implemented plan 001 item 2, the `tidy` build step —
`build_support/tidy.zig` (line/function length, missing `//!` header, unproven
`catch unreachable`, `std.debug.print`/`std.time.*`, `usize` in wire formats; 30 TDD tests) plus
`build_support/tidy_main.zig` CLI, wired into `zig build test`; generated `tidy_baseline.txt`
(447 entries) as the starting ratchet. PR #21 opened (merged next cycle after a Windows-only
CRLF fix — see [[debugging]]).

Cycle 0 (RESTRUCTURE, 2026-09-05): realm created; memory migrated from the repo's former
`.claude/memory/`; plan `001` prescribed (Zig 0.16 migration, MAJOR → v3.0.0, 368 probe errors +
`linkLibC`). `wip/timeline-description-rendering` preserved mid-cycle TDD work (finished as PR
#22 in cycle 3). Standing backlog carried forward, still partly open: the v2.100.0
"Widget Doc-Comment Audit Round 3" milestone has `terminal.zig` (`AnsiParseState` wiring),
`pager.zig` (soft-wrap), `metrics_dashboard.zig`/`richtext.zig` (scope decisions), and
`paragraph.zig` (word/char wrap + RTL/bidi, architect pass, do last) still unaddressed —
separate from plan `001`/milestone #19, not yet resumed. Repo hygiene backlog (stale
`README.md`/`docs/PRD.md`, 52 files >800 lines) also still open, tracked in STATE.md.

Cycle 1 (FEATURE, 2026-09-05): plan `001` merged as #18; opened tracking issue #19 (12-item
checklist). Implemented item 1 (hygiene leftovers) as PR #20, merged.
