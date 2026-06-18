---
name: llm-data-curator
description: Curate CEK-TA LLM datasets from source-backed knowledge, task cards, sanitized trade results, audit reports, and reviewed labels; enforce sanitization, split safety, label quality, leakage checks, and dataset card completion.
---

# LLM Data Curator

## Use When

Use this skill when creating or reviewing:

```text
dataset cards
training samples
eval samples
preference pairs
trade-result training cases
task-card examples
knowledge audit examples
```

## Workflow

1. Identify target capability and whether the need belongs in RAG, Skill, SFT, preference data, or eval.
2. Collect only source-traceable candidates.
3. Remove raw private trades, secrets, account data, project-private config, and unsafe prompts.
4. Preserve causal context needed for labels and root cause.
5. Assign label_quality: gold, silver, bronze, or unverified.
6. Assign split: train, eval, or holdout.
7. Run leakage checks across source_ref, case family, incident family, and expected output.
8. Fill `dataset_card.md`.
9. Block release if sanitization, license, label, or leakage gates fail.

## Hard Rules

```text
Do not train on latest market facts or time-sensitive exchange/API rules.
Do not train on raw private trades.
Do not allow eval samples into train split.
Do not mark unverified labels as training-ready.
Do not destroy context needed to judge correctness.
```

## Output

```json
{
  "dataset_id": "",
  "target_capability": "",
  "recommended_use": {
    "rag": false,
    "skill": false,
    "sft": false,
    "preference": false,
    "eval": true
  },
  "sample_counts": {},
  "blocked_samples": [],
  "leakage_check": "pending | passed | failed",
  "release_decision": "not_ready | ready_for_eval | ready_for_training | rejected",
  "open_questions": []
}
```
