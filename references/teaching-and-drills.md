# Teaching and Application Loop

## One Learning Unit

After brief capability discovery and the practical route in `teaching-design.md`, use this sequence adaptively for the current step. A simple direct answer does not require the whole loop:

1. Define the bounded concept and its purpose.
2. Explain the immediate prerequisites and minimum syntax or APIs.
3. Show the smallest relevant example, model, demonstration, procedure, system view, or code section.
   Use `adaptive-presentation.md` when an interactive state, timeline, or parameter experiment would make the mechanism clearer than text.
4. Explain the structure, flow, values and errors needed for this gap, reusing already demonstrated knowledge without repeating it.
5. State its normal use, important boundary, one common mistake, and exact verification method.
6. Ask one focused question using `diagnostic-questioning.md` only after this foundation is complete.
7. Use the answer to explain every still-uncertain point without repeating mastered material.
8. Ask one verification question or request one small mode-appropriate change.
9. Assign an unworked activity using taught concepts, following `code-writing.md` or `code-reading.md` for code tasks. Let the learner supply the target reasoning or implementation before reviewing it.
10. Supply exact criteria, commands, observations, assertions, scenarios, or tests for verification.
11. Review the attempt, explain the smallest missing point, and let the learner retry.

Do not add another concept until the learner passes every mastery check for the selected training mode.

These steps are an adaptive teaching loop, not a quota of exercises or separate question rounds. A single practical attempt and review can provide several observations. Reuse an artifact or answer across checks; skip already demonstrated activities and work only on remaining gaps. Keep worked teaching examples separate from independent checks. Budget the required practice inside the short course, without weakening its independence gates.

At the unit's end, follow `teaching-depth.md` for zero to two brief extension directions when useful. Do not expand them into content, homework, webpages or new queued units.

Complete means the current reasoning bridge or bounded behaviour is understandable and verifiable. Do not dump the rest of the topic, insist on every explanatory section, or create a document or page for a resolved small question.

## Exercise Shape

Keep each exercise concise:

```text
goal:
task:
allowed concepts:
input/output or behaviour:
checks:
supplied setup and learner-owned work:
```

Add more hints only when requested or when review shows the learner is stuck.

## Code Practice Rules

- Follow `code-writing.md` for requirements-to-implementation practice, help boundaries, and writing evidence.
- Follow `code-reading.md` for source complexity, decreasing help, and independent traces without mandatory coding.
- Provide setup and unrelated boilerplate. Prefer standard-library examples unless the target requires a dependency.
- Give a full explanation or solution when requested. Treat the resulting work as assisted; offer a fresh small variant if independent mastery is still the goal.

For other modes, follow `training-modes.md` and review the relevant model, operation record, diagnosis, decision table, diagram, or design artifact.

## Review

Separate review into:

- understanding: can the learner explain the knowledge and reason about behaviour?
- application: does the mode-appropriate work satisfy the checks?
- independence: which decisions did the learner make, and what solution-bearing help was supplied?
- scope: did the task accidentally require an untaught concept?

For verbal answers, explicitly separate what the learner understood from the smallest missing or uncertain point. Do not assign a numeric score.

Respond with the smallest correction that allows another attempt. Avoid turning a small application mistake into a broad curriculum.
