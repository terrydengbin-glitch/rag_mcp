---
name: sft-engineer
description: Plan CEK-TA supervised fine-tuning only when stable workflows or output contracts fail repeatedly; define target behavior, dataset readiness, training boundaries, evaluation gates, rollback, and release criteria without selecting a provider by default.
---

# SFT Engineer

## Use When

Use this skill when deciding whether CEK-TA needs supervised fine-tuning for:

```text
task card writing
strategy audit output format
trade-quality analysis output format
bad-case labeling workflow
knowledge conflict review workflow
structured eval judgment
```

## Workflow

1. Confirm the behavior is stable enough for SFT.
2. Confirm RAG or Skill alone is insufficient.
3. Define target capability and output contract.
4. Check dataset card readiness.
5. Confirm train/eval/holdout split and leakage status.
6. Define baseline and candidate comparison.
7. Define release gates from `eval_report.md`.
8. Define rollback path.
9. Do not proceed if data is raw, unreviewed, time-sensitive fact-heavy, or license-restricted.

## Hard Rules

```text
SFT is for stable behavior, not current facts.
Do not fine-tune exchange rules, model/API behavior, or project config.
Do not train without eval gates.
Do not train on unsanitized project data.
Do not release if safety or boundary regressions appear.
```

## Output

```json
{
  "sft_decision": "not_needed | ready_to_plan | blocked",
  "reason": "",
  "target_capability": "",
  "dataset_requirements": [],
  "eval_requirements": [],
  "blocked_by": [],
  "rollback_path": "",
  "release_gates": []
}
```
