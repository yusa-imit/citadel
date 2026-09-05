Plan (and optionally execute) a cross-repo integration: $ARGUMENTS  (e.g. "zoltraak sigil" — consumer first, foundation second)

1. Call `kingdom-architect` with the pair. Required output: what code in the consumer is replaced, the foundation API it maps onto, parity tests, rollback
2. Check the foundation's `docs/milestones.md` — if the required API is not implemented yet, stop and record the dependency in `docs/ROADMAP.md` instead
3. Update `docs/ROADMAP.md` with the plan (checkbox items)
4. If asked to execute: work inside the consumer repo (`../<consumer>`) following *its* CLAUDE.md, on a branch `feat/<foundation>-integration`, keeping the consumer's full test suite green
5. Report: plan location, branch, tests status
