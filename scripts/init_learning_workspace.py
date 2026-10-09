#!/usr/bin/env python3
import argparse
import json
import re
from datetime import datetime
from pathlib import Path


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]+", "-", value.strip()).strip("-")
    return slug.lower() or "learning-task"


def write_text(path: Path, content: str, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, value: dict, overwrite: bool) -> None:
    write_text(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n", overwrite)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Initialize a minimal persistent keep-learning workspace."
    )
    parser.add_argument("--root", default="learning-workspace")
    parser.add_argument("--goal", required=True)
    parser.add_argument("--scope", default="bounded development topic")
    parser.add_argument("--duration", default="about 3 hours")
    parser.add_argument("--current-level", default="unassessed")
    parser.add_argument("--mode", default="understand-apply-verify")
    parser.add_argument(
        "--training-mode",
        default="auto",
        choices=["auto", "manual-coding", "code-reading", "conceptual", "operational", "architecture", "mixed"],
    )
    parser.add_argument("--ai-allowance", default="hints-first")
    parser.add_argument(
        "--explanation-detail",
        default="standard",
        choices=["brief", "standard", "detailed"],
    )
    parser.add_argument("--max-new-concepts", type=int, default=1, choices=[1, 2, 3])
    parser.add_argument(
        "--questioning",
        default="adaptive",
        choices=["adaptive", "off"],
    )
    parser.add_argument("--questions-per-round", type=int, default=1, choices=[1, 2, 3])
    parser.add_argument("--rolling-unit-window", type=int, default=5, choices=range(3, 8))
    parser.add_argument(
        "--engineering-expansion",
        default="on-request",
        choices=["on-request", "light", "full"],
    )
    parser.add_argument("--done", action="append", default=[])
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    task = Path(args.root).expanduser() / slugify(args.goal)
    for item in [
        "00-meta",
        "01-lessons",
        "01-lessons/archive",
        "02-practice",
        "02-practice/archive",
        "03-evidence/submitted",
        "03-evidence/reviewed",
        "03-evidence/reference",
        "04-status",
    ]:
        (task / item).mkdir(parents=True, exist_ok=True)

    done_criteria = args.done or [
        "Explain the important knowledge in plain language",
        "Apply it independently using the selected training mode",
        "Pass every mode-specific mastery check",
        "Verify the result against supplied criteria",
    ]
    now = datetime.now().astimezone().isoformat(timespec="seconds")

    config = {
        "schema_version": 4,
        "goal": args.goal,
        "scope": args.scope,
        "duration": args.duration,
        "current_level": args.current_level,
        "mode": args.mode,
        "training_mode": args.training_mode,
        "ai_allowance": args.ai_allowance,
        "preferences": {
            "explanation_detail": args.explanation_detail,
            "pre_question_explanation": "comprehensive-foundation",
            "line_by_line_code_explanation": True,
            "max_new_concepts_per_unit": args.max_new_concepts,
            "practice_sequence": "mode-specific",
            "diagnostic_questioning": {
                "enabled": args.questioning == "adaptive",
                "questions_per_round": args.questions_per_round,
                "file_code_enabled": True,
                "retry_limit": 2,
            },
            "autonomous_progression": {
                "enabled": True,
                "rolling_unit_window": args.rolling_unit_window,
            },
            "engineering_expansion": args.engineering_expansion,
        },
        "done_criteria": done_criteria,
    }
    progress = {
        "schema_version": 4,
        "current_phase": "discovery",
        "current_unit": "",
        "unit_plan": [],
        "mastery_evidence": {},
        "knowledge_gaps": {},
        "completed_units": [],
        "active_units": [],
        "blocked_units": [],
        "next_actions": ["Use known context or one brief capability check, plan a few-hour normal-work route, then select one ready core unit"],
        "last_review": "",
        "updated_at": now,
    }

    write_json(task / "00-meta/learning-config.json", config, args.overwrite)
    write_text(
        task / "01-lessons/current.md",
        "# Current Lesson\n\n"
        "## Design Context\n\n- Reuse known context and make one brief boundary check only when needed.\n"
        "- Select the normal-work scenarios and basic principles; estimate teaching, essential practice and verification within a few hours.\n"
        "- Develop only this core step; keep specialised directions optional.\n\n"
        "- Use only the sections needed for the current gap; this template is not a mandatory report.\n\n"
        "## Goal and Boundary\n\n- Select one bounded concept or code path.\n\n"
        "## Purpose and Prerequisites\n\n- Explain the problem, use, and immediate prerequisites.\n\n"
        "## Mechanism, Syntax, or Procedure\n\n- Explain the required mechanism, model, APIs, or steps.\n\n"
        "## Minimal Example or Demonstration\n\n- Add one relevant example, model, procedure, system view, or code section.\n\n"
        "## Behaviour and Flow\n\n- Explain important elements, sequence, values, inputs, outputs, side effects, and errors.\n\n"
        "## Boundaries and Common Mistakes\n\n- Add one important boundary and common mistake.\n\n"
        "## Verification\n\n- Add exact commands, tests, or observations.\n\n"
        "## Optional Further Directions\n\n- If useful, name up to two topics and when to learn them, one line each. Do not add lessons or tasks.\n",
        args.overwrite,
    )
    write_text(
        task / "02-practice/current.md",
        "# Current Practice\n\n"
        f"- Preferred training mode: {args.training_mode}\n\n"
        "## Mode Selection\n\n- Select one concrete mode: manual-coding, code-reading, conceptual, operational, or architecture.\n\n"
        "## Diagnostic Question\n\n- Ask one focused question using taught concepts.\n\n"
        "## Independent Application\n\n- Define one bounded unworked task and the supplied setup. Keep its solution separate from the teaching example.\n"
        "- For writing, let the learner derive and implement the target logic; for reading, select a source level and support stage without requiring a rewrite.\n\n"
        "## Verification\n\n- Add the selected mode's exact checks; reuse evidence across checks.\n\n"
        "## Evidence Review\n\n- Record the actual answer or artifact, assistance supplied, supported checks, and remaining gap.\n",
        args.overwrite,
    )
    write_json(task / "04-status/progress.json", progress, args.overwrite)
    write_text(
        task / "04-status/next-actions.md",
        "# Next Actions\n\n- Use known context or one brief capability check, plan a few-hour normal-work route, then select one ready core unit\n",
        args.overwrite,
    )
    write_text(task / "04-status/completed.md", "# Completed\n\n- None\n", args.overwrite)
    write_text(task / "04-status/blocked.md", "# Blocked\n\n- None\n", args.overwrite)
    print(task)


if __name__ == "__main__":
    main()
