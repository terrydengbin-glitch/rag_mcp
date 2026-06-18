# Runtime Ranking Quality Report

## Report Identity

```text
report_id: cek_ta_runtime_ranking_quality_20260608
phase: Phase 20
task_id: CEK-TA-082
tested_at: 2026-06-08
eval_set: codex-expert-kit/rag/eval_sets/runtime_ranking_eval_cases.json
runtime: codex-expert-kit/mcp/search_expert_knowledge.py
knowledge_scope: Phase 17 seed knowledge, 10 approved items
```

## Purpose

本报告验证 MCP 轻量检索在 `top_k=5` 下是否能命中 Phase 17 的 10 条 seed 知识，并检查排序是否优先考虑查询相关性、来源、边界和阻断安全。

## Runtime Change

```text
1. tokenize 从保留下划线改为按字母/数字 token 拆分，使 bad_trade_taxonomy、risk_budget 等 ID 可被自然语言查询命中。
2. item_text 增加 procedure、examples、anti_patterns、assumptions、citation_notes、source_title、evidence_summary。
3. 排序键调整为 review_status approved -> lexical score -> source_quality high。
4. canonical_node_id、canonical_tree_path、canonical_tree_path_prefix 已纳入过滤和返回。
```

## Metrics

| Metric | Result |
| --- | --- |
| seed_case_count | 10 |
| top_k | 5 |
| target_in_top5_count | 10 |
| target_in_top5_rate | 1.0 |
| target_rank1_count | 10 |
| target_rank1_rate | 1.0 |
| source_return_rate | 1.0 |
| boundary_return_rate | 1.0 |
| unsafe_default_guidance_rate | 0.0 |

## Case Results

| Case | Expected Knowledge | Rank | Status |
| --- | --- | --- | --- |
| seed_runtime_001 | `kb_04_backtest.bias.multiple_testing_overfit.v1` | 1 | pass |
| seed_runtime_002 | `kb_04_backtest.fill_model.ohlc_same_bar_path_ambiguity.v1` | 1 | pass |
| seed_runtime_003 | `kb_02_kline_strategy.signal_boundary.timeframe_market_scope.v1` | 1 | pass |
| seed_runtime_004 | `kb_06_live_execution.risk_control.kill_switch_no_new_orders.v1` | 1 | pass |
| seed_runtime_005 | `kb_01_quant_foundation.risk_return.position_risk_budget_before_signal.v1` | 1 | pass |
| seed_runtime_006 | `kb_04_backtest.fill_model.explicit_slippage_fee_assumptions.v1` | 1 | pass |
| seed_runtime_007 | `kb_05_replay_simulation.execution_semantics.backtest_not_live_truth.v1` | 1 | pass |
| seed_runtime_008 | `kb_07_trade_analysis.bad_trade_taxonomy.root_cause_separation.v1` | 1 | pass |
| seed_runtime_009 | `kb_09_rag_engineering.source_quality.unsourced_default_block.v1` | 1 | pass |
| seed_runtime_010 | `kb_08_llm_training.eval_and_risk.source_boundary_human_escalation.v1` | 1 | pass |

## Safety Checks

```text
无 source_evidence 的知识不进入 results。
confirmed conflict 不进入 results。
deprecated 不进入 results。
draft 默认不进入 results。
rejected 不进入 results。
project_binding mismatch 不进入 results。
blocked_results 返回 blocked_reason 和 recommended_fix。
```

## Tests

```text
pytest codex-expert-kit/mcp/tests
18 passed

runtime_ranking_eval_cases.json
JSON parse passed
```

## Remaining Gaps

```text
1. 当前仍是轻量词法排序，不是向量检索或 reranker。
2. ranking quality 只覆盖 10 条 seed 知识，后续大规模知识入库后需要扩大评测集。
3. source_quality 目前作为同分加权使用，尚未做更细的可靠性评分融合。
```

## DoD

```text
10 条 seed ranking eval cases 存在: pass
目标知识 top_k=5 命中率有报告: pass
目标知识 top_k=5 命中率 >= 0.8: pass
阻断规则继续有效: pass
不引入数据库、后端或外部服务: pass
UTF-8 中文无乱码: pass
```
