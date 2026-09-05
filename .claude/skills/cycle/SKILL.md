---
name: cycle
description: Run one autonomous development cycle for a kingdom realm (preflight, inbox, plan or implement or stabilize, report). Use at the start of every unattended session.
argument-hint: <realm>
disable-model-invocation: true
---

Run one cycle for realm `$ARGUMENTS` following `citadel/protocol/CYCLE.md` exactly.

Paths: realm repo `/Users/fn/codespace/$ARGUMENTS`, realm dir
`/Users/fn/codespace/citadel/realms/$ARGUMENTS`, citadel `/Users/fn/codespace/citadel`.

## 0 · Preflight
1. Read `realms/$ARGUMENTS/REALM.md`, `STATE.md`, `memory/context.md`, `citadel/docs/ROADMAP.md`.
2. Counter: `n=$(($(cat memory/counter 2>/dev/null || echo 0)+1)); echo $n > memory/counter`.
   Mode = STABILIZATION if `n % 5 == 0`, else FEATURE. Print `CYCLE $n MODE <mode>`.
3. In the repo: `git fetch --prune && git checkout main && git pull --ff-only`. If the tree is
   dirty, `/inbox` step 0 applies (preserve on `wip/<slug>`).
4. Collect: `gh run list --limit 3 --json conclusion,headBranch,name`,
   `gh pr list --json number,title,labels,headRefName`,
   `gh issue list --json number,title,labels --limit 30`.
   Red CI or any `bug` issue → mode becomes STABILIZATION.

## 1 · Inbox
Run `/inbox $ARGUMENTS`. It returns `plan_pr_open: yes|no`, `milestone_issue: <n>|none`.

## 2 · Mode
- FEATURE and plan PR open → skip to report.
- FEATURE and no milestone issue → look at the newest `docs/plans/NNN-*.md` on `main`. If it
  has unchecked items, the human has approved it by merging: open the tracking issue now
  (`gh issue create --label milestone --title "milestone: NNN <theme>" --body "<the checklist>"`),
  record it in memory, and continue to the implement branch below in this same cycle.
  Only if every existing plan is fully checked → `/plan $ARGUMENTS` → report.
- FEATURE with a milestone → find the first unchecked item whose blockers are clear
  (`REALM.md` `blocked_by`, `ROADMAP.md`) → `/implement $ARGUMENTS <item>` → if the checklist
  is now complete and the plan declares version impact → `/release $ARGUMENTS`.
  If every remaining item is blocked → say so in the report; do one stabilization task instead.
- STABILIZATION → `/stabilize $ARGUMENTS`.

## 3 · Report
Run `/report $ARGUMENTS <mode> <summary>`. Then kill any process you started.

Rules: one item per cycle; never push to main; never wait for a human; subagents ≤ 4
(`opus` = architect/planner, `sonnet` = developer/test-writer/reviewer, `haiku` = git/ci).
