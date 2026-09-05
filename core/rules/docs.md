# Documentation placement

Repos contain code and `docs/`; never `CLAUDE.md`, `.claude/` (exceptions need a plan), session
logs, audits, scratch files, release notes in root, generated docs, or vendored tarballs.
`docs/PRD.md` (design), `docs/plans/NNN-*.md` (milestones, via plan PR), `docs/adr/`,
`docs/guides/`, `docs/internals/`, `docs/releases/`. `CONTRIBUTING.md`/`SECURITY.md` under
`.github/`. README must not claim what the code does not do. 100-column markdown.
Full policy: `citadel/protocol/DOCS.md`.
