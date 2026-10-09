# Training Modes

Select practice from the current unit and the capability boundary found with `teaching-design.md`. Within teaching, foundations precede practice; discovery and route planning precede both. Do not infer a need for coding merely because the topic belongs to software development.

## Selection

- `manual-coding`: use when the learner must independently implement, modify, or repair source code, SQL, scripts, tests, or configuration-as-code. Follow `code-writing.md`.
- `code-reading`: use when the learner must understand existing source, trace execution, diagnose behaviour, or assess a proposed change without implementing it. Follow `code-reading.md`.
- `conceptual`: use for principles, protocols, standards, mathematical ideas, runtime mechanisms, hardware theory, or other knowledge best demonstrated through explanation and application.
- `operational`: use for tools, GUIs, commands, deployment, middleware administration, observability, hardware operation, or workflows whose real skill is safe execution and troubleshooting.
- `architecture`: use for component boundaries, request or data flows, tradeoffs, failure modes, capacity, reliability, and system design.
- `mixed`: use only as a task-level preference. Split the task into units and assign one primary mode to each unit.
- `auto`: inspect each unit and choose one of the five concrete modes.

For a code task, distinguish reading, writing, or both from the user's goal. Do not turn a reading-only request into a writing exercise. For both, share the source/context but use separate unit IDs and evidence; a reading pass does not establish writing ability.

Do not invent a coding task merely to preserve manual coding. Avoid toy scripts unrelated to the target skill, unsafe live-system operations, or simulations that hide the actual concept. When required hardware, accounts, or environments are unavailable, use a trace, decision table, diagram, dry run, supplied artifact, or scenario analysis and state the limitation.

## Mastery Checks

### Manual Coding

`explain`, `predict`, `modify`, `write`, `verify`

The learner derives an implementation from requirements, explains their choices, predicts behaviour, handles a meaningful changed requirement, and verifies the result. Apply the independence and minimum-workload rules in `code-writing.md`; copied or solution-assisted work cannot pass `write`.

### Code Reading

`explain`, `trace`, `predict`, `impact`, `verify`

The learner explains and traces source, predicts behaviour, assesses a proposed change, and checks the reasoning. Use the source levels and independent-reading gate in `code-reading.md`. No implementation is required.

### Conceptual

`explain`, `model`, `compare`, `apply`, `verify`

The learner explains the concept, reconstructs a model, distinguishes it from alternatives, applies it to a new scenario, and checks the reasoning against stated rules or evidence.

### Operational

`explain`, `sequence`, `perform`, `diagnose`, `verify`

The learner explains the purpose, orders the steps safely, performs or accurately dry-runs the operation, diagnoses a realistic failure, and verifies the resulting state.

### Architecture

`explain`, `trace`, `tradeoff`, `design`, `verify`

The learner explains the system, traces one important flow, evaluates tradeoffs, produces or revises a bounded design, and verifies it against requirements and failure scenarios.

## Mixed Subjects

Choose mode per unit. For example, learning Redis may use:

- conceptual for eviction and consistency;
- code-reading for tracing an existing cache integration;
- manual-coding for cache-aside integration;
- operational for inspection, metrics, and failover;
- architecture for cache placement and failure handling.
