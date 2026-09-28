sailor-migration: the Zig 0.16.0 migration window for sailor — plan 001, milestone #19 items 4,
6, 7, 8, 9, 10. TEMPORARY job, OWNER-approved in sailor#34; the operator removes it once #34 is
closed. The system prompt's SAILOR-MIGRATION AMENDMENT says which contract rules change here.

Z16=/Users/fn/.zr/toolchains/zig/0.16.0/zig (use it for every build and fmt on the migration
branch; the global `zig` stays 0.15.2 for the regular cycle). The job is killed at 3h: note the
start time with `date`, start no new step after 2h30m, and spend the rest on steps 5 and 6.

0. Expiry. If `gh issue view 34 -R yusa-imit/sailor --json state --jq .state` prints CLOSED, or
   `git -C /Users/fn/codespace/sailor show origin/main:build.zig.zon` already carries
   `.minimum_zig_version = "0.16.0"`, the window is over. Send `openclaw message send --channel
   discord --target user:264745080709971968 --message "[sailor-migration] window over; operator:
   remove the TEMP(sailor#34) entries in citadel/workflows"` and stop. Change nothing else.
1. Preflight in /Users/fn/codespace/sailor. Preserve a dirty tree or a non-main checkout exactly
   as protocol/CYCLE.md step 0.3 says, then `git switch main && git pull --ff-only`. Switch to
   `wip/zig-016-migration` (create it from main and `git push -u origin wip/zig-016-migration` if
   it does not exist), then `git merge --no-edit origin/main` so the regular cycle's work flows
   in. Merge, never rebase. Resolve a conflict by keeping main's intent in the 0.16 spelling.
2. Orient. Read citadel/realms/sailor/REALM.md, memory/context.md (its `## Migration window`
   section is this job's log), docs/plans/001-zig-0.16-and-tiger-baseline.md,
   citadel/core/rules/zig-0.16.md, and the /migrate-zig skill. Record the probe error count:
   `$Z16 build test 2>&1 | grep -c 'error:'` (`$Z16 test src/sailor.zig` while build.zig itself
   does not compile). The compiler stops each unit at its first error, so the count can rise as
   earlier walls fall.
3. Migrate in plan order: build.zig fix + mechanical renames → std.Io wave 1 (buffer sinks) →
   wave 2 (real I/O) → time, threads, error.Canceled → `io: Io` on the public API → tests,
   `.minimum_zig_version = "0.16.0"`, ci.yml on `mlugg/setup-zig@v2` with no hardcoded version.
   Each plan item's *Verify* line is its exit test. Do not bump `.version` and do not tag:
   v3.0.0 also needs items 11 and 12, which stay with the regular cycle.
   - Behaviour changes (new `io` parameters, `error.Canceled` prongs) get a failing test first;
     pure renames need no new test, the compiler is the test.
   - Use `zig-developer`, `test-writer` and `code-reviewer` subagents on disjoint file sets,
     at most 4 at once, one heavy build at a time. Never run the cross-compile matrix locally.
4. Checkpoint. Commit each logical step with explicit paths and a Conventional Commit message,
   and push the branch after every commit so a timeout never loses work.
5. Land, once `$Z16 build test` is green and `$Z16 fmt --check src build.zig` is clean. Tick
   items 4 and 6-10 in docs/plans/001-zig-0.16-and-tiger-baseline.md on the branch, then open ONE
   PR from `wip/zig-016-migration` to main, titled `feat!: migrate to Zig 0.16.0 (plan 001 items
   4, 6-10)`, body linking #19 and #34. Merge it yourself (squash, keep the branch) once every CI
   job is green and no `hold` label is present. If CI is red, fix it on the branch this run or
   the next. After the merge: tick the same items in #19, set REALM.md's Zig row to 0.16.0,
   comment on #34 that the migration merged, close #34, and send the step 0 Discord line.
6. Report, every run. Update the `## Migration window` section of
   citadel/realms/sailor/memory/context.md (create it under the file header if absent): date,
   error count before → after, what landed, next step, blockers. Keep it under 15 lines and fold
   older runs into one line; the file stays under 200 lines. Commit it with
   `python3 /Users/fn/codespace/citadel/scripts/hooks/citadel_commit.py sailor <n>`, where `<n>`
   is the unchanged value of memory/counter. Post one progress comment on #34 (errors before →
   after, commits, next step). Send `openclaw message send --channel discord --target
   user:264745080709971968 --message "[sailor-migration] errors <before>→<after> | <branch/PR
   state> | next: <step>"`. End on a clean tree with `git switch main`, so the regular cycle
   starts from main.
