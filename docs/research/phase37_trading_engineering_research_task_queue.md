# Phase 37 Trading Engineering P0 ResearchIngestionTask 队列

## 目标

本队列把 Phase 37 的 96 条 Trading Engineering P0 知识点拆成可执行的 ResearchIngestionTask。每个任务都必须经过联网检索、来源评分、冲突检测、候选 JSON 生成、AI/人工审计包导出，才能进入 formal reviewed/caveat_only 沉淀流程。

## 执行顺序

| 批次 | 分组 | 数量 | 状态 | 说明 |
| --- | --- | ---: | --- | --- |
| P37-A | Quant Foundation / 量化基础 | 12 | formal_reviewed_validated | 12 条已沉淀 formal reviewed/caveat_only，并完成全量联动验证 |
| P37-B | Data Engineering / 市场数据工程 | 12 | formal_reviewed_validated | 12 条已沉淀 formal reviewed/caveat_only，并完成全量联动验证 |
| P37-E | Backtest / 回测可信度 | 12 | formal_reviewed_validated | 12 条已沉淀 formal reviewed/caveat_only，并完成全量联动验证 |
| P37-F | Replay / Simulation / 回放与模拟 | 12 | formal_reviewed_validated | 12 条已沉淀 formal reviewed/caveat_only，并完成全量联动验证 |
| P37-G | Live Execution / Risk Management / 实盘执行与风控 | 12 | formal_reviewed_validated | 12 条已沉淀 formal reviewed/caveat_only，其中 Live Execution 6 条、Risk Management 6 条；approved/default guidance/hard gate/risk threshold advice 仍关闭 |
| P37-H | Trade Analysis / 交易复盘 | 12 | formal_reviewed_validated | 12 条已按补证再审结果沉淀为 formal reviewed/caveat_only，并完成 knowledge_items、Vue3、MCP/SearchLab/KnowledgeTree 联动验证；approved/default guidance/hard gate/risk threshold advice 仍关闭 |
| P37-C | Kline / Strategy Engineering / K 线与策略工程 | 12 | formal_reviewed_validated | 12 条已沉淀 formal reviewed/caveat_only，并完成全量联动验证 |
| P37-D | Market Microstructure / 市场微观结构 | 12 | formal_reviewed_validated | 12 条已沉淀 formal reviewed/caveat_only，并完成全量联动验证 |

## ResearchIngestionTask 契约

```json
{
  "research_task_id": "P37-A-Q01",
  "knowledge_slug": "quant_foundation.expected_value_definition.v1",
  "primary_partition": "KB_01_QUANT_FOUNDATION",
  "canonical_node_id": "kt.trading_engineering.quant_foundation.expected_value_definition",
  "priority": "P0",
  "status": "candidate_ready | todo | needs_more_evidence | reviewed",
  "required_source_types": [
    "official_doc",
    "paper",
    "regulatory_doc",
    "professional_research",
    "framework_doc"
  ],
  "minimum_source_count": 2,
  "must_define": [
    "applicability",
    "not_applicable_when",
    "assumptions",
    "conflict_audit",
    "llm_usage_policy",
    "machine_gate"
  ]
}
```

## P37-A Quant Foundation 首批任务

| ID | knowledge_slug | primary_partition | 状态 |
| --- | --- | --- | --- |
| P37-A-Q01 | quant_foundation.expected_value_definition.v1 | KB_01_QUANT_FOUNDATION | candidate_ready |
| P37-A-Q02 | quant_foundation.r_multiple_definition.v1 | KB_01_QUANT_FOUNDATION | candidate_ready |
| P37-A-Q03 | quant_foundation.risk_reward_boundary.v1 | KB_01_QUANT_FOUNDATION | candidate_ready |
| P37-A-Q04 | quant_foundation.cost_adjusted_expectancy_required.v1 | KB_01_QUANT_FOUNDATION | candidate_ready |
| P37-A-Q05 | quant_foundation.win_rate_not_enough.v1 | KB_01_QUANT_FOUNDATION | candidate_ready |
| P37-A-Q06 | quant_foundation.position_sizing_requires_risk_unit.v1 | KB_01_QUANT_FOUNDATION | candidate_ready |
| P37-A-Q07 | quant_foundation.leverage_amplifies_drawdown.v1 | KB_01_QUANT_FOUNDATION | candidate_ready |
| P37-A-Q08 | quant_foundation.signal_decision_execution_separation.v1 | KB_01_QUANT_FOUNDATION | candidate_ready |
| P37-A-Q09 | quant_foundation.trade_frequency_vs_quality_boundary.v1 | KB_01_QUANT_FOUNDATION | candidate_ready |
| P37-A-Q10 | quant_foundation.edge_requires_out_of_sample_evidence.v1 | KB_01_QUANT_FOUNDATION | candidate_ready |
| P37-A-Q11 | quant_foundation.sample_size_and_regime_caveat.v1 | KB_01_QUANT_FOUNDATION | candidate_ready |
| P37-A-Q12 | quant_foundation.no_profit_claim_without_costs.v1 | KB_01_QUANT_FOUNDATION | candidate_ready |

## 首批来源方向

P37-A 已优先选择以下来源类型：

```text
1. CFA Institute 交易执行、市场风险资料。
2. Morgan Stanley expected value / payoff 研究。
3. SEC / FINRA / CFTC / NFA 对 margin、leverage、day trading、forex/virtual currency risk 的公开监管资料。
4. Bailey 等关于回测过拟合和样本外证据的论文。
5. Investopedia / Trademetria / CrossTrade 等作为低权重辅助说明来源。
```

## 后续审计要求

```text
1. P37-A 审计通过后，才能转 formal reviewed/caveat_only。
2. P37-A 不得直接写 approved、default guidance 或 hard gate。
3. 若外部审计认为某些来源不足，先补证再二审。
4. 若外部审计认为某条知识更适合 AI Engineering，必须移出 Trading Engineering 或改成引用关系。
```
