---
name: inbox
description: Triage GitHub state for a realm — dirty tree, bug issues, red CI, plan PR comments, question answers, directives, holds. Each item becomes a PR or a comment.
argument-hint: <realm>
---

Realm `$ARGUMENTS`. Repo `/Users/fn/codespace/$ARGUMENTS`. Follow `citadel/protocol/GITHUB.md`.

0. Dirty tree: `git status --short`. If anything is modified: `git checkout -b wip/<slug>`,
   add the modified files explicitly, commit `wip: <what>`, push, `git checkout main`. Record in
   `memory/context.md`. Never discard.
1. `bug` issues (`gh issue list --label bug`): for each, `/implement $ARGUMENTS fix #<n>` with a
   regression test first. Close the issue from the PR body (`Fixes #n`).
2. Red CI on main: `gh run view <id> --log-failed`; fix via PR (`ci:`/`fix:`).
3. Open `plan` PR (`gh pr list --label plan`): read unresolved review comments
   (`gh api repos/yusa-imit/$ARGUMENTS/pulls/<n>/comments` and issue comments). For each: revise
   `docs/plans/NNN-*.md` on the plan branch, push, reply quoting the change. If the human closed
   the plan PR since last cycle, record the reason and note that a new plan is needed.
4. `question` issues with new human comments: record the answer in `memory/decisions.md` (and
   `docs/adr/` via PR if architectural), reply "Recorded", close.
5. `directive` issues: if doable in one cycle, do it via PR and close with the PR link; else
   add it to the next plan's scope and comment saying so.
6. Open implementation PRs: if CI green and no `hold` → merge (squash), label `auto-merged`.
   If red → fix on branch (max 2 attempts) else label `needs-human` + comment.

Output exactly: `plan_pr_open: yes|no`, `milestone_issue: <number>|none`, and a bullet list of
actions taken.
