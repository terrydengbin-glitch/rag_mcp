# CEK-TA Contribution From Project Template

Use this template in a business project when a reusable finding should be proposed back to CEK-TA.

This template is a runtime entrypoint. It creates a proposed contribution package only. It must not write into CEK-TA approved knowledge.

## Contribution Runtime Envelope

```yaml
contribution_id: KC-YYYYMMDD-001
status: proposed
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
created_by: codex | human | mixed
source_project_id: ""
source_project_name: ""
source_project_adapter: docs/project_adapter.md
target_queue: "<cek_ta_path>/contributions/proposed/"
direct_approved_write_allowed: false
```

## Source Project Snapshot

```yaml
project_type: "kline_trend_strategy | abnormal_move_strategy | high_fidelity_simulator | live_binance_futures | trading_llm_assistant | custom"
market: "crypto | futures | spot | stock | general"
asset_classes:
  - ""
runtime_mode_where_found: "research | backtest | replay | simulation | paper | live"
strategy_or_system_version: ""
project_fact_refs:
  - docs/project_overview.md
  - docs/current_pipeline.md
  - docs/data_schema.md
```

## Contribution Type

```yaml
contribution_type: backtest_bias | fill_model | live_risk | trade_analysis | kline_strategy | llm_training | rag_engineering | ui_audit | official_rule_update | other
target_domain: ""
target_subdomain: ""
candidate_knowledge_tree_node: ""
relationship_to_existing_knowledge: new_rule | correction | extension | conflict | deprecation | training_sample | ui_improvement
```

## Raw Finding Summary

```text
Summarize the finding in plain language.
Do not paste secrets, raw account data, raw private orders, private logs, private customer data, or one-off project-only config.
```

## Sanitization Gate

```yaml
contains_secrets: false
contains_account_data: false
contains_raw_orders: false
contains_private_project_fields: false
contains_personal_or_org_sensitive_data: false
contains_project_only_config: false
sanitization_status: proposed | sanitized | rejected
removed_or_replaced:
  - original_kind: ""
    replacement: ""
residual_risk: low | medium | high
```

Fail the contribution if:

```text
contains_secrets is true
contains_account_data is true and not sanitized
contains_raw_orders is true and not sanitized
residual_risk is high
```

## Generalized Knowledge Candidate

```text
Write the reusable professional rule, engineering pattern, risk warning, bad case label, or evaluation insight.
Separate project-specific facts from generalized knowledge.
```

## Applicability Boundary

```yaml
applies_when:
  market: ""
  asset_class: ""
  timeframe: ""
  data_granularity: ""
  runtime_mode: ""
  assumptions:
    - ""
does_not_apply_when:
  - ""
known_limitations:
  - ""
```

## Sources And Evidence

```yaml
sources:
  - source_title: ""
    source_url: ""
    source_type: "official_doc | paper | exchange_rule | framework_doc | book | research_report | engineering_article | internal_report | task_card | code_doc | runbook"
    publisher: ""
    published_at: null
    accessed_at: YYYY-MM-DD
    reliability: high | medium | low
    evidence_summary: ""
project_evidence_refs:
  - ""
```

Rules:

```text
1. A project observation alone is not enough for general knowledge unless it is clearly labeled as internal evidence.
2. Official rules, papers, framework docs, or public engineering sources should be added when available.
3. Long copyrighted excerpts must not be copied.
```

## Conflict Check

```yaml
conflict_status: unchecked | none | potential | confirmed | resolved
checked_against:
  - CEK-TA knowledge item IDs or files
conflict_items:
  - knowledge_id: ""
    conflict_type: direct_conflict | scope_conflict | version_conflict | market_conflict | granularity_conflict | assumption_conflict
    resolution: ""
approval_allowed: false
```

Rules:

```text
1. unchecked cannot move beyond proposed.
2. potential or confirmed conflict must include applicability boundaries.
3. approval_allowed remains false until CEK-TA review.
```

## Suggested CEK-TA Output

```yaml
output_type: knowledge_item | skill_update | dataset_sample | eval_case | ui_task | reject
target_partition: ""
target_domain: ""
target_subdomain: ""
target_file: ""
expected_review_path: "proposed -> sanitized -> sourced -> classified -> conflict_checked -> reviewed -> accepted"
```

## Submission Steps

```text
1. Create this file inside the business project.
2. Fill Source Project Snapshot, Sanitization Gate, Applicability Boundary, Sources, and Conflict Check.
3. Copy the completed file into <cek_ta_path>/contributions/proposed/.
4. Do not edit CEK-TA approved knowledge.
5. Wait for CEK-TA review.
```

## Definition of Done

```text
1. status is proposed.
2. target_queue points to CEK-TA contributions/proposed.
3. direct_approved_write_allowed is false.
4. Sensitive data is removed or the contribution is rejected.
5. Sources and evidence are present.
6. Applicability and non-applicability are explicit.
7. Conflict status is not ignored.
8. Suggested CEK-TA output is clear.
```
