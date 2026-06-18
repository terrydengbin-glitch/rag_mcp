# CEK-TA Dataset Card Template

Use this template for any CEK-TA dataset intended for LLM training, evaluation, preference comparison, RAG test sets, or Skill regression.

All samples must be sanitized, source-traceable, split-safe, and reviewed before training use.

## Dataset Identity

```yaml
dataset_id: cek_ta_dataset_YYYYMMDD_slug
dataset_name: ""
dataset_version: 0.1.0
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
owner: codex | human | mixed
status: draft | reviewed | approved | rejected | deprecated
```

## Target Capability

```yaml
capability:
  domain: quant_trading | kline_strategy | backtest | replay_simulation | live_trading | trade_analysis | llm_training | rag_engineering | project_runbooks
  task_type: strategy_audit | kline_review | backtest_review | trade_quality_analysis | task_card_writing | knowledge_conflict_review | rag_answering | eval_judgment
  desired_behavior: ""
  output_contract: ""
```

## RAG / Skill / SFT / Preference / Eval Decision

```yaml
recommended_use:
  rag: false
  skill: false
  sft: false
  preference: false
  eval: true
reason: ""
```

Decision rules:

```text
Use RAG for source-backed facts and changing knowledge.
Use Skill for stable step-by-step workflows.
Use SFT for stable output format or behavior.
Use preference data for reviewed better/worse judgments.
Use eval for capability measurement and regression gates.
```

## Source Mix

```json
{
  "source_counts": {
    "knowledge_item": 0,
    "task_card": 0,
    "trade_result": 0,
    "audit_report": 0,
    "human_preference": 0,
    "synthetic": 0
  },
  "source_quality": {
    "gold": 0,
    "silver": 0,
    "bronze": 0,
    "unverified": 0
  }
}
```

## Sample Schema

```json
{
  "sample_id": "string",
  "source_type": "knowledge_item | task_card | trade_result | audit_report | human_preference | synthetic",
  "source_ref": "string",
  "task_type": "string",
  "input": {},
  "expected_output": {},
  "rubric": [],
  "label_quality": "gold | silver | bronze | unverified",
  "split": "train | eval | holdout",
  "sanitization_status": "not_applicable | sanitized | rejected | raw_project_only",
  "license_or_reuse_status": "allowed | restricted | unknown | internal_only",
  "review_status": "draft | reviewed | approved | rejected | deprecated",
  "risk_flags": []
}
```

## Sanitization Rules

```text
1. Remove secrets, account identifiers, raw private orders, and project-private config.
2. Replace project-private field names with generic mapping when possible.
3. Remove or generalize personal or organization-sensitive data.
4. Mark raw_project_only samples as not trainable.
5. Do not sanitize by destroying causal context needed for the label.
```

## Split Rules

```text
1. Same incident family cannot appear in train and eval.
2. Same trade_result_id cannot appear across splits.
3. Same task card revision cannot appear across train and eval.
4. Holdout must remain untouched until release decision.
5. Eval set should include failure cases, edge cases, and normal cases.
```

## Leakage Check

```yaml
leakage_check:
  status: pending | passed | failed
  checked_at: YYYY-MM-DD | null
  checks:
    duplicate_source_ref: false
    same_case_across_splits: false
    answer_in_prompt: false
    private_data_present: false
    eval_seen_in_training: false
  notes: ""
```

## Quality Gates

Dataset can become `approved` only when:

```text
1. Every train/eval sample has source_ref.
2. Every training sample is sanitized or not_applicable.
3. Every training sample has review_status = reviewed or approved.
4. label_quality is not unverified.
5. leakage_check.status = passed.
6. license_or_reuse_status is allowed or internal_only.
7. Eval split is preserved.
```

## Risk Notes

```text
time_sensitive_rules:
private_data_risk:
label_noise_risk:
overfitting_risk:
coverage_gaps:
```

## Release Decision

```yaml
release_decision:
  decision: not_ready | ready_for_eval | ready_for_training | rejected
  reason: ""
  required_next_steps:
    - ""
```
