# Phase 44: AI Trader Project Gap Audit

## Phase 目标

基于当前 CEK-TA 正式知识库，设计一个“AI 交易者项目”的理论方案审计任务，用端到端业务链路检查知识库是否能支撑外接项目完成方案设计、数据收集、数据治理、交易分析、AI 训练、持续学习、模拟盘、实盘风控和知识记忆。

本 Phase 不实现交易系统，不创建数据库，不连接交易所，不训练模型，不生成买卖点、仓位、止损止盈或实盘指令。它只做知识库覆盖度审计和断层识别。

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-371 | P0 | done | 创建 Phase 44 任务卡并登记任务索引 | `docs/tasks/phase44_ai_trader_project_gap_audit.md`、`docs/index_tasks.md`、`docs/tasks/README.md` | CEK-TA-370 |
| CEK-TA-372 | P0 | done | 生成 AI 交易者项目方案断层审计任务 JSON，供 AI/人工复核 | `docs/audit/phase44_ai_trader_project_gap_audit_task.json` | CEK-TA-371 |
| CEK-TA-373 | P0 | done | 使用当前正式知识库推演 AI 交易者项目理论方案，并输出知识断层报告 | `docs/reports/phase44_ai_trader_project_gap_audit_report.md` | CEK-TA-372 |
| CEK-TA-374 | P0 | done | 聚焦 AI 层技术底座重新推演业务流拓扑，排除 Trading Engineering 本体断点 | `docs/reports/phase44_ai_layer_business_flow_topology.md` | CEK-TA-373 |

## 上游输入

```text
1. codex-expert-kit/rag/indexes/knowledge_items.json
2. Phase 36 AI Engineering gating/scoring 知识
3. Phase 38 AI 模型平台与交易 Gating/Scoring POC 知识
4. Phase 40 持续学习与再训练闭环知识
5. Phase 41 Hybrid Scoring 与 Qwen3 审计助手知识
6. Phase 42 Database / Data Contract / Storage Engineering 知识
7. Phase 43 External Project AI Memory Layer 知识
8. 既有 Trading Engineering seed 知识：量化基础、K 线边界、回测、回放、实盘执行、风控
```

## 下游输出

```text
1. AI 交易者项目理论方案审计任务。
2. 当前知识库可支撑的端到端方案骨架。
3. 知识断层清单，说明哪些地方已有知识、哪些地方薄弱、哪些地方缺正式知识。
4. 后续 Phase 或知识采集优先级建议。
```

## 输入契约

审计任务输入必须包含：

```text
knowledge_index_path
project_goal
workflow_stages
required_domains
hard_boundaries
expected_output_schema
review_questions
```

## 输出契约

审计报告必须包含：

```text
1. 当前知识库总体覆盖情况。
2. AI 交易者端到端理论方案。
3. 每个阶段引用的代表性知识点。
4. 断层分类：missing / thin / contract_gap / runtime_gap / governance_gap。
5. 风险优先级：P0 / P1 / P2。
6. 后续建议：补知识、补契约、补评测、补运行时验证。
```

## 边界范围

范围内：

```text
1. 使用当前正式知识库做理论审计。
2. 检查 AI 交易者项目从数据到交易闭环的知识覆盖。
3. 标出 Trading Engineering 与 AI Engineering 的交界断点。
4. 输出后续知识采集建议。
```

范围外：

```text
1. 不实现 AI 交易者项目。
2. 不接入交易所、券商、行情源或实盘账户。
3. 不训练模型。
4. 不产生具体交易信号、买卖点、仓位、止损止盈或订单。
5. 不把 reviewed/caveat_only 知识升级为 approved。
```

## 涉及组件

```text
codex-expert-kit/rag/indexes/knowledge_items.json
docs/audit/
docs/reports/
docs/index_tasks.md
docs/tasks/README.md
```

## 涉及数据结构

```text
knowledge_id
title
metadata.partition_id
metadata.canonical_node_id
review.review_status
machine_gate.default_guidance
source_evidence
applicability
not_applicable_when
```

## 涉及数据库/存储

本 Phase 不创建数据库，只审计 Phase 42 中已存在的数据库/存储知识是否足以支撑 AI 交易者项目方案。

## 实施步骤

```text
1. 读取正式知识索引，统计知识分区、review_status 和 machine_gate。
2. 设计 AI 交易者项目理论链路。
3. 将链路阶段映射到当前知识库中的代表性知识点。
4. 标出缺失、薄弱、契约不足和运行时不足。
5. 生成审计任务 JSON。
6. 生成断层审计报告。
7. 更新索引和任务状态。
8. 运行 UTF-8/乱码检查。
```

## Definition of Done

```text
1. Phase 44 任务卡存在。
2. docs/index_tasks.md 和 docs/tasks/README.md 已登记 Phase 44。
3. 审计任务 JSON 已生成。
4. 断层审计报告已生成。
5. 报告明确不实现交易项目、不产生实盘建议。
6. 报告明确当前知识库的强项和断层。
7. UTF-8/乱码检查通过。
```

## 测试与验收

```text
python codex-expert-kit/rag/scripts/validate_no_mojibake.py
```

## 风险与回滚

| 风险 | 影响 | 处理 |
| --- | --- | --- |
| 把理论方案误读为实现计划 | 可能错误启动实盘或模型训练 | 报告中明确“只做理论断层审计” |
| 把 AI Engineering 规则当交易本体 | 交易知识污染 | 报告中单独标出 Trading Engineering 断层 |
| reviewed/caveat_only 被误作默认指导 | 治理风险 | 报告保留 review_status 和 machine_gate 区分 |

回滚方式：

```text
删除 docs/audit/phase44_ai_trader_project_gap_audit_task.json
删除 docs/reports/phase44_ai_trader_project_gap_audit_report.md
回滚 docs/index_tasks.md、docs/tasks/README.md 和本任务卡中的 Phase 44 记录。
```
