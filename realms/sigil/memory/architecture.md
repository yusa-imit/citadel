# sigil — architecture

_(migrated from the repo's former `.claude/memory/architecture.md`, condensed)_

See `docs/PRD.md` §4 for the intended layering. Record here only what **diverges from** or
**refines** the PRD as modules actually land — as of 2026-09-05 nothing has landed yet
(pure stub scaffold, see `STATE.md`), so all three sections below are still empty in
substance; they are kept as the place to fill in once Phase 1 starts.

## Layering (as built)

_(empty — update as modules land; PRD §4 is the only source until then)_

## Interfaces

_(empty — record vtable definitions, ownership rules, lifetime contracts here once core/
and reflect/ exist. Known lifetime rule to document immediately once written: reflection
result slices are tied to the owning `ValueTree`'s lifetime — see `REALM.md`
Realm-specific rules.)_

## Formats

_(empty — record file/wire format version numbers and bump rules here once a format
module ships something byte-stable, e.g. MessagePack/CBOR encoding options.)_

## Module layout (reference only)

The full planned submodule breakdown (e.g. `core/{value,tree,number,timestamp,
diagnostics,unicode}.zig`, `json/{scanner,dom,writer,reflect}.zig`, etc.) lives in
`REALM.md`'s Layout table and the repo's own `README.md`. It is reference-only and may
change during implementation — update both this file and `REALM.md` when it does.
