# synod — debugging

_(migrated from the repo's former .claude/memory; keep under 200 lines)_

Format: `## <symptom>` / **Cause** / **Fix** / **How to detect next time**

Empty — the old `.claude/memory/debugging.md` had no entries (no real code existed yet to
produce tricky bugs). Add entries here as they're resolved during Phase 1 onward.

One tooling gotcha surfaced by the Zig 0.16 migration probe, worth knowing before that plan
lands: `zig build test` on 0.16 can report all tests passing even when `main()` itself would
fail to compile-and-run, because `zig test` never calls `main` and Zig's lazy top-level
analysis skips code that only `main` reaches. Verify 0.16 readiness with `zig build` (builds
the real executable) or `zig test src/main.zig`, not `zig build test` alone.
