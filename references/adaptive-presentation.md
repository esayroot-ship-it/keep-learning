# Adaptive Teaching Presentation

Choose the medium for the learning problem. This is a presentation layer shared by all training modes; it does not replace their independence or mastery checks.

Start after the design questions and route in `teaching-design.md`. Choose the medium for each learning step, not once for the whole subject. Prepare the current step's material when needed. A deep topic can still need a careful text explanation; a simple state transition can sometimes benefit from a small diagram.

For a broad module, complete the coverage/depth review in `curriculum-quality.md` before allocating media. A diagram or interactive scene named in the plan does not compensate for an unspecified prerequisite or mechanism; tie it to an explicitly designed unit and evidence task.

## Build One Coherent Business Module

When the target is a development workflow, use a bounded, realistic user journey that fits the confirmed route. Name the actors, trigger, initial data, request/response contract, source of truth, and observable business outcome. Reuse the same IDs, values, functions, and interfaces in the relevant steps. A definition or a syntax doubt does not need a business application, module shell, or full backend.

Write a connected foundational lesson that a learner can follow without an animation. Explain why the request exists, how the entry function calls its dependencies, how data changes, what is returned, and how failures change the outcome. Define a term when its role first becomes necessary. Short text means a bounded explanation, not isolated slogans or missing causal steps. Add code and observable checks where they help connect the lesson to actual development.

Use interactive media when the difficult part depends on changes the learner should explore. For a request history, show the payload, active code, before/after state, and user-visible response. Make relevant transaction, snapshot, or retry states distinct. If a static diagram already explains the relationship, stop there; do not add animation or a website just for visual variety.

Supply a runnable fragment or implementation when running or modifying it is part of the current learning outcome. A visual explanation alone does not justify creating an API server, database, or test platform. Label simulated components and real integrations precisely. A successful animation does not validate a backend, and a passing test does not establish learner mastery.

## Allocate Markdown and Web Content for Large Modules

For a large goal with multiple learning stages, decide the division of content while planning the route. A stage can use Markdown alone, a focused webpage linked to Markdown, or an existing code/experiment artifact. Do not require both new files for every stage. Small questions remain proportionate conversational answers.

Markdown owns the coherent explanation and durable reference; an interactive page owns the states or alternatives the learner can manipulate. The page should provide the context needed to understand its experiment, but should not paste the whole chapter beside an unrelated animation. Markdown should remain understandable when the page is unavailable: include the relevant assumptions, a trace or static fallback, and the conclusion the experiment helps examine.

| Teaching stage | Markdown responsibility when saved material is appropriate | Interactive-web responsibility when useful |
| --- | --- | --- |
| Capability discovery | After answers, summarise confirmed ability, gaps, unknowns and supporting evidence; do not fill answers in advance | Reuse a focused scenario for a diagnostic only if its interaction is needed; a new quiz website is not the default |
| Overall route | Goal, prerequisites, stage order, outcomes, content allocation and links in a concise index | Optional navigation of a substantial existing module; do not build a course platform merely to display the route |
| Prerequisites and concepts | Definitions, causal explanation, a small example or derivation, common confusion and relevant boundaries | Only a diagram or manipulable example that reveals a specific relation; text-only stages need no page |
| Business or code flow | Trigger, request/response, important source path, data changes, normal outcome and failure branches | The same actors, payloads, active code and before/after state; step, pause or replay the flow |
| Deep mechanisms and faults | Assumptions, reasoning, counterexample, guarantee limits and verification criteria | Change order, inputs or failure conditions; show the resulting trace and state with reproducible reset |
| Independent application | Task contract, allowed concepts, artifact/source references, checks and hints separated from the reference solution | Optional prediction, tracing or scenario controls; do not reveal the answer automatically or require a browser IDE |
| Review and consolidation | Actual learner evidence, corrections, remaining gap, reusable conclusions and next step | Reuse the relevant scene to retest a changed case; clicks and visited tabs do not prove mastery |

In the route, state the division for each actual stage and omit irrelevant stages. For example, a cache-consistency module might put the read/write contract in Markdown, connect a request trace to a flow page, connect an old-refill counterexample to an order-manipulation experiment, and keep the independent coding requirements and checks in Markdown/source files. This is a possible allocation, not a fixed curriculum.

### Keep the Artifacts Connected

- Use stable unit and scenario identifiers, the same data values, terminology and source version across the explanation, animation and exercise.
- Link the relevant Markdown section to the exact page/scene, and provide a return link or named document section in the page. When local Markdown anchors cannot be opened in the host, provide the document path and section name.
- State the handoff: what to read first, what to predict before interacting, what to change, what to observe, and how to return to the explanation or submit evidence. Avoid making the learner search two parallel collections.
- For a large saved module, use a short Markdown index and split detailed documents/scenes only where the learning boundaries justify it. Do not impose a fixed folder tree or create empty future artifacts. Saved teaching material does not itself request a persistent progress workspace.
- Keep content and experiment data in one maintained source when practical. Reuse existing code instead of retyping diverging versions; no build framework is required for this relationship.
- Put observed outputs, parameters and assistance notes in the existing review material when tracking is requested. Do not silently convert experiment use into completed learning status.

Prepare each pair of artifacts when that stage is reached, unless the user explicitly requests the complete package now. When a capability gap changes the route, update the affected document, scene and links together; recheck the links, facts, source references and meaningful interaction after such changes.

## Judge Depth Before Choosing a Medium

Use the demonstrated capability boundary and the current gap first. Then consider prerequisite load, interacting components, branching/concurrency, hidden state, and failure consequences. Explain the depth and medium briefly when the choice is not obvious. Do not infer proficiency from topic complexity or invent a score.

| Current learning need | Smallest useful presentation | Expansion trigger |
| --- | --- | --- |
| Definition, syntax rule, one observable step | Concise text and one example in chat | A specific unanswered doubt |
| Execution of existing code | Relevant source excerpt, annotation or value trace | Several calls or state changes cannot be followed from the excerpt |
| Derivation, proof, or conceptual mechanism | A connected step-by-step explanation, with a small figure if needed | A spatial or causal relation needs to be seen |
| Dependencies, component relations or comparison | Small tree, Mermaid diagram or table plus explanation | A meaningful change must be explored |
| Race, state transition or parameter-sensitive outcome | A focused interactive experiment, reusing an existing one when suitable | Inputs or order materially change the result |
| Architecture decision | Constraints, failure case, tradeoff table and a bounded task | A specific protocol or executable outcome needs validation |

Use only dimensions that reveal something distinct: purpose, structure, execution, data/state, boundaries, failure, tradeoffs, implementation, verification. Reuse material; do not repeat the explanation as text, cards, and diagrams to fill space. Do not make every item in the route a document or put every depth into one simple website. A requested page or document takes precedence, with scope proportionate to the requested outcome.

## Adapt Without Guessing Mastery

- When relevant ability is unknown, use design probes before generating substantial materials. If questioning is declined, use stated provisional assumptions rather than claiming an assessed starting depth.
- During teaching, check the current reasoning step after explaining its necessary foundation. Adapt from the specific gap; do not begin with an entire lesson package and diagnose only afterwards.
- Offer manual depth selection. A learner may explore advanced material without passing a gate, but viewing, clicking, or a small multiple-choice check does not satisfy independent design or coding evidence.
- On a teaching page, show why a depth is recommended. Local rules may suggest a route from answers; do not claim an AI tutor or persistent assessment engine if none exists.
- Keep reference answers collapsed or behind an explicit reveal. Mark a revealed solution as study material, not evidence of independent mastery.

## Native Teaching Page Contract

Use semantic HTML, CSS, and vanilla JavaScript by default. Prefer local files with no build step, no external fonts, and no framework or chart library unless the interaction requires one. Use native DOM or SVG for diagrams. Keep the page useful when opened locally, or document a minimal local server when required.

Before generating a page, identify the learning question, what meaningful variable or order the learner will change, and why existing text/code/diagrams are insufficient. Prefer one focused scene or mechanism over a full application. Add navigation, backend services, worksheets, or exports only when the current goal needs them. All production and verification remains in the current agent.

Design it as an edited technical lesson: restrained colour, readable Chinese typography, useful navigation, meaningful labels, and enough space around diagrams. Avoid promotional hero copy, emoji-led feature grids, decorative gradients, glass effects, ornamental dashboards, fake progress percentages, and generic repeated cards. Explain specific mechanisms and consequences instead of slogans.

An interactive element must change a meaningful teaching state and expose its consequence. Provide initial conditions, assumptions, input constraints, step/reset controls where appropriate, and a textual state/trace alternative. Separate simulated time and data from measurements. Make deterministic counterexamples reproducible. Do not present a toy model as a production benchmark, complete protocol proof, or a live connection to a real service.

Keep the explanation needed for this interaction visible. Reveal further detail when feedback or the task requires it, rather than automatically packaging foundation, mechanism and engineering tiers. Include only the source views, failure paths, comparisons or practice that support the current outcome. Scope completeness to that outcome and identify unresolved assumptions.

Do not execute learner-submitted code through `eval` or silently contact services. A design worksheet can collect and export local notes without grading open-ended answers. Do not save learning progress or assert completion unless the user requested tracking and the relevant evidence exists.

## Verify Before Delivery

- Browse primary documentation for version-sensitive or specialist claims. Link sources close to supported content and label original deductions, assumptions, and simplified models.
- Check the model's invariants and meaningful failure cases with executable tests when the page simulates logic. Keep simulation logic separable from rendering where practical.
- Exercise the actual page: primary controls, reset/replay, recommendations, answer reveal, exports, keyboard focus, narrow screens, and console errors. Inspect screenshots for clipping and illegible diagrams.
- Deliver the page path or a working local preview and a concise route into the lesson. State what was actually tested and any material limits. Do not publish the lesson externally merely because a local teaching artifact was requested.
