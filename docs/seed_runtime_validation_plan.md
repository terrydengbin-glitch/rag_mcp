# CEK-TA Seed Runtime Validation Plan

本文定义 Phase 19 的运行时验证计划，用 MCP/SearchLab 查询 Phase 17 的 10 条 accepted seed 知识，确认默认指导能命中、能返回来源和适用边界，并能阻断不安全知识。

## 计划身份

```yaml
plan_id: cek_ta_seed_runtime_validation_20260608
phase: Phase 19
status: doing
created_at: 2026-06-08
updated_at: 2026-06-08
encoding: UTF-8
```

## 目标

```text
1. 验证 10 条 seed 知识可以被 MCP search_expert_knowledge 查询命中。
2. 验证命中结果包含 source_refs、applicable_scope、not_applicable_scope、review_status、conflict_status、recommended_next_action。
3. 验证 default guidance 阻断无来源、confirmed conflict、deprecated、draft、rejected、project mismatch。
4. 验证 SearchLab 至少能展示 seed 查询用例和命中结果。
5. 把运行时验证结果写入报告，为后续外部项目接入提供 smoke test 基线。
```

## MCP 查询用例

| Case ID | Query | task_type | Expected Seed |
| --- | --- | --- | --- |
| `seed_runtime_001` | `multiple testing overfitting backtest bias` | `backtest_review` | `kb_04_backtest.bias.multiple_testing_overfit.v1` |
| `seed_runtime_002` | `OHLC same bar take profit stop loss fill model` | `backtest_review` | `kb_04_backtest.fill_model.ohlc_same_bar_path_ambiguity.v1` |
| `seed_runtime_003` | `Kline indicator signal timeframe market boundary` | `strategy_design` | `kb_02_kline_strategy.signal_boundary.timeframe_market_scope.v1` |
| `seed_runtime_004` | `live trading kill switch no new orders` | `live_trading` | `kb_06_live_execution.risk_control.kill_switch_no_new_orders.v1` |
| `seed_runtime_005` | `position sizing risk budget before signal` | `strategy_design` | `kb_01_quant_foundation.risk_return.position_risk_budget_before_signal.v1` |
| `seed_runtime_006` | `backtest fill model slippage fee assumptions` | `backtest_review` | `kb_04_backtest.fill_model.explicit_slippage_fee_assumptions.v1` |
| `seed_runtime_007` | `simulation execution semantics backtest not live truth` | `simulation` | `kb_05_replay_simulation.execution_semantics.backtest_not_live_truth.v1` |
| `seed_runtime_008` | `bad trade taxonomy signal execution risk data root cause` | `trade_analysis` | `kb_07_trade_analysis.bad_trade_taxonomy.root_cause_separation.v1` |
| `seed_runtime_009` | `unsourced RAG knowledge default guidance block` | `rag_engineering` | `kb_09_rag_engineering.source_quality.unsourced_default_block.v1` |
| `seed_runtime_010` | `LLM RAG output source boundary human escalation trading` | `llm_training` | `kb_08_llm_training.eval_and_risk.source_boundary_human_escalation.v1` |

## MCP 成功断言

```text
1. status 不为 error。
2. top_k 结果中包含 expected knowledge_id。
3. 命中结果 review_status = approved。
4. 命中结果 conflict_status = none 或 resolved。
5. 命中结果 source_refs 非空。
6. 命中结果 applicable_scope.applies_when 非空。
7. 命中结果 not_applicable_scope 非空。
8. 命中结果 recommended_next_action 不为 no_default_guidance。
```

## 阻断回归用例

| Case ID | 构造项 | Expected |
| --- | --- | --- |
| `blocking_unsourced` | approved 但 source_evidence 为空 | default guidance 不返回 |
| `blocking_confirmed_conflict` | conflict_status = confirmed | default guidance 不返回 |
| `blocking_deprecated` | review_status = deprecated 或 freshness = deprecated | default guidance 不返回 |
| `blocking_draft` | review_status = draft | default guidance 不返回 |
| `blocking_rejected` | review_status = rejected | default guidance 不返回 |
| `blocking_project_mismatch` | project_binding 不等于 active project | default guidance 不返回 |

## SearchLab 验证

SearchLab 至少展示：

```text
seed_runtime_002: OHLC same bar TP/SL
seed_runtime_004: live trading kill switch
seed_runtime_009: unsourced RAG default block
```

每条展示必须包含：

```text
query
task_type
filters
matches[].item_id
matches[].title
matches[].tree_path
matches[].review_status
matches[].conflict_status
matches[].recommended_next_action
warnings when relevant
```

## 边界

```text
1. 不做真实交易。
2. 不读取账户、密钥或项目私有数据。
3. 不引入数据库或外部 RAG 服务。
4. 不改变 MCP 权限。
5. 不采集实时行情或 K线数据。
```

## DoD

```text
1. MCP seed 查询测试通过。
2. MCP 阻断回归测试通过。
3. SearchLab seed 用例存在。
4. 运行时验证报告存在。
5. UTF-8 中文无乱码。
```
