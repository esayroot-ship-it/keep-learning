# Persistent Workspace

Use a workspace only when the user explicitly asks for saved progress, a multi-session task, or continuation of an existing learning task.

Use `local-management.md` and `scripts/manage_learning.py` for reusable local lifecycle management. The central registry indexes task paths and selection only; this workspace retains its canonical configuration, state and evidence. A skill-management change is not a request to instantiate a particular subject's learning project.

## Load Order and Data Ownership

Use these sources in order:

1. the user's current request overrides saved preferences for the current turn;
2. `00-meta/learning-config.json` is the only persisted source for goals, preferences, and done criteria;
3. skill defaults apply when neither source specifies a value.

`04-status/progress.json` is the only persisted source for operational state. Never copy learning configuration into it. `next-actions.md`, `completed.md`, and `blocked.md` are generated views of `progress.json`, not independent data sources.

For a legacy workspace without `learning-config.json`, read the old `learning-parameters.json` and configuration fields in `progress.json` once, write `learning-config.json`, and remove duplicated configuration fields from `progress.json`. Do not keep synchronising two configuration formats.

## Resume Rule

When the user asks to continue:

1. use the local task index or the user's explicit path to find/select the matching workspace;
2. read `00-meta/learning-config.json`;
3. read `04-status/progress.json`, falling back to legacy `06-status/progress.json`;
4. continue the current active unit, or the first next action if no unit is active;
5. do not reset progress unless requested.

The management `resume` command regenerates `overview.md` without changing learning evidence. Read the source files and relevant review notes returned by it before teaching; an overview is only a generated view.

For a new task, the initial phase is `discovery` and unknown ability is `unassessed`. Keep the capability summary and overall route in existing lesson/review materials rather than adding a parallel state system. Reuse prior evidence when continuing; ask only about gaps that change the next step. Advancing to an active unit does not itself prove discovery or mastery.

## Minimal Layout

```text
learning-workspace/<task-slug>/
  00-meta/
    learning-config.json
  01-lessons/
    current.md
    archive/
  02-practice/
    current.md
    archive/
  03-evidence/
    submitted/
    reviewed/
    reference/
  04-status/
    progress.json
    next-actions.md
    completed.md
    blocked.md
    overview.md
    history.jsonl
    backups/
```

Add a roadmap, project folders, or assessments only when the user explicitly requests them.

## Progress Schema

```json
{
  "schema_version": 4,
  "current_phase": "discovery",
  "current_unit": "",
  "unit_plan": [],
  "mastery_evidence": {},
  "knowledge_gaps": {},
  "completed_units": [],
  "active_units": [],
  "blocked_units": [],
  "next_actions": [],
  "last_review": "",
  "updated_at": ""
}
```

A unit must appear in at most one of `completed_units`, `active_units`, and `blocked_units`. `unit_plan` defines order and prerequisites without duplicating runtime status. `mastery_evidence` and `knowledge_gaps` are keyed by unit ID. Use `scripts/update_progress.py` for transitions, archives, autonomous advancement, and generated status views.

For managed tasks, invoke transitions through `manage_learning.py` so the update is locked, preceded by a snapshot and accompanied by reviewed notes where appropriate. `overview.md` and Markdown status lists are regenerated; history/backups do not replace `progress.json`.

`code-reading` is supported as a concrete unit mode within schema 4; it uses `explain/trace/predict/impact/verify`. Existing modes keep their check names and saved history. For code units, keep brief observed evidence and assistance notes in `03-evidence/reviewed/`; progress flags are the operational state, not proof of an independent attempt. Complete planned units with `--advance`; `--complete` cannot newly complete a planned unit.
