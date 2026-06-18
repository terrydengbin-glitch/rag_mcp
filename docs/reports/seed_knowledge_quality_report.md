# CEK-TA Seed Knowledge Quality Report

## Report Identity

```yaml
report_id: cek_ta_quality_20260608_seed_knowledge_assets
report_version: 1.0.0
period_start: 2026-06-08
period_end: 2026-06-08
created_at: 2026-06-08
created_by: codex
status: approved
```

## Scope

```yaml
phase: Phase 17
tree_version: mixed
default_tree: codex-expert-kit/rag/knowledge_tree.md
canonical_tree: codex-expert-kit/rag/knowledge_tree_v2.md
knowledge_storage_root: codex-expert-kit/rag/knowledge/
index_storage_root: codex-expert-kit/rag/indexes/
eval_level: seed_release
```

参与评测的分区：

```text
KB_01_QUANT_FOUNDATION
KB_02_KLINE_STRATEGY
KB_04_BACKTEST
KB_05_REPLAY_SIMULATION
KB_06_LIVE_EXECUTION
KB_07_TRADE_ANALYSIS
KB_08_LLM_TRAINING
KB_09_RAG_ENGINEERING
```

## Input Inventory

```yaml
knowledge_item_count: 10
approved_item_count: 10
reviewed_item_count: 0
draft_item_count: 0
source_count: 14
conflict_audit_count: 10
knowledge_index_records: 10
source_index_records: 14
conflict_index_records: 10
retrieval_eval_case_count: 12
external_usage_log_count: 0
contribution_record_count: 0
```

## Seed Knowledge Items

| ID | Area | Status | Sources | Conflict |
| --- | --- | --- | ---: | --- |
| `kb_04_backtest.bias.multiple_testing_overfit.v1` | 回测偏差 | approved | 1 | none |
| `kb_04_backtest.fill_model.ohlc_same_bar_path_ambiguity.v1` | 回测成交模型 | approved | 2 | none |
| `kb_02_kline_strategy.signal_boundary.timeframe_market_scope.v1` | K线/指标边界 | approved | 1 | none |
| `kb_06_live_execution.risk_control.kill_switch_no_new_orders.v1` | 实盘风控 | approved | 2 | none |
| `kb_01_quant_foundation.risk_return.position_risk_budget_before_signal.v1` | 仓位风险预算 | approved | 1 | none |
| `kb_04_backtest.fill_model.explicit_slippage_fee_assumptions.v1` | 回测滑点费用 | approved | 2 | none |
| `kb_05_replay_simulation.execution_semantics.backtest_not_live_truth.v1` | 模拟盘/实盘语义 | approved | 2 | none |
| `kb_07_trade_analysis.bad_trade_taxonomy.root_cause_separation.v1` | 坏交易分类 | approved | 2 | none |
| `kb_09_rag_engineering.source_quality.unsourced_default_block.v1` | RAG 来源质量 | approved | 3 | none |
| `kb_08_llm_training.eval_and_risk.source_boundary_human_escalation.v1` | LLM/RAG 风险输出 | approved | 3 | none |

## Score Summary

```yaml
overall_quality_score: 0.91
coverage_score: 0.82
source_quality_score: 0.93
conflict_safety_score: 1.00
freshness_score: 0.90
retrieval_quality_score: 0.82
citation_completeness_score: 1.00
boundary_quality_score: 1.00
review_readiness_score: 0.95
reuse_score: 0.00
tree_routing_score: 0.90
```

说明：

```text
reuse_score 为 0 是预期状态，因为首批 seed 尚未被外部项目真实调用。
retrieval_quality_score 基于文件化索引和 eval case 覆盖判断，未代表完整向量检索效果。
tree_routing_score 基于每条知识已双写 tree_node_id 与 canonical_node_id；alias mismatch 阻断仍待 MCP/RAG 运行时测试覆盖。
```

## Core Rates

```yaml
coverage:
  seed_target_count: 10
  seed_completed_count: 10
  seed_completion_rate: 1.0
  approved_leaf_rate_for_seed_scope: 1.0

source:
  source_presence_rate: 1.0
  medium_high_source_rate: 1.0
  low_only_approved_count: 0
  primary_or_high_source_item_count: 8

conflict:
  conflict_rate: 0.0
  unresolved_confirmed_conflict_count: 0
  approved_unchecked_conflict_count: 0
  unsafe_default_guidance_rate: 0.0

freshness:
  time_sensitive_item_count: 5
  time_sensitive_review_rate: 1.0
  high_impact_stale_count: 0
  deprecated_return_rate: 0.0

retrieval:
  knowledge_index_records: 10
  citation_completeness: 1.0
  boundary_preservation_rate: 1.0
  recommended_action_accuracy: "not_runtime_tested"

tree_routing:
  v1_canonical_dual_mapping_rate: 1.0
  alias_resolution_success_rate: "not_runtime_tested"
  alias_mismatch_block_rate: "defined_in_eval_set_not_runtime_tested"
  split_target_default_block_rate: "defined_in_eval_set_not_runtime_tested"

reuse:
  reuse_count: 0
  reuse_project_count: 0
  contribution_acceptance_rate: "not_applicable"
```

## Hard Gates

| Gate | Result | Evidence |
| --- | --- | --- |
| `unsafe_default_guidance_rate > 0` | pass | 所有 approved 条目均有来源，冲突为 none |
| `unresolved_confirmed_conflict_count > 0` | pass | conflict_index 中 10 条均为 none |
| `low_only_approved_count > 0` | pass | 无 low-only approved 条目 |
| `source_presence_rate < 1.0` | pass | 10/10 条有 source_evidence |
| `approved knowledge lacks applicability boundary` | pass | 10/10 条有 applies_when 和 not_applicable_when |
| `high-impact stale knowledge returned without warning` | pass | 高风险 time_sensitive 条目均有 accessed_at/reviewed_at |
| `project-private fact promoted to general` | pass | 全部 contribution 为 not_applicable，private_data_removed=true |

```yaml
hard_gate_status: pass
blocking_issue_count: 0
```

## Regression Result

```yaml
eval_sets:
  retrieval: codex-expert-kit/rag/eval_sets/retrieval_eval_cases.json
  qa: codex-expert-kit/rag/eval_sets/qa_eval_cases.json
  tree_routing: codex-expert-kit/rag/eval_sets/tree_routing_eval_cases.json

file_contract_checks:
  json_parse: pass
  index_parse: pass
  source_presence: pass
  conflict_status: pass
  review_status: pass
  tree_mapping: pass
  utf8_mojibake_check: pass

runtime_checks:
  mcp_runtime_query: not_run
  vector_retrieval_query: not_run
  vue_render_check: not_run

release_decision: pass_for_file_based_seed_release
```

## Top Gaps

```json
[
  {
    "gap_id": "gap_001",
    "severity": "medium",
    "area": "retrieval",
    "description": "当前质量评测基于文件化索引，尚未执行真实向量检索或 MCP runtime 查询。",
    "impact": "不能代表最终 RAG 排序质量，只能证明正式知识契约和索引可用。",
    "recommended_action": "在下一轮为 Phase 14 MCP runtime 增加 seed knowledge query smoke tests。"
  },
  {
    "gap_id": "gap_002",
    "severity": "medium",
    "area": "source",
    "description": "仓位风险预算和坏交易分类主要使用 medium 来源或内部来源。",
    "impact": "可作为 seed，但后续批量扩展时应补充更权威来源或脱敏复盘证据。",
    "recommended_action": "为 position sizing 和 bad trade taxonomy 增加高质量书籍、论文或机构文档来源。"
  },
  {
    "gap_id": "gap_003",
    "severity": "low",
    "area": "reuse",
    "description": "尚无外部项目真实复用日志。",
    "impact": "reuse_score 初始为 0，不能判断跨项目价值。",
    "recommended_action": "让其他交易项目通过 MCP 调用 3-5 个 seed 知识并回传使用记录。"
  }
]
```

## Blocking Issues

```json
[]
```

## Recommended Actions

```json
[
  {
    "action_id": "action_001",
    "priority": "P0",
    "action_type": "runtime_test",
    "target": "codex-expert-kit/mcp/tests/",
    "reason": "验证 approved seed 是否能被 MCP default_guidance 正确返回并保留 source_refs。",
    "done_when": "10 条 seed 均可通过 MCP 查询命中或按预期阻断。"
  },
  {
    "action_id": "action_002",
    "priority": "P1",
    "action_type": "source_expansion",
    "target": "position_sizing and bad_trade_taxonomy",
    "reason": "补强 medium-only 或 internal-heavy 知识的外部来源。",
    "done_when": "相关知识至少有一个 high reliability 外部来源。"
  },
  {
    "action_id": "action_003",
    "priority": "P1",
    "action_type": "vue_audit",
    "target": "ui/src/views/KnowledgeDetail.vue",
    "reason": "让 Vue3 可直接展示 seed 知识的 source、boundary、conflict、canonical mapping。",
    "done_when": "审计界面能展示 10 条 seed 的关键 metadata。"
  }
]
```

## Human Review Notes

```text
首批 10 条 seed 已满足文件化正式知识入库要求。
本报告不声称这些知识覆盖完整交易工程知识树。
本报告不提供投资建议、交易信号或收益承诺。
后续扩展应优先补运行时检索测试、外部项目复用记录和更权威来源。
```

## Boundaries

```text
1. 本报告不自动批准后续新知识。
2. 本报告不自动删除低分知识。
3. 本报告不采集实时行情、K线或订单流原始数据。
4. 本报告不改变 MCP 权限。
5. 本报告不改变默认知识树。
6. 本报告不代表实盘交易建议。
```

## DoD Checklist

```text
1. report_id、period、scope 完整。pass
2. 输入数据清单完整。pass
3. 指标结果包含覆盖率、来源、冲突、时效、检索、引用、边界、路由和复用。pass
4. hard gates 明确 pass/fail/needs_review。pass
5. top_gaps 和 recommended_actions 可执行。pass
6. 阻断问题有 required_fix 和 rollback。pass: 当前无阻断问题
7. UTF-8 中文可读，无乱码。pass
```
