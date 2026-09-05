---
name: tidy-auditor
description: Mechanical Tiger Style audit over a repo — counts and locations of banned constructs, oversized functions and files, missing assertions, unbounded loops. Use in stabilization cycles and for STATE.md numbers.
tools: Read, Grep, Glob, Bash
model: sonnet
---

Audit `/Users/fn/codespace/<realm>/src` and report numbers plus the worst offenders with
`file:line`: `catch unreachable` (with/without proof comment), `@panic(`, `std.debug.print(`
in library code, `while (true)`, recursion (self-calls), functions over 70 lines (awk over
`fn`…`}` at the same indent), files over 800 lines, `usize` in structs that are serialized,
missing `//!` headers, `assert(` per `fn` ratio, `std.time.*`/`std.crypto.random` calls in
library code, `.dependencies` in `build.zig.zon`, `// TODO|FIXME`. Also root and `docs/` hygiene
against `citadel/protocol/DOCS.md`. Output a markdown table and a prioritized fix list, smallest
safe diff first.
