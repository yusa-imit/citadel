# Docs policy

Repos hold code and documentation. They hold no AI configuration: no `CLAUDE.md`, no `.claude/`.
The kingdom's AI configuration lives in `citadel` and reaches every repo through the parent
directory (`/Users/fn/codespace/CLAUDE.md` → `citadel/core/KINGDOM.md`).

## Repository root (allowed files)

`README.md` `LICENSE` `CHANGELOG.md` `build.zig` `build.zig.zon` `.gitignore` `zr.toml`
`<name>.conf.example` `install.sh` `install.ps1`. Nothing else. Binaries, logs, databases,
object files, scratch `.zig` files, session notes, release notes, audits: never in root.

## `.github/`

`workflows/ci.yml` (and `release.yml`), `CONTRIBUTING.md`, `SECURITY.md`, issue and PR templates.

## `docs/`

| Path | Content | Changed by |
|---|---|---|
| `docs/PRD.md` | Requirements and architecture, living | PR (`docs:`), architect-reviewed |
| `docs/plans/NNN-<theme>.md` | Milestone plans, one per milestone, numbered | `plan` PR to create; implementation PRs tick boxes |
| `docs/plans/000-inherited.md` | The pre-kingdom roadmap, frozen | never (read-only history) |
| `docs/adr/NNNN-<title>.md` | Architecture decisions: Context · Decision · Consequences | PR, often with the code it justifies |
| `docs/guides/` | User-facing guides | PR |
| `docs/internals/` | Developer-facing design notes (Tiger Style: say why) | PR |
| `docs/releases/` | Archived release notes | frozen |

Not allowed anywhere in a repo: session logs, iteration summaries, audit reports, agent specs,
scratchpads, generated autodoc output, vendored source tarballs. Those belong in
`citadel/realms/<repo>/` (memory) or in GitHub issues, or are regenerated.

## Style

- Markdown wraps at 100 columns. Every line is a line spent: list the facts, then shorten.
- `README.md` states version, what exists, how to build, how to use, and links to `docs/`. It
  must not claim what the code does not do. STABILIZATION cycles diff it against reality.
- `CHANGELOG.md` follows Keep a Changelog; every release adds a section.
- Doc comments (`///`) are the library's contract. `//!` at the top of every file states purpose
  and invariants.

## Exception

A repo may carry `.claude/settings.json` only for a hook that `citadel/core/fleet-settings.json`
cannot express, and only after a plan names it. `.claude/rules/local.md` is allowed for build
quirks that are true only inside that repo. Nothing else.
