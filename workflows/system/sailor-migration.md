SAILOR-MIGRATION AMENDMENT (TEMPORARY; OWNER-approved in yusa-imit/sailor#34 and
yusa-imit/citadel#15). It applies to the `sailor-migration` job only and overrides the kingdom
contract above where the two conflict:
A. Rule 1: this job does not run /cycle. It runs the migration procedure in its prompt, and its
   timeout is 3 hours instead of 25 minutes.
B. Rule 4: bugs and red CI on main stay with the regular sailor-cycle. This job fixes only the CI
   of its own migration PR.
C. Rule 6: checkpoint commits on `wip/zig-016-migration` may fail `zig build test`, because the
   0.15.2 → 0.16.0 switch has no incremental green path. The PR from that branch reaches main
   only when `zig build test` and `zig fmt --check` pass under Zig 0.16.0 and every CI job is
   green. Commits on any other branch keep rule 6 in full.
D. Rule 8: report in the `## Migration window` section of memory/context.md, not as a cycle.
   Never change `memory/counter`.
Every other rule stands, including rules 2, 3, 5 and 7.
