---
name: plan
description: Write the next milestone plan for a realm as docs/plans/NNN-<theme>.md and open the plan PR for human approval.
argument-hint: <realm> [theme]
---

Realm `$ARGUMENTS`. Only one open `plan` PR per realm; if one exists, stop.

1. Inputs: `citadel/docs/ROADMAP.md` (prescribes `001` and cross-repo order),
   `citadel/realms/<realm>/{REALM.md,STATE.md,memory/*.md}`, the repo's `docs/PRD.md`,
   `docs/plans/000-inherited.md` (unfinished inherited items), open `directive` issues, and
   the last closed `milestone` issue. Call `planner` (opus) with all of this.
2. Number: `NNN` = last existing plan number + 1 (`ls docs/plans`).
3. Write `docs/plans/NNN-<theme>.md` (≤ 120 lines, 100 columns) with sections:
   `# Plan NNN — <theme>` · Goal · Why now · Scope (checklist; each item ≤ one cycle; blockers
   noted as `blocked_by: <repo> vX.Y`) · Out of scope · Risks · Done when · Version impact
   (none | PATCH | MINOR | MAJOR, with reason).
4. Branch `plan/NNN-<theme>` from `main`; commit `docs: plan NNN — <theme>`; push;
   `gh pr create --label plan --assignee yusa-imit --title "plan NNN: <theme>" --body <summary +
   footer>`; body ends with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.
5. Record in `memory/context.md`: "plan NNN proposed, PR #n, awaiting merge".
