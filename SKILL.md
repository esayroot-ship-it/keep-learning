---
name: keep-learning
description: Explicit-only practical learning for independent normal work in a few hours. Use only when the user invokes `$keep-learning` or asks to use the skill. Briefly check the starting boundary, cover common application needs and basic principles, and use suitable media, independent writing and graded reading. Save progress only when requested.
---

# Keep Learning

Teach just enough to use the selected subject fluently in normal work: explain the basic why, choose an appropriate action, perform it independently, and verify/correct the result. Optimise for a short, usable course rather than exhaustive expertise.

For a topic course, default to about three hours total for teaching and essential practice, normally within two to four hours; small questions stay much shorter. Aim to cover roughly 95% of common application needs within the stated role and environment, not 95% of a subject's knowledge. This is a planning target, not a measured coverage claim or a guarantee of proficiency by a deadline. Use `references/curriculum-quality.md` to select scope, budget and evidence. Explicit user scope/time requirements take precedence; disclose a mismatch instead of silently growing the course or claiming impossible completeness.

## Invariants

- Work in this agent only: no subagents, forks, delegation or another agent's review.
- Default to lightweight conversation. A small factual question needs no interview or course. Durable plans, materials and tracking require the relevant user request; improving the skill itself does not create a subject project.
- Discover capability before planning with one brief round, reusing known goals and ability evidence. Ask one primary question, up to three short related items; permit one follow-up only when it changes the starting step or scope. Await answers and distinguish gaps from unknowns. Respect direct-answer/no-question requests; do not turn discovery into a domain-wide assessment.
- Default to one primary question per round, at most three. Wait before revealing its answer unless the learner requests it.
- Teach one small concept/reasoning step and its immediate prerequisite at a time. Include the purpose, mechanism/flow, values, I/O, errors, boundaries and verification needed for this gap. Assigned activities use understood/taught concepts or supplied setup; do not test hidden prerequisites.
- Inspect a requested file and its role/entry/call path first; read only dependencies needed for that path. Guided examples can be fully explained; independent checks use unworked cases without solution-bearing help. Keep essential behaviour understandable rather than hidden in frameworks or generated code.
- Select one concrete training mode per unit. Reading and writing have separate evidence; conceptual, operational and architecture units use authentic application, without artificial coding. Requirements/checks and progressive hints precede full solutions; provide full answers when requested, after an attempt/review, or when training is not the purpose.
- Complete a unit only with all mode-specific observable checks and no unresolved gap. Copied/assisted work needs a fresh independent variant. One artifact may satisfy several checks; correct only the smallest missing point and do not repeat mastered work.
- For multi-unit goals, select frequent work scenarios, necessary basic principles and common failure handling within the short-course budget. A listed command is not a designed application. Do not expand a broad title such as "master a technology" into all internals, administration and architecture unless those outcomes are explicitly requested. Keep later unknowns provisional and optional depth outside the core.
- End a small unit with at most two brief extension directions when useful: name the topic and when it becomes relevant. Do not teach, assign, generate pages for, or queue those extensions automatically.
- Choose each step's medium and length from its content and learner gap. Small questions stay small; deep explanations remain complete. Large routes allocate linked Markdown and interactive-web responsibilities. Depth alone does not require a page, module shell or backend.
- Expand architecture/deployment/performance/reliability only when requested or necessary. Browse official documentation before current or version-sensitive commands, APIs or behaviour.
- Local tasks use canonical configuration, progress and reviewed evidence, with snapshots and generated views. Creation/viewing does not prove mastery; archive only tracked materials. Current instructions override saved preferences, then defaults; preferences stay out of progress.

## Workflow

1. Choose the smallest task scope. For tracked work, select/register and resume the authorised workspace without resetting it.
2. Inspect relevant artifacts; make the brief boundary check, then state the normal-work goal, starting point and relevant unknowns.
3. Plan the shortest complete practical route: core scenarios, basic principles, prerequisites, estimated teaching/practice time, medium and independent evidence. Mark what stays outside the core. For multi-stage modules, specify Markdown/web ownership and links. Audit both missing common uses and unnecessary depth. A planning-only request ends with the checked plan.
4. When teaching is requested, select the first ready unit and concrete training mode, show the route and begin without an extra approval ritual.
5. Prepare only the current step's needed explanation/resources. Use the smallest relevant example, code, model or procedure; keep teaching examples separate from independent answers.
6. Ask a focused comprehension question, explain the revealed gap, then assign/review the mode-appropriate application and independent verification. Adapt the route when evidence or the target changes.
7. After all checks pass, select the next prerequisite-ready core unit using the rolling execution queue; stop at the agreed practical outcome. For tracked tasks, save factual reviews, checks, gaps and next actions through the manager before ending meaningful work; regenerate views.

A normal unit contains one practical behaviour and its immediate prerequisite, a minimal example, necessary explanation, adaptive application and independent evidence. Reuse one activity across checks rather than requiring separate question rounds or assignments for each check. Finish with a short review and optional extension pointers. Stop expanding after mastery; full-material requests cover the agreed scope, not every adjacent subject.

## Read References by Trigger

Apply every relevant rule. Reuse a reference only when its unchanged instructions remain in the current context; reload after edits or loss through compaction. Do not repeatedly dump the directory. A clearly scoped conditional section can be read with its common rules and required dependencies. This loading policy does not replace fresh learner state or current factual verification.

| Trigger | Required guidance |
| --- | --- |
| Task scope or persistence choice | `references/task-model.md` |
| New/changed learning target or capability discovery | `references/teaching-design.md` |
| Any multi-unit plan, scope/time/95% coverage decision, or reported omission | `references/curriculum-quality.md` |
| A worked example of practical scope, sequencing or transfer across learning modes is useful | `references/practical-course-example.md` (Linux video example; read on demand) |
| Practice-mode selection | `references/training-modes.md` |
| Independent implementation | `references/code-writing.md` |
| Code-reading source level/help/independent trace | `references/code-reading.md` |
| Shared teaching/application loop | `references/teaching-and-drills.md` |
| Comprehension questioning | `references/diagnostic-questioning.md` |
| Explanation depth and completeness | `references/teaching-depth.md` |
| Prerequisites for questions/activities | `references/prerequisite-control.md` |
| Medium selection; large-module allocation; page creation/QA | Relevant common and conditional sections of `references/adaptive-presentation.md` |
| Multi-unit queue, completion and continuation | `references/autonomous-progression.md` |
| Requested local registration/status/updates/recovery | `references/local-management.md` |
| Persistent data ownership, resume or legacy layout | `references/workspace.md` |
| Durable learning settings | `references/learning-parameters.md` |
| Explicit broad curriculum discovery | `references/capability-map.md` (seed only) |
| Requested/essential engineering depth | `references/engineering-expansion.md` |

## Local Tools

- `scripts/manage_learning.py`: create/register/select/list/status/resume, factual records, locked recoverable updates, restore and non-destructive index archiving.
- `scripts/init_learning_workspace.py`: initialise canonical configuration and a minimal persistent workspace.
- `scripts/update_progress.py`: exclusive transitions, mode checks, generated views and prerequisite-ready advancement; `--advance` checks evidence/gaps and archives tracked current materials.

Run tools directly; read source only for editing/debugging. Optional `manage_learning.py --compact <command>` reduces the response, preserving the full saved state and all gates. Relative returned paths use `path_base`. Use read-only `status` without the flag for complete details; do not repeat a mutation just to expand its output. Record several actually demonstrated checks together when one artifact supports them.
