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
4. For each consumer in `citadel/zr-repos.toml [deps]`: open issue `migration: <realm> vX.Y.Z`
   with label `from:<realm>` listing API changes (`gh label create from:<realm>` if missing).
5. Close the `milestone` issue with the release link. Update `citadel/docs/KINGDOM.md` table.
