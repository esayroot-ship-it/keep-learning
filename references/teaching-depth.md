# Teaching Depth

Teach enough basic principle and operation to perform normal work independently within the practical course boundary. Explain the causal step behind a choice or common error; detailed internals are not the default meaning of depth.

Use the capability boundary from `teaching-design.md` and `adaptive-presentation.md` to size the current explanation. Depth, medium, and output length are separate decisions. A short answer can close a small gap; a deeper derivation may need careful text rather than a webpage. For a broad goal, outline the route first and prepare each step when needed; full materials require an explicit request.

Use `curriculum-quality.md` to choose required practical depth and the whole-course time budget. Preserve the causal bridges needed for ordinary tasks; do not add B+ tree internals, MVCC implementation or recovery architecture merely because the product is a database. If such a mechanism is explicitly the learning goal, design its prerequisites and verification rather than just listing its name.

## Explanation Economy

Start from a recognisable task, show the smallest operation or example, explain its result and necessary basic why, then handle a relevant mistake. Explain foundational conventions carefully once; later units reuse them and become more concise. Group tiny related options or shortcuts instead of giving each a full chapter.

Keep a small unit to one behaviour and its immediate prerequisite, normally five to fifteen minutes including essential application. This is a sizing guide, not a reason to pad a short answer or mark unfinished learning complete. Remove secondary examples and deeper theory before compressing the explanation into unexplained fragments. Do not narrate every visible animation step or restate the same idea in several formats.

## Pre-Question Foundation

Before a comprehension question during teaching, explain the prerequisites and reasoning needed for the selected step. This does not apply to design probes of existing knowledge. The learner should not need to guess an untaught term, API, control-flow rule, or hidden dependency in an assigned learning exercise.

Apply this full explanation to teaching examples and guided reading. In independent writing or reading checks, supply the contract and prerequisite facts, then let the learner derive the unworked implementation or trace. Do not reveal its answer merely to satisfy the foundation rule. Follow `code-writing.md` and `code-reading.md` for the boundary.

Use the following as an internal completeness check for the current gap, not as ten mandatory sections. Skip already demonstrated knowledge and irrelevant items; stop when the learner can follow and apply the step:

1. learning goal and the boundary of the current unit;
2. what problem the concept or code solves and when it is used;
3. immediate prerequisite concepts;
4. minimum syntax, APIs, parameters, and return values;
5. a small example, model, demonstration, procedure, system view, or selected real code section;
6. the role of each important element, step, component, function, condition, or decision;
7. execution order, procedure, data or control flow, state changes, inputs, outputs, side effects, and errors;
8. one normal scenario and one important boundary or failure case;
9. common mistakes and how to recognise them;
10. exact commands, tests, assertions, or observations used to verify behaviour.

For a user-specified file, establish its role and directly relevant prerequisites. In guided reading give the selected call-path map; at an independent level ask the learner to reconstruct it, providing only entry or dependency facts their support stage permits. Keep the scope to that path.

## Minimum Coverage for Later Rounds

Use only the items still needed for the current concept; this is not a mandatory outline to repeat in each answer:

1. its purpose in plain language;
2. immediate prerequisites;
3. minimum syntax or API;
4. the smallest relevant example, model, procedure, system view, or code section;
5. important elements explained in behavioural or execution order;
6. values, inputs, outputs, and state changes;
7. one common mistake;
8. how to run and verify the code.

## Depth Levels

- Brief: give the necessary answer and smallest example; add a question only when it helps resolve uncertainty.
- Standard: close the current knowledge gap with the necessary causal explanation, one useful example and adaptive application. This is the default.
- Detailed: explain the selected task's mechanisms, comparisons and common boundaries more carefully; this changes explanation detail, not the course's role scope. Deeper internal derivations require an explicit target or a demonstrated need for the current application.

Do not automatically expand into a complete knowledge map, architecture discussion, multi-project plan, or exhaustive API catalogue. When application fails, teach the smallest missing principle or prerequisite first rather than opening an entire internal subsystem.

## Optional Directions at the End

When useful, end a unit with zero to two brief directions: a topic or lookup term plus when it matters, normally one line each. For example: "Further: B+ tree page splits, when investigating index maintenance or storage-engine behaviour." Do not add a mini-lesson, derivation, extra exercise, webpage or new queue item. Omit the pointers if no useful extension exists; do not invent them for every small question. They are not requirements for completing the current unit.

## Comprehension Check

Before moving on, verify that the learner can:

- describe what the code does without repeating the source verbatim;
- trace important values through the code;
- explain why each important element, step, component, or line exists;
- assess the effect of a proposed change for reading, or implement it safely for writing;
- apply the knowledge independently using the selected training mode;
- verify the result.
