You are an autonomous developer. At the START of each cycle, determine your mode using the session counter.

## Mode Selection (MANDATORY FIRST STEP)
Read and increment the session counter to determine mode:
```bash
COUNTER_FILE=".claude/session-counter"
COUNTER=$(cat "$COUNTER_FILE" 2>/dev/null || echo 0)
COUNTER=$((COUNTER + 1))
echo "$COUNTER" > "$COUNTER_FILE"
if [ $((COUNTER % 5)) -eq 0 ]; then echo "STABILIZATION"; else echo "NORMAL"; fi
```
- If counter % 5 == 0 (every 5th execution): **STABILIZATION MODE**
- Otherwise: **FEATURE MODE**

---

## STABILIZATION MODE (every 5th execution)

Focus: ensuring existing features work correctly, CI green, bugs fixed.

### Priority Order (STRICT — follow top-down)

#### 1. Check GitHub Actions CI Status (ALWAYS FIRST)
```
gh run list --limit 5 --json status,conclusion,name,headBranch,createdAt
```
- If any run on `main` has FAILED: analyze the failure, fix the root cause, commit, push, and verify CI passes.
- Do NOT proceed to other tasks until CI is green.

#### 2. Check GitHub Issues
```
gh issue list --state open --limit 10
```
- Review open issues for bug reports, feature requests, or user feedback.
- If there are bug reports or issues that affect stability, prioritize fixing them.
- If an issue is resolved by your work, close it with `gh issue close <number> --comment "Fixed in <commit>"`.

#### 3. Test Coverage for Existing Features
- Read `src/` to identify all implemented modules.
- Check which modules have tests and which don't.
- Write tests for UNTESTED functions. Each test should cover:
  - Normal path
  - Error paths
  - Edge cases (empty, max, overflow)
  - Memory leak detection using `std.testing.allocator`
- Run `zig build test` to verify.
- Commit and push after each test batch.

#### 4. Bug Fixes & Edge Cases
- If tests reveal bugs, fix them immediately.
- For database code: verify B+Tree invariants, page checksum integrity, WAL consistency.
- Test with various page sizes (512, 4096, 65536).

#### 5. Fuzz Testing (if Phase 1 complete)
- Run existing fuzz tests if available.
- Add new fuzz tests for: page read/write, B+Tree insert/delete sequences, varint encoding.

---

## FEATURE MODE (other executions)

Focus: implementing Silica's database engine following `docs/PRD.md`.

### Priority Order (STRICT — follow dependency graph)

#### 0. CI & Issues Quick Check (max 2 minutes)
Run `gh run list --limit 3` and `gh issue list --state open --limit 5`.
- If CI is RED on main: switch to stabilization mode regardless of counter.
- If there are critical bug reports: fix them first.
- Otherwise: proceed to feature implementation.

#### 1. Read Current State
- Read `docs/PRD.md` for the full roadmap.
- Read `.claude/memory/project-context.md` for what's already done.
- Identify the NEXT uncompleted item following the dependency graph:

```
Bootstrap (if no build.zig):
  build.zig + build.zig.zon → src/main.zig skeleton

Phase 1 — Storage Foundation (Weeks 1-6):
  Milestone 1 — Page Manager & File Format:
    1A Utilities (CRC32C, varint) → no deps
    1B Page Manager (header, read/write, freelist) ← depends on 1A
    1C Basic test suite ← depends on 1B

  Milestone 2 — B+Tree & Buffer Pool:
    2A Buffer Pool (LRU, pin/unpin, dirty tracking) ← depends on 1B
    2B B+Tree (insert, delete, point lookup) ← depends on 1B, 2A
    2C Leaf splits and merges ← depends on 2B
    2D Range scan cursors ← depends on 2C
    2E Overflow pages ← depends on 2B
    2F B+Tree fuzz tests ← depends on 2B-2E

Phase 2 — SQL Layer (Weeks 7-14):
  Milestone 3 — Tokenizer & Parser:
    3A Tokenizer ← no deps on Phase 1 internals (can work with AST types)
    3B Parser (recursive descent → AST) ← depends on 3A
    3C DDL statements ← depends on 3B
    3D DML statements ← depends on 3B
    3E Parser error recovery ← depends on 3B

  Milestone 4 — Semantic Analysis & Execution:
    4A Schema catalog ← depends on 2B (B+Tree for schema storage)
    4B Name resolution & type checking ← depends on 3B, 4A
    4C Query planner (AST → logical → physical plan) ← depends on 4B
    4D Volcano executor (Scan, Filter, Project, Sort, Limit) ← depends on 4C, 2D
    4E WHERE clause with index selection ← depends on 4D
    4F JOIN execution ← depends on 4D
    4G Aggregates & GROUP BY ← depends on 4D

Phase 3 — Transactions & ACID (Weeks 15-20):
  Milestone 5 — WAL & Crash Recovery:
    5A WAL file format & frame writer ← depends on 1B
    5B Read-path WAL integration ← depends on 5A, 2A
    5C Checkpoint process ← depends on 5B
    5D Crash recovery tests ← depends on 5C

  Milestone 6 — Concurrency & Constraints:
    6A Single-writer / multi-reader locks ← depends on 5C
    6B Snapshot isolation ← depends on 6A
    6C UNIQUE constraint via index ← depends on 2B, 4B
    6D FOREIGN KEY basic support ← depends on 6C
    6E Savepoints ← depends on 5C

Phase 4 — Client-Server & Polish (Weeks 21-26):
  Milestone 7 — Wire Protocol & Server:
    7A Wire protocol ← depends on 4D
    7B TCP server ← depends on 7A
    7C Client library ← depends on 7B
    7D Authentication ← depends on 7B

  Milestone 8 — Production Readiness:
    8A EXPLAIN & PRAGMA ← depends on 4C
    8B Benchmark suite ← depends on Phase 1-3
    8C Fuzz campaign ← depends on Phase 1-3
    8D Documentation ← depends on Phase 1-3
    8E CI/CD pipeline polish ← depends on 8B
```

#### 2. Implement ONE Sub-item Per Cycle
- Pick the highest priority item whose dependencies are satisfied.
- Create the new files and modify existing files as needed.
- Write unit tests for ALL new public functions.
- Run `zig build test` to verify.
- Commit and push incrementally (per-file or per-module, not all at once).

#### 3. Bootstrap Notes (if project has no build.zig)
If `build.zig` does not exist, create the project skeleton FIRST:
1. Create `build.zig` with library target + test step
2. Create `build.zig.zon` with package metadata
3. Create `src/main.zig` with minimal entry point
4. Verify `zig build` and `zig build test` pass
5. Commit and push, then proceed to Phase 1 items.

#### 4. Phase-Specific Implementation Notes

**1A Utilities**: Create `src/util/checksum.zig` (CRC32C using Zig's std.hash.crc) and `src/util/varint.zig` (variable-length integer encode/decode). These are pure functions with no external deps.

**1B Page Manager**: Create `src/storage/page.zig`. Define page header struct, page types enum, file header (magic "SLCA", version, page_size, page_count, freelist_head). Implement readPage/writePage with checksum verification. Implement freelist as linked list of free pages.

**2A Buffer Pool**: Create `src/storage/buffer_pool.zig`. LRU cache with configurable capacity (default 2000 pages). Pin/unpin with reference counting. Dirty page tracking for write-back. Use page-aligned memory allocation.

**2B B+Tree**: Create `src/storage/btree.zig`. Implement insert, delete, point lookup. Use the buffer pool for page access. Variable-length keys stored with length prefix. Internal nodes: [key, child_page_num] pairs. Leaf nodes: [key, value] pairs with next_leaf pointer.

**3A Tokenizer**: Create `src/sql/tokenizer.zig`. Hand-written lexer. Token types: keywords (SELECT, INSERT, CREATE, etc.), identifiers, integer/float/string literals, operators, punctuation.

**3B Parser**: Create `src/sql/parser.zig` and `src/sql/ast.zig`. Recursive descent parser producing typed AST nodes. Start with simple SELECT, INSERT, CREATE TABLE.

#### 5. Update Memory After Implementation
- Update `.claude/memory/project-context.md` checklist with completed items.
- If you learned something important, update relevant memory files.
- If you discovered a new pattern, add it to `.claude/memory/patterns.md`.

---

## Mandatory Rules (BOTH MODES)
1. You MUST commit and push at least one meaningful change per cycle.
2. NEVER use EnterPlanMode or ExitPlanMode — plan internally then implement.
3. If you find yourself only reading files and writing summaries — STOP. Go implement something.
4. Run `zig build test` before every commit. Do not push broken code.
5. Use `git add <specific files>` — never `git add -A`.
6. Database correctness is paramount — never skip checksum verification or invariant checks.
7. Every B+Tree operation must have a corresponding test verifying the invariants.

## End of Cycle
1. Update `.claude/memory/` files with what you learned.
2. Commit memory updates: `chore: update session memory` and push.
3. Send Discord summary via: openclaw message send --channel discord --target user:264745080709971968 --message "<summary including mode (STABILIZATION/FEATURE) and what was done>"
