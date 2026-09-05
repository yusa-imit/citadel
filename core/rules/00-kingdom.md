# Kingdom layering and dependencies

- Layers: foundation (sigil, sirocco, strata, synod) → libraries (zuda, sailor) → tooling (zr)
  → services (silica, zoltraak). Dependencies point down only.
- Foundation `build.zig.zon` has no `.dependencies`, and a foundation never depends on another
  foundation. Where two foundations must meet (synod needs a codec, a transport, a log store),
  the foundation defines a vtable interface and the *binary that composes them* (a service, or a
  tiny adapter package owned by the consumer) supplies the implementation. `src/adapters/` in a
  foundation may only contain adapters to Zig std.
- Consumers depend on kingdom libraries by release tag URL + hash. `git+…?ref=` is forbidden.
  Consumers converge on the newest tag; `/status` lists laggards.
- Precedence: `realms/<repo>/REALM.md` may override a `core/rules` rule for that repo only; the
  override must cite the rule and say why. Otherwise core rules win.
- zuda-first: general-purpose data structures and algorithms come from zuda; file a
  `feature-request` issue there (label `from:<repo>`) instead of writing a local copy. Domain
  structures (TUI cell buffers, DB pages) stay local.
- Upstream bugs in a kingdom dependency are fixed upstream via an issue and a PR there, never
  worked around locally.
- `io: std.Io` is injected. Foundation libraries never choose the `Io` implementation; the
  binary does at `main`.
