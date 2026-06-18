# Phase 23 ResearchIngestionTask 队列

本队列用于启动 13 个 KB 分区的专业知识采集。状态为 `todo` 的任务尚未采集；`researching` 表示正在联网搜索；`candidate_ready` 表示候选包已生成但未审计；`accepted_for_draft` 只表示可转换为正式知识 draft，不表示 approved。

## 状态定义

```text
todo: 未开始
researching: 正在联网搜索和阅读
candidate_ready: 候选包已生成
needs_review: 等待人工审计
accepted_for_draft: 可转正式知识 draft
rejected: 不适合入库
blocked: 缺少来源或存在未解决冲突
```

## 任务总览

| ID | 优先级 | 状态 | 分区 | 主题 | 目标节点 | 预期产物 |
| --- | --- | --- | --- | --- | --- | --- |
| CEK-TA-RESEARCH-20260608-023-001 | P0 | candidate_ready | `KB_04_BACKTEST` | 回测前视偏差、数据泄漏、过拟合与多重测试风险 | `kt.trading_engineering.backtest.bias` | checklist、anti_pattern、eval_case |
| CEK-TA-RESEARCH-20260608-023-002 | P0 | candidate_ready | `KB_05_REPLAY_SIMULATION` | OHLC 同根 TP/SL、fill model、滑点和延迟假设 | `kt.trading_engineering.replay_simulation.fill_model` | principle、procedure、eval_case |
| CEK-TA-RESEARCH-20260608-023-003 | P0 | candidate_ready | `KB_06_LIVE_EXECUTION` | 实盘订单状态机、仓位同步、安全停机和异常恢复 | `kt.trading_engineering.live_execution.order_state_machine` | procedure、checklist、incident |
| CEK-TA-RESEARCH-20260608-023-004 | P0 | candidate_ready | `KB_07_RISK_MANAGEMENT` | 风控闸门、单笔风险、组合暴露、日亏损限制和 ruin risk | `kt.trading_engineering.risk_management.risk_gate` | principle、procedure、checklist |
| CEK-TA-RESEARCH-20260608-023-005 | P0 | candidate_ready | `KB_10_RAG_ENGINEERING` | RAG metadata、citation、conflict-aware retrieval 和 freshness policy | `kt.ai_engineering.rag_engineering.retrieval_policy` | schema、procedure、eval_case |
| CEK-TA-RESEARCH-20260608-023-006 | P0 | candidate_ready | `KB_11_MCP_ENGINEERING` | MCP tool contract、只读权限、错误结构和观测性 | `kt.ai_engineering.mcp_engineering.tool_contract` | schema、procedure、anti_pattern |
| CEK-TA-RESEARCH-20260608-023-007 | P0 | candidate_ready | `KB_13_KNOWLEDGE_GOVERNANCE` | 知识状态生命周期、来源评分、冲突阻断和废弃策略 | `kt.knowledge_governance.status_lifecycle` | schema、procedure、audit_rule |
| CEK-TA-RESEARCH-20260608-023-008 | P1 | todo | `KB_01_QUANT_FOUNDATION` | 期望值、风险收益比、成本和仓位公式适用边界 | `kt.trading_engineering.quant_foundation.ev_rr_cost` | formula、principle、checklist |
| CEK-TA-RESEARCH-20260608-023-009 | P1 | todo | `KB_02_DATA_ENGINEERING` | 交易数据时间对齐、缺失重复、时区、数据版本和特征泄漏 | `kt.trading_engineering.data_engineering.time_alignment` | schema、procedure、checklist |
| CEK-TA-RESEARCH-20260608-023-010 | P1 | todo | `KB_03_STRATEGY_ENGINEERING` | K线结构、指标边界、微观结构和衍生品流解释边界 | `kt.trading_engineering.strategy_engineering.kline_strategy.market_structure` | definition、principle、anti_pattern |
| CEK-TA-RESEARCH-20260608-023-011 | P1 | todo | `KB_08_TRADE_ANALYSIS` | 交易质量、坏例 taxonomy、R/R 分解、成本分解和迭代闭环 | `kt.trading_engineering.trade_analysis.trade_quality_metrics` | taxonomy、procedure、eval_case |
| CEK-TA-RESEARCH-20260608-023-012 | P1 | todo | `KB_09_LLM_TRAINING` | RAG vs finetune、dataset card、训练/评测泄漏和数据授权 | `kt.ai_engineering.llm_training.dataset_design` | checklist、anti_pattern、eval_case |
| CEK-TA-RESEARCH-20260608-023-013 | P1 | todo | `KB_12_PROJECT_INTEGRATION` | 外部项目 adapter、truth boundary、healthcheck 和知识回灌边界 | `kt.project_integration.adapter` | adapter_rule、procedure、checklist |

## 任务详情模板

每个任务执行时必须填写：

```yaml
research_task_id: CEK-TA-RESEARCH-20260608-023-001
status: todo
topic: ""
target_node_id: ""
tree_path: ""
partition_id: ""
domain: ""
subdomain: ""
question_set:
  - ""
source_policy:
  preferred_source_types: []
  minimum_reliability: medium
freshness_requirement: stable
must_include_sources: []
must_exclude_sources: []
conflict_check_scope:
  domain: ""
  subdomain: ""
  related_tree_nodes: []
expected_outputs: []
reviewer: mixed
created_at: 2026-06-08
updated_at: 2026-06-08
```

## P0 执行契约

```text
1. P0 任务优先执行，因为它们影响安全、回测可信度、检索可信度和知识治理。
2. 每个 P0 任务至少需要 1 个 high 或 medium 来源。
3. 涉及官方文档或框架行为时必须记录 accessed_at。
4. 每个 P0 候选必须执行 conflict_audit。
5. 候选状态最多到 candidate_ready 或 needs_review，不能直接 approved。
```

## 分区覆盖检查

```text
KB_01_QUANT_FOUNDATION: covered
KB_02_DATA_ENGINEERING: covered
KB_03_STRATEGY_ENGINEERING: covered
KB_04_BACKTEST: covered
KB_05_REPLAY_SIMULATION: covered
KB_06_LIVE_EXECUTION: covered
KB_07_RISK_MANAGEMENT: covered
KB_08_TRADE_ANALYSIS: covered
KB_09_LLM_TRAINING: covered
KB_10_RAG_ENGINEERING: covered
KB_11_MCP_ENGINEERING: covered
KB_12_PROJECT_INTEGRATION: covered
KB_13_KNOWLEDGE_GOVERNANCE: covered
```

## 当前不做

```text
1. 不把本队列主题视为已验证知识。
2. 不直接生成 approved 知识。
3. 不采集实时行情、K线或订单流原始数据。
4. 不把项目私有经验提升为通用规则。
```
