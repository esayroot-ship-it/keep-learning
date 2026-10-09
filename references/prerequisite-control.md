# Prerequisite Control

Before asking a comprehension question during teaching or assigning an activity, list internally the concepts, APIs, tools, procedures, and design ideas it requires. Each must be one of:

- already understood or confirmed by the learner;
- taught in the current unit;
- unavoidable setup that is supplied without becoming part of the exercise.

If the question or task requires an untaught concept, explain that concept first or reduce its scope. A wrong answer caused by a hidden prerequisite is a teaching-design error, not evidence that the learner failed. Do not create a formal prerequisite map for ordinary conversational learning.

Design probes in `teaching-design.md` serve a different purpose: they may ask whether a relevant target or prerequisite is understood before teaching it, accept "not learned", and adapt to that answer. They are not graded exercises and do not authorise assigning untaught implementations. Mark an unassessed prerequisite as unknown until evidence is available.

For a persistent task, record only the small current set in the lesson file:

```text
already understood:
current concept:
not ready yet:
```

For manual coding, adapt support to the remaining gap:

1. predict or modify a taught example when guided practice is needed;
2. have the learner derive and implement a small unworked requirement;
3. test a meaningful variation in the same artifact when transfer remains unverified;
4. combine concepts only after the learner succeeds independently.

Reuse existing evidence rather than requiring every activity again. For `code-reading`, use the source-complexity and support progression in `code-reading.md`; for other modes, use `training-modes.md`. Apply the same prerequisite rule throughout. An unworked implementation may use familiar constructs: unfamiliar source is not permission to test untaught syntax, tools, or domain rules.

When reviewing, decide whether an error comes from missing understanding, missing prerequisite knowledge, or an implementation mistake. Fix only that gap before retrying.
