# Phase 43: External Project AI Memory Layer

## Phase 目标

为使用 CEK-TA 知识库的外接 AI 项目定义可复用、可审计、可迁移的项目记忆层知识体系。

本 Phase 不是给 CEK-TA 本项目保存项目进度记忆，也不是立刻实现生产数据库或绑定某个第三方 memory vendor。它的目标是沉淀外接项目 AI IDE / Agent 使用的 Memory Contract、MemoryItem schema、Project Memory MCP/API 契约、写入门禁、检索预算、安全治理、adapter 选型和评估方法。

核心原则：

```text
1. Memory is project state, not professional knowledge.
2. CEK-TA defines memory contract, not project-private memory content.
3. RAG Knowledge 与 Project Memory 必须分离。
4. AI 只能 propose memory，不能直接写 active memory。
5. PostgreSQL JSONB 是 v0.1 推荐 canonical memory store；pgvector 仅为可选 retrieval index。
6. 第三方 memory engine 只能作为 adapter，不能成为 CEK-TA 核心契约。
7. Memory retrieval 必须受 project_id、visibility、status、top-k 和 token budget 限制。
8. Memory write 必须有来源、审计、脱敏、冲突检查和投毒防护。
```

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-358 | P0 | done | 创建 Phase 43 任务卡并登记任务索引 | `docs/tasks/phase43_external_project_ai_memory_layer.md`、`docs/index_tasks.md`、`docs/tasks/README.md` | CEK-TA-357 |
| CEK-TA-359 | P0 | done | 定义 External Project AI Memory 范围、知识树节点和 RAG/Memory 边界 | `docs/research/phase43_external_project_ai_memory_scope.md`、`codex-expert-kit/rag/knowledge_tree.md` | CEK-TA-358 |
| CEK-TA-360 | P0 | done | 定义 MemoryItem schema、memory_event_log、memory_links 和 lifecycle contract | `docs/contracts/phase43_project_memory_contract.md` | CEK-TA-359 |
| CEK-TA-361 | P0 | done | 定义 Project Memory MCP/API 只读与受控写入契约 | `docs/contracts/phase43_project_memory_mcp_api_contract.md` | CEK-TA-360 |
| CEK-TA-362 | P0 | done | 定义 memory write gate、retrieval policy、visibility、supersede 和 context budget 规则 | `docs/contracts/phase43_memory_write_retrieval_policy.md` | CEK-TA-361 |
| CEK-TA-363 | P0 | done | 定义 memory poisoning、prompt injection、secret scan、rollback 和 integrity check 安全规则 | `docs/contracts/phase43_memory_security_governance_contract.md` | CEK-TA-362 |
| CEK-TA-364 | P0 | done | 创建 29 条 AI Memory 知识点采集矩阵和 ResearchIngestionTask 队列 | `docs/research/phase43_memory_collection_matrix.md`、`docs/research/phase43_research_task_queue.md` | CEK-TA-363 |
| CEK-TA-365 | P1 | done | 导出 Phase 43 知识范围审计 JSON，先审计边界、schema、任务数量和 adapter 选型口径 | `docs/audit/phase43_external_project_ai_memory_scope_for_audit.json` | CEK-TA-364 |
| CEK-TA-366 | P1 | done | 联网采集 29 条记忆层知识来源，生成候选知识包并运行来源、冲突、乱码和污染门禁 | `codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/`、`docs/research/phase43_candidate_research.md`、`docs/reports/phase43_candidate_generation_report.md` | CEK-TA-365 |
| CEK-TA-367 | P1 | done | 导出 Phase 43 候选 AI 审计包并按 Phase 32 工作流等待审计结果 | `docs/audit/phase43_candidate_audit_package_20260611.json`、`docs/reports/phase43_candidate_audit_package_quality_gate.json` | CEK-TA-366 |
| CEK-TA-368 | P1 | done | 按审计结果补证、回写、沉淀 formal reviewed/caveat_only 知识并重建索引和 Vue3 fixture | `docs/reports/phase43_candidate_audit_import_report.json`、`docs/audit/phase43_supplemental_reaudit_package_20260611.json`、`docs/reports/phase43_formal_draft_reviewed_import_report.json`、`ui/src/data/` | CEK-TA-367 |
| CEK-TA-369 | P1 | done | 验证 MCP/SearchLab/KnowledgeTree 能按 AI Memory 子板块检索、引用、阻断和降级 | `codex-expert-kit/rag/scripts/validate_phase43_runtime_linkage.py`、`docs/reports/phase43_runtime_linkage_validation_report.json` | CEK-TA-368 |
| CEK-TA-370 | P1 | done | 生成 Phase 43 验收报告并更新 Phase 状态 | `docs/reports/phase43_external_project_ai_memory_layer_report.md` | CEK-TA-369 |

## 上游输入

```text
1. Phase 35 外部项目 AI 主动检索协议。
2. Phase 36 AI Engineering 交易 LLM Gating/Scoring 知识扩展。
3. Phase 38 AI 模型平台与交易 Gating/Scoring POC 知识扩展。
4. Phase 40 AI Continuous Learning 与再训练闭环。
5. Phase 41 Hybrid Scoring 与 Qwen3 审计助手知识扩展。
6. Phase 42 Database / Data Contract / Storage Engineering for Trading AI。
7. Phase 32 候选到 reviewed 知识的批量审计工作流。
8. AGENTS.md 中路径 resolver、UTF-8、MCP/API、数据库/存储和知识库规范。
```

## 下游输出

```text
1. 外接 AI 项目可复用的 Project Memory Contract。
2. AI Engineering 下 External Project AI Memory Layer 知识子分支。
3. MemoryItem、memory_event_log、memory_links 的 schema 和生命周期知识。
4. Project Memory MCP/API 的只读与受控写入契约。
5. 记忆写入门禁、检索预算、visibility、supersede、rollback 和安全治理规则。
6. LangGraph、Letta、Mem0、Zep/Graphiti、PostgreSQL JSONB + pgvector adapter 选型边界知识。
7. MCP/SearchLab/KnowledgeTree/Vue3 可检索、可审计、可引用的 formal reviewed 知识。
```

## 建议 L3 专题

Phase 43 默认挂在 `kt.ai_engineering.external_project_memory` 下。

| L3 专题 | canonical node | 说明 |
| --- | --- | --- |
| Memory Boundary | `kt.ai_engineering.external_project_memory.memory_boundary` | RAG Knowledge 与 Project Memory 的职责分离、污染阻断和跨 MCP 调用边界 |
| Memory MCP API Contract | `kt.ai_engineering.external_project_memory.memory_mcp_api_contract` | Project Memory MCP/API 最小权限工具集、读写边界、错误结构和审计事件 |
| Memory Schema Lifecycle | `kt.ai_engineering.external_project_memory.memory_schema_lifecycle` | MemoryItem、6 类 memory_type、状态机、review_status、supersede、deprecated |
| Memory Event Log | `kt.ai_engineering.external_project_memory.memory_event_log` | append-only event log、事件类型、trace_id、source_hash、长期记忆筛选边界 |
| Memory Write Gate | `kt.ai_engineering.external_project_memory.memory_write_gate` | AI propose only、source check、secret scan、visibility check、conflict check |
| Memory Retrieval Context | `kt.ai_engineering.external_project_memory.memory_retrieval_context` | project_id、visibility、status、top-k、token budget、默认注入范围 |
| Memory Security Governance | `kt.ai_engineering.external_project_memory.memory_security_governance` | prompt injection、memory poisoning、private data、rollback、integrity check |
| Memory Retention Privacy | `kt.ai_engineering.external_project_memory.memory_retention_privacy` | retention、deletion、export、privacy minimization、tombstone 和生命周期证据 |
| Memory Adapter Selection | `kt.ai_engineering.external_project_memory.memory_adapter_selection` | PostgreSQL JSONB、pgvector、LangGraph、Letta、Mem0、Zep/Graphiti 选型边界 |
| Memory Evaluation Regression | `kt.ai_engineering.external_project_memory.memory_evaluation_regression` | retrieval regression、stale memory test、permission test、poisoning test |

## 知识点规划

建议首批规划 29 条：P0-Core 22 条，P0-Extended 4 条，P1 3 条。

### P0-Core：22 条

```text
P43-P0-001：RAG Knowledge 与 Project Memory 必须分离。
P43-P0-002：Project Memory 不能污染 CEK-TA 通用专业知识库。
P43-P0-003：CEK-TA 只定义 Memory Contract，不保存外接项目私有记忆。
P43-P0-004：外接 AI IDE 执行任务时应同时查询 CEK-TA MCP 与 Project Memory MCP。
P43-P0-005：第一版 MemoryType 应压缩为 goal / task / decision / artifact / lesson / boundary。
P43-P0-006：process 不应作为长期 MemoryItem，应进入 append-only memory_event_log。
P43-P0-007：future_plan 应并入 task，用 todo / blocked / deferred 表示状态。
P43-P0-008：error 应并入 lesson，并记录 error_cause / fix / prevention。
P43-P0-009：MemoryItem 必须有 source_type、source_event_id 或 source_artifact_ref，并记录 source_hash、source_trust 和 write_origin。
P43-P0-010：MemoryItem 必须支持 supersede，不允许静默覆盖。
P43-P0-011：deprecated memory 只能作为历史参考，不能作为当前事实。
P43-P0-012：AI 只能 propose memory，不能直接写 active memory。
P43-P0-013：长期记忆写入必须通过 source check、secret scan、prompt_injection_scan、memory_poisoning_scan、visibility check、conflict check 和 untrusted_input 标记。
P43-P0-014：不能把所有聊天自动写入长期记忆。
P43-P0-015：用户明确“记住”、项目目标变化、架构决策、失败复盘和审计结论才适合进入长期记忆。
P43-P0-016：普通对话、临时 debug、中间推断和短期日志只能进入 event_log 或不保存。
P43-P0-017：Project Memory MCP/API 必须使用最小权限工具集，写入类工具必须经过 write gate。
P43-P0-018：Memory retention / deletion / export policy 必须显式定义，不能无限期保留所有项目记忆。
P43-P0-019：Memory conflict resolution 必须记录 conflict_status、conflict_reason、resolver 和 resolution_event_id。
P43-P0-020：长期记忆必须防 prompt injection / memory poisoning。
P43-P0-021：MemoryItem 必须可回滚、可完整性校验，并保留审计链。
P43-P0-022：PostgreSQL JSONB 是 v0.1 Project Memory canonical store 推荐基线。
```

### P0-Extended：4 条

```text
P43-P0E-001：Memory recall 必须受 project_id、visibility、status、top-k 和 token budget 限制。
P43-P0E-002：默认上下文只注入 goal、current task、boundary 和 relevant lesson。
P43-P0E-003：长 process log、完整 audit history 和 deprecated memory 必须显式请求。
P43-P0E-004：Memory quality 必须用 retrieval regression set、stale memory test、poisoning test 和 permission test 验证。
```

### P1：3 条

```text
P43-P1-001：第三方 memory engine 只能作为 adapter，不能成为 CEK-TA 核心契约。
P43-P1-002：pgvector 是可选 semantic index，不是事实源，也不是默认必须启用。
P43-P1-003：Adapter portability test 必须验证第三方 memory engine 可迁移回 CEK-TA Memory Contract。
```

## 输入契约

Phase 43 的知识采集任务至少包含：

```text
knowledge_topic_id
target_canonical_node_id
priority: P0 | P0E | P1
claim_type
memory_layer_role: boundary | schema | lifecycle | event_log | write_gate | retrieval | security | adapter | evaluation
expected_sources
source_types
applicability
not_applicable_when
external_project_consumer: ai_ide | agent | memory_mcp | project_adapter
acceptance_gate
```

外接项目调用 Project Memory 时，至少应提供：

```text
project_id
agent_id
task_id
requested_memory_action: search | get | propose | update_status | supersede | list_current_goals | list_active_tasks
requested_memory_type
visibility_scope
top_k
token_budget
source_event_id
source_artifact_ref
trace_id
```

## 输出契约

RAG/MCP 返回 Phase 43 知识时必须包含：

```text
knowledge_id
canonical_node_id
review_status
machine_gate.default_guidance
claim_type
memory_layer_role
llm_usage_policy
source_evidence
conflict_status
freshness
applicability
not_applicable_when
recommended_next_action
```

Project Memory MCP 的建议 tool 契约：

```text
search_memory:
  输入 project_id、query、memory_type、visibility_scope、status、top_k、token_budget
  输出 memory_items、source_refs、retrieval_reason、blocked_items、warnings

get_memory:
  输入 project_id、memory_id
  输出 MemoryItem、audit_trace、visibility_result

propose_memory:
  输入 project_id、memory_type、content、source、relations、security
  输出 memory_candidate_id、status=proposed、review_required=true

update_memory_status:
  输入 project_id、memory_id、target_status、review_record
  输出 updated MemoryItem、audit_event_id

supersede_memory:
  输入 project_id、old_memory_id、new_memory_candidate
  输出 supersede_relation、audit_event_id
```

## MemoryItem v0.1 契约

```json
{
  "memory_id": "mem_...",
  "project_id": "project_...",
  "memory_type": "goal | task | decision | artifact | lesson | boundary",
  "title": "string",
  "summary": "string",
  "content": "string",
  "source": {
    "source_type": "conversation | task_card | audit_report | build_log | code_diff | user_instruction | external_doc",
    "source_event_id": "string",
    "source_artifact_ref": "string",
    "source_hash": "string"
  },
  "relations": {
    "related_task_ids": [],
    "related_decision_ids": [],
    "related_artifact_ids": [],
    "supersedes": []
  },
  "lifecycle": {
    "status": "proposed | active | superseded | deprecated | rejected",
    "valid_from": "datetime",
    "valid_to": null,
    "created_at": "datetime",
    "updated_at": "datetime"
  },
  "review": {
    "review_status": "unreviewed | reviewed | approved",
    "reviewer": "human | rule | ai_assisted",
    "reviewed_at": null
  },
  "security": {
    "visibility": "private | project | team",
    "contains_private_data": false,
    "sanitized": true,
    "untrusted_input": false,
    "poisoning_risk": "low | medium | high",
    "allowed_agents": []
  },
  "retrieval": {
    "retrievable": true,
    "include_by_default": false,
    "top_k_scope": "project | task | agent",
    "last_used_at": null
  }
}
```

## 涉及数据库/存储

本 Phase 只定义外接项目 Project Memory 推荐存储知识，不在 CEK-TA 中引入真实数据库。

v0.1 推荐逻辑表：

```text
memory_items
memory_events
memory_links
```

边界：

```text
1. memory_items 是长期记忆主表。
2. memory_events 是 append-only 事件账本。
3. memory_links 记录 memory 与 task / decision / artifact 的关系。
4. PostgreSQL JSONB 可作为默认 canonical memory store。
5. pgvector 只做可选 semantic retrieval index，不是事实源。
6. 第三方 memory engine 只能作为 adapter，不替代 Memory Contract。
```

## 边界范围

本 Phase 包含：

```text
1. 外接项目 AI Memory Layer 的知识范围、schema、状态机和安全治理。
2. Project Memory MCP/API 的契约设计。
3. PostgreSQL JSONB + 可选 pgvector 的最小可审计记忆后端知识。
4. LangGraph、Letta、Mem0、Zep/Graphiti 等第三方 adapter 选型边界知识。
5. 29 条知识点采集矩阵、审计包、候选知识和 formal reviewed 沉淀流程。
```

本 Phase 不包含：

```text
1. 不给 CEK-TA 本项目实现私有记忆库。
2. 不保存外接项目私有目标、任务、错误、决策或产物内容。
3. 不直接创建生产数据库。
4. 不直接实现 Project Memory MCP server。
5. 不绑定 LangGraph、Letta、Mem0、Zep/Graphiti 中任何一个为唯一标准。
6. 不把 Project Memory 当作 CEK-TA 专业知识。
7. 不允许 AI 自动把所有聊天写入长期记忆。
8. 不允许 LLM 自己写 active memory。
9. 不允许 vector hit 当作事实。
10. 不允许记忆直接喂给 final gate 或交易执行。
```

## 涉及组件

```text
docs/tasks/
docs/research/
docs/contracts/
docs/audit/
docs/reports/
codex-expert-kit/rag/knowledge_tree.md
codex-expert-kit/rag/knowledge_item_schema.md
codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/
codex-expert-kit/rag/knowledge/
codex-expert-kit/rag/indexes/knowledge_items.json
codex-expert-kit/rag/scripts/
codex-expert-kit/mcp/
codex-expert-kit/api/
ui/src/data/
ui/src/views/KnowledgeTreeView.vue
ui/src/views/SearchLab.vue
```

## 涉及数据结构

```text
MemoryItem v0.1
MemoryEvent
MemoryLink
ProjectMemoryMcpRequest
ProjectMemoryMcpResponse
MemoryWriteGateResult
MemoryRetrievalPolicy
MemorySecurityPolicy
MemoryAdapterSelectionRecord
MemoryEvaluationCase
KnowledgeItem v1.1
ResearchIngestionTask
CandidateKnowledge
AI audit package
```

## 实施步骤

```text
1. 创建 Phase 43 任务卡并更新索引。
2. 定义 External Project AI Memory 范围、L3 专题和跨分支边界。
3. 定义 MemoryItem、memory_event_log、memory_links 和生命周期契约。
4. 定义 Project Memory MCP/API 契约。
5. 定义 write gate、retrieval policy、visibility、supersede 和 context budget 规则。
6. 定义 poisoning、prompt injection、secret scan、rollback 和 integrity check 安全规则。
7. 创建 29 条知识点采集矩阵和 ResearchIngestionTask 队列。
8. 导出知识范围审计 JSON。
9. 审计通过后开始联网采集 P0-Core。
10. 生成候选知识、审计包、补证和 formal reviewed。
11. 重建索引和 Vue3 fixture。
12. 验证 MCP/SearchLab/KnowledgeTree 可命中、引用、阻断和降级。
13. 生成 Phase 43 验收报告。
```

## CEK-TA-368 首轮审计处理记录

```text
处理日期：2026-06-11
审计结果：audit_result_phase43_candidate_audit_package_20260611_strict_v1
输入候选：29 条
accepted_for_draft：12 条，仅允许进入后续 draft 队列，不创建 reviewed/approved/default guidance/hard gate。
needs_more_evidence：11 条，已补充 CEK-TA 内部契约、MCP/API、MemoryItem、event log、retention/privacy、pgvector/PostgreSQL 和 adapter portability 来源。
rejected：6 条，原候选保留为 rejected 审计追踪，并用唯一 normalized_claim 标记 rejected original；另创建 6 条修复 slug/normalized_claim 后的重建候选。
二审包：docs/audit/phase43_supplemental_reaudit_package_20260611.json
二审包数量：17 条
二审包质量门禁：pass
运行时边界：本轮未创建 formal reviewed、approved、default guidance 或 hard gate。
```

后续收到二审报告后，继续按 Phase 32 工作流处理：

```text
1. accepted_for_draft 仍不是 reviewed。
2. 只有二审明确 reviewed/caveat_only 允许后，才能另起 formal reviewed 沉淀。
3. reviewed 仍不得自动进入 approved 或默认指导。
4. MCP/SearchLab/KnowledgeTree 只能读取 formal knowledge 索引，不能把 candidate 当默认知识读取。
```

## CEK-TA-368 二审处理记录

```text
处理日期：2026-06-11
审计结果：audit_result_phase43_supplemental_reaudit_20260611_strict_v2
输入候选：17 条补证/重建候选
accepted_for_draft：17 条
needs_more_evidence：0 条
rejected：0 条
blocked：0 条
reviewed_allowed：0 条
approved_allowed：0 条
default_guidance_allowed：0 条
hard_gate_allowed：0 条
导入脚本：codex-expert-kit/rag/scripts/apply_phase43_supplemental_reaudit_result.py
导入报告：docs/reports/phase43_supplemental_reaudit_import_report.json
审计归档：docs/audit/audit_result_phase43_supplemental_reaudit_20260611_strict_v2.json
当前状态：29 条 Phase 43 有效候选均为 accepted_for_draft / ai_passed；6 条 rejected 原始候选仅保留审计追踪。
运行时边界：本轮未创建 formal reviewed、approved、default guidance 或 hard gate。
```

二审后的下一步：

```text
1. 先生成 formal draft，仍不得标记 reviewed。
2. 只有收到单独 reviewed/caveat_only 授权后，才允许创建 formal reviewed 知识。
3. reviewed 仍不得自动进入 approved、default guidance 或 hard gate。
4. formal draft / reviewed 转换必须保留外接项目私有记忆不入 CEK-TA、AI 只能 propose memory、pgvector 不是事实源等边界。
```

## CEK-TA-368 formal draft 沉淀记录

```text
处理日期：2026-06-11
输入范围：Phase 43 中 accepted_for_draft 且位于 ai_passed/formalized 队列的候选。
formal draft 数量：29 条
跳过数量：6 条 rejected 原始候选，仅保留审计追踪。
生成脚本：codex-expert-kit/rag/scripts/promote_phase43_accepted_candidates_to_formal_draft.py
formal knowledge 目录：codex-expert-kit/rag/knowledge/KB_AI_27_PROJECT_MEMORY/
生成报告：docs/reports/phase43_formal_draft_generation_report.json
候选回链：workflow.stage=formalized_draft，workflow.formal_review_status=draft。
正式知识状态：review.review_status=draft。
机器门禁：machine_gate.default_guidance=deny。
索引状态：knowledge_items.json 已重建，正式知识总数为 336。
运行时边界：本轮未创建 reviewed、approved、default guidance 或 hard gate。
```

formal draft 后的下一步：

```text
1. 导出 Phase 43 formal draft reviewed/caveat_only 审计包。
2. 只有外部审计或人工治理明确 reviewed_allowed=true 后，才允许执行 formal reviewed 转换。
3. reviewed 仍不得自动进入 approved、default guidance 或 hard gate。
4. CEK-TA-369 前必须验证 MCP/SearchLab/KnowledgeTree 能命中 AI Memory 子板块，并正确阻断 draft/default guidance。
```

## CEK-TA-368 formal draft reviewed/caveat_only 审计包导出记录

```text
处理日期：2026-06-11
输入范围：29 条 Phase 43 formal draft 知识。
导出脚本：codex-expert-kit/rag/scripts/export_phase43_formal_draft_reviewed_audit_package.py
审计包：docs/audit/phase43_formal_draft_reviewed_audit_package_20260611.json
质量门禁：docs/reports/phase43_formal_draft_reviewed_audit_package_quality_gate.json
缺口报告：docs/reports/phase43_formal_draft_reviewed_preparation_gap_report.json
门禁结果：pass
formal draft 数量：29 条
失败数量：0
允许审计决策：accepted_for_reviewed_caveat_only / needs_more_evidence / rejected / blocked
运行时边界：本轮只导出 reviewed/caveat_only 准备审计包，未创建 reviewed、approved、default guidance 或 hard gate。
```

审计包返回后的处理边界：

```text
1. 只有 decision=accepted_for_reviewed_caveat_only 且 reviewed_allowed=true 的条目才能进入 formal reviewed。
2. formal reviewed 必须设置 machine_gate.default_guidance=caveat_only。
3. approved_allowed/default_guidance_allowed/hard_gate_allowed 必须保持 false。
4. rejected/blocked/needs_more_evidence 不得进入 reviewed。
5. formal reviewed 转换后必须重建 knowledge_items.json、Vue3 fixture，并执行 MCP/SearchLab/KnowledgeTree 联动验证。
```

## CEK-TA-368 formal reviewed/caveat_only 沉淀记录

```text
处理日期：2026-06-11
审计结果：audit_result_phase43_formal_draft_reviewed_preparation_20260611_strict_v1
输入范围：29 条 Phase 43 formal draft 知识。
审计结论：29 条全部 accepted_for_reviewed_caveat_only。
reviewed_allowed：29 条
approved_allowed：0 条
default_guidance_allowed：0 条
hard_gate_allowed：0 条
导入脚本：codex-expert-kit/rag/scripts/apply_phase43_formal_draft_reviewed_result.py
审计归档：docs/audit/audit_result_phase43_formal_draft_reviewed_preparation_20260611_strict_v1.json
导入报告：docs/reports/phase43_formal_draft_reviewed_import_report.json
formal knowledge 目录：codex-expert-kit/rag/knowledge/KB_AI_27_PROJECT_MEMORY/
正式知识状态：review.review_status=reviewed，review.review_mode=caveat_only。
机器门禁：machine_gate.default_guidance=caveat_only，gate_version=1.0.0。
候选回链：workflow.stage=formalized_reviewed，workflow.formal_review_status=reviewed，workflow.formal_review_mode=caveat_only。
索引状态：knowledge_items.json 已重建，正式知识总数为 336，allow=10，caveat_only=326。
Vue3 fixture：formalKnowledgeItems.ts、phase23Candidates.ts、knowledgeTreeNodes.ts 已重建。
运行时边界：未创建 approved，未启用 default guidance，未启用 hard gate；仍禁止保存外接项目私有记忆、真实数据库迁移、第三方 vendor 绑定和交易执行建议。
```

CEK-TA-368 验收测试：

```text
python -m py_compile codex-expert-kit/rag/scripts/apply_phase43_formal_draft_reviewed_result.py
python codex-expert-kit/rag/scripts/build_knowledge_items_index.py
python codex-expert-kit/rag/scripts/build_ui_knowledge_fixture.py
python codex-expert-kit/rag/scripts/build_ui_candidate_fixture.py
python codex-expert-kit/rag/scripts/build_ui_knowledge_tree_fixture.py
python codex-expert-kit/rag/scripts/validate_knowledge_item_schema_v1_1.py
python codex-expert-kit/rag/scripts/validate_candidate_to_reviewed_workflow.py
python codex-expert-kit/rag/scripts/validate_no_mojibake.py
python codex-expert-kit/rag/scripts/validate_knowledge_tree_alignment.py
npm --prefix ui run build
```

测试结果：

```text
schema：pass，336 条正式知识，allow=10，caveat_only=326，failure_count=0。
candidate workflow：pass，340 条候选，336 条正式知识，failure_count=0，warning_count=0。
UTF-8/乱码：pass，扫描 995 个文件，failure_count=0。
知识树对齐：pass。
Vue3 build：pass；仅保留 Vite chunk size warning，不影响构建。
```

## CEK-TA-369 运行时联动验证记录

```text
处理日期：2026-06-11
验证脚本：codex-expert-kit/rag/scripts/validate_phase43_runtime_linkage.py
验证报告：docs/reports/phase43_runtime_linkage_validation_report.json
验证范围：29 条 Phase 43 External Project AI Memory Layer formal reviewed/caveat_only 知识。
文件索引：knowledge_items.json 可识别 29 条 Phase 43 知识。
KnowledgeTree：10 个 External Project AI Memory Layer L3 专题均可浏览。
SearchLab/API：可按根节点和 L3 子节点过滤 Phase 43 知识，状态均为 reviewed/caveat_only。
MCP：可按 memory_boundary、memory_write_gate、memory_schema_lifecycle、memory_adapter_selection 检索并返回来源。
默认指导阻断：default_guidance_only 不返回 Phase 43 caveat_only 知识，并在 blocked_results 中保留阻断记录。
权限阻断：approve/write 类权限请求被拒绝。
Vue3 fixture：formalKnowledgeItems.ts、phase23Candidates.ts、knowledgeTreeNodes.ts 均包含 Phase 43 正式知识和节点。
机器边界补丁：phase43_conversion 已统一补齐 external_project_private_memory_allowed=false、production_database_changes_allowed=false、vendor_activation_allowed=false、trading_execution_allowed=false。
运行时边界：不创建 approved，不启用 default guidance，不启用 hard gate，不保存外接项目私有记忆，不创建生产数据库迁移，不绑定第三方 vendor，不提供交易执行建议。
验证结论：pass。
```

CEK-TA-369 回归测试：

```text
python -m py_compile codex-expert-kit/rag/scripts/validate_phase43_runtime_linkage.py codex-expert-kit/rag/scripts/apply_phase43_formal_draft_reviewed_result.py
python codex-expert-kit/rag/scripts/validate_phase43_runtime_linkage.py
python codex-expert-kit/rag/scripts/build_knowledge_items_index.py
python codex-expert-kit/rag/scripts/build_ui_knowledge_fixture.py
python codex-expert-kit/rag/scripts/build_ui_knowledge_tree_fixture.py
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
Vue3 build：pass；仅保留 Vite chunk size warning，不影响构建。
```

## CEK-TA-370 Phase 验收记录

```text
处理日期：2026-06-11
验收报告：docs/reports/phase43_external_project_ai_memory_layer_report.md
Phase 状态：done
正式知识：29 条 reviewed/caveat_only
默认指导：0 条
approved：0 条
hard gate：0 条
最终边界：Phase 43 只提供 External Project AI Memory Layer 知识和契约，不保存外接项目私有记忆，不实现生产 Project Memory MCP。
```

## Definition of Done

```text
1. Phase 43 已登记到 docs/index_tasks.md。
2. docs/tasks/README.md 已登记 Phase 43。
3. Phase 43 任务卡存在，且包含上下游、契约、边界、DoD、测试。
4. 明确 CEK-TA 不保存外接项目私有记忆。
5. 明确 RAG Knowledge 与 Project Memory 的边界。
6. 明确第一版使用 6 类 MemoryType，而不是 10 类。
7. 明确 process 进入 append-only event log，不进入长期 MemoryItem。
8. 明确 AI 只能 propose memory，不能直接 active。
9. 明确 PostgreSQL JSONB 是 v0.1 推荐 canonical memory store，pgvector 只做可选 retrieval index。
10. 明确第三方 memory engine 只能作为 adapter。
11. 明确 29 条知识点矩阵包含 priority、target_canonical_node_id、source_types、acceptance_gate。
12. 中文文档保持 UTF-8，无乱码。
```

## 测试与验收

文档阶段：

```text
1. 检查 docs/index_tasks.md 包含 Phase 43。
2. 检查 docs/tasks/README.md 包含 Phase 43。
3. 检查 docs/tasks/phase43_external_project_ai_memory_layer.md 包含任务卡必备章节。
4. 运行 UTF-8/乱码门禁。
```

后续采集与入库阶段：

```text
python codex-expert-kit/rag/scripts/validate_knowledge_item_schema_v1_1.py
python codex-expert-kit/rag/scripts/validate_knowledge_pollution.py
python codex-expert-kit/rag/scripts/validate_candidate_to_reviewed_workflow.py
python codex-expert-kit/rag/scripts/validate_no_mojibake.py
python codex-expert-kit/rag/scripts/validate_knowledge_tree_alignment.py
python codex-expert-kit/rag/scripts/validate_phase43_runtime_linkage.py
npm --prefix ui run build
```

## 风险与回滚

| 风险 | 影响 | 处理 |
| --- | --- | --- |
| 把 Project Memory 误当 CEK-TA 通用知识 | 项目私有事实污染通用知识库 | 明确 CEK-TA 只保存 contract 与治理规则，不保存项目事实 |
| 第一版过度设计，引入复杂 graph memory | 成本过高，外接项目难落地 | v0.1 默认 PostgreSQL JSONB + event log；Zep/Graphiti 后置 |
| 自动保存所有聊天 | 记忆污染、隐私泄漏、上下文噪音 | 写入白名单和 AI propose only |
| 长期记忆被 prompt injection 投毒 | 后续 agent 跨会话持续错误 | 加 source check、poisoning risk、secret scan、rollback 和 integrity check |
| 第三方 vendor lock-in | 外接项目迁移困难 | 第三方只作为 adapter，CEK-TA 只定义 Memory Contract |
| 记忆越权注入 final gate | 交易执行风险 | Memory 只能辅助上下文，不得写 final gate 或交易执行 |

回滚方式：

```text
1. 如果 Phase 43 分类不合适，回滚 docs/index_tasks.md、docs/tasks/README.md 和本任务卡新增内容。
2. 如果 knowledge_tree 节点不合适，先修正范围文档和节点映射，不生成候选。
3. 如果后续候选混入项目私有事实，删除候选并记录污染报告，不进入 formal reviewed。
```

## 需要开发者确认的问题

```text
1. 是否确认 Phase 43 新增 AI Engineering 下 External Project AI Memory Layer 子分支。
2. 是否接受首批 29 条作为 Phase 43 知识点范围。
3. 是否确认 v0.1 推荐 PostgreSQL JSONB + append-only event log，pgvector 仅可选。
4. 是否确认 LangGraph、Letta、Mem0、Zep/Graphiti 只作为 adapter 选型知识，不作为核心契约。
5. 是否后续需要另起“外接项目 Project Memory MCP 实现 Phase”，用于真实代码实现。
```

## 状态更新要求

完成每个任务后必须更新：

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase43_external_project_ai_memory_layer.md
```

如果新增契约、研究、审计或报告文档，还必须更新：

```text
docs/index_tasks.md 的文档入口
相关 Phase 报告
```
