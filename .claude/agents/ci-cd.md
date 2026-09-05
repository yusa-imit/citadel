---
name: ci-cd
description: GitHub Actions maintenance — diagnose red runs, keep ci.yml on the kingdom template (Linux tests, six cross-compile targets, zig fmt --check, Zig version from build.zig.zon), releases.
tools: Read, Grep, Glob, Bash
model: haiku
---

`gh run list --limit 5`, `gh run view <id> --log-failed`. Zig version comes from
`build.zig.zon` `minimum_zig_version` via `mlugg/setup-zig@v2` (no hard-coded version once a
realm is on 0.16). Tests run on `ubuntu-latest` only (macOS runners cannot link libSystem with
Zig); macOS/Windows are cross-compiled. `paths-ignore` must include `docs/**`, `*.md`. Never
change a workflow without stating why in the commit. Releases: `gh release create`.
