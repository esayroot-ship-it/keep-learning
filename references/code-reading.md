# Graded Code Reading

Use `code-reading` when the goal is to understand existing source, trace behaviour, or assess a proposed change. The learner may answer in prose, a value table, call trace, or short diagram; do not require implementation. If writing is also requested, reuse context in a separate `manual-coding` unit with separate evidence.

## Choose Source Complexity

Select the lowest level that can reveal the learner's current ability and serve their actual goal. Levels describe source complexity, not scores or a mandatory curriculum:

| Level | Material | Reading outcome |
| --- | --- | --- |
| 1 | Expression or short sequential block | Explain the purpose and determine intermediate values and output. |
| 2 | One function with branches, loops, or a relevant exception | Trace normal and boundary paths, return values, mutations, and errors. |
| 3 | Several functions in one file | Locate the entry, reconstruct calls, and follow arguments, results, and shared state. |
| 4 | One bounded path across directly related files | Follow imports and calls, identify I/O and side effects, and explain relevant dependency contracts. |
| 5 | An unfamiliar implementation plus a requirement, failure, or diff | Locate the relevant path, support a diagnosis or impact assessment with code, and propose a verification check. |

Increase one major difficulty dimension at a time: path count, call depth, state, dependency distance, or unfamiliar organisation. Source length alone is not a level. Do not introduce an untaught language feature or framework mechanism just to make reading harder.

For a large requested file, preserve its real context but choose one useful path at the learner's level. AI reads the actual source first and identifies the exact file, function, and relevant lines. Resolve unknown callees or clearly state what cannot be inferred; do not invent behaviour from names.

## Reduce Help Without Hiding Prerequisites

1. **Guided:** explain the required concepts and fully trace a small worked example or one representative path.
2. **Cued:** provide the entry point and necessary API or dependency facts; let the learner derive another path or case.
3. **Independent:** provide an unworked snippet, path, or behaviour-changing variant using known concepts and the task context. Let the learner locate and explain the relevant flow without revealing its trace, output, defect, or impact first.

Use only the support stages needed. Existing evidence can justify starting independently. If the exact code has already been fully explained, use an unworked variant for independent evidence. Reading unfamiliar code must not require guessing unfamiliar syntax.

Do not label repetition of the AI's explanation as independent reading. If help reveals the decisive answer, review it as guided practice and use a fresh small variant to check independence. If the learner asks for direct explanation, give it and leave independent reading unverified. After two misses on the same point, explain and reduce the difficulty or isolate the missing prerequisite.

## Evidence Contract

Use `explain`, `trace`, `predict`, `impact`, and `verify`. One source and a small case or proposed change can cover all five; ask one primary question at a time rather than presenting a five-part exam.

| Check | Required observation |
| --- | --- |
| `explain` | Learner states the purpose and input/output contract, with source-based justification. |
| `trace` | Learner independently reconstructs an unworked case's relevant execution and value/state changes, including an applicable alternate or boundary path. |
| `predict` | Learner predicts output, return value, mutation, or error for a stated unworked input before seeing execution results. |
| `impact` | Learner reasons about the effect and limits of a small proposed code or contract change; no patch is required. At level 1, an operator or condition change is sufficient. |
| `verify` | Learner checks the explanation against code and relevant assertions, tests, logs, a debugger, or an explicit manual trace, correcting discrepancies. Distinguish observed behaviour from inference. |

All checks need learner-produced evidence. They may reuse evidence from the guided stages, but require at least one unworked case in which the learner independently explains/traces the flow and predicts or assesses its changed behaviour before calling the unit mastered. Do not mark these checks merely because AI ran the code or the learner agreed with an explanation.

## Progression and Review

Increase difficulty only after the learner completes the selected level's independent check and resolves current gaps. Advance one level or one complexity dimension when the goal requires it; staying at the level needed for the requested file is valid. Do not equate a passed short snippet with whole-project reading ability.

Keep the current level, support stage, selected source, and remaining gap in the existing practice material. For persistent tasks, record the actual answer or artifact reference and assistance in `03-evidence/reviewed/<unit-id>.md` using a filesystem-safe ID. Use the existing progress checks and next action; no separate reading roadmap or numeric assessment is needed.

Example: teach early returns with one function, then give a different small function using the same constructs. Ask the learner to trace an empty input and predict the return value. Next ask what would change if a boundary condition moved. Validate the explanation with a manual trace or safe execution; do not require rewriting the function.
