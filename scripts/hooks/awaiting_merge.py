#!/usr/bin/env python3
"""Keep one citadel issue open for every realm PR that waits on the human's merge.

    awaiting_merge.py sync [<realm>...]   # every realm in zr-repos.toml when none is named
    awaiting_merge.py hook                # PostToolUse on Bash: sync the realm a `gh pr` touched

A realm PR waits on the human when it is open, not a draft, authored by the kingdom account and
labeled `plan` or `needs-human`: guard_bash.py refuses to merge those, so the session that opened
one can only wait. GitHub does not notify an account of its own PRs, and the human reads
citadel's issues, not nine PR tabs. So each such PR gets one citadel issue
`awaiting-merge: <realm>#<n> — <title>` (labels `awaiting-merge` + `from:<realm>`), found again
by the marker in its body, and closed with a reason once `gh pr view` shows the PR merged, closed
or no longer waiting. Idempotent: the hook runs it the moment a PR is opened or relabeled,
`/report` every cycle, and the citadel cycle daily for every realm (protocol/GITHUB.md).
"""
import json
import os
import re
import subprocess
import sys

CODESPACE = os.path.realpath(os.environ.get("KINGDOM_CODESPACE", "/Users/fn/codespace"))
CITADEL = f"{CODESPACE}/citadel"
OWNER = "yusa-imit"
HUB = f"{OWNER}/citadel"
LABEL = "awaiting-merge"
LIST_LIMIT = 100
GH_TIMEOUT_S = 60
FOOTER = "🤖 Generated with [Claude Code](https://claude.com/claude-code)"
MARKER = re.compile(r"<!-- awaiting-merge: " + OWNER + r"/([a-z0-9_-]+)#([0-9]+) -->")
PR_COMMAND = re.compile(r"\bgh\s+pr\s+(create|edit|ready|close|reopen)\b")
# Labels that make a PR wait on the human, in priority order, with what the merge decides.
WAITING = {
    "plan": "It is a plan: merge = approve, comment on the PR = change request, close = reject. "
            "Until then the realm spends its cycles on stabilization only.",
    "needs-human": "The AI could not land it on its own; the PR's latest comment says why. Fix, "
                   "merge or close it.",
}


class GhError(Exception):
    pass


def gh(*args):
    result = subprocess.run(["gh", *args], capture_output=True, text=True, timeout=GH_TIMEOUT_S)
    if result.returncode != 0:
        raise GhError(f"gh {' '.join(args[:2])} failed: {result.stderr.strip()[:300]}")
    return result.stdout


def gh_json(*args):
    return json.loads(gh(*args) or "null")


def realms():
    """Realm names from zr-repos.toml, the kingdom's repo registry (citadel is not one)."""
    with open(f"{CITADEL}/zr-repos.toml") as f:
        names = re.findall(r"^\[repos\.([a-z0-9_-]+)\]", f.read(), re.M)
    assert names, "zr-repos.toml lists no repos"
    assert "citadel" not in names, "citadel PRs are not realm PRs"
    return names


def waiting_label(pr):
    """The label that makes `pr` wait on the human's merge, or None when it does not wait."""
    if pr["state"] != "OPEN" or pr["isDraft"] or (pr["author"] or {}).get("login") != OWNER:
        return None
    labels = {label["name"] for label in pr["labels"]}
    return next((name for name in WAITING if name in labels), None)


def escalations():
    """Open awaiting-merge issues: {(realm, pr): issue} plus [(issue, kept issue)] duplicates.
    Issues without the marker were not opened here and are left alone."""
    issues = gh_json("issue", "list", "-R", HUB, "--label", LABEL, "--state", "open",
                     "--limit", str(LIST_LIMIT), "--json", "number,body")
    found, duplicates = {}, []
    for issue in sorted(issues, key=lambda i: i["number"]):
        m = MARKER.search(issue["body"] or "")
        if not m:
            continue
        key = (m.group(1), int(m.group(2)))
        if key in found:
            duplicates.append((key, issue["number"], found[key]))
        else:
            found[key] = issue["number"]
    return found, duplicates


def open_issue(realm, pr, label):
    number = pr["number"]
    assert label in WAITING and number > 0, (label, number)
    gh("label", "create", LABEL, "--color", "FBCA04", "--force", "-R", HUB,
       "--description", "A realm PR waits on the human's merge")
    gh("label", "create", f"from:{realm}", "--color", "EDEDED", "--force", "-R", HUB)
    body = (f"[{realm}#{number}]({pr['url']}) **{pr['title']}** waits on your merge. "
            f"It is labeled `{label}`, so no session may merge it.\n\n{WAITING[label]}\n\n"
            "Answer on the PR; nothing reads comments here. This issue closes on the next sync "
            "after the PR is merged, closed or relabeled.\n\n"
            f"<!-- awaiting-merge: {OWNER}/{realm}#{number} -->\n\n{FOOTER}\n")
    url = gh("issue", "create", "-R", HUB, "--title",
             f"{LABEL}: {realm}#{number} — {pr['title']}", "--body", body, "--label", LABEL,
             "--label", f"from:{realm}", "--assignee", OWNER).strip()
    return f"opened {url} for {realm}#{number}"


def close_issue(issue, text):
    gh("issue", "close", str(issue), "-R", HUB, "--comment", f"{text}\n\n{FOOTER}")


def settle(realm, number, issue):
    """Close `issue` if its PR no longer waits. `pr list` may be truncated, so the PR itself is
    the evidence: an issue is closed only on what `gh pr view` says now."""
    pr = gh_json("pr", "view", str(number), "-R", f"{OWNER}/{realm}", "--json",
                 "state,isDraft,author,labels")
    if waiting_label(pr):
        return None
    reason = {"MERGED": "merged", "CLOSED": "closed without merge"}.get(
        pr["state"], "no longer waits on a human merge")
    close_issue(issue, f"{realm}#{number} {reason}.")
    return f"closed citadel#{issue}: {realm}#{number} {reason}"


def sync_realm(realm, escalated):
    prs = gh_json("pr", "list", "-R", f"{OWNER}/{realm}", "--state", "open", "--limit",
                  str(LIST_LIMIT), "--json", "number,title,url,state,isDraft,author,labels")
    if len(prs) >= LIST_LIMIT:
        print(f"warning: {realm} has {LIST_LIMIT}+ open PRs; only the newest were checked",
              file=sys.stderr)
    waiting = {}
    for pr in prs:
        label = waiting_label(pr)
        if label:
            waiting[pr["number"]] = (pr, label)
    actions = [open_issue(realm, pr, label) for number, (pr, label) in sorted(waiting.items())
               if (realm, number) not in escalated]
    for (owner_realm, number), issue in sorted(escalated.items()):
        if owner_realm == realm and number not in waiting:
            actions.append(settle(realm, number, issue))
    return [action for action in actions if action]


def sync(names):
    known = realms()
    unknown = [name for name in names if name not in known]
    if unknown:
        raise SystemExit(f"awaiting_merge: unknown realm(s) {', '.join(unknown)}; "
                         f"zr-repos.toml lists {', '.join(known)}")
    targets = names or known
    escalated, duplicates = escalations()
    actions = []
    for (realm, number), issue, kept in duplicates:
        if realm in targets:
            close_issue(issue, f"Duplicate of #{kept}, which tracks {realm}#{number}.")
            actions.append(f"closed citadel#{issue}: duplicate of #{kept}")
    for realm in targets:
        actions += sync_realm(realm, escalated)
    return actions


def touched_realm(command, cwd):
    """The repository a `gh pr` command acts on: its -R/--repo flag, a PR URL, else the cwd."""
    m = (re.search(r"(?:-R|--repo)[=\s]+(?:[^\s/]+/)*([a-z0-9_-]+)", command)
         or re.search(r"github\.com/" + OWNER + r"/([a-z0-9_-]+)/pull/", command))
    if m:
        return m.group(1)
    path = os.path.realpath(cwd)
    if path.startswith(CODESPACE + "/"):
        return path[len(CODESPACE) + 1:].split("/")[0]
    return None


def hook(data):
    """PostToolUse: after a `gh pr` call that can open or relabel a PR, sync that realm. Never
    fails the tool call; what it did reaches the session as context."""
    command = " ".join(((data.get("tool_input") or {}).get("command") or "").split())
    if not PR_COMMAND.search(command):
        return
    realm = touched_realm(command, data.get("cwd") or os.getcwd())
    if realm not in realms():
        return
    try:
        note = "; ".join(sync([realm]))
    except (GhError, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as e:
        note = f"sync failed ({e}); /report runs it again"
    if note:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse",
                                                 "additionalContext": f"{LABEL}: {note}"}}))


def main(argv):
    if argv[1:2] == ["sync"]:
        try:
            actions = sync(argv[2:])
        except GhError as e:
            sys.exit(f"awaiting_merge: {e}")
        for action in actions:
            print(action)
    elif argv[1:] == ["hook"]:
        hook(json.load(sys.stdin))
    else:
        sys.exit("usage: awaiting_merge.py sync [<realm>...] | hook")


if __name__ == "__main__":
    main(sys.argv)
