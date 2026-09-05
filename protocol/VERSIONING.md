# Versioning

- Semantic versioning. Versions only go up. Check `build.zig.zon` and the latest `git tag`
  before every bump; a lower or skipped version is a stop.
- Release requires: milestone checklist complete, `zig build test` green on all CI targets,
  zero open `bug` issues, `CHANGELOG.md` section written, `build.zig.zon` bumped in the same PR.
- **PATCH**: fixes only. **MINOR**: a milestone with additive features. **MAJOR**: breaking
  public API, or a Zig toolchain major/minor bump that changes the public API (0.15 → 0.16 is a
  MAJOR for sailor and zuda because `std.Io` changes their signatures).
- Foundation repos stay `0.x` until two consumers depend on them; MINOR may break during `0.x`.
- Consumers pin foundation and library dependencies by tag URL + hash. `git+…?ref=main` is
  forbidden. One version of each dependency across the kingdom (`citadel/zr-repos.toml`).
- Tagging: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`, `gh release create` with the changelog
  section, then open `migration` issues on each consumer (`from:<repo>` label) listing the API
  changes they must absorb.
