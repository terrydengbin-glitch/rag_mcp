# CEK-TA Knowledge Contribution Task Template

Use this template in a business project before contributing knowledge, cases, audit conclusions, rule updates, or training samples back to CEK-TA.

Never write directly into CEK-TA approved knowledge.

## Contribution ID

```yaml
contribution_id: KC-YYYYMMDD-001
status: proposed
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
owner: codex | human | mixed
```

## Source Project

```yaml
project_name: ""
project_type: ""
adapter_ref: "docs/project_adapter.md"
project_binding: "project_name"
```

## Contribution Type

```yaml
contribution_type: backtest_bias | fill_model | live_risk | trade_analysis | kline_strategy | llm_training | rag_engineering | ui_audit | official_rule_update | other
target_domain: ""
target_subdomain: ""
```

## Raw Finding Summary

```text
Describe the original project finding, incident, audit conclusion, or reusable rule candidate.
Do not paste secrets, raw account data, or raw private orders.
```

## Private Data Risk

```yaml
contains_private_fields: false
contains_account_data: false
contains_raw_orders: false
contains_secrets: false
contains_project_config: false
contains_personal_or_org_sensitive_data: false
risk_notes:
  - ""
```

## Sanitization Report

```yaml
sanitization_status: proposed | sanitized | rejected
removed_fields:
  - ""
replaced_fields:
  project_field: generic_field
generalization_notes:
  - ""
residual_risk: low | medium | high
```

## Generalized Rule

```text
Extract the reusable professional rule.
Separate project facts from general knowledge.
```

## Applicability

```yaml
market: "crypto | futures | spot | stock | general"
asset: "BTC | ETH | multi | general"
timeframe: "tick | 1s | 1m | 3m | 15m | 1h | 4h | 1d | general"
data_granularity: "tick | trade | order_book | second | kline | account_event | general"
project_type: ""
assumptions:
  - ""
not_applicable_when:
  - ""
```

## Sources and Evidence

```yaml
sources:
  - source_title: ""
    source_url: ""
    source_type: "official_doc | paper | exchange_rule | framework_doc | book | research_report | engineering_article | internal_report | task_card | code_doc | runbook"
    publisher: ""
    published_at: null
    accessed_at: YYYY-MM-DD
    reliability: "high | medium | low"
    evidence_summary: ""
```

## Relationship to Existing Knowledge

```yaml
relationship: new_rule | correction | extension | conflict | deprecation | training_sample | ui_improvement
existing_knowledge_ids:
  - ""
```

## Conflict Check

```yaml
conflict_status: none | potential | confirmed | resolved | deprecated_by_conflict
conflict_items:
  - knowledge_id: ""
    conflict_type: direct_conflict | scope_conflict | version_conflict | market_conflict | granularity_conflict | assumption_conflict
    resolution: ""
approval_allowed: false
```

## Suggested CEK-TA Output

```yaml
output_type: knowledge_item | skill_update | dataset_sample | eval_case | ui_task | reject
target_file: ""
target_partition: ""
target_domain: ""
target_subdomain: ""
```

## Review Decision

```yaml
review_status: draft | reviewed | approved | rejected | deprecated
decision: accepted | rejected | needs_more_evidence
reviewer: codex | human | mixed | null
reviewed_at: null
reason: ""
open_questions:
  - ""
```

## Definition of Done

```text
1. Sensitive project data has been removed or rejected.
2. Sources and evidence are present.
3. Applicability and assumptions are explicit.
4. Conflict check is complete.
5. Target CEK-TA output is clear.
6. Review decision is recorded.
```
