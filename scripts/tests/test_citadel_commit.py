"""Tests for scripts/hooks/citadel_commit.py against throwaway git repositories.

Each test builds a bare `origin`, the shared `checkout` the helper works on (every realm session
edits it concurrently), and an `elsewhere` clone standing in for changes that reach main through
GitHub. Run: `python3 -m unittest discover -s scripts/tests`.
"""
import os
import shutil
import subprocess
import tempfile
import unittest

SCRIPT = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "hooks",
                                       "citadel_commit.py"))
SEED = {
    "protocol/CYCLE.md": "cycle v1\n",
    "realms/alpha/REALM.md": "alpha realm v1\n",
    "realms/alpha/STATE.md": "alpha state v1\n",
    "realms/alpha/settings.json": "{}\n",
    "realms/alpha/memory/context.md": "alpha cycle 1\n",
    "realms/alpha/memory/counter": "1\n",
    "realms/alpha/memory/old.md": "alpha old notes\n",
    "realms/beta/REALM.md": "beta realm v1\n",
    "realms/beta/memory/context.md": "beta cycle 1\n",
    "realms/beta/memory/counter": "1\n",
    ".gitignore": ".DS_Store\n",
}
ENV = dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1",
           GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t",
           GIT_COMMITTER_EMAIL="t@t")
for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
    ENV.pop(key, None)


def git(cwd, *args, check=True):
    result = subprocess.run(["git", "-C", cwd, *args], capture_output=True, text=True, env=ENV)
    if check and result.returncode != 0:
        raise AssertionError(f"git {' '.join(args)} failed: {result.stderr}")
    return result.stdout.strip()


class Kingdom(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="citadel-commit-")
        self.origin = os.path.join(self.root, "origin.git")
        self.checkout = os.path.join(self.root, "checkout")
        self.elsewhere = os.path.join(self.root, "elsewhere")
        git(self.root, "init", "-q", "--bare", "-b", "main", self.origin)
        git(self.root, "clone", "-q", self.origin, self.elsewhere)
        for rel, text in SEED.items():
            self.write(self.elsewhere, rel, text)
        git(self.elsewhere, "add", "--", *SEED)
        git(self.elsewhere, "commit", "-q", "-m", "seed")
        git(self.elsewhere, "push", "-q", "origin", "HEAD:main")
        git(self.root, "clone", "-q", self.origin, self.checkout)
        self.seed_main = self.origin_main()

    def tearDown(self):
        shutil.rmtree(self.root)

    def write(self, repo, rel, text):
        path = os.path.join(repo, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(text)

    def read(self, repo, rel):
        with open(os.path.join(repo, rel)) as f:
            return f.read()

    def origin_main(self):
        return git(self.origin, "rev-parse", "main")

    def origin_file(self, rel):
        result = subprocess.run(["git", "-C", self.origin, "show", f"main:{rel}"],
                                capture_output=True, text=True, env=ENV)
        return result.stdout if result.returncode == 0 else None

    def push_elsewhere(self, rel, text):
        git(self.elsewhere, "pull", "-q", "--ff-only")
        self.write(self.elsewhere, rel, text)
        git(self.elsewhere, "add", "--", rel)
        git(self.elsewhere, "commit", "-q", "-m", f"upstream edit of {rel}")
        git(self.elsewhere, "push", "-q", "origin", "HEAD:main")

    def run_helper(self, realm="alpha", cycle="2"):
        env = dict(ENV, KINGDOM_CITADEL=self.checkout)
        return subprocess.run(["python3", SCRIPT, realm, cycle], capture_output=True,
                              text=True, env=env, timeout=120)

    def reject_pushes(self, times):
        """Install a pre-receive hook on origin that rejects the next `times` pushes."""
        budget = os.path.join(self.root, "rejections")
        with open(budget, "w") as f:
            f.write(str(times))
        hook = os.path.join(self.origin, "hooks", "pre-receive")
        with open(hook, "w") as f:
            f.write("#!/bin/sh\n"
                    f"n=$(cat {budget})\n"
                    "[ \"$n\" -gt 0 ] || exit 0\n"
                    f"echo $((n - 1)) > {budget}\n"
                    "echo rejected by test >&2\n"
                    "exit 1\n")
        os.chmod(hook, 0o755)

    def edit_alpha(self):
        self.write(self.checkout, "realms/alpha/memory/context.md", "alpha cycle 2\n")
        self.write(self.checkout, "realms/alpha/memory/counter", "2\n")

    def assert_pushed_alpha(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("pushed", result.stdout)
        self.assertEqual(self.origin_file("realms/alpha/memory/context.md"), "alpha cycle 2\n")
        self.assertEqual(self.origin_file("realms/alpha/memory/counter"), "2\n")
        subject = git(self.origin, "log", "-1", "--format=%s", "main")
        self.assertEqual(subject, "chore(alpha): cycle 2 memory")


class CommitTest(Kingdom):
    def test_commits_own_realm_past_foreign_staged_and_unstaged_changes(self):
        self.write(self.checkout, "realms/beta/memory/context.md", "beta staged\n")
        git(self.checkout, "add", "--", "realms/beta/memory/context.md")
        self.write(self.checkout, "realms/beta/memory/counter", "9\n")
        self.edit_alpha()
        result = self.run_helper()
        self.assert_pushed_alpha(result)
        self.assertEqual(self.origin_file("realms/beta/memory/context.md"), "beta cycle 1\n")
        self.assertEqual(self.origin_file("realms/beta/memory/counter"), "1\n")
        self.assertEqual(git(self.origin, "rev-parse", "main~1"), self.seed_main)
        self.assertEqual(self.read(self.checkout, "realms/beta/memory/context.md"),
                         "beta staged\n")
        self.assertEqual(self.read(self.checkout, "realms/beta/memory/counter"), "9\n")
        staged = git(self.checkout, "diff", "--cached", "--name-only")
        self.assertEqual(staged, "realms/beta/memory/context.md")

    def test_lands_on_main_when_checkout_is_on_another_branch(self):
        git(self.checkout, "switch", "-q", "-c", "chore/pr-branch")
        self.write(self.checkout, "protocol/CYCLE.md", "cycle v2 draft\n")
        git(self.checkout, "commit", "-q", "-am", "draft protocol change")
        branch_head = git(self.checkout, "rev-parse", "HEAD")
        self.edit_alpha()
        result = self.run_helper()
        self.assert_pushed_alpha(result)
        self.assertEqual(self.origin_file("protocol/CYCLE.md"), "cycle v1\n")
        self.assertEqual(git(self.checkout, "symbolic-ref", "--short", "HEAD"),
                         "chore/pr-branch")
        self.assertEqual(git(self.checkout, "rev-parse", "HEAD"), branch_head)
        self.assertIn("not main", result.stdout)

    def test_keeps_upstream_edit_to_a_realm_file_the_cycle_did_not_touch(self):
        git(self.checkout, "switch", "-q", "-c", "chore/pr-branch")
        self.push_elsewhere("realms/alpha/REALM.md", "alpha realm v2\n")
        self.edit_alpha()
        result = self.run_helper()
        self.assert_pushed_alpha(result)
        self.assertEqual(self.origin_file("realms/alpha/REALM.md"), "alpha realm v2\n")

    def test_warns_when_its_copy_replaces_a_change_main_made_to_the_same_file(self):
        git(self.checkout, "switch", "-q", "-c", "chore/pr-branch")
        self.push_elsewhere("realms/alpha/memory/context.md", "alpha upstream fold\n")
        self.edit_alpha()
        result = self.run_helper()
        self.assert_pushed_alpha(result)
        self.assertIn("warning: main also changed realms/alpha/memory/context.md; this cycle's "
                      "copy replaces it\n", result.stdout)

    def test_commits_added_and_deleted_realm_files_but_not_ignored_ones(self):
        self.edit_alpha()
        self.write(self.checkout, "realms/alpha/memory/new.md", "alpha new notes\n")
        self.write(self.checkout, "realms/alpha/memory/.DS_Store", "finder junk\n")
        os.remove(os.path.join(self.checkout, "realms/alpha/memory/old.md"))
        result = self.run_helper()
        self.assert_pushed_alpha(result)
        self.assertEqual(self.origin_file("realms/alpha/memory/new.md"), "alpha new notes\n")
        self.assertIsNone(self.origin_file("realms/alpha/memory/old.md"))
        self.assertIsNone(self.origin_file("realms/alpha/memory/.DS_Store"))

    def test_never_commits_realm_files_outside_memory_state_and_realm(self):
        self.edit_alpha()
        self.write(self.checkout, "realms/alpha/settings.json", '{"edited": true}\n')
        result = self.run_helper()
        self.assert_pushed_alpha(result)
        self.assertEqual(self.origin_file("realms/alpha/settings.json"), "{}\n")

    def test_concurrent_realms_both_land_and_leave_the_checkout_clean(self):
        self.edit_alpha()
        self.write(self.checkout, "realms/beta/memory/context.md", "beta cycle 7\n")
        env = dict(ENV, KINGDOM_CITADEL=self.checkout)
        runs = [subprocess.Popen(["python3", SCRIPT, realm, cycle], env=env, text=True,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                for realm, cycle in (("alpha", "2"), ("beta", "7"))]
        for run in runs:
            out, err = run.communicate(timeout=120)
            self.assertEqual(run.returncode, 0, out + err)
        self.assertEqual(self.origin_file("realms/alpha/memory/context.md"), "alpha cycle 2\n")
        self.assertEqual(self.origin_file("realms/beta/memory/context.md"), "beta cycle 7\n")
        self.assertEqual(git(self.origin, "rev-list", "--count", f"{self.seed_main}..main"), "2")
        self.assertEqual(git(self.checkout, "rev-parse", "HEAD"), self.origin_main())
        self.assertEqual(git(self.checkout, "status", "--porcelain"), "")

    def test_stale_staged_copy_left_by_the_old_helper_does_not_block(self):
        self.write(self.checkout, "realms/alpha/memory/context.md", "alpha stale\n")
        git(self.checkout, "add", "--", "realms/alpha/memory/context.md")
        self.edit_alpha()
        result = self.run_helper()
        self.assert_pushed_alpha(result)
        self.assertEqual(git(self.checkout, "rev-parse", "HEAD"), self.origin_main())
        self.assertEqual(git(self.checkout, "status", "--porcelain"), "")


class NothingToCommitTest(Kingdom):
    def test_clean_realm_pushes_nothing(self):
        result = self.run_helper()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("nothing to commit", result.stdout)
        self.assertEqual(self.origin_main(), self.seed_main)

    def test_foreign_dirt_alone_pushes_nothing(self):
        self.write(self.checkout, "realms/beta/memory/context.md", "beta cycle 2\n")
        result = self.run_helper()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("nothing to commit", result.stdout)
        self.assertEqual(self.origin_main(), self.seed_main)
        self.assertEqual(self.read(self.checkout, "realms/beta/memory/context.md"),
                         "beta cycle 2\n")


class ArgumentTest(Kingdom):
    def test_rejects_unknown_realm_malformed_realm_and_bad_cycle(self):
        self.edit_alpha()
        for realm, cycle in (("gamma", "2"), ("../alpha", "2"), ("alpha", "two"),
                             ("alpha", "-1"), ("", "2")):
            result = self.run_helper(realm, cycle)
            self.assertNotEqual(result.returncode, 0, (realm, cycle))
        self.assertEqual(self.origin_main(), self.seed_main)


class SyncTest(Kingdom):
    def test_fast_forwards_checkout_and_keeps_foreign_edits(self):
        self.push_elsewhere("protocol/CYCLE.md", "cycle v2\n")
        self.write(self.checkout, "realms/beta/memory/context.md", "beta in progress\n")
        self.edit_alpha()
        result = self.run_helper()
        self.assert_pushed_alpha(result)
        self.assertEqual(self.origin_file("protocol/CYCLE.md"), "cycle v2\n")
        self.assertEqual(git(self.checkout, "rev-parse", "HEAD"), self.origin_main())
        self.assertEqual(self.read(self.checkout, "protocol/CYCLE.md"), "cycle v2\n")
        self.assertEqual(self.read(self.checkout, "realms/beta/memory/context.md"),
                         "beta in progress\n")
        status = git(self.checkout, "status", "--porcelain")
        self.assertEqual(status, "M realms/beta/memory/context.md")

    def test_leaves_checkout_alone_when_main_changed_a_locally_edited_file(self):
        self.push_elsewhere("realms/beta/memory/context.md", "beta upstream\n")
        self.write(self.checkout, "realms/beta/memory/context.md", "beta local\n")
        head = git(self.checkout, "rev-parse", "HEAD")
        self.edit_alpha()
        result = self.run_helper()
        self.assert_pushed_alpha(result)
        self.assertEqual(self.origin_file("realms/beta/memory/context.md"), "beta upstream\n")
        self.assertEqual(self.read(self.checkout, "realms/beta/memory/context.md"),
                         "beta local\n")
        self.assertEqual(git(self.checkout, "rev-parse", "HEAD"), head)
        self.assertIn("warning", result.stdout)

    def test_leaves_checkout_alone_when_local_main_has_unpushed_commits(self):
        self.write(self.checkout, "protocol/CYCLE.md", "cycle local\n")
        git(self.checkout, "commit", "-q", "-am", "local-only commit")
        head = git(self.checkout, "rev-parse", "HEAD")
        self.edit_alpha()
        result = self.run_helper()
        self.assert_pushed_alpha(result)
        self.assertEqual(self.origin_file("protocol/CYCLE.md"), "cycle v1\n")
        self.assertEqual(git(self.checkout, "rev-parse", "HEAD"), head)
        self.assertIn("warning", result.stdout)


class PushFailureTest(Kingdom):
    def test_retries_a_rejected_push(self):
        self.reject_pushes(1)
        self.edit_alpha()
        self.assert_pushed_alpha(self.run_helper())

    def test_gives_up_without_a_local_commit_and_the_next_run_carries_the_memory(self):
        self.reject_pushes(99)
        head = git(self.checkout, "rev-parse", "HEAD")
        self.edit_alpha()
        result = self.run_helper()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.origin_main(), self.seed_main)
        self.assertEqual(git(self.checkout, "rev-parse", "HEAD"), head)
        self.assertEqual(git(self.checkout, "diff", "--cached", "--name-only"), "")
        self.reject_pushes(0)
        self.assert_pushed_alpha(self.run_helper())


if __name__ == "__main__":
    unittest.main()
