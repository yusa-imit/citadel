---
name: implement
description: Implement one milestone item or bug fix for a realm with TDD, open the PR, wait for CI, merge when green, tick the checklist.
argument-hint: <realm> <item or "fix #n">
---

Realm and item from `$ARGUMENTS`. Repo `/Users/fn/codespace/<realm>`.

1. Branch `feat|fix|refactor|test|docs/<slug>` from fresh `main`.
2. Design note (text): files, public API, error set, assertions to add, limits, tests.
   Interface, on-disk or wire format change → call `architect` (opus) first and add an ADR.
3. Red: `test-writer` (sonnet) writes failing tests from the contract, including negative
   space and every new error variant. Confirm they fail.
4. Green: `zig-developer` (sonnet) implements the minimum. Tiger Style applies
   (`citadel/core/rules/tiger-style.md`): ≥ 2 assertions per function, bounded loops, no
   allocation after init in hot paths, 70-line functions, exhaustive error switches.
5. Refactor with tests green. `zig fmt`. `zig build test`.
6. `code-reviewer` (sonnet). Fix CRITICAL and WARNING.
7. Tick the item in `docs/plans/NNN-*.md` in the same branch. Update `CHANGELOG.md`
   `[Unreleased]`.
8. Commit with explicit paths and a message that says why. Push.
   `gh pr create --title "<type>: <subject>" --body "<what/why> · Plan NNN item k · Refs #<issue>
   · footer"`.
9. `gh pr checks <n> --watch --interval 30` (bounded: give up after 25 minutes and leave the PR
   open with a comment). Green and no `hold` → `gh pr merge <n> --squash --delete-branch`,
   `gh pr edit <n> --add-label auto-merged`. Red → fix on branch, max 2 attempts, then
   `needs-human`.
10. Tick the checklist in the tracking issue body (`gh issue edit`), comment one line.
