"""Tests for scripts/hooks/awaiting_merge.py against a fake GitHub.

Each test builds a throwaway codespace whose `citadel/zr-repos.toml` names two realms, `alpha` and
`beta`, and puts a fake `gh` on PATH that serves PRs and citadel issues from a JSON state file,
applies `issue create`/`issue close` to it, and logs every call. Run: `python3 -m unittest
discover -s scripts/tests`.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPT = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "hooks",
                                       "awaiting_merge.py"))
REPOS_TOML = """[workspace]
name = "test"

[repos.alpha]
path = "../alpha"

[repos.beta]
path = "../beta"

[deps]
beta = ["alpha"]
"""
FAKE_GH = r"""#!/usr/bin/env python3
import json, os, sys
path = os.environ["FAKE_GH_STATE"]
with open(path) as f:
    state = json.load(f)
args = sys.argv[1:]
state["calls"].append(args)


def opt(name):
    return [args[i + 1] for i, a in enumerate(args[:-1]) if a == name]


def finish(out, code=0):
    with open(path, "w") as f:
        json.dump(state, f)
    (sys.stdout if code == 0 else sys.stderr).write(out)
    sys.exit(code)


if state.get("fail"):
    finish("HTTP 502: Bad Gateway", 1)
repo = (opt("-R") or [""])[0].split("/")[-1]
verb = tuple(args[:2])
if verb == ("pr", "list"):
    finish(json.dumps([p for p in state["prs"].get(repo, [])
                       if p["state"] == "OPEN" and not p.get("hidden")]))
if verb == ("pr", "view"):
    found = [p for p in state["prs"].get(repo, []) if p["number"] == int(args[2])]
    finish(json.dumps(found[0]) if found else "no pull requests found", 0 if found else 1)
if verb == ("issue", "list"):
    label = opt("--label")[0]
    finish(json.dumps([i for i in state["issues"]
                       if i["state"] == "OPEN" and label in i["labels"]]))
if verb == ("issue", "create"):
    number = 100 + len(state["issues"])
    state["issues"].append({"number": number, "title": opt("--title")[0],
                            "body": opt("--body")[0], "labels": opt("--label"),
                            "assignees": opt("--assignee"), "state": "OPEN", "comments": []})
    finish(f"https://github.com/yusa-imit/citadel/issues/{number}\n")
if verb == ("issue", "close"):
    issue = [i for i in state["issues"] if i["number"] == int(args[2])][0]
    issue["state"] = "CLOSED"
    issue["comments"] += opt("--comment")
    finish("")
if verb == ("label", "create"):
    finish("")
finish("unexpected gh call", 2)
"""
FOOTER = "🤖 Generated with [Claude Code](https://claude.com/claude-code)"


def pr(number, labels=("plan",), state="OPEN", draft=False, author="yusa-imit",
       title="plan 004: phase 2 json", repo="alpha"):
    return {"number": number, "title": title, "state": state, "isDraft": draft,
            "author": {"login": author}, "labels": [{"name": n} for n in labels],
            "url": f"https://github.com/yusa-imit/{repo}/pull/{number}"}


class AwaitingMergeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = os.path.realpath(tempfile.mkdtemp())
        self.codespace = os.path.join(self.tmp, "codespace")
        citadel = os.path.join(self.codespace, "citadel")
        for d in (citadel, os.path.join(self.codespace, "alpha", "src"),
                  os.path.join(self.codespace, "beta")):
            os.makedirs(d)
        with open(os.path.join(citadel, "zr-repos.toml"), "w") as f:
            f.write(REPOS_TOML)
        bindir = os.path.join(self.tmp, "bin")
        os.makedirs(bindir)
        gh = os.path.join(bindir, "gh")
        with open(gh, "w") as f:
            f.write(FAKE_GH)
        os.chmod(gh, 0o755)
        self.state_path = os.path.join(self.tmp, "gh.json")
        self.save({"prs": {"alpha": [], "beta": []}, "issues": [], "calls": []})
        self.env = dict(os.environ, KINGDOM_CODESPACE=self.codespace,
                        FAKE_GH_STATE=self.state_path,
                        PATH=bindir + os.pathsep + os.environ["PATH"])

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def save(self, state):
        with open(self.state_path, "w") as f:
            json.dump(state, f)

    def state(self):
        with open(self.state_path) as f:
            return json.load(f)

    def set_prs(self, realm, prs):
        state = self.state()
        state["prs"][realm] = prs
        state["calls"] = []
        self.save(state)

    def run_script(self, *args, stdin=""):
        result = subprocess.run([sys.executable, SCRIPT, *args], input=stdin, text=True,
                                capture_output=True, env=self.env)
        return result.returncode, result.stdout, result.stderr

    def sync(self, *realms):
        code, out, err = self.run_script("sync", *realms)
        self.assertEqual(code, 0, f"sync failed: {err}")
        return out

    def hook(self, command, cwd=None):
        payload = json.dumps({"tool_input": {"command": command},
                              "cwd": cwd or os.path.join(self.codespace, "alpha")})
        code, out, err = self.run_script("hook", stdin=payload)
        self.assertEqual(code, 0, f"the hook must never fail the tool call: {err}")
        return json.loads(out)["hookSpecificOutput"]["additionalContext"] if out else ""

    def open_issues(self):
        return [i for i in self.state()["issues"] if i["state"] == "OPEN"]

    def writes(self):
        return [c[:2] for c in self.state()["calls"] if c[:2] in (["issue", "create"],
                                                                   ["issue", "close"])]

    # ── sync: opening ───────────────────────────────────────────────────────────────
    def test_sync_opens_one_citadel_issue_for_an_open_plan_pr(self):
        self.set_prs("alpha", [pr(38)])
        out = self.sync()
        [issue] = self.open_issues()
        self.assertEqual(issue["title"], "awaiting-merge: alpha#38 — plan 004: phase 2 json")
        self.assertEqual(sorted(issue["labels"]), ["awaiting-merge", "from:alpha"])
        self.assertEqual(issue["assignees"], ["yusa-imit"])
        self.assertIn("https://github.com/yusa-imit/alpha/pull/38", issue["body"])
        self.assertIn("<!-- awaiting-merge: yusa-imit/alpha#38 -->", issue["body"])
        self.assertTrue(issue["body"].rstrip().endswith(FOOTER))
        self.assertIn("alpha#38", out)

    def test_sync_opens_an_issue_for_a_needs_human_pr(self):
        self.set_prs("beta", [pr(5, labels=("needs-human", "bug"), repo="beta")])
        self.sync()
        [issue] = self.open_issues()
        self.assertIn("from:beta", issue["labels"])
        self.assertIn("`needs-human`", issue["body"])

    def test_sync_is_idempotent(self):
        self.set_prs("alpha", [pr(38)])
        self.sync()
        self.set_prs("alpha", [pr(38)])
        self.assertEqual(self.sync(), "")
        self.assertEqual(self.writes(), [])
        self.assertEqual(len(self.open_issues()), 1)

    def test_sync_ignores_prs_a_session_may_merge_or_that_are_not_ours(self):
        self.set_prs("alpha", [pr(1, labels=()), pr(2, labels=("auto-merged",)),
                               pr(3, labels=("hold",)), pr(4, draft=True),
                               pr(5, author="stranger"), pr(6, labels=("wip",))])
        self.assertEqual(self.sync(), "")
        self.assertEqual(self.writes(), [])

    # ── sync: closing ───────────────────────────────────────────────────────────────
    def test_sync_closes_the_issue_once_the_pr_is_merged(self):
        self.set_prs("alpha", [pr(38)])
        self.sync()
        self.set_prs("alpha", [pr(38, state="MERGED")])
        out = self.sync()
        self.assertEqual(self.open_issues(), [])
        [issue] = self.state()["issues"]
        self.assertIn("merged", issue["comments"][0])
        self.assertTrue(issue["comments"][0].rstrip().endswith(FOOTER))
        self.assertIn("closed", out)

    def test_sync_closes_the_issue_when_the_pr_is_closed_unmerged(self):
        self.set_prs("alpha", [pr(38)])
        self.sync()
        self.set_prs("alpha", [pr(38, state="CLOSED")])
        self.sync()
        [issue] = self.state()["issues"]
        self.assertEqual(issue["state"], "CLOSED")
        self.assertIn("closed without merge", issue["comments"][0])

    def test_sync_closes_the_issue_when_the_pr_loses_its_label(self):
        self.set_prs("alpha", [pr(9, labels=("needs-human",))])
        self.sync()
        self.set_prs("alpha", [pr(9, labels=())])
        self.sync()
        self.assertEqual(self.open_issues(), [])

    def test_sync_keeps_the_issue_while_an_unlisted_pr_still_waits(self):
        self.set_prs("alpha", [pr(38)])
        self.sync()
        self.set_prs("alpha", [dict(pr(38), hidden=True)])  # absent from `pr list`: truncated
        self.sync()
        self.assertEqual(len(self.open_issues()), 1)
        self.assertEqual(self.writes(), [])

    def test_sync_closes_a_duplicate_issue_for_the_same_pr(self):
        self.set_prs("alpha", [pr(38)])
        self.sync()
        state = self.state()
        dup = dict(state["issues"][0], number=150)
        state["issues"].append(dup)
        self.save(state)
        self.set_prs("alpha", [pr(38)])
        self.sync()
        [kept] = self.open_issues()
        self.assertEqual(kept["number"], 100)
        self.assertIn("#100", [i for i in self.state()["issues"]
                               if i["number"] == 150][0]["comments"][0])

    def test_sync_leaves_issues_without_a_marker_alone(self):
        state = self.state()
        state["issues"].append({"number": 7, "title": "awaiting-merge: by hand", "body": "x",
                                "labels": ["awaiting-merge"], "state": "OPEN", "comments": []})
        self.save(state)
        self.sync()
        self.assertEqual(self.writes(), [])

    # ── sync: scope and errors ──────────────────────────────────────────────────────
    def test_sync_of_one_realm_touches_only_that_realm(self):
        self.set_prs("alpha", [pr(1)])
        self.set_prs("beta", [pr(2, repo="beta")])
        self.sync()
        self.set_prs("beta", [pr(2, state="MERGED", repo="beta")])
        self.sync("alpha")
        self.assertEqual(len(self.open_issues()), 2)
        repos = {c[c.index("-R") + 1] for c in self.state()["calls"] if "-R" in c}
        self.assertNotIn("yusa-imit/beta", repos)

    def test_sync_rejects_an_unknown_realm(self):
        code, _, err = self.run_script("sync", "gamma")
        self.assertNotEqual(code, 0)
        self.assertIn("gamma", err)
        self.assertEqual(self.state()["calls"], [])

    def test_sync_fails_loudly_when_github_fails(self):
        state = self.state()
        state["fail"] = True
        self.save(state)
        code, _, err = self.run_script("sync")
        self.assertNotEqual(code, 0)
        self.assertIn("502", err)

    # ── hook ────────────────────────────────────────────────────────────────────────
    def test_hook_opens_the_issue_right_after_gh_pr_create(self):
        self.set_prs("alpha", [pr(38)])
        note = self.hook('gh pr create --label plan --title "plan 004" --body x',
                         cwd=os.path.join(self.codespace, "alpha", "src"))
        self.assertEqual(len(self.open_issues()), 1)
        self.assertIn("alpha#38", note)

    def test_hook_follows_the_repo_flag_over_the_cwd(self):
        self.set_prs("beta", [pr(2, labels=("needs-human",), repo="beta")])
        self.hook("gh pr edit 2 -R yusa-imit/beta --add-label needs-human")
        [issue] = self.open_issues()
        self.assertIn("from:beta", issue["labels"])

    def test_hook_follows_a_pr_url(self):
        self.set_prs("beta", [pr(2, state="CLOSED", repo="beta")])
        self.hook("gh pr close https://github.com/yusa-imit/beta/pull/2")
        repos = {c[c.index("-R") + 1] for c in self.state()["calls"] if "-R" in c}
        self.assertIn("yusa-imit/beta", repos)
        self.assertNotIn("yusa-imit/alpha", repos)

    def test_hook_ignores_other_commands(self):
        self.set_prs("alpha", [pr(38)])
        for command in ("git status", "gh pr list --label plan", "gh pr view 38",
                        "gh issue create --title x", "zig build test"):
            with self.subTest(command=command):
                self.assertEqual(self.hook(command), "")
        self.assertEqual(self.state()["calls"], [])

    def test_hook_ignores_repositories_outside_the_kingdom(self):
        self.set_prs("alpha", [pr(38)])
        self.assertEqual(self.hook("gh pr create --label plan", cwd=self.tmp), "")
        self.assertEqual(self.hook("gh pr create --label plan",
                                   cwd=os.path.join(self.codespace, "citadel")), "")
        self.assertEqual(self.state()["calls"], [])

    def test_hook_reports_a_github_failure_without_failing(self):
        state = self.state()
        state["fail"] = True
        self.save(state)
        note = self.hook("gh pr create --label plan")
        self.assertIn("failed", note)
        self.assertIn("/report", note)


if __name__ == "__main__":
    unittest.main()
