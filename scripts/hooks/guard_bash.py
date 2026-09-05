#!/usr/bin/env python3
"""PreToolUse guard for Bash in realm sessions. Exit 2 blocks the call (before permission rules).

Blocks: force pushes, pushes to main, git add -A/--all/., reset --hard, clean -f, history rewrites,
deleting wip/* or plan/* branches, merging PRs labeled plan/hold/needs-human, rm -rf of a repo root.
"""
import json
import re
import subprocess
import sys

data = json.load(sys.stdin)
cmd = (data.get("tool_input") or {}).get("command", "")
flat = " ".join(cmd.split())

RULES = [
    (r"\bgit\b[^|;&]*\bpush\b[^|;&]*(--force\b|--force-with-lease\b|\s-f\b|\s\+\S)", "force push is forbidden"),
    (r"\bgit\b[^|;&]*\bpush\b[^|;&]*(\bmain\b|HEAD:main|:main\b)", "pushing to main is forbidden; open a PR"),
    (r"\bgit\b[^|;&]*\badd\b[^|;&]*(\s-A\b|\s--all\b|\s\.(\s|$))", "git add -A / . is forbidden; add explicit paths"),
    (r"\bgit\b[^|;&]*\breset\b[^|;&]*--hard", "git reset --hard is forbidden"),
    (r"\bgit\b[^|;&]*\bclean\b[^|;&]*\s-[a-zA-Z]*f", "git clean -f is forbidden"),
    (r"\bgit\b[^|;&]*\b(filter-branch|filter-repo)\b", "history rewriting is forbidden"),
    (r"\bgit\b[^|;&]*\bbranch\b[^|;&]*\s-[dD]\b[^|;&]*\b(wip|plan)/", "wip/* and plan/* branches are never deleted by the AI"),
    (r"\bgit\b[^|;&]*\bpush\b[^|;&]*(--delete|:(wip|plan)/)", "wip/* and plan/* branches are never deleted by the AI"),
    (r"\brm\b[^|;&]*\s-[a-zA-Z]*r[a-zA-Z]*\s+(/Users/fn/codespace/[a-z]+/?|\.|\.\.|/|~)(\s|$)", "refusing to remove a repository root"),
]
for pat, why in RULES:
    if re.search(pat, flat):
        print(f"BLOCKED by kingdom guard: {why}. Command: {flat[:200]}", file=sys.stderr)
        sys.exit(2)

m = re.search(r"\bgh\s+pr\s+merge\s+(\d+)", flat)
if m:
    repo = re.search(r"-R\s+(\S+)|--repo\s+(\S+)", flat)
    args = ["gh", "pr", "view", m.group(1), "--json", "labels,isDraft,isCrossRepository,author"]
    if repo:
        args += ["-R", repo.group(1) or repo.group(2)]
    try:
        info = json.loads(subprocess.run(args, capture_output=True, text=True, timeout=20).stdout or "{}")
    except Exception as e:  # network failure: fail closed
        print(f"BLOCKED by kingdom guard: cannot inspect PR ({e})", file=sys.stderr)
        sys.exit(2)
    labels = {l["name"] for l in info.get("labels", [])}
    bad = labels & {"plan", "hold", "needs-human", "wip"}
    if bad or info.get("isDraft") or info.get("isCrossRepository"):
        print(f"BLOCKED by kingdom guard: PR is {sorted(bad) or 'draft/fork'}; only the human merges it", file=sys.stderr)
        sys.exit(2)
    if (info.get("author") or {}).get("login") not in ("yusa-imit",):
        print("BLOCKED by kingdom guard: PR author is not the kingdom account", file=sys.stderr)
        sys.exit(2)
sys.exit(0)
