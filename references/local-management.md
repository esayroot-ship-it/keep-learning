# Local Learning Management

Use this workflow when the user wants saved learning projects, convenient local progress updates, or cross-session continuation. It is a reusable skill capability, not an instruction to create a subject project while editing the skill. A skill-management request alone creates no learner task. Keep all work in the current agent.

## Storage and Ownership

- The user/project chooses the learning root; default to `learning-workspace/<goal-slug>/` under the working directory when creating an authorised task.
- `00-meta/learning-config.json` owns durable goals, preferences and done criteria. The user's current request can temporarily override it without silently changing saved preferences.
- `04-status/progress.json` owns current units, checks, gaps and runtime status. A full teaching route or coverage map belongs in the existing metadata/lesson materials, not copied into progress as a second plan state.
- `03-evidence/submitted/` and `reviewed/` hold the learner's actual artifacts and factual review notes.
- Keep the approved route/content allocation in a linked Markdown plan within the task's metadata or lessons. Use `current.md` for the editable current step and its archives for completed historical versions. Generate an interactive scene under `01-lessons/visuals/` only when the learning step needs it; link the scene and its Markdown with the same unit ID. Do not create empty files for every future unit or duplicate editable lesson bodies.
- `next-actions.md`, `completed.md`, `blocked.md` and `overview.md` are generated views. Never use them as independent state or mark learning complete because a file exists.
- `04-status/backups/` stores update snapshots; `history.jsonl` records the operation and snapshot path. They are recovery/audit data, not the current truth.
- The central index is `$CODEX_HOME/learning/registry.json`, falling back to `~/.codex/learning/registry.json`. It stores workspace identity/path, selection and archive metadata only. Counts, goals and status are read from each actual workspace; do not duplicate them in the registry.

## Use the Management Entry Point

`scripts/manage_learning.py` wraps the existing initializer and progress transitions. It uses Python's standard library, outputs structured JSON for the assistant, preserves the canonical schema, and does not require a web server. Markdown views are the low-cost local viewing surface; create an additional interface only when the user requests one.

For PowerShell or CMD, run the following examples from this skill repository or installation directory. From another working directory, use the absolute path to your own installed script:

```text
python -X utf8 "scripts/manage_learning.py" list
python -X utf8 "scripts/manage_learning.py" status
python -X utf8 "scripts/manage_learning.py" resume
```

`list` discovers only registered tasks and computes their actual status. `status` reads the selected task without changing learning state. `resume` selects it and regenerates the overview; read the returned configuration, progress, current lesson/practice, next action and relevant evidence before continuing. It does not reset progress or restart the full capability interview.

For a new explicitly authorised learning task, use `create --goal <goal> --root <root>`, with the confirmed level and task-level training mode when available. An existing path is rejected rather than overwritten. Use `register --workspace <path>` to adopt an existing compatible workspace, then resume it. A task ID from `list` can be selected with `--task`; an explicit path can be supplied with `--workspace`.

## Save Meaningful Work

After an answer, artifact review, diagnosed gap, or revised next action, update the local task before ending the teaching turn. Record only what happened; do not set mastery flags just because the material was produced or read.

```text
python -X utf8 "scripts/manage_learning.py" record --workspace "<workspace>" --text "<factual note>"
python -X utf8 "scripts/manage_learning.py" record --workspace "<workspace>" --text "<reviewed independent evidence>" --check write --independent --artifact "03-evidence/submitted/attempt.py"
python -X utf8 "scripts/manage_learning.py" update --workspace "<workspace>" -- --gap "<specific missing concept>" --next "<one concrete next action>"
python -X utf8 "scripts/manage_learning.py" update --workspace "<workspace>" -- --advance
```

Use structured process arguments or tool inputs for learner text; never interpolate answers into shell code. The path placeholders above must be replaced with a real authorised workspace. The script's `--registry` override is useful for isolated tests or a deliberately chosen index; it does not move the learning files.

A note without `--check` does not establish mastery. A passed check needs a nonempty factual note and must match the unit's training mode. `write` and an independent `code-reading` trace require `--independent`; supplying decisive help makes that attempt assisted. This declaration records a reviewed judgment, not an automatic ability assessment. Referenced artifacts must exist within the task.

Use `update` for queue, dependency, gap, block/unblock and next-action transitions; arguments after `--` go to the existing progress helper. The management entry point rejects raw `--mastered`, `--complete` and `--finish-topic` bypasses. Record evidence first, then use the normal advance gate. Ending a whole topic additionally needs the curriculum coverage and overall done-criteria review; the helper's flags alone do not prove it.

## Recovery, Relocation and Archiving

Every management update takes a snapshot of canonical state and current materials before the transition. An unsuccessful transition restores those files. Successful operations record the snapshot path and regenerate views. Exclusive lock files prevent overlapping writers using this entry point; do not edit progress concurrently through another tool.

`restore --workspace <path> --snapshot <snapshot-path>` restores a validated snapshot from that task's backup directory and takes another snapshot first. It restores state/current materials, retains submitted evidence and archives, and does not claim post-snapshot work never happened. Review the retained notes before continuing.

If an interrupted process leaves a lock, inspect its PID and confirm that writer has stopped before removing the named lock file. Do not silently discard it or reset the workspace. If a workspace moved, register the new path; an unavailable index entry is reported as unavailable, not completed.

`archive` hides the task in the index without moving or deleting its files; `list --all` includes it. `unarchive` unhides it, and `resume` makes it current again. These are learning-project operations, not Codex task/thread operations. Never remove a user's old learning task merely to get a clean start.

Do not create a subject project, webpage or learning content merely to demonstrate this management capability. Verify changes with temporary registries and temporary workspaces, then deliver the reusable tool and workflow.
