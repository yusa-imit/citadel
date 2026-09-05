---
name: implement
description: Implement one milestone item or bug fix for a realm with TDD, open the PR, wait for CI within the cycle deadline, merge when green, tick the checklist.
argument-hint: <realm> <item or "fix #n">
---

Realm and item from `$ARGUMENTS`. Repo `/Users/fn/codespace/<realm>`. Respect the cycle deadline
set in `/cycle` step 0.1: stop waiting at START+22 min and report instead.

1. Branch `feat|fix|refactor|test|docs/<slug>` from fresh `main`.
2. Design note (text): files, public API, error set, assertions to add, limits, tests.
   Interface, on-disk or wire format change → call `architect` (opus) first and add an ADR.
3. Red: `test-writer` (sonnet) writes failing tests from the contract, including negative
   space and every new error variant. Confirm they fail.
4. Green: `zig-developer` (sonnet) implements the minimum. Tiger Style applies
   (`/Users/fn/codespace/citadel/core/rules/tiger-style.md`).
5. Refactor with tests green. `zig fmt`. Tests: use the realm's `test_command` from `REALM.md`
   when the full suite exceeds 5 minutes (targeted `--test-filter`); CI runs the full suite.
6. `code-reviewer` (sonnet). Fix CRITICAL and WARNING.
7. Tick the item in `docs/plans/NNN-*.md` in the same branch. Update `CHANGELOG.md`
   `[Unreleased]`.
8. Commit with explicit paths and a message that says why. Push.
   `gh pr create --title "<type>: <subject>" --body "<what/why> · Plan NNN item k · Refs #<issue>
   · footer"`.
9. `gh pr checks <n> --watch --interval 30` capped at `min(8 min, deadline − now)`. Green and no
   `hold` → `gh pr merge <n> --squash --delete-branch`, label `auto-merged`, tick the checklist in
   the tracking issue. Not green in time → comment "awaiting CI; merge next cycle" and let the
   next cycle's inbox merge it. Red → fix on branch (max 2 attempts) then `needs-human`.
