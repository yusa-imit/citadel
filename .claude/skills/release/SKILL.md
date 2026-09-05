---
name: release
description: Release a realm after a milestone completes — version bump, CHANGELOG, tag, GitHub release, consumer migration issues.
argument-hint: <realm> <major|minor|patch>
---

Follow `citadel/protocol/VERSIONING.md`. Abort loudly on any failed gate.
1. Gates: milestone checklist complete; `zig build test` green; CI green on main; zero open
   `bug` issues; `git tag -l 'v*' --sort=-v:refname | head -1` < new version; `build.zig.zon`
   version < new version.
2. PR `chore: release vX.Y.Z`: bump `build.zig.zon`, move `CHANGELOG.md` `[Unreleased]` into
   `## [X.Y.Z] - YYYY-MM-DD`. Merge when green.
3. `git tag -a vX.Y.Z -m "Release vX.Y.Z"`, `git push origin vX.Y.Z`,
   `gh release create vX.Y.Z --title vX.Y.Z --notes-file <changelog section>`.
4. Consumers = repos whose `build.zig.zon` `.dependencies` actually names this realm (grep the
   nine sibling repos), intersected with `citadel/zr-repos.toml [deps]`. For each, open ONE issue
   `migration: <realm> vX.Y.Z` (label `from:<realm>`, create the label if missing) unless an open
   one already exists for that consumer; list the API changes from CHANGELOG.
5. Close the `milestone` issue with the release link. Update `citadel/docs/KINGDOM.md` table.
