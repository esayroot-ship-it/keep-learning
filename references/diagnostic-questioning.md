# Diagnostic Questioning

Use questions to discover what the learner does not yet understand. Treat the exchange as diagnosis and teaching, not as an exam.

## Distinguish Design from Teaching

Before designing a new learning path, use the brief discovery limit in `teaching-design.md`: one short round, with one clarification only if needed to choose the starting point or scope. Do not explain the probe's answer first or generate the whole course while waiting. A "not learned" answer is enough to choose a foundational start, not a reason for a longer assessment.

The foundation-first rules below apply to checks during teaching, after the path has been chosen. Keep these checks focused on the current taught step; do not repeat the full design interview each round.

## Choose the Learning Source

- Lesson code: give the comprehensive bounded foundation and example before asking about it.
- User-specified file: read the requested file first and establish its role and prerequisites. In guided reading explain the selected path; in an independent reading check let the learner derive it. Read only directly relevant imports, definitions, tests, or callers needed for that path.
- Learner-written code: ensure the relevant concepts were taught, then ask about intended behaviour, expected results, and one concrete implementation choice before supplying an explanation or correction that would reveal the answer.
- Non-coding material: use the smallest relevant model, diagram, trace, procedure, interface state, configuration, log, decision, or scenario. Explain it before asking the learner to reason about or apply it.

For a local file, identify the exact file and tight line range or function under discussion. Do not turn file-based learning into an unrelated repository audit.

Use `code-reading.md` to distinguish guided teaching from independent source analysis and `code-writing.md` for independent implementation. Teaching the required concepts does not require disclosing the answer to the later unworked task.

## Question Ladder

Start at the lowest level that can reveal understanding:

1. Purpose: what does this function, block, or expression do?
2. Trace: in what order does it run, and how do important values change?
3. Prediction: what output, return value, state change, or error will occur?
4. Reasoning: why is this syntax, API, step, mechanism, component, or decision used here?
5. Change: what effect would a proposed change have, or what small edit or action would produce a specified behaviour? Reading-only work may answer in words.
6. Independent application: can the learner code, model, perform, diagnose, or design an equivalent case without copying?

Do not jump to architecture or design questions when the learner is still uncertain about syntax or execution flow.

## One Round

1. Show or reference the smallest relevant code section, model, procedure, trace, system view, or artifact.
2. Confirm that the pre-question foundation covered every concept needed to answer.
3. Ask one primary question by default; ask at most three closely related questions.
4. Wait for the learner's answer before explaining the answer.
5. Classify the evidence as understood, partially understood, missing prerequisite, or implementation mistake.
6. Confirm what was correct, then explain only the smallest missing knowledge point.
7. Ask one easier verification question or request one small mode-appropriate application.
8. End the round once the question is resolved; complete the unit only after the selected mode's checks and independence requirements are satisfied. Do not repeat all checks every round.

If the learner answers incorrectly twice on the same point, lower the difficulty and explain it directly before asking again. If they say they do not know, explain without pressure. If they ask for direct explanation or no questions, respect that preference.

## Good Question Properties

- Answerable from the shown code and already taught context.
- Focused on one observable concept.
- Has a concrete basis in execution, values, behaviour, or code structure.
- Reveals a likely knowledge gap rather than testing trivia.
- Leads naturally to an explanation or small mode-appropriate action.

Avoid ambiguous style questions, hidden prerequisites, trick questions, long quizzes, repeated questions after mastery, and asking the learner to guess framework internals that were not taught.

## Knowledge-Gap Response

After an answer, state briefly:

```text
understood:
missing or uncertain:
explanation:
verification question or code change:
```

Do not persist a score. For a tracked task, record only the current missing concept or completed learning unit when it affects the next session.
