# Worked Example: Just-Enough Linux

Use this worked planning example when scope, sequencing or a small unit needs a concrete model. It is not a Linux syllabus to impose on other topics, and does not replace training-modes.md, code-writing.md, code-reading.md or adaptive-presentation.md.

## Source and Evidence Boundary

Source: ChrisKim_ZHT, [只学够用的 Linux：长度正好的零基础入门教程](https://www.bilibili.com/video/BV13ctf6RECM/), with an [author-provided written version](https://www.zouht.com/4399.html). The video description states CC BY-NC-SA 4.0. This example paraphrases the teaching design rather than reproducing its lessons.

The extracted Bilibili AI captions contain 4,235 cues, from 00:00:00.040 to 02:52:33.040; video duration is 02:52:35. Use them as evidence for sequence and spoken teaching choices, not authoritative spelling of commands or proof of visual quality.

The target is a beginner's ordinary Linux terminal work and ability to look up unfamiliar needs. The demonstrations assume access to a working Linux terminal. In a new course, supply or teach missing setup explicitly; do not hide it behind an assumed prerequisite.

The source's runtime is presentation time, not measured learner proficiency or a total including independent practice. The skill adds its own brief boundary check, independent verification and optional progress tracking. Its roughly 95% normal-use target is not a statistic established by this video.

## Reverse-Engineered Course Pattern

| Source observation | Reusable design decision |
| --- | --- |
| 00:00-02:13: limits the audience and goal, separates foundations/common uses/further directions, and discourages memorising every command | Define the normal-work endpoint first. Teach how to choose and check an action; uncommon syntax can be looked up. |
| 00:05:15-00:20:55: prompt, simple commands, waiting, interruption, parameters, input shortcuts and help | Make the first useful interaction understandable before presenting a large knowledge map. Include small usability barriers, not just topic names. |
| 00:20:55 onward introduces paths through familiar directory behaviour; detailed directory roles wait until 01:55:31 | Teach the immediate model, then defer the wider taxonomy until practical actions make it meaningful. |
| 00:42:12-00:56:18 distinguishes copy/move/delete outcomes, existing targets and mistakes; 01:26:11-01:41:51 demonstrates permission effects | Cover behaviour-changing options, expected state and common failures. A command list alone does not establish usable knowledge. |
| 02:00:07 begins a faster practical layer: downloading, archives, text handling, links, background tasks, resource observation, mounts and environment configuration | Reuse foundations; allocate less explanation to routine variations. Check whole application families so small high-frequency tasks are not lost behind advanced chapters. |
| 02:13:18 introduces links through data relocation and a fixed application path; 02:19:41 introduces background work through a busy shell and disconnected sessions | Start a mechanism from the problem it solves, explain the minimal model, demonstrate a normal case, then show its relevant limit. |
| 02:46:56 groups watch, tee, diff, system identification and shortcut recovery | Bundle tiny useful items into a concise reference or demonstration; avoid a full module for every command. |
| 02:51:13 onward describes a needs-to-tools index and explicitly leaves that third chapter outside the video | End with lookup directions. Do not silently turn the written index into further taught chapters or claim those capabilities were demonstrated. |

The resulting route is **careful foundation -> concise common applications -> brief lookup directions**. This is a change in explanatory density, not a rule that later topics receive incomplete explanations.

When adapting it, choose one primary environment and the smallest representative tool set. Keep a basic principle when it explains a choice or likely failure; leave internal implementation details for a named extension. Do not copy every alternative tool, shortcut or informal recommendation from the source.

## One Small Unit, Made Reviewable

The source's link examples illustrate problem-first teaching. The following independent activity is an adaptation added by the skill, not an exercise claimed to exist in the video.

| Design field | Example |
| --- | --- |
| Outcome | Choose a link type for a stated file-access requirement and predict what changes when a name or target is removed. |
| Primary mode | operational: actual file operations and state verification; no unrelated programming assignment. |
| Prerequisites/setup | Paths, viewing/copying/moving files and basic permissions. Supply disposable practice files; explain the necessary link operations before the independent attempt. |
| Basic model | A symbolic link refers to a target path; hard-linked file names refer to the same file identity. Teach the practical same-filesystem and ordinary-file limits needed for this task, without a VFS implementation lesson. |
| Teaching example | Demonstrate a symbolic file alias and check reads/edits through it. Rename its target and explain the failure; contrast the already-taught hard-link model. |
| Independent variation | Give a fresh requirement: two file names must share content, and removing either name must leave the other usable on the same filesystem. Let the learner choose, order and perform the operations without giving the decisive solution. |
| Evidence | The learner explains the choice, predicts states, performs the steps, diagnoses the relevant failure and checks surviving content/link information. Reuse this activity for the operational checks; do not turn them into five assignments. |
| Media | Text for purpose, rules and commands; the terminal for real results; a small relationship diagram when helpful. Use an interactive name/target/deletion scene only if manipulating those states resolves a demonstrated gap. |
| Size and stop | Roughly 10-15 minutes including the small application, subject to actual readiness. Stop at independent use; do not expand into implementing a filesystem. |
| Optional ending | Further: inode/VFS implementation, when studying filesystem internals. One line; no automatic lesson or new queued task. |

A renamed copy of the fully explained task is not independent transfer. If help reveals the decisive answer, use a fresh small variant under the existing practice rules.

## Transfer the Pattern, Not the Terminal Format

Choose the unit's mode from its required outcome, then choose its medium separately. A webpage is a presentation choice, not a sixth training mode.

| Required outcome in another subject | Mode and suitable evidence |
| --- | --- |
| Write a language feature, function, SQL statement or small patch | manual-coding: derive the implementation from a new requirement, handle a meaningful variation and verify it. |
| Understand an existing code path | code-reading: independently trace an unworked case, predict behaviour and assess a change; no compulsory rewrite. |
| Design a component boundary or failure-handling approach | architecture: a bounded diagram/flow, explicit tradeoffs and a design checked against constraints and failure cases; no compulsory coding. |
| Operate a tool, deployment or middleware feature | operational: an ordered procedure, actual state/log observations and a common-failure diagnosis. |
| Understand a principle or protocol without implementing it | conceptual: explain/model/compare it and apply it to a fresh scenario with verification. |

Keep one concrete mode per unit. A mixed course can share context across separate reading, writing or design units; evidence from one mode does not certify another. Use training-modes.md for the authoritative checks.

## Keep Local Maintenance Independent of Course Size

If saved progress is requested or already authorised, use local-management.md and workspace.md: resume the selected task, retain configuration separately from progress and reviewed evidence, record the actual attempt/help/gap, and advance/archive only through the existing checks. Brief extension pointers are not unfinished required units.

A short course can span several sessions without widening its scope. Creating a lesson or viewing a page is not mastery. Without a tracking request, keep the example and evidence in conversation; editing this skill does not create a Linux learning project.
