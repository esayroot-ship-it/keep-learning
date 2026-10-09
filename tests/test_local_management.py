"""Local lifecycle checks; every test uses an isolated registry and workspace."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPTS=Path(__file__).resolve().parents[1]/"scripts"
sys.path.insert(0,str(SCRIPTS))
from manage_learning import LocalManager, ManagementError, compact_output, lock_file


class LocalManagementTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix="keep-learning-management-test-")
        self.root=Path(self.temp.name).resolve()
        self.manager=LocalManager(self.root/"registry.json")
        self.addCleanup(self.cleanup)

    def cleanup(self):
        self.assertEqual(self.root.parent,Path(tempfile.gettempdir()).resolve())
        self.assertTrue(self.root.name.startswith("keep-learning-management-test-"))
        self.temp.cleanup()

    def create(self,goal="example",mode="manual-coding"):
        return Path(self.manager.create(goal,self.root/"work",training_mode=mode)["workspace"])

    def start(self,workspace,mode="manual-coding"):
        self.manager.update(workspace,["--plan-unit","one=One unit","--training-mode","one="+mode,"--advance"])

    def progress(self,workspace):
        return json.loads((workspace/"04-status/progress.json").read_text(encoding="utf-8"))

    def test_create_index_and_reselect_without_reset(self):
        one=self.create("first")
        self.start(one)
        self.manager.update(one,["--gap","return value unclear"])
        before=self.progress(one)
        two=self.create("second")
        self.assertEqual(self.manager.resolve(),two)
        self.manager.resume(one)
        self.assertEqual(self.manager.resolve(),one)
        self.assertEqual(self.progress(one),before)
        self.assertTrue((one/"04-status/overview.md").is_file())
        index=self.manager.index()
        self.assertNotIn("completed_units",index["tasks"][0])

    def test_create_never_overwrites_existing_task(self):
        workspace=self.create()
        before=(workspace/"04-status/progress.json").read_bytes()
        with self.assertRaises(ManagementError):self.create()
        self.assertEqual((workspace/"04-status/progress.json").read_bytes(),before)

    def test_note_alone_cannot_mark_mastery(self):
        workspace=self.create()
        self.start(workspace)
        self.manager.record(workspace,"Read the example with help")
        self.assertFalse(any(self.progress(workspace)["mastery_evidence"]["one"].values()))
        self.assertIn("note only",(workspace/"03-evidence/reviewed/one.md").read_text(encoding="utf-8"))

    def test_write_requires_independent_attempt_and_valid_artifact(self):
        workspace=self.create()
        self.start(workspace)
        with self.assertRaises(ManagementError):self.manager.record(workspace,"Copied reference",["write"])
        with self.assertRaises(ManagementError):self.manager.record(workspace,"outside",["write"],"../../outside.py",True)
        artifact=workspace/"03-evidence/submitted/attempt.py"
        artifact.write_text("result = 1",encoding="utf-8")
        self.manager.record(workspace,"Implemented and explained a fresh variant",["write"],"03-evidence/submitted/attempt.py",True)
        self.assertTrue(self.progress(workspace)["mastery_evidence"]["one"]["write"])

    def test_reading_checks_are_mode_specific(self):
        workspace=self.create(mode="code-reading")
        self.start(workspace,"code-reading")
        with self.assertRaises(ManagementError):self.manager.record(workspace,"invalid",["write"],independent=True)
        with self.assertRaises(ManagementError):self.manager.record(workspace,"guided trace",["trace"])
        self.manager.record(workspace,"Independently traced the new path",["trace"],independent=True)
        self.assertTrue(self.progress(workspace)["mastery_evidence"]["one"]["trace"])

    def test_failed_advance_restores_state_and_lesson(self):
        workspace=self.create()
        self.start(workspace)
        before=self.progress(workspace)
        lesson=(workspace/"01-lessons/current.md").read_bytes()
        with self.assertRaises(ManagementError):self.manager.update(workspace,["--advance"])
        self.assertEqual(self.progress(workspace),before)
        self.assertEqual((workspace/"01-lessons/current.md").read_bytes(),lesson)

    def test_complete_checks_advance_archives_and_restore_is_recoverable(self):
        workspace=self.create()
        self.start(workspace)
        for check in ("explain","predict","modify","write","verify"):
            self.manager.record(workspace,"Observed evidence for "+check,[check],independent=True)
        result=self.manager.update(workspace,["--advance"])
        self.assertEqual(self.progress(workspace)["completed_units"],["one"])
        self.assertEqual(len(list((workspace/"01-lessons/archive/one").glob("*.md"))),1)
        self.manager.restore(workspace,result["snapshot"])
        self.assertEqual(self.progress(workspace)["current_unit"],"one")
        self.assertEqual(self.progress(workspace)["completed_units"],[])
        self.assertTrue((workspace/"03-evidence/reviewed/one.md").is_file())

    def test_raw_completion_and_evidence_bypass_are_rejected(self):
        workspace=self.create()
        self.start(workspace)
        for args in (["--complete","one"],["--mastered","write"],["--finish-topic"]):
            with self.subTest(args=args),self.assertRaises(ManagementError):self.manager.update(workspace,args)

    def test_archive_retains_data_and_resume_restores_selection(self):
        workspace=self.create()
        original=self.progress(workspace)
        self.manager.archive(workspace)
        self.assertEqual(self.manager.tasks(),[])
        self.assertTrue(workspace.exists())
        self.assertEqual(len(self.manager.tasks(True)),1)
        self.manager.resume(workspace)
        self.assertEqual(self.progress(workspace),original)
        self.assertFalse(self.manager.tasks()[0]["archived"])

    def test_snapshot_rejects_path_escape_before_any_write(self):
        workspace=self.create()
        self.start(workspace)
        saved=self.manager.snapshot(workspace,"invalid-example")
        data=json.loads(saved.read_text(encoding="utf-8"))
        data["files"]["../escape.md"]="bad"
        saved.write_text(json.dumps(data),encoding="utf-8")
        before=self.progress(workspace)
        with self.assertRaises(ManagementError):self.manager.restore(workspace,saved)
        self.assertEqual(self.progress(workspace),before)
        self.assertFalse((workspace.parent/"escape.md").exists())

    def test_lock_prevents_concurrent_writer(self):
        workspace=self.create()
        target=workspace/"04-status/.management.lock"
        with lock_file(target):
            with self.assertRaises(ManagementError):self.manager.update(workspace,["--gap","busy"])
        self.assertFalse(target.exists())

    def test_cli_forwards_only_arguments_after_separator(self):
        workspace=self.create()
        result=subprocess.run([sys.executable,"-X","utf8",str(SCRIPTS/"manage_learning.py"),
                               "--registry",str(self.manager.registry),"update","--workspace",str(workspace),
                               "--","--plan-unit","one=One unit","--training-mode","one=manual-coding","--advance"],
                              capture_output=True,text=True,encoding="utf-8",timeout=30)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(json.loads(result.stdout)["current_unit"],"one")

    def test_compact_preserves_current_context_without_mutating_result(self):
        workspace=self.create()
        self.start(workspace)
        self.manager.record(workspace,"Explained the example; independent implementation pending",["explain"])
        original=self.manager.status(workspace)
        before=json.dumps(original,sort_keys=True)
        brief=compact_output(original)
        for field in ("goal","phase","current_unit","current_definition","evidence","gaps","next_actions","last_review"):
            self.assertEqual(brief[field],original[field])
        self.assertEqual(brief["completed_count"],len(original["completed_units"]))
        self.assertEqual(Path(brief["path_base"])/brief["paths"]["progress"],Path(original["paths"]["progress"]))
        self.assertEqual(json.dumps(original,sort_keys=True),before)
        self.assertNotIn("completed_units",brief)

    def test_compact_status_cli_keeps_full_default_and_is_read_only(self):
        workspace=self.create()
        self.start(workspace)
        before=self.progress(workspace)
        command=[sys.executable,"-X","utf8",str(SCRIPTS/"manage_learning.py"),"--registry",str(self.manager.registry)]
        full=subprocess.run([*command,"status","--workspace",str(workspace)],capture_output=True,text=True,encoding="utf-8",check=True)
        short=subprocess.run([*command,"--compact","status","--workspace",str(workspace)],capture_output=True,text=True,encoding="utf-8",check=True)
        full_value,short_value=json.loads(full.stdout),json.loads(short.stdout)
        self.assertIn("completed_units",full_value)
        self.assertEqual(full_value["current_definition"],short_value["current_definition"])
        self.assertEqual(full_value["paths"]["progress"],str(workspace/"04-status/progress.json"))
        self.assertEqual(short_value["path_base"],str(workspace))
        self.assertEqual(self.progress(workspace),before)

    def test_compact_update_cli_runs_the_same_transition_and_retains_snapshot(self):
        workspace=self.create()
        result=subprocess.run([sys.executable,"-X","utf8",str(SCRIPTS/"manage_learning.py"),
                               "--registry",str(self.manager.registry),"--compact","update","--workspace",str(workspace),
                               "--","--plan-unit","one=One unit","--training-mode","one=manual-coding","--advance"],
                              capture_output=True,text=True,encoding="utf-8",timeout=30)
        self.assertEqual(result.returncode,0,result.stderr)
        response=json.loads(result.stdout)
        self.assertEqual(response["current_unit"],self.progress(workspace)["current_unit"])
        self.assertTrue(Path(response["snapshot"]).is_file())
        self.assertFalse(any(response["evidence"].values()))

    def test_compact_other_results_preserve_all_fields(self):
        values=[{"id":"task-id","workspace":"path","archived":True},[{"id":"task-id","available":False}]]
        for value in values:
            with self.subTest(value=value):self.assertEqual(compact_output(value),value)


if __name__=="__main__":
    unittest.main()
