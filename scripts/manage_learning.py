"""Local task index, evidence records and recoverable updates for keep-learning."""
import argparse
from contextlib import contextmanager
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import uuid

import init_learning_workspace as initializer
import update_progress as progress_tool


class ManagementError(Exception):
    pass


def compact_output(value):
    """Optional presentation only; never mutate the manager result or saved state."""
    if not isinstance(value, dict) or "current_unit" not in value or "paths" not in value:
        return value
    fields = ("workspace", "goal", "phase", "current_unit", "current_definition",
              "evidence", "gaps", "next_actions", "updated_at", "last_review", "snapshot")
    result = {key:value[key] for key in fields if key in value}
    for name in ("completed", "active", "blocked"):
        result[name + "_count"] = len(value.get(name + "_units", []))
    workspace = Path(value["workspace"])
    result["paths"] = {}
    for name in ("config", "progress", "lesson", "practice", "reviewed"):
        if name in value["paths"]:
            path = Path(value["paths"][name])
            try:
                result["paths"][name] = path.relative_to(workspace).as_posix()
            except ValueError:
                result["paths"][name] = str(path)
    result["path_base"] = value["workspace"]
    return result


def now():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


@contextmanager
def lock_file(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError as exc:
        raise ManagementError(f"Another update holds {path}; retry after it finishes") from exc
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump({"pid":os.getpid(),"started_at":now()}, stream)
        yield
    finally:
        path.unlink(missing_ok=True)


def run_helper(name, args):
    result = subprocess.run(
        [sys.executable, "-X", "utf8", str(Path(__file__).with_name(name)), *map(str,args)],
        capture_output=True, text=True, encoding="utf-8", timeout=30,
    )
    if result.returncode:
        raise ManagementError(result.stderr.strip() or result.stdout.strip())


class LocalManager:
    def __init__(self, registry=None):
        codex_dir = Path(os.environ.get("CODEX_HOME", Path.home()/".codex")).expanduser()
        self.registry = Path(registry).expanduser().resolve() if registry else codex_dir/"learning"/"registry.json"

    def index(self):
        if not self.registry.is_file():
            return {"schema_version":1,"active_task":"","tasks":[]}
        data = read_json(self.registry)
        if not isinstance(data,dict) or not isinstance(data.get("tasks"),list):
            raise ManagementError("Invalid local learning registry")
        return data

    def register(self, workspace, activate=True):
        workspace = Path(workspace).expanduser().resolve()
        progress_tool.find_status_dir(workspace)
        identifier = hashlib.sha256(str(workspace).casefold().encode()).hexdigest()[:12]
        with lock_file(self.registry.with_suffix(".lock")):
            data = self.index()
            task = next((x for x in data["tasks"] if x["id"]==identifier),None)
            if task is None:
                task = {"id":identifier,"workspace":str(workspace),"registered_at":now(),"archived":False}
                data["tasks"].append(task)
            if activate:
                task["archived"] = False
                task["last_used"] = now()
                data["active_task"] = identifier
            progress_tool.atomic_write_json(self.registry,data)
        return identifier

    def resolve(self, workspace=None, task_id=None):
        if workspace:
            result = Path(workspace).expanduser().resolve()
        else:
            data = self.index()
            selector = task_id or data.get("active_task")
            task = next((x for x in data["tasks"] if x["id"]==selector),None)
            if task is None:
                raise ManagementError("No selected learning task; use list, create or register")
            result = Path(task["workspace"]).resolve()
        try:
            progress_tool.find_status_dir(result)
        except FileNotFoundError as exc:
            raise ManagementError(f"Workspace unavailable: {result}; register its new path if moved") from exc
        return result

    def create(self, goal, root, current_level="unassessed", training_mode="auto"):
        workspace = Path(root).expanduser().resolve()/initializer.slugify(goal)
        if workspace.exists():
            raise ManagementError(f"Workspace already exists; register/resume it without resetting: {workspace}")
        run_helper("init_learning_workspace.py",[
            "--root",workspace.parent,"--goal",goal,"--current-level",current_level,
            "--training-mode",training_mode,
        ])
        self.register(workspace)
        return self.render_overview(workspace)

    def status(self, workspace):
        workspace = Path(workspace).resolve()
        status_dir = progress_tool.find_status_dir(workspace)
        progress = read_json(status_dir/"progress.json")
        config_path = workspace/"00-meta/learning-config.json"
        config = read_json(config_path) if config_path.is_file() else {}
        current = progress.get("current_unit","")
        definition = next((u for u in progress.get("unit_plan",[]) if u["id"]==current),None)
        paths = {
            "config":str(config_path),"progress":str(status_dir/"progress.json"),
            "lesson":str(workspace/"01-lessons/current.md"),
            "practice":str(workspace/"02-practice/current.md"),
            "next_actions":str(status_dir/"next-actions.md"),
            "reviewed":str(workspace/"03-evidence/reviewed"),
            "overview":str(status_dir/"overview.md"),
        }
        return {"workspace":str(workspace),"goal":config.get("goal",progress.get("goal",workspace.name)),
                "phase":progress.get("current_phase",""),"current_unit":current,
                "current_definition":definition,"evidence":progress.get("mastery_evidence",{}).get(current,{}),
                "gaps":progress.get("knowledge_gaps",{}).get(current,[]),
                "completed_units":progress.get("completed_units",[]),"active_units":progress.get("active_units",[]),
                "blocked_units":progress.get("blocked_units",[]),"next_actions":progress.get("next_actions",[]),
                "updated_at":progress.get("updated_at",""),"last_review":progress.get("last_review",""),
                "paths":paths}

    def tasks(self, include_archived=False):
        data = self.index()
        rows=[]
        for task in data["tasks"]:
            if task.get("archived") and not include_archived:
                continue
            try:
                state=self.status(Path(task["workspace"]))
                rows.append({"id":task["id"],"workspace":task["workspace"],"goal":state["goal"],
                             "phase":state["phase"],"current_unit":state["current_unit"],
                             "completed_count":len(state["completed_units"]),"archived":task.get("archived",False),
                             "selected":task["id"]==data.get("active_task"),"available":True})
            except (FileNotFoundError,ValueError):
                rows.append({"id":task["id"],"workspace":task["workspace"],"available":False,
                             "archived":task.get("archived",False)})
        return rows

    def render_overview(self, workspace):
        state=self.status(workspace)
        labels={"config":"学习配置","progress":"真实进度数据","lesson":"当前教材","practice":"当前练习",
                "next_actions":"下一步","reviewed":"学习证据与评阅","overview":"学习概览"}
        parts=["# 学习概览",f"- 目标：{state['goal']}",f"- 当前阶段：{state['phase']}",
               f"- 当前单元：{state['current_unit'] or '尚未选择'}",
               f"- 已完成的登记单元：{len(state['completed_units'])}",
               f"- 最近更新：{state['updated_at']}",
               "\n这是由进度生成的视图。完成单元或登记检查不等于已经精通整个领域。",
               "\n## 下一步",*["- "+x for x in state["next_actions"] or ["暂无"]],
               "\n## 当前检查",*[f"- {key}：{'已登记通过' if value else '尚未验证'}" for key,value in state["evidence"].items()],
               "\n## 当前知识缺口",*["- "+x for x in state["gaps"] or ["暂无登记"]],
               "\n## 本地入口",*[f"- [{labels[key]}](<{Path(value).as_posix()}>)" for key,value in state["paths"].items()]]
        progress_tool.atomic_write_text(Path(state["paths"]["overview"]),"\n".join(parts)+"\n")
        return state

    def snapshot(self, workspace, operation):
        status_dir=progress_tool.find_status_dir(workspace)
        paths=[workspace/"00-meta/learning-config.json",workspace/"01-lessons/current.md",
               workspace/"02-practice/current.md",*[status_dir/name for name in
               ("progress.json","next-actions.md","completed.md","blocked.md","overview.md")]]
        files={p.relative_to(workspace).as_posix():p.read_text(encoding="utf-8") for p in paths if p.is_file()}
        stamp=datetime.now().astimezone().strftime("%Y%m%dT%H%M%S%f")+"-"+uuid.uuid4().hex[:6]
        target=status_dir/"backups"/(stamp+".json")
        progress_tool.atomic_write_json(target,{"workspace":str(workspace),"created_at":now(),
                                               "operation":operation,"files":files})
        return target

    def restore_files(self, workspace, snapshot):
        data=read_json(snapshot)
        if not isinstance(data,dict) or not isinstance(data.get("files"),dict):
            raise ManagementError("Invalid snapshot format")
        if data.get("workspace")!=str(workspace):
            raise ManagementError("Snapshot belongs to a different workspace")
        allowed={"00-meta/learning-config.json","01-lessons/current.md","02-practice/current.md"}
        for folder in ("04-status","06-status"):
            allowed.update(f"{folder}/{name}" for name in
                           ("progress.json","next-actions.md","completed.md","blocked.md","overview.md"))
        for relative,text in data["files"].items():
            target=(workspace/relative).resolve()
            if relative not in allowed or not target.is_relative_to(workspace):
                raise ManagementError("Snapshot contains an invalid restoration path")
            if not isinstance(text,str):
                raise ManagementError("Snapshot file contents must be text")
        for relative,text in data["files"].items():
            progress_tool.atomic_write_text(workspace/relative,text)

    def mutate(self, workspace, operation, action):
        workspace=Path(workspace).resolve()
        status_dir=progress_tool.find_status_dir(workspace)
        with lock_file(status_dir/".management.lock"):
            saved=self.snapshot(workspace,operation)
            try:
                action()
                state=self.render_overview(workspace)
                with (status_dir/"history.jsonl").open("a",encoding="utf-8") as stream:
                    stream.write(json.dumps({"at":now(),"operation":operation,"snapshot":str(saved),
                                             "current_unit":state["current_unit"]},ensure_ascii=False)+"\n")
            except Exception:
                self.restore_files(workspace,saved)
                raise
        state["snapshot"]=str(saved)
        return state

    def update(self, workspace, arguments):
        if not arguments:
            raise ManagementError("Supply an update action")
        if any(a.split("=",1)[0] in {"--mastered","--complete","--finish-topic"} for a in arguments):
            raise ManagementError("Use record for passed checks and --advance for completion; whole-goal completion needs a coverage review")
        return self.mutate(workspace,"update",lambda:run_helper("update_progress.py",[workspace,*arguments]))

    def record(self, workspace, text, checks=(), artifact=None, independent=False):
        text=text.strip()
        if not text:
            raise ManagementError("A factual evidence/review note is required")
        state=self.status(workspace)
        unit=state["current_unit"]
        if checks and not unit:
            raise ManagementError("Select a current unit before recording passed checks")
        definition=state["current_definition"]
        if checks and definition is None:
            raise ManagementError("Current unit is not in the plan")
        if checks:
            invalid=set(checks)-set(progress_tool.required_checks(definition))
            if invalid:
                raise ManagementError("Checks do not match the unit mode: "+", ".join(sorted(invalid)))
        needs_independence = "write" in checks or (
            "trace" in checks and definition is not None and definition.get("training_mode")=="code-reading"
        )
        if needs_independence and not independent:
            raise ManagementError("write/trace requires an explicitly independent attempt; otherwise save a note only")
        if artifact:
            artifact_path=(Path(workspace)/artifact).resolve()
            if not artifact_path.is_relative_to(Path(workspace).resolve()) or not artifact_path.is_file():
                raise ManagementError("Artifact must be an existing file inside the learning workspace")
        def action():
            args=[workspace,"--review",text]
            for check in dict.fromkeys(checks):
                args.extend(["--mastered",check])
            run_helper("update_progress.py",args)
            review=Path(workspace)/"03-evidence/reviewed"/(progress_tool.safe_unit_slug(unit or "task-notes")+".md")
            entry=f"\n## {now()}\n\n{text}\n\n- Recorded checks: {', '.join(dict.fromkeys(checks)) or 'none; note only'}\n- Independent attempt declared: {independent}\n- Artifact: {artifact or 'answer described in note'}\n"
            review.parent.mkdir(parents=True,exist_ok=True)
            with review.open("a",encoding="utf-8") as stream:
                stream.write(entry)
        return self.mutate(workspace,"record",action)

    def restore(self, workspace, snapshot):
        candidate=Path(snapshot).expanduser().resolve()
        backups=progress_tool.find_status_dir(workspace)/"backups"
        if not candidate.is_relative_to(backups.resolve()) or not candidate.is_file():
            raise ManagementError("Choose an existing snapshot from this task's backups")
        return self.mutate(workspace,"restore",lambda:self.restore_files(workspace,candidate))

    def resume(self, workspace):
        self.register(workspace)
        with lock_file(progress_tool.find_status_dir(workspace)/".management.lock"):
            return self.render_overview(workspace)

    def archive(self, workspace, archived=True):
        identifier=self.register(workspace,activate=False)
        with lock_file(self.registry.with_suffix(".lock")):
            data=self.index()
            next(t for t in data["tasks"] if t["id"]==identifier)["archived"]=archived
            if archived and data.get("active_task")==identifier:
                data["active_task"]=""
            progress_tool.atomic_write_json(self.registry,data)
        return {"id":identifier,"archived":archived,"workspace":str(workspace)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry",help="Optional index path; default is CODEX_HOME/learning/registry.json")
    parser.add_argument("--compact",action="store_true",help="Compact response only; saved data and update gates are unchanged")
    sub=parser.add_subparsers(dest="command",required=True)
    create=sub.add_parser("create")
    create.add_argument("--goal",required=True)
    create.add_argument("--root",default="learning-workspace")
    create.add_argument("--current-level",default="unassessed")
    create.add_argument("--training-mode",default="auto",choices=sorted(progress_tool.CONFIG_TRAINING_MODES))
    listing=sub.add_parser("list")
    listing.add_argument("--all",action="store_true")
    for name in ("register","status","resume","update","record","restore","archive","unarchive"):
        item=sub.add_parser(name)
        item.add_argument("--workspace",help="Explicit task path; otherwise use --task or the selected task")
        item.add_argument("--task",help="Task id from list")
        if name=="update":
            item.add_argument("arguments",nargs=argparse.REMAINDER)
        if name=="record":
            item.add_argument("--text",required=True)
            item.add_argument("--check",action="append",default=[],choices=progress_tool.EVIDENCE_CHECKS)
            item.add_argument("--artifact")
            item.add_argument("--independent",action="store_true")
        if name=="restore":
            item.add_argument("--snapshot",required=True)
    args=parser.parse_args()
    manager=LocalManager(args.registry)
    try:
        if args.command=="create":
            result=manager.create(args.goal,args.root,args.current_level,args.training_mode)
        elif args.command=="list":
            result=manager.tasks(args.all)
        else:
            workspace=manager.resolve(args.workspace,args.task)
            if args.command=="register":result={"id":manager.register(workspace),"workspace":str(workspace)}
            elif args.command=="status":result=manager.status(workspace)
            elif args.command=="resume":result=manager.resume(workspace)
            elif args.command=="update":
                arguments=args.arguments[1:] if args.arguments[:1]==["--"] else args.arguments
                result=manager.update(workspace,arguments)
            elif args.command=="record":result=manager.record(workspace,args.text,args.check,args.artifact,args.independent)
            elif args.command=="restore":result=manager.restore(workspace,args.snapshot)
            else:result=manager.archive(workspace,args.command=="archive")
        if args.compact:
            print(json.dumps(compact_output(result),ensure_ascii=False,separators=(",",":")))
        else:
            print(json.dumps(result,ensure_ascii=False,indent=2))
    except (ManagementError,ValueError,FileNotFoundError) as exc:
        parser.exit(2,str(exc)+"\n")


if __name__=="__main__":
    main()
