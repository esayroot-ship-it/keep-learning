"""CLI regressions for mode-specific practice and progress; uses temporary workspaces."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SKILL = Path(__file__).resolve().parents[1]
INIT = SKILL / "scripts/init_learning_workspace.py"
UPDATE = SKILL / "scripts/update_progress.py"
READING = ("explain", "trace", "predict", "impact", "verify")
WRITING = ("explain", "predict", "modify", "write", "verify")


class LearningProgressTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="keep-learning-test-")
        self.root = Path(self.temporary.name).resolve()
        self.addCleanup(self.cleanup_workspace)

    def cleanup_workspace(self):
        # Verify the resolved target before recursive cleanup on Windows.
        self.assertEqual(self.root.parent, Path(tempfile.gettempdir()).resolve())
        self.assertTrue(self.root.name.startswith("keep-learning-test-"))
        self.temporary.cleanup()

    def cli(self, script, *args, error=None):
        result = subprocess.run(
            [sys.executable, "-X", "utf8", str(script), *map(str, args)],
            capture_output=True, text=True, encoding="utf-8", timeout=30,
        )
        if error is None:
            self.assertEqual(result.returncode, 0, result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout)
            self.assertIn(error, result.stderr)
        return result

    def workspace(self, mode="code-reading", name="lesson"):
        self.cli(INIT, "--root", self.root, "--goal", name, "--training-mode", mode)
        return self.root / name

    def progress(self, workspace):
        return json.loads((workspace / "04-status/progress.json").read_text(encoding="utf-8"))

    def start(self, workspace):
        self.cli(UPDATE, workspace, "--plan-unit", "one=First unit", "--advance")

    def mark(self, workspace, checks):
        args = [arg for check in checks for arg in ("--mastered", check)]
        self.cli(UPDATE, workspace, *args)

    def test_reading_mode_survives_configuration_and_planning(self):
        workspace = self.workspace()
        self.start(workspace)
        self.cli(UPDATE, workspace, "--review", "trace pending")
        config = json.loads((workspace / "00-meta/learning-config.json").read_text(encoding="utf-8"))
        state = self.progress(workspace)
        self.assertEqual(config["training_mode"], "code-reading")
        self.assertEqual(state["unit_plan"][0]["training_mode"], "code-reading")
        self.assertEqual(set(state["mastery_evidence"]["one"]), set(READING))
        self.assertFalse(any(state["mastery_evidence"]["one"].values()))

    def test_reading_rejects_write_without_mutating_progress(self):
        workspace = self.workspace()
        self.start(workspace)
        before = self.progress(workspace)
        self.cli(UPDATE, workspace, "--mastered", "write", error="mastery checks not valid")
        self.assertEqual(self.progress(workspace), before)

    def test_reading_needs_impact_but_does_not_need_writing(self):
        workspace = self.workspace()
        self.start(workspace)
        self.mark(workspace, (check for check in READING if check != "impact"))
        self.cli(UPDATE, workspace, "--advance", error="missing mastery evidence: impact")
        self.mark(workspace, ["impact"])
        self.cli(UPDATE, workspace, "--advance")
        state = self.progress(workspace)
        self.assertEqual(state["completed_units"], ["one"])
        self.assertNotIn("write", state["mastery_evidence"]["one"])
        self.assertEqual(state["current_phase"], "planning")

    def test_writing_cannot_advance_without_independent_write_flag(self):
        workspace = self.workspace("manual-coding")
        self.start(workspace)
        self.mark(workspace, (check for check in WRITING if check != "write"))
        self.cli(UPDATE, workspace, "--advance", error="missing mastery evidence: write")
        self.assertEqual(self.progress(workspace)["completed_units"], [])
        self.mark(workspace, ["write"])
        self.cli(UPDATE, workspace, "--advance")
        self.assertEqual(self.progress(workspace)["completed_units"], ["one"])

    def test_manual_completion_cannot_bypass_planned_unit_gate(self):
        for mode in ("manual-coding", "code-reading"):
            with self.subTest(mode=mode):
                workspace = self.workspace(mode, mode)
                self.start(workspace)
                before = self.progress(workspace)
                self.cli(UPDATE, workspace, "--complete", "one", "--finish-topic", error="use --advance")
                self.assertEqual(self.progress(workspace), before)
                self.assertEqual(list((workspace / "01-lessons/archive").rglob("*.md")), [])

    def test_reading_to_writing_keeps_separate_evidence_and_archives(self):
        workspace = self.workspace("mixed")
        self.cli(
            UPDATE, workspace,
            "--plan-unit", "read=Read a function", "--training-mode", "read=code-reading",
            "--plan-unit", "write=Implement a function", "--training-mode", "write=manual-coding",
            "--requires", "write=read", "--advance",
        )
        materials = {}
        for folder in ("01-lessons", "02-practice"):
            path = workspace / folder / "current.md"
            path.write_text("Actual learner material for " + folder, encoding="utf-8")
            materials[folder] = path.read_bytes()
        self.mark(workspace, READING)
        self.cli(UPDATE, workspace, "--advance")
        state = self.progress(workspace)
        self.assertEqual(state["current_unit"], "write")
        self.assertEqual(state["completed_units"], ["read"])
        self.assertTrue(state["mastery_evidence"]["read"]["impact"])
        self.assertFalse(any(state["mastery_evidence"]["write"].values()))
        for folder, expected in materials.items():
            archived = list((workspace / folder / "archive/read").glob("*.md"))
            self.assertEqual(len(archived), 1)
            self.assertEqual(archived[0].read_bytes(), expected)

    def test_unresolved_reading_gap_prevents_completion(self):
        workspace = self.workspace()
        self.start(workspace)
        self.mark(workspace, READING)
        self.cli(UPDATE, workspace, "--gap", "answer supplied by tutor")
        self.cli(UPDATE, workspace, "--advance", error="unresolved knowledge gaps")
        self.cli(UPDATE, workspace, "--resolve-gap", "answer supplied by tutor", "--advance")
        self.assertEqual(self.progress(workspace)["completed_units"], ["one"])

    def test_block_and_unblock_preserve_reading_evidence(self):
        workspace = self.workspace()
        self.start(workspace)
        self.mark(workspace, READING)
        self.cli(UPDATE, workspace, "--block", "one")
        self.cli(UPDATE, workspace, "--advance", error="is blocked")
        self.cli(UPDATE, workspace, "--unblock", "one", "--review", "independent case verified")
        state = self.progress(workspace)
        self.assertEqual(state["blocked_units"], [])
        self.assertEqual(state["active_units"], ["one"])
        self.assertTrue(all(state["mastery_evidence"]["one"].values()))

    def test_other_training_modes_still_complete_normally(self):
        cases = {
            "conceptual": ("explain", "model", "compare", "apply", "verify"),
            "operational": ("explain", "sequence", "perform", "diagnose", "verify"),
            "architecture": ("explain", "trace", "tradeoff", "design", "verify"),
        }
        for mode, checks in cases.items():
            with self.subTest(mode=mode):
                workspace = self.workspace(mode, mode)
                self.start(workspace)
                self.mark(workspace, checks)
                self.cli(UPDATE, workspace, "--advance", "--finish-topic")
                self.assertEqual(self.progress(workspace)["current_phase"], "complete")

    def test_auto_mode_requires_explicit_unit_mode(self):
        workspace = self.workspace("auto")
        self.cli(UPDATE, workspace, "--plan-unit", "one", error="select --training-mode")
        self.cli(UPDATE, workspace, "--plan-unit", "one", "--training-mode", "one=code-reading", "--advance")
        self.assertEqual(self.progress(workspace)["current_unit"], "one")

    def test_legacy_schema_four_evidence_is_not_reset(self):
        workspace = self.workspace("manual-coding")
        self.start(workspace)
        self.mark(workspace, ["explain", "predict"])
        path = workspace / "04-status/progress.json"
        state = self.progress(workspace)
        state["unit_plan"][0].pop("training_mode")
        path.write_text(json.dumps(state), encoding="utf-8")
        self.cli(UPDATE, workspace, "--review", "legacy learning resumed")
        resumed = self.progress(workspace)
        self.assertEqual(resumed["schema_version"], 4)
        self.assertEqual(resumed["unit_plan"][0]["training_mode"], "manual-coding")
        self.assertEqual(resumed["mastery_evidence"], state["mastery_evidence"])

    def test_completed_history_and_legacy_completion_stay_idempotent(self):
        workspace = self.workspace()
        self.start(workspace)
        self.mark(workspace, READING)
        self.cli(UPDATE, workspace, "--advance")
        self.cli(UPDATE, workspace, "--complete", "one", "--complete", "old-unplanned")
        self.cli(UPDATE, workspace, "--complete", "old-unplanned")
        self.assertEqual(self.progress(workspace)["completed_units"], ["one", "old-unplanned"])

    def test_archive_failure_keeps_current_reading_unit(self):
        workspace = self.workspace()
        self.start(workspace)
        self.mark(workspace, READING)
        before = self.progress(workspace)
        practice = workspace / "02-practice/current.md"
        practice.rename(practice.with_name("held.md"))
        self.cli(UPDATE, workspace, "--advance", error="Cannot archive missing file")
        self.assertEqual(self.progress(workspace), before)


if __name__ == "__main__":
    unittest.main()
