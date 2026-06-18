# Phase 23 CEK-TA-102 Candidate To Draft Report

## 报告定位

本报告用于验收 `CEK-TA-102`：将 Phase 23 首批 `accepted_for_draft` 候选转换为正式知识 `draft`，重建 `knowledge_items.json`，并确认 MCP 默认检索不会把 draft 当作 approved 指导返回。

## 上下游

上游输入：

```text
1. codex-expert-kit/rag/candidates/**/*.json
2. docs/reports/phase23_candidate_quality_report.md
3. docs/reports/phase24_candidate_audit_handoff.md
4. codex-expert-kit/rag/ingestion_candidate_schema.md
5. codex-expert-kit/rag/knowledge_item_schema.md
```

下游输出：

```text
1. codex-expert-kit/rag/scripts/convert_candidates_to_knowledge_drafts.py
2. codex-expert-kit/rag/knowledge/**/*.json
3. codex-expert-kit/rag/indexes/knowledge_items.json
4. MCP/SearchLab runtime validation
```

## 转换 Gate

转换脚本只允许满足以下条件的候选进入正式知识 draft：

```text
1. status.ingestion_decision 为 convert_to_knowledge_item 或 convert_to_skill_and_knowledge。
2. conversion_target.target_review_status 必须为 draft。
3. source_refs 非空。
4. applies_when、not_applicable_when、assumptions 非空。
5. conflict_audit.conflict_status 为 none 或 resolved。
6. conflict_audit.approval_allowed 为 true。
7. copyright.stores_full_text 为 false。
8. copyright.stores_long_quote 为 false。
9. 如目标文件已存在且不是 draft，脚本拒绝覆盖。
```

## 转换结果

执行命令：

```text
python codex-expert-kit\rag\scripts\convert_candidates_to_knowledge_drafts.py
```

结果：

```text
converted 7 candidates to draft knowledge items
```

生成的 draft：

```text
codex-expert-kit/rag/knowledge/KB_04_BACKTEST/kb_04_backtest.bias.leakage_overfit_audit_gates.v1.json
codex-expert-kit/rag/knowledge/KB_05_REPLAY_SIMULATION/kb_05_replay_simulation.fill_model.ohlc_same_bar_tp_sl_ambiguity.v1.json
codex-expert-kit/rag/knowledge/KB_06_LIVE_EXECUTION/kb_06_live_execution.order_state_machine.event_rest_position_reconciliation.v1.json
codex-expert-kit/rag/knowledge/KB_07_RISK_MANAGEMENT/kb_07_risk_management.risk_gate.pre_trade_order_risk_controls.v1.json
codex-expert-kit/rag/knowledge/KB_10_RAG_ENGINEERING/kb_10_rag_engineering.retrieval_policy.metadata_citation_freshness_conflict_gate.v1.json
codex-expert-kit/rag/knowledge/KB_11_MCP_ENGINEERING/kb_11_mcp_engineering.tool_contract.readonly_errors_observability.v1.json
codex-expert-kit/rag/knowledge/KB_13_KNOWLEDGE_GOVERNANCE/kb_13_knowledge_governance.status_lifecycle.evidence_conflict_deprecation_gate.v1.json
```

## 索引重建

执行命令：

```text
python codex-expert-kit\rag\scripts\build_knowledge_items_index.py
```

结果：

```text
wrote codex-expert-kit/rag/indexes/knowledge_items.json with 18 items
```

## MCP 回归

执行命令：

```text
python -m pytest codex-expert-kit\mcp\tests\test_server_runtime.py codex-expert-kit\mcp\tests\test_seed_runtime_blocking.py
python -m pytest codex-expert-kit\mcp\tests\test_seed_runtime_validation.py codex-expert-kit\mcp\tests\test_phase20_runtime_quality.py
```

结果：

```text
15 passed
6 passed
```

额外 draft 阻断验证：

```text
query: metadata citation freshness conflict gate
filters.partition_id: KB_10_RAG_ENGINEERING
result_count: 0
blocked_count: 7
blocked_reasons: review_status_draft
returned_review_statuses: []
```

结论：新转换的 draft 已进入正式聚合索引，但 MCP 默认检索不会把 draft 作为默认指导返回。

## 边界确认

```text
1. 本任务未把候选或 draft 标记为 approved。
2. 本任务未开放 MCP 写权限。
3. 本任务未引入数据库或后端服务。
4. 本任务未采集行情、K 线、订单簿或交易原始数据。
5. 转换脚本使用 path resolver，不依赖开发机绝对路径。
6. 中文文档和 JSON 均保持 UTF-8。
```

## DoD 结论

`CEK-TA-102` 已完成。Phase 23 首批候选已转为正式知识 draft，正式索引已重建，MCP 默认检索阻断规则通过回归验证。
