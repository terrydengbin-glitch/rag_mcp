# Phase 43 External Project AI Memory Layer 验收报告

生成日期：2026-06-11

## 结论

Phase 43 已完成。

本 Phase 为使用 CEK-TA 的外接 AI 项目沉淀了 External Project AI Memory Layer 知识分支、Memory Contract、Project Memory MCP/API 契约、写入门禁、检索预算、安全治理、adapter 选型和运行时验证机制。

最终入库结果：

```text
正式知识：29 条
review_status=reviewed：29 条
review_mode=caveat_only：29 条
machine_gate.default_guidance=caveat_only：29 条
approved：0 条
default guidance：0 条
hard gate：0 条
```

## 上下游对齐

上游输入：

```text
1. Phase 32 候选到 reviewed 知识批量审计工作流。
2. Phase 35 外部项目 AI 主动检索协议。
3. Phase 40 AI Continuous Learning 与再训练闭环。
4. Phase 41 Hybrid Scoring 与 Qwen3 审计助手知识。
5. Phase 42 Database / Data Contract / Storage Engineering。
```

下游输出：

```text
1. 外接项目 AI IDE / Agent 可复用的 Project Memory Contract。
2. AI Engineering 下 External Project AI Memory Layer 知识子分支。
3. MCP/SearchLab/KnowledgeTree/Vue3 可检索和可审计的 formal reviewed/caveat_only 知识。
4. 后续“外接项目 Project Memory MCP 实现 Phase”可复用的边界和契约。
```

## 知识树与分区

知识分区：

```text
KB_AI_27_PROJECT_MEMORY
```

根节点：

```text
kt.ai_engineering.external_project_memory
```

L3 专题与正式知识数量：

| L3 专题 | 数量 |
| --- | ---: |
| memory_adapter_selection | 3 |
| memory_boundary | 4 |
| memory_evaluation_regression | 2 |
| memory_event_log | 1 |
| memory_mcp_api_contract | 1 |
| memory_retention_privacy | 1 |
| memory_retrieval_context | 3 |
| memory_schema_lifecycle | 7 |
| memory_security_governance | 2 |
| memory_write_gate | 5 |

## 核心边界

Phase 43 只沉淀外接项目 AI Memory Layer 的专业知识和治理规则，不保存外接项目私有记忆。

硬边界：

```text
1. RAG Knowledge 与 Project Memory 必须分离。
2. CEK-TA 只保存 Memory Contract 和治理规则，不保存外接项目私有项目状态。
3. AI 只能 propose memory，不能直接写 active memory。
4. Project Memory 不能进入交易 final gate，也不能生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。
5. PostgreSQL JSONB 是 v0.1 canonical store 建议，pgvector 只是可选 semantic index，不是事实源。
6. 第三方 memory engine 只能作为 adapter，不成为 CEK-TA 核心契约。
7. 所有 Phase 43 知识当前只允许 reviewed/caveat_only，不允许 approved/default guidance/hard gate。
```

## 关键交付物

任务卡和范围：

```text
docs/tasks/phase43_external_project_ai_memory_layer.md
docs/research/phase43_external_project_ai_memory_scope.md
docs/research/phase43_memory_collection_matrix.md
docs/research/phase43_research_task_queue.md
```

契约：

```text
docs/contracts/phase43_project_memory_contract.md
docs/contracts/phase43_project_memory_mcp_api_contract.md
docs/contracts/phase43_memory_write_retrieval_policy.md
docs/contracts/phase43_memory_security_governance_contract.md
docs/contracts/phase43_memory_retention_privacy_contract.md
```

候选、审计与沉淀：

```text
docs/audit/phase43_candidate_audit_package_20260611.json
docs/audit/audit_result_phase43_candidate_audit_package_20260611_strict_v1.json
docs/audit/phase43_supplemental_reaudit_package_20260611.json
docs/audit/audit_result_phase43_supplemental_reaudit_20260611_strict_v2.json
docs/audit/phase43_formal_draft_reviewed_audit_package_20260611.json
docs/audit/audit_result_phase43_formal_draft_reviewed_preparation_20260611_strict_v1.json
docs/reports/phase43_formal_draft_reviewed_import_report.json
```

正式知识与索引：

```text
codex-expert-kit/rag/knowledge/KB_AI_27_PROJECT_MEMORY/
codex-expert-kit/rag/indexes/knowledge_items.json
ui/src/data/formalKnowledgeItems.ts
ui/src/data/phase23Candidates.ts
ui/src/data/knowledgeTreeNodes.ts
```

运行时验证：

```text
codex-expert-kit/rag/scripts/validate_phase43_runtime_linkage.py
docs/reports/phase43_runtime_linkage_validation_report.json
```

## 验收测试

已执行：

```text
python -m py_compile codex-expert-kit/rag/scripts/validate_phase43_runtime_linkage.py codex-expert-kit/rag/scripts/apply_phase43_formal_draft_reviewed_result.py
python codex-expert-kit/rag/scripts/validate_phase43_runtime_linkage.py
python codex-expert-kit/rag/scripts/validate_knowledge_item_schema_v1_1.py
python codex-expert-kit/rag/scripts/validate_candidate_to_reviewed_workflow.py
python codex-expert-kit/rag/scripts/validate_no_mojibake.py
python codex-expert-kit/rag/scripts/validate_knowledge_tree_alignment.py
npm --prefix ui run build
```

测试结果：

```text
Phase 43 runtime linkage：pass，errors=[]。
schema：pass，336 条正式知识，allow=10，caveat_only=326，failure_count=0。
candidate workflow：pass，340 条候选，336 条正式知识，failure_count=0，warning_count=0。
UTF-8/乱码：pass，扫描 996 个文件，failure_count=0。
知识树对齐：pass。
Vue3 build：pass。
```

Vue3 build 仍有 chunk size warning，这是当前前端 fixture 数据量较大导致的体积提醒，不影响本 Phase 验收。

## 运行时验证摘要

CEK-TA-369 已确认：

```text
1. 文件索引可识别 29 条 Phase 43 formal reviewed/caveat_only 知识。
2. KnowledgeTree 可浏览 10 个 External Project AI Memory Layer L3 专题。
3. SearchLab/API 可按根节点和 L3 子节点过滤 Phase 43 知识。
4. MCP 可按 memory_boundary、memory_write_gate、memory_schema_lifecycle、memory_adapter_selection 检索并返回来源。
5. MCP default_guidance_only 不返回 Phase 43 caveat_only 知识，并保留 blocked_results。
6. MCP approve/write 类权限请求会被拒绝。
7. Vue3 fixture 包含 Phase 43 正式知识、候选回链和知识树节点。
```

## 风险与后续建议

剩余风险：

```text
1. Phase 43 目前是知识和契约层，不是 Project Memory MCP 的真实实现。
2. 如果后续实现真实 Project Memory，需要另起 Phase 定义数据库迁移、API 写权限、审计事件和回滚机制。
3. reviewed/caveat_only 不是 approved；若要成为默认指导，必须走单独人工治理任务。
```

建议下一步：

```text
1. 若继续完善外接项目能力，另起“外接项目 Project Memory MCP 实现 Phase”。
2. 若继续扩充知识库，可进入 Phase 37 Trading Engineering 或新增外接项目接入样板。
3. 前端后续可优化大 fixture 的 code splitting，降低 Vue3 build chunk size warning。
```
