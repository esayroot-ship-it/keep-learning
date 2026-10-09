# Autonomous Progression

Use this workflow for Mode 2 or Mode 3 after the capability discovery and overall route in `teaching-design.md`. The short rolling queue controls execution; it does not replace planning the path to the user's goal. Keep that route concise in chat unless a durable plan was requested, and generate detailed materials for the current unit when needed.

## Rolling Unit Plan

For an ongoing topic, keep three to seven upcoming units when enough work remains; do not invent filler to reach three for a smaller goal. Each unit has:

```json
{
  "id": "functions-basics",
  "title": "Function definitions and calls",
  "prerequisites": ["variables-and-values"],
  "training_mode": "manual-coding"
}
```

Choose units from the finite core route, the user's goal, current level, target environment, demonstrated gaps, and completed units. Assign each unit one concrete training mode from `training-modes.md` and keep it small enough for that mode's teaching and mastery loop. Use the scope/time budget in `curriculum-quality.md`; extension pointers are not queue entries or unresolved gaps.

Do not write every lesson or enumerate unrelated domain content upfront. Refill the queue only with remaining agreed core outcomes or their necessary gap repairs; do not add deeper theory merely because fewer than two units remain. Use fewer than three near completion. If a prerequisite gap threatens the estimated budget, state the remaining work rather than hiding extra hours or marking it mastered. Replan explicitly when the demonstrated boundary or target changes. Archive applies only to tracked workspaces.

## Completion Gate

A unit is complete only when all five checks for its selected training mode have observable evidence. Read the check sets from `training-modes.md`; do not require `write` for `code-reading` or other non-writing units. Checks may share one artifact; they are not separate homework quotas.

For code units, apply the independence rules in `code-writing.md` or `code-reading.md` before recording passed checks. Store a brief observation, assistance supplied, and answer/artifact reference in the existing reviewed evidence directory. Boolean progress flags record a reviewed judgment; the script does not assess learner answers. Keep already completed history, but do not relabel old guided work as independently verified under the new rules.

Use `--advance` to complete planned units and preserve the evidence/archive gate. Manual `--complete` is reserved for legacy unplanned records or repeating an already recorded completion.

Do not advance while the current unit has an unresolved knowledge gap. Teach the gap, ask an easier verification question, and update the evidence after the learner succeeds.

## Next-Unit Selection

Use this order:

1. continue the current active, non-blocked unit;
2. after completion, choose the first unit in plan order that is not completed or blocked and whose prerequisites are all completed;
3. if no unit is ready but unfinished units remain, mark the learning task blocked and report the unmet prerequisites;
4. if the rolling queue is exhausted but the overall done criteria are not met, extend the queue before continuing;
5. mark the topic complete only after all planned units and the overall done criteria are complete.

For a topic course, reconcile the agreed normal-work scenarios reviewed with `curriculum-quality.md`: every core item needs its intended independent evidence, with core deferrals resolved or the scope explicitly revised. Optional extension directions do not block completion and are not automatically scheduled next. An exhausted queue, boolean progress flags or successful `--finish-topic` command do not independently prove proficiency or a 95% usage-coverage claim.

The user's current request may change the next unit. Record the revised order rather than silently abandoning unfinished units.

## Archive Rule

When a unit passes the completion gate:

1. copy `01-lessons/current.md` to `01-lessons/archive/<unit-id>/<timestamp>.md`;
2. copy `02-practice/current.md` to `02-practice/archive/<unit-id>/<timestamp>.md`;
3. preserve submitted, reviewed, and solution code in their existing folders;
4. mark the unit complete;
5. select the next ready unit;
6. replace both `current.md` files with fresh templates for that next unit.

Never overwrite an existing archive. If archiving fails, do not complete or advance the unit.

## Persistent Commands

Add or update the rolling queue with repeatable unit specifications:

```text
python scripts/update_progress.py <workspace> --plan-unit "variables=Variables and values" --training-mode "variables=conceptual" --plan-unit "functions=Functions" --training-mode "functions=manual-coding" --requires "functions=variables"
```

Record learning evidence and gaps:

```text
python scripts/update_progress.py <workspace> --mastered explain --mastered predict
python scripts/update_progress.py <workspace> --gap "return value versus printed output"
python scripts/update_progress.py <workspace> --resolve-gap "return value versus printed output"
```

Select the first unit or complete and advance the current unit:

```text
python scripts/update_progress.py <workspace> --advance
```

Use `--finish-topic` only when the overall done criteria are also satisfied. For Mode 2 without a workspace, follow the same queue and completion rules in conversation without creating files.
