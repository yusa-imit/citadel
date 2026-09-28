"""Tests for scripts/jobs.py's local job loading (no cron server involved).

Each test builds a throwaway `workflows/` tree and points the module at it.
Run: `python3 -m unittest discover -s scripts/tests`.
"""
import importlib.util
import os
import pathlib
import shutil
import tempfile
import unittest

SCRIPT = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "jobs.py"))


def load_jobs_module():
    spec = importlib.util.spec_from_file_location("jobs_under_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class LocalJobsTest(unittest.TestCase):
    def setUp(self):
        self.root = pathlib.Path(tempfile.mkdtemp())
        self.wf = self.root / "workflows"
        (self.wf / "prompts").mkdir(parents=True)
        (self.wf / "system").mkdir()
        self.jobs = load_jobs_module()
        self.jobs.ROOT = self.root
        self.jobs.WF = self.wf

    def tearDown(self):
        shutil.rmtree(self.root)

    def write(self, rel, text):
        (self.wf / rel).write_text(text)

    def test_system_prompt_defaults_to_job_name(self):
        self.write("jobs.toml", '[jobs.solo]\nexpression = "5 1 * * *"\n')
        self.write("prompts/solo.md", "do it\n")
        self.write("system/solo.md", "solo system\n")
        job = self.jobs.local_jobs()["solo"]
        self.assertEqual(job["appendSystemPrompt"], "solo system")
        self.assertEqual(job["prompt"], "do it")

    def test_system_parts_concatenate_in_order(self):
        self.write("jobs.toml", '[jobs.extra]\nexpression = "5 1 * * *"\n'
                                'systemParts = ["base", "amend"]\n')
        self.write("prompts/extra.md", "go\n")
        self.write("system/base.md", "base contract\n")
        self.write("system/amend.md", "amendment\n")
        self.write("system/extra.md", "must be ignored\n")
        job = self.jobs.local_jobs()["extra"]
        self.assertEqual(job["appendSystemPrompt"], "base contract\n\namendment")

    def test_system_parts_missing_file_fails(self):
        self.write("jobs.toml", '[jobs.extra]\nexpression = "5 1 * * *"\n'
                                'systemParts = ["base", "absent"]\n')
        self.write("prompts/extra.md", "go\n")
        self.write("system/base.md", "base contract\n")
        with self.assertRaises(SystemExit) as caught:
            self.jobs.local_jobs()
        self.assertIn("absent.md", str(caught.exception))

    def test_system_parts_is_not_a_server_field(self):
        self.write("jobs.toml", '[jobs.extra]\nexpression = "5 1 * * *"\n'
                                'systemParts = ["base"]\n')
        self.write("prompts/extra.md", "go\n")
        self.write("system/base.md", "base contract\n")
        job = self.jobs.local_jobs()["extra"]
        remote = {"expression": "5 1 * * *", "prompt": "go",
                  "appendSystemPrompt": "base contract"}
        self.assertEqual(self.jobs.diff(job, remote), {})


if __name__ == "__main__":
    unittest.main()
