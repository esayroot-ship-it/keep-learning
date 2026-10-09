#!/usr/bin/env python3
import argparse
import json
import re
import shutil
from datetime import datetime
from pathlib import Path


CONFIG_FIELDS = {
    "goal",
    "scope",
    "duration",
    "current_level",
    "mode",
    "training_mode",
    "ai_allowance",
    "learning_parameters",
    "done_criteria",
}
TRAINING_MODE_CHECKS = {
    "manual-coding": ("explain", "predict", "modify", "write", "verify"),
    "code-reading": ("explain", "trace", "predict", "impact", "verify"),
    "conceptual": ("explain", "model", "compare", "apply", "verify"),
    "operational": ("explain", "sequence", "perform", "diagnose", "verify"),
    "architecture": ("explain", "trace", "tradeoff", "design", "verify"),
}
CONFIG_TRAINING_MODES = set(TRAINING_MODE_CHECKS) | {"auto", "mixed"}
EVIDENCE_CHECKS = tuple(
    dict.fromkeys(check for checks in TRAINING_MODE_CHECKS.values() for check in checks)
)


def normalize_training_mode(value, default="manual-coding") -> str:
    return value if value in TRAINING_MODE_CHECKS else default


def required_checks(unit: dict) -> tuple[str, ...]:
    return TRAINING_MODE_CHECKS[normalize_training_mode(unit.get("training_mode"))]


def unique_strings(values) -> list[str]:
    result = []
    for value in values if isinstance(values, list) else []:
        if isinstance(value, str) and value and value not in result:
            result.append(value)
    return result


def normalize_unit_plan(value) -> list[dict]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError("unit_plan must be a JSON array")
    result = []
    seen = set()
    for item in value:
        if not isinstance(item, dict):
            raise ValueError("each unit_plan item must be a JSON object")
        unit_id = item.get("id")
        if not isinstance(unit_id, str) or not unit_id.strip():
            raise ValueError("each unit_plan item needs a non-empty string id")
        unit_id = unit_id.strip()
        if unit_id in seen:
            raise ValueError(f"duplicate unit id in unit_plan: {unit_id}")
        seen.add(unit_id)
        title = item.get("title", unit_id)
        if not isinstance(title, str) or not title.strip():
            title = unit_id
        result.append(
            {
                "id": unit_id,
                "title": title.strip(),
                "prerequisites": unique_strings(item.get("prerequisites", [])),
                "training_mode": normalize_training_mode(item.get("training_mode")),
            }
        )
    return result


def normalize_mastery_evidence(value) -> dict[str, dict[str, bool]]:
    if not isinstance(value, dict):
        return {}
    result = {}
    for unit_id, evidence in value.items():
        if isinstance(unit_id, str) and isinstance(evidence, dict):
            result[unit_id] = {
                check: bool(value)
                for check, value in evidence.items()
                if check in EVIDENCE_CHECKS
            }
    return result


def normalize_knowledge_gaps(value) -> dict[str, list[str]]:
    if not isinstance(value, dict):
        return {}
    return {
        unit_id: unique_strings(gaps)
        for unit_id, gaps in value.items()
        if isinstance(unit_id, str)
    }


def atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(path)


def atomic_write_json(path: Path, value: dict) -> None:
    atomic_write_text(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def safe_unit_slug(unit_id: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff._-]+", "-", unit_id).strip("-.")
    return slug or "learning-unit"


def current_lesson_template(unit_id: str, title: str, training_mode: str) -> str:
    return (
        "# Current Lesson\n\n"
        f"- Unit ID: {unit_id}\n"
        f"- Title: {title}\n"
        f"- Training mode: {training_mode}\n\n"
        "- Use only the sections needed for the current gap; this template is not a mandatory report.\n\n"
        "## Goal and Boundary\n\n- Define this bounded unit.\n\n"
        "## Purpose and Prerequisites\n\n- Explain the problem, use, and immediate prerequisites.\n\n"
        "## Mechanism, Syntax, or Procedure\n\n- Explain the required mechanism, model, APIs, or steps.\n\n"
        "## Minimal Example or Demonstration\n\n- Add one relevant example, model, procedure, system view, or code section.\n\n"
        "## Behaviour and Flow\n\n- Explain important elements, sequence, values, inputs, outputs, side effects, and errors.\n\n"
        "## Boundaries and Common Mistakes\n\n- Add one important boundary and common mistake.\n\n"
        "## Verification\n\n- Add exact commands, tests, or observations.\n"
    )


def current_practice_template(unit_id: str, title: str, training_mode: str) -> str:
    activities = {
        "manual-coding": (
            "## Independent Implementation\n\n"
            "- State one unworked requirement, input/output contract, and supplied setup.\n"
            "- Learner proposes steps and implements the target logic without solution-bearing help.\n"
            "- Before running, predict a normal and applicable boundary case.\n\n"
            "## Transfer\n\n"
            "- Apply one meaningful changed requirement to the same artifact only if that evidence is still missing.\n"
            "- A copied or assisted solution needs a fresh small independent variant before write can pass.\n"
        ),
        "code-reading": (
            "## Reading Scope\n\n"
            "- Select the source file/function, complexity level (1-5), and support stage (guided/cued/independent).\n\n"
            "## Independent Reading\n\n"
            "- Use taught constructs in an unworked case. Let the learner explain and trace before revealing the answer.\n"
            "- Predict behaviour and assess a small proposed change; no implementation is required.\n"
            "- Ask one primary question at a time and reuse the trace across checks.\n"
        ),
        "conceptual": "## Model\n\n- Reconstruct the concept.\n\n## Compare\n\n- Distinguish it from an alternative.\n\n## Apply\n\n- Apply it to a new scenario.\n",
        "operational": "## Sequence\n\n- Order the steps safely.\n\n## Perform\n\n- Perform or dry-run the operation.\n\n## Diagnose\n\n- Diagnose a realistic failure.\n",
        "architecture": "## Trace\n\n- Trace an important flow.\n\n## Tradeoff\n\n- Evaluate a design choice.\n\n## Design\n\n- Produce or revise a bounded design.\n",
    }[training_mode]
    evidence_review = (
        "\n## Evidence Review\n\n"
        "- Record answer/artifact references, actual assistance, independently supported checks, and the remaining gap.\n"
        "- Keep a brief factual review in 03-evidence/reviewed using a filesystem-safe unit ID.\n"
        if training_mode in {"manual-coding", "code-reading"}
        else ""
    )
    return (
        "# Current Practice\n\n"
        f"- Unit ID: {unit_id}\n"
        f"- Title: {title}\n"
        f"- Training mode: {training_mode}\n\n"
        "## Diagnostic Question\n\n- Ask one focused question about the taught material.\n\n"
        f"{activities}\n"
        "## Verify\n\n- Add exact evidence and checks.\n"
        f"{evidence_review}"
    )


def write_current_templates(workspace: Path, unit_id: str, title: str, training_mode: str) -> None:
    if not unit_id:
        for folder, heading in (("01-lessons", "Lesson"), ("02-practice", "Practice")):
            atomic_write_text(
                workspace / folder / "current.md",
                f"# Current {heading}\n\nNo active unit. Follow 04-status/next-actions.md.\n",
            )
        return
    atomic_write_text(
        workspace / "01-lessons/current.md",
        current_lesson_template(unit_id, title, training_mode),
    )
    atomic_write_text(
        workspace / "02-practice/current.md",
        current_practice_template(unit_id, title, training_mode),
    )


def archive_current_unit(workspace: Path, unit_id: str) -> None:
    timestamp = datetime.now().astimezone().strftime("%Y%m%dT%H%M%S%f%z")
    slug = safe_unit_slug(unit_id)
    sources = [
        (workspace / "01-lessons/current.md", workspace / "01-lessons/archive"),
        (workspace / "02-practice/current.md", workspace / "02-practice/archive"),
    ]
    prepared = []
    try:
        for source, archive_root in sources:
            if not source.is_file():
                raise FileNotFoundError(f"Cannot archive missing file: {source}")
            destination_dir = archive_root / slug
            destination_dir.mkdir(parents=True, exist_ok=True)
            destination = destination_dir / f"{timestamp}.md"
            if destination.exists():
                raise FileExistsError(f"Refusing to overwrite archive: {destination}")
            temporary = destination.with_name(destination.name + ".tmp")
            shutil.copy2(source, temporary)
            prepared.append((temporary, destination))
        for temporary, destination in prepared:
            temporary.replace(destination)
    finally:
        for temporary, _ in prepared:
            if temporary.exists():
                temporary.unlink()


def plan_lookup(unit_plan: list[dict]) -> dict[str, dict]:
    return {unit["id"]: unit for unit in unit_plan}


def add_plan_specs(
    unit_plan,
    plan_specs,
    requirement_specs,
    training_specs,
    default_training_mode,
    completed,
    parser,
):
    lookup = plan_lookup(unit_plan)
    for spec in plan_specs:
        unit_id, separator, title = spec.partition("=")
        unit_id = unit_id.strip()
        title = title.strip() if separator else unit_id
        if not unit_id:
            parser.error("--plan-unit requires ID or ID=Title")
        if unit_id in lookup:
            if separator and title:
                lookup[unit_id]["title"] = title
        else:
            unit = {
                "id": unit_id,
                "title": title or unit_id,
                "prerequisites": [],
                "training_mode": default_training_mode,
            }
            unit_plan.append(unit)
            lookup[unit_id] = unit

    for spec in requirement_specs:
        unit_id, separator, raw_prerequisites = spec.partition("=")
        unit_id = unit_id.strip()
        if not separator or not unit_id or unit_id not in lookup:
            parser.error("--requires needs an existing planned unit as ID=PREREQ1,PREREQ2")
        prerequisites = unique_strings(
            [item.strip() for item in raw_prerequisites.split(",") if item.strip()]
        )
        lookup[unit_id]["prerequisites"] = prerequisites

    for spec in training_specs:
        unit_id, separator, mode = spec.partition("=")
        unit_id = unit_id.strip()
        mode = mode.strip()
        if not separator or not unit_id or unit_id not in lookup:
            parser.error("--training-mode needs an existing planned unit as ID=MODE")
        if mode not in TRAINING_MODE_CHECKS:
            parser.error(
                "--training-mode MODE must be " + ", ".join(TRAINING_MODE_CHECKS)
            )
        lookup[unit_id]["training_mode"] = mode

    missing_modes = [unit["id"] for unit in unit_plan if not unit.get("training_mode")]
    if missing_modes:
        parser.error(
            "select --training-mode ID=MODE for new units when task training_mode is auto or mixed: "
            + ", ".join(missing_modes)
        )

    known = set(lookup) | set(completed)
    for unit in unit_plan:
        unknown = [item for item in unit["prerequisites"] if item not in known]
        if unknown:
            parser.error(
                f"unit {unit['id']!r} has unknown prerequisites: {', '.join(unknown)}"
            )

    visiting = set()
    visited = set()

    def visit(unit_id):
        if unit_id in visiting:
            parser.error(f"unit_plan contains a prerequisite cycle at {unit_id!r}")
        if unit_id in visited or unit_id not in lookup:
            return
        visiting.add(unit_id)
        for prerequisite in lookup[unit_id]["prerequisites"]:
            visit(prerequisite)
        visiting.remove(unit_id)
        visited.add(unit_id)

    for unit_id in lookup:
        visit(unit_id)


def select_next_unit(unit_plan, completed, blocked):
    completed_set = set(completed)
    blocked_set = set(blocked)
    for unit in unit_plan:
        unit_id = unit["id"]
        if unit_id in completed_set or unit_id in blocked_set:
            continue
        if all(item in completed_set for item in unit["prerequisites"]):
            return unit
    return None


def remaining_units(unit_plan, completed):
    completed_set = set(completed)
    return [unit for unit in unit_plan if unit["id"] not in completed_set]


def blocked_plan_message(unit_plan, completed, blocked):
    completed_set = set(completed)
    blocked_set = set(blocked)
    details = []
    for unit in unit_plan:
        if unit["id"] in completed_set:
            continue
        missing = [item for item in unit["prerequisites"] if item not in completed_set]
        reasons = []
        if unit["id"] in blocked_set:
            reasons.append("unit is blocked")
        if missing:
            reasons.append("missing prerequisites: " + ", ".join(missing))
        if reasons:
            details.append(f"{unit['id']} ({'; '.join(reasons)})")
    return "No ready unit: " + "; ".join(details)


def find_status_dir(workspace: Path) -> Path:
    current = workspace / "04-status"
    legacy = workspace / "06-status"
    if (current / "progress.json").is_file():
        return current
    if (legacy / "progress.json").is_file():
        return legacy
    raise FileNotFoundError(
        f"No progress.json found under {current} or legacy path {legacy}"
    )


def migrate_config(workspace: Path, progress: dict) -> None:
    config_path = workspace / "00-meta/learning-config.json"
    if config_path.is_file():
        config = json.loads(config_path.read_text(encoding="utf-8"))
        if not isinstance(config, dict):
            raise ValueError(f"Expected a JSON object in {config_path}")
        original_config = json.dumps(config, ensure_ascii=False, sort_keys=True)
        preferences = config.setdefault("preferences", {})
        if not isinstance(preferences, dict):
            raise ValueError(f"Expected preferences to be an object in {config_path}")
        preferences.setdefault(
            "pre_question_explanation", "comprehensive-foundation"
        )
        preferences.setdefault(
            "diagnostic_questioning",
            {
                "enabled": True,
                "questions_per_round": 1,
                "file_code_enabled": True,
                "retry_limit": 2,
            },
        )
        preferences.setdefault(
            "autonomous_progression",
            {"enabled": True, "rolling_unit_window": 5},
        )
        config.setdefault("training_mode", "auto")
        config.setdefault("current_level", "unassessed")
        preferences.setdefault("practice_sequence", "mode-specific")
        if config.get("training_mode") not in CONFIG_TRAINING_MODES:
            config["training_mode"] = "auto"
        config["schema_version"] = 4
        if json.dumps(config, ensure_ascii=False, sort_keys=True) != original_config:
            atomic_write_json(config_path, config)
        for field in CONFIG_FIELDS:
            progress.pop(field, None)
        return

    legacy_parameters_path = workspace / "00-meta/learning-parameters.json"
    legacy_parameters = {}
    if legacy_parameters_path.is_file():
        loaded = json.loads(legacy_parameters_path.read_text(encoding="utf-8"))
        if isinstance(loaded, dict):
            legacy_parameters = loaded
    embedded_parameters = progress.get("learning_parameters", {})
    if not isinstance(embedded_parameters, dict):
        embedded_parameters = {}
    parameters = {**embedded_parameters, **legacy_parameters}

    old_depth = parameters.get("depth", "standard")
    explanation_detail = {
        "brief": "brief",
        "standard": "standard",
        "deep": "detailed",
        "expert": "detailed",
    }.get(old_depth, "standard")
    old_expansion = parameters.get("engineering_expansion", "on-request")
    engineering_expansion = {
        "none": "on-request",
        "auto": "on-request",
    }.get(old_expansion, old_expansion)
    if engineering_expansion not in {"on-request", "light", "full"}:
        engineering_expansion = "on-request"
    max_concepts = parameters.get("max_new_concepts_per_lesson", 1)
    if not isinstance(max_concepts, int) or isinstance(max_concepts, bool):
        max_concepts = 1
    max_concepts = min(3, max(1, max_concepts))

    config = {
        "schema_version": 4,
        "goal": progress.get("goal", ""),
        "scope": progress.get("scope", "bounded development topic"),
        "duration": progress.get("duration", "flexible"),
        "current_level": progress.get("current_level", "unassessed"),
        "mode": "understand-apply-verify",
        "training_mode": "auto",
        "ai_allowance": "hints-first",
        "preferences": {
            "explanation_detail": explanation_detail,
            "pre_question_explanation": "comprehensive-foundation",
            "line_by_line_code_explanation": True,
            "max_new_concepts_per_unit": max_concepts,
            "practice_sequence": "mode-specific",
            "diagnostic_questioning": {
                "enabled": True,
                "questions_per_round": 1,
                "file_code_enabled": True,
                "retry_limit": 2,
            },
            "autonomous_progression": {
                "enabled": True,
                "rolling_unit_window": 5,
            },
            "engineering_expansion": engineering_expansion,
        },
        "done_criteria": unique_strings(progress.get("done_criteria", [])),
    }
    atomic_write_json(config_path, config)
    for field in CONFIG_FIELDS:
        progress.pop(field, None)


def remove(items: list[str], value: str) -> None:
    while value in items:
        items.remove(value)


def add(items: list[str], value: str) -> None:
    if value and value not in items:
        items.append(value)


def render_list(title: str, items: list[str]) -> str:
    body = "\n".join(f"- {item}" for item in items) if items else "- None"
    return f"# {title}\n\n{body}\n"


def sync_views(status_dir: Path, progress: dict) -> None:
    atomic_write_text(
        status_dir / "next-actions.md",
        render_list("Next Actions", progress["next_actions"]),
    )
    atomic_write_text(
        status_dir / "completed.md",
        render_list("Completed", progress["completed_units"]),
    )
    atomic_write_text(
        status_dir / "blocked.md",
        render_list("Blocked", progress["blocked_units"]),
    )


def validate_transition_conflicts(parser, transitions: dict[str, list[str]]) -> None:
    owners: dict[str, str] = {}
    for state, units in transitions.items():
        for unit in units:
            previous = owners.get(unit)
            if previous and previous != state:
                parser.error(
                    f"unit {unit!r} cannot transition to both {previous} and {state}"
                )
            owners[unit] = state


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Update keep-learning progress with mutually exclusive unit states."
    )
    parser.add_argument("workspace")
    parser.add_argument("--phase")
    parser.add_argument("--unit")
    parser.add_argument(
        "--complete", action="append", default=[],
        help="Complete a legacy unplanned record; use --advance for planned units.",
    )
    parser.add_argument("--active", action="append", default=[])
    parser.add_argument("--block", action="append", default=[])
    parser.add_argument("--unblock", action="append", default=[])
    parser.add_argument("--next", action="append", default=[])
    parser.add_argument("--review")
    parser.add_argument(
        "--plan-unit",
        action="append",
        default=[],
        help="Append or rename a rolling-plan unit as ID or ID=Title.",
    )
    parser.add_argument(
        "--requires",
        action="append",
        default=[],
        help="Set prerequisites as ID=PREREQ1,PREREQ2.",
    )
    parser.add_argument(
        "--training-mode",
        action="append",
        default=[],
        help="Set a planned unit mode as ID=" + "|".join(TRAINING_MODE_CHECKS) + ".",
    )
    parser.add_argument(
        "--mastered",
        action="append",
        default=[],
        choices=EVIDENCE_CHECKS,
        help="Record a passed mastery check for the current unit.",
    )
    parser.add_argument("--gap", action="append", default=[])
    parser.add_argument("--resolve-gap", action="append", default=[])
    parser.add_argument(
        "--advance",
        action="store_true",
        help="Complete and archive the current unit, then select the next ready unit.",
    )
    parser.add_argument(
        "--finish-topic",
        action="store_true",
        help="Mark the topic complete after all planned units and done criteria pass.",
    )
    args = parser.parse_args()

    if args.advance and any(
        [args.complete, args.active, args.block, args.unblock, args.unit is not None, args.next]
    ):
        parser.error(
            "--advance cannot be combined with manual state transitions, --unit, or --next"
        )

    workspace = Path(args.workspace).expanduser()
    status_dir = find_status_dir(workspace)
    progress_path = status_dir / "progress.json"
    progress = json.loads(progress_path.read_text(encoding="utf-8"))
    if not isinstance(progress, dict):
        raise ValueError(f"Expected a JSON object in {progress_path}")

    transitions = {
        "completed": unique_strings(args.complete),
        "active": unique_strings(args.active),
        "blocked": unique_strings(args.block),
        "unblocked": unique_strings(args.unblock),
    }
    validate_transition_conflicts(parser, transitions)
    migrate_config(workspace, progress)
    config_path = workspace / "00-meta/learning-config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    configured_training_mode = config.get("training_mode", "auto")
    default_training_mode = (
        configured_training_mode
        if configured_training_mode in TRAINING_MODE_CHECKS
        else None
    )

    completed = unique_strings(progress.get("completed_units", []))
    active = unique_strings(progress.get("active_units", []))
    blocked = unique_strings(progress.get("blocked_units", []))
    unit_plan = normalize_unit_plan(progress.get("unit_plan", []))
    mastery_evidence = normalize_mastery_evidence(
        progress.get("mastery_evidence", {})
    )
    knowledge_gaps = normalize_knowledge_gaps(progress.get("knowledge_gaps", {}))
    add_plan_specs(
        unit_plan,
        args.plan_unit,
        args.requires,
        args.training_mode,
        default_training_mode,
        completed,
        parser,
    )
    lookup = plan_lookup(unit_plan)
    manual_planned_completions = [
        unit for unit in transitions["completed"]
        if unit in lookup and unit not in completed
    ]
    if manual_planned_completions:
        parser.error(
            "planned units require mastery checks and archiving; use --advance instead of --complete: "
            + ", ".join(manual_planned_completions)
        )
    if args.finish_topic and not unit_plan:
        parser.error("cannot finish a topic with an empty unit_plan")

    current_unit = progress.get("current_unit", "")
    if not isinstance(current_unit, str):
        current_unit = ""
    current_unit = current_unit.strip()
    if (args.mastered or args.gap or args.resolve_gap) and not current_unit:
        parser.error("mastery evidence and knowledge gaps require a current unit")
    if current_unit:
        current_definition = lookup.get(
            current_unit,
            {"training_mode": "manual-coding"},
        )
        current_checks = required_checks(current_definition)
        invalid_checks = [check for check in args.mastered if check not in current_checks]
        if invalid_checks:
            parser.error(
                f"mastery checks not valid for {current_definition['training_mode']}: "
                + ", ".join(invalid_checks)
            )
        current_evidence = mastery_evidence.setdefault(
            current_unit, {}
        )
        for check in current_checks:
            current_evidence.setdefault(check, False)
        for check in args.mastered:
            current_evidence[check] = True
        current_gaps = knowledge_gaps.setdefault(current_unit, [])
        for gap in unique_strings(args.gap):
            add(current_gaps, gap)
        for gap in unique_strings(args.resolve_gap):
            remove(current_gaps, gap)

    for unit in transitions["active"]:
        remove(completed, unit)
        remove(blocked, unit)
        add(active, unit)
    for unit in transitions["blocked"]:
        remove(completed, unit)
        remove(active, unit)
        add(blocked, unit)
    for unit in transitions["unblocked"]:
        remove(blocked, unit)
        if unit not in completed:
            add(active, unit)
    for unit in transitions["completed"]:
        remove(active, unit)
        remove(blocked, unit)
        add(completed, unit)

    if args.phase:
        progress["current_phase"] = args.phase
    if args.unit is not None:
        current_unit = args.unit.strip()
    elif current_unit in completed:
        current_unit = active[0] if active else ""

    if args.advance:
        if not unit_plan:
            parser.error("unit_plan is empty; add at least one --plan-unit before advancing")
        if current_unit:
            if current_unit not in lookup:
                parser.error(
                    f"current unit {current_unit!r} is not present in unit_plan"
                )
            if current_unit in blocked:
                parser.error(f"current unit {current_unit!r} is blocked")
            evidence = mastery_evidence.setdefault(
                current_unit, {}
            )
            checks = required_checks(lookup[current_unit])
            for check in checks:
                evidence.setdefault(check, False)
            missing_checks = [check for check in checks if not evidence[check]]
            if missing_checks:
                parser.error(
                    "cannot advance; missing mastery evidence: "
                    + ", ".join(missing_checks)
                )
            unresolved = knowledge_gaps.get(current_unit, [])
            if unresolved:
                parser.error(
                    "cannot advance; unresolved knowledge gaps: "
                    + "; ".join(unresolved)
                )
            if args.finish_topic:
                all_unresolved = [
                    f"{unit_id}: {gap}"
                    for unit_id, gaps in knowledge_gaps.items()
                    for gap in gaps
                ]
                if all_unresolved:
                    parser.error(
                        "cannot finish topic with unresolved knowledge gaps: "
                        + "; ".join(all_unresolved)
                    )
            hypothetical_completed = completed + [current_unit]
            if args.finish_topic and remaining_units(unit_plan, hypothetical_completed):
                parser.error(
                    "cannot finish topic while planned units remain incomplete"
                )
            archive_current_unit(workspace, current_unit)
            remove(active, current_unit)
            remove(blocked, current_unit)
            add(completed, current_unit)
            current_unit = ""

        next_unit = select_next_unit(unit_plan, completed, blocked)
        if next_unit:
            if args.finish_topic:
                parser.error("cannot finish topic while a ready planned unit remains")
            current_unit = next_unit["id"]
            active = [current_unit]
            progress["current_phase"] = "learning"
            progress["next_actions"] = [f"Study {next_unit['title']}"]
            mastery_evidence.setdefault(
                current_unit, {check: False for check in required_checks(next_unit)}
            )
            knowledge_gaps.setdefault(current_unit, [])
            write_current_templates(
                workspace,
                current_unit,
                next_unit["title"],
                next_unit["training_mode"],
            )
        else:
            active = []
            current_unit = ""
            remaining = remaining_units(unit_plan, completed)
            if remaining:
                if args.finish_topic:
                    parser.error("cannot finish topic while planned units remain incomplete")
                progress["current_phase"] = "blocked"
                progress["next_actions"] = [
                    blocked_plan_message(unit_plan, completed, blocked)
                ]
            elif args.finish_topic:
                progress["current_phase"] = "complete"
                progress["next_actions"] = []
            else:
                progress["current_phase"] = "planning"
                progress["next_actions"] = [
                    "Extend the rolling unit plan or confirm the overall done criteria"
                ]
            write_current_templates(workspace, "", "No active unit", "manual-coding")

    if args.finish_topic and not args.advance:
        if current_unit:
            parser.error("cannot finish topic while a current unit is active")
        if remaining_units(unit_plan, completed):
            parser.error("cannot finish topic while planned units remain incomplete")
        unresolved = [
            f"{unit_id}: {gap}"
            for unit_id, gaps in knowledge_gaps.items()
            for gap in gaps
        ]
        if unresolved:
            parser.error(
                "cannot finish topic with unresolved knowledge gaps: "
                + "; ".join(unresolved)
            )
        progress["current_phase"] = "complete"
        progress["next_actions"] = []

    progress["schema_version"] = 4
    progress["current_unit"] = current_unit
    progress["unit_plan"] = unit_plan
    progress["mastery_evidence"] = mastery_evidence
    progress["knowledge_gaps"] = knowledge_gaps
    progress["completed_units"] = completed
    progress["active_units"] = active
    progress["blocked_units"] = blocked
    if not args.advance and not args.finish_topic:
        progress["next_actions"] = (
            unique_strings(args.next)
            if args.next
            else unique_strings(progress.get("next_actions", []))
        )
    if args.review is not None:
        progress["last_review"] = args.review
    else:
        progress.setdefault("last_review", "")
    progress["updated_at"] = datetime.now().astimezone().isoformat(timespec="seconds")

    atomic_write_json(progress_path, progress)
    sync_views(status_dir, progress)
    print(progress_path)


if __name__ == "__main__":
    main()
