# Independent Code Writing

Use for `manual-coding` units. The outcome is an implementation derived from requirements, using taught concepts, with the learner able to explain and verify their choices.

## Minimum Effective Task

- Choose one bounded behaviour and one main knowledge point. Prefer one expression, function, query, or small patch when it can demonstrate the goal.
- Supply imports, fixtures, invocation code, environment setup, and unrelated boilerplate. Leave the target decisions and implementation to the learner; do not supply their algorithm as a skeleton.
- State the contract: inputs, outputs, relevant constraints, allowed concepts, and observable acceptance criteria. The learner briefly restates it and proposes their own steps or data representation before coding; a few sentences are enough.
- Teach with a separate worked example. The independent task changes a meaningful condition, input shape, or application; renaming variables or changing constants alone does not establish transfer.
- Default to one independent implementation with a small changed requirement applied to it. If existing work already supplies the same evidence, reuse it instead of adding another exercise.
- One artifact and discussion may satisfy several mastery checks. Do not turn five checks into five mandatory assignments, impose line-count targets, or require a project for a small concept.
- Stop when all relevant evidence is present and no knowledge gap remains. Add an exercise only to resolve a specific gap or meet an explicit broader goal.

## Independence and Help

Separate supported practice from the independent attempt. Before the attempt, teach missing concepts and make the contract unambiguous. During it, permit documentation or syntax lookup that does not supply the solution; independent work is not API memorisation.

Ask for the learner's attempt or current reasoning before giving task-specific help. If needed, escalate from a conceptual cue to pseudocode, then a partial implementation. Give the full solution when requested, or when an attempted task needs a worked correction. Do not require repeated failure before helping.

Supplying the target algorithm, decisive branch, pseudocode, core skeleton, or generated implementation makes that attempt assisted. Running or retyping it does not satisfy `write`. After explanation, offer one fresh, equally small variant using the same taught concepts; mark independence only after that attempt succeeds without solution-bearing help. Record a declined attempt as unverified, not failed or mastered.

## Evidence Contract

Keep the existing five check names; these are evidence categories, not a fixed exercise sequence:

| Check | Required observation |
| --- | --- |
| `explain` | Learner identifies the contract, explains their decomposition and important implementation choices in their own words. |
| `predict` | Before execution, learner reasons through a representative input and an applicable boundary case. |
| `write` | Learner implements the target logic from requirements on an unworked task, without copying or receiving its solution. |
| `modify` | Learner independently adapts to one meaningful changed requirement, or demonstrates equivalent transfer in already submitted work. |
| `verify` | Learner selects or justifies checks, states expected results, examines actual behaviour, and corrects any revealed error with an explanation. |

Provide a test harness when writing one is outside the learning goal. Include a normal case and a relevant boundary or failure case; do not demand artificial errors where the contract has none. The learner must understand the expected outcomes. AI-only tests and an unexplained green result do not establish `verify`. If code cannot run, label a manual trace as provisional execution evidence and leave runtime-dependent verification pending.

When code fails, ask the learner to compare expected and actual behaviour and locate a likely cause before supplying a repair. If that requires untaught knowledge, teach it first and narrow the task.

## Compact Review

State what the learner did independently, what help was supplied, which checks the artifact supports, and the smallest remaining gap. For persistent tasks, retain a short factual note and artifact or answer reference in `03-evidence/reviewed/<unit-id>.md` using a filesystem-safe ID; do not create another score system. Mark `--mastered` only after reviewing the corresponding observation, then advance through the normal gate.

Example: after teaching a list filter, ask for a function that selects records matching a stated condition. Supply sample records and the invocation harness. Let the learner choose the expression, handle the empty input, and later adjust one selection rule. Reuse that function and its explanation for the checks rather than assigning a separate script per check.
