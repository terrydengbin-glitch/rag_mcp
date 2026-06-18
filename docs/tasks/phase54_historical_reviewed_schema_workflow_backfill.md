# Phase 54: 历史 reviewed schema 与候选回链全量回填

## Phase 目标

Phase 54 用于承接 Phase 36/38 收口后暴露出的历史门禁欠账：部分已沉淀为 `formal reviewed/caveat_only` 的知识卡缺少 schema v1.1 治理字段，部分候选缺少 Phase 32 候选到正式知识的 workflow 回链字段。

本 Phase 的目标是让：

```text
1. 历史 formal reviewed 知识满足 schema v1.1 机器门禁字段要求。
2. 历史候选与 formal reviewed 知识保持 source_candidate_id、formal_knowledge_id、ai_audit_result_id 等回链一致。
3. MCP/SearchLab/KnowledgeTree/Vue3 读取的正式知识索引能够通过 schema、workflow、乱码和前端构建门禁。
4. 不改变知识 claim、来源、适用边界，不升级 approved，不启用 default guidance 或 hard gate。
```

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-527 | P0 | done | 创建 Phase 54 任务卡、索引入口和回填契约 | `docs/tasks/phase54_historical_reviewed_schema_workflow_backfill.md`、`docs/index_tasks.md`、`docs/tasks/README.md` | CEK-TA-526 |
| CEK-TA-528 | P0 | done | 统计历史 schema v1.1 与 candidate workflow 失败项 | `docs/reports/phase54_backfill_precheck_report.json` | CEK-TA-527 |
| CEK-TA-529 | P0 | done | 实现历史 formal reviewed schema v1.1 字段回填脚本 | `codex-expert-kit/rag/scripts/backfill_phase54_reviewed_schema_v1_1.py`、`docs/reports/phase54_reviewed_schema_backfill_report.json` | CEK-TA-528 |
| CEK-TA-530 | P0 | done | 实现历史 candidate workflow 与 formal knowledge 回链回填脚本 | `codex-expert-kit/rag/scripts/backfill_phase54_candidate_workflow_links.py`、`docs/reports/phase54_candidate_workflow_backfill_report.json` | CEK-TA-529 |
| CEK-TA-531 | P0 | done | 重建正式知识索引、候选 fixture、正式知识 fixture 和知识树范围索引 | `codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/public/data/`、`ui/src/data/` | CEK-TA-530 |
| CEK-TA-532 | P0 | done | 运行 schema/workflow/乱码/知识树/前端构建门禁 | `docs/reports/phase54_validation_report.json` | CEK-TA-531 |
| CEK-TA-533 | P1 | done | 生成 Phase 54 验收报告并更新任务状态 | `docs/reports/phase54_historical_reviewed_schema_workflow_backfill_report.md` | CEK-TA-532 |

## 上游输入

```text
docs/reports/phase34_schema_v1_1_validation_report.json
docs/reports/phase32_candidate_to_reviewed_quality_gate.json
codex-expert-kit/rag/knowledge/**/*.json
codex-expert-kit/rag/candidates/**/*.json
codex-expert-kit/rag/indexes/knowledge_items.json
ui/public/data/formalKnowledgeItems.json
ui/public/data/phase23Candidates.json
ui/src/data/formalKnowledgeItems.ts
ui/src/data/phase23Candidates.ts
```

## 下游输出

```text
1. 历史 schema/workflow 失败项预检查报告。
2. formal reviewed schema v1.1 字段回填报告。
3. candidate workflow 与 formal knowledge 回链回填报告。
4. 重建后的 knowledge_items.json、formalKnowledgeItems、phase23Candidates 和知识树范围索引。
5. schema/workflow/乱码/知识树/前端构建验收报告。
6. Phase 54 验收报告。
```

## 输入契约

### Formal Knowledge 输入

每个 formal knowledge JSON 至少读取：

```text
knowledge_id
schema_version
metadata
content
applicability
source_evidence
source_quality
conflict_audit
review
llm_usage_policy
machine_gate
recommended_extra_sources
```

### Candidate 输入

每个 candidate JSON 至少读取：

```text
candidate_id
proposed_knowledge_id 或 workflow.formal_knowledge_id
review
workflow
status
```

## 输出契约

### Schema Backfill Report

`phase54_reviewed_schema_backfill_report.json` 必须包含：

```text
report_id
generated_at
task_id
scanned_count
updated_count
skipped_count
unsafe_count
updated_items[]
status
```

每个 `updated_items[]` 必须包含：

```text
knowledge_id
source_path
fields_added
fields_normalized
review_status_before
machine_gate_before
machine_gate_after
```

### Candidate Workflow Backfill Report

`phase54_candidate_workflow_backfill_report.json` 必须包含：

```text
report_id
generated_at
task_id
candidate_count
formalized_candidate_count
updated_candidate_count
updated_formal_count
unmatched_count
updated_candidates[]
updated_formal_items[]
status
```

## 边界范围

范围内：

```text
1. 补齐 schema_version=1.1.0 所需的 governance 字段。
2. 补齐 metadata.claim_type、classification_notes。
3. 补齐 llm_usage_policy.required_context、fallback_behavior。
4. 补齐 machine_gate.blocking_reasons、checked_at、gate_version。
5. 将 recommended_extra_sources 规范为 list，并规范 source status。
6. 补齐候选 workflow.stage、queue_group、hidden_from_default_queue、next_action。
7. 根据 formal knowledge review.source_candidate_id 与 candidate_id 回填 formal_knowledge_id。
8. 对已有 AI audit trace 的 formal reviewed 知识补齐 ai_audit_result_id 或 source_candidate_id。
9. 重建索引和 Vue3 fixture。
```

范围外：

```text
1. 不修改知识 content.statement、procedure、applicability、source_evidence 的语义。
2. 不新增专业知识。
3. 不删除候选或正式知识。
4. 不把 reviewed 升级为 approved。
5. 不启用 default guidance。
6. 不启用 hard gate。
7. 不改变 MCP tool 权限。
8. 不改变 Vue3 信息架构。
9. 不引入数据库或新后端框架。
10. 不生成买卖点、仓位、杠杆、止损止盈、风险阈值或实盘执行建议。
```

## 涉及组件

```text
codex-expert-kit/rag/knowledge/
codex-expert-kit/rag/candidates/
codex-expert-kit/rag/indexes/knowledge_items.json
codex-expert-kit/rag/scripts/
ui/public/data/
ui/src/data/
docs/reports/
docs/index_tasks.md
docs/tasks/README.md
```

## 涉及数据结构

```text
KnowledgeItem schema v1.1
CandidateWorkflow
ReviewGovernanceFields
LLMUsagePolicy
MachineGate
RecommendedExtraSource
Phase54BackfillReport
```

## 涉及数据库/存储

不引入数据库，不修改存储架构。继续使用文件化 JSON 正式知识、候选 JSON、聚合索引和 Vue3 fixture。

## 实施步骤

```text
1. 运行现有 schema/workflow 校验，生成 Phase 54 precheck。
2. 实现 formal reviewed schema v1.1 回填脚本。
3. 仅对缺失或格式错误的治理字段做最小回填。
4. 实现 candidate workflow 与 formal knowledge 回链回填脚本。
5. 重建 knowledge_items.json、formalKnowledgeItems、phase23Candidates 和 knowledgeTreeScopeIndex。
6. 重新运行 schema/workflow/乱码/知识树/前端构建门禁。
7. 生成 Phase 54 验收报告。
8. 更新 docs/index_tasks.md、docs/tasks/README.md 和本任务卡状态。
```

## Definition of Done

```text
1. Phase 54 任务卡存在并已写入 docs/index_tasks.md 和 docs/tasks/README.md。
2. precheck 报告存在。
3. schema v1.1 回填脚本存在并生成报告。
4. candidate workflow 回链回填脚本存在并生成报告。
5. knowledge_items.json、formalKnowledgeItems、phase23Candidates 和 knowledgeTreeScopeIndex 已重建。
6. validate_knowledge_item_schema_v1_1.py 通过。
7. validate_candidate_to_reviewed_workflow.py 通过，或报告中只剩明确不可自动修复的人工项。
8. validate_no_mojibake.py 通过。
9. validate_knowledge_tree_alignment.py 通过。
10. npm --prefix ui run build 通过。
11. 不存在 reviewed 被升级为 approved/default guidance/hard gate 的情况。
12. Phase 54 验收报告存在。
13. 任务状态已更新。
```

## 测试与验收

必须执行：

```text
python codex-expert-kit/rag/scripts/validate_knowledge_item_schema_v1_1.py
python codex-expert-kit/rag/scripts/validate_candidate_to_reviewed_workflow.py
python codex-expert-kit/rag/scripts/backfill_phase54_reviewed_schema_v1_1.py
python codex-expert-kit/rag/scripts/backfill_phase54_candidate_workflow_links.py
python codex-expert-kit/rag/scripts/build_knowledge_items_index.py
python codex-expert-kit/rag/scripts/build_ui_knowledge_fixture.py
python codex-expert-kit/rag/scripts/build_ui_candidate_fixture.py
python codex-expert-kit/rag/scripts/build_ui_knowledge_tree_scope_index.py
python codex-expert-kit/rag/scripts/validate_no_mojibake.py
python codex-expert-kit/rag/scripts/validate_knowledge_tree_alignment.py
npm --prefix ui run build
```

如脚本返回失败，必须记录失败原因、剩余条目和下一步，不得把任务标记 done。

## 风险与回滚

风险：

```text
1. 历史知识卡来源格式差异较大，自动回填可能误判 claim_type。
2. 候选与正式知识回链字段可能存在多对一或重建候选，不能盲目覆盖。
3. 生成文件可能覆盖前端 fixture 中的人工调试内容。
```

回滚：

```text
1. 回填报告记录每个被修改文件和字段。
2. 如果 claim_type 或 workflow 推断不确定，脚本必须跳过并写入 unmatched/manual_required。
3. 生成文件可通过源 JSON 重新生成。
4. 如发现误改，按 report 中 source_path 定位并恢复对应字段。
```

## 需要开发者确认的问题

```text
1. 若发现多个候选指向同一 formal knowledge，是否另开人工治理任务处理。
2. 若发现正式知识应升级 approved/default guidance/hard gate，不在本 Phase 内处理，必须另开人工审批任务。
3. 若发现需要修改 schema v1.1 校验规则本身，需另行确认。
```
