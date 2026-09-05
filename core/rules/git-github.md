# Git and GitHub

- `main` is protected by protocol, not by GitHub: every change is a PR; the AI merges
  implementation PRs after CI is green; humans merge `plan` PRs. See `citadel/protocol/GITHUB.md`.
- Branch names: `plan/NNN-<theme>`, `feat/<slug>`, `fix/<slug>`, `refactor/<slug>`,
  `test/<slug>`, `docs/<slug>`, `chore/<slug>`, `wip/<slug>` (preserved interrupted work).
- Commits: Conventional Commits, imperative subject ≤ 72 chars, body says why; trailer
  `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`. Explicit paths only.
- Never: `git add -A`, `--force`, `reset --hard` on shared branches, history rewrites, deleting
  branches you did not create this cycle, pushing to `main`.
- Labels with meaning: `plan`, `milestone`, `bug`, `directive`, `question`, `needs-human`,
  `hold`, `auto-merged`, `wip`, `from:<repo>`.
- PR body footer: `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.
