---
name: plan
description: Write the next milestone plan for a realm as docs/plans/NNN-<theme>.md and open the plan PR for human approval.
argument-hint: <realm> [theme]
---

Realm `$ARGUMENTS`. Only one open `plan` PR per realm; if one exists, stop. Also stop if the
newest `docs/plans/NNN-*.md` on `main` still has unchecked items — that plan is approved and
in progress (or needs its `milestone` issue opened by `/cycle`); do not write the next one.

1. Inputs: `/Users/fn/codespace/citadel/docs/ROADMAP.md` (prescribes `001` and cross-repo
   order), `/Users/fn/codespace/citadel/realms/<realm>/{REALM.md,STATE.md,memory/*.md}`, the
   repo's `docs/PRD.md`,
   `docs/plans/000-inherited.md` (unfinished inherited items), open `directive` issues, and
   the last closed `milestone` issue. Call `planner` (opus) with all of this.
2. Number: `NNN` = last existing plan number + 1 (`ls docs/plans`). Items touching a `wip/*`
   branch may finish or leave it; the AI never deletes a `wip/*` branch.
3. Write `docs/plans/NNN-<theme>.md` (≤ 120 lines, 100 columns) with sections:
   `# Plan NNN — <theme>` · Goal · Why now · Scope (checklist; each item ≤ one cycle; blockers
   noted as `blocked_by: <repo> vX.Y`) · Out of scope · Risks · Done when · Version impact
   (none | PATCH | MINOR | MAJOR, with reason).
4. Branch `plan/NNN-<theme>` from `main`; commit `docs: plan NNN — <theme>`; push;
   `gh pr create --label plan --assignee yusa-imit --title "plan NNN: <theme>" --body <summary +
   footer>`; body ends with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.
5. Record in `/Users/fn/codespace/citadel/realms/<realm>/memory/context.md`: "plan NNN
   proposed, PR #n, awaiting merge". Questions the plan raises go in an issue with `origin: ai`.
