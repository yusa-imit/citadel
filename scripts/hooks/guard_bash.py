#!/usr/bin/env python3
"""PreToolUse guard for Bash in kingdom sessions. Exit 2 blocks the call (before permission rules).

Blocks: force pushes; pushes that would land on main (explicit refspec, or a bare push while HEAD is
main); git add -A/--all/.; reset --hard; clean -f; history rewrites; deleting wip/* or plan/*
branches; merging PRs that are plan/hold/needs-human/wip/draft/fork/foreign; rm -rf of a workspace
root; shell writes into citadel outside the session's own realm or into another repo; jobs.py
apply/prune from a governed session. This is a text matcher, not a policy engine — the GitHub
ruleset on main is the server-side backstop.
"""
import json
import os
import re
import subprocess
import sys

data = json.load(sys.stdin)
cmd = (data.get("tool_input") or {}).get("command", "") or ""
cwd = os.path.realpath(data.get("cwd") or os.getcwd())
flat = " ".join(cmd.split())
CODESPACE = "/Users/fn/codespace"
CITADEL = f"{CODESPACE}/citadel"
HOME = os.path.expanduser("~")


def block(why):
    print(f"BLOCKED by kingdom guard: {why}. Command: {flat[:200]}", file=sys.stderr)
    sys.exit(2)


def realm_of(path):
    path = os.path.realpath(path)
    if not path.startswith(CODESPACE + "/"):
        return None
    return path[len(CODESPACE) + 1:].split("/")[0] or None


realm = realm_of(cwd)  # None outside the workspace; 'citadel' for operator sessions

# ── git ────────────────────────────────────────────────────────────────────────
GIT = r"\bgit\b(?:\s+-C\s+\S+)?[^|;&]*?"
if re.search(GIT + r"\bpush\b[^|;&]*(\s--force\b|\s--force-with-lease\b|\s-f\b|\s\+\S)", flat):
    block("force push is forbidden")
# explicit refspec whose destination is main
if re.search(GIT + r"\bpush\b(?:\s+-\S+)*(?:\s+\S+)?\s+\+?(?:\S+:)?(?:refs/heads/)?main(?:\s|$)", flat):
    block("pushing to main is forbidden; open a PR")
# bare push (no refspec, or HEAD) while the checked-out branch is main
pm = re.search(GIT + r"\bpush\b(.*?)(?:$|[|;&])", flat)
if pm:
    toks = [t for t in pm.group(1).split() if not t.startswith("-")]
    dest = toks[1] if len(toks) > 1 else "HEAD"
    if dest == "HEAD" or ":" not in dest and dest == "":
        branch = "main"  # fail closed
        try:
            branch = subprocess.run(["git", "-C", cwd, "symbolic-ref", "--short", "HEAD"],
                                    capture_output=True, text=True, timeout=10).stdout.strip() or "main"
        except Exception:
            pass
        if branch == "main":
            block("pushing the checked-out main is forbidden; work on a branch and open a PR")
if re.search(GIT + r"\badd\b[^|;&]*(\s-A\b|\s--all\b|\s\.(\s|$))", flat):
    block("git add -A / . is forbidden; add explicit paths")
if re.search(GIT + r"\breset\b[^|;&]*--hard", flat):
    block("git reset --hard is forbidden")
if re.search(GIT + r"\bclean\b[^|;&]*\s-[a-zA-Z]*f", flat):
    block("git clean -f is forbidden")
if re.search(GIT + r"\b(filter-branch|filter-repo)\b", flat):
    block("history rewriting is forbidden")
if re.search(GIT + r"\bbranch\b[^|;&]*\s-[dD]\b[^|;&]*\b(wip|plan)/", flat) or re.search(GIT + r"\bpush\b[^|;&]*(--delete[^|;&]*\b(wip|plan)/|\s:(wip|plan)/)", flat):
    block("wip/* and plan/* branches are never deleted by the AI")

# ── destructive rm ────────────────────────────────────────────────────────────
for target in re.findall(r"\brm\b[^|;&]*\s-[a-zA-Z]*[rR][a-zA-Z]*\s+((?:\S+\s*)+)", flat):
    for tok in target.split():
        if tok.startswith("-"):
            continue
        t = os.path.expanduser(tok.replace("$HOME", HOME)).rstrip("/") or "/"
        t = os.path.realpath(t if t.startswith("/") else os.path.join(cwd, t))
        if t in ("/", HOME, CODESPACE) or (t.startswith(CODESPACE + "/") and t.count("/") == CODESPACE.count("/") + 1):
            block("refusing to remove a workspace or repository root")

# ── shell writes outside the session's territory (realm sessions only) ────────
if realm and realm != "citadel":
    own = f"{CITADEL}/realms/{realm}/"
    if re.search(r"(>>?|\btee\b|\bsed\s+-i|\bcp\b|\bmv\b|\binstall\b|\btruncate\b|\bdd\b)", flat):
        for tok in flat.split():
            t = tok.strip("'\"")
            if "/" not in t and not t.startswith("~") and "." not in t:
                continue
            if t.startswith("-"):
                continue
            path = t if t.startswith("/") or t.startswith("~") else os.path.join(cwd, t)
            path = os.path.realpath(os.path.expanduser(path.replace("$HOME", HOME)))
            if path.startswith(CITADEL + "/") and not path.startswith(own):
                block(f"realm session for '{realm}' may only write citadel/realms/{realm}/")
            other = realm_of(path)
            if other and other not in (realm, "citadel") and not path.startswith("/private/tmp"):
                block(f"realm session for '{realm}' may not write into another repository")
            rel = os.path.relpath(path, f"{CODESPACE}/{realm}")
            if not rel.startswith("..") and rel.split("/")[0] in ("CLAUDE.md", "CLAUDE.local.md", ".claude"):
                block("realm repos carry no AI files")
if re.search(r"\bjobs\.py\s+(apply|prune)\b", flat):
    block("jobs.py apply/prune is an operator action, not a session action")

# ── gh pr merge, any form ─────────────────────────────────────────────────────
if re.search(r"\bgh\s+pr\s+merge\b", flat):
    tail = flat.split("pr merge", 1)[1]
    repo_m = re.search(r"(?:-R|--repo)\s+(\S+)", tail)
    toks = [t for t in tail.split() if not t.startswith("-") and (not repo_m or t != repo_m.group(1))]
    selector = toks[0] if toks else None
    args = ["gh", "pr", "view"] + ([selector] if selector else []) + ["--json", "labels,isDraft,isCrossRepository,author,number"]
    if repo_m:
        args += ["-R", repo_m.group(1)]
    try:
        out = subprocess.run(args, capture_output=True, text=True, timeout=25, cwd=cwd).stdout
        info = json.loads(out or "{}")
    except Exception as e:
        block(f"cannot inspect PR ({e})")
    if not info.get("number"):
        block("cannot identify the PR to merge")
    labels = {l["name"] for l in info.get("labels", [])}
    bad = labels & {"plan", "hold", "needs-human", "wip"}
    if bad or info.get("isDraft") or info.get("isCrossRepository"):
        block(f"PR #{info['number']} is {sorted(bad) or 'draft/fork'}; only the human merges it")
    if (info.get("author") or {}).get("login") != "yusa-imit":
        block("PR author is not the kingdom account")
sys.exit(0)
