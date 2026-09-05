# Testing rules

- TDD: a failing test precedes every implementation and every bug fix (regression test).
- Every declared error variant is provoked by a test. Test valid data, invalid data, and valid
  data becoming invalid. Boundaries: empty, one, max, max+1.
- `std.testing.allocator` everywhere; `std.testing.io` for I/O on 0.16; temp dirs cleaned.
- Stateful structures ship `check_invariants()`; tests and fuzzers call it after every mutation.
- Model-based seeded tests are the library form of simulation testing: same op stream into the
  structure and a trivial reference, compare after each step, inject faults through seams
  (failing allocator, short reads, torn writes). Reproduce from `(seed, commit)`.
- One construction path: tests build components through `testing/fixtures.zig`.
- Local: `zig build test`. CI only: cross-compile matrix, benchmarks, fuzz campaigns
  (STABILIZATION may run them when no other Zig build is active).
- Forbidden tests: `expect(true)`, copied expected values, assertion-free, "does not crash" only.
