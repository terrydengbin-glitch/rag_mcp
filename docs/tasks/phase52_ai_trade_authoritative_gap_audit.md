# Phase 52: AI/Trading Engineering 权威资料缺口复审

## 任务目标

对当前 AI Engineering 与 Trading Engineering 两条主线进行一次外部权威资料对照审计，确认现有 L1/L2/L3、正式知识、候选沉淀和运行时消费边界是否仍有明显缺口。

本 Phase 只做“缺口识别、优先级判断、后续任务建议”，不直接创建正式知识，不提升 `reviewed` 到 `approved`，不改变 MCP 默认指导策略。

## 上游输入

```text
docs/index_tasks.md
docs/tasks/README.md
codex-expert-kit/rag/indexes/knowledge_items.json
docs/reports/phase44_ai_trader_project_gap_audit_report.md
docs/reports/phase46_trading_engineering_regression_eval_report.md
docs/reports/phase47_ai_trade_engineering_alignment_audit_report.md
docs/reports/phase48_tree_alias_schema_backfill_report.md
docs/reports/phase51_knowledge_tree_large_scope_performance_report.md
```

## 下游输出

```text
docs/reports/phase52_ai_trade_authoritative_gap_audit_report.md
docs/index_tasks.md
docs/tasks/README.md
```

下游 Phase 可基于本报告创建新的知识采集任务，但必须重新走候选、审计、补证、reviewed/caveat_only 或 approved 治理流程。

## 输入契约

```text
1. 正式知识以 codex-expert-kit/rag/indexes/knowledge_items.json 为准。
2. 关键词扫描只作为弱信号，不能替代人工/外部资料审计。
3. 权威资料优先级：监管/标准/官方文档 > 研究论文 > 交易所/经纪商/平台官方文档 > vendor/博客案例。
4. 用户显式要求联网搜索时，必须引用来源链接。
```

## 输出契约

报告必须包含：

```text
1. 当前覆盖概况。
2. 外部权威资料对照来源。
3. 已覆盖但需要保持边界的主题。
4. 建议新增或强化的知识点。
5. 不建议新增的主题及原因。
6. 后续 Phase 建议。
7. DoD 与测试结果。
```

## 边界范围

范围内：

```text
1. AI Engineering：模型治理、LLM/Agent 安全、训练/评估/部署/监控、RAG/MCP、记忆层、数据库与存储。
2. Trading Engineering：数据工程、策略工程、回测、Replay/Simulation、Live Execution、Risk Management、Trade Analysis、TCA、订单语义、市场数据授权、系统韧性。
3. 外部权威资料和案例对照。
```

范围外：

```text
1. 不直接生成新知识卡。
2. 不直接创建候选审计包。
3. 不直接修改 Vue3、FastAPI、MCP 运行时代码。
4. 不把 reviewed 知识升级为 approved。
5. 不输出买卖点、仓位、杠杆、止损止盈或实盘执行建议。
```

## 涉及组件

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/
docs/reports/
codex-expert-kit/rag/indexes/knowledge_items.json
```

## 涉及数据结构

```text
KnowledgeItem
canonical_node_id
tree_node_id
review.review_status
machine_gate
source_evidence
llm_usage_policy
```

## 涉及数据库/存储

本 Phase 不引入数据库，不修改存储结构。

## 实施步骤

| ID | 优先级 | 状态 | 任务 | 交付物 |
| --- | --- | --- | --- | --- |
| CEK-TA-514 | P0 | done | 创建 Phase 52 任务卡和任务索引 | `docs/tasks/phase52_ai_trade_authoritative_gap_audit.md` |
| CEK-TA-515 | P0 | done | 扫描本地 AI/Trading 知识覆盖和关键词缺口 | `docs/reports/phase52_ai_trade_authoritative_gap_audit_report.md` |
| CEK-TA-516 | P0 | done | 联网检索权威资料、标准和案例并建立对照判断 | `docs/reports/phase52_ai_trade_authoritative_gap_audit_report.md` |
| CEK-TA-517 | P1 | done | 输出补充知识点建议、优先级和后续 Phase 建议 | `docs/reports/phase52_ai_trade_authoritative_gap_audit_report.md` |

## Definition of Done

```text
1. Phase 52 已登记到 docs/index_tasks.md。
2. Phase 52 已登记到 docs/tasks/README.md。
3. 任务卡包含上下游、契约、边界、DoD 和测试。
4. 审计报告列出权威资料来源和建议补充项。
5. 未直接修改正式知识状态。
6. UTF-8 检查通过，无中文乱码。
```

## 测试与验收

```text
1. PowerShell UTF-8 读取任务卡和报告。
2. 运行 mojibake 检查脚本。
3. 人工确认报告不包含交易建议、阈值建议或实盘执行许可。
```

## 风险与回滚

风险：

```text
1. 权威资料覆盖不等于知识卡可直接入库。
2. 关键词扫描可能漏掉语义等价知识。
3. 部分监管资料有地域边界，不能泛化到所有市场。
```

回滚：

```text
1. 删除 Phase 52 任务卡和报告。
2. 从 docs/index_tasks.md 与 docs/tasks/README.md 移除 Phase 52 入口。
```

## 需要开发者确认的问题

```text
1. 是否按本报告建议创建下一阶段知识采集 Phase。
2. Trade 侧是否优先补“市场操纵/交易监控”还是“Reg NMS/DEA/Market Access”。
3. AI 侧是否优先补“LLM/Agent 安全”还是“AI SBOM/模型供应链”。
```
