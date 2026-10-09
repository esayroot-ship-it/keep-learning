# Task Model

## Choose the Smallest Mode

- Mode 0, direct answer: answer a simple question with one minimal example and no files.
- Mode 1, learning unit: identify the specific gap with existing evidence or one focused design question, then teach-apply-review. Select a training mode with `training-modes.md`. This includes focused learning from a user-specified file and is the normal learning mode.
- Mode 2, bounded topic: use `teaching-design.md` to discover the relevant ability boundary and outline the overall dependency route in conversation; then maintain a rolling execution queue with `autonomous-progression.md`. Do not create files unless requested or needed for an explicitly requested artifact.
- Mode 3, persistent task: create or resume a local workspace, persist the rolling unit queue, and archive completed units when the user explicitly asks for multi-day tracking, saved progress, or continuation across sessions.

These modes control task size and persistence. Separately select `manual-coding`, `code-reading`, `conceptual`, `operational`, or `architecture` practice for each unit. Advanced topics do not automatically require a heavy workflow.

Modes 2 and 3 use the few-hours practical scope in `curriculum-quality.md`: normal work for a stated role, common scenarios and basic principles. Saving progress does not widen the syllabus. A request to learn a product defaults to its routine use in the requested role; an explicit specialist topic gets its own bounded route. Extension directions are outside the active unit plan and done criteria unless selected by the user.

## Information Needed

For Modes 1 and 2, infer only what is needed now:

- the code or concept to understand;
- the user-specified file or code section, when provided;
- the learner's demonstrated ability on the relevant prerequisites, gaps, and unassessed branches;
- the target runtime, framework version, operating environment, or project context when it affects runnable code;
- whether they want hints or a full example;
- for code, whether the goal is independent writing, reading, or both; infer this from the request without requiring a questionnaire;
- whether the subject can be authentically practised through code, or needs conceptual, operational, architecture, or mixed training.

For Mode 3, record goal, current level, approximate duration, AI-answer allowance, learning preferences, and measurable done criteria in `00-meta/learning-config.json`. Infer conservative defaults when safe.

Unknown ability remains `unassessed`, not automatically beginner. Use design questions before settling the route; saved evidence can make another interview unnecessary. A concise route in chat does not require a persistent workspace. Mode 0 remains a direct answer: a simple question is not automatically an invitation to build a course.

## Done Criteria

Prefer direct evidence appropriate to the selected training mode:

- explain the important knowledge in plain language;
- reason about behaviour, sequence, model, or flow;
- apply it through code, operation, scenario analysis, or bounded design;
- produce the selected mode's independent artifact or action;
- pass the corresponding verification checks;
- identify at least one common mistake.

Do not make completion depend on elaborate plans, reports, or project structures unless the user explicitly wants them.

## Web Lookup

Browse official documentation when the user requests current information or when commands, SDKs, frameworks, package versions, or cloud behaviour may have changed.
