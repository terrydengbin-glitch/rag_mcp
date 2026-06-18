# Phase 24 Candidate Audit Handoff

## 报告定位

本报告是 Phase 24 Vue3 候选知识审计工作台生成的 `CEK-TA-102` 交接草案，用于说明当前 Phase 23 首批候选知识是否具备转换为正式知识 `draft` 的条件。

本报告不是 approved 知识，不代表候选知识已经进入 MCP 默认指导。`CEK-TA-102` 执行时仍必须把候选转换为正式知识 `draft`，随后走 `draft -> reviewed -> approved` 状态流，并重建 `knowledge_items.json`、运行 MCP/SearchLab 回归。

## 上游输入

```text
1. codex-expert-kit/rag/candidates/**/*.json
2. ui/src/data/phase23Candidates.ts
3. ui/src/data/candidateHandoff.ts
4. codex-expert-kit/rag/ingestion_candidate_schema.md
5. docs/reports/phase23_candidate_quality_report.md
```

## 下游消费方

```text
target_task_id: CEK-TA-102
target_output:
  - codex-expert-kit/rag/knowledge/**/*.json
  - codex-expert-kit/rag/indexes/knowledge_items.json
  - MCP/SearchLab runtime validation
```

## Handoff 决策规则

```text
accepted_for_draft:
  candidate_status 为 candidate_ready 或 accepted_for_draft
  source_refs 非空
  missing_fields 为空
  blocking_issues 为空
  conversion_target.target_review_status 为 draft

needs_more_evidence:
  缺 source_refs、applies_when、not_applicable_when、assumptions 或其他必填字段
  需要 reviewer 补充证据或人工确认

rejected:
  candidate_status 为 blocked/rejected
  存在 blocking_issues
  不允许进入 CEK-TA-102 draft 转换
```

## 当前批次摘要

```text
candidate_count: 7
accepted_for_draft_recommended: 7
needs_more_evidence: 0
rejected_or_blocked: 0
source_refs_present: 7
blocking_issues_present: 0
missing_fields_present: 0
```

## 候选交接清单

| candidate_id | partition | decision | proposed_knowledge_id | domain | subdomain | sources | conflict | missing_fields | blocking_issues |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cand_20260608_backtest_bias_leakage_overfit_001 | KB_04_BACKTEST | accepted_for_draft | kb_04_backtest.bias.leakage_overfit_audit_gates.v1 | backtest | bias | 4 | resolved | - | - |
| cand_20260608_replay_simulation_ohlc_same_bar_fill_001 | KB_05_REPLAY_SIMULATION | accepted_for_draft | kb_05_replay_simulation.fill_model.ohlc_same_bar_tp_sl_ambiguity.v1 | replay_simulation | fill_model | 4 | none | - | - |
| cand_20260608_live_execution_order_state_reconciliation_001 | KB_06_LIVE_EXECUTION | accepted_for_draft | kb_06_live_execution.order_state_machine.event_rest_position_reconciliation.v1 | live_execution | order_state_machine | 6 | resolved | - | - |
| cand_20260608_risk_management_pre_trade_risk_gates_001 | KB_07_RISK_MANAGEMENT | accepted_for_draft | kb_07_risk_management.risk_gate.pre_trade_order_risk_controls.v1 | risk_management | risk_gate | 4 | resolved | - | - |
| cand_20260608_rag_engineering_metadata_citation_freshness_policy_001 | KB_10_RAG_ENGINEERING | accepted_for_draft | kb_10_rag_engineering.retrieval_policy.metadata_citation_freshness_conflict_gate.v1 | rag_engineering | retrieval_policy | 7 | resolved | - | - |
| cand_20260608_mcp_engineering_tool_contract_readonly_errors_observability_001 | KB_11_MCP_ENGINEERING | accepted_for_draft | kb_11_mcp_engineering.tool_contract.readonly_errors_observability.v1 | mcp_engineering | tool_contract | 6 | resolved | - | - |
| cand_20260608_knowledge_governance_lifecycle_evidence_conflict_deprecation_001 | KB_13_KNOWLEDGE_GOVERNANCE | accepted_for_draft | kb_13_knowledge_governance.status_lifecycle.evidence_conflict_deprecation_gate.v1 | knowledge_governance | status_lifecycle | 7 | resolved | - | - |

## CEK-TA-102 执行要求

```text
1. 每个 accepted_for_draft 候选只能转换为正式知识 draft，不能直接 approved。
2. 转换时必须保留 source_refs/source_quality/conflict_audit/applicability/review/copyright。
3. 转换后必须重建 codex-expert-kit/rag/indexes/knowledge_items.json。
4. MCP 默认检索仍只能返回 reviewed/approved 且安全的正式知识。
5. SearchLab 必须验证 draft 不会作为默认指导返回。
6. 如果人工复审发现冲突、来源不足或适用边界不足，必须退回 needs_more_evidence 或 rejected。
```

## 风险提示

```text
1. 本报告基于前端 fixture 和候选 JSON 的结构化字段生成，不替代人工审计。
2. 当前 7 条候选均为 candidate_ready，不代表 reviewer 已经正式接受。
3. time_sensitive 来源在转换为 draft 时必须保留 accessed_at/version/freshness。
4. 与已有 approved 知识存在 resolved overlap 的候选，正式 draft 应通过 related/duplicate/complement 标注避免重复规则。
```
