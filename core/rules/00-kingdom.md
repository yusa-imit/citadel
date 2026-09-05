# Kingdom layering and dependencies

- Layers: foundation (sigil, sirocco, strata, synod) → libraries (zuda, sailor) → tooling (zr)
  → services (silica, zoltraak). Dependencies point down only.
- Foundation `build.zig.zon` has no `.dependencies`. Kingdom integrations are opt-in adapters
  under `src/adapters/` of the foundation or inside the consumer.
- Consumers depend on kingdom libraries by release tag URL + hash. `git+…?ref=` is forbidden.
  One version of each dependency kingdom-wide (`citadel/zr-repos.toml [deps]`).
- zuda-first: general-purpose data structures and algorithms come from zuda; file a
  `feature-request` issue there (label `from:<repo>`) instead of writing a local copy. Domain
  structures (TUI cell buffers, DB pages) stay local.
- Upstream bugs in a kingdom dependency are fixed upstream via an issue and a PR there, never
  worked around locally.
- `io: std.Io` is injected. Foundation libraries never choose the `Io` implementation; the
  binary does at `main`.
