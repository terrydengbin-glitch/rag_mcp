# Phase 31 候选知识 AI 审计结果回写验收报告

## 结论

Phase 31 已完成。

外部 AI 审计结果已结构化保存并回写：

```text
1. 7 条候选知识全部标记为 accepted。
2. 7 条正式 draft 知识全部标记为 reviewed。
3. 所有回写均记录 review.ai_audit 和审计日志。
4. 没有任何条目被升级为 approved。
```

## 回写范围

候选：

```text
codex-expert-kit/rag/candidates/**/*.json
```

正式知识：

```text
codex-expert-kit/rag/knowledge/KB_04_BACKTEST/kb_04_backtest.bias.leakage_overfit_audit_gates.v1.json
codex-expert-kit/rag/knowledge/KB_05_REPLAY_SIMULATION/kb_05_replay_simulation.fill_model.ohlc_same_bar_tp_sl_ambiguity.v1.json
codex-expert-kit/rag/knowledge/KB_06_LIVE_EXECUTION/kb_06_live_execution.order_state_machine.event_rest_position_reconciliation.v1.json
codex-expert-kit/rag/knowledge/KB_07_RISK_MANAGEMENT/kb_07_risk_management.risk_gate.pre_trade_order_risk_controls.v1.json
codex-expert-kit/rag/knowledge/KB_10_RAG_ENGINEERING/kb_10_rag_engineering.retrieval_policy.metadata_citation_freshness_conflict_gate.v1.json
codex-expert-kit/rag/knowledge/KB_11_MCP_ENGINEERING/kb_11_mcp_engineering.tool_contract.readonly_errors_observability.v1.json
codex-expert-kit/rag/knowledge/KB_13_KNOWLEDGE_GOVERNANCE/kb_13_knowledge_governance.status_lifecycle.evidence_conflict_deprecation_gate.v1.json
```

## 关键修正

```text
1. MCP 知识已更新到 2025-11-25 specification，并补充 readOnlyHint 只是 hint，不能替代服务端只读权限控制。
2. RAG 知识已补充 conflict_status/review_status/freshness gate 是 CEK-TA 组合治理规则。
3. Binance 实盘执行知识已强化 Binance USDⓈ-M Futures 边界。
4. pre-trade risk gate 已补充不提供具体仓位、杠杆、止损或策略参数建议。
5. 知识治理生命周期已补充 NIST AI RMF 支撑治理框架，但 CEK-TA 状态机是内部规则。
6. OHLC 同根 TP/SL 已补充 OHLC-only 与 tick/path replay 的边界。
7. 回测偏差知识已保留后续拆分 data leakage 与 multiple testing/PBO 的说明。
```

## 生成物

```text
docs/tasks/phase31_candidate_ai_audit_result_backwrite.md
docs/contracts/candidate_ai_audit_result_backwrite_contract.md
docs/audit/phase31_candidate_ai_audit_result_20260609.json
codex-expert-kit/rag/scripts/apply_candidate_ai_audit_result.py
codex-expert-kit/rag/indexes/knowledge_items.json
ui/src/data/phase23Candidates.ts
ui/src/types.ts
```

## 测试

```text
python codex-expert-kit/rag/scripts/apply_candidate_ai_audit_result.py --dry-run
结果：7 candidates / 7 knowledge 命中，skipped = []

python codex-expert-kit/rag/scripts/apply_candidate_ai_audit_result.py
结果：7 candidates / 7 knowledge 已回写，skipped = []

python codex-expert-kit/rag/scripts/build_knowledge_items_index.py
结果：knowledge_items.json with 18 items

python codex-expert-kit/rag/scripts/build_ui_candidate_fixture.py
结果：phase23Candidates.ts with 7 candidates

python -m pytest codex-expert-kit/api/tests
结果：15 passed

npm run build
结果：passed
```

## 状态校验

```text
候选 review_status:
7 accepted

正式知识 review_status:
7 reviewed

approved 变化:
0
```

## 边界

```text
1. 本 Phase 表示 AI 审计通过并完成 Codex 对齐修正。
2. reviewed 仍不是 approved。
3. 进入默认指导链路必须由后续人工 approved 治理任务明确处理。
```

