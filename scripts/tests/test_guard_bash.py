"""Tests for the grant rules in scripts/hooks/guard_bash.py (protocol/GITHUB.md, "Grants").

Each test builds a throwaway codespace: a `citadel` git repo with a bare `origin`, a realm
directory, and a fake `gh` on PATH that answers `gh pr view` from $FAKE_GH_PR. The guard runs as
a subprocess exactly as the PreToolUse hook does. Run: `python3 -m unittest discover -s
scripts/tests`.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPT = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "hooks",
                                       "guard_bash.py"))
SEED = {
    "core/CONTRACT.md": "contract v1\n",
    "workflows/jobs.toml": "[jobs.a]\n",
    "scripts/jobs.py": "# stand-in\n",
    "docs/ROADMAP.md": "roadmap v1\n",
}
FAKE_GH = """#!/usr/bin/env python3
import os, sys
sys.stdout.write(os.environ.get("FAKE_GH_PR", "{}"))
"""
GIT_ENV = dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1",
               GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t",
               GIT_COMMITTER_EMAIL="t@t")
for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
    GIT_ENV.pop(key, None)


def git(cwd, *args):
    result = subprocess.run(["git", "-C", cwd, *args], capture_output=True, text=True,
                            env=GIT_ENV)
    if result.returncode != 0:
        raise AssertionError(f"git {' '.join(args)} failed: {result.stderr}")
    return result.stdout.strip()


def pr(url, files, labels=(), changed=None):
    return json.dumps({
        "number": 7, "url": url, "isDraft": False, "isCrossRepository": False,
        "author": {"login": "yusa-imit"}, "labels": [{"name": n} for n in labels],
        "files": [{"path": p} for p in files],
        "changedFiles": len(files) if changed is None else changed,
    })


CITADEL_PR = "https://github.com/yusa-imit/citadel/pull/7"
REALM_PR = "https://github.com/yusa-imit/sailor/pull/7"


class GuardGrantTest(unittest.TestCase):
    def setUp(self):
        self.tmp = os.path.realpath(tempfile.mkdtemp())
        self.codespace = os.path.join(self.tmp, "codespace")
        self.citadel = os.path.join(self.codespace, "citadel")
        self.realm = os.path.join(self.codespace, "alpha")
        os.makedirs(self.realm)
        origin = os.path.join(self.tmp, "origin.git")
        subprocess.run(["git", "init", "-q", "--bare", "-b", "main", origin], check=True,
                       env=GIT_ENV)
        subprocess.run(["git", "init", "-q", "-b", "main", self.citadel], check=True,
                       env=GIT_ENV)
        for rel, text in SEED.items():
            self.write(rel, text)
        git(self.citadel, "add", *SEED)
        git(self.citadel, "commit", "-q", "-m", "seed")
        git(self.citadel, "remote", "add", "origin", origin)
        git(self.citadel, "push", "-q", "-u", "origin", "main")
        bindir = os.path.join(self.tmp, "bin")
        os.makedirs(bindir)
        gh = os.path.join(bindir, "gh")
        with open(gh, "w") as f:
            f.write(FAKE_GH)
        os.chmod(gh, 0o755)
        self.env = dict(GIT_ENV, KINGDOM_CODESPACE=self.codespace,
                        PATH=bindir + os.pathsep + os.environ["PATH"])

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def write(self, rel, text):
        path = os.path.join(self.citadel, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(text)

    def guard(self, command, cwd=None, pr_json=None):
        env = dict(self.env, FAKE_GH_PR=pr_json or "{}")
        payload = json.dumps({"tool_input": {"command": command}, "cwd": cwd or self.citadel})
        result = subprocess.run([sys.executable, SCRIPT], input=payload, capture_output=True,
                                text=True, env=env)
        return result.returncode, result.stderr

    def assert_blocked(self, command, reason, **kw):
        code, err = self.guard(command, **kw)
        self.assertEqual(code, 2, f"expected a block, got exit {code}: {err}")
        self.assertIn(reason, err)

    def assert_allowed(self, command, **kw):
        code, err = self.guard(command, **kw)
        self.assertEqual(code, 0, f"expected no block, got exit {code}: {err}")

    # ── jobs.py apply ────────────────────────────────────────────────────────────────
    def test_apply_allowed_from_citadel_on_clean_main_equal_to_origin(self):
        self.assert_allowed("python3 scripts/jobs.py apply --yes")

    def test_apply_blocked_from_a_realm_session(self):
        self.assert_blocked(f"python3 {self.citadel}/scripts/jobs.py apply --yes",
                            "only a citadel session", cwd=self.realm)

    def test_apply_blocked_off_main(self):
        git(self.citadel, "switch", "-q", "-c", "chore/x")
        self.assert_blocked("python3 scripts/jobs.py apply --yes", "not on main")

    def test_apply_blocked_when_main_is_ahead_of_origin(self):
        self.write("workflows/jobs.toml", "[jobs.a]\n[jobs.b]\n")
        git(self.citadel, "commit", "-q", "-am", "unmerged")
        self.assert_blocked("python3 scripts/jobs.py apply --yes", "origin/main")

    def test_apply_blocked_with_a_modified_permission_file(self):
        self.write("workflows/jobs.toml", "[jobs.a]\n[jobs.b]\n")
        self.assert_blocked("python3 scripts/jobs.py apply --yes", "workflows/jobs.toml")

    def test_apply_blocked_with_an_untracked_permission_file(self):
        self.write("workflows/system/a.md", "sneaky\n")
        self.assert_blocked("python3 scripts/jobs.py apply --yes", "workflows/system/a.md")

    def test_apply_allowed_with_unrelated_dirty_files(self):
        self.write("docs/ROADMAP.md", "roadmap v2\n")
        self.write("realms/alpha/memory/context.md", "cycle 2\n")
        self.assert_allowed("python3 scripts/jobs.py apply --yes")

    def test_apply_blocked_for_a_copy_of_jobs_py(self):
        self.assert_blocked(f"python3 {self.tmp}/jobs.py apply --yes", "scripts/jobs.py")

    def test_apply_blocked_for_a_relative_path_after_cd(self):
        self.assert_blocked(f"cd {self.tmp} && python3 scripts/jobs.py apply --yes",
                            "absolute path")

    def test_prune_blocked_even_on_clean_main(self):
        self.assert_blocked("python3 scripts/jobs.py prune --yes", "operator action")

    def test_direct_cron_api_blocked(self):
        self.assert_blocked("curl -X POST http://localhost:3000/jobs -d '{}'",
                            "cron server")

    # ── gh pr merge ─────────────────────────────────────────────────────────────────
    def test_merge_blocked_for_a_grant_label(self):
        self.assert_blocked("gh pr merge 7 --squash", "grant",
                            pr_json=pr(CITADEL_PR, ["docs/ROADMAP.md"], labels=["grant"]))

    def test_merge_blocked_for_a_citadel_pr_on_the_permission_surface(self):
        for path in ("workflows/jobs.toml", "core/CONTRACT.md", "scripts/hooks/guard_bash.py",
                     ".claude/skills/cycle/SKILL.md", "protocol/GITHUB.md", "CLAUDE.md",
                     "realms/alpha/settings.json", "realms/alpha/system.md"):
            with self.subTest(path=path):
                self.assert_blocked("gh pr merge 7 --squash", "permission surface",
                                    pr_json=pr(CITADEL_PR, ["docs/ROADMAP.md", path]))

    def test_merge_blocked_when_the_file_list_is_truncated(self):
        self.assert_blocked("gh pr merge 7 --squash", "file list",
                            pr_json=pr(CITADEL_PR, ["docs/ROADMAP.md"], changed=101))

    def test_merge_allowed_for_a_citadel_pr_off_the_surface(self):
        files = ["docs/ROADMAP.md", "realms/alpha/memory/context.md", "realms/alpha/STATE.md",
                 "scripts/tests/test_jobs.py"]
        self.assert_allowed("gh pr merge 7 --squash", pr_json=pr(CITADEL_PR, files))

    def test_merge_allowed_for_a_realm_pr_touching_its_ci_workflow(self):
        self.assert_allowed("gh pr merge 7 --squash", cwd=self.realm,
                            pr_json=pr(REALM_PR, [".github/workflows/ci.yml", "core/x.zig"]))


if __name__ == "__main__":
    unittest.main()
