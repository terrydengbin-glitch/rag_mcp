# CEK-TA Contribution Schema

This schema defines a knowledge contribution record before it can become CEK-TA reusable knowledge, Skill updates, dataset samples, eval cases, or UI tasks.

## Schema Version

```yaml
schema_name: cek_ta_contribution
schema_version: 1.0.0
encoding: UTF-8
```

## Required Object

```json
{
  "schema_version": "1.0.0",
  "contribution_id": "KC-YYYYMMDD-001",
  "status": "proposed | sanitized | sourced | classified | conflict_checked | reviewed | accepted | rejected | needs_more_evidence",
  "source_project": {
    "project_name": "string",
    "project_type": "string",
    "adapter_ref": "string",
    "project_binding": "project_name"
  },
  "contribution_type": "backtest_bias | fill_model | live_risk | trade_analysis | kline_strategy | llm_training | rag_engineering | ui_audit | official_rule_update | other",
  "raw_finding_summary": "string",
  "private_data_risk": {
    "contains_private_fields": false,
    "contains_account_data": false,
    "contains_raw_orders": false,
    "contains_secrets": false,
    "contains_project_config": false,
    "contains_personal_or_org_sensitive_data": false,
    "risk_notes": []
  },
  "sanitization": {
    "sanitization_status": "proposed | sanitized | rejected",
    "removed_fields": [],
    "replaced_fields": {},
    "generalization_notes": [],
    "residual_risk": "low | medium | high"
  },
  "generalized_rule": {
    "statement": "string",
    "rationale": "string",
    "project_facts_removed": [],
    "generic_concepts": []
  },
  "applicability": {
    "market": "crypto | futures | spot | stock | general",
    "asset": "BTC | ETH | multi | general",
    "timeframe": "tick | 1s | 1m | 3m | 15m | 1h | 4h | 1d | general",
    "data_granularity": "tick | trade | order_book | second | kline | account_event | general",
    "project_type": "string",
    "assumptions": [],
    "not_applicable_when": []
  },
  "sources": [],
  "classification": {
    "partition_id": "string",
    "domain": "string",
    "subdomain": "string",
    "rule_type": "definition | principle | procedure | formula | checklist | anti_pattern | adapter_rule | schema | incident | eval_case"
  },
  "conflict_check": {
    "conflict_status": "none | potential | confirmed | resolved | deprecated_by_conflict",
    "checked_against": [],
    "conflicts": [],
    "approval_allowed": false,
    "resolution_summary": "string"
  },
  "accepted_outputs": [
    {
      "output_type": "knowledge_item | skill_update | dataset_sample | eval_case | ui_task",
      "target_file": "string",
      "target_id": "string | null"
    }
  ],
  "review": {
    "review_status": "draft | reviewed | approved | rejected | deprecated",
    "decision": "accepted | rejected | needs_more_evidence",
    "reviewer": "codex | human | mixed | null",
    "reviewed_at": "YYYY-MM-DD | null",
    "reason": "string",
    "open_questions": []
  },
  "audit_log": [
    {
      "at": "YYYY-MM-DD",
      "actor": "codex | human",
      "action": "created | sanitized | sourced | classified | conflict_checked | reviewed | accepted | rejected | revised",
      "notes": "string"
    }
  ],
  "created_at": "YYYY-MM-DD",
  "updated_at": "YYYY-MM-DD"
}
```

## Required Fields

```text
schema_version
contribution_id
status
source_project
contribution_type
raw_finding_summary
private_data_risk
sanitization
generalized_rule
applicability
sources
classification
conflict_check
review
audit_log
created_at
updated_at
```

## State Rules

```text
proposed:
  contribution exists but is not safe to reuse

sanitized:
  private data removed and generic mapping documented

sourced:
  sources and evidence added

classified:
  domain/subdomain/partition selected

conflict_checked:
  checked against existing CEK-TA knowledge

reviewed:
  reviewed by Codex or human

accepted:
  allowed to create accepted_outputs

rejected:
  blocked from reuse

needs_more_evidence:
  evidence or scope is insufficient
```

## Acceptance Gate

Contribution can become `accepted` only when:

```text
1. sanitization.sanitization_status = sanitized.
2. private_data_risk contains no secrets, account data, or raw orders.
3. sources is not empty.
4. classification.domain and classification.subdomain are present.
5. applicability assumptions and not_applicable_when are explicit.
6. conflict_check.conflict_status is none or resolved.
7. review.decision = accepted.
8. accepted_outputs are defined.
```

## Blocking Conditions

```text
1. contains_secrets = true.
2. contains_account_data = true.
3. contains_raw_orders = true and not sanitized.
4. residual_risk = high.
5. sources are missing.
6. conflict_status = confirmed without resolution.
7. contribution tries to promote project-private facts as general knowledge.
```

## Output Mapping

```text
knowledge_item:
  create or update CEK-TA knowledge after source and conflict audit

skill_update:
  update a stable workflow only after review

dataset_sample:
  may enter dataset_card only if sanitized and label reviewed

eval_case:
  may enter eval_report/eval set if split-safe

ui_task:
  may become Vue3 issue or task card
```
