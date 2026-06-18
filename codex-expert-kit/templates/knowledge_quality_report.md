# CEK-TA Knowledge Quality Report

本模板用于记录知识库质量评测、检索回归、v1/v2 路由一致性、来源完整性、冲突安全和外部项目复用情况。质量报告只作为审计与优化依据，不能自动批准或删除知识。

## Report Identity

```yaml
report_id: cek_ta_quality_YYYYMMDD_slug
report_version: 1.0.0
period_start: YYYY-MM-DD
period_end: YYYY-MM-DD
created_at: YYYY-MM-DD
created_by: codex | human | mixed
status: draft | reviewed | approved | rejected
```

## Scope

```yaml
tree_version: v1 | v2 | mixed
default_tree: codex-expert-kit/rag/knowledge_tree.md
canonical_tree: codex-expert-kit/rag/knowledge_tree_v2.md
partitions:
  - KB_04_BACKTEST
domains:
  - backtest
node_ids:
  - kt.backtest.bias
canonical_node_ids:
  - kt.trading_engineering.backtest.bias
eval_level: smoke | regression | release | audit
```

## Input Inventory

```yaml
knowledge_item_count: 0
approved_item_count: 0
reviewed_item_count: 0
draft_item_count: 0
source_count: 0
conflict_audit_count: 0
retrieval_eval_case_count: 0
qa_eval_case_count: 0
routing_eval_case_count: 0
external_usage_log_count: 0
contribution_record_count: 0
```

## Score Summary

```yaml
overall_quality_score: 0.0
coverage_score: 0.0
source_quality_score: 0.0
conflict_safety_score: 0.0
freshness_score: 0.0
retrieval_quality_score: 0.0
citation_completeness_score: 0.0
boundary_quality_score: 0.0
review_readiness_score: 0.0
reuse_score: 0.0
tree_routing_score: 0.0
```

## Core Rates

```yaml
coverage:
  leaf_coverage_rate: 0.0
  approved_leaf_rate: 0.0
  required_type_coverage: 0.0
  overgrown_node_rate: 0.0

source:
  source_presence_rate: 0.0
  medium_high_source_rate: 0.0
  primary_source_rate: 0.0
  source_scope_match_rate: 0.0
  low_only_approved_count: 0

conflict:
  conflict_rate: 0.0
  unresolved_confirmed_conflict_count: 0
  approved_unchecked_conflict_count: 0
  scope_boundary_resolution_rate: 0.0
  unsafe_default_guidance_rate: 0.0

freshness:
  time_sensitive_review_rate: 0.0
  staleness_rate: 0.0
  high_impact_stale_count: 0
  deprecated_return_rate: 0.0

retrieval:
  retrieval_hit_rate: 0.0
  top1_node_accuracy: 0.0
  citation_completeness: 0.0
  boundary_preservation_rate: 0.0
  recommended_action_accuracy: 0.0

tree_routing:
  v1_v2_route_consistency_rate: 0.0
  alias_resolution_success_rate: 0.0
  alias_mismatch_block_rate: 0.0
  split_target_default_block_rate: 0.0
  routing_warning_completeness: 0.0

reuse:
  reuse_count: 0
  reuse_project_count: 0
  contribution_acceptance_rate: 0.0
  rejected_private_fact_rate: 0.0
  post_reuse_issue_rate: 0.0
```

## Regression Result

```yaml
eval_sets:
  retrieval: codex-expert-kit/rag/eval_sets/retrieval_eval_cases.json
  qa: codex-expert-kit/rag/eval_sets/qa_eval_cases.json
  tree_routing: codex-expert-kit/rag/eval_sets/tree_routing_eval_cases.json

baseline:
  report_id: ""
  overall_quality_score: 0.0
  unsafe_default_guidance_rate: 0.0
candidate:
  report_id: ""
  overall_quality_score: 0.0
  unsafe_default_guidance_rate: 0.0
delta:
  overall_quality_score: 0.0
  retrieval_hit_rate: 0.0
  citation_completeness: 0.0
  v1_v2_route_consistency_rate: 0.0
release_decision: pass | fail | needs_review
```

## Hard Gates

Release or accepted-ingestion must be blocked when any item is true:

```text
1. unsafe_default_guidance_rate > 0
2. unresolved_confirmed_conflict_count > 0 for approved/default scope
3. low_only_approved_count > 0
4. source_presence_rate < 1.0 for reviewed/approved scope
5. alias_mismatch_block_rate < 1.0
6. approved knowledge lacks applicable_scope or not_applicable_scope
7. high-impact stale knowledge is returned without warning
```

Current gate result:

```yaml
hard_gate_status: pass | fail | needs_review
blocking_issue_count: 0
```

## Top Gaps

```json
[
  {
    "gap_id": "gap_001",
    "severity": "critical | high | medium | low",
    "area": "coverage | source | conflict | freshness | retrieval | routing | reuse",
    "node_id": "string | null",
    "canonical_node_id": "string | null",
    "description": "string",
    "impact": "string",
    "recommended_action": "string",
    "owner": "codex | human | mixed | null"
  }
]
```

## Blocking Issues

```json
[
  {
    "issue_id": "issue_001",
    "severity": "critical | high",
    "blocked_scope": "default_guidance | ingestion_acceptance | release | external_reuse",
    "related_case_id": "string | null",
    "related_knowledge_id": "string | null",
    "reason": "string",
    "required_fix": "string",
    "rollback": "string"
  }
]
```

## Recommended Actions

```json
[
  {
    "action_id": "action_001",
    "priority": "P0 | P1 | P2",
    "action_type": "collect_source | split_scope | resolve_conflict | add_eval_case | refresh_source | improve_retrieval | update_alias | create_leaf_package",
    "target": "string",
    "reason": "string",
    "expected_quality_impact": "string",
    "done_when": "string"
  }
]
```

## Human Review Notes

```text
记录人工审计结论、不能自动判断的理论冲突、需要开发者确认的重大决策，以及下一轮采集或修复建议。
```

## Boundaries

```text
1. 本报告不自动批准知识。
2. 本报告不自动删除低分知识。
3. 本报告不引入外部评测服务。
4. 本报告不采集实时行情、K线或订单数据。
5. 本报告不改变 MCP 权限。
6. 本报告不改变默认知识树。
```

## DoD Checklist

```text
1. report_id、period、scope 完整。
2. 输入数据清单完整。
3. 指标结果包含覆盖率、来源、冲突、时效、检索、引用、边界、路由和复用。
4. hard gates 明确 pass/fail/needs_review。
5. top_gaps 和 recommended_actions 可执行。
6. 阻断问题有 required_fix 和 rollback。
7. UTF-8 中文可读，无乱码。
```
