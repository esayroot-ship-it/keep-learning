# Learning Configuration

This reference applies only to persistent tasks. Store all durable learning settings in `00-meta/learning-config.json`.

## Canonical Configuration

```json
{
  "schema_version": 4,
  "goal": "",
  "scope": "bounded development topic",
  "duration": "about 3 hours",
  "current_level": "unassessed",
  "mode": "understand-apply-verify",
  "training_mode": "auto",
  "ai_allowance": "hints-first",
  "preferences": {
    "explanation_detail": "standard",
    "pre_question_explanation": "comprehensive-foundation",
    "line_by_line_code_explanation": true,
    "max_new_concepts_per_unit": 1,
    "practice_sequence": "mode-specific",
    "diagnostic_questioning": {
      "enabled": true,
      "questions_per_round": 1,
      "file_code_enabled": true,
      "retry_limit": 2
    },
    "autonomous_progression": {
      "enabled": true,
      "rolling_unit_window": 5
    },
    "engineering_expansion": "on-request"
  },
  "done_criteria": []
}
```

## Rules

- Treat this file as the only persisted configuration source.
- For a new topic, default `duration` to `about 3 hours`, following the teaching-plus-essential-practice budget in `curriculum-quality.md`. Honour an explicit duration instead; a small task should stay smaller. An older `flexible` value leaves scheduling open but does not request unlimited breadth. Keep the selected role, normal-work scenarios and extension boundary in the existing plan, not new duplicated progress fields.
- New defaults do not rewrite existing configuration, queues, completed evidence or archived lessons. Apply current user instructions first and make any change to an existing route explicit.
- An unknown level is `unassessed`; do not assume beginner or overwrite a previously demonstrated level. Use focused design questions in `teaching-design.md` before choosing the route, and keep a brief boundary summary in existing lesson/review materials when tracking is requested.
- Set `training_mode` to `auto`, `manual-coding`, `code-reading`, `conceptual`, `operational`, `architecture`, or `mixed`. `auto` is the default; select a concrete mode for each unit.
- Do not duplicate any of these fields in `progress.json`.
- Let the current user request temporarily override saved values without rewriting the file unless the user asks to save the change.
- Keep `max_new_concepts_per_unit` between 1 and 3; default to 1.
- Keep the compatible `pre_question_explanation` value `comprehensive-foundation`: fully explain the selected practical behaviour, its basic why and worked example, not the whole underlying subsystem. This and `line_by_line_code_explanation` apply to teaching/guided reading; do not disclose an independent task's solution or trace before the learner attempts it. `explanation_detail: detailed` adds clarity inside the chosen scope, not extra specialist topics.
- Keep questioning adaptive and lightweight. Design discovery uses the one brief round and conditional single follow-up in `teaching-design.md`; the configured questions-per-round value is a ceiling, not a quota. Comprehension checks use taught concepts afterwards. Honour direct-teaching or questioning-off preferences.
- Default the ongoing execution window to five units; configured limits are three to seven. A short or nearly completed goal may need fewer units; never add filler to reach the configured window. The overall route is planned separately in proportion to the goal.
- Default engineering expansion to `on-request`.
- Prefer a small number of activities that prove comprehension and independent application. Require hand-written code only for `manual-coding` units.
- Do not use abstract teaching/practice weights. Choose the next activity from learner evidence: explain more when comprehension is missing; practise when the example is understood.
