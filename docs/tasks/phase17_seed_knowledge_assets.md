# Phase 17: 首批真实知识资产沉淀任务卡

## Phase 目标

基于前面建立的知识树、采集流水线、RAG 数据层、MCP 查询和质量评测体系，沉淀第一批可复用、可审计、可检索的高价值交易与 AI 专业知识资产。

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 |
| --- | --- | --- | --- | --- |
| CEK-TA-065 | P0 | done | 定义首批知识资产范围与验收标准 | `docs/seed_knowledge_assets_plan.md` |
| CEK-TA-066 | P1 | done | 创建首批 accepted 知识样例 | `codex-expert-kit/rag/knowledge/` |
| CEK-TA-067 | P1 | done | 对首批知识执行质量评测 | `docs/reports/seed_knowledge_quality_report.md` |

## 上游输入

```text
codex-expert-kit/rag/knowledge_tree.md
codex-expert-kit/rag/knowledge_item_schema.md
codex-expert-kit/rag/source_quality_rules.md
codex-expert-kit/rag/conflict_detection_rules.md
codex-expert-kit/rag/quality_metrics.md
codex-expert-kit/templates/research_ingestion_runbook.md
```

## 下游输出

```text
其他项目可复用知识
MCP 可检索数据
Vue3 可审计知识
质量评测基线
后续批量采集样板
```

## 输入契约

每条知识资产必须满足：

```text
有来源
有 source_type
有 domain/subdomain
有 knowledge_tree_node
有适用范围
有不适用场景
有 confidence
有 freshness
有 review_status
有 conflict_status
有 citation
```

## 输出契约

首批知识资产计划必须定义：

```text
target_count
topic_distribution
source_policy
review_policy
acceptance_threshold
excluded_topics
quality_report_path
```

建议第一批目标：

```text
20 条：回测偏差与数据质量
20 条：K线/指标使用边界
20 条：风控与仓位管理
15 条：交易执行与滑点
15 条：交易复盘与坏交易分类
10 条：LLM/RAG 在交易项目中的边界
```

## 边界范围

范围内：

```text
定义首批知识资产计划
沉淀少量高质量样例
执行来源和冲突审计
生成质量报告
```

范围外：

```text
不追求一次性填满全部知识树
不采集无来源观点
不直接接受冲突规则
不把项目私有案例写入通用知识
不提供投资建议或交易信号
```

## 涉及组件

```text
codex-expert-kit/rag/knowledge/
codex-expert-kit/rag/examples/
docs/seed_knowledge_assets_plan.md
docs/reports/
ui/src/views/
codex-expert-kit/mcp/
```

## 涉及数据结构

```text
KnowledgeItem
SourceRef
ConflictAudit
QualityReport
SeedAssetPlan
```

## 涉及数据库/存储

使用 Phase 13 定义的本地文件化正式知识存储。不得绕过 schema 写入自由格式知识。

## 实施步骤

1. 编写首批知识资产计划。
2. 按知识树节点选择高价值主题。
3. 使用 Phase 12 流程采集与生成候选知识。
4. 通过来源质量和冲突审计。
5. 将少量样例升级为 accepted。
6. 运行 Phase 16 质量评测。
7. 更新索引。

## Definition of Done

```text
首批知识资产计划存在
正式知识目录存在
每条 accepted 知识有来源和引用
每条 accepted 知识绑定知识树节点
每条 accepted 知识有适用与不适用范围
冲突状态明确
质量报告存在
UTF-8 中文无乱码
```

## 测试与验收

```text
检查 seed plan 存在
检查知识条目 schema 字段完整
检查来源引用可追踪
检查冲突状态不为 unchecked
使用 MCP 或检索脚本查询样例知识
检查质量报告存在
使用 Get-Content -Encoding UTF8 检查中文显示
```

## 风险与回滚

风险：

```text
知识质量不稳定
来源权威性不足
结论适用边界不清
用户误解为投资建议
```

回滚：

```text
未达标知识保持 candidate/review 状态
accepted 知识可降级为 deprecated 或 needs_review
质量报告记录降级原因
```

## 需要开发者确认的问题

```text
第一批知识目标数量是否按 100 条规划
是否指定优先市场和资产类别
是否允许联网采集并引用公开资料
```

当前执行决策：

```text
第一轮不一次性创建 100 条，先创建 10 条高质量 seed 样例，跑通真实知识闭环后再扩展。
优先市场和资产类别默认 general；涉及例子时可覆盖 crypto/multi，但不得形成交易信号。
允许联网采集和引用公开资料；所有正式知识必须记录 source_type、publisher、accessed_at、reliability 和 evidence_summary。
```

## 状态更新要求

完成后更新：

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase17_seed_knowledge_assets.md
```

## 进度记录

```yaml
current_status: done
completed_tasks:
  - CEK-TA-065
  - CEK-TA-066
  - CEK-TA-067
in_progress_tasks: []
remaining_tasks: []
deliverables:
  - docs/seed_knowledge_assets_plan.md
  - codex-expert-kit/rag/knowledge/KB_01_QUANT_FOUNDATION/kb_01_quant_foundation.risk_return.position_risk_budget_before_signal.v1.json
  - codex-expert-kit/rag/knowledge/KB_02_KLINE_STRATEGY/kb_02_kline_strategy.signal_boundary.timeframe_market_scope.v1.json
  - codex-expert-kit/rag/knowledge/KB_04_BACKTEST/kb_04_backtest.bias.multiple_testing_overfit.v1.json
  - codex-expert-kit/rag/knowledge/KB_04_BACKTEST/kb_04_backtest.fill_model.explicit_slippage_fee_assumptions.v1.json
  - codex-expert-kit/rag/knowledge/KB_04_BACKTEST/kb_04_backtest.fill_model.ohlc_same_bar_path_ambiguity.v1.json
  - codex-expert-kit/rag/knowledge/KB_05_REPLAY_SIMULATION/kb_05_replay_simulation.execution_semantics.backtest_not_live_truth.v1.json
  - codex-expert-kit/rag/knowledge/KB_06_LIVE_EXECUTION/kb_06_live_execution.risk_control.kill_switch_no_new_orders.v1.json
  - codex-expert-kit/rag/knowledge/KB_07_TRADE_ANALYSIS/kb_07_trade_analysis.bad_trade_taxonomy.root_cause_separation.v1.json
  - codex-expert-kit/rag/knowledge/KB_08_LLM_TRAINING/kb_08_llm_training.eval_and_risk.source_boundary_human_escalation.v1.json
  - codex-expert-kit/rag/knowledge/KB_09_RAG_ENGINEERING/kb_09_rag_engineering.source_quality.unsourced_default_block.v1.json
  - codex-expert-kit/rag/indexes/knowledge_index.json
  - codex-expert-kit/rag/indexes/source_index.json
  - codex-expert-kit/rag/indexes/conflict_index.json
  - docs/reports/seed_knowledge_quality_report.md
notes:
  - Phase 17 已完成首批 seed 闭环。
  - 第一轮 seed 目标为 10 条 accepted 知识资产。
  - CEK-TA-066 已完成 10/10 条 accepted seed 样例。
  - CEK-TA-067 已完成文件化质量报告。
  - 不采集实时行情、原始 K线或订单流数据。
  - 运行时 MCP 查询和 Vue3 渲染测试未在本阶段执行，已写入质量报告 top gaps。
```
