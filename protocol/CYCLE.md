# The cycle

One cron run = one cycle = one realm. The `/cycle` skill drives it. Cycles are short (≤ 30 min),
idempotent, and safe to interrupt: every step commits or records before moving on.

## 0 · Preflight (≤ 2 min)

1. `realm` comes from the prompt. Read `citadel/realms/<realm>/REALM.md`, `STATE.md`,
   `memory/context.md`, then `docs/ROADMAP.md` (kingdom) for blockers.
2. Counter: increment `citadel/realms/<realm>/memory/counter`. `counter % 5 == 0` →
   STABILIZATION, else FEATURE. Red CI or open `bug` issues force STABILIZATION regardless.
3. `git -C <repo> fetch --prune`; `git status` must be clean on `main`. If dirty: commit the
   work to `wip/<slug>`, push, return to `main`, note it in memory. Never discard.
4. `gh run list --limit 3` (CI), `gh pr list`, `gh issue list` — build the inbox.

## 1 · Inbox (always)

Handle in this order, each as its own PR or comment:
1. `bug` issues → reproduce with a failing test → fix → PR → merge when green.
2. Red CI on `main` → fix → PR.
3. Comments on the open `plan` PR → revise the plan file, push, reply per comment.
4. Answers on `question` issues → record in memory (and `docs/adr/` if architectural), close.
5. `directive` issues → do what they say if it fits one cycle; else fold into the next plan.
6. `hold` labels are respected; PRs with `needs-human` are left alone.

## 2 · Mode

### FEATURE
- If an open `plan` PR exists → stop after the inbox (report only).
- If no `milestone` issue is open → write the next plan (`/plan`) and open the PR. Stop.
- Else pick the **first unchecked item** of the milestone checklist whose blockers are cleared
  (`ROADMAP.md`, `REALM.md: blocked_by`). Run `/implement <item>`: TDD → PR → CI → merge →
  tick the checklist in the tracking issue and in `docs/plans/NNN-*.md` (same PR).
- If the item is too large for a cycle, split it in the plan file (same PR as the slice).
- When every item is checked → `/release` if the plan has version impact → close the issue.

### STABILIZATION
- `/stabilize`: CI matrix, test-quality audit (test-writer), Tiger Style audit sweep
  (`tidy` findings: assertions, bounded loops, `catch unreachable`, file/function size),
  benchmark drift, dependency pins, docs drift (README vs reality). Each fix is a PR.
- Update `STATE.md` with fresh numbers.

## 3 · Report (always, even after an early stop)

1. `memory/context.md`: session number, mode, what happened, next priority, open questions.
   Other memory files as needed; keep each under 200 lines.
2. Commit citadel (`chore(<realm>): cycle <n> memory`) and push citadel.
3. Comment on the tracking issue or plan PR; Discord summary.
4. Kill any process this cycle started (servers, watchers); free ports.

## Budget and tools

- Subagents: ≤ 4 concurrent; `opus` for `architect`/`planner`, `sonnet` for the rest,
  `haiku` for `git-manager`/`ci-cd`.
- Local runs: `zig build`, `zig build test`, `zig fmt`. Cross-compile, benchmarks, fuzz
  campaigns: CI only, except in STABILIZATION when no other Zig build is running
  (`pgrep -f "zig build"`).
- One item per cycle. Reading and summarizing without a PR or a recorded decision is a failed
  cycle unless the inbox was empty and the plan PR is awaiting the human.
