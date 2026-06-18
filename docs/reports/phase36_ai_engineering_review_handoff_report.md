# Phase 36 AI Engineering 候选知识审计交接报告

## 结论

Phase 36 已完成首批 AI Engineering P0-Core 候选知识采集、来源评分、冲突检查、污染门禁、候选审计包导出和前端/API/MCP 契约验证。

当前不能继续执行 `CEK-TA-187`，原因是本地尚未存在 Phase 36 对应的外部 AI/人工审计结果。按照 CEK-TA 候选知识治理规则，candidate 不等于 formal reviewed，AI 审计包不等于审计结果，不能在没有审计结论的情况下把候选知识转成正式 reviewed 知识。

## 当前状态

```text
CEK-TA-185: done
CEK-TA-186: done
CEK-TA-187: blocked，等待 Phase 36 审计结果
CEK-TA-188: blocked，等待 CEK-TA-187 完成
```

## 已完成交付物

```text
docs/contracts/ai_engineering_gating_scoring_contract.md
docs/contracts/ai_engineering_knowledge_item_policy.md
docs/research/phase36_ai_engineering_p0_collection_matrix.md
docs/research/phase36_ai_engineering_research_task_queue.md
docs/reports/phase36_ai_engineering_collection_report.md
docs/reports/phase36_ai_engineering_candidate_quality_gate.json
docs/audit/phase36_ai_engineering_candidate_audit_package_20260609.json
codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/
```

## 待审计候选范围

本批待审计候选共 113 条，全部位于：

```text
codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/
```

审计包位于：

```text
docs/audit/phase36_ai_engineering_candidate_audit_package_20260609.json
```

## 审计结果输入契约

恢复执行 `CEK-TA-187` 前，需要把外部 AI/人工审计结果写回 `docs/audit/`，并至少包含：

```text
audit_result_id
source_package_id: phase36_ai_engineering_candidate_audit_package_20260609
generated_at
reviewer
global_gate
summary.accepted_for_draft
summary.needs_more_evidence
summary.rejected
decisions[]
```

每个 `decisions[]` 至少包含：

```text
candidate_id
decision: accepted_for_draft | needs_more_evidence | rejected
reason
source_patch_notes
content_patch_notes
boundary_patch_notes
conflict_patch_notes
required_followups
```

## 允许的后续动作

收到审计结果后，才能执行：

```text
1. 将 accepted_for_draft 候选转为 formal knowledge draft。
2. 按审计补丁优化正式知识卡内容、来源、适用边界、冲突审计和 llm_usage_policy。
3. 将正式知识标记为 reviewed。
4. 重建 knowledge_items.json 和 Vue3 formalKnowledgeItems.ts。
5. 跑 MCP/SearchLab/KnowledgeTree 命中、引用、阻断和降级验证。
```

## 禁止动作

```text
1. 不得把未审计候选直接转 reviewed。
2. 不得把 accepted_for_draft 直接转 approved。
3. 不得让 Phase 36 候选进入 MCP/SearchLab 默认指导。
4. 不得把外接项目私有事实、账号信息、策略私有参数写入正式通用知识库。
```

## 已跑验证

```text
python codex-expert-kit/rag/scripts/validate_knowledge_item_schema_v1_1.py
python codex-expert-kit/rag/scripts/validate_knowledge_pollution.py
python codex-expert-kit/rag/scripts/validate_candidate_to_reviewed_workflow.py
python -m pytest codex-expert-kit/mcp/tests/test_external_ai_active_retrieval_protocol.py codex-expert-kit/api/tests/test_candidate_audit_api_contract.py codex-expert-kit/api/tests/test_knowledge_tree_api_contract.py
cd ui && npm run build
```

验证结果均通过。

## 恢复执行入口

当 `docs/audit/` 中出现 Phase 36 审计结果后，恢复执行：

```text
CEK-TA-187 将通过审计的候选沉淀为 formal reviewed 知识并重建索引
CEK-TA-188 验证 MCP/SearchLab/KnowledgeTree 能命中、引用、阻断和降级
```
