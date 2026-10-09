# Practical Scope, Coverage and Time

Use for any multi-unit course or a reported planning gap. The objective is a short course that makes normal work independently achievable. Review it in this agent, without delegation.

## Define the Application Boundary

Name the subject, role, environment and everyday outcome before selecting topics. Reuse the brief boundary check; do not create a second interview. A product name is not a request for every profession associated with it. Select the work the learner needs to perform rather than combining ordinary use, administration, internal implementation and architecture into one course.

Aim to cover roughly 95% of common application needs within that stated boundary. Count meaningful work scenarios, not commands, chapter titles, manual pages or all possible subject knowledge. Build a compact scenario set from the user's work and relevant primary documentation; a manual's table of contents helps discover gaps but does not define the teaching order.

The percentage is a design target unless representative usage data exists. Do not invent frequencies or announce a measured 95% from a hand-picked exercise set. Passing 38 of 40 exercises measures performance on those exercises, not real-world demand coverage. When frequencies are available, explain the population and weighting briefly; otherwise label the estimate qualitative and show the mapped common tasks and remaining uncertainty.

Use three scope buckets:

- **Core:** frequent normal tasks, their indispensable prerequisites/basic principles, common mistakes and the correctness/recovery steps needed for those actions.
- **Brief extension:** low-frequency alternatives, specialised internals or adjacent roles. Give only a topic and the situation that would justify learning it.
- **Outside this course:** unrelated capabilities; leave them out rather than creating a long optional catalogue.

An infrequent prerequisite or high-impact basic mistake cannot be omitted merely to fit a frequency target. This does not justify expanding into enterprise architecture or disaster recovery unrelated to the selected job. Do not narrow the declared role after finding a missing common task just to claim coverage.

## Keep the Whole Route Within a Few Hours

Default to about three hours total for explanation, essential independent practice and verification, usually two to four hours. A small topic may take minutes. These are planning estimates, not deadlines that force a false mastery claim. List substantial setup/download delays separately.

Give units approximate times and add them up. A small unit normally covers one useful behaviour in about five to fifteen minutes; group tiny related operations, and split a genuinely complex task at a natural dependency. Do not multiply short courses or append mandatory follow-on stages until a nominally short topic becomes a long curriculum.

To reduce length, remove repeated explanations, obscure options, alternative tools with the same purpose, out-of-role duties and deeper internal derivations. Preserve the common scenarios and causal explanation required for independent use. Choose a primary tool/environment and explain the transfer points instead of teaching several complete toolchains.

If the required role breadth and learner prerequisites cannot honestly fit, state that constraint, give the smallest coherent practical route and identify the specific unmet outcomes. Do not label it 95% complete or quietly prescribe a much longer course. Explicit user scope and time choices override the defaults.

## Design Each Core Unit

Make every required scenario traceable to:

1. an action the learner will perform and the expected result;
2. the immediate prerequisites and basic causal model needed to choose that action;
3. essential syntax, statements, APIs or operating steps;
4. a normal case and a meaningful common failure/boundary;
5. a small independent activity and observable verification, reusing one artifact across checks;
6. its owner unit, medium and estimated teaching/practice time.

Keep these decisions in the existing plan. A heading such as "network", "SQL" or "indexes" is not enough; nor is listing a tool without the applications it must support. For example, using curl for connectivity does not design file downloading, and teaching variables does not automatically design persistent environment configuration.

The default depth is **use + basic mechanism + common boundaries + independent application**. Teach why the operation works well enough to predict an ordinary variation or diagnose a common failure. Supporting facts may need only recognition. Internal algorithms, proofs, source internals and specialist tradeoffs become core only when the stated target requires them.

The learner must still meet the chosen training mode's independent evidence checks. Shortening the course changes scope and duplication, not what qualifies as independent writing, reading or verification.

## Worked Planning Example

Use [the reverse-engineered Linux teaching example](practical-course-example.md) when a concrete illustration of scope, sequence, unit design or transfer to other learning modes would help. It replaces a product-specific checklist with an observed teaching pattern: carefully explained foundations, concise common tasks, and short further-learning directions.

The example distinguishes what the video demonstrates from the skill's own brief discovery, independent evidence and local-progress requirements. Adapt the pattern to the learner's actual work; do not reuse the Linux command list, assume a three-hour video proves proficiency, or treat 95% as an observed statistic. If a named internal mechanism is the requested subject, it remains core to its own bounded course.

## Audit Before Delivery and at Completion

- **Forward:** are the next action and its prerequisites understandable without untaught syntax or hidden setup?
- **Backward:** can every stated normal-work outcome be reached through a designed unit and independent verification?
- **Breadth:** are high-frequency practical actions missing while advanced topics take space? Audit the adjacent scenario families when a gap is found.
- **Depth:** is there enough basic why to predict and correct behaviour, without defaulting to lower-level implementation detail?
- **Length:** does the total include required practice, and does every core item justify its cost? Are extensions short and optional?
- **Evidence:** distinguish planned, taught and independently demonstrated. A page, title, successful AI demonstration or exhausted queue proves neither proficiency nor coverage.

Repair the plan before calling it complete. At the end of teaching, review the selected core outcomes and unresolved gaps; do not require mastery of extension directions. A complete plan is still only a design, not evidence that the learner has already become proficient.
